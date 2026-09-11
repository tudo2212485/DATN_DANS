# Phase 3 Specification: Data Pipeline, Web Scraping & Scheduler (Thu Thập & Xử Lý Dữ Liệu)

## 1. Mục Tiêu (Objective)
Thu thập dữ liệu giá cả thị trường nông sản từ các nguồn bên ngoài (`giacaphe.com`, `yfinance`), làm sạch và tiền xử lý chuỗi thời gian bằng Pandas/Numpy, kiểm tra tính dừng (ADF Test), xử lý ngoại lai (IQR Capping), và thiết lập tiến trình chạy nền tự động với APScheduler.

## 2. Kiến Trúc Data Pipeline (Architecture)

```text
[ External Sources ] (Yahoo Finance, giacaphe.com, Hiệp hội VFA/VPA)
         │
         ▼
[ Ingestion & Scraping Module ] (requests, BeautifulSoup4, yfinance)
         │
         ▼
[ Data Cleaning & Preprocessing ]
 ├── Linear Interpolation (Điền khuyết chuỗi ngày liên tục)
 ├── IQR Outlier Capping (Chặn nhiễu sai lệch giá)
 ├── ADF Stationarity Test (Kiểm định chuỗi dừng p <= 0.05)
 └── Exogenous Variables Merge (Tích hợp USD/VND, Giá dầu WTI)
         │
         ▼
[ Database Storage ] (PostgreSQL - price_history, alerts)
         │
         ▼
[ Automated Scheduler & Engine ]
 ├── Daily Scraper Cron (Chạy lúc 06:00 AM mỗi ngày)
 └── Alert Engine (Đánh giá ngưỡng giá & gửi email cảnh báo)
```

## 3. Đặc Tả Chi Tiết Các Thành Phần

### 3.1 Module Thu Thập Dữ Liệu (`ml_pipeline/scraper.py`)
- **Web Scraping:** Cào giá nội địa thực tế tại các vùng trọng điểm (Tây Nguyên, ĐBSCL).
- **YFinance Connector:** Thu thập chuỗi giá tham chiếu hợp đồng tương lai (Rough Rice `ZR=F`, Coffee `KC=F`, Sugar `SB=F`).
- **Resilience:** Thiết lập timeout, User-Agent header đầy đủ và try/except an toàn.

### 3.2 Module Xử Lý Chuỗi Thời Gian (`ml_pipeline/data_loader.py`)
- **Điền khuyết ngày thiếu:** Tạo `date_range` liên tục hàng ngày và áp dụng `interpolate(method='linear')` kết hợp `ffill`/`bfill`.
- **Chặn ngoại lai (`handle_outliers_iqr`):** Cắt tỉa giá trị ngoài khoảng $[Q1 - 1.5 \times IQR, Q3 + 1.5 \times IQR]$ để tránh làm méo mó mô hình học máy.
- **Biến ngoại sinh (Exogenous Features):** Ghép nối tỷ giá USD/VND (`USDVND=X`) và Giá dầu thô WTI (`CL=F`) vào tập huấn luyện.

### 3.3 Động Cơ Đánh Giá Cảnh Báo (`app/services/alert_service.py`)
- Quét tự động các quy tắc: `PRICE_ABOVE`, `PRICE_BELOW`, `PCT_INC_7D`, `PCT_DEC_7D`.
- Tự động ghi lại nhật ký `AlertLog` và gửi email thông báo qua SMTP.

### 3.4 Điều Phối Tác Vụ Ngầm (`app/core/scheduler.py`)
- `daily_scraper`: Kích hoạt lúc 06:00 AM mỗi ngày.
- `daily_alert_evaluation`: Kích hoạt lúc 06:30 AM và 18:30 PM mỗi ngày.

## 4. Kết Quả Kiểm Thử (Testing & Acceptance Criteria)
Bộ test `tests/test_pipeline.py` bao phủ đầy đủ:
- [x] Test thuật toán IQR Outlier Capping chặn giá trị bất thường chính xác.
- [x] Test hàm `load_clean_data` xử lý an toàn khi DB trống và điền khuyết khi có dữ liệu.
- [x] Test bộ đánh giá quy tắc cảnh báo tự động phát hiện vượt ngưỡng và tạo `AlertLog`.
- [x] Test API Admin trigger cào dữ liệu chạy ngầm `/admin/tasks/scrape` thành công.
- [x] Bộ test suite 100% Passed (22/22 tests).

## 5. Sản Phẩm Bàn Giao (Deliverables)
1. Module cào dữ liệu và chuẩn hóa (`ml_pipeline/scraper.py`).
2. Module xử lý và làm sạch dữ liệu (`ml_pipeline/data_loader.py`).
3. Dịch vụ cảnh báo và gửi mail (`app/services/alert_service.py`).
4. Background Scheduler tích hợp vào vòng đời FastAPI (`app/core/scheduler.py`).
