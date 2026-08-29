import sys
import os
import warnings
import pandas as pd
import numpy as np
from datetime import datetime
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Ensure UTF-8 output on Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

warnings.filterwarnings("ignore")
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.models.models import Commodity, Forecast
from ml_pipeline.data_loader import load_clean_data

def calculate_mape(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    y_true = np.where(y_true == 0, 1e-8, y_true)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

def optimize_arima(series: pd.Series):
    """Grid search for best ARIMA parameters based on AIC"""
    best_aic = float("inf")
    best_order = None
    best_model = None
    
    # Simple grid for demonstration (p, d, q)
    p_values = [0, 1, 2]
    d_values = [0, 1]
    q_values = [0, 1, 2]
    
    print("Finding best ARIMA parameters via AIC...")
    for p in p_values:
        for d in d_values:
            for q in q_values:
                try:
                    model = ARIMA(series, order=(p, d, q))
                    results = model.fit()
                    if results.aic < best_aic:
                        best_aic = results.aic
                        best_order = (p, d, q)
                        best_model = results
                except:
                    continue
                    
    print(f"Best ARIMA Order: {best_order} with AIC: {best_aic:.2f}")
    return best_order, best_model

def run_arima(commodity_id: int, commodity_name: str, df: pd.DataFrame, db_session, horizon: int = 14):
    print(f"\n--- Training ARIMA for {commodity_name} ---")
    
    prices = df["price"].values
    
    # Train-test split for evaluation
    train_size = int(len(prices) * 0.85)
    train, test = prices[:train_size], prices[train_size:]
    
    if len(train) == 0 or len(test) == 0:
        return
        
    # Find best order on train set
    best_order, _ = optimize_arima(train)
    if not best_order:
        best_order = (1, 1, 1) # Fallback
        
    # Evaluate on test set
    eval_model = ARIMA(train, order=best_order).fit()
    test_preds = eval_model.forecast(steps=len(test))
    
    mae = mean_absolute_error(test, test_preds)
    rmse = np.sqrt(mean_squared_error(test, test_preds))
    mape = calculate_mape(test, test_preds)
    r2 = r2_score(test, test_preds)
    
    print(f"Evaluation -> MAE: {mae:.2f}, RMSE: {rmse:.2f}, MAPE: {mape:.2f}%, R2: {r2:.3f}")
    
    # Train on full data for future forecasting
    final_model = ARIMA(prices, order=best_order).fit()
    forecast_res = final_model.get_forecast(steps=horizon)
    
    preds = forecast_res.predicted_mean
    conf_int = forecast_res.conf_int(alpha=0.05) # 95% CI
    
    preds = np.maximum(preds, 0)
    lower_cis = np.maximum(conf_int[:, 0], 0)
    upper_cis = np.maximum(conf_int[:, 1], 0)
    
    # Generate future dates
    last_date = df['record_date'].iloc[-1]
    # Handle if record_date is pandas timestamp or python date
    if hasattr(last_date, 'date'):
        last_date = last_date.date()
    future_dates = [last_date + pd.Timedelta(days=i) for i in range(1, horizon + 1)]
    
    # Save to DB
    model_name = "ARIMA"
    db_session.query(Forecast).filter(
        Forecast.commodity_id == commodity_id,
        Forecast.model_name == model_name
    ).delete()
    
    records = []
    for i, dt in enumerate(future_dates):
        records.append(Forecast(
            commodity_id=commodity_id,
            model_name=model_name,
            forecast_date=dt,
            predicted_price=float(preds[i]),
            lower_ci=float(lower_cis[i]),
            upper_ci=float(upper_cis[i]),
            mae=float(mae),
            rmse=float(rmse),
            mape=float(mape),
            r2=float(r2) if r2 > 0 else 0.5,
            training_date=datetime.now().date()
        ))
    db_session.add_all(records)
    db_session.commit()
    print(f"Saved {horizon} forecasts for {commodity_name} using ARIMA.")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        commodities = db.query(Commodity).all()
        for c in commodities:
            df = load_clean_data(c.id, db)
            if not df.empty:
                run_arima(c.id, c.name, df, db, horizon=14)
    finally:
        db.close()
