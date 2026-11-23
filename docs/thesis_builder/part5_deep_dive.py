# -*- coding: utf-8 -*-
"""
Phần 5: Nội dung chuyên sâu bổ sung cho Chương 1, Chương 2, Chương 3 và Chương 4
Đảm bảo báo cáo Khóa luận tốt nghiệp đạt đúng độ dài chuẩn 75 - 100 trang A4 nội dung chính
(Times New Roman 13pt, giãn dòng 1.5 lines, lề trái 3.5cm, phải 2cm, trên 2.5cm, dưới 2.5cm)
với 100% số liệu, cấu trúc bảng, thuật toán và 72 kịch bản kiểm thử thực tế của dự án AgroForecast.
"""

CH1_EXTRA_SUBSECTIONS = [
    {
        "code": "1.1.4.",
        "title": "Phân tích đặc tính chu kỳ thu hoạch và yếu tố mùa vụ của 8 mặt hàng nông sản Việt Nam",
        "paragraphs": [
            "Mỗi loại nông sản trong 8 mặt hàng mục tiêu của hệ thống AgroForecast sở hữu một lịch thời vụ sinh trưởng, thu hoạch và xuất bán tại vườn hoàn toàn khác biệt. Việc phân tích tường minh quy luật mùa vụ này là cơ sở khoa học trực tiếp để thiết kế các đặc trưng lịch (Calendar Features), cấu hình chuỗi Fourier mùa vụ trong mô hình Prophet và xây dựng bộ trọng số giải thích mô hình (Explainable AI - XAI).",
            "1. Đối với Cà phê Robusta (COFFEE_ROBUSTA): Niên vụ cà phê Việt Nam tại Tây Nguyên (Đắk Lắk, Lâm Đồng, Gia Lai, Đắk Nông) bắt đầu thu hoạch bói từ tháng 10, vào chính vụ thu hoạch rộ trong tháng 11 và tháng 12, và kết thúc phơi sấy vào tháng 1 năm sau. Trong giai đoạn thu hoạch rộ (tháng 11 - 12), lượng cà phê nhân xô mới đưa ra thị trường dồi dào kết hợp nhu cầu cần tiền mặt trả công thu hái của nông hộ thường tạo áp lực điều chỉnh giá ngắn hạn tại vườn. Ngược lại, từ tháng 5 đến tháng 9 là giai đoạn giáp hạt, tồn kho trong dân cạn dần, giá cà phê tại vườn nhạy cảm mạnh với tình hình thời tiết khô hạn tại Tây Nguyên và biến động tồn kho đạt chuẩn trên sàn London ICE Europe.",
            "2. Đối với Hồ tiêu đen (PEPPER_BLACK): Vụ thu hoạch hồ tiêu tại Gia Lai, Đắk Lắk, Đắk Nông, Bình Phước và Bà Rịa - Vũng Tàu diễn ra từ sau Tết Nguyên đán (tháng 2) đến hết tháng 4 dương lịch. Hồ tiêu khô có ưu thế bảo quản được lâu trong kho của hộ nông dân (từ 1 đến 3 năm nếu phơi đạt độ ẩm chuẩn <= 13%), do đó hành vi giữ hàng chờ giá của nông hộ tại Chư Sê (Gia Lai) hay Châu Đức (Bà Rịa - Vũng Tàu) đóng vai trò quyết định đến nguồn cung thực tế.",
            "3. Đối với Lúa gạo IR50404 (RICE_IR504): Đồng bằng sông Cửu Long có 3 vụ lúa chính trong năm: vụ Đông Xuân (thu hoạch tháng 2 - tháng 4, cho năng suất và chất lượng gạo tốt nhất), vụ Hè Thu (thu hoạch tháng 6 - tháng 8) và vụ Thu Đông (thu hoạch tháng 10 - tháng 11). Do lúa tươi IR50404 sau khi gặt có độ ẩm cao (24% - 28%) phải đưa vào lò sấy trong vòng 24 - 48 giờ, nông hộ tại Châu Phú, Thoại Sơn (An Giang) hay Tháp Mười (Đồng Tháp) chủ yếu bán lúa tươi ngay tại bờ ruộng cho thương lái ghe thủy nội địa.",
            "4. Đối với Mía đường 10 CCS (SUGARCANE): Vụ ép mía tại Phú Yên, Gia Lai, Tây Ninh và Hậu Giang kéo dài từ tháng 11 đến tháng 4 năm sau. Giá mía nguyên liệu bán tại ruộng phụ thuộc trực tiếp vào chữ đường thương mại (CCS - Commercial Cane Sugar): khi thời tiết nắng khô vào cuối vụ, chữ đường tích lũy trong cây mía tăng lên (từ 9 CCS lên 11 - 12 CCS), giúp giá thu mua thực tế tại ruộng tăng tương ứng 8% - 15%.",
            "5. Đối với Dâu tây Đà Lạt (STRAWBERRY) và Khoai tây Đà Lạt (POTATO): Tại Phường 7, Phường 8 (TP. Đà Lạt) và các huyện Lạc Dương, Đức Trọng, Đơn Dương (Lâm Đồng), khí hậu chia làm hai mùa rõ rệt: mùa khô (từ tháng 11 đến tháng 4 năm sau) với biên độ nhiệt ngày đêm lớn, nắng ấm ban ngày và se lạnh ban đêm là thời điểm vàng cho dâu tây Đà Lạt đạt độ ngọt (Brix) cao nhất và khoai tây đạt năng suất củ thương phẩm loại 1 cao nhất. Ngược lại, vào các tháng mưa dầm mùa hè (tháng 6 - tháng 9), tỷ lệ hao hụt tại vườn tăng cao đẩy giá bán tại vườn biến động mạnh.",
            "6. Đối với Khoai lang tím Nhật (SWEET_POTATO) và Hạt điều thô (CASHEW_NUT): Khoai lang tím tại huyện Bình Tân (Vĩnh Long) có chu kỳ canh tác 4 - 4,5 tháng và phụ thuộc chặt chẽ vào hạn ngạch kiểm dịch thực vật xuất khẩu chính ngạch. Trong khi đó, hạt điều thô tại Bù Đăng, Phú Riềng (Bình Phước) thu hoạch tập trung từ tháng 2 đến tháng 5, chịu tác động kép của năng suất đậu quả sau các đợt mưa trái mùa và nhu cầu nhập khẩu điều nhân của thị trường Hoa Kỳ, châu Âu.",
        ],
    },
]

CH2_EXTRA_SUBSECTIONS = [
    {
        "code": "2.1.5.",
        "title": "Quy trình chuẩn hóa dữ liệu Min-Max Scaling và kiến tạo mẫu cửa sổ trượt cho mạng học sâu",
        "paragraphs": [
            "Khác với các mô hình cây quyết định (Random Forest, XGBoost) vốn bất biến với phép biến đổi đơn điệu của thang đo đặc trưng, mạng nơ-ron hồi quy sâu PyTorch LSTM sử dụng các hàm kích hoạt phi tuyến Sigmoid sigma(z) = 1 / (1 + e^{-z}) và Hyperbolic Tangent tanh(z) = (e^z - e^{-z}) / (e^z + e^{-z}). Nếu đưa trực tiếp giá trị giá nông sản gốc (ví dụ 71.700 VNĐ/kg đối với cà phê hoặc 1.208.000 VNĐ/tấn đối với mía đường) vào mạng LSTM, tích vô hướng W * x sẽ rơi vào vùng bão hòa cực trị của hàm kích hoạt, làm cho đạo hàm tiến về 0 và khiến quá trình huấn luyện lan truyền ngược theo thời gian (Backpropagation Through Time - BPTT) hoàn toàn thất bại.",
            "Do đó, hệ thống AgroForecast thực hiện phép chuẩn hóa tuyến tính Min-Max Scaling đưa chuỗi giá về miền giá trị chuẩn [0, 1] hoặc [-1, 1] strictly dựa trên giá trị nhỏ nhất (p_min_train) và lớn nhất (p_max_train) của riêng Tập huấn luyện (Training Set): p_norm_t = (p_t - p_min_train) / (p_max_train - p_min_train + 10^{-8}). Việc chỉ tính p_min_train và p_max_train trên Tập huấn luyện mà không tính trên Tập kiểm thử Holdout là nguyên tắc bắt buộc để đảm bảo không xảy ra rò rỉ thông tin thống kê từ tương lai.",
            "Tiếp theo, chuỗi chuẩn hóa {p_norm_1, p_norm_2, ..., p_norm_{N_train}} được chuyển đổi thành tập các cặp tensor đầu vào - đầu ra theo cơ chế cửa sổ trượt độ dài L (Sliding Window Sequence Generation với L = 14 bước thời gian): với mỗi chỉ số k từ 1 đến N_train - L, tensor đầu vào X_k = [p_norm_k, p_norm_{k+1}, ..., p_norm_{k+L-1}]^T có kích thước (batch_size, seq_length = L, input_size = 1) được ánh xạ tới nhãn mục tiêu y_k = p_norm_{k+L}. Khi suy luận dự báo đa bước (Multi-step Recursive Forecasting) cho H ngày tương lai (H = 7, 10, 14, 30), giá trị dự báo chuẩn hóa hat{y}_{t+1} ở bước 1 được nối tiếp vào cuối cửa sổ trượt và dịch cửa sổ sang phải 1 đơn vị để dự báo bước t+2, lặp lại đệ quy cho đến hết bước t+H trước khi thực hiện phép biến đổi ngược: hat{p}_{t+h} = hat{y}_{t+h} * (p_max_train - p_min_train) + p_min_train.",
        ],
    },
    {
        "code": "2.2.6.",
        "title": "So sánh đặc tính toán học, ưu điểm và giới hạn của 5 mô hình học máy trong dự án",
        "paragraphs": [
            "Việc tích hợp đồng thời cả 5 mô hình thuộc 3 trường phái toán học khác nhau (Thống kê kinh tế lượng: ARIMA; Phân rã hàm cộng tính chu kỳ: Prophet; Học máy tổ hợp cây quyết định: Random Forest, XGBoost; và Mạng nơ-ron học sâu: LSTM) tạo nên một hệ thống dự báo đa mô hình bổ trợ lẫn nhau hoàn hảo. Bảng 2.1 tổng hợp đối sánh chi tiết cơ chế toán học, ưu điểm và giới hạn của từng mô hình khi áp dụng vào dữ liệu giá nông sản Việt Nam.",
        ],
        "tables": [
            {
                "caption": "Bảng 2.1. Đối sánh đặc tính kỹ thuật, ưu điểm và giới hạn của 5 mô hình dự báo trong hệ thống AgroForecast",
                "headers": ["Mô hình AI", "Nhóm thuật toán", "Cơ chế toán học cốt lõi", "Ưu điểm nổi bật trên giá nông sản", "Giới hạn & Điều kiện áp dụng tốt nhất"],
                "rows": [
                    ["ARIMA", "Thống kê tuyến tính (Box-Jenkins)", "Kết hợp tự hồi quy AR(p), sai phân I(d) và trung bình trượt sai số MA(q)", "Rất chính xác và ít quá khớp trên chuỗi giá biến động hẹp, ổn định ngắn hạn (như Lúa IR50404)", "Giả định quan hệ tuyến tính; phản ứng chậm trước các cú sốc phi tuyến đột ngột"],
                    ["Prophet", "Mô hình cộng tính tổng quát (GAM)", "Phân rã hàm xu thế gãy khúc g(t) + chuỗi lượng giác Fourier mùa vụ s(t)", "Xử lý tự động ngày nghỉ/khuyết dữ liệu; trực quan hóa tốt tính mùa vụ thu hoạch hàng năm", "Khi chuỗi ngắn hoặc có bước nhảy giá dốc đứng ở cuối chuỗi dễ bị phóng đại độ dốc xu thế"],
                    ["Random Forest", "Học máy tổ hợp (Bagging Trees)", "Trung bình cộng dự báo của B = 120 cây quyết định độc lập huấn luyện trên mẫu Bootstrap", "Phương sai sai số thấp, kháng nhiễu và điểm ngoại lai rất tốt, không bị bùng nổ dự báo", "Không thể ngoại suy vượt ra ngoài miền giá trị cực đại/cực tiểu đã từng xuất hiện trong quá khứ"],
                    ["XGBoost", "Học máy tăng cường (Gradient Boosting)", "Xây dựng chuỗi cây nối tiếp sửa sai số dư bằng đạo hàm bậc hai (Hessian) + điều chuẩn L1/L2", "Bắt nhịp cực nhạy với biến động mạnh và đảo chiều xu hướng (đứng số 1 trên Cà phê & Hồ tiêu)", "Cần trích xuất đầy đủ đặc trưng độ trễ (Lag) và động lượng (Momentum) chất lượng cao"],
                    ["PyTorch LSTM", "Học sâu chuỗi thời gian (Deep RNN)", "Ô nhớ dài hạn Cell State kết hợp 3 cổng Sigmoid/Tanh (Forget, Input, Output Gate)", "Học được các mẫu hình chu kỳ phi tuyến mượt mà dài hạn (đứng số 1 trên Dâu tây, Khoai tây, Điều)", "Đòi hỏi chuẩn hóa Min-Max chặt chẽ và thời gian tính toán huấn luyện cao hơn ARIMA/Trees"],
                ],
            }
        ],
    },
]

CH3_EXTRA_SUBSECTIONS = [
    {
        "code": "3.2.4.",
        "title": "Thiết kế chi tiết bảng trọng số Giải thích Mô hình (Explainable AI - XAI) cho 8 nông sản",
        "paragraphs": [
            "Trong lĩnh vực nông nghiệp thông minh (AgriTech), người nông dân và nhà phân phối không chỉ cần biết 'con số dự báo ngày mai là bao nhiêu' mà còn cần hiểu rõ 'những yếu tố thực tế nào đang thúc đẩy hoặc kìm hãm giá'. Tại mô-đun giao diện frontend/src/components/dashboard/XAIFeatureDrivers.tsx, hệ thống thiết kế bộ giải thích tầm quan trọng đặc trưng (Feature Importance Attribution) chuyên biệt cho từng mặt hàng nông sản, kết hợp giữa động lượng chuỗi thời gian của mô hình AI đang chọn và các yếu tố cơ bản của ngành hàng đó. Bảng 3.6 trình bày chi tiết cấu hình các nhân tố giải thích XAI trong hệ thống.",
        ],
        "tables": [
            {
                "caption": "Bảng 3.6. Đặc tả các nhân tố giải thích mô hình học máy (Explainable AI - XAI Drivers) theo từng nhóm nông sản",
                "headers": ["Nhóm nông sản", "Nhân tố ảnh hưởng thứ 1 (Trọng số cao nhất)", "Nhân tố ảnh hưởng thứ 2", "Nhân tố ảnh hưởng thứ 3", "Nhân tố ảnh hưởng thứ 4 & 5"],
                "rows": [
                    ["Cà phê Robusta (COFFEE_ROBUSTA)", "Động lượng giá trễ ngắn hạn (Lag t-1..t-7) & Tồn kho sàn London ICE (34%)", "Lượng mưa & Thời tiết vùng trồng Tây Nguyên (Đắk Lắk, Lâm Đồng) (26%)", "Tỷ giá ngoại tệ USD/VND & Chi phí cước tàu biển (18%)", "Chu kỳ thu hoạch vụ mới (12%) & Giá phân bón NPK đầu vào (10%)"],
                    ["Hồ tiêu đen (PEPPER_BLACK)", "Xu hướng giá thu mua nội địa 7 ngày gần nhất & Tâm lý trữ hàng tại hộ (36%)", "Nhu cầu nhập khẩu từ thị trường Trung Quốc, Mỹ, Châu Âu (25%)", "Sản lượng vụ thu hoạch mới tại Gia Lai, Đắk Lắk, Bà Rịa - Vũng Tàu (20%)", "Tỷ giá USD/VND (11%) & Chi phí vận chuyển xuất khẩu (8%)"],
                    ["Lúa gạo IR50404 (RICE_IR504)", "Quán tính giá lúa tươi tại ruộng An Giang - Đồng Tháp 7 ngày qua (35%)", "Tiến độ thu hoạch vụ Đông Xuân / Hè Thu / Thu Đông tại ĐBSCL (27%)", "Nhu cầu thu mua gạo xuất khẩu (Philippines, Indonesia) (20%)", "Điều kiện vận tải thủy nội địa & Chi phí sấy lúa (18%)"],
                    ["Dâu tây & Khoai tây Đà Lạt", "Biến động nhiệt độ, lượng mưa và độ ẩm tại TP. Đà Lạt - Lâm Đồng (36%)", "Động lượng giá cắt tại vườn Phường 7, Phường 8 tuần qua (30%)", "Nhu cầu tiêu thụ du lịch cuối tuần & Siêu thị TP.HCM (20%)", "Chi phí giống, nhà kính và vận chuyển lạnh (14%)"],
                    ["Khoai lang tím & Hạt điều thô", "Động lượng giá thu mua tại ruộng Bình Tân / vườn Bù Đăng (34%)", "Tiến độ thông quan xuất khẩu & Nhu cầu nhà máy chế biến (28%)", "Chu kỳ thời vụ thu hoạch và chất lượng củ/hạt thương phẩm (22%)", "Chi phí nhân công thu hoạch & vận tải nội địa (16%)"],
                ],
            }
        ],
    },
    {
        "code": "3.3.3.",
        "title": "Đặc tả cấu trúc các bảng Quản trị, Người dùng, Cảnh báo và Kiểm toán dữ liệu",
        "paragraphs": [
            "Bên cạnh các bảng lưu trữ chuỗi giá và kết quả dự báo, hệ thống Cơ sở dữ liệu PostgreSQL còn bao gồm 6 bảng phục vụ quản trị người dùng, kiểm toán lịch sử chỉnh sửa dữ liệu, vận hành cảnh báo tự động và theo dõi tác vụ nền. Bảng 3.7 đặc tả chi tiết cấu trúc của các bảng này.",
        ],
        "tables": [
            {
                "caption": "Bảng 3.7. Đặc tả cấu trúc bảng users, price_revisions, alert_rules, alert_logs và background_jobs",
                "headers": ["Tên bảng", "Tên trường (Column)", "Kiểu dữ liệu", "Ràng buộc", "Mô tả chi tiết ý nghĩa"],
                "rows": [
                    ["users", "id", "SERIAL / INTEGER", "PRIMARY KEY", "Mã định danh tự tăng của người dùng"],
                    ["users", "email", "VARCHAR(255)", "UNIQUE, NOT NULL, INDEX", "Địa chỉ email đăng nhập duy nhất của người dùng"],
                    ["users", "password_hash", "VARCHAR(255)", "NOT NULL", "Chuỗi mật khẩu đã băm một chiều bằng thuật toán Bcrypt + Salt"],
                    ["users", "full_name", "VARCHAR(255)", "NOT NULL", "Họ và tên hiển thị (đã làm sạch XSS qua sanitize_text)"],
                    ["users", "role", "VARCHAR(50)", "DEFAULT 'user'", "Vai trò phân quyền RBAC: admin | analyst | user"],
                    ["users", "is_active", "BOOLEAN", "DEFAULT TRUE", "Trạng thái kích hoạt tài khoản (False = bị khóa bởi Admin)"],
                    ["price_revisions", "id", "SERIAL / INTEGER", "PRIMARY KEY", "Mã định danh bản ghi lưu vết chỉnh sửa giá"],
                    ["price_revisions", "price_history_id", "INTEGER", "FK -> price_history.id", "Liên kết tới bản ghi giá gốc bị chỉnh sửa"],
                    ["price_revisions", "price", "NUMERIC(12, 2)", "NOT NULL", "Giá trị cũ trước khi bị Quản trị viên ghi đè"],
                    ["price_revisions", "provenance", "VARCHAR(30)", "NOT NULL", "Trạng thái nguồn gốc cũ trước khi chỉnh sửa"],
                    ["alert_rules", "id", "SERIAL / INTEGER", "PRIMARY KEY", "Mã định danh quy tắc cảnh báo biến động giá"],
                    ["alert_rules", "commodity_id", "INTEGER", "FK -> commodities.id", "Mặt hàng nông sản cần theo dõi biến động giá"],
                    ["alert_rules", "rule_name", "VARCHAR(255)", "NOT NULL", "Tên quy tắc cảnh báo do người dùng đặt (đã lọc XSS)"],
                    ["alert_rules", "condition_type", "VARCHAR(50)", "NOT NULL", "Điều kiện kích hoạt: PRICE_ABOVE (vượt ngưỡng) | PRICE_BELOW (thấp hơn)"],
                    ["alert_rules", "threshold_value", "NUMERIC(12, 2)", "NOT NULL", "Mức giá ngưỡng kích hoạt cảnh báo (VNĐ/kg hoặc VNĐ/tấn)"],
                    ["alert_rules", "email", "VARCHAR(255)", "NOT NULL", "Địa chỉ Email nhận thông báo tự động khi điều kiện thỏa mãn"],
                    ["alert_logs", "id", "SERIAL / INTEGER", "PRIMARY KEY", "Mã định danh nhật ký cảnh báo đã kích hoạt"],
                    ["alert_logs", "rule_id", "INTEGER", "FK -> alert_rules.id", "Quy tắc cảnh báo đã được kích hoạt"],
                    ["alert_logs", "triggered_price", "NUMERIC(12, 2)", "NOT NULL", "Mức giá thực tế tại thời điểm kích hoạt cảnh báo"],
                    ["alert_logs", "message", "TEXT", "NOT NULL", "Nội dung thông điệp cảnh báo chi tiết đã gửi"],
                    ["background_jobs", "id", "SERIAL / INTEGER", "PRIMARY KEY", "Mã định danh tiến trình chạy ngầm (Scrape / Retrain)"],
                    ["background_jobs", "kind / status", "VARCHAR(40)", "NOT NULL, INDEX", "Loại tác vụ (scrape | retrain) và trạng thái (RUNNING | SUCCESS | FAILED)"],
                    ["background_jobs", "records_processed", "INTEGER", "DEFAULT 0", "Số lượng bản ghi giá hoặc điểm dự báo đã xử lý thành công"],
                ],
            }
        ],
    },
]
