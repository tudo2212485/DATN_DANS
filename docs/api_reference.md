# 📡 API REFERENCE — AgroForecast RESTful API

## Hệ thống Dự báo Giá Nông sản & Cảnh báo Thị trường

> **Framework:** Python FastAPI + Pydantic v2 + SQLAlchemy 2.x  
> **Phiên bản API:** v1 (stable)  
> **Cập nhật:** 10/09/2026  
> **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)  
> **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Mục lục

1. [Quy ước Chung](#1-quy-ước-chung)
2. [Nhóm Auth — Xác thực & Phân quyền](#2-nhóm-auth--xác-thực--phân-quyền)
3. [Nhóm Market — Dữ liệu Thị trường](#3-nhóm-market--dữ-liệu-thị-trường)
4. [Nhóm Forecast — Dự báo & Mô hình](#4-nhóm-forecast--dự-báo--mô-hình)
5. [Nhóm Alerts — Cảnh báo Thị trường](#5-nhóm-alerts--cảnh-báo-thị-trường)
6. [Nhóm Admin — Quản trị Hệ thống](#6-nhóm-admin--quản-trị-hệ-thống)
7. [Nhóm System — Health Check](#7-nhóm-system--health-check)
8. [Phụ lục — Bảng Mã lỗi & Pydantic Schemas](#8-phụ-lục)

---

## 1. Quy ước Chung

### 1.1. Base URL

```
http://localhost:8000/api/v1
```

Tất cả endpoint được khai báo trong `app/api/v1/api.py` với prefix `/api/v1`. Router được nhóm bởi FastAPI `APIRouter` với các tag riêng biệt.

### 1.2. Authentication Header

```http
Authorization: Bearer <access_token>
```

- Token type: **JWT (JSON Web Token)** — thuật toán `HS256`
- Thời hạn: **7 ngày** (10,080 phút) kể từ lúc đăng nhập
- Token scheme: `OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")`
- Payload: `{ "sub": "<user_id>", "role": "<role>", "iat": <unix_ts>, "exp": <unix_ts> }`

### 1.3. Phân quyền (RBAC)

| Role | Quyền hạn |
|------|-----------|
| `admin` | Toàn quyền — CRUD nông sản, quản lý user, trigger tasks, import/export CSV |
| `analyst` | Đọc toàn bộ dữ liệu, export CSV, xem crawler logs, xem model config |
| `user` | Đọc dữ liệu public (overview, forecast, prices) |
| **Public** | Không cần token — endpoint overview, forecast, prices, commodities list |

### 1.4. Cấu trúc Response chuẩn

Tất cả endpoint trả về JSON tuân theo cấu trúc nhất quán. FastAPI tự động validate qua Pydantic v2 schema.

**Thành công:**

```json
{
  "success": true,
  "status_code": 200,
  "message": "Thao tác thành công",
  "data": { ... }
}
```

**Thất bại:**

```json
{
  "success": false,
  "status_code": 404,
  "message": "Không tìm thấy nông sản",
  "data": null
}
```

> **Ghi chú:** Một số endpoint kế thừa trả trực tiếp payload (không bọc trong `success/data`) qua `response_model` Pydantic. Xem Response mẫu cụ thể cho từng endpoint bên dưới.

### 1.5. Bảng HTTP Status Code sử dụng

| Code | Ý nghĩa | Khi nào xảy ra |
|:----:|---------|-----------------|
| `200` | OK | Request thành công |
| `201` | Created | Tạo tài nguyên mới thành công (register, create rule) |
| `400` | Bad Request | Dữ liệu đầu vào không hợp lệ, email trùng |
| `401` | Unauthorized | Thiếu token, token hết hạn, sai credentials |
| `403` | Forbidden | Token hợp lệ nhưng role không đủ quyền |
| `404` | Not Found | Tài nguyên không tồn tại (commodity, user, rule) |
| `422` | Unprocessable Entity | Pydantic validation thất bại (sai kiểu dữ liệu) |
| `429` | Too Many Requests | Vượt quá rate limit (25 req/60s auth, 10 req/60s tasks) |
| `500` | Internal Server Error | Lỗi server không mong muốn |

### 1.6. Rate Limiting

| Scope | Giới hạn | Cơ chế |
|-------|---------|--------|
| **Auth endpoints** (login, register) | 25 requests / 60 giây per IP | Sliding Window in-memory (`RateLimiter`) |
| **Task endpoints** (scrape, retrain) | 10 requests / 60 giây per IP | Sliding Window in-memory (`RateLimiter`) |

---

## 2. Nhóm Auth — Xác thực & Phân quyền

> **Router prefix:** `/api/v1/auth`  
> **Tag:** `Authentication`  
> **Source:** `app/api/v1/endpoints/auth.py`

---

### 2.1. POST `/auth/login`

Xác thực người dùng, kiểm tra trạng thái tài khoản và cấp JWT access token.

| Thuộc tính | Giá trị |
|-----------|---------|
| **Method** | `POST` |
| **Full Path** | `/api/v1/auth/login` |
| **Auth** | Public |
| **Rate Limit** | 25 req / 60s per IP |
| **Content-Type** | `application/json` |

**Request Body:**

```json
{
  "email": "analyst@agroforecast.vn",
  "password": "SecurePass123"
}
```

| Field | Type | Required | Validation |
|-------|------|:--------:|------------|
| `email` | `EmailStr` | ✅ | Phải đúng format email |
| `password` | `str` | ✅ | — |

**Response — 200 OK:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwicm9sZSI6ImFkbWluIiwiaWF0IjoxNzI2MDA0ODAwLCJleHAiOjE3MjY2MDk2MDB9.abc123...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "analyst@agroforecast.vn",
    "full_name": "Nguyễn Văn An",
    "role": "analyst",
    "is_active": true,
    "created_at": "2026-08-15T09:30:00+07:00"
  }
}
```

**Response — 401 Unauthorized:**

```json
{
  "detail": "Email hoặc mật khẩu không chính xác."
}
```

**Response — 403 Forbidden:**

```json
{
  "detail": "Tài khoản này đã bị tạm khóa bởi Quản trị viên. Vui lòng liên hệ để được hỗ trợ."
}
```

**Response — 429 Too Many Requests:**

```json
{
  "detail": "Quá nhiều lần thử đăng nhập. Vui lòng thử lại sau ít phút."
}
```

---

### 2.2. POST `/auth/register`

Tạo tài khoản mới. Mật khẩu được băm bằng `bcrypt.gensalt()` + `bcrypt.hashpw()`. Input text được sanitize qua `sanitize_text()` chống XSS.

| Thuộc tính | Giá trị |
|-----------|---------|
| **Method** | `POST` |
| **Full Path** | `/api/v1/auth/register` |
| **Auth** | Public |
| **Rate Limit** | 25 req / 60s per IP |
| **Response Code** | `201 Created` |

**Request Body:**

```json
{
  "email": "newuser@example.com",
  "full_name": "Trần Thị Bình",
  "password": "MyStr0ngPwd!",
  "role": "analyst"
}
```

| Field | Type | Required | Validation |
|-------|------|:--------:|------------|
| `email` | `EmailStr` | ✅ | Phải là email hợp lệ, unique trong hệ thống |
| `full_name` | `str` | ✅ | `min_length=2`, `max_length=150` |
| `password` | `str` | ✅ | `min_length=6`, `max_length=100` |
| `role` | `str` | ⬜ | Mặc định `"analyst"`. Chấp nhận: `admin`, `analyst`, `user` |

**Response — 201 Created:**

```json
{
  "id": 5,
  "email": "newuser@example.com",
  "full_name": "Trần Thị Bình",
  "role": "analyst",
  "is_active": true,
  "created_at": "2026-09-10T22:00:00+07:00"
}
```

**Response — 400 Bad Request:**

```json
{
  "detail": "Email 'newuser@example.com' đã được đăng ký trong hệ thống."
}
```

**Response — 422 Unprocessable Entity (Pydantic):**

```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "password"],
      "msg": "String should have at least 6 characters",
      "input": "abc"
    }
  ]
}
```

---

### 2.3. GET `/auth/me`

Trả về thông tin profile của user đang đăng nhập dựa trên JWT token.

| Thuộc tính | Giá trị |
|-----------|---------|
| **Method** | `GET` |
| **Full Path** | `/api/v1/auth/me` |
| **Auth** | 🔒 Bearer Token (bất kỳ role) |

**Request Header:**

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

**Response — 200 OK:**

```json
{
  "id": 1,
  "email": "admin@agroforecast.vn",
  "full_name": "Quản trị viên",
  "role": "admin",
  "is_active": true,
  "created_at": "2026-07-20T08:00:00+07:00"
}
```

**Response — 401 Unauthorized:**

```json
{
  "detail": "Chưa xác thực hoặc thiếu Access Token"
}
```

---

## 3. Nhóm Market — Dữ liệu Thị trường

> **Router prefix:** `/api/v1/commodities` + `/api/v1/prices`  
> **Tags:** `Commodities`, `Prices`  
> **Source:** `app/api/v1/endpoints/commodities.py`, `prices.py`

---

### 3.1. GET `/commodities/overview` — Tổng quan giá 4 nông sản

Trả về giá mới nhất, % biến động 7 ngày và sparkline mini-chart cho 4 nông sản.

| Thuộc tính | Giá trị |
|-----------|---------|
| **Method** | `GET` |
| **Full Path** | `/api/v1/commodities/overview` |
| **Auth** | Public |
| **Response Model** | `List[CommodityOverviewCard]` |

**Response — 200 OK:**

```json
[
  {
    "id": 1,
    "code": "RICE",
    "name": "Lúa gạo",
    "category": "Lương thực",
    "unit": "VNĐ/kg",
    "region": "Đồng bằng sông Cửu Long",
    "currentPrice": 7250.0,
    "formattedPrice": "7.250",
    "changePct": 2.1,
    "isPositive": true,
    "sparkline": [
      { "date": "04/09", "value": 7100.0 },
      { "date": "05/09", "value": 7120.0 },
      { "date": "06/09", "value": 7080.0 },
      { "date": "07/09", "value": 7150.0 },
      { "date": "08/09", "value": 7200.0 },
      { "date": "09/09", "value": 7220.0 },
      { "date": "10/09", "value": 7250.0 }
    ]
  },
  {
    "id": 2,
    "code": "COFFEE",
    "name": "Cà phê",
    "category": "Công nghiệp",
    "unit": "VNĐ/kg",
    "region": "Tây Nguyên",
    "currentPrice": 125300.0,
    "formattedPrice": "125.300",
    "changePct": -1.5,
    "isPositive": false,
    "sparkline": [ ... ]
  }
]
```

---

### 3.2. GET `/prices/history` — Lịch sử giá theo chuỗi thời gian

Trả về chuỗi giá hàng ngày sắp xếp theo `record_date` tăng dần cho 1 nông sản.

| Thuộc tính | Giá trị |
|-----------|---------|
| **Method** | `GET` |
| **Full Path** | `/api/v1/prices/history` |
| **Auth** | Public |
| **Response Model** | `List[PriceHistoryResponse]` |

**Query Parameters:**

| Param | Type | Required | Default | Mô tả |
|-------|------|:--------:|:-------:|-------|
| `commodity_id` | `int` | ✅ | — | ID nông sản (1=Lúa, 2=Cà phê, 3=Tiêu, 4=Mía) |
| `days` | `int` | ⬜ | `60` | Số ngày lịch sử cần lấy (giới hạn N bản ghi gần nhất) |

**Request:**

```http
GET /api/v1/prices/history?commodity_id=2&days=30
```

**Response — 200 OK:**

```json
[
  {
    "commodity_id": 2,
    "record_date": "2026-08-12",
    "price": 123500.0,
    "price_min": 122000.0,
    "price_max": 125000.0,
    "volume": 1850.0,
    "source": "Sở NN&PTNT / Hiệp hội Nông sản",
    "id": 4521
  },
  {
    "commodity_id": 2,
    "record_date": "2026-08-13",
    "price": 124200.0,
    "price_min": 122800.0,
    "price_max": 125600.0,
    "volume": 2100.0,
    "source": "Sở NN&PTNT / Hiệp hội Nông sản",
    "id": 4522
  }
]
```

---

### 3.3. GET `/commodities/comparison` — Biểu đồ tương quan tăng trưởng

Trả về chuỗi % thay đổi chuẩn hóa của 4 nông sản so với giá đầu kỳ (90 ngày gần nhất, lấy mẫu ~9 mốc).

| Thuộc tính | Giá trị |
|-----------|---------|
| **Method** | `GET` |
| **Full Path** | `/api/v1/commodities/comparison` |
| **Auth** | Public |
| **Response Model** | `List[MarketComparisonPoint]` |

**Response — 200 OK:**

```json
[
  { "date": "15/06", "rice": 0.0,  "coffee": 0.0,  "pepper": 0.0,  "sugar": 0.0  },
  { "date": "27/06", "rice": 1.2,  "coffee": -0.8, "pepper": 2.5,  "sugar": 0.3  },
  { "date": "10/07", "rice": 2.8,  "coffee": 1.5,  "pepper": 3.1,  "sugar": -0.5 },
  { "date": "25/07", "rice": 3.5,  "coffee": 4.2,  "pepper": 1.8,  "sugar": 1.2  },
  { "date": "08/08", "rice": 2.1,  "coffee": 5.8,  "pepper": -1.2, "sugar": 2.0  },
  { "date": "22/08", "rice": 4.0,  "coffee": 3.6,  "pepper": 0.5,  "sugar": 3.1  },
  { "date": "05/09", "rice": 3.2,  "coffee": 2.9,  "pepper": 1.0,  "sugar": 2.8  },
  { "date": "10/09", "rice": 5.1,  "coffee": 1.2,  "pepper": 2.3,  "sugar": 3.5  }
]
```

---

### 3.4. GET `/commodities/spotlight` — Tiêu điểm nông sản

Trả về thông tin tiêu điểm 1 nông sản: giá hiện tại, biến động 3 tháng, giá đỉnh, chuỗi xu hướng 7 điểm.

| Thuộc tính | Giá trị |
|-----------|---------|
| **Method** | `GET` |
| **Full Path** | `/api/v1/commodities/spotlight` |
| **Auth** | Public |

**Query Parameters:**

| Param | Type | Required | Default | Mô tả |
|-------|------|:--------:|:-------:|-------|
| `code` | `str` | ⬜ | `"COFFEE_ROBUSTA"` | Mã nông sản trong DB |

**Response — 200 OK:**

```json
{
  "commodityCode": "COFFEE",
  "commodityName": "Cà phê Robusta Đắk Lắk",
  "subtitle": "Xu hướng 3 tháng từ Database",
  "currentPrice": "125.300 VNĐ/kg",
  "change3Months": "+8.5%",
  "peakPrice": "132.000 VNĐ/kg",
  "trendData": [
    { "date": "12/06", "value": 115500.0 },
    { "date": "02/07", "value": 118200.0 },
    { "date": "22/07", "value": 122000.0 },
    { "date": "11/08", "value": 126500.0 },
    { "date": "31/08", "value": 124800.0 },
    { "date": "10/09", "value": 125300.0 }
  ]
}
```

---

### 3.5. GET `/commodities/regional-prices` — Bảng giá vùng miền

Trả về bảng giá thị trường mới nhất của tất cả nông sản kèm khu vực, biên độ min–max, sản lượng.

| Thuộc tính | Giá trị |
|-----------|---------|
| **Method** | `GET` |
| **Full Path** | `/api/v1/commodities/regional-prices` |
| **Auth** | Public |

**Response — 200 OK:**

```json
[
  {
    "id": 1,
    "commodityName": "Lúa gạo IR504",
    "code": "RICE",
    "region": "Đồng bằng sông Cửu Long",
    "price": "7.250",
    "unit": "VNĐ/kg",
    "minMax": "7.141 - 7.359",
    "volume": "1.250 tấn",
    "changePct": 2.1,
    "source": "Sở NN&PTNT / Hiệp hội Ngành hàng",
    "updatedAt": "Ngày 10/09/2026"
  },
  {
    "id": 2,
    "commodityName": "Cà phê Robusta Đắk Lắk",
    "code": "COFFEE",
    "region": "Tây Nguyên",
    "price": "125.300",
    "unit": "VNĐ/kg",
    "minMax": "123.421 - 127.179",
    "volume": "2.100 tấn",
    "changePct": -1.5,
    "source": "Sở NN&PTNT / Hiệp hội Ngành hàng",
    "updatedAt": "Ngày 10/09/2026"
  }
]
```

---

### 3.6. GET `/commodities` — Danh sách nông sản

| Thuộc tính | Giá trị |
|-----------|---------|
| **Method** | `GET` |
| **Full Path** | `/api/v1/commodities` |
| **Auth** | Public |

**Response — 200 OK:**

```json
[
  {
    "code": "RICE_IR504",
    "name": "Lúa gạo IR504",
    "category": "Lương thực",
    "unit": "VNĐ/kg",
    "region": "Đồng bằng sông Cửu Long",
    "description": "Giống lúa IR504 chất lượng cao...",
    "id": 1,
    "created_at": "2026-07-20T08:00:00+07:00"
  }
]
```

---

## 4. Nhóm Forecast — Dự báo & Mô hình

> **Router prefix:** `/api/v1/predictions` + `/api/v1/forecast`  
> **Tags:** `Predictions & ML Pipeline`, `Forecast & ML (Legacy)`  
> **Source:** `app/api/v1/endpoints/predictions.py`, `forecast.py`

---

### 4.1. GET `/predictions/forecast` — Dự báo giá realtime

**Endpoint chính** — Gọi `PricePredictor.forecast()` trong realtime, trả về chuỗi dự báo tương lai kèm dải tin cậy 95% và lịch sử gần nhất.

| Thuộc tính | Giá trị |
|-----------|---------|
| **Method** | `GET` |
| **Full Path** | `/api/v1/predictions/forecast` |
| **Auth** | Public |
| **Response Model** | `PredictionForecastResponse` |
| **Cache** | In-Memory (tự động, có thể tắt `use_cache=false`) |

**Query Parameters:**

| Param | Type | Required | Default | Mô tả |
|-------|------|:--------:|:-------:|-------|
| `symbol` | `str` | ⬜ | `None` | Mã nông sản (VD: `COFFEE_ROBUSTA`, `RICE_IR504`, `PEPPER_BLACK`, `SUGARCANE`) |
| `commodity_id` | `int` | ⬜ | `None` | Hoặc ID nông sản (1, 2, 3, 4). Ưu tiên nếu cả 2 có giá trị |
| `model` | `str` | ⬜ | `"LSTM"` | Mô hình: `LSTM`, `XGBoost`, `Prophet`, `ARIMA`, `Random Forest` |
| `days` | `int` | ⬜ | `7` | Số ngày dự báo tương lai. Giới hạn: `1 ≤ days ≤ 60` |
| `include_history` | `int` | ⬜ | `5` | Số điểm lịch sử gần nhất (để vẽ chart liền mạch). `0 ≤ x ≤ 30` |
| `use_cache` | `bool` | ⬜ | `true` | Sử dụng cache (response < 100ms) hoặc force tính toán mới |

**Request:**

```http
GET /api/v1/predictions/forecast?commodity_id=2&model=LSTM&days=7&include_history=5
```

**Response — 200 OK:**

```json
{
  "symbol": "COFFEE_ROBUSTA",
  "commodity": {
    "id": 2,
    "code": "COFFEE_ROBUSTA",
    "name": "Cà phê Robusta Đắk Lắk"
  },
  "model_name": "LSTM",
  "forecast_days": 7,
  "response_time_ms": 42.5,
  "cached": true,
  "metrics": {
    "mae": 3022.16,
    "rmse": 3448.24,
    "mape": 3.17,
    "r2": 0.89
  },
  "history": [
    {
      "date": "2026-09-06",
      "display_date": "06/09",
      "yhat": 124800.0,
      "yhat_lower": 124800.0,
      "yhat_upper": 124800.0,
      "actual_price": 124800.0,
      "is_forecast": false
    },
    {
      "date": "2026-09-10",
      "display_date": "10/09",
      "yhat": 125300.0,
      "yhat_lower": 125300.0,
      "yhat_upper": 125300.0,
      "actual_price": 125300.0,
      "is_forecast": false
    }
  ],
  "forecast": [
    {
      "date": "2026-09-11",
      "display_date": "11/09",
      "yhat": 125950.5,
      "yhat_lower": 119107.2,
      "yhat_upper": 132793.8,
      "actual_price": null,
      "is_forecast": true
    },
    {
      "date": "2026-09-12",
      "display_date": "12/09",
      "yhat": 126420.0,
      "yhat_lower": 119380.1,
      "yhat_upper": 133459.9,
      "actual_price": null,
      "is_forecast": true
    }
  ],
  "all_points": [ "... history + forecast merged ..." ]
}
```

> **Công thức 95% CI:**  
> `lower_ci = ŷ_t − 1.96 × RMSE × √(1 + 0.05t)`  
> `upper_ci = ŷ_t + 1.96 × RMSE × √(1 + 0.05t)`  
> Trong đó `t` là bước dự báo (1, 2, ..., T).

**Response — 404 Not Found:**

```json
{
  "detail": "Không tìm thấy thông tin hàng hóa yêu cầu."
}
```

**Response — 500 Internal Server Error:**

```json
{
  "detail": "Lỗi khi thực hiện dự báo với mô hình LSTM: <chi tiết lỗi>"
}
```

---

### 4.2. GET `/predictions/metrics` — So sánh metrics tất cả mô hình

Trả về chỉ số MAE, RMSE, MAPE, R² của tất cả model đã train cho 1 nông sản, kèm trạng thái kiểm duyệt chất lượng.

| Thuộc tính | Giá trị |
|-----------|---------|
| **Method** | `GET` |
| **Full Path** | `/api/v1/predictions/metrics` |
| **Auth** | Public |
| **Response Model** | `PredictionMetricsResponse` |

**Query Parameters:**

| Param | Type | Required | Default | Mô tả |
|-------|------|:--------:|:-------:|-------|
| `symbol` | `str` | ⬜ | `None` | Mã nông sản |
| `commodity_id` | `int` | ⬜ | `None` | ID nông sản |

**Request:**

```http
GET /api/v1/predictions/metrics?commodity_id=2
```

**Response — 200 OK:**

```json
{
  "symbol": "COFFEE_ROBUSTA",
  "models": [
    {
      "model_name": "LSTM",
      "metrics": {
        "mae": 3022.16,
        "rmse": 3448.24,
        "mape": 3.17,
        "r2": 0.89
      },
      "trained_at": "2026-09-10 09:26:27",
      "passed_threshold": true,
      "threshold_reason": "Passed Quality Check (RMSE/Mean = 5.83%)"
    },
    {
      "model_name": "XGBoost",
      "metrics": {
        "mae": 1523.45,
        "rmse": 2105.67,
        "mape": 1.82,
        "r2": 0.94
      },
      "trained_at": "2026-09-10 09:25:14",
      "passed_threshold": true,
      "threshold_reason": "Passed Quality Check (RMSE/Mean = 3.56%)"
    },
    {
      "model_name": "Prophet",
      "metrics": {
        "mae": 4521.30,
        "rmse": 5890.12,
        "mape": 4.52,
        "r2": 0.78
      },
      "trained_at": "2026-09-10 09:24:50",
      "passed_threshold": true,
      "threshold_reason": "Passed Quality Check"
    }
  ]
}
```

---

### 4.3. GET `/forecast` — Dashboard dự báo (Legacy)

Endpoint gốc phục vụ trang `/forecast` frontend, trả kết hợp historical + forecast points kèm 1 bộ metrics.

| Thuộc tính | Giá trị |
|-----------|---------|
| **Method** | `GET` |
| **Full Path** | `/api/v1/forecast` |
| **Auth** | Public |
| **Response Model** | `ForecastDashboardResponse` |

**Query Parameters:**

| Param | Type | Required | Default | Mô tả |
|-------|------|:--------:|:-------:|-------|
| `commodity_id` | `int` | ⬜ | `2` | ID nông sản (mặc định Cà phê Robusta) |
| `model_name` | `str` | ⬜ | `"LSTM"` | Tên mô hình |
| `days` | `int` | ⬜ | `10` | Số ngày dự báo |

**Response — 200 OK:**

```json
{
  "commodity": {
    "code": "COFFEE_ROBUSTA",
    "name": "Cà phê Robusta Đắk Lắk",
    "category": "Công nghiệp",
    "unit": "VNĐ/kg",
    "region": "Tây Nguyên",
    "description": null,
    "id": 2,
    "created_at": "2026-07-20T08:00:00+07:00"
  },
  "modelName": "LSTM",
  "metrics": {
    "modelName": "LSTM",
    "mae": 420.5,
    "rmse": 610.2,
    "mape": 1.12,
    "r2": 0.942,
    "trainDate": "05/09/2026"
  },
  "forecastData": [
    {
      "date": "08/09",
      "actualPrice": 125300.0,
      "predictedPrice": 125300.0,
      "lowerCI": 125300.0,
      "upperCI": 125300.0,
      "isForecast": false
    },
    {
      "date": "11/09 (T+1)",
      "actualPrice": null,
      "predictedPrice": 126150.5,
      "lowerCI": 124924.3,
      "upperCI": 127376.7,
      "isForecast": true
    },
    {
      "date": "12/09 (T+2)",
      "actualPrice": null,
      "predictedPrice": 126580.0,
      "lowerCI": 125280.8,
      "upperCI": 127879.2,
      "isForecast": true
    }
  ]
}
```

---

### 4.4. GET `/forecast/compare/{commodity_id}` — So sánh 5 mô hình (Legacy)

Trả về metrics bộ 5 mô hình cho 1 nông sản. Nếu DB thiếu dữ liệu thì dùng fallback mặc định.

| Thuộc tính | Giá trị |
|-----------|---------|
| **Method** | `GET` |
| **Full Path** | `/api/v1/forecast/compare/{commodity_id}` |
| **Auth** | Public |
| **Response Model** | `List[ModelMetricsResponse]` |

**Path Parameters:**

| Param | Type | Mô tả |
|-------|------|-------|
| `commodity_id` | `int` | ID nông sản |

**Response — 200 OK:**

```json
[
  { "modelName": "LSTM",          "mae": 420.5,  "rmse": 610.2,  "mape": 1.12, "r2": 0.942, "trainDate": "05/09/2026" },
  { "modelName": "XGBoost",       "mae": 470.8,  "rmse": 680.5,  "mape": 1.25, "r2": 0.925, "trainDate": "05/09/2026" },
  { "modelName": "Random Forest", "mae": 520.4,  "rmse": 730.1,  "mape": 1.48, "r2": 0.890, "trainDate": "05/09/2026" },
  { "modelName": "Prophet",       "mae": 680.2,  "rmse": 890.6,  "mape": 2.10, "r2": 0.840, "trainDate": "05/09/2026" },
  { "modelName": "ARIMA",         "mae": 850.6,  "rmse": 1120.4, "mape": 2.95, "r2": 0.760, "trainDate": "05/09/2026" }
]
```

**Response — 404 Not Found:**

```json
{
  "detail": "Không tìm thấy nông sản"
}
```

---

## 5. Nhóm Alerts — Cảnh báo Thị trường

> **Router prefix:** `/api/v1/alerts`  
> **Tag:** `Alerts`  
> **Source:** `app/api/v1/endpoints/alerts.py`, `app/services/alert_service.py`

---

### 5.1. GET `/alerts` — Danh sách quy tắc cảnh báo

| Thuộc tính | Giá trị |
|-----------|---------|
| **Method** | `GET` |
| **Full Path** | `/api/v1/alerts` |
| **Auth** | Public |
| **Response Model** | `List[AlertRuleResponse]` |

**Response — 200 OK:**

```json
[
  {
    "id": 1,
    "commodity_id": 2,
    "commodity_name": "Cà phê Robusta Đắk Lắk",
    "user_id": null,
    "rule_name": "Cảnh báo cà phê vượt 130K",
    "condition_type": "PRICE_ABOVE",
    "threshold_value": 130000.0,
    "email": "analyst@agroforecast.vn",
    "is_active": true,
    "created_at": "2026-09-01T10:00:00+07:00"
  },
  {
    "id": 2,
    "commodity_id": 1,
    "commodity_name": "Lúa gạo IR504",
    "user_id": null,
    "rule_name": "Cảnh báo lúa giảm 5% trong 7 ngày",
    "condition_type": "PCT_DEC_7D",
    "threshold_value": 5.0,
    "email": "manager@vfa.org.vn",
    "is_active": true,
    "created_at": "2026-09-05T14:30:00+07:00"
  }
]
```

---

### 5.2. POST `/alerts` — Tạo quy tắc cảnh báo mới

| Thuộc tính | Giá trị |
|-----------|---------|
| **Method** | `POST` |
| **Full Path** | `/api/v1/alerts` |
| **Auth** | Public |
| **Response Model** | `AlertRuleResponse` |

**Request Body:**

```json
{
  "commodity_id": 3,
  "rule_name": "Hồ tiêu tăng mạnh 7 ngày",
  "condition_type": "PCT_INC_7D",
  "threshold_value": 10.0,
  "email": "trader@pepper.vn"
}
```

| Field | Type | Required | Mô tả |
|-------|------|:--------:|-------|
| `commodity_id` | `int` | ✅ | ID nông sản cần theo dõi |
| `rule_name` | `str` | ✅ | Tên quy tắc (hiển thị trong email) |
| `condition_type` | `str` | ✅ | Loại điều kiện — xem bảng bên dưới |
| `threshold_value` | `float` | ✅ | Giá trị ngưỡng (VNĐ/kg hoặc %) |
| `email` | `str` | ✅ | Địa chỉ email nhận thông báo |

**Bảng `condition_type`:**

| Giá trị | Ý nghĩa | Ví dụ threshold |
|---------|---------|-----------------|
| `PRICE_ABOVE` | Giá ≥ ngưỡng | `130000.0` (VNĐ/kg) |
| `PRICE_BELOW` | Giá ≤ ngưỡng | `6500.0` (VNĐ/kg) |
| `PCT_INC_7D` | % tăng 7 ngày ≥ ngưỡng | `10.0` (%) |
| `PCT_DEC_7D` | % giảm 7 ngày ≥ ngưỡng (tuyệt đối) | `5.0` (%) |

**Response — 200 OK:**

```json
{
  "id": 5,
  "commodity_id": 3,
  "commodity_name": "Hồ tiêu đen Bình Phước",
  "user_id": null,
  "rule_name": "Hồ tiêu tăng mạnh 7 ngày",
  "condition_type": "PCT_INC_7D",
  "threshold_value": 10.0,
  "email": "trader@pepper.vn",
  "is_active": true,
  "created_at": "2026-09-10T22:00:00+07:00"
}
```

**Response — 404 Not Found:**

```json
{
  "detail": "Không tìm thấy nông sản"
}
```

---

### 5.3. PATCH `/alerts/{rule_id}/toggle` — Bật/Tắt quy tắc

| Thuộc tính | Giá trị |
|-----------|---------|
| **Method** | `PATCH` |
| **Full Path** | `/api/v1/alerts/{rule_id}/toggle` |
| **Auth** | Public |

**Request Body:**

```json
{
  "is_active": false
}
```

**Response — 200 OK:** Trả về `AlertRuleResponse` đã cập nhật `is_active`.

---

### 5.4. DELETE `/alerts/{rule_id}` — Xóa quy tắc

| Thuộc tính | Giá trị |
|-----------|---------|
| **Method** | `DELETE` |
| **Full Path** | `/api/v1/alerts/{rule_id}` |
| **Auth** | Public |

**Response — 200 OK:**

```json
{
  "message": "Đã xóa quy tắc cảnh báo thành công"
}
```

**Response — 404 Not Found:**

```json
{
  "detail": "Không tìm thấy quy tắc cảnh báo"
}
```

---

### 5.5. POST `/alerts/{rule_id}/test` — Gửi email test

Gửi email thử nghiệm cho 1 rule, đồng thời tạo bản ghi `AlertLog`.

| Thuộc tính | Giá trị |
|-----------|---------|
| **Method** | `POST` |
| **Full Path** | `/api/v1/alerts/{rule_id}/test` |
| **Auth** | Public |

**Response — 200 OK:**

```json
{
  "status": "success",
  "message": "Đã gửi cảnh báo thử nghiệm tới trader@pepper.vn thành công!",
  "rule_name": "Hồ tiêu tăng mạnh 7 ngày"
}
```

---

### 5.6. GET `/alerts/logs` — Lịch sử cảnh báo đã kích hoạt

| Thuộc tính | Giá trị |
|-----------|---------|
| **Method** | `GET` |
| **Full Path** | `/api/v1/alerts/logs` |
| **Auth** | Public |

**Query Parameters:**

| Param | Type | Default | Mô tả |
|-------|------|:-------:|-------|
| `limit` | `int` | `30` | Số bản ghi (1–100) |

**Response — 200 OK:**

```json
[
  {
    "id": 42,
    "rule_id": 1,
    "rule_name": "Cảnh báo cà phê vượt 130K",
    "commodity_name": "Cà phê Robusta Đắk Lắk",
    "email": "analyst@agroforecast.vn",
    "triggered_price": 131200.0,
    "message": "Giá [Cà phê Robusta Đắk Lắk] đã vượt ngưỡng 130,000 VNĐ/kg (Hiện tại: 131,200 VNĐ/kg).",
    "status": "SENT",
    "triggered_at": "2026-09-09T06:30:00+07:00"
  }
]
```

---

## 6. Nhóm Admin — Quản trị Hệ thống

> **Router prefix:** `/api/v1/admin`  
> **Tag:** `Admin Management`  
> **Source:** `app/api/v1/endpoints/admin.py` (24,170 bytes — 19 endpoints)  
> **Bảo vệ:** Tất cả endpoint yêu cầu `require_role(["admin"])` trừ khi ghi chú `admin | analyst`

---

### 6.1. GET `/admin/stats` — Thống kê hệ thống

| Thuộc tính | Giá trị |
|-----------|---------|
| **Method** | `GET` |
| **Full Path** | `/api/v1/admin/stats` |
| **Auth** | 🔒 Admin only |
| **Response Model** | `AdminStatsResponse` |

**Response — 200 OK:**

```json
{
  "total_commodities": 4,
  "total_price_records": 2840,
  "total_forecast_records": 560,
  "total_alert_rules": 8,
  "latest_price_date": "2026-09-10",
  "system_status": "ONLINE"
}
```

**Response — 403 Forbidden:**

```json
{
  "detail": "Quyền truy cập bị từ chối! Yêu cầu vai trò: admin (Vai trò hiện tại: analyst)"
}
```

---

### 6.2. POST `/admin/tasks/scrape` — Kích hoạt Scraper

Chạy web scraper trong `BackgroundTasks` để cào giá nông sản mới nhất từ tất cả nguồn dữ liệu.

| Thuộc tính | Giá trị |
|-----------|---------|
| **Method** | `POST` |
| **Full Path** | `/api/v1/admin/tasks/scrape` |
| **Auth** | 🔒 Admin only |
| **Execution** | Asynchronous (BackgroundTasks) |

**Query Parameters:**

| Param | Type | Default | Mô tả |
|-------|------|:-------:|-------|
| `days` | `int` | `30` | Số ngày cần cào/cập nhật (1–1600) |

**Request:**

```http
POST /api/v1/admin/tasks/scrape?days=7
Authorization: Bearer <admin_token>
```

**Response — 200 OK:**

```json
{
  "task_name": "Cào dữ liệu thị trường (Scraper)",
  "status": "RUNNING",
  "message": "Đã kích hoạt tiến trình cào dữ liệu cho 7 ngày gần nhất trong nền.",
  "records_processed": 0,
  "timestamp": "2026-09-10 22:00:30"
}
```

---

### 6.3. POST `/admin/tasks/retrain` — Huấn luyện lại 5 mô hình

Kích hoạt pipeline huấn luyện lại tuần tự: XGBoost/RF → Prophet → ARIMA → LSTM cho 1 hoặc toàn bộ nông sản.

| Thuộc tính | Giá trị |
|-----------|---------|
| **Method** | `POST` |
| **Full Path** | `/api/v1/admin/tasks/retrain` |
| **Auth** | 🔒 Admin only |
| **Execution** | Asynchronous (BackgroundTasks) |

**Query Parameters:**

| Param | Type | Default | Mô tả |
|-------|------|:-------:|-------|
| `commodity_id` | `int` | `None` | ID nông sản (bỏ trống = huấn luyện toàn bộ 4 mặt hàng) |

**Response — 200 OK:**

```json
{
  "task_name": "Huấn luyện lại mô hình AI (Re-train Models)",
  "status": "RUNNING",
  "message": "Đã bắt đầu tiến trình re-train các thuật toán cho tất cả các mặt hàng nông sản.",
  "records_processed": 0,
  "timestamp": "2026-09-10 22:01:15"
}
```

---

### 6.4. POST `/admin/prices` — Thêm/Cập nhật giá thủ công

Thêm mới hoặc cập nhật (upsert) bản ghi giá cho 1 nông sản vào 1 ngày cụ thể. Nếu ngày đã tồn tại → update.

| Thuộc tính | Giá trị |
|-----------|---------|
| **Method** | `POST` |
| **Full Path** | `/api/v1/admin/prices` |
| **Auth** | 🔒 Admin only |
| **Response Model** | `AdminPriceItem` |

**Request Body:**

```json
{
  "commodity_id": 2,
  "record_date": "2026-09-10",
  "price": 125500.0,
  "price_min": 124000.0,
  "price_max": 127000.0,
  "volume": 2200.0,
  "source": "Nhập thủ công bởi Quản trị viên"
}
```

| Field | Type | Required | Default | Mô tả |
|-------|------|:--------:|:-------:|-------|
| `commodity_id` | `int` | ✅ | — | ID nông sản |
| `record_date` | `date` | ✅ | — | Ngày ghi nhận (format: `YYYY-MM-DD`) |
| `price` | `float` | ✅ | — | Giá trung bình (VNĐ/kg) |
| `price_min` | `float` | ⬜ | `price × 0.98` | Giá thấp nhất |
| `price_max` | `float` | ⬜ | `price × 1.02` | Giá cao nhất |
| `volume` | `float` | ⬜ | `0.0` | Khối lượng giao dịch (tấn) |
| `source` | `str` | ⬜ | `"Nhập thủ công bởi Quản trị viên"` | Nguồn dữ liệu |

**Response — 200 OK:**

```json
{
  "id": 2841,
  "commodity_id": 2,
  "commodity_name": "Cà phê Robusta Đắk Lắk",
  "record_date": "2026-09-10",
  "price": 125500.0,
  "price_min": 124000.0,
  "price_max": 127000.0,
  "volume": 2200.0,
  "source": "Nhập thủ công bởi Quản trị viên"
}
```

**Response — 404 Not Found:**

```json
{
  "detail": "Nông sản không tồn tại"
}
```

---

### 6.5. DELETE `/admin/prices/{price_id}` — Xóa bản ghi giá

| Thuộc tính | Giá trị |
|-----------|---------|
| **Method** | `DELETE` |
| **Full Path** | `/api/v1/admin/prices/{price_id}` |
| **Auth** | 🔒 Admin only |

**Response — 200 OK:**

```json
{
  "message": "Đã xóa bản ghi giá thành công"
}
```

---

### 6.6. POST `/admin/prices/import-csv` — Import dữ liệu từ CSV

Upload file CSV chứa dữ liệu giá, hệ thống tự parse columns và upsert vào PostgreSQL.

| Thuộc tính | Giá trị |
|-----------|---------|
| **Method** | `POST` |
| **Full Path** | `/api/v1/admin/prices/import-csv` |
| **Auth** | 🔒 Admin only |
| **Content-Type** | `multipart/form-data` |

**CSV Format mẫu:**

```csv
commodity_code,record_date,price,price_min,price_max,volume,source
COFFEE_ROBUSTA,2026-09-01,124500,123000,126000,1800,Import CSV
COFFEE_ROBUSTA,2026-09-02,125000,123500,126500,1950,Import CSV
```

**Các column headers được chấp nhận:**

| Cột chính | Alias hỗ trợ |
|-----------|--------------|
| `commodity_code` | `code`, `Mã` |
| `commodity_id` | — |
| `record_date` | `date`, `Ngày` |
| `price` | `Giá` |

**Response — 200 OK:**

```json
{
  "message": "Đã xử lý xong file CSV: Thêm mới 28, Cập nhật 2",
  "records_created": 28,
  "records_updated": 2,
  "errors": []
}
```

**Response — 400 Bad Request:**

```json
{
  "detail": "Chỉ chấp nhận file định dạng CSV (.csv)"
}
```

---

### 6.7. GET `/admin/prices/export-csv` — Xuất dữ liệu CSV

Download toàn bộ hoặc filtered lịch sử giá dưới dạng file CSV.

| Thuộc tính | Giá trị |
|-----------|---------|
| **Method** | `GET` |
| **Full Path** | `/api/v1/admin/prices/export-csv` |
| **Auth** | 🔒 Admin \| Analyst |
| **Response** | `StreamingResponse` (text/csv) |

**Query Parameters:**

| Param | Type | Default | Mô tả |
|-------|------|:-------:|-------|
| `commodity_id` | `int` | `None` | Lọc theo ID nông sản (bỏ trống = xuất toàn bộ) |

**Response Header:**

```http
Content-Type: text/csv
Content-Disposition: attachment; filename=commodity_prices_export.csv
```

---

### 6.8. Quản lý User (Admin)

#### GET `/admin/users` — Danh sách user

| Auth | Response |
|------|----------|
| 🔒 Admin | `List[UserResponse]` |

#### POST `/admin/users` — Tạo user mới

| Auth | Request Body |
|------|-------------|
| 🔒 Admin | `{ "email": "...", "full_name": "...", "password": "...", "role": "analyst" }` |

#### PATCH `/admin/users/{user_id}/role` — Đổi role

| Auth | Request Body |
|------|-------------|
| 🔒 Admin | `{ "role": "admin" }` |

**Giá trị role hợp lệ:** `admin`, `analyst`, `user`

**Response — 200 OK:**

```json
{
  "id": 3,
  "email": "user@example.com",
  "full_name": "Lê Văn Cường",
  "role": "admin",
  "is_active": true,
  "created_at": "2026-08-20T10:00:00+07:00"
}
```

#### PATCH `/admin/users/{user_id}/toggle-status` — Khóa/Mở tài khoản

| Auth | Logic |
|------|-------|
| 🔒 Admin | Toggle `role` thêm/xóa suffix `_disabled`. Không cho phép admin tự khóa. |

**Response — 200 OK:**

```json
{
  "message": "Đã khóa tài khoản thành công",
  "user_id": 3,
  "current_role": "analyst_disabled"
}
```

**Response — 400 Bad Request:**

```json
{
  "detail": "Không thể tự khóa tài khoản quản trị viên hiện tại"
}
```

---

### 6.9. GET `/admin/models/active` — Model mặc định hiện tại

| Thuộc tính | Giá trị |
|-----------|---------|
| **Auth** | 🔒 Admin \| Analyst |

**Response — 200 OK:**

```json
{
  "active_model": "LSTM",
  "description": "Mô hình Mạng Nơ-ron hồi quy LSTM 2 lớp",
  "updated_at": "2026-09-10 22:00:00"
}
```

### 6.10. POST `/admin/models/active` — Chuyển model mặc định

| Auth | Request Body |
|------|-------------|
| 🔒 Admin | `{ "active_model": "XGBoost" }` |

**Response — 200 OK:**

```json
{
  "active_model": "XGBOOST",
  "description": "Mô hình XGBoost đã được kích hoạt làm mặc định",
  "updated_at": "2026-09-10 22:01:00"
}
```

---

## 7. Nhóm System — Health Check

> **Source:** `app/main.py`  
> **Prefix:** Không có prefix `/api/v1` — đặt tại root

---

### 7.1. GET `/` — Thông tin API

| Auth | Public |
|------|--------|

**Response — 200 OK:**

```json
{
  "status": "online",
  "service": "AgroForecast - Hệ thống Dự báo Giá Nông sản",
  "version": "2.4.1",
  "docs": "/docs",
  "api_v1": "/api/v1"
}
```

### 7.2. GET `/health` — Health Check

Kiểm tra sức khỏe hệ thống và kết nối PostgreSQL.

| Auth | Public |
|------|--------|

**Response — 200 OK (healthy):**

```json
{
  "status": "healthy",
  "database": "connected",
  "version": "2.4.1",
  "timestamp": "CURRENT_TIMESTAMP"
}
```

**Response — 200 OK (degraded):**

```json
{
  "status": "degraded",
  "database": "unhealthy: connection refused",
  "version": "2.4.1",
  "timestamp": "CURRENT_TIMESTAMP"
}
```

---

## 8. Phụ lục

### 8.1. Tổng hợp Endpoint Map

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    AGROFORECAST API ENDPOINT MAP                         │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  🌐 PUBLIC (Không cần token)                                            │
│  ├── GET  /                                       System info           │
│  ├── GET  /health                                 Health check          │
│  ├── GET  /api/v1/commodities                     List nông sản         │
│  ├── GET  /api/v1/commodities/overview            4 thẻ tổng quan       │
│  ├── GET  /api/v1/commodities/comparison          Chart tương quan      │
│  ├── GET  /api/v1/commodities/spotlight           Tiêu điểm             │
│  ├── GET  /api/v1/commodities/regional-prices     Bảng giá vùng        │
│  ├── GET  /api/v1/prices/history                  Lịch sử giá          │
│  ├── GET  /api/v1/forecast                        Dashboard dự báo     │
│  ├── GET  /api/v1/forecast/compare/{id}           So sánh 5 model      │
│  ├── GET  /api/v1/predictions/forecast            Dự báo realtime      │
│  ├── GET  /api/v1/predictions/metrics             Metrics tất cả model │
│  ├── GET  /api/v1/alerts                          List alert rules     │
│  ├── POST /api/v1/alerts                          Tạo alert rule       │
│  ├── PATCH/api/v1/alerts/{id}/toggle              Toggle on/off        │
│  ├── DELETE /api/v1/alerts/{id}                   Xóa rule             │
│  ├── POST /api/v1/alerts/{id}/test                Test email           │
│  ├── GET  /api/v1/alerts/logs                     Lịch sử cảnh báo    │
│  ├── POST /api/v1/auth/login                      Đăng nhập            │
│  └── POST /api/v1/auth/register                   Đăng ký              │
│                                                                          │
│  🔒 BEARER TOKEN (Bất kỳ role đã đăng nhập)                            │
│  ├── GET  /api/v1/auth/me                         Profile              │
│  └── POST /api/v1/predictions/retrain             Retrain models       │
│                                                                          │
│  🛡️ ADMIN ONLY (role = "admin")                                        │
│  ├── GET  /api/v1/admin/stats                     Thống kê hệ thống   │
│  ├── GET  /api/v1/admin/commodities               List nông sản        │
│  ├── POST /api/v1/admin/commodities               Tạo nông sản        │
│  ├── PUT  /api/v1/admin/commodities/{id}          Sửa nông sản        │
│  ├── DELETE /api/v1/admin/commodities/{id}        Xóa nông sản        │
│  ├── GET  /api/v1/admin/prices/recent             Giá gần nhất        │
│  ├── POST /api/v1/admin/prices                    Thêm/Sửa giá        │
│  ├── DELETE /api/v1/admin/prices/{id}             Xóa giá             │
│  ├── POST /api/v1/admin/prices/import-csv         Import CSV           │
│  ├── POST /api/v1/admin/tasks/scrape              Trigger scraper      │
│  ├── POST /api/v1/admin/tasks/retrain             Trigger retrain      │
│  ├── GET  /api/v1/admin/users                     List users           │
│  ├── POST /api/v1/admin/users                     Tạo user             │
│  ├── PATCH/api/v1/admin/users/{id}/role           Đổi role             │
│  ├── PATCH/api/v1/admin/users/{id}/toggle-status  Khóa/Mở             │
│  └── POST /api/v1/admin/models/active             Chuyển model         │
│                                                                          │
│  🔓 ADMIN | ANALYST                                                     │
│  ├── GET  /api/v1/admin/prices/export-csv         Export CSV           │
│  ├── GET  /api/v1/admin/logs/crawler              Nhật ký crawler      │
│  └── GET  /api/v1/admin/models/active             Model hiện tại       │
│                                                                          │
│  Tổng: 42 endpoints                                                     │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

### 8.2. Pydantic Schema Reference

| Schema Name | Module | Mục đích |
|-------------|--------|---------|
| `LoginRequest` | `schemas.py` | Body đăng nhập |
| `RegisterRequest` | `schemas.py` | Body đăng ký (email, full_name, password, role) |
| `TokenResponse` | `schemas.py` | Response login (access_token + user) |
| `UserResponse` | `schemas.py` | Thông tin user (id, email, full_name, role, is_active) |
| `CommodityResponse` | `schemas.py` | Nông sản cơ bản |
| `CommodityOverviewCard` | `schemas.py` | Thẻ overview + sparkline + changePct |
| `MarketComparisonPoint` | `schemas.py` | Điểm so sánh 4 nông sản (% chuẩn hóa) |
| `SpotlightSummaryResponse` | `schemas.py` | Tiêu điểm nông sản (trendData 7 điểm) |
| `RegionalPriceResponse` | `schemas.py` | Bảng giá vùng miền |
| `PriceHistoryResponse` | `schemas.py` | Lịch sử giá 1 bản ghi |
| `ForecastDashboardResponse` | `schemas.py` | Response dashboard (commodity + metrics + forecastData) |
| `ForecastPointResponse` | `schemas.py` | 1 điểm forecast (actualPrice, predictedPrice, CI) |
| `ModelMetricsResponse` | `schemas.py` | Metrics 1 model (mae, rmse, mape, r2) |
| `PredictionForecastResponse` | `schemas.py` | Response predict realtime (history + forecast + metrics) |
| `PredictionMetricsResponse` | `schemas.py` | Metrics tất cả model cho 1 commodity |
| `PredictionModelMetric` | `schemas.py` | Metrics 1 model + trạng thái quality check |
| `AlertRuleCreate` | `schemas.py` | Body tạo alert rule |
| `AlertRuleResponse` | `schemas.py` | Response alert rule + commodity_name |
| `AlertLogResponse` | `schemas.py` | Lịch sử cảnh báo đã gửi |
| `AdminStatsResponse` | `schemas.py` | Thống kê hệ thống |
| `PriceCreateManual` | `schemas.py` | Body nhập giá thủ công |
| `AdminPriceItem` | `schemas.py` | Response bản ghi giá (admin view) |
| `TaskRunResponse` | `schemas.py` | Response async task (scrape/retrain) |
| `CSVImportResponse` | `schemas.py` | Kết quả import CSV |
| `ActiveModelSetting` | `schemas.py` | Cấu hình model mặc định |

### 8.3. cURL Cheat Sheet

```bash
# 1. Đăng nhập
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@agroforecast.vn","password":"admin123"}'

# 2. Lấy tổng quan 4 nông sản
curl http://localhost:8000/api/v1/commodities/overview

# 3. Dự báo cà phê 7 ngày bằng LSTM
curl "http://localhost:8000/api/v1/predictions/forecast?commodity_id=2&model=LSTM&days=7"

# 4. So sánh 5 mô hình cho cà phê
curl http://localhost:8000/api/v1/forecast/compare/2

# 5. Metrics tất cả model cho lúa gạo
curl "http://localhost:8000/api/v1/predictions/metrics?commodity_id=1"

# 6. Tạo cảnh báo
curl -X POST http://localhost:8000/api/v1/alerts \
  -H "Content-Type: application/json" \
  -d '{"commodity_id":2,"rule_name":"Coffee > 130K","condition_type":"PRICE_ABOVE","threshold_value":130000,"email":"me@mail.com"}'

# 7. Trigger scraper (cần admin token)
curl -X POST "http://localhost:8000/api/v1/admin/tasks/scrape?days=7" \
  -H "Authorization: Bearer <admin_token>"

# 8. Trigger retrain toàn bộ (cần admin token)
curl -X POST http://localhost:8000/api/v1/admin/tasks/retrain \
  -H "Authorization: Bearer <admin_token>"

# 9. Nhập giá thủ công (cần admin token)
curl -X POST http://localhost:8000/api/v1/admin/prices \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{"commodity_id":2,"record_date":"2026-09-10","price":125500}'

# 10. Health check
curl http://localhost:8000/health
```

---

> **📝 Tài liệu này được tạo tự động từ mã nguồn thực tế** trong `app/api/v1/endpoints/`, `app/schemas/schemas.py` và `app/services/`.  
> Swagger UI tương tác: [http://localhost:8000/docs](http://localhost:8000/docs)  
> Đọc kèm: [`REQUIREMENTS_PLAN.md`](file:///d:/DA_TN/docs/REQUIREMENTS_PLAN.md) | [`PROJECT_TRACKER.md`](file:///d:/DA_TN/docs/PROJECT_TRACKER.md)

---

*AgroForecast API Reference v2.4.1 — Đồ án Tốt nghiệp 2026*
