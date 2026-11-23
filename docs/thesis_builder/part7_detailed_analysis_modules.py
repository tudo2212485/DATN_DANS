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
            "Giống lúa IR50404 là giống lúa ngắn ngày (thời gian sinh trưởng 85 - 90 ngày) được gieo trồng phổ biến nhất tại các tỉnh Đồng bằng sông Cửu Long nhờ khả năng thích nghi rộng, năng suất ổn định và hàm lượng amylose cao phù hợp cho cả tiêu thụ nội địa lẫn chế biến bún, bánh và xuất khẩu. Trong cơ sở dữ liệu của hệ thống AgroForecast (chốt mốc 23/11/2026), chuỗi lịch sử giá lúa tươi IR50404 bán trực tiếp tại bờ ruộng tỉnh An Giang & ĐBSCL bao gồm 442 quan sát đã xác minh từ ngày 01/01/2024 đến ngày 23/11/2026 (100% có đường dẫn bài báo/bản tin VFA gốc kiểm chứng, cộng 1.101 quan sát cấp tỉnh tại 7 tỉnh ĐBSCL), với mức giá giao dịch mới nhất đạt 6.850 VNĐ/kg.",
            "Khi phân tích đặc tính thống kê của chuỗi giá RICE_IR504, phương sai biến động ngày của lúa tươi tương đối nhỏ và có tính tự tương quan bậc 1–2 rất mạnh. Trong thực nghiệm đối sánh Walk-Forward 7 ngày của 5 mô hình học máy, mô hình thống kê ARIMA đạt sai số MAPE thấp nhất là 1,58% (MAE = 100,24 VNĐ/kg, RMSE = 169,20 VNĐ/kg, R2 = 0,5340, PICP 95% = 89,39%), theo sát là Facebook Prophet (MAE = 100,13 VNĐ/kg, RMSE thấp nhất 156,67 VNĐ/kg, MAPE = 1,59%, R2 = 0,6005) và XGBoost (MAPE = 1,65%).",
            "Về phân bố giá bán tại ruộng theo các địa phương ĐBSCL: tại huyện Thoại Sơn (An Giang) giá cao hơn mức chuẩn Châu Phú +50 VNĐ/kg; tại huyện Tháp Mười (Đồng Tháp) đạt +150 VNĐ/kg nhờ thuận lợi vận tải thủy nội địa; tại huyện Cái Bè (Tiền Giang) đạt +100 VNĐ/kg; trong khi tại huyện Tân Hiệp (Kiên Giang) chiết khấu -150 VNĐ/kg do cước ghe trung chuyển xa hơn.",
        ],
    ),
    (
        "Phân tích chuyên sâu Mặt hàng 2: Cà phê nhân xô Robusta (Mã COFFEE_ROBUSTA - Địa phương chuẩn: Huyện Cư M'gar, Đắk Lắk)",
        [
            "Cà phê Robusta (Coffea canephora) là mặt hàng nông sản xuất khẩu chiến lược số một của vùng Tây Nguyên, chiếm trên 90% diện tích cà phê cả nước. Chuỗi dữ liệu lịch sử của COFFEE_ROBUSTA trong hệ thống gồm 919 quan sát đã xác minh từ ngày 04/01/2024 đến ngày 23/11/2026 (919 bài báo kiểm chứng độc lập trên vietnambiz.vn & giacaphe.com cùng 3.485 quan sát khảo sát 4 tỉnh Tây Nguyên), ghi nhận trọn vẹn chu kỳ biến động lịch sử từ đỉnh 135.200 VNĐ/kg về vùng điều chỉnh cuối năm 2026 ở mức 71.700 VNĐ/kg.",
            "Do giá cà phê nhân xô tại vườn chịu tác động trực tiếp từ sàn kỳ hạn London ICE Europe, tỷ giá USD/VND và chi phí năng lượng/vận tải, việc bổ sung 2 biến ngoại sinh nhân quả (USD/VND và Dầu thô WTI <= t-1) giúp mạng học sâu PyTorch Stacked LSTM (7 kênh nhân quả) xuất sắc đạt Hạng 1 tuyệt đối trên kiểm định Walk-Forward 7 ngày với MAE = 1.555,41 VNĐ/kg, RMSE = 1.978,28 VNĐ/kg, MAPE = 1,79%, R2 = 0,8972 và PICP 95% = 92,22%, vượt trội rõ rệt so với ARIMA (MAPE = 1,86%), Random Forest (RMSE = 2.087,40, MAPE = 1,90%) và Naive Baseline (MAPE = 1,88%, RMSE = 2.147,01 VNĐ/kg).",
            "Về chênh lệch giá bán tại vườn giữa các tỉnh/huyện Tây Nguyên: hệ thống đồng bộ trực tiếp bảng giá từng ngày tại Đắk Lắk, Lâm Đồng, Gia Lai, Đắk Nông và áp dụng định mức độ lệch cấp huyện (-100 đ/kg tại Buôn Hồ, -300 đ/kg tại Chư Prông, -800 đ/kg tại Di Linh và +200 đ/kg tại Đắk Mil).",
        ],
    ),
    (
        "Phân tích chuyên sâu Mặt hàng 3: Hồ tiêu đen xô khô (Mã PEPPER_BLACK - Địa phương chuẩn: Huyện Chư Sê, Gia Lai)",
        [
            "Hồ tiêu đen Việt Nam giữ vị trí dẫn đầu thế giới về sản lượng xuất khẩu. Trong hệ thống AgroForecast, chuỗi dữ liệu PEPPER_BLACK gồm 793 quan sát thực tế từ ngày 04/01/2024 đến ngày 23/11/2026 (793 bài báo gốc vietnambiz.vn và 4.446 quan sát khảo sát trực tiếp tại 6 tỉnh trọng điểm), dao động trong biên độ 77.800 – 169.200 VNĐ/kg với mức giá mới nhất ngày 23/11/2026 đạt 129.100 VNĐ/kg.",
            "Trên tập kiểm thử Walk-Forward 7 ngày (90 phiên cuối), cả 5 mô hình đều đạt sai số MAPE xuất sắc dưới 0,90%: đứng đầu về MAPE là ARIMA (MAE = 990,46 VNĐ/kg, RMSE = 1.643,77 VNĐ/kg, MAPE = 0,74%, PICP 95% = 94,44%, vượt Baseline RMSE 1.646,34 VNĐ/kg), đứng thứ hai là XGBoost (MAE = 1.045,64 VNĐ/kg, MAPE = 0,78%) và đứng thứ ba là Random Forest (RMSE thấp nhất 1.631,93 VNĐ/kg, MAPE = 0,78%, R2 = 0,3353). Về chênh lệch địa phương, Bà Rịa - Vũng Tàu (Châu Đức) luôn cao hơn vùng chuẩn do dung trọng hạt lớn và gần cụm cảng Cái Mép - Thị Vải.",
        ],
    ),
    (
        "Phân tích chuyên sâu Mặt hàng 4 & 5: Dâu tây Đà Lạt (STRAWBERRY) và Khoai tây Đà Lạt (POTATO)",
        [
            "Dâu tây tươi Đà Lạt (mã STRAWBERRY, địa phương chuẩn: Phường 8 - TP. Đà Lạt) và Khoai tây thương phẩm Đà Lạt (mã POTATO, địa phương chuẩn: Phường 7 Thái Phiên - TP. Đà Lạt) là hai mặt hàng nông sản ôn đới đặc trưng của tỉnh Lâm Đồng - nơi đặt trụ sở Trường Đại học Đà Lạt. Do thị trường rau củ quả nội địa không niêm yết giá hằng ngày nhiều năm, bộ dữ liệu thực nghiệm của cả hai mặt hàng gồm 504 phiên (21/11/2024 – 23/11/2026) neo giá khảo sát sống tại Việt Nam (kamereo.vn 100.000 VNĐ/kg cho dâu tây Đà Lạt; vựa namtinhvegetable.com Lâm Đồng 20.000 VNĐ/kg cho khoai tây hồng Đà Lạt) kết hợp chuỗi tham chiếu Proxy Index ETF nông sản thực tế Yahoo Finance (DBA x USD/VND và MOO x USD/VND), hiển thị nhãn minh bạch trên /history.",
            "Trên kiểm định Walk-Forward 7 ngày, mô hình Facebook Prophet đạt hiệu năng cao nhất trên cả hai mặt hàng ôn đới nhờ nắm bắt tốt nhịp điệu mùa vụ: trên Dâu tây Đà Lạt đạt MAE = 1.164,79 VNĐ/kg, RMSE = 1.610,18 VNĐ/kg, MAPE = 1,08%, R2 = 0,8693 (PICP 95% = 100%, vượt sâu Naive Baseline 1,30%); trên Khoai tây Đà Lạt đạt MAE = 276,05 VNĐ/kg, RMSE = 368,60 VNĐ/kg, MAPE = 1,30%, R2 = 0,7119 (PICP 95% = 100%, vượt Naive Baseline 1,39%). Cả 5 mô hình đều đạt MAPE thấp từ 1,08% đến 1,60%.",
        ],
    ),
    (
        "Phân tích chuyên sâu Mặt hàng 6, 7 & 8: Khoai lang tím Vĩnh Long, Hạt điều thô Bình Phước và Mía đường 10 CCS",
        [
            "Đối với Khoai lang tím Nhật Vĩnh Long (mã SWEET_POTATO, địa phương chuẩn: huyện Bình Tân - Vĩnh Long, 504 phiên từ 21/11/2024 – 23/11/2026, neo giá khảo sát sống tại banggianongsan.com 16.000 VNĐ/kg kết hợp chuỗi tham chiếu Proxy Index ETF Yahoo Finance CORN x USD/VND), mô hình XGBoost đứng hạng 1 với MAE = 305,09 VNĐ/kg, RMSE = 393,93 VNĐ/kg, MAPE = 1,71%, R2 = 0,8844 và PICP 95% = 97,33% (vượt Baseline 1,715%, bám sát là ARIMA 1,75% và Random Forest 1,77%).",
            "Đối với Hạt điều thô (mã CASHEW_NUT, địa phương chuẩn: huyện Bù Đăng - Bình Phước, 504 phiên từ 21/11/2024 – 23/11/2026, neo giá khảo sát sống 7 tỉnh tại banggianongsan.com mức 32.500 VNĐ/kg tại Bình Phước kết hợp chuỗi tham chiếu Proxy Index ETF Yahoo Finance SOYB x USD/VND), mô hình ARIMA đạt hạng 1 với MAE = 444,00 VNĐ/kg, RMSE = 555,34 VNĐ/kg, MAPE = 1,30%, R2 = 0,8127 và PICP 95% = 100%; theo sát là XGBoost (MAPE = 1,33%) và PyTorch LSTM (MAPE = 1,35%).",
            "Đối với Mía nguyên liệu 10 chữ đường (mã SUGARCANE, đơn vị VNĐ/tấn), bộ dữ liệu gồm 729 phiên giao dịch thật từ 02/01/2024 đến 23/11/2026 quy đổi minh bạch từ sàn đường thô thế giới ICE Sugar #11 (Yahoo Finance SB=F x USD/VND theo hệ số 10 CCS, giá chốt 23/11/2026 đạt 1.230.000 VNĐ/tấn) kết hợp 8 bài báo khảo sát vụ ép 2024–2026 tại Khánh Hòa (1.000.000 – 1.270.000 đ/tấn), Phú Yên và Gia Lai. Trên kiểm định Walk-Forward 7 ngày, Facebook Prophet dẫn đầu với MAPE = 2,62%, RMSE = 46.011,00 VNĐ/tấn, R2 = 0,8571, PICP 95% = 97,78%, theo sát là Random Forest (MAPE = 2,70%) — cả hai đều vượt Naive Baseline (2,74%).",
        ],
    ),
]
