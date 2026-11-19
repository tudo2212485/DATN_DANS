# -*- coding: utf-8 -*-
"""
Phần 12: Mở rộng chuyên sâu nội dung 4 chương của Khóa luận tốt nghiệp
bằng việc phân tích chi tiết kiến trúc mã nguồn, cấu trúc từng bảng CSDL, từng Endpoint API,
kịch bản thực nghiệm từng mặt hàng và từng bài kiểm thử của dự án AgroForecast.
"""

def get_chapter_expansions():
    exp1 = [
        {
            "code": "1.4.3.",
            "title": "Phân tích ý nghĩa khoa học và tác động kinh tế - xã hội của hệ thống đối với nông nghiệp Việt Nam",
            "paragraphs": [
                "Về mặt ý nghĩa khoa học, đề tài đóng góp một khung kiến trúc tham chiếu toàn diện (Reference Architecture) cho bài toán dự báo chuỗi thời gian kinh tế nông nghiệp tại các quốc gia đang phát triển có cấu trúc thị trường phân mảnh như Việt Nam. Thay vì tiếp cận bài toán dự báo giá như một bài toán khớp hàm thuần túy trên dữ liệu tĩnh, khóa luận đã kết hợp chặt chẽ ba trụ cột của Khoa học Dữ liệu hiện đại: (1) Quản trị dữ liệu có kiểm chứng nguồn gốc (Data Provenance & Cryptographic Fingerprinting); (2) Huấn luyện đối sánh đa mô hình học máy qua kiểm định giữ lại theo thời gian (Multi-Model Walk-Forward Tournament); và (3) Phân rã không gian - thời gian xuống cấp độ giá bán tại vườn/ruộng địa phương (Spatio-Temporal Farm-Gate Decomposition).",
                "Về mặt tác động kinh tế - xã hội đối với nông hộ và hợp tác xã tại tỉnh Lâm Đồng, khu vực Tây Nguyên và Đồng bằng sông Cửu Long: khi người nông dân trồng cà phê tại huyện Cư M'gar, huyện Di Linh hay trồng dâu tây, khoai tây tại Phường 7, Phường 8 (TP. Đà Lạt) nắm bắt được xu hướng dự báo 7 đến 30 ngày tới cùng biên độ dao động 95% (LowerCI - UpperCI), họ có cơ sở định lượng rõ ràng để thương lượng giá bán tại vườn với thương lái, tránh bị ép giá bất hợp lý do thiếu thông tin. Đồng thời, hệ thống cảnh báo biến động giá tự động qua Email giúp nông hộ và các doanh nghiệp thu mua chế biến chủ động lập kế hoạch thu hoạch, sấy bảo quản và chốt hợp đồng cung ứng đúng thời điểm tối ưu.",
            ],
        },
    ]

    exp2 = [
        {
            "code": "2.2.7.",
            "title": "Phân tích chi tiết thuật toán huấn luyện và suy luận của từng mô hình trong mã nguồn thực tế",
            "paragraphs": [
                "Trong tệp mã nguồn backend/app/services/training_service.py và backend/ml_pipeline/model_trainer.py, mỗi thuật toán trong 5 mô hình học máy được cài đặt với quy trình tiền xử lý, hàm mất mát và cơ chế suy luận đệ quy chuyên biệt nhằm khai thác tối đa thế mạnh của từng kiến trúc:",
                "1. Quy trình thực thi chi tiết của mô hình ARIMA (predict_arima): Chuỗi giá lịch sử S có độ dài N được chuyển sang mảng số thực dấu phẩy động 64-bit (float64). Hệ thống khởi tạo đối tượng statsmodels.tsa.arima.model.ARIMA(series, order=(2, 1, 1)). Trong quá trình gọi phương thức fit(), bộ giải trạng thái - không gian tính toán sai phân bậc 1: Delta y_t = y_t - y_{t-1}, sau đó ước lượng đồng thời hai hệ số tự hồi quy phi_1, phi_2 và hệ số trung bình trượt theta_1 bằng cách cực đại hóa hàm log-likelihood. Khi suy luận dự báo H bước tương lai qua phương thức forecast(steps=horizon), phương trình trạng thái tự động ngoại suy quỹ đạo trung tâm và truyền qua hàm chặn dưới np.maximum(0.0, pred) để đảm bảo giá nông sản không bao giờ nhận giá trị âm.",
                "2. Quy trình thực thi chi tiết của mô hình Facebook Prophet (predict_prophet): Hệ thống chuẩn hóa chuỗi lịch sử thành cấu trúc bảng DataFrame hai cột bắt buộc của Prophet là 'ds' (mốc thời gian kiểu datetime64) và 'y' (giá trị giá thực tế). Đối tượng Prophet được khởi tạo với cấu hình tắt mùa vụ ngày (daily_seasonality = False do dữ liệu nông sản thu thập theo ngày làm việc không có biến động theo giờ), bật mùa vụ tuần (weekly_seasonality = True) và tự động bật mùa vụ năm nếu độ dài chuỗi lịch sử vượt quá 180 ngày. Sau khi gọi model.fit(df), hệ thống kiến tạo khung thời gian tương lai future = model.make_future_dataframe(periods=horizon, freq=step) khớp chính xác với tần suất công bố của từng loại nông sản (1 ngày đối với chuỗi daily, bước nhảy kỳ đối với chuỗi periodic) và trích xuất cột dự báo trung tâm 'yhat'.",
                "3. Quy trình thực thi chi tiết của mô hình Random Forest và XGBoost (predict_tree): Hàm tabular_features(series) quét qua toàn bộ chuỗi từ chỉ số idx = 14 đến N - 1 để kiến tạo ma trận đặc trưng X gồm 12 cột: [lag_1, lag_2, lag_3, lag_7, lag_14, mean_7, std_7, mean_14, diff_1, diff_7, day_of_week, month] và véc-tơ nhãn mục tiêu y = p_{idx}. Đối với XGBoost, hệ thống khởi tạo XGBRegressor(n_estimators=120, max_depth=4, learning_rate=0.06, subsample=0.9, colsample_bytree=0.9, random_state=42, verbosity=0); đối với Random Forest, hệ thống khởi tạo RandomForestRegressor(n_estimators=120, max_depth=6, random_state=42). Khi dự báo tương lai từng bước từ step = 1 đến H, giá trị dự báo mới nhất vừa sinh ra được đẩy ngay vào danh sách lịch sử tạm thời (history.append(pred)), từ đó tính lại tức thời lag_1, mean_7, std_7, diff_1 cho bước dự báo kế tiếp.",
                "4. Quy trình thực thi chi tiết của mô hình Học sâu LSTM (predict_lstm & TorchLSTMModel): Trong ml_pipeline/model_trainer.py, lớp mạng nơ-ron TorchLSTMModel kế thừa từ torch.nn.Module bao gồm khối nn.LSTM(input_size=1, hidden_size=64, num_layers=2, batch_first=True, dropout=0.2) nối tiếp với tầng tuyến tính nn.Linear(64, 1). Chuỗi giá được chuẩn hóa MinMaxScaler vào miền [-1, 1] hoặc [0, 1], cắt thành các cửa sổ trượt độ dài window = 14 bước thời gian. Trong mỗi kỷ nguyên huấn luyện (epoch), mạng xóa đạo hàm cũ (optimizer.zero_grad()), truyền xuôi tensor X_batch qua 2 tầng LSTM để lấy trạng thái ẩn ở bước thời gian cuối cùng out[:, -1, :], tính hàm mất mát MSELoss so với nhãn y_batch, lan truyền ngược (loss.backward()) và cập nhật trọng số bằng bộ tối ưu Adam trước khi giải chuẩn hóa về đơn vị VNĐ.",
            ],
        },
    ]

    exp3 = [
        {
            "code": "3.1.9.",
            "title": "Đặc tả chi tiết quy tắc kiểm tra tính hợp lệ dữ liệu và xử lý lỗi (Error Handling Matrix)",
            "paragraphs": [
                "Một hệ thống phần mềm đạt chuẩn kỹ sư Công nghệ Thông tin không chỉ xử lý đúng khi người dùng nhập dữ liệu chuẩn (Happy Path) mà quan trọng hơn là phải kiểm soát chặt chẽ mọi tình huống dữ liệu biên, dữ liệu khuyết và hành vi truy cập bất hợp lệ (Edge Cases & Exception Paths). Bảng 3.9 đặc tả ma trận các quy tắc kiểm tra tính hợp lệ và mã trạng thái HTTP phản hồi chuẩn hóa trên toàn bộ hệ thống AgroForecast.",
            ],
            "tables": [
                {
                    "caption": "Bảng 3.9. Ma trận quy tắc kiểm tra tính hợp lệ dữ liệu và xử lý ngoại lệ HTTP trong hệ thống AgroForecast",
                    "headers": ["Tình huống kiểm tra / Ngoại lệ", "Tầng xử lý", "Mã HTTP", "Cơ chế xử lý và thông điệp phản hồi chuẩn"],
                    "rows": [
                        ["Email đăng ký đã tồn tại trong CSDL", "auth.py", "400 Bad Request", "Kiểm tra ilike(email), từ chối tạo trùng và báo Email đã đăng ký"],
                        ["Ngày bắt đầu > Ngày kết thúc hoặc > Hôm nay", "history.py / admin.py", "400 Bad Request", "Chặn truy vấn lịch sử/cào dữ liệu tương lai, báo khoảng ngày không hợp lệ"],
                        ["Tập tin tải lên không phải .csv hoặc > 5 MB", "admin.py", "400 Bad Request", "Kiểm tra đuôi tập tin và giới hạn kích thước đọc tối đa 5.242.880 byte"],
                        ["Admin tự hạ quyền hoặc tự khóa chính mình", "admin.py", "400 Bad Request", "So sánh user.id == current_user.id, bảo vệ tài khoản quản trị đang hoạt động"],
                        ["Thiếu Bearer Token hoặc JWT hết hạn / bị sửa", "deps.py / security.py", "401 Unauthorized", "Kiểm tra chữ ký HMAC-SHA256 và nhãn thời gian exp, trả về WWW-Authenticate"],
                        ["Tài khoản thường gọi API Admin hoặc bị khóa", "deps.py / auth.py", "403 Forbidden", "Kiểm tra is_active == False hoặc role không thuộc allowed_roles"],
                        ["Truy vấn ID nông sản / bản ghi giá không tồn tại", "commodities / admin", "404 Not Found", "Kiểm tra kết quả truy vấn ORM bằng None, trả về thông báo không tìm thấy"],
                        ["Dữ liệu lịch sử thay đổi lệch mã băm SHA-256", "forecast_service.py", "409 Conflict", "So sánh run.dataset_hash != fingerprint(rows), yêu cầu huấn luyện lại AI"],
                        ["Kích hoạt trùng 2 tiến trình nền cùng loại", "job_service.py", "409 Conflict", "Kiểm tra BackgroundJob.status == 'RUNNING', ngăn chặn xung đột CPU/DB"],
                        ["Dữ liệu JSON sai kiểu, giá âm, mật khẩu < 6 ký tự", "Pydantic v2 Schemas", "422 Unprocessable", "Tự động từ chối tại biên Router và trả về chi tiết trường dữ liệu vi phạm"],
                        ["Gửi quá 25 request đăng nhập / 60 giây từ 1 IP", "security.py", "429 Too Many Req", "Sliding Window RateLimiter chặn tạm thời IP tấn công vét cạn mật khẩu"],
                        ["Lỗi ngoại lệ hệ thống không lường trước", "main.py", "500 Server Error", "Global Exception Handler ghi Stack Trace vào log nội bộ, ẩn thông tin nhạy cảm"],
                    ],
                }
            ],
        },
    ]

    exp4 = [
        {
            "code": "4.3.4.",
            "title": "Đánh giá trải nghiệm người dùng (UI/UX) và khả năng tương thích đa thiết bị (Responsive Design)",
            "paragraphs": [
                "Giao diện của hệ thống AgroForecast đã được kiểm thử hiển thị thực tế trên nhiều độ phân giải màn hình khác nhau từ máy tính để bàn phân giải cao (Desktop 1440px - 1920px), máy tính xách tay (Laptop 1280px - 1366px), máy tính bảng (Tablet 768px - 1024px) cho đến điện thoại thông minh (Mobile 375px - 430px). Nhờ sử dụng hệ thống lưới đáp ứng CSS Grid (grid-cols-1 sm:grid-cols-2 lg:grid-cols-4) và thanh điều hướng bên thu gọn thông minh (Collapsible Sidebar), mọi bảng số liệu và biểu đồ dự báo Recharts đều tự động co giãn mượt mà theo khung nhìn (ResponsiveContainer width='100%').",
                "Đặc biệt, việc chuyển đổi sang bộ phông chữ kỹ thuật hiện đại Plus Jakarta Sans (hỗ trợ đầy đủ dấu tiếng Việt) kết hợp phông chữ số đơn cách JetBrains Mono đã giải quyết triệt để lỗi hiển thị dấu tiếng Việt trên trình duyệt Windows và giúp người dùng đọc nhanh hàng trăm con số giá cả, biên độ dự báo và chỉ số sai số mà không bị mỏi mắt.",
            ],
        },
    ]

    return exp1, exp2, exp3, exp4
