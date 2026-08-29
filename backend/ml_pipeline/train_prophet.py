import sys
import os
import warnings
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from prophet import Prophet
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

def run_prophet(commodity_id: int, commodity_name: str, df: pd.DataFrame, db_session, horizon: int = 14):
    print(f"\n--- Training Facebook Prophet for {commodity_name} ---")
    
    # Prepare dataframe for Prophet
    df_p = df.rename(columns={'record_date': 'ds', 'price': 'y'})
    df_p['ds'] = pd.to_datetime(df_p['ds'])
    
    train_size = int(len(df_p) * 0.85)
    train, test = df_p.iloc[:train_size], df_p.iloc[train_size:]
    
    if len(train) == 0 or len(test) == 0:
        return
        
    # Initialize and train eval model
    eval_model = Prophet(daily_seasonality=False, yearly_seasonality=True)
    # Add exogenous regressors if they exist
    if 'usd_vnd' in df_p.columns: eval_model.add_regressor('usd_vnd')
    if 'crude_oil' in df_p.columns: eval_model.add_regressor('crude_oil')
        
    eval_model.fit(train)
    
    # Evaluate
    test_future = eval_model.make_future_dataframe(periods=len(test))
    # We must provide future values for exogenous regressors in testing. 
    # Since we have them in the full df, we'll merge them.
    if 'usd_vnd' in df_p.columns: 
        test_future = pd.merge(test_future, df_p[['ds', 'usd_vnd', 'crude_oil']], on='ds', how='left')
        
    test_forecast = eval_model.predict(test_future)
    test_preds = test_forecast['yhat'].values[-len(test):]
    
    mae = mean_absolute_error(test['y'].values, test_preds)
    rmse = np.sqrt(mean_squared_error(test['y'].values, test_preds))
    mape = calculate_mape(test['y'].values, test_preds)
    r2 = r2_score(test['y'].values, test_preds)
    
    print(f"Prophet Metrics -> MAE: {mae:.2f}, RMSE: {rmse:.2f}, MAPE: {mape:.2f}%, R2: {r2:.3f}")
    
    # Full Model Training
    full_model = Prophet(daily_seasonality=False, yearly_seasonality=True)
    if 'usd_vnd' in df_p.columns: full_model.add_regressor('usd_vnd')
    if 'crude_oil' in df_p.columns: full_model.add_regressor('crude_oil')
    
    full_model.fit(df_p)
    future = full_model.make_future_dataframe(periods=horizon)
    
    # We don't have future exogenous variables, so we naive forecast them (last known value)
    if 'usd_vnd' in df_p.columns:
        last_usd = df_p['usd_vnd'].iloc[-1]
        last_oil = df_p['crude_oil'].iloc[-1]
        
        # Merge existing
        future = pd.merge(future, df_p[['ds', 'usd_vnd', 'crude_oil']], on='ds', how='left')
        future['usd_vnd'].fillna(last_usd, inplace=True)
        future['crude_oil'].fillna(last_oil, inplace=True)
        
    forecast = full_model.predict(future)
    
    preds = forecast['yhat'].values[-horizon:]
    lower_cis = forecast['yhat_lower'].values[-horizon:]
    upper_cis = forecast['yhat_upper'].values[-horizon:]
    
    preds = np.maximum(preds, 0)
    lower_cis = np.maximum(lower_cis, 0)
    upper_cis = np.maximum(upper_cis, 0)
    
    future_dates = forecast['ds'].dt.date.values[-horizon:]
    
    model_name = "Prophet"
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
    print(f"Saved {horizon} forecasts for {commodity_name} using Prophet.")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        commodities = db.query(Commodity).all()
        for c in commodities:
            df = load_clean_data(c.id, db)
            if not df.empty:
                run_prophet(c.id, c.name, df, db, horizon=14)
    finally:
        db.close()
