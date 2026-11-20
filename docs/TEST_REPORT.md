# BÁO CÁO KIỂM THỬ TỰ ĐỘNG TOÀN DIỆN HỆ THỐNG AGROFORECAST (AUTOMATED TEST REPORT)

- **Dự án:** Hệ thống Dự báo Giá Nông sản & Cảnh báo Thị trường (AgroForecast)
- **Ngày xác minh:** 20/11/2026
- **Công cụ kiểm thử:**
  - **Backend API, Coverage & ML Pipeline:** `pytest 9.1.1`, `pytest-cov 7.1.0` (`coverage 7.17.3`), `FastAPI TestClient`, `SQLAlchemy 2.0`, `PyTorch / XGBoost / Prophet / Statsmodels / Scikit-learn`
  - **Real-Browser End-to-End (E2E):** `Playwright 1.65.2` (Headless Chrome) chạy trực tiếp trên Frontend `http://localhost:3000` kết nối Backend `http://127.0.0.1:8000` + PostgreSQL thực tế
  - **Frontend Verification:** `Node.js Test Runner (node:test)`, `TypeScript Compiler (tsc --noEmit)`, `ESLint (next lint)`, `Next.js 14 Production Build (next build)`
- **Tổng số kịch bản kiểm thử tự động:** **127 Test Cases** (**120 Backend Tests** + **3 Frontend Unit Tests** + **4 Playwright Real-Browser E2E Tests**) + **17/17 Static/Dynamic Next.js Routes Compiled**
- **Độ phủ mã nguồn Backend (`pytest-cov` trên toàn bộ gói `app/`):** **98%** (**2.194 / 2.247** câu lệnh thực thi, tăng từ **83%** ban đầu)
- **Tỷ lệ thành công:** **100% PASS (127/127 Passed, 0 Failed, 0 Console Errors, 0 Runtime Errors, 0 Syncfusion License Banners)**

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
| **TC-REG-02** | Phân biệt minh bạch `direct` và `regional_benchmark` tại Khánh Hòa | `GET /api/v1/market/overview?province=khanh-hoa` & `/api/v1/commodities/overview?province=khanh-hoa` | Mía đường trả `pricing_mode=direct` (`1.070.000`, `distance_km=0`); Cà phê trả `pricing_mode=regional_benchmark` tham chiếu Đắk Lắk kèm `distance_km > 100` & `logistics_spread > 0` | Phân biệt chính xác 100%, không `NaN`/`null` | **PASS** |
| **TC-REG-03** | Nhất quán `?province=khanh-hoa` trên `/history`, `/forecast`, `/market/compare` và bảng chênh lệch theo tỉnh | Gọi đồng bộ `/history`, `/forecast?days=14`, `/market/compare`, `/market/regional-prices/{code}` với `province=khanh-hoa` | Điểm chuyển tiếp lịch sử–dự báo dịch chuyển đồng nhất đúng `basis_offset`; toàn bộ 14 điểm dự báo thỏa `lowerCI <= predictedPrice <= upperCI`; bảng so sánh tỉnh phân loại đúng `direct` vs `regional_benchmark` | 100% điểm khớp liền mạch và thỏa mãn bất đẳng thức 95% CI | **PASS** |

### 1.7. Kiểm thử Mở rộng Phủ nhánh Nghiệp vụ & Xử lý Lỗi (TDD + Coverage Analysis — `backend/tests/test_coverage_gaps.py`)

| ID | Phân hệ / Mục Tiêu Kiểm Thử | Nhánh Nghiệp Vụ & Biên Lỗi Được Phủ | Kết Quả |
| :--- | :--- | :--- | :---: |
| **TC-COV-01..03** | Bảo mật Auth, JWT & Rate Limiting (`auth.py`, `deps.py`, `security.py`) | Giới hạn tần suất `429 Too Many Requests` trên `/login` & `/register`; JWT thiếu `sub` (`401`), user đã xóa (`404`); `get_optional_current_user` hạ cấp an toàn với token lỗi; `verify_password` hash hỏng & `sanitize_csv_cell` | **PASS** |
| **TC-COV-04..06** | Quản trị Nông sản, Giá thủ công, Audit & CSV (`admin.py`, `commodities.py`, `schemas.py`) | CRUD đầy đủ + chặn trùng mã `400`/`404`; xác minh giá ghi `PriceRevision` (`UPDATED`/`DELETED`); toàn bộ 6 luật validate của `PriceCreateManual` (nguồn xác minh, giá âm, ngày tương lai, min/max, độ dài nguồn); `429` cho Scrape/Retrain; chuẩn hóa vai trò `_disabled`; Import CSV mã hóa `latin-1` & lỗi từng dòng | **PASS** |
| **TC-COV-07..08** | Đánh giá Cảnh báo 7 ngày & SMTP (`alert_service.py`, `alerts.py`) | Kích hoạt `PCT_INC_7D` (+20%) và `PCT_DEC_7D` (-20%), bỏ qua mặt hàng chưa có giá; phân quyền xem quy tắc theo user vs admin; toàn bộ nhánh `404`; nhánh SMTP thực tế thành công & bắt lỗi ngoại lệ mạng an toàn | **PASS** |
| **TC-COV-09..10** | Định giá Vùng `VNĐ/tấn`, Chuỗi Trực tiếp & Lịch sử (`regional_pricing_service.py`, `commodity_service.py`, `history.py`, `prices.py`, `regions.py`) | Công thức cước vận chuyển cho đơn vị `VNĐ/tấn` (Mía đường) và khoảng cách $\le 5$ km; mã tỉnh không tồn tại hồi quy an toàn về `national_benchmark`; chuỗi khảo sát trực tiếp $\ge 5$ phiên trên `/overview` & `/history`; `/history/readiness`, `/training-runs/{id}`, `/sources`, `/prices/history`, `/spotlight` | **PASS** |
| **TC-COV-11..15** | Pipeline ML, Phục hồi Tác vụ, APScheduler & Schema Upgrade (`training_service.py`, `job_service.py`, `forecast_service.py`, `history_service.py`, `predictions.py`, `scheduler.py`, `schema_upgrade.py`, `main.py`) | Cô lập lỗi theo từng mô hình (`PARTIAL`/`FAILED`, chặn dự báo `>= 1e12`); tự động cập nhật `active_model` tốt nhất sau Walk-Forward; `sync_forecast_after_scrape` nhận diện snapshot đồng bộ; `run_job("retrain")` thành công & lỗi; lỗi `/forecast` (`404`/`400`/`409`) và chuỗi `periodic`/`irregular`; vòng đời `APScheduler`; `upgrade_existing_schema()` thêm cột an toàn; `/health` trạng thái `degraded` và `global_exception_handler` `500` | **PASS** |

---

## 2. KẾT QUẢ THỰC THI TERMINAL THỰC TẾ

### 2.1. Kết quả `pytest --cov=app --cov-report=term-missing -v` (Backend Suite — 120/120 PASSED, 98% Coverage)
```text
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.1.1, pluggy-1.6.0 -- D:\DA_TN\backend\venv\Scripts\python.exe
rootdir: D:\DA_TN\backend
configfile: pytest.ini
testpaths: tests
plugins: anyio-4.14.2, cov-7.1.0
collecting ... collected 120 items
...
tests/test_coverage_gaps.py::test_auth_rate_limiting_login_and_register PASSED
tests/test_coverage_gaps.py::test_jwt_missing_sub_and_deleted_user PASSED
tests/test_coverage_gaps.py::test_optional_current_user_edge_tokens_and_security_helpers PASSED
tests/test_coverage_gaps.py::test_admin_and_public_commodities_crud_lifecycle PASSED
tests/test_coverage_gaps.py::test_admin_manual_price_audit_and_schema_validation PASSED
tests/test_coverage_gaps.py::test_admin_user_model_task_and_csv_branches PASSED
tests/test_coverage_gaps.py::test_alert_evaluation_pct_triggers_ownership_and_404s PASSED
tests/test_coverage_gaps.py::test_alert_email_smtp_success_and_error PASSED
tests/test_coverage_gaps.py::test_regional_pricing_tonnes_unknown_province_and_direct_series PASSED
tests/test_coverage_gaps.py::test_history_readiness_sources_prices_comparison_and_spotlight PASSED
tests/test_coverage_gaps.py::test_history_service_cadence_and_readiness_branches PASSED
tests/test_coverage_gaps.py::test_forecast_service_errors_and_legacy_fallback PASSED
tests/test_coverage_gaps.py::test_training_service_and_job_service_recovery PASSED
tests/test_coverage_gaps.py::test_predictions_endpoints_and_async_retrain PASSED
tests/test_coverage_gaps.py::test_scheduler_schema_upgrade_and_main_health PASSED
...
TOTAL                                       2247     53    98%
================ 120 passed, 18 warnings in 100.33s (0:01:40) =================
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

============================= 4 passed in 28.53s ==============================
```

### 2.3. Kết quả Kiểm thử Frontend (`node --test`, `npx tsc --noEmit`, `npm run lint`, `npm run build`)
```text
TAP version 13
ok 1 - TC-FE-01: Format tiền tệ chuẩn Việt Nam và đơn vị nhất quán (Mía đường là VNĐ/tấn)
ok 2 - TC-FE-02: Format ngày giờ chuẩn Việt Nam DD/MM/YYYY và DD/MM/YYYY HH:mm (loại bỏ ISO thô)
ok 3 - TC-FE-03: Tính toán phần trăm tăng trưởng chuẩn hóa và tương quan Pearson (không NaN/Infinity)
1..3
# tests 3 | pass 3 | fail 0

> frontend@0.1.0 lint
> next lint
✔ No ESLint warnings or errors

> frontend@0.1.0 build
> next build
  ▲ Next.js 14.2.35
  - Environments: .env.local
   Creating an optimized production build ...
 ✓ Compiled successfully
   Linting and checking validity of types ...
   Collecting page data ...
 ✓ Generating static pages (17/17)
```

---

## 3. BÁO CÁO ĐO & TỐI ƯU ĐỘ PHỦ MÃ NGUỒN BACKEND (`pytest-cov`)

Sau khi đo mức nền ban đầu (**83%** trên 2.247 dòng lệnh thực thi của gói `app/`), nhóm áp dụng kỹ thuật phân tích độ phủ (**Coverage Analysis**) kết hợp **TDD** để nhận diện và bổ sung 15 kịch bản kiểm thử chuyên sâu cho các nhánh nghiệp vụ, kiểm soát truy cập và xử lý lỗi quan trọng, nâng tổng độ phủ lên **98%** (giảm số dòng chưa phủ từ **377** xuống chỉ còn **53** dòng).

| Module (`backend/app/...`) | Số lệnh (Stmts) | Trước tối ưu (Baseline) | Sau tối ưu (Final) | Mức tăng | Ghi chú các nhánh quan trọng đã đóng |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `api/v1/api.py` | 13 | 100% | **100%** | — | Định tuyến API v1 |
| `api/v1/endpoints/admin.py` | 316 | 72% | **96%** | **+24%** | CRUD nông sản/giá/người dùng, Audit Log, Rate Limit 429, Import/Export CSV |
| `api/v1/endpoints/alerts.py` | 30 | 97% | **100%** | **+3%** | Lọc cảnh báo theo phiên người dùng & khách |
| `api/v1/endpoints/auth.py` | 41 | 95% | **100%** | **+5%** | Chống brute-force `429 Too Many Requests` trên `/login` & `/register` |
| `api/v1/endpoints/commodities.py` | 50 | 72% | **100%** | **+28%** | `PUT`/`DELETE` nông sản + kiểm tra `404` |
| `api/v1/endpoints/forecast.py` | 14 | 100% | **100%** | — | API dự báo & so sánh 5 mô hình |
| `api/v1/endpoints/history.py` | 63 | 70% | **98%** | **+28%** | `/readiness`, `/training-runs/{id}`, `/sources`, chuỗi khảo sát trực tiếp theo tỉnh |
| `api/v1/endpoints/market.py` | 25 | 96% | **100%** | **+4%** | Chặn `404` cho mã nông sản không tồn tại trên `/market/regional-prices/{code}` |
| `api/v1/endpoints/predictions.py` | 58 | 64% | **100%** | **+36%** | `/forecast` theo `commodity_id`, `/metrics`, xử lý ngoại lệ `500`, `_async_retrain_task` |
| `api/v1/endpoints/prices.py` | 12 | 83% | **100%** | **+17%** | `GET /api/v1/prices/history` |
| `api/v1/endpoints/regions.py` | 14 | 86% | **100%** | **+14%** | Xử lý lỗi định vị địa lý trả `400` an toàn |
| `core/config.py` | 20 | 100% | **100%** | — | Tải cấu hình môi trường |
| `core/database.py` | 11 | 64% | **64%** | — | `get_db()` được override bởi SQLite in-memory trong fixture test |
| `core/deps.py` | 42 | 86% | **100%** | **+14%** | JWT thiếu `sub`, user đã bị xóa (`404`), hạ cấp an toàn `get_optional_current_user` |
| `core/scheduler.py` | 47 | 26% | **100%** | **+74%** | Toàn bộ tác vụ lập lịch scrape/cảnh báo, xử lý ngoại lệ & vòng đời APScheduler |
| `core/schema_upgrade.py` | 23 | 39% | **74%** | **+35%** | Nâng cấp lược đồ thêm cột idempotent (6 dòng còn lại đặc thù riêng dialect PostgreSQL) |
| `core/security.py` | 79 | 95% | **100%** | **+5%** | Hash hỏng, chống CSV Formula Injection rỗng, reset khóa RateLimiter |
| `main.py` | 55 | 85% | **93%** | **+8%** | Endpoint `/`, `/health` trạng thái `degraded`, `global_exception_handler` `500` |
| `models/models.py` | 153 | 100% | **100%** | — | Toàn bộ thực thể ORM SQLAlchemy |
| `schemas/schemas.py` | 318 | 98% | **100%** | **+2%** | Đủ 6 ràng buộc nghiệp vụ của `PriceCreateManual` |
| `services/alert_service.py` | 159 | 77% | **99%** | **+22%** | Đánh giá `PCT_INC_7D`/`PCT_DEC_7D`, lọc sở hữu, SMTP thật & lỗi mạng |
| `services/commodity_service.py` | 135 | 81% | **96%** | **+15%** | Sparkline trực tiếp theo tỉnh ($\ge 5$ phiên), `spotlight`, bảng so sánh rỗng |
| `services/forecast_service.py` | 121 | 86% | **97%** | **+11%** | Mã lỗi `404`/`400`/`409` và chế độ tương thích bản ghi dự báo cũ |
| `services/history_service.py` | 106 | 83% | **100%** | **+17%** | Kiểm tra khoảng trống chuỗi >14 ngày, giá $\le 0$, hồi quy `periodic` $\to$ `daily` & `irregular` |
| `services/job_service.py` | 70 | 84% | **93%** | **+9%** | Thực thi `run_job("retrain")` thành công/thất bại & đồng bộ snapshot sau scrape |
| `services/regional_pricing_service.py` | 166 | 89% | **96%** | **+7%** | Cước vận chuyển `VNĐ/tấn`, khoảng cách $\le 5$ km, fallback mã tỉnh lạ |
| `services/training_service.py` | 106 | 78% | **99%** | **+21%** | Cô lập lỗi theo mô hình (`PARTIAL`), chặn tràn số $\ge 10^{12}$, tự chọn `active_model` |
| **TỔNG CỘNG (`app/`)** | **2.247** | **83% (377 miss)** | **98% (53 miss)** | **+15%** | **53 dòng còn lại chủ yếu là nhánh riêng PostgreSQL (`pg_advisory_xact_lock`, migration PG) và entrypoint `uvicorn`** |

---

## 4. KẾT QUẢ KIỂM THỬ END-TO-END TRÊN TRÌNH DUYỆT THẬT (PLAYWRIGHT)

Bộ kiểm thử tự động [e2e/test_agroforecast_e2e.py](file:///d:/DA_TN/e2e/test_agroforecast_e2e.py) điều khiển trình duyệt Chrome thật (`1440x900`) thao tác trực tiếp trên toàn bộ giao diện Next.js + Syncfusion EJ2 (`http://localhost:3000`) kết nối API FastAPI + PostgreSQL (`http://127.0.0.1:8000`):

| Mã E2E | Kịch Bản Người Dùng Thực Tế | Xác Minh Giao Diện & Dữ Liệu | Console / Runtime Errors | Banner Bản Quyền Syncfusion | Kết Quả |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **E2E-01** | **Trang Tổng quan (`/`) & Định giá theo Vị trí Khánh Hòa** | Mở bộ chọn khu vực trên Topbar, tìm & chọn **Khánh Hòa**; xác nhận thẻ Mía đường hiển thị huy hiệu xanh **`Khảo sát tại Khánh Hòa`**, các mặt hàng còn lại hiển thị **`Tham chiếu ...`**; mở bảng **`Chênh lệch giá theo tỉnh hôm nay`** hiển thị nhãn **`Đang chọn`** | **0** | **0** | **PASS** |
| **E2E-02** | **Trang Dự báo (`/forecast`) — Mô hình tốt nhất ($\star$), Kỳ hạn & Chuyển Tab** | Kiểm tra tự động kích hoạt mô hình tốt nhất (`★`) cho Lúa gạo & khi đổi sang Mía đường; chuyển kỳ hạn **`7N` $\leftrightarrow$ `30N`**; chuyển tab **`Bảng chi tiết dự báo` $\leftrightarrow$ `So sánh 5 mô hình`** kèm di chuột lên biểu đồ Syncfusion (đảm bảo không còn lỗi `BaseTooltip.appendChild`) | **0** | **0** | **PASS** |
| **E2E-03** | **Lịch sử (`/history`), So sánh (`/compare`) & Cảnh báo (`/alerts`)** | Xác nhận `GridComponent` (`.e-grid`) và `ChartComponent` (`.e-chart svg`) của Syncfusion hiển thị hoàn chỉnh, biểu đồ Pearson render sạch trên `/compare` | **0** | **0** | **PASS** |
| **E2E-04** | **Kiểm soát Truy cập RBAC (Guest / Analyst / Admin)** | 1) **Khách chưa đăng nhập** truy cập `/dashboard/overview` bị đẩy về `/login`; 2) **Analyst** (`anhnguyen@agroforecast.vn`) bị ẩn menu Quản trị ở Sidebar **và** bị chặn chuyển hướng khỏi toàn bộ 4 URL `/dashboard/*`; 3) **Admin** (`admin@agroforecast.vn`) truy cập trọn vẹn 4 trang `/dashboard/overview`, `/dashboard/data-control`, `/dashboard/ml-models`, `/dashboard/users` | **0** | **0** | **PASS** |

> **Phát hiện & Khắc phục Lỗ hổng Thực tế qua Quy trình TDD (Red → Green):**
> Trong lần chạy đầu tiên của **E2E-04**, Playwright đã bắt được một lỗi phân quyền thực tế trên Frontend: mặc dù Sidebar đã ẩn nhóm *Quản trị hệ thống* đối với vai trò `Analyst`, thành phần bảo vệ tuyến đường [frontend/src/app/dashboard/layout.tsx](file:///d:/DA_TN/frontend/src/app/dashboard/layout.tsx) vẫn kiểm tra `!['admin', 'analyst'].includes(user.role)`, khiến tài khoản `Analyst` vẫn mở được trang quản trị khi gõ trực tiếp URL `/dashboard/overview`. Nhóm đã thu hẹp điều kiện bảo vệ về chặt chẽ `user.role !== 'admin'`, build lại bản production (`next build`) và chạy lại **E2E-04** đạt **PASS 100%**.

---

## 5. QUY TRÌNH ỨNG DỤNG AGENT SKILLS TRONG KIỂM THỬ TỰ ĐỘNG (QA METHODOLOGY)

Để đảm bảo tính khoa học, khả năng tái lập và chất lượng công nghiệp cho đồ án tốt nghiệp, quy trình kiểm thử và nghiệm thu hệ thống **AgroForecast** áp dụng đồng bộ 4 **Agent Skills** chuẩn hóa lưu trong thư mục `.agents/skills/`:

1. **`coverage-analysis` (Phân tích Độ phủ Mã nguồn):**
   - Thiết lập mốc cơ sở (**Baseline = 83%**) bằng `pytest --cov=app --cov-report=term-missing`, phân loại các vùng mã chưa được phủ theo mức độ rủi ro nghiệp vụ (bảo mật Auth/RBAC, tính toàn vẹn dữ liệu giá/CSV, định giá theo tỉnh, cô lập lỗi huấn luyện ML, cảnh báo tự động) thay vì tăng số liệu hình thức.
   - Kết quả: Đẩy độ phủ Backend lên **98%**, với 12/27 module cốt lõi đạt **100%**.
2. **`test-driven-development` (Phát triển Hướng Kiểm thử — TDD Red/Green/Refactor):**
   - Viết trước kịch bản kiểm thử hành vi thực tế phản ánh đúng hợp đồng nghiệp vụ (không mock tràn lan logic cốt lõi, tự tính giá trị kỳ vọng bằng tay cho cước vận chuyển Haversine `VNĐ/tấn`, ngưỡng tăng/giảm 7 ngày, xác thực RBAC).
   - Chu trình **RED → GREEN** trên E2E-04 trực tiếp phát hiện và vá triệt để lỗ hổng truy cập URL trực tiếp `/dashboard/*` của tài khoản `Analyst`.
3. **`webapp-testing` (Kiểm thử Ứng dụng Web Thực tế với Playwright):**
   - Áp dụng mô hình *Reconnaissance-then-Action* kết hợp `wait_until="networkidle"`, gắn bộ thu thập tự động `page.on("console")` và `page.on("pageerror")` để kiểm chứng 100% luồng người dùng cuối trên trình duyệt thật (Location Picker Khánh Hòa, Syncfusion Grid/Chart tương tác chuột, phân quyền đa vai trò).
4. **`verification-before-completion` (Xác minh Chứng cứ Trước khi Kết luận):**
   - Tuân thủ nguyên tắc *Evidence Before Assertions*: mọi con số trong báo cáo (120/120 Backend tests, 98% coverage, 4/4 E2E Playwright, 3/3 Frontend unit tests, 0 TypeScript/ESLint errors, 17/17 Next.js routes) đều được trích xuất trực tiếp từ kết quả thực thi lệnh mới nhất ngay sau lần chỉnh sửa mã nguồn cuối cùng.
