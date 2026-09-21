import os
import pytest

# Never migrate or train against the user's database during test collection.
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db
from app.models.models import User, Commodity
from app.core.security import get_password_hash

# Sử dụng SQLite in-memory cho testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def isolate_background_work(monkeypatch, tmp_path):
    import app.core.database as database
    import app.core.scheduler as scheduler
    import app.api.v1.endpoints.predictions as predictions
    import app.services.job_service as jobs
    import app.services.training_service as training
    import ml_pipeline.observation_scraper as scraper
    import ml_pipeline.model_trainer as trainer
    import ml_pipeline.predictor as predictor
    import ml_pipeline.data_loader as loader
    import pandas as pd
    for module in (database, scheduler, predictions, jobs, training, scraper):
        monkeypatch.setattr(module, "SessionLocal", TestingSessionLocal)
    monkeypatch.setattr(trainer, "SAVED_MODELS_DIR", str(tmp_path))
    monkeypatch.setattr(predictor, "SAVED_MODELS_DIR", str(tmp_path))
    monkeypatch.setattr(loader, "get_exogenous_data", lambda *args: pd.DataFrame())
    monkeypatch.setattr("app.main.start_scheduler", lambda: None)
    monkeypatch.setattr("app.main.stop_scheduler", lambda: None)
    predictor.clear_prediction_cache()
    yield
    predictor.clear_prediction_cache()

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    # Tạo user test
    admin_user = User(
        email="admin@test.com",
        password_hash=get_password_hash("Admin123!"),
        full_name="Admin Tester",
        role="admin"
    )
    normal_user = User(
        email="user@test.com",
        password_hash=get_password_hash("User123!"),
        full_name="Normal User",
        role="analyst"
    )
    db.add(admin_user)
    db.add(normal_user)
    
    # Tạo commodity test
    c1 = Commodity(
        code="COFFEE_ROBUSTA",
        name="Cà phê Robusta",
        category="Nông sản",
        unit="VND/kg",
        region="Tây Nguyên",
        description="Cà phê Robusta Tây Nguyên"
    )
    db.add(c1)
    db.commit()
    
    yield db
    
    db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
            
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
