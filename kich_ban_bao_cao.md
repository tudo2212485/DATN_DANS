# Kịch Bản Báo Cáo Bảo Vệ Khóa Luận Tốt Nghiệp: Hệ Thống AgroForecast

**Thời lượng trình bày:** 8 – 10 phút  
**Nhóm sinh viên thực hiện:** Đỗ Trung Tú (`2212485`), Nguyễn Thành Huy Thông (`2212469`), Lê Văn Minh (`2212416`)  
**Giảng viên hướng dẫn:** ThS. La Quốc Thắng — Khoa Công nghệ Thông tin, Trường Đại học Đà Lạt  

---

## 1. Mở đầu & Đặt vấn đề (1,5 phút)
- **Lời chào:** "Kính chào quý thầy cô trong Hội đồng chấm Khóa luận tốt nghiệp. Nhóm chúng em gồm Đỗ Trung Tú, Nguyễn Thành Huy Thông và Lê Văn Minh, dưới sự hướng dẫn của ThS. La Quốc Thắng, xin phép trình bày đề tài: **Xây dựng ứng dụng phân tích dữ liệu và dự báo biến động giá nông sản theo chuỗi thời gian sử dụng học máy (AgroForecast)**."
- **Bài toán thực tiễn:** Giá bán nông sản tại vườn/ruộng (Farm-gate Price) như cà phê Tây Nguyên, hồ tiêu, lúa ĐBSCL, mía đường và đặc sản Đà Lạt (dâu tây, khoai tây) biến động liên tục theo mùa vụ, tỷ giá USD/VND và giá năng lượng thế giới. Các trang tin hiện nay chỉ thống kê giá quá khứ theo vùng lớn, chưa có dự báo định lượng theo địa phương kèm khoảng tin cậy và cảnh báo tự động.
- **Đóng góp của đề tài:** Xây dựng hệ thống Web Full-Stack chuẩn sản xuất quản lý **8 mặt hàng nông sản** (gồm đặc sản Đà Lạt – Lâm Đồng), **4.899 bản ghi giá lịch sử 2024–2026** + **9.079 quan sát khảo sát theo tỉnh** *(chốt mốc 23/11/2026, tự động cập nhật hằng ngày)*, đối sánh **5 thuật toán ML/DL** có tích hợp **biến ngoại sinh nhân quả (USD/VND, Dầu thô WTI)**, đánh giá **Walk-Forward 7 ngày không rò rỉ dữ liệu**, và kiểm thử tự động **132 kịch bản (125 Pytest + 3 FE Unit + 4 Playwright E2E) + bảo mật OWASP Top 10 (Bandit 0 lỗi)**.

---

## 2. Kiến trúc, Dữ liệu thật & Học máy (2 phút)
- **Kiến trúc 3 tầng:** Frontend **Next.js 14 + TypeScript + Syncfusion EJ2 (`AgroGrid`, `FinChart`)** ↔ Backend **FastAPI + SQLAlchemy 2.0 + APScheduler** ↔ **PostgreSQL 17 (12 bảng chuẩn hóa)**, hỗ trợ đóng gói qua **Docker Compose**.
- **Minh bạch nguồn gốc dữ liệu — Phân tách rõ 3 nhóm nguồn (Zero Fabrication):**
  - **Nhóm 1 — 3 nông sản chủ lực có 100% URL bài báo kiểm chứng từng ngày (2.154 phiên):** Cà phê Robusta (`919` bài `vietnambiz.vn` + `giacaphe.com`), Hồ tiêu đen (`793` bài `vietnambiz.vn`), Lúa gạo IR50404 (`442` bài/bản tin Sở NN&PTNT An Giang + VFA `vietfood.org.vn`).
  - **Nhóm 2 — Mía đường 10 CCS (`729` phiên):** quy đổi minh bạch từ sàn ICE Sugar #11 (`SB=F × USD/VND`) kết hợp 8 bài báo khảo sát vụ ép 2024–2026 tại Khánh Hòa, Phú Yên, Gia Lai.
  - **Nhóm 3 — 4 đặc sản mở rộng (Dâu tây Đà Lạt, Khoai tây Đà Lạt, Khoai lang tím Vĩnh Long, Hạt điều — `504` phiên/mặt hàng):** neo giá khảo sát sống tại Việt Nam (`Kamereo`, `Nam Tĩnh Lâm Đồng`, `banggianongsan.com`) kết hợp chuỗi tham chiếu Proxy Index ETF Yahoo Finance (`DBA`, `MOO`, `CORN`, `SOYB` × `USD/VND`) do thị trường rau củ nội địa không niêm yết giá hằng ngày nhiều năm — gắn nhãn minh bạch trực tiếp trên giao diện `/history`.
- **Đường ống ML chuẩn khoa học:**
  - Huấn luyện đồng bộ **5 mô hình**: **PyTorch Stacked LSTM (7 kênh)**, **XGBoost (22 đặc trưng)**, **Random Forest (22 đặc trưng)**, **Facebook Prophet** và **ARIMA**.
  - Đưa **biến ngoại sinh nhân quả** (`USD/VND`, `WTI CL=F` chỉ lấy độ trễ quá khứ ≤ `t-1`) — riêng trên **Cà phê Robusta (919 phiên)**, **PyTorch Stacked LSTM (7 kênh)** xuất sắc vươn lên **Hạng 1 toàn bảng** với **RMSE = `1.978,28 VNĐ/kg`**, **MAPE = `1,79%`**, **`R² = 0,8972`** (vượt sâu Naive Baseline `MAPE 1,88%`, `RMSE 2.147,01 VNĐ/kg`).
  - Mọi phiên huấn luyện lưu chữ ký **SHA-256 `dataset_hash`** trong `training_runs` (chống Stale Forecast) và khoảng tin cậy **Conformal 95% CI** mở rộng theo $\sqrt{h}$ (độ phủ thực nghiệm `PICP 89,4% – 100%`).

---

## 3. Demo trực tiếp trên hệ thống thật (4 – 5 phút)
*(Mở trình duyệt tại `http://localhost:3000` — cả 2 server đã chạy sẵn)*

1. **Trang Tổng quan (`/`) & Định giá theo vị trí 33 tỉnh/thành:**
   - Chỉ 8 thẻ nông sản (có Dâu tây Đà Lạt, Khoai tây Đà Lạt, Khoai lang tím, Hạt điều).
   - Mở bộ chọn vị trí trên Topbar → chọn **Khánh Hòa** (hoặc **Lâm Đồng**): chứng minh cơ chế 2 tầng minh bạch (**Khảo sát trực tiếp tại địa phương** vs **Tham chiếu vùng lân cận + cước vận chuyển Haversine**), mở bảng *"Chênh lệch giá theo tỉnh hôm nay"*.
2. **Trang Dữ liệu lịch sử (`/history`):**
   - Chọn **Cà phê Robusta** / **Lúa gạo IR50404** / **Mía đường**, bật khoảng `1N`: chỉ biểu đồ Syncfusion `FinChart` trục `DateTime` mượt (không chồng nhãn nhiều năm).
   - **Điểm nhấn kiểm chứng:** Bấm trực tiếp vào liên kết trong cột **Nguồn công bố** (`VietnamBiz ↗`, `giacaphe.com ↗`, `Yahoo Finance SB=F ↗`) → mở ra đúng bài báo gốc ngày đó khớp từng đồng với giá trong bảng!
3. **Trang Phân tích & Dự báo AI (`/forecast` & `/commodities/[id]`):**
   - Chọn từng nông sản → chỉ hệ thống **tự động kích hoạt mô hình tối ưu (`★`)** (VD: Cà phê `PyTorch LSTM 1,79% / R² = 0,8972`, Hồ tiêu `ARIMA 0,74%`, Lúa `ARIMA 1,58%`, Mía đường `Prophet 2,62%`, Dâu tây Đà Lạt `Prophet 1,08%`).
   - Chuyển kỳ hạn **7N / 14N / 30N** → thấy dải tin cậy 95% mở rộng tự nhiên theo thời gian; chuyển sang tab **So sánh 5 mô hình** (đối chiếu cả 5 thuật toán trên MAE, RMSE, MAPE, R²) và nút xuất Excel/CSV từ `AgroGrid`.
4. **Trang So sánh (`/compare`) & Cảnh báo Email (`/alerts`):**
   - Xem đồ thị tăng trưởng chuẩn hóa + ma trận tương quan Pearson giữa các nông sản.
   - Tạo nhanh 1 quy tắc cảnh báo ngưỡng giá và bấm nút **Gửi thử Email** chứng minh SMTP hoạt động thật.
5. **Phân hệ Quản trị & Bảo mật RBAC (`/dashboard/*`):**
   - Đăng nhập bằng **Analyst** (`anhnguyen@agroforecast.vn`) → gõ thẳng `/dashboard/overview` → chứng minh bị chặn tuyệt đối ở cả Frontend lẫn Backend (`403 Forbidden`).
   - Đăng nhập bằng **Admin** (`admin@agroforecast.vn` / `admin123`) → trình diễn quản trị điểm giá (có `PriceRevision` Audit Log), kích hoạt Scrape/Retrain nền (`background_jobs`), đổi mô hình mặc định (`system_settings`) và quản lý khóa/mở tài khoản.

---

## 4. Kết luận & Trả lời câu hỏi Hội đồng (1 phút)
- Tóm tắt 4 kết quả đạt được (8 nông sản với 4.899 phiên lịch sử, 40 mô hình MAPE `0,74%–2,62%` trong đó PyTorch LSTM dẫn đầu Cà phê Robusta `R² = 0,8972`, định giá 33 tỉnh thành, 132 kịch bản kiểm thử 100% PASS & Bandit 0 lỗi).
- Nhắc hướng phát triển: tích hợp thêm dữ liệu khí tượng thời gian thực (lượng mưa, nhiệt độ Tây Nguyên – Đà Lạt), mô hình Temporal Fusion Transformer (TFT) và ứng dụng di động cho nông hộ.
- Cảm ơn GVHD ThS. La Quốc Thắng và quý thầy cô Hội đồng, mời đặt câu hỏi.
