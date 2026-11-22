from datetime import date, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Commodity, TrainingRun, PeriodicPrice, RegionalPriceObservation
from app.services.history_service import observations, training_context
from app.services.regional_pricing_service import (
    normalize_province_code,
    resolve_commodity_location_context,
)
from ml_pipeline.source_catalog import SOURCES
import json

router = APIRouter()


@router.get("/readiness")
def training_readiness(commodity_id: int, db: Session = Depends(get_db)):
    commodity = db.get(Commodity, commodity_id)
    if not commodity:
        raise HTTPException(404, "Không tìm thấy nông sản")
    return training_context(db, commodity)["quality"]


@router.get("/training-runs/{run_id}")
def training_snapshot(run_id: int, db: Session = Depends(get_db)):
    run = db.get(TrainingRun, run_id)
    if not run:
        raise HTTPException(404, "Không tìm thấy lần huấn luyện")
    return dict(run_id=run.id, commodity_id=run.commodity_id, dataset_hash=run.dataset_hash,
                created_at=run.created_at, **json.loads(run.metadata_json))


@router.get("/sources")
def sources(db: Session = Depends(get_db)):
    from sqlalchemy import func
    from app.models.models import PriceHistory
    latest_map = dict(
        db.query(PriceHistory.commodity_id, func.max(PriceHistory.record_date))
        .group_by(PriceHistory.commodity_id)
        .all()
    )
    return [dict(id=c.id, code=c.code, name=c.name, unit=c.unit,
                 automatic=c.code in SOURCES,
                 latest_date=str(latest_map[c.id]) if c.id in latest_map and latest_map[c.id] else None,
                 **SOURCES.get(c.code, dict(kind='daily', source_url=None, limitation='Chưa có nguồn Việt Nam được xác minh; nhập CSV có nguồn.')))
            for c in db.query(Commodity).order_by(Commodity.id).all()]


def _extract_safe_http_url(raw_source: Optional[str], details: Optional[dict], direct_url: Optional[str] = None) -> Optional[str]:
    """Return a validated http(s) verification URL for UI display (XSS-safe).
    `direct_url` should ONLY be passed when an observation matches the exact same `record_date`.
    """
    candidates = [
        direct_url,
        (details or {}).get("source_url") if isinstance(details, dict) else None,
        raw_source,
    ]
    for cand in candidates:
        if isinstance(cand, str):
            trimmed = cand.strip()
            if trimmed.lower().startswith(("https://", "http://")):
                return trimmed
    return None


def _clean_source_label(raw_source: Optional[str], details: Optional[dict]) -> str:
    """Return a clean human-readable source name (never empty, avoids displaying raw URLs when provider exists)."""
    text = (raw_source or "").strip()
    if text and not text.lower().startswith(("https://", "http://")):
        return text
    if isinstance(details, dict):
        prov = str(details.get("provider") or "").strip()
        if prov:
            return prov
    if text.lower().startswith(("https://", "http://")):
        if "giacaphe.com" in text.lower():
            return "giacaphe.com (Giá cà phê nội địa)"
        return text
    return "Nguồn thị trường xác minh"


@router.get("")
def history(
    commodity_id: int,
    start_date: date = Query(...),
    end_date: date = Query(...),
    include_unverified: bool = False,
    province: Optional[str] = Query(None, description="Mã tỉnh/thành phố (VD: khanh-hoa, dak-lak, all)"),
    db: Session = Depends(get_db),
):
    commodity = db.get(Commodity, commodity_id)
    if not commodity:
        raise HTTPException(404, "Không tìm thấy nông sản")
    if end_date < start_date or end_date > date.today() or (end_date - start_date).days > 1826:
        raise HTTPException(400, "Chọn khoảng quá khứ hợp lệ, tối đa 5 năm mỗi lần xem")
    rows = observations(db, commodity_id, start_date, end_date, not include_unverified)
    dates = {r.record_date for r in rows}
    count = (end_date - start_date).days + 1
    reports = db.query(PeriodicPrice).filter(PeriodicPrice.commodity_id == commodity_id,
               PeriodicPrice.period_end >= start_date, PeriodicPrice.period_start <= end_date).order_by(PeriodicPrice.period_start).all()

    loc = resolve_commodity_location_context(db, commodity, province)
    norm_prov = normalize_province_code(province)

    direct_by_date = {}
    if norm_prov and loc.get("pricing_mode") == "direct":
        reg_rows = (
            db.query(RegionalPriceObservation)
            .filter(
                RegionalPriceObservation.commodity_id == commodity_id,
                RegionalPriceObservation.province_code == norm_prov,
                RegionalPriceObservation.recorded_date >= start_date,
                RegionalPriceObservation.recorded_date <= end_date,
            )
            .all()
        )
        direct_by_date = {rr.recorded_date: rr for rr in reg_rows}

    offset = float(loc.get("basis_offset", 0.0)) if norm_prov else 0.0
    if norm_prov and loc.get("pricing_mode") == "direct" and loc.get("latest_direct_price") and rows and not direct_by_date:
        # Periodic direct survey (e.g., Sugarcane in Khánh Hòa): anchor to exact provincial survey price
        offset = float(loc["latest_direct_price"]) - float(rows[-1].price)

    records_out = []
    for r in rows:
        parsed_details = json.loads(r.source_details) if r.source_details else None
        base_label = _clean_source_label(r.source, parsed_details)
        reg_hit = direct_by_date.get(r.record_date)
        if reg_hit is not None:
            price_val = float(reg_hit.price)
            src_val = f"{reg_hit.source} ({loc['province_name']})"
            prov_val = "collected"
            # Only use provincial survey URL when the survey matches this exact record_date
            src_url = _extract_safe_http_url(r.source, parsed_details, reg_hit.source_url)
        else:
            price_val = max(0.0, round(float(r.price) + offset, 2))
            if norm_prov:
                src_val = (
                    f"{base_label} · {loc['note']}"
                    if loc["pricing_mode"] == "regional_benchmark"
                    else f"{base_label} (Tham chiếu {loc['province_name']})"
                )
            else:
                src_val = base_label
            prov_val = r.provenance
            # NEVER inherit loc["direct_source_url"] from a different date/year onto this row!
            src_url = _extract_safe_http_url(r.source, parsed_details, None)
        records_out.append(
            dict(
                id=r.id,
                date=str(r.record_date),
                price=price_val,
                source=src_val,
                source_url=src_url,
                provenance=prov_val,
                source_details=parsed_details,
            )
        )

    return {
        "periodic_records": [dict(id=r.id, start=str(r.period_start), end=str(r.period_end),
            published_date=str(r.published_date), buying_price=float(r.buying_price), selling_price=float(r.selling_price),
            unit=r.unit, specification=r.specification, market=r.market, source=r.source_url, attribution=r.attribution) for r in reports],
        "records": records_out,
        "missing_dates": [str(start_date + timedelta(days=i)) for i in range(count)
                          if start_date + timedelta(days=i) not in dates],
        "readiness": training_context(db, commodity)["quality"],
        "range_readiness": training_context(db, commodity, start_date, end_date)["quality"],
        "unverified_count": sum(r.provenance not in ("collected", "reviewed")
                                for r in observations(db, commodity_id, start_date, end_date, False)),
        "location_context": loc,
    }
