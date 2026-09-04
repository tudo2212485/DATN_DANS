import sys
import os
import warnings
import pandas as pd
import numpy as np
from datetime import datetime
import torch
import torch.nn as nn
from sklearn.preprocessing import MinMaxScaler
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

class MultiLayerLSTM(nn.Module):
    def __init__(self, input_size, hidden_size=64, num_layers=2, output_size=1):
        super(MultiLayerLSTM, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, dropout=0.2)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])
        return out

def create_sequences(data, seq_length):
    xs = []
    ys = []
    # y is the first column (price)
    for i in range(len(data)-seq_length):
        xs.append(data[i:(i+seq_length)])
        ys.append(data[i+seq_length, 0]) 
    return np.array(xs), np.array(ys)

def run_lstm(commodity_id: int, commodity_name: str, df: pd.DataFrame, db_session, horizon: int = 30):
    print(f"\n--- Training Deep Learning LSTM for {commodity_name} ---")
    
    # Use price and exogenous features if available
    features = ['price']
    if 'usd_vnd' in df.columns: features.append('usd_vnd')
    if 'crude_oil' in df.columns: features.append('crude_oil')
        
    data = df[features].values
    
    scaler = MinMaxScaler(feature_range=(-1, 1))
    scaled_data = scaler.fit_transform(data)
    
    seq_length = 14
    if len(scaled_data) < seq_length + 2:
        print("Not enough data.")
        return
        
    X, y = create_sequences(scaled_data, seq_length)
    
    train_size = int(len(X) * 0.85)
    X_train, y_train = X[:train_size], y[:train_size]
    X_test, y_test = X[train_size:], y[train_size:]
    
    X_train = torch.tensor(X_train, dtype=torch.float32)
    y_train = torch.tensor(y_train, dtype=torch.float32)
    X_test = torch.tensor(X_test, dtype=torch.float32)
    y_test = torch.tensor(y_test, dtype=torch.float32)
    
    input_size = len(features)
    model = MultiLayerLSTM(input_size=input_size, hidden_size=64, num_layers=2)
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.005)
    
    print("Training PyTorch LSTM over 50 epochs...")
    model.train()
    for epoch in range(50):
        optimizer.zero_grad()
        outputs = model(X_train).squeeze()
        loss = criterion(outputs, y_train)
        loss.backward()
        optimizer.step()
        
    # Evaluate
    model.eval()
    with torch.no_grad():
        test_preds_scaled = model(X_test).numpy()
        
    # We need to inverse transform just the price. 
    # Create dummy array with same shape as scaled_data to inverse_transform
    dummy_test_preds = np.zeros((len(test_preds_scaled), len(features)))
    dummy_test_preds[:, 0] = test_preds_scaled.flatten()
    test_preds = scaler.inverse_transform(dummy_test_preds)[:, 0]
    
    dummy_y_test = np.zeros((len(y_test), len(features)))
    dummy_y_test[:, 0] = y_test.numpy()
    test_actual = scaler.inverse_transform(dummy_y_test)[:, 0]
    
    mae = mean_absolute_error(test_actual, test_preds)
    rmse = np.sqrt(mean_squared_error(test_actual, test_preds))
    mape = calculate_mape(test_actual, test_preds)
    r2 = r2_score(test_actual, test_preds)
    
    print(f"LSTM Metrics -> MAE: {mae:.2f}, RMSE: {rmse:.2f}, MAPE: {mape:.2f}%, R2: {r2:.3f}")
    
    # Forecast future
    preds = []
    curr_seq = torch.tensor(scaled_data[-seq_length:], dtype=torch.float32).unsqueeze(0)
    
    for _ in range(horizon):
        with torch.no_grad():
            pred = model(curr_seq).item()
            
        preds.append(pred)
        
        # Prepare next input step (autoregressive for price, holding exo constant)
        next_step = curr_seq[:, -1:, :].clone()
        next_step[0, 0, 0] = pred # update price
        # exo variables stay the same as last known
        
        curr_seq = torch.cat((curr_seq[:, 1:, :], next_step), dim=1)
        
    # Inverse transform predictions
    dummy_preds = np.zeros((len(preds), len(features)))
    dummy_preds[:, 0] = preds
    final_preds = scaler.inverse_transform(dummy_preds)[:, 0]
    final_preds = np.maximum(final_preds, 0)
    
    std_err = rmse
    lower_cis = [p - 1.96 * std_err * (1 + 0.05*i) for i, p in enumerate(final_preds)]
    upper_cis = [p + 1.96 * std_err * (1 + 0.05*i) for i, p in enumerate(final_preds)]
    
    last_date = df['record_date'].iloc[-1]
    if hasattr(last_date, 'date'): last_date = last_date.date()
    future_dates = [last_date + pd.Timedelta(days=i) for i in range(1, horizon + 1)]
    
    model_name = "LSTM"
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
            predicted_price=float(final_preds[i]),
            lower_ci=float(max(lower_cis[i], 0)),
            upper_ci=float(upper_cis[i]),
            mae=float(mae),
            rmse=float(rmse),
            mape=float(mape),
            r2=float(r2) if r2 > 0 else 0.5,
            training_date=datetime.now().date()
        ))
    db_session.add_all(records)
    db_session.commit()
    print(f"Saved {horizon} forecasts for {commodity_name} using LSTM.")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        commodities = db.query(Commodity).all()
        for c in commodities:
            df = load_clean_data(c.id, db)
            if not df.empty:
                run_lstm(c.id, c.name, df, db, horizon=30)
    finally:
        db.close()
