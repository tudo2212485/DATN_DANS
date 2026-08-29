import pandas as pd
import numpy as np

def create_features(df: pd.DataFrame, target_col: str = 'price') -> pd.DataFrame:
    """
    Creates lag features, rolling statistics, and datetime features
    for tabular machine learning models (XGBoost, Random Forest).
    """
    df = df.copy()
    
    # Ensure it's sorted by date just in case
    df = df.sort_values(by='record_date').reset_index(drop=True)
    
    # 1. Datetime features (Seasonality)
    df['record_date'] = pd.to_datetime(df['record_date'])
    df['day_of_week'] = df['record_date'].dt.dayofweek
    df['month'] = df['record_date'].dt.month
    df['quarter'] = df['record_date'].dt.quarter
    
    # 2. Lag features (t-1, t-2, t-3, t-7, t-14)
    lags = [1, 2, 3, 7, 14]
    for lag in lags:
        df[f'{target_col}_lag_{lag}'] = df[target_col].shift(lag)
        
    # 3. Rolling Statistics
    windows = [7, 14]
    for w in windows:
        df[f'rolling_mean_{w}d'] = df[target_col].shift(1).rolling(window=w).mean()
        df[f'rolling_std_{w}d'] = df[target_col].shift(1).rolling(window=w).std()
        
    # Drop rows with NaN values created by shifting/rolling
    df.dropna(inplace=True)
    
    return df
