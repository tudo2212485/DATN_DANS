# Phase 4 Specification: Machine Learning Models & Prediction API

## 1. Mục Tiêu (Objective)
Xây dựng, huấn luyện và đánh giá các mô hình học máy (Prophet, XGBoost, PyTorch/LSTM) phục vụ dự báo giá hàng hóa trong tương lai (7 ngày, 30 ngày), đồng thời tạo các API endpoints phục vụ dữ liệu dự báo cho Frontend.

## 2. Đặc Tả Chi Tiết Mô Hình Machine Learning

### 2.1 Các Mô Hình Sử Dụng (ML Algorithms)
- **Facebook Prophet:** Sử dụng cho các chuỗi thời gian có tính chu kỳ (seasonality) cao.
- **XGBoost Regressor:** Dự báo dựa trên các thuộc tính kết hợp (giá quá quứ, khối lượng giao dịch, chỉ số kỹ thuật).
- **LSTM / Neural Network (PyTorch):** Dự báo biến động giá phức tạp phi tuyến tính.

### 2.2 Quy Trình Huấn Luyện (Training Pipeline)
```text
[ Preprocessed Data ] ──► [ Feature Engineering ] ──► [ Model Training ] ──► [ Model Evaluation (RMSE/MAE) ] ──► [ Save Weights (.pkl / .pt) ]
```

### 2.3 Caching & Prediction Serving
- Lưu mô hình đã huấn luyện vào thư mục `app/ml_pipeline/saved_models/`.
- Tự động retrain định kỳ khi có dữ liệu mới.
- Cache kết quả dự báo trong bộ nhớ để phục vụ API nhanh chóng (<100ms response time).

## 3. Đặc Tả API Endpoints (ML Services)
- `GET /api/v1/predictions/forecast?symbol=COPPER&days=7`: Lấy kết quả dự báo giá trong 7 ngày tới.
- `GET /api/v1/predictions/metrics`: Lấy các chỉ số đánh giá độ chính xác mô hình (MAE, RMSE, R2 Score).

## 4. Bảo Mật & Tối Ưu Hiệu Năng
- Async Execution: Chạy dự báo trong background thread/process để không làm nghẽn Event Loop của FastAPI.
- Rate Limiting đối với các API gọi tính toán heavy ML.

## 5. Kiểm Thử (Testing & Evaluation)
- Viết test case đánh giá RMSE của mô hình phải nhỏ hơn ngưỡng cho phép trước khi deploy weights mới.
- Test API trả về đủ cấu hình dữ liệu JSON cho biểu đồ Frontend (ngày, giá dự đoán, khoảng tin cậy `yhat_lower`, `yhat_upper`).

## 6. Sản Phẩm Bàn Giao (Deliverables)
1. Các module huấn luyện: `model_trainer.py`, `predictor.py`.
2. Model weights đã được lưu.
3. API endpoints trả về kết quả dự báo hoạt động chính xác.
