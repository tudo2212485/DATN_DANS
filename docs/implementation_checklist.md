# Checklist Triển Khai (Implementation Checklist) - Toàn Bộ 7 Phase

Đánh dấu `[x]` khi hoàn thành các đầu việc cho từng Phase.

## Phase 1: Setup & Architecture
- [x] Khởi tạo thư mục `docs/` chứa tài liệu dự án đầy đủ 12 file.
- [x] Cài đặt FastAPI, Next.js và các dependencies cơ bản.
- [x] Cấu hình ESLint, Prettier (Frontend) & Ruff/Pytest (Backend).
- [x] Cấu hình `.gitignore`, `requirements.txt`, `package.json`.
- [x] Tạo file `.env.example` với các biến môi trường cần thiết.
- [x] Setup kết nối CSDL PostgreSQL với SQLAlchemy & Asyncpg.
- [x] Setup Pytest cho backend và cấu hình `pytest.ini`.

## Phase 2: Database & Core API (Auth & RBAC)
- [x] Thiết kế và vẽ sơ đồ CSDL (ERD).
- [x] Viết các SQLAlchemy Models (`User`, `Commodity`, `PriceHistory`, `Forecast`, `AlertRule`, `AlertLog`).
- [x] Viết API Đăng ký & Đăng nhập (`/auth/login`, `/auth/me`).
- [x] Phân quyền người dùng (Role: `admin`, `analyst`, `user`).
- [x] Áp dụng Passlib (Bcrypt) băm mật khẩu & JWT authentication.
- [x] Viết Unit Test cho module xác thực và phân quyền (10/10 tests pass 100%).

## Phase 3: Machine Learning & Data Pipeline
- [x] Xây dựng crawler thu thập dữ liệu (YFinance, BeautifulSoup).
- [x] Viết script tiền xử lý dữ liệu (Pandas, Numpy, Outlier IQR).
- [x] Cấu hình APScheduler chạy cào dữ liệu định kỳ và đánh giá cảnh báo.
- [x] Viết API kích hoạt Scraper chạy ngầm (`/admin/tasks/scrape`).

## Phase 4: AI/ML Models & Prediction API
- [x] Tích hợp 4 mô hình dự báo (Prophet, XGBoost, PyTorch/LSTM, ARIMA).
- [x] Đóng gói và lưu trữ model weights trong `ml_pipeline/saved_models/`.
- [x] Đánh giá sai số mô hình (RMSE, MAE, MAPE, R2 Score).
- [x] Xây dựng API trả về dữ liệu dự báo & so sánh mô hình (`/forecast`, `/forecast/compare/{id}`).

## Phase 5: Admin Dashboard Development (Quản Trị)
- [x] Xây dựng trang Tổng quan hệ thống (`/dashboard/overview`).
- [x] Xây dựng giao diện kích hoạt cào dữ liệu thủ công, bảng Crawler Logs, Import/Export file CSV giá (`/dashboard/data-control`).
- [x] Xây dựng giao diện Thêm/Sửa/Xóa giá nông sản thủ công.
- [x] Xây dựng trang quản lý mô hình AI, bộ chọn Active Model Switcher & kích hoạt Retrain model (`/dashboard/ml-models`).
- [x] Xây dựng trang quản lý người dùng, đổi Role & Khóa/Mở khóa tài khoản (`/dashboard/users`).
- [x] Phân tách layout Dashboard Full-screen tối chuyên dụng, chặn truy cập nếu không có quyền Admin/Analyst.

## Phase 6: Public User UI Development (Nông Dân & Thương Lái)
- [x] Xây dựng Quick Search & Category/Region filter bar (`QuickSearchBar.tsx`).
- [x] Xây dựng Hot Movers Banner hiển thị Top 3 nông sản biến động mạnh nhất (`HotMoversBanner.tsx`).
- [x] Xây dựng Trang chi tiết nông sản (`/commodities/[id]`) với Interactive Composed Chart (Lịch sử + Dự báo nét đứt + Dải biên độ tin cậy 95% Confidence Interval).
- [x] Xây dựng AI Insight Summary Card đưa ra khuyến nghị thực tế cho nông dân và thương lái (`AIInsightCard.tsx`).
- [x] Xây dựng Trang so sánh thị trường & đối sánh giá vùng miền (`/compare`).
- [x] Tối ưu giao diện Responsive cho điện thoại di động & máy tính bảng.

## Phase 7: Security Audit & Final Release
- [x] Rà soát bảo mật OWASP Top 10 (100% Parameterized qua SQLAlchemy ORM, Rate Limiting, Security Headers).
- [x] Cấu hình SecurityHeadersMiddleware (HSTS, nosniff, DENY clickjacking, XSS protection).
- [x] Tích hợp cơ chế RateLimiter chống brute force / credential stuffing trên auth endpoints.
- [x] Xây dựng bộ kiểm thử an ninh `test_security_phase7.py` (6/6 tests pass).
- [x] Build và kiểm thử thành công toàn bộ hệ thống (`pytest` 42/42 tests pass 100%, Next.js build pass 15/15 static/dynamic routes).
- [x] Hoàn thiện Báo cáo kiểm toán bảo mật `docs/security_audit_report.md`.
