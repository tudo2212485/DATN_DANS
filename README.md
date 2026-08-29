# AgroForecast — Hệ Thống Dự Báo Giá & Cảnh Báo Thị Trường Nông Sản

Hệ thống ứng dụng Trí tuệ Nhân tạo (AI & Machine Learning) phục vụ theo dõi biến động, phân tích xu hướng và dự báo giá các mặt hàng nông sản chủ lực của Việt Nam (Lúa gạo, Cà phê, Hồ tiêu, Mía đường) kèm dải tin cậy 95% (Confidence Interval).

---

## 🚀 Công Nghệ Sử Dụng

- **Frontend:** Next.js 14 (App Router), TypeScript, Tailwind CSS, Recharts, Lucide Icons.
- **Backend:** Python 3.11, FastAPI, SQLAlchemy, Pydantic, Uvicorn.
- **Database:** PostgreSQL (Lưu trữ dữ liệu lịch sử giá, kết quả dự báo và cấu hình cảnh báo).
- **Machine Learning & Pipeline:** LSTM (Deep Learning), Facebook Prophet, ARIMA, Scikit-learn, Pandas.

---

## 🌟 Tính Năng Nổi Bật

1. **Tổng quan thị trường (Market Dashboard):**
   - Theo dõi giá giao dịch thời gian thực (Live Price), biên độ dao động và đồ thị sparkline cho 4 nông sản trọng điểm.
   - Biểu đồ chuẩn hóa tăng/giảm so với đầu kỳ & bảng giá theo từng khu vực/vùng chuyên canh.
2. **Mô hình & Dự báo AI (AI Forecasting):**
   - Dự báo chuỗi thời gian đa thuật toán (LSTM, Prophet, ARIMA, XGBoost).
   - Tích hợp dải tin cậy 95% (Upper / Lower Bound CI).
   - Đánh giá sai số mô hình trực tiếp: MAE, RMSE, MAPE, $R^2$.
   - Bảng chi tiết mốc dự báo có thanh cuộn dọc mượt mà, hiển thị tối ưu và gọn gàng.
3. **Quản lý Cảnh báo (Alerts Engine):**
   - Thiết lập quy tắc cảnh báo biến động giá thông minh (ngưỡng vượt đỉnh, sụt giảm nhanh).
   - Tự động kích hoạt thông báo email khi phát hiện điều kiện thị trường bất thường.
4. **Giao diện tối ưu & linh hoạt:**
   - Hỗ trợ thu gọn/mở rộng thanh điều hướng (Sidebar Collapse/Expand) giúp mở rộng không gian làm việc.

---

## 📁 Cấu Trúc Dự Án

```text
DA_TN/
├── backend/                  # REST API & Business Logic (FastAPI)
│   ├── app/                  # Endpoints, Models, Schemas, Services
│   ├── ml_pipeline/          # Huấn luyện mô hình (LSTM, Prophet) & Scraper
│   └── requirements.txt      # Thư viện Python
├── database/                 # Khởi tạo CSDL & Script nạp dữ liệu
│   ├── init.sql              # Schema CSDL PostgreSQL
│   └── load_database.py      # Seed dữ liệu lịch sử và dự báo
└── frontend/                 # Giao diện Web App (Next.js 14)
    ├── src/app/              # App Router (Dashboard, Forecast, Alerts, Login)
    ├── src/components/       # Layout, Charts, Tables, Cards
    └── package.json          # Dependencies Frontend
```

---

## 🛠 Hướng Dẫn Cài Đặt & Khởi Chạy

### 1. Cơ sở dữ liệu (PostgreSQL)
Tạo cơ sở dữ liệu PostgreSQL và import schema:
```bash
# Tạo database tên: agroforecast_db
# Thực thi script init.sql trong thư mục database/
```

### 2. Khởi chạy Backend (FastAPI)
```bash
cd backend
python -m venv venv
# Kích hoạt virtual environment (Windows: venv\Scripts\activate | Linux/macOS: source venv/bin/activate)
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
- **API URL:** `http://localhost:8000`
- **Swagger Docs:** `http://localhost:8000/docs`

### 3. Khởi chạy Frontend (Next.js)
```bash
cd frontend
npm install
npm run dev
```
- **Web App:** `http://localhost:3000`

---

## 🔑 Tài Khoản Dùng Thử (Demo Accounts)

| Vai trò | Email | Mật khẩu |
| :--- | :--- | :--- |
| **Nhà phân tích (Analyst)** | `anhnguyen@agroforecast.vn` | `123456` |
| **Quản trị viên (Admin)** | `admin@agroforecast.vn` | `admin123` |
