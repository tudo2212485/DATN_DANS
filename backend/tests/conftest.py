import pytest
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
