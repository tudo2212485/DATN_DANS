# -*- coding: utf-8 -*-
"""
Chương 3: PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG DỰ BÁO GIÁ NÔNG SẢN AGROFORECAST
"""

CHUONG_3_DATA = {
    "title": "Chương 3: PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG DỰ BÁO GIÁ NÔNG SẢN AGROFORECAST",
    "sections": [
        {
            "code": "3.1.",
            "title": "Phân tích yêu cầu hệ thống",
            "subsections": [
                {
                    "code": "3.1.1.",
                    "title": "Xác định các tác nhân (Actors) và ma trận phân quyền vai trò (RBAC)",
                    "paragraphs": [
                        "Hệ thống AgroForecast được thiết kế để phục vụ ba nhóm tác nhân người dùng chính trong hệ sinh thái nông nghiệp Việt Nam, được quản lý thông qua cơ chế Kiểm soát truy cập dựa trên vai trò (Role-Based Access Control - RBAC) tại mô-đun app/core/deps.py:",
                        "1. Nông hộ, Thương lái và Nhà đầu tư (Vai trò User / Guest): Là những người trực tiếp sản xuất nông sản tại vườn/ruộng hoặc thu mua nông sản tại địa phương. Họ có nhu cầu tra cứu bảng giá bán tại vườn hôm nay của 8 mặt hàng chủ lực, xem biểu đồ dự báo biến động giá 7 ngày, 10 ngày, 14 ngày và 30 ngày tới theo từng huyện chuyên canh, xem đối sánh sai số giữa 5 mô hình AI, tải báo cáo dự báo định dạng CSV và đăng ký nhận cảnh báo tự động qua Email khi giá vượt ngưỡng mong muốn.",
                        "2. Chuyên viên Phân tích Thị trường (Vai trò Analyst): Ngoài toàn bộ quyền tra cứu của User, chuyên viên phân tích được phép truy cập bảng thống kê hệ thống, tra cứu nhật ký thu thập dữ liệu của Bot Scraper, xem toàn bộ lịch sử giá bao gồm cả các bản ghi đang chờ xác minh (unverified) và xuất tập tin dữ liệu lịch sử phục vụ công tác kiểm định chất lượng dữ liệu.",
                        "3. Quản trị viên Hệ thống (Vai trò Admin): Là người có thẩm quyền cao nhất trong hệ thống, chịu trách nhiệm quản lý danh mục nông sản (CRUD), nhập bổ sung hoặc hiệu chỉnh điểm giá thủ công kèm lưu vết lịch sử chỉnh sửa (Price Revisions), nhập dữ liệu hàng loạt từ file CSV, kích hoạt tác vụ ngầm thu thập dữ liệu (Scrape Task) và huấn luyện lại 5 mô hình học máy (Retrain Task), chuyển đổi mô hình AI mặc định của hệ thống và quản lý tài khoản người dùng (cấp quyền, khóa/mở khóa tài khoản).",
                    ],
                    "tables": [
                        {
                            "caption": "Bảng 3.1. Ma trận phân quyền truy cập chức năng theo vai trò người dùng (RBAC Matrix)",
                            "headers": ["Mã chức năng", "Tên nhóm chức năng nghiệp vụ", "Khách / Nông hộ (User)", "Chuyên viên (Analyst)", "Quản trị viên (Admin)"],
                            "rows": [
                                ["UC-01", "Tra cứu tổng quan thị trường & giá bán tại vườn theo huyện", "Cho phép", "Cho phép", "Cho phép"],
                                ["UC-02", "Phân tích & Dự báo AI 5 mô hình (7, 10, 14, 30 ngày) + XAI", "Cho phép", "Cho phép", "Cho phép"],
                                ["UC-03", "Tra cứu lịch sử giá đã xác minh & Xuất báo cáo CSV", "Cho phép", "Cho phép", "Cho phép"],
                                ["UC-04", "Đối sánh tương quan biến động giá đa nông sản", "Cho phép", "Cho phép", "Cho phép"],
                                ["UC-05", "Tạo, bật/tắt, xóa và gửi thử quy tắc cảnh báo giá Email", "Cho phép", "Cho phép", "Cho phép"],
                                ["UC-06", "Đăng ký tài khoản, Đăng nhập JWT và Xem hồ sơ cá nhân", "Cho phép", "Cho phép", "Cho phép"],
                                ["UC-07", "Xem thống kê hệ thống, tiến trình tác vụ nền & nhật ký Scraper", "Từ chối (403)", "Cho phép", "Cho phép"],
                                ["UC-08", "Quản lý danh mục nông sản (Thêm, Sửa, Xóa nông sản)", "Từ chối (403)", "Từ chối (403)", "Cho phép"],
                                ["UC-09", "Cập nhật giá thủ công, duyệt nguồn (Reviewed) & Nhập CSV", "Từ chối (403)", "Từ chối (403)", "Cho phép"],
                                ["UC-10", "Kích hoạt Bot thu thập dữ liệu (Scrape) & Huấn luyện lại AI (Retrain)", "Từ chối (403)", "Từ chối (403)", "Cho phép"],
                                ["UC-11", "Cấu hình mô hình AI mặc định & Quản lý tài khoản người dùng", "Từ chối (403)", "Từ chối (403)", "Cho phép"],
                            ],
                        }
                    ],
                },
                {
                    "code": "3.1.2.",
                    "title": "Đặc tả chi tiết các yêu cầu chức năng cốt lõi",
                    "paragraphs": [
                        "Hệ thống được phân rã thành 6 phân hệ chức năng chính liên kết chặt chẽ với nhau:",
                        "Phân hệ 1 - Tổng quan thị trường giá nông sản bán tại vườn (Market Overview): Hiển thị dải chỉ số độ rộng thị trường (số mặt hàng tăng, giảm, đi ngang, mặt hàng tăng trưởng mạnh nhất), thanh tìm kiếm và lọc nhanh theo nhóm nông sản hoặc địa phương, lưới thẻ nông sản (Commodity Cards) kèm đồ thị thu nhỏ (Sparkline 7 ngày) và bảng khảo sát giá bán tại vườn theo địa phương.",
                        "Phân hệ 2 - Phân tích và Dự báo giá nông sản bằng 5 mô hình AI (AI Forecast & Spatio-Temporal Dashboard): Cho phép người dùng lựa chọn linh hoạt giữa 8 mặt hàng nông sản, 5 thuật toán học máy (LSTM, Prophet, ARIMA, XGBoost, Random Forest), 4 kỳ hạn dự báo (7, 10, 14, 30 ngày) và danh sách các huyện bán tại vườn/ruộng tương ứng. Hệ thống hiển thị dải 4 chỉ số tổng hợp (Giá bán tại vườn hiện tại, Giá dự báo cuối kỳ kèm tỷ lệ % thay đổi, Biên độ dao động cuối kỳ theo khoảng tin cậy 95%, và Sai số mô hình MAPE kèm gợi ý tự động mô hình có sai số thấp nhất), biểu đồ kết hợp đường thực tế liền nét với đường dự báo đứt nét và vùng bóng CI 95%, mô-đun Giải thích mô hình (Explainable AI - XAI Feature Drivers), biểu đồ so sánh sai số giữa 5 mô hình và bảng lịch trình giá dự báo chi tiết từng ngày có hỗ trợ tải xuống CSV.",
                        "Phân hệ 3 - Quản lý lịch sử biến động giá và Kiểm chứng nguồn gốc (Historical Observations & Provenance): Cho phép lọc chuỗi giá lịch sử theo khoảng ngày tùy chọn (30 ngày, 90 ngày, 1 năm hoặc toàn bộ lịch sử), hiển thị rõ siêu dữ liệu nguồn công bố (tên cơ quan công bố, đường dẫn gốc URL để đối chiếu, loại giá bán tại hộ/vườn, quy cách), thống kê số ngày khuyết dữ liệu (missing dates) và trạng thái sẵn sàng cho huấn luyện học máy (Model Readiness).",
                        "Phân hệ 4 - Đối sánh tương quan thị trường (Market Comparison): Trực quan hóa đường cong tăng trưởng chuẩn hóa giữa các nhóm nông sản chủ lực trên cùng một hệ trục tọa độ và bảng đối sánh biên độ giá sàn - giá trần tại từng địa phương.",
                        "Phân hệ 5 - Cảnh báo biến động giá tự động (Automated Price Alerts): Cho phép thiết lập các quy tắc cảnh báo theo điều kiện giá vượt lên trên ngưỡng (PRICE_ABOVE) hoặc tụt xuống dưới ngưỡng (PRICE_BELOW), tự động đối chiếu khi có dữ liệu giá mới, gửi thông báo qua giao thức SMTP Email và lưu vết lịch sử kích hoạt cảnh báo (Audit Trail).",
                        "Phân hệ 6 - Quản trị hệ thống và Điều phối đường ống ML (Admin Control Center): Cung cấp công cụ quản trị toàn diện cho Admin để nhập/xuất CSV, điều chỉnh điểm giá kèm lưu trữ phiên bản cũ vào bảng price_revisions, theo dõi tiến trình ngầm (Background Jobs) của Bot thu thập dữ liệu và bộ huấn luyện 5 mô hình AI theo thời gian thực.",
                    ],
                },
                {
                    "code": "3.1.3.",
                    "title": "Đặc tả các yêu cầu phi chức năng (Hiệu năng, Toàn vẹn dữ liệu và Bảo mật)",
                    "paragraphs": [
                        "Về hiệu năng phản hồi (Performance & Latency): Hệ thống cài đặt bộ nhớ đệm dự báo trong RAM (In-Memory Prediction Cache tại ml_pipeline/predictor.py) với thời gian sống TTL = 15 phút kết hợp lưu trữ sẵn kết quả dự báo đã kiểm định trong bảng forecasts của PostgreSQL, đảm bảo thời gian phản hồi API dự báo đạt dưới 50 ms cho các truy vấn lặp lại.",
                        "Về tính toàn vẹn dữ liệu học máy (Data Integrity & Anti-Tampering): Mọi phiên huấn luyện trong bảng training_runs đều tính toán và lưu trữ chữ ký băm mật mã SHA-256 (dataset_hash) của toàn bộ chuỗi lịch sử đầu vào thông qua hàm fingerprint(). Khi người dùng yêu cầu hiển thị dự báo hoặc khi có bất kỳ điểm giá lịch sử nào bị chỉnh sửa, hệ thống lập tức đối chiếu lại chữ ký SHA-256; nếu dữ liệu lịch sử đã thay đổi mà mô hình chưa được huấn luyện lại, hệ thống sẽ cảnh báo minh bạch (HTTP 409 Conflict) thay vì hiển thị dự báo cũ không còn khớp với thực tế.",
                        "Về độ tin cậy và an toàn bảo mật: Hệ thống phải vượt qua 100% kịch bản kiểm thử tự động (72/72 bài kiểm thử Pytest) và đáp ứng đầy đủ các tiêu chuẩn phòng vệ OWASP Top 10 trước các cuộc tấn công giả mạo JWT, leo thang đặc quyền RBAC, SQL Injection, Stored/Reflected XSS, CSV Formula Injection và tấn công vét cạn mật khẩu Brute-Force.",
                    ],
                },
            ],
        },
        {
            "code": "3.2.",
            "title": "Thiết kế kiến trúc tổng thể và luồng xử lý dữ liệu",
            "subsections": [
                {
                    "code": "3.2.1.",
                    "title": "Kiến trúc phân tầng 4 lớp (4-Tier System Architecture)",
                    "paragraphs": [
                        "Hệ thống AgroForecast được thiết kế theo kiến trúc phân tầng 4 lớp tách biệt rõ ràng về trách nhiệm (Separation of Concerns), giúp dễ dàng mở rộng, bảo trì và kiểm thử độc lập từng thành phần:",
                        "Tầng 1 - Tầng Giao diện Trình diễn (Presentation Tier - Next.js 14 Frontend): Vận hành tại cổng 3000, bao gồm các trang giao diện App Router (/ , /forecast, /history, /compare, /alerts, /admin, /login, /register), các thành phần biểu đồ Recharts tương tác, bộ quản lý trạng thái xác thực JWT và lớp giao tiếp HTTP Client (src/lib/api.ts).",
                        "Tầng 2 - Tầng Cổng Bảo mật và Điều phối REST API (API & Security Gateway Tier - FastAPI): Vận hành tại cổng 8000, tiếp nhận mọi yêu cầu HTTP thông qua chuỗi lớp trung gian: CORSMiddleware -> SecurityHeadersMiddleware (gắn 7 tiêu đề bảo mật OWASP) -> RateLimiter (chống Brute-Force và DoS) -> OAuth2 JWT & RBAC Dependency (get_current_user, require_role) -> Pydantic v2 Schema Validation -> Các bộ định tuyến API v1 (/api/v1/*).",
                        "Tầng 3 - Tầng Nghiệp vụ và Đường ống Học máy (Business Logic & ML Pipeline Tier): Bao gồm các dịch vụ nghiệp vụ (commodity_service, history_service, forecast_service, training_service, alert_service, job_service) và gói đường ống học máy chuyên biệt (ml_pipeline: source_catalog, agro_history, domestic_sources, periodic_reports, data_loader, feature_engineering, model_trainer, predictor, scheduler_jobs).",
                        "Tầng 4 - Tầng Lưu trữ Bền vững (Data Persistence Tier): Bao gồm Cơ sở dữ liệu quan hệ PostgreSQL (lưu trữ 11 bảng dữ liệu nghiệp vụ có đánh chỉ mục tối ưu) và Kho lưu trữ trọng số mô hình trên đĩa cứng (ml_pipeline/saved_models/ chứa các tập tin .pt của PyTorch LSTM, .pkl của Prophet/XGBoost/RandomForest/ARIMA và _metrics.json).",
                    ],
                },
                {
                    "code": "3.2.2.",
                    "title": "Thiết kế đường ống thu thập, xác minh nguồn gốc (Provenance) và huấn luyện tự động",
                    "paragraphs": [
                        "Điểm khác biệt cốt lõi trong thiết kế của AgroForecast là quy trình kiểm soát chất lượng dữ liệu đầu vào trước khi cho phép mô hình học máy học quy luật giá. Mỗi bản ghi giá trong bảng price_history được quản lý bởi trường trạng thái nguồn gốc provenance thuộc một trong ba giá trị: 'collected' (dữ liệu được bóc tách tự động thành công từ nguồn công bố chính thức kèm siêu dữ liệu JSON source_details ghi rõ URL, ngày công bố, chợ/địa phương, loại giá), 'reviewed' (dữ liệu đã được Quản trị viên kiểm duyệt và xác nhận tính chính xác), hoặc 'unverified' (dữ liệu mới nhập thô chưa qua kiểm chứng).",
                        "Hàm modeling_rows() và readiness() trong mô-đun app/services/history_service.py thiết lập quy tắc kiểm định nghiêm ngặt: (1) Loại bỏ hoàn toàn các bản ghi 'unverified' khỏi tập dữ liệu huấn luyện; (2) Kiểm tra các khoảng trống thời gian (gaps) để phát hiện kỳ nghỉ lễ hoặc giai đoạn ngưng công bố dài hạn; (3) Yêu cầu chuỗi dữ liệu liên tục gần nhất phải đạt tối thiểu 60 quan sát đối với chuỗi ngày (daily), 30 quan sát đối với chuỗi không đều (irregular) và 24 kỳ đối với chuỗi báo cáo định kỳ (periodic). Chỉ khi đạt trạng thái ready = True, bộ huấn luyện training_service.retrain() mới tiến hành chia tập Train/Holdout, huấn luyện đồng thời 5 mô hình, tính toán chỉ số sai số và cập nhật bảng forecasts.",
                    ],
                },
                {
                    "code": "3.2.3.",
                    "title": "Thiết kế mô-đun Giải thích Mô hình Học máy (Explainable AI - XAI Feature Importance)",
                    "paragraphs": [
                        "Để giúp người nông dân, thương lái và hội đồng chuyên môn hiểu rõ vì sao mô hình AI đưa ra mức dự báo tăng hay giảm thay vì hoạt động như một 'hộp đen' (Black Box), hệ thống thiết kế thành phần XAIFeatureDrivers.tsx kết hợp trọng số đặc trưng của mô hình để định lượng tỷ trọng đóng góp (%) và chiều hướng tác động (Thúc đẩy tăng / Kìm hãm giá / Ổn định) của 5 nhóm nhân tố chính đối với từng loại nông sản: (1) Động lượng giá trễ ngắn hạn (Lag t-1 đến t-7); (2) Chu kỳ mùa vụ thu hoạch và thời tiết vùng trồng (Lượng mưa Tây Nguyên, nắng hạn El Nino hoặc sương muối Đà Lạt); (3) Tỷ giá USD/VND và giá sàn kỳ hạn quốc tế; (4) Chi phí vận chuyển, phân bón đầu vào; và (5) Nhu cầu thu mua xuất khẩu của các thị trường chủ lực.",
                    ],
                },
            ],
        },
        {
            "code": "3.3.",
            "title": "Thiết kế Cơ sở dữ liệu quan hệ (PostgreSQL Schema & ERD)",
            "subsections": [
                {
                    "code": "3.3.1.",
                    "title": "Tổng quan kiến trúc Cơ sở dữ liệu và mối quan hệ thực thể (ERD)",
                    "paragraphs": [
                        "Cơ sở dữ liệu của hệ thống AgroForecast (tên CSDL: agroforecast_db) được thiết kế chuẩn hóa ở dạng chuẩn 3 (3NF) gồm 11 bảng dữ liệu quan hệ được định nghĩa tại app/models/models.py và database/init.sql. Trong đó, bảng commodities đóng vai trò là thực thể trung tâm có quan hệ một-nhiều (1 - N, kèm ràng buộc xóa lan truyền ON DELETE CASCADE) tới 5 bảng dữ liệu chuỗi thời gian và nghiệp vụ: price_history (lịch sử giá hàng ngày), periodic_prices (lịch sử giá mua/bán theo kỳ báo cáo), forecasts (điểm dự báo của 5 mô hình AI), training_runs (nhật ký và chữ ký SHA-256 của các phiên huấn luyện), và alert_rules (quy tắc cảnh báo giá). Bảng price_history có quan hệ 1 - N tới bảng price_revisions để lưu vết mọi lịch sử chỉnh sửa điểm giá; bảng alert_rules có quan hệ 1 - N tới bảng alert_logs để lưu nhật ký gửi cảnh báo.",
                    ],
                    "tables": [
                        {
                            "caption": "Bảng 3.2. Danh mục 11 bảng dữ liệu trong Cơ sở dữ liệu PostgreSQL của hệ thống AgroForecast",
                            "headers": ["STT", "Tên bảng vật lý", "Lớp ORM Model", "Khóa chính (PK)", "Khóa ngoại (FK)", "Chức năng lưu trữ chính"],
                            "rows": [
                                ["1", "users", "User", "id (SERIAL)", "Không", "Lưu tài khoản người dùng, mật khẩu băm Bcrypt, vai trò (admin/analyst/user) và trạng thái khóa"],
                                ["2", "commodities", "Commodity", "id (SERIAL)", "Không", "Lưu 8 mặt hàng nông sản chủ lực, mã code, đơn vị tính, địa phương bán tại vườn/ruộng"],
                                ["3", "price_history", "PriceHistory", "id (SERIAL)", "commodity_id -> commodities.id", "Lưu chuỗi giá lịch sử theo ngày, min/max, sản lượng, nguồn và trạng thái xác minh provenance"],
                                ["4", "periodic_prices", "PeriodicPrice", "id (SERIAL)", "commodity_id -> commodities.id", "Lưu dữ liệu giá mua và giá bán theo kỳ báo cáo (dành cho mặt hàng công bố theo tuần/kỳ)"],
                                ["5", "price_revisions", "PriceRevision", "id (SERIAL)", "price_history_id, commodity_id", "Lưu vết kiểm toán (Audit Trail) các phiên bản giá cũ trước khi Admin cập nhật"],
                                ["6", "training_runs", "TrainingRun", "id (SERIAL)", "commodity_id -> commodities.id", "Lưu siêu dữ liệu phiên huấn luyện AI, chữ ký SHA-256 (dataset_hash) và kết quả kiểm định Holdout"],
                                ["7", "forecasts", "Forecast", "id (SERIAL)", "commodity_id, training_run_id", "Lưu chuỗi dự báo tương lai của 5 mô hình AI kèm lower_ci, upper_ci, MAE, RMSE, MAPE, R2"],
                                ["8", "alert_rules", "AlertRule", "id (SERIAL)", "commodity_id -> commodities.id", "Lưu quy tắc cảnh báo biến động giá (PRICE_ABOVE / PRICE_BELOW), ngưỡng giá và Email nhận"],
                                ["9", "alert_logs", "AlertLog", "id (SERIAL)", "rule_id -> alert_rules.id", "Lưu lịch sử các lần kích hoạt cảnh báo tự động và trạng thái gửi thông báo"],
                                ["10", "background_jobs", "BackgroundJob", "id (SERIAL)", "Không", "Lưu tiến trình, trạng thái (RUNNING/SUCCESS/FAILED) của tác vụ cào dữ liệu và huấn luyện ngầm"],
                                ["11", "system_settings", "SystemSetting", "key (VARCHAR)", "Không", "Lưu cấu hình toàn cục của hệ thống (như thuật toán AI mặc định active_model)"],
                            ],
                        }
                    ],
                },
                {
                    "code": "3.3.2.",
                    "title": "Đặc tả chi tiết cấu trúc các bảng dữ liệu cốt lõi",
                    "paragraphs": [
                        "Dưới đây là đặc tả chi tiết các trường dữ liệu, kiểu dữ liệu vật lý trong PostgreSQL, ràng buộc toàn vẹn và ý nghĩa của các bảng trọng tâm trong hệ thống:",
                    ],
                    "tables": [
                        {
                            "caption": "Bảng 3.3. Đặc tả cấu trúc bảng danh mục nông sản (commodities) và bảng lịch sử giá (price_history)",
                            "headers": ["Tên bảng", "Tên trường (Column)", "Kiểu dữ liệu", "Ràng buộc", "Mô tả chi tiết ý nghĩa"],
                            "rows": [
                                ["commodities", "id", "SERIAL / INTEGER", "PRIMARY KEY", "Mã định danh tự tăng của mặt hàng nông sản (1 -> 8)"],
                                ["commodities", "code", "VARCHAR(50)", "UNIQUE, NOT NULL, INDEX", "Mã ký hiệu chuẩn (RICE_IR504, COFFEE_ROBUSTA, PEPPER_BLACK...)"],
                                ["commodities", "name", "VARCHAR(255)", "NOT NULL", "Tên hiển thị tiếng Việt của nông sản (Cà phê Robusta, Hồ tiêu đen...)"],
                                ["commodities", "category", "VARCHAR(100)", "NOT NULL", "Nhóm phân loại (Nông sản xuất khẩu, Lương thực, Nông sản đặc sản...)"],
                                ["commodities", "unit", "VARCHAR(50)", "NOT NULL", "Đơn vị tính chuẩn (VNĐ/kg hoặc VNĐ/tấn)"],
                                ["commodities", "region", "VARCHAR(255)", "NOT NULL", "Địa phương tham chiếu chuẩn bán tại vườn / tại ruộng"],
                                ["commodities", "description", "TEXT", "NULLABLE", "Mô tả quy cách thương phẩm và các huyện thu mua trọng điểm"],
                                ["price_history", "id", "SERIAL / INTEGER", "PRIMARY KEY", "Mã định danh bản ghi giá lịch sử"],
                                ["price_history", "commodity_id", "INTEGER", "FK -> commodities.id, INDEX", "Liên kết tới mặt hàng nông sản tương ứng"],
                                ["price_history", "record_date", "DATE", "NOT NULL, INDEX", "Ngày ghi nhận mức giá giao dịch thực tế"],
                                ["price_history", "price", "NUMERIC(12, 2)", "NOT NULL", "Mức giá bán tại vườn / tại ruộng ở địa phương chuẩn"],
                                ["price_history", "price_min / price_max", "NUMERIC(12, 2)", "NULLABLE", "Biên độ giá thấp nhất và cao nhất trong ngày khảo sát"],
                                ["price_history", "volume", "NUMERIC(12, 2)", "DEFAULT 0", "Ước tính khối lượng giao dịch hoặc thu hoạch (tấn)"],
                                ["price_history", "source", "VARCHAR(255)", "NULLABLE", "Tên cơ quan / hiệp hội công bố mức giá"],
                                ["price_history", "provenance", "VARCHAR(30)", "NOT NULL, DEFAULT 'unverified'", "Trạng thái xác minh nguồn gốc: collected | reviewed | unverified"],
                                ["price_history", "source_details", "TEXT (JSON)", "NULLABLE", "Chuỗi JSON lưu URL gốc, ngày công bố, chợ địa phương, loại giá"],
                            ],
                        },
                        {
                            "caption": "Bảng 3.4. Đặc tả cấu trúc bảng kết quả dự báo học máy (forecasts) và phiên huấn luyện (training_runs)",
                            "headers": ["Tên bảng", "Tên trường (Column)", "Kiểu dữ liệu", "Ràng buộc", "Mô tả chi tiết ý nghĩa"],
                            "rows": [
                                ["forecasts", "id", "SERIAL / INTEGER", "PRIMARY KEY", "Mã định danh điểm dự báo tương lai"],
                                ["forecasts", "commodity_id", "INTEGER", "FK -> commodities.id, INDEX", "Mã mặt hàng nông sản được dự báo"],
                                ["forecasts", "training_run_id", "INTEGER", "FK -> training_runs.id, INDEX", "Liên kết tới phiên huấn luyện đã sinh ra dự báo này"],
                                ["forecasts", "model_name", "VARCHAR(50)", "NOT NULL, INDEX", "Tên mô hình AI: LSTM | Prophet | ARIMA | XGBoost | Random Forest"],
                                ["forecasts", "training_date", "DATE", "NOT NULL", "Ngày mốc lịch sử cuối cùng dùng để huấn luyện mô hình"],
                                ["forecasts", "forecast_date", "DATE", "NOT NULL, INDEX", "Ngày mục tiêu trong tương lai được dự báo (t+1 .. t+30)"],
                                ["forecasts", "predicted_price", "NUMERIC(12, 2)", "NOT NULL", "Giá dự báo trung tâm (yhat) tính theo đơn vị của nông sản"],
                                ["forecasts", "lower_ci / upper_ci", "NUMERIC(12, 2)", "NOT NULL", "Cận dưới và cận trên của khoảng tin cậy 95% (yhat +/- 1.96*RMSE)"],
                                ["forecasts", "mae / rmse / mape / r2", "NUMERIC(12, 4)", "NULLABLE", "Bốn chỉ số đánh giá sai số của mô hình trên tập kiểm thử Holdout"],
                                ["training_runs", "id", "SERIAL / INTEGER", "PRIMARY KEY", "Mã định danh phiên huấn luyện"],
                                ["training_runs", "commodity_id", "INTEGER", "FK -> commodities.id, INDEX", "Mã mặt hàng nông sản được huấn luyện"],
                                ["training_runs", "dataset_hash", "VARCHAR(64)", "NOT NULL, INDEX", "Chữ ký băm mật mã SHA-256 đảm bảo toàn vẹn tập dữ liệu huấn luyện"],
                                ["training_runs", "history_start / end", "DATE", "NOT NULL", "Ngày bắt đầu và ngày kết thúc của chuỗi lịch sử đưa vào huấn luyện"],
                                ["training_runs", "observed_count", "INTEGER", "NOT NULL", "Tổng số điểm quan sát hợp lệ đã dùng để huấn luyện và kiểm định"],
                                ["training_runs", "metadata_json", "TEXT (JSON)", "NOT NULL", "Lưu chi tiết kết quả Holdout, mô hình cơ sở Naive và danh sách điểm giá"],
                            ],
                        },
                    ],
                },
            ],
        },
        {
            "code": "3.4.",
            "title": "Thiết kế hệ thống RESTful API và Giao diện người dùng (UI/UX)",
            "subsections": [
                {
                    "code": "3.4.1.",
                    "title": "Thiết kế hệ thống 28 Endpoint RESTful API theo chuẩn OpenAPI 3.0",
                    "paragraphs": [
                        "Toàn bộ giao tiếp giữa Frontend và Backend được chuẩn hóa qua tiền tố /api/v1 với 8 nhóm bộ định tuyến (Routers) được định nghĩa tại app/api/v1/api.py. Bảng 3.5 tổng hợp chi tiết các Endpoint chính của hệ thống.",
                    ],
                    "tables": [
                        {
                            "caption": "Bảng 3.5. Đặc tả các Endpoint RESTful API chính của hệ thống AgroForecast",
                            "headers": ["Phương thức", "Đường dẫn Endpoint (URI)", "Phân quyền", "Mô tả chức năng và dữ liệu trả về"],
                            "rows": [
                                ["POST", "/api/v1/auth/register", "Public (Rate Limited)", "Đăng ký tài khoản mới, băm mật khẩu Bcrypt và làm sạch XSS"],
                                ["POST", "/api/v1/auth/login", "Public (Rate Limited)", "Xác thực email/mật khẩu, kiểm tra khóa tài khoản và cấp JWT Bearer Token"],
                                ["GET", "/api/v1/auth/me", "Authenticated User", "Trả về thông tin hồ sơ và vai trò của người dùng đang đăng nhập"],
                                ["GET", "/api/v1/commodities/overview", "Public", "Lấy danh sách 8 nông sản kèm giá bán tại vườn mới nhất, % thay đổi và Sparkline"],
                                ["GET", "/api/v1/commodities/comparison", "Public", "Lấy chuỗi tăng trưởng chuẩn hóa đa nông sản phục vụ biểu đồ đối sánh"],
                                ["GET", "/api/v1/commodities/regional-prices", "Public", "Lấy bảng giá bán tại vườn/ruộng, biên độ sàn/trần và nguồn công bố"],
                                ["GET", "/api/v1/forecast", "Public", "Trả về chuỗi lịch sử + dự báo theo nông sản, mô hình AI, kỳ hạn (7-30 ngày) và huyện (region)"],
                                ["GET", "/api/v1/forecast/compare/{id}", "Public", "Trả về bảng đối sánh 4 chỉ số MAE, RMSE, MAPE, R2 của cả 5 mô hình AI"],
                                ["GET", "/api/v1/predictions/forecast", "Public", "API dự báo tốc độ cao có tích hợp bộ nhớ đệm In-Memory Cache (< 50ms)"],
                                ["POST", "/api/v1/predictions/retrain", "Admin Only (JWT)", "Kích hoạt huấn luyện lại toàn bộ 5 mô hình học máy trong tiến trình nền"],
                                ["GET", "/api/v1/history/sources", "Public", "Lấy danh mục 8 nguồn dữ liệu chính thống Việt Nam và trạng thái sẵn sàng AI"],
                                ["GET", "/api/v1/history", "Public", "Truy vấn lịch sử giá theo khoảng ngày, lọc theo provenance và liệt kê ngày khuyết"],
                                ["GET / POST", "/api/v1/alerts", "Public / User", "Lấy danh sách quy tắc cảnh báo hoặc tạo mới quy tắc cảnh báo (có lọc XSS)"],
                                ["PATCH / DELETE", "/api/v1/alerts/{rule_id}", "Public / User", "Bật/tắt trạng thái hoạt động hoặc xóa quy tắc cảnh báo giá"],
                                ["POST", "/api/v1/alerts/{rule_id}/test", "Public / User", "Kích hoạt gửi thử nghiệm thông báo cảnh báo giá qua giao thức SMTP Email"],
                                ["GET", "/api/v1/admin/stats", "Admin / Analyst", "Lấy số liệu thống kê tổng quan CSDL và trạng thái máy chủ"],
                                ["POST / DELETE", "/api/v1/admin/prices", "Admin Only (JWT)", "Thêm/cập nhật điểm giá thủ công (lưu vết PriceRevision) hoặc xóa điểm giá lỗi"],
                                ["POST / GET", "/api/v1/admin/prices/import-csv", "Admin Only (JWT)", "Nhập dữ liệu giá hàng loạt từ file CSV (chống CSV Injection) & Xuất CSV"],
                                ["POST", "/api/v1/admin/tasks/scrape", "Admin Only (JWT)", "Kích hoạt Bot thu thập dữ liệu lịch sử từ các nguồn nông sản Việt Nam"],
                                ["GET / PATCH", "/api/v1/admin/users", "Admin Only (JWT)", "Quản lý danh sách người dùng, phân quyền Role và khóa/mở khóa tài khoản"],
                            ],
                        }
                    ],
                },
                {
                    "code": "3.4.2.",
                    "title": "Thiết kế Giao diện người dùng (UI/UX) chuẩn Modern Clean Fintech x Sustainable AgriTech",
                    "paragraphs": [
                        "Giao diện người dùng của hệ thống AgroForecast được thiết kế lại toàn diện theo ngôn ngữ thiết kế sản phẩm chuyên nghiệp (lấy cảm hứng từ sự tinh gọn, chuẩn xác dữ liệu của Koyfin/Linear kết hợp sắc thái tự nhiên của nông nghiệp hiện đại):",
                        "Về bảng màu (Color Tokens): Sử dụng nền tảng màu trung tính Zinc sắc nét (#FAFAFA cho nền ứng dụng, #FFFFFF cho bề mặt thẻ, #18181B cho văn bản chính) kết hợp màu chủ đạo Xanh lục trầm Emerald (#059669 cho đường giá thực tế và trạng thái tăng trưởng), Xanh dương kỹ thuật (#2563EB cho đường dự báo AI đứt nét và dải tin cậy CI 95%), Đỏ san hô (#E11D48 cho tín hiệu giảm giá) và Vàng hổ phách (#D97706 cho cảnh báo rủi ro).",
                        "Về kiểu chữ (Typography): Kết hợp bộ phông chữ không chân hiện đại Plus Jakarta Sans hỗ trợ đầy đủ bộ ký tự tiếng Việt có dấu (vietnamese subset) cho tiêu đề/nhãn điều hướng và phông chữ đơn cách kỹ thuật JetBrains Mono (tabular-nums) cho toàn bộ các trường hiển thị giá tiền (VNĐ/kg), tỷ lệ phần trăm biến động (%) và chỉ số sai số (MAE, RMSE, MAPE, R2), giúp các cột số liệu luôn thẳng hàng tuyệt đối.",
                        "Về bố cục hiển thị biểu đồ (Chart Ergonomics): Khắc phục hoàn toàn lỗi nén dẹt đường biểu đồ về gốc 0 bằng thuật toán tự động tính toán miền giá trị trục tung động (yDomain) bám sát biên độ dao động thực tế của nông sản (+/- 12% khoảng đệm), đồng thời nối liền mạch điểm lịch sử cuối cùng với điểm dự báo đầu tiên (isBridgePoint) để người dùng quan sát trực quan hướng bẻ góc của xu hướng giá.",
                    ],
                },
            ],
        },
    ],
}
