# AgroForecast — Hệ Thống Phân Tích Dữ Liệu & Dự Báo Giá Nông Sản Việt Nam

**Khóa luận Tốt nghiệp Kỹ sư Công nghệ Thông tin — Trường Đại học Đà Lạt (Khóa 46, 2022–2026)**
- **Nhóm sinh viên thực hiện:** Đỗ Trung Tú (`2212485`), Nguyễn Thành Huy Thông (`2212469`), Lê Văn Minh (`2212416`)
- **Giảng viên hướng dẫn:** ThS. La Quốc Thắng

Hệ thống Web Full-Stack ứng dụng Học máy & Học sâu (PyTorch Stacked LSTM, XGBoost, Random Forest, Prophet, ARIMA) tích hợp **biến ngoại sinh vĩ mô nhân quả (USD/VND & Dầu thô WTI)**, kiểm định **Walk-Forward 7 ngày không rò rỉ dữ liệu**, khoảng tin cậy **Conformal 95% CI**, định giá theo **33 tỉnh/thành phố (Haversine Location-Aware)** và truy xuất nguồn bài báo kiểm chứng thực tế cho **8 mặt hàng nông sản trọng điểm của Việt Nam**.

---

## Công Nghệ Sử Dụng

- **Frontend:** Next.js 14 (App Router), React 18, TypeScript 5, Tailwind CSS, **Syncfusion Essential Studio EJ2 React** (`AgroGrid`, `FinChart`), Recharts, Lucide Icons.
- **Backend:** Python 3.11, FastAPI, SQLAlchemy 2.x ORM, Pydantic v2, Uvicorn, APScheduler.
- **Database:** PostgreSQL 17 (12 bảng chuẩn hóa kèm `regional_markets`, `regional_price_observations`, `training_runs`, `price_revisions`, `background_jobs`, `system_settings`).
- **ML / Deep Learning:** PyTorch (Stacked LSTM 7 kênh), XGBoost & Random Forest (22 đặc trưng nhân quả), Facebook Prophet, Statsmodels ARIMA, kiểm định Walk-Forward + Conformal 95% CI.
- **Kiểm thử & Bảo mật:** Pytest (`125/125 PASS`), Playwright E2E trên Chrome thật (`4/4 PASS`), Bandit SAST (`0 Medium / 0 High`), OWASP Top 10 Hardening, Docker Compose.

---

## Danh Mục 8 Nông Sản & Độ Chính Xác Thực Nghiệm (Chốt mốc 23/11/2026)

| ID | Mã hàng | Tên nông sản | Số bản ghi (`price_history`) | Giai đoạn | Giá mới nhất | Mô hình tối ưu (`★`) | MAPE | R² | PICP 95% |
| :-: | :--- | :--- | :-: | :--- | --: | :--- | :-: | :-: | :-: |
| 1 | `RICE_IR504` | Lúa gạo IR50404 | 442 *(442 URL bài báo)* | 01/2024–11/2026 | 6.850 VNĐ/kg | ARIMA | 1,58% | 0,534 | 89,4% |
| 2 | `COFFEE_ROBUSTA` | Cà phê Robusta | 919 *(919 URL bài báo)* | 01/2024–11/2026 | 71.700 VNĐ/kg | **PyTorch LSTM** | 1,79% | **0,897** | 92,2% |
| 3 | `PEPPER_BLACK` | Hồ tiêu đen | 793 *(793 URL bài báo)* | 01/2024–11/2026 | 129.100 VNĐ/kg | ARIMA | 0,74% | 0,326 | 94,4% |
| 4 | `SUGARCANE` | Mía đường 10 CCS | 729 *(ICE #11 + 8 báo 2024–26)* | 01/2024–11/2026 | 1.230.000 VNĐ/tấn | Prophet | 2,62% | 0,857 | 97,8% |
| 5 | `STRAWBERRY` | Dâu tây Đà Lạt | 504 *(Kamereo + ETF DBA×FX)* | 11/2024–11/2026 | 100.000 VNĐ/kg | Prophet | 1,08% | 0,869 | 100,0% |
| 6 | `POTATO` | Khoai tây Đà Lạt | 504 *(Nam Tĩnh + ETF MOO×FX)* | 11/2024–11/2026 | 20.000 VNĐ/kg | Prophet | 1,30% | 0,712 | 100,0% |
| 7 | `SWEET_POTATO` | Khoai lang tím Vĩnh Long | 504 *(BGNS + ETF CORN×FX)* | 11/2024–11/2026 | 16.000 VNĐ/kg | XGBoost | 1,71% | 0,884 | 97,3% |
| 8 | `CASHEW_NUT` | Hạt điều | 504 *(BGNS 7 tỉnh + ETF SOYB×FX)* | 11/2024–11/2026 | 32.500 VNĐ/kg | ARIMA | 1,30% | 0,813 | 100,0% |

*(Tổng cộng **4.899 bản ghi** trong `price_history` và **9.079 quan sát khảo sát cấp tỉnh** trong `regional_price_observations` chốt tại mốc 23/11/2026; hệ thống vận hành thực tế tiếp tục tự động cập nhật hằng ngày qua APScheduler 06:00 & 18:00 GMT+7.)*

---

## Tính Năng Chính

1. **Tổng quan thị trường & Định giá theo vị trí 33 tỉnh/thành (`/`):**
   - Hiển thị 8 nông sản với sparkline, bộ lọc nhanh, chọn tỉnh/thành trên Topbar (hoặc GPS Haversine tự định vị): tự động tách nhãn **Khảo sát trực tiếp** vs **Tham chiếu vùng lân cận (+cước vận chuyển)**.
2. **Phân tích & Dự báo AI 5 mô hình (`/forecast` và `/commodities/[id]`):**
   - Tự động chọn mô hình tối ưu (`★`), hỗ trợ kỳ hạn **7N / 14N / 30N**, khoảng tin cậy Conformal 95% mở rộng theo $\sqrt{h}$, giải thích AI (XAI), bảng chi tiết `AgroGrid` xuất Excel/CSV và tab so sánh trực quan 5 mô hình.
3. **Dữ liệu lịch sử & Kiểm chứng nguồn gốc (`/history`):**
   - Biểu đồ Syncfusion `FinChart` trục `DateTime` chống chồng chéo nhiều năm, cột **Nguồn công bố** cho phép bấm trực tiếp mở bài báo gốc (`vietnambiz.vn`, `giacaphe.com`, `vietfood.org.vn`, `finance.yahoo.com`, báo địa phương 2024–2026).
4. **So sánh nông sản (`/compare`) & Cảnh báo Email tự động (`/alerts`):**
   - Chuẩn hóa đường tăng trưởng + ma trận tương quan Pearson; cảnh báo 4 điều kiện (`PRICE_ABOVE`, `PRICE_BELOW`, `PCT_INC_7D`, `PCT_DEC_7D`) gửi email SMTP thực qua APScheduler (06:30 & 18:30 GMT+7).
5. **Phân hệ Quản trị Admin (`/dashboard/*`):**
   - Khóa chặt RBAC (`admin` only), CRUD giá & nông sản kèm `PriceRevision` Audit Log, Import/Export CSV chống Formula Injection, kích hoạt Scrape & Retrain chạy nền lưu vết trong `background_jobs`, chuyển đổi mô hình mặc định lưu bền vững trong `system_settings`, quản lý tài khoản & khóa phiên tức thời.

---

## Hướng Dẫn Cài Đặt & Khởi Chạy

### Cách 1: Chạy trực tiếp trên Windows (Khuyến nghị khi demo)
```bat
setup_env.bat
run_all.bat
```
Hoặc chạy thủ công từng dịch vụ:
```powershell
# Backend (http://127.0.0.1:8000 | Swagger: http://127.0.0.1:8000/docs)
cd backend
.\venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000

# Frontend (http://localhost:3000)
cd frontend
npm run build && npm run start
```

### Cách 2: Chạy bằng Docker Compose
```bash
# Tạo file .env ở thư mục gốc chứa POSTGRES_PASSWORD, SECRET_KEY, NEXT_PUBLIC_SYNCFUSION_LICENSE_KEY
docker compose up --build -d
```

### Chạy bộ Kiểm thử & Kiểm toán Bảo mật
```powershell
# Backend Unit, Integration, ML & OWASP Tests (125/125 PASS)
cd backend && .\venv\Scripts\pytest.exe -v

# Backend SAST (Bandit: 0 Medium / 0 High)
cd backend && .\venv\Scripts\bandit.exe -r app -ll && .\venv\Scripts\bandit.exe -r ml_pipeline -ll

# End-to-End Browser Tests (Playwright Chrome: 4/4 PASS)
.\backend\venv\Scripts\pytest.exe e2e\test_agroforecast_e2e.py -v
```

---

## Tài Khoản Dùng Thử (Demo Accounts)

| Vai trò | Email | Mật khẩu | Quyền hạn |
| :--- | :--- | :--- | :--- |
| **Quản trị viên (Admin)** | `admin@agroforecast.vn` | `admin123` | Toàn quyền quản trị `/dashboard/*`, cào dữ liệu, retrain AI |
| **Chuyên viên (Analyst)** | `anhnguyen@agroforecast.vn` | `123456` | Tra cứu, dự báo, cảnh báo cá nhân (bị chặn khỏi `/dashboard/*`) |
