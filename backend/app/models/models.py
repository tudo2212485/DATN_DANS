from sqlalchemy import Column, Integer, BigInteger, String, Text, Numeric, Boolean, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base


class SystemSetting(Base):
    __tablename__ = "system_settings"
    key = Column(String(100), primary_key=True)
    value = Column(Text, nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class BackgroundJob(Base):
    __tablename__ = "background_jobs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    kind = Column(String(30), nullable=False, index=True)
    status = Column(String(20), nullable=False, default="RUNNING")
    message = Column(Text, nullable=False, default="Đang chờ xử lý")
    records_processed = Column(Integer, nullable=False, default=0)
    progress = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, server_default=func.now())
    finished_at = Column(DateTime, nullable=True)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(150), nullable=False)
    role = Column(String(50), nullable=False, default="analyst")  # 'analyst' | 'admin' | 'user'
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    alert_rules = relationship("AlertRule", back_populates="user", cascade="all, delete-orphan")


class Commodity(Base):
    __tablename__ = "commodities"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(150), nullable=False)
    category = Column(String(50), nullable=False)
    unit = Column(String(30), nullable=False)
    region = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    prices = relationship("PriceHistory", back_populates="commodity", cascade="all, delete-orphan")
    forecasts = relationship("Forecast", back_populates="commodity", cascade="all, delete-orphan")
    alert_rules = relationship("AlertRule", back_populates="commodity", cascade="all, delete-orphan")


class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True, index=True)
    commodity_id = Column(Integer, ForeignKey("commodities.id", ondelete="CASCADE"), nullable=False, index=True)
    record_date = Column(Date, nullable=False, index=True)
    price = Column(Numeric(14, 2), nullable=False)
    price_min = Column(Numeric(14, 2), nullable=True)
    price_max = Column(Numeric(14, 2), nullable=True)
    volume = Column(Numeric(16, 2), default=0)
    source = Column(String(100), default="Sở NN&PTNT / Hiệp hội Nông sản")
    provenance = Column(String(30), nullable=False, default="unverified", server_default="unverified")
    source_details = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    commodity = relationship("Commodity", back_populates="prices")


class Forecast(Base):
    __tablename__ = "forecasts"

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True, index=True)
    commodity_id = Column(Integer, ForeignKey("commodities.id", ondelete="CASCADE"), nullable=False, index=True)
    model_name = Column(String(50), nullable=False, index=True)  # LSTM, Prophet, ARIMA, XGBoost
    training_run_id = Column(Integer, ForeignKey("training_runs.id"), nullable=True)
    forecast_date = Column(Date, nullable=False, index=True)
    predicted_price = Column(Numeric(14, 2), nullable=False)
    lower_ci = Column(Numeric(14, 2), nullable=False)
    upper_ci = Column(Numeric(14, 2), nullable=False)
    mae = Column(Numeric(10, 4), nullable=True)
    rmse = Column(Numeric(10, 4), nullable=True)
    mape = Column(Numeric(10, 4), nullable=True)
    r2 = Column(Numeric(10, 4), nullable=True)
    training_date = Column(Date, server_default=func.current_date())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    commodity = relationship("Commodity", back_populates="forecasts")


class TrainingRun(Base):
    __tablename__ = "training_runs"
    id = Column(Integer, primary_key=True)
    commodity_id = Column(Integer, ForeignKey("commodities.id"), nullable=False)
    dataset_hash = Column(String(64), nullable=False)
    metadata_json = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class PeriodicPrice(Base):
    __tablename__ = "periodic_prices"
    id = Column(Integer, primary_key=True)
    commodity_id = Column(Integer, ForeignKey("commodities.id"), nullable=False)
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    published_date = Column(Date, nullable=False)
    buying_price = Column(Numeric(14, 2), nullable=False)
    selling_price = Column(Numeric(14, 2), nullable=False)
    unit = Column(String(30), nullable=False)
    specification = Column(String(150), nullable=False)
    market = Column(String(150), nullable=False)
    source_url = Column(Text, nullable=False, unique=True)
    attribution = Column(Text, nullable=False)
    collected_at = Column(DateTime, server_default=func.now())


class PriceRevision(Base):
    __tablename__ = "price_revisions"
    id = Column(Integer, primary_key=True)
    price_id = Column(BigInteger, nullable=False)
    snapshot_json = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class AlertRule(Base):
    __tablename__ = "alert_rules"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    commodity_id = Column(Integer, ForeignKey("commodities.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    rule_name = Column(String(150), nullable=False)
    condition_type = Column(String(50), nullable=False)  # PRICE_ABOVE, PRICE_BELOW, PCT_INC_7D, PCT_DEC_7D
    threshold_value = Column(Numeric(14, 2), nullable=False)
    email = Column(String(150), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    commodity = relationship("Commodity", back_populates="alert_rules")
    user = relationship("User", back_populates="alert_rules")
    logs = relationship("AlertLog", back_populates="rule", cascade="all, delete-orphan")


class AlertLog(Base):
    __tablename__ = "alert_logs"

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True, index=True)
    rule_id = Column(Integer, ForeignKey("alert_rules.id", ondelete="CASCADE"), nullable=False, index=True)
    triggered_price = Column(Numeric(14, 2), nullable=False)
    message = Column(Text, nullable=False)
    status = Column(String(30), default="SENT")
    triggered_at = Column(DateTime(timezone=True), server_default=func.now())

    rule = relationship("AlertRule", back_populates="logs")
