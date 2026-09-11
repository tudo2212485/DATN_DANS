# 🛠️ SETUP & DEPLOYMENT GUIDE — AgroForecast

## Hướng Dẫn Thiết Lập & Khởi Chạy Môi Trường Phát Triển Cục Bộ (Local Environment)

> **Hệ thống:** AgroForecast — Dự Báo Giá Nông Sản & Cảnh Báo Thị Trường Ứng Dụng Deep Learning  
> **Phiên bản:** v2.4.1 (Stable)  
> **Hệ điều hành khuyến nghị:** Windows 10/11 (Hỗ trợ tốt Linux/macOS)  
> **Cập nhật:** 10/09/2026  

---

## Mục lục

1. [Yêu cầu Môi trường Tiên quyết (Prerequisites)](#1-yêu-cầu-môi-trường-tiên-quyết-prerequisites)
2. [Cấu trúc Thư mục Dự án (Monorepo Layout)](#2-cấu-trúc-thư-mục-dự-án-monorepo-layout)
3. [Quy trình Cài đặt Từng bước (Step-by-Step Installation)](#3-quy-trình-cài-đặt-từng-bước-step-by-step-installation)
   - [Bước 1: Clone Mã Nguồn](#bước-1-clone-mã-nguồn-từ-github)
   - [Bước 2: Cài Đặt & Khởi Tạo Cơ Sở Dữ Liệu PostgreSQL](#bước-2-cài-đặt--khởi-tạo-cơ-sở-dữ-liệu-postgresql)
   - [Bước 3: Cấu Hình Biến Môi Trường (.env)](#bước-3-cấu-hình-biến-môi-trường-env)
   - [Bước 4: Cài Đặt Phụ Thuộc & Seed Dữ Liệu Backend](#bước-4-cài-đặt-phụ-thuộc--seed-dữ-liệu-backend)
   - [Bước 5: Cài Đặt Phụ Thuộc Frontend Next.js](#bước-5-cài-đặt-phụ-thuộc-frontend-nextjs)
4. [Khởi Chạy Hệ Thống (Running Application)](#4-khởi-chạy-hệ-thống-running-application)
   - [Cách 1: Khởi chạy One-Click (run_all.bat)](#cách-1-khởi-chạy-one-click-run_allbat-trên-windows)
   - [Cách 2: Khởi chạy Độc lập Từng Terminal](#cách-2-khởi-chạy-độc-lập-từng-terminal)
   - [Tài khoản Đăng nhập Demo](#tài-khoản-đăng-nhập-demo)
5. [Hướng Dẫn Khắc Phục Lỗi Thường Gặp trên Windows (Troubleshooting)](#5-hướng-dẫn-khắc-phục-lỗi-thường-gặp-trên-windows-troubleshooting)
   - [5.1. Lỗi PowerShell Script Execution Policy](#51-lỗi-powershell-script-execution-policy)
   - [5.2. Lỗi Kẹt Cổng (Port Conflict :8000 hoặc :3000)](#52-lỗi-kẹt-cổng-port-conflict-8000-hoặc-3000)
   - [5.3. Lỗi Thiếu Microsoft Visual C++ Build Tools (PyTorch / Prophet)](#53-lỗi-thiếu-microsoft-visual-c-build-tools-pytorch--prophet)
   - [5.4. Lỗi Dịch Vụ PostgreSQL Chưa Chạy hoặc Sai Mật Khẩu](#54-lỗi-dịch-vụ-postgresql-chưa-chạy-hoặc-sai-mật-khẩu)
   - [5.5. Lỗi Font / Mã Hóa Tiếng Việt Trên Console CMD Windows](#55-lỗi-font--mã-hóa-tiếng-việt-trên-console-cmd-windows)

---

## 1. Yêu cầu Môi trường Tiên quyết (Prerequisites)

Trước khi tiến hành cài đặt, đảm bảo máy tính đã cài đặt các công cụ sau:

| Thành phần | Phiên bản yêu cầu | Mục đích sử dụng | Kiểm tra phiên bản |
|------------|-------------------|------------------|-------------------|
| **Python** | `3.10.x` hoặc `3.11.x` *(khuyến nghị 3.11)* | Chạy Backend FastAPI, Data Scraper, PyTorch & ML models | `python --version` |
| **Node.js & npm** | Node `18.x` hoặc `20.x` LTS, npm `9.x+` | Chạy Web Frontend Next.js 14 App Router | `node -v` và `npm -v` |
| **PostgreSQL** | `15.x` hoặc cao hơn *(tối thiểu 14.x)* | Lưu trữ dữ liệu quan hệ, lịch sử giá, tài khoản, logs | `psql -U postgres -V` |
| **Git** | `2.35+` | Quản lý phiên bản mã nguồn | `git --version` |
| **C++ Build Tools** *(Windows)* | Microsoft Visual C++ 14.0+ | Biên dịch các gói C/C++ (Prophet, PyTorch wheel) | Cài qua Visual Studio Installer |

> ⚠️ **Lưu ý về phiên bản Python:** Không nên dùng Python 3.12+ cho các thư viện AI cũ (Prophet, PyTorch, statsmodels) vì một số wheel chưa được biên dịch sẵn cho Windows trên Python 3.12. Phiên bản tối ưu nhất là **Python 3.11.9 64-bit**.

---

## 2. Cấu trúc Thư mục Dự án (Monorepo Layout)

Dự án được tổ chức theo kiến trúc Monorepo thống nhất:

```text
DA_TN/
├── backend/                       # Phân hệ Backend API & AI Engine (FastAPI)
│   ├── app/                       # Source code chính của ứng dụng
│   │   ├── api/v1/                # RESTful API Endpoints (Auth, Market, Forecast, Alerts, Admin)
│   │   ├── core/                  # Cấu hình hệ thống (config.py, database.py, security.py)
│   │   ├── models/                # SQLAlchemy ORM Models (User, Commodity, PriceHistory, Alert, ...)
│   │   ├── schemas/               # Pydantic v2 Validation Schemas
│   │   ├── services/              # Business Logic (Email alert service, CSV export, ...)
│   │   └── main.py                # FastAPI Application Entrypoint
│   ├── ml_pipeline/               # Pipeline Máy học & Dữ liệu
│   │   ├── models/                # Lưu trữ trọng số mô hình đã huấn luyện (.pt, .joblib, .pkl)
│   │   ├── data_loader.py         # Tiền xử lý, lọc nhiễu IQR, ADF test, nạp biến ngoại sinh
│   │   ├── scraper.py             # Cào dữ liệu giá nông sản tự động (giacaphe.com, VFA)
│   │   ├── train_lstm.py          # Huấn luyện mô hình Deep Learning Stacked LSTM (PyTorch)
│   │   ├── train_prophet.py       # Huấn luyện mô hình Facebook Prophet
│   │   └── train_arima.py         # Huấn luyện mô hình thống kê ARIMA
│   ├── tests/                     # Bộ Unit Test & Integration Test (Pytest)
│   ├── seed_db.py                 # Script tạo tài khoản Admin & Analyst ban đầu
│   ├── requirements.txt           # Danh sách thư viện Python phụ thuộc
│   └── .env.example               # Mẫu cấu hình biến môi trường Backend
│
├── database/                      # Quản lý CSDL PostgreSQL
│   ├── init.sql                   # Kịch bản DDL tạo bảng, quan hệ, indexes & dữ liệu mẫu
│   └── load_database.py           # Script Python tự động tạo DB và nạp schema
│
├── frontend/                      # Phân hệ Frontend Web Application (Next.js 14)
│   ├── src/                       # Mã nguồn TypeScript / React
│   │   ├── app/                   # App Router: layout, dashboard, forecast, alerts, login, admin
│   │   ├── components/            # Reusable UI Components (Sidebar, Navbar, Charts, Cards)
│   │   └── lib/                   # Utility functions, axios client, API constants
│   ├── public/                    # Tài nguyên tĩnh (Favicon, hình ảnh, icons)
│   ├── package.json               # Danh sách thư viện JavaScript/Node.js
│   ├── tailwind.config.js         # Cấu hình bảng màu giao diện & Tailwind CSS
│   └── .env.local.example         # Mẫu cấu hình biến môi trường Frontend
│
├── docs/                          # Tài liệu kỹ thuật đồ án tốt nghiệp
│   ├── REQUIREMENTS_PLAN.md       # Đặc tả yêu cầu & kiến trúc toàn diện
│   ├── PROJECT_TRACKER.md         # Checklist tiến độ & trạng thái các module
│   ├── api_reference.md           # Đặc tả chi tiết 42 RESTful API endpoints
│   └── setup_guide.md             # Tài liệu hướng dẫn cài đặt & triển khai (file này)
│
├── kich_ban_bao_cao.md            # Kịch bản thuyết trình bảo vệ đồ án trước Hội đồng
├── run_all.bat                    # Script khởi chạy tự động cả Backend và Frontend trên Windows
└── README.md                      # Giới thiệu tổng quan dự án
```

---

## 3. Quy trình Cài đặt Từng bước (Step-by-Step Installation)

### Bước 1: Clone Mã Nguồn Từ GitHub

Mở **PowerShell** hoặc **Git Bash** và thực thi:

```bash
git clone https://github.com/tudo2212485/DATN_DANS.git
cd DATN_DANS
```

---

### Bước 2: Cài Đặt & Khởi Tạo Cơ Sở Dữ Liệu PostgreSQL

1. **Khởi động dịch vụ PostgreSQL:**
   Đảm bảo PostgreSQL service đang hoạt động trên cổng `5432`.

2. **Cách A (Khuyến nghị — Tự động bằng Script Python):**
   ```bash
   # Sử dụng script đã viết sẵn trong thư mục database:
   python database/load_database.py
   ```
   *Script sẽ tự động kết nối PostgreSQL, tạo cơ sở dữ liệu `agroforecast_db`, thực thi toàn bộ script DDL `database/init.sql` và nạp dữ liệu khởi tạo.*

3. **Cách B (Thủ công qua psql Command Line):**
   ```bash
   # Đăng nhập vào PostgreSQL với user postgres:
   psql -U postgres -h localhost -p 5432

   # Tạo CSDL:
   CREATE DATABASE agroforecast_db WITH ENCODING 'UTF8';
   \q

   # Thực thi file init.sql vào CSDL vừa tạo:
   psql -U postgres -d agroforecast_db -f database/init.sql
   ```

4. **Kiểm tra CSDL sau khi tạo:**
   CSDL `agroforecast_db` phải bao gồm các bảng chính:
   - `users`
   - `commodities`
   - `price_history`
   - `exogenous_data`
   - `model_registry`
   - `forecast_results`
   - `alert_rules`
   - `alert_logs`
   - `crawler_logs`

---

### Bước 3: Cấu Hình Biến Môi Trường (.env)

#### 3.1. Cấu hình Backend (`backend/.env`)

Tạo file `backend/.env` bằng cách copy từ `backend/.env.example`:

```bash
# Trên Windows CMD/PowerShell:
copy backend\.env.example backend\.env
```

Mở file `backend/.env` và điền thông tin kết nối thực tế:

```env
# ==========================================
# CẤU HÌNH CƠ SỞ DỮ LIỆU POSTGRESQL
# Cú pháp: postgresql://<user>:<password>@<host>:<port>/<dbname>
# ==========================================
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/agroforecast_db
DATABASE_URL_ASYNC=postgresql+asyncpg://postgres:postgres@localhost:5432/agroforecast_db

# ==========================================
# CẤU HÌNH API & JWT AUTHENTICATION
# ==========================================
API_V1_STR=/api/v1
PROJECT_NAME="AgroForecast - Hệ thống Dự báo Giá Nông sản"
SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# ==========================================
# CẤU HÌNH EMAIL GỬI CẢNH BÁO THỊ TRƯỜNG (SMTP)
# (Tuỳ chọn: Dùng tài khoản Gmail có bật App Password)
# ==========================================
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_gmail_app_password
EMAIL_FROM="AgroForecast Market Alerts <no-reply@agroforecast.vn>"
```

#### 3.2. Cấu hình Frontend (`frontend/.env.local`)

Tạo file `frontend/.env.local`:

```bash
# Trên Windows CMD/PowerShell:
copy frontend\.env.local.example frontend\.env.local
```

Nội dung file `frontend/.env.local`:

```env
# URL trỏ về Backend API Gateway
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_SITE_NAME="AgroForecast VN"
```

---

### Bước 4: Cài Đặt Phụ Thuộc & Seed Dữ Liệu Backend

1. **Di chuyển vào thư mục backend và tạo môi trường ảo Python (Virtual Environment):**
   ```bash
   cd backend
   python -m venv venv
   ```

2. **Kích hoạt môi trường ảo:**
   - **Trên Windows PowerShell:**
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - **Trên Windows CMD:**
     ```cmd
     venv\Scripts\activate.bat
     ```
   - **Trên Linux / macOS:**
     ```bash
     source venv/bin/activate
     ```

3. **Nâng cấp pip và cài đặt thư viện phụ thuộc:**
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Khởi tạo dữ liệu người dùng mẫu (Database Seeding):**
   ```bash
   python seed_db.py
   ```
   *Output hiển thị:*
   ```text
   Created user: admin@agroforecast.vn
   Created user: anhnguyen@agroforecast.vn
   Database seeding completed.
   ```

5. *(Tùy chọn) Chạy kiểm thử huấn luyện nhanh mô hình AI:*
   ```bash
   python -m ml_pipeline.train_lstm --commodity CA_PHE_ROBUSTA --epochs 5
   ```

6. **Quay lại thư mục gốc dự án:**
   ```bash
   cd ..
   ```

---

### Bước 5: Cài Đặt Phụ Thuộc Frontend Next.js

1. **Di chuyển vào thư mục frontend:**
   ```bash
   cd frontend
   ```

2. **Cài đặt các gói Node packages:**
   ```bash
   npm install
   ```

3. **Quay lại thư mục gốc dự án:**
   ```bash
   cd ..
   ```

---

## 4. Khởi Chạy Hệ Thống (Running Application)

### Cách 1: Khởi chạy One-Click (`run_all.bat`) trên Windows

Dự án đã tích hợp sẵn kịch bản khởi chạy đồng thời cả hai phân hệ bằng file `run_all.bat` tại thư mục gốc:

1. Click đúp chuột vào file `run_all.bat` hoặc chạy từ dòng lệnh:
   ```cmd
   .\run_all.bat
   ```
2. Hệ thống sẽ tự động bật 2 cửa sổ Command Prompt riêng biệt:
   - Cửa sổ 1: Backend FastAPI đang lắng nghe tại `http://localhost:8000`.
   - Cửa sổ 2: Frontend Next.js đang lắng nghe tại `http://localhost:3000`.
3. Trình duyệt mặc định sẽ tự động mở trang `http://localhost:3000`.

---

### Cách 2: Khởi chạy Độc lập Từng Terminal

Nếu bạn muốn kiểm tra log chi tiết từng tiến trình:

#### Terminal 1 — Backend FastAPI:
```bash
cd backend
# Kích hoạt môi trường ảo:
.\venv\Scripts\activate
# Khởi chạy server Uvicorn:
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
- **Trang chủ API:** `http://localhost:8000`
- **Tài liệu Swagger UI:** `http://localhost:8000/docs`
- **Tài liệu ReDoc:** `http://localhost:8000/redoc`

#### Terminal 2 — Frontend Next.js:
```bash
cd frontend
npm run dev
```
- **Giao diện Web:** `http://localhost:3000`

---

### Tài khoản Đăng nhập Demo

Hệ thống đã được cấu hình sẵn 2 tài khoản phân quyền mẫu để báo cáo và đánh giá:

| Vai trò | Email đăng nhập | Mật khẩu | Quyền hạn trong hệ thống |
|---------|-----------------|----------|--------------------------|
| 👑 **Quản trị viên (Admin)** | `admin@agroforecast.vn` | `admin123` | Quản lý toàn quyền CSDL, Trigger Retrain mô hình, Theo dõi Crawler Logs, CRUD nông sản & tài khoản |
| 📊 **Chuyên viên (Analyst)** | `anhnguyen@agroforecast.vn` | `123456` | Xem chi tiết mô hình AI, So sánh chỉ số MAE/RMSE/MAPE, Thiết lập quy tắc cảnh báo, Xuất báo cáo CSV |

---

## 5. Hướng Dẫn Khắc Phục Lỗi Thường Gặp trên Windows (Troubleshooting)

### 5.1. Lỗi PowerShell Script Execution Policy

**Triệu chứng:**
Khi gõ `.\venv\Scripts\Activate.ps1`, PowerShell báo lỗi:
```text
File ...\venv\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled on this system.
```

**Nguyên nhân:**
Chính sách bảo mật mặc định của Windows PowerShell chặn thực thi script chưa ký số.

**Cách khắc phục:**
Mở PowerShell dưới quyền **Run as Administrator** và chạy lệnh:
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Nhấn `Y` để xác nhận. Sau đó tắt đi mở lại PowerShell bình thường, bạn sẽ kích hoạt được virtualenv.

---

### 5.2. Lỗi Kẹt Cổng (Port Conflict :8000 hoặc :3000)

**Triệu chứng:**
- Backend báo: `[Errno 10048] error while attempting to bind on address ('127.0.0.1', 8000): only one usage of each socket address is normally permitted`
- Frontend Next.js tự động chuyển sang port 3001 thay vì 3000.

**Cách khắc phục:**
Mở CMD hoặc PowerShell và tìm PID đang chiếm giữ cổng:

```cmd
# Kiểm tra tiến trình chiếm cổng 8000:
netstat -ano | findstr :8000

# Giả sử PID tìm được ở cột cuối là 14220, cưỡng chế tắt tiến trình:
taskkill /PID 14220 /F

# Tương tự kiểm tra cổng 3000:
netstat -ano | findstr :3000
taskkill /PID <PID_PORT_3000> /F
```

---

### 5.3. Lỗi Thiếu Microsoft Visual C++ Build Tools (PyTorch / Prophet)

**Triệu chứng:**
Khi cài đặt `requirements.txt`, tiến trình báo lỗi đỏ:
```text
error: Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools"
```

**Cách khắc phục:**
1. Tải bộ cài chính thức từ Microsoft: [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/).
2. Khi giao diện cài đặt hiện lên, tích chọn **"Desktop development with C++"** (Phát triển ứng dụng Desktop với C++).
3. Đảm bảo các tùy chọn bên phải có:
   - *MSVC v143 - VS 2022 C++ x64/x86 build tools*
   - *Windows 10/11 SDK*
4. Bấm **Install** và khởi động lại máy.
5. Chạy lại lệnh cài đặt:
   ```bash
   pip install --no-cache-dir -r requirements.txt
   ```

---

### 5.4. Lỗi Dịch Vụ PostgreSQL Chưa Chạy hoặc Sai Mật Khẩu

**Triệu chứng:**
Backend báo lỗi: `psycopg2.OperationalError: connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused` hoặc `password authentication failed for user "postgres"`.

**Cách khắc phục:**
1. **Kiểm tra service PostgreSQL:**
   Mở CMD với quyền Admin:
   ```cmd
   net start postgresql-x64-15
   ```
   *(Hoặc gõ `services.msc`, tìm dịch vụ có tên bắt đầu bằng `postgresql...`, click chuột phải chọn **Start**).*
2. **Kiểm tra mật khẩu:**
   Đảm bảo mật khẩu của user `postgres` trong chuỗi kết nối `DATABASE_URL` tại file `backend/.env` khớp hoàn toàn với mật khẩu bạn đã đặt khi cài đặt PostgreSQL.
3. **Thử kết nối bằng psql:**
   ```bash
   psql -U postgres -h localhost -p 5432
   ```

---

### 5.5. Lỗi Font / Mã Hóa Tiếng Việt Trên Console CMD Windows

**Triệu chứng:**
Các dòng in tiếng Việt trong script Python hoặc bat file bị hiển thị thành ký tự lạ dạng `H? th?ng d? bo gi...`.

**Cách khắc phục:**
1. Chuyển bảng mã console sang Unicode UTF-8 trước khi chạy lệnh:
   ```cmd
   chcp 65001
   ```
2. Đặt font chữ của cửa sổ Command Prompt / Windows Terminal sang các font hỗ trợ UTF-8 đầy đủ như **Cascadia Code**, **Consolas**, hoặc **Lucida Console**.
3. File `run_all.bat` của dự án đã tự động cấu hình dòng `chcp 65001 > nul` ngay dòng đầu tiên để ngăn chặn hiện tượng này.

---

## 6. Tổng Kết Kiểm Tra Môi Trường Sẵn Sàng (Readiness Checklist)

Trước khi đem dự án nộp cho Giảng viên Hướng dẫn hoặc Hội đồng bảo vệ, bạn hãy tự kiểm tra theo checklist sau:

- [ ] PostgreSQL đã được bật và CSDL `agroforecast_db` có đầy đủ dữ liệu trong 9 bảng.
- [ ] File `backend/.env` và `frontend/.env.local` đã được tạo và không bị lỗi cú pháp.
- [ ] Backend khởi chạy thành công, truy cập `http://localhost:8000/docs` hiển thị đủ 42 endpoints.
- [ ] Frontend khởi chạy thành công, truy cập `http://localhost:3000` hiển thị Dashboard đẹp mắt, biểu đồ Recharts mượt mà.
- [ ] Đăng nhập được bằng cả tài khoản `admin@agroforecast.vn` và `anhnguyen@agroforecast.vn`.
- [ ] Thử click vào trang **Dự báo & Mô hình (Forecast)** để kiểm tra hiển thị dải tin cậy 95% và bảng so sánh sai số.
- [ ] File script `run_all.bat` chạy êm xuôi chỉ với 1 cú nhấp chuột.
