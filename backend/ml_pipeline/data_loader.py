import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf
from statsmodels.tsa.stattools import adfuller

# Ensure UTF-8 output on Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.models.models import Commodity, PriceHistory

def get_exogenous_data(start_date: str, end_date: str) -> pd.DataFrame:
    """Fetch exogenous variables from Yahoo Finance"""
    print(f"Fetching Exogenous Variables (USD/VND, Crude Oil) from {start_date} to {end_date}...")
    try:
        # Fetch USD/VND
        usdvnd = yf.download("VND=X", start=start_date, end=end_date, progress=False)
        usdvnd = usdvnd[['Close']].rename(columns={'Close': 'usd_vnd'})
        
        # Fetch Crude Oil WTI
        oil = yf.download("CL=F", start=start_date, end=end_date, progress=False)
        oil = oil[['Close']].rename(columns={'Close': 'crude_oil'})
        
        # Merge them
        df_exo = usdvnd.join(oil, how='outer')
        
        # Flatten MultiIndex columns if any
        if isinstance(df_exo.columns, pd.MultiIndex):
            df_exo.columns = df_exo.columns.get_level_values(0)
            
        df_exo = df_exo.reset_index()
        df_exo['Date'] = pd.to_datetime(df_exo['Date']).dt.date
        df_exo.rename(columns={'Date': 'record_date'}, inplace=True)
        
        # Forward fill and backward fill missing values
        df_exo.ffill(inplace=True)
        df_exo.bfill(inplace=True)
        
        return df_exo
    except Exception as e:
        print(f"Error fetching exogenous data: {e}")
        return pd.DataFrame()

def handle_outliers_iqr(df: pd.DataFrame, column: str = 'price') -> pd.DataFrame:
    """Cap outliers using the IQR method"""
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Cap values instead of dropping to maintain time series continuity
    df[column] = np.where(df[column] < lower_bound, lower_bound, df[column])
    df[column] = np.where(df[column] > upper_bound, upper_bound, df[column])
    return df

def test_stationarity(series: pd.Series):
    """Perform Augmented Dickey-Fuller test"""
    result = adfuller(series.dropna())
    print(f'ADF Statistic: {result[0]:.4f}')
    print(f'p-value: {result[1]:.4f}')
    if result[1] <= 0.05:
        print("=> Data is stationary")
    else:
        print("=> Data is non-stationary")
    return result[1]

def load_clean_data(commodity_id: int, db_session) -> pd.DataFrame:
    """Load commodity data, clean it, and merge with exogenous variables."""
    # 1. Fetch commodity history
    history = db_session.query(PriceHistory).filter(PriceHistory.commodity_id == commodity_id).order_by(PriceHistory.record_date).all()
    if not history:
        return pd.DataFrame()
        
    dates = [h.record_date for h in history]
    prices = [float(h.price) for h in history]
    
    df = pd.DataFrame({"record_date": dates, "price": prices})
    df['record_date'] = pd.to_datetime(df['record_date']).dt.date
    
    # 2. Handle missing dates by creating a full date range
    full_date_range = pd.date_range(start=df['record_date'].min(), end=df['record_date'].max(), freq='D')
    full_df = pd.DataFrame({"record_date": full_date_range.date})
    df = pd.merge(full_df, df, on="record_date", how="left")
    
    # 3. Missing Value Imputation (Linear Interpolation)
    df['price'] = df['price'].interpolate(method='linear').ffill().bfill()
    
    # 4. Outlier Handling
    df = handle_outliers_iqr(df, 'price')
    
    # 5. Stationarity Test
    print(f"--- Stationarity Test for Commodity {commodity_id} ---")
    test_stationarity(df['price'])
    
    # 6. Fetch and Merge Exogenous Variables
    start_date = df['record_date'].min().strftime('%Y-%m-%d')
    end_date = (df['record_date'].max() + timedelta(days=1)).strftime('%Y-%m-%d') # yfinance end date is exclusive
    
    df_exo = get_exogenous_data(start_date, end_date)
    
    if not df_exo.empty:
        df = pd.merge(df, df_exo, on='record_date', how='left')
        # Fill missing exogenous after merge
        df.ffill(inplace=True)
        df.bfill(inplace=True)
    else:
        print("Warning: Exogenous data not available. Proceeding without them.")
        df['usd_vnd'] = 25000.0
        df['crude_oil'] = 75.0
        
    return df
