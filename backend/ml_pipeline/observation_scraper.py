"""Collect published coffee prices by date, preserving existing observations."""
import re
import json
import time
from datetime import date, datetime, timedelta
import requests
from bs4 import BeautifulSoup
from app.core.database import SessionLocal
from app.models.models import Commodity, PriceHistory, PeriodicPrice
from app.services.history_service import archive_price
from .source_catalog import SOURCES, SUGARCANE_REPORTS

HEADERS = {"User-Agent": "AgroForecast/1.0 (academic price history collector)"}


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


def scrape_and_update_db(days=30, progress=None, commodity_id=None, start_date=None, end_date=None):
    if not 1 <= days <= 365:
        raise ValueError("Phạm vi thu thập từ 1 đến 365 ngày")
    end = date.fromisoformat(str(end_date)) if end_date else date.today()
    start = date.fromisoformat(str(start_date)) if start_date else end - timedelta(days=days - 1)
    days = (end - start).days + 1
    if days < 1 or days > 1827 or end > date.today():
        raise ValueError("Khoảng thu thập phải nằm trong quá khứ, tối đa 5 năm mỗi tác vụ")
    created, skipped, unavailable = 0, 0, 0
    errors = []
    with SessionLocal() as db, requests.Session() as http:
        commodity = db.get(Commodity, commodity_id) if commodity_id else db.query(Commodity).filter(Commodity.code == "COFFEE_ROBUSTA").first()
        if not commodity:
            raise ValueError("Chưa có nông sản COFFEE_ROBUSTA trong danh mục")
        if commodity.code not in SOURCES:
            raise ValueError("Nông sản này chưa có nguồn lịch sử tự động được xác minh")
        if commodity.code != "COFFEE_ROBUSTA":
            return collect_domestic_history(db, http, commodity, start, end, progress)
        if commodity.unit.lower().replace('đ', 'd') != 'vnd/kg':
            raise ValueError("Nguồn giá sử dụng VNĐ/kg; đơn vị nông sản không khớp")
        for index in range(days):
            day = end - timedelta(days=index)
            source = f"https://giacaphe.com/gia-ca-phe-noi-dia-ngay-{day.isoformat()}/"
            existing = db.query(PriceHistory).filter(PriceHistory.commodity_id == commodity.id,
                                                     PriceHistory.record_date == day).first()
            if existing and existing.provenance in ("collected", "reviewed"):
                skipped += 1
            else:
                try:
                    response = http.get(source, headers=HEADERS, timeout=(5, 15))
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
                            if existing:
                                archive_price(db, existing)
                                existing.price = price
                                existing.price_min = existing.price_max = existing.volume = None
                                existing.source = source
                                existing.provenance = "collected"
                            else:
                                db.add(PriceHistory(commodity_id=commodity.id, record_date=day, price=price,
                                                    price_min=None, price_max=None, volume=None, source=source,
                                                    provenance="collected"))
                            db.commit()
                            created += 1
                except SourceAccessRequired as exc:
                    errors.append(f"{day}: {exc}")
                    break
                except (requests.RequestException, ValueError) as exc:
                    errors.append(f"{day}: {exc}")
                    if len(errors) >= 5 or (isinstance(exc, requests.HTTPError) and exc.response.status_code in (401, 403, 429)):
                        break
                time.sleep(0.2)
            if progress:
                progress(index + 1, days)
    message = (f"Cà phê {start} – {end}: ghi nhận {created}, giữ nguyên {skipped} bản ghi; "
               f"{unavailable} ngày không có trang công bố.")
    if errors:
        message += " Lỗi nguồn: " + "; ".join(errors[:5])
    if not created and not skipped and not errors:
        errors.append("Không có quan sát nào trong khoảng yêu cầu")
        message += " Không thu được quan sát; không tạo dữ liệu thay thế."
    return {"count": created, "status": ("PARTIAL" if created or skipped else "FAILED") if errors else "SUCCESS", "message": message}


def collect_domestic_history(db, http, commodity, start, end, progress=None):
    config = SOURCES[commodity.code]
    if config['kind'] == 'periodic':
        from .periodic_history import parse_sugarcane_report
        if commodity.unit.lower().replace('đ','d') != 'vnd/tấn':
            raise ValueError("Nguồn mía sử dụng VNĐ/tấn")
        count, skipped, errors = 0, 0, []
        for index, url in enumerate(SUGARCANE_REPORTS):
            try:
                response = http.get(url, headers=HEADERS, timeout=(10,40))
                response.raise_for_status(); response.encoding='utf-8'
                row = parse_sugarcane_report(response.text, url)
                if row['period_end'] >= start and row['period_start'] <= end:
                    if not db.query(PeriodicPrice).filter(PeriodicPrice.source_url == url).first():
                        db.add(PeriodicPrice(commodity_id=commodity.id, **row)); db.commit(); count += 1
                    else:
                        skipped += 1
            except (requests.RequestException, ValueError) as exc:
                errors.append(str(exc))
            if progress:
                progress(index+1, len(SUGARCANE_REPORTS))
        status = ('PARTIAL' if count or skipped else 'FAILED') if errors else 'SUCCESS'
        return dict(count=count, status=status, message=f"Mía: lưu {count}, giữ nguyên {skipped} báo cáo theo kỳ. "
                    "Bộ Công Thương/Khuyến nông Phú Yên, giá mua và bán riêng; không đưa vào huấn luyện ngày. "
                    "Danh mục đã xác minh hiện có hai kỳ năm 2024." + (' Lỗi: '+'; '.join(errors) if errors else ''))
    if commodity.unit.lower().replace('đ','d') != 'vnd/kg':
        raise ValueError("AGROINFO trả VNĐ/kg, đơn vị nông sản không khớp")
    from .agro_history import fetch_history
    rows = fetch_history(http, config, start, end, progress)
    count, skipped = 0, 0
    for item in rows:
        existing = db.query(PriceHistory).filter(PriceHistory.commodity_id == commodity.id,
                                                PriceHistory.record_date == item['date']).first()
        if existing and existing.provenance in ('collected','reviewed'):
            skipped += 1
            continue
        if existing:
            archive_price(db, existing)
        else:
            existing = PriceHistory(commodity_id=commodity.id, record_date=item['date'])
            db.add(existing)
        existing.price = item['price']
        existing.price_min = existing.price_max = existing.volume = None
        existing.source = item['source']
        existing.provenance = 'collected'
        existing.source_details = json.dumps(item['details'], ensure_ascii=False)
        count += 1
    db.commit()
    return dict(count=count, status='SUCCESS' if rows else 'FAILED',
                message=f"AGROINFO – {config['product']} – {config['market']} – {config['price_type']}: "
                f"ghi nhận {count}, giữ nguyên {skipped} ngày trong {start} – {end}. "
                + ("Ngày không công bố được để trống." if rows else "Nguồn không có dữ liệu đúng mặt hàng/địa bàn trong khoảng này; thử khoảng lịch sử cũ hơn."))
