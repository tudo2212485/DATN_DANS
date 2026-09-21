from datetime import date, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Commodity, TrainingRun, PeriodicPrice
from app.services.history_service import observations, readiness
from ml_pipeline.source_catalog import SOURCES
import json

router = APIRouter()


@router.get("/readiness")
def training_readiness(commodity_id: int, db: Session = Depends(get_db)):
    if not db.get(Commodity, commodity_id):
        raise HTTPException(404, "Không tìm thấy nông sản")
    rows = observations(db, commodity_id)
    return readiness(rows)


@router.get("/training-runs/{run_id}")
def training_snapshot(run_id: int, db: Session = Depends(get_db)):
    run = db.get(TrainingRun, run_id)
    if not run:
        raise HTTPException(404, "Không tìm thấy lần huấn luyện")
    return dict(run_id=run.id, commodity_id=run.commodity_id, dataset_hash=run.dataset_hash,
                created_at=run.created_at, **json.loads(run.metadata_json))


@router.get("/sources")
def sources(db: Session = Depends(get_db)):
    return [dict(id=c.id, code=c.code, name=c.name, unit=c.unit,
                 automatic=c.code in SOURCES,
                 **SOURCES.get(c.code, dict(kind='daily', source_url=None, limitation='Chưa có nguồn Việt Nam được xác minh; nhập CSV có nguồn.')))
            for c in db.query(Commodity).order_by(Commodity.id).all()]


@router.get("")
def history(commodity_id: int, start_date: date = Query(...), end_date: date = Query(...),
            include_unverified: bool = False, db: Session = Depends(get_db)):
    if not db.get(Commodity, commodity_id):
        raise HTTPException(404, "Không tìm thấy nông sản")
    if end_date < start_date or end_date > date.today() or (end_date - start_date).days > 1826:
        raise HTTPException(400, "Chọn khoảng quá khứ hợp lệ, tối đa 5 năm mỗi lần xem")
    rows = observations(db, commodity_id, start_date, end_date, not include_unverified)
    dates = {r.record_date for r in rows}
    count = (end_date - start_date).days + 1
    reports = db.query(PeriodicPrice).filter(PeriodicPrice.commodity_id == commodity_id,
               PeriodicPrice.period_end >= start_date, PeriodicPrice.period_start <= end_date).order_by(PeriodicPrice.period_start).all()
    return {
        "periodic_records": [dict(id=r.id, start=str(r.period_start), end=str(r.period_end),
            published_date=str(r.published_date), buying_price=float(r.buying_price), selling_price=float(r.selling_price),
            unit=r.unit, specification=r.specification, market=r.market, source=r.source_url, attribution=r.attribution) for r in reports],
        "records": [dict(id=r.id, date=str(r.record_date), price=float(r.price), source=r.source,
                         provenance=r.provenance, source_details=json.loads(r.source_details) if r.source_details else None) for r in rows],
        "missing_dates": [str(start_date + timedelta(days=i)) for i in range(count)
                          if start_date + timedelta(days=i) not in dates],
        "readiness": readiness(observations(db, commodity_id)),
        "range_readiness": readiness(observations(db, commodity_id, start_date, end_date)),
        "unverified_count": sum(r.provenance not in ("collected", "reviewed")
                                for r in observations(db, commodity_id, start_date, end_date, False)),
    }
