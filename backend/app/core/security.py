import bcrypt
import jwt
import re
import time
import html
from collections import defaultdict
from threading import Lock
from datetime import datetime, timedelta, timezone
from typing import Optional, Any, Union, Dict, List
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.config import settings

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Kiểm tra mật khẩu nhập vào khớp với hash trong DB"""
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False

def get_password_hash(password: str) -> str:
    """Tạo salt và băm mật khẩu bằng Bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def create_access_token(subject: Union[str, Any], role: str = "analyst", expires_delta: Optional[timedelta] = None) -> str:
    """Tạo JWT access token chứa định danh (sub), vai trò (role) và thời hạn (exp)"""
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "role": role,
        "iat": now
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    """Giải mã và xác thực tính hợp lệ của JWT token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except Exception:
        return None

def sanitize_text(input_str: Optional[str]) -> str:
    """Sanitize and escape user input strings to mitigate XSS and injection attacks"""
    if not input_str:
        return ""
    # Strip dangerous HTML/script tags and escape special chars
    cleaned = re.sub(r'<[^>]*?>', '', input_str)
    return html.escape(cleaned.strip())

class RateLimiter:
    """
    Thread-safe In-Memory Sliding Window Rate Limiter
    Prevents brute-force, dictionary attacks, and endpoint abuse
    """
    def __init__(self, max_requests: int = 20, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._records: Dict[str, List[float]] = defaultdict(list)
        self._lock = Lock()

    def is_rate_limited(self, key: str) -> bool:
        """Kiểm tra xem key (IP hoặc User identifier) có bị vượt ngưỡng request hay không"""
        now = time.time()
        with self._lock:
            # Dọn dẹp các timestamp cũ hơn cửa sổ thời gian
            valid_timestamps = [ts for ts in self._records[key] if now - ts < self.window_seconds]
            if len(valid_timestamps) >= self.max_requests:
                self._records[key] = valid_timestamps
                return True
            valid_timestamps.append(now)
            self._records[key] = valid_timestamps
            return False

    def reset(self, key: Optional[str] = None):
        """Reset bộ nhớ rate limit cho key hoặc toàn bộ"""
        with self._lock:
            if key:
                self._records.pop(key, None)
            else:
                self._records.clear()

# Khởi tạo instance Rate Limiter
auth_rate_limiter = RateLimiter(max_requests=25, window_seconds=60)
task_rate_limiter = RateLimiter(max_requests=10, window_seconds=60)

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware bổ sung các HTTP Response Headers bảo mật theo khuyến nghị OWASP Top 10
    """
    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        
        # 1. Chặn MIME-sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"
        
        # 2. Chặn Clickjacking (Iframe embedding)
        response.headers["X-Frame-Options"] = "DENY"
        
        # 3. Kích hoạt bộ lọc XSS trình duyệt
        response.headers["X-XSS-Protection"] = "1; mode=block"
        
        # 4. Enforce HTTPS via HSTS
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        # 5. Bảo vệ thông tin Referrer
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # 6. Hạn chế quyền phần cứng trình duyệt
        response.headers["Permissions-Policy"] = "geolocation=(), camera=(), microphone=()"
        
        return response
