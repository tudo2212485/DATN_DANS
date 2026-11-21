# -*- coding: utf-8 -*-
"""
Phần 17: Bổ sung Nội dung Báo cáo Kỹ thuật - Kiểm định Chất lượng & Kiểm toán Bảo mật Hệ thống AgroForecast
Kèm Kỹ năng AI UI (Syncfusion EJ2 AgroGrid, LocationSelector, ProvinceComparisonPanel)
và Kỹ năng Biểu đồ (Syncfusion EJ2 FinChart, Candlestick, Walk-Forward No-Leakage & Conformal 95% CI).
Tài liệu đối chiếu: BaoCaoKLTN.pdf, docs/TEST_REPORT.md, docs/security_audit_report.md, docs/DATA_AND_ML_VERIFICATION_REPORT.md.
"""

CH3_UI_AND_CHART_SKILLS_SECTIONS = [
    {
        "code": "3.6.4.",
        "title": "Thiết kế thành phần AI UI cao cấp với Syncfusion Essential Studio EJ2 React",
        "paragraphs": [
            "Nhằm mang lại trải nghiệm chuyên nghiệp tiệm cận các nền tảng tài chính quốc tế (Fintech) kết hợp công nghệ nông nghiệp số (AgriTech), hệ thống AgroForecast tích hợp bộ thư viện công nghiệp hàng đầu Syncfusion Essential Studio EJ2 React (phiên bản v35.2.12). Việc ứng dụng bộ thư viện này được chuẩn hóa thông qua thành phần AgroGrid (tại tệp frontend/src/components/ui/AgroGrid.tsx) và cấu hình bản địa hóa L10n tiếng Việt hoàn chỉnh (tại tệp frontend/src/lib/syncfusion.ts).",
            "Thành phần AgroGrid cung cấp giải pháp hiển thị và phân tích dữ liệu bảng chuyên sâu với các tính năng vượt trội: (1) Phân trang mượt mà (Pagination) hỗ trợ cấu hình kích thước trang linh hoạt [10, 20, 50, 100] bản ghi; (2) Sắp xếp đa cột (Multi-column Sorting) cho phép kết hợp nhiều tiêu chí đánh giá; (3) Bộ lọc nâng cao kiểu Excel (Excel-like Filtering) và thanh tìm kiếm toàn văn thời gian thực (Search Toolbar); (4) Tính năng trích xuất dữ liệu trực tiếp ra tệp tin Excel (.xlsx) và CSV với cơ chế tự động làm sạch ký tự đầu ô nhằm triệt tiêu nguy cơ tấn công CSV Formula Injection; (5) Hệ thống bản địa hóa (Vietnamese Localization) chuyển ngữ 100% các nhãn điều khiển, tiêu đề menu ngữ cảnh và hộp thoại thông báo sang tiếng Việt chuẩn, xóa bỏ hoàn toàn rào cản ngôn ngữ cho người dùng nông nghiệp.",
            "Bên cạnh lưới dữ liệu, hệ thống xây dựng thành phần chọn vị trí động LocationSelector (tại frontend/src/components/layout/LocationSelector.tsx) kết hợp với ngữ cảnh quản lý trạng thái tập trung LocationContext (tại frontend/src/contexts/LocationContext.tsx). Cơ chế này cho phép người dùng chuyển đổi linh hoạt điểm khảo sát giữa 33 tỉnh thành và 29 vùng trồng chuyên canh trên toàn quốc. Ngay khi vị trí thay đổi, toàn bộ các bảng điều khiển, thẻ nông sản và biểu đồ trên giao diện sẽ tự động đồng bộ lại số liệu tương ứng.",
            "Đặc biệt, hệ thống bổ sung bảng phân tích chênh lệch giá cấp vùng ProvinceComparisonPanel (tại frontend/src/components/dashboard/ProvinceComparisonPanel.tsx). Bảng điều khiển này ứng dụng thuật toán tính khoảng cách trắc địa mặt cầu Haversine giữa tọa độ vùng trồng xuất xứ và tọa độ trung tâm thương mại của tỉnh lựa chọn, từ đó mô hình hóa chi phí logistics minh bạch và trực quan hóa tỷ lệ phần trăm chênh lệch giá bán tại vườn/ruộng so với giá thị trường tiêu thụ tại các đô thị lớn.",
        ],
    },
    {
        "code": "3.6.5.",
        "title": "Thiết kế kỹ năng biểu đồ phân tích kỹ thuật FinChart và trực quan hóa Walk-Forward",
        "paragraphs": [
            "Đối với phân hệ phân tích chuỗi thời gian và dự báo giá, hệ thống xây dựng thành phần biểu đồ tài chính cao cấp FinChart (tại frontend/src/components/ui/FinChart.tsx) dựa trên Syncfusion ChartComponent. Thành phần này giải quyết triệt để các hạn chế của biểu đồ thông thường, mang đến các kỹ năng trực quan hóa phân tích kỹ thuật chuyên sâu:",
            "1. Hỗ trợ chuyển đổi đa dạng 4 chế độ biểu diễn đồ thị: (a) Biểu đồ diện tích mượt (SplineArea) hiển thị rõ nét xu hướng biến động và vùng giá trị lịch sử; (b) Biểu đồ đường phân tích (Line) thể hiện sắc nét các điểm gãy và đường trung bình động MA-7/MA-30; (c) Biểu đồ cột khối lượng (Column) minh họa mức độ biến động tuyệt đối từng phiên; và (d) Biểu đồ Nến Nhật Bản (Candlestick / HiloOpenClose) chuẩn quốc tế hiển thị đầy đủ 4 mức giá Mở cửa (Open), Cao nhất (High), Thấp nhất (Low) và Đóng cửa (Close) trong từng kỳ giao dịch.",
            "2. Trực quan hóa dải khoảng tin cậy mở rộng Conformal Prediction 95% (PICP): Trên chuỗi dự báo 7 ngày và 30 ngày, biểu đồ FinChart hiển thị vùng biên độ sai số động mở rộng dần theo thời gian [y_hat - 1.96 * RMSE, y_hat + 1.96 * RMSE]. Cơ chế này phản ánh trung thực quy luật độ bất định tăng dần khi dự báo càng xa về tương lai, giúp người nông dân và doanh nghiệp nhận biết rõ biên độ rủi ro.",
            "3. Trực quan hóa quy trình đánh giá Walk-Forward 7 ngày không rò rỉ dữ liệu (No Data Leakage Walk-Forward Evaluation): Biểu đồ thể hiện trực quan ranh giới phân tách nghiêm ngặt giữa tập huấn luyện (Train) và tập kiểm thử (Test). Dữ liệu tương lai hoàn toàn không bị rò rỉ vào quá trình trích xuất đặc trưng hay chuẩn hóa dữ liệu.",
            "4. Xử lý tương tác mượt mà và tối ưu hóa DOM: Hệ thống tích hợp tính năng rê chuột tra cứu đa điểm (Crosshair và Multi-series Tooltip), đồng thời xử lý triệt để xung đột gắn kết phần tử DOM (loại bỏ hoàn toàn lỗi BaseTooltip.appendChild thường gặp trên các phiên bản thư viện đồ thị phức tạp), đảm bảo tỷ lệ khung hình 60 FPS ổn định ngay cả khi hiển thị hàng nghìn điểm dữ liệu.",
        ],
    },
]

CH4_QA_AND_SECURITY_FULL_REPORT_SECTIONS = [
    {
        "code": "4.9.",
        "title": "KẾT QUẢ KIỂM ĐỊNH CHẤT LƯỢNG & KIỂM TOÁN BẢO MẬT TOÀN DIỆN HỆ THỐNG AGROFORECAST",
        "subsections": [
            {
                "code": "4.9.1.",
                "title": "Tóm tắt kết quả kiểm định tổng thể (Backend, Frontend, Coverage, E2E & Bảo mật)",
                "paragraphs": [
                    "Quá trình kiểm thử và kiểm toán bảo mật hệ thống AgroForecast được thực hiện khép kín và độc lập trên cả hai phân hệ Backend (FastAPI, Python 3.11, PostgreSQL) và Frontend (Next.js 14, React 18, TypeScript, Syncfusion EJ2) nhằm bảo đảm độ tin cậy chức năng tuyệt đối, độ phủ mã nguồn ở mức rất cao và năng lực phòng thủ chủ động trước các rủi ro an toàn thông tin mạng phổ biến. Toàn bộ các chỉ số kiểm định đều được đo đạc, ghi nhận khách quan và xác minh lại sau khi áp dụng đầy đủ các bản vá bảo mật chuẩn công nghiệp.",
                    "Bảng 4.4 tổng hợp kết quả đối chiếu giữa trạng thái ban đầu (Trước khi xử lý) và trạng thái nghiệm thu kỹ thuật cuối cùng (Sau khi hoàn thiện & vá bảo mật). Kết quả khẳng định hệ thống AgroForecast đã đạt và vượt toàn bộ các tiêu chuẩn kiểm định khắt khe nhất của ngành kỹ thuật phần mềm.",
                ],
                "tables": [
                    {
                        "caption": "Bảng 4.4. Tóm tắt kết quả kiểm định chất lượng phần mềm và kiểm toán bảo mật hệ thống AgroForecast",
                        "headers": ["Hạng mục kiểm định", "Trước khi xử lý (Baseline)", "Sau khi hoàn thiện & vá", "Đánh giá nghiệm thu"],
                        "rows": [
                            ["Kiểm thử tự động Backend (pytest)", "105 kịch bản PASS", "121 / 121 PASS (100,57s)", "ĐẠT (100%)"],
                            ["Độ phủ mã nguồn Backend (pytest-cov)", "83% (377 dòng chưa phủ)", "98% (2.194 / 2.247 statements)", "ĐẠT (Xuất sắc)"],
                            ["Kiểm thử đơn vị & Build Frontend", "Kiểm tra cơ bản", "3/3 Unit PASS • 0 lỗi TS/Lint • 17/17 routes build", "ĐẠT"],
                            ["Kiểm thử E2E trình duyệt (Playwright)", "Phát hiện 1 lỗi RBAC ở pha RED", "4 / 4 PASS (28,67s) • 0 lỗi Console/Runtime", "ĐẠT"],
                            ["Quét mã nguồn tĩnh Backend (Bandit -ll)", "3 Medium (1 B104, 2 B614)", "0 lỗi (No issues identified)", "SẠCH (100%)"],
                            ["Quét lỗ hổng thư viện Python (pip-audit)", "100 CVEs trên 12 gói", "0 CVEs (No known vulnerabilities)", "SẠCH (Tuyệt đối)"],
                            ["Quét lỗ hổng thư viện Node.js (npm audit)", "14 lỗ hổng (1 Crit, 6 High, 7 Mod)", "6 cảnh báo tồn dư (vá 8/8 non-breaking; đã giảm thiểu)", "GIẢM THIỂU"],
                            ["Kiểm toán Bí mật & TLS (git ls-files)", "Khóa mặc định + 10 điểm verify=False", "0 điểm vi phạm (CSPRNG 256-bit, verify=True 100%)", "SẠCH (100%)"],
                        ],
                    }
                ],
            },
            {
                "code": "4.9.2.",
                "title": "Phương pháp và quy trình kiểm định kết hợp các Agent Skills chuyên sâu",
                "paragraphs": [
                    "Để tránh tình trạng kiểm thử hình thức hoặc bỏ sót các lỗi logic nghiệp vụ biên (Edge Cases), quy trình kiểm định chất lượng và an ninh mạng của dự án kết hợp trực tiếp giữa bộ công cụ kiểm thử thực chiến và các quy trình Agent Skills chuyên sâu được cài đặt chuẩn mực:",
                    "1. Nhóm quy trình Kiểm thử phần mềm (Testing Skills): (a) Áp dụng skill coverage-analysis để quét và phân tích cây phân nhánh luồng lệnh, truy tìm chính xác từng dòng mã nghiệp vụ chưa được bao phủ; (b) Áp dụng mô hình Test-Driven Development (TDD) theo chu trình RED-GREEN-REFACTOR: viết kịch bản kiểm thử tái hiện chính xác lỗi trước khi sửa, sau đó viết mã khắc phục và xác nhận trạng thái chuyển xanh; (c) Áp dụng skill webapp-testing để tự động hóa toàn bộ luồng thao tác của người dùng cuối trên trình duyệt thực Headless Chrome qua Playwright; và (d) Thực thi quy trình verification-before-completion bắt buộc chạy lại toàn bộ lệnh kiểm thử thực tế trên hệ thống đang chạy trước khi nghiệm thu.",
                    "2. Nhóm quy trình Kiểm toán Bảo mật (Security Skills): (a) Áp dụng quy trình audit-context-building nhằm lập bản đồ toàn diện bề mặt tấn công của hệ thống (bao gồm cơ chế cấp phát và kiểm tra JWT, ma trận phân quyền RBAC, kiểm tra biên tham số REST API, quy trình nhập/xuất CSV và các đường ống Bot cào dữ liệu); (b) Ứng dụng skill cvss-scoring để định lượng mức độ nghiêm trọng của từng lỗ hổng theo chuẩn quốc tế CVSS v3.1 (kèm vector tham chiếu CVSS v4.0); (c) Áp dụng systematic-debugging và differential-review nhằm rà soát chéo các thay đổi mã nguồn, đảm bảo mọi bản vá bảo mật không gây ra hồi quy logic hoặc tạo ra các lỗ hổng phụ phát sinh.",
                ],
            },
            {
                "code": "4.9.3.",
                "title": "Chi tiết kết quả kiểm thử hệ thống đa tầng (128 / 128 kịch bản PASS)",
                "paragraphs": [
                    "Tổng cộng 128 kịch bản kiểm thử tự động trên toàn hệ thống đã vượt qua 100% sau bản vá bảo mật cuối cùng (bao gồm 120 kịch bản chức năng & phủ nhánh ở đợt kiểm thử chính, bổ sung thêm 1 kịch bản hồi quy bảo mật toàn diện ở đợt kiểm toán, cùng 3 kiểm thử đơn vị Frontend và 4 luồng kiểm thử E2E trình duyệt thật).",
                    "Bảng 4.5 tổng hợp phân bổ kết quả kiểm thử trên 4 tầng kiến trúc phần mềm của AgroForecast.",
                ],
                "tables": [
                    {
                        "caption": "Bảng 4.5. Phân bổ kết quả kiểm định chất lượng phần mềm đa tầng của hệ thống AgroForecast",
                        "headers": ["Tầng kiểm thử", "Công cụ & Tập kiểm thử", "Kết quả xác minh", "Ghi chú kỹ thuật"],
                        "rows": [
                            ["Backend Unit & API Integration", "pytest -v (bao gồm test_coverage_gaps.py, test_regional_pricing.py, test_security_phase7.py)", "121 / 121 PASS (100,57s)", "Bao gồm test hồi quy RBAC, Alerts, SSRF, Secret và ML No Data Leakage"],
                            ["Frontend Unit Tests", "node --test (src/lib/__tests__/formatters.test.mjs)", "3 / 3 PASS", "Kiểm chứng logic định dạng tiền tệ, ngày tháng và tiện ích xử lý dữ liệu giao diện"],
                            ["Frontend Type, Lint & Production Build", "npx tsc --noEmit, next lint, next build", "0 lỗi • 0 cảnh báo", "Đóng gói thành công toàn bộ 17 / 17 tuyến trang (routes) tĩnh và động"],
                            ["End-to-End (E2E) Trình duyệt thật", "Playwright (e2e/test_agroforecast_e2e.py) trên Headless Chrome", "4 / 4 PASS (28,67s)", "0 lỗi Console, 0 lỗi Runtime, 0 xuất hiện banner bản quyền Syncfusion"],
                        ],
                    }
                ],
            },
            {
                "code": "4.9.4.",
                "title": "Phân tích nâng cao độ phủ mã nguồn Backend (tăng từ 83% lên 98%)",
                "paragraphs": [
                    "Từ mức nền độ phủ 83% (với 105 kịch bản ban đầu, còn 377 dòng lệnh chưa được thực thi), nhóm nghiên cứu đã xây dựng bổ sung 15 kịch bản kiểm thử chuyên sâu trong tệp backend/tests/test_coverage_gaps.py. Các kịch bản này tập trung vào các nhánh xử lý ngoại lệ phức tạp, các điều kiện biên của thuật toán và các tình huống lỗi mạng/cơ sở dữ liệu, nâng tổng độ phủ toàn bộ gói backend/app/ lên mức kỷ lục 98% (2.194 / 2.247 statements).",
                    "Chỉ còn 53 dòng lệnh (chiếm 2% tổng số dòng) chưa được kích hoạt, đây là các nhánh mã đặc thù chỉ chạy trong môi trường cơ sở dữ liệu PostgreSQL vật lý của máy chủ cụm (như khóa pg_advisory_xact_lock, khối mã migration nâng cấp schema tự động và điểm khởi chạy tiến trình ASGI uvicorn). Bảng 4.6 trình bày chi tiết độ phủ theo từng mô-đun chức năng.",
                ],
                "tables": [
                    {
                        "caption": "Bảng 4.6. Bảng phân tích chi tiết độ phủ mã nguồn Backend theo từng nhóm mô-đun (pytest-cov)",
                        "headers": ["Nhóm / Mô-đun mã nguồn", "Baseline (Trước)", "Sau tối ưu", "Các nhánh nghiệp vụ & biên lỗi đã bao phủ bổ sung"],
                        "rows": [
                            ["auth.py, deps.py, security.py", "—", "100%", "Rate limit 429 cho /login & /register, JWT thiếu sub (401), user đã xóa (404), hạ cấp an toàn get_optional_current_user, hash Bcrypt hỏng, chống CSV Formula Injection."],
                            ["schemas.py, market.py, regions.py, commodities.py", "—", "100%", "CRUD nông sản (400/404), đủ 6 luật kiểm tra hợp lệ PriceCreateManual, chuẩn hóa tài khoản _disabled, fallback mã tỉnh lạ, định giá theo vùng."],
                            ["admin.py", "72%", "96%", "Xác minh giá & ghi nhận Audit Log (UPDATED / DELETED), Import CSV (mã hóa latin-1, báo lỗi từng dòng), Export CSV an toàn."],
                            ["alert_service.py", "77%", "99%", "Đánh giá quy tắc PCT_INC_7D / PCT_DEC_7D, bỏ qua mặt hàng chưa có giá, lọc quyền xem user vs admin, nhánh gửi SMTP thành công & bắt lỗi mạng."],
                            ["training_service.py", "78%", "99%", "Cô lập lỗi theo từng mô hình (PARTIAL / FAILED), chặn tràn số >= 10^12, tự động cập nhật active_model tối ưu."],
                            ["history_service.py", "83%", "100%", "Xử lý chuỗi thời gian periodic / irregular, chuỗi khảo sát trực tiếp >= 5 phiên trên /overview và /history."],
                            ["predictions.py", "64%", "100%", "Các endpoint /readiness, /training-runs/{id}, /sources, /spotlight và run_job('retrain')."],
                            ["scheduler.py", "26%", "100%", "Vòng đời khởi tạo/dừng APScheduler, cùng kiểm thử upgrade_existing_schema(), /health trạng thái degraded và global_exception_handler."],
                        ],
                    }
                ],
            },
            {
                "code": "4.9.5.",
                "title": "Kết quả kiểm thử E2E trên trình duyệt thật (Playwright)",
                "paragraphs": [
                    "Bộ kiểm thử tự động e2e/test_agroforecast_e2e.py được thiết lập để chạy trực tiếp trên môi trường thực tế (Frontend Next.js tại http://localhost:3000 kết nối đồng bộ với Backend FastAPI tại http://127.0.0.1:8000 và PostgreSQL). Bộ kiểm thử mô phỏng toàn bộ hành vi thao tác của người dùng thực tế trên giao diện và theo dõi nhật ký Console để kiểm soát lỗi Runtime.",
                    "Bảng 4.7 trình bày chi tiết kết quả kiểm chứng trên 4 luồng nghiệp vụ người dùng cốt lõi.",
                ],
                "tables": [
                    {
                        "caption": "Bảng 4.7. Danh mục kịch bản kiểm thử End-to-End (E2E) trên trình duyệt thật qua Playwright",
                        "headers": ["Mã kịch bản", "Tuyến kiểm thử", "Nội dung kiểm chứng & Phát hiện thực tế", "Kết quả"],
                        "rows": [
                            ["E2E-01", "/ (Tổng quan)", "Chọn vị trí Khánh Hòa trên thanh điều hướng: xác nhận hiển thị đúng nhãn 'Khảo sát tại Khánh Hòa' đối với Mía đường, nhãn 'Tham chiếu' đối với các mặt hàng còn lại và mở bảng Chênh lệch giá theo tỉnh hôm nay.", "PASS"],
                            ["E2E-02", "/forecast (Dự báo)", "Xác nhận tự động kích hoạt mô hình tốt nhất (★) khi đổi nông sản, chuyển kỳ hạn 7N <-> 30N, chuyển tab Bảng chi tiết dự báo <-> So sánh 5 mô hình kèm rê chuột trực tiếp trên biểu đồ Syncfusion không phát sinh lỗi BaseTooltip.appendChild.", "PASS"],
                            ["E2E-03", "/history, /compare, /alerts", "Kiểm chứng Syncfusion GridComponent và ChartComponent hiển thị đầy đủ dữ liệu, tương tác ổn định và tuyệt đối không xuất hiện banner cảnh báo bản quyền Syncfusion.", "PASS"],
                            ["E2E-04", "/dashboard/* (Phân quyền RBAC)", "Phát hiện lỗi thực tế ở pha TDD RED: Tài khoản Analyst vẫn mở được /dashboard/overview khi truy cập trực tiếp qua URL do layout.tsx cho phép ['admin', 'analyst']. Đã siết chặt điều kiện bảo vệ về user.role !== 'admin', biên dịch lại bản production và xác nhận chặn triệt để ở pha GREEN.", "PASS"],
                        ],
                    }
                ],
            },
            {
                "code": "4.9.6.",
                "title": "Danh sách 9 lỗ hổng bảo mật phát hiện, chấm điểm CVSS v3.1 và giải pháp khắc phục",
                "paragraphs": [
                    "Thông qua hoạt động rà soát toàn diện bề mặt tấn công kết hợp công cụ quét mã tĩnh SAST (Bandit) và quét phụ thuộc SCA (pip-audit, npm audit), nhóm phát triển đã phát hiện và phân loại chính xác 9 phát hiện bảo mật (mã định danh từ SEC-01 đến SEC-09). Toàn bộ các phát hiện đều được lượng hóa theo khung điểm tiêu chuẩn quốc tế CVSS v3.1 và được xử lý triệt để theo thứ tự ưu tiên từ Nghiêm trọng (Critical) đến Trung bình (Medium).",
                    "Bảng 4.8 mô tả chi tiết từng lỗ hổng, vị trí phát hiện, điểm số CVSS v3.1, mã lỗi CWE và biện pháp vá bảo mật đã triển khai thành công.",
                ],
                "tables": [
                    {
                        "caption": "Bảng 4.8. Danh mục 9 lỗ hổng bảo mật được phát hiện, định lượng CVSS v3.1 và biện pháp khắc phục triệt để",
                        "headers": ["Mã phát hiện", "Điểm CVSS v3.1 & CWE", "Mô tả lỗ hổng phát hiện & Vị trí", "Biện pháp vá bảo mật đã triển khai", "Trạng thái"],
                        "rows": [
                            ["SEC-01", "9.8 Critical • CWE-798", "Khóa ký JWT mặc định ví dụ FastAPI vẫn được sử dụng trong config.py, .env.example và .env cục bộ.", "Xoay vòng khóa CSPRNG 256-bit (64 ký tự hex) trong .env; xóa mật khẩu DB & khóa mẫu khỏi mã nguồn; thêm field_validator đối chiếu SHA-256 chặn mọi khóa yếu/mẫu.", "ĐÃ VÁ"],
                            ["SEC-02", "8.6 High • CWE-862, CWE-639", "Các endpoint /api/v1/alerts* bỏ qua kiểm tra chủ sở hữu khi thiếu header Authorization, cho phép khách đọc email cá nhân, sửa/xóa quy tắc người khác và spam gửi email test SMTP.", "Bắt buộc Depends(get_current_user) trên toàn bộ thao tác ghi/xóa/test và áp rate limit 429 tại alerts.py; siết chế độ fail-closed trong alert_service.py; bổ sung headers: getAuthHeaders() trong api.ts.", "ĐÃ VÁ"],
                            ["SEC-08", "8.6 High • CWE-1395", "100 CVEs tồn tại trên 12 thư viện Python (PyJWT, python-jose, ecdsa, urllib3, pillow, certifi, soupsieve...).", "Xóa mã chết app/core/auth.py & app/schemas/user.py; gỡ bỏ python-jose, ecdsa, passlib; nâng cấp toàn bộ 10 gói còn lại trong requirements.txt -> pip-audit đạt 0 CVE.", "ĐÃ VÁ"],
                            ["SEC-04", "7.8 High • CWE-502 (Bandit B614)", "Hai lệnh torch.load() trong predictor.py chưa bật weights_only=True, tiềm ẩn rủi ro giải tuần tự hóa không an toàn (Insecure Deserialization).", "Bật tham số weights_only=True cho cả 2 lệnh torch.load() trong predictor.py; quét lại Bandit trên ml_pipeline đạt 0 lỗi.", "ĐÃ VÁ"],
                            ["SEC-09", "7.0 High • CWE-1395", "14 lỗ hổng phụ thuộc Frontend phát hiện qua npm audit (7 Moderate, 6 High, 1 Critical).", "Chạy npm audit fix xử lý 8/8 lỗi không phá vỡ tương thích (còn 6 cảnh báo gắn với next@14->16 & dev-only eslint-config-next); cấu hình images: { unoptimized: true }, tắt poweredByHeader và bật 6 OWASP Security Headers trong next.config.mjs.", "GIẢM THIỂU"],
                            ["SEC-03", "6.5 Medium • CWE-295", "10 vị trí tắt xác thực chứng chỉ SSL/TLS (verify=False và urllib3.disable_warnings) khi thu thập dữ liệu.", "Gỡ bỏ 100% lệnh verify=False và urllib3.disable_warnings; ép xác thực TLS chuẩn (verify=True) với bộ chứng chỉ certifi mới nhất.", "ĐÃ VÁ"],
                            ["SEC-05", "6.5 Medium • CWE-863", "Chính sách kiểm soát truy cập trên các tuyến quản trị chưa đồng nhất tuyệt đối giữa Backend và Frontend.", "Khóa chặt toàn bộ 20/20 endpoints /api/v1/admin/* trong admin.py bằng require_role(['admin']), đồng bộ 1:1 với lớp bảo vệ Frontend.", "ĐÃ VÁ"],
                            ["SEC-07", "4.8 Medium • CWE-605 (Bandit B104)", "Cấu hình mặc định lắng nghe trên toàn bộ giao diện mạng 0.0.0.0 trong main.py.", "Chuyển địa chỉ lắng nghe mặc định sang 127.0.0.1 với reload=False trong main.py; quét lại Bandit trên backend/app đạt 0 lỗi.", "ĐÃ VÁ"],
                            ["SEC-06", "4.7 Medium • CWE-918, CWE-79", "Nguy cơ SSRF trên bộ thu thập Scraper và rủi ro XSS thông qua chuỗi source_url lưu trữ hiển thị ra giao diện.", "Áp dụng whitelist tên miền & chặn dải IP nội bộ/metadata (127.0.0.1, 169.254.169.254) trong vietnam_real_scrapers.py và specialized_scrapers.py; làm sạch source_url ở observation_scraper.py và chặn giao thức javascript: tại ProvinceComparisonPanel.tsx.", "ĐÃ VÁ"],
                        ],
                    }
                ],
            },
            {
                "code": "4.9.7.",
                "title": "Ma trận đối chiếu các lớp phòng thủ theo chuẩn bảo mật quốc tế OWASP Top 10 (2021)",
                "paragraphs": [
                    "Để mang lại cái nhìn toàn cảnh về khả năng an ninh của ứng dụng, hệ thống đối chiếu toàn bộ các biện pháp kiểm soát kỹ thuật đã xây dựng với 10 nhóm rủi ro an ninh mạng nghiêm trọng nhất theo phân loại OWASP Top 10:2021.",
                    "Toàn bộ các lớp phòng vệ này đã được xác nhận thực tế thông qua kịch bản kiểm thử hồi quy an toàn thông tin test_security_audit_remediations_rbac_alerts_ssrf_and_secret. Bảng 4.9 trình bày chi tiết ma trận đối chiếu.",
                ],
                "tables": [
                    {
                        "caption": "Bảng 4.9. Ma trận đối chiếu các lớp phòng thủ kỹ thuật của AgroForecast theo chuẩn OWASP Top 10 (2021)",
                        "headers": ["Nhóm rủi ro OWASP Top 10 (2021)", "Cơ chế kiểm soát đã triển khai & xác minh thực tế", "Tình trạng"],
                        "rows": [
                            ["A01: Broken Access Control", "Khóa 20/20 endpoints /api/v1/admin/* bằng require_role(['admin']); chặn truy cập trực tiếp /dashboard/* cho Analyst; siết fail-closed chống IDOR trên /api/v1/alerts*; cấu hình CORS whitelist.", "ĐẠT"],
                            ["A02: Cryptographic Failures", "Băm mật khẩu bằng Bcrypt; khóa ký JWT CSPRNG 256-bit lưu ngoài mã nguồn kèm kiểm tra chặn khóa yếu; bắt buộc xác thực chứng chỉ TLS verify=True 100%.", "ĐẠT"],
                            ["A03: Injection", "Truy vấn tham số hóa qua SQLAlchemy ORM chống SQL Injection; lọc chống CSV Formula Injection khi xuất dữ liệu; làm sạch source_url và chặn javascript: URI chống XSS.", "ĐẠT"],
                            ["A04: Insecure Design", "Áp dụng giới hạn tần suất (Rate Limiting trả HTTP 429) cho /login, /register và kiểm thử gửi email cảnh báo SMTP; tách biệt rõ dữ liệu chuẩn và dữ liệu theo vùng.", "ĐẠT"],
                            ["A05: Security Misconfiguration", "Chuyển bind mặc định sang 127.0.0.1 (reload=False); tắt header X-Powered-By; cấu hình 6 OWASP Security Headers tại next.config.mjs; giữ bí mật trong .env / .env.local không đưa lên Git.", "ĐẠT"],
                            ["A06: Vulnerable & Outdated Components", "Backend pip-audit đạt 0 CVE sau khi gỡ gói cũ và nâng cấp toàn bộ thư viện; Frontend npm audit đã vá sạch các gói non-breaking và áp dụng lớp giảm thiểu bù trừ cho 6 cảnh báo tồn dư.", "KIỂM SOÁT"],
                            ["A07: Identification & Authentication Failures", "Xác thực JWT chặt chẽ (từ chối token thiếu sub trả 401, tài khoản bị xóa trả 404, xử lý an toàn hash hỏng, bảo vệ khóa tài khoản người dùng).", "ĐẠT"],
                            ["A08: Software & Data Integrity Failures", "Bật weights_only=True cho toàn bộ lời gọi torch.load(); kiểm tra dữ liệu đầu vào bằng Pydantic (6 luật validate giá); kiểm định chống rò rỉ dữ liệu ML (No Data Leakage).", "ĐẠT"],
                            ["A09: Security Logging & Monitoring", "Ghi nhận đầy đủ nhật ký chỉnh sửa dữ liệu giá (Audit Log: UPDATED / DELETED), nhật ký thu thập dữ liệu (Crawling Logs) và nhật ký cảnh báo phục vụ truy vết sự cố.", "ĐẠT"],
                            ["A10: Server-Side Request Forgery (SSRF)", "Áp dụng danh sách tên miền cho phép (whitelist) và chặn truy cập IP nội bộ/metadata (127.0.0.1, 169.254.169.254) trong các bộ thu thập dữ liệu web.", "ĐẠT"],
                        ],
                    }
                ],
            },
            {
                "code": "4.9.8.",
                "title": "Quản trị rủi ro tồn dư và kết luận nghiệm thu an toàn thông tin",
                "paragraphs": [
                    "Giải trình quản trị rủi ro tồn dư đối với 6 cảnh báo npm audit (SEC-09): Sau khi vá triệt để 8/8 lỗ hổng không gây xung đột tương thích trên Frontend, 6 cảnh báo còn lại xuất phát từ hai nhóm nguyên nhân: (1) Gói eslint-config-next chỉ phục vụ kiểm tra cú pháp ở môi trường lập trình của lập trình viên (devDependencies), hoàn toàn không được đóng gói vào bản biên dịch chạy thực tế của máy chủ sản xuất; và (2) Bản vá yêu cầu nâng cấp nhảy phiên bản lớn từ next@14.2.35 lên Next.js 16 gây phá vỡ tương thích hoàn toàn với React 18 và bộ thư viện Syncfusion EJ2. Để loại trừ bề mặt tấn công mà vẫn giữ vững độ ổn định tuyệt đối của hệ thống, nhóm nghiên cứu đã triển khai các biện pháp kiểm soát bù trừ (compensating controls): bật cấu hình images: { unoptimized: true } nhằm vô hiệu hóa hoàn toàn endpoint xử lý ảnh /_next/image (triệt tiêu nguy cơ tấn công từ chối dịch vụ DoS và thực thi mã từ xa RCE liên quan), đồng thời tắt poweredByHeader và kích hoạt đầy đủ 6 tiêu đề bảo mật OWASP Security Headers trong tệp next.config.mjs.",
                    "Kết luận nghiệm thu: Sau khi hoàn tất toàn bộ các bản vá bảo mật và siết chặt chính sách phân quyền RBAC, hệ thống AgroForecast đã vượt qua kỳ kiểm thử hồi quy toàn diện với 121/121 kiểm thử Backend PASS (độ phủ mã nguồn đạt 98%), 3/3 kiểm thử đơn vị Frontend PASS, 17/17 tuyến trang đóng gói sạch không lỗi và 4/4 luồng kiểm thử E2E Playwright PASS trực tiếp trên trình duyệt thật. Hai dịch vụ Backend (http://127.0.0.1:8000) và Frontend (http://localhost:3000) vận hành hoàn toàn ổn định, đáp ứng trọn vẹn các tiêu chuẩn khắt khe về độ tin cậy phần mềm và an toàn thông tin mạng để trình bày bảo vệ trước Hội đồng chấm khóa luận tốt nghiệp.",
                ],
            },
        ],
    },
]
