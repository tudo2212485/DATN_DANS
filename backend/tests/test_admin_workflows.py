from datetime import date, datetime, timedelta
import pytest
from app.models.models import User, Commodity, PriceHistory, BackgroundJob, SystemSetting, Forecast


@pytest.fixture
def headers(client):
    result = client.post('/api/v1/auth/login', json={'email': 'admin@test.com', 'password': 'Admin123!'})
    return {'Authorization': 'Bearer ' + result.json()['access_token']}


def test_lock_rejects_existing_token_and_unlock_restores_role(client, db_session, headers):
    login = client.post('/api/v1/auth/login', json={'email': 'user@test.com', 'password': 'User123!'})
    user_headers = {'Authorization': 'Bearer ' + login.json()['access_token']}
    user = db_session.query(User).filter_by(email='user@test.com').one()
    assert client.patch(f'/api/v1/admin/users/{user.id}/toggle-status', headers=headers).status_code == 200
    assert client.get('/api/v1/auth/me', headers=user_headers).status_code == 403
    assert client.post('/api/v1/auth/login', json={'email': 'user@test.com', 'password': 'User123!'}).status_code == 403
    client.patch(f'/api/v1/admin/users/{user.id}/toggle-status', headers=headers)
    response = client.get('/api/v1/auth/me', headers=user_headers)
    assert response.status_code == 200
    assert response.json()['role'] == 'analyst'


def test_admin_cannot_demote_self_or_create_invalid_role(client, db_session, headers):
    admin = db_session.query(User).filter_by(email='admin@test.com').one()
    assert client.patch(f'/api/v1/admin/users/{admin.id}/role', headers=headers, json={'role': 'user'}).status_code == 400
    assert client.post('/api/v1/admin/users', headers=headers, json={
        'email': 'new@test.com', 'full_name': 'Test User', 'password': 'Password123', 'role': 'superadmin'
    }).status_code == 422


def test_price_import_filters_and_update(client, db_session, headers):
    commodity = db_session.query(Commodity).first()
    content = ('commodity_id,record_date,price,source\n'
               f'{commodity.id},2026-01-01,100,CSV\n'
               f'{commodity.id},2026-01-02,-5,CSV\n'
               f'{commodity.id},2026-01-03,120,CSV\n'
               f'{commodity.id},2026-01-01,110,CSV\n')
    result = client.post('/api/v1/admin/prices/import-csv', headers=headers,
                         files={'file': ('prices.csv', content.encode(), 'text/csv')})
    assert result.status_code == 200
    assert result.json()['records_created'] == 2
    assert result.json()['records_updated'] == 1
    assert len(result.json()['errors']) == 1
    rows = client.get('/api/v1/admin/prices/recent?start_date=2026-01-03&end_date=2026-01-03', headers=headers).json()
    assert len(rows) == 1 and rows[0]['price'] == 120
    exported = client.get('/api/v1/admin/prices/export-csv?start_date=2026-01-03', headers=headers).text
    assert '2026-01-03' in exported and '2026-01-01' not in exported
    assert client.get('/api/v1/admin/prices/recent?offset=1&limit=1', headers=headers).json()[0]['price'] == 110
    assert client.get('/api/v1/admin/prices/recent?start_date=2026-02-01&end_date=2026-01-01', headers=headers).status_code == 400
    assert db_session.query(PriceHistory).first().price_min is None


def test_real_job_lifecycle_and_conflict(client, db_session, headers, monkeypatch):
    monkeypatch.setattr('app.services.job_service.run_job', lambda *args: None)
    monkeypatch.setattr('app.api.v1.endpoints.admin.run_job', lambda *args: None)
    result = client.post('/api/v1/admin/tasks/scrape?days=7', headers=headers)
    task_id = result.json()['task_id']
    assert result.json()['status'] == 'RUNNING'
    assert client.post('/api/v1/admin/tasks/retrain', headers=headers).status_code == 409
    job = db_session.get(BackgroundJob, task_id)
    job.status = 'FAILED'
    job.message = 'Source unavailable'
    job.finished_at = datetime.now()
    db_session.commit()
    assert client.get(f'/api/v1/admin/tasks/{task_id}', headers=headers).json()['status'] == 'FAILED'
    logs = client.get('/api/v1/admin/logs/crawler', headers=headers).json()
    assert len(logs) == 1 and logs[0]['records_extracted'] == 0
    assert logs[0]['details'] == 'Source unavailable'


def test_default_model_applies_to_forecast_api(client, db_session, headers):
    commodity = db_session.query(Commodity).first()
    from app.models.models import TrainingRun
    from app.services.history_service import observations, fingerprint
    for offset in range(60):
        db_session.add(PriceHistory(
            commodity_id=commodity.id,
            record_date=date.today() - timedelta(days=60 - offset),
            price=100 + offset,
            provenance='collected',
        ))
    db_session.commit()
    run = TrainingRun(commodity_id=commodity.id, dataset_hash=fingerprint(observations(db_session,commodity.id)), metadata_json='{}')
    db_session.add(run)
    db_session.commit()
    db_session.add(Forecast(commodity_id=commodity.id, model_name='XGBoost', forecast_date=date.today(),
                           training_run_id=run.id, predicted_price=105, lower_ci=95, upper_ci=115, mae=2, rmse=3, mape=2, r2=-0.5))
    db_session.commit()
    assert client.post('/api/v1/admin/models/active', headers=headers, json={'active_model': 'XGBoost'}).status_code == 200
    assert db_session.get(SystemSetting, 'active_model').value == 'XGBOOST'
    result = client.get(f'/api/v1/forecast?commodity_id={commodity.id}&days=1')
    assert result.status_code == 200
    assert result.json()['modelName'] == 'XGBoost'
    assert result.json()['metrics']['r2'] == -0.5
    assert client.post('/api/v1/admin/models/active', headers=headers, json={'active_model': 'invalid'}).status_code == 400


def test_scrape_job_auto_retrains_changed_ready_series(db_session, monkeypatch):
    import app.services.job_service as jobs
    import app.services.training_service as training
    import ml_pipeline.scraper as scraper

    commodity = db_session.query(Commodity).first()
    for offset in range(60):
        db_session.add(PriceHistory(
            commodity_id=commodity.id,
            record_date=date.today() - timedelta(days=60 - offset),
            price=100 + offset,
            provenance='collected',
            source='Test source',
        ))
    job = BackgroundJob(kind='scrape', status='RUNNING', message='running')
    db_session.add(job)
    db_session.commit()

    monkeypatch.setattr(scraper, 'scrape_and_update_db', lambda **kwargs: {
        'status': 'SUCCESS', 'count': 0, 'message': 'Không có bản ghi mới.'
    })
    called = []
    monkeypatch.setattr(training, 'retrain', lambda commodity_id, progress: (
        called.append(commodity_id) or {'status': 'SUCCESS', 'count': 150, 'message': 'Đã huấn luyện.'}
    ))

    jobs.run_job(job.id, 'scrape', {'days': 7, 'commodity_id': commodity.id})
    db_session.expire_all()
    finished = db_session.get(BackgroundJob, job.id)
    assert called == [commodity.id]
    assert finished.status == 'SUCCESS' and finished.progress == 100
    assert 'Đã huấn luyện' in finished.message
