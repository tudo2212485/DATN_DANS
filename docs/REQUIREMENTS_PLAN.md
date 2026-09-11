# 📋 REQUIREMENTS & ARCHITECTURE PLAN

## Hệ thống Dự báo Giá Nông sản & Cảnh báo Thị trường Ứng dụng Deep Learning

**Tên hệ thống:** AgroForecast  
**Phiên bản tài liệu:** 2.4  
**Ngày tạo:** 10/09/2026  
**Tác giả:** Software Architect & Data System Specialist  
**Trạng thái:** ✅ Production-Ready

---

## Mục lục

- [1. Thông tin Đề tài](#1-thông-tin-đề-tài)
- [2. Milestones Tracker](#2-milestones-tracker)
- [3. Kiến trúc Hệ thống](#3-kiến-trúc-hệ-thống)
- [4. Mô hình Dữ liệu](#4-mô-hình-dữ-liệu)
- [5. Quy tắc Nghiệp vụ](#5-quy-tắc-nghiệp-vụ)
- [6. Tiêu chuẩn Mã nguồn](#6-tiêu-chuẩn-mã-nguồn)

---

## 1. Thông tin Đề tài

### 1.1. Mục tiêu Dự án

| # | Mục tiêu | Mô tả chi tiết |
|---|----------|-----------------|
| O1 | **Xây dựng hệ thống dự báo giá** | Phát triển mô hình Deep Learning (Stacked LSTM) kết hợp ML ensemble (XGBoost, Random Forest) và thống kê (Prophet, ARIMA) để dự báo giá 4 nông sản chiến lược của Việt Nam trong khung thời gian 7–30 ngày. |
| O2 | **Tích hợp biến ngoại sinh** | Đưa tỷ giá USD/VND và giá dầu thô WTI làm đặc trưng ngoại sinh (exogenous features) vào mô hình, nâng cao độ chính xác dự báo nhờ phản ánh tác động kinh tế vĩ mô. |
| O3 | **Cảnh báo thị trường tự động** | Thiết lập engine cảnh báo theo ngưỡng giá (Price Above/Below) và biến động phần trăm (% tăng/giảm trong 7 ngày), tự động đánh giá 2 lần/ngày qua APScheduler và gửi thông báo qua email SMTP. |
| O4 | **Dashboard phân tích trực quan** | Xây dựng giao diện web responsive với biểu đồ tương tác (Recharts), bảng so sánh hiệu suất mô hình, và bản đồ giá vùng miền trên nền Next.js 14 App Router. |
| O5 | **So sánh & đánh giá mô hình** | Benchmark 5 mô hình (LSTM, XGBoost, Random Forest, Prophet, ARIMA) trên cùng bộ dữ liệu với các chỉ số MAE, RMSE, MAPE, R² — chứng minh ưu thế Deep Learning trong bài toán chuỗi thời gian tài chính. |

### 1.2. Phạm vi Nông sản

| # | Nông sản | Mã code | Đơn vị | Vùng trọng điểm | Nguồn dữ liệu |
|---|----------|---------|--------|------------------|----------------|
| 1 | **Lúa gạo IR504** | `LUA_IR504` | VNĐ/kg | Đồng bằng sông Cửu Long | Sở NN&PTNT, Hiệp hội Lương thực VN (VFA) |
| 2 | **Cà phê Robusta** | `CA_PHE_ROBUSTA` | VNĐ/kg | Tây Nguyên (Đắk Lắk, Gia Lai) | Sở NN&PTNT, Hiệp hội Cà phê - Ca cao VN (VICOFA) |
| 3 | **Hồ tiêu đen** | `HO_TIEU_DEN` | VNĐ/kg | Đông Nam Bộ (Bình Phước, Bà Rịa) | Hiệp hội Hồ tiêu VN (VPA) |
| 4 | **Mía đường** | `MIA_DUONG` | VNĐ/kg | ĐBSCL, Duyên hải Nam Trung Bộ | Hiệp hội Mía đường VN (VSSA) |

### 1.3. Biến Ngoại sinh (Exogenous Variables)

| # | Biến | Ký hiệu Yahoo Finance | Ý nghĩa kinh tế | Phương thức thu thập |
|---|------|------------------------|------------------|----------------------|
| 1 | **Tỷ giá USD/VND** | `USDVND=X` | Phản ánh sức mua đồng nội tệ, ảnh hưởng trực tiếp đến giá xuất khẩu nông sản | `yfinance` API, tần suất hàng ngày |
| 2 | **Dầu thô WTI** | `CL=F` | Tác động chi phí vận chuyển, phân bón, năng lượng sản xuất nông nghiệp | `yfinance` API, tần suất hàng ngày |

### 1.4. Technology Stack

```
┌─────────────────────────────────────────────────────────────────────┐
│                        TECHNOLOGY STACK                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─── Frontend ───────────────────────────────────────────────┐    │
│  │  Next.js 14 (App Router) • TypeScript • Tailwind CSS       │    │
│  │  Recharts • React Hook Form • Axios                        │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                     │
│  ┌─── Backend ────────────────────────────────────────────────┐    │
│  │  Python 3.11+ • FastAPI • Pydantic v2 • Uvicorn            │    │
│  │  SQLAlchemy 2.x ORM • pydantic-settings • APScheduler      │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                     │
│  ┌─── ML / Deep Learning ─────────────────────────────────────┐    │
│  │  PyTorch (Stacked LSTM) • XGBoost • scikit-learn (RF)      │    │
│  │  Prophet • statsmodels (ARIMA) • yfinance                   │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                     │
│  ┌─── Database & Infra ───────────────────────────────────────┐    │
│  │  PostgreSQL 15 • APScheduler (BackgroundScheduler)          │    │
│  │  bcrypt • PyJWT • SMTP (Gmail)                              │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. Milestones Tracker

### 2.1. Tổng quan 10 Giai đoạn

> **Thời gian thực hiện:** 20/07/2026 → 29/11/2026 (19 tuần)  
> **Phương pháp:** Iterative Development bám sát đề cương bảo vệ tốt nghiệp

| Phase | Giai đoạn | Thời gian | Tuần | Deliverables chính | Trạng thái |
|:-----:|-----------|-----------|:----:|---------------------|:----------:|
| **P1** | Khảo sát & Phân tích yêu cầu | 20/07 → 02/08 | 2 | Đề cương chi tiết, SRS, Use Case Diagram | ✅ Done |
| **P2** | Thiết kế kiến trúc hệ thống | 03/08 → 16/08 | 2 | System Architecture, DB Schema, API Contract, Wireframe | ✅ Done |
| **P3** | Thu thập & Xử lý dữ liệu | 17/08 → 30/08 | 2 | Data Pipeline (Scraper → Clean → PostgreSQL), EDA Report | ✅ Done |
| **P4** | Xây dựng ML Pipeline (Baseline) | 31/08 → 13/09 | 2 | ARIMA + Prophet baseline, Training script, Model Registry | 🔄 In Progress |
| **P5** | Deep Learning — Stacked LSTM | 14/09 → 27/09 | 2 | LSTM architecture, Hyperparameter tuning, Exogenous integration | ⬜ Pending |
| **P6** | Ensemble Models (XGBoost, RF) | 28/09 → 11/10 | 2 | XGBoost & Random Forest trainers, Feature importance analysis | ⬜ Pending |
| **P7** | Backend API & Cảnh báo | 12/10 → 25/10 | 2 | RESTful API endpoints, Alert Engine, Scheduler cron jobs | ⬜ Pending |
| **P8** | Frontend Dashboard | 26/10 → 08/11 | 2 | Dashboard UI, Biểu đồ dự báo, Bảng so sánh mô hình, Admin panel | ⬜ Pending |
| **P9** | Tích hợp, Testing & Tối ưu | 09/11 → 22/11 | 2 | Integration testing, Performance tuning, Security hardening | ⬜ Pending |
| **P10** | Viết báo cáo & Bảo vệ | 23/11 → 29/11 | 1 | Báo cáo tốt nghiệp, Slide thuyết trình, Demo video | ⬜ Pending |

### 2.2. Gantt Chart (ASCII)

```
Phase  Jul           Aug           Sep           Oct           Nov
       20  27  03  10  17  24  31  07  14  21  28  05  12  19  26  02  09  16  23  29
P1     ████████
P2             ████████
P3                     ████████
P4                             ████████
P5                                     ████████
P6                                             ████████
P7                                                     ████████
P8                                                             ████████
P9                                                                     ████████
P10                                                                            ████
       ─────────────────────────────────────────────────────────────────────────────
       Nghiên cứu & Thiết kế │  ML/DL Development  │   Full-stack Dev   │Bảo vệ
```

### 2.3. Chi tiết Deliverables theo Phase

<details>
<summary><strong>P1 — Khảo sát & Phân tích yêu cầu (20/07 → 02/08)</strong></summary>

- [x] Xác định bài toán dự báo chuỗi thời gian (Time Series Forecasting)
- [x] Khảo sát 4 nguồn dữ liệu nông sản (VFA, VICOFA, VPA, VSSA)
- [x] Xác định 2 biến ngoại sinh (USD/VND, WTI Crude Oil)
- [x] Viết đề cương chi tiết (Problem Statement, Objectives, Scope)
- [x] Vẽ Use Case Diagram & Activity Diagram
- [x] Tài liệu `docs/phase_1_spec.md`
</details>

<details>
<summary><strong>P2 — Thiết kế kiến trúc hệ thống (03/08 → 16/08)</strong></summary>

- [x] Thiết kế System Architecture (3-tier: Client → API → DB)
- [x] Thiết kế Database Schema PostgreSQL (7 bảng)
- [x] Định nghĩa API Contract (OpenAPI 3.0)
- [x] Wireframe Dashboard (Figma/Excalidraw)
- [x] Thiết kế Auth Flow (JWT + OAuth2PasswordBearer + bcrypt)
- [x] Tài liệu `docs/phase_2_spec.md`
</details>

<details>
<summary><strong>P3 — Thu thập & Xử lý dữ liệu (17/08 → 30/08)</strong></summary>

- [x] Xây dựng `ml_pipeline/scraper.py` — Web scraper cho 4 nông sản
- [x] Xây dựng `ml_pipeline/data_loader.py` — Data pipeline (Clean → Merge → Store)
- [x] Xử lý missing data: Linear Interpolation + Forward/Backward Fill
- [x] Xử lý ngoại lai: IQR Capping method
- [x] Kiểm định tính dừng: Augmented Dickey-Fuller (ADF) test
- [x] Tích hợp biến ngoại sinh từ Yahoo Finance (`yfinance`)
- [x] Tài liệu `docs/phase_3_spec.md`
</details>

<details>
<summary><strong>P4 — ML Pipeline Baseline (31/08 → 13/09)</strong></summary>

- [x] Xây dựng `ml_pipeline/baseline_arima.py` — ARIMA/SARIMAX baseline
- [x] Xây dựng `ml_pipeline/train_prophet.py` — Facebook Prophet
- [x] Thiết kế `ml_pipeline/feature_engineering.py` — Feature extraction
- [ ] Xây dựng Model Registry (save/load `.pkl`, `.pt` files)
- [ ] Benchmark ARIMA vs Prophet trên 4 nông sản
- [ ] Tài liệu `docs/phase_4_spec.md`
</details>

<details>
<summary><strong>P5 → P10 — Remaining Phases</strong></summary>

Xem chi tiết tại: `docs/phase_5_spec.md` → `docs/phase_7_spec.md`
</details>

---

## 3. Kiến trúc Hệ thống (System Architecture)

### 3.1. Sơ đồ Khối Tổng thể

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                              AGROFORECAST SYSTEM                                 │
│                         System Architecture Overview                             │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────┐         │
│  │                     🌐 CLIENT LAYER                                 │         │
│  │  ┌─────────────────────────────────────────────────────────────┐   │         │
│  │  │              Next.js 14 (App Router)                        │   │         │
│  │  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐  │   │         │
│  │  │  │Dashboard │ │Forecast  │ │ Alerts   │ │Admin Panel   │  │   │         │
│  │  │  │  Page    │ │ Chart    │ │ Manager  │ │(CRUD + User) │  │   │         │
│  │  │  └────┬─────┘ └────┬─────┘ └────┬─────┘ └──────┬───────┘  │   │         │
│  │  │       └─────────────┴────────────┴──────────────┘          │   │         │
│  │  │                    Axios HTTP Client                        │   │         │
│  │  │                  (Bearer JWT Token)                         │   │         │
│  │  └──────────────────────────┬──────────────────────────────────┘   │         │
│  └─────────────────────────────┼─────────────────────────────────────┘         │
│                                │ HTTPS :3000 → :8000                            │
│                                ▼                                                │
│  ┌─────────────────────────────────────────────────────────────────────┐         │
│  │                  🔐 API GATEWAY / FastAPI Router                    │         │
│  │  ┌───────────────────────────────────────────────────────────────┐ │         │
│  │  │  CORSMiddleware │ SecurityHeadersMiddleware │ RateLimiter     │ │         │
│  │  └───────────────────────────────────────────────────────────────┘ │         │
│  │  ┌───────────────────────────────────────────────────────────────┐ │         │
│  │  │                  /api/v1/ Router                               │ │         │
│  │  │  ┌──────────┐ ┌───────────┐ ┌──────────┐ ┌───────────────┐  │ │         │
│  │  │  │/auth/*   │ │/commodit* │ │/forecast │ │/alerts/*      │  │ │         │
│  │  │  │login     │ │/prices/*  │ │/predict  │ │/admin/*       │  │ │         │
│  │  │  │register  │ │           │ │/compare  │ │               │  │ │         │
│  │  │  └──────────┘ └───────────┘ └──────────┘ └───────────────┘  │ │         │
│  │  └──────────────────────────┬────────────────────────────────────┘ │         │
│  └─────────────────────────────┼─────────────────────────────────────┘         │
│                                │                                                │
│                                ▼                                                │
│  ┌─────────────────────────────────────────────────────────────────────┐         │
│  │                     ⚙️ SERVICES LAYER                               │         │
│  │                                                                     │         │
│  │  ┌─────────────┐  ┌─────────────┐  ┌──────────────────────────┐   │         │
│  │  │  Forecast   │  │   Alert     │  │     Commodity            │   │         │
│  │  │  Service    │  │   Service   │  │     Service              │   │         │
│  │  │             │  │             │  │                          │   │         │
│  │  │ • dashboard │  │ • evaluate  │  │ • get_all / get_by_id    │   │         │
│  │  │ • compare   │  │ • create    │  │ • price_history          │   │         │
│  │  │ • predict   │  │ • send_mail │  │ • regional_prices        │   │         │
│  │  └──────┬──────┘  └──────┬──────┘  └────────────┬─────────────┘   │         │
│  │         └────────────────┼──────────────────────┘                  │         │
│  └──────────────────────────┼────────────────────────────────────────┘         │
│                             │                                                   │
│                             ▼                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐         │
│  │                   🤖 ML PIPELINE ENGINE                             │         │
│  │                                                                     │         │
│  │  ┌──────────┐  ┌────────────┐  ┌─────────────┐  ┌──────────────┐  │         │
│  │  │  Data    │  │  Feature   │  │   Model     │  │  Predictor   │  │         │
│  │  │  Loader  │  │  Engineer  │  │   Trainer   │  │              │  │         │
│  │  │          │  │            │  │             │  │  • forecast  │  │         │
│  │  │ • clean  │  │ • lag feat │  │ • LSTM      │  │  • CI band   │  │         │
│  │  │ • merge  │  │ • rolling  │  │ • XGBoost   │  │  • metrics   │  │         │
│  │  │ • impute │  │ • exo vars │  │ • RF        │  │  • cache     │  │         │
│  │  │ • IQR    │  │ • diff     │  │ • Prophet   │  │              │  │         │
│  │  │ • ADF    │  │            │  │ • ARIMA     │  │              │  │         │
│  │  └──────────┘  └────────────┘  └─────────────┘  └──────────────┘  │         │
│  │                                                                     │         │
│  │  saved_models/  *.pt (PyTorch)  *.pkl (scikit-learn, XGBoost)      │         │
│  └─────────────────────────────────────────────────────────────────────┘         │
│                             │                                                   │
│                             ▼                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐         │
│  │                   🗄️ DATABASE LAYER                                 │         │
│  │                                                                     │         │
│  │  ┌──────────────────────────────────────────────────────────────┐  │         │
│  │  │                PostgreSQL 15                                  │  │         │
│  │  │  ┌──────┐ ┌───────────┐ ┌─────────────┐ ┌──────────────┐   │  │         │
│  │  │  │users │ │commodities│ │price_history│ │  forecasts   │   │  │         │
│  │  │  └──────┘ └───────────┘ └─────────────┘ └──────────────┘   │  │         │
│  │  │  ┌───────────┐ ┌───────────┐                                │  │         │
│  │  │  │alert_rules│ │alert_logs │                                │  │         │
│  │  │  └───────────┘ └───────────┘                                │  │         │
│  │  └──────────────────────────────────────────────────────────────┘  │         │
│  └─────────────────────────────────────────────────────────────────────┘         │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────┐         │
│  │                   ⏰ BACKGROUND SCHEDULER                           │         │
│  │                                                                     │         │
│  │  APScheduler (BackgroundScheduler)                                  │         │
│  │  ┌───────────────────────┐  ┌────────────────────────────────────┐ │         │
│  │  │ daily_scraper         │  │ daily_alert_evaluation             │ │         │
│  │  │ CronTrigger: 06:00    │  │ CronTrigger: 06:30, 18:30         │ │         │
│  │  │ → scrape_and_update_db│  │ → evaluate_all_alert_rules        │ │         │
│  │  └───────────────────────┘  └────────────────────────────────────┘ │         │
│  └─────────────────────────────────────────────────────────────────────┘         │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────┐         │
│  │                 📡 EXTERNAL DATA SOURCES                            │         │
│  │                                                                     │         │
│  │  • Yahoo Finance API (yfinance) — USD/VND, Crude Oil WTI           │         │
│  │  • Sở NN&PTNT / Hiệp hội Nông sản — Giá nông sản hàng ngày       │         │
│  │  • Gmail SMTP — Email cảnh báo                                     │         │
│  └─────────────────────────────────────────────────────────────────────┘         │
│                                                                                  │
└──────────────────────────────────────────────────────────────────────────────────┘
```

### 3.2. Luồng Request/Response

```
┌────────┐        ┌──────────┐       ┌──────────┐       ┌──────────┐       ┌──────┐
│ Client │──req──▶│Middleware │──────▶│  Router  │──────▶│ Service  │──────▶│  DB  │
│Next.js │        │CORS+Sec  │       │/api/v1/* │       │  Layer   │       │ PgSQL│
│        │◀─res──│+RateLim  │◀──────│          │◀──────│          │◀──────│      │
└────────┘        └──────────┘       └──────────┘       └──────────┘       └──────┘
    │                  │                  │                  │
    │  Authorization: Bearer <JWT>       │                  │
    │─────────────────────────────────────▶                  │
    │                  │          OAuth2PasswordBearer       │
    │                  │          decode_access_token()      │
    │                  │          ──────────────────────▶    │
    │                  │                  │  get_current_user │
    │                  │                  │  ────────────────▶│
    │                  │                  │                   │ SELECT * FROM users
    │                  │                  │                   │─────────────────▶
    │                  │                  │                   │◀────── User row
    │                  │                  │◀──── User object  │
    │                  │                  │                   │
    │◀───────── JSON Response ───────────│                   │
```

### 3.3. Luồng Bảo mật (Authentication & Authorization Flow)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                     🔐 AUTHENTICATION FLOW                                   │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─ ĐĂNG KÝ (Register) ──────────────────────────────────────────────────┐  │
│  │                                                                        │  │
│  │  Client                    FastAPI                    PostgreSQL       │  │
│  │    │                         │                           │             │  │
│  │    │  POST /api/v1/auth/register                        │             │  │
│  │    │  { email, password, full_name }                     │             │  │
│  │    │────────────────────────▶│                           │             │  │
│  │    │                         │ 1. Validate (Pydantic v2) │             │  │
│  │    │                         │ 2. sanitize_text(input)   │             │  │
│  │    │                         │ 3. Check duplicate email  │             │  │
│  │    │                         │───────────────────────────▶│            │  │
│  │    │                         │◀── EXISTS? ───────────────│            │  │
│  │    │                         │ 4. bcrypt.gensalt()       │             │  │
│  │    │                         │    bcrypt.hashpw(pwd)     │             │  │
│  │    │                         │ 5. INSERT user            │             │  │
│  │    │                         │───────────────────────────▶│            │  │
│  │    │◀── 201 Created ────────│                           │             │  │
│  │    │    { user_id, email }  │                           │             │  │
│  │                                                                        │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌─ ĐĂNG NHẬP (Login) ───────────────────────────────────────────────────┐  │
│  │                                                                        │  │
│  │  Client                    FastAPI                    PostgreSQL       │  │
│  │    │                         │                           │             │  │
│  │    │  POST /api/v1/auth/login                           │             │  │
│  │    │  Content-Type: x-www-form-urlencoded                │             │  │
│  │    │  { username, password }                             │             │  │
│  │    │────────────────────────▶│                           │             │  │
│  │    │                         │ 1. RateLimiter check      │             │  │
│  │    │                         │    (25 req/60s per IP)    │             │  │
│  │    │                         │ 2. Query user by email    │             │  │
│  │    │                         │───────────────────────────▶│            │  │
│  │    │                         │◀── user row ──────────────│            │  │
│  │    │                         │ 3. bcrypt.checkpw(pwd,    │             │  │
│  │    │                         │    user.password_hash)    │             │  │
│  │    │                         │ 4. create_access_token(   │             │  │
│  │    │                         │    sub=user.id,           │             │  │
│  │    │                         │    role=user.role,        │             │  │
│  │    │                         │    exp=7 days)            │             │  │
│  │    │◀── 200 OK ─────────────│                           │             │  │
│  │    │  { access_token,       │                           │             │  │
│  │    │    token_type:"bearer" }│                          │             │  │
│  │                                                                        │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌─ XÁC THỰC REQUEST (Protected Route) ──────────────────────────────────┐  │
│  │                                                                        │  │
│  │  Authorization: Bearer eyJhbGciOiJIUzI1NiIs...                       │  │
│  │         │                                                              │  │
│  │         ▼                                                              │  │
│  │  OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")                  │  │
│  │         │                                                              │  │
│  │         ▼                                                              │  │
│  │  decode_access_token(token)                                            │  │
│  │    ├─ jwt.decode(token, SECRET_KEY, algorithm="HS256")                │  │
│  │    ├─ Validate: exp (expiration), sub (user_id), role                 │  │
│  │    └─ Return payload or None                                          │  │
│  │         │                                                              │  │
│  │         ▼                                                              │  │
│  │  get_current_user(payload.sub) → Query DB → User object               │  │
│  │         │                                                              │  │
│  │         ▼                                                              │  │
│  │  require_role(["admin"]) → Check user.role ∈ allowed_roles            │  │
│  │    ├─ ✅ Allowed → Proceed to endpoint handler                        │  │
│  │    └─ ❌ Denied  → 403 Forbidden                                      │  │
│  │                                                                        │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌─ JWT TOKEN STRUCTURE ──────────────────────────────────────────────────┐  │
│  │                                                                        │  │
│  │  Header:  { "alg": "HS256", "typ": "JWT" }                           │  │
│  │  Payload: {                                                            │  │
│  │    "sub": "42",              // User ID (string)                      │  │
│  │    "role": "analyst",        // "analyst" | "admin" | "user"          │  │
│  │    "iat": 1726000000,        // Issued At (Unix timestamp)            │  │
│  │    "exp": 1726604800         // Expiration (iat + 7 days)             │  │
│  │  }                                                                     │  │
│  │  Signature: HMACSHA256(base64(header) + "." + base64(payload),        │  │
│  │                        SECRET_KEY)                                     │  │
│  │                                                                        │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌─ SECURITY HARDENING (OWASP Top 10) ───────────────────────────────────┐  │
│  │                                                                        │  │
│  │  Middleware Stack (áp dụng cho MỌI response):                         │  │
│  │    ✓ X-Content-Type-Options: nosniff          (Chống MIME-sniffing)   │  │
│  │    ✓ X-Frame-Options: DENY                    (Chống Clickjacking)   │  │
│  │    ✓ X-XSS-Protection: 1; mode=block          (XSS Filter)          │  │
│  │    ✓ Strict-Transport-Security: max-age=31536000 (Force HTTPS)       │  │
│  │    ✓ Referrer-Policy: strict-origin-when-cross-origin                │  │
│  │    ✓ Permissions-Policy: geolocation=(), camera=(), microphone=()    │  │
│  │                                                                        │  │
│  │  Input Sanitization:                                                   │  │
│  │    ✓ sanitize_text() — Strip HTML tags + html.escape()               │  │
│  │    ✓ Pydantic v2 validators — Type-safe schema validation            │  │
│  │                                                                        │  │
│  │  Rate Limiting:                                                        │  │
│  │    ✓ auth_rate_limiter: 25 requests / 60 seconds per IP              │  │
│  │    ✓ task_rate_limiter: 10 requests / 60 seconds per IP              │  │
│  │                                                                        │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 3.4. Luồng ML Pipeline

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                       🤖 ML PIPELINE FLOW                                    │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌─────────┐  │
│  │  DATA  │───▶│  CLEAN   │───▶│ FEATURE  │───▶│  TRAIN   │───▶│ PREDICT │  │
│  │ INGEST │    │ & MERGE  │    │ENGINEER  │    │ & EVAL   │    │ & STORE │  │
│  └────────┘    └──────────┘    └──────────┘    └──────────┘    └─────────┘  │
│       │              │              │              │              │          │
│       ▼              ▼              ▼              ▼              ▼          │
│  ┌─────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌──────────┐   │
│  │scraper  │  │data_loader│  │feature_   │  │model_     │  │predictor │   │
│  │.py      │  │.py        │  │engineering│  │trainer.py │  │.py       │   │
│  │         │  │           │  │.py        │  │           │  │          │   │
│  │• Web    │  │• Interpo- │  │• Lag      │  │• LSTM     │  │• Load    │   │
│  │  scrape │  │  lation   │  │  features │  │• XGBoost  │  │  model   │   │
│  │• Yahoo  │  │• IQR Cap  │  │• Rolling  │  │• RF       │  │• Predict │   │
│  │  Finance│  │• ADF Test │  │  mean/std │  │• Prophet  │  │• 95% CI  │   │
│  │• Store  │  │• Merge    │  │• Exo vars │  │• ARIMA    │  │• Metrics │   │
│  │  to DB  │  │  exo vars │  │• Diff     │  │• Save .pt │  │• Cache   │   │
│  │         │  │           │  │           │  │  + .pkl   │  │          │   │
│  └─────────┘  └───────────┘  └───────────┘  └───────────┘  └──────────┘   │
│                                                                              │
│  Artifacts: saved_models/{commodity_code}_{model_name}.{pt|pkl}             │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Mô hình Dữ liệu (Database Schema)

### 4.1. Entity-Relationship Diagram (ASCII)

```
┌──────────────┐       ┌────────────────┐       ┌────────────────┐
│    users     │       │  commodities   │       │ price_history  │
├──────────────┤       ├────────────────┤       ├────────────────┤
│ PK id        │       │ PK id          │◀──FK──│ FK commodity_id│
│    email     │       │    code        │       │ PK id          │
│    password_ │       │    name        │       │    record_date │
│      hash    │       │    category    │       │    price       │
│    full_name │       │    unit        │       │    price_min   │
│    role      │       │    region      │       │    price_max   │
│    is_active │       │    description │       │    volume      │
│    created_at│       │    created_at  │       │    source      │
│    updated_at│       │    updated_at  │       │    created_at  │
└──────┬───────┘       └──────┬─────┬──┘       └────────────────┘
       │                      │     │
       │                      │     │          ┌────────────────┐
       │                      │     └────FK───▶│   forecasts    │
       │                      │                ├────────────────┤
       │                      │                │ PK id          │
       │                      │                │ FK commodity_id│
       │                      │                │    model_name  │
       │                      │                │    forecast_   │
       │                      │                │      date      │
       │                      │                │    predicted_  │
       │                      │                │      price     │
       │                      │                │    lower_ci    │
       │                      │                │    upper_ci    │
       │                      │                │    mae         │
       │                      │                │    rmse        │
       │                      │                │    mape        │
       │                      │                │    r2          │
       │                      │                │    training_   │
       │                      │                │      date      │
       │                      │                │    created_at  │
       │                      │                └────────────────┘
       │                      │
       │    ┌─────────────────┘
       │    │
       ▼    ▼
┌──────────────────┐         ┌────────────────┐
│   alert_rules    │         │   alert_logs   │
├──────────────────┤         ├────────────────┤
│ PK id            │◀──FK────│ FK rule_id     │
│ FK commodity_id  │         │ PK id          │
│ FK user_id       │         │    triggered_  │
│    rule_name     │         │      price     │
│    condition_type│         │    message     │
│    threshold_    │         │    status      │
│      value       │         │    triggered_at│
│    email         │         └────────────────┘
│    is_active     │
│    created_at    │
│    updated_at    │
└──────────────────┘
```

### 4.2. Chi tiết Định nghĩa Bảng

#### 4.2.1. Bảng `users` — Quản lý tài khoản người dùng

```sql
CREATE TABLE users (
    id              SERIAL          PRIMARY KEY,
    email           VARCHAR(150)    NOT NULL UNIQUE,
    password_hash   VARCHAR(255)    NOT NULL,
    full_name       VARCHAR(150)    NOT NULL,
    role            VARCHAR(50)     NOT NULL DEFAULT 'analyst',
    is_active       BOOLEAN         NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE UNIQUE INDEX idx_users_email ON users(email);
```

| Cột | Kiểu PostgreSQL | Ràng buộc | Ghi chú |
|-----|-----------------|-----------|---------|
| `id` | `SERIAL` (Integer auto-increment) | `PRIMARY KEY` | Khóa chính auto-increment |
| `email` | `VARCHAR(150)` | `NOT NULL`, `UNIQUE` | Định danh đăng nhập, Index tìm kiếm |
| `password_hash` | `VARCHAR(255)` | `NOT NULL` | Chuỗi bcrypt hash (60 ký tự) |
| `full_name` | `VARCHAR(150)` | `NOT NULL` | Tên hiển thị |
| `role` | `VARCHAR(50)` | `NOT NULL`, `DEFAULT 'analyst'` | Enum logic: `'analyst'` \| `'admin'` \| `'user'` |
| `is_active` | `BOOLEAN` | `NOT NULL`, `DEFAULT TRUE` | Soft-delete flag |
| `created_at` | `TIMESTAMPTZ` | `NOT NULL`, `DEFAULT NOW()` | Thời điểm tạo (UTC) |
| `updated_at` | `TIMESTAMPTZ` | `NOT NULL`, `DEFAULT NOW()` | Auto-update via `onupdate=func.now()` |

---

#### 4.2.2. Bảng `commodities` — Danh mục nông sản

```sql
CREATE TABLE commodities (
    id              SERIAL          PRIMARY KEY,
    code            VARCHAR(50)     NOT NULL UNIQUE,
    name            VARCHAR(150)    NOT NULL,
    category        VARCHAR(50)     NOT NULL,
    unit            VARCHAR(30)     NOT NULL,
    region          VARCHAR(100)    NOT NULL,
    description     TEXT            NULL,
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE UNIQUE INDEX idx_commodities_code ON commodities(code);
```

| Cột | Kiểu PostgreSQL | Ràng buộc | Ghi chú |
|-----|-----------------|-----------|---------|
| `id` | `SERIAL` | `PRIMARY KEY` | Khóa chính |
| `code` | `VARCHAR(50)` | `NOT NULL`, `UNIQUE` | Mã nông sản: `LUA_IR504`, `CA_PHE_ROBUSTA`, `HO_TIEU_DEN`, `MIA_DUONG` |
| `name` | `VARCHAR(150)` | `NOT NULL` | Tên hiển thị tiếng Việt |
| `category` | `VARCHAR(50)` | `NOT NULL` | Phân loại: `'Lương thực'`, `'Công nghiệp'` |
| `unit` | `VARCHAR(30)` | `NOT NULL` | Đơn vị: `'VNĐ/kg'` |
| `region` | `VARCHAR(100)` | `NOT NULL` | Vùng trồng chính |
| `description` | `TEXT` | `NULL` | Mô tả chi tiết (nullable) |

---

#### 4.2.3. Bảng `price_history` — Lịch sử giá nông sản

```sql
CREATE TABLE price_history (
    id              BIGSERIAL       PRIMARY KEY,
    commodity_id    INTEGER         NOT NULL REFERENCES commodities(id) ON DELETE CASCADE,
    record_date     DATE            NOT NULL,
    price           NUMERIC(14,2)   NOT NULL,
    price_min       NUMERIC(14,2)   NULL,
    price_max       NUMERIC(14,2)   NULL,
    volume          NUMERIC(16,2)   DEFAULT 0,
    source          VARCHAR(100)    DEFAULT 'Sở NN&PTNT / Hiệp hội Nông sản',
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

-- Composite Index for time-series queries
CREATE INDEX idx_price_history_commodity_date ON price_history(commodity_id, record_date);
CREATE INDEX idx_price_history_date ON price_history(record_date);
```

| Cột | Kiểu PostgreSQL | Ràng buộc | Ghi chú |
|-----|-----------------|-----------|---------|
| `id` | `BIGSERIAL` | `PRIMARY KEY` | Khóa chính BigInteger (dữ liệu lớn) |
| `commodity_id` | `INTEGER` | `FK → commodities(id)`, `ON DELETE CASCADE` | Khóa ngoại, **Indexed** |
| `record_date` | `DATE` | `NOT NULL` | Ngày ghi nhận giá, **Indexed** |
| `price` | `NUMERIC(14,2)` | `NOT NULL` | Giá trung bình (VNĐ/kg) |
| `price_min` | `NUMERIC(14,2)` | `NULL` | Giá thấp nhất trong ngày |
| `price_max` | `NUMERIC(14,2)` | `NULL` | Giá cao nhất trong ngày |
| `volume` | `NUMERIC(16,2)` | `DEFAULT 0` | Khối lượng giao dịch |
| `source` | `VARCHAR(100)` | `DEFAULT '...'` | Nguồn dữ liệu |

> **⚡ Index Strategy:** Composite index `(commodity_id, record_date)` tối ưu cho truy vấn `WHERE commodity_id = ? ORDER BY record_date` — query pattern chính của hệ thống.

---

#### 4.2.4. Bảng `forecasts` — Kết quả dự báo

```sql
CREATE TABLE forecasts (
    id              BIGSERIAL       PRIMARY KEY,
    commodity_id    INTEGER         NOT NULL REFERENCES commodities(id) ON DELETE CASCADE,
    model_name      VARCHAR(50)     NOT NULL,
    forecast_date   DATE            NOT NULL,
    predicted_price NUMERIC(14,2)   NOT NULL,
    lower_ci        NUMERIC(14,2)   NOT NULL,
    upper_ci        NUMERIC(14,2)   NOT NULL,
    mae             NUMERIC(10,4)   NULL,
    rmse            NUMERIC(10,4)   NULL,
    mape            NUMERIC(10,4)   NULL,
    r2              NUMERIC(10,4)   NULL,
    training_date   DATE            DEFAULT CURRENT_DATE,
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_forecasts_commodity_model ON forecasts(commodity_id, model_name);
CREATE INDEX idx_forecasts_date ON forecasts(forecast_date);
CREATE INDEX idx_forecasts_model ON forecasts(model_name);
```

| Cột | Kiểu PostgreSQL | Ràng buộc | Ghi chú |
|-----|-----------------|-----------|---------|
| `id` | `BIGSERIAL` | `PRIMARY KEY` | Khóa chính |
| `commodity_id` | `INTEGER` | `FK → commodities(id)`, `CASCADE` | **Indexed** |
| `model_name` | `VARCHAR(50)` | `NOT NULL` | `'LSTM'` \| `'XGBoost'` \| `'Random Forest'` \| `'Prophet'` \| `'ARIMA'`, **Indexed** |
| `forecast_date` | `DATE` | `NOT NULL` | Ngày được dự báo (tương lai), **Indexed** |
| `predicted_price` | `NUMERIC(14,2)` | `NOT NULL` | Giá dự báo $\hat{y}_t$ |
| `lower_ci` | `NUMERIC(14,2)` | `NOT NULL` | Cận dưới 95% CI |
| `upper_ci` | `NUMERIC(14,2)` | `NOT NULL` | Cận trên 95% CI |
| `mae` | `NUMERIC(10,4)` | `NULL` | Mean Absolute Error |
| `rmse` | `NUMERIC(10,4)` | `NULL` | Root Mean Squared Error |
| `mape` | `NUMERIC(10,4)` | `NULL` | Mean Absolute Percentage Error (%) |
| `r2` | `NUMERIC(10,4)` | `NULL` | R² Score (Coefficient of Determination) |
| `training_date` | `DATE` | `DEFAULT CURRENT_DATE` | Ngày train mô hình |

---

#### 4.2.5. Bảng `alert_rules` — Quy tắc cảnh báo

```sql
CREATE TABLE alert_rules (
    id              SERIAL          PRIMARY KEY,
    commodity_id    INTEGER         NOT NULL REFERENCES commodities(id) ON DELETE CASCADE,
    user_id         INTEGER         NULL REFERENCES users(id) ON DELETE CASCADE,
    rule_name       VARCHAR(150)    NOT NULL,
    condition_type  VARCHAR(50)     NOT NULL,
    threshold_value NUMERIC(14,2)   NOT NULL,
    email           VARCHAR(150)    NOT NULL,
    is_active       BOOLEAN         DEFAULT TRUE,
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_alert_rules_commodity ON alert_rules(commodity_id);
CREATE INDEX idx_alert_rules_user ON alert_rules(user_id);
```

| Cột | Kiểu PostgreSQL | Ràng buộc | Ghi chú |
|-----|-----------------|-----------|---------|
| `id` | `SERIAL` | `PRIMARY KEY` | Khóa chính |
| `commodity_id` | `INTEGER` | `FK → commodities(id)`, `CASCADE` | **Indexed** |
| `user_id` | `INTEGER` | `FK → users(id)`, `CASCADE`, `NULL` | **Indexed**, nullable (system rules) |
| `condition_type` | `VARCHAR(50)` | `NOT NULL` | Enum: `'PRICE_ABOVE'` \| `'PRICE_BELOW'` \| `'PCT_INC_7D'` \| `'PCT_DEC_7D'` |
| `threshold_value` | `NUMERIC(14,2)` | `NOT NULL` | Ngưỡng kích hoạt (giá VNĐ hoặc %) |
| `is_active` | `BOOLEAN` | `DEFAULT TRUE` | Bật/tắt rule |

---

#### 4.2.6. Bảng `alert_logs` — Nhật ký cảnh báo đã gửi

```sql
CREATE TABLE alert_logs (
    id              BIGSERIAL       PRIMARY KEY,
    rule_id         INTEGER         NOT NULL REFERENCES alert_rules(id) ON DELETE CASCADE,
    triggered_price NUMERIC(14,2)   NOT NULL,
    message         TEXT            NOT NULL,
    status          VARCHAR(30)     DEFAULT 'SENT',
    triggered_at    TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_alert_logs_rule ON alert_logs(rule_id);
CREATE INDEX idx_alert_logs_triggered ON alert_logs(triggered_at);
```

| Cột | Kiểu PostgreSQL | Ràng buộc | Ghi chú |
|-----|-----------------|-----------|---------|
| `id` | `BIGSERIAL` | `PRIMARY KEY` | Khóa chính |
| `rule_id` | `INTEGER` | `FK → alert_rules(id)`, `CASCADE` | **Indexed** |
| `triggered_price` | `NUMERIC(14,2)` | `NOT NULL` | Giá tại thời điểm kích hoạt |
| `message` | `TEXT` | `NOT NULL` | Nội dung cảnh báo đã gửi |
| `status` | `VARCHAR(30)` | `DEFAULT 'SENT'` | `'SENT'` \| `'FAILED'` \| `'PENDING'` |
| `triggered_at` | `TIMESTAMPTZ` | `NOT NULL`, `DEFAULT NOW()` | Thời điểm kích hoạt, **Indexed** |

### 4.3. Tổng hợp Index Strategy

| Bảng | Index | Cột | Loại | Mục đích |
|------|-------|-----|------|----------|
| `users` | `idx_users_email` | `email` | `UNIQUE` | Login lookup O(1) |
| `commodities` | `idx_commodities_code` | `code` | `UNIQUE` | Tìm nông sản theo mã |
| `price_history` | `idx_price_history_commodity_date` | `commodity_id, record_date` | `COMPOSITE` | Query chuỗi thời gian |
| `price_history` | `idx_price_history_date` | `record_date` | `BTREE` | Filter theo khoảng thời gian |
| `forecasts` | `idx_forecasts_commodity_model` | `commodity_id, model_name` | `COMPOSITE` | Dashboard lookup |
| `forecasts` | `idx_forecasts_date` | `forecast_date` | `BTREE` | Range query dự báo |
| `forecasts` | `idx_forecasts_model` | `model_name` | `BTREE` | So sánh mô hình |
| `alert_rules` | `idx_alert_rules_commodity` | `commodity_id` | `BTREE` | Đánh giá rules theo nông sản |
| `alert_logs` | `idx_alert_logs_triggered` | `triggered_at` | `BTREE` | Xem lịch sử cảnh báo |

---

## 5. Quy tắc Nghiệp vụ (Core Business Rules)

### 5.1. Tiền xử lý Dữ liệu (Data Preprocessing Pipeline)

#### 5.1.1. Xử lý Missing Data

```
┌──────────────────────────────────────────────────────────────────────┐
│                   MISSING DATA HANDLING                              │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Input: Raw price series with gaps (weekends, holidays, errors)     │
│                                                                      │
│  Step 1: Create full date range (daily frequency)                   │
│  ─────────────────────────────────────────────────────────          │
│  full_range = pd.date_range(start=min_date, end=max_date, freq='D')│
│  df = pd.merge(full_range, raw_data, on='date', how='left')        │
│                                                                      │
│  Step 2: Linear Interpolation (primary)                             │
│  ─────────────────────────────────────                              │
│  Công thức nội suy tuyến tính giữa 2 điểm đã biết (x₁,y₁),(x₂,y₂):│
│                                                                      │
│                    (x - x₁)                                         │
│    y = y₁ + ──────────── × (y₂ - y₁)                               │
│                (x₂ - x₁)                                            │
│                                                                      │
│  df['price'] = df['price'].interpolate(method='linear')             │
│                                                                      │
│  Step 3: Forward Fill + Backward Fill (fallback)                    │
│  ──────────────────────────────────────────────                     │
│  Cho các giá trị đầu/cuối chuỗi không thể nội suy:                │
│                                                                      │
│    • Ffill (Forward Fill): Lấy giá trị liền trước lấp vào          │
│      y_t = y_{t-1}  nếu y_t là NaN                                 │
│                                                                      │
│    • Bfill (Backward Fill): Lấy giá trị liền sau lấp vào           │
│      y_t = y_{t+1}  nếu y_t vẫn là NaN                             │
│                                                                      │
│  df['price'] = df['price'].ffill().bfill()                          │
│                                                                      │
│  Output: Complete daily price series (no missing values)            │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

#### 5.1.2. Xử lý Ngoại lai (Outlier Handling — IQR Capping)

```
┌──────────────────────────────────────────────────────────────────────┐
│                   IQR CAPPING METHOD                                 │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Bước 1: Tính tứ phân vị                                           │
│  ───────────────────────                                            │
│    Q1 = df['price'].quantile(0.25)    // Phân vị 25%               │
│    Q3 = df['price'].quantile(0.75)    // Phân vị 75%               │
│    IQR = Q3 - Q1                       // Khoảng tứ phân vị        │
│                                                                      │
│  Bước 2: Xác định biên giới                                        │
│  ────────────────────────                                           │
│    Lower Bound = Q1 - 1.5 × IQR                                    │
│    Upper Bound = Q3 + 1.5 × IQR                                    │
│                                                                      │
│  Bước 3: Capping (giới hạn giá trị, KHÔNG xóa)                    │
│  ───────────────────────────────────────────────                    │
│    if x < Lower Bound → x = Lower Bound                            │
│    if x > Upper Bound → x = Upper Bound                            │
│    else               → x = x (giữ nguyên)                         │
│                                                                      │
│  ⚠️ Lý do dùng Capping thay vì Drop:                               │
│    Trong chuỗi thời gian, việc xóa điểm dữ liệu phá vỡ tính      │
│    liên tục thời gian. Capping giữ nguyên số lượng quan sát        │
│    đồng thời giảm thiểu ảnh hưởng của giá trị bất thường.          │
│                                                                      │
│  Implementation: handle_outliers_iqr() trong data_loader.py        │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

#### 5.1.3. Kiểm định Tính dừng (Stationarity Test — ADF)

```
┌──────────────────────────────────────────────────────────────────────┐
│               AUGMENTED DICKEY-FULLER (ADF) TEST                     │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Giả thuyết:                                                        │
│    H₀ (Null):        Chuỗi có nghiệm đơn vị → KHÔNG dừng          │
│    H₁ (Alternative): Chuỗi KHÔNG có nghiệm đơn vị → DỪNG          │
│                                                                      │
│  Phương trình hồi quy ADF:                                         │
│                          p                                           │
│    Δyₜ = α + βt + γyₜ₋₁ + Σ δᵢΔyₜ₋ᵢ + εₜ                        │
│                         i=1                                          │
│                                                                      │
│  Trong đó:                                                          │
│    • Δyₜ = yₜ - yₜ₋₁        (sai phân bậc 1)                      │
│    • α: hằng số (drift)                                             │
│    • βt: xu hướng thời gian (trend)                                 │
│    • γ: hệ số kiểm định (test statistic)                           │
│    • p: số bậc trễ (lag order)                                      │
│                                                                      │
│  Quy tắc quyết định:                                               │
│  ┌──────────────────┬──────────────────────────────┐                │
│  │  p-value ≤ 0.05  │  Bác bỏ H₀ → Chuỗi DỪNG    │                │
│  │  p-value > 0.05  │  Chấp nhận H₀ → KHÔNG DỪNG  │                │
│  └──────────────────┴──────────────────────────────┘                │
│                                                                      │
│  Hành động khi chuỗi không dừng:                                   │
│    • ARIMA: Tự động differencing (d parameter)                      │
│    • LSTM/XGBoost: Sử dụng returns hoặc log-returns                │
│    • Prophet: Xử lý nội bộ (trend decomposition)                   │
│                                                                      │
│  Implementation: test_stationarity() trong data_loader.py           │
│                  sử dụng statsmodels.tsa.stattools.adfuller()       │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### 5.2. Công thức Đánh giá Mô hình (Model Evaluation Metrics)

#### 5.2.1. Bảng tổng hợp Chỉ số

| Chỉ số | Tên đầy đủ | Công thức | Ý nghĩa | Đơn vị | Mục tiêu |
|--------|-----------|-----------|---------|--------|----------|
| **MAE** | Mean Absolute Error | Xem bên dưới | Sai số trung bình tuyệt đối, dễ diễn giải | VNĐ/kg | Minimize |
| **RMSE** | Root Mean Squared Error | Xem bên dưới | Phạt mạnh sai số lớn, nhạy với outlier | VNĐ/kg | Minimize |
| **MAPE** | Mean Absolute Percentage Error | Xem bên dưới | Sai số tương đối (%), so sánh cross-commodity | % | Minimize |
| **R²** | Coefficient of Determination | Xem bên dưới | Tỷ lệ phương sai được giải thích bởi mô hình | [0, 1] | Maximize |

#### 5.2.2. Chi tiết Công thức

```
┌──────────────────────────────────────────────────────────────────────┐
│                    MODEL EVALUATION METRICS                          │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Ký hiệu chung:                                                    │
│    n     = Số quan sát (test set size)                              │
│    yₜ    = Giá thực tế tại thời điểm t                             │
│    ŷₜ    = Giá dự báo tại thời điểm t                              │
│    ȳ     = Giá trung bình thực tế                                  │
│                                                                      │
│  ──────────────────────────────────────────────────────────         │
│                                                                      │
│  ① MAE (Mean Absolute Error):                                      │
│                                                                      │
│              1   n                                                   │
│    MAE  =  ─── × Σ  |yₜ - ŷₜ|                                      │
│              n  t=1                                                  │
│                                                                      │
│    Ý nghĩa: Trung bình sai lệch giá dự báo so với giá thực.       │
│    Đơn vị: VNĐ/kg (cùng đơn vị với giá gốc)                       │
│                                                                      │
│  ──────────────────────────────────────────────────────────         │
│                                                                      │
│  ② RMSE (Root Mean Squared Error):                                  │
│               ┌──────────────────┐                                   │
│              │  1   n            │                                   │
│    RMSE = √ │ ─── × Σ (yₜ-ŷₜ)² │                                   │
│              │  n  t=1           │                                   │
│               └──────────────────┘                                   │
│                                                                      │
│    Ý nghĩa: Như MAE nhưng phạt nặng hơn cho sai số lớn.            │
│    Tính chất: RMSE ≥ MAE (luôn luôn)                                │
│                                                                      │
│  ──────────────────────────────────────────────────────────         │
│                                                                      │
│  ③ MAPE (Mean Absolute Percentage Error):                           │
│                                                                      │
│              100%   n   |yₜ - ŷₜ|                                   │
│    MAPE  = ────── × Σ  ──────────                                   │
│               n    t=1     yₜ                                        │
│                                                                      │
│    Ý nghĩa: Sai số tương đối (%), dùng so sánh giữa                │
│    các nông sản có thang giá khác nhau (Lúa ~7K vs Tiêu ~90K).     │
│    ⚠️ Lưu ý: Không xác định khi yₜ = 0.                            │
│                                                                      │
│  ──────────────────────────────────────────────────────────         │
│                                                                      │
│  ④ R² Score (Coefficient of Determination):                         │
│                                                                      │
│                 Σ (yₜ - ŷₜ)²        SS_res                          │
│    R²  = 1 -  ──────────────  = 1 - ───────                         │
│                 Σ (yₜ - ȳ)²         SS_tot                          │
│                                                                      │
│    Diễn giải:                                                       │
│    ┌────────────┬────────────────────────────────────────┐           │
│    │  R² = 1.0  │  Mô hình dự báo hoàn hảo              │           │
│    │  R² > 0.9  │  Mô hình rất tốt (mục tiêu LSTM)     │           │
│    │  R² > 0.8  │  Mô hình tốt                          │           │
│    │  R² < 0.5  │  Mô hình kém, cần cải thiện           │           │
│    │  R² < 0.0  │  Mô hình tệ hơn dự báo bằng trung bình│          │
│    └────────────┴────────────────────────────────────────┘           │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### 5.3. Dải Tin cậy 95% (95% Confidence Interval)

```
┌──────────────────────────────────────────────────────────────────────┐
│              95% CONFIDENCE INTERVAL FORMULA                         │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Công thức dải tin cậy mở rộng theo thời gian:                      │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                                                             │    │
│  │   CI_t = ŷ_t  ±  1.96 × RMSE × √(1 + 0.05t)              │    │
│  │                                                             │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  Trong đó:                                                          │
│    • ŷ_t    : Giá dự báo tại bước t (predicted_price)              │
│    • 1.96   : Z-score cho mức tin cậy 95%                          │
│    •           (P(-1.96 ≤ Z ≤ 1.96) = 0.95)                       │
│    • RMSE   : Root Mean Squared Error trên tập test                │
│    • t      : Bước dự báo (1, 2, ..., T)                          │
│    • 0.05   : Hệ số mở rộng độ bất định theo thời gian            │
│    • √(1+0.05t): Fan-out factor — CI mở rộng khi t tăng           │
│                                                                      │
│  Cận trên/dưới:                                                    │
│    upper_ci = ŷ_t + 1.96 × RMSE × √(1 + 0.05t)                   │
│    lower_ci = ŷ_t - 1.96 × RMSE × √(1 + 0.05t)                   │
│                                                                      │
│  Ví dụ minh họa (RMSE = 610.2 VNĐ/kg):                            │
│  ┌──────┬───────────┬──────────┬───────────┬───────────┐            │
│  │ Bước │ √(1+0.05t)│  Margin  │ Lower CI  │ Upper CI  │            │
│  │  t   │           │  (VNĐ)   │   (VNĐ)   │   (VNĐ)   │            │
│  ├──────┼───────────┼──────────┼───────────┼───────────┤            │
│  │  T+1 │   1.025   │ ±1,226   │  ŷ-1,226  │  ŷ+1,226  │            │
│  │  T+3 │   1.074   │ ±1,284   │  ŷ-1,284  │  ŷ+1,284  │            │
│  │  T+7 │   1.170   │ ±1,399   │  ŷ-1,399  │  ŷ+1,399  │            │
│  │ T+14 │   1.338   │ ±1,600   │  ŷ-1,600  │  ŷ+1,600  │            │
│  │ T+30 │   1.581   │ ±1,891   │  ŷ-1,891  │  ŷ+1,891  │            │
│  └──────┴───────────┴──────────┴───────────┴───────────┘            │
│                                                                      │
│  Trực quan hóa:                                                     │
│                                                                      │
│  Giá (VNĐ/kg)                                                      │
│    │            ╱ Upper CI (fan-out)                                 │
│    │    ╱╲   ╱╱╱╱╱╱╱╱╱╱                                            │
│    │   ╱  ╲╱╱───── Predicted (ŷ_t)                                  │
│    │  ╱  ╱╲╲╲╲╲╲╲╲╲╲                                               │
│    │ ╱╱╱╱    ╲ Lower CI (fan-out)                                   │
│    │╱                                                                │
│    └────────┬──────────────────▶ Thời gian (t)                      │
│          Hiện tại                                                    │
│      ◀─History─▶◀───── Forecast ──────▶                             │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### 5.4. Quy tắc Cảnh báo Thị trường (Alert Engine Rules)

```
┌──────────────────────────────────────────────────────────────────────┐
│                    ALERT ENGINE BUSINESS RULES                       │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  condition_type         Quy tắc kích hoạt                           │
│  ──────────────         ──────────────────                          │
│                                                                      │
│  PRICE_ABOVE            current_price > threshold_value             │
│                         "Giá {commodity} VƯỢT ngưỡng {threshold}"   │
│                                                                      │
│  PRICE_BELOW            current_price < threshold_value             │
│                         "Giá {commodity} DƯỚI ngưỡng {threshold}"   │
│                                                                      │
│  PCT_INC_7D             price_change_7d% > threshold_value          │
│                         "Giá {commodity} TĂNG {pct}% trong 7 ngày" │
│                                                                      │
│  PCT_DEC_7D             price_change_7d% < -threshold_value         │
│                         "Giá {commodity} GIẢM {pct}% trong 7 ngày" │
│                                                                      │
│  ────────────────────────────────────────────────────────────       │
│                                                                      │
│  Công thức biến động %:                                             │
│                                                                      │
│                 price_today - price_7d_ago                           │
│    Δ%₇ ngày =  ─────────────────────────── × 100%                  │
│                      price_7d_ago                                    │
│                                                                      │
│  ────────────────────────────────────────────────────────────       │
│                                                                      │
│  Lịch đánh giá (APScheduler):                                      │
│    • 06:30 sáng — Sau khi scraper cập nhật giá mới (06:00)         │
│    • 18:30 chiều — Kiểm tra lần 2 (phiên giao dịch chiều)         │
│                                                                      │
│  Luồng xử lý:                                                      │
│    1. Fetch all active rules (is_active = TRUE)                     │
│    2. For each rule:                                                │
│       a. Get latest price for rule.commodity_id                     │
│       b. Evaluate condition_type against threshold_value            │
│       c. If triggered:                                              │
│          - Create alert_log record (status = 'SENT')                │
│          - Send email via SMTP (Gmail)                              │
│       d. If SMTP fails:                                             │
│          - Create alert_log record (status = 'FAILED')              │
│    3. Return count of triggered rules                               │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 6. Tiêu chuẩn Mã nguồn (Code Standards)

### 6.1. Quy chuẩn REST API

#### 6.1.1. URL Convention

```
Base URL:   /api/v1
Format:     /api/v1/{resource}/{id?}/{sub-resource?}
```

| Method | Endpoint | Mô tả | Auth |
|--------|----------|-------|------|
| **Authentication** | | | |
| `POST` | `/api/v1/auth/register` | Đăng ký tài khoản | Public |
| `POST` | `/api/v1/auth/login` | Đăng nhập → JWT Token | Public |
| `GET` | `/api/v1/auth/me` | Thông tin user hiện tại | Bearer |
| **Commodities** | | | |
| `GET` | `/api/v1/commodities` | Danh sách nông sản | Public |
| `GET` | `/api/v1/commodities/{id}` | Chi tiết 1 nông sản | Public |
| `GET` | `/api/v1/commodities/{id}/prices` | Lịch sử giá | Public |
| `GET` | `/api/v1/commodities/{id}/regional-prices` | Giá theo vùng miền | Public |
| **Forecast** | | | |
| `GET` | `/api/v1/forecast/dashboard` | Dashboard dự báo | Public |
| `GET` | `/api/v1/forecast/compare/{commodity_id}` | So sánh mô hình | Public |
| `POST` | `/api/v1/predictions/predict` | Dự báo realtime | Bearer |
| `POST` | `/api/v1/predictions/train` | Huấn luyện mô hình | Admin |
| **Alerts** | | | |
| `GET` | `/api/v1/alerts` | Danh sách alert rules | Bearer |
| `POST` | `/api/v1/alerts` | Tạo alert rule | Bearer |
| `PUT` | `/api/v1/alerts/{id}` | Cập nhật alert rule | Bearer |
| `DELETE` | `/api/v1/alerts/{id}` | Xóa alert rule | Bearer |
| **Admin** | | | |
| `GET` | `/api/v1/admin/dashboard` | Thống kê hệ thống | Admin |
| `GET` | `/api/v1/admin/users` | Quản lý user | Admin |
| `POST` | `/api/v1/admin/scrape` | Trigger scraper thủ công | Admin |
| **System** | | | |
| `GET` | `/` | Thông tin API | Public |
| `GET` | `/health` | Health check + DB status | Public |

#### 6.1.2. Định dạng Phản hồi Chuẩn (Standard JSON Response)

```
┌──────────────────────────────────────────────────────────────────────┐
│                 STANDARD API RESPONSE FORMAT                         │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Cấu trúc JSON chung cho MỌI endpoint:                             │
│                                                                      │
│  {                                                                   │
│    "success":     bool,       // true = thành công                  │
│    "status_code": int,        // HTTP status code (200, 201, ...)   │
│    "message":     str,        // Mô tả kết quả                     │
│    "data":        any         // Payload (object | array | null)    │
│  }                                                                   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

**Ví dụ Response thành công (200 OK):**
```json
{
  "success": true,
  "status_code": 200,
  "message": "Lấy danh sách nông sản thành công",
  "data": [
    {
      "id": 1,
      "code": "LUA_IR504",
      "name": "Lúa gạo IR504",
      "category": "Lương thực",
      "unit": "VNĐ/kg",
      "region": "Đồng bằng sông Cửu Long"
    }
  ]
}
```

**Ví dụ Response lỗi (401 Unauthorized):**
```json
{
  "success": false,
  "status_code": 401,
  "message": "Chưa xác thực hoặc thiếu Access Token",
  "data": null
}
```

**Ví dụ Response lỗi (404 Not Found):**
```json
{
  "success": false,
  "status_code": 404,
  "message": "Không tìm thấy nông sản",
  "data": null
}
```

**Ví dụ Response lỗi (500 Internal Server Error):**
```json
{
  "success": false,
  "status_code": 500,
  "message": "Đã xảy ra lỗi nội bộ máy chủ. Vui lòng thử lại sau.",
  "data": null
}
```

#### 6.1.3. Forecast Dashboard Response (Specialized)

```json
{
  "commodity": {
    "id": 2,
    "code": "CA_PHE_ROBUSTA",
    "name": "Cà phê Robusta",
    "unit": "VNĐ/kg",
    "region": "Tây Nguyên"
  },
  "modelName": "LSTM",
  "metrics": {
    "modelName": "LSTM",
    "mae": 420.5,
    "rmse": 610.2,
    "mape": 1.12,
    "r2": 0.942,
    "trainDate": "05/09/2026"
  },
  "forecastData": [
    {
      "date": "08/09",
      "actualPrice": 125300.0,
      "predictedPrice": 125300.0,
      "lowerCI": 125300.0,
      "upperCI": 125300.0,
      "isForecast": false
    },
    {
      "date": "12/09 (T+1)",
      "actualPrice": null,
      "predictedPrice": 126150.5,
      "lowerCI": 124924.3,
      "upperCI": 127376.7,
      "isForecast": true
    }
  ]
}
```

### 6.2. Quy chuẩn Cấu trúc Dự án

```
DA_TN/
├── backend/
│   ├── app/
│   │   ├── main.py                    # FastAPI entry point + lifespan
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── api.py             # Router aggregator
│   │   │       └── endpoints/
│   │   │           ├── auth.py        # Login / Register / Me
│   │   │           ├── commodities.py # CRUD nông sản
│   │   │           ├── prices.py      # Lịch sử giá
│   │   │           ├── forecast.py    # Dashboard dự báo
│   │   │           ├── predictions.py # Predict / Train endpoints
│   │   │           ├── alerts.py      # CRUD cảnh báo
│   │   │           └── admin.py       # Admin panel API
│   │   ├── core/
│   │   │   ├── config.py             # Settings (pydantic-settings)
│   │   │   ├── database.py           # SQLAlchemy engine + session
│   │   │   ├── deps.py              # Dependency injection (auth)
│   │   │   ├── security.py          # JWT + bcrypt + middleware
│   │   │   ├── auth.py              # Auth business logic
│   │   │   └── scheduler.py         # APScheduler (cron jobs)
│   │   ├── models/
│   │   │   └── models.py            # SQLAlchemy ORM models (6 tables)
│   │   ├── schemas/
│   │   │   └── schemas.py           # Pydantic v2 request/response
│   │   └── services/
│   │       ├── forecast_service.py   # Forecast business logic
│   │       ├── alert_service.py      # Alert evaluation + email
│   │       └── commodity_service.py  # Commodity CRUD + price logic
│   ├── ml_pipeline/
│   │   ├── data_loader.py           # Data ingestion + preprocessing
│   │   ├── feature_engineering.py   # Feature extraction
│   │   ├── model_trainer.py         # Multi-model trainer
│   │   ├── predictor.py             # Inference + CI calculation
│   │   ├── scraper.py               # Web scraper (4 sources)
│   │   ├── train_lstm.py            # Stacked LSTM (PyTorch)
│   │   ├── train_ml.py              # XGBoost + Random Forest
│   │   ├── train_prophet.py         # Facebook Prophet
│   │   ├── baseline_arima.py        # ARIMA/SARIMAX baseline
│   │   ├── train_all_and_save.py    # Batch training script
│   │   └── saved_models/            # Serialized models (.pt, .pkl)
│   ├── tests/                        # pytest test suite
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   └── src/
│       ├── app/                      # Next.js 14 App Router pages
│       ├── components/               # React components (dashboard, ...)
│       ├── lib/                      # Utilities, API client, types
│       └── types/                    # TypeScript type definitions
├── database/                         # SQL migrations & seed scripts
├── docs/                            # Project documentation
│   ├── REQUIREMENTS_PLAN.md         # ← Tài liệu này
│   ├── phase_1_spec.md → phase_7_spec.md
│   ├── implementation_plan.md
│   ├── implementation_checklist.md
│   ├── api_reference.md
│   ├── setup_guide.md
│   ├── security_audit_report.md
│   └── security_operations.md
└── README.md
```

### 6.3. Quy chuẩn Code Style

| Ngôn ngữ | Convention | Ví dụ |
|-----------|-----------|-------|
| **Python** (Backend) | snake_case (functions, variables) | `get_forecast_dashboard()`, `commodity_id` |
| **Python** (Classes) | PascalCase | `ForecastService`, `PriceHistory` |
| **Python** (Constants) | UPPER_SNAKE_CASE | `ACCESS_TOKEN_EXPIRE_MINUTES`, `API_V1_STR` |
| **TypeScript** (Components) | PascalCase | `ForecastChart.tsx`, `RegionalPriceTable.tsx` |
| **TypeScript** (Functions) | camelCase | `fetchForecastData()`, `handleSubmit()` |
| **TypeScript** (Types) | PascalCase | `CommodityResponse`, `ForecastPoint` |
| **SQL** (Tables) | snake_case (plural) | `price_history`, `alert_rules` |
| **SQL** (Columns) | snake_case | `commodity_id`, `forecast_date` |
| **API** (Endpoints) | kebab-case (URL), snake_case (query params) | `/api/v1/regional-prices?commodity_id=2` |
| **API** (Response fields) | camelCase (JSON) | `{ "modelName": "LSTM", "forecastData": [...] }` |

### 6.4. Ngưỡng Chất lượng Mô hình (Model Quality Gates)

| Chỉ số | Mục tiêu LSTM | Ngưỡng chấp nhận (tất cả models) | Cảnh báo đỏ |
|--------|--------------|----------------------------------|-------------|
| **MAE** | ≤ 500 VNĐ/kg | ≤ 1,000 VNĐ/kg | > 1,500 VNĐ/kg |
| **RMSE** | ≤ 700 VNĐ/kg | ≤ 1,200 VNĐ/kg | > 2,000 VNĐ/kg |
| **MAPE** | ≤ 1.5% | ≤ 3.0% | > 5.0% |
| **R²** | ≥ 0.93 | ≥ 0.80 | < 0.60 |

---

> **📝 Ghi chú cuối:**  
> Tài liệu này phản ánh trạng thái thực tế của codebase AgroForecast tính đến ngày 10/09/2026. Mọi thay đổi kiến trúc hoặc schema cần được cập nhật đồng bộ tại đây và trong `docs/implementation_plan.md`.

---

*Tạo bởi: AgroForecast Architecture Team — Đồ án Tốt nghiệp 2026*
