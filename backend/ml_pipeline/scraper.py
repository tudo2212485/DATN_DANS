import sys
import os
import pandas as pd
from datetime import datetime, timedelta

# Try importing yfinance, if not available, we'll install it later.
try:
    import yfinance as yf
except ImportError:
    print("yfinance not found. Please run 'pip install yfinance'")
    sys.exit(1)

# Ensure UTF-8 output on Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Add backend directory to sys.path to import SQLAlchemy models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.models.models import Commodity, PriceHistory

# Map local commodity codes to Yahoo Finance tickers
TICKER_MAP = {
    "RICE_IR504": "ZR=F",      # Rough Rice Futures
    "COFFEE_ROBUSTA": "KC=F",  # Coffee C Futures
    "PEPPER_BLACK": "SB=F",    # Sugar (as placeholder if pepper isn't available)
    "RUBBER_SVR3L": "RUBBER.T" # Placeholder/approximate
}
DEFAULT_TICKER = "ZC=F" # Corn as default agricultural commodity

def fetch_yfinance_data(ticker_symbol: str, days: int = 365) -> pd.DataFrame:
    """Fetch historical data from Yahoo Finance."""
    print(f"Fetching data for ticker: {ticker_symbol}")
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Download data
        ticker = yf.Ticker(ticker_symbol)
        df = ticker.history(start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))
        
        if df.empty:
            print(f"No data found for {ticker_symbol}.")
            return pd.DataFrame()
            
        # Reset index to get Date as column
        df = df.reset_index()
        # Convert timezone-aware datetime to timezone-naive date
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        
        # We only need Date, Close, Low, High, Volume
        df = df[['Date', 'Close', 'Low', 'High', 'Volume']]
        df.columns = ['record_date', 'price', 'price_min', 'price_max', 'volume']
        
        # Forward fill any missing values just in case
        df = df.ffill()
        
        return df
    except Exception as e:
        print(f"Error fetching data for {ticker_symbol}: {e}")
        return pd.DataFrame()

def scrape_and_update_db(days: int = 365):
    """Fetch data for all commodities and update the database."""
    print("==================================================")
    print("BẮT ĐẦU CÀO DỮ LIỆU TỪ YAHOO FINANCE")
    print("==================================================")
    
    db = SessionLocal()
    
    try:
        commodities = db.query(Commodity).all()
        if not commodities:
            print("Không tìm thấy nông sản nào trong CSDL.")
            return

        for c in commodities:
            ticker = TICKER_MAP.get(c.code, DEFAULT_TICKER)
            print(f"[{c.name}] ({c.code}) -> Ánh xạ tới mã Ticker: {ticker}")
            
            df = fetch_yfinance_data(ticker, days=days)
            
            if df.empty:
                print(f"Bỏ qua {c.name} do không lấy được dữ liệu.")
                continue
                
            # Scale the price to match local currency scale (VND) if needed
            last_price_record = db.query(PriceHistory).filter(PriceHistory.commodity_id == c.id).order_by(PriceHistory.record_date.desc()).first()
            scale_factor = 1.0
            
            if last_price_record and float(last_price_record.price) > 5000:
                avg_yfinance_price = df['price'].mean()
                if avg_yfinance_price > 0:
                    scale_factor = float(last_price_record.price) / avg_yfinance_price
            
            print(f"Hệ số điều chỉnh giá (Scale Factor): {scale_factor:.2f}")

            # Delete old data
            db.query(PriceHistory).filter(PriceHistory.commodity_id == c.id).delete()
            
            records_to_insert = []
            for _, row in df.iterrows():
                ph = PriceHistory(
                    commodity_id=c.id,
                    record_date=row['record_date'],
                    price=row['price'] * scale_factor,
                    price_min=row['price_min'] * scale_factor,
                    price_max=row['price_max'] * scale_factor,
                    volume=row['volume'],
                    source="Yahoo Finance (Real Data)"
                )
                records_to_insert.append(ph)
                
            db.add_all(records_to_insert)
            db.commit()
            print(f"Đã lưu {len(records_to_insert)} bản ghi giá cho {c.name}.")

        print("==================================================")
        print("HOÀN TẤT CÀO DỮ LIỆU!")
        print("==================================================")
    finally:
        db.close()

if __name__ == "__main__":
    scrape_and_update_db(days=730) # 2 years of history
