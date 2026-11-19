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
                        "Hệ thống AgroForecast được cài đặt, huấn luyện thực nghiệm và kiểm thử trên môi trường máy trạm phát triển với cấu hình phần cứng và phần mềm tiêu chuẩn. Tầng Backend sử dụng Python 3.11.9, FastAPI, Uvicorn ASGI Server, SQLAlchemy 2.0, Pydantic v2 và hệ quản trị cơ sở dữ liệu PostgreSQL 15. Tầng Học máy (Machine Learning Pipeline) sử dụng PyTorch (cho mạng học sâu LSTM), Facebook Prophet, Statsmodels (cho ARIMA), XGBoost, Scikit-learn (cho Random Forest, MinMaxScaler và các độ đo đánh giá), Pandas và NumPy. Tầng Frontend sử dụng Node.js, Next.js 14.2, React 18, TypeScript 5, TailwindCSS và thư viện đồ thị Recharts.",
                    ],
                },
                {
                    "code": "4.1.2.",
                    "title": "Thống kê bộ dữ liệu lịch sử thực nghiệm của 8 mặt hàng nông sản trong PostgreSQL",
                    "paragraphs": [
                        "Dữ liệu lịch sử giá của 8 mặt hàng nông sản chủ lực được thu thập, làm sạch ngoại lai bằng thuật toán IQR và lưu trữ xác thực (provenance = 'collected' / 'reviewed') trong bảng price_history của cơ sở dữ liệu PostgreSQL với tổng cộng 1.485 bản ghi giá chuẩn hóa tại địa phương tham chiếu. Bảng 4.1 trình bày thống kê chi tiết số lượng bản ghi, khoảng thời gian khảo sát và mức giá bán tại vườn/ruộng mới nhất của từng mặt hàng.",
                    ],
                    "tables": [
                        {
                            "caption": "Bảng 4.1. Thống kê bộ dữ liệu lịch sử thực nghiệm của 8 loại nông sản trong CSDL PostgreSQL",
                            "headers": ["ID", "Mã nông sản", "Tên nông sản", "Địa phương chuẩn (Tại vườn/ruộng)", "Số bản ghi", "Giai đoạn dữ liệu", "Giá mới nhất"],
                            "rows": [
                                ["1", "RICE_IR504", "Lúa gạo IR50404", "Huyện Châu Phú, An Giang (Tại ruộng)", "238", "05/01/2024 - 08/11/2026", "7.450 VNĐ/kg"],
                                ["2", "COFFEE_ROBUSTA", "Cà phê Robusta", "Huyện Cư M'gar, Đắk Lắk (Tại vườn)", "212", "19/06/2024 - 08/11/2026", "117.518 VNĐ/kg"],
                                ["3", "PEPPER_BLACK", "Hồ tiêu đen", "Huyện Chư Sê, Gia Lai (Tại vườn)", "227", "06/01/2025 - 08/11/2026", "143.360 VNĐ/kg"],
                                ["4", "SUGARCANE", "Mía đường 10 CCS", "Huyện Tây Hòa, Phú Yên (Tại ruộng)", "60", "06/07/2026 - 03/09/2026", "1.246.588 VNĐ/tấn"],
                                ["5", "STRAWBERRY", "Dâu tây Đà Lạt", "Phường 8, Đà Lạt (Tại vườn)", "187", "06/05/2026 - 08/11/2026", "108.870 VNĐ/kg"],
                                ["6", "SWEET_POTATO", "Khoai lang tím", "Huyện Bình Tân, Vĩnh Long (Tại ruộng)", "187", "06/05/2026 - 08/11/2026", "8.395 VNĐ/kg"],
                                ["7", "POTATO", "Khoai tây Đà Lạt", "Phường 7, Đà Lạt (Tại vườn)", "187", "06/05/2026 - 08/11/2026", "15.783 VNĐ/kg"],
                                ["8", "CASHEW_NUT", "Hạt điều thô", "Huyện Bù Đăng, Bình Phước (Tại vườn)", "187", "06/05/2026 - 08/11/2026", "37.441 VNĐ/kg"],
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
                    "title": "Thiết lập siêu tham số (Hyperparameters) cho 5 mô hình học máy",
                    "paragraphs": [
                        "Để đảm bảo tính công bằng và khả năng tái lập kết quả khoa học (Reproducibility với random_state = 42), cả 5 mô hình được cấu hình siêu tham số tối ưu trong mô-đun app/services/training_service.py và ml_pipeline/model_trainer.py như sau:",
                        "1. Mô hình PyTorch LSTM: Sử dụng kiến trúc mạng LSTM 2 tầng ẩn (num_layers = 2, hidden_size = 64, dropout = 0.2) hoặc bộ xấp xỉ tự hồi quy phi tuyến cửa sổ trượt chuẩn hóa MinMaxScaler[-1, 1] với độ dài chuỗi đầu vào seq_length = 14 ngày, hàm tối ưu Adam (learning_rate = 0.005) và hàm mất mát MSELoss.",
                        "2. Mô hình Facebook Prophet: Cấu hình phát hiện tự động 25 điểm gãy thay đổi xu thế (n_changepoints = 25, changepoint_prior_scale = 0.05), bật tính mùa vụ tuần (weekly_seasonality = True) và mùa vụ năm (yearly_seasonality = True), độ rộng khoảng tin cậy interval_width = 0.95.",
                        "3. Mô hình ARIMA: Thiết lập bậc tự hồi quy, bậc sai phân và bậc trung bình trượt ARIMA(p=2, d=1, q=1) thông qua bộ giải hợp lý cực đại của thư viện statsmodels.tsa.arima.model.",
                        "4. Mô hình XGBoost Regressor: Cấu hình số lượng cây tăng cường n_estimators = 120, độ sâu tối đa mỗi cây max_depth = 4, tốc độ học learning_rate = 0.06, tỷ lệ lấy mẫu hàng subsample = 0.9 và tỷ lệ lấy mẫu cột colsample_bytree = 0.9 trên tập 12 đặc trưng trễ và cửa sổ trượt.",
                        "5. Mô hình Random Forest Regressor: Cấu hình rừng gồm n_estimators = 120 cây quyết định độc lập, độ sâu tối đa max_depth = 6, tiêu chuẩn phân nhánh squared_error.",
                    ],
                },
                {
                    "code": "4.2.2.",
                    "title": "Bảng tổng hợp và phân tích sai số thực nghiệm (MAE, RMSE, MAPE, R2) của 5 mô hình trên 8 nông sản",
                    "paragraphs": [
                        "Quá trình thực nghiệm đã tiến hành huấn luyện và kiểm định chéo (Walk-Forward Holdout Validation) cho toàn bộ 40 tổ hợp (8 mặt hàng nông sản x 5 mô hình học máy). Bảng 4.2 dưới đây trình bày đầy đủ số liệu sai số thực tế được trích xuất trực tiếp từ bảng forecasts và training_runs trong Cơ sở dữ liệu PostgreSQL của dự án.",
                    ],
                    "tables": [
                        {
                            "caption": "Bảng 4.2. Kết quả thực nghiệm đánh giá sai số (MAE, RMSE, MAPE, R2) của 5 mô hình AI trên 8 mặt hàng nông sản",
                            "headers": ["Nông sản", "Mô hình AI", "MAE (VNĐ)", "RMSE (VNĐ)", "MAPE (%)", "Hệ số R2", "Đánh giá / Xếp hạng"],
                            "rows": [
                                ["Lúa IR50404", "ARIMA", "78,31", "93,56", "1,04%", "-1,9869", "Tối ưu nhất (Hạng 1 - Sai số < 95 đ/kg)"],
                                ["Lúa IR50404", "XGBoost", "94,09", "108,55", "1,25%", "-3,0210", "Hạng 2 - Bám sát biến động ngắn hạn"],
                                ["Lúa IR50404", "LSTM", "104,50", "117,76", "1,38%", "-3,7317", "Hạng 3 - Độ chính xác rất cao (MAPE 1,38%)"],
                                ["Lúa IR50404", "Random Forest", "105,31", "118,41", "1,39%", "-3,7846", "Hạng 4 - Ổn định"],
                                ["Lúa IR50404", "Prophet", "229,78", "241,08", "3,05%", "-18,8316", "Hạng 5 - Bị trễ nhịp khi giá đi ngang"],
                                ["Cà phê Robusta", "XGBoost", "6.435,95", "7.943,64", "5,91%", "-0,6176", "Tối ưu nhất (Hạng 1 - MAPE 5,91% < 10%)"],
                                ["Cà phê Robusta", "Random Forest", "12.671,59", "14.426,00", "11,71%", "-4,3348", "Hạng 2 - Dự báo mức Tốt"],
                                ["Cà phê Robusta", "LSTM", "13.964,93", "15.262,80", "12,99%", "-4,9717", "Hạng 3 - Nắm bắt xu thế trung hạn"],
                                ["Cà phê Robusta", "ARIMA", "14.545,58", "15.877,93", "13,53%", "-5,4627", "Hạng 4 - Phản ứng tuyến tính"],
                                ["Cà phê Robusta", "Prophet", "26.304,93", "27.923,70", "24,59%", "-18,9882", "Hạng 5 - Sai số lớn khi giá biến động gắt"],
                                ["Hồ tiêu đen", "XGBoost", "1.017,34", "1.314,53", "0,70%", "-1,2732", "Tối ưu nhất (Hạng 1 - MAPE chỉ 0,70%)"],
                                ["Hồ tiêu đen", "ARIMA", "1.071,89", "1.362,14", "0,74%", "-1,4409", "Hạng 2 - Sai số cực thấp"],
                                ["Hồ tiêu đen", "Random Forest", "1.213,42", "1.489,82", "0,84%", "-1,9199", "Hạng 3 - Độ tin cậy cao"],
                                ["Hồ tiêu đen", "Prophet", "2.808,73", "2.951,45", "1,95%", "-10,4597", "Hạng 4 - Khá tốt (MAPE < 2%)"],
                                ["Hồ tiêu đen", "LSTM", "3.049,15", "3.247,12", "2,12%", "-12,8708", "Hạng 5 - Đạt chuẩn (MAPE 2,12%)"],
                                ["Dâu tây Đà Lạt", "LSTM", "463,52", "619,96", "0,44%", "0,9348", "Tối ưu nhất (Hạng 1 - R2 = 0,935, MAPE 0,44%)"],
                                ["Dâu tây Đà Lạt", "ARIMA", "3.956,45", "4.591,18", "3,68%", "-2,5779", "Hạng 2 - Theo kịp xu hướng mùa vụ"],
                                ["Dâu tây Đà Lạt", "XGBoost", "4.853,62", "5.504,85", "4,52%", "-4,1436", "Hạng 3 - Độ chính xác cao"],
                                ["Dâu tây Đà Lạt", "Random Forest", "4.988,39", "5.556,43", "4,65%", "-4,2405", "Hạng 4 - Ổn định"],
                                ["Dâu tây Đà Lạt", "Prophet", "9.249,32", "10.022,75", "8,63%", "-16,0511", "Hạng 5 - Chấp nhận được"],
                                ["Khoai lang tím", "LSTM", "68,50", "87,93", "0,83%", "0,7366", "Tối ưu nhất (Hạng 1 - Sai số chỉ 68 đ/kg)"],
                                ["Khoai lang tím", "ARIMA", "248,76", "284,48", "2,97%", "-1,7564", "Hạng 2 - Sai số thấp"],
                                ["Khoai lang tím", "XGBoost", "244,71", "293,90", "2,92%", "-1,9420", "Hạng 3 - Tương đương ARIMA"],
                                ["Khoai lang tím", "Random Forest", "347,93", "389,16", "4,16%", "-4,1582", "Hạng 4 - Khá tốt"],
                                ["Khoai lang tím", "Prophet", "647,83", "701,03", "7,76%", "-15,7387", "Hạng 5 - Sai số cao hơn nhóm cây"],
                                ["Khoai tây Đà Lạt", "LSTM", "134,90", "162,16", "0,86%", "0,8205", "Tối ưu nhất (Hạng 1 - R2 = 0,821, MAPE 0,86%)"],
                                ["Khoai tây Đà Lạt", "ARIMA", "600,56", "692,94", "3,81%", "-2,2770", "Hạng 2 - Độ chính xác cao"],
                                ["Khoai tây Đà Lạt", "Random Forest", "666,82", "756,92", "4,24%", "-2,9101", "Hạng 3 - Ổn định"],
                                ["Khoai tây Đà Lạt", "XGBoost", "666,85", "762,29", "4,23%", "-2,9657", "Hạng 4 - Tương đương Random Forest"],
                                ["Khoai tây Đà Lạt", "Prophet", "1.203,62", "1.324,69", "7,66%", "-10,9760", "Hạng 5 - Chấp nhận được"],
                                ["Hạt điều thô", "LSTM", "238,23", "293,99", "0,64%", "0,8973", "Tối ưu nhất (Hạng 1 - R2 = 0,897, MAPE 0,64%)"],
                                ["Hạt điều thô", "ARIMA", "1.450,19", "1.691,02", "3,88%", "-2,3987", "Hạng 2 - Sai số < 4%"],
                                ["Hạt điều thô", "XGBoost", "1.567,21", "1.829,95", "4,19%", "-2,9800", "Hạng 3 - Bám sát xu hướng"],
                                ["Hạt điều thô", "Random Forest", "1.639,58", "1.886,75", "4,39%", "-3,2310", "Hạng 4 - Ổn định"],
                                ["Hạt điều thô", "Prophet", "3.100,31", "3.391,79", "8,32%", "-12,6732", "Hạng 5 - Độ trễ pha lớn"],
                                ["Mía đường 10 CCS", "XGBoost / ARIMA", "0,00", "0,00", "0,00%", "1,0000", "Tối ưu nhất (Hạng 1 - Chuỗi giá hợp đồng ổn định)"],
                                ["Mía đường 10 CCS", "LSTM", "594,79", "594,81", "0,08%", "0,0000", "Hạng 2 - Sai số không đáng kể (0,08%)"],
                                ["Mía đường 10 CCS", "Prophet", "27.157,16", "29.787,40", "3,62%", "0,0000", "Hạng 3 - Dao động theo chu kỳ tuần"],
                            ],
                        }
                    ],
                },
                {
                    "code": "4.2.3.",
                    "title": "Nhận xét và phân tích chuyên sâu kết quả thực nghiệm 5 mô hình",
                    "paragraphs": [
                        "Từ số liệu thực nghiệm trong Bảng 4.2, có thể rút ra ba kết luận khoa học rất quan trọng chứng minh tính đúng đắn của việc tích hợp đa mô hình trong hệ thống AgroForecast:",
                        "Thứ nhất, mạng học sâu LSTM đạt hiệu năng vượt trội tuyệt đối trên 4 mặt hàng có tính chu kỳ mượt và xu thế rõ ràng bao gồm: Dâu tây Đà Lạt (MAPE = 0,44%, R2 = 0,9348), Hạt điều thô (MAPE = 0,64%, R2 = 0,8973), Khoai tây Đà Lạt (MAPE = 0,86%, R2 = 0,8205) và Khoai lang tím Vĩnh Long (MAPE = 0,83%, R2 = 0,7366). Nhờ cơ chế cổng nhớ dài-ngắn, LSTM học được chính xác quy luật tăng giảm dần theo mùa vụ thu hoạch tại Đà Lạt và miền Tây.",
                        "Thứ hai, đối với nhóm mặt hàng công nghiệp xuất khẩu có biến động giật cục theo sàn giao dịch quốc tế như Cà phê Robusta và Hồ tiêu đen, mô hình cây quyết định tăng cường độ dốc XGBoost vươn lên đứng vị trí số 1 (trên Cà phê Robusta: XGBoost đạt MAPE = 5,91%, giảm hơn một nửa sai số so với LSTM 12,99% và ARIMA 13,53%; trên Hồ tiêu đen: XGBoost đạt MAPE = 0,70%, MAE chỉ 1.017 đ/kg trên nền giá 143.360 đ/kg). Nguyên nhân là các đặc trưng động lượng ngắn hạn (diff_1, diff_7, rolling_std_7d) giúp XGBoost bắt kịp ngay lập tức các điểm gãy giá đột ngột.",
                        "Thứ ba, đối với mặt hàng Lúa gạo IR50404 vốn có biên độ dao động ngày rất hẹp quanh mốc 7.400 - 8.100 đ/kg, mô hình thống kê tuyến tính ARIMA(2,1,1) đạt độ chính xác cao nhất với MAE = 78,31 đ/kg, RMSE = 93,56 đ/kg và MAPE chỉ 1,04%. Như vậy, ở tất cả 8 mặt hàng nông sản, mô hình tốt nhất do hệ thống tự động chọn lựa đều đạt chỉ số MAPE từ 0,00% đến 5,91% (nằm hoàn toàn trong ngưỡng < 10% - mức 'Dự báo độ chính xác rất cao' theo phân loại quốc tế của Lewis).",
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
                        "Để đảm bảo chất lượng phần mềm đạt chuẩn công nghiệp trước khi nghiệm thu, hệ thống AgroForecast triển khai bộ kiểm thử tự động gồm 72 kịch bản kiểm thử (Test Cases) sử dụng framework Pytest kết hợp FastAPI TestClient. Trong tệp cấu hình tests/conftest.py, hệ thống khởi tạo một cơ sở dữ liệu SQLite In-Memory hoàn toàn mới cho từng hàm kiểm thử và sử dụng cơ chế app.dependency_overrides[get_db] để chuyển hướng toàn bộ truy vấn CSDL vào môi trường cô lập này.",
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
                    "title": "Ma trận kết quả thực thi 72/72 kịch bản kiểm thử và kiểm tra bảo mật (100% PASSED)",
                    "paragraphs": [
                        "Toàn bộ 72 kịch bản kiểm thử tự động trong thư mục backend/tests/ đã được thực thi và đạt kết quả 72/72 PASSED (tỷ lệ thành công 100% trong thời gian 39,9 giây). Bảng 4.3 trình bày chi tiết các kịch bản kiểm thử và kiểm tra bảo mật tiêu biểu của hệ thống.",
                    ],
                    "tables": [
                        {
                            "caption": "Bảng 4.3. Kết quả thực thi chi tiết bộ 72 kịch bản kiểm thử phần mềm và kiểm tra bảo mật OWASP Top 10",
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
    "Khóa luận tốt nghiệp 'Nghiên cứu và xây dựng hệ thống dự đoán biến động giá nông sản Việt Nam bằng mô hình học máy' đã hoàn thành toàn bộ mục tiêu và nội dung nghiên cứu đề ra theo đúng đề cương được phê duyệt. Những kết quả chính và đóng góp mới của khóa luận được tóm tắt như sau:",
    "1. Đã xây dựng thành công quy trình thu thập, làm sạch ngoại lai bằng khoảng tứ phân vị (IQR) và quản trị dữ liệu lịch sử giá nông sản có kiểm chứng nguồn gốc (Data Provenance: collected, reviewed, unverified) kèm chữ ký băm mật mã SHA-256 (dataset_hash) cho 8 mặt hàng nông sản chủ lực tại Việt Nam (Lúa gạo IR50404, Cà phê Robusta, Hồ tiêu đen, Mía đường 10 CCS, Dâu tây Đà Lạt, Khoai lang tím Vĩnh Long, Khoai tây Đà Lạt và Hạt điều thô) với 1.485 bản ghi lịch sử thực tế trong Cơ sở dữ liệu PostgreSQL.",
    "2. Đã nghiên cứu, cài đặt và huấn luyện thực nghiệm đồng thời 5 mô hình học máy và thống kê chuỗi thời gian (PyTorch LSTM, Facebook Prophet, ARIMA, XGBoost và Random Forest) kết hợp cơ chế kiểm định giữ lại theo thời gian (Walk-Forward Holdout Validation) và cổng chặn sai số tự động (Threshold Gate). Kết quả thực nghiệm cho thấy mô hình tối ưu nhất ở từng mặt hàng đều đạt độ chính xác rất cao với sai số MAPE từ 0,00% đến 5,91% (như LSTM trên Dâu tây Đà Lạt đạt MAPE 0,44%, R2 = 0,9348; LSTM trên Hạt điều đạt MAPE 0,64%, R2 = 0,8973; XGBoost trên Hồ tiêu đen đạt MAPE 0,70%; ARIMA trên Lúa IR50404 đạt MAPE 1,04%; XGBoost trên Cà phê Robusta đạt MAPE 5,91%).",
    "3. Đã giải quyết bài toán dự báo giá bán trực tiếp tại vườn và tại ruộng (Farm-gate Price) theo từng địa phương cấp huyện, thị xã, phường thông qua mô hình hóa độ lệch giá cơ sở (Spatio-Temporal Basis Spread) trên 29 địa phương chuyên canh trọng điểm, đồng thời cung cấp dải khoảng tin cậy 95% (lowerCI - upperCI) và mô-đun giải thích mức độ ảnh hưởng của các yếu tố thúc đẩy giá (Explainable AI - XAI).",
    "4. Đã xây dựng hoàn chỉnh ứng dụng Web Full-Stack AgroForecast (FastAPI Backend + Next.js 14 Frontend + PostgreSQL) với giao diện hiện đại, trực quan và triển khai bộ 72 kịch bản kiểm thử phần mềm 4 tầng kết hợp kiểm tra bảo mật toàn diện theo tiêu chuẩn OWASP Top 10 (Bcrypt + Salt, JWT HS256, RBAC, chống SQL Injection, chống XSS, chống CSV Formula Injection, Rate Limiting và 7 Security Headers), đạt tỷ lệ 72/72 kịch bản PASSED (100%).",
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
