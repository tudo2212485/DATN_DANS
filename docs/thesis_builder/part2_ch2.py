# -*- coding: utf-8 -*-
"""
Chương 2: CƠ SỞ LÝ THUYẾT VÀ CÔNG NGHỆ SỬ DỤNG
"""

CHUONG_2_DATA = {
    "title": "Chương 2: CƠ SỞ LÝ THUYẾT VÀ CÔNG NGHỆ SỬ DỤNG",
    "sections": [
        {
            "code": "2.1.",
            "title": "Lý thuyết về chuỗi thời gian (Time Series) và tiền xử lý dữ liệu nông sản",
            "subsections": [
                {
                    "code": "2.1.1.",
                    "title": "Các thành phần của chuỗi thời gian và tính chất giá nông sản",
                    "paragraphs": [
                        "Một chuỗi thời gian (Time Series) là một dãy các quan sát của biến ngẫu nhiên Y_t được ghi nhận theo thứ tự thời gian t = 1, 2, ..., T với khoảng cách thời gian đều đặn (theo ngày giao dịch hoặc theo kỳ báo cáo). Trong bài toán dự báo giá nông sản của hệ thống AgroForecast, mỗi chuỗi giá Y_t = {p_1, p_2, ..., p_T} biểu diễn mức giá bán tại vườn/ruộng (đơn vị VNĐ/kg hoặc VNĐ/tấn) của một mặt hàng tại mốc thời gian t.",
                        "Về mặt cấu trúc toán học, một chuỗi thời gian giá nông sản Y_t được hợp thành từ bốn thành phần cơ bản theo mô hình cộng tính (Additive Decomposition): Y_t = T_t + S_t + C_t + e_t, hoặc mô hình nhân tính (Multiplicative Decomposition): Y_t = T_t * S_t * C_t * e_t. Trong đó: (1) Thành phần xu thế dài hạn (Trend - T_t) phản ánh sự dịch chuyển chung của mặt bằng giá theo lạm phát, chi phí phân bón, nhân công và nhu cầu xuất khẩu; (2) Thành phần mùa vụ (Seasonality - S_t) phản ánh quy luật lặp lại theo chu kỳ sinh trưởng và thu hoạch nông nghiệp hàng năm (ví dụ giá cà phê Tây Nguyên thường chịu áp lực điều chỉnh nhẹ khi bước vào chính vụ thu hoạch rộ tháng 11 - tháng 12, trong khi giá tăng cao vào giai đoạn giáp hạt tháng 7 - tháng 9); (3) Thành phần chu kỳ kinh tế (Cycle - C_t) kéo dài nhiều năm theo chu kỳ tái canh cây trồng hoặc hiện tượng khí hậu El Nino / La Nina; và (4) Thành phần nhiễu ngẫu nhiên (Irregular/Residual - e_t) biểu diễn các biến động bất thường ngắn hạn.",
                    ],
                },
                {
                    "code": "2.1.2.",
                    "title": "Kiểm định tính dừng Augmented Dickey-Fuller (ADF) và kỹ thuật sai phân",
                    "paragraphs": [
                        "Một chuỗi thời gian Y_t được gọi là dừng yếu (Weakly Stationary) nếu kỳ vọng toán học E(Y_t) = mu là hằng số không phụ thuộc vào thời gian t, phương sai Var(Y_t) = sigma^2 hữu hạn không đổi theo thời gian, và hiệp phương sai tự tương quan Cov(Y_t, Y_{t-k}) = gamma_k chỉ phụ thuộc vào độ trễ k chứ không phụ thuộc vào thời điểm t. Hầu hết các chuỗi giá nông sản thực tế đều là chuỗi không dừng (Non-stationary) do có xu thế tăng/giảm dài hạn.",
                        "Để kiểm tra một chuỗi giá có dừng hay không trước khi đưa vào mô hình ARIMA, hệ thống AgroForecast (tại mô-đun ml_pipeline/data_loader.py) sử dụng kiểm định nghiệm đơn vị Augmented Dickey-Fuller (ADF) thông qua phương trình hồi quy: Delta Y_t = alpha + beta*t + gamma*Y_{t-1} + sum_{i=1..p} (delta_i * Delta Y_{t-i}) + epsilon_t. Giả thuyết không H_0: gamma = 0 (chuỗi có nghiệm đơn vị, tức không dừng) được đối chiếu với giả thuyết đối H_1: gamma < 0 (chuỗi dừng). Nếu giá trị p-value > 0.05, chuỗi chưa dừng và cần thực hiện phép lấy sai phân bậc một (First-order Differencing): Delta Y_t = Y_t - Y_{t-1} hoặc sai phân bậc d: Delta^d Y_t = (1 - B)^d Y_t (với B là toán tử trễ B*Y_t = Y_{t-1}) cho đến khi chuỗi đạt trạng thái dừng.",
                    ],
                },
                {
                    "code": "2.1.3.",
                    "title": "Thuật toán phát hiện và chặn giá trị ngoại lai bằng khoảng tứ phân vị (IQR Outlier Capping)",
                    "paragraphs": [
                        "Trong quá trình thu thập dữ liệu giá nông sản tự động từ các trang tin điện tử hoặc nhập liệu CSV, đôi khi xuất hiện các điểm dữ liệu dị biệt (Outliers) do lỗi đánh máy của nguồn công bố hoặc biến động cục bộ cực đoan. Nếu giữ nguyên các điểm ngoại lai này, hàm mất mát bình phương sai số (MSE) của các mô hình học máy sẽ bị kéo lệch nghiêm trọng; ngược lại, nếu xóa bỏ dòng dữ liệu đó sẽ làm đứt gãy tính liên tục của chuỗi thời gian.",
                        "Để giải quyết triệt để vấn đề này, hàm handle_outliers_iqr() trong ml_pipeline/data_loader.py áp dụng phương pháp chặn ngưỡng tứ phân vị (Winsorizing / IQR Capping). Gọi Q_1 (phân vị thứ 25) và Q_3 (phân vị thứ 75) của chuỗi giá hoặc chuỗi sai phân giá, khoảng tứ phân vị được xác định bởi công thức: IQR = Q_3 - Q_1. Ngưỡng dưới (Lower Bound) và ngưỡng trên (Upper Bound) được thiết lập là: L_bound = Q_1 - 1.5 * IQR và U_bound = Q_3 + 1.5 * IQR. Mọi quan sát p_t vượt ra ngoài khoảng [L_bound, U_bound] đều được ép (clip) về đúng biên gần nhất: p_t_clean = min(max(p_t, L_bound), U_bound). Phương pháp này vừa bảo toàn đầy đủ số lượng ngày quan sát vừa loại bỏ hoàn toàn tác động gây nhiễu của các điểm dị biệt.",
                    ],
                },
                {
                    "code": "2.1.4.",
                    "title": "Kỹ thuật trích xuất đặc trưng chuỗi thời gian (Lag Features & Rolling Statistics)",
                    "paragraphs": [
                        "Đối với các thuật toán học máy dạng bảng như Random Forest và XGBoost, chuỗi thời gian một chiều {p_1, p_2, ..., p_T} cần được biến đổi thành ma trận đặc trưng đa chiều X in R^{N x M} và nhãn mục tiêu y in R^N. Trong hệ thống AgroForecast (mô-đun ml_pipeline/feature_engineering.py và app/services/training_service.py), tại mỗi bước thời gian t, véc-tơ đặc trưng x_t được kiến tạo từ bốn nhóm biến số sau:",
                        "Nhóm 1 - Các biến trễ tự hồi quy (Autoregressive Lag Features): Bao gồm giá tại các ngày liền trước p_{t-1}, p_{t-2}, p_{t-3}, p_{t-7}, p_{t-14}, phản ánh trực tiếp quán tính giá ngắn hạn và chu kỳ tuần.",
                        "Nhóm 2 - Thống kê cửa sổ trượt (Rolling Window Statistics): Bao gồm trung bình trượt 7 ngày (rolling_mean_7d = (1/7)*sum_{k=1..7} p_{t-k}), trung bình trượt 14 ngày (rolling_mean_14d), và độ lệch chuẩn trượt 7 ngày (rolling_std_7d = sqrt((1/7)*sum_{k=1..7} (p_{t-k} - rolling_mean_7d)^2)) dùng để đo lường mức độ biến động (Volatility) của thị trường ngay trước thời điểm dự báo.",
                        "Nhóm 3 - Động lượng giá và tốc độ thay đổi (Momentum & Differences): Bao gồm biến chênh lệch tuyệt đối diff_1 = p_{t-1} - p_{t-2} và chênh lệch tuần diff_7 = p_{t-1} - p_{t-7}, giúp mô hình nhận diện nhanh sự đảo chiều từ xu hướng tăng sang giảm hoặc ngược lại.",
                        "Nhóm 4 - Đặc trưng lịch và chu kỳ mùa vụ (Calendar & Cyclical Features): Bao gồm thứ trong tuần (day_of_week), ngày trong tháng (day_of_month), tháng trong năm (month) nhằm phản ánh chính xác tính thời vụ thu hoạch của nông sản Việt Nam.",
                    ],
                },
            ],
        },
        {
            "code": "2.2.",
            "title": "Cơ sở toán học và cơ chế hoạt động của 5 mô hình học máy dự báo giá",
            "subsections": [
                {
                    "code": "2.2.1.",
                    "title": "Mô hình Tự hồi quy tích hợp trung bình trượt (ARIMA)",
                    "paragraphs": [
                        "Mô hình ARIMA(p, d, q) là sự kết hợp của ba thành phần: Tự hồi quy bậc p (AutoRegressive - AR(p)), Tích hợp sai phân bậc d (Integrated - I(d)) và Trung bình trượt bậc q (Moving Average - MA(q)). Gọi y'_t = Delta^d Y_t = (1 - B)^d Y_t là chuỗi đã lấy sai phân bậc d để đạt tính dừng, phương trình toán học tổng quát của ARIMA(p, d, q) có dạng:",
                        "y'_t = c + phi_1 * y'_{t-1} + phi_2 * y'_{t-2} + ... + phi_p * y'_{t-p} + theta_1 * epsilon_{t-1} + theta_2 * epsilon_{t-2} + ... + theta_q * epsilon_{t-q} + epsilon_t",
                        "Trong đó: c là hằng số cơ sở; phi_1, ..., phi_p là các hệ số tự hồi quy biểu diễn mức độ ảnh hưởng của p giá trị quá khứ gần nhất; theta_1, ..., theta_q là các hệ số trung bình trượt biểu diễn mức độ điều chỉnh theo các cú sốc sai số quá khứ; và epsilon_t ~ WN(0, sigma^2) là nhiễu trắng có kỳ vọng bằng 0. Các tham số (phi, theta, c) được ước lượng bằng phương pháp Hợp lý cực đại (Maximum Likelihood Estimation - MLE) thông qua bộ lọc Kalman trạng thái - không gian (State-Space Kalman Filter) của thư viện statsmodels.",
                    ],
                },
                {
                    "code": "2.2.2.",
                    "title": "Mô hình phân rã chuỗi thời gian cộng tính (Facebook Prophet)",
                    "paragraphs": [
                        "Mô hình Prophet tiếp cận bài toán dự báo chuỗi thời gian như một bài toán khớp đường cong hồi quy cộng tính tổng quát (Generalized Additive Model - GAM) theo phương trình: y(t) = g(t) + s(t) + h(t) + epsilon_t.",
                        "Thành phần xu thế g(t) được mô hình hóa bằng hàm tuyến tính từng khúc có các điểm gãy thay đổi xu hướng (Changepoints): g(t) = (k + a(t)^T * delta) * t + (m + a(t)^T * gamma), trong đó k là tốc độ tăng trưởng cơ bản, delta là véc-tơ điều chỉnh độ dốc tại S điểm gãy s_j (j = 1..S), và a_j(t) = 1 nếu t >= s_j (ngược lại bằng 0). Để tránh hiện tượng quá khớp (Overfitting) khi dự báo xa, Prophet đặt phân phối tiên nghiệm Laplace: delta_j ~ Laplace(0, tau) (tương đương điều chuẩn L1 Lasso) giúp chỉ giữ lại những điểm đảo chiều xu thế thực sự có ý nghĩa.",
                        "Thành phần mùa vụ s(t) được biểu diễn mượt mà bằng chuỗi lượng giác Fourier bậc N: s(t) = sum_{n=1..N} [a_n * cos(2*pi*n*t / P) + b_n * sin(2*pi*n*t / P)], với P = 365.25 cho chu kỳ mùa vụ nông nghiệp hàng năm và P = 7 cho chu kỳ giao dịch hàng tuần. Quá trình tối ưu tham số được thực hiện bằng thuật toán L-BFGS tốc độ cao.",
                    ],
                },
                {
                    "code": "2.2.3.",
                    "title": "Mô hình Rừng ngẫu nhiên (Random Forest Regressor)",
                    "paragraphs": [
                        "Random Forest Regressor là thuật toán học máy tổ hợp (Ensemble Learning) dựa trên kỹ thuật Bagging (Bootstrap Aggregating) kết hợp lựa chọn đặc trưng ngẫu nhiên trên tập hợp B cây quyết định hồi quy độc lập {T_1(x), T_2(x), ..., T_B(x)}. Từ tập dữ liệu huấn luyện gốc D gồm N mẫu đặc trưng chuỗi thời gian, thuật toán tạo ra B tập mẫu con D_b bằng phương pháp lấy mẫu có hoàn lại (Bootstrap) và xây dựng mỗi cây quyết định T_b bằng cách tại mỗi nút phân nhánh chỉ xét một tập con ngẫu nhiên các đặc trưng để tìm ngưỡng chia giảm thiểu phương sai nội nhóm (MSE Impurity) nhiều nhất.",
                        "Giá trị dự báo cuối cùng hat{y} của Random Forest tại bước thời gian tương lai là trung bình cộng dự báo của tất cả B cây thành viên: hat{y}(x) = (1 / B) * sum_{b=1..B} T_b(x). Nhờ cơ chế lấy trung bình trên các cây có tương quan thấp, phương sai của sai số dự báo giảm đi theo hệ số 1/B mà không làm tăng độ chệch (Bias), giúp mô hình hoạt động rất ổn định trước các biến động nhiễu của thị trường nông sản.",
                    ],
                },
                {
                    "code": "2.2.4.",
                    "title": "Mô hình Tăng cường độ dốc cực đại (Extreme Gradient Boosting - XGBoost)",
                    "paragraphs": [
                        "Khác với Random Forest xây dựng các cây độc lập song song, XGBoost xây dựng chuỗi K cây hồi quy nối tiếp nhau (Additive Boosting), trong đó cây thứ k được huấn luyện để sửa trực tiếp sai số dư (Residuals) của k-1 cây trước đó: hat{y}_i^{(k)} = hat{y}_i^{(k-1)} + eta * f_k(x_i), với eta là tốc độ học (Learning Rate).",
                        "Hàm mục tiêu có điều chuẩn của XGBoost tại bước lặp thứ k được xác định bởi: L^{(k)} = sum_{i=1..n} l(y_i, hat{y}_i^{(k-1)} + f_k(x_i)) + Omega(f_k), trong đó hàm phạt độ phức tạp của cây là Omega(f) = gamma * T + (1/2) * lambda * sum_{j=1..T} w_j^2 (T là số nút lá, w_j là trọng số nút lá thứ j). Bằng cách khai triển chuỗi Taylor bậc hai sử dụng cả đạo hàm bậc nhất g_i (Gradient) và đạo hàm bậc hai h_i (Hessian) của hàm mất mát, trọng số tối ưu của nút lá j được tính tường minh theo công thức: w_j^* = - (sum_{i in I_j} g_i) / (sum_{i in I_j} h_i + lambda). Nhờ điều chuẩn L1/L2 chặt chẽ và tối ưu hóa bậc hai, XGBoost đạt độ chính xác rất cao trên các chuỗi giá có biên độ biến động lớn như Cà phê Robusta và Hồ tiêu đen.",
                    ],
                },
                {
                    "code": "2.2.5.",
                    "title": "Mạng Nơ-ron Hồi quy Bộ nhớ dài-ngắn (PyTorch LSTM)",
                    "paragraphs": [
                        "Mạng LSTM (Long Short-Term Memory) được thiết kế chuyên biệt để học các phụ thuộc chuỗi ngắn hạn và dài hạn thông qua trạng thái ô nhớ (Cell State - c_t) và ba cổng điều khiển phi tuyến tại mỗi bước thời gian t với đầu vào x_t và trạng thái ẩn trước đó h_{t-1}:",
                        "1. Cổng quên (Forget Gate): f_t = sigma(W_f * [h_{t-1}, x_t] + b_f), quyết định tỷ lệ thông tin quá khứ trong c_{t-1} cần giữ lại hay loại bỏ (với sigma là hàm Sigmoid có miền giá trị [0, 1]).",
                        "2. Cổng đầu vào (Input Gate) và Trạng thái ứng viên: i_t = sigma(W_i * [h_{t-1}, x_t] + b_i) và tilde{c}_t = tanh(W_c * [h_{t-1}, x_t] + b_c), quyết định lượng thông tin biến động giá mới tại thời điểm t được nạp vào bộ nhớ.",
                        "3. Cập nhật trạng thái ô nhớ dài hạn: c_t = f_t (x) c_{t-1} + i_t (x) tilde{c}_t (với (x) là phép nhân từng phần tử Hadamard).",
                        "4. Cổng đầu ra (Output Gate) và Trạng thái ẩn mới: o_t = sigma(W_o * [h_{t-1}, x_t] + b_o) và h_t = o_t (x) tanh(c_t).",
                        "Trạng thái ẩn ở bước cuối cùng của cửa sổ trượt độ dài L (h_L) được đưa qua tầng kết nối đầy đủ (Fully Connected Linear Layer): hat{y}_{t+1} = W_{fc} * h_L + b_{fc} để sinh ra giá trị dự báo đã chuẩn hóa Min-Max, sau đó biến đổi ngược (Inverse Transform) về đơn vị tiền tệ VNĐ thực tế.",
                    ],
                },
            ],
        },
        {
            "code": "2.3.",
            "title": "Các độ đo đánh giá chất lượng mô hình và ước lượng khoảng tin cậy",
            "subsections": [
                {
                    "code": "2.3.1.",
                    "title": "Bốn chỉ số đánh giá sai số chuẩn: MAE, RMSE, MAPE và hệ số xác định R2",
                    "paragraphs": [
                        "Để đánh giá khách quan và toàn diện chất lượng dự báo của 5 mô hình học máy trên tập dữ liệu kiểm thử gồm n quan sát {y_1, y_2, ..., y_n} và chuỗi giá dự báo tương ứng {hat{y}_1, hat{y}_2, ..., hat{y}_n}, hệ thống AgroForecast tính toán đồng thời 4 độ đo chuẩn mực sau:",
                        "1. Sai số tuyệt đối trung bình (Mean Absolute Error - MAE): MAE = (1 / n) * sum_{i=1..n} |y_i - hat{y}_i|. Chỉ số MAE có cùng đơn vị với giá nông sản (VNĐ/kg hoặc VNĐ/tấn), cho biết trung bình mỗi ngày mô hình dự báo lệch bao nhiêu đồng so với giá thực tế tại vườn.",
                        "2. Sai số bình phương trung bình căn bậc hai (Root Mean Square Error - RMSE): RMSE = sqrt( (1 / n) * sum_{i=1..n} (y_i - hat{y}_i)^2 ). Do bình phương sai số trước khi lấy trung bình, RMSE phạt nặng các sai số lớn đột biến, được dùng làm tiêu chuẩn chính để xếp hạng mô hình tối ưu nhất và tính toán bề rộng dải tin cậy.",
                        "3. Sai số phần trăm tuyệt đối trung bình (Mean Absolute Percentage Error - MAPE): MAPE = (100% / n) * sum_{i=1..n} |(y_i - hat{y}_i) / y_i|. Do không phụ thuộc vào đơn vị tiền tệ, MAPE cho phép so sánh trực tiếp độ chính xác dự báo giữa mặt hàng giá vài nghìn đồng (như Lúa 6.850 đ/kg) với mặt hàng giá trên trăm nghìn đồng (như Hồ tiêu 129.100 đ/kg). Theo chuẩn phân loại của Lewis (1982): MAPE < 10% là dự báo có độ chính xác rất cao (Highly Accurate); 10% <= MAPE < 20% là dự báo tốt (Good); 20% <= MAPE < 50% là dự báo hợp lý (Reasonable).",
                        "4. Hệ số xác định (Coefficient of Determination - R2): R2 = 1 - [ sum_{i=1..n} (y_i - hat{y}_i)^2 / sum_{i=1..n} (y_i - bar{y})^2 ]. Nhờ áp dụng kiểm định Walk-Forward cuộn 7 ngày trên cửa sổ 66–90 phiên cuối cùng thay vì cửa sổ ngắn hẹp, toàn bộ 40/40 mô hình trên 8 mặt hàng của AgroForecast đều đạt hệ số R2 dương thực nghiệm (0,2536 đến 0,8972), kết hợp RMSE và MAPE để đánh giá toàn diện năng lực dự báo.",
                    ],
                },
                {
                    "code": "2.3.2.",
                    "title": "Phương pháp kiểm định Walk-Forward Holdout Validation và Cổng chặn sai số (Threshold Gate)",
                    "paragraphs": [
                        "Nhằm ngăn chặn tuyệt đối hiện tượng rò rỉ dữ liệu tương lai (Data Leakage), mô-đun huấn luyện của hệ thống (app/services/training_service.py) tách chuỗi lịch sử có độ dài N ngày thành hai phần nghiêm ngặt theo thứ tự thời gian: Tập huấn luyện (Training Set) gồm N - H ngày đầu tiên (từ t = 1 đến t = N - H) và Tập kiểm thử giữ lại (Holdout Test Set) gồm H = min(14, max(5, floor(N / 6))) ngày cuối cùng. Các mô hình chỉ được học trên Tập huấn luyện, sau đó dự báo đệ quy H bước tới để đo lường MAE, RMSE, MAPE, R2 và đối sánh trực tiếp với mô hình cơ sở Naive Persistence (dự báo giá ngày mai bằng giá hôm nay).",
                        "Bên cạnh đó, lớp ModelTrainer (trong ml_pipeline/model_trainer.py) cài đặt cơ chế Cổng chặn sai số (Threshold Gate): một mô hình sau khi huấn luyện chỉ được chấp nhận xuất bản (passed_threshold = True) nếu tỷ lệ RMSE trên mức giá trung bình thỏa mãn điều kiện: (RMSE / mean_price) <= max_rmse_threshold_ratio. Sau khi vượt qua bước kiểm định, mô hình mới được huấn luyện lại trên toàn bộ N quan sát mới nhất để sinh chuỗi dự báo 30 ngày tương lai phục vụ người dùng.",
                    ],
                },
                {
                    "code": "2.3.3.",
                    "title": "Mô hình hóa khoảng tin cậy 95% (CI) và hiệu chỉnh giá địa phương (Spatio-Temporal Basis Spread)",
                    "paragraphs": [
                        "Một điểm dự báo đơn lẻ (Point Forecast) không phản ánh hết rủi ro biến động thị trường. Do đó, tại bước dự báo tương lai h (h = 1, 2, ..., 30), hệ thống AgroForecast ước lượng dải khoảng tin cậy 95% mở rộng dần theo căn bậc hai của kỳ hạn dự báo hoặc theo độ lệch chuẩn sai số kiểm định RMSE: Margin_h = 1.96 * RMSE, từ đó xác định cận dưới (Lower Confidence Bound): LowerCI_{t+h} = max(0, hat{y}_{t+h} - 1.96 * RMSE) và cận trên (Upper Confidence Bound): UpperCI_{t+h} = hat{y}_{t+h} + 1.96 * RMSE.",
                        "Khi người dùng chọn một địa phương bán tại vườn/ruộng cụ thể r có độ lệch giá cơ sở Delta_r (Basis Spread), mô hình không gian - thời gian tại app/services/forecast_service.py thực hiện phép biến đổi đồng nhất trên cả chuỗi lịch sử, chuỗi dự báo trung tâm và hai biên của dải tin cậy: hat{y}_{t+h}^{(r)} = max(0, hat{y}_{t+h}^{(0)} + Delta_r), LowerCI_{t+h}^{(r)} = max(0, LowerCI_{t+h}^{(0)} + Delta_r), và UpperCI_{t+h}^{(r)} = max(0, UpperCI_{t+h}^{(0)} + Delta_r). Phép biến đổi này bảo toàn tính chất bất biến của bất đẳng thức: LowerCI_{t+h}^{(r)} <= hat{y}_{t+h}^{(r)} <= UpperCI_{t+h}^{(r)} tại mọi địa phương.",
                    ],
                },
            ],
        },
        {
            "code": "2.4.",
            "title": "Cơ sở công nghệ phát triển hệ thống và tiêu chuẩn bảo mật OWASP Top 10",
            "subsections": [
                {
                    "code": "2.4.1.",
                    "title": "Kiến trúc Backend RESTful API với FastAPI, SQLAlchemy ORM và PostgreSQL",
                    "paragraphs": [
                        "Hệ thống Backend được phát triển bằng ngôn ngữ Python 3.11 trên nền tảng framework FastAPI hiệu năng cao. FastAPI sử dụng chuẩn ASGI (Asynchronous Server Gateway Interface) thông qua máy chủ Uvicorn kết hợp thư viện Pydantic v2 viết bằng Rust để kiểm tra kiểu dữ liệu (Data Validation & Serialization) tự động cho mọi gói tin JSON đầu vào và đầu ra.",
                        "Tầng lưu trữ dữ liệu sử dụng hệ quản trị cơ sở dữ liệu quan hệ PostgreSQL kết hợp bộ ánh xạ quan hệ hướng đối tượng SQLAlchemy ORM 2.0. Việc truy vấn dữ liệu thông qua biểu thức đối tượng của SQLAlchemy ORM giúp hệ thống tự động biên dịch thành các câu lệnh truy vấn tham số hóa (Parameterized Queries), vừa tối ưu hóa hiệu năng qua bộ nhớ đệm kết nối (Connection Pooling) vừa triệt tiêu nguy cơ tấn công tiêm mã lệnh SQL (SQL Injection).",
                    ],
                },
                {
                    "code": "2.4.2.",
                    "title": "Kiến trúc Frontend hiện đại với Next.js 14, TypeScript và Recharts",
                    "paragraphs": [
                        "Phân hệ giao diện người dùng (Frontend) được xây dựng trên nền tảng Next.js 14 (App Router) kết hợp React 18 và ngôn ngữ định kiểu tĩnh TypeScript. Việc sử dụng TypeScript đảm bảo mọi cấu trúc dữ liệu nhận về từ REST API (như điểm dự báo ForecastPoint, chỉ số sai số ModelMetrics, thông tin vùng RegionInfo) đều được kiểm tra tính tương thích kiểu ngay từ lúc biên dịch (Compile-time Type Safety).",
                        "Hệ thống biểu đồ phân tích chuỗi thời gian được xây dựng bằng thư viện đồ họa véc-tơ SVG Recharts (ComposedChart kết hợp Line và Area) với thuật toán tự động tính toán miền giá trị trục tung động (Dynamic Y-Axis Domain Scaling) và cầu nối liền mạch (Bridge Point Connection) giữa điểm lịch sử cuối cùng với đường dự báo đứt nét và vùng bóng dải tin cậy 95%.",
                    ],
                },
                {
                    "code": "2.4.3.",
                    "title": "Cơ sở lý thuyết về Kiểm thử phần mềm và Bảo mật ứng dụng Web theo OWASP Top 10",
                    "paragraphs": [
                        "Về kiểm thử phần mềm, dự án áp dụng mô hình Kim tự tháp Kiểm thử (Testing Pyramid) kết hợp phương pháp kiểm thử hộp trắng (White-box), hộp xám (Grey-box) và hộp đen (Black-box). Mọi kịch bản kiểm thử tự động được vận hành độc lập trên cơ sở dữ liệu ảo trong bộ nhớ RAM (SQLite In-Memory Sandbox) thông qua cơ chế Dependency Override của FastAPI.",
                        "Về an toàn bảo mật thông tin, hệ thống tuân thủ danh mục 10 rủi ro bảo mật ứng dụng Web nghiêm trọng nhất của tổ chức OWASP (OWASP Top 10), bao gồm: Kiểm soát truy cập hỏng (A01 - Broken Access Control) được giải quyết bằng phân quyền RBAC nghiêm ngặt; Lỗi mật mã học (A02 - Cryptographic Failures) được giải quyết bằng thuật toán băm mật khẩu một chiều Bcrypt kèm Salt ngẫu nhiên và chữ ký số JWT HS256; Lỗi tiêm mã độc (A03 - Injection) được phòng vệ bằng SQLAlchemy ORM, hàm làm sạch HTML/XSS sanitize_text() và hàm chống tiêm công thức bảng tính sanitize_csv_cell(); Thiết kế thiếu an toàn & Lỗi xác thực (A04 & A07) được bảo vệ bằng thuật toán giới hạn tần suất truy cập cửa sổ trượt (Sliding Window Rate Limiter); và Cấu hình bảo mật sai (A05 - Security Misconfiguration) được gia cố bằng lớp trung gian SecurityHeadersMiddleware gắn 7 tiêu đề HTTP bảo mật chuẩn quốc tế.",
                    ],
                },
            ],
        },
    ],
}
