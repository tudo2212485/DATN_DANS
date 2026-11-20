import hashlib
import logging
import os
import secrets
from typing import List
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger("app.core.config")

# SHA-256 digests of known insecure tutorial/placeholder secrets (never store plaintext secrets in code)
_INSECURE_SECRET_SHA256 = {
    "570dad43de1af4c925f92c16a68a50936da42b7dd6fdeb24850507a1199aac89",
    hashlib.sha256(b"CHANGE_ME_GENERATE_WITH_OPENSSL_RAND_HEX_32").hexdigest(),
    hashlib.sha256(b"secret").hexdigest(),
    hashlib.sha256(b"changeme").hexdigest(),
}


class Settings(BaseSettings):
    PROJECT_NAME: str = "AgroForecast - Hệ thống Dự báo Giá Nông sản"
    VERSION: str = "2.4.1"
    API_V1_STR: str = "/api/v1"

    # JWT Auth: load from backend/.env; fallback to ephemeral CSPRNG key in isolated dev/test only
    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Database Configuration (credentials MUST be supplied via backend/.env, never hardcoded in source)
    DATABASE_URL: str = "sqlite:///./agroforecast_dev.db"
    DATABASE_URL_ASYNC: str = "sqlite+aiosqlite:///./agroforecast_dev.db"

    # CORS Origins (Explicit whitelist; never pair "*" with allow_credentials=True)
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]

    # Email / SMTP Settings
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAIL_FROM: str = "AgroForecast <no-reply@agroforecast.vn>"

    @field_validator("SECRET_KEY", mode="before")
    @classmethod
    def ensure_strong_secret_key(cls, value: str) -> str:
        cleaned = (value or "").strip()
        digest = hashlib.sha256(cleaned.encode("utf-8")).hexdigest() if cleaned else ""
        if not cleaned or digest in _INSECURE_SECRET_SHA256 or len(cleaned) < 32:
            logger.warning(
                "SECRET_KEY missing, weak (<32 chars), or matches example value; "
                "generating ephemeral 256-bit CSPRNG key for this process."
            )
            return secrets.token_hex(32)
        return cleaned

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
