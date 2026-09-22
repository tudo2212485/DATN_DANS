"""One auditable input series shared by history views and model training."""
import hashlib
import json
import math
from types import SimpleNamespace
from datetime import date
from statistics import median
from app.models.models import Commodity, PeriodicPrice, PriceHistory, PriceRevision

ELIGIBLE = ("collected", "reviewed")
SERIES_BREAK_DAYS = 30
MAX_FILL_DAYS = 14


def archive_price(db, row):
    db.add(PriceRevision(price_id=row.id, snapshot_json=json.dumps({
        column.name: str(getattr(row, column.name)) for column in row.__table__.columns
    }, ensure_ascii=False)))


def observations(db, commodity_id, start=None, end=None, eligible_only=True):
    query = db.query(PriceHistory).filter(PriceHistory.commodity_id == commodity_id,
                                       PriceHistory.record_date <= (end or date.today()))
    if start:
        query = query.filter(PriceHistory.record_date >= start)
    if eligible_only:
        query = query.filter(PriceHistory.provenance.in_(ELIGIBLE))
    rows = query.order_by(PriceHistory.record_date, PriceHistory.id).all()
    return list({r.record_date: r for r in rows}.values())


def fingerprint(rows):
    return hashlib.sha256(json.dumps([
        [r.record_date.isoformat(), str(r.price), r.source, r.provenance, r.source_details] for r in rows
    ], ensure_ascii=False).encode()).hexdigest()


def _segments(rows):
    if not rows:
        return []
    result, start = [], 0
    for index, (older, newer) in enumerate(zip(rows, rows[1:]), start=1):
        if (newer.record_date - older.record_date).days - 1 > SERIES_BREAK_DAYS:
            result.append(rows[start:index])
            start = index
    result.append(rows[start:])
    return result


def _max_gap(rows):
    return max(((b.record_date - a.record_date).days - 1 for a, b in zip(rows, rows[1:])), default=0)


def modeling_rows(rows):
    """Use the newest complete regime; retain a short newer fragment for collection only."""
    segments = _segments(rows)
    for segment in reversed(segments):
        if len(segment) >= 60 and _max_gap(segment) <= MAX_FILL_DAYS:
            return segment
    return segments[-1] if segments else []


def readiness(rows, cadence="daily"):
    original_count = len(rows)
    rows = rows if cadence in ("periodic", "irregular") else modeling_rows(rows)
    count = len(rows)
    gap = _max_gap(rows)
    minimum = 8 if cadence == "periodic" else 60
    reason = None
    if count < minimum:
        unit = "kỳ báo cáo" if cadence == "periodic" else ("mốc công bố" if cadence == "irregular" else "ngày giá")
        reason = f"Cần tối thiểu {minimum} {unit} có nguồn đã thu thập/được xác nhận; hiện có {count}."
    elif cadence == "daily" and gap > MAX_FILL_DAYS:
        reason = f"Chuỗi có khoảng trống {gap} ngày; cần bổ sung dữ liệu trước khi huấn luyện."
    elif any(not math.isfinite(float(r.price)) or float(r.price) <= 0 for r in rows):
        reason = "Chuỗi chứa giá không hợp lệ."
    return {"ready": reason is None, "reason": reason, "observation_count": count,
            "start_date": str(rows[0].record_date) if rows else None,
            "end_date": str(rows[-1].record_date) if rows else None, "max_gap_days": gap,
            "excluded_older_observations": original_count - count,
            "series_break_days": SERIES_BREAK_DAYS, "max_fill_days": MAX_FILL_DAYS,
            "cadence": cadence}


def periodic_observations(db, commodity_id, start=None, end=None):
    query = db.query(PeriodicPrice).filter(PeriodicPrice.commodity_id == commodity_id)
    if start:
        query = query.filter(PeriodicPrice.published_date >= start)
    if end:
        query = query.filter(PeriodicPrice.published_date <= end)
    reports = query.order_by(PeriodicPrice.published_date, PeriodicPrice.id).all()
    return [SimpleNamespace(
        record_date=row.published_date,
        price=row.buying_price,
        source=row.source_url,
        provenance="collected",
        source_details=json.dumps({
            "period_start": str(row.period_start),
            "period_end": str(row.period_end),
            "selling_price": float(row.selling_price),
            "specification": row.specification,
            "market": row.market,
            "target": "Giá mua",
        }, ensure_ascii=False),
    ) for row in reports]


def training_context(db, commodity_or_id, start=None, end=None):
    commodity = commodity_or_id if isinstance(commodity_or_id, Commodity) else db.get(Commodity, commodity_or_id)
    if not commodity:
        raise ValueError("Không tìm thấy nông sản")
    from ml_pipeline.source_catalog import SOURCES
    cadence = SOURCES.get(commodity.code, {}).get("kind", "daily")
    if cadence == "periodic":
        rows = periodic_observations(db, commodity.id, start, end)
        selected = rows
        quality = readiness(rows, cadence)
        intervals = [(b.record_date - a.record_date).days for a, b in zip(rows, rows[1:])]
        step_days = max(1, int(median(intervals))) if intervals else 30
        quality.update(cadence_days=step_days, target="Giá mua theo kỳ")
    elif cadence == "irregular":
        rows = observations(db, commodity.id, start, end)
        selected = rows
        quality = readiness(rows, cadence)
        intervals = [(b.record_date - a.record_date).days for a, b in zip(rows, rows[1:])]
        step_days = max(1, int(median(intervals))) if intervals else 7
        quality.update(cadence_days=step_days, target="Giá tại mốc AGROINFO công bố")
    else:
        rows = observations(db, commodity.id, start, end)
        selected = modeling_rows(rows)
        quality = readiness(rows, cadence)
        step_days = 1
        quality.update(cadence_days=step_days, target="Giá công bố")
    return {"all_rows": rows, "rows": selected, "quality": quality,
            "cadence": cadence, "cadence_days": step_days}
