from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import date, datetime

# --- User & Auth Schemas ---
class UserBase(BaseModel):
    email: str
    full_name: str
    role: str = "analyst"  # 'analyst' | 'admin'

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: str
    password: str

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
    email: Optional[str] = None
    triggered_price: float
    message: str
    status: str
    triggered_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# --- Retrain Admin Schema ---
class RetrainResponse(BaseModel):
    status: str
    message: str
    timestamp: str
