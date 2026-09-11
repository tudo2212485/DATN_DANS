# Phase 2 Specification: Thiết Kế CSDL, ORM Models & Xác Thực Phân Quyền (Auth & RBAC)

## 1. Mục Tiêu (Objective)
Thiết kế CSDL PostgreSQL, tạo các mô hình dữ liệu (SQLAlchemy ORM Models), xây dựng hệ thống Xác thực (Authentication) với Bcrypt + JWT và Phân quyền theo vai trò (Role-Based Access Control - RBAC) tuân thủ OWASP Top 10.

## 2. Thiết Kế Cơ Sở Dữ Liệu (Database Schema Design)

### 2.1 Bảng Users (`users`)
- `id`: Integer (Primary Key, Auto-increment)
- `email`: String(150) (Unique, Indexed, Nullable=False)
- `password_hash`: String(255) (Bcrypt hashed, Nullable=False)
- `full_name`: String(150) (Nullable=False)
- `role`: String(50) (Mặc định: `analyst`, Hỗ trợ: `admin`, `analyst`, `user`)
- `created_at`: DateTime(timezone=True)
- `updated_at`: DateTime(timezone=True)

### 2.2 Bảng Commodities (`commodities`)
- `id`: Integer (Primary Key, Index)
- `code`: String(50) (Unique, Index)
- `name`: String(150) (Nullable=False)
- `category`: String(50)
- `unit`: String(30)
- `region`: String(100)
- `description`: Text

### 2.3 Bảng Price History (`price_history`)
- `id`: BigInteger (Primary Key)
- `commodity_id`: Integer (ForeignKey -> `commodities.id`, ondelete="CASCADE")
- `record_date`: Date (Indexed)
- `price`: Numeric(14, 2)
- `price_min`: Numeric(14, 2)
- `price_max`: Numeric(14, 2)
- `volume`: Numeric(16, 2)
- `source`: String(100)

### 2.4 Bảng Forecasts (`forecasts`)
- `id`: BigInteger (Primary Key)
- `commodity_id`: Integer (ForeignKey -> `commodities.id`)
- `model_name`: String(50) (`LSTM`, `Prophet`, `ARIMA`, `XGBoost`)
- `forecast_date`: Date
- `predicted_price`: Numeric(14, 2)
- `lower_ci`: Numeric(14, 2) (95% CI Lower)
- `upper_ci`: Numeric(14, 2) (95% CI Upper)
- `mae`, `rmse`, `mape`, `r2`: Numeric(10, 4)

---

## 3. Đặc Tả API Xác Thực & Phân Quyền (Auth & RBAC Endpoints)
- `POST /api/v1/auth/register`: Đăng ký tài khoản người dùng mới (Validate EmailStr, mật khẩu tối thiểu 6 ký tự).
- `POST /api/v1/auth/login`: Đăng nhập, nhận Bearer Access Token (JWT).
- `GET /api/v1/auth/me`: Lấy thông tin cá nhân của User đang đăng nhập qua Token.

## 4. Tiêu Chuẩn Bảo Mật OWASP (Security Specs)
- **Mã Hóa Mật Khẩu (Bcrypt):** Băm mật khẩu bằng `bcrypt.hashpw` với `gensalt()`. Không lưu trữ mật khẩu gốc dưới bất kỳ hình thức nào.
- **Xác Thực JWT:** 
  - Mã hóa Token bằng `HS256` với `SECRET_KEY` từ Settings.
  - Token chứa định danh `sub` (User ID), `role` (Phân quyền) và thời hạn `exp`.
- **Phòng Chống SQL Injection:** 100% truy vấn DB sử dụng SQLAlchemy ORM.
- **Input Validation:** Sử dụng Pydantic `EmailStr` và `Field(min_length=...)` để chặn dữ liệu đầu vào không hợp lệ.

## 5. Kết Quả Kiểm Thử TDD (Test-Driven Development)
Bộ test `tests/test_auth.py` và `tests/test_commodities.py` bao phủ đầy đủ:
- [x] Đăng ký tài khoản thành công -> `201 Created`.
- [x] Đăng ký email trùng lặp -> `400 Bad Request`.
- [x] Đăng ký email sai định dạng / mật khẩu ngắn -> `422 Unprocessable Entity`.
- [x] Đăng nhập đúng tài khoản -> `200 OK` + Access Token.
- [x] Đăng nhập sai mật khẩu / email không tồn tại -> `401 Unauthorized`.
- [x] Gọi `/auth/me` với Token hợp lệ -> `200 OK`.
- [x] Gọi `/auth/me` không có Token hoặc Token sai -> `401 Unauthorized`.
- [x] Gọi API Admin `/commodities` (POST/PUT/DELETE) không có quyền Admin -> `401/403 Forbidden`.

## 6. Sản Phẩm Bàn Giao (Deliverables)
1. ORM Models hoàn chỉnh trong [`app/models/models.py`](file:///d:/DA_TN/backend/app/models/models.py).
2. Module Security & Auth trong [`app/core/security.py`](file:///d:/DA_TN/backend/app/core/security.py) và [`app/api/v1/endpoints/auth.py`](file:///d:/DA_TN/backend/app/api/v1/endpoints/auth.py).
3. Trang Đăng nhập Frontend kết nối API động trong [`frontend/src/app/login/page.tsx`](file:///d:/DA_TN/frontend/src/app/login/page.tsx).
4. Bộ test suite 100% Passed (17/17 tests).
