# -*- coding: utf-8 -*-
"""
Chương 4: CÀI ĐẶT, THỰC NGHIỆM 5 MÔ HÌNH HỌC MÁY, KIỂM THỬ VÀ BẢO MẬT HỆ THỐNG
KẾT LUẬN, HƯỚNG PHÁT TRIỂN, TÀI LIỆU THAM KHẢO, PHỤ LỤC
"""

CHUONG_4_DATA = {
    "title": "Chương 4: CÀI ĐẶT, THỰC NGHIỆM 5 MÔ HÌNH HỌC MÁY, KIỂM THỬ VÀ BẢO MẬT HỆ THỐNG",
    "sections": [
        {
            "code": "4.1.",
            "title": "Môi trường cài đặt và bộ dữ liệu thực nghiệm của hệ thống",
            "subsections": [
                {
                    "code": "4.1.1.",
                    "title": "Cấu hình môi trường phần cứng, phần mềm và thư viện triển khai",
                    "paragraphs": [
                        "Hệ thống AgroForecast được cài đặt, huấn luyện thực nghiệm và kiểm thử trên môi trường máy trạm phát triển với cấu hình phần cứng và phần mềm tiêu chuẩn. Tầng Backend sử dụng Python 3.11.9, FastAPI, Uvicorn ASGI Server, SQLAlchemy 2.0, Pydantic v2, APScheduler và hệ quản trị cơ sở dữ liệu PostgreSQL 17 (12 bảng chuẩn hóa). Tầng Học máy (Machine Learning Pipeline) sử dụng PyTorch (cho mạng học sâu Stacked LSTM 7 kênh), Facebook Prophet, Statsmodels (cho ARIMA), XGBoost, Scikit-learn (cho Random Forest và các độ đo đánh giá), Pandas và NumPy, kết hợp biến ngoại sinh nhân quả USD/VND (VND=X) và Dầu thô WTI (CL=F). Tầng Frontend sử dụng Node.js 20, Next.js 14.2, React 18, TypeScript 5, TailwindCSS, bộ thành phần doanh nghiệp Syncfusion Essential Studio EJ2 React (AgroGrid, FinChart) và Recharts; toàn bộ 3 tầng được đóng gói triển khai qua Docker Compose.",
                    ],
                },
                {
                    "code": "4.1.2.",
                    "title": "Thống kê bộ dữ liệu lịch sử thực nghiệm của 8 mặt hàng nông sản trong PostgreSQL",
                    "paragraphs": [
                        "Dữ liệu lịch sử giá giai đoạn 2024–2026 của 8 mặt hàng nông sản chủ lực được tổ chức minh bạch theo 3 nhóm nguồn gốc và lưu trữ xác thực (provenance = 'collected') trong bảng price_history với tổng cộng 4.899 bản ghi cùng 9.079 quan sát khảo sát tách riêng theo cấp tỉnh trong bảng regional_price_observations: (1) Nhóm 3 mặt hàng chủ lực đạt 100% URL bài báo kiểm chứng riêng từng ngày (Lúa gạo IR50404: 442 phiên vietnambiz.vn & VFA vietfood.org.vn; Cà phê Robusta: 919 phiên vietnambiz.vn & giacaphe.com; Hồ tiêu đen: 793 phiên vietnambiz.vn); (2) Nhóm Mía đường 10 CCS (729 phiên) quy đổi minh bạch từ sàn ICE Sugar #11 (Yahoo Finance SB=F x USD/VND) kết hợp 8 bài báo khảo sát vụ ép 2024–2026 tại Khánh Hòa, Phú Yên, Gia Lai; và (3) Nhóm 4 đặc sản mở rộng (Dâu tây Đà Lạt, Khoai tây Đà Lạt, Khoai lang tím Vĩnh Long, Hạt điều — 504 phiên/mặt hàng) neo giá khảo sát sống tại Việt Nam (kamereo.vn, namtinhvegetable.com, banggianongsan.com) kết hợp chuỗi tham chiếu Proxy Index ETF Yahoo Finance (DBA, MOO, CORN, SOYB x USD/VND) do thị trường rau củ nội địa không niêm yết giá hằng ngày nhiều năm.",
                        "Lưu ý về mốc thời gian thực nghiệm: Toàn bộ số liệu bảng biểu và chỉ số đánh giá mô hình trình bày trong Chương 4 được chốt tại mốc ngày 23/11/2026 để bảo đảm tính nhất quán học thuật khi đối chiếu; trong quá trình vận hành thực tế, hệ thống AgroForecast tiếp tục tự động thu thập dữ liệu phiên mới và tái huấn luyện hằng ngày qua bộ lập lịch nền APScheduler (06:00 và 18:00 GMT+7). Bảng 4.1 trình bày thống kê chi tiết tại mốc chốt 23/11/2026.",
                    ],
                    "tables": [
                        {
                            "caption": "Bảng 4.1. Thống kê bộ dữ liệu lịch sử thực nghiệm của 8 loại nông sản trong CSDL PostgreSQL (chốt mốc 23/11/2026)",
                            "headers": ["ID", "Mã nông sản", "Tên nông sản", "Địa phương chuẩn (Tại vườn/ruộng)", "Số bản ghi", "Giai đoạn dữ liệu", "Giá mới nhất"],
                            "rows": [
                                ["1", "RICE_IR504", "Lúa gạo IR50404", "Huyện Châu Phú, An Giang (Tại ruộng)", "442", "01/01/2024 - 23/11/2026", "6.850 VNĐ/kg"],
                                ["2", "COFFEE_ROBUSTA", "Cà phê Robusta", "Huyện Cư M'gar, Đắk Lắk (Tại vườn)", "919", "04/01/2024 - 23/11/2026", "71.700 VNĐ/kg"],
                                ["3", "PEPPER_BLACK", "Hồ tiêu đen", "Huyện Chư Sê, Gia Lai (Tại vườn)", "793", "04/01/2024 - 23/11/2026", "129.100 VNĐ/kg"],
                                ["4", "SUGARCANE", "Mía đường 10 CCS", "Huyện Tây Hòa, Phú Yên / Khánh Hòa", "729", "02/01/2024 - 23/11/2026", "1.230.000 VNĐ/tấn"],
                                ["5", "STRAWBERRY", "Dâu tây Đà Lạt", "Phường 8, Đà Lạt (Tại vườn)", "504", "21/11/2024 - 23/11/2026", "100.000 VNĐ/kg"],
                                ["6", "POTATO", "Khoai tây Đà Lạt", "Phường 7, Đà Lạt (Tại vườn)", "504", "21/11/2024 - 23/11/2026", "20.000 VNĐ/kg"],
                                ["7", "SWEET_POTATO", "Khoai lang tím Vĩnh Long", "Huyện Bình Tân, Vĩnh Long (Tại ruộng)", "504", "21/11/2024 - 23/11/2026", "16.000 VNĐ/kg"],
                                ["8", "CASHEW_NUT", "Hạt điều thô", "Huyện Bù Đăng, Bình Phước (Tại vườn)", "504", "21/11/2024 - 23/11/2026", "32.500 VNĐ/kg"],
                            ],
                        }
                    ],
                },
            ],
        },
        {
            "code": "4.2.",
            "title": "Kết quả thực nghiệm huấn luyện và đánh giá sai số của 5 mô hình học máy",
            "subsections": [
                {
                    "code": "4.2.1.",
                    "title": "Thiết lập siêu tham số (Hyperparameters) & Đặc trưng ngoại sinh nhân quả cho 5 mô hình",
                    "paragraphs": [
                        "Để đảm bảo tính công bằng, chống rò rỉ dữ liệu tuyệt đối (Zero Data Leakage) và khả năng tái lập khoa học (random_state = 42), cả 5 mô hình được huấn luyện bằng phương pháp dự báo lợi suất log (Stationary Log-Return) và kiểm định Walk-Forward cuộn 7 ngày trong app/services/training_service.py và ml_pipeline/history_models.py:",
                        "1. Mô hình PyTorch Stacked LSTM (7 kênh nhân quả): Kiến trúc 2 tầng ẩn (num_layers = 2, hidden_size = 24), độ dài chuỗi seq_length = 14 ngày, 7 kênh đầu vào gồm [lợi suất log r_t, độ lệch trung bình động MA7, biến động thực tế Vol7, sin/cos chu kỳ năm, lợi suất tỷ giá USD/VND và lợi suất dầu thô WTI <= t-1], tối ưu hóa AdamW (lr = 0.002, weight_decay = 1e-2) và SmoothL1Loss. Bộ chuẩn hóa StandardScaler chỉ fit duy nhất trên tập Train.",
                        "2. Mô hình Facebook Prophet (trên miền Log): Cấu hình seasonal Fourier năm/tuần thích nghi theo độ dài chuỗi (changepoint_prior_scale = 0.01, seasonality_prior_scale = 0.15), neo gốc nhân quả tại điểm quan sát cuối t0 giúp triệt tiêu hiện tượng đứt gãy mức giá tại điểm chuyển giao lịch sử - dự báo.",
                        "3. Mô hình ARIMA (trên miền Log): Tự động tuyển chọn bậc ổn định từ tập ứng viên {(2,1,1), (1,1,1), (1,1,0), (0,1,0)} trên tập Train và áp dụng tham số đóng băng (.apply()) lên từng cửa sổ kiểm định Walk-Forward (không tái khớp lên tập Test).",
                        "4. Mô hình XGBoost Regressor (22 đặc trưng nhân quả): Cấu hình n_estimators = 160, max_depth = 3, learning_rate = 0.03, subsample = 0.8, colsample_bytree = 0.8, điều chuẩn L1/L2 (reg_alpha = 0.5, reg_lambda = 8.0) trên 18 đặc trưng trễ/động lượng/biến động/lịch + 4 đặc trưng ngoại sinh trễ (fx_r1, fx_mom7, oil_r1, oil_mom7).",
                        "5. Mô hình Random Forest Regressor (22 đặc trưng nhân quả): Cấu hình n_estimators = 150 cây quyết định, max_depth = 6, max_features = 'sqrt' trên cùng tập 22 đặc trưng nhân quả, kèm hiệu chỉnh khoảng tin cậy Conformal 95% mở rộng theo sqrt(h).",
                    ],
                },
                {
                    "code": "4.2.2.",
                    "title": "Bảng tổng hợp và phân tích sai số thực nghiệm Walk-Forward 7 ngày của 5 mô hình trên 8 nông sản",
                    "paragraphs": [
                        "Quá trình thực nghiệm đã tiến hành huấn luyện và kiểm định Walk-Forward cuộn 7 ngày (Zero Data Leakage, tích hợp biến ngoại sinh USD/VND & WTI) cho toàn bộ 40 tổ hợp (8 mặt hàng nông sản x 5 mô hình học máy). Bảng 4.2 trình bày đầy đủ số liệu sai số thực tế (MAE, RMSE, MAPE, R2 và độ phủ thực nghiệm 95% CI - PICP) trích xuất trực tiếp từ bảng training_runs và forecasts trong PostgreSQL ngày 23/11/2026.",
                    ],
                    "tables": [
                        {
                            "caption": "Bảng 4.2. Kết quả thực nghiệm Walk-Forward 7 ngày (có biến ngoại sinh USD/VND & WTI) của 5 mô hình AI trên 8 mặt hàng nông sản",
                            "headers": ["Nông sản", "Mô hình AI", "MAE (VNĐ)", "RMSE (VNĐ)", "MAPE (%)", "Hệ số R2", "Đánh giá / Xếp hạng (PICP 95%)"],
                            "rows": [
                                ["Lúa IR50404", "ARIMA", "100,24", "169,20", "1,58%", "0,5340", "Tối ưu nhất ★ (Hạng 1 - PICP 89,4%)"],
                                ["Lúa IR50404", "Prophet", "100,13", "156,67", "1,59%", "0,6005", "Hạng 2 - RMSE thấp nhất & R2 cao nhất (PICP 89,4%)"],
                                ["Lúa IR50404", "XGBoost", "104,50", "170,92", "1,65%", "0,5244", "Hạng 3 (PICP 87,9%)"],
                                ["Lúa IR50404", "Random Forest", "105,29", "170,13", "1,67%", "0,5288", "Hạng 4 (PICP 89,4%)"],
                                ["Lúa IR50404", "LSTM", "111,45", "171,72", "1,77%", "0,5200", "Hạng 5 (PICP 89,4%)"],
                                ["Cà phê Robusta", "PyTorch LSTM", "1.555,41", "1.978,28", "1,79%", "0,8972", "Tối ưu nhất ★ (Hạng 1 — Vượt Baseline 1,88%, PICP 92,2%)"],
                                ["Cà phê Robusta", "ARIMA", "1.605,21", "2.121,40", "1,86%", "0,8818", "Hạng 2 - Vượt Baseline 1,88% (PICP 90,0%)"],
                                ["Cà phê Robusta", "Random Forest", "1.643,09", "2.087,40", "1,90%", "0,8856", "Hạng 3 - RMSE thấp thứ 2 (PICP 90,0%)"],
                                ["Cà phê Robusta", "XGBoost", "1.703,99", "2.120,44", "1,96%", "0,8819", "Hạng 4 (PICP 92,2%)"],
                                ["Cà phê Robusta", "Prophet", "1.882,04", "2.386,65", "2,15%", "0,8504", "Hạng 5 (PICP 87,8%)"],
                                ["Hồ tiêu đen", "ARIMA", "990,46", "1.643,77", "0,74%", "0,3256", "Tối ưu nhất ★ (Vượt Baseline RMSE 1.646,34 - PICP 94,4%)"],
                                ["Hồ tiêu đen", "XGBoost", "1.045,64", "1.646,95", "0,78%", "0,3230", "Hạng 2 - Sai số cực thấp (PICP 94,4%)"],
                                ["Hồ tiêu đen", "Random Forest", "1.054,90", "1.631,93", "0,78%", "0,3353", "Hạng 3 - RMSE thấp nhất & R2 cao nhất (PICP 94,4%)"],
                                ["Hồ tiêu đen", "LSTM", "1.070,99", "1.729,36", "0,79%", "0,2536", "Hạng 4 - Đạt chuẩn < 1% (PICP 92,2%)"],
                                ["Hồ tiêu đen", "Prophet", "1.174,41", "1.708,35", "0,87%", "0,2716", "Hạng 5 (PICP 94,4%)"],
                                ["Mía đường 10 CCS", "Prophet", "34.245,40", "46.011,00", "2,62%", "0,8571", "Tối ưu nhất ★ (Vượt Baseline 2,74% - PICP 97,8%)"],
                                ["Mía đường 10 CCS", "Random Forest", "35.303,99", "48.177,63", "2,70%", "0,8434", "Hạng 2 - Vượt Baseline 2,74% (PICP 96,7%)"],
                                ["Mía đường 10 CCS", "ARIMA", "35.800,52", "47.960,56", "2,74%", "0,8448", "Hạng 3 (PICP 97,8%)"],
                                ["Mía đường 10 CCS", "LSTM", "36.056,90", "48.324,82", "2,75%", "0,8424", "Hạng 4 (PICP 96,7%)"],
                                ["Mía đường 10 CCS", "XGBoost", "36.244,16", "48.578,33", "2,77%", "0,8408", "Hạng 5 (PICP 97,8%)"],
                                ["Dâu tây Đà Lạt", "Prophet", "1.164,79", "1.610,18", "1,08%", "0,8693", "Tối ưu nhất ★ (Vượt sâu Baseline 1,30% - PICP 100%)"],
                                ["Dâu tây Đà Lạt", "ARIMA", "1.393,33", "1.684,24", "1,30%", "0,8570", "Hạng 2 (PICP 100,0%)"],
                                ["Dâu tây Đà Lạt", "XGBoost", "1.398,31", "1.687,84", "1,30%", "0,8564", "Hạng 3 (PICP 100,0%)"],
                                ["Dâu tây Đà Lạt", "Random Forest", "1.400,17", "1.694,39", "1,31%", "0,8553", "Hạng 4 (PICP 100,0%)"],
                                ["Dâu tây Đà Lạt", "LSTM", "1.429,96", "1.864,54", "1,35%", "0,8247", "Hạng 5 (PICP 93,3%)"],
                                ["Khoai tây Đà Lạt", "Prophet", "276,05", "368,60", "1,30%", "0,7119", "Tối ưu nhất ★ (Vượt Baseline 1,39% - PICP 100%)"],
                                ["Khoai tây Đà Lạt", "ARIMA", "295,28", "389,19", "1,40%", "0,6789", "Hạng 2 (PICP 100,0%)"],
                                ["Khoai tây Đà Lạt", "Random Forest", "301,30", "390,70", "1,42%", "0,6764", "Hạng 3 (PICP 100,0%)"],
                                ["Khoai tây Đà Lạt", "XGBoost", "302,97", "399,72", "1,43%", "0,6612", "Hạng 4 (PICP 100,0%)"],
                                ["Khoai tây Đà Lạt", "LSTM", "338,12", "439,38", "1,60%", "0,5907", "Hạng 5 (PICP 98,7%)"],
                                ["Khoai lang tím", "XGBoost", "305,09", "393,93", "1,71%", "0,8844", "Tối ưu nhất ★ (R2 = 0,884 - PICP 97,3%)"],
                                ["Khoai lang tím", "ARIMA", "312,35", "399,68", "1,75%", "0,8810", "Hạng 2 (PICP 97,3%)"],
                                ["Khoai lang tím", "Random Forest", "316,30", "410,99", "1,77%", "0,8741", "Hạng 3 (PICP 97,3%)"],
                                ["Khoai lang tím", "LSTM", "342,59", "437,71", "1,93%", "0,8573", "Hạng 4 (PICP 97,3%)"],
                                ["Khoai lang tím", "Prophet", "348,48", "416,80", "1,97%", "0,8706", "Hạng 5 (PICP 96,0%)"],
                                ["Hạt điều thô", "ARIMA", "444,00", "555,34", "1,30%", "0,8127", "Tối ưu nhất ★ (R2 = 0,813 - PICP 100%)"],
                                ["Hạt điều thô", "XGBoost", "452,95", "561,88", "1,33%", "0,8082", "Hạng 2 (PICP 100,0%)"],
                                ["Hạt điều thô", "LSTM", "459,15", "578,31", "1,35%", "0,7968", "Hạng 3 (PICP 98,7%)"],
                                ["Hạt điều thô", "Random Forest", "477,33", "583,76", "1,40%", "0,7930", "Hạng 4 (PICP 100,0%)"],
                                ["Hạt điều thô", "Prophet", "491,06", "696,47", "1,43%", "0,7053", "Hạng 5 (PICP 97,3%)"],
                            ],
                        }
                    ],
                },
                {
                    "code": "4.2.3.",
                    "title": "Nhận xét và phân tích chuyên sâu kết quả thực nghiệm 5 mô hình",
                    "paragraphs": [
                        "Từ số liệu thực nghiệm Walk-Forward 7 ngày không rò rỉ dữ liệu chốt tại mốc 23/11/2026 trong Bảng 4.2, có thể rút ra ba kết luận khoa học quan trọng chứng minh hiệu quả của kiến trúc đa mô hình kết hợp biến ngoại sinh nhân quả trong AgroForecast:",
                        "Thứ nhất, trên toàn bộ 8/8 mặt hàng nông sản (40/40 tổ hợp mô hình), sai số MAPE của mô hình tối ưu đều nằm rất sâu trong ngưỡng < 3% (từ 0,74% đến 2,62%), đạt chuẩn 'Dự báo độ chính xác rất cao' (< 10%) theo phân loại quốc tế của Lewis, với 40/40 mô hình đều đạt hệ số xác định R2 dương (0,2536 đến 0,8972) và độ bao phủ thực nghiệm khoảng tin cậy 95% Conformal CI đạt 89,4% – 100,0%.",
                        "Thứ hai, việc tích hợp 2 biến ngoại sinh vĩ mô nhân quả (USD/VND và Dầu thô WTI chỉ lấy độ trễ quá khứ <= t-1) phát huy tác dụng mạnh mẽ nhất trên mặt hàng xuất khẩu biến động sâu nhất hệ thống là Cà phê Robusta (919 ngày quan sát thật): mạng học sâu PyTorch Stacked LSTM (7 kênh nhân quả) vươn lên Hạng 1 tuyệt đối trên cả 4 chỉ số với MAE = 1.555,41 VNĐ/kg, RMSE = 1.978,28 VNĐ/kg, MAPE = 1,79%, R2 = 0,8972 và PICP 95% = 92,22%, vượt trội rõ rệt so với Naive Baseline (MAE = 1.621,11, RMSE = 2.147,01 VNĐ/kg, MAPE = 1,88%).",
                        "Thứ ba, kết quả khẳng định định lý No Free Lunch trong dự báo nông sản: không có một mô hình đơn lẻ nào thắng tuyệt đối trên mọi chuỗi. PyTorch Stacked LSTM dẫn đầu trên chuỗi xuất khẩu dày và phi tuyến mạnh (Cà phê Robusta MAPE 1,79%, R2 = 0,8972); ARIMA tối ưu trên chuỗi bước giá hẹp/tự tương quan cao (Hồ tiêu đen 0,74%, Hạt điều 1,30%, Lúa IR50404 1,58%); Prophet dẫn đầu trên chuỗi có xu thế và chu kỳ mùa vụ rõ (Dâu tây Đà Lạt 1,08%, Khoai tây Đà Lạt 1,30%, Mía đường 2,62%); và XGBoost dẫn đầu Khoai lang tím Vĩnh Long (1,71%, R2 = 0,8844). Do đó, cơ chế tự động xếp hạng và gắn sao (★) đề xuất mô hình tối ưu theo từng mặt hàng mang lại giá trị thực tiễn cao.",
                    ],
                },
            ],
        },
        {
            "code": "4.3.",
            "title": "Kiểm thử phần mềm và Kiểm tra bảo mật hệ thống theo chuẩn OWASP Top 10",
            "subsections": [
                {
                    "code": "4.3.1.",
                    "title": "Phương pháp kiểm thử 4 tầng và môi trường kiểm thử cô lập (Sandbox Testing)",
                    "paragraphs": [
                        "Để đảm bảo chất lượng phần mềm đạt chuẩn công nghiệp trước khi nghiệm thu, hệ thống AgroForecast triển khai bộ kiểm thử tự động mở rộng lên 125 kịch bản Pytest Backend (kế thừa bộ nền tảng 72 kịch bản cốt lõi kết hợp nhóm kiểm thử phủ nhánh 98%, kiểm toán sự thật dữ liệu và chống rò rỉ biến ngoại sinh), đi kèm 3 Frontend Unit Tests và 4 Playwright E2E trên trình duyệt thật. Trong tệp cấu hình tests/conftest.py, hệ thống khởi tạo một cơ sở dữ liệu SQLite In-Memory hoàn toàn mới cho từng hàm kiểm thử và sử dụng cơ chế app.dependency_overrides[get_db] để chuyển hướng toàn bộ truy vấn CSDL vào môi trường cô lập này.",
                        "Bốn tầng kiểm thử được thực thi đồng bộ bao gồm: (1) Kiểm thử đơn vị hộp trắng (White-box Unit Testing) cho các hàm toán học lọc ngoại lai IQR, hàm tạo đặc trưng chuỗi thời gian, hàm tính sai số và hàm làm sạch bảo mật; (2) Kiểm thử tích hợp hộp xám (Grey-box API & Database Integration Testing) kiểm tra toàn bộ các Endpoint REST API và tính toàn vẹn khóa ngoại CSDL; (3) Kiểm định đường ống học máy (ML Pipeline Backtesting) kiểm tra huấn luyện thực tế cả 5 mô hình AI, cổng chặn sai số Threshold Gate và điều kiện biên của khoảng tin cậy 95%; và (4) Kiểm thử luồng nghiệp vụ đầu-cuối (End-to-End Workflow Testing).",
                    ],
                },
                {
                    "code": "4.3.2.",
                    "title": "Triển khai 6 lớp phòng vệ bảo mật ứng dụng theo chuẩn OWASP Top 10",
                    "paragraphs": [
                        "Tại mô-đun app/core/security.py, app/core/deps.py và app/main.py, hệ thống đã cài đặt và kiểm chứng thực nghiệm 6 lớp phòng vệ bảo mật trọng yếu:",
                        "Lớp 1 - Băm mật khẩu một chiều Bcrypt với Salt ngẫu nhiên (Chống OWASP A02 - Cryptographic Failures): Sử dụng hàm bcrypt.gensalt() và bcrypt.hashpw() để mã hóa mật khẩu một chiều. Hai lần băm cùng một mật khẩu luôn sinh ra hai chuỗi hash khác biệt hoàn toàn, vô hiệu hóa tấn công từ điển và bảng cầu vồng (Rainbow Table Attack).",
                        "Lớp 2 - Xác thực phi trạng thái JWT (HS256) và Phân quyền RBAC (Chống OWASP A01 - Broken Access Control): Mỗi token truy cập được ký số bằng thuật toán HMAC-SHA256 kèm thời hạn hết hạn (exp) và vai trò (role). Khi tài khoản bị Quản trị viên khóa (is_active = False) hoặc khi tài khoản thường cố tình gọi API quản trị, bộ kiểm tra require_role() lập tức từ chối truy cập với mã lỗi HTTP 403 Forbidden.",
                        "Lớp 3 - Phòng chống tiêm mã lệnh SQL Injection (Chống OWASP A03 - Injection): 100% truy vấn dữ liệu sử dụng biểu thức ORM tham số hóa của SQLAlchemy, tách biệt hoàn toàn câu lệnh SQL và dữ liệu đầu vào.",
                        "Lớp 4 - Phòng chống XSS và CSV Formula Injection (Chống OWASP A03 - Injection): Hàm sanitize_text() dùng biểu thức chính quy loại bỏ toàn bộ thẻ <script>, <iframe>, HTML độc hại và mã hóa thực thể HTML khi người dùng đăng ký hoặc tạo quy tắc cảnh báo. Hàm sanitize_csv_cell() tự động phát hiện và vô hiệu hóa các ký tự kích hoạt macro độc hại (=, +, -, @) ở đầu ô dữ liệu khi nhập/xuất CSV.",
                        "Lớp 5 - Giới hạn tần suất truy cập cửa sổ trượt (Sliding Window Rate Limiter - Chống OWASP A04 & A07): Lớp RateLimiter sử dụng khóa đồng bộ luồng (threading.Lock) để giám sát số lượng request theo từng địa chỉ IP trong cửa sổ thời gian trượt (chặn HTTP 429 Too Many Requests khi vượt quá 25 lần đăng nhập/phút hoặc 10 tác vụ nặng/phút).",
                        "Lớp 6 - Gia cố 7 Tiêu đề Bảo mật HTTP (SecurityHeadersMiddleware - Chống OWASP A05): Mọi phản hồi HTTP từ máy chủ đều được gắn tự động 7 tiêu đề bảo mật: X-Content-Type-Options: nosniff, X-Frame-Options: DENY (chống Clickjacking), X-XSS-Protection: 1; mode=block, Strict-Transport-Security: max-age=31536000; includeSubDomains, Referrer-Policy: strict-origin-when-cross-origin, Permissions-Policy: geolocation=(), camera=(), microphone=() và Content-Security-Policy: default-src 'self'; frame-ancestors 'none'; object-src 'none'.",
                    ],
                },
                {
                    "code": "4.3.3.",
                    "title": "Ma trận kết quả thực thi bộ kiểm thử tự động cốt lõi và kiểm toán bảo mật (100% PASSED)",
                    "paragraphs": [
                        "Toàn bộ 125 kịch bản Pytest Backend (gồm 72 kịch bản nền tảng tiêu biểu trình bày trong Bảng 4.3 và 53 kịch bản mở rộng về phủ nhánh 98%, kiểm toán sự thật dữ liệu, biến ngoại sinh nhân quả và vá bảo mật OWASP ở Mục 4.9) cùng 3 Frontend Unit Tests và 4 Playwright E2E đều đạt 100% PASSED.",
                    ],
                    "tables": [
                        {
                            "caption": "Bảng 4.3. Kết quả thực thi các nhóm kịch bản kiểm thử nền tảng cốt lõi và bảo mật OWASP Top 10",
                            "headers": ["Mã Test", "Tệp kiểm thử", "Tên hàm kiểm thử (Test Case)", "Nội dung kiểm tra & Kịch bản tấn công giả lập", "Kết quả"],
                            "rows": [
                                ["TC-01", "test_security_phase7.py", "test_security_headers_present", "Kiểm tra phản hồi HTTP gắn đủ 7 tiêu đề bảo mật chuẩn OWASP Top 10", "PASSED"],
                                ["TC-02", "test_security_phase7.py", "test_password_hashing_and_verification", "Kiểm tra băm mật khẩu Bcrypt sinh Salt ngẫu nhiên và xác thực chính xác", "PASSED"],
                                ["TC-03", "test_security_phase7.py", "test_sanitize_text_xss_protection", "Kiểm tra lọc bỏ mã độc <script>alert('XSS')</script> trong dữ liệu đầu vào", "PASSED"],
                                ["TC-04", "test_security_phase7.py", "test_csv_formula_injection_defense", "Kiểm tra chặn công thức thực thi lệnh độc hại =cmd|... và @SUM(...) trong CSV", "PASSED"],
                                ["TC-05", "test_security_phase7.py", "test_rate_limiter_mechanism", "Kiểm tra Sliding Window Rate Limiter chặn IP khi vượt ngưỡng request", "PASSED"],
                                ["TC-06", "test_security_phase7.py", "test_jwt_tampering_expiration_and_alg_none", "Kiểm tra từ chối JWT bị sửa chữ ký, hết hạn hoặc ký bằng khóa giả mạo", "PASSED"],
                                ["TC-07", "test_security_phase7.py", "test_rbac_privilege_escalation_defense", "Kiểm tra chặn tài khoản thường gọi API Admin (/scrape, /retrain, /users -> 403)", "PASSED"],
                                ["TC-08", "test_security_phase7.py", "test_sql_injection_defense_in_commodity_query", "Bơm payload SQLi (COFFEE' OR '1'='1, DROP TABLE) vào API tra cứu nông sản", "PASSED"],
                                ["TC-09", "test_security_phase7.py", "test_xss_sanitization_in_alert_creation", "Kiểm tra chống Stored XSS khi tạo quy tắc cảnh báo chứa script đánh cắp cookie", "PASSED"],
                                ["TC-10", "test_security_phase7.py", "test_spatio_temporal_farm_gate_regional_pricing", "Kiểm tra dự báo giá bán tại vườn theo huyện, độ lệch basisSpread và SHA-256 hash", "PASSED"],
                                ["TC-11..20", "test_auth.py", "10 kịch bản kiểm thử xác thực (Auth Suite)", "Đăng ký (201), trùng email (400), mật khẩu yếu (422), sai mật khẩu/token (401)", "PASSED (10/10)"],
                                ["TC-21..29", "test_predictions.py", "9 kịch bản kiểm thử đường ống dự báo ML", "Tạo đặc trưng Lag/Rolling, Threshold Gate, huấn luyện Prophet/XGBoost/LSTM, Cache", "PASSED (9/9)"],
                                ["TC-30..40", "test_history_workflow.py", "11 kịch bản kiểm thử lịch sử & 5 mô hình thật", "Lọc provenance, chặn dữ liệu unverified, kiểm định Holdout 5 mô hình AI thực tế", "PASSED (11/11)"],
                                ["TC-41..52", "test_admin_*.py", "12 kịch bản kiểm thử phân hệ Quản trị Admin", "Thống kê, nhật ký Scraper, chuyển đổi mô hình AI, nhập/xuất CSV, khóa tài khoản", "PASSED (12/12)"],
                                ["TC-53..60", "test_vietnam_sources.py", "8 kịch bản kiểm thử bộ bóc tách nguồn Việt Nam", "Kiểm tra Parser lấy đúng ngày, chợ, loại giá Bán tại hộ/vườn và đơn vị VNĐ/kg", "PASSED (8/8)"],
                                ["TC-61..72", "test_pipeline.py & khác", "12 kịch bản kiểm thử hệ thống, IQR & Cảnh báo", "Lọc ngoại lai IQR, điền khuyết chuỗi thời gian, kích hoạt cảnh báo Email, Health", "PASSED (12/12)"],
                            ],
                        }
                    ],
                },
            ],
        },
    ],
}

KET_LUAN_PARAGRAPHS = [
    "Khóa luận tốt nghiệp 'Xây dựng ứng dụng phân tích dữ liệu và dự báo biến động giá nông sản theo chuỗi thời gian sử dụng học máy' đã hoàn thành toàn bộ mục tiêu và nội dung nghiên cứu đề ra theo đúng đề cương được phê duyệt. Những kết quả chính và đóng góp mới của khóa luận được tóm tắt như sau:",
    "1. Đã xây dựng thành công đường ống thu thập, làm sạch ngoại lai và quản trị dữ liệu lịch sử giá nông sản giai đoạn 2024–2026 phân tách minh bạch 3 nhóm nguồn gốc (3 mặt hàng chủ lực 100% URL bài báo từng ngày, Mía đường quy đổi ICE SB=F + khảo sát vụ ép, và 4 đặc sản mở rộng neo giá khảo sát sống Việt Nam kết hợp chuỗi tham chiếu Proxy Index ETF Yahoo Finance DBA/MOO/CORN/SOYB x USD/VND) kèm chữ ký băm mật mã SHA-256 (dataset_hash) với 4.899 bản ghi trong price_history và 9.079 quan sát tách theo tỉnh trong regional_price_observations (chốt mốc 23/11/2026).",
    "2. Đã nghiên cứu, cài đặt và huấn luyện thực nghiệm đồng thời 5 mô hình học máy và thống kê chuỗi thời gian (PyTorch Stacked LSTM 7 kênh, XGBoost & Random Forest 22 đặc trưng, Facebook Prophet và ARIMA) tích hợp biến ngoại sinh nhân quả (USD/VND và Dầu thô WTI) theo quy trình kiểm định Walk-Forward cuộn 7 ngày không rò rỉ dữ liệu kèm khoảng tin cậy Conformal 95% CI. Kết quả thực nghiệm trên toàn bộ 8/8 mặt hàng (40/40 mô hình đều có R2 > 0) đạt sai số MAPE tối ưu từ 0,74% đến 2,62%, tiêu biểu là PyTorch Stacked LSTM vươn lên Hạng 1 trên Cà phê Robusta (MAPE 1,79%, RMSE 1.978,28 VNĐ/kg, R2 = 0,8972), Hồ tiêu đen ARIMA 0,74%, Dâu tây Đà Lạt Prophet 1,08%, Khoai tây Đà Lạt Prophet 1,30%, Hạt điều ARIMA 1,30%, Lúa IR50404 ARIMA 1,58%, Khoai lang tím XGBoost 1,71% và Mía đường Prophet 2,62%.",
    "3. Đã giải quyết bài toán định giá nông sản theo vị trí địa lý trên 33 tỉnh/thành phố (Location-Aware Regional Pricing dùng công thức Haversine phân tách minh bạch giữa Khảo sát trực tiếp và Tham chiếu vùng lân cận + cước vận chuyển), kết hợp tầng hiệu chỉnh cấp huyện/phường, khoảng tin cậy 95% mở rộng theo sqrt(h) và giải thích AI (XAI).",
    "4. Đã hoàn thiện ứng dụng Web Full-Stack AgroForecast (FastAPI + PostgreSQL 17 + Next.js 14 + Syncfusion EJ2 AgroGrid/FinChart + Docker Compose) và thực thi thành công 129/129 kịch bản kiểm thử tự động (125 Pytest Backend + 4 Playwright E2E trên Chrome thật) cùng kiểm toán an toàn thông tin chuẩn OWASP Top 10 (Bandit SAST 0 lỗi Medium/High, RBAC khóa chặt cả hai tầng, Bcrypt, JWT HS256, chống SQLi/XSS/SSRF/CSV Injection).",
]

HUONG_PHAT_TRIEN_PARAGRAPHS = [
    "Trên cơ sở nền tảng kiến trúc và đường ống học máy đã xây dựng trong khóa luận, hệ thống AgroForecast có thể tiếp tục được nghiên cứu mở rộng theo bốn hướng phát triển tiếp theo sau đây:",
    "1. Tích hợp dữ liệu viễn thám khí tượng và biến ngoại sinh thời gian thực (Multivariate Exogenous Time Series): Kết nối tự động API dữ liệu lượng mưa, độ ẩm đất, nhiệt độ tại các trạm khí tượng Tây Nguyên, Lâm Đồng, Đồng bằng sông Cửu Long cùng chỉ số giá phân bón và cước vận tải biển quốc tế vào kiến trúc mạng học sâu đa biến (Temporal Fusion Transformer - TFT hoặc Multivariate LSTM).",
    "2. Mở rộng độ phủ địa lý và danh mục nông sản đặc sản: Mở rộng mô hình độ lệch giá tại vườn (Basis Spread) tới cấp xã/hợp tác xã cho thêm các mặt hàng nông sản có giá trị kinh tế cao của tỉnh Lâm Đồng và Việt Nam như Sầu riêng Ri6/Monthong, Cà phê Arabica Cầu Đất, Chè Bảo Lộc, Hoa Đà Lạt, Thanh long và Tôm thẻ chân trắng.",
    "3. Phát triển ứng dụng di động đa nền tảng và trợ lý giọng nói tiếng Việt cho nông hộ: Xây dựng ứng dụng di động (React Native / Flutter) tích hợp thông báo đẩy (Push Notification) và giao diện tra cứu bằng giọng nói tiếng Việt giúp bà con nông dân dễ dàng nắm bắt giá bán tại vườn và xu hướng dự báo ngay tại nương rẫy.",
    "4. Nghiên cứu cơ chế học trực tuyến liên tục (Online Continual Learning) và phát hiện trôi dạt dữ liệu (Concept Drift Detection): Tự động phát hiện ngay khi cấu trúc thị trường có biến động vĩ mô bất thường để điều chỉnh trọng số mô hình tức thời mà không cần chờ chu kỳ huấn luyện lại toàn bộ.",
]

REFERENCES_LIST = [
    "1. Box G. E. P., Jenkins G. M., Reinsel G. C., Ljung G. M., Time Series Analysis: Forecasting and Control, 5th Edition, John Wiley & Sons, Hoboken, New Jersey, 2015.",
    "2. Breiman L., Random Forests, Machine Learning, Vol. 45, No. 1, 2001, pp. 5 - 32.",
    "3. Bộ Nông nghiệp và Phát triển Nông thôn - Viện Chính sách và Chiến lược Phát triển Nông nghiệp Nông thôn (IPSARD / AGROINFO), Báo cáo thường niên thị trường nông sản Việt Nam và Hệ thống cơ sở dữ liệu giá nông sản nội địa, Hà Nội, 2025.",
    "4. Chen T., Guestrin C., XGBoost: A Scalable Tree Boosting System, Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, San Francisco, California, USA, Aug. 13-17, 2016, pp. 785 - 794.",
    "5. Dickey D. A., Fuller W. A., Distribution of the Estimators for Autoregressive Time Series with a Unit Root, Journal of the American Statistical Association, Vol. 74, No. 366a, 1979, pp. 427 - 431.",
    "6. Hiệp hội Cà phê - Ca cao Việt Nam (VICOFA) và Hiệp hội Hồ tiêu và Cây gia vị Việt Nam (VPSA), Bản tin tổng hợp thị trường xuất khẩu và giá nông sản thu mua nội địa Tây Nguyên - Đông Nam Bộ, TP. Hồ Chí Minh, 2025.",
    "7. Hochreiter S., Schmidhuber J., Long Short-Term Memory, Neural Computation, Vol. 9, No. 8, 1997, pp. 1735 - 1780.",
    "8. Hyndman R. J., Athanasopoulos G., Forecasting: Principles and Practice, 3rd Edition, OTexts, Melbourne, Australia, 2021.",
    "9. Lewis C. D., Industrial and Business Forecasting Methods: A Practical Guide to Exponential Smoothing and Curve Fitting, Butterworth Scientific, London, 1982.",
    "10. Lundberg S. M., Lee S. I., A Unified Approach to Interpreting Model Predictions, Proceedings of the 31st International Conference on Neural Information Processing Systems (NeurIPS), Long Beach, California, USA, Dec. 4-9, 2017, pp. 4765 - 4774.",
    "11. Open Worldwide Application Security Project (OWASP), OWASP Top 10: The Ten Most Critical Web Application Security Risks & OWASP Web Security Testing Guide (WSTG v4.2), OWASP Foundation, Wakefield, USA, 2021.",
    "12. Paszke A., Gross S., Massa F., Lerer A., Bradbury J., et al., PyTorch: An Imperative Style, High-Performance Deep Learning Library, Advances in Neural Information Processing Systems (NeurIPS 32), Vancouver, Canada, Dec. 8-14, 2019, pp. 8024 - 8035.",
    "13. Pedregosa F., Varoquaux G., Gramfort A., Michel V., Thirion B., et al., Scikit-learn: Machine Learning in Python, Journal of Machine Learning Research (JMLR), Vol. 12, 2011, pp. 2825 - 2830.",
    "14. Taylor S. J., Letham B., Forecasting at Scale, The American Statistician, Vol. 72, No. 1, 2018, pp. 37 - 45.",
]
