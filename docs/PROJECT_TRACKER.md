# PROJECT TRACKER — AgroForecast (v3.0 Final Release)

> **Cập nhật lần cuối:** 23/11/2026 (GMT+7)  
> **Trạng thái tổng thể:** **98% Hoàn thành (Production-Ready — Sẵn sàng Bảo vệ KLTN)**

---

## Bảng Tổng Quan Tiến Độ Phân Hệ

| # | Phân hệ chức năng | Backend (FastAPI) | Frontend (Next.js + Syncfusion EJ2) | AI / ML Pipeline | Tỷ lệ |
| :-: | :--- | :-: | :-: | :-: | :-: |
| 1 | **Auth & RBAC (OWASP Hardened)** | Done | Done | — | **100%** |
| 2 | **Market Overview & 33-Province Location-Aware** | Done | Done | Haversine + Direct Survey | **100%** |
| 3 | **ML Forecast 5 Models × 8 Commodities (Exogenous USD/VND + WTI)** | Done | Done | 40/40 Walk-Forward Models | **100%** |
| 4 | **History Verification Links & Compare (Pearson)** | Done | Done | 4.899 rows + 9.079 reg rows | **100%** |
| 5 | **Alert System & Live SMTP Email + APScheduler** | Done | Done | Cron 06:00/18:00 + Auto Catch-up | **100%** |
| 6 | **Admin Panel (Persistent Settings, Real Jobs, Audit Log)** | Done | Done | Background Jobs + SHA-256 | **100%** |
| 7 | **Testing, Security, Docker & Thesis Docs** | 125 Pytest + Bandit 0 | 4 Playwright E2E + Build 0 | Dockerfile + Compose + Thesis Synced | **95%** |

---

## Các Hạng Mục Đã Hoàn Thành Triệt Để So Với Phiên Bản Đầu (v2.4 → v3.0)

- [x] **Mở rộng từ 4 lên 8 mặt hàng nông sản (chốt mốc 23/11/2026):** Lúa IR50404 (`442`), Cà phê Robusta (`919`), Hồ tiêu đen (`793`), Mía đường 10 CCS (`729`), Dâu tây Đà Lạt (`504`), Khoai tây Đà Lạt (`504`), Khoai lang tím Vĩnh Long (`504`), Hạt điều (`504`) — tổng `4.899` phiên `price_history` + `9.079` quan sát cấp tỉnh.
- [x] **Kiểm toán 100% sự thật dữ liệu:** Xóa bài cũ TTC Sugar 2021, chuẩn hóa nhãn `giacaphe.com (Giá cà phê nội địa)`, sửa lỗi trùng slug `201/301` của VietnamBiz, gắn link bấm kiểm chứng trực tiếp trên `/history` và `/dashboard/data-control`.
- [x] **Tích hợp biến ngoại sinh nhân quả (O2) vào luồng huấn luyện live:** `history_models.py` + `training_service.py` tải thực `USD/VND (VND=X)` và `WTI Crude Oil (CL=F)` qua HTTPS, chỉ dùng độ trễ quá khứ (`<= t-1`, Zero Data Leakage — đã khóa bằng unit test `test_exogenous_features_strictly_causal_zero_leakage`).
- [x] **Hoàn thiện đủ 5 mô hình cho cả 8 nông sản (40 mô hình):** Random Forest, XGBoost, Prophet, ARIMA, PyTorch Stacked LSTM — đánh giá Walk-Forward 7 ngày + Conformal 95% CI (`MAPE tối ưu 0,74% – 2,62%`, nổi bật **PyTorch Stacked LSTM ★ đạt hạng 1 trên Cà phê Robusta với `R² = 0,8972`, `RMSE = 1.978,28 VNĐ/kg`**), siết chuẩn 3 kỳ hạn `days: Literal[7, 14, 30]` ở cả API và UI.
- [x] **Lưu bền vững cấu hình & nhật ký trong PostgreSQL:** `active_model` lưu vào `system_settings`, nhật ký scraper lưu vào `background_jobs`, kiểm toán chỉnh sửa giá lưu vào `price_revisions`, chữ ký dữ liệu SHA-256 lưu vào `training_runs`.
- [x] **Nâng cấp UI Syncfusion EJ2 & Đồng bộ `/commodities/[id]`:** `AgroGrid` (cột link native `queryCellInfo` chống lỗi React Portal), `FinChart` trục `DateTime`, `/commodities/[id]` đủ 5 mô hình + `★` + `LocationContext`.
- [x] **Cấu hình SMTP thật & APScheduler catch-up ngày mới:** `backend/.env` đã cấu hình `SMTP_HOST/PORT/USER/PASSWORD`; scheduler tự cập nhật nếu dữ liệu cũ hơn ngày hiện tại (GMT+7).
- [x] **Đóng gói Docker & Kiểm thử toàn diện:** Đã tạo `backend/Dockerfile`, `frontend/Dockerfile`, `.dockerignore`, `docker-compose.yml`; đạt **125/125 Pytest**, **4/4 Playwright E2E**, **Bandit SAST 0 Medium / 0 High**.

---

## Việc Còn Lại Duy Nhất Trước Ngày Bảo Vệ (Thủ công của sinh viên)

- [ ] Soạn **Slide thuyết trình PowerPoint** (15–20 trang, dựa trên `kich_ban_bao_cao.md` và 15 hình 300 DPI trong `docs/figures/`).
- [ ] Quay **Video demo ngắn (5 phút)** dự phòng trường hợp mất mạng tại phòng bảo vệ (nếu hội đồng yêu cầu).
