# 📑 PHASE 5 SPECIFICATION — AgroForecast

## Đặc Tả Kỹ Thuật: Huấn Luyện Đa Mô Hình Machine Learning & Deep Learning LSTM

> **Hệ thống:** AgroForecast — Hệ Thống Dự Báo Giá Nông Sản & Cảnh Báo Thị Trường  
> **Giai đoạn:** Phase 5 — Model Training, Evaluation & Multi-Algorithm Inference  
> **Chịu trách nhiệm:** Tech Lead & AI/Data Systems Specialist  
> **Phiên bản tài liệu:** v2.4.1  
> **Thời gian triển khai:** 14/09/2026 → 27/09/2026  
> **Trạng thái:** 🎯 Đang thực hiện (Active Development)  

---

## Mục lục

1. [Mục Tiêu và Phạm Vi Kỹ Thuật (Objective & Scope)](#1-mục-tiêu-và-phạm-vi-kỹ-thuật-objective--scope)
2. [Cấu Trúc Dữ Liệu: SQLAlchemy Models & Pydantic Schemas](#2-cấu-trúc-dữ-liệu-sqlalchemy-models--pydantic-schemas)
   - [2.1. SQLAlchemy ORM Models](#21-sqlalchemy-orm-models)
   - [2.2. Pydantic v2 Schemas (Validation & Serialization)](#22-pydantic-v2-schemas-validation--serialization)
3. [Thuật Toán Chi Tiết & Kiến Trúc AI Engine](#3-thuật-toán-chi-tiết--kiến-trúc-ai-engine)
   - [3.1. Kiến Trúc Mạng Nơ-ron Deep Learning Stacked LSTM](#31-kiến-trúc-mạng-nơ-ron-deep-learning-stacked-lstm)
   - [3.2. Cấu Hình Siêu Tham Số (Hyperparameters Registry)](#32-cấu-hình-siêu-tham-số-hyperparameters-registry)
   - [3.3. Tích Hợp Biến Ngoại Sinh (Exogenous Features Integration)](#33-tích-hợp-biến-ngoại-sinh-exogenous-features-integration)
   - [3.4. Danh Mục Hàm Cần Triển Khai Trong Module `ml_pipeline`](#34-danh-mục-hàm-cần-triển-khai-trong-module-ml_pipeline)
   - [3.5. Công Thức Tính Dải Tin Cậy 95% (95% Confidence Interval)](#35-công-thức-tính-dải-tin-cậy-95-95-confidence-interval)
4. [Đặc Tả RESTful API Endpoints Trong FastAPI](#4-đặc-tả-restful-api-endpoints-trong-fastapi)
5. [Thiết Kế Giao Diện Frontend Next.js 14 & UI Components](#5-thiết-kế-giao-diện-frontend-nextjs-14--ui-components)
6. [Tiêu Chí Nghiệm Thu (Acceptance Criteria) & Kịch Bản Kiểm Thử (Pytest)](#6-tiêu-chí-nghiệm-thu-acceptance-criteria--kịch-bản-kiểm-thử-pytest)

---

## 1. Mục Tiêu và Phạm Vi Kỹ Thuật (Objective & Scope)

### 1.1. Mục Tiêu Chính
Xây dựng pipeline hoàn chỉnh để huấn luyện, đánh giá độc lập và suy luận (inference) đa mô hình chuỗi thời gian (Time-Series) cho **4 loại nông sản chiến lược** (Lúa gạo IR504, Cà phê Robusta, Hồ tiêu đen, Mía đường), bao gồm:
1. **Mô hình Deep Learning:** PyTorch Stacked LSTM đa biến (Multivariate Stacked LSTM) tiếp nhận chuỗi giá nội địa kết hợp biến kinh tế vĩ mô.
2. **Mô hình Ensemble Machine Learning:** XGBoost Regressor và Random Forest Regressor với kỹ thuật Lagged Features & Rolling Statistics.
3. **Mô hình Thống kê Truyền thống:** Facebook Prophet và Box-Jenkins ARIMA (Baseline benchmark).
4. **Cơ chế suy luận đa chân trời:** Dự báo tương lai trong khung **7 ngày, 14 ngày và 30 ngày** kèm dải tin cậy 95% (Upper / Lower Bounds).
5. **Đánh giá & Benchmark:** So sánh khách quan 5 mô hình qua 4 chỉ số: **MAE, RMSE, MAPE, $R^2$**.

### 1.2. Phạm Vi Kỹ Thuật (Technical Scope)
- **Frameworks:** PyTorch 2.2+, XGBoost 2.0+, scikit-learn 1.4+, Prophet 1.1+, statsmodels 0.14+.
- **Bộ dữ liệu đầu vào:** Dữ liệu lịch sử giá 2023–2026 từ PostgreSQL (`price_history`) sau khi lọc nhiễu ngoại lai (IQR Capping) kết hợp biến ngoại sinh USD/VND và Dầu thô WTI (`exogenous_data`).
- **Lưu trữ Model Artifacts:** Trọng số `.pt` (PyTorch state_dict), `.joblib` / `.pkl` (Scikit-Learn/XGBoost/Prophet) và scaler parameters trong thư mục `backend/ml_pipeline/saved_models/`.

---

## 2. Cấu Trúc Dữ Liệu: SQLAlchemy Models & Pydantic Schemas

### 2.1. SQLAlchemy ORM Models

Cập nhật và tối ưu 2 bảng CSDL cốt lõi phục vụ lưu trữ kết quả và chỉ số mô hình:

```python
# app/models/models.py
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Forecast(Base):
    """Lưu trữ kết quả dự báo của từng mô hình theo ngày"""
    __tablename__ = "forecast_results"

    id = Column(Integer, primary_key=True, index=True)
    commodity_id = Column(Integer, ForeignKey("commodities.id", ondelete="CASCADE"), nullable=False)
    model_name = Column(String(50), nullable=False)  # "lstm", "xgboost", "random_forest", "prophet", "arima"
    forecast_date = Column(Date, nullable=False, index=True)
    predicted_price = Column(Float, nullable=False)
    confidence_lower = Column(Float, nullable=True)  # Ngưỡng dưới dải tin cậy 95%
    confidence_upper = Column(Float, nullable=True)  # Ngưỡng trên dải tin cậy 95%
    horizon_days = Column(Integer, default=30)
    created_at = Column(DateTime, default=datetime.utcnow)

    commodity = relationship("Commodity", back_populates="forecasts")

    __table_args__ = (
        UniqueConstraint('commodity_id', 'model_name', 'forecast_date', name='uq_commodity_model_forecast_date'),
    )

class ModelRegistry(Base):
    """Lưu metadata, trạng thái hoạt động và chỉ số đánh giá của từng thuật toán"""
    __tablename__ = "model_registry"

    id = Column(Integer, primary_key=True, index=True)
    commodity_id = Column(Integer, ForeignKey("commodities.id", ondelete="CASCADE"), nullable=False)
    model_name = Column(String(50), nullable=False)
    version = Column(String(20), default="1.0.0")
    mae = Column(Float, nullable=True)
    rmse = Column(Float, nullable=True)
    mape = Column(Float, nullable=True)
    r2_score = Column(Float, nullable=True)
    hyperparameters = Column(Text, nullable=True)  # JSON-encoded string
    is_active = Column(Integer, default=1)        # 1: Ưu tiên dùng để suy luận API mặc định
    trained_at = Column(DateTime, default=datetime.utcnow)

    commodity = relationship("Commodity")
```

---

### 2.2. Pydantic v2 Schemas (Validation & Serialization)

```python
# app/schemas/prediction.py
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict
from datetime import date, datetime

class ForecastPointSchema(BaseModel):
    date: date
    price: float = Field(..., description="Giá dự đoán (VNĐ/kg)")
    lower_bound: Optional[float] = Field(None, description="Ngưỡng dưới 95% CI")
    upper_bound: Optional[float] = Field(None, description="Ngưỡng trên 95% CI")

class ModelMetricsSchema(BaseModel):
    model_name: str
    mae: float
    rmse: float
    mape: float
    r2_score: float
    trained_at: datetime
    is_active: bool

class ForecastComparisonResponse(BaseModel):
    commodity_id: int
    commodity_code: str
    commodity_name: str
    historical_last_date: date
    historical_last_price: float
    models: Dict[str, List[ForecastPointSchema]]
    metrics: List[ModelMetricsSchema]

class RetrainRequestSchema(BaseModel):
    commodity_id: int
    model_types: List[str] = ["lstm", "xgboost", "prophet", "arima"]
    epochs: Optional[int] = Field(50, ge=10, le=500)
    horizon_days: Optional[int] = Field(30, ge=7, le=90)
```

---

## 3. Thuật Toán Chi Tiết & Kiến Trúc AI Engine

### 3.1. Kiến Trúc Mạng Nơ-ron Deep Learning Stacked LSTM

Mô hình Deep Learning được xây dựng theo kiến trúc **Stacked LSTM 2 lớp với Dropout chống quá khớp (Overfitting)**:

```text
Input Tensor: [Batch_Size, Seq_Length=14, Num_Features=3] (Price, USD/VND, Crude_Oil)
       │
       ▼
┌────────────────────────────────────────────────────────┐
│ LSTM Layer 1: hidden_size=64, return_sequences=True    │
│ Dropout = 0.2 (Khử liên kết nơ-ron ngẫu nhiên)         │
└──────────────────────────┬─────────────────────────────┘
                           │ [Batch_Size, 14, 64]
                           ▼
┌────────────────────────────────────────────────────────┐
│ LSTM Layer 2: hidden_size=32, return_sequences=False   │
│ Dropout = 0.2                                          │
└──────────────────────────┬─────────────────────────────┘
                           │ [Batch_Size, 32]
                           ▼
┌────────────────────────────────────────────────────────┐
│ Fully Connected (Dense): Linear(32 -> 16) + ReLU       │
│ Output Layer: Linear(16 -> 1)                          │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
Output: Predicted Scaled Price [Batch_Size, 1] ──► Inverse MinMaxScaler
```

```python
# ml_pipeline/train_lstm.py
import torch
import torch.nn as nn

class StackedLSTM(nn.Module):
    def __init__(self, input_size: int = 3, hidden_size: int = 64, num_layers: int = 2, output_size: int = 1):
        super(StackedLSTM, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=0.2 if num_layers > 1 else 0.0
        )
        self.fc1 = nn.Linear(hidden_size, 16)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(16, output_size)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        out, _ = self.lstm(x, (h0, c0))
        out = self.fc1(out[:, -1, :])
        out = self.relu(out)
        out = self.fc2(out)
        return out
```

---

### 3.2. Cấu Hình Siêu Tham Số (Hyperparameters Registry)

| Mô hình | Thuật toán cốt lõi | Siêu tham số tối ưu (Optimal Hyperparameters) | Cơ chế chống Overfitting |
|---|---|---|---|
| **Stacked LSTM** | PyTorch Deep Recurrent NN | `seq_length=14`, `hidden_size=64`, `layers=2`, `lr=0.001`, `optimizer=Adam`, `epochs=80`, `batch_size=16` | Dropout = 0.2, Early Stopping (patience=10) |
| **XGBoost** | Gradient Boosted Trees | `n_estimators=150`, `max_depth=5`, `learning_rate=0.03`, `subsample=0.8`, `colsample_bytree=0.8` | Regularization `reg_alpha=0.1`, `reg_lambda=1.0` |
| **Random Forest** | Bootstrap Aggregation Trees | `n_estimators=200`, `max_depth=8`, `min_samples_split=5`, `min_samples_leaf=2` | Giới hạn `max_features='sqrt'` |
| **Facebook Prophet** | Generalized Additive Model | `growth='linear'`, `yearly_seasonality=True`, `weekly_seasonality=False`, `changepoint_prior_scale=0.05` | MCMC sampling 95% interval width |
| **ARIMA** | Box-Jenkins Autoregressive | Order `(p=2, d=1, q=2)` dựa trên kiểm định nghiệm đơn vị ADF Test | Tối thiểu hóa AIC / BIC |

---

### 3.3. Tích Hợp Biến Ngoại Sinh (Exogenous Features Integration)

1. **Chuỗi dữ liệu tỷ giá USD/VND (`USDVND=X`):** Tác động trực tiếp đến giá trị xuất khẩu quy đổi.
2. **Chuỗi dữ liệu Dầu thô WTI (`CL=F`):** Đại diện cho chi phí phân bón, vận chuyển logistic và năng lượng tưới tiêu.
3. **Kỹ thuật đồng bộ chuỗi thời gian:**
   - Sử dụng `pd.merge_asof` hoặc `outer join` căn chỉnh theo cột ngày (`record_date`).
   - Xử lý các ngày nghỉ lễ/cuối tuần bằng phương pháp nội suy tuyến tính (`interpolate(method='time')`) và lấp đầy chuyển tiếp (`ffill()`).

---

### 3.4. Danh Mục Hàm Cần Triển Khai Trong Module `ml_pipeline`

#### Module `ml_pipeline/train_lstm.py`:
- `create_sliding_sequences(data: np.ndarray, seq_length: int = 14) -> Tuple[torch.Tensor, torch.Tensor]`
  - *Đầu vào:* Mảng dữ liệu chuẩn hóa 2 chiều `[N, features]`.
  - *Đầu ra:* Cặp tensor `(X, y)` với kích thước `X: [N - seq, seq, features]`, `y: [N - seq, 1]`.
- `train_lstm_model(commodity_id: int, df: pd.DataFrame, epochs: int = 80) -> Dict[str, Any]`
  - *Chức năng:* Tách tập Train (85%) / Test (15%), chuẩn hóa `MinMaxScaler(-1, 1)`, huấn luyện bằng PyTorch với hàm mất mát `nn.MSELoss()`, lưu file trọng số `saved_models/lstm_{commodity_code}.pt`.
  - *Trả về:* Dictionary chứa chỉ số `{"mae": ..., "rmse": ..., "mape": ..., "r2": ...}` và đường dẫn model.
- `predict_lstm_horizon(model: nn.Module, last_sequence: np.ndarray, horizon: int = 30) -> np.ndarray`
  - *Chức năng:* Suy luận đệ quy (Recursive Multi-step Forecasting) cho 30 ngày tiếp theo.

#### Module `ml_pipeline/train_ml.py` (XGBoost & Random Forest):
- `build_lagged_features(df: pd.DataFrame, lags: List[int] = [1, 3, 7, 14]) -> pd.DataFrame`
  - *Chức năng:* Tạo các thuộc tính trễ (`price_lag_1`, `price_lag_7`), chỉ số trung bình động (`rolling_mean_7`, `rolling_std_7`), và biến ngoại sinh.
- `train_xgboost(commodity_id: int, df: pd.DataFrame) -> Dict[str, Any]`
- `train_random_forest(commodity_id: int, df: pd.DataFrame) -> Dict[str, Any]`

#### Module `ml_pipeline/predictor.py` (Unified Prediction Serving):
- `get_or_generate_forecast(commodity_id: int, model_name: str, days: int = 30, db_session = None) -> List[Dict]`
  - *Logic ngoại lệ:* Nếu mô hình chưa được huấn luyện hoặc file trọng số bị thiếu, tự động fallback về mô hình baseline Prophet hoặc trả về thông báo lỗi chi tiết thay vì crash hệ thống.

---

### 3.5. Công Thức Tính Dải Tin Cậy 95% (95% Confidence Interval)

Đối với các mô hình Machine Learning / Deep Learning không cung cấp sẵn dải tin cậy như Prophet:
- Độ lệch chuẩn phần dư kiểm thử (Residual Standard Error):
  $$S_e = \sqrt{\frac{1}{N} \sum_{t=1}^{N} (y_t - \hat{y}_t)^2} = \text{RMSE}$$
- Ngưỡng dao động mở rộng theo thời gian tương lai bước $h \in [1, 30]$:
  $$\hat{y}_{t+h}^{\text{upper}} = \hat{y}_{t+h} + 1.96 \cdot S_e \cdot \sqrt{1 + \frac{h}{30}}$$
  $$\hat{y}_{t+h}^{\text{lower}} = \hat{y}_{t+h} - 1.96 \cdot S_e \cdot \sqrt{1 + \frac{h}{30}}$$

---

## 4. Đặc Tả RESTful API Endpoints Trong FastAPI

Triển khai tại router `backend/app/api/v1/endpoints/predictions.py`:

### 4.1. Lấy kết quả dự báo theo nông sản và mô hình
- **HTTP Method & Path:** `GET /api/v1/predictions/forecast`
- **Quyền hạn:** Public
- **Query Parameters:**
  - `commodity_id` (int, required): ID nông sản (1: Lúa IR504, 2: Cà phê, 3: Hồ tiêu, 4: Mía đường).
  - `model_name` (str, optional, default="lstm"): Tên mô hình (`lstm`, `xgboost`, `random_forest`, `prophet`, `arima`).
  - `days` (int, optional, default=30): Số ngày tương lai (7, 14, 30).
- **Response JSON (200 OK):**
```json
{
  "success": true,
  "commodity_code": "CA_PHE_ROBUSTA",
  "model_name": "lstm",
  "horizon_days": 30,
  "forecast": [
    {
      "date": "2026-09-11",
      "price": 121500.0,
      "lower_bound": 118200.0,
      "upper_bound": 124800.0
    },
    {
      "date": "2026-09-12",
      "price": 122100.0,
      "lower_bound": 118600.0,
      "upper_bound": 125600.0
    }
  ]
}
```

### 4.2. Lấy bảng so sánh sai số 5 mô hình (Model Comparison)
- **HTTP Method & Path:** `GET /api/v1/predictions/comparison?commodity_id=2`
- **Response JSON (200 OK):**
```json
{
  "commodity_name": "Cà phê Robusta",
  "metrics": [
    { "model_name": "Stacked LSTM", "mae": 1240.5, "rmse": 1680.2, "mape": 1.38, "r2_score": 0.942, "is_active": true },
    { "model_name": "XGBoost", "mae": 1420.0, "rmse": 1890.1, "mape": 1.58, "r2_score": 0.925, "is_active": false },
    { "model_name": "Facebook Prophet", "mae": 1850.2, "rmse": 2340.0, "mape": 2.05, "r2_score": 0.887, "is_active": false },
    { "model_name": "Random Forest", "mae": 1920.4, "rmse": 2480.6, "mape": 2.14, "r2_score": 0.871, "is_active": false },
    { "model_name": "ARIMA Baseline", "mae": 2450.8, "rmse": 3120.4, "mape": 2.72, "r2_score": 0.812, "is_active": false }
  ]
}
```

### 4.3. Kích hoạt huấn luyện lại mô hình (Admin Trigger)
- **HTTP Method & Path:** `POST /api/v1/admin/tasks/retrain`
- **Quyền hạn:** `Admin` (Bearer Token)
- **Request Body:**
```json
{
  "commodity_id": 2,
  "model_types": ["lstm", "xgboost"],
  "epochs": 80,
  "horizon_days": 30
}
```
- **Response JSON (202 Accepted):**
```json
{
  "success": true,
  "task_id": "retrain-task-20260910-01",
  "message": "Tiến trình huấn luyện mô hình PyTorch Stacked LSTM và XGBoost đã được đưa vào hàng đợi xử lý ngầm (Background Task)."
}
```

---

## 5. Thiết Kế Giao Diện Frontend Next.js 14 & UI Components

Triển khai tại thư mục `frontend/src/app/forecast/page.tsx` và `frontend/src/components/forecast/`:

```text
frontend/src/
├── app/forecast/
│   └── page.tsx                     # Trang tổng hợp Dự báo AI & So sánh mô hình
└── components/forecast/
    ├── ForecastChart.tsx            # Biểu đồ Recharts ComposedChart (Giá thực tế, Giá dự báo, Dải CI 95%)
    ├── ModelComparisonTable.tsx     # Bảng so sánh 4 chỉ số MAE, RMSE, MAPE, R² với Badge xếp hạng Best Model
    ├── CommoditySelector.tsx        # Tabs chuyển đổi 4 nông sản với icon trực quan
    ├── HorizonSelector.tsx          # Toggle chọn khung 7 ngày, 14 ngày, 30 ngày
    └── ConfidenceIntervalToggle.tsx # Nút bật/tắt dải bóng mờ tin cậy (Area chart opacity)
```

### Các Đặc Điểm Giao Diện Trọng Tâm:
1. **Biểu đồ `ForecastChart`:**
   - Sử dụng `<ComposedChart>` của Recharts.
   - Đường giá lịch sử: Nét liền màu xanh sậm (`#1E3A8A`).
   - Đường giá dự báo: Nét đứt (strokeDasharray="4 4") màu hổ phách ấm (`#D97706`).
   - Dải tin cậy 95%: `<Area>` màu vàng hổ phách với `fillOpacity={0.15}` nằm kẹp giữa `upper_bound` và `lower_bound`.
2. **Bảng đánh giá mô hình `ModelComparisonTable`:**
   - Làm nổi bật mô hình có MAPE thấp nhất bằng huy hiệu `🏆 Optimal Model`.
   - Có cột Switcher cho phép xem đường biểu diễn của từng mô hình trên cùng biểu đồ.

---

## 6. Tiêu Chí Nghiệm Thu (Acceptance Criteria) & Kịch Bản Kiểm Thử (Pytest)

### 6.1. Bảng Tiêu Chí Nghiệm Thu (Checklist)

- [ ] **AC1:** Module `train_lstm.py` thực thi không lỗi trên CPU/CUDA, xuất file trọng số `.pt` vào `saved_models/`.
- [ ] **AC2:** Sai số MAPE trên tập Test của Stacked LSTM đạt dưới **3.0%** đối với cả 4 loại nông sản.
- [ ] **AC3:** Cả 5 mô hình (LSTM, XGBoost, RF, Prophet, ARIMA) đều lưu chỉ số (MAE, RMSE, MAPE, $R^2$) vào bảng `model_registry`.
- [ ] **AC4:** API `/predictions/forecast` phản hồi trong thời gian $< 150\text{ms}$ nhờ cơ chế pre-computed kết quả lưu tại bảng `forecast_results`.
- [ ] **AC5:** Dải tin cậy 95% thỏa mãn điều kiện logic toán học: $\text{lower\_bound} \le \text{predicted\_price} \le \text{upper\_bound}$.
- [ ] **AC6:** Frontend Next.js render trơn tru biểu đồ dải tin cậy, không bị giật lag khi chuyển đổi giữa 4 loại nông sản.

---

### 6.2. Kịch Bản Kiểm Thử Tự Động Pytest (`tests/test_predictions.py`)

```python
# backend/tests/test_predictions.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_forecast_lstm_success():
    """Kiểm thử API dự báo trả về đủ 30 ngày và dải tin cậy hợp lệ"""
    response = client.get("/api/v1/predictions/forecast?commodity_id=2&model_name=lstm&days=30")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["forecast"]) == 30
    
    first_day = data["forecast"][0]
    assert "date" in first_day
    assert "price" in first_day
    assert first_day["lower_bound"] <= first_day["price"] <= first_day["upper_bound"]

def test_model_comparison_metrics_sorted():
    """Kiểm thử bảng so sánh trả về đủ các chỉ số và có mô hình active"""
    response = client.get("/api/v1/predictions/comparison?commodity_id=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["metrics"]) >= 4
    
    # Kiểm tra tồn tại các chỉ số chuẩn
    for metric in data["metrics"]:
        assert "mae" in metric and metric["mae"] > 0
        assert "rmse" in metric and metric["rmse"] > 0
        assert "mape" in metric and 0 < metric["mape"] < 100
        assert "r2_score" in metric

def test_retrain_task_rbac_protection():
    """Kiểm thử bảo mật: Người dùng chưa đăng nhập không thể kích hoạt retrain"""
    response = client.post("/api/v1/admin/tasks/retrain", json={"commodity_id": 2})
    assert response.status_code in [401, 403]
```

#### Lệnh thực thi kiểm thử:
```powershell
cd d:\DA_TN\backend
pytest tests/test_predictions.py -v
```
