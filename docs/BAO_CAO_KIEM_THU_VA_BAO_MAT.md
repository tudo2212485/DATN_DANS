# BÁO CÁO QUY TRÌNH & KẾT QUẢ KIỂM THỬ PHẦN MỀM, KIỂM TRA BẢO MẬT HỆ THỐNG AGROFORECAST

**Dự án:** Hệ thống Dự báo Biến động Giá Nông sản Việt Nam bằng Mô hình Học máy (Machine Learning)  
**Tiêu chuẩn áp dụng:** IEEE 829 (Software Test Documentation) & OWASP Top 10 / OWASP API Security

---

## 1. LỰA CHỌN PHƯƠNG PHÁP KIỂM THỬ & KIỂM TRA BẢO MẬT

Do hệ thống AgroForecast kết hợp giữa **Web Application (Next.js + FastAPI + PostgreSQL)**, **Thu thập dữ liệu tự động (Web Scraper)** và **Đường ống Học máy Chuỗi thời gian (5 mô hình AI: LSTM, Prophet, ARIMA, XGBoost, Random Forest)**, dự án sử dụng mô hình kiểm thử đa tầng như sau:

### 1.1. Các loại Kiểm thử Phần mềm (Software Testing) được áp dụng
1. **Kiểm thử Đơn vị — Hộp trắng (White-box Unit Testing):**
   - Kiểm tra trực tiếp từng hàm xử lý toán học và làm sạch dữ liệu (`handle_outliers_iqr`, `create_features`, `evaluate_metrics`, `sanitize_text`, `sanitize_csv_cell`).
2. **Kiểm thử Tích hợp API & Cơ sở dữ liệu — Hộp xám (Grey-box Integration Testing):**
   - Kiểm tra sự phối hợp giữa `FastAPI Router <-> Service <-> SQLAlchemy ORM <-> Database` trên môi trường CSDL cô lập (`SQLite In-Memory`), đảm bảo không làm sai lệch dữ liệu thật.
3. **Kiểm định Mô hình Học máy & Dự báo Không gian - Thời gian (ML Backtesting & Spatio-Temporal Validation):**
   - Kiểm tra cổng chặn sai số (`Threshold Gate` theo `RMSE`, `MAE`, `MAPE`, `R²`), kiểm tra tính hợp lệ toán học của dải tin cậy 95% (`lowerCI <= predictedPrice <= upperCI`) và kiểm tra độ lệch giá bán tại vườn/ruộng (`basisSpread`) giữa các huyện địa phương.
4. **Kiểm thử Chức năng Hệ thống — Hộp đen (Black-box End-to-End Workflow Testing):**
   - Kiểm tra luồng nghiệp vụ hoàn chỉnh từ *Thu thập lịch sử giá -> Duyệt dữ liệu (`provenance`) -> Huấn luyện mô hình -> Dự báo & Cảnh báo giá*.

### 1.2. Các loại Kiểm tra Bảo mật (Security Testing) được áp dụng
1. **Kiểm tra Bảo mật Tĩnh (SAST & Type/Dependency Verification):**
   - Rà soát mã nguồn tĩnh, kiểm tra cấu hình biến môi trường (`.env`) và kiểm tra kiểu dữ liệu nghiêm ngặt (`Pydantic v2` + `TypeScript Compiler`).
2. **Kiểm tra Bảo mật Động & Thâm nhập API Tự động (DAST / Automated API Penetration Testing):**
   - Giả lập các cuộc tấn công thực tế vào REST API theo khung **OWASP Top 10**:
     - Tấn công giả mạo chữ ký/thời hạn `JWT Token` (`HS256`) và mật khẩu `Bcrypt`.
     - Tấn công leo thang đặc quyền (`Privilege Escalation` / `RBAC Bypass`) từ tài khoản thường lên quyền `Admin`.
     - Tấn công tiêm mã độc `SQL Injection` (`SQLi`), `Cross-Site Scripting` (`Stored/Reflected XSS`) và `CSV Formula Injection`.
     - Tấn công vét cạn mật khẩu & làm nghẽn máy chủ (`Brute-Force & Rate Limiting`).
     - Kiểm tra 7 tiêu đề bảo mật phản hồi HTTP (`OWASP Security Response Headers`).

---

## 2. QUY TRÌNH THỰC HIỆN 5 BƯỚC

```
[Bước 1: Khởi tạo Sandbox DB cô lập (conftest.py)]
        ↓
[Bước 2: Kiểm thử Đơn vị & Làm sạch Dữ liệu (IQR Outlier, Lag/Rolling Features)]
        ↓
[Bước 3: Kiểm thử Tích hợp REST API & Kiểm định 5 Mô hình AI (Threshold Gate)]
        ↓
[Bước 4: Kiểm tra Bảo mật & Tấn công Giả lập OWASP Top 10 (test_security_phase7.py)]
        ↓
[Bước 5: Tổng hợp Ma trận Nghiệm thu (72/72 Tests PASSED - 100%)]
```

---

## 3. MA TRẬN KẾT QUẢ KIỂM THỬ & BẢO MẬT (TEST TRACEABILITY MATRIX)

| Mã nhóm | Tệp kiểm thử | Nội dung kiểm tra | Số kịch bản | Kết quả |
| :--- | :--- | :--- | :---: | :---: |
| **SEC-01** | `tests/test_security_phase7.py` | Kiểm tra 7 OWASP Security Headers, băm Bcrypt + Salt, chống XSS (`sanitize_text`), chống CSV Formula Injection (`sanitize_csv_cell`), Rate Limiter chống Brute-force, chống giả mạo JWT, chống leo thang đặc quyền RBAC (`403 Forbidden`), chống SQL Injection và kiểm chứng giá bán tại vườn theo huyện (`basisSpread`). | 10 | **PASSED (10/10)** |
| **AUTH-01** | `tests/test_auth.py` | Đăng ký, chặn trùng email (`400`), kiểm tra độ mạnh mật khẩu (`422`), đăng nhập cấp JWT, chặn sai mật khẩu/thiếu token (`401`). | 10 | **PASSED (10/10)** |
| **ML-01** | `tests/test_predictions.py` | Tạo đặc trưng chuỗi thời gian (`lag`, `rolling`), đánh giá `MAE/RMSE/MAPE/R²`, cổng chặn sai số `Threshold Gate`, huấn luyện & lưu model (`Prophet`, `XGBoost`, `PyTorch LSTM`), kiểm tra khoảng tin cậy 95% và `In-Memory Cache`. | 9 | **PASSED (9/9)** |
| **PIPE-01** | `tests/test_pipeline.py` | Chặn ngoại lai bằng thuật toán `IQR`, điền khuyết chuỗi thời gian, tự động kích hoạt quy tắc cảnh báo giá (`PRICE_ABOVE`), điều phối tác vụ cào dữ liệu ngầm. | 5 | **PASSED (5/5)** |
| **HIST-01** | `tests/test_history_workflow.py` | Kiểm soát nguồn gốc dữ liệu (`collected`, `reviewed`, `unverified`), chặn huấn luyện AI trên dữ liệu chưa xác minh, huấn luyện thực tế 5 thuật toán AI. | 11 | **PASSED (11/11)** |
| **SRC-01** | `tests/test_vietnam_sources.py` | Kiểm tra bộ bóc tách dữ liệu (Parser/Scraper) từ các nguồn nông sản Việt Nam (An Giang, Tây Nguyên, Viện Chiến lược, Hiệp hội Đường). | 6 | **PASSED (6/6)** |
| **ADM-01** | `tests/test_admin_phase5.py` & `test_admin_workflows.py` | Quản trị nông sản, nhập/xuất CSV, khóa/mở khóa người dùng, nhật ký Bot Scraper, chuyển đổi mô hình AI mặc định. | 17 | **PASSED (17/17)** |
| **SYS-01** | `tests/test_commodities.py`, `test_health.py`, `test_config.py` | Kiểm tra sức khỏe hệ thống (`/health`), kết nối CSDL, cấu hình môi trường và API tổng quan thị trường. | 4 | **PASSED (4/4)** |
| **TỔNG** | **Toàn bộ hệ thống Backend & AI** | **Tất cả các bài kiểm thử tự động & bảo mật** | **72** | **100% PASSED** |

---

## 4. HƯỚNG DẪN CHẠY LỆNH KIỂM CHỨNG TRỰC TIẾP

1. **Chạy kiểm thử Bảo mật & Chống tấn công OWASP Top 10:**
   ```powershell
   cd DATN_DANS\backend
   .\venv\Scripts\pytest.exe tests/test_security_phase7.py -v
   ```
2. **Chạy toàn bộ 72 kịch bản kiểm thử của hệ thống:**
   ```powershell
   cd DATN_DANS\backend
   .\venv\Scripts\pytest.exe -v
   ```
3. **Kiểm tra an toàn kiểu dữ liệu giao diện Frontend (TypeScript):**
   ```powershell
   cd DATN_DANS\frontend
   npx tsc --noEmit
   ```
