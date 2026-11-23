# -*- coding: utf-8 -*-
"""
Phần 16: Phân tích chuyên sâu từng bộ định tuyến REST API (8 Routers),
phân tích thực nghiệm từng mặt hàng nông sản trên cả 5 mô hình AI (8 tiểu mục riêng biệt)
và đặc tả chi tiết từng nhóm kịch bản trong 72 kịch bản kiểm thử tự động & bảo mật OWASP.
"""

CH3_ROUTER_BY_ROUTER_SPECS = [
    {
        "code": "3.4.8.",
        "title": "Đặc tả thiết kế chi tiết Bộ định tuyến Xác thực & Quản lý Phiên (app/api/v1/endpoints/auth.py)",
        "paragraphs": [
            "Bộ định tuyến xác thực người dùng được gắn tại tiền tố /api/v1/auth, đóng vai trò là chốt chặn an ninh đầu tiên cho mọi thao tác quản trị và cá nhân hóa trong hệ thống AgroForecast. Mô-đun bao gồm 3 Endpoint cốt lõi: POST /register, POST /login và GET /me.",
            "Tại Endpoint POST /api/v1/auth/register: Hệ thống trích xuất địa chỉ IP của máy khách (request.client.host) và kiểm tra qua bộ giới hạn tần suất auth_rate_limiter.is_rate_limited(f'reg_{client_ip}'). Nếu vượt quá 25 yêu cầu trong 60 giây, yêu cầu bị từ chối ngay với mã HTTP 429 Too Many Requests. Tiếp theo, địa chỉ email được chuẩn hóa bằng phương thức strip().lower() và truy vấn không phân biệt hoa thường qua User.email.ilike(email_clean). Nếu email chưa tồn tại, hệ thống gọi hàm sanitize_text(payload.full_name) để loại bỏ triệt để mọi thẻ HTML/Script độc hại, gọi get_password_hash(payload.password) để sinh chuỗi băm Bcrypt 60 ký tự với Salt ngẫu nhiên 128-bit, gán vai trò mặc định role = 'user', trạng thái is_active = True và lưu vào bảng users.",
            "Tại Endpoint POST /api/v1/auth/login: Sau khi vượt qua bước kiểm tra Rate Limit theo khóa f'login_{client_ip}', hệ thống tìm kiếm bản ghi người dùng theo email. Nếu không tìm thấy hoặc kết quả verify_password(payload.password, user.password_hash) trả về False, hệ thống trả về thông báo lỗi thống nhất 'Email hoặc mật khẩu không chính xác' kèm mã HTTP 401 Unauthorized (việc trả về cùng một thông báo lỗi cho cả hai trường hợp sai email và sai mật khẩu là kỹ thuật bảo mật chống dò tìm danh sách tài khoản - Anti-User Enumeration theo khuyến nghị OWASP A07). Nếu tài khoản có is_active == False, hệ thống chặn đăng nhập với mã HTTP 403 Forbidden. Khi xác thực thành công, hàm create_access_token(subject=user.id, role=user.role) ký phát chuỗi JWT HS256 để trả về cho trình duyệt.",
        ],
    },
    {
        "code": "3.4.9.",
        "title": "Đặc tả thiết kế chi tiết Bộ định tuyến Nông sản, Giá thị trường & Lịch sử (commodities.py, prices.py, history.py)",
        "paragraphs": [
            "Nhóm 3 bộ định tuyến phục vụ tra cứu dữ liệu thị trường và lịch sử được thiết kế tối ưu cho tốc độ đọc cao và tính minh bạch nguồn gốc dữ liệu:",
            "1. Bộ định tuyến Nông sản (app/api/v1/endpoints/commodities.py - Tiền tố /api/v1/commodities): Cung cấp 5 Endpoint phục vụ trang chủ và trang đối sánh bao gồm: GET /overview (trả về danh sách 8 mặt hàng kèm giá bán tại vườn mới nhất, % thay đổi và chuỗi Sparkline 7 ngày), GET /comparison (trả về chuỗi tăng trưởng chuẩn hóa đa nông sản), GET /spotlight (trả về phân tích tiêu điểm 3 tháng của một mặt hàng theo mã code, đã được kiểm thử chống SQL Injection), GET /regional-prices (trả về bảng khảo sát giá bán tại vườn/ruộng, biên độ min/max, khối lượng và nguồn công bố) và GET /catalog (trả về danh mục nông sản rút gọn cho các hộp chọn lọc).",
            "2. Bộ định tuyến Lịch sử và Kiểm chứng Nguồn gốc (app/api/v1/endpoints/history.py - Tiền tố /api/v1/history): Cung cấp 2 Endpoint trọng tâm là GET /sources và GET ''. Endpoint GET /api/v1/history/sources kết hợp danh mục nguồn chuẩn SOURCES trong ml_pipeline/source_catalog.py với dữ liệu thực tế trong PostgreSQL để trả về thông tin chi tiết của từng nông sản: tên nguồn công bố chính thức, đường dẫn URL gốc, loại tần suất (daily, irregular, periodic), ngày bắt đầu thu thập gợi ý, tổng số bản ghi đã xác minh, số bản ghi chưa xác minh và trạng thái sẵn sàng cho huấn luyện học máy (readiness). Endpoint GET /api/v1/history nhận các tham số commodity_id, start_date, end_date, include_unverified, kiểm tra tính hợp lệ của khoảng thời gian (start_date <= end_date <= date.today()) và trả về mảng bản ghi lịch sử kèm danh sách các ngày khuyết dữ liệu (missing_dates).",
        ],
    },
    {
        "code": "3.4.10.",
        "title": "Đặc tả thiết kế chi tiết Bộ định tuyến Dự báo AI, Đường ống ML, Cảnh báo & Quản trị (forecast.py, predictions.py, alerts.py, admin.py)",
        "paragraphs": [
            "1. Bộ định tuyến Dự báo Không gian - Thời gian (app/api/v1/endpoints/forecast.py - Tiền tố /api/v1/forecast): Cung cấp Endpoint chính GET /api/v1/forecast nhận 4 tham số truy vấn: commodity_id (mặc định = 2), model_name (LSTM, Prophet, ARIMA, XGBoost, Random Forest; nếu để trống sẽ tự động lấy thuật toán mặc định active_model trong bảng system_settings), days (số bước dự báo từ 1 đến 30) và region (mã địa phương cấp huyện/phường bán tại vườn/ruộng). Kết quả trả về kết hợp chuỗi lịch sử, chuỗi dự báo đã hiệu chỉnh theo độ lệch giá cơ sở basisSpread của huyện đang chọn, dải khoảng tin cậy 95%, siêu dữ liệu kiểm định TrainingRun và danh sách toàn bộ địa phương của mặt hàng đó. Endpoint thứ hai là GET /api/v1/forecast/compare/{commodity_id} trả về mảng 5 đối tượng ModelMetricsResponse để so sánh trực diện MAE, RMSE, MAPE, R2 của cả 5 mô hình.",
            "2. Bộ định tuyến Đường ống Dự báo Tốc độ cao (app/api/v1/endpoints/predictions.py - Tiền tố /api/v1/predictions): Cung cấp các cổng API chuyên biệt cho suy luận thời gian thực có tích hợp bộ nhớ đệm trong RAM (In-Memory Cache): GET /forecast (trả về chuỗi dự báo kèm thời gian phản hồi tính bằng mili-giây response_time_ms và cờ đánh dấu cached = True/False), GET /metrics (trả về thông số đánh giá từ các tập tin _metrics.json trên đĩa) và POST /retrain (yêu cầu quyền Admin để kích hoạt huấn luyện lại).",
            "3. Bộ định tuyến Cảnh báo Biến động Giá (app/api/v1/endpoints/alerts.py - Tiền tố /api/v1/alerts): Cung cấp đầy đủ 6 thao tác quản lý quy tắc cảnh báo: GET '' (liệt kê toàn bộ quy tắc cảnh báo), GET '/logs' (truy xuất lịch sử các cảnh báo đã kích hoạt), POST '' (tạo quy tắc mới có làm sạch XSS), PATCH '/{rule_id}/toggle' (bật hoặc tắt quy tắc), DELETE '/{rule_id}' (xóa quy tắc) và POST '/{rule_id}/test' (gửi thư điện tử thử nghiệm qua giao thức SMTP).",
            "4. Bộ định tuyến Quản trị Hệ thống (app/api/v1/endpoints/admin.py - Tiền tố /api/v1/admin): Bao gồm 16 Endpoint chuyên biệt dành cho Admin và Analyst để thống kê hệ thống (/stats), quản lý CRUD nông sản (/commodities), quản lý điểm giá và lưu vết kiểm toán (/prices/recent, POST /prices, DELETE /prices/{id}), nhập và xuất dữ liệu hàng loạt qua CSV (/prices/import-csv, /prices/export-csv), điều phối và giám sát tác vụ nền (/tasks/scrape, /tasks/retrain, /tasks, /tasks/{id}), xem nhật ký Bot thu thập (/logs/crawler), chuyển đổi mô hình AI mặc định (/models/active) và quản lý phân quyền, khóa/mở khóa người dùng (/users, /users/{id}/role, /users/{id}/toggle-status).",
        ],
    },
]

CH4_EIGHT_COMMODITIES_EXPERIMENT_DEEP_DIVE = [
    {
        "code": "4.2.8.",
        "title": "Phân tích kết quả thực nghiệm chi tiết trên Mặt hàng 1 (Lúa gạo IR50404) và Mặt hàng 2 (Cà phê Robusta)",
        "paragraphs": [
            "1. Kết quả thực nghiệm trên Mặt hàng Lúa gạo IR50404 (Mã RICE_IR504 — 442 phiên xác thực từ 01/01/2024 đến 23/11/2026, 100% URL bài báo riêng vietnambiz.vn & VFA vietfood.org.vn + 1.101 quan sát tách 7 tỉnh): Trên tập kiểm định Walk-Forward 66 điểm cuối (07/09/2026 – 23/11/2026) quanh vùng giá 6.850 VNĐ/kg, mô hình ARIMA đạt kết quả tối ưu nhất về MAPE với MAE = 100,24 VNĐ/kg, RMSE = 169,20 VNĐ/kg, MAPE = 1,58%, R² = 0,5340 và PICP 95% = 89,39%. Bám sát ngay sau là Facebook Prophet với MAE = 100,13 VNĐ/kg, RMSE thấp nhất 156,67 VNĐ/kg, MAPE = 1,59% và R² = 0,6005; tiếp theo là XGBoost (MAPE = 1,65%), Random Forest (1,67%) và Stacked LSTM (1,77%).",
            "2. Kết quả thực nghiệm trên Mặt hàng Cà phê nhân xô Robusta (Mã COFFEE_ROBUSTA — 919 phiên xác thực từ 04/01/2024 đến 23/11/2026, 100% URL bài báo riêng vietnambiz.vn & giacaphe.com + 3.485 quan sát tách 4 tỉnh Tây Nguyên): Chuỗi giá gần 3 năm phản ánh trọn vẹn chu kỳ đỉnh – điều chỉnh từ 67.600 đến 135.200 VNĐ/kg (phiên 23/11/2026 đạt 71.700 VNĐ/kg). Trên 90 điểm Walk-Forward (13/08 – 23/11/2026), nhờ tích hợp 2 biến ngoại sinh vĩ mô nhân quả (USD/VND + Dầu thô WTI <= t-1), mạng học sâu PyTorch Stacked LSTM (7 kênh) xuất sắc giành Hạng 1 tuyệt đối trên cả 4 thước đo với MAE = 1.555,41 VNĐ/kg, RMSE = 1.978,28 VNĐ/kg, MAPE = 1,79%, R² = 0,8972 và PICP = 92,22% (vượt sâu Naive Baseline 1,88%, RMSE 2.147,01 VNĐ/kg). Theo sau là ARIMA (1,86%), Random Forest (RMSE 2.087,40 đ/kg, 1,90%), XGBoost (1,96%) và Prophet (2,15%).",
        ],
    },
    {
        "code": "4.2.9.",
        "title": "Phân tích kết quả thực nghiệm chi tiết trên Mặt hàng 3 (Hồ tiêu đen) và Mặt hàng 4 (Mía đường 10 CCS)",
        "paragraphs": [
            "1. Kết quả thực nghiệm trên Mặt hàng Hồ tiêu đen xô khô (Mã PEPPER_BLACK — 793 phiên xác thực từ 04/01/2024 đến 23/11/2026, 100% URL bài báo riêng vietnambiz.vn + 4.446 quan sát tách 6 tỉnh): Chuỗi giá trải dài từ 77.800 đến 169.200 VNĐ/kg (phiên 23/11/2026 đạt 129.100 VNĐ/kg). Trên 90 điểm kiểm định Walk-Forward (26/08 – 23/11/2026), cả 5 mô hình đều đạt MAPE xuất sắc dưới 0,90%: ARIMA đứng Hạng 1 với MAE = 990,46 VNĐ/kg, RMSE = 1.643,77 VNĐ/kg, MAPE = 0,74%, R² = 0,3256 và PICP 95% = 94,44% (vượt Baseline RMSE 1.646,34 VNĐ/kg); bám sát ngay sau là XGBoost (MAPE = 0,78%), Random Forest (RMSE thấp nhất 1.631,93 đ/kg, R² = 0,3353, MAPE = 0,78%), LSTM (0,79%) và Prophet (0,87%).",
            "2. Kết quả thực nghiệm trên Mặt hàng Mía đường 10 CCS (Mã SUGARCANE — 729 phiên giao dịch thật quy đổi từ sàn ICE Sugar #11 Yahoo Finance SB=F × tỷ giá USD/VND giai đoạn 02/01/2024 – 23/11/2026, kết hợp 8 bài báo khảo sát trực tiếp vụ ép 2024–2026 tại Khánh Hòa, Phú Yên, Gia Lai): Chuỗi giá dao động thực tế từ 965.000 đến 1.656.000 VNĐ/tấn (phiên 23/11/2026 đạt 1.230.000 VNĐ/tấn). Trên 90 điểm kiểm định Walk-Forward (20/07 – 23/11/2026), Facebook Prophet giành Hạng 1 với MAE = 34.245,40 VNĐ/tấn, RMSE = 46.011,00 VNĐ/tấn, MAPE = 2,62%, R² = 0,8571 và PICP 95% = 97,78% (vượt Baseline 2,74%); tiếp theo là Random Forest (2,70%), ARIMA (2,74%), LSTM (2,75%) và XGBoost (2,77%).",
        ],
    },
    {
        "code": "4.2.10.",
        "title": "Phân tích kết quả thực nghiệm chi tiết trên Mặt hàng 5 (Dâu tây Đà Lạt), Mặt hàng 6 (Khoai lang tím), Mặt hàng 7 (Khoai tây Đà Lạt) và Mặt hàng 8 (Hạt điều thô)",
        "paragraphs": [
            "1. Kết quả thực nghiệm trên Mặt hàng Dâu tây Đà Lạt (Mã STRAWBERRY — 504 phiên từ 21/11/2024 – 23/11/2026, neo giá khảo sát sống tại kamereo.vn 100.000 VNĐ/kg kết hợp chuỗi tham chiếu Proxy Index ETF Yahoo Finance DBA × USD/VND): Trên 75 điểm Walk-Forward (12/08 – 23/11/2026), Facebook Prophet giành Hạng 1 vượt trội với MAE = 1.164,79 VNĐ/kg, RMSE = 1.610,18 VNĐ/kg, MAPE = 1,08%, R² = 0,8693 và PICP 95% = 100,0% (vượt sâu Baseline 1,30%); tiếp theo là ARIMA (1,30%), XGBoost (1,30%), Random Forest (1,31%) và LSTM (1,35%).",
            "2. Kết quả thực nghiệm trên Mặt hàng Khoai lang tím Vĩnh Long (Mã SWEET_POTATO — 504 phiên từ 21/11/2024 – 23/11/2026, neo giá khảo sát sống tại banggianongsan.com 16.000 VNĐ/kg kết hợp chuỗi tham chiếu Proxy Index ETF Yahoo Finance CORN × USD/VND): Trên 75 điểm Walk-Forward, XGBoost (22 đặc trưng) giành Hạng 1 với MAE = 305,09 VNĐ/kg, RMSE = 393,93 VNĐ/kg, MAPE = 1,71%, R² = 0,8844 và PICP 95% = 97,33% (vượt Baseline 1,715%); tiếp theo là ARIMA (1,75%), Random Forest (1,77%), LSTM (1,93%) và Prophet (1,97%).",
            "3. Kết quả thực nghiệm trên Mặt hàng Khoai tây Đà Lạt (Mã POTATO — 504 phiên từ 21/11/2024 – 23/11/2026, neo giá khảo sát sống tại namtinhvegetable.com Lâm Đồng 20.000 VNĐ/kg kết hợp chuỗi tham chiếu Proxy Index ETF Yahoo Finance MOO × USD/VND): Trên 75 điểm Walk-Forward, Facebook Prophet giành Hạng 1 với MAE = 276,05 VNĐ/kg, RMSE = 368,60 VNĐ/kg, MAPE = 1,30%, R² = 0,7119 và PICP 95% = 100,0% (vượt Baseline 1,39%); bám sát là ARIMA (1,40%), Random Forest (1,42%), XGBoost (1,43%) và LSTM (1,60%).",
            "4. Kết quả thực nghiệm trên Mặt hàng Hạt điều thô (Mã CASHEW_NUT — 504 phiên từ 21/11/2024 – 23/11/2026, neo giá khảo sát sống 7 tỉnh tại banggianongsan.com mức 32.500 VNĐ/kg tại Bình Phước kết hợp chuỗi tham chiếu Proxy Index ETF Yahoo Finance SOYB × USD/VND): Trên 75 điểm Walk-Forward, ARIMA giành Hạng 1 với MAE = 444,00 VNĐ/kg, RMSE = 555,34 VNĐ/kg, MAPE = 1,30%, R² = 0,8127 và PICP 95% = 100,0%; bám sát là XGBoost (1,33%), LSTM (1,35%), Random Forest (1,40%) và Prophet (1,43%).",
        ],
    },
]
