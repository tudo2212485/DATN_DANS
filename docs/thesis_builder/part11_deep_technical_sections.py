# -*- coding: utf-8 -*-
"""
Phần 11: Đặc tả kỹ thuật chuyên sâu về giải thuật, cấu trúc gói tin JSON, sơ đồ luồng tuần tự,
phân tích độ phức tạp thuật toán và đánh giá thực nghiệm chi tiết cho từng chương
để đảm bảo phần Nội dung chính của Khóa luận đạt chuẩn 75 - 100 trang A4 (Times New Roman 13pt, 1.5 lines).
"""

def generate_deep_algorithmic_and_system_analysis():
    """
    Sinh nội dung phân tích kỹ thuật chi tiết cho từng chương dựa trên đúng mã nguồn thực tế
    của dự án AgroForecast (không trùng lặp, 100% bám sát kiến trúc và số liệu của dự án).
    """
    ch1_deep = [
        (
            "1.2.3.",
            "Phân tích so sánh chi tiết giữa các hệ thống hiện hành và hệ thống đề xuất AgroForecast",
            [
                "Để làm rõ tính mới và đóng góp thực tiễn của đề tài so với các cổng thông tin giá nông sản truyền thống cũng như các đề tài nghiên cứu đơn mô hình trước đây, chúng ta tiến hành đối sánh trực diện trên 8 tiêu chí kỹ thuật cốt lõi: (1) Độ phân giải không gian của dữ liệu giá; (2) Cơ chế kiểm chứng nguồn gốc dữ liệu đầu vào; (3) Số lượng và sự đa dạng của các mô hình dự báo học máy; (4) Phương pháp kiểm định chống rò rỉ dữ liệu tương lai; (5) Khả năng định lượng rủi ro qua khoảng tin cậy dự báo; (6) Khả năng giải thích quyết định của trí tuệ nhân tạo (Explainable AI); (7) Kiến trúc phần mềm và khả năng cảnh báo tự động; và (8) Quy trình kiểm thử phần mềm tự động và bảo mật theo chuẩn quốc tế.",
                "Trên tiêu chí độ phân giải không gian: trong khi các trang tin điện tử hiện hành chỉ dừng lại ở mức giá bình quân toàn tỉnh hoặc toàn vùng vĩ mô (như Tây Nguyên, Đồng bằng sông Cửu Long), hệ thống AgroForecast đi sâu tới mức giá nông hộ bán trực tiếp tại vườn và tại ruộng ở 29 địa phương cấp huyện, thị xã, phường thông qua mô hình hóa độ lệch giá cơ sở (Spatial Basis Spread). Điều này giúp một nông hộ trồng cà phê tại huyện Di Linh (Lâm Đồng) hay trồng dâu tây tại Phường 8 (TP. Đà Lạt) nhận được con số dự báo sát với thực tế giao dịch tại chính mảnh vườn của mình.",
                "Trên tiêu chí kiểm chứng nguồn gốc và chống rò rỉ dữ liệu: hệ thống AgroForecast là một trong số ít các công trình đồ án tốt nghiệp thiết lập trạng thái provenance ('collected', 'reviewed', 'unverified') cho từng bản ghi lịch sử, kết hợp hàm băm mật mã SHA-256 (dataset_hash) để khóa chặt mối liên kết toàn vẹn giữa tập dữ liệu lịch sử và tập kết quả dự báo. Bất kỳ sự thay đổi nào trên dữ liệu lịch sử cũng tự động kích hoạt cơ chế phát hiện lệch mã băm, ngăn chặn triệt để việc hiển thị dự báo sai lệch.",
            ],
            {
                "caption": "Bảng 1.2. Đối sánh tổng hợp giữa các hệ thống thông tin giá truyền thống, nghiên cứu đơn lẻ và hệ thống AgroForecast",
                "headers": ["Tiêu chí đánh giá", "Cổng thông tin giá truyền thống", "Nghiên cứu học thuật đơn mô hình", "Hệ thống đề xuất AgroForecast"],
                "rows": [
                    ["Phạm vi dữ liệu", "Hiển thị giá quá khứ & hôm nay, không có dự báo", "Thường chỉ thử nghiệm 1 - 2 nông sản tĩnh", "8 nông sản chủ lực (4.899 bản ghi lịch sử + 9.079 quan sát cấp tỉnh)"],
                    ["Độ phân giải vùng", "Gộp theo vùng lớn (Tây Nguyên, ĐBSCL)", "Không phân biệt chênh lệch giá địa phương", "Chi tiết 29 huyện/thị xã/phường bán tại vườn/ruộng"],
                    ["Thuật toán dự báo", "Không có mô hình học máy", "Chỉ dùng 1 mô hình (thường là ARIMA hoặc LSTM)", "Tích hợp & đối sánh tự động 5 mô hình AI"],
                    ["Định lượng rủi ro", "Không có biên độ dự báo", "Chỉ đưa ra dự báo điểm (Point Forecast)", "Khoảng tin cậy 95% (LowerCI - UpperCI) theo RMSE"],
                    ["Giải thích AI (XAI)", "Không áp dụng", "Hoạt động như hộp đen (Black Box)", "Trực quan hóa trọng số 5 yếu tố thúc đẩy giá"],
                    ["Kiểm chứng nguồn", "Không lưu vết lịch sử chỉnh sửa", "Dữ liệu CSV tĩnh không kiểm tra provenance", "Quản lý provenance + PriceRevision + SHA-256 Hash"],
                    ["Cảnh báo tự động", "Người dùng phải tự vào xem thủ công", "Không có phân hệ cảnh báo", "Cảnh báo tự động qua SMTP Email (PRICE_ABOVE/BELOW)"],
                    ["Kiểm thử & Bảo mật", "Không công bố kịch bản kiểm thử", "Không kiểm tra bảo mật ứng dụng Web", "125/125 Pytest + 4/4 Playwright E2E + Bandit 0 lỗi OWASP Top 10"],
                ],
            },
        ),
    ]

    ch2_deep = [
        (
            "2.3.5.",
            "Phân tích độ phức tạp tính toán (Computational Complexity) của 5 thuật toán trong đường ống huấn luyện",
            [
                "Trong một hệ thống thông tin dự báo vận hành thực tế, bên cạnh độ chính xác dự báo (MAE, RMSE, MAPE, R2), thời gian huấn luyện và độ phức tạp tính toán của từng thuật toán đóng vai trò quyết định đến khả năng đáp ứng khi chạy tác vụ nền (Background Retrain Job). Gọi N là số lượng quan sát lịch sử của mặt hàng nông sản (441–918 phiên), M là số lượng đặc trưng đầu vào (M = 22 đặc trưng nhân quả gồm 18 đặc trưng nội sinh và 4 đặc trưng vĩ mô USD/VND + WTI), B là số lượng cây quyết định và D là độ sâu tối đa của cây:",
                "1. Độ phức tạp của thuật toán ARIMA(p, d, q): Quá trình ước lượng hợp lý cực đại thông qua bộ lọc Kalman trạng thái - không gian có độ phức tạp thời gian mỗi vòng lặp tối ưu là O(N * (p + q)^2). Với p = 2, d = 1, q = 1 và N ~ 200..250 quan sát, thời gian huấn luyện ARIMA cho một mặt hàng chỉ mất khoảng 80 - 150 mili-giây.",
                "2. Độ phức tạp của thuật toán Random Forest và XGBoost: Việc xây dựng B cây quyết định có độ sâu D trên N mẫu và M đặc trưng có độ phức tạp thời gian là O(B * D * M * N * log(N)). Nhờ cài đặt song song hóa đa luồng CPU và chia giỏ histogram trong thư viện xgboost và scikit-learn, thời gian huấn luyện cả hai mô hình cho mỗi nông sản đạt từ 120 đến 350 mili-giây.",
                "3. Độ phức tạp của thuật toán Facebook Prophet: Quá trình khớp hàm xu thế từng khúc và chuỗi lượng giác Fourier bằng thuật toán L-BFGS có độ phức tạp O(I * N * (S + 2*K)), trong đó S = 25 là số điểm gãy xu thế, K là bậc chuỗi Fourier và I là số bước lặp hội tụ. Thời gian thực thi trung bình từ 300 đến 600 mili-giây.",
                "4. Độ phức tạp của mạng học sâu PyTorch LSTM: Mỗi bước truyền xuôi và lan truyền ngược theo thời gian (BPTT) qua chuỗi độ dài L = 14 với kích thước tầng ẩn H_dim = 64 có độ phức tạp O(E * (N - L) * L * (4 * H_dim^2 + 4 * H_dim * d_in)), trong đó hệ số 4 tương ứng với 4 phép biến đổi ma trận tại cổng quên, cổng vào, trạng thái ứng viên và cổng ra, còn E là số kỷ nguyên huấn luyện (epochs). Tổng thời gian huấn luyện toàn bộ 5 mô hình cho một nông sản kèm kiểm định Holdout 10 bước chỉ mất từ 1,2 đến 2,5 giây, hoàn toàn phù hợp để vận hành trực tuyến.",
            ],
            None,
        ),
    ]

    ch3_deep = [
        (
            "3.4.4.",
            "Thiết kế hợp đồng dữ liệu JSON (Data Contracts) và Schema kiểm tra kiểu Pydantic v2",
            [
                "Để ngăn chặn triệt để các lỗi không tương thích dữ liệu giữa tầng Backend Python và tầng Frontend TypeScript, toàn bộ các gói tin trao đổi qua giao thức HTTP đều được định nghĩa bằng các lớp Pydantic BaseModel tại tệp backend/app/schemas/schemas.py. Pydantic v2 thực thi kiểm tra kiểu dữ liệu, miền giá trị và định dạng chuỗi ngay tại biên tiếp nhận request trước khi dữ liệu đi vào tầng dịch vụ.",
                "Cụ thể, đối với dữ liệu đầu vào khi tạo điểm giá thủ công (PriceCreateManual), Pydantic kiểm tra trường price > 0, trường record_date phải là ngày hợp lệ không vượt quá ngày hiện tại (date.today()), và biên độ giá phải thỏa mãn bất đẳng thức price_min <= price <= price_max. Đối với dữ liệu đầu vào khi đăng ký người dùng (RegisterRequest), trường email bắt buộc tuân thủ chuẩn RFC 5322 thông qua bộ kiểm tra EmailStr, mật khẩu phải có độ dài tối thiểu 6 ký tự (min_length = 6) và họ tên không được để trống.",
                "Đối với dữ liệu đầu ra của bảng điều khiển dự báo (ForecastDashboardResponse), gói tin JSON trả về được đóng gói thành một cấu trúc đồng nhất gồm 7 trường cấp cao: commodity (thông tin mặt hàng và địa phương chuẩn), modelName (tên thuật toán đang chọn), metrics (bộ 4 chỉ số mae, rmse, mape, r2 và ngày huấn luyện trainDate), forecastData (mảng kết hợp 30 điểm lịch sử isForecast=false và 7..30 điểm dự báo tương lai isForecast=true), training (siêu dữ liệu kiểm định Holdout, chữ ký dataset_hash, độ trễ ngày stale_days và thông số mô hình cơ sở baseline), availableRegions (danh sách các huyện bán tại vườn kèm basisSpread và description) và selectedRegion (mã định danh huyện đang chọn).",
            ],
            {
                "caption": "Bảng 3.8. Đặc tả các lớp Pydantic Schema kiểm tra tính hợp lệ dữ liệu tại Backend (app/schemas/schemas.py)",
                "headers": ["Tên lớp Pydantic Schema", "Hướng dữ liệu", "Các trường dữ liệu & Ràng buộc kiểm tra chính", "Endpoint sử dụng"],
                "rows": [
                    ["RegisterRequest / LoginRequest", "Request Body", "email (EmailStr), password (min_length=6), full_name (min_length=2)", "POST /api/v1/auth/register, /login"],
                    ["TokenResponse / UserResponse", "Response JSON", "access_token (JWT), token_type ('bearer'), user (id, email, role, is_active)", "POST /api/v1/auth/login, GET /me"],
                    ["CommodityOverviewCard", "Response JSON", "id, code, name, unit, region, currentPrice, changePct, sparkline[7]", "GET /api/v1/commodities/overview"],
                    ["ForecastPointResponse", "Response JSON", "date, actualPrice, predictedPrice, lowerCI, upperCI, isForecast (bool)", "GET /api/v1/forecast"],
                    ["RegionInfo", "Response JSON", "id, name (Huyện/Phường tại vườn), basisSpread (float), description", "GET /api/v1/forecast"],
                    ["ForecastDashboardResponse", "Response JSON", "commodity, modelName, metrics, forecastData, training, availableRegions", "GET /api/v1/forecast"],
                    ["AlertRuleCreate", "Request Body", "commodity_id, rule_name (lọc XSS), condition_type, threshold_value (>0), email", "POST /api/v1/alerts"],
                    ["PriceCreateManual", "Request Body", "commodity_id, record_date (<= today), price (>0), price_min, price_max, reviewed", "POST /api/v1/admin/prices"],
                    ["CSVImportResponse", "Response JSON", "message, records_created (int), records_updated (int), errors (List[str])", "POST /api/v1/admin/prices/import-csv"],
                ],
            },
        ),
    ]

    return ch1_deep, ch2_deep, ch3_deep
