# -*- coding: utf-8 -*-
import os
import sys

# Ensure UTF-8 output in Windows console
sys.stdout.reconfigure(encoding='utf-8')

from app.core.database import SessionLocal
from app.models.models import Commodity, PriceHistory, Forecast
from sqlalchemy import func

def inspect_data():
    db = SessionLocal()
    commodities = db.query(Commodity).all()

    print("======================================================================")
    print("  KIEM TRA TINH DUNG DAN VA PHU HOP CUA DU LIEU GIA TRONG DATABASE")
    print("======================================================================\n")

    for c in commodities:
        count = db.query(PriceHistory).filter(PriceHistory.commodity_id == c.id).count()
        min_p = db.query(func.min(PriceHistory.price)).filter(PriceHistory.commodity_id == c.id).scalar() or 0
        max_p = db.query(func.max(PriceHistory.price)).filter(PriceHistory.commodity_id == c.id).scalar() or 0
        avg_p = db.query(func.avg(PriceHistory.price)).filter(PriceHistory.commodity_id == c.id).scalar() or 0
        
        first_r = db.query(PriceHistory).filter(PriceHistory.commodity_id == c.id).order_by(PriceHistory.record_date.asc()).first()
        latest_r = db.query(PriceHistory).filter(PriceHistory.commodity_id == c.id).order_by(PriceHistory.record_date.desc()).first()
        
        print(f"[*] MAT HANG: {c.name.upper()} (Mã: {c.code}) - Don vi: {c.unit} | Khu vuc: {c.region}")
        print(f"    - Tong so ngay du lieu: {count} ngay (Tu {first_r.record_date if first_r else 'N/A'} den {latest_r.record_date if latest_r else 'N/A'})")
        print(f"    - Vung gia lich su: {min_p:,.0f} d  -->  {max_p:,.0f} d (Trung binh: {avg_p:,.0f} d/{c.unit})")
        if latest_r:
            print(f"    - Gia phien gan nhat ({latest_r.record_date}): {latest_r.price:,.0f} d/{c.unit} (Min: {latest_r.price_min:,.0f} d, Max: {latest_r.price_max:,.0f} d)")
            print(f"    - Nguon du lieu: {latest_r.source}")
        
        # Check forecasts
        print("    - Du bao 7 ngay tiep theo cua cac mo hinh:")
        for model_name in ['Prophet', 'ARIMA', 'LSTM', 'XGBoost', 'Random Forest']:
            fc = db.query(Forecast).filter(Forecast.commodity_id == c.id, Forecast.model_name == model_name).order_by(Forecast.forecast_date.asc()).first()
            if fc:
                print(f"      + {model_name:13}: Ngay {fc.forecast_date} -> {fc.predicted_price:,.0f} d (Khoang: {fc.lower_ci:,.0f} - {fc.upper_ci:,.0f}) | MAE={fc.mae:,.0f} d, MAPE={fc.mape:.2f}%")
        print("-" * 70)

    db.close()

if __name__ == "__main__":
    inspect_data()
