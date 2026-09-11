from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import date, datetime

# --- User & Auth Schemas ---
class UserBase(BaseModel):
    email: str
    full_name: str
    role: str = "analyst"  # 'analyst' | 'admin' | 'user'
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=150)
    password: str = Field(..., min_length=6, max_length=100)
    role: Optional[str] = "analyst"

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class TokenPayload(BaseModel):
    sub: Optional[str] = None
    role: Optional[str] = None
    exp: Optional[int] = None

# --- Commodity Schemas ---
class CommodityBase(BaseModel):
    code: str
    name: str
    category: str
    unit: str
    region: str
    description: Optional[str] = None

class CommodityCreate(CommodityBase):
    pass

class CommodityResponse(CommodityBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# --- Sparkline & Overview Schemas ---
class SparklinePoint(BaseModel):
    date: str
    value: float

class CommodityOverviewCard(BaseModel):
    id: int
    code: str
    name: str
    category: str
    unit: str
    region: str
    currentPrice: float
    formattedPrice: str
    changePct: float
    isPositive: bool = Field(alias="isPositive", default=True)
    sparkline: List[SparklinePoint]

    class Config:
        populate_by_name = True

class MarketComparisonPoint(BaseModel):
    date: str
    rice: float
    coffee: float
    pepper: float
    sugar: float

class SpotlightSummaryResponse(BaseModel):
    commodityCode: str
    commodityName: str
    subtitle: str
    currentPrice: str
    change3Months: str
    peakPrice: str
    trendData: List[SparklinePoint]

class RegionalPriceResponse(BaseModel):
    id: int
    commodityName: str
    code: str
    region: str
    price: str
    unit: str
    minMax: str
    volume: str
    changePct: float
    source: str
    updatedAt: str

# --- Price History Schemas ---
class PriceHistoryBase(BaseModel):
    commodity_id: int
    record_date: date
    price: float
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    volume: Optional[float] = 0.0
    source: Optional[str] = None

class PriceHistoryResponse(PriceHistoryBase):
    id: int

    class Config:
        from_attributes = True

# --- Forecast Schemas ---
class ForecastPointResponse(BaseModel):
    date: str
    actualPrice: Optional[float] = None
    predictedPrice: float
    lowerCI: float
    upperCI: float
    isForecast: bool = False

class ModelMetricsResponse(BaseModel):
    modelName: str
    mae: float
    rmse: float
    mape: float
    r2: float
    trainDate: str

class ForecastDashboardResponse(BaseModel):
    commodity: CommodityResponse
    modelName: str
    metrics: ModelMetricsResponse
    forecastData: List[ForecastPointResponse]

# --- Alert Rules Schemas ---
class AlertRuleCreate(BaseModel):
    commodity_id: int
    rule_name: str
    condition_type: str  # PRICE_ABOVE, PRICE_BELOW, PCT_INC_7D, PCT_DEC_7D
    threshold_value: float
    email: str

class AlertRuleResponse(BaseModel):
    id: int
    commodity_id: int
    commodity_name: Optional[str] = None
    user_id: Optional[int] = None
    rule_name: str
    condition_type: str
    threshold_value: float
    email: str
    is_active: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class AlertRuleToggle(BaseModel):
    is_active: bool

# --- Alert Logs Schemas ---
class AlertLogResponse(BaseModel):
    id: int
    rule_id: int
    rule_name: Optional[str] = None
    commodity_name: Optional[str] = None
    email: Optional[str] = None
    triggered_price: float
    message: str
    status: str
    triggered_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# --- Admin Schemas ---
class AdminStatsResponse(BaseModel):
    total_commodities: int
    total_price_records: int
    total_forecast_records: int
    total_alert_rules: int
    latest_price_date: Optional[str] = None
    system_status: str = "ONLINE"

class PriceCreateManual(BaseModel):
    commodity_id: int
    record_date: date
    price: float
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    volume: Optional[float] = 0.0
    source: Optional[str] = "Nhập thủ công bởi Quản trị viên"

class AdminPriceItem(BaseModel):
    id: int
    commodity_id: int
    commodity_name: str
    record_date: str
    price: float
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    volume: Optional[float] = 0.0
    source: Optional[str] = None

class TaskRunResponse(BaseModel):
    task_name: str
    status: str
    message: str
    records_processed: Optional[int] = 0
    timestamp: str

# --- Retrain Admin Schema ---
class RetrainResponse(BaseModel):
    status: str
    message: str
    timestamp: str

# --- Phase 4 Machine Learning & Prediction Schemas ---
class PredictionPointItem(BaseModel):
    date: str
    display_date: Optional[str] = None
    yhat: float
    yhat_lower: float
    yhat_upper: float
    actual_price: Optional[float] = None
    is_forecast: bool = True

class PredictionMetricsItem(BaseModel):
    mae: float
    rmse: float
    mape: float
    r2: float

class PredictionForecastResponse(BaseModel):
    symbol: str
    commodity: Optional[dict] = None
    model_name: str
    forecast_days: int
    response_time_ms: float
    cached: bool = False
    metrics: dict
    history: List[PredictionPointItem] = []
    forecast: List[PredictionPointItem] = []
    all_points: List[PredictionPointItem] = []

class PredictionModelMetric(BaseModel):
    model_name: str
    metrics: dict
    trained_at: Optional[str] = None
    passed_threshold: bool = True
    threshold_reason: Optional[str] = None

class PredictionMetricsResponse(BaseModel):
    symbol: Optional[str] = None
    models: List[PredictionModelMetric]

# --- Phase 5 Admin Dashboard & Control Panel Schemas ---
class CrawlerLogItem(BaseModel):
    id: int
    crawler_name: str
    target_source: str
    records_extracted: int
    status: str  # SUCCESS, FAILED, RUNNING
    duration_sec: float
    timestamp: str
    details: Optional[str] = None

class CSVImportResponse(BaseModel):
    message: str
    records_created: int
    records_updated: int
    errors: List[str] = []

class UserRoleUpdate(BaseModel):
    role: str  # admin, analyst, user

class UserStatusUpdate(BaseModel):
    is_active: bool

class ActiveModelSetting(BaseModel):
    active_model: str  # LSTM, XGBoost, Prophet, ARIMA
    description: Optional[str] = None
    updated_at: Optional[str] = None


