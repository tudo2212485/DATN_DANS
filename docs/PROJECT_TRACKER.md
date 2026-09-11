# 📊 PROJECT TRACKER — AgroForecast

## Hệ thống Dự báo Giá Nông sản & Cảnh báo Thị trường Ứng dụng Deep Learning

> **Cập nhật lần cuối:** 10/09/2026 — 21:55 (GMT+7)  
> **Phiên bản hiện tại:** v2.4.1

---

### 🛠️ Technology Stack

| Layer | Công nghệ | Phiên bản |
|-------|-----------|-----------|
| **Frontend** | Next.js 14 (App Router), TypeScript, Tailwind CSS, Recharts, Lucide Icons | Next 14.x |
| **Backend** | Python FastAPI, Pydantic v2, SQLAlchemy 2.x ORM, Uvicorn | FastAPI ≥0.110 |
| **ML / DL** | PyTorch (Stacked LSTM), XGBoost, Random Forest, Prophet, ARIMA | PyTorch ≥2.2 |
| **Database** | PostgreSQL 15, APScheduler (BackgroundScheduler) | PG 15 |
| **Security** | JWT (HS256) + OAuth2PasswordBearer + bcrypt + OWASP Headers | — |
| **Testing** | Pytest, HTTPX (TestClient) | Pytest ≥8.0 |

### 📌 Quy ước đánh dấu

| Ký hiệu | Ý nghĩa |
|----------|---------|
| `- [x]` | ✅ Đã hoàn thành — code tồn tại, đã test, hoạt động |
| `- [~]` | 🔶 Hoàn thành một phần — tồn tại nhưng cần cải thiện/bổ sung |
| `- [ ]` | ⬜ Chưa thực hiện — cần triển khai |

---

## 📋 Bảng Tổng quan Tiến độ Phân hệ

| # | Phân hệ chức năng | Backend (FastAPI) | Frontend (Next.js) | AI Engine / Pipeline | Tỷ lệ hoàn thành |
|---|-------------------|:-----------------:|:------------------:|:--------------------:|:-----------------:|
| 1 | **Auth & RBAC** | ✅ Done | ✅ Done | — | **95%** |
| 2 | **Market Overview (Trang chủ)** | ✅ Done | ✅ Done | — | **95%** |
| 3 | **ML Forecast & Model Comparison** | ✅ Done | ✅ Done | 🔶 4/5 models trained | **85%** |
| 4 | **Alert System & Email** | ✅ Done | ✅ Done | ✅ Scheduler Done | **90%** |
| 5 | **Admin Data Management** | ✅ Done | ✅ Done | ✅ Tasks/Retrain Done | **90%** |
| 6 | **Đóng gói & Báo cáo** | ⬜ Docker chưa có | ⬜ Docker chưa có | 🔶 Pytest có 8 files | **35%** |

**Tổng tiến độ ước tính: ~82%**

---

## Module 1: Cào & Tiền xử lý Dữ liệu (Data Ingestion & Preprocessing)

### 1.1. Web Scraper — `ml_pipeline/scraper.py`

- [x] Cào giá cà phê nội địa từ `giacaphe.com` bằng `BeautifulSoup4`
- [x] Cào giá nông sản từ nguồn Sở NN&PTNT / Hiệp hội
- [x] Hàm `scrape_and_update_db(days)` — ghi kết quả trực tiếp vào bảng `price_history` PostgreSQL
- [x] Xử lý trùng lặp (upsert: nếu trùng `commodity_id + record_date` thì update)
- [x] Hỗ trợ tham số `days` để giới hạn phạm vi cào

### 1.2. Biến ngoại sinh — `ml_pipeline/data_loader.py :: get_exogenous_data()`

- [x] Fetch tỷ giá **USD/VND** (`USDVND=X`) qua `yfinance` API
- [x] Fetch giá **Dầu thô WTI** (`CL=F`) qua `yfinance` API
- [x] Merge outer join 2 chuỗi exogenous, xử lý MultiIndex columns
- [x] Forward Fill + Backward Fill cho dữ liệu exogenous bị thiếu

### 1.3. Tiền xử lý — `ml_pipeline/data_loader.py :: load_clean_data()`

- [x] Tạo full date range (daily frequency) lấp đầy ngày thiếu
- [x] Missing data: **Linear Interpolation** `df['price'].interpolate(method='linear')`
- [x] Missing data fallback: **Forward Fill** `.ffill()` + **Backward Fill** `.bfill()`
- [x] Xử lý ngoại lai: **IQR Capping** — `handle_outliers_iqr()` (Q1−1.5×IQR, Q3+1.5×IQR)
- [x] Kiểm định tính dừng: **Augmented Dickey-Fuller test** — `test_stationarity()` (p-value ≤ 0.05)
- [x] Merge biến ngoại sinh (USD/VND, Crude Oil) vào dataframe chính

### 1.4. Feature Engineering — `ml_pipeline/feature_engineering.py`

- [x] File `feature_engineering.py` tồn tại (1,192 bytes)
- [~] Lag features, rolling mean/std — cơ bản có, cần mở rộng thêm feature
- [ ] Tính toán RSI, Bollinger Bands (nếu cần cho báo cáo nâng cao)

### 1.5. Cron Job tự động — `app/core/scheduler.py`

- [x] `APScheduler BackgroundScheduler` khởi động cùng FastAPI lifespan
- [x] Job `daily_scraper`: CronTrigger **06:00** hàng ngày → `scrape_and_update_db(days=1)`
- [x] Job `daily_alert_evaluation`: CronTrigger **06:30, 18:30** → `evaluate_all_alert_rules()`
- [x] Hàm `start_scheduler()` / `stop_scheduler()` quản lý lifecycle

### 1.6. Seed & Init Database

- [x] File `database/init.sql` — DDL schema khởi tạo (18,355 bytes)
- [x] File `database/load_database.py` — Script nạp dữ liệu ban đầu
- [x] File `backend/seed_db.py` — Seed 4 nông sản + dữ liệu mẫu

---

## Module 2: Huấn luyện 5 Mô hình ML/DL (Model Training Pipeline)

### 2.1. ARIMA / SARIMAX (Baseline) — `ml_pipeline/baseline_arima.py`

- [x] File `baseline_arima.py` tồn tại (4,608 bytes)
- [x] Hàm `run_arima()` — huấn luyện ARIMA cho từng commodity
- [x] Auto-differencing cho chuỗi không dừng
- [ ] Lưu model ARIMA dạng `.pkl` vào `saved_models/` (⚠️ chưa thấy file arima_model.pkl)
- [ ] Ghi `arima_metrics.json` vào `saved_models/{commodity}/`

### 2.2. Facebook Prophet — `ml_pipeline/train_prophet.py`

- [x] File `train_prophet.py` tồn tại (5,074 bytes)
- [x] Hàm `run_prophet()` — huấn luyện Prophet với daily seasonality
- [x] Lưu model → `saved_models/{commodity}/prophet_model.pkl` ✅ (4/4 commodities)
- [x] Ghi metrics → `saved_models/{commodity}/prophet_metrics.json` ✅ (4/4 commodities)

### 2.3. XGBoost — `ml_pipeline/train_ml.py`

- [x] File `train_ml.py` tồn tại (6,796 bytes)
- [x] Hàm `run_ml_models()` — huấn luyện XGBoost Regressor
- [x] Lưu model → `saved_models/{commodity}/xgboost_model.pkl` ✅ (4/4 commodities)
- [x] Ghi metrics → `saved_models/{commodity}/xgboost_metrics.json` ✅ (4/4 commodities)
- [x] Lưu feature list → `saved_models/{commodity}/xgboost_features.json` ✅ (4/4 commodities)

### 2.4. Random Forest — `ml_pipeline/train_ml.py`

- [x] Logic Random Forest nằm chung trong `train_ml.py`
- [ ] Lưu model → `saved_models/{commodity}/rf_model.pkl` (⚠️ chưa thấy artifact riêng)
- [ ] Ghi `rf_metrics.json` vào `saved_models/` (⚠️ chưa có)
- [ ] Feature importance analysis & visualization cho báo cáo

### 2.5. PyTorch Stacked LSTM (Deep Learning) — `ml_pipeline/train_lstm.py`

- [x] File `train_lstm.py` tồn tại (6,688 bytes)
- [x] Hàm `run_lstm()` — huấn luyện Stacked LSTM 2 lớp
- [x] Lưu model → `saved_models/{commodity}/lstm_model.pt` ✅ (4/4 commodities, ~208KB mỗi file)
- [x] Lưu scaler → `saved_models/{commodity}/lstm_scaler.pkl` ✅ (4/4 commodities)
- [x] Ghi metrics → `saved_models/{commodity}/lstm_metrics.json` ✅ (4/4 commodities)
- [x] Features: `["price", "usd_vnd", "crude_oil"]`, seq_length=14
- [~] Hyperparameter tuning — đang dùng cấu hình mặc định, cần grid search / optuna

### 2.6. Batch Training — `ml_pipeline/train_all_and_save.py`

- [x] Script chạy huấn luyện toàn bộ 4 nông sản × 5 mô hình (4,353 bytes)

### 2.7. Predictor / Inference — `ml_pipeline/predictor.py`

- [x] Class `PricePredictor` — inference engine thống nhất cho tất cả model (19,254 bytes)
- [x] Hàm `forecast(model_name, days, include_history, use_cache)` — dự báo realtime
- [x] Tính toán 95% Confidence Interval: `ŷ_t ± 1.96 × RMSE × √(1 + 0.05t)`
- [x] In-Memory Cache cho response time < 100ms
- [x] Hàm `get_metrics_summary()` — tổng hợp metrics tất cả model
- [x] Hàm `clear_prediction_cache()` — xóa cache sau retrain

### 2.8. Model Trainer — `ml_pipeline/model_trainer.py`

- [x] Class `ModelTrainer` — orchestrator huấn luyện tất cả model (13,174 bytes)
- [x] Hàm `train_all(df)` — gọi tuần tự LSTM → XGBoost → Prophet → ARIMA

### 📊 Trạng thái Saved Models theo Commodity

| Commodity | LSTM `.pt` | LSTM Scaler | XGBoost `.pkl` | Prophet `.pkl` | RF `.pkl` | ARIMA `.pkl` |
|-----------|:----------:|:-----------:|:--------------:|:--------------:|:---------:|:------------:|
| COFFEE_ROBUSTA | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ |
| RICE_IR504 | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ |
| PEPPER_BLACK | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ |
| SUGARCANE | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ |

---

## Module 3: RESTful API Backend (FastAPI)

### 3.1. Cấu trúc Core — `app/core/`

- [x] `config.py` — Settings với `pydantic-settings`, load `.env`, JWT config
- [x] `database.py` — SQLAlchemy engine + `SessionLocal` + `get_db()` dependency
- [x] `security.py` — `verify_password()`, `get_password_hash()`, `create_access_token()`, `decode_access_token()`
- [x] `security.py` — `RateLimiter` class (Sliding Window: 25 req/60s auth, 10 req/60s tasks)
- [x] `security.py` — `SecurityHeadersMiddleware` (OWASP: X-Content-Type-Options, X-Frame-Options, HSTS, v.v.)
- [x] `security.py` — `sanitize_text()` — strip HTML tags + `html.escape()`
- [x] `deps.py` — `OAuth2PasswordBearer`, `get_current_user()`, `get_optional_current_user()`, `require_role()`
- [x] `auth.py` — Auth business logic (1,932 bytes)
- [x] `scheduler.py` — APScheduler lifecycle management

### 3.2. ORM Models — `app/models/models.py`

- [x] Model `User` — bảng `users` (id, email, password_hash, full_name, role, is_active)
- [x] Model `Commodity` — bảng `commodities` (id, code, name, category, unit, region)
- [x] Model `PriceHistory` — bảng `price_history` (id BigInt, commodity_id FK, record_date, price NUMERIC(14,2))
- [x] Model `Forecast` — bảng `forecasts` (id BigInt, model_name, predicted_price, lower_ci, upper_ci, mae, rmse, mape, r2)
- [x] Model `AlertRule` — bảng `alert_rules` (condition_type, threshold_value, email, is_active)
- [x] Model `AlertLog` — bảng `alert_logs` (triggered_price, message, status, triggered_at)
- [x] Relationship ORM: User↔AlertRule, Commodity↔PriceHistory/Forecast/AlertRule, AlertRule↔AlertLog
- [x] CASCADE delete trên tất cả foreign keys
- [x] Index trên `commodity_id`, `record_date`, `model_name`, `email`

### 3.3. Pydantic Schemas — `app/schemas/schemas.py` + `user.py`

- [x] Auth: `LoginRequest`, `RegisterRequest`, `TokenResponse`, `TokenPayload`, `UserResponse`
- [x] Commodity: `CommodityBase`, `CommodityCreate`, `CommodityResponse`
- [x] Overview: `SparklinePoint`, `CommodityOverviewCard`, `MarketComparisonPoint`, `SpotlightSummaryResponse`, `RegionalPriceResponse`
- [x] Price: `PriceHistoryBase`, `PriceHistoryResponse`
- [x] Forecast: `ForecastPointResponse`, `ModelMetricsResponse`, `ForecastDashboardResponse`
- [x] Alert: `AlertRuleCreate`, `AlertRuleResponse`, `AlertRuleToggle`, `AlertLogResponse`
- [x] Admin: `AdminStatsResponse`, `PriceCreateManual`, `AdminPriceItem`, `TaskRunResponse`, `RetrainResponse`
- [x] ML: `PredictionPointItem`, `PredictionMetricsItem`, `PredictionForecastResponse`, `PredictionModelMetric`, `PredictionMetricsResponse`
- [x] Phase 5: `CrawlerLogItem`, `CSVImportResponse`, `UserRoleUpdate`, `UserStatusUpdate`, `ActiveModelSetting`

### 3.4. API Endpoints — `app/api/v1/endpoints/`

#### 🔐 Auth — `auth.py` (3,782 bytes)

| Endpoint | Method | Mô tả | Auth | Trạng thái |
|----------|--------|-------|------|:----------:|
| `/api/v1/auth/register` | POST | Đăng ký tài khoản | Public | ✅ |
| `/api/v1/auth/login` | POST | Đăng nhập → JWT | Public | ✅ |
| `/api/v1/auth/me` | GET | Thông tin user hiện tại | Bearer | ✅ |

- [x] Rate Limit trên register (25 req/60s per IP)
- [x] Rate Limit trên login (25 req/60s per IP)
- [x] Kiểm tra `is_active` trước khi cấp token
- [x] `sanitize_text()` cho `full_name` khi register

#### 🌾 Commodities — `commodities.py` (3,316 bytes)

| Endpoint | Method | Mô tả | Auth | Trạng thái |
|----------|--------|-------|------|:----------:|
| `/api/v1/commodities` | GET | Danh sách nông sản | Public | ✅ |
| `/api/v1/commodities` | POST | Tạo nông sản | Admin | ✅ |
| `/api/v1/commodities/{id}` | PUT | Cập nhật nông sản | Admin | ✅ |
| `/api/v1/commodities/{id}` | DELETE | Xóa nông sản | Admin | ✅ |
| `/api/v1/commodities/overview` | GET | 4 thẻ overview + sparkline | Public | ✅ |
| `/api/v1/commodities/comparison` | GET | Chart so sánh % biến động | Public | ✅ |
| `/api/v1/commodities/spotlight` | GET | Tiêu điểm nông sản 3 tháng | Public | ✅ |
| `/api/v1/commodities/regional-prices` | GET | Bảng giá vùng miền | Public | ✅ |

#### 💰 Prices — `prices.py` (863 bytes)

| Endpoint | Method | Mô tả | Auth | Trạng thái |
|----------|--------|-------|------|:----------:|
| `/api/v1/prices/history` | GET | Lịch sử giá (query: commodity_id, days) | Public | ✅ |

#### 📈 Forecast (Legacy) — `forecast.py` (1,278 bytes)

| Endpoint | Method | Mô tả | Auth | Trạng thái |
|----------|--------|-------|------|:----------:|
| `/api/v1/forecast` | GET | Dashboard dự báo (commodity_id, model_name, days) | Public | ✅ |
| `/api/v1/forecast/compare/{commodity_id}` | GET | So sánh 5 mô hình (MAE, RMSE, MAPE, R²) | Public | ✅ |

#### 🤖 Predictions & ML — `predictions.py` (5,947 bytes)

| Endpoint | Method | Mô tả | Auth | Trạng thái |
|----------|--------|-------|------|:----------:|
| `/api/v1/predictions/forecast` | GET | Dự báo realtime (symbol/id, model, days, cache) | Public | ✅ |
| `/api/v1/predictions/metrics` | GET | Metrics tất cả model cho 1 commodity | Public | ✅ |
| `/api/v1/predictions/retrain` | POST | Trigger retrain background task | Bearer | ✅ |

- [x] In-Memory Cache (`use_cache=True`)
- [x] Background retrain via `BackgroundTasks`
- [x] `clear_prediction_cache()` sau retrain

#### 🔔 Alerts — `alerts.py` (1,947 bytes)

| Endpoint | Method | Mô tả | Auth | Trạng thái |
|----------|--------|-------|------|:----------:|
| `/api/v1/alerts` | GET | Danh sách alert rules | Public | ✅ |
| `/api/v1/alerts` | POST | Tạo alert rule mới | Public | ✅ |
| `/api/v1/alerts/{id}/toggle` | PATCH | Bật/tắt rule | Public | ✅ |
| `/api/v1/alerts/{id}` | DELETE | Xóa rule | Public | ✅ |
| `/api/v1/alerts/{id}/test` | POST | Gửi test email | Public | ✅ |
| `/api/v1/alerts/logs` | GET | Lịch sử cảnh báo đã gửi | Public | ✅ |

#### 🛡️ Admin — `admin.py` (24,170 bytes — file lớn nhất)

| Endpoint | Method | Mô tả | Auth | Trạng thái |
|----------|--------|-------|------|:----------:|
| `/api/v1/admin/stats` | GET | Thống kê hệ thống | Admin | ✅ |
| `/api/v1/admin/commodities` | GET | List nông sản (admin) | Admin | ✅ |
| `/api/v1/admin/commodities` | POST | Tạo nông sản | Admin | ✅ |
| `/api/v1/admin/commodities/{id}` | PUT | Cập nhật nông sản | Admin | ✅ |
| `/api/v1/admin/commodities/{id}` | DELETE | Xóa nông sản + cascade | Admin | ✅ |
| `/api/v1/admin/prices/recent` | GET | Bản ghi giá gần nhất | Admin | ✅ |
| `/api/v1/admin/prices` | POST | Thêm/cập nhật giá thủ công | Admin | ✅ |
| `/api/v1/admin/prices/{id}` | DELETE | Xóa bản ghi giá | Admin | ✅ |
| `/api/v1/admin/prices/import-csv` | POST | Import CSV vào DB | Admin | ✅ |
| `/api/v1/admin/prices/export-csv` | GET | Export CSV để tải về | Admin/Analyst | ✅ |
| `/api/v1/admin/tasks/scrape` | POST | Trigger scraper nền | Admin | ✅ |
| `/api/v1/admin/tasks/retrain` | POST | Trigger retrain nền | Admin | ✅ |
| `/api/v1/admin/users` | GET | Danh sách users | Admin | ✅ |
| `/api/v1/admin/users` | POST | Tạo user mới | Admin | ✅ |
| `/api/v1/admin/users/{id}/role` | PATCH | Đổi role | Admin | ✅ |
| `/api/v1/admin/users/{id}/toggle-status` | PATCH | Khóa/mở tài khoản | Admin | ✅ |
| `/api/v1/admin/logs/crawler` | GET | Nhật ký bot cào | Admin/Analyst | ✅ |
| `/api/v1/admin/models/active` | GET | Model mặc định hiện tại | Admin/Analyst | ✅ |
| `/api/v1/admin/models/active` | POST | Chuyển model mặc định | Admin | ✅ |

### 3.5. Services Layer — `app/services/`

- [x] `forecast_service.py` — `get_forecast_dashboard()`, `get_forecast_comparison()` (6,343 bytes)
- [x] `alert_service.py` — `evaluate_all_alert_rules()`, `send_email_notification()`, CRUD rules, `send_test_alert()` (10,844 bytes)
- [x] `commodity_service.py` — `get_commodities_overview()`, `get_market_comparison()`, `get_spotlight_commodity()`, `get_regional_prices_list()` (9,324 bytes)

---

## Module 4: Giao diện Dashboard (Frontend Next.js 14)

### 4.1. Layout & Navigation

- [x] `app/layout.tsx` — Root layout, font Plus Jakarta Sans, metadata SEO
- [x] `app/globals.css` — Theme "be sữa" (#F9F6F2 background, #2D231E text, #9C6644 accent)
- [x] `components/layout/Sidebar.tsx` — Sidebar navigation chính (10,544 bytes)
- [x] `components/layout/Header.tsx` — Top header bar (1,570 bytes)
- [x] `components/layout/LayoutWrapper.tsx` — Layout wrapper responsive (2,107 bytes)
- [x] Custom scrollbar styling (thin, rounded, color #D4CEBE)
- [x] Animation `pulse-live` cho live indicators

### 4.2. Trang Chủ (Landing / Market Overview) — `app/page.tsx`

- [x] `app/page.tsx` — Trang Tổng quan thị trường (5,575 bytes)
- [x] `components/dashboard/CommodityCard.tsx` — Thẻ nông sản 4 loại + sparkline (2,794 bytes)
- [x] `components/dashboard/HotMoversBanner.tsx` — Banner biến động mạnh nhất (3,606 bytes)
- [x] `components/dashboard/CommoditySpotlight.tsx` — Tiêu điểm nông sản (2,676 bytes)
- [x] `components/dashboard/MarketComparisonChart.tsx` — Biểu đồ so sánh 4 nông sản Recharts (8,694 bytes)
- [x] `components/dashboard/RegionalPriceTable.tsx` — Bảng giá vùng miền (6,585 bytes)
- [x] `components/dashboard/QuickSearchBar.tsx` — Thanh tìm kiếm nhanh (3,974 bytes)
- [x] `components/dashboard/AIInsightCard.tsx` — Thẻ nhận định AI (3,072 bytes)

### 4.3. Trang Chi tiết Nông sản — `app/commodities/[id]/`

- [x] `app/commodities/[id]/page.tsx` — Dynamic route chi tiết từng loại nông sản

### 4.4. Trang Dự báo — `app/forecast/page.tsx`

- [x] `app/forecast/page.tsx` — Trang dự báo giá chính (22,446 bytes)
- [x] Biểu đồ line chart Recharts: actual vs predicted + 95% CI band
- [x] Selector: chọn nông sản, chọn mô hình (LSTM/XGBoost/Prophet/ARIMA)
- [x] Hiển thị metrics: MAE, RMSE, MAPE, R² Score
- [x] Toggle số ngày dự báo (7/14/30)

### 4.5. Trang So sánh Mô hình — `app/compare/page.tsx`

- [x] `app/compare/page.tsx` — So sánh hiệu suất 5 mô hình (12,420 bytes)
- [x] `components/forecast/ModelComparisonChart.tsx` — Bar chart so sánh metrics (6,733 bytes)

### 4.6. Trang Cảnh báo — `app/alerts/page.tsx`

- [x] `app/alerts/page.tsx` — Quản lý alert rules (33,628 bytes)
- [x] Form tạo rule mới (chọn commodity, condition_type, threshold, email)
- [x] Danh sách rules với toggle on/off
- [x] Nút gửi test email
- [x] Lịch sử alert logs

### 4.7. Trang Đăng nhập — `app/login/page.tsx`

- [x] `app/login/page.tsx` — Form login (6,377 bytes)
- [x] Redirect sau đăng nhập
- [x] Lưu token + user info vào localStorage

### 4.8. Trang Admin (Dashboard Quản trị) — `app/dashboard/`

- [x] `app/dashboard/layout.tsx` — Admin layout với sidebar riêng (8,991 bytes)
- [x] `app/dashboard/page.tsx` — Entry redirect (128 bytes)
- [x] `app/dashboard/overview/page.tsx` — Thống kê hệ thống: tổng commodities, prices, forecasts, alerts (12,773 bytes)
- [x] `app/dashboard/data-control/page.tsx` — Quản lý dữ liệu: CRUD giá, Import/Export CSV, nút Scrape/Retrain (20,167 bytes)
- [x] `app/dashboard/ml-models/page.tsx` — Quản lý mô hình: model switcher, trạng thái training (13,308 bytes)
- [x] `app/dashboard/users/page.tsx` — Quản lý user: list, create, phân quyền, khóa tài khoản (12,500 bytes)
- [x] Guard route: redirect nếu chưa login hoặc role không phải admin/analyst
- [x] Lucide Icons (LayoutDashboard, Database, Cpu, Users, LogOut, v.v.)

### 4.9. Frontend Utilities — `src/lib/`

- [x] `lib/api.ts` — Axios client, interceptor, tất cả API functions (25,342 bytes)
- [x] `lib/auth.ts` — `getUser()`, `getToken()`, `logout()` (965 bytes)
- [x] `lib/mockData.ts` — Dữ liệu mẫu fallback (6,647 bytes)
- [x] `types/index.ts` — TypeScript interfaces cho tất cả response types (3,181 bytes)

### 4.10. Admin Page riêng — `app/admin/page.tsx`

- [x] `app/admin/page.tsx` — Admin control panel (60,300 bytes — page tổng hợp)

---

## Module 5: Cảnh báo & Email Notification (Alert System)

### 5.1. Alert Engine — `app/services/alert_service.py`

- [x] Hàm `evaluate_all_alert_rules(db)` — quét tất cả rules đang active
- [x] Logic: `PRICE_ABOVE` — `current_price >= threshold_value`
- [x] Logic: `PRICE_BELOW` — `current_price <= threshold_value`
- [x] Logic: `PCT_INC_7D` — `((today - 7d_ago) / 7d_ago) * 100% >= threshold`
- [x] Logic: `PCT_DEC_7D` — `pct_change <= -abs(threshold)`
- [x] Ghi `AlertLog` với status `SENT` / `FAILED`
- [x] Return count triggered rules

### 5.2. SMTP Email — `app/services/alert_service.py :: send_email_notification()`

- [x] Cấu hình SMTP: `smtp.gmail.com:587` (TLS/STARTTLS)
- [x] Template HTML email chuyên nghiệp (brand color #2D5A27, border-radius, responsive)
- [x] Hàm `send_test_alert()` — gửi email test cho 1 rule cụ thể
- [x] Fallback simulator: nếu chưa set `SMTP_USER`/`SMTP_PASSWORD` thì print log thay vì crash
- [~] Cần cấu hình `SMTP_USER` & `SMTP_PASSWORD` thật trong `.env` để gửi email production

### 5.3. Scheduler tự động

- [x] Đánh giá rules tự động 2 lần/ngày (06:30 và 18:30) qua APScheduler
- [x] Chạy sau scraper (06:00 scrape → 06:30 evaluate) — đảm bảo dữ liệu mới nhất

---

## Module 6: Quản trị Hệ thống (Admin Panel)

### 6.1. Phân quyền RBAC

- [x] 3 roles: `admin` | `analyst` | `user`
- [x] Decorator `require_role(["admin"])` bảo vệ tất cả Admin endpoints
- [x] `require_role(["admin", "analyst"])` cho export CSV, crawler logs
- [x] Frontend guard: redirect nếu role không đủ quyền
- [x] Chặn admin tự khóa tài khoản chính mình

### 6.2. Data Management (Admin)

- [x] CRUD nông sản đầy đủ (Create/Read/Update/Delete) với cascade
- [x] CRUD giá thủ công (thêm mới hoặc upsert nếu trùng date)
- [x] Import CSV (parse `commodity_code`, `record_date`, `price`, validate + error report)
- [x] Export CSV (streaming download)
- [x] Xóa bản ghi giá sai lệch

### 6.3. Task Trigger (Scrape & Retrain)

- [x] Nút **"Cào dữ liệu"** → `POST /api/v1/admin/tasks/scrape` → `BackgroundTasks`
- [x] Nút **"Huấn luyện lại"** → `POST /api/v1/admin/tasks/retrain` → `BackgroundTasks`
- [x] Hỗ trợ retrain 1 commodity cụ thể hoặc toàn bộ
- [x] Background retrain gọi tuần tự: XGBoost/RF → Prophet → ARIMA → LSTM
- [x] Xóa prediction cache sau retrain

### 6.4. User Management (Admin)

- [x] List users
- [x] Create user (admin phân quyền)
- [x] Cập nhật role (`PATCH /users/{id}/role`)
- [x] Khóa/mở tài khoản (`PATCH /users/{id}/toggle-status`)

### 6.5. Model Switcher

- [x] Xem model mặc định hiện tại (`GET /admin/models/active`)
- [x] Chuyển model mặc định (`POST /admin/models/active` — in-memory config)
- [~] Chưa persist model config vào DB (hiện lưu biến global `_ACTIVE_MODEL_CONFIG`)

### 6.6. Crawler Logs

- [x] Endpoint `/admin/logs/crawler` trả về nhật ký cào
- [~] Hiện trả dữ liệu mock hardcoded, chưa ghi log thực vào bảng DB riêng

---

## Module 7: Đóng gói, Testing & Báo cáo

### 7.1. Kiểm thử API (Pytest)

- [x] `tests/conftest.py` — Fixture: TestClient, mock DB session (1,881 bytes)
- [x] `tests/test_health.py` — Test endpoint `/` và `/health` (984 bytes)
- [x] `tests/test_config.py` — Test Settings load đúng (445 bytes)
- [x] `tests/test_auth.py` — Test register, login, rate limit, invalid credentials (4,010 bytes)
- [x] `tests/test_commodities.py` — Test CRUD commodities (1,701 bytes)
- [x] `tests/test_predictions.py` — Test forecast, metrics, retrain endpoints (7,278 bytes)
- [x] `tests/test_admin_phase5.py` — Test admin stats, CRUD prices, CSV import (4,570 bytes)
- [x] `tests/test_security_phase7.py` — Test security headers, XSS, rate limiter (3,945 bytes)
- [x] `tests/test_pipeline.py` — Test ML pipeline data loader, trainer (3,605 bytes)
- [ ] Test coverage report (chưa cấu hình `pytest-cov`)
- [ ] Test frontend (Jest / React Testing Library / Playwright)

### 7.2. Docker & Deployment

- [ ] `backend/Dockerfile` — Python FastAPI container
- [ ] `frontend/Dockerfile` — Next.js production build container
- [ ] `docker-compose.yml` — Orchestrate: backend + frontend + postgres
- [ ] `.dockerignore` cho backend và frontend
- [ ] `nginx.conf` hoặc reverse proxy config (nếu cần)
- [ ] Environment variables documentation cho production
- [ ] Health check trong docker-compose

### 7.3. Tài liệu Dự án

- [x] `README.md` — Giới thiệu dự án (3,930 bytes)
- [x] `docs/REQUIREMENTS_PLAN.md` — Kiến trúc & yêu cầu chi tiết
- [x] `docs/implementation_plan.md` — Kế hoạch triển khai
- [x] `docs/implementation_checklist.md` — Checklist implementation
- [x] `docs/api_reference.md` — Tham chiếu API
- [x] `docs/setup_guide.md` — Hướng dẫn cài đặt
- [x] `docs/security_audit_report.md` — Báo cáo kiểm tra bảo mật
- [x] `docs/security_operations.md` — Vận hành bảo mật
- [x] `docs/phase_1_spec.md` → `phase_7_spec.md` — Spec từng giai đoạn (7 files)
- [x] `docs/PROJECT_TRACKER.md` — File này
- [ ] `docs/API_ENDPOINTS_FULL.md` — Tài liệu API đầy đủ với request/response examples
- [ ] `docs/DEPLOYMENT_GUIDE.md` — Hướng dẫn deploy production

### 7.4. Chuẩn bị Báo cáo & Demo

- [x] `kich_ban_bao_cao.md` — Kịch bản báo cáo hội đồng (3,882 bytes)
- [ ] Slide thuyết trình PowerPoint / Google Slides (15-20 slides)
- [ ] Video demo quay màn hình (5-7 phút)
- [ ] Poster / Infographic tóm tắt kết quả (nếu yêu cầu)
- [ ] Bảng so sánh benchmark 5 mô hình trên 4 nông sản (bảng tổng hợp cho báo cáo)
- [ ] Script demo live (`run_all.bat` đã có, cần kiểm tra lại)

---

## 📦 Tóm tắt File theo Thư mục

### Backend — `backend/` (đếm file code thực tế, không tính `__pycache__`)

```
backend/
├── app/
│   ├── main.py                          ✅ 2,951 bytes
│   ├── core/
│   │   ├── config.py                    ✅ 1,258 bytes
│   │   ├── database.py                  ✅   512 bytes
│   │   ├── deps.py                      ✅ 2,477 bytes
│   │   ├── security.py                  ✅ 4,747 bytes
│   │   ├── auth.py                      ✅ 1,932 bytes
│   │   └── scheduler.py                ✅ 2,186 bytes
│   ├── models/
│   │   └── models.py                    ✅ 5,276 bytes  (6 ORM models)
│   ├── schemas/
│   │   ├── schemas.py                   ✅ 7,100 bytes  (30+ schemas)
│   │   └── user.py                      ✅   565 bytes
│   ├── services/
│   │   ├── forecast_service.py          ✅ 6,343 bytes
│   │   ├── alert_service.py             ✅ 10,844 bytes
│   │   └── commodity_service.py         ✅ 9,324 bytes
│   └── api/v1/
│       ├── api.py                       ✅   763 bytes
│       └── endpoints/
│           ├── auth.py                  ✅  3,782 bytes  (3 endpoints)
│           ├── commodities.py           ✅  3,316 bytes  (8 endpoints)
│           ├── prices.py                ✅    863 bytes  (1 endpoint)
│           ├── forecast.py              ✅  1,278 bytes  (2 endpoints)
│           ├── predictions.py           ✅  5,947 bytes  (3 endpoints)
│           ├── alerts.py                ✅  1,947 bytes  (6 endpoints)
│           └── admin.py                 ✅ 24,170 bytes  (19 endpoints)
├── ml_pipeline/
│   ├── scraper.py                       ✅ 16,456 bytes
│   ├── data_loader.py                   ✅  4,612 bytes
│   ├── feature_engineering.py           ✅  1,192 bytes
│   ├── model_trainer.py                 ✅ 13,174 bytes
│   ├── predictor.py                     ✅ 19,254 bytes
│   ├── baseline_arima.py                ✅  4,608 bytes
│   ├── train_prophet.py                 ✅  5,074 bytes
│   ├── train_ml.py                      ✅  6,796 bytes
│   ├── train_lstm.py                    ✅  6,688 bytes
│   ├── train_all_and_save.py            ✅  4,353 bytes
│   └── saved_models/                    ✅ 4 commodities × 3 models
├── tests/                               ✅ 9 test files
├── requirements.txt                     ✅ 25 dependencies
└── .env.example                         ✅
```

### Frontend — `frontend/src/` (file `.tsx` và `.ts`)

```
frontend/src/
├── app/
│   ├── layout.tsx                       ✅    780 bytes
│   ├── page.tsx                         ✅  5,575 bytes  (Landing)
│   ├── globals.css                      ✅  1,363 bytes  (Theme be sữa)
│   ├── login/page.tsx                   ✅  6,377 bytes
│   ├── forecast/page.tsx                ✅ 22,446 bytes
│   ├── compare/page.tsx                 ✅ 12,420 bytes
│   ├── alerts/page.tsx                  ✅ 33,628 bytes
│   ├── admin/page.tsx                   ✅ 60,300 bytes
│   ├── commodities/[id]/page.tsx        ✅
│   └── dashboard/
│       ├── layout.tsx                   ✅  8,991 bytes  (Admin sidebar layout)
│       ├── page.tsx                     ✅    128 bytes
│       ├── overview/page.tsx            ✅ 12,773 bytes
│       ├── data-control/page.tsx        ✅ 20,167 bytes
│       ├── ml-models/page.tsx           ✅ 13,308 bytes
│       └── users/page.tsx               ✅ 12,500 bytes
├── components/
│   ├── dashboard/
│   │   ├── CommodityCard.tsx            ✅  2,794 bytes
│   │   ├── HotMoversBanner.tsx          ✅  3,606 bytes
│   │   ├── CommoditySpotlight.tsx       ✅  2,676 bytes
│   │   ├── MarketComparisonChart.tsx    ✅  8,694 bytes
│   │   ├── RegionalPriceTable.tsx       ✅  6,585 bytes
│   │   ├── QuickSearchBar.tsx           ✅  3,974 bytes
│   │   └── AIInsightCard.tsx            ✅  3,072 bytes
│   ├── forecast/
│   │   └── ModelComparisonChart.tsx      ✅  6,733 bytes
│   └── layout/
│       ├── Sidebar.tsx                  ✅ 10,544 bytes
│       ├── Header.tsx                   ✅  1,570 bytes
│       └── LayoutWrapper.tsx            ✅  2,107 bytes
├── lib/
│   ├── api.ts                           ✅ 25,342 bytes
│   ├── auth.ts                          ✅    965 bytes
│   └── mockData.ts                      ✅  6,647 bytes
└── types/
    └── index.ts                         ✅  3,181 bytes
```

---

## 🎯 Các Việc cần Ưu tiên Hoàn thành

### 🔴 Ưu tiên Cao (Ảnh hưởng demo & báo cáo)

- [ ] Lưu model **Random Forest** riêng (`rf_model.pkl` + `rf_metrics.json`) cho 4 commodities
- [ ] Lưu model **ARIMA** riêng (`arima_model.pkl` + `arima_metrics.json`) cho 4 commodities
- [ ] Tuning hyperparameter LSTM (Learning rate, hidden_size, num_layers, dropout) — chạy grid search
- [ ] Tạo bảng tổng hợp benchmark 5 models × 4 commodities (20 bộ metrics) cho chương kết quả báo cáo
- [ ] Slide thuyết trình 15-20 trang
- [ ] Video demo 5-7 phút

### 🟡 Ưu tiên Trung bình (Hoàn thiện chất lượng)

- [ ] Persist `_ACTIVE_MODEL_CONFIG` vào bảng DB thay vì biến global
- [ ] Ghi crawler logs thực vào bảng DB riêng (thay vì mock data)
- [ ] Cấu hình `SMTP_USER` / `SMTP_PASSWORD` thật trong `.env` và test gửi email
- [ ] Test coverage report (`pytest --cov=app --cov-report=html`)
- [ ] `docs/API_ENDPOINTS_FULL.md` với request/response examples chi tiết

### 🟢 Ưu tiên Thấp (Nice-to-have)

- [ ] Docker: `Dockerfile` backend + frontend + `docker-compose.yml`
- [ ] Frontend unit tests (Jest / React Testing Library)
- [ ] Feature importance visualization cho Random Forest / XGBoost
- [ ] RSI / Bollinger Bands features bổ sung
- [ ] Poster / Infographic tóm tắt

---

> **📝 Ghi chú:**  
> Tracker này phản ánh trạng thái thực tế của codebase tại thời điểm 10/09/2026.  
> Cập nhật bằng cách sửa checkbox `[ ]` → `[x]` khi hoàn thành từng đầu việc.  
> Đọc kèm: [`REQUIREMENTS_PLAN.md`](file:///d:/DA_TN/docs/REQUIREMENTS_PLAN.md) | [`implementation_plan.md`](file:///d:/DA_TN/docs/implementation_plan.md) | [`kich_ban_bao_cao.md`](file:///d:/DA_TN/kich_ban_bao_cao.md)

---

*AgroForecast Project Tracker — Đồ án Tốt nghiệp 2026*
