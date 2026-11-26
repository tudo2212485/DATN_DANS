import pytest
from app.core.config import Settings, normalize_database_url, settings
from app.core.database import build_async_engine, build_sync_engine


def test_settings_loaded():
    """Kiểm tra các giá trị cấu hình cơ bản được nạp thành công"""
    assert settings.PROJECT_NAME != ""
    assert settings.API_V1_STR == "/api/v1"
    assert settings.ALGORITHM == "HS256"
    assert settings.ACCESS_TOKEN_EXPIRE_MINUTES > 0
    assert len(settings.SECRET_KEY) >= 32
    assert "http://localhost:3000" in settings.CORS_ORIGINS


def test_neon_database_url_normalization_and_engine_pooling():
    """Kiểm tra chuẩn hóa SSL cho Neon PostgreSQL (sync & asyncpg) và pool_pre_ping/pool_recycle=300"""
    neon_url = (
        "postgresql://neondb_owner:pass123@ep-demo-pooler.ap-southeast-1.aws.neon.tech/"
        "neondb?sslmode=require&channel_binding=require"
    )
    sync_url = normalize_database_url(neon_url, is_async=False)
    assert sync_url.startswith("postgresql://")
    assert "sslmode=require" in sync_url

    async_url = normalize_database_url(neon_url, is_async=True)
    assert async_url.startswith("postgresql+asyncpg://")
    assert "ssl=require" in async_url
    assert "sslmode=" not in async_url
    assert "channel_binding=" not in async_url

    # Tự thêm SSL cho host *.neon.tech nếu bị thiếu tham số SSL
    bare_neon = "postgres://u:p@ep-bare.us-east-2.aws.neon.tech/neondb"
    assert "sslmode=require" in normalize_database_url(bare_neon, is_async=False)
    assert normalize_database_url(bare_neon, is_async=True).endswith("?ssl=require")

    # Kiểm tra bật pool_pre_ping=True và pool_recycle=300 trên cả sync và async engine
    sync_eng = build_sync_engine(neon_url)
    async_eng = build_async_engine(neon_url)
    try:
        assert sync_eng.pool._pre_ping is True
        assert sync_eng.pool._recycle == 300
        assert async_eng is not None
        assert async_eng.sync_engine.pool._pre_ping is True
        assert async_eng.sync_engine.pool._recycle == 300
    finally:
        sync_eng.dispose()
        if async_eng is not None:
            async_eng.sync_engine.dispose()


def test_cors_origins_env_comma_separated_and_json(monkeypatch):
    """Kiểm tra CORS_ORIGINS đọc danh sách nhiều domain phân cách dấu phẩy hoặc JSON từ biến môi trường"""
    monkeypatch.setenv(
        "CORS_ORIGINS",
        "https://agroforecast.vercel.app/, https://tudo-agroforecast.hf.space , http://localhost:3000",
    )
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql://u:p@ep-demo.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require",
    )
    monkeypatch.delenv("DATABASE_URL_ASYNC", raising=False)
    s = Settings(_env_file=None)
    assert s.CORS_ORIGINS == [
        "https://agroforecast.vercel.app",
        "https://tudo-agroforecast.hf.space",
        "http://localhost:3000",
    ]
    assert s.DATABASE_URL_ASYNC.startswith("postgresql+asyncpg://")
    assert "ssl=require" in s.DATABASE_URL_ASYNC
    assert "channel_binding" not in s.DATABASE_URL_ASYNC

    monkeypatch.setenv("CORS_ORIGINS", '["https://a.example.com", "https://b.example.com/"]')
    s_json = Settings(_env_file=None)
    assert s_json.CORS_ORIGINS == ["https://a.example.com", "https://b.example.com"]
