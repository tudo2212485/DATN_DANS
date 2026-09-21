from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI, Request, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime, timezone

from app.core.config import settings
from app.core.database import engine, Base, get_db
from app.api.v1.api import api_router
from app.core.scheduler import start_scheduler, stop_scheduler
from app.core.schema_upgrade import upgrade_existing_schema

logger = logging.getLogger("app.main")

# Khởi tạo các bảng nếu chưa có
try:
    upgrade_existing_schema()
    Base.metadata.create_all(bind=engine)
except Exception as e:
    logger.warning(f"Warning: Unable to connect to DB at startup: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.models.models import BackgroundJob
    from app.core.database import SessionLocal
    from datetime import datetime
    with SessionLocal() as db:
        db.query(BackgroundJob).filter(BackgroundJob.status == "RUNNING").update({
            "status": "FAILED", "message": "Tác vụ bị gián đoạn khi máy chủ khởi động lại", "finished_at": datetime.now()})
        db.commit()
    # Khởi động Background Scheduler
    start_scheduler()
    yield
    # Dừng Background Scheduler
    stop_scheduler()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    description="AgroForecast REST API - Hệ thống Dự báo Giá Nông sản & Cảnh báo Thị trường.",
    lifespan=lifespan
)

from app.core.security import SecurityHeadersMiddleware

# Cấu hình Security Headers Middleware (OWASP Top 10 Hardening)
app.add_middleware(SecurityHeadersMiddleware)

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.url}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Đã xảy ra lỗi nội bộ máy chủ. Vui lòng thử lại sau."},
    )

# Kết nối Router V1
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/", tags=["System"])
def root():
    """Thông tin cơ bản về hệ thống API"""
    return {
        "status": "online",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": "/docs",
        "api_v1": settings.API_V1_STR
    }

@app.get("/health", tags=["System"])
def health_check(db: Session = Depends(get_db)):
    """Kiểm tra sức khỏe hệ thống và kết nối CSDL PostgreSQL"""
    db_status = "connected"
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    return {
        "status": "healthy" if db_status == "connected" else "degraded",
        "database": db_status,
        "version": settings.VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
