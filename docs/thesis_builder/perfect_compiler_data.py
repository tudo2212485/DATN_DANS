# -*- coding: utf-8 -*-
"""
Dữ liệu chuẩn hóa cho bản báo cáo Khóa luận Tốt nghiệp hoàn thiện Đại học Đà Lạt.
"""
THESIS_METADATA = {
    "university": "TRƯỜNG ĐẠI HỌC ĐÀ LẠT",
    "faculty": "KHOA CÔNG NGHỆ THÔNG TIN",
    "degree_title": "KHÓA LUẬN TỐT NGHIỆP KỸ SƯ CÔNG NGHỆ THÔNG TIN",
    "thesis_title": "XÂY DỰNG ỨNG DỤNG PHÂN TÍCH DỮ LIỆU VÀ DỰ BÁO BIẾN ĐỘNG GIÁ NÔNG SẢN THEO CHUỖI THỜI GIAN SỬ DỤNG HỌC MÁY",
    "thesis_title_en": "DEVELOPMENT OF A WEB APPLICATION FOR TIME-SERIES AGRICULTURAL COMMODITY PRICE ANALYSIS AND FORECASTING USING MACHINE LEARNING",
    "advisor": "ThS. La Quốc Thắng",
    "students": [
        {"name": "Đỗ Trung Tú", "id": "2212485", "role": "Trưởng nhóm", "tasks": "Phân tích yêu cầu, Kiến trúc hệ thống, Backend FastAPI, Cơ sở dữ liệu PostgreSQL, Đường ống MLOps & Fingerprint SHA-256", "contribution": "100%"},
        {"name": "Nguyễn Thành Huy Thông", "id": "2212469", "role": "Thành viên", "tasks": "Khoa học dữ liệu, Tiền xử lý IQR, Nghiên cứu toán học & Huấn luyện 5 mô hình ML/Deep Learning, Thực nghiệm 40 tổ hợp mô hình, Giải thích XAI", "contribution": "100%"},
        {"name": "Lê Văn Minh", "id": "2212416", "role": "Thành viên", "tasks": "Giao diện Next.js 14, Tích hợp Syncfusion EJ2 (AgroGrid, FinChart), Thiết lập bộ 128 kịch bản kiểm thử (Pytest, Playwright) & Kiểm toán bảo mật OWASP Top 10", "contribution": "100%"},
    ],
    "cohort": "Khóa 46 (2022 - 2026)",
    "major": "Kỹ thuật Phần mềm / Khoa học Dữ liệu",
    "location_year": "Đà Lạt, tháng 11 năm 2026",
}

CORRECTED_APPENDIX_C_ROWS = [
    # 1. Lúa gạo IR50404 (An Giang, Đồng Tháp, Kiên Giang, Tiền Giang)
    ["Lúa IR50404", "Châu Phú (An Giang)", "ARIMA(2,1,1)", "78,31", "93,56", "1,04%", "-1,9869", "0,42 giây"],
    ["Lúa IR50404", "Châu Phú (An Giang)", "XGBoost", "94,09", "108,55", "1,25%", "-3,0210", "1,05 giây"],
    ["Lúa IR50404", "Châu Phú (An Giang)", "PyTorch LSTM", "104,50", "117,76", "1,38%", "-3,7317", "7,80 giây"],
    ["Lúa IR50404", "Châu Phú (An Giang)", "Random Forest", "105,31", "118,41", "1,39%", "-3,7846", "1,35 giây"],
    ["Lúa IR50404", "Châu Phú (An Giang)", "Facebook Prophet", "229,78", "241,08", "3,05%", "-18,8316", "2,60 giây"],

    # 2. Cà phê Robusta (Đắk Lắk, Lâm Đồng, Gia Lai, Đắk Nông)
    ["Cà phê Robusta", "Cư M'gar (Đắk Lắk)", "XGBoost", "6.435,95", "7.943,64", "5,91%", "-0,6176", "1,15 giây"],
    ["Cà phê Robusta", "Cư M'gar (Đắk Lắk)", "Random Forest", "12.671,59", "14.426,00", "11,71%", "-4,3348", "1,45 giây"],
    ["Cà phê Robusta", "Cư M'gar (Đắk Lắk)", "PyTorch LSTM", "13.964,93", "15.262,80", "12,99%", "-4,9717", "8,20 giây"],
    ["Cà phê Robusta", "Cư M'gar (Đắk Lắk)", "ARIMA(2,1,1)", "14.545,58", "15.877,93", "13,53%", "-5,4627", "0,45 giây"],
    ["Cà phê Robusta", "Cư M'gar (Đắk Lắk)", "Facebook Prophet", "26.304,93", "27.923,70", "24,59%", "-18,9882", "2,75 giây"],

    # 3. Hồ tiêu đen (Gia Lai, Đắk Lắk, Bà Rịa - Vũng Tàu, Bình Phước, Đắk Nông)
    ["Hồ tiêu đen", "Chư Sê (Gia Lai)", "XGBoost", "1.017,34", "1.314,53", "0,70%", "-1,2732", "1,12 giây"],
    ["Hồ tiêu đen", "Chư Sê (Gia Lai)", "ARIMA(2,1,1)", "1.071,89", "1.362,14", "0,74%", "-1,4409", "0,44 giây"],
    ["Hồ tiêu đen", "Chư Sê (Gia Lai)", "Random Forest", "1.213,42", "1.489,82", "0,84%", "-1,9199", "1,48 giây"],
    ["Hồ tiêu đen", "Chư Sê (Gia Lai)", "Facebook Prophet", "2.808,73", "2.951,45", "1,95%", "-10,4597", "2,85 giây"],
    ["Hồ tiêu đen", "Chư Sê (Gia Lai)", "PyTorch LSTM", "3.049,15", "3.247,12", "2,12%", "-12,8708", "8,40 giây"],

    # 4. Mía đường 10 CCS (Phú Yên, Tây Ninh, Gia Lai, Hậu Giang)
    ["Mía đường 10 CCS", "Tây Hòa (Phú Yên)", "XGBoost", "0,00", "0,00", "0,00%", "1,0000", "0,92 giây"],
    ["Mía đường 10 CCS", "Tây Hòa (Phú Yên)", "ARIMA(1,0,0)", "0,00", "0,00", "0,00%", "1,0000", "0,32 giây"],
    ["Mía đường 10 CCS", "Tây Hòa (Phú Yên)", "Random Forest", "0,00", "0,00", "0,00%", "1,0000", "1,15 giây"],
    ["Mía đường 10 CCS", "Tây Hòa (Phú Yên)", "PyTorch LSTM", "594,79", "594,81", "0,08%", "0,0000", "7,20 giây"],
    ["Mía đường 10 CCS", "Tây Hòa (Phú Yên)", "Facebook Prophet", "27.157,16", "29.787,40", "3,62%", "0,0000", "2,40 giây"],

    # 5. Dâu tây Đà Lạt (Phường 8 Đà Lạt, Lạc Dương, Mộc Châu)
    ["Dâu tây Đà Lạt", "Phường 8 (Đà Lạt)", "PyTorch LSTM", "463,52", "619,96", "0,44%", "0,9348", "8,10 giây"],
    ["Dâu tây Đà Lạt", "Phường 8 (Đà Lạt)", "ARIMA(2,1,1)", "3.956,45", "4.591,18", "3,68%", "-2,5779", "0,46 giây"],
    ["Dâu tây Đà Lạt", "Phường 8 (Đà Lạt)", "XGBoost", "4.853,62", "5.504,85", "4,52%", "-4,1436", "1,10 giây"],
    ["Dâu tây Đà Lạt", "Phường 8 (Đà Lạt)", "Random Forest", "4.988,39", "5.556,43", "4,65%", "-4,2405", "1,42 giây"],
    ["Dâu tây Đà Lạt", "Phường 8 (Đà Lạt)", "Facebook Prophet", "9.249,32", "10.022,75", "8,63%", "-16,0511", "2,70 giây"],

    # 6. Khoai lang tím Vĩnh Long (Bình Tân, Châu Thành, Châu Thành A)
    ["Khoai lang tím", "Bình Tân (Vĩnh Long)", "PyTorch LSTM", "68,50", "87,93", "0,83%", "0,7366", "7,90 giây"],
    ["Khoai lang tím", "Bình Tân (Vĩnh Long)", "ARIMA(1,1,1)", "248,76", "284,48", "2,97%", "-1,7564", "0,40 giây"],
    ["Khoai lang tím", "Bình Tân (Vĩnh Long)", "XGBoost", "244,71", "293,90", "2,92%", "-1,9420", "1,08 giây"],
    ["Khoai lang tím", "Bình Tân (Vĩnh Long)", "Random Forest", "347,93", "389,16", "4,16%", "-4,1582", "1,38 giây"],
    ["Khoai lang tím", "Bình Tân (Vĩnh Long)", "Facebook Prophet", "647,83", "701,03", "7,76%", "-15,7387", "2,65 giây"],

    # 7. Khoai tây Đà Lạt (Phường 7 Thái Phiên, Đức Trọng, Đơn Dương)
    ["Khoai tây Đà Lạt", "Phường 7 (Đà Lạt)", "PyTorch LSTM", "134,90", "162,16", "0,86%", "0,8205", "8,00 giây"],
    ["Khoai tây Đà Lạt", "Phường 7 (Đà Lạt)", "ARIMA(2,1,1)", "600,56", "692,94", "3,81%", "-2,2770", "0,42 giây"],
    ["Khoai tây Đà Lạt", "Phường 7 (Đà Lạt)", "Random Forest", "666,82", "756,92", "4,24%", "-2,9101", "1,40 giây"],
    ["Khoai tây Đà Lạt", "Phường 7 (Đà Lạt)", "XGBoost", "666,85", "762,29", "4,23%", "-2,9657", "1,12 giây"],
    ["Khoai tây Đà Lạt", "Phường 7 (Đà Lạt)", "Facebook Prophet", "1.203,62", "1.324,69", "7,66%", "-10,9760", "2,70 giây"],

    # 8. Hạt điều thô (Bù Đăng, Phú Riềng, Định Quán, Krông Pa)
    ["Hạt điều thô", "Bù Đăng (Bình Phước)", "PyTorch LSTM", "238,23", "293,99", "0,64%", "0,8973", "8,15 giây"],
    ["Hạt điều thô", "Bù Đăng (Bình Phước)", "ARIMA(1,1,1)", "1.450,19", "1.691,02", "3,88%", "-2,3987", "0,45 giây"],
    ["Hạt điều thô", "Bù Đăng (Bình Phước)", "XGBoost", "1.567,21", "1.829,95", "4,19%", "-2,9800", "1,15 giây"],
    ["Hạt điều thô", "Bù Đăng (Bình Phước)", "Random Forest", "1.639,58", "1.886,75", "4,39%", "-3,2310", "1,45 giây"],
    ["Hạt điều thô", "Bù Đăng (Bình Phước)", "Facebook Prophet", "3.100,31", "3.391,79", "8,32%", "-12,6732", "2,80 giây"],
]

APPENDIX_D_TABLES_DATA = [
    {
        "title": "D.1. Đặc tả Kiến trúc Phân tầng 4 Lớp của Hệ thống AgroForecast",
        "intro": "Hệ thống AgroForecast được thiết kế theo mô hình kiến trúc phân tầng 4 lớp chuẩn mực của kỹ thuật phần mềm hiện đại, đảm bảo tính phân tách trách nhiệm (Separation of Concerns), an toàn thông tin mạng và khả năng mở rộng quy mô độc lập:",
        "headers": ["Tầng kiến trúc (Tier)", "Công nghệ sử dụng", "Cổng dịch vụ & Giao thức", "Trách nhiệm và Chức năng kỹ thuật"],
        "rows": [
            ["Tầng Trình diễn (Presentation Tier)", "Next.js 14, React 18, TypeScript, TailwindCSS, Syncfusion EJ2, Recharts", "Cổng 3000 (HTTPS, Web Browser, Responsive UI)", "Hiển thị Dashboard tổng quan thị trường, biểu đồ chuỗi thời gian FinChart (Candlestick, Area, Line), dải tin cậy 95%, bảng dữ liệu ảo hóa AgroGrid, quản lý vị trí 33 tỉnh thành."],
            ["Tầng Cổng Bảo mật (API & Security Gateway)", "FastAPI 0.110+, Pydantic v2, PyJWT, Bcrypt, Starlette Middleware", "Cổng 8000 (/api/v1/*, JSON RESTful API)", "Kiểm soát truy cập CORS, gắn 7 tiêu đề HTTP bảo mật OWASP, giới hạn tần suất Sliding Window Rate Limiter (HTTP 429), xác thực JWT Bearer và phân quyền RBAC 3 vai trò."],
            ["Tầng Dịch vụ & ML Pipeline (Business & ML Tier)", "Python 3.11, PyTorch 2.2, Scikit-learn, XGBoost, Prophet, Statsmodels, APScheduler", "Tiến trình nội bộ máy chủ (Async Background Worker)", "Lọc ngoại lai IQR, tạo đặc trưng trễ/trung bình trượt, kiểm định dừng ADF, huấn luyện 5 mô hình AI, đánh giá Walk-Forward, tính dải tin cậy 95%, băm mật mã SHA-256."],
            ["Tầng Lưu trữ Bền vững (Data Persistence Tier)", "PostgreSQL 15+, SQLAlchemy ORM 2.0, AsyncPG Connection Pool", "Cổng 5432 (TCP Socket có tham số hóa truy vấn)", "Lưu trữ 11 bảng CSDL chuẩn 3NF: commodities, price_history, periodic_prices, forecasts, training_runs, price_revisions, alert_rules, alert_logs, background_jobs, system_settings, users."]
        ]
    },
    {
        "title": "D.2. Đặc tả Quy trình Huấn luyện và Kiểm soát Tính toàn vẹn Dữ liệu (MLOps SHA-256 Sequence)",
        "intro": "Quy trình phối hợp tuần tự giữa Quản trị viên, Máy chủ Backend, Cơ sở dữ liệu PostgreSQL và Động cơ Học máy nhằm loại trừ rủi ro rò rỉ dữ liệu (No Data Leakage) và ngăn chặn dự báo lỗi thời (Stale Forecast):",
        "headers": ["Bước (Step)", "Thành phần khởi phát", "Thành phần tiếp nhận", "Hành động kỹ thuật & Thông điệp trao đổi"],
        "rows": [
            ["Bước 1", "Quản trị viên (Admin)", "Frontend Client", "Đăng nhập tài khoản Admin, điều hướng vào /admin và nhấn nút 'Kích hoạt thu thập dữ liệu'."],
            ["Bước 2", "Frontend Client", "FastAPI Backend", "Gửi yêu cầu POST /api/v1/admin/tasks/scrape đính kèm JWT Bearer Token tại tiêu đề Authorization."],
            ["Bước 3", "FastAPI Backend", "Database PostgreSQL", "Kiểm tra quyền require_role(['admin']), khởi tạo bản ghi BackgroundJob(kind='scrape', status='RUNNING')."],
            ["Bước 4", "Background Worker", "Cổng thông tin nguồn", "Kết nối nguồn AGROINFO, VPSA, VSSA thu thập dữ liệu giá mới, lọc ngoại lai IQR, gán provenance='collected'."],
            ["Bước 5", "Background Worker", "Database PostgreSQL", "Ghi các bản ghi giá mới vào price_history, tính dấu vân tay chuỗi H = SHA256(data) và lưu vào training_runs."],
            ["Bước 6", "Quản trị viên (Admin)", "FastAPI Backend", "Kích hoạt huấn luyện lại qua POST /api/v1/admin/tasks/retrain khi chuỗi lịch sử có quan sát mới."],
            ["Bước 7", "ML Engine", "ML Engine", "Tách tập Train và Holdout theo thứ tự thời gian (No Data Leakage), huấn luyện 5 mô hình, tính MAE, RMSE, MAPE, R2."],
            ["Bước 8", "ML Engine", "Database PostgreSQL", "Lưu 30 điểm dự báo tương lai kèm dải tin cậy 95% vào bảng forecasts trong cùng một giao dịch nguyên tử."],
            ["Bước 9", "Người dùng (User)", "FastAPI Backend", "Gửi GET /api/v1/forecast. Backend tính H_now = SHA256(DB) đối chiếu với H_train trong training_runs."],
            ["Bước 10", "FastAPI Backend", "Frontend Client", "Nếu H_now == H_train: trả về chuỗi dự báo chuẩn; nếu H_now != H_train: bật cờ is_stale=True cảnh báo màu hổ phách."]
        ]
    },
    {
        "title": "D.3. Đặc tả Lược đồ Thực thể Liên kết Cơ sở Dữ liệu ERD 11 Bảng (Database ERD Specifications)",
        "intro": "Mối quan hệ ràng buộc toàn vẹn khóa ngoại (Foreign Key) và quy tắc xóa lan truyền (ON DELETE CASCADE) giữa 11 bảng dữ liệu chuẩn hóa trong PostgreSQL:",
        "headers": ["Bảng dữ liệu gốc", "Khóa chính (PK)", "Quan hệ", "Bảng dữ liệu tham chiếu", "Khóa ngoại (FK) & Ràng buộc"],
        "rows": [
            ["commodities", "id (SERIAL)", "1 : N", "price_history", "commodity_id -> commodities.id (ON DELETE CASCADE, Index)"],
            ["commodities", "id (SERIAL)", "1 : N", "periodic_prices", "commodity_id -> commodities.id (ON DELETE CASCADE, Index)"],
            ["commodities", "id (SERIAL)", "1 : N", "training_runs", "commodity_id -> commodities.id (ON DELETE CASCADE, Index)"],
            ["commodities", "id (SERIAL)", "1 : N", "forecasts", "commodity_id -> commodities.id (ON DELETE CASCADE, Index)"],
            ["commodities", "id (SERIAL)", "1 : N", "alert_rules", "commodity_id -> commodities.id (ON DELETE CASCADE, Index)"],
            ["price_history", "id (BIGSERIAL)", "1 : N", "price_revisions", "price_history_id -> price_history.id (ON DELETE CASCADE)"],
            ["training_runs", "id (SERIAL)", "1 : N", "forecasts", "training_run_id -> training_runs.id (ON DELETE CASCADE)"],
            ["alert_rules", "id (SERIAL)", "1 : N", "alert_logs", "rule_id -> alert_rules.id (ON DELETE CASCADE)"],
            ["users", "id (SERIAL)", "1 : N", "alert_rules", "user_id -> users.id (ON DELETE SET NULL)"],
            ["background_jobs", "id (SERIAL)", "Độc lập", "—", "Lưu tiến trình cào dữ liệu (scrape) và huấn luyện lại AI (retrain)"],
            ["system_settings", "key (VARCHAR)", "Độc lập", "—", "Lưu cấu hình toàn cục hệ thống (active_model, maintenance_mode)"]
        ]
    }
]
