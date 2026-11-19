# -*- coding: utf-8 -*-
"""
Phần 1: Các trang đầu khóa luận (Mẫu M01 -> M06, Cam đoan, Cảm ơn, Mục lục, Ký hiệu viết tắt, Tóm tắt)
MỞ ĐẦU và Chương 1: TỔNG QUAN
Tuân thủ tuyệt đối Quy định Hình thức Trình bày KLTN - Khoa CNTT - Trường Đại học Đà Lạt.
"""

FRONT_MATTER = {
    "university": "TRƯỜNG ĐẠI HỌC ĐÀ LẠT",
    "faculty": "KHOA CÔNG NGHỆ THÔNG TIN",
    "student_name": "<HỌ VÀ TÊN SINH VIÊN>",
    "student_id": "<MÃ SỐ SINH VIÊN>",
    "cohort": "Khóa 46 (2022 - 2026)",
    "major": "Kỹ thuật Phần mềm / Khoa học Dữ liệu",
    "advisor": "<TÊN GV HƯỚNG DẪN>",
    "thesis_title": "NGHIÊN CỨU VÀ XÂY DỰNG HỆ THỐNG DỰ ĐOÁN BIẾN ĐỘNG GIÁ NÔNG SẢN VIỆT NAM BẰNG MÔ HÌNH HỌC MÁY",
    "degree_title": "KHÓA LUẬN TỐT NGHIỆP KỸ SƯ CÔNG NGHỆ THÔNG TIN",
    "location_year": "Đà Lạt, Năm 2026",
}

ABBREVIATIONS = [
    ("ADF", "Augmented Dickey-Fuller (Kiểm định nghiệm đơn vị tính dừng chuỗi thời gian)"),
    ("AI", "Artificial Intelligence (Trí tuệ nhân tạo)"),
    ("API", "Application Programming Interface (Giao diện lập trình ứng dụng)"),
    ("ARIMA", "AutoRegressive Integrated Moving Average (Tự hồi quy tích hợp trung bình trượt)"),
    ("CCS", "Commercial Cane Sugar (Chữ đường thương mại trong mía nguyên liệu)"),
    ("CI", "Confidence Interval (Khoảng tin cậy dự báo)"),
    ("CORS", "Cross-Origin Resource Sharing (Chia sẻ tài nguyên khác nguồn gốc)"),
    ("CRUD", "Create, Read, Update, Delete (Tạo mới, Đọc, Cập nhật, Xóa dữ liệu)"),
    ("CSDL", "Cơ sở dữ liệu"),
    ("CSV", "Comma-Separated Values (Định dạng tập tin giá trị phân tách bằng dấu phẩy)"),
    ("DAST", "Dynamic Application Security Testing (Kiểm thử bảo mật ứng dụng động)"),
    ("ĐBSCL", "Đồng bằng sông Cửu Long"),
    ("ERD", "Entity-Relationship Diagram (Sơ đồ thực thể kết hợp)"),
    ("HSTS", "HTTP Strict Transport Security (Chính sách bắt buộc giao tiếp an toàn HTTPS)"),
    ("HTTP", "HyperText Transfer Protocol (Giao thức truyền tải siêu văn bản)"),
    ("IQR", "Interquartile Range (Khoảng tứ phân vị dùng để lọc giá trị ngoại lai)"),
    ("JSON", "JavaScript Object Notation (Định dạng trao đổi dữ liệu văn bản nhẹ)"),
    ("JWT", "JSON Web Token (Chuẩn mã thông báo xác thực chữ ký số)"),
    ("LSTM", "Long Short-Term Memory (Mạng nơ-ron hồi quy bộ nhớ dài-ngắn)"),
    ("MAE", "Mean Absolute Error (Sai số tuyệt đối trung bình)"),
    ("MAPE", "Mean Absolute Percentage Error (Sai số phần trăm tuyệt đối trung bình)"),
    ("ML", "Machine Learning (Học máy)"),
    ("ORM", "Object-Relational Mapping (Ánh xạ quan hệ hướng đối tượng)"),
    ("OWASP", "Open Worldwide Application Security Project (Tổ chức bảo mật ứng dụng mở toàn cầu)"),
    ("RBAC", "Role-Based Access Control (Kiểm soát truy cập dựa trên vai trò)"),
    ("REST", "Representational State Transfer (Kiến trúc dịch vụ Web phi trạng thái)"),
    ("RMSE", "Root Mean Square Error (Sai số bình phương trung bình căn bậc hai)"),
    ("RNN", "Recurrent Neural Network (Mạng nơ-ron hồi quy)"),
    ("SAST", "Static Application Security Testing (Phân tích bảo mật mã nguồn tĩnh)"),
    ("SQL", "Structured Query Language (Ngôn ngữ truy vấn có cấu trúc)"),
    ("SQLi", "SQL Injection (Lỗ hổng tấn công tiêm mã lệnh SQL)"),
    ("UI/UX", "User Interface / User Experience (Giao diện và Trải nghiệm người dùng)"),
    ("VFA", "Vietnam Food Association (Hiệp hội Lương thực Việt Nam)"),
    ("VICOFA", "Vietnam Coffee-Cocoa Association (Hiệp hội Cà phê - Ca cao Việt Nam)"),
    ("VINACAS", "Vietnam Cashew Association (Hiệp hội Điều Việt Nam)"),
    ("VPSA", "Vietnam Pepper and Spice Association (Hiệp hội Hồ tiêu và Cây gia vị Việt Nam)"),
    ("VSSA", "Vietnam Sugarcane and Sugar Association (Hiệp hội Mía đường Việt Nam)"),
    ("XAI", "Explainable Artificial Intelligence (Trí tuệ nhân tạo có khả năng giải thích)"),
    ("XGBoost", "Extreme Gradient Boosting (Thuật toán tăng cường độ dốc cực đại)"),
    ("XSS", "Cross-Site Scripting (Lỗ hổng tấn công chèn kịch bản độc hại chéo trang)"),
]

MO_DAU_SECTIONS = [
    (
        "1. Lý do chọn đề tài",
        [
            "Việt Nam là quốc gia có nền nông nghiệp nhiệt đới giữ vai trò trụ cột trong cơ cấu kinh tế và đảm bảo sinh kế cho hàng chục triệu nông hộ tại các vùng chuyên canh trọng điểm như Tây Nguyên, Đồng bằng sông Cửu Long, Đông Nam Bộ và Duyên hải miền Trung. Các mặt hàng nông sản chủ lực của Việt Nam bao gồm cà phê Robusta, hồ tiêu đen, lúa gạo, hạt điều, mía đường cũng như nhóm nông sản ôn đới đặc sản tại Đà Lạt - Lâm Đồng (dâu tây, khoai tây) và khoai lang xuất khẩu tại Vĩnh Long đóng góp hàng chục tỷ USD kim ngạch xuất khẩu mỗi năm. Tuy nhiên, một trong những thách thức lớn nhất mà người nông dân, hợp tác xã, thương lái thu mua và doanh nghiệp chế biến phải đối mặt hàng ngày là hiện tượng biến động giá nông sản diễn ra vô cùng phức tạp, phi tuyến tính và chịu tác động đồng thời của nhiều yếu tố vĩ mô lẫn vi mô.",
            "Trên thực tế sản xuất tại địa phương, giá nông sản mà người nông dân trực tiếp bán ra tại vườn hoặc tại ruộng (Farm-gate Price) không hoàn toàn đồng nhất với mức giá tham chiếu bình quân toàn vùng hay giá giao dịch trên sàn kỳ hạn quốc tế. Chẳng hạn, cùng là mặt hàng cà phê nhân xô Robusta nhưng giá bán tại vườn ở huyện Cư M'gar (Đắk Lắk) luôn có sự chênh lệch nhất định so với giá bán tại vườn ở huyện Di Linh (Lâm Đồng) hay huyện Chư Prông (Gia Lai) do khác biệt về độ ẩm hạt trong mùa mưa, chi phí vận chuyển từ rẫy về kho chế biến và chất lượng sàng hạt. Tương tự, giá lúa tươi IR50404 thương lái cân trực tiếp tại ruộng ở huyện Châu Phú (An Giang) khác với huyện Tháp Mười (Đồng Tháp) hay huyện Tân Hiệp (Kiên Giang) tùy thuộc vào điều kiện ghe vận tải thủy nội địa.",
            "Hiện nay, phần lớn nông hộ và thương lái địa phương vẫn tiếp cận thông tin giá cả theo phương thức truyền thống thông qua truyền miệng, các bản tin tổng hợp rời rạc hoặc mạng xã hội mà thiếu đi công cụ phân tích xu hướng định lượng có cơ sở khoa học. Hệ quả là tình trạng 'được mùa mất giá', bán tháo nông sản ngay trước thời điểm giá phục hồi, hoặc trữ hàng sai thời điểm gây thiệt hại kinh tế nặng nề. Mặt khác, các nghiên cứu học thuật hiện có về dự báo giá nông sản thường chỉ dừng lại ở việc chạy thử nghiệm một thuật toán đơn lẻ trên tập dữ liệu tĩnh trong phòng thí nghiệm mà chưa giải quyết được bài toán hoàn chỉnh từ khâu tự động thu thập dữ liệu thực tế, kiểm chứng nguồn gốc dữ liệu (Data Provenance), huấn luyện đối sánh đa mô hình học máy, ước lượng dải tin cậy rủi ro (Confidence Interval), phân rã giá bán tại vườn theo từng huyện địa phương cho đến việc xây dựng một hệ thống phần mềm hoàn chỉnh đáp ứng tiêu chuẩn kiểm thử và an toàn bảo mật thông tin.",
            "Xuất phát từ nhu cầu thực tiễn cấp thiết đó tại địa bàn tỉnh Lâm Đồng, khu vực Tây Nguyên và cả nước, việc thực hiện đề tài 'Nghiên cứu và xây dựng hệ thống dự đoán biến động giá nông sản Việt Nam bằng mô hình học máy' (AgroForecast) mang ý nghĩa khoa học và giá trị ứng dụng thực tiễn cao, góp phần số hóa quy trình phân tích thị trường nông sản và hỗ trợ ra quyết định hiệu quả cho nông hộ cũng như doanh nghiệp nông nghiệp.",
        ],
    ),
    (
        "2. Mục đích nghiên cứu",
        [
            "Mục đích cốt lõi của khóa luận là nghiên cứu, thiết kế và xây dựng hoàn chỉnh hệ thống thông tin dự báo biến động giá nông sản Việt Nam (AgroForecast) kết hợp giữa nền tảng công nghệ Web hiện đại và đường ống học máy chuỗi thời gian tự động (Automated Time-Series Machine Learning Pipeline). Cụ thể, đề tài hướng tới năm mục tiêu trọng tâm sau đây:",
            "Thứ nhất, xây dựng cơ chế thu thập, làm sạch và quản trị dữ liệu lịch sử giá nông sản có kiểm chứng nguồn gốc (Data Provenance) từ các cơ quan, viện nghiên cứu và hiệp hội ngành hàng chính thống tại Việt Nam, đảm bảo nguyên tắc chỉ sử dụng dữ liệu đã xác minh ('collected' và 'reviewed') để huấn luyện mô hình trí tuệ nhân tạo.",
            "Thứ hai, nghiên cứu cơ sở toán học, cài đặt và huấn luyện thực nghiệm đồng thời 5 mô hình học máy và thống kê chuỗi thời gian tiêu biểu bao gồm: ARIMA (AutoRegressive Integrated Moving Average), Facebook Prophet, Random Forest Regressor, XGBoost (Extreme Gradient Boosting) và mạng nơ-ron học sâu PyTorch LSTM (Long Short-Term Memory) trên dữ liệu thực tế của 8 loại nông sản chủ lực.",
            "Thứ ba, thiết lập cơ chế kiểm định chéo theo thời gian (Walk-Forward Holdout Validation) và cổng chặn sai số tự động (Threshold Gate) dựa trên 4 chỉ số đánh giá chuẩn (MAE, RMSE, MAPE và hệ số xác định R2) nhằm tự động lựa chọn mô hình tối ưu nhất cho từng mặt hàng nông sản ở các khung thời gian dự báo 7 ngày, 10 ngày, 14 ngày và 30 ngày tới.",
            "Thứ tư, giải quyết bài toán dự báo giá theo không gian - thời gian (Spatio-Temporal Regional Pricing) thông qua mô hình hóa độ lệch giá cơ sở (Basis Spread) tại 29 địa phương cấp huyện, thị xã, phường sản xuất trọng điểm, giúp phản ánh chính xác mức giá nông hộ bán ra trực tiếp tại vườn và tại ruộng.",
            "Thứ năm, thiết kế giao diện người dùng (UI/UX) trực quan, hiện đại theo phong cách tài chính nông nghiệp (Modern Clean Fintech x Sustainable AgriTech) và triển khai quy trình kiểm thử phần mềm 4 tầng kết hợp kiểm tra bảo mật toàn diện theo tiêu chuẩn quốc tế OWASP Top 10 với 72 kịch bản kiểm thử tự động.",
        ],
    ),
    (
        "3. Đối tượng nghiên cứu",
        [
            "Đối tượng nghiên cứu của khóa luận bao gồm hai nhóm chính: nhóm đối tượng dữ liệu nông sản thực nghiệm và nhóm đối tượng mô hình toán học - công nghệ phần mềm.",
            "Về đối tượng dữ liệu nông sản, khóa luận tập trung nghiên cứu chuỗi dữ liệu lịch sử giá và quy luật biến động giá bán tại vườn/ruộng của 8 mặt hàng nông sản tiêu biểu đại diện cho các vùng sinh thái nông nghiệp Việt Nam: (1) Lúa gạo IR50404 (mã RICE_IR504, đơn vị VNĐ/kg); (2) Cà phê nhân xô Robusta (mã COFFEE_ROBUSTA, đơn vị VNĐ/kg); (3) Hồ tiêu đen xô khô (mã PEPPER_BLACK, đơn vị VNĐ/kg); (4) Mía nguyên liệu 10 CCS (mã SUGARCANE, đơn vị VNĐ/tấn); (5) Dâu tây tươi Đà Lạt (mã STRAWBERRY, đơn vị VNĐ/kg); (6) Khoai lang tím Nhật Vĩnh Long (mã SWEET_POTATO, đơn vị VNĐ/kg); (7) Khoai tây thương phẩm Đà Lạt (mã POTATO, đơn vị VNĐ/kg); và (8) Hạt điều thô (mã CASHEW_NUT, đơn vị VNĐ/kg).",
            "Về đối tượng thuật toán và công nghệ, khóa luận nghiên cứu sâu các kỹ thuật tiền xử lý chuỗi thời gian (kiểm định tính dừng ADF, xử lý ngoại lai bằng khoảng tứ phân vị IQR, trích xuất đặc trưng độ trễ Lag và thống kê cửa sổ trượt Rolling Window), 5 thuật toán dự báo chuỗi thời gian (ARIMA, Prophet, Random Forest, XGBoost, LSTM), kỹ thuật giải thích mô hình học máy (Explainable AI - XAI), kiến trúc dịch vụ Web RESTful API với FastAPI, cơ sở dữ liệu quan hệ PostgreSQL, giao diện Next.js 14 và các kỹ thuật kiểm thử tự động, phòng vệ bảo mật ứng dụng Web.",
        ],
    ),
    (
        "4. Phương pháp nghiên cứu",
        [
            "Để giải quyết triệt để các mục tiêu đề ra, khóa luận áp dụng kết hợp bốn phương pháp nghiên cứu khoa học gắn liền với quy trình kỹ nghệ phần mềm và khoa học dữ liệu:",
            "Một là phương pháp nghiên cứu tài liệu và tổng hợp lý thuyết: Thu thập, phân tích các bài báo khoa học trong và ngoài nước về dự báo chuỗi thời gian nông sản; nghiên cứu tài liệu kỹ thuật của các thuật toán ARIMA, Prophet, cây quyết định tổ hợp (Random Forest, XGBoost), mạng học sâu LSTM và tài liệu chuẩn bảo mật OWASP Web Security Testing Guide.",
            "Hai là phương pháp thu thập và xử lý dữ liệu thực tiễn: Xây dựng các bộ thu thập và bóc tách dữ liệu tự động (Parsers/Scrapers) từ các nguồn công bố chính thức tại Việt Nam như Viện Chính sách và Chiến lược Phát triển Nông nghiệp Nông thôn (AGROINFO), Hiệp hội Hồ tiêu và Cây gia vị Việt Nam (VPSA), Hiệp hội Điều Việt Nam (VINACAS), Hiệp hội Mía đường Việt Nam (VSSA), Sở Nông nghiệp và Phát triển Nông thôn các tỉnh Tây Nguyên và Đồng bằng sông Cửu Long. Mọi bản ghi đều được gắn nhãn nguồn gốc (provenance) và kiểm tra chữ ký băm dữ liệu SHA-256 (dataset_hash) trước khi đưa vào huấn luyện.",
            "Ba là phương pháp thực nghiệm định lượng và đối sánh mô hình (Empirical Backtesting): Thiết lập quy trình huấn luyện và kiểm định độc lập cho từng mặt hàng nông sản bằng cách tách biệt nghiêm ngặt tập huấn luyện (Training Set) và tập kiểm thử giữ lại theo thời gian (Temporal Holdout Test Set). Đo lường khách quan 4 chỉ số sai số MAE, RMSE, MAPE, R2 và đối chiếu với mô hình cơ sở (Naive Persistence Baseline) để chứng minh hiệu quả thực tế của từng thuật toán.",
            "Bốn là phương pháp kiểm thử phần mềm đa tầng và kiểm tra thâm nhập bảo mật: Áp dụng mô hình kết hợp kiểm thử hộp trắng (White-box Unit Testing), kiểm thử hộp xám (Grey-box API & Database Integration Testing) và kiểm thử hộp đen (Black-box End-to-End Testing) cùng các kịch bản tấn công bảo mật giả lập tự động (SQL Injection, XSS, CSV Formula Injection, JWT Tampering, RBAC Privilege Escalation, Rate Limiting) bằng công cụ Pytest trên môi trường cơ sở dữ liệu cô lập.",
        ],
    ),
    (
        "5. Phạm vi nghiên cứu và Bố cục của khóa luận",
        [
            "Về phạm vi không gian và dữ liệu: Hệ thống tập trung vào thị trường nội địa Việt Nam với 8 mặt hàng nông sản chủ lực và 29 địa phương cấp huyện/thị xã/phường đại diện cho giá bán trực tiếp tại vườn và tại ruộng. Về phạm vi thời gian dự báo: Hệ thống tập trung vào bài toán dự báo ngắn hạn và trung hạn (7 ngày, 10 ngày, 14 ngày và 30 ngày/kỳ tiếp theo sau mốc dữ liệu lịch sử cuối cùng), phục vụ trực tiếp cho quyết định thu hoạch, xuất bán tại vườn và thu mua thương phẩm.",
            "Ngoài phần Mở đầu, Kết luận, Hướng phát triển, Danh mục tài liệu tham khảo và Phụ lục, nội dung chính của khóa luận được tổ chức thành 4 chương theo đúng quy định của Khoa Công nghệ Thông tin - Trường Đại học Đà Lạt: Chương 1 trình bày Tổng quan về đề tài nghiên cứu; Chương 2 trình bày Cơ sở lý thuyết và công nghệ sử dụng; Chương 3 trình bày Phân tích và thiết kế hệ thống dự báo giá nông sản AgroForecast; Chương 4 trình bày Kết quả cài đặt, thực nghiệm 5 mô hình học máy, kiểm thử và kiểm tra bảo mật hệ thống.",
        ],
    ),
]
