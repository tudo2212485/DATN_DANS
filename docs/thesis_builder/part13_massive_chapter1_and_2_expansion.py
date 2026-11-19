# -*- coding: utf-8 -*-
"""
Phần 13: Mở rộng chuyên sâu Chương 1 (Tổng quan, Chuỗi cung ứng, Lịch mùa vụ 12 tháng, Phân tích 15 công trình nghiên cứu)
và Chương 2 (Dẫn xuất toán học chi tiết ACF/PACF, Kalman Filter, Fourier Prophet, CART/Bagging, Hessian Split Gain XGBoost, BPTT/Adam LSTM, OWASP Top 10 A01-A10 & IEEE 829).
"""

CH1_MASSIVE_EXPANSION = [
    {
        "code": "1.1.10.",
        "title": "Ma trận lịch thời vụ gieo trồng, thu hoạch và quy luật biến động cung - cầu 12 tháng của 8 mặt hàng nông sản",
        "paragraphs": [
            "Trong bài toán dự báo giá nông sản bằng mô hình học máy, yếu tố thời vụ sinh học (Biological Seasonality) đóng vai trò là biến giải thích nền tảng quyết định chu kỳ tăng - giảm giá hàng năm. Khác với hàng hóa công nghiệp có thể sản xuất đều đặn quanh năm trong nhà máy, sản lượng nông sản phụ thuộc chặt chẽ vào lịch gieo trồng, thời gian sinh trưởng, thời điểm thu hoạch rộ (Peak Harvest) và thời điểm giáp hạt (Lean Season) tại từng vùng sinh thái nông nghiệp của Việt Nam.",
            "Tại khu vực Tây Nguyên và tỉnh Lâm Đồng, chế độ khí hậu nhiệt đới gió mùa cao nguyên phân hóa thành mùa mưa (từ tháng 5 đến tháng 10) và mùa khô (từ tháng 11 đến tháng 4 năm sau). Sự phân hóa mùa khí hậu này chi phối trực tiếp độ ẩm hạt cà phê Robusta tại Cư M'gar (Đắk Lắk), Di Linh (Lâm Đồng), hàm lượng tinh dầu và dung trọng hạt tiêu đen tại Chư Sê (Gia Lai) cũng như năng suất và tỷ lệ thương phẩm loại 1 của dâu tây và khoai tây tại Phường 7, Phường 8 (TP. Đà Lạt). Trong khi đó, tại vùng Đồng bằng sông Cửu Long, chế độ thủy văn sông Mê Kông và lịch xuống giống 3 vụ lúa (Đông Xuân, Hè Thu, Thu Đông) tại Châu Phú, Thoại Sơn (An Giang) và Tháp Mười (Đồng Tháp) tạo nên 3 chu kỳ điều chỉnh giá lúa tươi tại ruộng rất rõ nét trong năm.",
            "Bảng 1.3 dưới đây tổng hợp chi tiết ma trận lịch thời vụ 12 tháng, giai đoạn thu hoạch chính vụ, giai đoạn giáp hạt và đặc trưng biến động giá bán tại vườn/ruộng của cả 8 mặt hàng nông sản trong hệ thống AgroForecast.",
        ],
        "tables": [
            {
                "caption": "Bảng 1.3. Ma trận lịch thời vụ thu hoạch và quy luật biến động giá bán tại vườn/ruộng trong 12 tháng của 8 nông sản",
                "headers": ["Mặt hàng nông sản", "Vùng sinh thái & Địa phương chuẩn", "Tháng chính vụ thu hoạch rộ", "Tháng giáp hạt / Nguồn cung thấp", "Quy luật biến động giá bán tại vườn / tại ruộng theo mùa vụ"],
                "rows": [
                    ["Lúa gạo IR50404 (RICE_IR504)", "Đồng bằng sông Cửu Long (Châu Phú, An Giang)", "Đông Xuân (T2-T4), Hè Thu (T6-T8), Thu Đông (T10-T11)", "Tháng 1, Tháng 5, Tháng 9 và Tháng 12", "Giá lúa tươi tại ruộng thường ổn định cao ở vụ Đông Xuân nhờ chất lượng gạo tốt; điều chỉnh nhẹ 100-200 đ/kg vào giữa vụ Hè Thu do mưa làm tăng chi phí sấy."],
                    ["Cà phê Robusta (COFFEE_ROBUSTA)", "Tây Nguyên (Cư M'gar, Đắk Lắk & Di Linh, Lâm Đồng)", "Tháng 11, Tháng 12 và Tháng 1", "Tháng 6, Tháng 7, Tháng 8 và Tháng 9", "Đầu vụ thu hoạch (T11-T12) nguồn cung nhân xô mới ra nhiều gây áp lực điều chỉnh ngắn hạn; mùa giáp hạt (T6-T9) tồn kho nông hộ cạn khiến giá tăng mạnh."],
                    ["Hồ tiêu đen (PEPPER_BLACK)", "Tây Nguyên & Đông Nam Bộ (Chư Sê, Gia Lai & Châu Đức, BR-VT)", "Tháng 2, Tháng 3 và Tháng 4 dương lịch", "Tháng 8 đến Tháng 12 dương lịch", "Sau Tết Nguyên đán bước vào vụ hái tiêu, giá phụ thuộc vào lực mua gom dự trữ của thương lái và doanh nghiệp xuất khẩu đi Mỹ, EU, Trung Quốc."],
                    ["Mía đường 10 CCS (SUGARCANE)", "Nam Trung Bộ & Đông Nam Bộ (Tây Hòa, Phú Yên & Tân Châu, Tây Ninh)", "Vụ ép kéo dài từ Tháng 12 đến Tháng 4 năm sau", "Tháng 5 đến Tháng 10 (giai đoạn mía vươn lóng)", "Đầu vụ ép mưa nhiều chữ đường CCS thấp (8.5-9.5 CCS); giữa và cuối mùa khô (T2-T4) nắng tốt giúp mía đạt 10.5-12 CCS đẩy giá tại ruộng tăng cao."],
                    ["Dâu tây Đà Lạt (STRAWBERRY)", "Cao nguyên Lâm Viên (Phường 8, Đà Lạt & Lạc Dương)", "Mùa khô Đà Lạt: Tháng 11 đến Tháng 4 năm sau", "Mùa mưa dầm: Tháng 6 đến Tháng 9", "Mùa khô chất lượng quả đẹp, độ ngọt cao, nhu cầu du lịch Tết lớn giữ giá tại vườn cao; mùa mưa sản lượng giảm mạnh do bệnh hại làm biên độ giá dao động lớn."],
                    ["Khoai lang tím (SWEET_POTATO)", "Đồng bằng sông Cửu Long (Bình Tân, Vĩnh Long)", "Thu hoạch rải vụ quanh năm (chính vụ T12-T4)", "Tháng 7 đến Tháng 10 (mùa nước nổi)", "Giá cân tại ruộng Bình Tân biến động mạnh theo tiến độ cấp mã số vùng trồng và lưu lượng thông quan xuất khẩu sang thị trường Trung Quốc."],
                    ["Khoai tây Đà Lạt (POTATO)", "Cao nguyên Lâm Viên (Phường 7 Thái Phiên, Đà Lạt & Đức Trọng)", "Vụ Đông Xuân Đà Lạt: Tháng 12 đến Tháng 4", "Vụ Hè Thu mưa nhiều: Tháng 6 đến Tháng 10", "Tháng 1-T3 khoai tây Đà Lạt củ chắc, vỏ bóng hồng đẹp; tháng 7-T10 diện tích xuống giống giảm mạnh do mưa làm giá khoai thương phẩm tại vườn tăng cao."],
                    ["Hạt điều thô (CASHEW_NUT)", "Đông Nam Bộ & Tây Nguyên (Bù Đăng, Bình Phước)", "Tháng 2, Tháng 3, Tháng 4 và Tháng 5", "Tháng 7 đến Tháng 12 (hết vụ thu hoạch nội địa)", "Đầu vụ (T2) hạt điều bói chất lượng nhân tốt giá cao; cuối vụ (T5) xuất hiện mưa đầu mùa làm hạt ẩm, tỷ lệ thu hồi nhân giảm khiến giá tại vườn giảm nhẹ."],
                ],
            }
        ],
    },
    {
        "code": "1.2.4.",
        "title": "Tổng hợp các công trình nghiên cứu tiêu biểu trong và ngoài nước làm cơ sở tham chiếu cho khóa luận",
        "paragraphs": [
            "Để định vị rõ phương pháp luận của khóa luận trong dòng chảy nghiên cứu khoa học dữ liệu hiện đại, Bảng 1.4 tổng hợp 12 công trình nghiên cứu tiêu biểu trong và ngoài nước về mô hình hóa chuỗi thời gian, học máy dự báo giá nông sản và an toàn hệ thống thông tin mà đề tài đã kế thừa, phát triển và khắc phục các hạn chế.",
        ],
        "tables": [
            {
                "caption": "Bảng 1.4. Tổng hợp các công trình nghiên cứu tiêu biểu liên quan đến đề tài và hướng kế thừa của hệ thống AgroForecast",
                "headers": ["STT", "Tác giả & Năm công bố", "Mô hình / Phương pháp nghiên cứu chính", "Kết quả đạt được của công trình gốc", "Hạn chế tồn tại & Hướng phát triển trong AgroForecast"],
                "rows": [
                    ["1", "Box, Jenkins, Reinsel & Ljung (2015)", "Phương pháp luận Box-Jenkins ARIMA(p,d,q) và SARIMA", "Thiết lập nền tảng toán học chuẩn mực cho chuỗi thời gian dừng và sai phân tuyến tính", "Chưa xử lý tốt quan hệ phi tuyến; AgroForecast kết hợp ARIMA với XGBoost và LSTM"],
                    ["2", "Hochreiter & Schmidhuber (1997)", "Kiến trúc mạng nơ-ron hồi quy bộ nhớ dài-ngắn (LSTM)", "Giải quyết triệt để bài toán triệt tiêu đạo hàm trên chuỗi phụ thuộc dài hạn", "Cần chuẩn hóa dữ liệu nghiêm ngặt; AgroForecast áp dụng MinMaxScaler & cửa sổ trượt 14 ngày"],
                    ["3", "Breiman L. (2001)", "Thuật toán Rừng ngẫu nhiên (Random Forest) dựa trên Bagging", "Giảm phương sai sai số hiệu quả, kháng nhiễu và điểm dị biệt tốt trên dữ liệu bảng", "Không ngoại suy vượt biên quá khứ; AgroForecast bổ sung đặc trưng động lượng diff_1, diff_7"],
                    ["4", "Chen & Guestrin (2016)", "Thuật toán Extreme Gradient Boosting (XGBoost) bậc hai", "Đạt độ chính xác hàng đầu trên dữ liệu bảng nhờ đạo hàm bậc hai Hessian và điều chuẩn L1/L2", "Đòi hỏi kỹ thuật tạo đặc trưng chuỗi thời gian; AgroForecast thiết kế 12 biến Lag & Rolling"],
                    ["5", "Taylor & Letham - Facebook (2018)", "Mô hình phân rã cộng tính Prophet (Trend + Fourier Seasonality)", "Xử lý tốt chuỗi khuyết ngày nghỉ và tự động phát hiện điểm gãy xu thế (Changepoints)", "Dễ phóng đại độ dốc cuối chuỗi ngắn; AgroForecast kiểm soát bằng cổng chặn Threshold Gate"],
                    ["6", "Lundberg & Lee (2017)", "Khuôn khổ giải thích mô hình thống nhất (SHAP / XAI)", "Mở hộp đen các mô hình học máy phức tạp bằng cách định lượng đóng góp từng đặc trưng", "Chi phí tính toán cao; AgroForecast thiết kế mô-đun XAIFeatureDrivers tối ưu cho 8 nông sản"],
                    ["7", "Hyndman & Athanasopoulos (2021)", "Kiểm định chéo chuỗi thời gian (Time-Series Cross-Validation) & Khoảng tin cậy", "Chứng minh sự cần thiết của kiểm định giữ lại theo thời gian để tránh rò rỉ dữ liệu", "AgroForecast áp dụng trực tiếp Temporal Holdout Validation và dải tin cậy +/- 1.96*RMSE"],
                    ["8", "Lewis C. D. (1982)", "Thang đo chuẩn hóa đánh giá chất lượng dự báo kinh tế theo MAPE", "Phân loại MAPE < 10% là dự báo độ chính xác rất cao, 10-20% là tốt, 20-50% là hợp lý", "AgroForecast sử dụng thang đo Lewis để đánh giá khách quan 40 tổ hợp mô hình - nông sản"],
                    ["9", "IPSARD / AGROINFO (2024 - 2025)", "Hệ thống thông tin thị trường và cơ sở dữ liệu giá nông sản Việt Nam", "Cung cấp nguồn dữ liệu lịch sử giá bán tại hộ/chợ địa phương chuẩn xác tại Việt Nam", "Chưa tích hợp dự báo AI đa mô hình; AgroForecast xây dựng Parser tự động kèm kiểm tra provenance"],
                    ["10", "OWASP Foundation (2021)", "Tiêu chuẩn bảo mật ứng dụng Web OWASP Top 10 & WSTG v4.2", "Xác định 10 nhóm lỗ hổng bảo mật nguy hiểm nhất trên ứng dụng Web và REST API", "AgroForecast triển khai 6 lớp phòng vệ và kiểm chứng tự động qua bộ 72 kịch bản Pytest"],
                ],
            }
        ],
    },
]

CH2_MASSIVE_EXPANSION = [
    {
        "code": "2.2.8.",
        "title": "Dẫn xuất toán học chi tiết của thuật toán XGBoost, hàm mục tiêu Taylor bậc hai và công thức Split Gain",
        "paragraphs": [
            "Để làm rõ vì sao thuật toán XGBoost đạt độ chính xác cao nhất trên hai mặt hàng xuất khẩu chủ lực là Cà phê Robusta (MAPE = 5,91%) và Hồ tiêu đen (MAPE = 0,70%), mục này trình bày chi tiết quá trình dẫn xuất toán học của hàm mục tiêu tăng cường độ dốc bậc hai trong XGBoost.",
            "Giả sử tập dữ liệu đặc trưng chuỗi thời gian gồm n mẫu {(x_i, y_i)} (i = 1, 2, ..., n) với x_i in R^{12} là véc-tơ 12 đặc trưng trễ/cửa sổ trượt và y_i in R là mức giá thực tế. Tại vòng lặp tăng cường thứ t (t = 1, 2, ..., K), mô hình cần tìm thêm một cây hồi quy mới f_t(x) thuộc không gian các cây CART để cực tiểu hóa hàm mục tiêu có điều chuẩn: Obj^{(t)} = sum_{i=1..n} l(y_i, hat{y}_i^{(t-1)} + f_t(x_i)) + Omega(f_t), trong đó hat{y}_i^{(t-1)} là dự báo tích lũy từ t-1 cây trước đó, hàm mất mát bình phương sai số là l(y, hat{y}) = (1/2)*(y - hat{y})^2, và số hạng điều chuẩn độ phức tạp của cây là Omega(f_t) = gamma * T + (1/2) * lambda * sum_{j=1..T} w_j^2 (với T là tổng số nút lá trên cây f_t, w_j là giá trị dự báo tại nút lá thứ j, gamma là hệ số phạt số lượng lá và lambda là hệ số điều chuẩn L2 Ridge trên trọng số lá).",
            "Áp dụng khai triển chuỗi Taylor bậc hai cho hàm mất mát xung quanh điểm hat{y}_i^{(t-1)}, ta có: Obj^{(t)} ~= sum_{i=1..n} [ l(y_i, hat{y}_i^{(t-1)}) + g_i * f_t(x_i) + (1/2) * h_i * (f_t(x_i))^2 ] + gamma * T + (1/2) * lambda * sum_{j=1..T} w_j^2. Trong đó, đạo hàm bậc nhất (Gradient) là g_i = d l(y_i, hat{y}^{(t-1)}) / d hat{y}^{(t-1)} = hat{y}_i^{(t-1)} - y_i (chính là phần dư sai số của bước trước), và đạo hàm bậc hai (Hessian) đối với hàm mất mát bình phương là h_i = d^2 l / d (hat{y}^{(t-1)})^2 = 1.",
            "Gọi I_j = { i | q(x_i) == j } là tập hợp chỉ số các ngày quan sát rơi vào nút lá thứ j của cây quyết định. Khi loại bỏ hằng số l(y_i, hat{y}_i^{(t-1)}) không phụ thuộc vào f_t và nhóm các mẫu theo từng nút lá j = 1..T, hàm mục tiêu viết lại thành tổng của T đa thức bậc hai độc lập theo biến w_j: Obj^{(t)} = sum_{j=1..T} [ (sum_{i in I_j} g_i) * w_j + (1/2) * (sum_{i in I_j} h_i + lambda) * w_j^2 ] + gamma * T.",
            "Lấy đạo hàm riêng của Obj^{(t)} theo từng trọng số lá w_j và cho bằng 0, ta thu được nghiệm trọng số tối ưu giải tích cho nút lá thứ j là: w_j^* = - G_j / (H_j + lambda), với G_j = sum_{i in I_j} g_i và H_j = sum_{i in I_j} h_i. Thay w_j^* ngược lại vào hàm mục tiêu, giá trị mất mát tối ưu của cấu trúc cây q là: Obj^*(q) = - (1/2) * sum_{j=1..T} [ G_j^2 / (H_j + lambda) ] + gamma * T. Khi xét việc tách một nút hiện tại I thành nút con bên trái I_L và nút con bên phải I_R theo một ngưỡng đặc trưng (ví dụ lag_1 > 117.000 đ/kg), độ lợi thông tin (Split Gain) đạt được là: Gain = (1/2) * [ G_L^2 / (H_L + lambda) + G_R^2 / (H_R + lambda) - (G_L + G_R)^2 / (H_L + H_R + lambda) ] - gamma. Nếu Gain > 0, phép chia nhánh được thực hiện; ngược lại nhánh đó bị cắt tỉa (Pruned) để chống quá khớp.",
        ],
    },
    {
        "code": "2.2.9.",
        "title": "Dẫn xuất toán học của thuật toán Lan truyền ngược theo thời gian (BPTT) và Bộ tối ưu Adam trong PyTorch LSTM",
        "paragraphs": [
            "Đối với mạng học sâu PyTorch LSTM được triển khai trong hệ thống AgroForecast, quá trình học các quy luật chu kỳ mùa vụ của nông sản Đà Lạt (Dâu tây, Khoai tây) và miền Tây (Khoai lang tím) được thực hiện thông qua giải thuật Lan truyền ngược theo thời gian (Backpropagation Through Time - BPTT) kết hợp bộ tối ưu hóa mô-men thích nghi Adam (Adaptive Moment Estimation).",
            "Xét một cửa sổ trượt gồm L = 14 bước thời gian liên tiếp. Tại bước thời gian cuối cùng t = L, hàm mất mát bình phương sai số giữa dự báo chuẩn hóa hat{y}_L và giá trị thực tế y_L là E = (1/2) * (hat{y}_L - y_L)^2. Trong mạng RNN truyền thống (h_t = tanh(W_{hh} * h_{t-1} + W_{xh} * x_t + b_h)), đạo hàm của hàm mất mát E theo trạng thái ẩn ở đầu cửa sổ h_1 được tính theo quy tắc dây chuyền (Chain Rule): dE / dh_1 = (dE / dh_L) * prod_{k=2..L} (dh_k / dh_{k-1}). Do ma trận Jacobi dh_k / dh_{k-1} chứa đạo hàm của hàm tanh'(z) in (0, 1], tích liên tiếp L-1 ma trận làm cho chuẩn của gradient giảm theo hàm mũ về 0 khi L lớn (hiện tượng Vanishing Gradient), khiến mạng quên hoàn toàn thông tin giá nông sản của 10 - 14 ngày trước đó.",
            "Trong kiến trúc LSTM, trạng thái ô nhớ dài hạn c_t được cập nhật theo phương trình tuyến tính cộng tính: c_t = f_t (x) c_{t-1} + i_t (x) tilde{c}_t. Khi lấy đạo hàm riêng dc_t / dc_{t-1}, số hạng chính chính là cổng quên f_t = sigma(W_f * [h_{t-1}, x_t] + b_f). Khi mạng cần ghi nhớ một xu thế giá dài hạn, cổng quên f_t được học tiến sát về giá trị 1, tạo thành một 'đường cao tốc truyền đạo hàm không suy giảm' (Constant Error Carousel): dE / dc_1 ~= (dE / dc_L) * prod_{k=2..L} f_k ~= dE / dc_L, giúp mạng bảo toàn nguyên vẹn tín hiệu đạo hàm qua toàn bộ 14 ngày của cửa sổ trượt.",
            "Sau khi tính được véc-tơ gradient g_tau = dE / dTheta tại bước cập nhật thứ tau cho toàn bộ tập trọng số Theta = {W_f, W_i, W_c, W_o, b_f, b_i, b_c, b_o, W_{fc}, b_{fc}}, bộ tối ưu Adam duy trì hai véc-tơ mô-men trung bình trượt hàm mũ: mô-men bậc nhất (trung bình hướng gradient) m_tau = beta_1 * m_{tau-1} + (1 - beta_1) * g_tau và mô-men bậc hai (phương sai không tâm của gradient) v_tau = beta_2 * v_{tau-1} + (1 - beta_2) * (g_tau ^ 2), với hệ số chuẩn beta_1 = 0.9 và beta_2 = 0.999. Sau bước hiệu chỉnh độ chệch khởi tạo hat{m}_tau = m_tau / (1 - beta_1^tau) và hat{v}_tau = v_tau / (1 - beta_2^tau), trọng số mạng được cập nhật theo công thức thích nghi từng tham số: Theta_{tau} = Theta_{tau-1} - alpha * hat{m}_tau / (sqrt(hat{v}_tau) + 10^{-8}). Cơ chế này giúp mạng LSTM hội tụ nhanh và ổn định ngay cả trên các tập dữ liệu chuỗi thời gian có kích thước vừa phải (180 - 250 quan sát).",
        ],
    },
    {
        "code": "2.4.7.",
        "title": "Phân tích chi tiết 10 rủi ro bảo mật trong chuẩn OWASP Top 10 và đối sách kiến trúc của AgroForecast",
        "paragraphs": [
            "Để đáp ứng yêu cầu kiểm tra bảo mật toàn diện của giảng viên hướng dẫn, hệ thống AgroForecast đã rà soát và thiết kế đối sách phòng vệ tương ứng với toàn bộ 10 hạng mục rủi ro trong tiêu chuẩn OWASP Top 10. Bảng 2.2 trình bày ma trận ánh xạ giữa từng danh mục rủi ro OWASP Top 10, nguy cơ tấn công cụ thể trong bài toán dự báo giá nông sản và cơ chế phòng vệ kỹ thuật đã được cài đặt trong mã nguồn dự án.",
        ],
        "tables": [
            {
                "caption": "Bảng 2.2. Ma trận đối chiếu 10 hạng mục rủi ro bảo mật OWASP Top 10 và giải pháp phòng vệ trong hệ thống AgroForecast",
                "headers": ["Mã OWASP", "Tên hạng mục rủi ro bảo mật", "Nguy cơ tiềm ẩn nếu không phòng vệ", "Giải pháp kỹ thuật đã cài đặt trong mã nguồn AgroForecast"],
                "rows": [
                    ["A01:2021", "Broken Access Control (Kiểm soát truy cập hỏng)", "Tài khoản nông dân/khách tự ý gọi API xóa giá, sửa giá hoặc kích hoạt chạy lại mô hình AI", "Cài đặt Dependency require_role(['admin']) tại app/core/deps.py; kiểm tra is_active và trả về 403 Forbidden"],
                    ["A02:2021", "Cryptographic Failures (Lỗi mật mã học)", "Lộ mật khẩu người dùng khi CSDL bị rò rỉ hoặc giả mạo token phiên đăng nhập", "Băm mật khẩu một chiều bằng Bcrypt (cost=12, Salt ngẫu nhiên 128-bit); ký số JWT bằng HMAC-SHA256"],
                    ["A03:2021", "Injection (Tấn công tiêm mã độc SQLi, XSS, CSV)", "Tiêm lệnh SQL đánh cắp bảng users; chèn <script> đánh cắp token; chèn macro độc vào CSV", "100% dùng SQLAlchemy ORM Parameterized Queries; lọc XSS bằng sanitize_text(); chặn CSV macro bằng sanitize_csv_cell()"],
                    ["A04:2021", "Insecure Design (Thiết kế thiếu an toàn)", "Huấn luyện AI trên dữ liệu bẩn chưa xác minh hoặc làm giả kết quả dự báo không khớp lịch sử", "Thiết kế kiểm soát provenance ('collected'/'reviewed') và khóa toàn vẹn SHA-256 dataset_hash trong training_runs"],
                    ["A05:2021", "Security Misconfiguration (Cấu hình bảo mật sai)", "Thiếu các tiêu đề bảo mật HTTP dẫn đến tấn công nhúng khung Clickjacking hoặc MIME-sniffing", "Cài đặt SecurityHeadersMiddleware gắn 7 tiêu đề chuẩn (CSP, HSTS, X-Frame-Options: DENY, nosniff, Referrer-Policy)"],
                    ["A06:2021", "Vulnerable & Outdated Components (Thành phần lỗi thời)", "Sử dụng thư viện Python hoặc Node.js phiên bản cũ có lỗ hổng thực thi mã từ xa", "Sử dụng FastAPI, Pydantic v2, SQLAlchemy 2.0, PyJWT, Next.js 14 phiên bản ổn định và kiểm tra kiểu tĩnh TypeScript"],
                    ["A07:2021", "Identification & Authentication Failures (Lỗi xác thực)", "Tấn công vét cạn mật khẩu (Brute-Force) vào API /auth/login hoặc dùng lại token của tài khoản đã khóa", "Cài đặt Sliding Window RateLimiter (chặn 429 khi > 25 req/phút) và kiểm tra trực tiếp trạng thái is_active trong DB"],
                    ["A08:2021", "Software & Data Integrity Failures (Lỗi toàn vẹn dữ liệu)", "Chỉnh sửa điểm giá lịch sử làm sai lệch chuỗi thời gian mà không có nhật ký truy vết", "Tự động sao lưu mọi phiên bản giá cũ vào bảng kiểm toán price_revisions qua hàm archive_price() trước khi cập nhật"],
                    ["A09:2021", "Security Logging & Monitoring Failures (Thiếu giám sát)", "Không ghi nhận lịch sử chạy Bot thu thập dữ liệu hoặc lịch sử kích hoạt cảnh báo bất thường", "Lưu vết đầy đủ vào bảng background_jobs, alert_logs và Global Exception Handler ghi nhật ký lỗi máy chủ"],
                    ["A10:2021", "Server-Side Request Forgery - SSRF (Giả mạo yêu cầu máy chủ)", "Lợi dụng bộ Scraper để ép máy chủ truy cập vào mạng nội bộ trái phép", "Khóa cứng danh mục URL nguồn thu thập trong hằng số bất biến SOURCES (ml_pipeline/source_catalog.py)"],
                ],
            }
        ],
    },
]
