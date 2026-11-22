# BÁO CÁO KIỂM THỬ TỰ ĐỘNG TOÀN DIỆN HỆ THỐNG AGROFORECAST (AUTOMATED TEST REPORT)

- **Dự án:** Hệ thống Dự báo Giá Nông sản & Cảnh báo Thị trường (AgroForecast — Danh mục 8 nông sản)
- **Ngày xác minh:** 21/11/2026
- **Công cụ kiểm thử & bảo mật:**
  - **Backend API, Coverage & ML Pipeline:** `pytest 9.1.1`, `pytest-cov 7.1.0` (`coverage 7.17.3`), `FastAPI TestClient`, `SQLAlchemy 2.0`, `PyTorch / XGBoost / Prophet / Statsmodels / Scikit-learn`
  - **Backend SAST Security Scan:** `Bandit` (`bandit -r app -ll` & `bandit -r ml_pipeline -ll` — **0 Medium / 0 High** trên `8.338` LoC)
  - **Real-Browser End-to-End (E2E):** `Playwright 1.65.2` (Headless Chrome) chạy trực tiếp trên Frontend `http://localhost:3000` kết nối Backend `http://127.0.0.1:8000` + PostgreSQL thực tế (8 nông sản, 40 mô hình ML)
  - **Frontend Verification:** `Node.js Test Runner (node:test)`, `TypeScript Compiler (tsc --noEmit)`, `ESLint (next lint)`, `Next.js 14 Production Build (next build)`
- **Tổng số kịch bản kiểm thử tự động:** **128 Test Cases** (**121 Backend Tests** + **3 Frontend Unit Tests** + **4 Playwright Real-Browser E2E Tests**) + **17/17 Static/Dynamic Next.js Routes Compiled**
- **Độ phủ mã nguồn Backend (`pytest-cov` trên toàn bộ gói `app/`):** **97%** (**2.247 / 2.306** câu lệnh thực thi, tăng từ **83%** ban đầu; 13/27 module đạt **100%**)
- **Tỷ lệ thành công:** **100% PASS (128/128 Passed, 0 Failed, 0 Console Errors, 0 Runtime Errors, 0 Syncfusion License Banners, 0 Bandit Medium/High Issues)**

---

## 1. DANH MỤC KỊCH BẢN KIỂM THỬ TRỌNG TÂM (TEST CASE MATRIX)

### 1.1. Phân hệ Xác thực, Quản lý Phiên & Phân quyền RBAC (`backend/tests/test_auth_rbac.py`, `test_auth_and_rbac.py`, `test_auth.py`)

| ID | Mục Tiêu Kiểm Thử | Đầu Vào (Input) | Kết Quả Kỳ Vọng (Expected Output) | Kết Quả Thực Tế (Actual Result) | Trạng Thái |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **TC-AUTH-01** | Đăng ký tài khoản mới, băm mật khẩu Bcrypt và chống rò rỉ `password_hash` | `POST /api/v1/auth/register` với email mới & mật khẩu hợp lệ; gọi lặp lại cùng email | Lần 1 trả `201 Created`, JSON không chứa `password`/`password_hash`; lần 2 trùng email trả `400 Bad Request` | `201 Created` (không lộ hash), lần 2 trả `400 Bad Request` | **PASS** |
| **TC-AUTH-02** | Đăng nhập hợp lệ cấp JWT và từ chối mật khẩu sai / tài khoản không tồn tại | `POST /api/v1/auth/login` với mật khẩu đúng, mật khẩu sai, và email không tồn tại | Đúng trả `200 OK` kèm `access_token` (`bearer`); sai mật khẩu hoặc sai email trả `401 Unauthorized` | `200 OK` (JWT hợp lệ) và `401 Unauthorized` cho cả 2 trường hợp lỗi | **PASS** |
| **TC-AUTH-03** | Khóa tài khoản vô hiệu hóa ngay lập tức phiên JWT hiện tại và chặn đăng nhập lại | Admin gọi `PATCH /api/v1/admin/users/{id}/toggle-status`; Analyst gọi `/auth/me` và `/auth/login` | Tài khoản chuyển sang `is_active=False`; cả request dùng token cũ và request đăng nhập mới đều trả `403 Forbidden` | Cả `/auth/me` và `/auth/login` đều trả `403 Forbidden` | **PASS** |
| **TC-AUTH-04** | Chặn truy cập trái phép khi không đính kèm JWT Access Token | Gọi `GET /auth/me`, `GET /admin/stats`, `GET /admin/users`, `POST /admin/tasks/scrape`, `POST /admin/prices` không có header `Authorization` | Tất cả trả về `401 Unauthorized` | `401 Unauthorized` trên toàn bộ endpoints bảo vệ | **PASS** |
| **TC-AUTH-05** | Kiểm soát phân quyền RBAC: Chặn `Analyst` gọi các API đặc quyền của `Admin` | Tài khoản `role=analyst` gọi `/admin/tasks/scrape`, `/admin/tasks/retrain`, `/admin/users`, `POST/DELETE /admin/prices`, `POST /admin/models/active` | Tất cả bị chặn bởi `require_role(["admin"])` và trả về `403 Forbidden` | `403 Forbidden` trên toàn bộ 7 endpoints quản trị | **PASS** |

### 1.2. Phân hệ Thị trường, So sánh Tăng trưởng Chuẩn hóa & Import/Export CSV (`backend/tests/test_market_compare_csv.py`, `test_market_and_compare_api.py`)

| ID | Mục Tiêu Kiểm Thử | Đầu Vào (Input) | Kết Quả Kỳ Vọng (Expected Output) | Kết Quả Thực Tế (Actual Result) | Trạng Thái |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **TC-MKT-01** | Kiểm tra dữ liệu tổng quan thị trường và tính nhất quán đơn vị của Mía đường | `GET /api/v1/commodities/overview` và `GET /api/v1/commodities/regional-prices` | Trả đủ danh sách mặt hàng kèm `sparkline` 7 phiên; mặt hàng Mía đường (`SUGAR`) hiển thị đúng đơn vị `VNĐ/tấn` | `200 OK`, Mía đường hiển thị chính xác `VNĐ/tấn` trên cả hai API | **PASS** |
| **TC-MKT-02** | Kiểm tra công thức tính đường cong tăng trưởng chuẩn hóa (%) trên `/compare` | `GET /api/v1/commodities/comparison` với chuỗi giá tăng đều 1%/ngày trong 15 ngày | Không có giá trị `NaN`/`Infinity`; điểm đầu kỳ bằng `0.0%`, điểm cuối kỳ bằng `+14.0%` đúng công thức $\frac{P_t - P_0}{P_0} \times 100$ | `200 OK`, đầu kỳ `0.0%`, cuối kỳ `+14.0%`, 100% giá trị hữu hạn | **PASS** |
| **TC-MKT-03** | Kiểm tra truy vấn lịch sử giá theo bộ lọc mặt hàng và khoảng thời gian | `GET /api/v1/history?commodity_id=2&start_date=...&end_date=...` | Chỉ trả về các bản ghi nằm trong khoảng ngày đã chọn kèm thông tin nguồn (`provenance=reviewed`) và `readiness` | `200 OK`, trả đúng 5 bản ghi trong phạm vi lọc | **PASS** |
| **TC-MKT-04** | Kiểm tra Import CSV (file hợp lệ, sai định dạng, quá 5MB, giá âm) & Export CSV chống Formula Injection + Audit Log | Upload `.exe`, file > 5MB, file CSV chứa dòng hợp lệ + dòng giá âm + dòng thiếu giá + công thức `=cmd...`; xóa điểm giá và gọi `/admin/prices/revisions` | File `.exe` và file > 5MB trả `400 Bad Request`; CSV hỗn hợp thêm 1 bản ghi và trả 3 lỗi chi tiết từng dòng; Export CSV tiền tố `'=cmd`; Audit Log ghi nhận bản ghi `DELETED` | `400` cho file lỗi/quá tải; `200 OK` kèm báo cáo 3 dòng lỗi; Export CSV đã escape `'=cmd`; Audit Log ghi nhận `DELETED` | **PASS** |

### 1.3. Phân hệ Dự báo 5 Mô hình ML & Pipeline Tiền xử lý Không Rò rỉ (`backend/tests/test_ml_forecast.py`, `test_forecast_and_ml_pipeline.py`, `test_history_workflow.py`)

| ID | Mục Tiêu Kiểm Thử | Đầu Vào (Input) | Kết Quả Kỳ Vọng (Expected Output) | Kết Quả Thực Tế (Actual Result) | Trạng Thái |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **TC-ML-01** | Kiểm tra tiền xử lý dữ liệu không còn `NaN` và chia tập Train/Test tuần tự thời gian (**No Data Leakage**) | Chuỗi 75 ngày giá lịch sử đã xác minh; chạy `load_clean_data()` và `training_service.retrain()` | Chuỗi sau tiền xử lý 0 giá trị `NaN`; ngày cuối tập Train nhỏ hơn tuyệt đối ngày đầu tập Test (`max(train_date) < min(test_date)`) | `0 NaN`, `train_end < test_start` cách nhau đúng 1 ngày, không rò rỉ dữ liệu tương lai | **PASS** |
| **TC-ML-02** | Kiểm tra API `/forecast` và `/forecast/compare/{id}` trả đủ 5 mô hình, 4 chỉ số và dải tin cậy 95% hợp lệ | `GET /api/v1/forecast/compare/{id}` và `GET /api/v1/forecast?model_name=...&days=14` cho cả 5 mô hình | Trả đủ 5 mô hình (`ARIMA`, `Prophet`, `Random Forest`, `XGBoost`, `LSTM`) với đủ `MAE`, `RMSE`, `MAPE`, `R²` hữu hạn; mọi điểm dự báo thỏa mãn `lowerCI <= predictedPrice <= upperCI` | Đủ 5 mô hình, 4 chỉ số hợp lệ, 100% điểm dự báo thỏa mãn `lowerCI <= predictedPrice <= upperCI` | **PASS** |
| **TC-ML-03** | Kiểm tra dự báo theo địa phương (Basis Spread) và kiểm tra chữ ký dữ liệu SHA-256 | `GET /api/v1/forecast?region=...`; chỉnh sửa giá lịch sử sau khi huấn luyện | Chênh lệch giá dự báo giữa các huyện khớp chính xác với `basisSpread`; khi dữ liệu gốc bị sửa chưa retrain, API trả `409 Conflict` để bảo vệ tính toàn vẹn | Khớp 100% `basisSpread` và phát hiện thay đổi dữ liệu qua SHA-256 hash | **PASS** |
| **TC-ML-04** | Kiểm định Walk-Forward 7 ngày không rò rỉ dữ liệu, `PICP 95% CI` mở rộng theo $\sqrt{h}$ & cấm sinh giá giả | Chạy `walk_forward_evaluate` 5 mô hình trên chuỗi 220 ngày; giả lập lỗi mạng trên `specialized_scrapers.py` | `accuracy = 100 - mape`, `0 <= picp_95 <= 100`, `width(D+30) > width(D+1)`; khi nguồn lỗi scraper trả `FAILED` và `count=0` | Đạt 100% trên cả 5 mô hình và 0 bản ghi giả khi lỗi mạng | **PASS** |

### 1.4. Phân hệ Cảnh báo Giá, Chống IDOR & Bộ Đánh giá Ngưỡng (`backend/tests/test_alerts.py`, `test_alerts_api.py`)

| ID | Mục Tiêu Kiểm Thử | Đầu Vào (Input) | Kết Quả Kỳ Vọng (Expected Output) | Kết Quả Thực Tế (Actual Result) | Trạng Thái |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **TC-ALT-01** | Kiểm tra CRUD đầy đủ cho quy tắc cảnh báo & kích hoạt gửi email thử nghiệm | `POST /alerts`, `PUT /alerts/{id}`, `PATCH /alerts/{id}/toggle`, `POST /alerts/{id}/test`, `GET /alerts/logs`, `DELETE /alerts/{id}` | Tạo, cập nhật ngưỡng/email, bật/tắt trạng thái, gửi test email tạo bản ghi trong `alert_logs` và xóa quy tắc thành công (`200 OK`) | Toàn bộ 6 thao tác CRUD & Test Email hoạt động chính xác (`200 OK`) | **PASS** |
| **TC-ALT-02** | Kiểm tra chống IDOR giữa các tài khoản người dùng trên `/alerts` | Analyst A tạo quy tắc; User B gọi `PUT`, `PATCH`, `DELETE` trên quy tắc của Analyst A; Admin gọi `DELETE` | User B bị chặn với mã `403 Forbidden`; Admin xóa thành công với mã `200 OK` | User B nhận `403 Forbidden` trên cả 3 thao tác; Admin nhận `200 OK` | **PASS** |
| **TC-ALT-03** | Kiểm tra bộ đánh giá điều kiện vượt trần (`PRICE_ABOVE`) và chạm sàn (`PRICE_BELOW`) | Giá mới nhất `105.000`; Rule 1 (`> 100.000`), Rule 2 (`< 110.000`), Rule 3 (`> 130.000`); chạy `evaluate_all_alert_rules()` | Kích hoạt đúng 2 quy tắc (Rule 1 và Rule 2), không kích hoạt Rule 3; ghi 2 bản ghi vào `alert_logs` | `triggered_count == 2`, ghi đúng 2 nhật ký vượt ngưỡng và chạm sàn | **PASS** |

### 1.5. Kiểm thử Đơn vị & Định dạng Giao diện Frontend (`frontend/src/lib/__tests__/formatters.test.mjs`)

| ID | Mục Tiêu Kiểm Thử | Đầu Vào (Input) | Kết Quả Kỳ Vọng (Expected Output) | Kết Quả Thực Tế (Actual Result) | Trạng Thái |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **TC-FE-01** | Định dạng số tiền Việt Nam và chuẩn hóa đơn vị Mía đường (`VNĐ/tấn`) | `formatVnd(93800, null, 'Cà phê Robusta')`, `formatVnd(1279515, null, 'Mía đường')` | `93.800 VNĐ/kg` và `1.279.515 VNĐ/tấn` | Khớp tuyệt đối `93.800 VNĐ/kg` và `1.279.515 VNĐ/tấn` | **PASS** |
| **TC-FE-02** | Chuẩn hóa ngày giờ Việt Nam `DD/MM/YYYY` và `DD/MM/YYYY HH:mm` | `formatDateVN('2026-08-28')`, `formatDateTimeVN('2026-08-28T16:08:19')` | `28/08/2026` và `28/08/2026 16:08` | Khớp tuyệt đối, loại bỏ chuỗi ISO thô | **PASS** |
| **TC-FE-03** | Tính toán tăng trưởng chuẩn hóa (%) và hệ số tương quan Pearson ($r$) | `calculateGrowthPct(114000, 100000)`, `calculatePearsonCorrelation([1,2,3,4], [2,4,6,8])` | `+14%` và `r = 1.0` (không phát sinh `NaN`/`Infinity` khi chia cho 0) | Khớp tuyệt đối (`14`, `1`, `-1`, `0` khi mẫu bằng 0) | **PASS** |

### 1.6. Phân hệ Thu thập & Phân tích giá theo Tỉnh/Vùng Địa lý (`backend/tests/test_regional_pricing.py`)

| ID | Mục Tiêu Kiểm Thử | Đầu Vào (Input) | Kết Quả Kỳ Vọng (Expected Output) | Kết Quả Thực Tế (Actual Result) | Trạng Thái |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **TC-REG-01** | Danh mục tỉnh hỗ trợ & Định vị GPS tự động (Haversine) | `GET /api/v1/regions`, `GET /api/v1/regions/locate?lat=12.2388&lng=109.1967` (Nha Trang), tọa độ lỗi `lat=999` | Trả đủ 33 tỉnh/thành; tọa độ Nha Trang trả đúng `khanh-hoa` (`Khánh Hòa`, `distance_km < 1.0`); tọa độ ngoài miền trả `422` (không bao giờ 500) | Trả 33 tỉnh; Nha Trang khớp `khanh-hoa` (`0.0 km`); tọa độ sai trả `422` | **PASS** |
| **TC-REG-02** | Phân biệt minh bạch `direct` và `regional_benchmark` tại Khánh Hòa | `GET /api/v1/market/overview?province=khanh-hoa` & `/api/v1/commodities/overview?province=khanh-hoa` | Mía đường trả `pricing_mode=direct` (`distance_km=0`); các nông sản khác trả `pricing_mode=regional_benchmark` kèm khoảng cách Haversine & cước vận chuyển | Phân biệt chính xác 100%, không `NaN`/`null` | **PASS** |
| **TC-REG-03** | Nhất quán `?province=khanh-hoa` trên `/history`, `/forecast`, `/market/compare` và bảng chênh lệch theo tỉnh | Gọi đồng bộ `/history`, `/forecast?days=14`, `/market/compare`, `/market/regional-prices/{code}` với `province=khanh-hoa` | Điểm chuyển tiếp lịch sử–dự báo dịch chuyển đồng nhất đúng `basis_offset`; toàn bộ 14 điểm dự báo thỏa `lowerCI <= predictedPrice <= upperCI`; bảng so sánh tỉnh phân loại đúng `direct` vs `regional_benchmark` | 100% điểm khớp liền mạch và thỏa mãn bất đẳng thức 95% CI | **PASS** |

### 1.7. Kiểm thử Mở rộng Phủ nhánh Nghiệp vụ, Auto Catch-up & Bảo mật (`backend/tests/test_coverage_gaps.py`, `test_security_hardening.py`)

| ID | Phân hệ / Mục Tiêu Kiểm Thử | Nhánh Nghiệp Vụ & Biên Lỗi Được Phủ | Kết Quả |
| :--- | :--- | :--- | :---: |
| **TC-COV-01..03** | Bảo mật Auth, JWT & Rate Limiting (`auth.py`, `deps.py`, `security.py`) | Giới hạn tần suất `429 Too Many Requests` trên `/login` & `/register`; JWT thiếu `sub` (`401`), user đã xóa (`404`); `get_optional_current_user` hạ cấp an toàn; `verify_password` hash hỏng & `sanitize_csv_cell` | **PASS** |
| **TC-COV-04..06** | Quản trị Nông sản, Giá thủ công, Audit & CSV (`admin.py`, `commodities.py`, `schemas.py`) | CRUD đầy đủ + chặn trùng mã `400`/`404`; xác minh giá ghi `PriceRevision` (`UPDATED`/`DELETED`); đủ 6 luật validate `PriceCreateManual`; `429` Scrape/Retrain; chuẩn hóa vai trò `_disabled`; Import CSV `latin-1` | **PASS** |
| **TC-COV-07..08** | Đánh giá Cảnh báo 7 ngày & SMTP (`alert_service.py`, `alerts.py`) | Kích hoạt `PCT_INC_7D` (+20%) và `PCT_DEC_7D` (-20%), bỏ qua mặt hàng chưa có giá; phân quyền xem quy tắc theo user vs admin; nhánh SMTP thực tế thành công & bắt lỗi ngoại lệ mạng an toàn | **PASS** |
| **TC-COV-09..10** | Định giá Vùng `VNĐ/tấn`, Chuỗi Trực tiếp & Lịch sử (`regional_pricing_service.py`, `commodity_service.py`, `history.py`, `prices.py`, `regions.py`) | Công thức cước `VNĐ/tấn` và $\le 5$ km; mã tỉnh không tồn tại hồi quy `national_benchmark`; chuỗi trực tiếp $\ge 5$ phiên trên `/overview` & `/history`; `/history/readiness`, `/training-runs/{id}`, `/sources`, `/prices/history`, `/spotlight` | **PASS** |
| **TC-COV-11..16** | Pipeline ML, Startup Auto Catch-up, APScheduler & Bảo mật SSRF/TLS (`training_service.py`, `job_service.py`, `scheduler.py`, `schema_upgrade.py`, `vietnam_real_scrapers.py`) | Cô lập lỗi theo mô hình (`PARTIAL`/`FAILED`, chặn tràn số $\ge 10^{12}$); `scheduled_scraper_task()` cào đủ 8 mặt hàng; `run_startup_catchup_if_stale()` (bỏ qua khi đang có job `RUNNING`, kích hoạt khi dữ liệu cũ, bỏ qua khi đã cào trong 2h hoặc đã có dữ liệu hôm nay, bắt lỗi an toàn); chống SSRF `ALLOWED_SCRAPER_DOMAINS`, chặn `javascript:`/`file://` trong `source_url`, `verify=True` 100% | **PASS** |

---

## 2. KẾT QUẢ THỰC THI TERMINAL THỰC TẾ (21/11/2026)

### 2.1. Kết quả `pytest --cov=app --cov-report=term-missing -v` & `bandit -ll` (Backend — 121/121 PASSED, 97% Coverage, 0 Bandit Issues)
```text
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.1.1, pluggy-1.6.0 -- D:\DA_TN\backend\venv\Scripts\python.exe
rootdir: D:\DA_TN\backend
configfile: pytest.ini
testpaths: tests
plugins: anyio-4.14.2, cov-7.1.0
collecting ... collected 121 items
...
TOTAL                                       2306     59    97%
================ 121 passed, 18 warnings in 124.90s (0:02:04) =================

bandit -r app -ll         -> 4,041 LoC scanned | Medium: 0 | High: 0 (No issues identified)
bandit -r ml_pipeline -ll -> 4,297 LoC scanned | Medium: 0 | High: 0 (No issues identified)
```

### 2.2. Kết quả Kiểm thử E2E trên Trình duyệt thật (`pytest e2e/test_agroforecast_e2e.py -v` — 4/4 PASSED)
```text
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.1.1, pluggy-1.6.0 -- D:\DA_TN\backend\venv\Scripts\python.exe
rootdir: D:\DA_TN
plugins: anyio-4.14.2, cov-7.1.0
collecting ... collected 4 items

e2e/test_agroforecast_e2e.py::test_e2e_01_overview_and_khanh_hoa_location_pricing PASSED [ 25%]
e2e/test_agroforecast_e2e.py::test_e2e_02_forecast_best_model_horizon_and_tabs PASSED [ 50%]
e2e/test_agroforecast_e2e.py::test_e2e_03_history_compare_alerts_clean_syncfusion PASSED [ 75%]
e2e/test_agroforecast_e2e.py::test_e2e_04_rbac_analyst_blocked_and_admin_full_access PASSED [100%]

============================= 4 passed in 29.03s ==============================
```

### 2.3. Kết quả Kiểm thử Frontend (`tsc --noEmit`, `next lint`, `node --test`, `next build`)
```text
> frontend@0.1.0 lint
> next lint
✔ No ESLint warnings or errors

TAP version 13
ok 1 - TC-FE-01: Format tiền tệ chuẩn Việt Nam và đơn vị nhất quán (Mía đường là VNĐ/tấn)
ok 2 - TC-FE-02: Format ngày giờ chuẩn Việt Nam DD/MM/YYYY và DD/MM/YYYY HH:mm (loại bỏ ISO thô)
ok 3 - TC-FE-03: Tính toán phần trăm tăng trưởng chuẩn hóa và tương quan Pearson (không NaN/Infinity)
1..3
# tests 3 | pass 3 | fail 0

> frontend@0.1.0 build
> next build
  ▲ Next.js 14.2.35
 ✓ Compiled successfully
 ✓ Generating static pages (17/17)
```

---

## 3. BÁO CÁO ĐO ĐỘ PHỦ MÃ NGUỒN BACKEND (`pytest-cov` — 21/11/2026)

| Module (`backend/app/...`) | Số lệnh (Stmts) | Chưa phủ (Miss) | Độ phủ (Cover) | Ghi chú |
| :--- | :---: | :---: | :---: | :--- |
| `api/v1/api.py` | 13 | 0 | **100%** | Định tuyến API v1 |
| `api/v1/endpoints/admin.py` | 316 | 14 | **96%** | CRUD nông sản/giá/người dùng, Audit Log, Rate Limit 429, Import/Export CSV |
| `api/v1/endpoints/alerts.py` | 33 | 1 | **97%** | Lọc cảnh báo theo phiên người dùng & chống IDOR |
| `api/v1/endpoints/auth.py` | 41 | 0 | **100%** | Chống brute-force `429` trên `/login` & `/register` |
| `api/v1/endpoints/commodities.py` | 50 | 0 | **100%** | CRUD nông sản + kiểm tra `404` |
| `api/v1/endpoints/forecast.py` | 14 | 0 | **100%** | API dự báo & so sánh 5 mô hình |
| `api/v1/endpoints/history.py` | 63 | 1 | **98%** | `/readiness`, `/training-runs/{id}`, `/sources`, chuỗi theo tỉnh |
| `api/v1/endpoints/market.py` | 25 | 0 | **100%** | `/market/overview` & `/market/regional-prices/{code}` |
| `api/v1/endpoints/predictions.py` | 58 | 0 | **100%** | `/predictions/forecast`, `/metrics`, xử lý lỗi `500` |
| `api/v1/endpoints/prices.py` | 12 | 0 | **100%** | `GET /api/v1/prices/history` |
| `api/v1/endpoints/regions.py` | 14 | 0 | **100%** | Danh mục 33 tỉnh & định vị GPS Haversine |
| `core/config.py` | 35 | 0 | **100%** | Kiểm tra cấu hình an toàn (JWT secret guard, CORS) |
| `core/database.py` | 11 | 4 | **64%** | `get_db()` được override bởi SQLite in-memory trong test |
| `core/deps.py` | 42 | 0 | **100%** | Xác thực JWT & phân quyền RBAC |
| `core/scheduler.py` | 78 | 3 | **96%** | APScheduler GMT+7 & toàn bộ nhánh Startup Auto Catch-up |
| `core/schema_upgrade.py` | 23 | 6 | **74%** | Nâng cấp lược đồ idempotent (6 dòng đặc thù riêng PG) |
| `core/security.py` | 79 | 0 | **100%** | Bcrypt, JWT, chống CSV Formula Injection, RateLimiter |
| `main.py` | 56 | 5 | **91%** | `/`, `/health` (`degraded`), `global_exception_handler` `500` |
| `models/models.py` | 153 | 0 | **100%** | Toàn bộ thực thể ORM SQLAlchemy |
| `schemas/schemas.py` | 318 | 0 | **100%** | Toàn bộ schema Pydantic & validation |
| `services/alert_service.py` | 168 | 2 | **99%** | Đánh giá ngưỡng & gửi email SMTP |
| `services/commodity_service.py` | 135 | 6 | **96%** | Tổng quan 8 mặt hàng, Sparkline trực tiếp, Spotlight |
| `services/forecast_service.py` | 121 | 4 | **97%** | Dự báo & tương thích bản ghi |
| `services/history_service.py` | 106 | 0 | **100%** | Kiểm tra chất lượng chuỗi & cadence |
| `services/job_service.py` | 70 | 5 | **93%** | Thực thi tác vụ nền scrape/retrain & đồng bộ 8 mặt hàng |
| `services/regional_pricing_service.py` | 166 | 7 | **96%** | Thuật toán Haversine 2 tầng & cước vận chuyển |
| `services/training_service.py` | 106 | 1 | **99%** | Walk-Forward 7N, Conformal 95% CI, tự chọn `active_model` |
| **TỔNG CỘNG (`app/`)** | **2.306** | **59** | **97%** | **13/27 module đạt 100%** |

---

## 4. KẾT QUẢ KIỂM THỬ END-TO-END TRÊN TRÌNH DUYỆT THẬT (PLAYWRIGHT — 8 NÔNG SẢN)

Bộ kiểm thử [e2e/test_agroforecast_e2e.py](file:///d:/DA_TN/e2e/test_agroforecast_e2e.py) điều khiển Chrome thật (`1440×900`) thao tác trực tiếp trên Next.js + Syncfusion EJ2 (`http://localhost:3000`) kết nối FastAPI + PostgreSQL (`http://127.0.0.1:8000`):

| Mã E2E | Kịch Bản Người Dùng Thực Tế | Xác Minh Giao Diện & Dữ Liệu | Console / Runtime Errors | Banner Syncfusion | Kết Quả |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **E2E-01** | **Trang Tổng quan (`/`) 8 nông sản & Định giá vị trí Khánh Hòa** | Xác nhận đủ **8 thẻ nông sản** (bao gồm `Dâu tây Đà Lạt`, `Khoai tây Đà Lạt`, `Khoai lang tím Vĩnh Long`, `Hạt điều`) hiển thị lưới 4×2 gọn gàng; chọn **Khánh Hòa** hiển thị huy hiệu xanh **`Khảo sát tại Khánh Hòa`** cho Mía đường và **`Tham chiếu Lâm Đồng`** (~87 km) cho nông sản Đà Lạt; bảng **`Chênh lệch giá theo tỉnh hôm nay`** hiển thị nhãn **`Đang chọn`** | **0** | **0** | **PASS** |
| **E2E-02** | **Trang Dự báo (`/forecast`) — Mô hình tốt nhất ($\star$), Dâu tây Đà Lạt & Tab** | Xác nhận tự động chọn mô hình tốt nhất (`★`) cho Lúa gạo, chuyển sang **`Dâu tây Đà Lạt`** (`Prophet ★`), đổi kỳ hạn **`7N` $\leftrightarrow$ `30N`**, chuyển tab **`Bảng chi tiết dự báo` $\leftrightarrow$ `So sánh 5 mô hình`** kèm di chuột trên biểu đồ Syncfusion (0 crash `BaseTooltip.appendChild`) | **0** | **0** | **PASS** |
| **E2E-03** | **Lịch sử (`/history`), So sánh 8 nông sản (`/compare`) & Cảnh báo (`/alerts`)** | Xác nhận Syncfusion `GridComponent` (`.e-grid`) và `ChartComponent` (`.e-chart svg`) render hoàn chỉnh đủ 8 đường tăng trưởng chuẩn hóa và bảng tương quan Pearson | **0** | **0** | **PASS** |
| **E2E-04** | **Kiểm soát Truy cập RBAC (Guest / Analyst / Admin)** | Khách chưa đăng nhập bị đẩy về `/login`; `Analyst` (`anhnguyen@agroforecast.vn`) bị ẩn menu Quản trị **và** bị chặn chuyển hướng khỏi toàn bộ 4 URL `/dashboard/*`; `Admin` (`admin@agroforecast.vn`) truy cập trọn vẹn 4 trang quản trị | **0** | **0** | **PASS** |
