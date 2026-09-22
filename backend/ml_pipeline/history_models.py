"""Fit a prefix, then forecast recursively without seeing holdout values."""
import numpy as np
import pandas as pd


def predict_series(name, series, horizon, future_index=None):
    values = np.asarray(series, dtype=float)
    dates = pd.DatetimeIndex(future_index) if future_index is not None else pd.date_range(
        series.index[-1] + pd.Timedelta(days=1), periods=horizon
    )
    lookback = min(14, max(2, len(values) // 3))
    if name in ("Random Forest", "XGBoost"):
        if name == "Random Forest":
            from sklearn.ensemble import RandomForestRegressor
            model = RandomForestRegressor(n_estimators=100, max_depth=8, random_state=42, n_jobs=1)
        else:
            from xgboost import XGBRegressor
            model = XGBRegressor(n_estimators=100, max_depth=3, learning_rate=.05, random_state=42, n_jobs=1)
        x = np.asarray([values[i-lookback:i] for i in range(lookback, len(values))])
        model.fit(x, values[lookback:])
        history, result = list(values), []
        for _ in range(horizon):
            prediction = max(float(model.predict(np.asarray(history[-lookback:]).reshape(1, -1))[0]), 0)
            result.append(prediction)
            history.append(prediction)
        return np.asarray(result)
    if name == "ARIMA":
        from statsmodels.tsa.arima.model import ARIMA
        return np.maximum(ARIMA(values, order=(2, 1, 1)).fit().forecast(horizon), 0)
    if name == "Prophet":
        from prophet import Prophet
        model = Prophet(yearly_seasonality=False, daily_seasonality=False, weekly_seasonality=True, uncertainty_samples=0)
        model.fit(pd.DataFrame({"ds": series.index, "y": values}))
        return np.maximum(model.predict(pd.DataFrame({"ds": dates}))["yhat"].to_numpy(), 0)
    if name == "LSTM":
        import torch
        from sklearn.preprocessing import MinMaxScaler
        from ml_pipeline.train_lstm import MultiLayerLSTM
        torch.manual_seed(42)
        scaler = MinMaxScaler(feature_range=(-1, 1))
        scaled = scaler.fit_transform(values.reshape(-1, 1)).ravel()
        x = torch.tensor(np.asarray([scaled[i-lookback:i] for i in range(lookback, len(values))]), dtype=torch.float32).unsqueeze(-1)
        y = torch.tensor(scaled[lookback:], dtype=torch.float32).unsqueeze(-1)
        model = MultiLayerLSTM(1, hidden_size=32)
        optimizer = torch.optim.Adam(model.parameters(), lr=.005)
        model.train()
        for _ in range(50):
            optimizer.zero_grad()
            loss = torch.nn.functional.mse_loss(model(x), y)
            loss.backward()
            optimizer.step()
        model.eval()
        history, result = list(scaled), []
        with torch.no_grad():
            for _ in range(horizon):
                prediction = float(model(torch.tensor(history[-lookback:], dtype=torch.float32).reshape(1, lookback, 1)).item())
                history.append(prediction)
                result.append(prediction)
        return np.maximum(scaler.inverse_transform(np.asarray(result).reshape(-1, 1)).ravel(), 0)
    raise ValueError(f"Unsupported model: {name}")


def score(actual, predicted):
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    actual, predicted = np.asarray(actual), np.asarray(predicted)
    if not np.isfinite(predicted).all():
        raise ValueError("Mô hình trả dự báo không hữu hạn")
    return {"mae": float(mean_absolute_error(actual, predicted)),
            "rmse": float(np.sqrt(mean_squared_error(actual, predicted))),
            "mape": float(np.mean(np.abs((actual-predicted)/actual)) * 100),
            "r2": float(r2_score(actual, predicted))}
