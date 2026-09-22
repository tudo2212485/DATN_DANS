"""The history/forecast contract uses isolated fixture prices, never market data."""
import json
from datetime import date, timedelta
from unittest.mock import Mock
import numpy as np
import pandas as pd
import pytest
from app.models.models import Commodity, PeriodicPrice, PriceHistory, Forecast, TrainingRun, PriceRevision
from app.services.history_service import observations, modeling_rows, readiness, training_context
from ml_pipeline.observation_scraper import parse_coffee_observation, SourceAccessRequired


def seed_history(db, count=70, provenance='reviewed'):
    commodity = db.query(Commodity).first()
    for i in range(count):
        db.add(PriceHistory(commodity_id=commodity.id, record_date=date.today()-timedelta(days=count-i),
                            price=1000+i*2+(i%3), provenance=provenance, source='Isolated test fixture'))
    db.commit()
    return commodity.id


def test_public_history_filters_provenance_and_gaps(client, db_session):
    cid=seed_history(db_session,3)
    db_session.add(PriceHistory(commodity_id=cid,record_date=date.today(),price=1200))
    db_session.commit()
    params={'commodity_id':cid,'start_date':str(date.today()-timedelta(days=4)), 'end_date':str(date.today())}
    response=client.get('/api/v1/history',params=params)
    assert response.status_code==200
    data=response.json()
    assert len(data['records'])==3 and len(data['missing_dates'])==2
    assert data['unverified_count']==1 and not data['readiness']['ready']
    assert len(client.get('/api/v1/history',params={**params,'include_unverified':True}).json()['records'])==4
    assert client.get('/api/v1/history',params={**params,'end_date':'2099-01-01'}).status_code==400


def test_training_does_not_read_holdout_and_invalidates_on_edit(client,db_session,monkeypatch):
    import app.services.training_service as training
    cid=seed_history(db_session)
    seen=[]
    def predict(name,series,horizon):
        seen.append((len(series),series.index[-1],horizon))
        return np.full(horizon,series.iloc[-1])
    monkeypatch.setattr(training,'predict_series',predict)
    result=training.retrain(cid,lambda *args:None)
    assert result['status']=='SUCCESS' and result['count']==150
    assert len(seen)==10
    assert all(seen[i][0]==60 and seen[i+1][0]==70 for i in range(0,10,2))
    run=db_session.query(TrainingRun).one()
    meta=json.loads(run.metadata_json)
    assert meta['test_count']==10 and meta['train_end'] < meta['test_start']
    assert len(meta['snapshot'])==70
    for horizon in [7,14,30]:
        response=client.get('/api/v1/forecast',params={'commodity_id':cid,'days':horizon})
        assert response.status_code==200
        data=response.json()
        assert sum(p['isForecast'] for p in data['forecastData'])==horizon
        assert data['training']['baseline']['rmse']==pytest.approx(data['metrics']['rmse'],abs=.0001)
        assert next(p for p in data['forecastData'] if p['isForecast'])['date']==str(date.today())
    row=db_session.query(PriceHistory).first()
    row.price=2000
    db_session.commit()
    assert client.get('/api/v1/forecast',params={'commodity_id':cid}).status_code==409
    assert client.get(f'/api/v1/forecast/compare/{cid}').json()==[]


def test_training_rejects_unverified_and_large_gaps(db_session):
    from app.services.training_service import retrain
    cid=seed_history(db_session,70,'unverified')
    assert retrain(cid,lambda *args:None)['status']=='FAILED'
    assert db_session.query(Forecast).count()==0
    rows=db_session.query(PriceHistory).all()
    for row in rows:
        row.provenance='reviewed'
    db_session.delete(rows[10])
    for row in rows[11:25]:
        db_session.delete(row)
    db_session.commit()
    assert not readiness(observations(db_session,cid))['ready']


def test_modeling_uses_latest_series_after_long_publication_break(db_session):
    commodity = db_session.query(Commodity).first()
    old_start = date.today()-timedelta(days=240)
    recent_start = date.today()-timedelta(days=69)
    for start, count in [(old_start, 10), (recent_start, 70)]:
        for i in range(count):
            db_session.add(PriceHistory(commodity_id=commodity.id, record_date=start+timedelta(days=i),
                                        price=1000+i, provenance='reviewed', source='Isolated test fixture'))
    db_session.commit()
    all_rows = observations(db_session, commodity.id)
    selected = modeling_rows(all_rows)
    quality = readiness(all_rows)
    assert len(selected) == 70 and selected[0].record_date == recent_start
    assert quality['ready'] and quality['excluded_older_observations'] == 10


def test_modeling_keeps_latest_complete_series_when_new_fragment_is_short(db_session):
    commodity = db_session.query(Commodity).first()
    old_start = date.today()-timedelta(days=300)
    recent_start = date.today()-timedelta(days=10)
    for start, count in [(old_start, 68), (recent_start, 2)]:
        for i in range(count):
            db_session.add(PriceHistory(commodity_id=commodity.id, record_date=start+timedelta(days=i),
                                        price=1000+i, provenance='reviewed', source='Isolated test fixture'))
    db_session.commit()
    selected = modeling_rows(observations(db_session, commodity.id))
    assert len(selected) == 68 and selected[-1].record_date < recent_start
    assert readiness(observations(db_session, commodity.id))['ready']


def test_periodic_reports_train_as_periods_without_creating_daily_prices(db_session, monkeypatch):
    import app.services.training_service as training
    commodity = db_session.query(Commodity).first()
    commodity.code = 'SUGARCANE'
    start = date(2023, 1, 1)
    for i in range(10):
        published = start + timedelta(days=i * 60)
        db_session.add(PeriodicPrice(
            commodity_id=commodity.id, period_start=published-timedelta(days=9), period_end=published,
            published_date=published, buying_price=700000+i*10000, selling_price=900000+i*10000,
            unit='VND/tấn', specification='Mía (từ 7 – 10 chữ đường)', market='Tây Hòa, Phú Yên',
            source_url=f'https://example.test/report-{i}', attribution='Isolated test fixture'))
    db_session.commit()
    seen = []
    def predict(name, series, horizon, future_index=None):
        seen.append((len(series), horizon, future_index is not None))
        return np.full(horizon, series.iloc[-1])
    monkeypatch.setattr(training, 'predict_series', predict)
    result = training.retrain(commodity.id, lambda *args: None)
    context = training_context(db_session, commodity)
    run = db_session.query(TrainingRun).one()
    metadata = json.loads(run.metadata_json)
    assert context['quality']['ready'] and context['cadence'] == 'periodic'
    assert result['status'] == 'SUCCESS' and result['count'] == 150
    assert metadata['cadence'] == 'periodic' and metadata['filled_days'] == 0
    assert all(has_dates for _, _, has_dates in seen)
    assert db_session.query(PriceHistory).count() == 0


def test_scraper_preserves_old_snapshot_and_stops_at_access_boundary(db_session,monkeypatch):
    import ml_pipeline.observation_scraper as scraper
    cid=seed_history(db_session,1,'unverified')
    day=date.today()-timedelta(days=1)
    success=Mock(status_code=200,text=f'<h1>Giá cà phê ngày {day:%d/%m/%Y}</h1><p>trung bình ở mức 95,000 VNĐ/kg</p>')
    restricted=Mock(status_code=200,text=f'<h1>Giá cà phê ngày {day-timedelta(days=1):%d/%m/%Y}</h1><p>Truy vấn quá giới hạn, đăng nhập để tiếp tục</p>')
    http=Mock()
    http.get.side_effect=[success,restricted]
    context=Mock();context.__enter__=Mock(return_value=http);context.__exit__=Mock(return_value=False)
    monkeypatch.setattr(scraper.requests,'Session',lambda:context)
    monkeypatch.setattr(scraper.time,'sleep',lambda _:None)
    result=scraper.scrape_and_update_db(commodity_id=cid,start_date=day-timedelta(days=3),end_date=day)
    assert result['status']=='PARTIAL' and result['count']==1 and http.get.call_count==2
    db_session.expire_all()
    row=db_session.query(PriceHistory).one()
    assert row.provenance=='collected' and row.price==95000
    assert db_session.query(PriceRevision).count()==1


def test_parser_does_not_bypass_login():
    with pytest.raises(SourceAccessRequired):
        parse_coffee_observation('<h1>01/07/2026</h1><p>quá giới hạn</p>',date(2026,7,1))


@pytest.mark.parametrize('name',['Random Forest','XGBoost','ARIMA','Prophet','LSTM'])
def test_real_models_forecast_from_fixture_prefix(name):
    from ml_pipeline.history_models import predict_series
    series=pd.Series(100+np.sin(np.arange(70)/5)+np.arange(70)*.2,index=pd.date_range('2025-01-01',periods=70))
    result=predict_series(name,series,7)
    assert len(result)==7 and np.isfinite(result).all() and (result>=0).all()
