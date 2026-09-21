"""One auditable input series shared by history views and model training."""
import hashlib
import json
import math
from datetime import date
from app.models.models import PriceHistory, PriceRevision

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


def modeling_rows(rows):
    """Use the newest published regime after a long source discontinuity."""
    if not rows:
        return []
    start = 0
    for index, (older, newer) in enumerate(zip(rows, rows[1:]), start=1):
        if (newer.record_date - older.record_date).days - 1 > SERIES_BREAK_DAYS:
            start = index
    return rows[start:]


def readiness(rows):
    original_count = len(rows)
    rows = modeling_rows(rows)
    count = len(rows)
    gap = max(((b.record_date - a.record_date).days - 1 for a, b in zip(rows, rows[1:])), default=0)
    reason = None
    if count < 60:
        reason = f"Cần tối thiểu 60 ngày giá có nguồn đã thu thập/được xác nhận; hiện có {count}."
    elif gap > MAX_FILL_DAYS:
        reason = f"Chuỗi có khoảng trống {gap} ngày; cần bổ sung dữ liệu trước khi huấn luyện."
    elif any(not math.isfinite(float(r.price)) or float(r.price) <= 0 for r in rows):
        reason = "Chuỗi chứa giá không hợp lệ."
    return {"ready": reason is None, "reason": reason, "observation_count": count,
            "start_date": str(rows[0].record_date) if rows else None,
            "end_date": str(rows[-1].record_date) if rows else None, "max_gap_days": gap,
            "excluded_older_observations": original_count - count,
            "series_break_days": SERIES_BREAK_DAYS, "max_fill_days": MAX_FILL_DAYS}
