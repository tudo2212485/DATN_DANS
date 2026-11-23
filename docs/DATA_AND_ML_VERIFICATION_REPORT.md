# BÁO CÁO KIỂM CHỨNG DỮ LIỆU THẬT 2024–2026 & ĐÁNH GIÁ 40 MÔ HÌNH HỌC MÁY (8 NÔNG SẢN × 5 THUẬT TOÁN)

- **Mốc chốt số liệu báo cáo:** `23/11/2026` *(hệ thống thực tế tiếp tục tự động cập nhật dữ liệu & tái huấn luyện hằng ngày qua APScheduler 06:00 & 18:00 GMT+7)*
- **Phạm vi dữ liệu:** `01/01/2024 – 23/11/2026` (**4.899 bản ghi** `price_history` + **9.079 quan sát cấp tỉnh** `regional_price_observations`)
- **Phương pháp đánh giá:** Walk-Forward cuộn 7 ngày (Zero Data Leakage), tích hợp **2 biến ngoại sinh vĩ mô nhân quả** (`USD/VND: VND=X`, `Dầu thô WTI: CL=F` chỉ dùng quan sát quá khứ `<= t-1`), hiệu chỉnh khoảng tin cậy **Conformal 95% CI** mở rộng theo $\sqrt{h}$, chuẩn 3 kỳ hạn **`7N / 14N / 30N`** (siết chặt `Literal[7, 14, 30]` ở cả API và UI).

---

## 1. Phân Tách Minh Bạch 3 Nhóm Nguồn Gốc Dữ Liệu (8 Nông Sản)

1. **Nhóm 1 — 3 mặt hàng xuất khẩu/lương thực chủ lực (2.154 phiên — 100% URL bài báo riêng theo từng ngày):** `RICE_IR504` (`442`), `COFFEE_ROBUSTA` (`919`), `PEPPER_BLACK` (`793`).
2. **Nhóm 2 — Mía đường 10 CCS (729 phiên):** quy đổi minh bạch từ sàn đường thế giới **ICE Sugar #11 (`Yahoo Finance SB=F × USD/VND`)** kết hợp **8 bài báo khảo sát vụ ép 2024–2026** tại Khánh Hòa, Phú Yên, Gia Lai trong `regional_price_observations`.
3. **Nhóm 3 — 4 mặt hàng đặc sản mở rộng (`504` phiên/mặt hàng):** neo giá **khảo sát sống tại Việt Nam** (`kamereo.vn`, `namtinhvegetable.com`, `banggianongsan.com`) kết hợp **chuỗi tham chiếu Proxy Index ETF Yahoo Finance (`DBA`, `MOO`, `CORN`, `SOYB` × `USD/VND`)** do thị trường rau củ quả nội địa không niêm yết giá hằng ngày nhiều năm. Toàn bộ hiển thị nhãn minh bạch trực tiếp trên `/history`.

| ID | Mã hàng | Tên nông sản | Số dòng `price_history` | `DISTINCT source_url` | Giai đoạn | Giá mới nhất | `regional` (dòng / tỉnh) | Nguồn gốc kiểm chứng minh bạch |
| :-: | :--- | :--- | :-: | :-: | :--- | --: | :-: | :--- |
| 1 | `RICE_IR504` | Lúa gạo IR50404 | 442 | 442 | 01/01/2024 – 23/11/2026 | 6.850 VNĐ/kg | 1.101 / 7 tỉnh | `vietnambiz.vn` (381) + VFA `vietfood.org.vn` (61) — 100% bài báo/bản tin từng ngày |
| 2 | `COFFEE_ROBUSTA` | Cà phê Robusta | 919 | 919 | 04/01/2024 – 23/11/2026 | 71.700 VNĐ/kg | 3.485 / 4 tỉnh | `vietnambiz.vn` (903) + `giacaphe.com` (16) — 100% bài báo thật từng ngày |
| 3 | `PEPPER_BLACK` | Hồ tiêu đen | 793 | 793 | 04/01/2024 – 23/11/2026 | 129.100 VNĐ/kg | 4.446 / 6 tỉnh | `vietnambiz.vn` (793) — 100% bài báo thật từng ngày (6 tỉnh trọng điểm) |
| 4 | `SUGARCANE` | Mía đường 10 CCS | 729 | 1 *(sàn)* + 8 *(báo tỉnh)* | 02/01/2024 – 23/11/2026 | 1.230.000 VNĐ/tấn | 8 / 3 tỉnh | Quy đổi sàn ICE Sugar #11 (`SB=F × VND=X`) + 8 báo vụ ép 2024–2026 |
| 5 | `STRAWBERRY` | Dâu tây Đà Lạt | 504 | 2 | 21/11/2024 – 23/11/2026 | 100.000 VNĐ/kg | 6 / 2 tỉnh | Khảo sát sống `kamereo.vn` (`21–23/11/2026`) + 501 phiên Proxy ETF `DBA × VND=X` |
| 6 | `POTATO` | Khoai tây Đà Lạt | 504 | 2 | 21/11/2024 – 23/11/2026 | 20.000 VNĐ/kg | 3 / 1 tỉnh | Khảo sát sống `namtinhvegetable.com` (`21–23/11/2026`) + 501 phiên Proxy ETF `MOO × VND=X` |
| 7 | `SWEET_POTATO` | Khoai lang tím Vĩnh Long | 504 | 2 | 21/11/2024 – 23/11/2026 | 16.000 VNĐ/kg | 9 / 3 tỉnh | Khảo sát sống `banggianongsan.com` (`21–23/11/2026`) + 501 phiên Proxy ETF `CORN × VND=X` |
| 8 | `CASHEW_NUT` | Hạt điều | 504 | 2 | 21/11/2024 – 23/11/2026 | 32.500 VNĐ/kg | 21 / 7 tỉnh | Khảo sát sống `banggianongsan.com` 7 tỉnh (`21–23/11/2026`) + 501 phiên Proxy ETF `SOYB × VND=X` |

---

## 2. Kết Quả Đánh Giá Walk-Forward 7 Ngày (Đầy Đủ 40 Mô Hình + Biến Ngoại Sinh USD/VND & WTI — Mốc 23/11/2026)

| Nông sản | Mô hình | MAE | RMSE | MAPE (%) | Accuracy (%) | R² | PICP 95% (%) | Ghi chú |
| :--- | :--- | --: | --: | --: | --: | --: | --: | :--- |
| **Lúa gạo IR50404** | **ARIMA** | **100,24** | **169,20** | **1,58%** | **98,42%** | **0,5340** | **89,39%** | **★ Tối ưu (Hạng 1)** |
| Lúa gạo IR50404 | Prophet | 100,13 | 156,67 | 1,59% | 98,41% | 0,6005 | 89,39% | Hạng 2 (RMSE thấp nhất & R² cao nhất) |
| Lúa gạo IR50404 | XGBoost | 104,50 | 170,92 | 1,65% | 98,35% | 0,5244 | 87,88% | Hạng 3 |
| Lúa gạo IR50404 | Random Forest | 105,29 | 170,13 | 1,67% | 98,33% | 0,5288 | 89,39% | Hạng 4 |
| Lúa gạo IR50404 | LSTM | 111,45 | 171,72 | 1,77% | 98,23% | 0,5200 | 89,39% | Hạng 5 |
| **Cà phê Robusta** | **PyTorch LSTM** | **1.555,41** | **1.978,28** | **1,79%** | **98,21%** | **0,8972** | **92,22%** | **★ Tối ưu (Hạng 1 — Vượt sâu Baseline 1,88%)** |
| Cà phê Robusta | ARIMA | 1.605,21 | 2.121,40 | 1,86% | 98,14% | 0,8818 | 90,00% | Hạng 2 (Vượt Baseline) |
| Cà phê Robusta | Random Forest | 1.643,09 | 2.087,40 | 1,90% | 98,10% | 0,8856 | 90,00% | Hạng 3 (RMSE thấp thứ 2) |
| Cà phê Robusta | XGBoost | 1.703,99 | 2.120,44 | 1,96% | 98,04% | 0,8819 | 92,22% | Hạng 4 |
| Cà phê Robusta | Prophet | 1.882,04 | 2.386,65 | 2,15% | 97,85% | 0,8504 | 87,78% | Hạng 5 |
| **Hồ tiêu đen** | **ARIMA** | **990,46** | **1.643,77** | **0,74%** | **99,26%** | **0,3256** | **94,44%** | **★ Tối ưu (Vượt Baseline RMSE 1.646,34)** |
| Hồ tiêu đen | XGBoost | 1.045,64 | 1.646,95 | 0,78% | 99,22% | 0,3230 | 94,44% | Hạng 2 |
| Hồ tiêu đen | Random Forest | 1.054,90 | 1.631,93 | 0,78% | 99,22% | 0,3353 | 94,44% | Hạng 3 (RMSE thấp nhất & R² cao nhất) |
| Hồ tiêu đen | LSTM | 1.070,99 | 1.729,36 | 0,79% | 99,21% | 0,2536 | 92,22% | Hạng 4 |
| Hồ tiêu đen | Prophet | 1.174,41 | 1.708,35 | 0,87% | 99,13% | 0,2716 | 94,44% | Hạng 5 |
| **Mía đường 10 CCS** | **Prophet** | **34.245,40** | **46.011,00** | **2,62%** | **97,38%** | **0,8571** | **97,78%** | **★ Tối ưu (Vượt Baseline 2,74%)** |
| Mía đường 10 CCS | Random Forest | 35.303,99 | 48.177,63 | 2,70% | 97,30% | 0,8434 | 96,67% | Hạng 2 (Vượt Baseline) |
| Mía đường 10 CCS | ARIMA | 35.800,52 | 47.960,56 | 2,74% | 97,26% | 0,8448 | 97,78% | Hạng 3 |
| Mía đường 10 CCS | LSTM | 36.056,90 | 48.324,82 | 2,75% | 97,25% | 0,8424 | 96,67% | Hạng 4 |
| Mía đường 10 CCS | XGBoost | 36.244,16 | 48.578,33 | 2,77% | 97,23% | 0,8408 | 97,78% | Hạng 5 |
| **Dâu tây Đà Lạt** | **Prophet** | **1.164,79** | **1.610,18** | **1,08%** | **98,92%** | **0,8693** | **100,00%** | **★ Tối ưu (Vượt sâu Baseline 1,30%)** |
| Dâu tây Đà Lạt | ARIMA | 1.393,33 | 1.684,24 | 1,30% | 98,70% | 0,8570 | 100,00% | Hạng 2 |
| Dâu tây Đà Lạt | XGBoost | 1.398,31 | 1.687,84 | 1,30% | 98,70% | 0,8564 | 100,00% | Hạng 3 |
| Dâu tây Đà Lạt | Random Forest | 1.400,17 | 1.694,39 | 1,31% | 98,69% | 0,8553 | 100,00% | Hạng 4 |
| Dâu tây Đà Lạt | LSTM | 1.429,96 | 1.864,54 | 1,35% | 98,65% | 0,8247 | 93,33% | Hạng 5 |
| **Khoai tây Đà Lạt** | **Prophet** | **276,05** | **368,60** | **1,30%** | **98,70%** | **0,7119** | **100,00%** | **★ Tối ưu (Vượt Baseline 1,39%)** |
| Khoai tây Đà Lạt | ARIMA | 295,28 | 389,19 | 1,40% | 98,60% | 0,6789 | 100,00% | Hạng 2 |
| Khoai tây Đà Lạt | Random Forest | 301,30 | 390,70 | 1,42% | 98,58% | 0,6764 | 100,00% | Hạng 3 |
| Khoai tây Đà Lạt | XGBoost | 302,97 | 399,72 | 1,43% | 98,57% | 0,6612 | 100,00% | Hạng 4 |
| Khoai tây Đà Lạt | LSTM | 338,12 | 439,38 | 1,60% | 98,40% | 0,5907 | 98,67% | Hạng 5 |
| **Khoai lang tím** | **XGBoost** | **305,09** | **393,93** | **1,71%** | **98,29%** | **0,8844** | **97,33%** | **★ Tối ưu (Vượt Baseline 1,715%)** |
| Khoai lang tím | ARIMA | 312,35 | 399,68 | 1,75% | 98,25% | 0,8810 | 97,33% | Hạng 2 |
| Khoai lang tím | Random Forest | 316,30 | 410,99 | 1,77% | 98,23% | 0,8741 | 97,33% | Hạng 3 |
| Khoai lang tím | LSTM | 342,59 | 437,71 | 1,93% | 98,07% | 0,8573 | 97,33% | Hạng 4 |
| Khoai lang tím | Prophet | 348,48 | 416,80 | 1,97% | 98,03% | 0,8706 | 96,00% | Hạng 5 |
| **Hạt điều** | **ARIMA** | **444,00** | **555,34** | **1,30%** | **98,70%** | **0,8127** | **100,00%** | **★ Tối ưu** |
| Hạt điều | XGBoost | 452,95 | 561,88 | 1,33% | 98,67% | 0,8082 | 100,00% | Hạng 2 |
| Hạt điều | LSTM | 459,15 | 578,31 | 1,35% | 98,65% | 0,7968 | 98,67% | Hạng 3 |
| Hạt điều | Random Forest | 477,33 | 583,76 | 1,40% | 98,60% | 0,7930 | 100,00% | Hạng 4 |
| Hạt điều | Prophet | 491,06 | 696,47 | 1,43% | 98,57% | 0,7053 | 97,33% | Hạng 5 |

> **Đánh giá hiệu quả biến ngoại sinh nhân quả (`USD/VND` & `WTI CL=F`):** Trên mặt hàng xuất khẩu biến động mạnh nhất hệ thống là **Cà phê Robusta (919 phiên)**, mạng học sâu **PyTorch Stacked LSTM (7 kênh nhân quả gồm 5 kênh nội sinh + lợi suất USD/VND & WTI `<= t-1`)** xuất sắc đạt **Hạng 1 tuyệt đối** trên mọi thước đo: **MAE = `1.555,41 VNĐ/kg`**, **RMSE = `1.978,28 VNĐ/kg`**, **MAPE = `1,79%`**, **`R² = 0,8972`** và **PICP 95% = `92,22%`**, vượt trội rõ rệt so với Naive Baseline (`MAE = 1.621,11`, `RMSE = 2.147,01`, `MAPE = 1,88%`, `R² = 0,8790`).
