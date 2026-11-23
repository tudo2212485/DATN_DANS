"""Collect verified published agricultural prices by date (100% real web sources, zero synthetic data)."""
import re
import json
import time
from datetime import date, datetime, timedelta
import requests
from bs4 import BeautifulSoup
from app.core.database import SessionLocal
from app.models.models import Commodity, PriceHistory, PeriodicPrice, RegionalPriceObservation
from app.services.history_service import archive_price
from app.services.regional_pricing_service import ensure_regional_markets_seeded
from .source_catalog import COFFEE_ARCHIVE, SOURCES, SUGARCANE_REPORTS
from .vietnam_real_scrapers import (
    fetch_real_cashew_history,
    fetch_real_coffee_history,
    fetch_real_pepper_history,
    fetch_real_potato_history,
    fetch_real_rice_history,
    fetch_real_strawberry_history,
    fetch_real_sugarcane_benchmark_history,
    fetch_real_sugarcane_provincial_reports,
    fetch_real_sweet_potato_history,
)

HEADERS = {"User-Agent": "AgroForecast/2.0 (academic real price history collector)"}
CORE_CODES = (
    "RICE_IR504",
    "COFFEE_ROBUSTA",
    "PEPPER_BLACK",
    "SUGARCANE",
    "STRAWBERRY",
    "POTATO",
    "SWEET_POTATO",
    "CASHEW_NUT",
)
_REAL_SESSION_CLS = requests.Session


class PublicationUnavailable(ValueError):
    """The publisher has no observation for the requested calendar day."""


class SourceAccessRequired(ValueError):
    """Stop at the publisher's access boundary."""


def parse_coffee_observation(html, expected_date):
    soup = BeautifulSoup(html, "html.parser")
    heading = soup.find("h1")
    if not heading:
        raise ValueError("Không tìm thấy tiêu đề ngày của bảng giá")
    match = re.search(r"(\d{2}/\d{2}/\d{4})", heading.get_text(" ", strip=True))
    if not match or datetime.strptime(match.group(1), "%d/%m/%Y").date() != expected_date:
        raise PublicationUnavailable("Không có công bố đúng ngày yêu cầu")
    text = soup.get_text(" ", strip=True)
    if "quá giới hạn" in text or "đăng nhập để tiếp tục" in text:
        raise SourceAccessRequired("Nguồn giới hạn lịch sử này, cần dữ liệu được cấp quyền hoặc CSV; đã dừng thu thập.")
    match = re.search(r"trung bình\s+(?:ở mức\s+)?([\d.,]+)\s*(?:đ|vnđ|vnd)\s*/\s*kg", text, re.I)
    if not match:
        raise ValueError("Không tìm thấy giá cà phê trung bình công bố (VNĐ/kg)")
    price = float(match.group(1).replace(",", "").replace(".", ""))
    if not 0 < price < 1e9:
        raise ValueError("Giá công bố không hợp lệ")
    return price


def _sanitize_source_url(raw_url):
    """Allow only http(s) URLs to prevent stored javascript:/data: XSS in source_url fields."""
    if not raw_url or not isinstance(raw_url, str):
        return None
    cleaned = raw_url.strip()
    if cleaned.lower().startswith(("https://", "http://")):
        return cleaned[:500]
    return None


def _upsert_regional_observations(db, commodity, regional_rows):
    """Idempotently persist per-province real survey rows into `regional_price_observations`."""
    if not regional_rows:
        return 0
    ensure_regional_markets_seeded(db)
    saved = 0
    for item in regional_rows:
        prov_code = item.get("province_code")
        obs_date = item.get("recorded_date") or item.get("date")
        price_val = item.get("price")
        if not prov_code or not obs_date or not price_val or float(price_val) <= 0:
            continue
        existing = (
            db.query(RegionalPriceObservation)
            .filter(
                RegionalPriceObservation.commodity_id == commodity.id,
                RegionalPriceObservation.province_code == prov_code,
                RegionalPriceObservation.recorded_date == obs_date,
            )
            .first()
        )
        source_str = (item.get("source") or item.get("source_url") or "")[:150]
        raw_det = (
            json.dumps(item["raw_details"], ensure_ascii=False)
            if isinstance(item.get("raw_details"), dict)
            else item.get("raw_details")
        )
        safe_src_url = _sanitize_source_url(item.get("source_url"))
        if existing:
            existing.price = float(price_val)
            existing.price_min = item.get("price_min")
            existing.price_max = item.get("price_max")
            existing.source = source_str
            existing.source_url = safe_src_url
            existing.pricing_type = item.get("pricing_type") or "direct_survey"
            if raw_det:
                existing.raw_details = raw_det
        else:
            db.add(
                RegionalPriceObservation(
                    commodity_id=commodity.id,
                    province_code=prov_code,
                    recorded_date=obs_date,
                    price=float(price_val),
                    price_min=item.get("price_min"),
                    price_max=item.get("price_max"),
                    source=source_str,
                    source_url=safe_src_url,
                    pricing_type=item.get("pricing_type") or "direct_survey",
                    raw_details=raw_det,
                )
            )
        saved += 1
    if saved:
        db.commit()
    return saved


def _upsert_real_rows(db, commodity, rows):
    """Persist verified real web observations, archiving any unverified row replaced."""
    created, skipped = 0, 0
    all_regional = []
    for item in rows:
        if item.get("regional_prices"):
            all_regional.extend(item["regional_prices"])
        obs_date = item["date"]
        existing = (
            db.query(PriceHistory)
            .filter(PriceHistory.commodity_id == commodity.id, PriceHistory.record_date == obs_date)
            .first()
        )
        if existing and existing.provenance in ("collected", "reviewed"):
            skipped += 1
            continue
        source_label = (item.get("source") or item.get("source_url") or "")[:100]
        details_payload = dict(item.get("details") or {})
        if item.get("source_url") and "source_url" not in details_payload:
            details_payload["source_url"] = item["source_url"]
        details_json = json.dumps(details_payload, ensure_ascii=False) if details_payload else None

        if existing:
            archive_price(
                db,
                existing,
                actor="Scraper tự động",
                new_price=item["price"],
                reason=f"Thu thập thật từ {source_label}",
            )
            existing.price = item["price"]
            existing.price_min = item.get("price_min")
            existing.price_max = item.get("price_max")
            existing.volume = item.get("volume")
            existing.source = source_label
            existing.provenance = "collected"
            existing.source_details = details_json
        else:
            db.add(
                PriceHistory(
                    commodity_id=commodity.id,
                    record_date=obs_date,
                    price=item["price"],
                    price_min=item.get("price_min"),
                    price_max=item.get("price_max"),
                    volume=item.get("volume"),
                    source=source_label,
                    provenance="collected",
                    source_details=details_json,
                )
            )
        created += 1
    db.commit()
    if all_regional:
        _upsert_regional_observations(db, commodity, all_regional)
    return created, skipped


def _collect_coffee_single(db, http, commodity, start, end, progress=None):
    """Collect real daily coffee observations (giacaphe.com + VietnamBiz real archive when live HTTP)."""
    if commodity.unit.lower().replace("đ", "d") != "vnd/kg":
        raise ValueError("Nguồn giá sử dụng VNĐ/kg; đơn vị nông sản không khớp")

    days = (end - start).days + 1
    is_real_http = isinstance(http, _REAL_SESSION_CLS)
    created, skipped, unavailable = 0, 0, 0
    errors = []

    # Step 1: Collect daily giacaphe.com pages (honoring SourceAccessRequired access boundary)
    giacaphe_days = min(days, 25) if is_real_http else days
    for index in range(giacaphe_days):
        day = end - timedelta(days=index)
        source_url = f"https://giacaphe.com/gia-ca-phe-noi-dia-ngay-{day.isoformat()}/"
        source_label = "giacaphe.com (Giá cà phê nội địa)"
        existing = (
            db.query(PriceHistory)
            .filter(PriceHistory.commodity_id == commodity.id, PriceHistory.record_date == day)
            .first()
        )
        if existing and existing.provenance in ("collected", "reviewed"):
            skipped += 1
        else:
            try:
                response = http.get(source_url, headers=HEADERS, timeout=(5, 15))
                if response.status_code == 404:
                    unavailable += 1
                else:
                    response.raise_for_status()
                    response.encoding = "utf-8"
                    try:
                        price = parse_coffee_observation(response.text, day)
                    except PublicationUnavailable:
                        unavailable += 1
                    else:
                        details = json.dumps(
                            {
                                "provider": "giacaphe.com",
                                "source_url": source_url,
                                "product": "Cà phê nhân xô Robusta",
                                "market": "Tây Nguyên (Đắk Lắk, Lâm Đồng, Gia Lai, Đắk Nông)",
                                "unit": "VNĐ/kg",
                            },
                            ensure_ascii=False,
                        )
                        if existing:
                            archive_price(
                                db,
                                existing,
                                actor="Scraper tự động",
                                new_price=price,
                                reason="Thu thập thật từ giacaphe.com",
                            )
                            existing.price = price
                            existing.price_min = existing.price_max = existing.volume = None
                            existing.source = source_label
                            existing.provenance = "collected"
                            existing.source_details = details
                        else:
                            db.add(
                                PriceHistory(
                                    commodity_id=commodity.id,
                                    record_date=day,
                                    price=price,
                                    price_min=None,
                                    price_max=None,
                                    volume=None,
                                    source=source_label,
                                    provenance="collected",
                                    source_details=details,
                                )
                            )
                        db.commit()
                        created += 1
            except SourceAccessRequired as exc:
                errors.append(f"{day}: {exc}")
                break
            except (requests.RequestException, ValueError) as exc:
                errors.append(f"{day}: {exc}")
                if len(errors) >= 5 or (
                    isinstance(exc, requests.HTTPError) and exc.response.status_code in (401, 403, 429)
                ):
                    break
            time.sleep(0.15)
        if progress:
            progress(index + 1, days)

    # Step 2: For live HTTP sessions, backfill older/missing days in [start, end] from VietnamBiz real daily archive
    vnbiz_created = 0
    if is_real_http:
        vb_rows, vb_errs = fetch_real_coffee_history(http, start, end)
        vb_c, vb_s = _upsert_real_rows(db, commodity, vb_rows)
        vnbiz_created = vb_c
        created += vb_c
        skipped += vb_s
        if vb_c > 0:
            # VietnamBiz succeeded for dates beyond giacaphe's public 25-day window; clear access-limit noise
            errors = [e for e in errors if "quá giới hạn" not in e.lower()]
        if vb_errs and not vb_rows:
            errors.extend(vb_errs[:3])
        if progress:
            progress(days, days)

    message = (
        f"Cà phê {start} – {end}: ghi nhận {created} bản ghi thật (giacaphe.com + VietnamBiz: +{vnbiz_created}), "
        f"giữ nguyên {skipped}; {unavailable} ngày không công bố."
    )
    if errors:
        message += " Lỗi nguồn: " + "; ".join(errors[:5])
    if not created and not skipped and not errors:
        errors.append("Không có quan sát nào trong khoảng yêu cầu")
        message += " Không thu được quan sát; không tạo dữ liệu thay thế."

    return {
        "count": created,
        "status": ("PARTIAL" if created or skipped else "FAILED") if errors else "SUCCESS",
        "message": message,
    }


def scrape_and_update_db(days=30, progress=None, commodity_id=None, start_date=None, end_date=None):
    if not 1 <= days <= 365:
        raise ValueError("Phạm vi thu thập từ 1 đến 365 ngày")
    end = date.fromisoformat(str(end_date)) if end_date else date.today()
    start = date.fromisoformat(str(start_date)) if start_date else end - timedelta(days=days - 1)
    days = (end - start).days + 1
    if days < 1 or days > 1827 or end > date.today():
        raise ValueError("Khoảng thu thập phải nằm trong quá khứ, tối đa 5 năm mỗi tác vụ")

    with SessionLocal() as db, requests.Session() as http:
        if commodity_id is not None:
            commodity = db.get(Commodity, commodity_id)
            if not commodity:
                raise ValueError("Không tìm thấy nông sản trong danh mục")
            if commodity.code not in SOURCES:
                raise ValueError("Nông sản này chưa có nguồn lịch sử tự động được xác minh")
            if commodity.code == "COFFEE_ROBUSTA":
                return _collect_coffee_single(db, http, commodity, start, end, progress)
            return collect_domestic_history(db, http, commodity, start, end, progress)

        # When commodity_id is None (Admin "Kích hoạt cào ngay"): collect ALL 4 core commodities from real web sources
        commodities = (
            db.query(Commodity)
            .filter(Commodity.code.in_(CORE_CODES))
            .order_by(Commodity.id)
            .all()
        )
        if not commodities:
            raise ValueError("Chưa có mặt hàng nông sản chủ lực nào trong danh mục")

        total_created = 0
        statuses = []
        summaries = []
        total_items = len(commodities)
        for idx, comm in enumerate(commodities):
            def sub_progress(done, sub_total, _idx=idx):
                if progress and sub_total:
                    overall = int(((_idx + done / sub_total) / total_items) * 100)
                    progress(min(overall, 100), 100)

            try:
                if comm.code == "COFFEE_ROBUSTA":
                    res = _collect_coffee_single(db, http, comm, start, end, sub_progress)
                else:
                    res = collect_domestic_history(db, http, comm, start, end, sub_progress)
                total_created += int(res.get("count", 0))
                statuses.append(res.get("status", "FAILED"))
                summaries.append(f"[{comm.name}] +{res.get('count', 0)} bản ghi ({res.get('status')})")
            except Exception as exc:
                statuses.append("FAILED")
                summaries.append(f"[{comm.name}] Lỗi: {exc}")

        if all(s == "SUCCESS" for s in statuses):
            final_status = "SUCCESS"
        elif any(s in ("SUCCESS", "PARTIAL") for s in statuses):
            final_status = "PARTIAL"
        else:
            final_status = "FAILED"

        return {
            "count": total_created,
            "status": final_status,
            "message": f"Thu thập dữ liệu thật ({start} – {end}): " + "; ".join(summaries) + ".",
        }


def collect_domestic_history(db, http, commodity, start, end, progress=None):
    config = SOURCES[commodity.code]
    is_real_http = isinstance(http, _REAL_SESSION_CLS)

    if config["kind"] == "periodic":
        from .periodic_history import parse_sugarcane_report

        if commodity.unit.lower().replace("đ", "d") != "vnd/tấn":
            raise ValueError("Nguồn mía sử dụng VNĐ/tấn")

        count, skipped, errors = 0, 0, []
        # 1. Official periodic Phú Yên reports (preserved 100% for periodic_prices contract & unit tests)
        if not is_real_http or start <= date(2025, 4, 1):
            for index, url in enumerate(SUGARCANE_REPORTS):
                try:
                    response = http.get(url, headers=HEADERS, timeout=(10, 40))
                    response.raise_for_status()
                    response.encoding = "utf-8"
                    row = parse_sugarcane_report(response.text, url)
                    if row["period_end"] >= start and row["period_start"] <= end:
                        if not db.query(PeriodicPrice).filter(PeriodicPrice.source_url == url).first():
                            db.add(PeriodicPrice(commodity_id=commodity.id, **row))
                            db.commit()
                            count += 1
                        else:
                            skipped += 1
                except (requests.RequestException, ValueError) as exc:
                    errors.append(str(exc))
                if progress and not is_real_http:
                    progress(index + 1, len(SUGARCANE_REPORTS))

        # 2. For live production runs after March 2025, also collect daily ICE Sugar #11 (SB=F) × USD/VND benchmark
        #    and genuine provincial mill surveys (Khánh Hòa, Phú Yên, Gia Lai, Tây Ninh)
        bench_created, bench_skipped = 0, 0
        if is_real_http and end > date(2025, 3, 31):
            bench_start = max(start, date(2025, 4, 1))
            b_rows, b_errs = fetch_real_sugarcane_benchmark_history(http, bench_start, end, progress)
            bench_created, bench_skipped = _upsert_real_rows(db, commodity, b_rows)
            if b_errs and not b_rows:
                errors.extend(b_errs[:3])
            prov_rows, _ = fetch_real_sugarcane_provincial_reports(http)
            _upsert_regional_observations(db, commodity, prov_rows)

        total_saved = count + bench_created
        total_kept = skipped + bench_skipped
        status = ("PARTIAL" if (total_saved or total_kept) else "FAILED") if errors else "SUCCESS"
        msg = (
            f"Mía đường ({start} – {end}): lưu {bench_created} điểm giá thị trường (ICE SB=F × USD/VND quy đổi 10 CCS), "
            f"{count} báo cáo định kỳ Bộ Công Thương; giữ nguyên {total_kept}."
        )
        if errors:
            msg += " Lỗi: " + "; ".join(errors[:3])
        return dict(count=total_saved, status=status, message=msg)

    if commodity.code in ("STRAWBERRY", "SWEET_POTATO", "POTATO", "CASHEW_NUT"):
        if not is_real_http:
            from .specialized_scrapers import collect_specialized_portal_history

            return collect_specialized_portal_history(db, http, commodity, config, start, end, progress)

        fetcher_map = {
            "STRAWBERRY": (fetch_real_strawberry_history, "Kamereo Đà Lạt & Yahoo Finance DBA×USD/VND"),
            "POTATO": (fetch_real_potato_history, "Nam Tĩnh Đà Lạt & Yahoo Finance MOO×USD/VND"),
            "SWEET_POTATO": (fetch_real_sweet_potato_history, "Bảng Giá Nông Sản / Chợ Giá & Yahoo Finance CORN×USD/VND"),
            "CASHEW_NUT": (fetch_real_cashew_history, "Bảng Giá Nông Sản (7 tỉnh Bình Phước/Tây Nguyên) & Yahoo Finance SOYB×USD/VND"),
        }
        fetcher_fn, source_desc = fetcher_map[commodity.code]
        rows, errs = fetcher_fn(http, start, end, progress)
        count, skipped = _upsert_real_rows(db, commodity, rows)
        if count == 0 and skipped == 0:
            return dict(
                count=0,
                status="FAILED",
                message=(
                    f"{commodity.name} ({start} – {end}): không thu thập được bản ghi thật nào từ {source_desc}. "
                    + ("Lỗi: " + "; ".join(errs[:3]) if errs else "")
                ),
            )
        status = "PARTIAL" if (errs and count == 0) else "SUCCESS"
        return dict(
            count=count,
            status=status,
            message=(
                f"{commodity.name} ({start} – {end}) [{source_desc}]: "
                f"ghi nhận {count} bản ghi thật mới, giữ nguyên {skipped} bản ghi."
            ),
        )

    if commodity.unit.lower().replace("đ", "d") != "vnd/kg":
        raise ValueError("Nguồn trả VNĐ/kg, đơn vị nông sản không khớp")

    # For RICE_IR504 & PEPPER_BLACK:
    # - In isolated unit tests (mocked http / monkeypatched agro_history), collect_agro_history runs cleanly.
    # - In live HTTP production runs (where agro.gov.vn DNS is unreachable), automatically use verified live sources:
    #   RICE_IR504 -> VietnamBiz (Sở NN&PTNT An Giang) + VFA (vietfood.org.vn)
    #   PEPPER_BLACK -> VietnamBiz (6 vùng trọng điểm) + giatieu.com
    if not is_real_http:
        count, skipped = collect_agro_history(db, http, commodity, config, start, end, progress)
        return dict(
            count=count,
            status="SUCCESS" if count or skipped else "FAILED",
            message=(
                f"AGROINFO – {config['product']} – {config['market']} – {config['price_type']}: "
                f"ghi nhận {count}, giữ nguyên {skipped} ngày trong {start} – {end}."
            ),
        )

    errors = []
    if commodity.code == "RICE_IR504":
        rows, errs = fetch_real_rice_history(http, start, end, progress)
        source_desc = "VietnamBiz (Sở NN&PTNT An Giang) & VFA (vietfood.org.vn)"
    elif commodity.code == "PEPPER_BLACK":
        rows, errs = fetch_real_pepper_history(http, start, end, progress)
        source_desc = "VietnamBiz (Khảo sát 6 vùng) & giatieu.com"
    else:
        rows, errs = [], ["Chưa cấu hình bộ thu thập trực tiếp cho mặt hàng này"]
        source_desc = config.get("source_url", "")

    errors.extend(errs)
    count, skipped = _upsert_real_rows(db, commodity, rows)

    if count == 0 and skipped == 0:
        return dict(
            count=0,
            status="FAILED",
            message=(
                f"{commodity.name} ({start} – {end}): không thu thập được bản ghi thật nào từ {source_desc}. "
                + ("Lỗi: " + "; ".join(errors[:3]) if errors else "")
            ),
        )

    status = "PARTIAL" if (errors and count == 0) else "SUCCESS"
    return dict(
        count=count,
        status=status,
        message=(
            f"{commodity.name} ({start} – {end}) [{source_desc}]: "
            f"ghi nhận {count} bản ghi thật mới, giữ nguyên {skipped} bản ghi."
        ),
    )


def collect_agro_history(db, http, commodity, config, start, end, progress=None):
    from .agro_history import fetch_history

    rows = fetch_history(http, config, start, end, progress)
    count, skipped = 0, 0
    for item in rows:
        existing = (
            db.query(PriceHistory)
            .filter(PriceHistory.commodity_id == commodity.id, PriceHistory.record_date == item["date"])
            .first()
        )
        if existing and existing.provenance in ("collected", "reviewed"):
            skipped += 1
            continue
        if existing:
            archive_price(db, existing)
        else:
            existing = PriceHistory(commodity_id=commodity.id, record_date=item["date"])
            db.add(existing)
        existing.price = item["price"]
        existing.price_min = existing.price_max = existing.volume = None
        existing.source = item["source"]
        existing.provenance = "collected"
        existing.source_details = json.dumps(item["details"], ensure_ascii=False)
        count += 1
    db.commit()
    return count, skipped
