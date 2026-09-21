import sys
import os
import warnings
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
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
from ml_pipeline.feature_engineering import create_features

def calculate_mape(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    y_true = np.where(y_true == 0, 1e-8, y_true)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

def prepare_tabular_data(df: pd.DataFrame):
    df_feat = create_features(df, target_col='price')
    # Drop columns that are not features (like record_date)
    features = [col for col in df_feat.columns if col not in ['record_date', 'price']]
    X = df_feat[features].values
    y = df_feat['price'].values
    return X, y, features, df_feat

def save_forecast(db_session, commodity_id, model_name, preds, std_err, metrics, future_dates, base_price):
    db_session.query(Forecast).filter(
        Forecast.commodity_id == commodity_id,
        Forecast.model_name == model_name
    ).delete()
    
    records = []
    for i, dt in enumerate(future_dates):
        pred_val = float(max(preds[i], 0))
        records.append(Forecast(
            commodity_id=commodity_id,
            model_name=model_name,
            forecast_date=dt,
            predicted_price=pred_val,
            lower_ci=float(max(pred_val - 1.96 * std_err, 0)),
            upper_ci=float(pred_val + 1.96 * std_err),
            mae=float(metrics['mae']),
            rmse=float(metrics['rmse']),
            mape=float(metrics['mape']),
            r2=float(metrics['r2']),
            training_date=datetime.now().date()
        ))
    db_session.add_all(records)
    db_session.commit()
    print(f"Saved forecasts for {model_name}.")
    return len(records)

def run_ml_models(commodity_id: int, commodity_name: str, df: pd.DataFrame, db_session, horizon: int = 30):
    print(f"\n--- Training Tabular ML Models for {commodity_name} ---")
    
    X, y, feature_names, df_feat = prepare_tabular_data(df)
    
    train_size = int(len(X) * 0.85)
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]
    
    if len(X_train) == 0 or len(X_test) == 0:
        raise ValueError("Không đủ dữ liệu huấn luyện và kiểm thử")
        
    base_price = np.mean(y)
    
    # 1. Random Forest
    print("\nTraining Random Forest...")
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    rf_preds = rf_model.predict(X_test)
    
    rf_metrics = {
        'mae': mean_absolute_error(y_test, rf_preds),
        'rmse': np.sqrt(mean_squared_error(y_test, rf_preds)),
        'mape': calculate_mape(y_test, rf_preds),
        'r2': r2_score(y_test, rf_preds)
    }
    print(f"RF Metrics -> MAE: {rf_metrics['mae']:.2f}, R2: {rf_metrics['r2']:.3f}")
    
    # 2. XGBoost with Basic Tuning
    print("\nTraining XGBoost with Hyperparameter tuning...")
    xgb_base = XGBRegressor(random_state=42, objective='reg:squarederror')
    param_grid = {
        'n_estimators': [50, 100],
        'max_depth': [3, 5],
        'learning_rate': [0.05, 0.1]
    }
    grid_search = GridSearchCV(estimator=xgb_base, param_grid=param_grid, cv=TimeSeriesSplit(n_splits=3), scoring='neg_mean_absolute_error')
    grid_search.fit(X_train, y_train)
    xgb_model = grid_search.best_estimator_
    
    print(f"Best XGBoost Params: {grid_search.best_params_}")
    xgb_preds = xgb_model.predict(X_test)
    
    xgb_metrics = {
        'mae': mean_absolute_error(y_test, xgb_preds),
        'rmse': np.sqrt(mean_squared_error(y_test, xgb_preds)),
        'mape': calculate_mape(y_test, xgb_preds),
        'r2': r2_score(y_test, xgb_preds)
    }
    print(f"XGB Metrics -> MAE: {xgb_metrics['mae']:.2f}, R2: {xgb_metrics['r2']:.3f}")
    
    # Feature Importance for XGBoost
    importances = xgb_model.feature_importances_
    feat_imp = sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True)
    print("\nXGBoost Feature Importance:")
    for f, imp in feat_imp[:5]:
        print(f" - {f}: {imp:.4f}")
        
    # Full training for future predictions
    rf_model.fit(X, y)
    xgb_model.fit(X, y)
    
    # Recompute all date, lag and rolling features for each new forecast day.
    def future_prices(model):
        history = df.copy()
        predictions = []
        for _ in range(horizon):
            next_row = history.iloc[-1].copy()
            next_row['record_date'] = pd.to_datetime(next_row['record_date']) + pd.Timedelta(days=1)
            history = pd.concat([history, pd.DataFrame([next_row])], ignore_index=True)
            features = create_features(history, target_col='price').iloc[-1][feature_names]
            prediction = float(max(model.predict(features.to_numpy(dtype=float).reshape(1, -1))[0], 0))
            history.loc[history.index[-1], 'price'] = prediction
            predictions.append(prediction)
        return predictions

    rf_future_preds = future_prices(rf_model)
    xgb_future_preds = future_prices(xgb_model)
        
    last_date = df['record_date'].iloc[-1]
    if hasattr(last_date, 'date'): last_date = last_date.date()
    future_dates = [last_date + pd.Timedelta(days=i) for i in range(1, horizon + 1)]
    
    save_forecast(db_session, commodity_id, "Random Forest", rf_future_preds, rf_metrics['rmse'], rf_metrics, future_dates, base_price)
    save_forecast(db_session, commodity_id, "XGBoost", xgb_future_preds, xgb_metrics['rmse'], xgb_metrics, future_dates, base_price)
    return len(rf_future_preds) + len(xgb_future_preds)

if __name__ == "__main__":
    db = SessionLocal()
    try:
        commodities = db.query(Commodity).all()
        for c in commodities:
            df = load_clean_data(c.id, db)
            if not df.empty:
                run_ml_models(c.id, c.name, df, db, horizon=30)
    finally:
        db.close()
