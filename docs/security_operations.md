# 🛡️ SECURITY OPERATIONS & GUIDELINES — AgroForecast

## Tài Liệu Đặc Tả An Toàn Thông Tin & Quy Chuẩn Bảo Mật Toàn Diện

> **Hệ thống:** AgroForecast — Hệ Thống Dự Báo Giá Nông Sản & Cảnh Báo Thị Trường  
> **Phiên bản:** v2.4.1 (Production & Academic Standard)  
> **Chuyên gia phụ trách:** Security Engineer & DevSecOps Lead  
> **Tiêu chuẩn tham chiếu:** OWASP Top 10:2021, CIS Benchmarks, NIST SP 800-53  
> **Cập nhật:** 10/09/2026  

---

## Mục lục

1. [Tổng Quan Kiến Trúc An Ninh Phòng Thủ Đa Tầng (Defense-in-Depth)](#1-tổng-quan-kiến-trúc-an-ninh-phòng-thủ-đa-tầng-defense-in-depth)
2. [Ma Trận Phòng Chống OWASP Top 10 Trong Python FastAPI & Next.js](#2-ma-trận-phòng-chống-owasp-top-10-trong-python-fastapi--nextjs)
   - [2.1. Phòng Chống Injection (SQLi & XSS)](#21-phòng-chống-injection-sqli--xss)
   - [2.2. Nhận Thực & Quản Lý Phiên (Broken Authentication - Passlib Bcrypt & JWT)](#22-nhận-thực--quản-lý-phiên-broken-authentication---passlib-bcrypt--jwt)
   - [2.3. Chống Rò Rỉ Dữ Liệu Nhạy Cảm (Sensitive Data Exposure - Pydantic Response Model & .env)](#23-chống-rò-rỉ-dữ-liệu-nhạy-cảm-sensitive-data-exposure---pydantic-response-model--env)
   - [2.4. Kiểm Soát Truy Cập Phân Quyền (Broken Access Control - RBAC Dependency Injection)](#24-kiểm-soát-truy-cập-phân-quyền-broken-access-control---rbac-dependency-injection)
   - [2.5. Cấu Hình Security Headers & Kiểm Soát CORS](#25-cấu-hình-security-headers--kiểm-soát-cors)
   - [2.6. Cơ Chế Giới Hạn Tần Suất Gọi API (Rate Limiting)](#26-cơ-chế-giới-hạn-tần-suất-gọi-api-rate-limiting)
3. [Quy Trình Kiểm Tra An Ninh Trước Khi Nộp Đồ Án](#3-quy-trình-kiểm-tra-an-ninh-trước-khi-nộp-đồ-án)
   - [3.1. Quét Lỗ Hổng Thư Viện Python Bằng `pip-audit`](#31-quét-lỗ-hổng-thư-viện-python-bằng-pip-audit)
   - [3.2. Quét Lỗ Hổng Frontend Bằng `npm audit`](#32-quét-lỗ-hổng-frontend-bằng-npm-audit)
   - [3.3. Bộ Kiểm Thử An Ninh Tự Động Pytest (Pytest Security Suite)](#33-bộ-kiểm-thử-an-ninh-tự-động-pytest-pytest-security-suite)
4. [Bảng Checklist Kiểm Toán An Ninh Pre-Submission (Readiness Verification)](#4-bảng-checklist-kiểm-toán-an-ninh-pre-submission-readiness-verification)

---

## 1. Tổng Quan Kiến Trúc An Ninh Phòng Thủ Đa Tầng (Defense-in-Depth)

Hệ sinh thái AgroForecast được thiết kế dựa trên nguyên tắc **Phòng thủ theo chiều sâu (Defense-in-Depth)** và **Đặc quyền tối thiểu (Principle of Least Privilege)**, bảo vệ toàn diện từ tầng mạng, cổng API, tầng ứng dụng đến tầng cơ sở dữ liệu:

```
[ Client: Next.js 14 Web App ]
         │ (HTTPS / TLS 1.3 - Secure Storage)
         ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 1. NETWORK & API GATEWAY PERIMETER                                     │
│    • CORS Policy: Giới hạn nghiêm ngặt domain được phép gọi API        │
│    • Security Headers: X-Frame-Options: DENY, nosniff, HSTS, CSP       │
│    • Rate Limiting: Sliding Window (25 req/phút Auth, 10 req/phút Task)│
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
┌──────────────────────────────────▼─────────────────────────────────────┐
│ 2. APPLICATION & AUTH LAYER (FastAPI)                                  │
│    • JSON Web Token (JWT) có hạn sử dụng, thuật toán HS256             │
│    • Dependency Injection: get_current_active_user & require_admin_role│
│    • Input Sanitization: Làm sạch dữ liệu đầu vào chống XSS            │
│    • Pydantic Schema response_model: Loại bỏ trường hashed_password   │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
┌──────────────────────────────────▼─────────────────────────────────────┐
│ 3. PERSISTENCE & DATA STORAGE LAYER                                    │
│    • SQLAlchemy 2.x ORM Parameterized Queries: Triệt tiêu SQL Injection│
│    • Băm mật khẩu bằng Passlib (Bcrypt 12 rounds) kèm Salt ngẫu nhiên  │
│    • Biến môi trường cô lập (.env): Ẩn giấu DB URL & tài khoản SMTP   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Ma Trận Phòng Chống OWASP Top 10 Trong Python FastAPI & Next.js

| Mã OWASP | Danh mục rủi ro | Giải pháp an ninh triển khai trong AgroForecast | Thành phần phụ trách |
|:---:|:---|:---|:---|
| **A01:2021** | **Broken Access Control** | FastAPI Dependency Injection (`get_current_active_user`, `require_admin_role`), bảo vệ các tác vụ nạp dữ liệu và huấn luyện lại. | `app/core/deps.py` |
| **A02:2021** | **Cryptographic Failures** | Che giấu thông tin kết nối SMTP và DB bằng file `.env`, mã hóa JWT HS256 có thời hạn. | `app/core/config.py` |
| **A03:2021** | **Injection (SQLi & XSS)** | 100% truy vấn qua SQLAlchemy ORM Parameterized Queries; hàm `sanitize_text()` lọc mã HTML/JS. | `app/core/security.py` |
| **A04:2021** | **Insecure Design** | Rate Limiting chống spam cào dữ liệu và tấn công vét cạn mật khẩu. | `app/core/security.py` |
| **A05:2021** | **Security Misconfiguration** | Middleware gắn đủ 6 HTTP Security Headers và cấu hình `CORSMiddleware` giới hạn domain. | `app/main.py` |
| **A07:2021** | **Identification & Authentication** | Băm mật khẩu bằng Passlib (Bcrypt 12 rounds) kèm Salt ngẫu nhiên, lưu token an toàn ở client. | `app/core/security.py` |
| **A08:2021** | **Sensitive Data Exposure** | Pydantic Schema `response_model` loại bỏ trường `hashed_password` khỏi toàn bộ output JSON. | `app/schemas/user.py` |

---

### 2.1. Phòng Chống Injection (SQLi & XSS)

> **Rủi ro:** Kẻ tấn công chèn các chuỗi SQL độc hại (`' OR '1'='1' --`) hoặc mã script (`<script>alert(1)</script>`) qua tham số API để chiếm quyền điều khiển CSDL hoặc chiếm phiên người dùng.

#### Giải pháp kỹ thuật triển khai:

1. **Sử dụng SQLAlchemy ORM Parameterized Queries — Tuyệt đối không ghép chuỗi SQL trần:**
   - 100% các câu truy vấn tương tác với CSDL PostgreSQL đều được thực thi thông qua SQLAlchemy ORM hoặc đối tượng `text()` có truyền tham số dạng bind parameter (`:parameter`).
   - Tham số đầu vào được engine database tự động escape và kiểm tra kiểu dữ liệu (strongly typed), triệt tiêu hoàn toàn nguy cơ SQL Injection.

```python
# ❌ NGUY HIỂM — LỖ HỔNG SQL INJECTION (TUYỆT ĐỐI KHÔNG DÙNG):
# Kẻ tấn công có thể truyền: code = "CA_PHE' OR '1'='1"
query = f"SELECT * FROM commodities WHERE code = '{user_input}'"
db.execute(text(query))

# ✅ CHUẨN AN TOÀN TRONG AGROFORECAST:
# Phương án 1: Sử dụng SQLAlchemy ORM Query API (Tự động tham số hóa)
commodity = db.query(Commodity).filter(Commodity.code == commodity_code).first()

# Phương án 2: Sử dụng Parameterized Bind Query khi viết SQL thuần
stmt = text("SELECT * FROM commodities WHERE code = :code")
result = db.execute(stmt, {"code": commodity_code}).first()
```

2. **Làm sạch dữ liệu đầu vào chống XSS (`sanitize_text`):**
   - Mọi dữ liệu dạng chuỗi do người dùng gửi lên (tên quy tắc cảnh báo, ghi chú admin) đều được xử lý qua hàm `sanitize_text()` trong `app/core/security.py` để loại bỏ toàn bộ các thẻ HTML độc hại trước khi lưu vào CSDL:

```python
# app/core/security.py
def sanitize_text(input_str: Optional[str]) -> str:
    """Loại bỏ thẻ HTML/Script nguy hiểm và mã hóa các ký tự đặc biệt"""
    if not input_str:
        return ""
    cleaned = re.sub(r'<[^>]*?>', '', input_str)
    return html.escape(cleaned.strip())
```

---

### 2.2. Nhận Thực & Quản Lý Phiên (Broken Authentication - Passlib Bcrypt & JWT)

> **Rủi ro:** Sử dụng thuật toán băm yếu (MD5, SHA1) dễ bị giải mã ngược qua Rainbow Table; token không có thời hạn hết hạn cho phép kẻ tấn công tái sử dụng phiên vô thời hạn.

#### Giải pháp kỹ thuật triển khai:

1. **Băm mật khẩu bằng Passlib (Bcrypt với 12 rounds):**
   - Hệ thống sử dụng thư viện `passlib` kết hợp thuật toán `bcrypt` với chi phí tính toán (cost factor / rounds) là **12**.
   - Mỗi mật khẩu được tự động tạo một chuỗi muối ngẫu nhiên (salt) độc nhất, khiến hai mật khẩu giống nhau vẫn sinh ra hai chuỗi băm hoàn toàn khác biệt.

```python
# app/core/security.py
from passlib.context import CryptContext

# Cấu hình CryptContext chuẩn Bcrypt với cost factor = 12 rounds
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)

def get_password_hash(password: str) -> str:
    """Tạo salt ngẫu nhiên và băm mật khẩu bằng Passlib Bcrypt (12 rounds)"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Kiểm tra mật khẩu khớp với hash trong CSDL (Kháng Timing Attack)"""
    return pwd_context.verify(plain_password, hashed_password)
```

2. **JSON Web Token (JWT) có hạn sử dụng (Expiration):**
   - Token được ký bằng thuật toán đối xứng an toàn **HS256** với khóa bí mật `SECRET_KEY` đạt độ dài entropy cao.
   - Payload chứa thông tin thời điểm phát hành (`iat`) và thời điểm hết hạn bắt buộc (`exp`):
     ```python
     expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
     to_encode = {"exp": expire, "sub": str(user_id), "role": user_role, "iat": datetime.now(timezone.utc)}
     encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
     ```
   - Khi token hết hạn, middleware trả về ngay lập tức mã lỗi `401 Unauthorized` yêu cầu đăng nhập lại.

3. **Lưu trữ token an toàn ở Client (Next.js):**
   - Token được lưu trữ trong client state hoặc Cookie có cờ `Secure`, `SameSite=Strict` nhằm ngăn chặn tấn công đánh cắp phiên qua XSS và CSRF.
   - Cơ chế Đăng xuất (Logout) xóa sạch token khỏi bộ nhớ trình duyệt và hủy context người dùng.

---

### 2.3. Chống Rò Rỉ Dữ Liệu Nhạy Cảm (Sensitive Data Exposure - Pydantic Response Model & .env)

> **Rủi ro:** API vô tình trả về trường mật khẩu băm (`hashed_password`) trong dữ liệu người dùng, hoặc mã nguồn vô tình làm lộ thông tin kết nối CSDL và tài khoản email gửi thông báo lên GitHub.

#### Giải pháp kỹ thuật triển khai:

1. **Sử dụng Pydantic Schema `response_model` loại bỏ trường `hashed_password`:**
   - Trong FastAPI, mọi endpoint trả về thông tin người dùng đều được định tuyến qua `response_model=UserResponse`.
   - Schema `UserResponse` chỉ chọn lọc các trường dữ liệu an toàn, **tuyệt đối không khai báo trường `hashed_password`**, đảm bảo dù model CSDL có chứa hash thì dữ liệu JSON trả về cũng bị lược bỏ triệt để.

```python
# app/schemas/user.py
from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

class UserResponse(BaseModel):
    """Schema công khai — Loại trừ triệt để trường hashed_password"""
    id: int
    email: EmailStr
    full_name: str
    role: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# app/api/v1/endpoints/auth.py
@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: User = Depends(get_current_active_user)):
    """Trả về profile — Pydantic response_model tự động lọc bỏ hashed_password"""
    return current_user
```

2. **Che giấu thông tin kết nối SMTP và DB bằng file `.env`:**
   - Chuỗi kết nối CSDL PostgreSQL (`DATABASE_URL`), thông tin đăng nhập máy chủ thư điện tử (`SMTP_USER`, `SMTP_PASSWORD`) và chuỗi bí mật `SECRET_KEY` được đọc tự động qua `pydantic-settings` từ file `.env` độc lập.
   - File `.env` và `.env.local` đã được cấu hình loại trừ trong file [.gitignore](file:///d:/DA_TN/.gitignore):
     ```gitignore
     # .gitignore
     .env
     .env.local
     .env.*.local
     *.pem
     *.key
     ```
   - Chỉ lưu file mẫu `.env.example` với các giá trị giữ chỗ trên GitHub để đảm bảo an toàn tuyệt đối.

---

### 2.4. Kiểm Soát Truy Cập Phân Quyền (Broken Access Control - RBAC Dependency Injection)

> **Rủi ro:** Người dùng không có thẩm quyền tự ý gửi request kích hoạt cào dữ liệu làm nghẽn băng thông, hoặc kích hoạt huấn luyện lại mô hình (retrain) làm cạn kiệt tài nguyên CPU/GPU máy chủ.

#### Giải pháp kỹ thuật triển khai:

1. **Dependency Injection trong FastAPI (`get_current_active_user`, `require_admin_role`):**
   - FastAPI cung cấp cơ chế Dependency Injection mạnh mẽ giúp xác thực và kiểm tra vai trò trước khi request đi vào thân hàm xử lý logic:

```python
# app/core/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """Giải mã JWT và trích xuất thông tin người dùng từ Database"""
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không hợp lệ hoặc đã hết hạn",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Người dùng không tồn tại")
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Xác minh tài khoản đang ở trạng thái kích hoạt (Active)"""
    # Nếu tài khoản bị vô hiệu hóa, lập tức chặn truy cập
    if hasattr(current_user, "is_active") and not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tài khoản đã bị vô hiệu hóa")
    return current_user

def require_admin_role(current_user: User = Depends(get_current_active_user)) -> User:
    """Chặn toàn bộ người dùng không mang vai trò admin"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Quyền truy cập bị từ chối! Thao tác này chỉ dành cho Quản trị viên (Admin)."
        )
    return current_user
```

2. **Áp dụng bảo vệ các task nạp dữ liệu và huấn luyện lại:**
   - Các endpoint kích hoạt nạp dữ liệu cào tự động và huấn luyện lại AI được gắn chặt với dependency `require_admin_role`:

```python
# app/api/v1/endpoints/admin.py
@router.post("/tasks/scrape")
def trigger_scrape_task(
    days: int = 7,
    current_user: User = Depends(require_admin_role), # 🛡️ BẢO VỆ CHẶT CHẼ
    db: Session = Depends(get_db)
):
    """Chỉ Admin mới có quyền kích hoạt tiến trình cào dữ liệu"""
    return {"message": "Tiến trình cào dữ liệu đã được khởi chạy."}

@router.post("/tasks/retrain")
def trigger_retrain_task(
    commodity_id: int,
    current_user: User = Depends(require_admin_role), # 🛡️ BẢO VỆ CHẶT CHẼ
    db: Session = Depends(get_db)
):
    """Chỉ Admin mới có quyền kích hoạt huấn luyện lại mô hình AI"""
    return {"message": "Tiến trình huấn luyện lại mô hình đã bắt đầu."}
```

---

### 2.5. Cấu Hình Security Headers & Kiểm Soát CORS

> **Rủi ro:** Trang web bị nhúng trộm vào iframe độc hại (Clickjacking), hoặc các trang web bên thứ ba gửi request chéo miền đánh cắp thông tin người dùng (Cross-Origin Resource Sharing).

#### Giải pháp kỹ thuật triển khai:

1. **Cấu hình `CORSMiddleware` hạn chế domain được phép gọi API:**
   - Trong `app/main.py`, hệ thống không mở tự do cho mọi nguồn (`*`) mà giới hạn nghiêm ngặt theo danh sách tên miền tin cậy của Frontend Next.js:

```python
# app/main.py
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  # ["http://localhost:3000", "http://127.0.0.1:3000"]
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)
```

2. **Gắn 6 HTTP Security Headers bắt buộc theo chuẩn OWASP (`SecurityHeadersMiddleware`):**
   - Mọi response trả về từ FastAPI đều được middleware gắn thêm các tiêu đề bảo vệ:

| HTTP Header | Giá trị cấu hình | Tác dụng bảo mật |
|---|---|---|
| `X-Content-Type-Options` | `nosniff` | Chặn trình duyệt tự suy đoán MIME type, ngăn thực thi mã độc giả dạng ảnh. |
| `X-Frame-Options` | `DENY` | Chặn hoàn toàn việc nhúng AgroForecast vào thẻ `<iframe>`, triệt tiêu Clickjacking. |
| `X-XSS-Protection` | `1; mode=block` | Kích hoạt bộ lọc chống XSS của trình duyệt; ngừng render khi phát hiện tấn công. |
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` | Ép buộc sử dụng kết nối HTTPS an toàn trong vòng 1 năm. |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | Ngăn chặn việc để lộ tham số nhạy cảm của URL sang các liên kết bên ngoài. |
| `Permissions-Policy` | `geolocation=(), camera=(), microphone=()` | Vô hiệu hóa quyền truy cập micro, webcam và vị trí địa lý của người dùng. |

---

### 2.6. Cơ Chế Giới Hạn Tần Suất Gọi API (Rate Limiting)

> **Rủi ro:** Kẻ tấn công sử dụng công cụ tự động gửi hàng nghìn request/giây để cào trộm toàn bộ dữ liệu lịch sử giá, hoặc tấn công dò mật khẩu (Brute-Force Attack) vào endpoint `/auth/login`.

#### Giải pháp kỹ thuật triển khai:

- Triển khai lớp `RateLimiter` theo thuật toán **Sliding Window (Cửa sổ trượt)** lưu trong bộ nhớ (In-Memory) với cơ chế khóa luồng an toàn (Thread-safe Lock):
  - **Auth Rate Limiter:** Giới hạn tối đa **25 requests / 60 giây** cho mỗi địa chỉ IP trên các endpoint `/auth/login` và `/auth/register`.
  - **Task Rate Limiter:** Giới hạn tối đa **10 requests / 60 giây** trên các tác vụ nặng như `/admin/tasks/scrape` và `/admin/tasks/retrain`.
- Khi vượt ngưỡng cho phép, hệ thống trả về mã lỗi HTTP `429 Too Many Requests` và yêu cầu client tạm dừng:

```python
# app/core/security.py
class RateLimiter:
    """Thread-safe Sliding Window Rate Limiter"""
    def __init__(self, max_requests: int = 25, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._records = defaultdict(list)
        self._lock = Lock()

    def is_rate_limited(self, key: str) -> bool:
        now = time.time()
        with self._lock:
            valid_ts = [ts for ts in self._records[key] if now - ts < self.window_seconds]
            if len(valid_ts) >= self.max_requests:
                self._records[key] = valid_ts
                return True
            valid_ts.append(now)
            self._records[key] = valid_ts
            return False
```

---

## 3. Quy Trình Kiểm Tra An Ninh Trước Khi Nộp Đồ Án

Trước khi đóng gói sản phẩm và nộp mã nguồn cho Giảng viên Hướng dẫn hoặc Hội đồng đánh giá, sinh viên thực hiện quy trình rà soát an ninh 3 bước độc lập:

```
┌────────────────────────┐     ┌────────────────────────┐     ┌────────────────────────┐
│  Bước 1: pip-audit     │ ──► │  Bước 2: npm audit     │ ──► │  Bước 3: Pytest Suite  │
│  (Quét thư viện Python)│     │  (Quét Frontend JS/CSS)│     │  (Kiểm thử an ninh)    │
└────────────────────────┘     └────────────────────────┘     └────────────────────────┘
```

---

### 3.1. Quét Lỗ Hổng Thư Viện Python Bằng `pip-audit`

`pip-audit` là công cụ quét bảo mật tiêu chuẩn cho hệ sinh thái Python, kiểm tra mã CVE dựa trên cơ sở dữ liệu PyPA Advisory Database.

#### Các bước thực hiện chi tiết:

1. **Mở PowerShell và kích hoạt môi trường ảo Backend:**
   ```powershell
   cd d:\DA_TN\backend
   .\venv\Scripts\activate
   ```

2. **Cài đặt công cụ `pip-audit`:**
   ```powershell
   pip install pip-audit
   ```

3. **Thực thi quét kiểm tra toàn bộ thư viện phụ thuộc:**
   ```powershell
   # Quét toàn bộ môi trường ảo hiện tại
   pip-audit

   # Hoặc quét trực tiếp file requirements.txt
   pip-audit -r requirements.txt
   ```

4. **Xuất báo cáo định dạng JSON làm minh chứng báo cáo:**
   ```powershell
   pip-audit -r requirements.txt --format json --output audit-python-report.json
   ```

5. **Xử lý khi phát hiện lỗ hổng:**
   - Nếu có gói thư viện bị cảnh báo lỗ hổng đã biết, chạy lệnh sửa tự động:
     ```powershell
     pip-audit --fix
     ```
   - Cập nhật lại file `requirements.txt`:
     ```powershell
     pip freeze > requirements.txt
     ```

---

### 3.2. Quét Lỗ Hổng Frontend Bằng `npm audit`

Môi trường JavaScript có cấu trúc phụ thuộc phân cấp phức tạp. Công cụ `npm audit` rà soát toàn bộ cây phụ thuộc trong `package-lock.json` với GitHub Advisory Database.

#### Các bước thực hiện chi tiết:

1. **Di chuyển vào thư mục Frontend:**
   ```powershell
   cd d:\DA_TN\frontend
   ```

2. **Chạy lệnh quét an ninh:**
   ```powershell
   npm audit
   ```
   *Màn hình sẽ hiển thị tổng số lỗ hổng phân theo 5 mức độ: `info`, `low`, `moderate`, `high`, `critical`.*

3. **Tự động vá các lỗi không gây xung đột (Non-breaking):**
   ```powershell
   npm audit fix
   ```

4. **Trường hợp xuất hiện lỗi nghiêm trọng (Critical/High):**
   - Xem chi tiết đường dẫn phụ thuộc bằng lệnh:
     ```powershell
     npm audit --json > audit-frontend-report.json
     ```
   - Nếu bản vá yêu cầu nâng cấp phiên bản lớn và không gây lỗi giao diện, chạy:
     ```powershell
     npm audit fix --force
     ```

---

### 3.3. Bộ Kiểm Thử An Ninh Tự Động Pytest (Pytest Security Suite)

Hệ thống đã xây dựng sẵn bộ kiểm thử an ninh chuyên biệt tại `backend/tests/test_security_phase7.py` kiểm tra thực tế:
- Sự hiện diện đầy đủ của 6 Security Headers.
- Khả năng băm và xác thực mật khẩu của Bcrypt 12 rounds.
- Khả năng loại bỏ mã độc XSS qua hàm `sanitize_text()`.
- Cơ chế chặn request vượt ngưỡng của `RateLimiter`.
- Cơ chế chặn Token JWT bị can thiệp chữ ký (tampering) hoặc hết hạn.
- Cơ chế phòng thủ SQL Injection trong truy vấn nông sản.

#### Lệnh thực thi:

```powershell
cd d:\DA_TN\backend
pytest tests/test_security_phase7.py -v
```

#### Kết quả thực tế kỳ vọng:
```text
tests/test_security_phase7.py::test_security_headers_present PASSED           [ 16%]
tests/test_security_phase7.py::test_password_hashing_and_verification PASSED  [ 33%]
tests/test_security_phase7.py::test_sanitize_text_xss_protection PASSED       [ 50%]
tests/test_security_phase7.py::test_rate_limiter_mechanism PASSED             [ 66%]
tests/test_security_phase7.py::test_jwt_tampering_and_expiration PASSED       [ 83%]
tests/test_security_phase7.py::test_sql_injection_defense_in_commodity_query PASSED [100%]

============================== 6 passed in 1.48s ==============================
```

---

## 4. Bảng Checklist Kiểm Toán An Ninh Pre-Submission (Readiness Verification)

Bảng nghiệm thu an ninh cuối cùng trước khi bàn giao đồ án:

| STT | Tiêu chí kiểm toán an ninh | Hiện trạng | Minh chứng kỹ thuật |
|:---:|:---|:---:|:---|
| 1 | **Chống SQL Injection (SQLi)** | ✅ ĐẠT | 100% truy vấn dùng SQLAlchemy ORM Parameterized Queries; không ghép chuỗi SQL trần. |
| 2 | **Băm mật khẩu người dùng** | ✅ ĐẠT | Sử dụng Passlib Bcrypt (12 rounds) kèm Salt ngẫu nhiên; không lưu mật khẩu thô. |
| 3 | **Bảo mật phiên đăng nhập** | ✅ ĐẠT | JWT token thuật toán HS256 có thời hạn (`exp`); lưu trữ an toàn tại client. |
| 4 | **Chống lộ lọt dữ liệu nhạy cảm** | ✅ ĐẠT | Pydantic Schema `response_model` loại trừ triệt để trường `hashed_password`. |
| 5 | **Bảo vệ Secrets & Môi trường** | ✅ ĐẠT | File `.env` chứa chuỗi kết nối DB và SMTP nằm ngoài Git thông qua `.gitignore`. |
| 6 | **Phân quyền truy cập (RBAC)** | ✅ ĐẠT | Dependency Injection (`get_current_active_user`, `require_admin_role`) chặn các tác vụ nạp dữ liệu và retrain. |
| 7 | **Security Headers & CORS** | ✅ ĐẠT | Cấu hình `CORSMiddleware` giới hạn domain; gắn đủ 6 header (`nosniff`, `DENY`, `HSTS`, ...). |
| 8 | **Chống Spam & Brute-Force** | ✅ ĐẠT | Bộ đệm trượt `RateLimiter` 25 req/phút cho Auth và 10 req/phút cho tác vụ hệ thống. |
| 9 | **Rà soát thư viện Python** | ✅ ĐẠT | Quét sạch lỗ hổng qua công cụ `pip-audit`. |
| 10 | **Rà soát thư viện Frontend** | ✅ ĐẠT | Quét sạch lỗ hổng qua công cụ `npm audit`. |
