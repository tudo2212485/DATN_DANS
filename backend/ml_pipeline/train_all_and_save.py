import os
import sys
import warnings
import pandas as pd
from datetime import datetime

# Set UTF-8 encoding on Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

warnings.filterwarnings("ignore")

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(CURRENT_DIR)
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app.core.database import SessionLocal
from app.models.models import Commodity, Forecast
from ml_pipeline.data_loader import load_clean_data
from ml_pipeline.model_trainer import ModelTrainer
from ml_pipeline.predictor import PricePredictor, clear_prediction_cache


def train_and_persist_all_commodities(horizon: int = 30):
    """
    Huấn luyện toàn bộ mô hình (Prophet, XGBoost, PyTorch LSTM),
    lưu model weights vào thư mục saved_models/ và lưu kết quả dự báo vào CSDL.
    """
    db = SessionLocal()
    print("=" * 60)
    print("  BẮT ĐẦU QUY TRÌNH HUẤN LUYỆN VÀ LƯU WEIGHTS MACHINE LEARNING")
    print("=" * 60)
    
    try:
        commodities = db.query(Commodity).all()
        if not commodities:
            print("Chưa có danh mục nông sản trong CSDL.")
            return

        for c in commodities:
            print(f"\n>>> Đang xử lý nông sản: [{c.code}] {c.name} (ID: {c.id})")
            df = load_clean_data(c.id, db)
            
            if df.empty or len(df) < 10:
                print(f"Bỏ qua {c.name}: Không đủ dữ liệu ({len(df)} dòng).")
                continue

            # 1. Huấn luyện và lưu weights
            trainer = ModelTrainer(commodity_code=c.code, max_rmse_threshold_ratio=0.35)
            training_results = trainer.train_all(df)

            # 2. Sử dụng Predictor để tạo dự báo 30 ngày và lưu vào bảng Forecasts trong CSDL
            predictor = PricePredictor(c.code, db=db)
            
            for model_name in ["Prophet", "XGBoost", "LSTM"]:
                try:
                    res = predictor.forecast(model_name=model_name, days=horizon, use_cache=False)
                    forecast_points = res.get("forecast", [])
                    metrics = res.get("metrics", {})
                    
                    if not forecast_points:
                        continue

                    # Xóa dự báo cũ của model này
                    db.query(Forecast).filter(
                        Forecast.commodity_id == c.id,
                        Forecast.model_name == model_name
                    ).delete()

                    new_records = []
                    for pt in forecast_points:
                        f_date = datetime.strptime(pt["date"], "%Y-%m-%d").date()
                        new_records.append(
                            Forecast(
                                commodity_id=c.id,
                                model_name=model_name,
                                forecast_date=f_date,
                                predicted_price=pt["yhat"],
                                lower_ci=pt["yhat_lower"],
                                upper_ci=pt["yhat_upper"],
                                mae=float(metrics.get("mae", 0.0)),
                                rmse=float(metrics.get("rmse", 0.0)),
                                mape=float(metrics.get("mape", 0.0)),
                                r2=float(metrics.get("r2", 0.5)),
                                training_date=datetime.now().date()
                            )
                        )
                    db.add_all(new_records)
                    db.commit()
                    print(f"  + Đã lưu dự báo {model_name}: MAE={metrics.get('mae', 0):.2f}, RMSE={metrics.get('rmse', 0):.2f}, R2={metrics.get('r2', 0):.3f}")
                except Exception as e:
                    print(f"  - Lỗi khi tạo dự báo {model_name} cho {c.name}: {e}")

        # Xóa cache để cập nhật dữ liệu mới nhất
        clear_prediction_cache()
        print("\n" + "=" * 60)
        print("  HOÀN THÀNH QUY TRÌNH HUẤN LUYỆN VÀ LƯU WEIGHTS THÀNH CÔNG!")
        print("=" * 60)
    finally:
        db.close()


if __name__ == "__main__":
    train_and_persist_all_commodities(horizon=30)
