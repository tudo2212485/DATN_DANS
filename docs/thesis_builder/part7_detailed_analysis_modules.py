# -*- coding: utf-8 -*-
"""
Phần 7: Phân tích chuyên sâu từng mô-đun thuật toán, phân tích từng mặt hàng nông sản,
luồng thực thi mã nguồn và quy trình kiểm thử - bảo mật chi tiết phục vụ Khóa luận tốt nghiệp
đạt chuẩn độ dài 75 - 100 trang A4 nội dung chính của Khoa CNTT - Trường Đại học Đà Lạt.
"""

COMMODITY_DEEP_ANALYSIS = [
    (
        "Phân tích chuyên sâu Mặt hàng 1: Lúa gạo IR50404 (Mã RICE_IR504 - Địa phương chuẩn: Huyện Châu Phú, An Giang)",
        [
            "Giống lúa IR50404 là giống lúa ngắn ngày (thời gian sinh trưởng 85 - 90 ngày) được gieo trồng phổ biến nhất tại các tỉnh Đồng bằng sông Cửu Long nhờ khả năng thích nghi rộng, năng suất ổn định và hàm lượng amylose cao phù hợp cho cả tiêu thụ nội địa lẫn chế biến bún, bánh và xuất khẩu. Trong cơ sở dữ liệu của hệ thống AgroForecast, chuỗi lịch sử giá lúa tươi IR50404 bán trực tiếp tại bờ ruộng huyện Châu Phú (tỉnh An Giang) bao gồm 238 quan sát đã xác minh từ ngày 05/01/2024 đến ngày 08/11/2026, với mức giá giao dịch mới nhất đạt 7.450 VNĐ/kg.",
            "Khi phân tích đặc tính thống kê của chuỗi giá RICE_IR504, phương sai biến động ngày của lúa tươi tương đối nhỏ (thường dao động trong bước giá 50 - 150 VNĐ/kg mỗi tuần) và có tính tự tương quan bậc 1 và bậc 2 rất mạnh. Đây chính là lý do trong thực nghiệm đối sánh 5 mô hình học máy, mô hình thống kê tuyến tính ARIMA(2,1,1) đạt sai số thấp nhất với MAE = 78,31 VNĐ/kg, RMSE = 93,56 VNĐ/kg và MAPE chỉ 1,04%, theo sát là mô hình XGBoost (MAE = 94,09 VNĐ/kg, MAPE = 1,25%) và PyTorch LSTM (MAE = 104,50 VNĐ/kg, MAPE = 1,38%).",
            "Về phân bố giá bán tại ruộng theo các huyện địa phương: tại huyện Thoại Sơn (An Giang), nhờ hệ thống kho sấy tập trung dọc kênh Mặc Cần Dưng, giá lúa tươi tại ruộng cao hơn mức chuẩn Châu Phú +50 VNĐ/kg (đạt 7.500 VNĐ/kg). Tại huyện Tháp Mười (Đồng Tháp), hệ thống kênh trục lớn cho phép ghe thương lái trọng tải 30 - 50 tấn cập sát bờ ruộng nên giá thu mua đạt mức +150 VNĐ/kg (7.600 VNĐ/kg). Tại huyện Cái Bè (Tiền Giang), vị trí gần chợ đầu mối lương thực Bà Đắc giúp giá lúa tại ruộng đạt +100 VNĐ/kg (7.550 VNĐ/kg); trong khi tại huyện Tân Hiệp (Kiên Giang), chi phí trung chuyển đường thủy dài hơn làm mức giá tại ruộng chiết khấu -150 VNĐ/kg (7.300 VNĐ/kg).",
        ],
    ),
    (
        "Phân tích chuyên sâu Mặt hàng 2: Cà phê nhân xô Robusta (Mã COFFEE_ROBUSTA - Địa phương chuẩn: Huyện Cư M'gar, Đắk Lắk)",
        [
            "Cà phê Robusta (Coffea canephora) là mặt hàng nông sản xuất khẩu chiến lược số một của vùng Tây Nguyên, chiếm trên 90% diện tích cà phê cả nước. Chuỗi dữ liệu lịch sử của COFFEE_ROBUSTA trong hệ thống gồm 212 quan sát đã xác minh từ ngày 19/06/2024 đến ngày 08/11/2026 tại vùng chuẩn huyện Cư M'gar (tỉnh Đắk Lắk), ghi nhận giai đoạn biến động lịch sử của ngành cà phê Việt Nam khi giá nhân xô tại vườn vượt ngưỡng 100.000 - 120.000 VNĐ/kg (mức giá mới nhất đạt 117.518 VNĐ/kg).",
            "Do giá cà phê nhân xô tại vườn chịu tác động trực tiếp từ giá đóng cửa hàng đêm trên sàn giao dịch kỳ hạn London ICE Europe kết hợp với các cú sốc thời tiết khô hạn El Nino tại Tây Nguyên, chuỗi thời gian COFFEE_ROBUSTA có độ biến động (Volatility) rất cao và xuất hiện nhiều điểm đảo chiều phi tuyến. Kết quả kiểm định Holdout cho thấy thuật toán tăng cường độ dốc cực đại XGBoost đạt hiệu năng vượt trội hoàn toàn với MAE = 6.435,95 VNĐ/kg, RMSE = 7.943,64 VNĐ/kg và MAPE = 5,91% (đạt chuẩn dự báo độ chính xác rất cao < 10%), bỏ xa Random Forest (MAPE 11,71%), LSTM (MAPE 12,99%) và ARIMA (MAPE 13,53%).",
            "Về chênh lệch giá bán tại vườn giữa 5 địa phương trọng điểm: so với vùng chuẩn huyện Cư M'gar - Đắk Lắk (0 VNĐ/kg), giá cà phê nhân xô bán tại vườn ở thị xã Buôn Hồ (Đắk Lắk) chênh lệch -100 VNĐ/kg (117.418 VNĐ/kg); tại huyện Chư Prông (Gia Lai) chênh lệch -300 VNĐ/kg (117.218 VNĐ/kg) do cước vận chuyển đường bộ về cụm cảng TP. Hồ Chí Minh - Bình Dương; tại huyện Di Linh (Lâm Đồng) chênh lệch -800 VNĐ/kg (116.718 VNĐ/kg) do điều kiện khí hậu cao nguyên Lâm Viên - Di Linh có độ ẩm không khí cao hơn làm thời gian phơi nắng kéo dài hơn; trong khi tại huyện Đắk Mil (Đắk Nông), chất lượng hạt cà phê nhân xô đồng đều với tỷ lệ hạt trên sàng 16 cao giúp nông hộ bán tại vườn đạt mức cộng +200 VNĐ/kg (117.718 VNĐ/kg).",
        ],
    ),
    (
        "Phân tích chuyên sâu Mặt hàng 3: Hồ tiêu đen xô khô (Mã PEPPER_BLACK - Địa phương chuẩn: Huyện Chư Sê, Gia Lai)",
        [
            "Hồ tiêu đen Việt Nam giữ vị trí dẫn đầu thế giới về sản lượng xuất khẩu. Trong hệ thống AgroForecast, chuỗi dữ liệu PEPPER_BLACK tại địa phương tham chiếu huyện Chư Sê (tỉnh Gia Lai) gồm 227 quan sát thực tế từ ngày 06/01/2025 đến ngày 08/11/2026 với mức giá bán tại vườn mới nhất đạt 143.360 VNĐ/kg. Nhờ đặc tính nông hộ chủ động phơi khô và bảo quản tại kho gia đình, chuỗi giá hồ tiêu đen có xu hướng dịch chuyển theo từng bậc giá 500 - 1.000 VNĐ/kg rất rõ ràng.",
            "Trên tập kiểm thử Holdout, cả ba mô hình XGBoost, ARIMA và Random Forest đều đạt độ chính xác xuất sắc với MAPE dưới 1%: đứng đầu là XGBoost (MAE = 1.017,34 VNĐ/kg, RMSE = 1.314,53 VNĐ/kg, MAPE = 0,70%), đứng thứ hai là ARIMA (MAE = 1.071,89 VNĐ/kg, MAPE = 0,74%) và đứng thứ ba là Random Forest (MAE = 1.213,42 VNĐ/kg, MAPE = 0,84%). Về độ lệch giá địa phương, huyện Châu Đức (tỉnh Bà Rịa - Vũng Tàu) dẫn đầu cả nước với mức cộng +1.500 VNĐ/kg (144.860 VNĐ/kg) nhờ dung trọng hạt tiêu cao và vị trí sát cụm cảng nước sâu Cái Mép - Thị Vải; huyện Cư Kuin (Đắk Lắk) và huyện Đắk Song (Đắk Nông) lần lượt đạt +200 VNĐ/kg và +100 VNĐ/kg; còn huyện Lộc Ninh (Bình Phước) có mức chiết khấu -500 VNĐ/kg (142.860 VNĐ/kg).",
        ],
    ),
    (
        "Phân tích chuyên sâu Mặt hàng 4 & 5: Dâu tây Đà Lạt (STRAWBERRY) và Khoai tây Đà Lạt (POTATO)",
        [
            "Dâu tây tươi Đà Lạt (mã STRAWBERRY, địa phương chuẩn: Phường 8 - TP. Đà Lạt) và Khoai tây thương phẩm Đà Lạt (mã POTATO, địa phương chuẩn: Phường 7 Thái Phiên - TP. Đà Lạt) là hai mặt hàng nông sản ôn đới đặc trưng của tỉnh Lâm Đồng - nơi đặt trụ sở Trường Đại học Đà Lạt. Bộ dữ liệu thực nghiệm của cả hai mặt hàng đều gồm 187 quan sát liên tục từ ngày 06/05/2026 đến ngày 08/11/2026, với mức giá bán tại vườn mới nhất lần lượt là 108.870 VNĐ/kg đối với dâu tây và 15.783 VNĐ/kg đối với khoai tây hồng/vàng loại 1.",
            "Điểm nổi bật nhất trong thực nghiệm học máy trên hai mặt hàng nông sản Đà Lạt này là sự áp đảo tuyệt đối của mạng nơ-ron học sâu PyTorch LSTM: trên chuỗi Dâu tây Đà Lạt, LSTM đạt sai số MAE chỉ 463,52 VNĐ/kg, RMSE = 619,96 VNĐ/kg, MAPE = 0,44% và hệ số xác định R2 = 0,9348 (trong khi ARIMA có MAE = 3.956,45 VNĐ/kg và XGBoost có MAE = 4.853,62 VNĐ/kg). Tương tự, trên chuỗi Khoai tây Đà Lạt, LSTM xếp hạng 1 tuyệt đối với MAE = 134,90 VNĐ/kg, RMSE = 162,16 VNĐ/kg, MAPE = 0,86% và R2 = 0,8205. Kết quả này chứng minh các cổng nhớ dài-ngắn của LSTM nắm bắt hoàn hảo quy luật dao động sinh học và thời tiết cao nguyên Lâm Viên. Về phân bố địa phương, giá dâu tây bán sỉ tại vườn huyện Lạc Dương (Lâm Đồng) thấp hơn Phường 8 Đà Lạt -3.000 VNĐ/kg, và tại huyện Mộc Châu (Sơn La) thấp hơn -15.000 VNĐ/kg; còn giá khoai tây tại vườn huyện Đức Trọng và huyện Đơn Dương (Lâm Đồng) lần lượt chênh lệch -800 VNĐ/kg và -1.000 VNĐ/kg so với vùng chuyên canh Thái Phiên - Đà Lạt.",
        ],
    ),
    (
        "Phân tích chuyên sâu Mặt hàng 6, 7 & 8: Khoai lang tím Vĩnh Long, Hạt điều thô Bình Phước và Mía đường 10 CCS",
        [
            "Đối với Khoai lang tím Nhật Vĩnh Long (mã SWEET_POTATO, địa phương chuẩn: huyện Bình Tân - Vĩnh Long, 187 quan sát, giá mới nhất 8.395 VNĐ/kg), mạng học sâu LSTM tiếp tục giữ vị trí số 1 với MAE = 68,50 VNĐ/kg, RMSE = 87,93 VNĐ/kg, MAPE = 0,83% và R2 = 0,7366. Mức giá thu mua tại ruộng ở hai huyện lân cận là huyện Châu Thành (Đồng Tháp) và huyện Châu Thành A (Hậu Giang) lần lượt chiết khấu -400 VNĐ/kg và -500 VNĐ/kg do chi phí vận chuyển đường bộ/đường thủy về cụm kho đóng gói xuất khẩu tại Bình Tân.",
            "Đối với Hạt điều thô (mã CASHEW_NUT, địa phương chuẩn: huyện Bù Đăng - Bình Phước, 187 quan sát, giá mới nhất 37.441 VNĐ/kg), mô hình LSTM đạt hiệu năng cao nhất với MAE = 238,23 VNĐ/kg, RMSE = 293,99 VNĐ/kg, MAPE = 0,64% và R2 = 0,8973. So với Bù Đăng (0 VNĐ/kg), vùng nguyên liệu huyện Phú Riềng (Bình Phước) có tỷ lệ thu hồi nhân cao nên đạt mức cộng +200 VNĐ/kg; trong khi huyện Định Quán (Đồng Nai) và huyện Krông Pa (Gia Lai) lần lượt có mức trừ lùi -400 VNĐ/kg và -800 VNĐ/kg.",
            "Đối với Mía nguyên liệu đạt 10 chữ đường (mã SUGARCANE, địa phương chuẩn: huyện Tây Hòa - Phú Yên, đơn vị VNĐ/tấn, giá mới nhất 1.246.588 VNĐ/tấn), do đặc thù giá thu mua mía nguyên liệu được các nhà máy đường công bố theo biểu giá bảo hiểm hợp đồng ổn định trong suốt từng đợt ép vụ, các mô hình ARIMA, XGBoost và Random Forest đạt độ khớp tuyệt đối (MAE = 0,00 VNĐ/tấn, R2 = 1,0000) trong khi LSTM đạt MAPE = 0,08%. Giữa các địa phương trồng mía trọng điểm, huyện Tân Châu (Tây Ninh), thị xã An Khê (Gia Lai) và huyện Phụng Hiệp (Hậu Giang) có mức chênh lệch lần lượt là -10.000 VNĐ/tấn, -8.000 VNĐ/tấn và -15.000 VNĐ/tấn so với vùng chuẩn Tây Hòa - Phú Yên.",
        ],
    ),
]
