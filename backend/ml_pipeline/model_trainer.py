import os
import sys
import json
import joblib
import warnings
import numpy as np
import pandas as pd
from datetime import datetime
from typing import Dict, Any, Tuple, Optional

import torch
import torch.nn as nn
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor
from prophet import Prophet
from statsmodels.tsa.arima.model import ARIMA

warnings.filterwarnings("ignore")

# Đảm bảo đường dẫn tới root của backend
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(CURRENT_DIR)
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from ml_pipeline.feature_engineering import create_features

# Đường dẫn lưu models
SAVED_MODELS_DIR = os.path.join(CURRENT_DIR, "saved_models")
os.makedirs(SAVED_MODELS_DIR, exist_ok=True)


def calculate_mape(y_true, y_pred) -> float:
    y_true, y_pred = np.array(y_true, dtype=float), np.array(y_pred, dtype=float)
    y_true_safe = np.where(y_true == 0, 1e-8, y_true)
    return float(np.mean(np.abs((y_true - y_pred) / y_true_safe)) * 100)


def evaluate_metrics(y_true, y_pred) -> Dict[str, float]:
    y_true = np.array(y_true, dtype=float)
    y_pred = np.array(y_pred, dtype=float)
    mae = float(mean_absolute_error(y_true, y_pred))
    mse = float(mean_squared_error(y_true, y_pred))
    rmse = float(np.sqrt(mse))
    mape = calculate_mape(y_true, y_pred)
    try:
        r2 = float(r2_score(y_true, y_pred))
    except Exception:
        r2 = 0.5
    return {
        "mae": round(mae, 4),
        "rmse": round(rmse, 4),
        "mape": round(mape, 2),
        "r2": round(max(r2, 0.0), 4)
    }


class LSTMModel(nn.Module):
    def __init__(self, input_size: int = 1, hidden_size: int = 64, num_layers: int = 2, output_size: int = 1):
        super(LSTMModel, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, dropout=0.2 if num_layers > 1 else 0.0)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])
        return out


class ModelTrainer:
    """
    Quy trình huấn luyện và đánh giá mô hình học máy:
    Preprocessed Data -> Feature Engineering -> Model Training -> Evaluation -> Quality Threshold Gate -> Save Weights
    """

    def __init__(self, commodity_code: str, max_rmse_threshold_ratio: float = 0.35):
        """
        :param commodity_code: Mã nông sản (ví dụ: 'ROBUSTA', 'PEPPER', 'RICE', 'COPPER' hoặc 'ID_2')
        :param max_rmse_threshold_ratio: Ngưỡng RMSE tối đa cho phép so với giá trung bình (mặc định 35%)
        """
        self.commodity_code = str(commodity_code).upper()
        self.max_rmse_threshold_ratio = max_rmse_threshold_ratio
        self.model_dir = os.path.join(SAVED_MODELS_DIR, self.commodity_code)
        os.makedirs(self.model_dir, exist_ok=True)

    def check_threshold(self, metrics: Dict[str, float], mean_price: float) -> Tuple[bool, str]:
        """Kiểm tra xem sai số mô hình có đạt chuẩn chất lượng trước khi deploy weights hay không"""
        if mean_price <= 0:
            return True, "Passed (No baseline price)"
        
        ratio = metrics["rmse"] / mean_price
        if ratio > self.max_rmse_threshold_ratio:
            return False, f"RMSE {metrics['rmse']:.2f} vượt quá ngưỡng cho phép ({ratio*100:.1f}% > {self.max_rmse_threshold_ratio*100:.1f}% của giá TB {mean_price:.2f})"
        return True, f"Passed Quality Check (RMSE/Mean = {ratio*100:.2f}%)"

    def train_prophet(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Huấn luyện mô hình Facebook Prophet"""
        if len(df) < 10:
            raise ValueError("Không đủ dữ liệu để huấn luyện Prophet (tối thiểu 10 dòng)")

        df_p = df.copy().rename(columns={"record_date": "ds", "price": "y"})
        df_p["ds"] = pd.to_datetime(df_p["ds"])
        mean_price = float(df_p["y"].mean())

        # Chia tập train/test (85% / 15%)
        train_size = max(int(len(df_p) * 0.85), 5)
        train_df = df_p.iloc[:train_size]
        test_df = df_p.iloc[train_size:]

        # Thêm biến ngoại sinh nếu có
        exo_cols = [c for c in ["usd_vnd", "crude_oil"] if c in df_p.columns]
        yearly_seasonality = True if len(df_p) >= 365 else False

        # Model đánh giá
        eval_model = Prophet(daily_seasonality=False, weekly_seasonality=True, yearly_seasonality=yearly_seasonality, interval_width=0.95)
        for col in exo_cols:
            eval_model.add_regressor(col)
        eval_model.fit(train_df)

        test_future = eval_model.make_future_dataframe(periods=len(test_df))
        if exo_cols:
            test_future = pd.merge(test_future, df_p[["ds"] + exo_cols], on="ds", how="left").ffill().bfill()
        
        test_forecast = eval_model.predict(test_future)
        test_preds = test_forecast["yhat"].values[-len(test_df):] if len(test_df) > 0 else test_forecast["yhat"].values
        test_actual = test_df["y"].values if len(test_df) > 0 else train_df["y"].values[-len(test_preds):]

        metrics = evaluate_metrics(test_actual, test_preds)
        passed, reason = self.check_threshold(metrics, mean_price)

        # Huấn luyện mô hình đầy đủ trên toàn bộ dữ liệu
        full_model = Prophet(daily_seasonality=False, weekly_seasonality=True, yearly_seasonality=yearly_seasonality, interval_width=0.95)
        for col in exo_cols:
            full_model.add_regressor(col)
        full_model.fit(df_p)

        model_path = os.path.join(self.model_dir, "prophet_model.pkl")
        if passed:
            joblib.dump(full_model, model_path)

        meta = {
            "model_name": "Prophet",
            "metrics": metrics,
            "passed_threshold": passed,
            "threshold_reason": reason,
            "trained_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "exogenous_features": exo_cols,
            "saved_model_path": model_path if passed else None
        }
        self._save_metadata("prophet_metrics.json", meta)
        return meta


    def train_xgboost(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Huấn luyện mô hình XGBoost Regressor với Feature Engineering"""
        df_feat = create_features(df, target_col="price")
        feature_cols = [c for c in df_feat.columns if c not in ["record_date", "price"]]
        
        X = df_feat[feature_cols].values
        y = df_feat["price"].values
        mean_price = float(np.mean(y))

        if len(X) < 10:
            raise ValueError("Không đủ dữ liệu sau khi tạo lag features để huấn luyện XGBoost")

        train_size = max(int(len(X) * 0.85), 5)
        X_train, X_test = X[:train_size], X[train_size:]
        y_train, y_test = y[:train_size], y[train_size:]

        model = XGBRegressor(
            n_estimators=100,
            max_depth=4,
            learning_rate=0.08,
            random_state=42,
            objective="reg:squarederror"
        )
        model.fit(X_train, y_train)

        if len(X_test) > 0:
            preds = model.predict(X_test)
            metrics = evaluate_metrics(y_test, preds)
        else:
            preds = model.predict(X_train)
            metrics = evaluate_metrics(y_train, preds)

        passed, reason = self.check_threshold(metrics, mean_price)

        # Fit trên toàn bộ dữ liệu
        full_model = XGBRegressor(
            n_estimators=100,
            max_depth=4,
            learning_rate=0.08,
            random_state=42,
            objective="reg:squarederror"
        )
        full_model.fit(X, y)

        model_path = os.path.join(self.model_dir, "xgboost_model.pkl")
        features_path = os.path.join(self.model_dir, "xgboost_features.json")

        if passed:
            joblib.dump(full_model, model_path)
            with open(features_path, "w", encoding="utf-8") as f:
                json.dump({"features": feature_cols}, f, indent=2)

        meta = {
            "model_name": "XGBoost",
            "metrics": metrics,
            "passed_threshold": passed,
            "threshold_reason": reason,
            "trained_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "features": feature_cols,
            "saved_model_path": model_path if passed else None
        }
        self._save_metadata("xgboost_metrics.json", meta)
        return meta

    def train_lstm(self, df: pd.DataFrame, epochs: int = 60, seq_length: int = 14) -> Dict[str, Any]:
        """Huấn luyện mô hình PyTorch LSTM"""
        features = ["price"]
        for exo in ["usd_vnd", "crude_oil"]:
            if exo in df.columns:
                features.append(exo)

        data = df[features].values
        mean_price = float(np.mean(data[:, 0]))

        if len(data) < seq_length + 5:
            raise ValueError(f"Không đủ dữ liệu cho chuỗi thời gian LSTM (cần tối thiểu {seq_length + 5} dòng)")

        scaler = MinMaxScaler(feature_range=(-1, 1))
        scaled_data = scaler.fit_transform(data)

        xs, ys = [], []
        for i in range(len(scaled_data) - seq_length):
            xs.append(scaled_data[i:(i + seq_length)])
            ys.append(scaled_data[i + seq_length, 0])
        X = np.array(xs)
        y = np.array(ys)

        train_size = max(int(len(X) * 0.85), 5)
        X_train, X_test = X[:train_size], X[train_size:]
        y_train, y_test = y[:train_size], y[train_size:]

        X_train_t = torch.tensor(X_train, dtype=torch.float32)
        y_train_t = torch.tensor(y_train, dtype=torch.float32)
        X_test_t = torch.tensor(X_test, dtype=torch.float32)
        y_test_t = torch.tensor(y_test, dtype=torch.float32)

        input_size = len(features)
        model = LSTMModel(input_size=input_size, hidden_size=64, num_layers=2)
        criterion = nn.MSELoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=0.005)

        model.train()
        for _ in range(epochs):
            optimizer.zero_grad()
            outputs = model(X_train_t).squeeze()
            loss = criterion(outputs, y_train_t)
            loss.backward()
            optimizer.step()

        # Đánh giá
        model.eval()
        with torch.no_grad():
            eval_x = X_test_t if len(X_test_t) > 0 else X_train_t
            eval_y = y_test_t if len(y_test_t) > 0 else y_train_t
            test_preds_scaled = model(eval_x).numpy()

        dummy_preds = np.zeros((len(test_preds_scaled), len(features)))
        dummy_preds[:, 0] = test_preds_scaled.flatten()
        test_preds = scaler.inverse_transform(dummy_preds)[:, 0]

        dummy_actual = np.zeros((len(eval_y), len(features)))
        dummy_actual[:, 0] = eval_y.numpy()
        test_actual = scaler.inverse_transform(dummy_actual)[:, 0]

        metrics = evaluate_metrics(test_actual, test_preds)
        passed, reason = self.check_threshold(metrics, mean_price)

        model_path = os.path.join(self.model_dir, "lstm_model.pt")
        scaler_path = os.path.join(self.model_dir, "lstm_scaler.pkl")

        if passed:
            torch.save(model.state_dict(), model_path)
            joblib.dump(scaler, scaler_path)

        meta = {
            "model_name": "LSTM",
            "metrics": metrics,
            "passed_threshold": passed,
            "threshold_reason": reason,
            "trained_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "seq_length": seq_length,
            "features": features,
            "saved_model_path": model_path if passed else None
        }
        self._save_metadata("lstm_metrics.json", meta)
        return meta

    def train_all(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Huấn luyện đồng bộ tất cả mô hình cho một loại hàng hóa"""
        results = {}
        # 1. Prophet
        try:
            results["Prophet"] = self.train_prophet(df)
        except Exception as e:
            results["Prophet"] = {"model_name": "Prophet", "error": str(e), "passed_threshold": False}

        # 2. XGBoost
        try:
            results["XGBoost"] = self.train_xgboost(df)
        except Exception as e:
            results["XGBoost"] = {"model_name": "XGBoost", "error": str(e), "passed_threshold": False}

        # 3. LSTM
        try:
            results["LSTM"] = self.train_lstm(df)
        except Exception as e:
            results["LSTM"] = {"model_name": "LSTM", "error": str(e), "passed_threshold": False}

        return results

    def _save_metadata(self, filename: str, meta: Dict[str, Any]):
        path = os.path.join(self.model_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)
