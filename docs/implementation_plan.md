# Kế Hoạch Triển Khai (Implementation Plan) - Cập Nhật

Tài liệu này mô tả chi tiết kiến trúc, công nghệ, tiêu chuẩn bảo mật và các giai đoạn triển khai của dự án Hệ thống Thu thập, Dự báo & Tra cứu Giá Hàng hóa.

## 1. Công Nghệ & Kiến Trúc (Tech Stack & Architecture)

Dự án được tổ chức theo kiến trúc **Client-Server (RESTful API)** kết hợp với các dịch vụ học máy (Machine Learning).

- **Frontend (Client):** 
  - **Framework:** Next.js (React)
  - **Ngôn ngữ:** TypeScript
  - **Styling:** Tailwind CSS
  - **Tách biệt Giao diện:** 
    1. **Admin Control Panel (`/dashboard`):** Dành cho Quản trị viên & Nhà phân tích (Quản lý Bot, Quản lý ML, Quản lý dữ liệu).
    2. **Public User UI (`/`):** Dành cho Nông dân, Thương lái tra cứu giá và xem dự báo nhanh chóng.

- **Backend (Server):** 
  - **Framework:** FastAPI
  - **Ngôn ngữ:** Python 3
  - **ORM:** SQLAlchemy (tương tác với CSDL)
  - **Machine Learning:** Scikit-learn, Prophet, PyTorch, XGBoost

- **Cơ sở dữ liệu (Database):**
  - PostgreSQL (Hỗ trợ Asyncpg)

## 2. Tiêu Chuẩn Bảo Mật (OWASP & Security)
- **Xác thực & Phân quyền (RBAC):** Phân chia rõ quyền `admin`, `analyst` và `user` công cộng.
- **Mã hóa:** Bcrypt băm mật khẩu, JWT mã hóa Token phiên làm việc.
- **An toàn CSDL & API:** Parameterized Queries phòng SQL Injection, Rate Limiting, Input Validation (Pydantic).

---

## 3. Các Giai Đoạn Triển Khai (Phases)

### Phase 1: Setup & Architecture (Khởi Tạo & Kiến Trúc)
- **Đặc tả:** Setup cấu trúc Backend/Frontend, Linting, Testing Framework (Pytest/Jest).

### Phase 2: Database & Core Auth (CSDL & Phân Quyền)
- **Đặc tả:** Sơ đồ CSDL PostgreSQL, SQLAlchemy Models, Auth API (Register/Login/JWT), Phân quyền Role-based.

### Phase 3: Data Ingestion & Crawler Pipeline (Thu Thập Dữ Liệu)
- **Đặc tả:** Module cào dữ liệu YFinance & Web Scraping (BS4), xử lý dữ liệu với Pandas, lập lịch định kỳ APScheduler.

### Phase 4: Machine Learning & Prediction API (AI/ML & API Dự Báo)
- **Đặc tả:** Huấn luyện mô hình Prophet/XGBoost, đo đạc sai số (RMSE, MAE), đóng gói mô hình và cung cấp API dự báo.

### Phase 5: Admin Dashboard Development (Giao Diện Quản Trị)
- **Đặc tả:** Xây dựng Bảng điều khiển Admin: Trigger cào dữ liệu thủ công, Theo dõi chỉ số ML Model & Retrain, Quản lý bảng giá & Người dùng.

### Phase 6: Public User UI Development (Giao Diện Người Dùng/Nông Dân)
- **Đặc tả:** Xây dựng trang chủ tra cứu giá công khai, xem biểu đồ dự báo trực quan, tối ưu giao diện Mobile/Tablet cho người dùng nông dân.

### Phase 7: Security Operations & Final Audit (Bảo Mật & Tối Ưu)
- **Đặc tả:** Audit theo tiêu chuẩn OWASP Top 10, tối ưu hiệu năng CSDL/API, tổng hợp tài liệu nghiệm thu.
