# -*- coding: utf-8 -*-
"""
Chương 1: TỔNG QUAN VỀ ĐỀ TÀI NGHIÊN CỨU
"""

CHUONG_1_DATA = {
    "title": "Chương 1: TỔNG QUAN VỀ ĐỀ TÀI NGHIÊN CỨU",
    "sections": [
        {
            "code": "1.1.",
            "title": "Tổng quan về thị trường nông sản Việt Nam và đặc thù giá bán tại vườn/ruộng",
            "subsections": [
                {
                    "code": "1.1.1.",
                    "title": "Đặc điểm hình thành giá nông sản tại hộ sản xuất (Farm-gate Price)",
                    "paragraphs": [
                        "Trong cấu trúc chuỗi giá trị nông sản tại Việt Nam, giá bán tại vườn hoặc tại ruộng (Farm-gate Price) là mức giá giao dịch đầu tiên được thiết lập trực tiếp giữa hộ nông dân sản xuất và thương lái địa phương, đại lý thu mua cấp xã/huyện hoặc hợp tác xã ngay tại địa điểm thu hoạch. Khác với giá xuất khẩu FOB tại cảng biển hay giá bán lẻ tại hệ thống siêu thị đô thị, giá bán tại vườn phản ánh trực tiếp thu nhập thực tế của người nông dân và chịu sự chi phối tức thời của chất lượng nông sản tươi, độ ẩm sau thu hoạch, điều kiện giao thông nội đồng và áp lực nguồn cung cục bộ trong từng đợt thu hoạch rộ.",
                        "Đối với nhóm cây công nghiệp dài ngày tại Tây Nguyên và Đông Nam Bộ như cà phê Robusta (Đắk Lắk, Lâm Đồng, Gia Lai, Đắk Nông), hồ tiêu đen (Gia Lai, Đắk Lắk, Bà Rịa - Vũng Tàu, Bình Phước) và hạt điều thô (Bình Phước, Đồng Nai), nông hộ thường thu hái, phơi sấy sơ bộ tại sân vườn và bán dạng nhân xô hoặc hạt khô cho các đại lý thu mua tại huyện. Mức giá giao dịch tại vườn biến động hàng ngày theo nhịp giá thế giới (sàn London ICE Europe đối với cà phê Robusta, sàn IPC đối với hồ tiêu) kết hợp với tỷ giá ngoại tệ USD/VND và mức cộng/trừ lùi vận chuyển của từng huyện.",
                        "Đối với nhóm cây lương thực và rau củ quả thương phẩm ngắn ngày như lúa IR50404 tại Đồng bằng sông Cửu Long (An Giang, Đồng Tháp, Kiên Giang, Tiền Giang), khoai lang tím Nhật tại Vĩnh Long hay dâu tây và khoai tây tại thành phố Đà Lạt (Lâm Đồng), tính chất thời vụ và độ tươi của sản phẩm đóng vai trò quyết định. Lúa tươi và khoai lang được thương lái đưa ghe hoặc xe tải về cân trực tiếp tại bờ ruộng ngay khi gặt hoặc dỡ củ; trong khi dâu tây và khoai tây Đà Lạt được cắt và phân loại ngay tại nhà vườn ở Phường 7, Phường 8 (Đà Lạt) hoặc huyện Lạc Dương, Đức Trọng, Đơn Dương trước khi đóng thùng vận chuyển đi TP. Hồ Chí Minh và các tỉnh phía Nam.",
                    ],
                },
                {
                    "code": "1.1.2.",
                    "title": "Phân tích cơ chế chênh lệch giá địa phương (Spatial Basis Spread) giữa các huyện chuyên canh",
                    "paragraphs": [
                        "Một sai lầm phổ biến của nhiều hệ thống thông tin thị trường hiện nay là gộp chung giá nông sản theo các vùng địa lý vĩ mô (chẳng hạn chỉ ghi chung là 'vùng Tây Nguyên' hoặc 'vùng Đồng bằng sông Cửu Long'). Trong thực tế giao dịch nông sản Việt Nam, giữa các huyện chuyên canh trong cùng một vùng hoặc giữa các tỉnh lân cận luôn tồn tại một độ lệch giá cơ sở ổn định gọi là Spatial Basis Spread (ký hiệu là Delta_r, tính bằng VNĐ/kg hoặc VNĐ/tấn).",
                        "Độ lệch giá cơ sở Delta_r giữa địa phương r và địa phương tham chiếu chuẩn r_0 được hình thành từ bốn yếu tố kinh tế - kỹ thuật rõ rệt: (1) Chi phí vận chuyển (Logistics Cost) từ vườn/ruộng đến nhà máy chế biến hoặc cảng xuất khẩu; (2) Chất lượng sinh thái và thổ nhưỡng đặc trưng (ví dụ hồ tiêu huyện Châu Đức - Bà Rịa Vũng Tàu có dung trọng hạt lớn và gần cảng Cái Mép nên giá bán tại vườn cao hơn vùng chuẩn Chư Sê - Gia Lai khoảng +1.500 VNĐ/kg; trong khi cà phê huyện Di Linh - Lâm Đồng có độ ẩm cao hơn vào mùa mưa nên thường chiết khấu -800 VNĐ/kg so với vùng chuẩn Cư M'gar - Đắk Lắk); (3) Mật độ đại lý thu mua và hạ tầng thủy lợi/giao thông tại ruộng (ví dụ vùng lúa huyện Tháp Mười - Đồng Tháp có hệ thống kênh rạch thuận lợi cho ghe lớn vào tận ruộng nên giá lúa tươi cao hơn +150 VNĐ/kg); và (4) Thương hiệu chỉ dẫn địa lý (ví dụ dâu tây cắt tại vườn Phường 8 - TP. Đà Lạt có giá cao hơn dâu tây Mộc Châu - Sơn La khoảng 15.000 VNĐ/kg).",
                        "Bảng 1.1 dưới đây tổng hợp chi tiết danh mục 8 loại nông sản chủ lực và 29 địa phương cấp huyện/thị xã/phường bán tại vườn/ruộng được nghiên cứu và mô hình hóa trực tiếp trong hệ thống AgroForecast.",
                    ],
                    "tables": [
                        {
                            "caption": "Bảng 1.1. Danh mục 8 mặt hàng nông sản và 29 địa phương khảo sát giá bán tại vườn/ruộng trong hệ thống AgroForecast",
                            "headers": ["Mã nông sản", "Tên nông sản", "Đơn vị", "Địa phương bán tại vườn / tại ruộng", "Độ lệch giá (Basis Spread)", "Đặc điểm kinh tế - kỹ thuật tại địa phương"],
                            "rows": [
                                ["COFFEE_ROBUSTA", "Cà phê Robusta", "VNĐ/kg", "Huyện Cư M'gar - Đắk Lắk (Tại vườn)", "0 (Mốc chuẩn)", "Giá cà phê nhân xô nông hộ bán trực tiếp tại vườn/sân phơi Cư M'gar"],
                                ["COFFEE_ROBUSTA", "Cà phê Robusta", "VNĐ/kg", "Thị xã Buôn Hồ - Đắk Lắk (Tại vườn)", "-100", "Giá bán tại vườn khu vực Buôn Hồ, Krông Năng"],
                                ["COFFEE_ROBUSTA", "Cà phê Robusta", "VNĐ/kg", "Huyện Di Linh - Lâm Đồng (Tại vườn)", "-800", "Độ ẩm hạt cao hơn vào mùa mưa, trừ lùi chi phí vận chuyển từ vườn"],
                                ["COFFEE_ROBUSTA", "Cà phê Robusta", "VNĐ/kg", "Huyện Chư Prông - Gia Lai (Tại vườn)", "-300", "Chiết khấu khoảng cách vận chuyển về kho chế biến xuất khẩu"],
                                ["COFFEE_ROBUSTA", "Cà phê Robusta", "VNĐ/kg", "Huyện Đắk Mil - Đắk Nông (Tại vườn)", "+200", "Cà phê nhân xô hạt đều, tỷ lệ trên sàng 16 cao tại vườn Đắk Mil"],
                                ["PEPPER_BLACK", "Hồ tiêu đen", "VNĐ/kg", "Huyện Chư Sê - Gia Lai (Tại vườn)", "0 (Mốc chuẩn)", "Giá tiêu đen xô phơi khô tại hộ nông dân vùng trọng điểm Chư Sê"],
                                ["PEPPER_BLACK", "Hồ tiêu đen", "VNĐ/kg", "Huyện Cư Kuin - Đắk Lắk (Tại vườn)", "+200", "Tiêu đen phơi khô tại vườn khu vực Cư Kuin, Ea H'leo"],
                                ["PEPPER_BLACK", "Hồ tiêu đen", "VNĐ/kg", "Huyện Châu Đức - Bà Rịa Vũng Tàu (Tại vườn)", "+1.500", "Hạt tiêu dung trọng cao, gần cụm cảng xuất khẩu Cái Mép - Thị Vải"],
                                ["PEPPER_BLACK", "Hồ tiêu đen", "VNĐ/kg", "Huyện Lộc Ninh - Bình Phước (Tại vườn)", "-500", "Giá tiêu nông hộ bán ra tại vườn khu vực Lộc Ninh, Bù Đốp"],
                                ["PEPPER_BLACK", "Hồ tiêu đen", "VNĐ/kg", "Huyện Đắk Song - Đắk Nông (Tại vườn)", "+100", "Vùng chuyên canh tiêu sản lượng lớn, thương lái thu mua tận vườn"],
                                ["RICE_IR504", "Lúa gạo IR50404", "VNĐ/kg", "Huyện Châu Phú - An Giang (Tại ruộng)", "0 (Mốc chuẩn)", "Giá lúa tươi thương lái cân trực tiếp tại bờ ruộng Châu Phú"],
                                ["RICE_IR504", "Lúa gạo IR50404", "VNĐ/kg", "Huyện Thoại Sơn - An Giang (Tại ruộng)", "+50", "Vùng chuyên canh lúa chất lượng đồng đều, gần cụm nhà máy xay xát"],
                                ["RICE_IR504", "Lúa gạo IR50404", "VNĐ/kg", "Huyện Tháp Mười - Đồng Tháp (Tại ruộng)", "+150", "Thuận lợi vận tải thủy nội địa, ghe thương lái vào tận ruộng"],
                                ["RICE_IR504", "Lúa gạo IR50404", "VNĐ/kg", "Huyện Tân Hiệp - Kiên Giang (Tại ruộng)", "-150", "Chiết khấu cước ghe vận chuyển từ ruộng về cụm kho xay xát trung tâm"],
                                ["RICE_IR504", "Lúa gạo IR50404", "VNĐ/kg", "Huyện Cái Bè - Tiền Giang (Tại ruộng)", "+100", "Gần chợ đầu mối lương thực Bà Đắc, nhu cầu thu mua tại ruộng cao"],
                                ["SUGARCANE", "Mía đường 10 CCS", "VNĐ/tấn", "Huyện Tây Hòa - Phú Yên (Tại ruộng)", "0 (Mốc chuẩn)", "Giá mía nguyên liệu 10 CCS cân trực tiếp tại ruộng Tây Hòa"],
                                ["SUGARCANE", "Mía đường 10 CCS", "VNĐ/tấn", "Huyện Tân Châu - Tây Ninh (Tại ruộng)", "-10.000", "Giá mía nguyên liệu thu mua tại ruộng khu vực Đông Nam Bộ"],
                                ["SUGARCANE", "Mía đường 10 CCS", "VNĐ/tấn", "Thị xã An Khê - Gia Lai (Tại ruộng)", "-8.000", "Trừ lùi cước xe tải vận chuyển từ ruộng đồi về nhà máy đường"],
                                ["SUGARCANE", "Mía đường 10 CCS", "VNĐ/tấn", "Huyện Phụng Hiệp - Hậu Giang (Tại ruộng)", "-15.000", "Chữ đường bình quân thấp hơn do đặc thù đất ngập nước ĐBSCL"],
                                ["STRAWBERRY", "Dâu tây Đà Lạt", "VNĐ/kg", "Phường 8 - TP. Đà Lạt (Tại vườn)", "0 (Mốc chuẩn)", "Giá dâu tây tươi hái và đóng hộp trực tiếp tại nhà vườn Phường 8"],
                                ["STRAWBERRY", "Dâu tây Đà Lạt", "VNĐ/kg", "Huyện Lạc Dương - Lâm Đồng (Tại vườn)", "-3.000", "Giá bán sỉ tại vườn khu vực chân núi Langbiang - Lạc Dương"],
                                ["STRAWBERRY", "Dâu tây Đà Lạt", "VNĐ/kg", "Huyện Mộc Châu - Sơn La (Tại vườn)", "-15.000", "Giá dâu tây thu hoạch tại vườn Mộc Châu vào chính vụ mùa đông"],
                                ["SWEET_POTATO", "Khoai lang tím", "VNĐ/kg", "Huyện Bình Tân - Vĩnh Long (Tại ruộng)", "0 (Mốc chuẩn)", "Giá khoai lang tím Nhật thương lái cân trực tiếp tại ruộng Bình Tân"],
                                ["SWEET_POTATO", "Khoai lang tím", "VNĐ/kg", "Huyện Châu Thành - Đồng Tháp (Tại ruộng)", "-400", "Giá bán tại ruộng khu vực Châu Thành, Lai Vung"],
                                ["SWEET_POTATO", "Khoai lang tím", "VNĐ/kg", "Huyện Châu Thành A - Hậu Giang (Tại ruộng)", "-500", "Chiết khấu chi phí vận chuyển đường thủy về vựa đóng gói xuất khẩu"],
                                ["POTATO", "Khoai tây Đà Lạt", "VNĐ/kg", "Phường 7 (Thái Phiên) - Đà Lạt (Tại vườn)", "0 (Mốc chuẩn)", "Giá khoai tây hồng/vàng Đà Lạt loại 1 thu mua tại vườn Thái Phiên"],
                                ["POTATO", "Khoai tây Đà Lạt", "VNĐ/kg", "Huyện Đức Trọng - Lâm Đồng (Tại vườn)", "-800", "Giá bán tại ruộng/vườn khu vực Liên Nghĩa, Hiệp Thạnh - Đức Trọng"],
                                ["POTATO", "Khoai tây Đà Lạt", "VNĐ/kg", "Huyện Đơn Dương - Lâm Đồng (Tại vườn)", "-1.000", "Giá thu mua tại vườn chuyên canh rau củ Lạc Lâm, Thạnh Mỹ - Đơn Dương"],
                                ["CASHEW_NUT", "Hạt điều thô", "VNĐ/kg", "Huyện Bù Đăng - Bình Phước (Tại vườn)", "0 (Mốc chuẩn)", "Giá hạt điều tươi/phơi ráo nông hộ bán tại vườn Bù Đăng, Phú Riềng"],
                            ],
                        }
                    ],
                },
                {
                    "code": "1.1.3.",
                    "title": "Đặc tả nguồn dữ liệu chính thống tại Việt Nam cho 8 mặt hàng nông sản",
                    "paragraphs": [
                        "Để đảm bảo tính xác thực và giá trị thực tiễn của mô hình học máy, hệ thống AgroForecast không sử dụng dữ liệu ngẫu nhiên hay dữ liệu ngoại suy không rõ nguồn gốc, mà thiết lập danh mục nguồn thu thập chính thức (Source Catalog) được định nghĩa trong mô-đun ml_pipeline/source_catalog.py. Mỗi mặt hàng nông sản được liên kết với cơ quan công bố có thẩm quyền tại Việt Nam, ghi nhận rõ tần suất công bố (daily, irregular hoặc periodic), loại giá (Bán tại hộ / Tại vườn / Tại ruộng) và quy cách thương phẩm.",
                        "Cụ thể, mặt hàng Lúa IR50404, Dâu tây Đà Lạt, Khoai lang tím Vĩnh Long, Khoai tây Đà Lạt và Hạt điều thô được thu thập và đối chiếu từ hệ thống cơ sở dữ liệu giá nông sản của Viện Chính sách và Chiến lược Phát triển Nông nghiệp Nông thôn (AGROINFO - Bộ Nông nghiệp và Phát triển Nông thôn) kết hợp báo cáo giá của Sở Nông nghiệp và Phát triển Nông thôn tỉnh An Giang, Lâm Đồng, Vĩnh Long, Bình Phước. Mặt hàng Cà phê Robusta và Hồ tiêu đen được thu thập từ chuyên trang giá nội địa Tây Nguyên (giacaphe.com, Vinanet) và Hiệp hội Hồ tiêu và Cây gia vị Việt Nam (VPSA). Mặt hàng Mía đường 10 CCS được thu thập theo kỳ báo cáo của Hiệp hội Mía đường Việt Nam (VSSA) và Viện Chiến lược.",
                    ],
                },
            ],
        },
        {
            "code": "1.2.",
            "title": "Phân tích, đánh giá các hướng nghiên cứu trong và ngoài nước",
            "subsections": [
                {
                    "code": "1.2.1.",
                    "title": "Các công trình nghiên cứu ngoài nước về dự báo chuỗi thời gian nông sản",
                    "paragraphs": [
                        "Trên thế giới, bài toán dự báo giá nông sản (Agricultural Commodity Price Forecasting) đã thu hút sự quan tâm lớn của cộng đồng nghiên cứu kinh tế lượng và trí tuệ nhân tạo. Về mặt phương pháp luận, các công trình quốc tế phát triển qua ba thế hệ mô hình chính: (1) Thế hệ các mô hình thống kê tuyến tính cổ điển; (2) Thế hệ các mô hình học máy phi tuyến dựa trên cây quyết định; và (3) Thế hệ các mạng nơ-ron học sâu (Deep Learning) kết hợp phân rã chuỗi thời gian.",
                        "Ở nhóm mô hình thống kê tuyến tính, phương pháp Box-Jenkins với mô hình ARIMA (AutoRegressive Integrated Moving Average) và SARIMA được xem là nền tảng chuẩn mực để mô hình hóa sự phụ thuộc tuyến tính giữa giá hiện tại và các giá trị quá khứ cùng sai số ngẫu nhiên. Năm 2017, nhóm nghiên cứu Taylor và Letham tại Facebook Core Data Science đã công bố mô hình Prophet, cho phép phân rã chuỗi thời gian thành hàm xu thế từng khúc (piecewise linear/logistic trend), chuỗi Fourier biểu diễn tính mùa vụ đa chu kỳ (tuần, tháng, năm) và hiệu ứng ngày lễ. Prophet khắc phục được nhược điểm của ARIMA khi chuỗi giá nông sản bị khuyết dữ liệu vào ngày cuối tuần hoặc có sự dịch chuyển xu thế đột ngột.",
                        "Ở nhóm mô hình học máy phi tuyến và học sâu, các nghiên cứu của Breiman (2001) với Random Forest và Chen & Guestrin (2016) với XGBoost đã chứng minh hiệu quả vượt trội khi chuyển đổi chuỗi thời gian thành bài toán học có giám sát dạng bảng (Tabular Supervised Learning) thông qua các biến trễ (Lag features) và thống kê cửa sổ trượt (Rolling statistics). Đặc biệt, đối với các chuỗi giá có tính phụ thuộc dài hạn phức tạp, kiến trúc mạng nơ-ron hồi quy bộ nhớ dài-ngắn LSTM (Long Short-Term Memory) do Hochreiter và Schmidhuber đề xuất đã giải quyết triệt để hiện tượng triệt tiêu đạo hàm (Vanishing Gradient) của mạng RNN truyền thống, giúp nắm bắt tốt các chu kỳ biến động giá nông sản kéo dài nhiều tuần liên tiếp.",
                    ],
                },
                {
                    "code": "1.2.2.",
                    "title": "Các công trình nghiên cứu trong nước và hệ thống thông tin giá nông sản hiện hành",
                    "paragraphs": [
                        "Tại Việt Nam, trong những năm gần đây đã có một số đề tài nghiên cứu ứng dụng ARIMA hoặc mạng nơ-ron nhân tạo để dự báo giá lúa gạo xuất khẩu hoặc giá cà phê nhân xô Tây Nguyên. Bên cạnh đó, các cổng thông tin điện tử như AGROINFO, Vinanet, Giacaphe hay các bản tin của Sở Nông nghiệp và Phát triển Nông thôn đã thực hiện tốt vai trò cập nhật bảng giá giao dịch hàng ngày hoặc hàng tuần.",
                        "Tuy nhiên, khi khảo sát thực tế các hệ thống thông tin và các đề tài nghiên cứu hiện có trong nước, có thể nhận thấy phần lớn các trang tin chỉ dừng lại ở mức độ thống kê mô tả (hiển thị bảng giá quá khứ và hôm nay) chứ chưa tích hợp công cụ dự báo tương lai bằng học máy. Ngược lại, các nghiên cứu học thuật có chạy mô hình dự báo lại thường hoạt động rời rạc trên môi trường Jupyter Notebook, chỉ khảo sát 1 hoặc 2 mặt hàng, chưa có cơ chế tự động hóa thu thập dữ liệu và chưa xây dựng được giao diện ứng dụng Web hoàn chỉnh phục vụ người dùng cuối.",
                    ],
                },
            ],
        },
        {
            "code": "1.3.",
            "title": "Những vấn đề còn tồn tại của các nghiên cứu và hệ thống hiện có",
            "subsections": [
                {
                    "code": "1.3.1.",
                    "title": "Hạn chế về độ phân giải không gian (thiếu giá bán tại vườn cấp huyện/phường)",
                    "paragraphs": [
                        "Hầu hết các công bố và công cụ hiện nay chỉ đưa ra một mức giá bình quân duy nhất cho cả vùng lớn (ví dụ 'Cà phê Tây Nguyên' hay 'Lúa Đồng bằng sông Cửu Long'). Khi người nông dân tại huyện Di Linh (Lâm Đồng) hay huyện Châu Phú (An Giang) tra cứu, họ không biết được mức giá thực tế bán ra tại vườn/ruộng địa phương mình đang chênh lệch bao nhiêu so với mức bình quân đó và dự báo 7 đến 30 ngày tới tại chính huyện mình sẽ biến động như thế nào.",
                    ],
                },
                {
                    "code": "1.3.2.",
                    "title": "Hạn chế về kiểm soát nguồn gốc dữ liệu (Data Provenance) và rò rỉ dữ liệu kiểm thử",
                    "paragraphs": [
                        "Nhiều hệ thống thử nghiệm trộn lẫn dữ liệu giả lập (mock/synthetic data) với dữ liệu thực tế hoặc không kiểm tra tính liên tục của chuỗi thời gian trước khi huấn luyện. Nghiêm trọng hơn, việc chia tập dữ liệu ngẫu nhiên (Random Shuffle Split) thay vì chia theo thứ tự thời gian (Temporal Holdout Split) dẫn đến hiện tượng rò rỉ dữ liệu tương lai vào quá trình huấn luyện (Data Leakage), làm cho chỉ số đánh giá trong báo cáo rất đẹp nhưng khi dự báo thực tế lại sai lệch lớn.",
                    ],
                },
                {
                    "code": "1.3.3.",
                    "title": "Hạn chế về việc dùng đơn lẻ một thuật toán, thiếu khoảng tin cậy và thiếu kiểm thử bảo mật",
                    "paragraphs": [
                        "Không có một thuật toán học máy duy nhất nào luôn tốt nhất cho mọi loại nông sản (theo định lý No Free Lunch). Thực tế trong dự án này cho thấy ARIMA và XGBoost đạt sai số rất thấp trên chuỗi lúa IR50404 và hồ tiêu đen, trong khi mạng học sâu LSTM lại vượt trội hoàn toàn trên nhóm nông sản đặc sản Đà Lạt (dâu tây, khoai tây) và khoai lang tím. Ngoài ra, các hệ thống hiện tại thường bỏ qua khâu kiểm thử phần mềm tự động và kiểm tra an toàn bảo mật ứng dụng Web theo chuẩn OWASP Top 10.",
                    ],
                },
            ],
        },
        {
            "code": "1.4.",
            "title": "Các vấn đề trọng tâm mà đề tài tập trung nghiên cứu giải quyết",
            "subsections": [
                {
                    "code": "1.4.1.",
                    "title": "Xây dựng đường ống dữ liệu xác thực và đối sánh tự động 5 mô hình học máy",
                    "paragraphs": [
                        "Đề tài giải quyết triệt để bài toán toàn vẹn dữ liệu bằng cách gắn nhãn nguồn gốc (provenance: collected, reviewed, unverified) và mã băm SHA-256 (dataset_hash) cho từng phiên huấn luyện. Hệ thống huấn luyện đồng thời cả 5 mô hình (LSTM, Prophet, ARIMA, XGBoost, Random Forest) trên tập huấn luyện chuẩn hóa, kiểm định trên tập Holdout cuối chuỗi và tự động đề xuất mô hình có RMSE thấp nhất cho người dùng.",
                    ],
                },
                {
                    "code": "1.4.2.",
                    "title": "Mô hình hóa giá bán tại vườn theo địa phương kết hợp giải thích AI (XAI) và bảo mật OWASP",
                    "paragraphs": [
                        "Đề tài tích hợp tầng hiệu chỉnh không gian - thời gian (Spatio-Temporal Basis Spread) cho 29 địa phương cấp huyện/phường, cung cấp dải tin cậy 95% (lowerCI - upperCI), tích hợp mô-đun giải thích mức độ ảnh hưởng của các yếu tố mùa vụ, tỷ giá, thời tiết (Explainable AI) và bảo vệ toàn diện hệ thống bằng 72 kịch bản kiểm thử tự động và kiểm tra thâm nhập bảo mật.",
                    ],
                },
            ],
        },
    ],
}
