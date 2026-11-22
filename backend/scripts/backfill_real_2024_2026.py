# -*- coding: utf-8 -*-
"""
Backfill 100% Real Historical Prices (2024-01-01 -> 2026-11-21) with Monthly Checkpointed UPSERT.

Usage examples:
  python scripts/backfill_real_2024_2026.py --commodity SUGARCANE --start 2024-01-01 --end 2026-11-21
  python scripts/backfill_real_2024_2026.py --commodity COFFEE_ROBUSTA --start 2024-01-01 --end 2026-11-21
  python scripts/backfill_real_2024_2026.py --commodity PEPPER_BLACK --start 2024-01-01 --end 2026-11-21
  python scripts/backfill_real_2024_2026.py --commodity RICE_IR504 --start 2024-01-01 --end 2026-11-21
  python scripts/backfill_real_2024_2026.py --commodity ALL --start 2024-01-01 --end 2026-11-21 --apply-cleanup

Security & Quality Contracts (SEC-03, SEC-06):
  - 100% strict TLS (`verify=True`) and `ALLOWED_SCRAPER_DOMAINS` SSRF allowlist.
  - Zero synthetic prices, zero random numbers, zero DB interpolation on weekends/holidays.
  - Polite delay (`--sleep 0.35`), explicit timeouts, max 2 retries with exponential backoff.
  - Outlier Guard: per-commodity valid price bounds + >20% 1-day anomaly spike rejection with logging.
  - Monthly checkpointed UPSERT into `price_history` (`provenance='collected'`) & `regional_price_observations`
    (`pricing_type='direct_survey'`), allowing seamless resume after interruption.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import date, datetime, timedelta
import json
import logging
from pathlib import Path
import re
import sys
import time
from typing import Callable, Dict, List, Optional, Tuple

import requests
from bs4 import BeautifulSoup
from sqlalchemy import func

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.core.database import SessionLocal
from app.models.models import Commodity, PriceHistory, RegionalPriceObservation
from ml_pipeline.observation_scraper import _sanitize_source_url, _upsert_regional_observations
from ml_pipeline.vietnam_real_scrapers import (
    ALLOWED_SCRAPER_DOMAINS,
    HEADERS,
    _collect_vnbiz_article_links,
    _fetch_vfa_weekly_rice,
    _is_safe_external_url,
    _parse_vn_number,
    _parse_vnbiz_coffee_article,
    _parse_vnbiz_pepper_article,
    _parse_vnbiz_rice_article,
    fetch_real_sugarcane_benchmark_history,
    fetch_real_sugarcane_provincial_reports,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("backfill_real_2024_2026")

# Reasonable 2024-2026 price corridors (Outlier Guard)
PRICE_BOUNDS: Dict[str, Tuple[float, float]] = {
    "COFFEE_ROBUSTA": (55_000.0, 145_000.0),
    "PEPPER_BLACK": (70_000.0, 185_000.0),
    "RICE_IR504": (4_500.0, 11_000.0),
    "SUGARCANE": (800_000.0, 1_800_000.0),
}

MAX_DAILY_JUMP_RATIO = 0.20  # Reject >20% 1-day isolated OCR/parse spikes


def _http_get_with_retry(
    http: requests.Session,
    url: str,
    allowed_domains: Tuple[str, ...] = ALLOWED_SCRAPER_DOMAINS,
    max_retries: int = 2,
    timeout: Tuple[int, int] = (8, 15),
) -> Optional[requests.Response]:
    """Strict HTTPS GET with SSRF allowlist check and exponential backoff retry (max 2 retries)."""
    if not _is_safe_external_url(url, allowed_domains):
        logger.warning("Blocked disallowed URL: %s", url)
        return None
    for attempt in range(max_retries + 1):
        try:
            resp = http.get(url, headers=HEADERS, timeout=timeout, verify=True)
            if resp.status_code == 200:
                resp.encoding = "utf-8"
                return resp
            if resp.status_code in (429, 500, 502, 503, 504) and attempt < max_retries:
                time.sleep(1.0 * (2 ** attempt))
                continue
            return None
        except requests.RequestException as exc:
            if attempt < max_retries:
                time.sleep(1.0 * (2 ** attempt))
            else:
                logger.warning("HTTP error (%s) for %s", type(exc).__name__, url)
                return None
    return None


def _has_verified_source_url(row: PriceHistory) -> bool:
    if row.provenance != "collected":
        return False
    if row.source and _is_safe_external_url(row.source):
        return True
    if row.source_details:
        try:
            details = json.loads(row.source_details)
            src_url = details.get("source_url")
            if src_url and _is_safe_external_url(src_url):
                return True
        except Exception:
            pass
    return False


def _load_existing_collected_dates(db, commodity_id: int) -> Dict[date, float]:
    rows = (
        db.query(PriceHistory)
        .filter(
            PriceHistory.commodity_id == commodity_id,
            PriceHistory.provenance == "collected",
        )
        .order_by(PriceHistory.record_date.asc())
        .all()
    )
    return {r.record_date: float(r.price) for r in rows if _has_verified_source_url(r)}


def _filter_outliers(
    code: str,
    records: List[Dict],
    anchor_prices: Dict[date, float],
) -> Tuple[List[Dict], int]:
    """Enforce bounds + >20% short-gap jump outlier guard."""
    lo, hi = PRICE_BOUNDS[code]
    valid_bounds = []
    rejected = 0
    for rec in sorted(records, key=lambda x: x["date"]):
        p = float(rec["price"])
        if not (lo <= p <= hi):
            logger.warning("[%s] Outlier bounds drop %s: price=%s (expected %s..%s)", code, rec["date"], p, lo, hi)
            rejected += 1
            continue
        valid_bounds.append(rec)

    # Combine with existing anchors to detect isolated >20% 1-day jump spikes
    accepted: List[Dict] = []
    known: Dict[date, float] = dict(anchor_prices)
    for idx, rec in enumerate(valid_bounds):
        d = rec["date"]
        p = float(rec["price"])
        prior_dates = [kd for kd in known.keys() if kd < d]
        if prior_dates:
            prev_d = max(prior_dates)
            prev_p = known[prev_d]
            gap_days = (d - prev_d).days
            jump = abs(p - prev_p) / prev_p if prev_p > 0 else 0.0
            if gap_days <= 3 and jump > MAX_DAILY_JUMP_RATIO:
                # Check if next day confirms a genuine regime shift vs isolated spike
                confirmed_shift = False
                if idx + 1 < len(valid_bounds):
                    nxt = valid_bounds[idx + 1]
                    if (nxt["date"] - d).days <= 3 and abs(float(nxt["price"]) - p) / p <= 0.08:
                        confirmed_shift = True
                if not confirmed_shift:
                    logger.warning(
                        "[%s] Outlier >20%% 1-day jump drop %s: %s -> %s (gap=%dd, jump=%.1f%%) url=%s",
                        code,
                        d,
                        prev_p,
                        p,
                        gap_days,
                        jump * 100.0,
                        rec.get("source_url"),
                    )
                    rejected += 1
                    continue
        accepted.append(rec)
        known[d] = p

    return accepted, rejected


def _upsert_month_batch(
    db,
    commodity: Commodity,
    records: List[Dict],
) -> Tuple[int, int, int]:
    """Checkpointed monthly UPSERT into `price_history` and `regional_price_observations`."""
    inserted, updated, reg_saved = 0, 0, 0
    all_regional: List[Dict] = []

    for rec in records:
        safe_url = _sanitize_source_url(rec.get("source_url"))
        if not safe_url or not _is_safe_external_url(safe_url):
            continue
        details = dict(rec.get("details") or {})
        details["source_url"] = safe_url
        details_json = json.dumps(details, ensure_ascii=False)
        src_name = (rec.get("source") or safe_url)[:100]

        existing = (
            db.query(PriceHistory)
            .filter(
                PriceHistory.commodity_id == commodity.id,
                PriceHistory.record_date == rec["date"],
            )
            .first()
        )
        if existing:
            existing.price = float(rec["price"])
            if rec.get("price_min") is not None:
                existing.price_min = float(rec["price_min"])
            if rec.get("price_max") is not None:
                existing.price_max = float(rec["price_max"])
            existing.source = src_name
            existing.provenance = "collected"
            existing.source_details = details_json
            updated += 1
        else:
            db.add(
                PriceHistory(
                    commodity_id=commodity.id,
                    record_date=rec["date"],
                    price=float(rec["price"]),
                    price_min=float(rec["price_min"]) if rec.get("price_min") is not None else None,
                    price_max=float(rec["price_max"]) if rec.get("price_max") is not None else None,
                    source=src_name,
                    provenance="collected",
                    source_details=details_json,
                )
            )
            inserted += 1

        for reg in rec.get("regional_prices") or []:
            reg_copy = dict(reg)
            reg_copy["source_url"] = _sanitize_source_url(reg_copy.get("source_url") or safe_url)
            all_regional.append(reg_copy)

    db.commit()
    if all_regional:
        reg_saved = _upsert_regional_observations(db, commodity, all_regional)
    return inserted, updated, reg_saved


def _backfill_sugarcane(
    http: requests.Session,
    db,
    commodity: Commodity,
    start: date,
    end: date,
    sleep_sec: float,
    force: bool,
) -> Dict:
    logger.info("=== [SUGARCANE] Fetching Yahoo Finance ICE SB=F x VND=X (%s -> %s) ===", start, end)
    rows, errors = fetch_real_sugarcane_benchmark_history(http, start, end)
    existing_anchors = _load_existing_collected_dates(db, commodity.id)
    filtered, dropped = _filter_outliers("SUGARCANE", rows, {} if force else existing_anchors)

    # Monthly checkpointed UPSERT
    by_month: Dict[Tuple[int, int], List[Dict]] = defaultdict(list)
    for rec in filtered:
        by_month[(rec["date"].year, rec["date"].month)].append(rec)

    tot_ins, tot_upd, tot_reg = 0, 0, 0
    for ym in sorted(by_month.keys()):
        ins, upd, reg = _upsert_month_batch(db, commodity, by_month[ym])
        tot_ins += ins
        tot_upd += upd
        tot_reg += reg

    # Refresh verified provincial sugarcane direct surveys (Khánh Hòa, Phú Yên, Gia Lai, Tây Ninh)
    prov_rows, prov_errs = fetch_real_sugarcane_provincial_reports(http)
    if prov_rows:
        tot_reg += _upsert_regional_observations(db, commodity, prov_rows)
    errors.extend(prov_errs)
    logger.info(
        "[SUGARCANE] Done: fetched=%d, inserted=%d, updated=%d, dropped=%d, provincial=%d, errors=%d",
        len(rows),
        tot_ins,
        tot_upd,
        dropped,
        tot_reg,
        len(errors),
    )
    return {"inserted": tot_ins, "updated": tot_upd, "dropped": dropped, "regional": tot_reg, "errors": errors}


def _backfill_vnbiz_commodity(
    http: requests.Session,
    db,
    commodity: Commodity,
    code: str,
    sources_cfg: List[Tuple[str, str, Tuple[str, ...], int]],
    parser: Callable[[str, str], Optional[Dict]],
    start: date,
    end: date,
    sleep_sec: float,
    force: bool,
    extra_rows_fn: Optional[Callable[[], List[Dict]]] = None,
) -> Dict:
    logger.info("=== [%s] Discovering archive URLs (%s -> %s) ===", code, start, end)
    link_map: Dict[date, str] = {}
    for first_u, paged_tpl, kws, max_pages in sources_cfg:
        found = _collect_vnbiz_article_links(
            http,
            first_page_url=first_u,
            paged_url_template=paged_tpl,
            slug_keyword=kws[0],
            slug_keywords=kws,
            start=start,
            end=end,
            max_pages=max_pages,
            sleep_sec=max(0.15, sleep_sec * 0.5),
        )
        for art_day, art_url in found:
            existing = link_map.get(art_day)
            if existing is None or ("hom-nay" in art_url.lower() and "hom-nay" not in existing.lower()):
                link_map[art_day] = art_url
        logger.info("[%s] After %s -> total unique dates discovered: %d", code, first_u, len(link_map))

    existing_collected = _load_existing_collected_dates(db, commodity.id)
    # Group candidate URLs by (year, month) for checkpointed monthly UPSERT
    by_month: Dict[Tuple[int, int], List[Tuple[date, str]]] = defaultdict(list)
    for d, u in sorted(link_map.items()):
        if not force and d in existing_collected:
            continue
        by_month[(d.year, d.month)].append((d, u))

    logger.info(
        "[%s] Already collected=%d | To fetch=%d across %d months",
        code,
        len(existing_collected),
        sum(len(v) for v in by_month.values()),
        len(by_month),
    )

    tot_ins, tot_upd, tot_drop, tot_reg = 0, 0, 0, 0
    errors: List[str] = []

    for ym in sorted(by_month.keys()):
        month_links = by_month[ym]
        month_parsed: List[Dict] = []
        for art_day, url in month_links:
            resp = _http_get_with_retry(http, url, ("vietnambiz.vn",))
            if resp is not None:
                parsed = parser(resp.text, url)
                if parsed and start <= parsed["date"] <= end:
                    month_parsed.append(parsed)
            else:
                errors.append(f"{art_day}: HTTP fail")
            time.sleep(sleep_sec)

        filtered, dropped = _filter_outliers(code, month_parsed, existing_collected)
        ins, upd, reg = _upsert_month_batch(db, commodity, filtered)
        for rec in filtered:
            existing_collected[rec["date"]] = float(rec["price"])
        tot_ins += ins
        tot_upd += upd
        tot_drop += dropped
        tot_reg += reg
        logger.info(
            "  [%s %04d-%02d] links=%2d parsed=%2d saved=+%d/upd=%d drop=%d reg=%d",
            code,
            ym[0],
            ym[1],
            len(month_links),
            len(month_parsed),
            ins,
            upd,
            dropped,
            reg,
        )

    # Optional supplementary source (e.g., VFA 7-province weekly bulletins for RICE_IR504)
    if extra_rows_fn is not None:
        extra_rows = extra_rows_fn()
        logger.info("[%s] Supplementary source fetched %d records", code, len(extra_rows))
        # Always upsert regional observations from VFA, and fill any missing daily price_history dates
        reg_batch: List[Dict] = []
        missing_daily: List[Dict] = []
        for rec in extra_rows:
            for r_item in rec.get("regional_prices") or []:
                reg_batch.append(r_item)
            if rec["date"] not in existing_collected:
                missing_daily.append(rec)
        if missing_daily:
            filtered_extra, drop_extra = _filter_outliers(code, missing_daily, existing_collected)
            ins, upd, reg = _upsert_month_batch(db, commodity, filtered_extra)
            tot_ins += ins
            tot_upd += upd
            tot_drop += drop_extra
            tot_reg += reg
        if reg_batch:
            tot_reg += _upsert_regional_observations(db, commodity, reg_batch)

    return {"inserted": tot_ins, "updated": tot_upd, "dropped": tot_drop, "regional": tot_reg, "errors": errors}


def _audit_commodity(db, commodity: Commodity) -> Dict:
    rows = (
        db.query(PriceHistory)
        .filter(
            PriceHistory.commodity_id == commodity.id,
            PriceHistory.provenance == "collected",
        )
        .order_by(PriceHistory.record_date.asc())
        .all()
    )
    verified = [r for r in rows if _has_verified_source_url(r)]
    by_year = defaultdict(int)
    for r in verified:
        by_year[r.record_date.year] += 1
    max_gap = max(((b.record_date - a.record_date).days - 1 for a, b in zip(verified, verified[1:])), default=0)
    reg_cnt = db.query(RegionalPriceObservation).filter(RegionalPriceObservation.commodity_id == commodity.id).count()
    return {
        "code": commodity.code,
        "name": commodity.name,
        "verified_total": len(verified),
        "by_year": dict(sorted(by_year.items())),
        "min_date": verified[0].record_date if verified else None,
        "max_date": verified[-1].record_date if verified else None,
        "max_gap": max_gap,
        "regional_obs": reg_cnt,
    }


def _cleanup_legacy_seed_rows(db, commodity: Commodity, min_keep_date: date) -> int:
    """Delete legacy init.sql seed rows (< min_keep_date OR provenance != 'collected' OR invalid source_url)."""
    rows = db.query(PriceHistory).filter(PriceHistory.commodity_id == commodity.id).all()
    deleted = 0
    for r in rows:
        if r.record_date < min_keep_date or not _has_verified_source_url(r):
            db.delete(r)
            deleted += 1
    db.commit()
    return deleted


def main():
    ap = argparse.ArgumentParser(description="Backfill 100% real agricultural prices (2024-2026) with monthly UPSERT.")
    ap.add_argument(
        "--commodity",
        default="ALL",
        choices=["ALL", "SUGARCANE", "COFFEE_ROBUSTA", "PEPPER_BLACK", "RICE_IR504"],
        help="Target commodity code or ALL",
    )
    ap.add_argument("--start", default="2024-01-01", help="Start date YYYY-MM-DD")
    ap.add_argument("--end", default="2026-11-21", help="End date YYYY-MM-DD")
    ap.add_argument("--sleep", type=float, default=0.35, help="Polite delay in seconds between requests")
    ap.add_argument("--force", action="store_true", help="Re-scrape dates already saved as collected")
    ap.add_argument(
        "--apply-cleanup",
        action="store_true",
        help="After backfill verification, remove legacy non-collected / pre-start seed rows",
    )
    args = ap.parse_args()

    start_d = date.fromisoformat(args.start)
    end_d = date.fromisoformat(args.end)
    targets = (
        ["SUGARCANE", "COFFEE_ROBUSTA", "PEPPER_BLACK", "RICE_IR504"]
        if args.commodity == "ALL"
        else [args.commodity]
    )

    http = requests.Session()
    with SessionLocal() as db:
        for code in targets:
            commodity = db.query(Commodity).filter(Commodity.code == code).first()
            if not commodity:
                logger.error("Commodity %s not found in DB!", code)
                continue

            if code == "SUGARCANE":
                _backfill_sugarcane(http, db, commodity, start_d, end_d, args.sleep, args.force)
            elif code == "COFFEE_ROBUSTA":
                _backfill_vnbiz_commodity(
                    http,
                    db,
                    commodity,
                    code,
                    sources_cfg=[
                        (
                            "https://vietnambiz.vn/gia-ca-phe-hom-nay.html",
                            "https://vietnambiz.vn/gia-ca-phe-hom-nay/trang-{page}.html",
                            ("gia-ca-phe-hom-nay", "gia-ca-phe-ngay", "gia-ca-phe-cuoi-tuan", "gia-ca-phe-the-gioi-ngay", "gia-ca-phe-robusta", "thi-truong-ngay-", "thi-truong-gia-ca-phe"),
                            105,
                        ),
                        (
                            "https://vietnambiz.vn/chu-de/ca-phe-34.htm",
                            "https://vietnambiz.vn/chu-de/ca-phe-34/trang-{page}.htm",
                            ("gia-ca-phe-hom-nay", "gia-ca-phe-ngay", "gia-ca-phe-cuoi-tuan", "gia-ca-phe-the-gioi-ngay", "gia-ca-phe-robusta", "thi-truong-ngay-", "thi-truong-gia-ca-phe"),
                            105,
                        ),
                    ],
                    parser=_parse_vnbiz_coffee_article,
                    start=start_d,
                    end=end_d,
                    sleep_sec=args.sleep,
                    force=args.force,
                )
            elif code == "PEPPER_BLACK":
                _backfill_vnbiz_commodity(
                    http,
                    db,
                    commodity,
                    code,
                    sources_cfg=[
                        (
                            "https://vietnambiz.vn/chu-de/ho-tieu-hat-tieu-39.htm",
                            "https://vietnambiz.vn/chu-de/ho-tieu-hat-tieu-39/trang-{page}.htm",
                            ("gia-tieu-hom-nay", "gia-tieu-ngay", "gia-ho-tieu"),
                            100,
                        ),
                        (
                            "https://vietnambiz.vn/gia-tieu.html",
                            "https://vietnambiz.vn/gia-tieu/trang-{page}.html",
                            ("gia-tieu-hom-nay", "gia-tieu-ngay", "gia-ho-tieu"),
                            95,
                        ),
                        (
                            "https://vietnambiz.vn/gia-tieu.html",
                            "https://vietnambiz.vn/gia-tieu-hom-nay/trang-{page}.html",
                            ("gia-tieu-hom-nay", "gia-tieu-ngay", "gia-ho-tieu"),
                            85,
                        ),
                    ],
                    parser=_parse_vnbiz_pepper_article,
                    start=start_d,
                    end=end_d,
                    sleep_sec=args.sleep,
                    force=args.force,
                )
            elif code == "RICE_IR504":
                _backfill_vnbiz_commodity(
                    http,
                    db,
                    commodity,
                    code,
                    sources_cfg=[
                        (
                            "https://vietnambiz.vn/chu-de/gao-41.htm",
                            "https://vietnambiz.vn/chu-de/gao-41/trang-{page}.htm",
                            ("gia-lua-gao-hom-nay", "gia-lua-gao-ngay", "gia-lua-gao-tang", "gia-lua-gao-giam", "gia-gao-hom-nay"),
                            90,
                        ),
                        (
                            "https://vietnambiz.vn/gia-lua-gao.html",
                            "https://vietnambiz.vn/gia-gao/trang-{page}.html",
                            ("gia-lua-gao-hom-nay", "gia-lua-gao-ngay", "gia-lua-gao-tang", "gia-lua-gao-giam", "gia-gao-hom-nay"),
                            70,
                        ),
                    ],
                    parser=_parse_vnbiz_rice_article,
                    start=start_d,
                    end=end_d,
                    sleep_sec=args.sleep,
                    force=args.force,
                    extra_rows_fn=lambda: _fetch_vfa_weekly_rice(http, start_d, end_d),
                )

            audit = _audit_commodity(db, commodity)
            logger.info(
                "AUDIT [%s]: total=%d | years=%s | range=%s..%s | max_gap=%dd | regional_obs=%d",
                audit["code"],
                audit["verified_total"],
                audit["by_year"],
                audit["min_date"],
                audit["max_date"],
                audit["max_gap"],
                audit["regional_obs"],
            )

            if args.apply_cleanup:
                # Only purge legacy seed data when verified real coverage is continuous (>= 400 rows, max_gap <= 14d)
                if audit["verified_total"] >= 400 and audit["max_gap"] <= 14 and audit["min_date"]:
                    removed = _cleanup_legacy_seed_rows(db, commodity, max(start_d, audit["min_date"]))
                    logger.info("CLEANUP [%s]: removed %d legacy non-collected/pre-start seed rows", code, removed)
                else:
                    logger.warning(
                        "CLEANUP SKIPPED [%s]: insufficient continuous coverage (total=%d, max_gap=%dd)",
                        code,
                        audit["verified_total"],
                        audit["max_gap"],
                    )


if __name__ == "__main__":
    main()
