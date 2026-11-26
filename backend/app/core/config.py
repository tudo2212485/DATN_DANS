import hashlib
import json
import logging
import os
import secrets
from typing import Annotated, List
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

logger = logging.getLogger("app.core.config")

# SHA-256 digests of known insecure tutorial/placeholder secrets (never store plaintext secrets in code)
_INSECURE_SECRET_SHA256 = {
    "570dad43de1af4c925f92c16a68a50936da42b7dd6fdeb24850507a1199aac89",
    hashlib.sha256(b"CHANGE_ME_GENERATE_WITH_OPENSSL_RAND_HEX_32").hexdigest(),
    hashlib.sha256(b"secret").hexdigest(),
    hashlib.sha256(b"changeme").hexdigest(),
}

_DEFAULT_SQLITE_URL = "sqlite:///./agroforecast_dev.db"
_DEFAULT_SQLITE_ASYNC_URL = "sqlite+aiosqlite:///./agroforecast_dev.db"

DEFAULT_CORS_ORIGINS: List[str] = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]


def normalize_database_url(url: str, *, is_async: bool = False) -> str:
    """Normalize PostgreSQL URLs for SQLAlchemy sync (psycopg2) and async (asyncpg), including Neon SSL."""
    cleaned = (url or "").strip()
    if not cleaned or cleaned.startswith("sqlite"):
        return cleaned

    parsed = urlsplit(cleaned)
    scheme = parsed.scheme.lower()
    is_pg = scheme in ("postgres", "postgresql", "postgresql+psycopg2", "postgresql+asyncpg")
    if not is_pg:
        return cleaned

    use_asyncpg = is_async or scheme == "postgresql+asyncpg"
    if use_asyncpg:
        new_scheme = "postgresql+asyncpg"
    elif scheme == "postgres":
        new_scheme = "postgresql"
    else:
        new_scheme = parsed.scheme

    hostname = (parsed.hostname or "").lower()
    is_neon = hostname.endswith(".neon.tech")
    query_pairs = parse_qsl(parsed.query, keep_blank_values=True)

    if use_asyncpg:
        normalized_pairs = []
        has_ssl = any(k.lower() == "ssl" for k, _ in query_pairs)
        for key, val in query_pairs:
            lower_key = key.lower()
            if lower_key == "channel_binding":
                continue
            if lower_key == "sslmode":
                if not has_ssl:
                    normalized_pairs.append(("ssl", val))
                    has_ssl = True
                continue
            normalized_pairs.append((key, val))
        if is_neon and not has_ssl:
            normalized_pairs.append(("ssl", "require"))
    else:
        normalized_pairs = []
        has_sslmode = any(k.lower() == "sslmode" for k, _ in query_pairs)
        for key, val in query_pairs:
            lower_key = key.lower()
            if lower_key == "ssl":
                if not has_sslmode:
                    normalized_pairs.append(("sslmode", val))
                    has_sslmode = True
                continue
            normalized_pairs.append((key, val))
        if is_neon and not has_sslmode:
            normalized_pairs.append(("sslmode", "require"))

    new_query = urlencode(normalized_pairs)
    return urlunsplit((new_scheme, parsed.netloc, parsed.path, new_query, parsed.fragment))


class Settings(BaseSettings):
    PROJECT_NAME: str = "AgroForecast - Hệ thống Dự báo Giá Nông sản"
    VERSION: str = "2.4.1"
    API_V1_STR: str = "/api/v1"

    # JWT Auth: load from backend/.env; fallback to ephemeral CSPRNG key in isolated dev/test only
    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Database Configuration (credentials MUST be supplied via backend/.env, never hardcoded in source)
    DATABASE_URL: str = _DEFAULT_SQLITE_URL
    DATABASE_URL_ASYNC: str = _DEFAULT_SQLITE_ASYNC_URL

    # CORS Origins (Explicit whitelist; supports comma-separated env string or JSON list)
    CORS_ORIGINS: Annotated[List[str], NoDecode] = DEFAULT_CORS_ORIGINS.copy()

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

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: object) -> List[str]:
        if value is None:
            return list(DEFAULT_CORS_ORIGINS)
        if isinstance(value, (list, tuple, set)):
            parsed = [str(item).strip().rstrip("/") for item in value if str(item).strip()]
            return parsed or list(DEFAULT_CORS_ORIGINS)
        if isinstance(value, str):
            raw = value.strip()
            if not raw:
                return list(DEFAULT_CORS_ORIGINS)
            if raw.startswith("["):
                try:
                    loaded = json.loads(raw)
                    if isinstance(loaded, list):
                        parsed = [str(item).strip().rstrip("/") for item in loaded if str(item).strip()]
                        return parsed or list(DEFAULT_CORS_ORIGINS)
                except json.JSONDecodeError:
                    pass
            parsed = [item.strip().rstrip("/") for item in raw.split(",") if item.strip()]
            return parsed or list(DEFAULT_CORS_ORIGINS)
        return list(DEFAULT_CORS_ORIGINS)

    @model_validator(mode="after")
    def normalize_database_urls(self) -> "Settings":
        self.DATABASE_URL = normalize_database_url(self.DATABASE_URL, is_async=False)
        if (
            self.DATABASE_URL_ASYNC == _DEFAULT_SQLITE_ASYNC_URL
            and self.DATABASE_URL.startswith(("postgresql", "postgres"))
        ):
            self.DATABASE_URL_ASYNC = normalize_database_url(self.DATABASE_URL, is_async=True)
        else:
            self.DATABASE_URL_ASYNC = normalize_database_url(self.DATABASE_URL_ASYNC, is_async=True)
        return self

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
