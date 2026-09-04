from fastapi import APIRouter
from app.api.v1.endpoints import commodities, prices, forecast, alerts, auth, admin

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(commodities.router, prefix="/commodities", tags=["Commodities"])
api_router.include_router(prices.router, prefix="/prices", tags=["Prices"])
api_router.include_router(forecast.router, prefix="/forecast", tags=["Forecast & ML"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["Alerts"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin Management"])
