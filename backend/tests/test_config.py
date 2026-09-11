import pytest
from app.core.config import settings

def test_settings_loaded():
    """Kiểm tra các giá trị cấu hình cơ bản được nạp thành công"""
    assert settings.PROJECT_NAME != ""
    assert settings.API_V1_STR == "/api/v1"
    assert settings.ALGORITHM == "HS256"
    assert settings.ACCESS_TOKEN_EXPIRE_MINUTES > 0
    assert len(settings.SECRET_KEY) >= 32
    assert "http://localhost:3000" in settings.CORS_ORIGINS
