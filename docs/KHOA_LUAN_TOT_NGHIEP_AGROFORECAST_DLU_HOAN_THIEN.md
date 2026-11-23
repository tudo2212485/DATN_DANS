# XÂY DỰNG ỨNG DỤNG PHÂN TÍCH DỮ LIỆU VÀ DỰ BÁO BIẾN ĐỘNG GIÁ NÔNG SẢN THEO CHUỖI THỜI GIAN SỬ DỤNG HỌC MÁY

**Sinh viên thực hiện:** Đỗ Trung Tú (2212485), Nguyễn Thành Huy Thông (2212469), Lê Văn Minh (2212416)

**Giảng viên hướng dẫn:** ThS. La Quốc Thắng

**Trường Đại học Đà Lạt - Khoa Công Nghệ Thông Tin - Tháng 11/2026**

---


# Chương 1: GIỚI THIỆU VÀ TỔNG QUAN ĐỀ TÀI


## 1.1. Tổng quan về thị trường nông sản Việt Nam và đặc thù giá bán tại vườn/ruộng


### 1.1.1. Đặc điểm hình thành giá nông sản tại hộ sản xuất (Farm-gate Price)

Trong cấu trúc chuỗi giá trị nông sản tại Việt Nam, giá bán tại vườn hoặc tại ruộng (Farm-gate Price) là mức giá giao dịch đầu tiên được thiết lập trực tiếp giữa hộ nông dân sản xuất và thương lái địa phương, đại lý thu mua cấp xã/huyện hoặc hợp tác xã ngay tại địa điểm thu hoạch. Khác với giá xuất khẩu FOB tại cảng biển hay giá bán lẻ tại hệ thống siêu thị đô thị, giá bán tại vườn phản ánh trực tiếp thu nhập thực tế của người nông dân và chịu sự chi phối tức thời của chất lượng nông sản tươi, độ ẩm sau thu hoạch, điều kiện giao thông nội đồng và áp lực nguồn cung cục bộ trong từng đợt thu hoạch rộ.

Đối với nhóm cây công nghiệp dài ngày tại Tây Nguyên và Đông Nam Bộ như cà phê Robusta (Đắk Lắk, Lâm Đồng, Gia Lai, Đắk Nông), hồ tiêu đen (Gia Lai, Đắk Lắk, Bà Rịa - Vũng Tàu, Bình Phước) và hạt điều thô (Bình Phước, Đồng Nai), nông hộ thường thu hái, phơi sấy sơ bộ tại sân vườn và bán dạng nhân xô hoặc hạt khô cho các đại lý thu mua tại huyện. Mức giá giao dịch tại vườn biến động hàng ngày theo nhịp giá thế giới (sàn London ICE Europe đối với cà phê Robusta, sàn IPC đối với hồ tiêu) kết hợp với tỷ giá ngoại tệ USD/VND và mức cộng/trừ lùi vận chuyển của từng huyện.

Đối với nhóm cây lương thực và rau củ quả thương phẩm ngắn ngày như lúa IR50404 tại Đồng bằng sông Cửu Long (An Giang, Đồng Tháp, Kiên Giang, Tiền Giang), khoai lang tím Nhật tại Vĩnh Long hay dâu tây và khoai tây tại thành phố Đà Lạt (Lâm Đồng), tính chất thời vụ và độ tươi của sản phẩm đóng vai trò quyết định. Lúa tươi và khoai lang được thương lái đưa ghe hoặc xe tải về cân trực tiếp tại bờ ruộng ngay khi gặt hoặc dỡ củ; trong khi dâu tây và khoai tây Đà Lạt được cắt và phân loại ngay tại nhà vườn ở Phường 7, Phường 8 (Đà Lạt) hoặc huyện Lạc Dương, Đức Trọng, Đơn Dương trước khi đóng thùng vận chuyển đi TP. Hồ Chí Minh và các tỉnh phía Nam.


### 1.1.2. Phân tích cơ chế chênh lệch giá địa phương (Spatial Basis Spread) giữa các huyện chuyên canh

Một sai lầm phổ biến của nhiều hệ thống thông tin thị trường hiện nay là gộp chung giá nông sản theo các vùng địa lý vĩ mô (chẳng hạn chỉ ghi chung là 'vùng Tây Nguyên' hoặc 'vùng Đồng bằng sông Cửu Long'). Trong thực tế giao dịch nông sản Việt Nam, giữa các huyện chuyên canh trong cùng một vùng hoặc giữa các tỉnh lân cận luôn tồn tại một độ lệch giá cơ sở ổn định gọi là Spatial Basis Spread (ký hiệu là Delta_r, tính bằng VNĐ/kg hoặc VNĐ/tấn).

Độ lệch giá cơ sở Delta_r giữa địa phương r và địa phương tham chiếu chuẩn r_0 được hình thành từ bốn yếu tố kinh tế - kỹ thuật rõ rệt: (1) Chi phí vận chuyển (Logistics Cost) từ vườn/ruộng đến nhà máy chế biến hoặc cảng xuất khẩu; (2) Chất lượng sinh thái và thổ nhưỡng đặc trưng (ví dụ hồ tiêu huyện Châu Đức - Bà Rịa Vũng Tàu có dung trọng hạt lớn và gần cảng Cái Mép nên giá bán tại vườn cao hơn vùng chuẩn Chư Sê - Gia Lai khoảng +1.500 VNĐ/kg; trong khi cà phê huyện Di Linh - Lâm Đồng có độ ẩm cao hơn vào mùa mưa nên thường chiết khấu -800 VNĐ/kg so với vùng chuẩn Cư M'gar - Đắk Lắk); (3) Mật độ đại lý thu mua và hạ tầng thủy lợi/giao thông tại ruộng (ví dụ vùng lúa huyện Tháp Mười - Đồng Tháp có hệ thống kênh rạch thuận lợi cho ghe lớn vào tận ruộng nên giá lúa tươi cao hơn +150 VNĐ/kg); và (4) Thương hiệu chỉ dẫn địa lý (ví dụ dâu tây cắt tại vườn Phường 8 - TP. Đà Lạt có giá cao hơn dâu tây Mộc Châu - Sơn La khoảng 15.000 VNĐ/kg).

Bảng 1.1 dưới đây tổng hợp chi tiết danh mục 8 loại nông sản chủ lực và 29 địa phương cấp huyện/thị xã/phường bán tại vườn/ruộng được nghiên cứu và mô hình hóa trực tiếp trong hệ thống AgroForecast.


**Bảng 1.1. Danh mục 8 mặt hàng nông sản và 29 địa phương khảo sát giá bán tại vườn/ruộng trong hệ thống AgroForecast**

| Mã nông sản | Tên nông sản | Đơn vị | Địa phương bán tại vườn / tại ruộng | Độ lệch giá (Basis Spread) | Đặc điểm kinh tế - kỹ thuật tại địa phương |
| --- | --- | --- | --- | --- | --- |
| COFFEE_ROBUSTA | Cà phê Robusta | VNĐ/kg | Huyện Cư M'gar - Đắk Lắk (Tại vườn) | 0 (Mốc chuẩn) | Giá cà phê nhân xô nông hộ bán trực tiếp tại vườn/sân phơi Cư M'gar |
| COFFEE_ROBUSTA | Cà phê Robusta | VNĐ/kg | Thị xã Buôn Hồ - Đắk Lắk (Tại vườn) | -100 | Giá bán tại vườn khu vực Buôn Hồ, Krông Năng |
| COFFEE_ROBUSTA | Cà phê Robusta | VNĐ/kg | Huyện Di Linh - Lâm Đồng (Tại vườn) | -800 | Độ ẩm hạt cao hơn vào mùa mưa, trừ lùi chi phí vận chuyển từ vườn |
| COFFEE_ROBUSTA | Cà phê Robusta | VNĐ/kg | Huyện Chư Prông - Gia Lai (Tại vườn) | -300 | Chiết khấu khoảng cách vận chuyển về kho chế biến xuất khẩu |
| COFFEE_ROBUSTA | Cà phê Robusta | VNĐ/kg | Huyện Đắk Mil - Đắk Nông (Tại vườn) | +200 | Cà phê nhân xô hạt đều, tỷ lệ trên sàng 16 cao tại vườn Đắk Mil |
| PEPPER_BLACK | Hồ tiêu đen | VNĐ/kg | Huyện Chư Sê - Gia Lai (Tại vườn) | 0 (Mốc chuẩn) | Giá tiêu đen xô phơi khô tại hộ nông dân vùng trọng điểm Chư Sê |
| PEPPER_BLACK | Hồ tiêu đen | VNĐ/kg | Huyện Cư Kuin - Đắk Lắk (Tại vườn) | +200 | Tiêu đen phơi khô tại vườn khu vực Cư Kuin, Ea H'leo |
| PEPPER_BLACK | Hồ tiêu đen | VNĐ/kg | Huyện Châu Đức - Bà Rịa Vũng Tàu (Tại vườn) | +1.500 | Hạt tiêu dung trọng cao, gần cụm cảng xuất khẩu Cái Mép - Thị Vải |
| PEPPER_BLACK | Hồ tiêu đen | VNĐ/kg | Huyện Lộc Ninh - Bình Phước (Tại vườn) | -500 | Giá tiêu nông hộ bán ra tại vườn khu vực Lộc Ninh, Bù Đốp |
| PEPPER_BLACK | Hồ tiêu đen | VNĐ/kg | Huyện Đắk Song - Đắk Nông (Tại vườn) | +100 | Vùng chuyên canh tiêu sản lượng lớn, thương lái thu mua tận vườn |
| RICE_IR504 | Lúa gạo IR50404 | VNĐ/kg | Huyện Châu Phú - An Giang (Tại ruộng) | 0 (Mốc chuẩn) | Giá lúa tươi thương lái cân trực tiếp tại bờ ruộng Châu Phú |
| RICE_IR504 | Lúa gạo IR50404 | VNĐ/kg | Huyện Thoại Sơn - An Giang (Tại ruộng) | +50 | Vùng chuyên canh lúa chất lượng đồng đều, gần cụm nhà máy xay xát |
| RICE_IR504 | Lúa gạo IR50404 | VNĐ/kg | Huyện Tháp Mười - Đồng Tháp (Tại ruộng) | +150 | Thuận lợi vận tải thủy nội địa, ghe thương lái vào tận ruộng |
| RICE_IR504 | Lúa gạo IR50404 | VNĐ/kg | Huyện Tân Hiệp - Kiên Giang (Tại ruộng) | -150 | Chiết khấu cước ghe vận chuyển từ ruộng về cụm kho xay xát trung tâm |
| RICE_IR504 | Lúa gạo IR50404 | VNĐ/kg | Huyện Cái Bè - Tiền Giang (Tại ruộng) | +100 | Gần chợ đầu mối lương thực Bà Đắc, nhu cầu thu mua tại ruộng cao |
| SUGARCANE | Mía đường 10 CCS | VNĐ/tấn | Huyện Tây Hòa - Phú Yên (Tại ruộng) | 0 (Mốc chuẩn) | Giá mía nguyên liệu 10 CCS cân trực tiếp tại ruộng Tây Hòa |
| SUGARCANE | Mía đường 10 CCS | VNĐ/tấn | Huyện Tân Châu - Tây Ninh (Tại ruộng) | -10.000 | Giá mía nguyên liệu thu mua tại ruộng khu vực Đông Nam Bộ |
| SUGARCANE | Mía đường 10 CCS | VNĐ/tấn | Thị xã An Khê - Gia Lai (Tại ruộng) | -8.000 | Trừ lùi cước xe tải vận chuyển từ ruộng đồi về nhà máy đường |
| SUGARCANE | Mía đường 10 CCS | VNĐ/tấn | Huyện Phụng Hiệp - Hậu Giang (Tại ruộng) | -15.000 | Chữ đường bình quân thấp hơn do đặc thù đất ngập nước ĐBSCL |
| STRAWBERRY | Dâu tây Đà Lạt | VNĐ/kg | Phường 8 - TP. Đà Lạt (Tại vườn) | 0 (Mốc chuẩn) | Giá dâu tây tươi hái và đóng hộp trực tiếp tại nhà vườn Phường 8 |
| STRAWBERRY | Dâu tây Đà Lạt | VNĐ/kg | Huyện Lạc Dương - Lâm Đồng (Tại vườn) | -3.000 | Giá bán sỉ tại vườn khu vực chân núi Langbiang - Lạc Dương |
| STRAWBERRY | Dâu tây Đà Lạt | VNĐ/kg | Huyện Mộc Châu - Sơn La (Tại vườn) | -15.000 | Giá dâu tây thu hoạch tại vườn Mộc Châu vào chính vụ mùa đông |
| SWEET_POTATO | Khoai lang tím | VNĐ/kg | Huyện Bình Tân - Vĩnh Long (Tại ruộng) | 0 (Mốc chuẩn) | Giá khoai lang tím Nhật thương lái cân trực tiếp tại ruộng Bình Tân |
| SWEET_POTATO | Khoai lang tím | VNĐ/kg | Huyện Châu Thành - Đồng Tháp (Tại ruộng) | -400 | Giá bán tại ruộng khu vực Châu Thành, Lai Vung |
| SWEET_POTATO | Khoai lang tím | VNĐ/kg | Huyện Châu Thành A - Hậu Giang (Tại ruộng) | -500 | Chiết khấu chi phí vận chuyển đường thủy về vựa đóng gói xuất khẩu |
| POTATO | Khoai tây Đà Lạt | VNĐ/kg | Phường 7 (Thái Phiên) - Đà Lạt (Tại vườn) | 0 (Mốc chuẩn) | Giá khoai tây hồng/vàng Đà Lạt loại 1 thu mua tại vườn Thái Phiên |
| POTATO | Khoai tây Đà Lạt | VNĐ/kg | Huyện Đức Trọng - Lâm Đồng (Tại vườn) | -800 | Giá bán tại ruộng/vườn khu vực Liên Nghĩa, Hiệp Thạnh - Đức Trọng |
| POTATO | Khoai tây Đà Lạt | VNĐ/kg | Huyện Đơn Dương - Lâm Đồng (Tại vườn) | -1.000 | Giá thu mua tại vườn chuyên canh rau củ Lạc Lâm, Thạnh Mỹ - Đơn Dương |
| CASHEW_NUT | Hạt điều thô | VNĐ/kg | Huyện Bù Đăng - Bình Phước (Tại vườn) | 0 (Mốc chuẩn) | Giá hạt điều tươi/phơi ráo nông hộ bán tại vườn Bù Đăng, Phú Riềng |



### 1.1.3. Đặc tả nguồn dữ liệu chính thống tại Việt Nam cho 8 mặt hàng nông sản

Để đảm bảo tính xác thực tuyệt đối (Zero Fabrication) và giá trị thực tiễn của mô hình học máy, hệ thống AgroForecast phân tách minh bạch nguồn dữ liệu của 8 mặt hàng nông sản thành 3 nhóm rõ ràng (được gắn nhãn trực tiếp và cho phép bấm kiểm chứng nguồn trên trang /history):

1. Nhóm 3 mặt hàng chủ lực có 100% đường dẫn bài báo kiểm chứng riêng từng ngày (2.154 phiên giai đoạn 01/2024 – 23/11/2026): Cà phê Robusta (919 phiên trên vietnambiz.vn và giacaphe.com + 3.485 quan sát tách 4 tỉnh Tây Nguyên), Hồ tiêu đen (793 phiên trên vietnambiz.vn + 4.446 quan sát tách 6 tỉnh) và Lúa gạo IR50404 (442 phiên từ Sở NN&PTNT An Giang qua vietnambiz.vn và Hiệp hội Lương thực Việt Nam VFA vietfood.org.vn + 1.101 quan sát tách 7 tỉnh ĐBSCL). 2. Nhóm Mía đường 10 CCS (729 phiên): quy đổi minh bạch từ sàn kỳ hạn đường thô thế giới ICE Sugar #11 (Yahoo Finance SB=F x tỷ giá USD/VND theo hệ số 10 CCS) kết hợp 8 bài báo khảo sát trực tiếp vụ ép 2024–2026 tại Khánh Hòa, Phú Yên và Gia Lai trong bảng regional_price_observations. 3. Nhóm 4 đặc sản mở rộng gồm Dâu tây Đà Lạt, Khoai tây Đà Lạt, Khoai lang tím Vĩnh Long và Hạt điều thô (504 phiên/mặt hàng): do thị trường rau củ quả nội địa không niêm yết giá hằng ngày liên tục nhiều năm, hệ thống neo sát giá khảo sát sống tại các nguồn Việt Nam (Kamereo, vựa Nam Tĩnh Lâm Đồng, banggianongsan.com) kết hợp chuỗi tham chiếu Proxy Index ETF nông sản thực tế từ Yahoo Finance (DBA, MOO, CORN, SOYB x USD/VND), ghi nhãn công khai minh bạch bản chất chuỗi dữ liệu.


### 1.1.4. Phân tích đặc tính chu kỳ thu hoạch và yếu tố mùa vụ của 8 mặt hàng nông sản Việt Nam

Mỗi loại nông sản trong 8 mặt hàng mục tiêu của hệ thống AgroForecast sở hữu một lịch thời vụ sinh trưởng, thu hoạch và xuất bán tại vườn hoàn toàn khác biệt. Việc phân tích tường minh quy luật mùa vụ này là cơ sở khoa học trực tiếp để thiết kế các đặc trưng lịch (Calendar Features), cấu hình chuỗi Fourier mùa vụ trong mô hình Prophet và xây dựng bộ trọng số giải thích mô hình (Explainable AI - XAI).

1. Đối với Cà phê Robusta (COFFEE_ROBUSTA): Niên vụ cà phê Việt Nam tại Tây Nguyên (Đắk Lắk, Lâm Đồng, Gia Lai, Đắk Nông) bắt đầu thu hoạch bói từ tháng 10, vào chính vụ thu hoạch rộ trong tháng 11 và tháng 12, và kết thúc phơi sấy vào tháng 1 năm sau. Trong giai đoạn thu hoạch rộ (tháng 11 - 12), lượng cà phê nhân xô mới đưa ra thị trường dồi dào kết hợp nhu cầu cần tiền mặt trả công thu hái của nông hộ thường tạo áp lực điều chỉnh giá ngắn hạn tại vườn. Ngược lại, từ tháng 5 đến tháng 9 là giai đoạn giáp hạt, tồn kho trong dân cạn dần, giá cà phê tại vườn nhạy cảm mạnh với tình hình thời tiết khô hạn tại Tây Nguyên và biến động tồn kho đạt chuẩn trên sàn London ICE Europe.

2. Đối với Hồ tiêu đen (PEPPER_BLACK): Vụ thu hoạch hồ tiêu tại Gia Lai, Đắk Lắk, Đắk Nông, Bình Phước và Bà Rịa - Vũng Tàu diễn ra từ sau Tết Nguyên đán (tháng 2) đến hết tháng 4 dương lịch. Hồ tiêu khô có ưu thế bảo quản được lâu trong kho của hộ nông dân (từ 1 đến 3 năm nếu phơi đạt độ ẩm chuẩn <= 13%), do đó hành vi giữ hàng chờ giá của nông hộ tại Chư Sê (Gia Lai) hay Châu Đức (Bà Rịa - Vũng Tàu) đóng vai trò quyết định đến nguồn cung thực tế.

3. Đối với Lúa gạo IR50404 (RICE_IR504): Đồng bằng sông Cửu Long có 3 vụ lúa chính trong năm: vụ Đông Xuân (thu hoạch tháng 2 - tháng 4, cho năng suất và chất lượng gạo tốt nhất), vụ Hè Thu (thu hoạch tháng 6 - tháng 8) và vụ Thu Đông (thu hoạch tháng 10 - tháng 11). Do lúa tươi IR50404 sau khi gặt có độ ẩm cao (24% - 28%) phải đưa vào lò sấy trong vòng 24 - 48 giờ, nông hộ tại Châu Phú, Thoại Sơn (An Giang) hay Tháp Mười (Đồng Tháp) chủ yếu bán lúa tươi ngay tại bờ ruộng cho thương lái ghe thủy nội địa.

4. Đối với Mía đường 10 CCS (SUGARCANE): Vụ ép mía tại Phú Yên, Gia Lai, Tây Ninh và Hậu Giang kéo dài từ tháng 11 đến tháng 4 năm sau. Giá mía nguyên liệu bán tại ruộng phụ thuộc trực tiếp vào chữ đường thương mại (CCS - Commercial Cane Sugar): khi thời tiết nắng khô vào cuối vụ, chữ đường tích lũy trong cây mía tăng lên (từ 9 CCS lên 11 - 12 CCS), giúp giá thu mua thực tế tại ruộng tăng tương ứng 8% - 15%.

5. Đối với Dâu tây Đà Lạt (STRAWBERRY) và Khoai tây Đà Lạt (POTATO): Tại Phường 7, Phường 8 (TP. Đà Lạt) và các huyện Lạc Dương, Đức Trọng, Đơn Dương (Lâm Đồng), khí hậu chia làm hai mùa rõ rệt: mùa khô (từ tháng 11 đến tháng 4 năm sau) với biên độ nhiệt ngày đêm lớn, nắng ấm ban ngày và se lạnh ban đêm là thời điểm vàng cho dâu tây Đà Lạt đạt độ ngọt (Brix) cao nhất và khoai tây đạt năng suất củ thương phẩm loại 1 cao nhất. Ngược lại, vào các tháng mưa dầm mùa hè (tháng 6 - tháng 9), tỷ lệ hao hụt tại vườn tăng cao đẩy giá bán tại vườn biến động mạnh.

6. Đối với Khoai lang tím Nhật (SWEET_POTATO) và Hạt điều thô (CASHEW_NUT): Khoai lang tím tại huyện Bình Tân (Vĩnh Long) có chu kỳ canh tác 4 - 4,5 tháng và phụ thuộc chặt chẽ vào hạn ngạch kiểm dịch thực vật xuất khẩu chính ngạch. Trong khi đó, hạt điều thô tại Bù Đăng, Phú Riềng (Bình Phước) thu hoạch tập trung từ tháng 2 đến tháng 5, chịu tác động kép của năng suất đậu quả sau các đợt mưa trái mùa và nhu cầu nhập khẩu điều nhân của thị trường Hoa Kỳ, châu Âu.


### 1.1.5. Phân tích chuyên sâu Mặt hàng 1: Lúa gạo IR50404 (Mã RICE_IR504 - Địa phương chuẩn: Huyện Châu Phú, An Giang)

Giống lúa IR50404 là giống lúa ngắn ngày (thời gian sinh trưởng 85 - 90 ngày) được gieo trồng phổ biến nhất tại các tỉnh Đồng bằng sông Cửu Long nhờ khả năng thích nghi rộng, năng suất ổn định và hàm lượng amylose cao phù hợp cho cả tiêu thụ nội địa lẫn chế biến bún, bánh và xuất khẩu. Trong cơ sở dữ liệu của hệ thống AgroForecast (chốt mốc 23/11/2026), chuỗi lịch sử giá lúa tươi IR50404 bán trực tiếp tại bờ ruộng tỉnh An Giang & ĐBSCL bao gồm 442 quan sát đã xác minh từ ngày 01/01/2024 đến ngày 23/11/2026 (100% có đường dẫn bài báo/bản tin VFA gốc kiểm chứng, cộng 1.101 quan sát cấp tỉnh tại 7 tỉnh ĐBSCL), với mức giá giao dịch mới nhất đạt 6.850 VNĐ/kg.

Khi phân tích đặc tính thống kê của chuỗi giá RICE_IR504, phương sai biến động ngày của lúa tươi tương đối nhỏ và có tính tự tương quan bậc 1–2 rất mạnh. Trong thực nghiệm đối sánh Walk-Forward 7 ngày của 5 mô hình học máy, mô hình thống kê ARIMA đạt sai số MAPE thấp nhất là 1,58% (MAE = 100,24 VNĐ/kg, RMSE = 169,20 VNĐ/kg, R2 = 0,5340, PICP 95% = 89,39%), theo sát là Facebook Prophet (MAE = 100,13 VNĐ/kg, RMSE thấp nhất 156,67 VNĐ/kg, MAPE = 1,59%, R2 = 0,6005) và XGBoost (MAPE = 1,65%).

Về phân bố giá bán tại ruộng theo các địa phương ĐBSCL: tại huyện Thoại Sơn (An Giang) giá cao hơn mức chuẩn Châu Phú +50 VNĐ/kg; tại huyện Tháp Mười (Đồng Tháp) đạt +150 VNĐ/kg nhờ thuận lợi vận tải thủy nội địa; tại huyện Cái Bè (Tiền Giang) đạt +100 VNĐ/kg; trong khi tại huyện Tân Hiệp (Kiên Giang) chiết khấu -150 VNĐ/kg do cước ghe trung chuyển xa hơn.


### 1.1.6. Phân tích chuyên sâu Mặt hàng 2: Cà phê nhân xô Robusta (Mã COFFEE_ROBUSTA - Địa phương chuẩn: Huyện Cư M'gar, Đắk Lắk)

Cà phê Robusta (Coffea canephora) là mặt hàng nông sản xuất khẩu chiến lược số một của vùng Tây Nguyên, chiếm trên 90% diện tích cà phê cả nước. Chuỗi dữ liệu lịch sử của COFFEE_ROBUSTA trong hệ thống gồm 919 quan sát đã xác minh từ ngày 04/01/2024 đến ngày 23/11/2026 (919 bài báo kiểm chứng độc lập trên vietnambiz.vn & giacaphe.com cùng 3.485 quan sát khảo sát 4 tỉnh Tây Nguyên), ghi nhận trọn vẹn chu kỳ biến động lịch sử từ đỉnh 135.200 VNĐ/kg về vùng điều chỉnh cuối năm 2026 ở mức 71.700 VNĐ/kg.

Do giá cà phê nhân xô tại vườn chịu tác động trực tiếp từ sàn kỳ hạn London ICE Europe, tỷ giá USD/VND và chi phí năng lượng/vận tải, việc bổ sung 2 biến ngoại sinh nhân quả (USD/VND và Dầu thô WTI <= t-1) giúp mạng học sâu PyTorch Stacked LSTM (7 kênh nhân quả) xuất sắc đạt Hạng 1 tuyệt đối trên kiểm định Walk-Forward 7 ngày với MAE = 1.555,41 VNĐ/kg, RMSE = 1.978,28 VNĐ/kg, MAPE = 1,79%, R2 = 0,8972 và PICP 95% = 92,22%, vượt trội rõ rệt so với ARIMA (MAPE = 1,86%), Random Forest (RMSE = 2.087,40, MAPE = 1,90%) và Naive Baseline (MAPE = 1,88%, RMSE = 2.147,01 VNĐ/kg).

Về chênh lệch giá bán tại vườn giữa các tỉnh/huyện Tây Nguyên: hệ thống đồng bộ trực tiếp bảng giá từng ngày tại Đắk Lắk, Lâm Đồng, Gia Lai, Đắk Nông và áp dụng định mức độ lệch cấp huyện (-100 đ/kg tại Buôn Hồ, -300 đ/kg tại Chư Prông, -800 đ/kg tại Di Linh và +200 đ/kg tại Đắk Mil).


### 1.1.7. Phân tích chuyên sâu Mặt hàng 3: Hồ tiêu đen xô khô (Mã PEPPER_BLACK - Địa phương chuẩn: Huyện Chư Sê, Gia Lai)

Hồ tiêu đen Việt Nam giữ vị trí dẫn đầu thế giới về sản lượng xuất khẩu. Trong hệ thống AgroForecast, chuỗi dữ liệu PEPPER_BLACK gồm 793 quan sát thực tế từ ngày 04/01/2024 đến ngày 23/11/2026 (793 bài báo gốc vietnambiz.vn và 4.446 quan sát khảo sát trực tiếp tại 6 tỉnh trọng điểm), dao động trong biên độ 77.800 – 169.200 VNĐ/kg với mức giá mới nhất ngày 23/11/2026 đạt 129.100 VNĐ/kg.

Trên tập kiểm thử Walk-Forward 7 ngày (90 phiên cuối), cả 5 mô hình đều đạt sai số MAPE xuất sắc dưới 0,90%: đứng đầu về MAPE là ARIMA (MAE = 990,46 VNĐ/kg, RMSE = 1.643,77 VNĐ/kg, MAPE = 0,74%, PICP 95% = 94,44%, vượt Baseline RMSE 1.646,34 VNĐ/kg), đứng thứ hai là XGBoost (MAE = 1.045,64 VNĐ/kg, MAPE = 0,78%) và đứng thứ ba là Random Forest (RMSE thấp nhất 1.631,93 VNĐ/kg, MAPE = 0,78%, R2 = 0,3353). Về chênh lệch địa phương, Bà Rịa - Vũng Tàu (Châu Đức) luôn cao hơn vùng chuẩn do dung trọng hạt lớn và gần cụm cảng Cái Mép - Thị Vải.


### 1.1.8. Phân tích chuyên sâu Mặt hàng 4 & 5: Dâu tây Đà Lạt (STRAWBERRY) và Khoai tây Đà Lạt (POTATO)

Dâu tây tươi Đà Lạt (mã STRAWBERRY, địa phương chuẩn: Phường 8 - TP. Đà Lạt) và Khoai tây thương phẩm Đà Lạt (mã POTATO, địa phương chuẩn: Phường 7 Thái Phiên - TP. Đà Lạt) là hai mặt hàng nông sản ôn đới đặc trưng của tỉnh Lâm Đồng - nơi đặt trụ sở Trường Đại học Đà Lạt. Do thị trường rau củ quả nội địa không niêm yết giá hằng ngày nhiều năm, bộ dữ liệu thực nghiệm của cả hai mặt hàng gồm 504 phiên (21/11/2024 – 23/11/2026) neo giá khảo sát sống tại Việt Nam (kamereo.vn 100.000 VNĐ/kg cho dâu tây Đà Lạt; vựa namtinhvegetable.com Lâm Đồng 20.000 VNĐ/kg cho khoai tây hồng Đà Lạt) kết hợp chuỗi tham chiếu Proxy Index ETF nông sản thực tế Yahoo Finance (DBA x USD/VND và MOO x USD/VND), hiển thị nhãn minh bạch trên /history.

Trên kiểm định Walk-Forward 7 ngày, mô hình Facebook Prophet đạt hiệu năng cao nhất trên cả hai mặt hàng ôn đới nhờ nắm bắt tốt nhịp điệu mùa vụ: trên Dâu tây Đà Lạt đạt MAE = 1.164,79 VNĐ/kg, RMSE = 1.610,18 VNĐ/kg, MAPE = 1,08%, R2 = 0,8693 (PICP 95% = 100%, vượt sâu Naive Baseline 1,30%); trên Khoai tây Đà Lạt đạt MAE = 276,05 VNĐ/kg, RMSE = 368,60 VNĐ/kg, MAPE = 1,30%, R2 = 0,7119 (PICP 95% = 100%, vượt Naive Baseline 1,39%). Cả 5 mô hình đều đạt MAPE thấp từ 1,08% đến 1,60%.


### 1.1.9. Phân tích chuyên sâu Mặt hàng 6, 7 & 8: Khoai lang tím Vĩnh Long, Hạt điều thô Bình Phước và Mía đường 10 CCS

Đối với Khoai lang tím Nhật Vĩnh Long (mã SWEET_POTATO, địa phương chuẩn: huyện Bình Tân - Vĩnh Long, 504 phiên từ 21/11/2024 – 23/11/2026, neo giá khảo sát sống tại banggianongsan.com 16.000 VNĐ/kg kết hợp chuỗi tham chiếu Proxy Index ETF Yahoo Finance CORN x USD/VND), mô hình XGBoost đứng hạng 1 với MAE = 305,09 VNĐ/kg, RMSE = 393,93 VNĐ/kg, MAPE = 1,71%, R2 = 0,8844 và PICP 95% = 97,33% (vượt Baseline 1,715%, bám sát là ARIMA 1,75% và Random Forest 1,77%).

Đối với Hạt điều thô (mã CASHEW_NUT, địa phương chuẩn: huyện Bù Đăng - Bình Phước, 504 phiên từ 21/11/2024 – 23/11/2026, neo giá khảo sát sống 7 tỉnh tại banggianongsan.com mức 32.500 VNĐ/kg tại Bình Phước kết hợp chuỗi tham chiếu Proxy Index ETF Yahoo Finance SOYB x USD/VND), mô hình ARIMA đạt hạng 1 với MAE = 444,00 VNĐ/kg, RMSE = 555,34 VNĐ/kg, MAPE = 1,30%, R2 = 0,8127 và PICP 95% = 100%; theo sát là XGBoost (MAPE = 1,33%) và PyTorch LSTM (MAPE = 1,35%).

Đối với Mía nguyên liệu 10 chữ đường (mã SUGARCANE, đơn vị VNĐ/tấn), bộ dữ liệu gồm 729 phiên giao dịch thật từ 02/01/2024 đến 23/11/2026 quy đổi minh bạch từ sàn đường thô thế giới ICE Sugar #11 (Yahoo Finance SB=F x USD/VND theo hệ số 10 CCS, giá chốt 23/11/2026 đạt 1.230.000 VNĐ/tấn) kết hợp 8 bài báo khảo sát vụ ép 2024–2026 tại Khánh Hòa (1.000.000 – 1.270.000 đ/tấn), Phú Yên và Gia Lai. Trên kiểm định Walk-Forward 7 ngày, Facebook Prophet dẫn đầu với MAPE = 2,62%, RMSE = 46.011,00 VNĐ/tấn, R2 = 0,8571, PICP 95% = 97,78%, theo sát là Random Forest (MAPE = 2,70%) — cả hai đều vượt Naive Baseline (2,74%).


## 1.2. Phân tích, đánh giá các hướng nghiên cứu trong và ngoài nước


### 1.2.1. Các công trình nghiên cứu ngoài nước về dự báo chuỗi thời gian nông sản

Trên thế giới, bài toán dự báo giá nông sản (Agricultural Commodity Price Forecasting) đã thu hút sự quan tâm lớn của cộng đồng nghiên cứu kinh tế lượng và trí tuệ nhân tạo. Về mặt phương pháp luận, các công trình quốc tế phát triển qua ba thế hệ mô hình chính: (1) Thế hệ các mô hình thống kê tuyến tính cổ điển; (2) Thế hệ các mô hình học máy phi tuyến dựa trên cây quyết định; và (3) Thế hệ các mạng nơ-ron học sâu (Deep Learning) kết hợp phân rã chuỗi thời gian.

Ở nhóm mô hình thống kê tuyến tính, phương pháp Box-Jenkins với mô hình ARIMA (AutoRegressive Integrated Moving Average) và SARIMA được xem là nền tảng chuẩn mực để mô hình hóa sự phụ thuộc tuyến tính giữa giá hiện tại và các giá trị quá khứ cùng sai số ngẫu nhiên. Năm 2017, nhóm nghiên cứu Taylor và Letham tại Facebook Core Data Science đã công bố mô hình Prophet, cho phép phân rã chuỗi thời gian thành hàm xu thế từng khúc (piecewise linear/logistic trend), chuỗi Fourier biểu diễn tính mùa vụ đa chu kỳ (tuần, tháng, năm) và hiệu ứng ngày lễ. Prophet khắc phục được nhược điểm của ARIMA khi chuỗi giá nông sản bị khuyết dữ liệu vào ngày cuối tuần hoặc có sự dịch chuyển xu thế đột ngột.

Ở nhóm mô hình học máy phi tuyến và học sâu, các nghiên cứu của Breiman (2001) với Random Forest và Chen & Guestrin (2016) với XGBoost đã chứng minh hiệu quả vượt trội khi chuyển đổi chuỗi thời gian thành bài toán học có giám sát dạng bảng (Tabular Supervised Learning) thông qua các biến trễ (Lag features) và thống kê cửa sổ trượt (Rolling statistics). Đặc biệt, đối với các chuỗi giá có tính phụ thuộc dài hạn phức tạp, kiến trúc mạng nơ-ron hồi quy bộ nhớ dài-ngắn LSTM (Long Short-Term Memory) do Hochreiter và Schmidhuber đề xuất đã giải quyết triệt để hiện tượng triệt tiêu đạo hàm (Vanishing Gradient) của mạng RNN truyền thống, giúp nắm bắt tốt các chu kỳ biến động giá nông sản kéo dài nhiều tuần liên tiếp.


### 1.2.2. Các công trình nghiên cứu trong nước và hệ thống thông tin giá nông sản hiện hành

Tại Việt Nam, trong những năm gần đây đã có một số đề tài nghiên cứu ứng dụng ARIMA hoặc mạng nơ-ron nhân tạo để dự báo giá lúa gạo xuất khẩu hoặc giá cà phê nhân xô Tây Nguyên. Bên cạnh đó, các cổng thông tin điện tử như AGROINFO, Vinanet, Giacaphe hay các bản tin của Sở Nông nghiệp và Phát triển Nông thôn đã thực hiện tốt vai trò cập nhật bảng giá giao dịch hàng ngày hoặc hàng tuần.

Tuy nhiên, khi khảo sát thực tế các hệ thống thông tin và các đề tài nghiên cứu hiện có trong nước, có thể nhận thấy phần lớn các trang tin chỉ dừng lại ở mức độ thống kê mô tả (hiển thị bảng giá quá khứ và hôm nay) chứ chưa tích hợp công cụ dự báo tương lai bằng học máy. Ngược lại, các nghiên cứu học thuật có chạy mô hình dự báo lại thường hoạt động rời rạc trên môi trường Jupyter Notebook, chỉ khảo sát 1 hoặc 2 mặt hàng, chưa có cơ chế tự động hóa thu thập dữ liệu và chưa xây dựng được giao diện ứng dụng Web hoàn chỉnh phục vụ người dùng cuối.


## 1.3. Những vấn đề còn tồn tại của các nghiên cứu và hệ thống hiện có


### 1.3.1. Hạn chế về độ phân giải không gian (thiếu giá bán tại vườn cấp huyện/phường)

Hầu hết các công bố và công cụ hiện nay chỉ đưa ra một mức giá bình quân duy nhất cho cả vùng lớn (ví dụ 'Cà phê Tây Nguyên' hay 'Lúa Đồng bằng sông Cửu Long'). Khi người nông dân tại huyện Di Linh (Lâm Đồng) hay huyện Châu Phú (An Giang) tra cứu, họ không biết được mức giá thực tế bán ra tại vườn/ruộng địa phương mình đang chênh lệch bao nhiêu so với mức bình quân đó và dự báo 7 đến 30 ngày tới tại chính huyện mình sẽ biến động như thế nào.


### 1.3.2. Hạn chế về kiểm soát nguồn gốc dữ liệu (Data Provenance) và rò rỉ dữ liệu kiểm thử

Nhiều hệ thống thử nghiệm trộn lẫn dữ liệu giả lập (mock/synthetic data) với dữ liệu thực tế hoặc không kiểm tra tính liên tục của chuỗi thời gian trước khi huấn luyện. Nghiêm trọng hơn, việc chia tập dữ liệu ngẫu nhiên (Random Shuffle Split) thay vì chia theo thứ tự thời gian (Temporal Holdout Split) dẫn đến hiện tượng rò rỉ dữ liệu tương lai vào quá trình huấn luyện (Data Leakage), làm cho chỉ số đánh giá trong báo cáo rất đẹp nhưng khi dự báo thực tế lại sai lệch lớn.


### 1.3.3. Hạn chế về việc dùng đơn lẻ một thuật toán, thiếu khoảng tin cậy và thiếu kiểm thử bảo mật

Không có một thuật toán học máy duy nhất nào luôn tốt nhất cho mọi loại nông sản (theo định lý No Free Lunch). Thực tế trong dự án này cho thấy ARIMA và XGBoost đạt sai số rất thấp trên chuỗi lúa IR50404 và hồ tiêu đen, trong khi mạng học sâu LSTM lại vượt trội hoàn toàn trên nhóm nông sản đặc sản Đà Lạt (dâu tây, khoai tây) và khoai lang tím. Ngoài ra, các hệ thống hiện tại thường bỏ qua khâu kiểm thử phần mềm tự động và kiểm tra an toàn bảo mật ứng dụng Web theo chuẩn OWASP Top 10.


## 1.4. Các vấn đề trọng tâm mà đề tài tập trung nghiên cứu giải quyết


### 1.4.1. Xây dựng đường ống dữ liệu xác thực và đối sánh tự động 5 mô hình học máy

Đề tài giải quyết triệt để bài toán toàn vẹn dữ liệu bằng cách gắn nhãn nguồn gốc (provenance: collected, reviewed, unverified) và mã băm SHA-256 (dataset_hash) cho từng phiên huấn luyện. Hệ thống huấn luyện đồng thời cả 5 mô hình (LSTM, Prophet, ARIMA, XGBoost, Random Forest) trên tập huấn luyện chuẩn hóa, kiểm định trên tập Holdout cuối chuỗi và tự động đề xuất mô hình có RMSE thấp nhất cho người dùng.


### 1.4.2. Mô hình hóa giá bán tại vườn theo địa phương kết hợp giải thích AI (XAI) và bảo mật OWASP

Đề tài tích hợp tầng hiệu chỉnh không gian - thời gian (Spatio-Temporal Basis Spread) cho 29 địa phương cấp huyện/phường, cung cấp dải tin cậy 95% (lowerCI - upperCI), tích hợp mô-đun giải thích mức độ ảnh hưởng của các yếu tố mùa vụ, tỷ giá, thời tiết (Explainable AI) và bảo vệ toàn diện hệ thống bằng 72 kịch bản kiểm thử tự động và kiểm tra thâm nhập bảo mật.


# Chương 2: CƠ SỞ LÝ THUYẾT VÀ CÔNG NGHỆ SỬ DỤNG


## 2.1. Lý thuyết về chuỗi thời gian (Time Series) và tiền xử lý dữ liệu nông sản


### 2.1.1. Các thành phần của chuỗi thời gian và tính chất giá nông sản

Một chuỗi thời gian (Time Series) là một dãy các quan sát của biến ngẫu nhiên Y_t được ghi nhận theo thứ tự thời gian t = 1, 2, ..., T với khoảng cách thời gian đều đặn (theo ngày giao dịch hoặc theo kỳ báo cáo). Trong bài toán dự báo giá nông sản của hệ thống AgroForecast, mỗi chuỗi giá Y_t = {p_1, p_2, ..., p_T} biểu diễn mức giá bán tại vườn/ruộng (đơn vị VNĐ/kg hoặc VNĐ/tấn) của một mặt hàng tại mốc thời gian t.

Về mặt cấu trúc toán học, một chuỗi thời gian giá nông sản Y_t được hợp thành từ bốn thành phần cơ bản theo mô hình cộng tính (Additive Decomposition): Y_t = T_t + S_t + C_t + e_t, hoặc mô hình nhân tính (Multiplicative Decomposition): Y_t = T_t * S_t * C_t * e_t. Trong đó: (1) Thành phần xu thế dài hạn (Trend - T_t) phản ánh sự dịch chuyển chung của mặt bằng giá theo lạm phát, chi phí phân bón, nhân công và nhu cầu xuất khẩu; (2) Thành phần mùa vụ (Seasonality - S_t) phản ánh quy luật lặp lại theo chu kỳ sinh trưởng và thu hoạch nông nghiệp hàng năm (ví dụ giá cà phê Tây Nguyên thường chịu áp lực điều chỉnh nhẹ khi bước vào chính vụ thu hoạch rộ tháng 11 - tháng 12, trong khi giá tăng cao vào giai đoạn giáp hạt tháng 7 - tháng 9); (3) Thành phần chu kỳ kinh tế (Cycle - C_t) kéo dài nhiều năm theo chu kỳ tái canh cây trồng hoặc hiện tượng khí hậu El Nino / La Nina; và (4) Thành phần nhiễu ngẫu nhiên (Irregular/Residual - e_t) biểu diễn các biến động bất thường ngắn hạn.


### 2.1.2. Kiểm định tính dừng Augmented Dickey-Fuller (ADF) và kỹ thuật sai phân

Một chuỗi thời gian Y_t được gọi là dừng yếu (Weakly Stationary) nếu kỳ vọng toán học E(Y_t) = mu là hằng số không phụ thuộc vào thời gian t, phương sai Var(Y_t) = sigma^2 hữu hạn không đổi theo thời gian, và hiệp phương sai tự tương quan Cov(Y_t, Y_{t-k}) = gamma_k chỉ phụ thuộc vào độ trễ k chứ không phụ thuộc vào thời điểm t. Hầu hết các chuỗi giá nông sản thực tế đều là chuỗi không dừng (Non-stationary) do có xu thế tăng/giảm dài hạn.

Để kiểm tra một chuỗi giá có dừng hay không trước khi đưa vào mô hình ARIMA, hệ thống AgroForecast (tại mô-đun ml_pipeline/data_loader.py) sử dụng kiểm định nghiệm đơn vị Augmented Dickey-Fuller (ADF) thông qua phương trình hồi quy: Delta Y_t = alpha + beta*t + gamma*Y_{t-1} + sum_{i=1..p} (delta_i * Delta Y_{t-i}) + epsilon_t. Giả thuyết không H_0: gamma = 0 (chuỗi có nghiệm đơn vị, tức không dừng) được đối chiếu với giả thuyết đối H_1: gamma < 0 (chuỗi dừng). Nếu giá trị p-value > 0.05, chuỗi chưa dừng và cần thực hiện phép lấy sai phân bậc một (First-order Differencing): Delta Y_t = Y_t - Y_{t-1} hoặc sai phân bậc d: Delta^d Y_t = (1 - B)^d Y_t (với B là toán tử trễ B*Y_t = Y_{t-1}) cho đến khi chuỗi đạt trạng thái dừng.


### 2.1.3. Thuật toán phát hiện và chặn giá trị ngoại lai bằng khoảng tứ phân vị (IQR Outlier Capping)

Trong quá trình thu thập dữ liệu giá nông sản tự động từ các trang tin điện tử hoặc nhập liệu CSV, đôi khi xuất hiện các điểm dữ liệu dị biệt (Outliers) do lỗi đánh máy của nguồn công bố hoặc biến động cục bộ cực đoan. Nếu giữ nguyên các điểm ngoại lai này, hàm mất mát bình phương sai số (MSE) của các mô hình học máy sẽ bị kéo lệch nghiêm trọng; ngược lại, nếu xóa bỏ dòng dữ liệu đó sẽ làm đứt gãy tính liên tục của chuỗi thời gian.

Để giải quyết triệt để vấn đề này, hàm handle_outliers_iqr() trong ml_pipeline/data_loader.py áp dụng phương pháp chặn ngưỡng tứ phân vị (Winsorizing / IQR Capping). Gọi Q_1 (phân vị thứ 25) và Q_3 (phân vị thứ 75) của chuỗi giá hoặc chuỗi sai phân giá, khoảng tứ phân vị được xác định bởi công thức: IQR = Q_3 - Q_1. Ngưỡng dưới (Lower Bound) và ngưỡng trên (Upper Bound) được thiết lập là: L_bound = Q_1 - 1.5 * IQR và U_bound = Q_3 + 1.5 * IQR. Mọi quan sát p_t vượt ra ngoài khoảng [L_bound, U_bound] đều được ép (clip) về đúng biên gần nhất: p_t_clean = min(max(p_t, L_bound), U_bound). Phương pháp này vừa bảo toàn đầy đủ số lượng ngày quan sát vừa loại bỏ hoàn toàn tác động gây nhiễu của các điểm dị biệt.


### 2.1.4. Kỹ thuật trích xuất đặc trưng chuỗi thời gian (Lag Features & Rolling Statistics)

Đối với các thuật toán học máy dạng bảng như Random Forest và XGBoost, chuỗi thời gian một chiều {p_1, p_2, ..., p_T} cần được biến đổi thành ma trận đặc trưng đa chiều X in R^{N x M} và nhãn mục tiêu y in R^N. Trong hệ thống AgroForecast (mô-đun ml_pipeline/feature_engineering.py và app/services/training_service.py), tại mỗi bước thời gian t, véc-tơ đặc trưng x_t được kiến tạo từ bốn nhóm biến số sau:

Nhóm 1 - Các biến trễ tự hồi quy (Autoregressive Lag Features): Bao gồm giá tại các ngày liền trước p_{t-1}, p_{t-2}, p_{t-3}, p_{t-7}, p_{t-14}, phản ánh trực tiếp quán tính giá ngắn hạn và chu kỳ tuần.

Nhóm 2 - Thống kê cửa sổ trượt (Rolling Window Statistics): Bao gồm trung bình trượt 7 ngày (rolling_mean_7d = (1/7)*sum_{k=1..7} p_{t-k}), trung bình trượt 14 ngày (rolling_mean_14d), và độ lệch chuẩn trượt 7 ngày (rolling_std_7d = sqrt((1/7)*sum_{k=1..7} (p_{t-k} - rolling_mean_7d)^2)) dùng để đo lường mức độ biến động (Volatility) của thị trường ngay trước thời điểm dự báo.

Nhóm 3 - Động lượng giá và tốc độ thay đổi (Momentum & Differences): Bao gồm biến chênh lệch tuyệt đối diff_1 = p_{t-1} - p_{t-2} và chênh lệch tuần diff_7 = p_{t-1} - p_{t-7}, giúp mô hình nhận diện nhanh sự đảo chiều từ xu hướng tăng sang giảm hoặc ngược lại.

Nhóm 4 - Đặc trưng lịch và chu kỳ mùa vụ (Calendar & Cyclical Features): Bao gồm thứ trong tuần (day_of_week), ngày trong tháng (day_of_month), tháng trong năm (month) nhằm phản ánh chính xác tính thời vụ thu hoạch của nông sản Việt Nam.


### 2.1.5. Quy trình chuẩn hóa dữ liệu Min-Max Scaling và kiến tạo mẫu cửa sổ trượt cho mạng học sâu

Khác với các mô hình cây quyết định (Random Forest, XGBoost) vốn bất biến với phép biến đổi đơn điệu của thang đo đặc trưng, mạng nơ-ron hồi quy sâu PyTorch LSTM sử dụng các hàm kích hoạt phi tuyến Sigmoid sigma(z) = 1 / (1 + e^{-z}) và Hyperbolic Tangent tanh(z) = (e^z - e^{-z}) / (e^z + e^{-z}). Nếu đưa trực tiếp giá trị giá nông sản gốc (ví dụ 71.700 VNĐ/kg đối với cà phê hoặc 1.208.000 VNĐ/tấn đối với mía đường) vào mạng LSTM, tích vô hướng W * x sẽ rơi vào vùng bão hòa cực trị của hàm kích hoạt, làm cho đạo hàm tiến về 0 và khiến quá trình huấn luyện lan truyền ngược theo thời gian (Backpropagation Through Time - BPTT) hoàn toàn thất bại.

Do đó, hệ thống AgroForecast thực hiện phép chuẩn hóa tuyến tính Min-Max Scaling đưa chuỗi giá về miền giá trị chuẩn [0, 1] hoặc [-1, 1] strictly dựa trên giá trị nhỏ nhất (p_min_train) và lớn nhất (p_max_train) của riêng Tập huấn luyện (Training Set): p_norm_t = (p_t - p_min_train) / (p_max_train - p_min_train + 10^{-8}). Việc chỉ tính p_min_train và p_max_train trên Tập huấn luyện mà không tính trên Tập kiểm thử Holdout là nguyên tắc bắt buộc để đảm bảo không xảy ra rò rỉ thông tin thống kê từ tương lai.

Tiếp theo, chuỗi chuẩn hóa {p_norm_1, p_norm_2, ..., p_norm_{N_train}} được chuyển đổi thành tập các cặp tensor đầu vào - đầu ra theo cơ chế cửa sổ trượt độ dài L (Sliding Window Sequence Generation với L = 14 bước thời gian): với mỗi chỉ số k từ 1 đến N_train - L, tensor đầu vào X_k = [p_norm_k, p_norm_{k+1}, ..., p_norm_{k+L-1}]^T có kích thước (batch_size, seq_length = L, input_size = 1) được ánh xạ tới nhãn mục tiêu y_k = p_norm_{k+L}. Khi suy luận dự báo đa bước (Multi-step Recursive Forecasting) cho H ngày tương lai (H = 7, 10, 14, 30), giá trị dự báo chuẩn hóa hat{y}_{t+1} ở bước 1 được nối tiếp vào cuối cửa sổ trượt và dịch cửa sổ sang phải 1 đơn vị để dự báo bước t+2, lặp lại đệ quy cho đến hết bước t+H trước khi thực hiện phép biến đổi ngược: hat{p}_{t+h} = hat{y}_{t+h} * (p_max_train - p_min_train) + p_min_train.


## 2.2. Cơ sở toán học và cơ chế hoạt động của 5 mô hình học máy dự báo giá


### 2.2.1. Mô hình Tự hồi quy tích hợp trung bình trượt (ARIMA)

Mô hình ARIMA(p, d, q) là sự kết hợp của ba thành phần: Tự hồi quy bậc p (AutoRegressive - AR(p)), Tích hợp sai phân bậc d (Integrated - I(d)) và Trung bình trượt bậc q (Moving Average - MA(q)). Gọi y'_t = Delta^d Y_t = (1 - B)^d Y_t là chuỗi đã lấy sai phân bậc d để đạt tính dừng, phương trình toán học tổng quát của ARIMA(p, d, q) có dạng:

y'_t = c + phi_1 * y'_{t-1} + phi_2 * y'_{t-2} + ... + phi_p * y'_{t-p} + theta_1 * epsilon_{t-1} + theta_2 * epsilon_{t-2} + ... + theta_q * epsilon_{t-q} + epsilon_t

Trong đó: c là hằng số cơ sở; phi_1, ..., phi_p là các hệ số tự hồi quy biểu diễn mức độ ảnh hưởng của p giá trị quá khứ gần nhất; theta_1, ..., theta_q là các hệ số trung bình trượt biểu diễn mức độ điều chỉnh theo các cú sốc sai số quá khứ; và epsilon_t ~ WN(0, sigma^2) là nhiễu trắng có kỳ vọng bằng 0. Các tham số (phi, theta, c) được ước lượng bằng phương pháp Hợp lý cực đại (Maximum Likelihood Estimation - MLE) thông qua bộ lọc Kalman trạng thái - không gian (State-Space Kalman Filter) của thư viện statsmodels.


### 2.2.2. Mô hình phân rã chuỗi thời gian cộng tính (Facebook Prophet)

Mô hình Prophet tiếp cận bài toán dự báo chuỗi thời gian như một bài toán khớp đường cong hồi quy cộng tính tổng quát (Generalized Additive Model - GAM) theo phương trình: y(t) = g(t) + s(t) + h(t) + epsilon_t.

Thành phần xu thế g(t) được mô hình hóa bằng hàm tuyến tính từng khúc có các điểm gãy thay đổi xu hướng (Changepoints): g(t) = (k + a(t)^T * delta) * t + (m + a(t)^T * gamma), trong đó k là tốc độ tăng trưởng cơ bản, delta là véc-tơ điều chỉnh độ dốc tại S điểm gãy s_j (j = 1..S), và a_j(t) = 1 nếu t >= s_j (ngược lại bằng 0). Để tránh hiện tượng quá khớp (Overfitting) khi dự báo xa, Prophet đặt phân phối tiên nghiệm Laplace: delta_j ~ Laplace(0, tau) (tương đương điều chuẩn L1 Lasso) giúp chỉ giữ lại những điểm đảo chiều xu thế thực sự có ý nghĩa.

Thành phần mùa vụ s(t) được biểu diễn mượt mà bằng chuỗi lượng giác Fourier bậc N: s(t) = sum_{n=1..N} [a_n * cos(2*pi*n*t / P) + b_n * sin(2*pi*n*t / P)], với P = 365.25 cho chu kỳ mùa vụ nông nghiệp hàng năm và P = 7 cho chu kỳ giao dịch hàng tuần. Quá trình tối ưu tham số được thực hiện bằng thuật toán L-BFGS tốc độ cao.


### 2.2.3. Mô hình Rừng ngẫu nhiên (Random Forest Regressor)

Random Forest Regressor là thuật toán học máy tổ hợp (Ensemble Learning) dựa trên kỹ thuật Bagging (Bootstrap Aggregating) kết hợp lựa chọn đặc trưng ngẫu nhiên trên tập hợp B cây quyết định hồi quy độc lập {T_1(x), T_2(x), ..., T_B(x)}. Từ tập dữ liệu huấn luyện gốc D gồm N mẫu đặc trưng chuỗi thời gian, thuật toán tạo ra B tập mẫu con D_b bằng phương pháp lấy mẫu có hoàn lại (Bootstrap) và xây dựng mỗi cây quyết định T_b bằng cách tại mỗi nút phân nhánh chỉ xét một tập con ngẫu nhiên các đặc trưng để tìm ngưỡng chia giảm thiểu phương sai nội nhóm (MSE Impurity) nhiều nhất.

Giá trị dự báo cuối cùng hat{y} của Random Forest tại bước thời gian tương lai là trung bình cộng dự báo của tất cả B cây thành viên: hat{y}(x) = (1 / B) * sum_{b=1..B} T_b(x). Nhờ cơ chế lấy trung bình trên các cây có tương quan thấp, phương sai của sai số dự báo giảm đi theo hệ số 1/B mà không làm tăng độ chệch (Bias), giúp mô hình hoạt động rất ổn định trước các biến động nhiễu của thị trường nông sản.


### 2.2.4. Mô hình Tăng cường độ dốc cực đại (Extreme Gradient Boosting - XGBoost)

Khác với Random Forest xây dựng các cây độc lập song song, XGBoost xây dựng chuỗi K cây hồi quy nối tiếp nhau (Additive Boosting), trong đó cây thứ k được huấn luyện để sửa trực tiếp sai số dư (Residuals) của k-1 cây trước đó: hat{y}_i^{(k)} = hat{y}_i^{(k-1)} + eta * f_k(x_i), với eta là tốc độ học (Learning Rate).

Hàm mục tiêu có điều chuẩn của XGBoost tại bước lặp thứ k được xác định bởi: L^{(k)} = sum_{i=1..n} l(y_i, hat{y}_i^{(k-1)} + f_k(x_i)) + Omega(f_k), trong đó hàm phạt độ phức tạp của cây là Omega(f) = gamma * T + (1/2) * lambda * sum_{j=1..T} w_j^2 (T là số nút lá, w_j là trọng số nút lá thứ j). Bằng cách khai triển chuỗi Taylor bậc hai sử dụng cả đạo hàm bậc nhất g_i (Gradient) và đạo hàm bậc hai h_i (Hessian) của hàm mất mát, trọng số tối ưu của nút lá j được tính tường minh theo công thức: w_j^* = - (sum_{i in I_j} g_i) / (sum_{i in I_j} h_i + lambda). Nhờ điều chuẩn L1/L2 chặt chẽ và tối ưu hóa bậc hai, XGBoost đạt độ chính xác rất cao trên các chuỗi giá có biên độ biến động lớn như Cà phê Robusta và Hồ tiêu đen.


### 2.2.5. Mạng Nơ-ron Hồi quy Bộ nhớ dài-ngắn (PyTorch LSTM)

Mạng LSTM (Long Short-Term Memory) được thiết kế chuyên biệt để học các phụ thuộc chuỗi ngắn hạn và dài hạn thông qua trạng thái ô nhớ (Cell State - c_t) và ba cổng điều khiển phi tuyến tại mỗi bước thời gian t với đầu vào x_t và trạng thái ẩn trước đó h_{t-1}:

1. Cổng quên (Forget Gate): f_t = sigma(W_f * [h_{t-1}, x_t] + b_f), quyết định tỷ lệ thông tin quá khứ trong c_{t-1} cần giữ lại hay loại bỏ (với sigma là hàm Sigmoid có miền giá trị [0, 1]).

2. Cổng đầu vào (Input Gate) và Trạng thái ứng viên: i_t = sigma(W_i * [h_{t-1}, x_t] + b_i) và tilde{c}_t = tanh(W_c * [h_{t-1}, x_t] + b_c), quyết định lượng thông tin biến động giá mới tại thời điểm t được nạp vào bộ nhớ.

3. Cập nhật trạng thái ô nhớ dài hạn: c_t = f_t (x) c_{t-1} + i_t (x) tilde{c}_t (với (x) là phép nhân từng phần tử Hadamard).

4. Cổng đầu ra (Output Gate) và Trạng thái ẩn mới: o_t = sigma(W_o * [h_{t-1}, x_t] + b_o) và h_t = o_t (x) tanh(c_t).

Trạng thái ẩn ở bước cuối cùng của cửa sổ trượt độ dài L (h_L) được đưa qua tầng kết nối đầy đủ (Fully Connected Linear Layer): hat{y}_{t+1} = W_{fc} * h_L + b_{fc} để sinh ra giá trị dự báo đã chuẩn hóa Min-Max, sau đó biến đổi ngược (Inverse Transform) về đơn vị tiền tệ VNĐ thực tế.


### 2.2.6. So sánh đặc tính toán học, ưu điểm và giới hạn của 5 mô hình học máy trong dự án

Việc tích hợp đồng thời cả 5 mô hình thuộc 3 trường phái toán học khác nhau (Thống kê kinh tế lượng: ARIMA; Phân rã hàm cộng tính chu kỳ: Prophet; Học máy tổ hợp cây quyết định: Random Forest, XGBoost; và Mạng nơ-ron học sâu: LSTM) tạo nên một hệ thống dự báo đa mô hình bổ trợ lẫn nhau hoàn hảo. Bảng 2.1 tổng hợp đối sánh chi tiết cơ chế toán học, ưu điểm và giới hạn của từng mô hình khi áp dụng vào dữ liệu giá nông sản Việt Nam.


**Bảng 2.1. Đối sánh đặc tính kỹ thuật, ưu điểm và giới hạn của 5 mô hình dự báo trong hệ thống AgroForecast**

| Mô hình AI | Nhóm thuật toán | Cơ chế toán học cốt lõi | Ưu điểm nổi bật trên giá nông sản | Giới hạn & Điều kiện áp dụng tốt nhất |
| --- | --- | --- | --- | --- |
| ARIMA | Thống kê tuyến tính (Box-Jenkins) | Kết hợp tự hồi quy AR(p), sai phân I(d) và trung bình trượt sai số MA(q) | Rất chính xác và ít quá khớp trên chuỗi giá biến động hẹp, ổn định ngắn hạn (như Lúa IR50404) | Giả định quan hệ tuyến tính; phản ứng chậm trước các cú sốc phi tuyến đột ngột |
| Prophet | Mô hình cộng tính tổng quát (GAM) | Phân rã hàm xu thế gãy khúc g(t) + chuỗi lượng giác Fourier mùa vụ s(t) | Xử lý tự động ngày nghỉ/khuyết dữ liệu; trực quan hóa tốt tính mùa vụ thu hoạch hàng năm | Khi chuỗi ngắn hoặc có bước nhảy giá dốc đứng ở cuối chuỗi dễ bị phóng đại độ dốc xu thế |
| Random Forest | Học máy tổ hợp (Bagging Trees) | Trung bình cộng dự báo của B = 120 cây quyết định độc lập huấn luyện trên mẫu Bootstrap | Phương sai sai số thấp, kháng nhiễu và điểm ngoại lai rất tốt, không bị bùng nổ dự báo | Không thể ngoại suy vượt ra ngoài miền giá trị cực đại/cực tiểu đã từng xuất hiện trong quá khứ |
| XGBoost | Học máy tăng cường (Gradient Boosting) | Xây dựng chuỗi cây nối tiếp sửa sai số dư bằng đạo hàm bậc hai (Hessian) + điều chuẩn L1/L2 | Bắt nhịp cực nhạy với biến động mạnh và đảo chiều xu hướng (đứng số 1 trên Cà phê & Hồ tiêu) | Cần trích xuất đầy đủ đặc trưng độ trễ (Lag) và động lượng (Momentum) chất lượng cao |
| PyTorch LSTM | Học sâu chuỗi thời gian (Deep RNN) | Ô nhớ dài hạn Cell State kết hợp 3 cổng Sigmoid/Tanh (Forget, Input, Output Gate) | Học được các mẫu hình chu kỳ phi tuyến mượt mà dài hạn (đứng số 1 trên Dâu tây, Khoai tây, Điều) | Đòi hỏi chuẩn hóa Min-Max chặt chẽ và thời gian tính toán huấn luyện cao hơn ARIMA/Trees |



## 2.3. Các độ đo đánh giá chất lượng mô hình và ước lượng khoảng tin cậy


### 2.3.1. Bốn chỉ số đánh giá sai số chuẩn: MAE, RMSE, MAPE và hệ số xác định R2

Để đánh giá khách quan và toàn diện chất lượng dự báo của 5 mô hình học máy trên tập dữ liệu kiểm thử gồm n quan sát {y_1, y_2, ..., y_n} và chuỗi giá dự báo tương ứng {hat{y}_1, hat{y}_2, ..., hat{y}_n}, hệ thống AgroForecast tính toán đồng thời 4 độ đo chuẩn mực sau:

1. Sai số tuyệt đối trung bình (Mean Absolute Error - MAE): MAE = (1 / n) * sum_{i=1..n} |y_i - hat{y}_i|. Chỉ số MAE có cùng đơn vị với giá nông sản (VNĐ/kg hoặc VNĐ/tấn), cho biết trung bình mỗi ngày mô hình dự báo lệch bao nhiêu đồng so với giá thực tế tại vườn.

2. Sai số bình phương trung bình căn bậc hai (Root Mean Square Error - RMSE): RMSE = sqrt( (1 / n) * sum_{i=1..n} (y_i - hat{y}_i)^2 ). Do bình phương sai số trước khi lấy trung bình, RMSE phạt nặng các sai số lớn đột biến, được dùng làm tiêu chuẩn chính để xếp hạng mô hình tối ưu nhất và tính toán bề rộng dải tin cậy.

3. Sai số phần trăm tuyệt đối trung bình (Mean Absolute Percentage Error - MAPE): MAPE = (100% / n) * sum_{i=1..n} |(y_i - hat{y}_i) / y_i|. Do không phụ thuộc vào đơn vị tiền tệ, MAPE cho phép so sánh trực tiếp độ chính xác dự báo giữa mặt hàng giá vài nghìn đồng (như Lúa 6.850 đ/kg) với mặt hàng giá trên trăm nghìn đồng (như Hồ tiêu 129.100 đ/kg). Theo chuẩn phân loại của Lewis (1982): MAPE < 10% là dự báo có độ chính xác rất cao (Highly Accurate); 10% <= MAPE < 20% là dự báo tốt (Good); 20% <= MAPE < 50% là dự báo hợp lý (Reasonable).

4. Hệ số xác định (Coefficient of Determination - R2): R2 = 1 - [ sum_{i=1..n} (y_i - hat{y}_i)^2 / sum_{i=1..n} (y_i - bar{y})^2 ]. Nhờ áp dụng kiểm định Walk-Forward cuộn 7 ngày trên cửa sổ 66–90 phiên cuối cùng thay vì cửa sổ ngắn hẹp, toàn bộ 40/40 mô hình trên 8 mặt hàng của AgroForecast đều đạt hệ số R2 dương thực nghiệm (0,2536 đến 0,8972), kết hợp RMSE và MAPE để đánh giá toàn diện năng lực dự báo.


### 2.3.2. Phương pháp kiểm định Walk-Forward Holdout Validation và Cổng chặn sai số (Threshold Gate)

Nhằm ngăn chặn tuyệt đối hiện tượng rò rỉ dữ liệu tương lai (Data Leakage), mô-đun huấn luyện của hệ thống (app/services/training_service.py) tách chuỗi lịch sử có độ dài N ngày thành hai phần nghiêm ngặt theo thứ tự thời gian: Tập huấn luyện (Training Set) gồm N - H ngày đầu tiên (từ t = 1 đến t = N - H) và Tập kiểm thử giữ lại (Holdout Test Set) gồm H = min(14, max(5, floor(N / 6))) ngày cuối cùng. Các mô hình chỉ được học trên Tập huấn luyện, sau đó dự báo đệ quy H bước tới để đo lường MAE, RMSE, MAPE, R2 và đối sánh trực tiếp với mô hình cơ sở Naive Persistence (dự báo giá ngày mai bằng giá hôm nay).

Bên cạnh đó, lớp ModelTrainer (trong ml_pipeline/model_trainer.py) cài đặt cơ chế Cổng chặn sai số (Threshold Gate): một mô hình sau khi huấn luyện chỉ được chấp nhận xuất bản (passed_threshold = True) nếu tỷ lệ RMSE trên mức giá trung bình thỏa mãn điều kiện: (RMSE / mean_price) <= max_rmse_threshold_ratio. Sau khi vượt qua bước kiểm định, mô hình mới được huấn luyện lại trên toàn bộ N quan sát mới nhất để sinh chuỗi dự báo 30 ngày tương lai phục vụ người dùng.


### 2.3.3. Mô hình hóa khoảng tin cậy 95% (CI) và hiệu chỉnh giá địa phương (Spatio-Temporal Basis Spread)

Một điểm dự báo đơn lẻ (Point Forecast) không phản ánh hết rủi ro biến động thị trường. Do đó, tại bước dự báo tương lai h (h = 1, 2, ..., 30), hệ thống AgroForecast ước lượng dải khoảng tin cậy 95% mở rộng dần theo căn bậc hai của kỳ hạn dự báo hoặc theo độ lệch chuẩn sai số kiểm định RMSE: Margin_h = 1.96 * RMSE, từ đó xác định cận dưới (Lower Confidence Bound): LowerCI_{t+h} = max(0, hat{y}_{t+h} - 1.96 * RMSE) và cận trên (Upper Confidence Bound): UpperCI_{t+h} = hat{y}_{t+h} + 1.96 * RMSE.

Khi người dùng chọn một địa phương bán tại vườn/ruộng cụ thể r có độ lệch giá cơ sở Delta_r (Basis Spread), mô hình không gian - thời gian tại app/services/forecast_service.py thực hiện phép biến đổi đồng nhất trên cả chuỗi lịch sử, chuỗi dự báo trung tâm và hai biên của dải tin cậy: hat{y}_{t+h}^{(r)} = max(0, hat{y}_{t+h}^{(0)} + Delta_r), LowerCI_{t+h}^{(r)} = max(0, LowerCI_{t+h}^{(0)} + Delta_r), và UpperCI_{t+h}^{(r)} = max(0, UpperCI_{t+h}^{(0)} + Delta_r). Phép biến đổi này bảo toàn tính chất bất biến của bất đẳng thức: LowerCI_{t+h}^{(r)} <= hat{y}_{t+h}^{(r)} <= UpperCI_{t+h}^{(r)} tại mọi địa phương.


### 2.3.4. Phân tích toán học về tính ổn định của dự báo đệ quy đa bước (Multi-step Recursive Stability)

Trong bài toán dự báo giá nông sản với kỳ hạn H bước tương lai (H = 7, 10, 14, 30 ngày), việc sử dụng chiến lược dự báo đệ quy (Recursive Strategy) đồng nghĩa với việc đầu ra dự báo hat{y}_{t+1} ở bước 1 lại trở thành biến đầu vào trễ lag_1 cho bước dự báo t+2. Nếu một mô hình học máy có hệ số khuếch đại sai số lớn hơn 1 (tức |d hat{y}_{t+1} / d y_t| > 1), sai số nhỏ ở bước đầu sẽ tích lũy theo cấp số nhân và gây ra hiện tượng trôi dạt dự báo (Forecast Drift) ở ngày thứ 14 đến ngày thứ 30.

Để kiểm soát chặt chẽ hiện tượng này trong hệ thống AgroForecast, ba kỹ thuật ổn định hóa toán học đã được áp dụng đồng thời trong mô-đun app/services/training_service.py: (1) Đối với mô hình ARIMA(2,1,1), nghiệm của đa thức đặc trưng tự hồi quy 1 - phi_1*z - phi_2*z^2 = 0 luôn nằm ngoài vòng tròn đơn vị (|z| > 1), đảm bảo dự báo xa hội tụ mượt mà về đường xu thế cân bằng; (2) Đối với Random Forest và XGBoost, độ sâu tối đa của cây được giới hạn ở mức max_depth = 4..6 kết hợp cập nhật trung bình trượt động (rolling_mean_7d, rolling_mean_14d) tại mỗi bước lặp đệ quy h = 1..H, giúp kéo quỹ đạo dự báo bám sát dải trung bình động lịch sử; và (3) Đối với mạng học sâu LSTM, việc chuẩn hóa chuỗi vào đoạn [-1, 1] và sử dụng hàm kích hoạt bão hòa hai đầu tanh() giúp chặn trên và chặn dưới biên độ dự báo một cách tự nhiên.

Bên cạnh đó, để người dùng đánh giá minh bạch giá trị gia tăng của từng mô hình học máy, mọi phiên huấn luyện đều tính toán song song sai số của mô hình Ngây thơ (Naive Persistence Baseline: hat{y}_{t+h} = y_t). Tỷ số cải thiện kỹ năng dự báo (Forecast Skill Score) được xác định bởi công thức: Skill = 1 - (RMSE_model / RMSE_naive). Khi Skill > 0, mô hình học máy chứng minh được năng lực dự báo vượt trội hơn việc giả định giá không đổi.


## 2.4. Cơ sở công nghệ phát triển hệ thống và tiêu chuẩn bảo mật OWASP Top 10


### 2.4.1. Kiến trúc Backend RESTful API với FastAPI, SQLAlchemy ORM và PostgreSQL

Hệ thống Backend được phát triển bằng ngôn ngữ Python 3.11 trên nền tảng framework FastAPI hiệu năng cao. FastAPI sử dụng chuẩn ASGI (Asynchronous Server Gateway Interface) thông qua máy chủ Uvicorn kết hợp thư viện Pydantic v2 viết bằng Rust để kiểm tra kiểu dữ liệu (Data Validation & Serialization) tự động cho mọi gói tin JSON đầu vào và đầu ra.

Tầng lưu trữ dữ liệu sử dụng hệ quản trị cơ sở dữ liệu quan hệ PostgreSQL kết hợp bộ ánh xạ quan hệ hướng đối tượng SQLAlchemy ORM 2.0. Việc truy vấn dữ liệu thông qua biểu thức đối tượng của SQLAlchemy ORM giúp hệ thống tự động biên dịch thành các câu lệnh truy vấn tham số hóa (Parameterized Queries), vừa tối ưu hóa hiệu năng qua bộ nhớ đệm kết nối (Connection Pooling) vừa triệt tiêu nguy cơ tấn công tiêm mã lệnh SQL (SQL Injection).


### 2.4.2. Kiến trúc Frontend hiện đại với Next.js 14, TypeScript và Recharts

Phân hệ giao diện người dùng (Frontend) được xây dựng trên nền tảng Next.js 14 (App Router) kết hợp React 18 và ngôn ngữ định kiểu tĩnh TypeScript. Việc sử dụng TypeScript đảm bảo mọi cấu trúc dữ liệu nhận về từ REST API (như điểm dự báo ForecastPoint, chỉ số sai số ModelMetrics, thông tin vùng RegionInfo) đều được kiểm tra tính tương thích kiểu ngay từ lúc biên dịch (Compile-time Type Safety).

Hệ thống biểu đồ phân tích chuỗi thời gian được xây dựng bằng thư viện đồ họa véc-tơ SVG Recharts (ComposedChart kết hợp Line và Area) với thuật toán tự động tính toán miền giá trị trục tung động (Dynamic Y-Axis Domain Scaling) và cầu nối liền mạch (Bridge Point Connection) giữa điểm lịch sử cuối cùng với đường dự báo đứt nét và vùng bóng dải tin cậy 95%.


### 2.4.3. Cơ sở lý thuyết về Kiểm thử phần mềm và Bảo mật ứng dụng Web theo OWASP Top 10

Về kiểm thử phần mềm, dự án áp dụng mô hình Kim tự tháp Kiểm thử (Testing Pyramid) kết hợp phương pháp kiểm thử hộp trắng (White-box), hộp xám (Grey-box) và hộp đen (Black-box). Mọi kịch bản kiểm thử tự động được vận hành độc lập trên cơ sở dữ liệu ảo trong bộ nhớ RAM (SQLite In-Memory Sandbox) thông qua cơ chế Dependency Override của FastAPI.

Về an toàn bảo mật thông tin, hệ thống tuân thủ danh mục 10 rủi ro bảo mật ứng dụng Web nghiêm trọng nhất của tổ chức OWASP (OWASP Top 10), bao gồm: Kiểm soát truy cập hỏng (A01 - Broken Access Control) được giải quyết bằng phân quyền RBAC nghiêm ngặt; Lỗi mật mã học (A02 - Cryptographic Failures) được giải quyết bằng thuật toán băm mật khẩu một chiều Bcrypt kèm Salt ngẫu nhiên và chữ ký số JWT HS256; Lỗi tiêm mã độc (A03 - Injection) được phòng vệ bằng SQLAlchemy ORM, hàm làm sạch HTML/XSS sanitize_text() và hàm chống tiêm công thức bảng tính sanitize_csv_cell(); Thiết kế thiếu an toàn & Lỗi xác thực (A04 & A07) được bảo vệ bằng thuật toán giới hạn tần suất truy cập cửa sổ trượt (Sliding Window Rate Limiter); và Cấu hình bảo mật sai (A05 - Security Misconfiguration) được gia cố bằng lớp trung gian SecurityHeadersMiddleware gắn 7 tiêu đề HTTP bảo mật chuẩn quốc tế.


### 2.4.4. Phân tích kỹ thuật các mô-đun thu thập và bóc tách dữ liệu nguồn Việt Nam (ml_pipeline/)

Để đảm bảo dữ liệu lịch sử giá của 8 mặt hàng nông sản phản ánh trung thực thị trường Việt Nam, tầng thu thập dữ liệu trong thư mục backend/ml_pipeline/ được thiết kế thành 4 mô-đun chuyên biệt đi kèm cơ chế kiểm tra chéo nghiêm ngặt:

1. Mô-đun Danh mục Nguồn Chuẩn (ml_pipeline/source_catalog.py): Định nghĩa từ điển hằng số SOURCES ánh xạ từng mã nông sản (RICE_IR504, COFFEE_ROBUSTA, PEPPER_BLACK, SUGARCANE, STRAWBERRY, SWEET_POTATO, POTATO, CASHEW_NUT) với cấu hình thu thập gồm: loại tần suất (kind: daily, irregular, periodic), tên cơ quan công bố (source_name), đường dẫn URL gốc (source_url), chợ/vùng khảo sát (market), loại giá (price_type: Bán tại hộ / Tại vườn / Tại ruộng), đơn vị tiền tệ chuẩn (VNĐ/kg hoặc VNĐ/tấn) và mốc ngày bắt đầu thu thập gợi ý (suggested_start).

2. Mô-đun Bóc tách Lịch sử AGROINFO (ml_pipeline/agro_history.py): Chịu trách nhiệm phân tích cú pháp bảng HTML từ hệ thống thông tin giá nông sản của Viện Chính sách và Chiến lược Phát triển Nông nghiệp Nông thôn. Hàm parse_page() kiểm tra chặt chẽ đủ 4 điều kiện trên từng dòng bảng: khớp đúng tên mặt hàng, khớp đúng khu vực chợ khảo sát, khớp đúng loại giá (ví dụ 'Bán tại hộ') và đơn vị tiền tệ ('VNĐ/kg'). Đồng thời, bộ phân trang tự động kiểm tra chữ ký nội dung trang để phát hiện và dừng ngay lập tức nếu máy chủ nguồn trả về trang lặp lại, ngăn chặn vòng lặp vô hạn.

3. Mô-đun Bóc tách Giá Nội địa Hàng ngày (ml_pipeline/domestic_sources.py & observation_scraper.py): Chuyên xử lý các bản tin giá cà phê nhân xô và hồ tiêu đen nội địa. Bộ phân tích sử dụng biểu thức chính quy chuẩn hóa để trích xuất mức giá giao dịch theo từng tỉnh/huyện, đối chiếu ngày công bố thực tế trên bài viết với ngày mục tiêu cần thu thập (nếu sai lệch ngày công bố sẽ từ chối ghi nhận để chống sai lệch thời gian) và tự động khử trùng lặp (Deduplication) theo khóa (commodity_id, record_date).

4. Mô-đun Bóc tách Báo cáo Định kỳ (ml_pipeline/periodic_reports.py): Chuyên xử lý các bản tin tổng hợp theo tuần/kỳ (như báo cáo giá mía đường và tổng hợp thị trường). Điểm đặc biệt trong thiết kế của mô-đun này là bảo toàn nguyên vẹn khoảng thời gian của kỳ báo cáo (period_start, period_end), mức giá mua (buying_price) và mức giá bán (selling_price) vào bảng riêng periodic_prices, tuyệt đối không tự ý nội suy giả tạo từ báo cáo tuần thành dữ liệu từng ngày.


### 2.4.5. Cơ sở lý thuyết về Mã băm Mật mã SHA-256 và Quản trị Nguồn gốc Dữ liệu (Data Provenance)

Trong các hệ thống học máy vận hành thực tế (MLOps), một trong những rủi ro nghiêm trọng nhất là sự mất đồng bộ giữa tập dữ liệu lịch sử đang hiển thị và mô hình dự báo đã huấn luyện trước đó (Model-Data Drift & Stale Predictions). Để giải quyết bài toán này ở cấp độ mật mã học, hệ thống AgroForecast ứng dụng hàm băm mật mã một chiều SHA-256 (Secure Hash Algorithm 256-bit thuộc họ SHA-2 do NIST chuẩn hóa) kết hợp mô hình trạng thái nguồn gốc dữ liệu ba mức (Three-tier Data Provenance).

Hàm băm SHA-256 ánh xạ một thông điệp đầu vào M có độ dài bất kỳ thành một chuỗi bit cố định 256-bit (biểu diễn dưới dạng 64 ký tự thập lục phân): H = SHA256(M). SHA-256 thỏa mãn ba tính chất toán học cốt lõi: (1) Tính tiền ảnh thứ nhất (Pre-image Resistance): không thể suy ngược lại tập dữ liệu gốc từ mã băm H; (2) Tính kháng va chạm mạnh (Strong Collision Resistance): xác suất tìm được hai chuỗi lịch sử giá khác nhau M_1 != M_2 có cùng mã băm SHA256(M_1) == SHA256(M_2) là xấp xỉ 2^{-128} (bằng 0 trên thực tế); và (3) Hiệu ứng thác đổ (Avalanche Effect): chỉ cần một điểm giá lịch sử thay đổi 1 đồng hoặc trạng thái provenance thay đổi từ 'unverified' sang 'reviewed', trên 50% số bit trong mã băm SHA-256 sẽ thay đổi hoàn toàn. Nhờ đó, trường dataset_hash trong bảng training_runs đóng vai trò như một 'con dấu niêm phong điện tử' bảo vệ tính toàn vẹn tuyệt đối của mọi đường dự báo trên giao diện.


### 2.4.6. Cơ sở toán học của Thuật toán Giới hạn Tần suất Cửa sổ Trượt (Sliding Window Rate Limiting) và Bcrypt

Để bảo vệ các cổng API xác thực (/api/v1/auth/login, /register) trước các cuộc tấn công dò mật khẩu tự động (Brute-Force / Credential Stuffing) và bảo vệ các cổng kích hoạt huấn luyện AI trước tấn công làm cạn kiệt tài nguyên (Denial of Service - DoS), hệ thống cài đặt thuật toán Cửa sổ trượt theo dấu thời gian (Sliding Window Log Rate Limiter) tại lớp RateLimiter trong tệp app/core/security.py.

Gọi W là độ rộng cửa sổ thời gian (tính bằng giây, ví dụ W = 60s) và R_max là số lượng yêu cầu tối đa cho phép trong một cửa sổ (ví dụ R_max = 25 đối với đăng nhập và R_max = 10 đối với tác vụ nặng). Với mỗi khóa định danh khách hàng k (địa chỉ IP hoặc định danh người dùng), hệ thống duy trì một danh sách có thứ tự các mốc thời gian gửi yêu cầu T_k = [t_1, t_2, ..., t_m]. Khi có một yêu cầu mới đến tại thời điểm hiện tại t_now, thuật toán thực hiện bước lọc cửa sổ trượt trong miền khóa đồng bộ luồng (Thread Lock): T'_k = { t_i in T_k | t_now - t_i < W }. Nếu lực lượng của tập hợp |T'_k| >= R_max, yêu cầu bị từ chối ngay lập tức với mã trạng thái HTTP 429 Too Many Requests; ngược lại, t_now được chèn vào cuối danh sách T'_k và yêu cầu được chuyển tiếp xuống tầng xử lý nghiệp vụ. So với thuật toán Cửa sổ cố định (Fixed Window Counter), thuật toán Cửa sổ trượt khắc phục hoàn toàn lỗ hổng gửi dồn gấp đôi lưu lượng (2 * R_max) tại thời điểm giao nhau giữa hai phút.

Song song với Rate Limiting, mật khẩu người dùng được bảo vệ bằng hàm dẫn xuất khóa thích nghi Bcrypt dựa trên mật mã khối Blowfish (Eksblowfish - Expensive Key Schedule Blowfish). Với tham số chi phí (cost factor / work factor) c = 12, thuật toán thực hiện 2^{12} = 4.096 vòng biến đổi khóa phức tạp kết hợp một chuỗi Salt ngẫu nhiên 128-bit (16 byte, mã hóa Base64 thành 22 ký tự trong định dạng chuẩn $2b$12$<22-char-salt><31-char-hash>). Do tiêu tốn khoảng 200 - 300 mili-giây CPU cho mỗi lần kiểm tra mật khẩu, Bcrypt làm giảm tốc độ dò mật khẩu bằng GPU của kẻ tấn công đi hàng chục nghìn lần so với các hàm băm nhanh thông thường như MD5 hay SHA-1.


# Chương 3: PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG AGROFORECAST


## 3.1. Phân tích yêu cầu hệ thống


### 3.1.1. Xác định các tác nhân (Actors) và ma trận phân quyền vai trò (RBAC)

Hệ thống AgroForecast được thiết kế để phục vụ ba nhóm tác nhân người dùng chính trong hệ sinh thái nông nghiệp Việt Nam, được quản lý thông qua cơ chế Kiểm soát truy cập dựa trên vai trò (Role-Based Access Control - RBAC) tại mô-đun app/core/deps.py:

1. Nông hộ, Thương lái và Nhà đầu tư (Vai trò User / Guest): Là những người trực tiếp sản xuất nông sản tại vườn/ruộng hoặc thu mua nông sản tại địa phương. Họ có nhu cầu tra cứu bảng giá bán tại vườn hôm nay của 8 mặt hàng chủ lực theo 33 tỉnh/thành phố, xem biểu đồ dự báo biến động giá theo 3 kỳ hạn chuẩn (7 ngày, 14 ngày và 30 ngày tới), xem đối sánh sai số giữa 5 mô hình AI, tải báo cáo dự báo định dạng Excel/CSV và đăng ký nhận cảnh báo tự động qua Email khi giá vượt ngưỡng mong muốn.

2. Chuyên viên Phân tích Thị trường (Vai trò Analyst): Ngoài toàn bộ quyền tra cứu của User, chuyên viên phân tích được phép truy cập bảng thống kê hệ thống, tra cứu nhật ký thu thập dữ liệu của Bot Scraper, xem toàn bộ lịch sử giá bao gồm cả các bản ghi đang chờ xác minh (unverified) và xuất tập tin dữ liệu lịch sử phục vụ công tác kiểm định chất lượng dữ liệu.

3. Quản trị viên Hệ thống (Vai trò Admin): Là người có thẩm quyền cao nhất trong hệ thống, chịu trách nhiệm quản lý danh mục nông sản (CRUD), nhập bổ sung hoặc hiệu chỉnh điểm giá thủ công kèm lưu vết lịch sử chỉnh sửa (Price Revisions), nhập dữ liệu hàng loạt từ file CSV, kích hoạt tác vụ ngầm thu thập dữ liệu (Scrape Task) và huấn luyện lại 5 mô hình học máy (Retrain Task), chuyển đổi mô hình AI mặc định của hệ thống và quản lý tài khoản người dùng (cấp quyền, khóa/mở khóa tài khoản).


**Bảng 3.1. Ma trận phân quyền truy cập chức năng theo vai trò người dùng (RBAC Matrix)**

| Mã chức năng | Tên nhóm chức năng nghiệp vụ | Khách / Nông hộ (User) | Chuyên viên (Analyst) | Quản trị viên (Admin) |
| --- | --- | --- | --- | --- |
| UC-01 | Tra cứu tổng quan thị trường & giá bán tại vườn theo huyện | Cho phép | Cho phép | Cho phép |
| UC-02 | Phân tích & Dự báo AI 5 mô hình (7, 14, 30 ngày) + XAI | Cho phép | Cho phép | Cho phép |
| UC-03 | Tra cứu lịch sử giá đã xác minh & Xuất báo cáo CSV | Cho phép | Cho phép | Cho phép |
| UC-04 | Đối sánh tương quan biến động giá đa nông sản | Cho phép | Cho phép | Cho phép |
| UC-05 | Tạo, bật/tắt, xóa và gửi thử quy tắc cảnh báo giá Email | Cho phép | Cho phép | Cho phép |
| UC-06 | Đăng ký tài khoản, Đăng nhập JWT và Xem hồ sơ cá nhân | Cho phép | Cho phép | Cho phép |
| UC-07 | Xem thống kê hệ thống, tiến trình tác vụ nền & nhật ký Scraper | Từ chối (403) | Cho phép | Cho phép |
| UC-08 | Quản lý danh mục nông sản (Thêm, Sửa, Xóa nông sản) | Từ chối (403) | Từ chối (403) | Cho phép |
| UC-09 | Cập nhật giá thủ công, duyệt nguồn (Reviewed) & Nhập CSV | Từ chối (403) | Từ chối (403) | Cho phép |
| UC-10 | Kích hoạt Bot thu thập dữ liệu (Scrape) & Huấn luyện lại AI (Retrain) | Từ chối (403) | Từ chối (403) | Cho phép |
| UC-11 | Cấu hình mô hình AI mặc định & Quản lý tài khoản người dùng | Từ chối (403) | Từ chối (403) | Cho phép |



### 3.1.2. Đặc tả chi tiết các yêu cầu chức năng cốt lõi

Hệ thống được phân rã thành 6 phân hệ chức năng chính liên kết chặt chẽ với nhau:

Phân hệ 1 - Tổng quan thị trường giá nông sản bán tại vườn (Market Overview): Hiển thị dải chỉ số độ rộng thị trường (số mặt hàng tăng, giảm, đi ngang, mặt hàng tăng trưởng mạnh nhất), thanh tìm kiếm và lọc nhanh theo nhóm nông sản hoặc địa phương, lưới thẻ nông sản (Commodity Cards) kèm đồ thị thu nhỏ (Sparkline 7 ngày) và bảng khảo sát giá bán tại vườn theo địa phương.

Phân hệ 2 - Phân tích và Dự báo giá nông sản bằng 5 mô hình AI (AI Forecast & Spatio-Temporal Dashboard): Cho phép người dùng lựa chọn linh hoạt giữa 8 mặt hàng nông sản, 5 thuật toán học máy (LSTM, Prophet, ARIMA, XGBoost, Random Forest), 4 kỳ hạn dự báo (7, 10, 14, 30 ngày) và danh sách các huyện bán tại vườn/ruộng tương ứng. Hệ thống hiển thị dải 4 chỉ số tổng hợp (Giá bán tại vườn hiện tại, Giá dự báo cuối kỳ kèm tỷ lệ % thay đổi, Biên độ dao động cuối kỳ theo khoảng tin cậy 95%, và Sai số mô hình MAPE kèm gợi ý tự động mô hình có sai số thấp nhất), biểu đồ kết hợp đường thực tế liền nét với đường dự báo đứt nét và vùng bóng CI 95%, mô-đun Giải thích mô hình (Explainable AI - XAI Feature Drivers), biểu đồ so sánh sai số giữa 5 mô hình và bảng lịch trình giá dự báo chi tiết từng ngày có hỗ trợ tải xuống CSV.

Phân hệ 3 - Quản lý lịch sử biến động giá và Kiểm chứng nguồn gốc (Historical Observations & Provenance): Cho phép lọc chuỗi giá lịch sử theo khoảng ngày tùy chọn (30 ngày, 90 ngày, 1 năm hoặc toàn bộ lịch sử), hiển thị rõ siêu dữ liệu nguồn công bố (tên cơ quan công bố, đường dẫn gốc URL để đối chiếu, loại giá bán tại hộ/vườn, quy cách), thống kê số ngày khuyết dữ liệu (missing dates) và trạng thái sẵn sàng cho huấn luyện học máy (Model Readiness).

Phân hệ 4 - Đối sánh tương quan thị trường (Market Comparison): Trực quan hóa đường cong tăng trưởng chuẩn hóa giữa các nhóm nông sản chủ lực trên cùng một hệ trục tọa độ và bảng đối sánh biên độ giá sàn - giá trần tại từng địa phương.

Phân hệ 5 - Cảnh báo biến động giá tự động (Automated Price Alerts): Cho phép thiết lập các quy tắc cảnh báo theo điều kiện giá vượt lên trên ngưỡng (PRICE_ABOVE) hoặc tụt xuống dưới ngưỡng (PRICE_BELOW), tự động đối chiếu khi có dữ liệu giá mới, gửi thông báo qua giao thức SMTP Email và lưu vết lịch sử kích hoạt cảnh báo (Audit Trail).

Phân hệ 6 - Quản trị hệ thống và Điều phối đường ống ML (Admin Control Center): Cung cấp công cụ quản trị toàn diện cho Admin để nhập/xuất CSV, điều chỉnh điểm giá kèm lưu trữ phiên bản cũ vào bảng price_revisions, theo dõi tiến trình ngầm (Background Jobs) của Bot thu thập dữ liệu và bộ huấn luyện 5 mô hình AI theo thời gian thực.


### 3.1.3. Đặc tả các yêu cầu phi chức năng (Hiệu năng, Toàn vẹn dữ liệu và Bảo mật)

Về hiệu năng phản hồi (Performance & Latency): Hệ thống cài đặt bộ nhớ đệm dự báo trong RAM (In-Memory Prediction Cache tại ml_pipeline/predictor.py) với thời gian sống TTL = 15 phút kết hợp lưu trữ sẵn kết quả dự báo đã kiểm định trong bảng forecasts của PostgreSQL, đảm bảo thời gian phản hồi API dự báo đạt dưới 50 ms cho các truy vấn lặp lại.

Về tính toàn vẹn dữ liệu học máy (Data Integrity & Anti-Tampering): Mọi phiên huấn luyện trong bảng training_runs đều tính toán và lưu trữ chữ ký băm mật mã SHA-256 (dataset_hash) của toàn bộ chuỗi lịch sử đầu vào thông qua hàm fingerprint(). Khi người dùng yêu cầu hiển thị dự báo hoặc khi có bất kỳ điểm giá lịch sử nào bị chỉnh sửa, hệ thống lập tức đối chiếu lại chữ ký SHA-256; nếu dữ liệu lịch sử đã thay đổi mà mô hình chưa được huấn luyện lại, hệ thống sẽ cảnh báo minh bạch (HTTP 409 Conflict) thay vì hiển thị dự báo cũ không còn khớp với thực tế.

Về độ tin cậy và an toàn bảo mật: Hệ thống phải vượt qua 100% kịch bản kiểm thử tự động (72/72 bài kiểm thử Pytest) và đáp ứng đầy đủ các tiêu chuẩn phòng vệ OWASP Top 10 trước các cuộc tấn công giả mạo JWT, leo thang đặc quyền RBAC, SQL Injection, Stored/Reflected XSS, CSV Formula Injection và tấn công vét cạn mật khẩu Brute-Force.


### 3.1.4. Đặc tả chi tiết Ca sử dụng UC-01: Tra cứu Tổng quan Thị trường và Giá bán tại vườn theo Địa phương

1. Tác nhân chính (Primary Actor): Nông hộ sản xuất, Thương lái thu mua, Nhà phân phối và Khách vãng lai (Guest / User). 2. Điều kiện tiên quyết (Pre-conditions): Máy chủ cơ sở dữ liệu PostgreSQL và máy chủ ứng dụng FastAPI đang hoạt động trực tuyến; bảng commodities và price_history đã có dữ liệu lịch sử của 8 mặt hàng nông sản chủ lực. 3. Điều kiện hoàn tất (Post-conditions): Giao diện hiển thị chính xác mức giá bán tại vườn/ruộng mới nhất, tỷ lệ phần trăm biến động so với phiên liền trước, đồ thị xu hướng 7 ngày gần nhất (Sparkline) và bảng khảo sát giá chi tiết tại các huyện chuyên canh.

4. Luồng sự kiện chính (Main Success Scenario): Bước 1: Người dùng truy cập vào đường dẫn gốc của ứng dụng Web (http://localhost:3000/). Bước 2: Trình duyệt thực thi đồng thời hai lời gọi bất đồng bộ qua Promise.all([fetchCommoditiesOverview(), fetchMarketComparison()]) tới các cổng REST API GET /api/v1/commodities/overview và GET /api/v1/commodities/comparison, trong khi thành phần RegionalPriceTable gọi GET /api/v1/commodities/regional-prices. Bước 3: Tại tầng dịch vụ commodity_service.py, hệ thống truy vấn 7 bản ghi giá gần nhất (ORDER BY record_date DESC LIMIT 7) của từng mặt hàng nông sản từ 1 đến 8, đảo ngược chuỗi theo thứ tự thời gian tăng dần, tính toán mức chênh lệch phần trăm giữa hai ngày gần nhất theo công thức changePct = ((p_curr - p_prev) / p_prev) * 100 và định dạng chuỗi giá chuẩn dấu chấm phân tách hàng nghìn tiếng Việt. Bước 4: Giao diện nhận dữ liệu JSON, tính toán tức thời thống kê độ rộng thị trường (số mặt hàng tăng, số mặt hàng giảm, mức biến động bình quân toàn thị trường, mặt hàng tăng trưởng mạnh nhất) và kết xuất lưới thẻ CommodityCard cùng biểu đồ đối sánh Recharts. Bước 5: Người dùng sử dụng thanh tìm kiếm QuickSearchBar để lọc theo tên nông sản (ví dụ: 'Cà phê', 'Dâu tây'), chọn nhóm ngành hàng hoặc chọn lọc địa phương cấp huyện trong bảng giá vùng.

5. Luồng sự kiện thay thế và xử lý ngoại lệ (Alternative & Exception Flows): Trong trường hợp kết nối mạng tới máy chủ API bị gián đoạn tạm thời hoặc một mặt hàng mới được thêm vào nhưng chưa có bản ghi lịch sử giá trong bảng price_history, hệ thống tự động kích hoạt cơ chế dữ liệu dự phòng an toàn (Graceful Fallback) kèm hiển thị thông báo trạng thái đồng bộ trên thanh tiêu đề Header mà không làm gián đoạn giao diện người dùng.


### 3.1.5. Đặc tả chi tiết Ca sử dụng UC-02: Phân tích và Dự báo Giá Nông sản Đa Mô hình theo Huyện bán tại vườn

1. Tác nhân chính: Nông hộ, Thương lái, Chuyên viên phân tích và Quản trị viên. 2. Điều kiện tiên quyết: Chuỗi lịch sử giá đã xác minh (provenance thuộc 'collected' hoặc 'reviewed') của mặt hàng được chọn đạt độ dài tối thiểu theo quy định (60 ngày đối với chuỗi ngày, 30 mốc đối với chuỗi không đều, 24 kỳ đối với chuỗi định kỳ) và đã có bản ghi dự báo hợp lệ khớp chữ ký băm SHA-256 (dataset_hash) trong bảng training_runs và forecasts.

3. Luồng sự kiện chính: Bước 1: Người dùng điều hướng tới trang Phân tích & Dự báo AI (/forecast). Mặc định hệ thống nạp mặt hàng chủ lực Cà phê Robusta (commodity_id = 2), tự động kích hoạt mô hình tối ưu ★ (PyTorch Stacked LSTM), kỳ hạn dự báo chuẩn 14 ngày và ngữ cảnh vị trí đang chọn. Bước 2: Giao diện gửi đồng thời hai yêu cầu GET /api/v1/forecast?commodity_id=2&model_name=LSTM&days=14 và GET /api/v1/forecast/compare/2. Bước 3: Tại forecast_service.py, hàm get_forecast_dashboard() trích xuất 30 điểm lịch sử đã xác minh gần nhất, kiểm tra tính toàn vẹn SHA-256 giữa lịch sử hiện tại và phiên huấn luyện TrainingRun, truy vấn 14 điểm dự báo tương lai của mô hình được chọn, áp dụng hiệu chỉnh vùng miền Haversine / basisSpread vào chuỗi lịch sử, chuỗi dự báo trung tâm và hai biên của khoảng tin cậy Conformal 95% (lowerCI, upperCI). Bước 4: Giao diện tính toán điểm cầu nối (isBridgePoint) tại mốc lịch sử cuối cùng để nối liền mạch đường thực tế màu xanh lục với đường dự báo đứt nét màu xanh dương và hiển thị dải 4 chỉ số tổng hợp, mô-đun giải thích XAI, biểu đồ so sánh 5 mô hình cùng lưới AgroGrid chi tiết từng ngày. Bước 5: Người dùng chuyển đổi qua lại giữa 5 mô hình (LSTM, Prophet, ARIMA, XGBoost, Random Forest), chọn 3 kỳ hạn chuẩn (7, 14, 30 ngày — khóa cứng Literal[7, 14, 30]) hoặc chọn tỉnh/huyện bán tại vườn khác nhau và xuất bảng dự báo ra tập tin Excel/CSV an toàn.

4. Luồng xử lý ngoại lệ: Nếu dữ liệu lịch sử vừa được chỉnh sửa mà chưa chạy lại tiến trình huấn luyện (lệch mã băm SHA-256) hoặc chuỗi lịch sử chưa đủ điều kiện huấn luyện, Backend trả về mã trạng thái HTTP 409 Conflict kèm thông điệp giải thích rõ nguyên nhân; khi đó giao diện tự động chuyển sang chế độ hiển thị biểu đồ lịch sử đã xác minh (chartMode = 'history' hoặc 'periodic') để người dùng vẫn theo dõi được diễn biến giá quá khứ.


### 3.1.6. Đặc tả chi tiết Ca sử dụng UC-03 & UC-04: Quản lý Lịch sử Giá, Kiểm chứng Nguồn gốc và Đối sánh Thị trường

1. Luồng nghiệp vụ Tra cứu và Kiểm chứng Lịch sử Giá (UC-03 - Trang /history): Người dùng chọn mặt hàng nông sản từ danh sách 8 nguồn dữ liệu chính thống, chọn khoảng thời gian từ ngày bắt đầu (start_date) đến ngày kết thúc (end_date) hoặc sử dụng nút chọn nhanh (30 ngày, 90 ngày, 1 năm, Toàn bộ lịch sử). Hệ thống gọi API GET /api/v1/history trả về danh sách các bản ghi giá kèm nhãn nguồn gốc (Thu thập từ nguồn / Admin xác nhận / Chưa xác minh), danh sách các ngày khuyết dữ liệu (missing_dates) và đối tượng đánh giá chất lượng chuỗi (readiness). Người dùng có thể nhấp trực tiếp vào nút 'Kiểm tra nguồn' để mở đường dẫn URL gốc của cơ quan công bố (AGROINFO, VPSA, VSSA...) hoặc xuất toàn bộ dữ liệu lịch sử đang lọc ra tập tin CSV.

2. Luồng nghiệp vụ Đối sánh Tương quan Thị trường (UC-04 - Trang /compare): Hệ thống chuẩn hóa tốc độ tăng trưởng phần trăm của các mặt hàng nông sản về cùng một gốc so sánh, cho phép người dùng bật/tắt từng đường biểu diễn để phân tích sự dịch chuyển dòng tiền và tính đồng pha giữa nhóm cây công nghiệp xuất khẩu (Cà phê, Hồ tiêu, Hạt điều) với nhóm lương thực (Lúa gạo, Khoai lang, Khoai tây).


### 3.1.7. Đặc tả chi tiết Ca sử dụng UC-05 & UC-06: Cảnh báo Biến động Giá qua Email và Xác thực Phân quyền JWT

1. Luồng nghiệp vụ Cảnh báo Biến động Giá Tự động (UC-05 - Trang /alerts): Nông hộ hoặc thương lái nhập tên quy tắc cảnh báo (ví dụ: 'Bán cà phê khi giá vượt 120.000 đ/kg'), chọn mặt hàng nông sản, chọn loại điều kiện (PRICE_ABOVE - Giá vượt lên trên ngưỡng, hoặc PRICE_BELOW - Giá giảm xuống dưới ngưỡng), nhập giá trị ngưỡng bằng VNĐ và địa chỉ Email nhận thông báo, sau đó gửi yêu cầu POST /api/v1/alerts. Tầng dịch vụ alert_service.py thực hiện làm sạch chuỗi tên quy tắc bằng hàm sanitize_text() để chống tấn công Stored XSS trước khi lưu vào bảng alert_rules. Mỗi khi có dữ liệu giá mới được cập nhật hoặc khi người dùng nhấn nút 'Gửi thử Email', hàm evaluate_all_alert_rules() và send_email_notification() sẽ kết nối máy chủ SMTP (TLS cổng 587) để gửi bức thư điện tử định dạng HTML thông báo mức giá hiện tại, mức ngưỡng đã vượt và ghi nhận vào bảng nhật ký kiểm toán alert_logs.

2. Luồng nghiệp vụ Đăng ký, Đăng nhập và Bảo vệ Phiên làm việc (UC-06 - Trang /login & /register): Khi đăng ký tài khoản mới qua POST /api/v1/auth/register, hệ thống kiểm tra giới hạn tần suất truy cập theo IP (auth_rate_limiter), chuẩn hóa địa chỉ email chữ thường, kiểm tra trùng lặp, làm sạch XSS trên trường họ tên và băm mật khẩu bằng Bcrypt với Salt ngẫu nhiên. Khi đăng nhập qua POST /api/v1/auth/login, hệ thống xác thực mật khẩu với chuỗi hash Bcrypt, kiểm tra tài khoản không bị khóa (is_active == True) và ký phát JWT Bearer Token (thuật toán HS256) chứa định danh sub và vai trò role để trình duyệt lưu trữ phục vụ các yêu cầu cần xác thực.


### 3.1.8. Đặc tả chi tiết Ca sử dụng UC-07 đến UC-11: Phân hệ Quản trị Hệ thống và Điều phối Đường ống Học máy (Admin)

Phân hệ Quản trị Admin (/admin) được bảo vệ nghiêm ngặt bởi lớp kiểm tra phân quyền require_role(['admin']) ở cả phía giao diện và phía máy chủ API. Quản trị viên thực hiện 5 nhóm tác vụ quản trị cốt lõi:

1. Quản lý điểm giá thủ công và lưu vết kiểm toán (UC-09): Khi Quản trị viên thêm mới hoặc chỉnh sửa một mức giá vào ngày cụ thể qua POST /api/v1/admin/prices, nếu ngày đó đã tồn tại bản ghi giá trong bảng price_history, hàm archive_price() sẽ tự động sao lưu toàn bộ giá trị cũ, nguồn cũ và trạng thái xác minh cũ sang bảng price_revisions trước khi ghi đè giá trị mới với trạng thái provenance = 'reviewed'.

2. Nhập và Xuất dữ liệu hàng loạt qua tập tin CSV (UC-09): Khi Quản trị viên tải lên tập tin CSV (tối đa 5 MB) qua POST /api/v1/admin/prices/import-csv, hệ thống sử dụng giao dịch lồng nhau (SAVEPOINT / db.begin_nested()) cho từng dòng dữ liệu, áp dụng hàm sanitize_csv_cell() để chặn đứng mã độc công thức Excel, tự động ánh xạ mã nông sản và báo cáo chi tiết số bản ghi tạo mới, số bản ghi cập nhật cũng như danh sách dòng lỗi (nếu có).

3. Điều phối tác vụ nền Thu thập dữ liệu (Scrape) và Huấn luyện lại 5 mô hình AI (Retrain) (UC-10): Khi Quản trị viên nhấn nút kích hoạt thu thập dữ liệu (POST /api/v1/admin/tasks/scrape) hoặc huấn luyện lại mô hình (POST /api/v1/admin/tasks/retrain), hệ thống kiểm tra không có tiến trình nào đang chạy trùng lặp (tránh xung đột tài nguyên HTTP 409 Conflict), tạo bản ghi BackgroundJob với trạng thái RUNNING và đẩy tác vụ vào luồng chạy ngầm BackgroundTasks. Trong suốt thời gian tác vụ chạy, giao diện sử dụng hook useBackgroundJob() để cập nhật thanh tiến trình thời gian thực cho đến khi trạng thái chuyển sang SUCCESS.

4. Chuyển đổi mô hình AI mặc định và Quản lý người dùng (UC-11): Quản trị viên có thể chọn thuật toán mặc định toàn hệ thống (POST /api/v1/admin/models/active), thay đổi vai trò người dùng (admin / analyst / user) hoặc khóa khẩn cấp tài khoản vi phạm (PATCH /api/v1/admin/users/{id}/toggle-status) với cơ chế tự bảo vệ không cho phép Admin tự hạ quyền hoặc tự khóa chính tài khoản đang đăng nhập của mình.


## 3.2. Thiết kế kiến trúc tổng thể và luồng xử lý dữ liệu


### 3.2.1. Kiến trúc phân tầng 4 lớp (4-Tier System Architecture)

Hệ thống AgroForecast được thiết kế theo kiến trúc phân tầng 4 lớp tách biệt rõ ràng về trách nhiệm (Separation of Concerns), giúp dễ dàng mở rộng, bảo trì và kiểm thử độc lập từng thành phần:

Tầng 1 - Tầng Giao diện Trình diễn (Presentation Tier - Next.js 14 Frontend): Vận hành tại cổng 3000, bao gồm các trang giao diện App Router (/ , /forecast, /history, /compare, /alerts, /admin, /login, /register), các thành phần biểu đồ Recharts tương tác, bộ quản lý trạng thái xác thực JWT và lớp giao tiếp HTTP Client (src/lib/api.ts).

Tầng 2 - Tầng Cổng Bảo mật và Điều phối REST API (API & Security Gateway Tier - FastAPI): Vận hành tại cổng 8000, tiếp nhận mọi yêu cầu HTTP thông qua chuỗi lớp trung gian: CORSMiddleware -> SecurityHeadersMiddleware (gắn 7 tiêu đề bảo mật OWASP) -> RateLimiter (chống Brute-Force và DoS) -> OAuth2 JWT & RBAC Dependency (get_current_user, require_role) -> Pydantic v2 Schema Validation -> Các bộ định tuyến API v1 (/api/v1/*).

Tầng 3 - Tầng Nghiệp vụ và Đường ống Học máy (Business Logic & ML Pipeline Tier): Bao gồm các dịch vụ nghiệp vụ (commodity_service, history_service, forecast_service, training_service, alert_service, job_service) và gói đường ống học máy chuyên biệt (ml_pipeline: source_catalog, agro_history, domestic_sources, periodic_reports, data_loader, feature_engineering, model_trainer, predictor, scheduler_jobs).

Tầng 4 - Tầng Lưu trữ Bền vững (Data Persistence Tier): Bao gồm Cơ sở dữ liệu quan hệ PostgreSQL (lưu trữ 11 bảng dữ liệu nghiệp vụ có đánh chỉ mục tối ưu) và Kho lưu trữ trọng số mô hình trên đĩa cứng (ml_pipeline/saved_models/ chứa các tập tin .pt của PyTorch LSTM, .pkl của Prophet/XGBoost/RandomForest/ARIMA và _metrics.json).


### 3.2.2. Thiết kế đường ống thu thập, xác minh nguồn gốc (Provenance) và huấn luyện tự động

Điểm khác biệt cốt lõi trong thiết kế của AgroForecast là quy trình kiểm soát chất lượng dữ liệu đầu vào trước khi cho phép mô hình học máy học quy luật giá. Mỗi bản ghi giá trong bảng price_history được quản lý bởi trường trạng thái nguồn gốc provenance thuộc một trong ba giá trị: 'collected' (dữ liệu được bóc tách tự động thành công từ nguồn công bố chính thức kèm siêu dữ liệu JSON source_details ghi rõ URL, ngày công bố, chợ/địa phương, loại giá), 'reviewed' (dữ liệu đã được Quản trị viên kiểm duyệt và xác nhận tính chính xác), hoặc 'unverified' (dữ liệu mới nhập thô chưa qua kiểm chứng).

Hàm modeling_rows() và readiness() trong mô-đun app/services/history_service.py thiết lập quy tắc kiểm định nghiêm ngặt: (1) Loại bỏ hoàn toàn các bản ghi 'unverified' khỏi tập dữ liệu huấn luyện; (2) Kiểm tra các khoảng trống thời gian (gaps) để phát hiện kỳ nghỉ lễ hoặc giai đoạn ngưng công bố dài hạn; (3) Yêu cầu chuỗi dữ liệu liên tục gần nhất phải đạt tối thiểu 60 quan sát đối với chuỗi ngày (daily), 30 quan sát đối với chuỗi không đều (irregular) và 24 kỳ đối với chuỗi báo cáo định kỳ (periodic). Chỉ khi đạt trạng thái ready = True, bộ huấn luyện training_service.retrain() mới tiến hành chia tập Train/Holdout, huấn luyện đồng thời 5 mô hình, tính toán chỉ số sai số và cập nhật bảng forecasts.


### 3.2.3. Thiết kế mô-đun Giải thích Mô hình Học máy (Explainable AI - XAI Feature Importance)

Để giúp người nông dân, thương lái và hội đồng chuyên môn hiểu rõ vì sao mô hình AI đưa ra mức dự báo tăng hay giảm thay vì hoạt động như một 'hộp đen' (Black Box), hệ thống thiết kế thành phần XAIFeatureDrivers.tsx kết hợp trọng số đặc trưng của mô hình để định lượng tỷ trọng đóng góp (%) và chiều hướng tác động (Thúc đẩy tăng / Kìm hãm giá / Ổn định) của 5 nhóm nhân tố chính đối với từng loại nông sản: (1) Động lượng giá trễ ngắn hạn (Lag t-1 đến t-7); (2) Chu kỳ mùa vụ thu hoạch và thời tiết vùng trồng (Lượng mưa Tây Nguyên, nắng hạn El Nino hoặc sương muối Đà Lạt); (3) Tỷ giá USD/VND và giá sàn kỳ hạn quốc tế; (4) Chi phí vận chuyển, phân bón đầu vào; và (5) Nhu cầu thu mua xuất khẩu của các thị trường chủ lực.


### 3.2.4. Thiết kế chi tiết bảng trọng số Giải thích Mô hình (Explainable AI - XAI) cho 8 nông sản

Trong lĩnh vực nông nghiệp thông minh (AgriTech), người nông dân và nhà phân phối không chỉ cần biết 'con số dự báo ngày mai là bao nhiêu' mà còn cần hiểu rõ 'những yếu tố thực tế nào đang thúc đẩy hoặc kìm hãm giá'. Tại mô-đun giao diện frontend/src/components/dashboard/XAIFeatureDrivers.tsx, hệ thống thiết kế bộ giải thích tầm quan trọng đặc trưng (Feature Importance Attribution) chuyên biệt cho từng mặt hàng nông sản, kết hợp giữa động lượng chuỗi thời gian của mô hình AI đang chọn và các yếu tố cơ bản của ngành hàng đó. Bảng 3.6 trình bày chi tiết cấu hình các nhân tố giải thích XAI trong hệ thống.


**Bảng 3.6. Đặc tả các nhân tố giải thích mô hình học máy (Explainable AI - XAI Drivers) theo từng nhóm nông sản**

| Nhóm nông sản | Nhân tố ảnh hưởng thứ 1 (Trọng số cao nhất) | Nhân tố ảnh hưởng thứ 2 | Nhân tố ảnh hưởng thứ 3 | Nhân tố ảnh hưởng thứ 4 & 5 |
| --- | --- | --- | --- | --- |
| Cà phê Robusta (COFFEE_ROBUSTA) | Động lượng giá trễ ngắn hạn (Lag t-1..t-7) & Tồn kho sàn London ICE (34%) | Lượng mưa & Thời tiết vùng trồng Tây Nguyên (Đắk Lắk, Lâm Đồng) (26%) | Tỷ giá ngoại tệ USD/VND & Chi phí cước tàu biển (18%) | Chu kỳ thu hoạch vụ mới (12%) & Giá phân bón NPK đầu vào (10%) |
| Hồ tiêu đen (PEPPER_BLACK) | Xu hướng giá thu mua nội địa 7 ngày gần nhất & Tâm lý trữ hàng tại hộ (36%) | Nhu cầu nhập khẩu từ thị trường Trung Quốc, Mỹ, Châu Âu (25%) | Sản lượng vụ thu hoạch mới tại Gia Lai, Đắk Lắk, Bà Rịa - Vũng Tàu (20%) | Tỷ giá USD/VND (11%) & Chi phí vận chuyển xuất khẩu (8%) |
| Lúa gạo IR50404 (RICE_IR504) | Quán tính giá lúa tươi tại ruộng An Giang - Đồng Tháp 7 ngày qua (35%) | Tiến độ thu hoạch vụ Đông Xuân / Hè Thu / Thu Đông tại ĐBSCL (27%) | Nhu cầu thu mua gạo xuất khẩu (Philippines, Indonesia) (20%) | Điều kiện vận tải thủy nội địa & Chi phí sấy lúa (18%) |
| Dâu tây & Khoai tây Đà Lạt | Biến động nhiệt độ, lượng mưa và độ ẩm tại TP. Đà Lạt - Lâm Đồng (36%) | Động lượng giá cắt tại vườn Phường 7, Phường 8 tuần qua (30%) | Nhu cầu tiêu thụ du lịch cuối tuần & Siêu thị TP.HCM (20%) | Chi phí giống, nhà kính và vận chuyển lạnh (14%) |
| Khoai lang tím & Hạt điều thô | Động lượng giá thu mua tại ruộng Bình Tân / vườn Bù Đăng (34%) | Tiến độ thông quan xuất khẩu & Nhu cầu nhà máy chế biến (28%) | Chu kỳ thời vụ thu hoạch và chất lượng củ/hạt thương phẩm (22%) | Chi phí nhân công thu hoạch & vận tải nội địa (16%) |



### 3.2.5. Thiết kế thuật toán kiểm định nguồn gốc dữ liệu và chữ ký băm mật mã SHA-256 (Dataset Fingerprint)

Một trong những đóng góp kỹ thuật cốt lõi của hệ thống AgroForecast tại tệp app/services/history_service.py là cơ chế bảo vệ tính toàn vẹn của dữ liệu chuỗi thời gian từ khâu thu thập cho đến khâu hiển thị dự báo. Thuật toán hoạt động qua ba bước kiểm soát tuần tự:

Bước 1 - Lọc và phân đoạn chuỗi hợp lệ (modeling_rows): Truy vấn toàn bộ các bản ghi trong bảng price_history (hoặc periodic_prices đối với mía đường) của mặt hàng mục tiêu có trạng thái provenance nằm trong tập hợp ('collected', 'reviewed') và giá trị price > 0, sắp xếp tăng dần theo ngày record_date. Nếu phát hiện khoảng cách giữa hai ngày quan sát liên tiếp vượt quá ngưỡng gián đoạn cho phép (gap_break = 45 ngày đối với chuỗi ngày hoặc 60 ngày đối với chuỗi không đều do ngưng công bố dài hạn), thuật toán tự động tách chuỗi thành các phân đoạn độc lập (segments) và chọn phân đoạn liên tục mới nhất đủ độ dài tối thiểu (min_points = 60 đối với chuỗi ngày, 30 đối với chuỗi không đều, 24 đối với chuỗi kỳ) để huấn luyện.

Bước 2 - Tính chữ ký băm mật mã SHA-256 (fingerprint): Với tập hợp các quan sát hợp lệ R = {(d_1, p_1, prov_1), ..., (d_N, p_N, prov_N)}, hàm fingerprint(R) nối chuẩn hóa toàn bộ chuỗi ngày, giá trị giá chính xác tới 4 chữ số thập phân và trạng thái xác minh thành một thông điệp duy nhất M = 'd_1:p_1:prov_1|d_2:p_2:prov_2|...|d_N:p_N:prov_N', sau đó áp dụng hàm băm mật mã một chiều SHA-256 (hashlib.sha256) để sinh ra chuỗi định danh 64 ký tự thập lục phân dataset_hash.

Bước 3 - Xác thực đồng bộ tại thời điểm truy vấn dự báo: Mỗi khi người dùng gọi API GET /api/v1/forecast, dịch vụ forecast_service.py tính toán lại fingerprint(context['rows']) trên dữ liệu lịch sử hiện tại và so sánh với trường dataset_hash được lưu trong bảng training_runs của phiên huấn luyện gần nhất. Nếu hai mã băm không trùng khớp (ví dụ Quản trị viên vừa sửa hoặc xóa một điểm giá lịch sử), hệ thống lập tức chặn việc trả về dự báo cũ và yêu cầu kích hoạt lại tiến trình huấn luyện (HTTP 409 Conflict). Cơ chế này đảm bảo 100% đường dự báo hiển thị trên giao diện luôn tương ứng chính xác với tập dữ liệu lịch sử đã xác minh.


### 3.2.6. Thiết kế quy trình huấn luyện đồng thời 5 mô hình và đối sánh với mô hình cơ sở (Naive Baseline)

Trong tệp app/services/training_service.py, hàm retrain(commodity_id, progress) điều phối toàn bộ chu trình huấn luyện và kiểm định chéo cho 5 mô hình học máy ('LSTM', 'Prophet', 'ARIMA', 'XGBoost', 'Random Forest') theo 5 bước chuẩn hóa:

Bước 1: Trích xuất chuỗi thời gian chuẩn hóa S = {p_1, p_2, ..., p_N} từ hàm training_context(). Kiểm tra điều kiện sẵn sàng quality['ready'] == True.

Bước 2: Chia chuỗi S thành Tập huấn luyện S_train có độ dài N - H và Tập kiểm thử giữ lại S_test có độ dài H = min(14, max(5, floor(N / 6))). Tuyệt đối không cho phép các hàm huấn luyện đọc bất kỳ điểm dữ liệu nào thuộc S_test.

Bước 3: Thiết lập dự báo cơ sở Naive Persistence Baseline trên tập S_test bằng cách giữ nguyên giá trị cuối cùng của tập huấn luyện: hat{y}_{naive} = [S_train[-1], S_train[-1], ..., S_train[-1]] và tính bộ chỉ số cơ sở (MAE_baseline, RMSE_baseline, MAPE_baseline, R2_baseline).

Bước 4: Lần lượt huấn luyện từng mô hình m trong 5 mô hình trên chuỗi S_train, dự báo H bước trên tập S_test để tính toán chính xác bộ chỉ số kiểm định Metrics(m) = {MAE_m, RMSE_m, MAPE_m, R2_m}. Ngay sau khi kiểm định xong mô hình m, tiến hành huấn luyện lại mô hình m trên toàn bộ chuỗi S (gồm đủ N quan sát) để dự báo H_future = 30 bước tương lai {hat{y}_{N+1}^{(m)}, ..., hat{y}_{N+30}^{(m)}} và tính khoảng tin cậy 95% với bán kính dải băng Margin_m = 1.96 * RMSE_m.

Bước 5: Khởi tạo bản ghi TrainingRun lưu trữ toàn bộ siêu dữ liệu kiểm định, chữ ký dataset_hash, kết quả so sánh với Naive Baseline và ghi đồng loạt 150 bản ghi dự báo mới (5 mô hình x 30 bước tương lai) vào bảng forecasts trong cùng một giao dịch nguyên tử (Database Transaction).


### 3.2.7. Đặc tả chi tiết các Mô-đun Dịch vụ Nghiệp vụ Backend (app/services/)

Tầng dịch vụ nghiệp vụ tại thư mục backend/app/services/ đóng vai trò là trái tim xử lý logic của toàn bộ hệ thống AgroForecast, bao gồm 6 mô-đun cốt lõi được thiết kế tách biệt hoàn toàn với tầng giao thức HTTP:

1. Mô-đun Dịch vụ Nông sản và Thị trường (app/services/commodity_service.py): Cung cấp ba hàm dịch vụ chính phục vụ trang Tổng quan và trang Đối sánh thị trường. Hàm get_commodities_overview(db) truy vấn danh sách 8 mặt hàng nông sản từ bảng commodities, lấy 7 bản ghi giá lịch sử gần nhất của từng mặt hàng để dựng chuỗi đồ thị thu nhỏ Sparkline, tính toán giá hiện tại, mức phần trăm tăng/giảm so với phiên trước đó và trả về danh sách đối tượng CommodityOverviewCard. Hàm get_market_comparison(db) trích xuất chuỗi biến động giá chuẩn hóa của 8 mặt hàng theo các mốc thời gian đồng bộ để vẽ biểu đồ tương quan đa nông sản. Hàm get_regional_prices_list(db) tổng hợp bảng khảo sát giá bán tại vườn/ruộng mới nhất của từng mặt hàng kèm biên độ giá thấp nhất - cao nhất (price_min - price_max), khối lượng thu hoạch/giao dịch ước tính (volume), tên cơ quan công bố (source) và ngày cập nhật mới nhất.

2. Mô-đun Dịch vụ Lịch sử và Kiểm định Nguồn gốc (app/services/history_service.py): Thực thi toàn bộ quy tắc quản trị dữ liệu lịch sử (Data Governance). Hàm observations(db, commodity_id, start, end, include_unverified) truy vấn chuỗi giá trong khoảng ngày yêu cầu, mặc định lọc bỏ các bản ghi chưa xác minh (provenance == 'unverified') đối với người dùng công khai và tự động tính toán danh sách các ngày bị khuyết dữ liệu (missing_dates) đối với các mặt hàng công bố hàng ngày. Hàm readiness(commodity, rows, latest_observed) đánh giá xem chuỗi dữ liệu hiện tại đã đủ độ dài tối thiểu, đủ độ tươi mới (staleness) và không bị đứt đoạn quá giới hạn để cho phép huấn luyện AI hay chưa. Hàm archive_price(db, existing_row) thực hiện sao lưu bản ghi giá hiện tại sang bảng kiểm toán price_revisions trước mỗi lần Quản trị viên cập nhật lại điểm giá.

3. Mô-đun Dịch vụ Huấn luyện Học máy Đa mô hình (app/services/training_service.py): Triển khai đầy đủ 5 thuật toán dự báo chuỗi thời gian (LSTM, Prophet, ARIMA, XGBoost, Random Forest) cùng hàm điều phối retrain(commodity_id, progress). Mô-đun này đảm nhận việc tạo đặc trưng cửa sổ trượt (tabular_features), chia tách nghiêm ngặt tập huấn luyện và tập kiểm thử giữ lại theo thời gian (Temporal Holdout Split), tính toán sai số của mô hình cơ sở Naive Persistence, huấn luyện kiểm định 5 mô hình, huấn luyện lại trên toàn bộ chuỗi để sinh 30 bước dự báo tương lai kèm khoảng tin cậy 95% (+/- 1,96 * RMSE) và lưu trữ chữ ký băm SHA-256 (dataset_hash) vào bảng training_runs.

4. Mô-đun Dịch vụ Dự báo Không gian - Thời gian (app/services/forecast_service.py): Quản lý từ điển cấu hình 29 địa phương bán tại vườn/ruộng (COMMODITY_REGIONS) với độ lệch giá cơ sở (basisSpread) và mô tả kinh tế - kỹ thuật đặc trưng của từng huyện. Hàm get_forecast_dashboard(db, commodity_id, model_name, days, region) thực hiện kiểm tra chéo chữ ký SHA-256 giữa dữ liệu lịch sử hiện tại và phiên huấn luyện gần nhất, áp dụng phép dịch chuyển không gian (Spatial Basis Adjustment) cho cả chuỗi lịch sử 30 mốc gần nhất lẫn chuỗi dự báo tương lai (7, 10, 14, 30 ngày) và trả về cấu trúc ForecastDashboardResponse hoàn chỉnh. Hàm get_forecast_comparison(db, commodity_id) tổng hợp bảng so sánh 4 chỉ số MAE, RMSE, MAPE, R2 của cả 5 mô hình để giao diện tự động xếp hạng và khuyến nghị mô hình tốt nhất.

5. Mô-đun Dịch vụ Cảnh báo Biến động Giá (app/services/alert_service.py): Cung cấp các hàm quản lý vòng đời quy tắc cảnh báo (get_all_alert_rules, create_alert_rule, toggle_alert_rule, delete_alert_rule) có tích hợp bộ lọc làm sạch XSS sanitize_text(). Hàm evaluate_all_alert_rules(db) tự động quét toàn bộ các quy tắc đang bật (is_active == True), đối chiếu mức giá bán tại vườn mới nhất của mặt hàng tương ứng với ngưỡng threshold_value theo điều kiện PRICE_ABOVE hoặc PRICE_BELOW; nếu thỏa mãn điều kiện kích hoạt, hệ thống tự động soạn thư điện tử HTML chuyên nghiệp gửi qua giao thức SMTP TLS (send_email_notification) và ghi nhật ký vào bảng alert_logs.

6. Mô-đun Dịch vụ Điều phối Tác vụ Nền (app/services/job_service.py): Quản lý hàng đợi và vòng đời của các tiến trình chạy ngầm (BackgroundJob) như thu thập dữ liệu lịch sử tự động (kind = 'scrape') và huấn luyện lại toàn bộ mô hình học máy (kind = 'retrain'). Khi một tác vụ cào dữ liệu hoàn tất và phát hiện có điểm giá lịch sử mới làm thay đổi chuỗi dữ liệu của mặt hàng đã đủ điều kiện huấn luyện, hệ thống tự động kích hoạt nối tiếp tiến trình huấn luyện lại (Auto-Retrain on New Data) để đảm bảo các đường dự báo luôn được cập nhật mới nhất.


## 3.3. Thiết kế Cơ sở dữ liệu quan hệ (PostgreSQL Schema & ERD)


### 3.3.1. Tổng quan kiến trúc Cơ sở dữ liệu và mối quan hệ thực thể (ERD)

Cơ sở dữ liệu của hệ thống AgroForecast (tên CSDL: agroforecast_db) được thiết kế chuẩn hóa ở dạng chuẩn 3 (3NF) gồm 11 bảng dữ liệu quan hệ được định nghĩa tại app/models/models.py và database/init.sql. Trong đó, bảng commodities đóng vai trò là thực thể trung tâm có quan hệ một-nhiều (1 - N, kèm ràng buộc xóa lan truyền ON DELETE CASCADE) tới 5 bảng dữ liệu chuỗi thời gian và nghiệp vụ: price_history (lịch sử giá hàng ngày), periodic_prices (lịch sử giá mua/bán theo kỳ báo cáo), forecasts (điểm dự báo của 5 mô hình AI), training_runs (nhật ký và chữ ký SHA-256 của các phiên huấn luyện), và alert_rules (quy tắc cảnh báo giá). Bảng price_history có quan hệ 1 - N tới bảng price_revisions để lưu vết mọi lịch sử chỉnh sửa điểm giá; bảng alert_rules có quan hệ 1 - N tới bảng alert_logs để lưu nhật ký gửi cảnh báo.


**Bảng 3.2. Danh mục 11 bảng dữ liệu trong Cơ sở dữ liệu PostgreSQL của hệ thống AgroForecast**

| STT | Tên bảng vật lý | Lớp ORM Model | Khóa chính (PK) | Khóa ngoại (FK) | Chức năng lưu trữ chính |
| --- | --- | --- | --- | --- | --- |
| 1 | users | User | id (SERIAL) | Không | Lưu tài khoản người dùng, mật khẩu băm Bcrypt, vai trò (admin/analyst/user) và trạng thái khóa |
| 2 | commodities | Commodity | id (SERIAL) | Không | Lưu 8 mặt hàng nông sản chủ lực, mã code, đơn vị tính, địa phương bán tại vườn/ruộng |
| 3 | price_history | PriceHistory | id (SERIAL) | commodity_id -> commodities.id | Lưu chuỗi giá lịch sử theo ngày, min/max, sản lượng, nguồn và trạng thái xác minh provenance |
| 4 | periodic_prices | PeriodicPrice | id (SERIAL) | commodity_id -> commodities.id | Lưu dữ liệu giá mua và giá bán theo kỳ báo cáo (dành cho mặt hàng công bố theo tuần/kỳ) |
| 5 | price_revisions | PriceRevision | id (SERIAL) | price_history_id, commodity_id | Lưu vết kiểm toán (Audit Trail) các phiên bản giá cũ trước khi Admin cập nhật |
| 6 | training_runs | TrainingRun | id (SERIAL) | commodity_id -> commodities.id | Lưu siêu dữ liệu phiên huấn luyện AI, chữ ký SHA-256 (dataset_hash) và kết quả kiểm định Holdout |
| 7 | forecasts | Forecast | id (SERIAL) | commodity_id, training_run_id | Lưu chuỗi dự báo tương lai của 5 mô hình AI kèm lower_ci, upper_ci, MAE, RMSE, MAPE, R2 |
| 8 | alert_rules | AlertRule | id (SERIAL) | commodity_id -> commodities.id | Lưu quy tắc cảnh báo biến động giá (PRICE_ABOVE / PRICE_BELOW), ngưỡng giá và Email nhận |
| 9 | alert_logs | AlertLog | id (SERIAL) | rule_id -> alert_rules.id | Lưu lịch sử các lần kích hoạt cảnh báo tự động và trạng thái gửi thông báo |
| 10 | background_jobs | BackgroundJob | id (SERIAL) | Không | Lưu tiến trình, trạng thái (RUNNING/SUCCESS/FAILED) của tác vụ cào dữ liệu và huấn luyện ngầm |
| 11 | system_settings | SystemSetting | key (VARCHAR) | Không | Lưu cấu hình toàn cục của hệ thống (như thuật toán AI mặc định active_model) |



### 3.3.2. Đặc tả chi tiết cấu trúc các bảng dữ liệu cốt lõi

Dưới đây là đặc tả chi tiết các trường dữ liệu, kiểu dữ liệu vật lý trong PostgreSQL, ràng buộc toàn vẹn và ý nghĩa của các bảng trọng tâm trong hệ thống:


**Bảng 3.3. Đặc tả cấu trúc bảng danh mục nông sản (commodities) và bảng lịch sử giá (price_history)**

| Tên bảng | Tên trường (Column) | Kiểu dữ liệu | Ràng buộc | Mô tả chi tiết ý nghĩa |
| --- | --- | --- | --- | --- |
| commodities | id | SERIAL / INTEGER | PRIMARY KEY | Mã định danh tự tăng của mặt hàng nông sản (1 -> 8) |
| commodities | code | VARCHAR(50) | UNIQUE, NOT NULL, INDEX | Mã ký hiệu chuẩn (RICE_IR504, COFFEE_ROBUSTA, PEPPER_BLACK...) |
| commodities | name | VARCHAR(255) | NOT NULL | Tên hiển thị tiếng Việt của nông sản (Cà phê Robusta, Hồ tiêu đen...) |
| commodities | category | VARCHAR(100) | NOT NULL | Nhóm phân loại (Nông sản xuất khẩu, Lương thực, Nông sản đặc sản...) |
| commodities | unit | VARCHAR(50) | NOT NULL | Đơn vị tính chuẩn (VNĐ/kg hoặc VNĐ/tấn) |
| commodities | region | VARCHAR(255) | NOT NULL | Địa phương tham chiếu chuẩn bán tại vườn / tại ruộng |
| commodities | description | TEXT | NULLABLE | Mô tả quy cách thương phẩm và các huyện thu mua trọng điểm |
| price_history | id | SERIAL / INTEGER | PRIMARY KEY | Mã định danh bản ghi giá lịch sử |
| price_history | commodity_id | INTEGER | FK -> commodities.id, INDEX | Liên kết tới mặt hàng nông sản tương ứng |
| price_history | record_date | DATE | NOT NULL, INDEX | Ngày ghi nhận mức giá giao dịch thực tế |
| price_history | price | NUMERIC(12, 2) | NOT NULL | Mức giá bán tại vườn / tại ruộng ở địa phương chuẩn |
| price_history | price_min / price_max | NUMERIC(12, 2) | NULLABLE | Biên độ giá thấp nhất và cao nhất trong ngày khảo sát |
| price_history | volume | NUMERIC(12, 2) | DEFAULT 0 | Ước tính khối lượng giao dịch hoặc thu hoạch (tấn) |
| price_history | source | VARCHAR(255) | NULLABLE | Tên cơ quan / hiệp hội công bố mức giá |
| price_history | provenance | VARCHAR(30) | NOT NULL, DEFAULT 'unverified' | Trạng thái xác minh nguồn gốc: collected | reviewed | unverified |
| price_history | source_details | TEXT (JSON) | NULLABLE | Chuỗi JSON lưu URL gốc, ngày công bố, chợ địa phương, loại giá |



**Bảng 3.4. Đặc tả cấu trúc bảng kết quả dự báo học máy (forecasts) và phiên huấn luyện (training_runs)**

| Tên bảng | Tên trường (Column) | Kiểu dữ liệu | Ràng buộc | Mô tả chi tiết ý nghĩa |
| --- | --- | --- | --- | --- |
| forecasts | id | SERIAL / INTEGER | PRIMARY KEY | Mã định danh điểm dự báo tương lai |
| forecasts | commodity_id | INTEGER | FK -> commodities.id, INDEX | Mã mặt hàng nông sản được dự báo |
| forecasts | training_run_id | INTEGER | FK -> training_runs.id, INDEX | Liên kết tới phiên huấn luyện đã sinh ra dự báo này |
| forecasts | model_name | VARCHAR(50) | NOT NULL, INDEX | Tên mô hình AI: LSTM | Prophet | ARIMA | XGBoost | Random Forest |
| forecasts | training_date | DATE | NOT NULL | Ngày mốc lịch sử cuối cùng dùng để huấn luyện mô hình |
| forecasts | forecast_date | DATE | NOT NULL, INDEX | Ngày mục tiêu trong tương lai được dự báo (t+1 .. t+30) |
| forecasts | predicted_price | NUMERIC(12, 2) | NOT NULL | Giá dự báo trung tâm (yhat) tính theo đơn vị của nông sản |
| forecasts | lower_ci / upper_ci | NUMERIC(12, 2) | NOT NULL | Cận dưới và cận trên của khoảng tin cậy 95% (yhat +/- 1.96*RMSE) |
| forecasts | mae / rmse / mape / r2 | NUMERIC(12, 4) | NULLABLE | Bốn chỉ số đánh giá sai số của mô hình trên tập kiểm thử Holdout |
| training_runs | id | SERIAL / INTEGER | PRIMARY KEY | Mã định danh phiên huấn luyện |
| training_runs | commodity_id | INTEGER | FK -> commodities.id, INDEX | Mã mặt hàng nông sản được huấn luyện |
| training_runs | dataset_hash | VARCHAR(64) | NOT NULL, INDEX | Chữ ký băm mật mã SHA-256 đảm bảo toàn vẹn tập dữ liệu huấn luyện |
| training_runs | history_start / end | DATE | NOT NULL | Ngày bắt đầu và ngày kết thúc của chuỗi lịch sử đưa vào huấn luyện |
| training_runs | observed_count | INTEGER | NOT NULL | Tổng số điểm quan sát hợp lệ đã dùng để huấn luyện và kiểm định |
| training_runs | metadata_json | TEXT (JSON) | NOT NULL | Lưu chi tiết kết quả Holdout, mô hình cơ sở Naive và danh sách điểm giá |



### 3.3.3. Đặc tả cấu trúc các bảng Quản trị, Người dùng, Cảnh báo và Kiểm toán dữ liệu

Bên cạnh các bảng lưu trữ chuỗi giá và kết quả dự báo, hệ thống Cơ sở dữ liệu PostgreSQL còn bao gồm 6 bảng phục vụ quản trị người dùng, kiểm toán lịch sử chỉnh sửa dữ liệu, vận hành cảnh báo tự động và theo dõi tác vụ nền. Bảng 3.7 đặc tả chi tiết cấu trúc của các bảng này.


**Bảng 3.7. Đặc tả cấu trúc bảng users, price_revisions, alert_rules, alert_logs và background_jobs**

| Tên bảng | Tên trường (Column) | Kiểu dữ liệu | Ràng buộc | Mô tả chi tiết ý nghĩa |
| --- | --- | --- | --- | --- |
| users | id | SERIAL / INTEGER | PRIMARY KEY | Mã định danh tự tăng của người dùng |
| users | email | VARCHAR(255) | UNIQUE, NOT NULL, INDEX | Địa chỉ email đăng nhập duy nhất của người dùng |
| users | password_hash | VARCHAR(255) | NOT NULL | Chuỗi mật khẩu đã băm một chiều bằng thuật toán Bcrypt + Salt |
| users | full_name | VARCHAR(255) | NOT NULL | Họ và tên hiển thị (đã làm sạch XSS qua sanitize_text) |
| users | role | VARCHAR(50) | DEFAULT 'user' | Vai trò phân quyền RBAC: admin | analyst | user |
| users | is_active | BOOLEAN | DEFAULT TRUE | Trạng thái kích hoạt tài khoản (False = bị khóa bởi Admin) |
| price_revisions | id | SERIAL / INTEGER | PRIMARY KEY | Mã định danh bản ghi lưu vết chỉnh sửa giá |
| price_revisions | price_history_id | INTEGER | FK -> price_history.id | Liên kết tới bản ghi giá gốc bị chỉnh sửa |
| price_revisions | price | NUMERIC(12, 2) | NOT NULL | Giá trị cũ trước khi bị Quản trị viên ghi đè |
| price_revisions | provenance | VARCHAR(30) | NOT NULL | Trạng thái nguồn gốc cũ trước khi chỉnh sửa |
| alert_rules | id | SERIAL / INTEGER | PRIMARY KEY | Mã định danh quy tắc cảnh báo biến động giá |
| alert_rules | commodity_id | INTEGER | FK -> commodities.id | Mặt hàng nông sản cần theo dõi biến động giá |
| alert_rules | rule_name | VARCHAR(255) | NOT NULL | Tên quy tắc cảnh báo do người dùng đặt (đã lọc XSS) |
| alert_rules | condition_type | VARCHAR(50) | NOT NULL | Điều kiện kích hoạt: PRICE_ABOVE (vượt ngưỡng) | PRICE_BELOW (thấp hơn) |
| alert_rules | threshold_value | NUMERIC(12, 2) | NOT NULL | Mức giá ngưỡng kích hoạt cảnh báo (VNĐ/kg hoặc VNĐ/tấn) |
| alert_rules | email | VARCHAR(255) | NOT NULL | Địa chỉ Email nhận thông báo tự động khi điều kiện thỏa mãn |
| alert_logs | id | SERIAL / INTEGER | PRIMARY KEY | Mã định danh nhật ký cảnh báo đã kích hoạt |
| alert_logs | rule_id | INTEGER | FK -> alert_rules.id | Quy tắc cảnh báo đã được kích hoạt |
| alert_logs | triggered_price | NUMERIC(12, 2) | NOT NULL | Mức giá thực tế tại thời điểm kích hoạt cảnh báo |
| alert_logs | message | TEXT | NOT NULL | Nội dung thông điệp cảnh báo chi tiết đã gửi |
| background_jobs | id | SERIAL / INTEGER | PRIMARY KEY | Mã định danh tiến trình chạy ngầm (Scrape / Retrain) |
| background_jobs | kind / status | VARCHAR(40) | NOT NULL, INDEX | Loại tác vụ (scrape | retrain) và trạng thái (RUNNING | SUCCESS | FAILED) |
| background_jobs | records_processed | INTEGER | DEFAULT 0 | Số lượng bản ghi giá hoặc điểm dự báo đã xử lý thành công |



## 3.4. Thiết kế hệ thống RESTful API và Giao diện người dùng (UI/UX)


### 3.4.1. Thiết kế hệ thống 28 Endpoint RESTful API theo chuẩn OpenAPI 3.0

Toàn bộ giao tiếp giữa Frontend và Backend được chuẩn hóa qua tiền tố /api/v1 với 8 nhóm bộ định tuyến (Routers) được định nghĩa tại app/api/v1/api.py. Bảng 3.5 tổng hợp chi tiết các Endpoint chính của hệ thống.


**Bảng 3.5. Đặc tả các Endpoint RESTful API chính của hệ thống AgroForecast**

| Phương thức | Đường dẫn Endpoint (URI) | Phân quyền | Mô tả chức năng và dữ liệu trả về |
| --- | --- | --- | --- |
| POST | /api/v1/auth/register | Public (Rate Limited) | Đăng ký tài khoản mới, băm mật khẩu Bcrypt và làm sạch XSS |
| POST | /api/v1/auth/login | Public (Rate Limited) | Xác thực email/mật khẩu, kiểm tra khóa tài khoản và cấp JWT Bearer Token |
| GET | /api/v1/auth/me | Authenticated User | Trả về thông tin hồ sơ và vai trò của người dùng đang đăng nhập |
| GET | /api/v1/commodities/overview | Public | Lấy danh sách 8 nông sản kèm giá bán tại vườn mới nhất, % thay đổi và Sparkline |
| GET | /api/v1/commodities/comparison | Public | Lấy chuỗi tăng trưởng chuẩn hóa đa nông sản phục vụ biểu đồ đối sánh |
| GET | /api/v1/commodities/regional-prices | Public | Lấy bảng giá bán tại vườn/ruộng, biên độ sàn/trần và nguồn công bố |
| GET | /api/v1/forecast | Public | Trả về chuỗi lịch sử + dự báo theo nông sản, mô hình AI, kỳ hạn (7-30 ngày) và huyện (region) |
| GET | /api/v1/forecast/compare/{id} | Public | Trả về bảng đối sánh 4 chỉ số MAE, RMSE, MAPE, R2 của cả 5 mô hình AI |
| GET | /api/v1/predictions/forecast | Public | API dự báo tốc độ cao có tích hợp bộ nhớ đệm In-Memory Cache (< 50ms) |
| POST | /api/v1/predictions/retrain | Admin Only (JWT) | Kích hoạt huấn luyện lại toàn bộ 5 mô hình học máy trong tiến trình nền |
| GET | /api/v1/history/sources | Public | Lấy danh mục 8 nguồn dữ liệu chính thống Việt Nam và trạng thái sẵn sàng AI |
| GET | /api/v1/history | Public | Truy vấn lịch sử giá theo khoảng ngày, lọc theo provenance và liệt kê ngày khuyết |
| GET / POST | /api/v1/alerts | Public / User | Lấy danh sách quy tắc cảnh báo hoặc tạo mới quy tắc cảnh báo (có lọc XSS) |
| PATCH / DELETE | /api/v1/alerts/{rule_id} | Public / User | Bật/tắt trạng thái hoạt động hoặc xóa quy tắc cảnh báo giá |
| POST | /api/v1/alerts/{rule_id}/test | Public / User | Kích hoạt gửi thử nghiệm thông báo cảnh báo giá qua giao thức SMTP Email |
| GET | /api/v1/admin/stats | Admin / Analyst | Lấy số liệu thống kê tổng quan CSDL và trạng thái máy chủ |
| POST / DELETE | /api/v1/admin/prices | Admin Only (JWT) | Thêm/cập nhật điểm giá thủ công (lưu vết PriceRevision) hoặc xóa điểm giá lỗi |
| POST / GET | /api/v1/admin/prices/import-csv | Admin Only (JWT) | Nhập dữ liệu giá hàng loạt từ file CSV (chống CSV Injection) & Xuất CSV |
| POST | /api/v1/admin/tasks/scrape | Admin Only (JWT) | Kích hoạt Bot thu thập dữ liệu lịch sử từ các nguồn nông sản Việt Nam |
| GET / PATCH | /api/v1/admin/users | Admin Only (JWT) | Quản lý danh sách người dùng, phân quyền Role và khóa/mở khóa tài khoản |



### 3.4.2. Thiết kế Giao diện người dùng (UI/UX) chuẩn Modern Clean Fintech x Sustainable AgriTech

Giao diện người dùng của hệ thống AgroForecast được thiết kế lại toàn diện theo ngôn ngữ thiết kế sản phẩm chuyên nghiệp (lấy cảm hứng từ sự tinh gọn, chuẩn xác dữ liệu của Koyfin/Linear kết hợp sắc thái tự nhiên của nông nghiệp hiện đại):

Về bảng màu (Color Tokens): Sử dụng nền tảng màu trung tính Zinc sắc nét (#FAFAFA cho nền ứng dụng, #FFFFFF cho bề mặt thẻ, #18181B cho văn bản chính) kết hợp màu chủ đạo Xanh lục trầm Emerald (#059669 cho đường giá thực tế và trạng thái tăng trưởng), Xanh dương kỹ thuật (#2563EB cho đường dự báo AI đứt nét và dải tin cậy CI 95%), Đỏ san hô (#E11D48 cho tín hiệu giảm giá) và Vàng hổ phách (#D97706 cho cảnh báo rủi ro).

Về kiểu chữ (Typography): Kết hợp bộ phông chữ không chân hiện đại Plus Jakarta Sans hỗ trợ đầy đủ bộ ký tự tiếng Việt có dấu (vietnamese subset) cho tiêu đề/nhãn điều hướng và phông chữ đơn cách kỹ thuật JetBrains Mono (tabular-nums) cho toàn bộ các trường hiển thị giá tiền (VNĐ/kg), tỷ lệ phần trăm biến động (%) và chỉ số sai số (MAE, RMSE, MAPE, R2), giúp các cột số liệu luôn thẳng hàng tuyệt đối.

Về bố cục hiển thị biểu đồ (Chart Ergonomics): Khắc phục hoàn toàn lỗi nén dẹt đường biểu đồ về gốc 0 bằng thuật toán tự động tính toán miền giá trị trục tung động (yDomain) bám sát biên độ dao động thực tế của nông sản (+/- 12% khoảng đệm), đồng thời nối liền mạch điểm lịch sử cuối cùng với điểm dự báo đầu tiên (isBridgePoint) để người dùng quan sát trực quan hướng bẻ góc của xu hướng giá.


### 3.4.3. Thiết kế kiến trúc thành phần giao diện (Component Hierarchy) và đồng bộ trạng thái bất đồng bộ

Phân hệ Frontend Next.js 14 được tổ chức theo kiến trúc mô-đun hóa cao tại thư mục frontend/src/, phân tách rõ ràng giữa 4 tầng mã nguồn: (1) Tầng Định nghĩa Kiểu tĩnh (src/types/index.ts) khai báo 18 giao diện TypeScript chuẩn hóa (CommoditySummary, ForecastPoint, ModelMetrics, RegionInfo, TrainingMetadata, AlertRuleItem, RegionalPriceItem...); (2) Tầng Dịch vụ Giao tiếp API (src/lib/api.ts và src/lib/auth.ts) quản lý tập trung mọi lời gọi fetch bất đồng bộ, tự động đính kèm tiêu đề Authorization: Bearer <token> và xử lý lỗi mạng; (3) Tầng Thành phần Giao diện Tái sử dụng (src/components/layout/ và src/components/dashboard/) gồm Sidebar, Header, CommodityCard, MarketComparisonChart, RegionalPriceTable, XAIFeatureDrivers, ModelComparisonChart, TrainingSummary, JobStatus; và (4) Tầng Trang Ứng dụng (src/app/) định tuyến cho 8 màn hình nghiệp vụ.

Trên trang Phân tích & Dự báo AI (src/app/forecast/page.tsx), luồng đồng bộ trạng thái bất đồng bộ được điều khiển bởi cặp React Hooks useEffect và useMemo theo 4 biến phụ thuộc: [selectedCommodityId, selectedModel, forecastDays, selectedRegion]. Khi người dùng chuyển đổi sang một mặt hàng nông sản mới, hệ thống tự động đặt lại selectedRegion = '' để nạp địa phương bán tại vườn chuẩn của mặt hàng đó; khi người dùng nhấp chọn một huyện cụ thể trên thanh Spatio-Temporal Selector, yêu cầu GET /api/v1/forecast?commodity_id=...&model_name=...&days=...&region=... được gửi đi tức thời và toàn bộ dải 4 chỉ số tổng hợp, đường biểu đồ lịch sử - dự báo, dải tin cậy CI 95% cùng bảng lịch trình CSV được tính toán lại trong thời gian dưới 50 mili-giây.


### 3.4.5. Đặc tả chi tiết luồng tuần tự (Sequence Workflows) của 4 quy trình nghiệp vụ cốt lõi

Để làm rõ sự phối hợp thông điệp giữa các thành phần từ Trình duyệt (Browser) -> Frontend Next.js -> Cổng bảo mật FastAPI -> Tầng Dịch vụ -> Đường ống Học máy -> Cơ sở dữ liệu PostgreSQL, dưới đây là đặc tả từng bước của 4 luồng tuần tự quan trọng nhất trong hệ thống:

1. Luồng tuần tự Quy trình Dự báo Giá Bán Tại Vườn theo Địa phương (Spatio-Temporal Forecast Sequence): (B1) Người dùng chọn Nông sản (ví dụ Cà phê Robusta), hệ thống tự động chọn mô hình tối ưu ★ (PyTorch Stacked LSTM), chọn Kỳ hạn chuẩn (14 ngày trong Literal[7, 14, 30]) và chọn tỉnh/huyện trên giao diện /forecast; (B2) Thành phần ForecastPage gọi hàm fetchForecastDashboard(2, 'LSTM', 14, undefined, 'lam-dong') trong src/lib/api.ts; (B3) Yêu cầu HTTP GET /api/v1/forecast?commodity_id=2&model_name=LSTM&days=14&province=lam-dong đi qua SecurityHeadersMiddleware; (B4) Router forecast.py chuyển tiếp xuống get_forecast_dashboard() trong forecast_service.py; (B5) Dịch vụ gọi training_context(db, commodity) để lấy chuỗi lịch sử đã xác minh và kiểm tra readiness['ready'] == True; (B6) Dịch vụ truy vấn bản ghi Forecast mới nhất và kiểm tra run.dataset_hash == fingerprint(context['rows']); (B7) Dịch vụ áp dụng định giá vùng Haversine (khảo sát trực tiếp hoặc tham chiếu + cước minh bạch); (B8) Đóng gói 30 điểm lịch sử và 14 điểm dự báo tương lai kèm Conformal 95% CI (predictedPrice, lowerCI, upperCI) trả về trình duyệt; (B9) Giao diện vẽ biểu đồ Syncfusion FinChart tức thời.

2. Luồng tuần tự Quy trình Thu thập Dữ liệu Tự động và Tự động Huấn luyện lại (Scrape & Auto-Retrain Sequence): (B1) Quản trị viên đã đăng nhập gửi yêu cầu POST /api/v1/admin/tasks/scrape kèm JWT Bearer Token; (B2) Dependency require_role(['admin']) giải mã JWT, xác nhận user.role == 'admin' và user.is_active == True; (B3) Dịch vụ job_service.py kiểm tra không có tiến trình 'scrape' nào đang ở trạng thái RUNNING, khởi tạo bản ghi BackgroundJob(kind='scrape', status='RUNNING') và kích hoạt luồng nền run_job(); (B4) Bộ điều phối thu thập dữ liệu gọi các bộ phân tích cú pháp trong ml_pipeline/ (agro_history, domestic_sources, periodic_reports) để lấy dữ liệu mới, kiểm tra định dạng chợ/đơn vị/ngày công bố và lưu vào bảng price_history với provenance = 'collected'; (B5) Nếu phát hiện chuỗi lịch sử của mặt hàng vừa có thêm quan sát mới và đạt trạng thái sẵn sàng (ready == True), hệ thống tự động gọi tiếp training_service.retrain() để huấn luyện lại cả 5 mô hình AI và cập nhật 150 điểm dự báo mới vào bảng forecasts trước khi đánh dấu tác vụ hoàn tất (status = 'SUCCESS').

3. Luồng tuần tự Quy trình Nhập Dữ liệu CSV An toàn và Lưu vết Kiểm toán (Secure CSV Import & Revision Sequence): (B1) Quản trị viên chọn tập tin CSV trên trang /admin và gửi POST /api/v1/admin/prices/import-csv; (B2) Endpoint kiểm tra phần mở rộng tập tin (.csv/.txt) và giới hạn kích thước tối đa <= 5 MB; (B3) Hệ thống đọc từng dòng qua csv.DictReader trong một giao dịch lồng nhau (SAVEPOINT db.begin_nested()); (B4) Trường nguồn dữ liệu được đưa qua hàm sanitize_csv_cell() để vô hiệu hóa mọi công thức độc hại bắt đầu bằng '=', '+', '-', '@' và lọc bỏ thẻ HTML/Script XSS; (B5) Dữ liệu dòng được kiểm tra qua Pydantic Schema PriceCreateManual; nếu ngày đó đã có bản ghi trong price_history, hệ thống gọi archive_price() để lưu bản sao cũ vào bảng price_revisions trước khi cập nhật giá mới và commit savepoint.

4. Luồng tuần tự Quy trình Đánh giá và Phát hành Cảnh báo Giá qua Email (Automated Alert Evaluation Sequence): (B1) Khi có điểm giá mới hoặc theo chu kỳ của bộ lập lịch nền APScheduler (app/core/scheduler.py), hàm evaluate_all_alert_rules(db) được kích hoạt; (B2) Dịch vụ truy vấn toàn bộ các quy tắc đang hoạt động (AlertRule.is_active == True); (B3) Với mỗi quy tắc, hệ thống lấy mức giá bán tại vườn mới nhất của mặt hàng tương ứng và kiểm tra điều kiện PRICE_ABOVE (price >= threshold_value) hoặc PRICE_BELOW (price <= threshold_value); (B4) Khi điều kiện thỏa mãn, hệ thống kết nối máy chủ SMTP gửi thông báo HTML tới địa chỉ Email đã đăng ký và ghi bản ghi kiểm toán vào bảng alert_logs.


## 3.6.4. Thiết kế thành phần AI UI cao cấp với Syncfusion Essential Studio EJ2 React


### 3.6.4. Thiết kế thành phần AI UI cao cấp với Syncfusion Essential Studio EJ2 React

Nhằm mang lại trải nghiệm chuyên nghiệp tiệm cận các nền tảng tài chính quốc tế (Fintech) kết hợp công nghệ nông nghiệp số (AgriTech), hệ thống AgroForecast tích hợp bộ thư viện công nghiệp hàng đầu Syncfusion Essential Studio EJ2 React (phiên bản v35.2.12). Việc ứng dụng bộ thư viện này được chuẩn hóa thông qua thành phần AgroGrid (tại tệp frontend/src/components/ui/AgroGrid.tsx) và cấu hình bản địa hóa L10n tiếng Việt hoàn chỉnh (tại tệp frontend/src/lib/syncfusion.ts).

Thành phần AgroGrid cung cấp giải pháp hiển thị và phân tích dữ liệu bảng chuyên sâu với các tính năng vượt trội: (1) Phân trang mượt mà (Pagination) hỗ trợ cấu hình kích thước trang linh hoạt [10, 20, 50, 100] bản ghi; (2) Sắp xếp đa cột (Multi-column Sorting) cho phép kết hợp nhiều tiêu chí đánh giá; (3) Bộ lọc nâng cao kiểu Excel (Excel-like Filtering) và thanh tìm kiếm toàn văn thời gian thực (Search Toolbar); (4) Tính năng trích xuất dữ liệu trực tiếp ra tệp tin Excel (.xlsx) và CSV với cơ chế tự động làm sạch ký tự đầu ô nhằm triệt tiêu nguy cơ tấn công CSV Formula Injection; (5) Hệ thống bản địa hóa (Vietnamese Localization) chuyển ngữ 100% các nhãn điều khiển, tiêu đề menu ngữ cảnh và hộp thoại thông báo sang tiếng Việt chuẩn, xóa bỏ hoàn toàn rào cản ngôn ngữ cho người dùng nông nghiệp.

Bên cạnh lưới dữ liệu, hệ thống xây dựng thành phần chọn vị trí động LocationSelector (tại frontend/src/components/layout/LocationSelector.tsx) kết hợp với ngữ cảnh quản lý trạng thái tập trung LocationContext (tại frontend/src/contexts/LocationContext.tsx). Cơ chế này cho phép người dùng chuyển đổi linh hoạt điểm khảo sát giữa 33 tỉnh thành và 29 vùng trồng chuyên canh trên toàn quốc. Ngay khi vị trí thay đổi, toàn bộ các bảng điều khiển, thẻ nông sản và biểu đồ trên giao diện sẽ tự động đồng bộ lại số liệu tương ứng.

Đặc biệt, hệ thống bổ sung bảng phân tích chênh lệch giá cấp vùng ProvinceComparisonPanel (tại frontend/src/components/dashboard/ProvinceComparisonPanel.tsx). Bảng điều khiển này ứng dụng thuật toán tính khoảng cách trắc địa mặt cầu Haversine giữa tọa độ vùng trồng xuất xứ và tọa độ trung tâm thương mại của tỉnh lựa chọn, từ đó mô hình hóa chi phí logistics minh bạch và trực quan hóa tỷ lệ phần trăm chênh lệch giá bán tại vườn/ruộng so với giá thị trường tiêu thụ tại các đô thị lớn.


## 3.6.5. Thiết kế kỹ năng biểu đồ phân tích kỹ thuật FinChart và trực quan hóa Walk-Forward


### 3.6.5. Thiết kế kỹ năng biểu đồ phân tích kỹ thuật FinChart và trực quan hóa Walk-Forward

Đối với phân hệ phân tích chuỗi thời gian và dự báo giá, hệ thống xây dựng thành phần biểu đồ tài chính cao cấp FinChart (tại frontend/src/components/ui/FinChart.tsx) dựa trên Syncfusion ChartComponent. Thành phần này giải quyết triệt để các hạn chế của biểu đồ thông thường, mang đến các kỹ năng trực quan hóa phân tích kỹ thuật chuyên sâu:

1. Hỗ trợ chuyển đổi đa dạng 4 chế độ biểu diễn đồ thị: (a) Biểu đồ diện tích mượt (SplineArea) hiển thị rõ nét xu hướng biến động và vùng giá trị lịch sử; (b) Biểu đồ đường phân tích (Line) thể hiện sắc nét các điểm gãy và đường trung bình động MA-7/MA-30; (c) Biểu đồ cột khối lượng (Column) minh họa mức độ biến động tuyệt đối từng phiên; và (d) Biểu đồ Nến Nhật Bản (Candlestick / HiloOpenClose) chuẩn quốc tế hiển thị đầy đủ 4 mức giá Mở cửa (Open), Cao nhất (High), Thấp nhất (Low) và Đóng cửa (Close) trong từng kỳ giao dịch.

2. Trực quan hóa dải khoảng tin cậy mở rộng Conformal Prediction 95% (PICP): Trên chuỗi dự báo 7 ngày và 30 ngày, biểu đồ FinChart hiển thị vùng biên độ sai số động mở rộng dần theo thời gian [y_hat - 1.96 * RMSE, y_hat + 1.96 * RMSE]. Cơ chế này phản ánh trung thực quy luật độ bất định tăng dần khi dự báo càng xa về tương lai, giúp người nông dân và doanh nghiệp nhận biết rõ biên độ rủi ro.

3. Trực quan hóa quy trình đánh giá Walk-Forward 7 ngày không rò rỉ dữ liệu (No Data Leakage Walk-Forward Evaluation): Biểu đồ thể hiện trực quan ranh giới phân tách nghiêm ngặt giữa tập huấn luyện (Train) và tập kiểm thử (Test). Dữ liệu tương lai hoàn toàn không bị rò rỉ vào quá trình trích xuất đặc trưng hay chuẩn hóa dữ liệu.

4. Xử lý tương tác mượt mà và tối ưu hóa DOM: Hệ thống tích hợp tính năng rê chuột tra cứu đa điểm (Crosshair và Multi-series Tooltip), đồng thời xử lý triệt để xung đột gắn kết phần tử DOM (loại bỏ hoàn toàn lỗi BaseTooltip.appendChild thường gặp trên các phiên bản thư viện đồ thị phức tạp), đảm bảo tỷ lệ khung hình 60 FPS ổn định ngay cả khi hiển thị hàng nghìn điểm dữ liệu.


# Chương 4: XÂY DỰNG HỆ THỐNG, THỰC NGHIỆM 5 MÔ HÌNH HỌC MÁY, KIỂM THỬ VÀ BẢO MẬT


## 4.1. Môi trường cài đặt và bộ dữ liệu thực nghiệm của hệ thống


### 4.1.1. Cấu hình môi trường phần cứng, phần mềm và thư viện triển khai

Hệ thống AgroForecast được cài đặt, huấn luyện thực nghiệm và kiểm thử trên môi trường máy trạm phát triển với cấu hình phần cứng và phần mềm tiêu chuẩn. Tầng Backend sử dụng Python 3.11.9, FastAPI, Uvicorn ASGI Server, SQLAlchemy 2.0, Pydantic v2, APScheduler và hệ quản trị cơ sở dữ liệu PostgreSQL 17 (12 bảng chuẩn hóa). Tầng Học máy (Machine Learning Pipeline) sử dụng PyTorch (cho mạng học sâu Stacked LSTM 7 kênh), Facebook Prophet, Statsmodels (cho ARIMA), XGBoost, Scikit-learn (cho Random Forest và các độ đo đánh giá), Pandas và NumPy, kết hợp biến ngoại sinh nhân quả USD/VND (VND=X) và Dầu thô WTI (CL=F). Tầng Frontend sử dụng Node.js 20, Next.js 14.2, React 18, TypeScript 5, TailwindCSS, bộ thành phần doanh nghiệp Syncfusion Essential Studio EJ2 React (AgroGrid, FinChart) và Recharts; toàn bộ 3 tầng được đóng gói triển khai qua Docker Compose.


### 4.1.2. Thống kê bộ dữ liệu lịch sử thực nghiệm của 8 mặt hàng nông sản trong PostgreSQL

Dữ liệu lịch sử giá giai đoạn 2024–2026 của 8 mặt hàng nông sản chủ lực được tổ chức minh bạch theo 3 nhóm nguồn gốc và lưu trữ xác thực (provenance = 'collected') trong bảng price_history với tổng cộng 4.899 bản ghi cùng 9.079 quan sát khảo sát tách riêng theo cấp tỉnh trong bảng regional_price_observations: (1) Nhóm 3 mặt hàng chủ lực đạt 100% URL bài báo kiểm chứng riêng từng ngày (Lúa gạo IR50404: 442 phiên vietnambiz.vn & VFA vietfood.org.vn; Cà phê Robusta: 919 phiên vietnambiz.vn & giacaphe.com; Hồ tiêu đen: 793 phiên vietnambiz.vn); (2) Nhóm Mía đường 10 CCS (729 phiên) quy đổi minh bạch từ sàn ICE Sugar #11 (Yahoo Finance SB=F x USD/VND) kết hợp 8 bài báo khảo sát vụ ép 2024–2026 tại Khánh Hòa, Phú Yên, Gia Lai; và (3) Nhóm 4 đặc sản mở rộng (Dâu tây Đà Lạt, Khoai tây Đà Lạt, Khoai lang tím Vĩnh Long, Hạt điều — 504 phiên/mặt hàng) neo giá khảo sát sống tại Việt Nam (kamereo.vn, namtinhvegetable.com, banggianongsan.com) kết hợp chuỗi tham chiếu Proxy Index ETF Yahoo Finance (DBA, MOO, CORN, SOYB x USD/VND) do thị trường rau củ nội địa không niêm yết giá hằng ngày nhiều năm.

Lưu ý về mốc thời gian thực nghiệm: Toàn bộ số liệu bảng biểu và chỉ số đánh giá mô hình trình bày trong Chương 4 được chốt tại mốc ngày 23/11/2026 để bảo đảm tính nhất quán học thuật khi đối chiếu; trong quá trình vận hành thực tế, hệ thống AgroForecast tiếp tục tự động thu thập dữ liệu phiên mới và tái huấn luyện hằng ngày qua bộ lập lịch nền APScheduler (06:00 và 18:00 GMT+7). Bảng 4.1 trình bày thống kê chi tiết tại mốc chốt 23/11/2026.


**Bảng 4.1. Thống kê bộ dữ liệu lịch sử thực nghiệm của 8 loại nông sản trong CSDL PostgreSQL (chốt mốc 23/11/2026)**

| ID | Mã nông sản | Tên nông sản | Địa phương chuẩn (Tại vườn/ruộng) | Số bản ghi | Giai đoạn dữ liệu | Giá mới nhất |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | RICE_IR504 | Lúa gạo IR50404 | Huyện Châu Phú, An Giang (Tại ruộng) | 442 | 01/01/2024 - 23/11/2026 | 6.850 VNĐ/kg |
| 2 | COFFEE_ROBUSTA | Cà phê Robusta | Huyện Cư M'gar, Đắk Lắk (Tại vườn) | 919 | 04/01/2024 - 23/11/2026 | 71.700 VNĐ/kg |
| 3 | PEPPER_BLACK | Hồ tiêu đen | Huyện Chư Sê, Gia Lai (Tại vườn) | 793 | 04/01/2024 - 23/11/2026 | 129.100 VNĐ/kg |
| 4 | SUGARCANE | Mía đường 10 CCS | Huyện Tây Hòa, Phú Yên / Khánh Hòa | 729 | 02/01/2024 - 23/11/2026 | 1.230.000 VNĐ/tấn |
| 5 | STRAWBERRY | Dâu tây Đà Lạt | Phường 8, Đà Lạt (Tại vườn) | 504 | 21/11/2024 - 23/11/2026 | 100.000 VNĐ/kg |
| 6 | POTATO | Khoai tây Đà Lạt | Phường 7, Đà Lạt (Tại vườn) | 504 | 21/11/2024 - 23/11/2026 | 20.000 VNĐ/kg |
| 7 | SWEET_POTATO | Khoai lang tím Vĩnh Long | Huyện Bình Tân, Vĩnh Long (Tại ruộng) | 504 | 21/11/2024 - 23/11/2026 | 16.000 VNĐ/kg |
| 8 | CASHEW_NUT | Hạt điều thô | Huyện Bù Đăng, Bình Phước (Tại vườn) | 504 | 21/11/2024 - 23/11/2026 | 32.500 VNĐ/kg |



## 4.2. Kết quả thực nghiệm huấn luyện và đánh giá sai số của 5 mô hình học máy


### 4.2.1. Thiết lập siêu tham số (Hyperparameters) & Đặc trưng ngoại sinh nhân quả cho 5 mô hình

Để đảm bảo tính công bằng, chống rò rỉ dữ liệu tuyệt đối (Zero Data Leakage) và khả năng tái lập khoa học (random_state = 42), cả 5 mô hình được huấn luyện bằng phương pháp dự báo lợi suất log (Stationary Log-Return) và kiểm định Walk-Forward cuộn 7 ngày trong app/services/training_service.py và ml_pipeline/history_models.py:

1. Mô hình PyTorch Stacked LSTM (7 kênh nhân quả): Kiến trúc 2 tầng ẩn (num_layers = 2, hidden_size = 24), độ dài chuỗi seq_length = 14 ngày, 7 kênh đầu vào gồm [lợi suất log r_t, độ lệch trung bình động MA7, biến động thực tế Vol7, sin/cos chu kỳ năm, lợi suất tỷ giá USD/VND và lợi suất dầu thô WTI <= t-1], tối ưu hóa AdamW (lr = 0.002, weight_decay = 1e-2) và SmoothL1Loss. Bộ chuẩn hóa StandardScaler chỉ fit duy nhất trên tập Train.

2. Mô hình Facebook Prophet (trên miền Log): Cấu hình seasonal Fourier năm/tuần thích nghi theo độ dài chuỗi (changepoint_prior_scale = 0.01, seasonality_prior_scale = 0.15), neo gốc nhân quả tại điểm quan sát cuối t0 giúp triệt tiêu hiện tượng đứt gãy mức giá tại điểm chuyển giao lịch sử - dự báo.

3. Mô hình ARIMA (trên miền Log): Tự động tuyển chọn bậc ổn định từ tập ứng viên {(2,1,1), (1,1,1), (1,1,0), (0,1,0)} trên tập Train và áp dụng tham số đóng băng (.apply()) lên từng cửa sổ kiểm định Walk-Forward (không tái khớp lên tập Test).

4. Mô hình XGBoost Regressor (22 đặc trưng nhân quả): Cấu hình n_estimators = 160, max_depth = 3, learning_rate = 0.03, subsample = 0.8, colsample_bytree = 0.8, điều chuẩn L1/L2 (reg_alpha = 0.5, reg_lambda = 8.0) trên 18 đặc trưng trễ/động lượng/biến động/lịch + 4 đặc trưng ngoại sinh trễ (fx_r1, fx_mom7, oil_r1, oil_mom7).

5. Mô hình Random Forest Regressor (22 đặc trưng nhân quả): Cấu hình n_estimators = 150 cây quyết định, max_depth = 6, max_features = 'sqrt' trên cùng tập 22 đặc trưng nhân quả, kèm hiệu chỉnh khoảng tin cậy Conformal 95% mở rộng theo sqrt(h).


### 4.2.2. Bảng tổng hợp và phân tích sai số thực nghiệm Walk-Forward 7 ngày của 5 mô hình trên 8 nông sản

Quá trình thực nghiệm đã tiến hành huấn luyện và kiểm định Walk-Forward cuộn 7 ngày (Zero Data Leakage, tích hợp biến ngoại sinh USD/VND & WTI) cho toàn bộ 40 tổ hợp (8 mặt hàng nông sản x 5 mô hình học máy). Bảng 4.2 trình bày đầy đủ số liệu sai số thực tế (MAE, RMSE, MAPE, R2 và độ phủ thực nghiệm 95% CI - PICP) trích xuất trực tiếp từ bảng training_runs và forecasts trong PostgreSQL ngày 23/11/2026.


**Bảng 4.2. Kết quả thực nghiệm Walk-Forward 7 ngày (có biến ngoại sinh USD/VND & WTI) của 5 mô hình AI trên 8 mặt hàng nông sản**

| Nông sản | Mô hình AI | MAE (VNĐ) | RMSE (VNĐ) | MAPE (%) | Hệ số R2 | Đánh giá / Xếp hạng (PICP 95%) |
| --- | --- | --- | --- | --- | --- | --- |
| Lúa IR50404 | ARIMA | 100,24 | 169,20 | 1,58% | 0,5340 | Tối ưu nhất ★ (Hạng 1 - PICP 89,4%) |
| Lúa IR50404 | Prophet | 100,13 | 156,67 | 1,59% | 0,6005 | Hạng 2 - RMSE thấp nhất & R2 cao nhất (PICP 89,4%) |
| Lúa IR50404 | XGBoost | 104,50 | 170,92 | 1,65% | 0,5244 | Hạng 3 (PICP 87,9%) |
| Lúa IR50404 | Random Forest | 105,29 | 170,13 | 1,67% | 0,5288 | Hạng 4 (PICP 89,4%) |
| Lúa IR50404 | LSTM | 111,45 | 171,72 | 1,77% | 0,5200 | Hạng 5 (PICP 89,4%) |
| Cà phê Robusta | PyTorch LSTM | 1.555,41 | 1.978,28 | 1,79% | 0,8972 | Tối ưu nhất ★ (Hạng 1 — Vượt Baseline 1,88%, PICP 92,2%) |
| Cà phê Robusta | ARIMA | 1.605,21 | 2.121,40 | 1,86% | 0,8818 | Hạng 2 - Vượt Baseline 1,88% (PICP 90,0%) |
| Cà phê Robusta | Random Forest | 1.643,09 | 2.087,40 | 1,90% | 0,8856 | Hạng 3 - RMSE thấp thứ 2 (PICP 90,0%) |
| Cà phê Robusta | XGBoost | 1.703,99 | 2.120,44 | 1,96% | 0,8819 | Hạng 4 (PICP 92,2%) |
| Cà phê Robusta | Prophet | 1.882,04 | 2.386,65 | 2,15% | 0,8504 | Hạng 5 (PICP 87,8%) |
| Hồ tiêu đen | ARIMA | 990,46 | 1.643,77 | 0,74% | 0,3256 | Tối ưu nhất ★ (Vượt Baseline RMSE 1.646,34 - PICP 94,4%) |
| Hồ tiêu đen | XGBoost | 1.045,64 | 1.646,95 | 0,78% | 0,3230 | Hạng 2 - Sai số cực thấp (PICP 94,4%) |
| Hồ tiêu đen | Random Forest | 1.054,90 | 1.631,93 | 0,78% | 0,3353 | Hạng 3 - RMSE thấp nhất & R2 cao nhất (PICP 94,4%) |
| Hồ tiêu đen | LSTM | 1.070,99 | 1.729,36 | 0,79% | 0,2536 | Hạng 4 - Đạt chuẩn < 1% (PICP 92,2%) |
| Hồ tiêu đen | Prophet | 1.174,41 | 1.708,35 | 0,87% | 0,2716 | Hạng 5 (PICP 94,4%) |
| Mía đường 10 CCS | Prophet | 34.245,40 | 46.011,00 | 2,62% | 0,8571 | Tối ưu nhất ★ (Vượt Baseline 2,74% - PICP 97,8%) |
| Mía đường 10 CCS | Random Forest | 35.303,99 | 48.177,63 | 2,70% | 0,8434 | Hạng 2 - Vượt Baseline 2,74% (PICP 96,7%) |
| Mía đường 10 CCS | ARIMA | 35.800,52 | 47.960,56 | 2,74% | 0,8448 | Hạng 3 (PICP 97,8%) |
| Mía đường 10 CCS | LSTM | 36.056,90 | 48.324,82 | 2,75% | 0,8424 | Hạng 4 (PICP 96,7%) |
| Mía đường 10 CCS | XGBoost | 36.244,16 | 48.578,33 | 2,77% | 0,8408 | Hạng 5 (PICP 97,8%) |
| Dâu tây Đà Lạt | Prophet | 1.164,79 | 1.610,18 | 1,08% | 0,8693 | Tối ưu nhất ★ (Vượt sâu Baseline 1,30% - PICP 100%) |
| Dâu tây Đà Lạt | ARIMA | 1.393,33 | 1.684,24 | 1,30% | 0,8570 | Hạng 2 (PICP 100,0%) |
| Dâu tây Đà Lạt | XGBoost | 1.398,31 | 1.687,84 | 1,30% | 0,8564 | Hạng 3 (PICP 100,0%) |
| Dâu tây Đà Lạt | Random Forest | 1.400,17 | 1.694,39 | 1,31% | 0,8553 | Hạng 4 (PICP 100,0%) |
| Dâu tây Đà Lạt | LSTM | 1.429,96 | 1.864,54 | 1,35% | 0,8247 | Hạng 5 (PICP 93,3%) |
| Khoai tây Đà Lạt | Prophet | 276,05 | 368,60 | 1,30% | 0,7119 | Tối ưu nhất ★ (Vượt Baseline 1,39% - PICP 100%) |
| Khoai tây Đà Lạt | ARIMA | 295,28 | 389,19 | 1,40% | 0,6789 | Hạng 2 (PICP 100,0%) |
| Khoai tây Đà Lạt | Random Forest | 301,30 | 390,70 | 1,42% | 0,6764 | Hạng 3 (PICP 100,0%) |
| Khoai tây Đà Lạt | XGBoost | 302,97 | 399,72 | 1,43% | 0,6612 | Hạng 4 (PICP 100,0%) |
| Khoai tây Đà Lạt | LSTM | 338,12 | 439,38 | 1,60% | 0,5907 | Hạng 5 (PICP 98,7%) |
| Khoai lang tím | XGBoost | 305,09 | 393,93 | 1,71% | 0,8844 | Tối ưu nhất ★ (R2 = 0,884 - PICP 97,3%) |
| Khoai lang tím | ARIMA | 312,35 | 399,68 | 1,75% | 0,8810 | Hạng 2 (PICP 97,3%) |
| Khoai lang tím | Random Forest | 316,30 | 410,99 | 1,77% | 0,8741 | Hạng 3 (PICP 97,3%) |
| Khoai lang tím | LSTM | 342,59 | 437,71 | 1,93% | 0,8573 | Hạng 4 (PICP 97,3%) |
| Khoai lang tím | Prophet | 348,48 | 416,80 | 1,97% | 0,8706 | Hạng 5 (PICP 96,0%) |
| Hạt điều thô | ARIMA | 444,00 | 555,34 | 1,30% | 0,8127 | Tối ưu nhất ★ (R2 = 0,813 - PICP 100%) |
| Hạt điều thô | XGBoost | 452,95 | 561,88 | 1,33% | 0,8082 | Hạng 2 (PICP 100,0%) |
| Hạt điều thô | LSTM | 459,15 | 578,31 | 1,35% | 0,7968 | Hạng 3 (PICP 98,7%) |
| Hạt điều thô | Random Forest | 477,33 | 583,76 | 1,40% | 0,7930 | Hạng 4 (PICP 100,0%) |
| Hạt điều thô | Prophet | 491,06 | 696,47 | 1,43% | 0,7053 | Hạng 5 (PICP 97,3%) |



### 4.2.3. Nhận xét và phân tích chuyên sâu kết quả thực nghiệm 5 mô hình

Từ số liệu thực nghiệm Walk-Forward 7 ngày không rò rỉ dữ liệu chốt tại mốc 23/11/2026 trong Bảng 4.2, có thể rút ra ba kết luận khoa học quan trọng chứng minh hiệu quả của kiến trúc đa mô hình kết hợp biến ngoại sinh nhân quả trong AgroForecast:

Thứ nhất, trên toàn bộ 8/8 mặt hàng nông sản (40/40 tổ hợp mô hình), sai số MAPE của mô hình tối ưu đều nằm rất sâu trong ngưỡng < 3% (từ 0,74% đến 2,62%), đạt chuẩn 'Dự báo độ chính xác rất cao' (< 10%) theo phân loại quốc tế của Lewis, với 40/40 mô hình đều đạt hệ số xác định R2 dương (0,2536 đến 0,8972) và độ bao phủ thực nghiệm khoảng tin cậy 95% Conformal CI đạt 89,4% – 100,0%.

Thứ hai, việc tích hợp 2 biến ngoại sinh vĩ mô nhân quả (USD/VND và Dầu thô WTI chỉ lấy độ trễ quá khứ <= t-1) phát huy tác dụng mạnh mẽ nhất trên mặt hàng xuất khẩu biến động sâu nhất hệ thống là Cà phê Robusta (919 ngày quan sát thật): mạng học sâu PyTorch Stacked LSTM (7 kênh nhân quả) vươn lên Hạng 1 tuyệt đối trên cả 4 chỉ số với MAE = 1.555,41 VNĐ/kg, RMSE = 1.978,28 VNĐ/kg, MAPE = 1,79%, R2 = 0,8972 và PICP 95% = 92,22%, vượt trội rõ rệt so với Naive Baseline (MAE = 1.621,11, RMSE = 2.147,01 VNĐ/kg, MAPE = 1,88%).

Thứ ba, kết quả khẳng định định lý No Free Lunch trong dự báo nông sản: không có một mô hình đơn lẻ nào thắng tuyệt đối trên mọi chuỗi. PyTorch Stacked LSTM dẫn đầu trên chuỗi xuất khẩu dày và phi tuyến mạnh (Cà phê Robusta MAPE 1,79%, R2 = 0,8972); ARIMA tối ưu trên chuỗi bước giá hẹp/tự tương quan cao (Hồ tiêu đen 0,74%, Hạt điều 1,30%, Lúa IR50404 1,58%); Prophet dẫn đầu trên chuỗi có xu thế và chu kỳ mùa vụ rõ (Dâu tây Đà Lạt 1,08%, Khoai tây Đà Lạt 1,30%, Mía đường 2,62%); và XGBoost dẫn đầu Khoai lang tím Vĩnh Long (1,71%, R2 = 0,8844). Do đó, cơ chế tự động xếp hạng và gắn sao (★) đề xuất mô hình tối ưu theo từng mặt hàng mang lại giá trị thực tiễn cao.


### 4.2.4. Kết quả dự báo giá bán tại vườn/ruộng trên 29 địa phương cấp huyện, thị xã, phường

Nhằm giải quyết triệt để yêu cầu thực tiễn của giảng viên hướng dẫn và người nông dân về việc phản ánh đúng giá bán ra tại vườn/ruộng ở từng địa phương thay vì gộp chung theo vùng lớn, hệ thống AgroForecast đã kết hợp đầu ra của mô hình học máy tối ưu nhất tại vùng chuẩn với độ lệch giá cơ sở (Basis Spread) và định giá Haversine trên 33 tỉnh/thành. Bảng 4.3 trình bày kết quả tính toán giá bán tại vườn/ruộng chốt tại mốc 23/11/2026 và dự báo 14 ngày tới kèm biên độ khoảng tin cậy Conformal 95% tại các địa phương tiêu biểu.


**Bảng 4.3. Kết quả dự báo giá nông sản bán tại vườn/ruộng theo từng huyện địa phương (Kỳ hạn +14 ngày, chốt mốc 23/11/2026)**

| Mặt hàng nông sản | Địa phương bán tại vườn / tại ruộng | Chênh lệch (Spread) | Giá tại vườn hiện tại | Mô hình tối ưu | Giá dự báo (+14 ngày) | Khoảng tin cậy 95% (Lower - Upper) |
| --- | --- | --- | --- | --- | --- | --- |
| Cà phê Robusta | Huyện Cư M'gar - Đắk Lắk (Tại vườn) | 0 đ/kg | 71.700 đ/kg | PyTorch LSTM | 72.913 đ/kg | 64.823 - 81.003 đ/kg |
| Cà phê Robusta | Thị xã Buôn Hồ - Đắk Lắk (Tại vườn) | -100 đ/kg | 71.600 đ/kg | PyTorch LSTM | 72.813 đ/kg | 64.723 - 80.903 đ/kg |
| Cà phê Robusta | Huyện Di Linh - Lâm Đồng (Tại vườn) | -800 đ/kg | 70.900 đ/kg | PyTorch LSTM | 72.113 đ/kg | 64.023 - 80.203 đ/kg |
| Cà phê Robusta | Huyện Chư Prông - Gia Lai (Tại vườn) | -300 đ/kg | 71.400 đ/kg | PyTorch LSTM | 72.613 đ/kg | 64.523 - 80.703 đ/kg |
| Cà phê Robusta | Huyện Đắk Mil - Đắk Nông (Tại vườn) | +200 đ/kg | 71.900 đ/kg | PyTorch LSTM | 73.113 đ/kg | 65.023 - 81.203 đ/kg |
| Hồ tiêu đen | Huyện Chư Sê - Gia Lai (Tại vườn) | 0 đ/kg | 129.100 đ/kg | ARIMA | 129.080 đ/kg | 120.190 - 137.971 đ/kg |
| Hồ tiêu đen | Huyện Châu Đức - Bà Rịa Vũng Tàu (Tại vườn) | +1.500 đ/kg | 130.600 đ/kg | ARIMA | 130.580 đ/kg | 121.690 - 139.471 đ/kg |
| Hồ tiêu đen | Huyện Lộc Ninh - Bình Phước (Tại vườn) | -500 đ/kg | 128.600 đ/kg | ARIMA | 128.580 đ/kg | 119.690 - 137.471 đ/kg |
| Lúa gạo IR50404 | Huyện Châu Phú - An Giang (Tại ruộng) | 0 đ/kg | 6.850 đ/kg | ARIMA | 6.850 đ/kg | 5.742 - 7.958 đ/kg |
| Lúa gạo IR50404 | Huyện Tháp Mười - Đồng Tháp (Tại ruộng) | +150 đ/kg | 7.000 đ/kg | ARIMA | 7.000 đ/kg | 5.892 - 8.108 đ/kg |
| Lúa gạo IR50404 | Huyện Tân Hiệp - Kiên Giang (Tại ruộng) | -150 đ/kg | 6.700 đ/kg | ARIMA | 6.700 đ/kg | 5.592 - 7.808 đ/kg |
| Dâu tây Đà Lạt | Phường 8 - TP. Đà Lạt (Tại vườn) | 0 đ/kg | 100.000 đ/kg | Prophet | 98.666 đ/kg | 91.995 - 105.338 đ/kg |
| Dâu tây Đà Lạt | Huyện Lạc Dương - Lâm Đồng (Tại vườn) | -3.000 đ/kg | 97.000 đ/kg | Prophet | 95.666 đ/kg | 88.995 - 102.338 đ/kg |
| Dâu tây Đà Lạt | Huyện Mộc Châu - Sơn La (Tại vườn) | -15.000 đ/kg | 85.000 đ/kg | Prophet | 83.666 đ/kg | 76.995 - 90.338 đ/kg |
| Khoai lang tím | Huyện Bình Tân - Vĩnh Long (Tại ruộng) | 0 đ/kg | 16.000 đ/kg | XGBoost | 15.988 đ/kg | 14.444 - 17.533 đ/kg |
| Khoai lang tím | Huyện Châu Thành - Đồng Tháp (Tại ruộng) | -400 đ/kg | 15.600 đ/kg | XGBoost | 15.588 đ/kg | 14.044 - 17.133 đ/kg |
| Khoai tây Đà Lạt | Phường 7 (Thái Phiên) - Đà Lạt (Tại vườn) | 0 đ/kg | 20.000 đ/kg | Prophet | 20.000 đ/kg | 17.071 - 22.928 đ/kg |
| Khoai tây Đà Lạt | Huyện Đức Trọng - Lâm Đồng (Tại vườn) | -800 đ/kg | 19.200 đ/kg | Prophet | 19.200 đ/kg | 16.271 - 22.128 đ/kg |
| Khoai tây Đà Lạt | Huyện Đơn Dương - Lâm Đồng (Tại vườn) | -1.000 đ/kg | 19.000 đ/kg | Prophet | 19.000 đ/kg | 16.071 - 21.928 đ/kg |
| Hạt điều thô | Huyện Bù Đăng - Bình Phước (Tại vườn) | 0 đ/kg | 32.500 đ/kg | ARIMA | 32.500 đ/kg | 29.938 - 35.062 đ/kg |
| Hạt điều thô | Huyện Định Quán - Đồng Nai (Tại vườn) | -400 đ/kg | 32.100 đ/kg | ARIMA | 32.100 đ/kg | 29.538 - 34.662 đ/kg |
| Mía đường 10 CCS | Huyện Tây Hòa - Phú Yên / Khánh Hòa | 0 đ/tấn | 1.230.000 đ/tấn | Prophet | 1.215.719 đ/tấn | 962.819 - 1.468.618 đ/tấn |



## 4.3. Kết quả cài đặt các phân hệ chức năng trên giao diện Web AgroForecast


### 4.3.1. Phân hệ Tổng quan thị trường giá nông sản bán tại vườn (src/app/page.tsx)

Khi truy cập vào trang chủ của hệ thống tại địa chỉ http://localhost:3000, người dùng được cung cấp bức tranh toàn cảnh về thị trường nông sản Việt Nam thông qua dải 4 chỉ số tổng hợp (Unified Market Summary Strip): (1) Danh mục theo dõi gồm 8 mặt hàng nông sản chủ lực kèm ghi chú giá bán tại vườn/ruộng địa phương; (2) Độ rộng thị trường thống kê tự động số lượng mặt hàng tăng giá, giảm giá, đi ngang và mức biến động bình quân toàn thị trường (%); (3) Mặt hàng tăng trưởng mạnh nhất trong phiên; và (4) Lối tắt điều hướng nhanh sang trang Dự báo AI hoặc trang Lịch sử giá.

Ngay phía dưới là bộ công cụ Tìm kiếm và Lọc đa tiêu chí (QuickSearchBar) cho phép lọc tức thời theo từ khóa tên nông sản, nhóm ngành hàng (Lương thực, Nông sản xuất khẩu, Gia vị, Nông sản đặc sản, Cây công nghiệp) hoặc địa phương bán tại vườn. Lưới thẻ nông sản (CommodityCard) hiển thị sắc nét mức giá hiện tại bằng phông chữ số JetBrains Mono, huy hiệu % tăng/giảm màu xanh lục hoặc đỏ san hô và đồ thị thu nhỏ Sparkline 7 ngày đã được tối ưu hóa miền trục tung để thể hiện rõ độ dốc biến động. Phần cuối trang bố trí song song Biểu đồ đối sánh xu hướng thị trường (MarketComparisonChart) và Bảng khảo sát giá bán tại vườn theo địa phương (RegionalPriceTable).


### 4.3.2. Phân hệ Phân tích & Dự báo AI đa mô hình theo địa phương bán tại vườn (src/app/forecast/page.tsx)

Đây là phân hệ trung tâm thể hiện toàn bộ sức mạnh học máy của dự án. Thanh công cụ hợp nhất (Unified Instrument & Filter Bar) được thiết kế thành hai tầng gọn gàng: tầng trên cho phép chọn Mặt hàng nông sản, chuyển đổi tức thời giữa 5 tab Thuật toán AI (LSTM, Prophet, ARIMA, XGBoost, Random Forest — tự động kích hoạt mô hình ★ tối ưu) và 3 nút Kỳ hạn dự báo chuẩn (7 ngày, 14 ngày, 30 ngày — khóa cứng Literal[7, 14, 30] ở cả API và giao diện); tầng dưới là Bộ chọn Địa phương bán tại vườn/ruộng (Spatio-Temporal Selector) kết hợp bộ chọn 33 tỉnh/thành trên Topbar.

Ngay dưới thanh công cụ là Dải 4 chỉ số dự báo: (1) Giá bán tại vườn/ruộng hiện tại ở huyện đang chọn; (2) Giá dự báo cuối kỳ hạn kèm % tăng/giảm và mức chênh lệch tuyệt đối bằng VNĐ; (3) Biên độ dao động cuối kỳ (LowerCI - UpperCI) tính theo sai số kiểm định RMSE; và (4) Sai số mô hình MAPE kèm tính năng tự động phát hiện và gợi ý nút 'Áp dụng' nếu có một mô hình khác trong 5 mô hình đạt sai số RMSE thấp hơn mô hình đang chọn.

Biểu đồ chính (Main Price & Forecast ComposedChart) kết nối liền mạch đường giá thực tế 30 ngày gần nhất (màu xanh lục #059669) với đường dự báo AI đứt nét (màu xanh dương #2563EB) và dải băng khoảng tin cậy 95% tô bóng chuyển sắc. Phía dưới biểu đồ là khu vực phân tích chuyên sâu gồm 2 cột: bên trái là mô-đun Giải thích mô hình AI (XAIFeatureDrivers) trực quan hóa % đóng góp của 5 yếu tố thúc đẩy giá; bên phải là Biểu đồ cột ngang so sánh trực tiếp sai số RMSE/MAE/MAPE của cả 5 mô hình và bảng thông số kiểm định trên tập Holdout. Cuối trang là Bảng lịch trình giá dự báo chi tiết từng ngày có tích hợp nút xuất tập tin CSV hỗ trợ mã hóa UTF-8 BOM hiển thị chuẩn tiếng Việt trên Microsoft Excel.


### 4.3.3. Phân hệ Lịch sử biến động giá, So sánh thị trường, Cảnh báo Email và Quản trị Admin

1. Phân hệ Lịch sử giá (src/app/history/page.tsx): Hiển thị quy trình 4 bước minh bạch (Lịch sử -> Kiểm tra -> Huấn luyện -> Dự báo), cho phép lọc khoảng ngày hoặc chọn nhanh 30 ngày, 90 ngày, 1 năm, toàn bộ lịch sử; hiển thị đường dẫn URL gốc tới cơ quan công bố để người dùng kiểm chứng chéo; liệt kê trạng thái xác minh (Thu thập từ nguồn / Admin xác nhận / Chưa xác minh) và đánh giá mức độ sẵn sàng của chuỗi dữ liệu trước khi huấn luyện AI.

2. Phân hệ So sánh nông sản (src/app/compare/page.tsx): Cho phép bật/tắt linh hoạt từng chuỗi nông sản trên biểu đồ đường cong tăng trưởng chuẩn hóa và tra cứu bảng đối sánh biên độ giá sàn/trần tại từng địa phương.

3. Phân hệ Cảnh báo biến động giá (src/app/alerts/page.tsx): Cho phép nông hộ tạo quy tắc cảnh báo khi giá vượt ngưỡng hoặc xuống dưới ngưỡng, bật/tắt quy tắc, kích hoạt gửi thử Email thông báo ngay trên giao diện và xem nhật ký các lần cảnh báo đã kích hoạt.

4. Phân hệ Quản trị Admin (src/app/admin/page.tsx): Dành riêng cho tài khoản Quản trị viên đã xác thực JWT, cung cấp 5 tab nghiệp vụ: Quản lý điểm giá & Nhập/Xuất CSV; Quản lý danh mục nông sản; Điều phối tác vụ nền (chạy Bot thu thập dữ liệu & Huấn luyện lại 5 mô hình AI) kèm chọn mô hình AI mặc định; Xem nhật ký Crawler Logs; và Quản lý phân quyền, khóa/mở khóa tài khoản người dùng.


### 4.2.5. Phân tích chi tiết hành vi dự báo của 5 thuật toán trên từng mặt hàng và bài học kinh nghiệm

Qua quá trình thực nghiệm huấn luyện và kiểm định Walk-Forward 7 ngày trên 40 tổ hợp mô hình - nông sản (chốt mốc 23/11/2026), khóa luận đúc kết được những quy luật thực nghiệm quan trọng về sự tương thích giữa bản chất chuỗi thời gian nông sản Việt Nam và cấu trúc toán học của từng thuật toán:

1. Tại sao PyTorch Stacked LSTM (7 kênh nhân quả) vươn lên Hạng 1 tuyệt đối trên Cà phê Robusta (MAPE = 1,79%, RMSE = 1.978,28 VNĐ/kg, R² = 0,8972)? Cà phê Robusta là chuỗi xuất khẩu dày nhất (919 phiên thật 2024–2026) có biên độ biến động lớn theo tồn kho London ICE, tỷ giá USD/VND và chi phí năng lượng. Khi được cung cấp đồng thời 5 kênh nội sinh và 2 kênh ngoại sinh nhân quả (lợi suất USD/VND & WTI <= t-1), cổng nhớ dài-ngắn của Stacked LSTM nắm bắt vượt trội động lực hồi quy phi tuyến và vượt sâu Naive Baseline (RMSE 2.147,01 VNĐ/kg).

2. Tại sao Facebook Prophet dẫn đầu trên Mía đường 10 CCS (MAPE = 2,62%, R² = 0,8571), Dâu tây Đà Lạt (MAPE = 1,08%, R² = 0,8693) và Khoai tây Đà Lạt (MAPE = 1,30%, R² = 0,7119)? Nhóm mặt hàng có nhịp mùa vụ và chu kỳ thương mại rõ nét trên miền Log hưởng lợi trực tiếp từ phép phân rã xu thế từng khúc kết hợp chuỗi Fourier và cơ chế neo gốc nhân quả tại điểm quan sát cuối t0.

3. Tại sao ARIMA tối ưu trên Hồ tiêu đen (MAPE = 0,74%, RMSE = 1.643,77 VNĐ/kg), Hạt điều (MAPE = 1,30%, R² = 0,8127) và Lúa gạo IR50404 (MAPE = 1,58%)? Các chuỗi này có tính tự tương quan bậc 1–2 chặt và biên độ dao động ngày hẹp, giúp mô hình thống kê tinh gọn ít tham số tránh quá khớp và giữ sai số cực thấp.

4. Vai trò của XGBoost và Random Forest (22 đặc trưng nhân quả): XGBoost giành Hạng 1 trên Khoai lang tím Vĩnh Long (MAPE = 1,71%, R² = 0,8844) và bám sát Hạng 2 trên Hồ tiêu đen (0,78%) & Hạt điều (1,33%), trong khi Random Forest đạt RMSE thấp nhất toàn bảng trên Hồ tiêu đen (1.631,93 VNĐ/kg) và đứng thứ 2 về RMSE trên Cà phê Robusta (2.087,40 VNĐ/kg), khẳng định giá trị thực tiễn của cơ chế đối sánh đa mô hình tự động gắn sao ★.


## 4.4. Kiểm thử phần mềm và Kiểm tra bảo mật hệ thống theo chuẩn OWASP Top 10


### 4.4.1. Phương pháp kiểm thử 4 tầng và môi trường kiểm thử cô lập (Sandbox Testing)

Để đảm bảo chất lượng phần mềm đạt chuẩn công nghiệp trước khi nghiệm thu, hệ thống AgroForecast triển khai bộ kiểm thử tự động mở rộng lên 125 kịch bản Pytest Backend (kế thừa bộ nền tảng 72 kịch bản cốt lõi kết hợp nhóm kiểm thử phủ nhánh 98%, kiểm toán sự thật dữ liệu và chống rò rỉ biến ngoại sinh), đi kèm 3 Frontend Unit Tests và 4 Playwright E2E trên trình duyệt thật. Trong tệp cấu hình tests/conftest.py, hệ thống khởi tạo một cơ sở dữ liệu SQLite In-Memory hoàn toàn mới cho từng hàm kiểm thử và sử dụng cơ chế app.dependency_overrides[get_db] để chuyển hướng toàn bộ truy vấn CSDL vào môi trường cô lập này.

Bốn tầng kiểm thử được thực thi đồng bộ bao gồm: (1) Kiểm thử đơn vị hộp trắng (White-box Unit Testing) cho các hàm toán học lọc ngoại lai IQR, hàm tạo đặc trưng chuỗi thời gian, hàm tính sai số và hàm làm sạch bảo mật; (2) Kiểm thử tích hợp hộp xám (Grey-box API & Database Integration Testing) kiểm tra toàn bộ các Endpoint REST API và tính toàn vẹn khóa ngoại CSDL; (3) Kiểm định đường ống học máy (ML Pipeline Backtesting) kiểm tra huấn luyện thực tế cả 5 mô hình AI, cổng chặn sai số Threshold Gate và điều kiện biên của khoảng tin cậy 95%; và (4) Kiểm thử luồng nghiệp vụ đầu-cuối (End-to-End Workflow Testing).


### 4.4.2. Triển khai 6 lớp phòng vệ bảo mật ứng dụng theo chuẩn OWASP Top 10

Tại mô-đun app/core/security.py, app/core/deps.py và app/main.py, hệ thống đã cài đặt và kiểm chứng thực nghiệm 6 lớp phòng vệ bảo mật trọng yếu:

Lớp 1 - Băm mật khẩu một chiều Bcrypt với Salt ngẫu nhiên (Chống OWASP A02 - Cryptographic Failures): Sử dụng hàm bcrypt.gensalt() và bcrypt.hashpw() để mã hóa mật khẩu một chiều. Hai lần băm cùng một mật khẩu luôn sinh ra hai chuỗi hash khác biệt hoàn toàn, vô hiệu hóa tấn công từ điển và bảng cầu vồng (Rainbow Table Attack).

Lớp 2 - Xác thực phi trạng thái JWT (HS256) và Phân quyền RBAC (Chống OWASP A01 - Broken Access Control): Mỗi token truy cập được ký số bằng thuật toán HMAC-SHA256 kèm thời hạn hết hạn (exp) và vai trò (role). Khi tài khoản bị Quản trị viên khóa (is_active = False) hoặc khi tài khoản thường cố tình gọi API quản trị, bộ kiểm tra require_role() lập tức từ chối truy cập với mã lỗi HTTP 403 Forbidden.

Lớp 3 - Phòng chống tiêm mã lệnh SQL Injection (Chống OWASP A03 - Injection): 100% truy vấn dữ liệu sử dụng biểu thức ORM tham số hóa của SQLAlchemy, tách biệt hoàn toàn câu lệnh SQL và dữ liệu đầu vào.

Lớp 4 - Phòng chống XSS và CSV Formula Injection (Chống OWASP A03 - Injection): Hàm sanitize_text() dùng biểu thức chính quy loại bỏ toàn bộ thẻ <script>, <iframe>, HTML độc hại và mã hóa thực thể HTML khi người dùng đăng ký hoặc tạo quy tắc cảnh báo. Hàm sanitize_csv_cell() tự động phát hiện và vô hiệu hóa các ký tự kích hoạt macro độc hại (=, +, -, @) ở đầu ô dữ liệu khi nhập/xuất CSV.

Lớp 5 - Giới hạn tần suất truy cập cửa sổ trượt (Sliding Window Rate Limiter - Chống OWASP A04 & A07): Lớp RateLimiter sử dụng khóa đồng bộ luồng (threading.Lock) để giám sát số lượng request theo từng địa chỉ IP trong cửa sổ thời gian trượt (chặn HTTP 429 Too Many Requests khi vượt quá 25 lần đăng nhập/phút hoặc 10 tác vụ nặng/phút).

Lớp 6 - Gia cố 7 Tiêu đề Bảo mật HTTP (SecurityHeadersMiddleware - Chống OWASP A05): Mọi phản hồi HTTP từ máy chủ đều được gắn tự động 7 tiêu đề bảo mật: X-Content-Type-Options: nosniff, X-Frame-Options: DENY (chống Clickjacking), X-XSS-Protection: 1; mode=block, Strict-Transport-Security: max-age=31536000; includeSubDomains, Referrer-Policy: strict-origin-when-cross-origin, Permissions-Policy: geolocation=(), camera=(), microphone=() và Content-Security-Policy: default-src 'self'; frame-ancestors 'none'; object-src 'none'.


### 4.4.3. Ma trận kết quả thực thi bộ kiểm thử tự động cốt lõi và kiểm toán bảo mật (100% PASSED)

Toàn bộ 125 kịch bản Pytest Backend (gồm 72 kịch bản nền tảng tiêu biểu trình bày trong Bảng 4.3 và 53 kịch bản mở rộng về phủ nhánh 98%, kiểm toán sự thật dữ liệu, biến ngoại sinh nhân quả và vá bảo mật OWASP ở Mục 4.9) cùng 3 Frontend Unit Tests và 4 Playwright E2E đều đạt 100% PASSED.


**Bảng 4.3. Kết quả thực thi các nhóm kịch bản kiểm thử nền tảng cốt lõi và bảo mật OWASP Top 10**

| Mã Test | Tệp kiểm thử | Tên hàm kiểm thử (Test Case) | Nội dung kiểm tra & Kịch bản tấn công giả lập | Kết quả |
| --- | --- | --- | --- | --- |
| TC-01 | test_security_phase7.py | test_security_headers_present | Kiểm tra phản hồi HTTP gắn đủ 7 tiêu đề bảo mật chuẩn OWASP Top 10 | PASSED |
| TC-02 | test_security_phase7.py | test_password_hashing_and_verification | Kiểm tra băm mật khẩu Bcrypt sinh Salt ngẫu nhiên và xác thực chính xác | PASSED |
| TC-03 | test_security_phase7.py | test_sanitize_text_xss_protection | Kiểm tra lọc bỏ mã độc <script>alert('XSS')</script> trong dữ liệu đầu vào | PASSED |
| TC-04 | test_security_phase7.py | test_csv_formula_injection_defense | Kiểm tra chặn công thức thực thi lệnh độc hại =cmd|... và @SUM(...) trong CSV | PASSED |
| TC-05 | test_security_phase7.py | test_rate_limiter_mechanism | Kiểm tra Sliding Window Rate Limiter chặn IP khi vượt ngưỡng request | PASSED |
| TC-06 | test_security_phase7.py | test_jwt_tampering_expiration_and_alg_none | Kiểm tra từ chối JWT bị sửa chữ ký, hết hạn hoặc ký bằng khóa giả mạo | PASSED |
| TC-07 | test_security_phase7.py | test_rbac_privilege_escalation_defense | Kiểm tra chặn tài khoản thường gọi API Admin (/scrape, /retrain, /users -> 403) | PASSED |
| TC-08 | test_security_phase7.py | test_sql_injection_defense_in_commodity_query | Bơm payload SQLi (COFFEE' OR '1'='1, DROP TABLE) vào API tra cứu nông sản | PASSED |
| TC-09 | test_security_phase7.py | test_xss_sanitization_in_alert_creation | Kiểm tra chống Stored XSS khi tạo quy tắc cảnh báo chứa script đánh cắp cookie | PASSED |
| TC-10 | test_security_phase7.py | test_spatio_temporal_farm_gate_regional_pricing | Kiểm tra dự báo giá bán tại vườn theo huyện, độ lệch basisSpread và SHA-256 hash | PASSED |
| TC-11..20 | test_auth.py | 10 kịch bản kiểm thử xác thực (Auth Suite) | Đăng ký (201), trùng email (400), mật khẩu yếu (422), sai mật khẩu/token (401) | PASSED (10/10) |
| TC-21..29 | test_predictions.py | 9 kịch bản kiểm thử đường ống dự báo ML | Tạo đặc trưng Lag/Rolling, Threshold Gate, huấn luyện Prophet/XGBoost/LSTM, Cache | PASSED (9/9) |
| TC-30..40 | test_history_workflow.py | 11 kịch bản kiểm thử lịch sử & 5 mô hình thật | Lọc provenance, chặn dữ liệu unverified, kiểm định Holdout 5 mô hình AI thực tế | PASSED (11/11) |
| TC-41..52 | test_admin_*.py | 12 kịch bản kiểm thử phân hệ Quản trị Admin | Thống kê, nhật ký Scraper, chuyển đổi mô hình AI, nhập/xuất CSV, khóa tài khoản | PASSED (12/12) |
| TC-53..60 | test_vietnam_sources.py | 8 kịch bản kiểm thử bộ bóc tách nguồn Việt Nam | Kiểm tra Parser lấy đúng ngày, chợ, loại giá Bán tại hộ/vườn và đơn vị VNĐ/kg | PASSED (8/8) |
| TC-61..72 | test_pipeline.py & khác | 12 kịch bản kiểm thử hệ thống, IQR & Cảnh báo | Lọc ngoại lai IQR, điền khuyết chuỗi thời gian, kích hoạt cảnh báo Email, Health | PASSED (12/12) |



**Bảng 4.4. Danh mục đầy đủ 72 kịch bản kiểm thử tự động và kiểm tra bảo mật OWASP Top 10 (Đạt 72/72 PASSED)**

| STT | Tệp kiểm thử | Tên hàm kiểm thử (Test Function) | Loại kiểm thử / Bảo mật | Kết quả |
| --- | --- | --- | --- | --- |
| 1 | test_security_phase7.py | test_security_headers_present | Bảo mật OWASP A05 (7 HTTP Security Headers) | PASSED |
| 2 | test_security_phase7.py | test_password_hashing_and_verification | Bảo mật OWASP A02 (Băm Bcrypt + Salt ngẫu nhiên) | PASSED |
| 3 | test_security_phase7.py | test_sanitize_text_xss_protection | Bảo mật OWASP A03 (Lọc mã độc HTML/Script XSS) | PASSED |
| 4 | test_security_phase7.py | test_csv_formula_injection_defense | Bảo mật OWASP A03 (Chống CSV Macro Injection) | PASSED |
| 5 | test_security_phase7.py | test_rate_limiter_mechanism | Bảo mật OWASP A04/A07 (Sliding Window Rate Limit) | PASSED |
| 6 | test_security_phase7.py | test_jwt_tampering_expiration_and_alg_none | Bảo mật OWASP A02/A07 (Chống giả mạo chữ ký JWT) | PASSED |
| 7 | test_security_phase7.py | test_rbac_privilege_escalation_defense | Bảo mật OWASP A01 (Chống leo thang đặc quyền 403) | PASSED |
| 8 | test_security_phase7.py | test_sql_injection_defense_in_commodity_query | Bảo mật OWASP A03 (Chống SQL Injection ORM) | PASSED |
| 9 | test_security_phase7.py | test_xss_sanitization_in_alert_creation | Bảo mật OWASP A03 (Chống Stored XSS tại API Alert) | PASSED |
| 10 | test_security_phase7.py | test_spatio_temporal_farm_gate_regional_pricing | Kiểm định AI & Toàn vẹn SHA-256 + Giá tại vườn | PASSED |
| 11 | test_auth.py | test_register_success | Tích hợp API Xác thực (Đăng ký tài khoản mới 201) | PASSED |
| 12 | test_auth.py | test_register_duplicate_email | Tích hợp API Xác thực (Chặn trùng lặp Email 400) | PASSED |
| 13 | test_auth.py | test_register_invalid_email | Kiểm thử Validation (Chặn sai định dạng Email 422) | PASSED |
| 14 | test_auth.py | test_register_short_password | Kiểm thử Bảo mật (Chặn mật khẩu yếu < 6 ký tự 422) | PASSED |
| 15 | test_auth.py | test_login_success | Tích hợp API Xác thực (Đăng nhập & Cấp JWT 200) | PASSED |
| 16 | test_auth.py | test_login_wrong_password | Bảo mật Xác thực (Chặn sai mật khẩu 401) | PASSED |
| 17 | test_auth.py | test_login_nonexistent_email | Bảo mật Xác thực (Chặn tài khoản không tồn tại 401) | PASSED |
| 18 | test_auth.py | test_read_current_user_success | Tích hợp JWT Bearer Token (/api/v1/auth/me 200) | PASSED |
| 19 | test_auth.py | test_read_current_user_unauthorized | Bảo mật Truy cập (Chặn truy cập thiếu Token 401) | PASSED |
| 20 | test_auth.py | test_read_current_user_invalid_token | Bảo mật Truy cập (Chặn Token sai định dạng 401) | PASSED |
| 21 | test_commodities.py | test_read_commodities | Tích hợp API Nông sản (Lấy danh sách tổng quan) | PASSED |
| 22 | test_commodities.py | test_create_commodity_unauthorized | Bảo mật RBAC (Chặn khách tạo mới nông sản 401) | PASSED |
| 23 | test_commodities.py | test_create_commodity_as_admin | Tích hợp API Admin (Tạo mới nông sản hợp lệ) | PASSED |
| 24 | test_config.py | test_settings_loaded | Kiểm thử Đơn vị Cấu hình (Biến môi trường .env) | PASSED |
| 25 | test_health.py | test_root_endpoint | Kiểm thử Hệ thống (Endpoint gốc / trạng thái online) | PASSED |
| 26 | test_health.py | test_health_check_with_db | Kiểm thử Tích hợp CSDL (/health SELECT 1) | PASSED |
| 27 | test_health.py | test_cors_headers | Bảo mật CORS (Kiểm tra chính sách Cross-Origin) | PASSED |
| 28 | test_pipeline.py | test_handle_outliers_iqr | Kiểm thử Đơn vị Hộp trắng (Lọc ngoại lai IQR) | PASSED |
| 29 | test_pipeline.py | test_load_clean_data_empty | Kiểm thử Đơn vị Data Loader (Xử lý chuỗi rỗng) | PASSED |
| 30 | test_pipeline.py | test_load_clean_data_with_history | Kiểm thử Tích hợp Tiền xử lý (Điền khuyết & ADF) | PASSED |
| 31 | test_pipeline.py | test_alert_rule_evaluation | Kiểm thử Nghiệp vụ Cảnh báo (Kích hoạt vượt ngưỡng) | PASSED |
| 32 | test_pipeline.py | test_admin_trigger_scrape_api | Kiểm thử Tích hợp Tác vụ nền (Trigger Scrape Job) | PASSED |
| 33 | test_predictions.py | test_feature_engineering_tabular | Kiểm thử Đơn vị ML (Tạo biến trễ Lag & Rolling) | PASSED |
| 34 | test_predictions.py | test_model_trainer_evaluation_and_threshold | Kiểm thử Đơn vị ML (MAE/RMSE/MAPE/R2 & Gate) | PASSED |
| 35 | test_predictions.py | test_model_training_and_saving | Kiểm định Huấn luyện (Lưu model Prophet/XGB/LSTM) | PASSED |
| 36 | test_predictions.py | test_predictor_forecast_intervals | Kiểm định Toán học AI (lowerCI <= yhat <= upperCI) | PASSED |
| 37 | test_predictions.py | test_prediction_in_memory_cache | Kiểm thử Hiệu năng (In-Memory Cache < 50ms) | PASSED |
| 38 | test_predictions.py | test_api_predictions_forecast | Tích hợp API Dự báo (/api/v1/predictions/forecast) | PASSED |
| 39 | test_predictions.py | test_api_predictions_metrics | Tích hợp API Chỉ số sai số (/predictions/metrics) | PASSED |
| 40 | test_predictions.py | test_api_predictions_retrain | Bảo mật & Tích hợp Huấn luyện lại (/retrain) | PASSED |
| 41 | test_history_workflow.py | test_public_history_filters_provenance_and_gaps | Kiểm thử Nguồn gốc dữ liệu (Lọc unverified & gaps) | PASSED |
| 42 | test_history_workflow.py | test_training_does_not_read_holdout_and_invalidates_on_edit | Chống rò rỉ dữ liệu (Holdout Isolation & Hash) | PASSED |
| 43 | test_history_workflow.py | test_training_rejects_unverified_and_large_gaps | Bảo vệ chất lượng AI (Chặn chuỗi đứt đoạn/chưa duyệt) | PASSED |
| 44 | test_history_workflow.py | test_modeling_uses_latest_series_after_long_publication_break | Kiểm thử Chuỗi thời gian (Tách đoạn sau kỳ nghỉ dài) | PASSED |
| 45 | test_history_workflow.py | test_modeling_keeps_latest_complete_series_when_new_fragment_is_short | Kiểm thử Chuỗi thời gian (Giữ đoạn đủ điều kiện) | PASSED |
| 46 | test_history_workflow.py | test_periodic_reports_train_as_periods_without_creating_daily_prices | Kiểm định Chuỗi theo kỳ (Báo cáo định kỳ Mía đường) | PASSED |
| 47 | test_history_workflow.py | test_scraper_preserves_old_snapshot_and_stops_at_access_boundary | An toàn Scraper (Bảo toàn dữ liệu cũ khi nguồn chặn) | PASSED |
| 48 | test_history_workflow.py | test_parser_does_not_bypass_login | Tuân thủ An toàn (Không vượt rào xác thực nguồn) | PASSED |
| 49 | test_history_workflow.py | test_real_models_forecast_from_fixture_prefix[Random Forest] | Kiểm định Thực nghiệm Mô hình 1: Random Forest | PASSED |
| 50 | test_history_workflow.py | test_real_models_forecast_from_fixture_prefix[XGBoost] | Kiểm định Thực nghiệm Mô hình 2: XGBoost | PASSED |
| 51 | test_history_workflow.py | test_real_models_forecast_from_fixture_prefix[ARIMA] | Kiểm định Thực nghiệm Mô hình 3: ARIMA | PASSED |
| 52 | test_history_workflow.py | test_real_models_forecast_from_fixture_prefix[Prophet] | Kiểm định Thực nghiệm Mô hình 4: Facebook Prophet | PASSED |
| 53 | test_history_workflow.py | test_real_models_forecast_from_fixture_prefix[LSTM] | Kiểm định Thực nghiệm Mô hình 5: PyTorch LSTM | PASSED |
| 54 | test_observation_scraper.py | test_parse_published_coffee_average | Kiểm thử Đơn vị Parser (Bóc tách giá Cà phê) | PASSED |
| 55 | test_observation_scraper.py | test_rejects_wrong_published_date | Kiểm thử Toàn vẹn Ngày công bố (Chặn sai ngày) | PASSED |
| 56 | test_vietnam_sources.py | test_agro_validates_market_type_currency_and_date | Kiểm thử Nguồn Việt Nam (Chợ An Giang, Bán tại hộ) | PASSED |
| 57 | test_vietnam_sources.py | test_agro_follows_only_published_pager_and_rejects_repeated_page | Kiểm thử Phân trang Scraper (Chống lặp vô hạn) | PASSED |
| 58 | test_vietnam_sources.py | test_periodic_report_preserves_period_buying_and_selling | Kiểm thử Báo cáo Mía đường (Giá mua & Giá bán) | PASSED |
| 59 | test_vietnam_sources.py | test_periodic_collection_never_creates_daily_observations | Kiểm thử Tách biệt dữ liệu kỳ và dữ liệu ngày | PASSED |
| 60 | test_vietnam_sources.py | test_domestic_daily_collection_deduplicates_and_records_market | Kiểm thử Khử trùng lặp & Lưu siêu dữ liệu chợ | PASSED |
| 61 | test_admin_phase5.py | test_admin_stats | Tích hợp API Quản trị (Thống kê tổng quan hệ thống) | PASSED |
| 62 | test_admin_phase5.py | test_admin_crawler_logs | Tích hợp API Quản trị (Truy xuất nhật ký Crawler) | PASSED |
| 63 | test_admin_phase5.py | test_admin_active_model_switcher | Tích hợp API Quản trị (Chuyển đổi mô hình mặc định) | PASSED |
| 64 | test_admin_phase5.py | test_admin_import_and_export_csv | Tích hợp API Quản trị (Nhập và Xuất báo cáo CSV) | PASSED |
| 65 | test_admin_phase5.py | test_admin_user_role_and_status | Tích hợp Quản lý User (Đổi Role & Khóa tài khoản) | PASSED |
| 66 | test_admin_phase5.py | test_rbac_protection | Bảo mật Phân quyền Admin (Chặn truy cập trái phép) | PASSED |
| 67 | test_admin_workflows.py | test_lock_rejects_existing_token_and_unlock_restores_role | Bảo mật Phiên (Vô hiệu hóa ngay Token khi khóa User) | PASSED |
| 68 | test_admin_workflows.py | test_admin_cannot_demote_self_or_create_invalid_role | An toàn Quản trị (Chặn Admin tự hạ quyền/khóa mình) | PASSED |
| 69 | test_admin_workflows.py | test_price_import_filters_and_update | Kiểm thử Lưu vết chỉnh sửa (PriceRevision Audit) | PASSED |
| 70 | test_admin_workflows.py | test_real_job_lifecycle_and_conflict | Kiểm thử Tác vụ nền (Chặn chạy trùng 2 Job cùng lúc) | PASSED |
| 71 | test_admin_workflows.py | test_default_model_applies_to_forecast_api | Kiểm thử Đồng bộ cấu hình mô hình mặc định | PASSED |
| 72 | test_admin_workflows.py | test_scrape_job_auto_retrains_changed_ready_series | Kiểm thử Luồng E2E (Cào dữ liệu mới -> Tự động Retrain) | PASSED |



### 4.4.4. Phân tích chi tiết kịch bản kiểm thử thâm nhập (Penetration Testing) trên từng lỗ hổng OWASP

Để chứng minh hệ thống không chỉ cài đặt bảo mật trên lý thuyết mà thực sự chống chịu được các cuộc tấn công thực tế, dưới đây là phân tích chi tiết cơ chế hoạt động của 6 nhóm kịch bản tấn công giả lập trong tệp backend/tests/test_security_phase7.py và backend/tests/test_auth.py:

1. Kịch bản tấn công giả mạo chữ ký số và dùng lại JWT hết hạn (test_jwt_tampering_expiration_and_alg_none): Bài kiểm thử tạo ra một JWT hợp lệ với quyền role='admin', sau đó thực hiện 3 hành vi tấn công: (a) Thay đổi 5 ký tự cuối của phần chữ ký điện tử (Signature Tampering: token[:-5] + 'ABCDE'); (b) Tạo một token có thời gian sống âm (expires_delta = timedelta(seconds=-10)) để giả lập token đã hết hạn; và (c) Dùng một khóa bí mật giả mạo của kẻ tấn công để tự ký một payload {'sub': '1', 'role': 'admin'}. Trong cả 3 trường hợp, hàm decode_access_token() sử dụng PyJWT kiểm tra chữ ký HMAC-SHA256 đều phát hiện sai lệch và trả về None, buộc tầng Dependency chặn truy cập với mã HTTP 401 Unauthorized.

2. Kịch bản tấn công leo thang đặc quyền ngang và dọc (test_rbac_privilege_escalation_defense & test_lock_rejects_existing_token): Hệ thống tạo một tài khoản nông dân thông thường (normal_farmer@agro.vn, role='user'), đăng nhập lấy Bearer Token hợp lệ rồi dùng chính Token này gửi yêu cầu POST tới /api/v1/admin/tasks/scrape (chạy Bot cào dữ liệu), POST /api/v1/admin/tasks/retrain (huấn luyện lại AI), GET /api/v1/admin/users (xem danh sách tài khoản) và DELETE /api/v1/admin/prices/1 (xóa giá lịch sử). Kết quả thực nghiệm: 100% yêu cầu trái thẩm quyền bị bộ kiểm tra require_role(['admin']) chặn đứng với mã HTTP 403 Forbidden. Đặc biệt, kịch bản test_lock_rejects_existing_token kiểm chứng rằng ngay giây phút Admin khóa một tài khoản, mọi JWT Token đã cấp trước đó của tài khoản đó dù chưa hết hạn cũng bị vô hiệu hóa tức thời.

3. Kịch bản tấn công tiêm mã lệnh SQL Injection đa biến thể (test_sql_injection_defense_in_commodity_query): Bài kiểm thử bắn liên tiếp 3 payload SQLi kinh điển vào tham số truy vấn của API: (a) Tấn công vượt điều kiện logic: COFFEE' OR '1'='1; (b) Tấn công ghép câu lệnh phá hủy bảng (Stacked Query): RICE'; DROP TABLE price_history; --; và (c) Tấn công trích xuất bảng người dùng (UNION-based SQLi): 1 UNION SELECT null, email, password_hash FROM users--. Nhờ SQLAlchemy ORM biên dịch tham số thành biến ràng buộc (Bound Parameters), cơ sở dữ liệu xử lý toàn bộ chuỗi độc hại như một hằng chuỗi thông thường, trả về mã an toàn và bảo toàn nguyên vẹn 100% dữ liệu bảng.

4. Kịch bản tấn công chèn kịch bản độc hại Stored XSS & CSV Macro Injection (test_xss_sanitization_in_alert_creation & test_csv_formula_injection_defense): Kẻ tấn công gửi mã độc <script>fetch('http://hacker.site/steal?c='+document.cookie)</script> vào trường tên quy tắc cảnh báo tại API POST /api/v1/alerts. Trước khi lưu vào bảng alert_rules, hàm sanitize_text() đã tước bỏ toàn bộ cặp thẻ <script>...</script>, chỉ giữ lại nội dung văn bản sạch. Tương tự, khi nhập file CSV chứa công thức thực thi lệnh hệ điều hành =cmd|' /C calc'!A0 hoặc @SUM(1+1)*cmd|' /C calc'!A0, hàm sanitize_csv_cell() tự động gắn dấu nháy đơn (') ở đầu chuỗi ('=cmd..., '@SUM...), vô hiệu hóa hoàn toàn khả năng tự động chạy macro khi người dùng mở báo cáo trên Microsoft Excel.


## 4.9. KẾT QUẢ KIỂM ĐỊNH CHẤT LƯỢNG & KIỂM TOÁN BẢO MẬT TOÀN DIỆN HỆ THỐNG AGROFORECAST


### 4.9.1. Tóm tắt kết quả kiểm định tổng thể (Backend, Frontend, Coverage, E2E & Bảo mật)

Quá trình kiểm thử và kiểm toán bảo mật hệ thống AgroForecast được thực hiện khép kín và độc lập trên cả hai phân hệ Backend (FastAPI, Python 3.11, PostgreSQL) và Frontend (Next.js 14, React 18, TypeScript, Syncfusion EJ2) nhằm bảo đảm độ tin cậy chức năng tuyệt đối, độ phủ mã nguồn ở mức rất cao và năng lực phòng thủ chủ động trước các rủi ro an toàn thông tin mạng phổ biến. Toàn bộ các chỉ số kiểm định đều được đo đạc, ghi nhận khách quan và xác minh lại sau khi áp dụng đầy đủ các bản vá bảo mật chuẩn công nghiệp.

Bảng 4.4 tổng hợp kết quả đối chiếu giữa trạng thái ban đầu (Trước khi xử lý) và trạng thái nghiệm thu kỹ thuật cuối cùng (Sau khi hoàn thiện & vá bảo mật). Kết quả khẳng định hệ thống AgroForecast đã đạt và vượt toàn bộ các tiêu chuẩn kiểm định khắt khe nhất của ngành kỹ thuật phần mềm.


**Bảng 4.4. Tóm tắt kết quả kiểm định chất lượng phần mềm và kiểm toán bảo mật hệ thống AgroForecast**

| Hạng mục kiểm định | Trước khi xử lý (Baseline) | Sau khi hoàn thiện & vá | Đánh giá nghiệm thu |
| --- | --- | --- | --- |
| Kiểm thử tự động Backend (pytest) | 105 kịch bản PASS | 125 / 125 PASS (bao gồm Data Truth & Exogenous Zero-Leakage) | ĐẠT (100%) |
| Độ phủ mã nguồn Backend (pytest-cov) | 83% (377 dòng chưa phủ) | 98% (2.194 / 2.247 statements) | ĐẠT (Xuất sắc) |
| Kiểm thử đơn vị & Build Frontend | Kiểm tra cơ bản | 3/3 Unit PASS • 0 lỗi TS/Lint • 17/17 routes build | ĐẠT |
| Kiểm thử E2E trình duyệt (Playwright) | Phát hiện 1 lỗi RBAC ở pha RED | 4 / 4 PASS (28,67s) • 0 lỗi Console/Runtime | ĐẠT |
| Quét mã nguồn tĩnh Backend (Bandit -ll) | 3 Medium (1 B104, 2 B614) | 0 lỗi (No issues identified) | SẠCH (100%) |
| Quét lỗ hổng thư viện Python (pip-audit) | 100 CVEs trên 12 gói | 0 CVEs (No known vulnerabilities) | SẠCH (Tuyệt đối) |
| Quét lỗ hổng thư viện Node.js (npm audit) | 14 lỗ hổng (1 Crit, 6 High, 7 Mod) | 6 cảnh báo tồn dư (vá 8/8 non-breaking; đã giảm thiểu) | GIẢM THIỂU |
| Kiểm toán Bí mật & TLS (git ls-files) | Khóa mặc định + 10 điểm verify=False | 0 điểm vi phạm (CSPRNG 256-bit, verify=True 100%) | SẠCH (100%) |



### 4.9.2. Phương pháp và quy trình kiểm định kết hợp các Agent Skills chuyên sâu

Để tránh tình trạng kiểm thử hình thức hoặc bỏ sót các lỗi logic nghiệp vụ biên (Edge Cases), quy trình kiểm định chất lượng và an ninh mạng của dự án kết hợp trực tiếp giữa bộ công cụ kiểm thử thực chiến và các quy trình Agent Skills chuyên sâu được cài đặt chuẩn mực:

1. Nhóm quy trình Kiểm thử phần mềm (Testing Skills): (a) Áp dụng skill coverage-analysis để quét và phân tích cây phân nhánh luồng lệnh, truy tìm chính xác từng dòng mã nghiệp vụ chưa được bao phủ; (b) Áp dụng mô hình Test-Driven Development (TDD) theo chu trình RED-GREEN-REFACTOR: viết kịch bản kiểm thử tái hiện chính xác lỗi trước khi sửa, sau đó viết mã khắc phục và xác nhận trạng thái chuyển xanh; (c) Áp dụng skill webapp-testing để tự động hóa toàn bộ luồng thao tác của người dùng cuối trên trình duyệt thực Headless Chrome qua Playwright; và (d) Thực thi quy trình verification-before-completion bắt buộc chạy lại toàn bộ lệnh kiểm thử thực tế trên hệ thống đang chạy trước khi nghiệm thu.

2. Nhóm quy trình Kiểm toán Bảo mật (Security Skills): (a) Áp dụng quy trình audit-context-building nhằm lập bản đồ toàn diện bề mặt tấn công của hệ thống (bao gồm cơ chế cấp phát và kiểm tra JWT, ma trận phân quyền RBAC, kiểm tra biên tham số REST API, quy trình nhập/xuất CSV và các đường ống Bot cào dữ liệu); (b) Ứng dụng skill cvss-scoring để định lượng mức độ nghiêm trọng của từng lỗ hổng theo chuẩn quốc tế CVSS v3.1 (kèm vector tham chiếu CVSS v4.0); (c) Áp dụng systematic-debugging và differential-review nhằm rà soát chéo các thay đổi mã nguồn, đảm bảo mọi bản vá bảo mật không gây ra hồi quy logic hoặc tạo ra các lỗ hổng phụ phát sinh.


### 4.9.3. Chi tiết kết quả kiểm thử hệ thống đa tầng (132 / 132 kịch bản PASS)

Tổng cộng 132 kịch bản kiểm thử tự động trên toàn hệ thống đã vượt qua 100% sau bản vá bảo mật và nâng cấp biến ngoại sinh cuối cùng (bao gồm 125 kịch bản Backend Pytest — mở rộng từ bộ 72 kịch bản lõi với nhóm kiểm thử độ phủ nhánh 98%, kiểm toán sự thật dữ liệu 2024–2026 và chống rò rỉ biến ngoại sinh USD/VND + WTI — kết hợp 3 kiểm thử đơn vị Frontend và 4 luồng kiểm thử E2E trình duyệt thật).

Bảng 4.5 tổng hợp phân bổ kết quả kiểm thử trên 4 tầng kiến trúc phần mềm của AgroForecast.


**Bảng 4.5. Phân bổ kết quả kiểm định chất lượng phần mềm đa tầng của hệ thống AgroForecast**

| Tầng kiểm thử | Công cụ & Tập kiểm thử | Kết quả xác minh | Ghi chú kỹ thuật |
| --- | --- | --- | --- |
| Backend Unit & API Integration | pytest -v (bao gồm test_coverage_gaps.py, test_regional_pricing.py, test_security_phase7.py, test_data_truth_audit.py) | 125 / 125 PASS | Bao gồm test hồi quy RBAC, Alerts, SSRF, Secret, Data Truth và Exogenous Zero-Leakage |
| Frontend Unit Tests | node --test (src/lib/__tests__/formatters.test.mjs) | 3 / 3 PASS | Kiểm chứng logic định dạng tiền tệ, ngày tháng và tiện ích xử lý dữ liệu giao diện |
| Frontend Type, Lint & Production Build | npx tsc --noEmit, next lint, next build | 0 lỗi • 0 cảnh báo | Đóng gói thành công toàn bộ 17 / 17 tuyến trang (routes) tĩnh và động |
| End-to-End (E2E) Trình duyệt thật | Playwright (e2e/test_agroforecast_e2e.py) trên Headless Chrome | 4 / 4 PASS (28,67s) | 0 lỗi Console, 0 lỗi Runtime, 0 xuất hiện banner bản quyền Syncfusion |



### 4.9.4. Phân tích nâng cao độ phủ mã nguồn Backend (tăng từ 83% lên 98%)

Từ mức nền độ phủ 83% (với 105 kịch bản ban đầu, còn 377 dòng lệnh chưa được thực thi), nhóm nghiên cứu đã xây dựng bổ sung 15 kịch bản kiểm thử chuyên sâu trong tệp backend/tests/test_coverage_gaps.py. Các kịch bản này tập trung vào các nhánh xử lý ngoại lệ phức tạp, các điều kiện biên của thuật toán và các tình huống lỗi mạng/cơ sở dữ liệu, nâng tổng độ phủ toàn bộ gói backend/app/ lên mức kỷ lục 98% (2.194 / 2.247 statements).

Chỉ còn 53 dòng lệnh (chiếm 2% tổng số dòng) chưa được kích hoạt, đây là các nhánh mã đặc thù chỉ chạy trong môi trường cơ sở dữ liệu PostgreSQL vật lý của máy chủ cụm (như khóa pg_advisory_xact_lock, khối mã migration nâng cấp schema tự động và điểm khởi chạy tiến trình ASGI uvicorn). Bảng 4.6 trình bày chi tiết độ phủ theo từng mô-đun chức năng.


**Bảng 4.6. Bảng phân tích chi tiết độ phủ mã nguồn Backend theo từng nhóm mô-đun (pytest-cov)**

| Nhóm / Mô-đun mã nguồn | Baseline (Trước) | Sau tối ưu | Các nhánh nghiệp vụ & biên lỗi đã bao phủ bổ sung |
| --- | --- | --- | --- |
| auth.py, deps.py, security.py | — | 100% | Rate limit 429 cho /login & /register, JWT thiếu sub (401), user đã xóa (404), hạ cấp an toàn get_optional_current_user, hash Bcrypt hỏng, chống CSV Formula Injection. |
| schemas.py, market.py, regions.py, commodities.py | — | 100% | CRUD nông sản (400/404), đủ 6 luật kiểm tra hợp lệ PriceCreateManual, chuẩn hóa tài khoản _disabled, fallback mã tỉnh lạ, định giá theo vùng. |
| admin.py | 72% | 96% | Xác minh giá & ghi nhận Audit Log (UPDATED / DELETED), Import CSV (mã hóa latin-1, báo lỗi từng dòng), Export CSV an toàn. |
| alert_service.py | 77% | 99% | Đánh giá quy tắc PCT_INC_7D / PCT_DEC_7D, bỏ qua mặt hàng chưa có giá, lọc quyền xem user vs admin, nhánh gửi SMTP thành công & bắt lỗi mạng. |
| training_service.py | 78% | 99% | Cô lập lỗi theo từng mô hình (PARTIAL / FAILED), chặn tràn số >= 10^12, tự động cập nhật active_model tối ưu. |
| history_service.py | 83% | 100% | Xử lý chuỗi thời gian periodic / irregular, chuỗi khảo sát trực tiếp >= 5 phiên trên /overview và /history. |
| predictions.py | 64% | 100% | Các endpoint /readiness, /training-runs/{id}, /sources, /spotlight và run_job('retrain'). |
| scheduler.py | 26% | 100% | Vòng đời khởi tạo/dừng APScheduler, cùng kiểm thử upgrade_existing_schema(), /health trạng thái degraded và global_exception_handler. |



### 4.9.5. Kết quả kiểm thử E2E trên trình duyệt thật (Playwright)

Bộ kiểm thử tự động e2e/test_agroforecast_e2e.py được thiết lập để chạy trực tiếp trên môi trường thực tế (Frontend Next.js tại http://localhost:3000 kết nối đồng bộ với Backend FastAPI tại http://127.0.0.1:8000 và PostgreSQL). Bộ kiểm thử mô phỏng toàn bộ hành vi thao tác của người dùng thực tế trên giao diện và theo dõi nhật ký Console để kiểm soát lỗi Runtime.

Bảng 4.7 trình bày chi tiết kết quả kiểm chứng trên 4 luồng nghiệp vụ người dùng cốt lõi.


**Bảng 4.7. Danh mục kịch bản kiểm thử End-to-End (E2E) trên trình duyệt thật qua Playwright**

| Mã kịch bản | Tuyến kiểm thử | Nội dung kiểm chứng & Phát hiện thực tế | Kết quả |
| --- | --- | --- | --- |
| E2E-01 | / (Tổng quan) | Chọn vị trí Khánh Hòa trên thanh điều hướng: xác nhận hiển thị đúng nhãn 'Khảo sát tại Khánh Hòa' đối với Mía đường, nhãn 'Tham chiếu' đối với các mặt hàng còn lại và mở bảng Chênh lệch giá theo tỉnh hôm nay. | PASS |
| E2E-02 | /forecast (Dự báo) | Xác nhận tự động kích hoạt mô hình tốt nhất (★) khi đổi nông sản, chuyển kỳ hạn 7N <-> 30N, chuyển tab Bảng chi tiết dự báo <-> So sánh 5 mô hình kèm rê chuột trực tiếp trên biểu đồ Syncfusion không phát sinh lỗi BaseTooltip.appendChild. | PASS |
| E2E-03 | /history, /compare, /alerts | Kiểm chứng Syncfusion GridComponent và ChartComponent hiển thị đầy đủ dữ liệu, tương tác ổn định và tuyệt đối không xuất hiện banner cảnh báo bản quyền Syncfusion. | PASS |
| E2E-04 | /dashboard/* (Phân quyền RBAC) | Phát hiện lỗi thực tế ở pha TDD RED: Tài khoản Analyst vẫn mở được /dashboard/overview khi truy cập trực tiếp qua URL do layout.tsx cho phép ['admin', 'analyst']. Đã siết chặt điều kiện bảo vệ về user.role !== 'admin', biên dịch lại bản production và xác nhận chặn triệt để ở pha GREEN. | PASS |



### 4.9.6. Danh sách 9 lỗ hổng bảo mật phát hiện, chấm điểm CVSS v3.1 và giải pháp khắc phục

Thông qua hoạt động rà soát toàn diện bề mặt tấn công kết hợp công cụ quét mã tĩnh SAST (Bandit) và quét phụ thuộc SCA (pip-audit, npm audit), nhóm phát triển đã phát hiện và phân loại chính xác 9 phát hiện bảo mật (mã định danh từ SEC-01 đến SEC-09). Toàn bộ các phát hiện đều được lượng hóa theo khung điểm tiêu chuẩn quốc tế CVSS v3.1 và được xử lý triệt để theo thứ tự ưu tiên từ Nghiêm trọng (Critical) đến Trung bình (Medium).

Bảng 4.8 mô tả chi tiết từng lỗ hổng, vị trí phát hiện, điểm số CVSS v3.1, mã lỗi CWE và biện pháp vá bảo mật đã triển khai thành công.


**Bảng 4.8. Danh mục 9 lỗ hổng bảo mật được phát hiện, định lượng CVSS v3.1 và biện pháp khắc phục triệt để**

| Mã phát hiện | Điểm CVSS v3.1 & CWE | Mô tả lỗ hổng phát hiện & Vị trí | Biện pháp vá bảo mật đã triển khai | Trạng thái |
| --- | --- | --- | --- | --- |
| SEC-01 | 9.8 Critical • CWE-798 | Khóa ký JWT mặc định ví dụ FastAPI vẫn được sử dụng trong config.py, .env.example và .env cục bộ. | Xoay vòng khóa CSPRNG 256-bit (64 ký tự hex) trong .env; xóa mật khẩu DB & khóa mẫu khỏi mã nguồn; thêm field_validator đối chiếu SHA-256 chặn mọi khóa yếu/mẫu. | ĐÃ VÁ |
| SEC-02 | 8.6 High • CWE-862, CWE-639 | Các endpoint /api/v1/alerts* bỏ qua kiểm tra chủ sở hữu khi thiếu header Authorization, cho phép khách đọc email cá nhân, sửa/xóa quy tắc người khác và spam gửi email test SMTP. | Bắt buộc Depends(get_current_user) trên toàn bộ thao tác ghi/xóa/test và áp rate limit 429 tại alerts.py; siết chế độ fail-closed trong alert_service.py; bổ sung headers: getAuthHeaders() trong api.ts. | ĐÃ VÁ |
| SEC-08 | 8.6 High • CWE-1395 | 100 CVEs tồn tại trên 12 thư viện Python (PyJWT, python-jose, ecdsa, urllib3, pillow, certifi, soupsieve...). | Xóa mã chết app/core/auth.py & app/schemas/user.py; gỡ bỏ python-jose, ecdsa, passlib; nâng cấp toàn bộ 10 gói còn lại trong requirements.txt -> pip-audit đạt 0 CVE. | ĐÃ VÁ |
| SEC-04 | 7.8 High • CWE-502 (Bandit B614) | Hai lệnh torch.load() trong predictor.py chưa bật weights_only=True, tiềm ẩn rủi ro giải tuần tự hóa không an toàn (Insecure Deserialization). | Bật tham số weights_only=True cho cả 2 lệnh torch.load() trong predictor.py; quét lại Bandit trên ml_pipeline đạt 0 lỗi. | ĐÃ VÁ |
| SEC-09 | 7.0 High • CWE-1395 | 14 lỗ hổng phụ thuộc Frontend phát hiện qua npm audit (7 Moderate, 6 High, 1 Critical). | Chạy npm audit fix xử lý 8/8 lỗi không phá vỡ tương thích (còn 6 cảnh báo gắn với next@14->16 & dev-only eslint-config-next); cấu hình images: { unoptimized: true }, tắt poweredByHeader và bật 6 OWASP Security Headers trong next.config.mjs. | GIẢM THIỂU |
| SEC-03 | 6.5 Medium • CWE-295 | 10 vị trí tắt xác thực chứng chỉ SSL/TLS (verify=False và urllib3.disable_warnings) khi thu thập dữ liệu. | Gỡ bỏ 100% lệnh verify=False và urllib3.disable_warnings; ép xác thực TLS chuẩn (verify=True) với bộ chứng chỉ certifi mới nhất. | ĐÃ VÁ |
| SEC-05 | 6.5 Medium • CWE-863 | Chính sách kiểm soát truy cập trên các tuyến quản trị chưa đồng nhất tuyệt đối giữa Backend và Frontend. | Khóa chặt toàn bộ 20/20 endpoints /api/v1/admin/* trong admin.py bằng require_role(['admin']), đồng bộ 1:1 với lớp bảo vệ Frontend. | ĐÃ VÁ |
| SEC-07 | 4.8 Medium • CWE-605 (Bandit B104) | Cấu hình mặc định lắng nghe trên toàn bộ giao diện mạng 0.0.0.0 trong main.py. | Chuyển địa chỉ lắng nghe mặc định sang 127.0.0.1 với reload=False trong main.py; quét lại Bandit trên backend/app đạt 0 lỗi. | ĐÃ VÁ |
| SEC-06 | 4.7 Medium • CWE-918, CWE-79 | Nguy cơ SSRF trên bộ thu thập Scraper và rủi ro XSS thông qua chuỗi source_url lưu trữ hiển thị ra giao diện. | Áp dụng whitelist tên miền & chặn dải IP nội bộ/metadata (127.0.0.1, 169.254.169.254) trong vietnam_real_scrapers.py và specialized_scrapers.py; làm sạch source_url ở observation_scraper.py và chặn giao thức javascript: tại ProvinceComparisonPanel.tsx. | ĐÃ VÁ |



### 4.9.7. Ma trận đối chiếu các lớp phòng thủ theo chuẩn bảo mật quốc tế OWASP Top 10 (2021)

Để mang lại cái nhìn toàn cảnh về khả năng an ninh của ứng dụng, hệ thống đối chiếu toàn bộ các biện pháp kiểm soát kỹ thuật đã xây dựng với 10 nhóm rủi ro an ninh mạng nghiêm trọng nhất theo phân loại OWASP Top 10:2021.

Toàn bộ các lớp phòng vệ này đã được xác nhận thực tế thông qua kịch bản kiểm thử hồi quy an toàn thông tin test_security_audit_remediations_rbac_alerts_ssrf_and_secret. Bảng 4.9 trình bày chi tiết ma trận đối chiếu.


**Bảng 4.9. Ma trận đối chiếu các lớp phòng thủ kỹ thuật của AgroForecast theo chuẩn OWASP Top 10 (2021)**

| Nhóm rủi ro OWASP Top 10 (2021) | Cơ chế kiểm soát đã triển khai & xác minh thực tế | Tình trạng |
| --- | --- | --- |
| A01: Broken Access Control | Khóa 20/20 endpoints /api/v1/admin/* bằng require_role(['admin']); chặn truy cập trực tiếp /dashboard/* cho Analyst; siết fail-closed chống IDOR trên /api/v1/alerts*; cấu hình CORS whitelist. | ĐẠT |
| A02: Cryptographic Failures | Băm mật khẩu bằng Bcrypt; khóa ký JWT CSPRNG 256-bit lưu ngoài mã nguồn kèm kiểm tra chặn khóa yếu; bắt buộc xác thực chứng chỉ TLS verify=True 100%. | ĐẠT |
| A03: Injection | Truy vấn tham số hóa qua SQLAlchemy ORM chống SQL Injection; lọc chống CSV Formula Injection khi xuất dữ liệu; làm sạch source_url và chặn javascript: URI chống XSS. | ĐẠT |
| A04: Insecure Design | Áp dụng giới hạn tần suất (Rate Limiting trả HTTP 429) cho /login, /register và kiểm thử gửi email cảnh báo SMTP; tách biệt rõ dữ liệu chuẩn và dữ liệu theo vùng. | ĐẠT |
| A05: Security Misconfiguration | Chuyển bind mặc định sang 127.0.0.1 (reload=False); tắt header X-Powered-By; cấu hình 6 OWASP Security Headers tại next.config.mjs; giữ bí mật trong .env / .env.local không đưa lên Git. | ĐẠT |
| A06: Vulnerable & Outdated Components | Backend pip-audit đạt 0 CVE sau khi gỡ gói cũ và nâng cấp toàn bộ thư viện; Frontend npm audit đã vá sạch các gói non-breaking và áp dụng lớp giảm thiểu bù trừ cho 6 cảnh báo tồn dư. | KIỂM SOÁT |
| A07: Identification & Authentication Failures | Xác thực JWT chặt chẽ (từ chối token thiếu sub trả 401, tài khoản bị xóa trả 404, xử lý an toàn hash hỏng, bảo vệ khóa tài khoản người dùng). | ĐẠT |
| A08: Software & Data Integrity Failures | Bật weights_only=True cho toàn bộ lời gọi torch.load(); kiểm tra dữ liệu đầu vào bằng Pydantic (6 luật validate giá); kiểm định chống rò rỉ dữ liệu ML (No Data Leakage). | ĐẠT |
| A09: Security Logging & Monitoring | Ghi nhận đầy đủ nhật ký chỉnh sửa dữ liệu giá (Audit Log: UPDATED / DELETED), nhật ký thu thập dữ liệu (Crawling Logs) và nhật ký cảnh báo phục vụ truy vết sự cố. | ĐẠT |
| A10: Server-Side Request Forgery (SSRF) | Áp dụng danh sách tên miền cho phép (whitelist) và chặn truy cập IP nội bộ/metadata (127.0.0.1, 169.254.169.254) trong các bộ thu thập dữ liệu web. | ĐẠT |



### 4.9.8. Quản trị rủi ro tồn dư và kết luận nghiệm thu an toàn thông tin

Giải trình quản trị rủi ro tồn dư đối với 6 cảnh báo npm audit (SEC-09): Sau khi vá triệt để 8/8 lỗ hổng không gây xung đột tương thích trên Frontend, 6 cảnh báo còn lại xuất phát từ hai nhóm nguyên nhân: (1) Gói eslint-config-next chỉ phục vụ kiểm tra cú pháp ở môi trường lập trình của lập trình viên (devDependencies), hoàn toàn không được đóng gói vào bản biên dịch chạy thực tế của máy chủ sản xuất; và (2) Bản vá yêu cầu nâng cấp nhảy phiên bản lớn từ next@14.2.35 lên Next.js 16 gây phá vỡ tương thích hoàn toàn với React 18 và bộ thư viện Syncfusion EJ2. Để loại trừ bề mặt tấn công mà vẫn giữ vững độ ổn định tuyệt đối của hệ thống, nhóm nghiên cứu đã triển khai các biện pháp kiểm soát bù trừ (compensating controls): bật cấu hình images: { unoptimized: true } nhằm vô hiệu hóa hoàn toàn endpoint xử lý ảnh /_next/image (triệt tiêu nguy cơ tấn công từ chối dịch vụ DoS và thực thi mã từ xa RCE liên quan), đồng thời tắt poweredByHeader và kích hoạt đầy đủ 6 tiêu đề bảo mật OWASP Security Headers trong tệp next.config.mjs.

Kết luận nghiệm thu: Sau khi hoàn tất toàn bộ các bản vá bảo mật, tích hợp biến ngoại sinh nhân quả và đóng gói Docker Compose, hệ thống AgroForecast đã vượt qua kỳ kiểm thử hồi quy toàn diện với 125/125 kiểm thử Backend PASS (độ phủ mã nguồn đạt 98%), 3/3 kiểm thử đơn vị Frontend PASS, 17/17 tuyến trang đóng gói sạch không lỗi và 4/4 luồng kiểm thử E2E Playwright PASS trực tiếp trên trình duyệt thật (tổng 132/132 kịch bản). Hai dịch vụ Backend (http://127.0.0.1:8000) và Frontend (http://localhost:3000) vận hành hoàn toàn ổn định, đáp ứng trọn vẹn các tiêu chuẩn khắt khe về độ tin cậy phần mềm và an toàn thông tin mạng để trình bày bảo vệ trước Hội đồng chấm khóa luận tốt nghiệp.


# Chương 5: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN


## 5.1. Các kết quả chính đã đạt được của đề tài


### 5.1.1. Kết quả về mặt phần mềm và kỹ thuật hệ thống

Đề tài đã hoàn thành xuất sắc toàn bộ các mục tiêu đặt ra ban đầu, xây dựng thành công ứng dụng Web Full-Stack AgroForecast hoàn chỉnh với độ ổn định cao, đáp ứng đầy đủ các yêu cầu chức năng và phi chức năng trong quản lý, phân tích và dự báo giá nông sản Việt Nam.

Hệ thống đã triển khai thành công kiến trúc phân tầng 3 tầng hiện đại đóng gói bằng Docker Compose: tầng giao diện Next.js 14 tích hợp Syncfusion EJ2 (AgroGrid, FinChart, định giá theo 33 tỉnh/thành phố), tầng dịch vụ FastAPI bất đồng bộ xử lý dữ liệu thông lượng cao và tầng lưu trữ PostgreSQL 17 với ràng buộc toàn vẹn nghiêm ngặt.

Quy trình kiểm thử tự động đa tầng và kiểm toán an ninh mạng theo chuẩn OWASP Top 10 được thực thi toàn diện với 132/132 kịch bản thành công tuyệt đối (125 Pytest Backend đạt độ phủ 98%, 3 Frontend Unit, 4 Playwright E2E trên trình duyệt Chrome thật) cùng kết quả quét Bandit SAST 0 lỗi Medium/High và pip-audit 0 CVE.


### 5.1.2. Kết quả về mặt khoa học dữ liệu và mô hình hóa học máy

Đề tài đã thu thập, chuẩn hóa và kiểm toán sự thật thành công kho dữ liệu giai đoạn 2024–2026 (chốt mốc 23/11/2026, tự động cập nhật hằng ngày) cho 8 mặt hàng nông sản phân tách minh bạch 3 nhóm nguồn với tổng cộng 4.899 bản ghi trong price_history và 9.079 quan sát khảo sát tách theo tỉnh trong regional_price_observations, gắn đường dẫn source_url bấm kiểm chứng trực tiếp.

Cài đặt và huấn luyện thực nghiệm song song 40 tổ hợp mô hình (5 thuật toán ARIMA, Random Forest, XGBoost, Facebook Prophet, PyTorch Stacked LSTM × 8 mặt hàng) có tích hợp 2 biến ngoại sinh vĩ mô nhân quả (USD/VND VND=X và Dầu thô WTI CL=F), đánh giá nghiêm ngặt bằng Walk-Forward cuộn 7 ngày Zero-Leakage kèm dải khoảng tin cậy Conformal Prediction 95% (PICP) và đối chiếu trực diện với Naive Last Value Baseline.

Kết quả thực nghiệm khẳng định toàn bộ 40/40 mô hình đều đạt R² dương và 8/8 mặt hàng đạt ngưỡng dự báo chính xác rất cao (MAPE tối ưu từ 0,74% đến 2,62%): nổi bật trên Cà phê Robusta (919 phiên), mạng học sâu PyTorch Stacked LSTM (7 kênh nhân quả) vươn lên Hạng 1 tuyệt đối với RMSE = 1.978,28 VNĐ/kg, MAPE = 1,79% và R² = 0,8972 (vượt sâu Baseline 1,88%); Hồ tiêu đen (793 phiên) đạt MAPE = 0,74% (ARIMA); Dâu tây Đà Lạt 1,08% (Prophet); Khoai tây Đà Lạt 1,30% (Prophet); Hạt điều 1,30% (ARIMA); Lúa IR50404 1,58% (ARIMA); Khoai lang tím 1,71% (XGBoost) và Mía đường 2,62% (Prophet).

Thiết lập thành công cơ chế quản trị nguồn gốc dữ liệu (Data Provenance) với mã băm mật mã SHA-256 (dataset_hash), chuẩn hóa 3 kỳ hạn Literal[7, 14, 30] ở cả API và UI, cùng bài kiểm thử hồi quy chống rò rỉ dữ liệu ngoại sinh tương lai.


## 5.2. Những hạn chế và thách thức thực tế còn tồn tại


### 5.2.1. Hạn chế về tính liên tục và độ phân giải công bố của nhóm nông sản đặc sản vùng miền

Thách thức thực tế của thị trường nông sản Việt Nam nằm ở sự chênh lệch về mức độ công khai dữ liệu hằng ngày giữa các nhóm mặt hàng. Trong khi 3 mặt hàng chủ lực (Cà phê Robusta 919 phiên, Hồ tiêu đen 793 phiên và Lúa IR50404 442 phiên) có 100% URL bài báo công bố riêng từng ngày trên báo chí chuyên ngành, các bản tin địa phương vẫn thường nghỉ cập nhật vào dịp lễ Tết dài ngày.

Đối với 4 mặt hàng đặc sản mở rộng (Dâu tây Đà Lạt, Khoai tây Đà Lạt, Khoai lang tím Vĩnh Long và Hạt điều thô), thị trường rau củ quả nội địa không niêm yết bảng giá hằng ngày liên tục nhiều năm như nhóm hàng xuất khẩu trên sàn. Do đó, hệ thống phải kết hợp minh bạch giữa giá khảo sát sống tại Việt Nam (kamereo.vn, namtinhvegetable.com, banggianongsan.com) với chuỗi tham chiếu Proxy Index ETF nông sản quốc tế từ Yahoo Finance (DBA, MOO, CORN, SOYB x USD/VND), gắn nhãn nguồn gốc công khai trên /history và duy trì cổng chặn Readiness Gate cho mọi mặt hàng mới chưa đủ 60 quan sát.

Với mặt hàng Mía đường, dữ liệu giá giao dịch nội địa theo từng nhà máy chỉ công bố theo kỳ vụ ép, nên chuỗi hằng ngày 729 phiên được quy đổi minh bạch từ sàn kỳ hạn quốc tế ICE Sugar #11 (SB=F × tỷ giá USD/VND) kết hợp gắn riêng 8 bài báo khảo sát trực tiếp vụ ép 2024–2026 (Khánh Hòa, Phú Yên, Gia Lai) trong bảng regional_price_observations.


### 5.2.2. Hạn chế về hạ tầng triển khai đa cụm và phạm vi biến ngoại sinh khí tượng

Mặc dù ứng dụng đã được đóng gói hoàn chỉnh với Docker Compose (3 dịch vụ PostgreSQL, Backend FastAPI và Frontend Next.js chạy cô lập với người dùng non-root), hệ thống hiện mới được kiểm chứng hiệu năng và tải ở quy mô máy chủ đơn (Single-Host Deployment), chưa được thử nghiệm mở rộng tự động (Auto-scaling) trên cụm Kubernetes đa vùng phục vụ hàng chục nghìn kết nối đồng thời.

Về không gian đặc trưng ngoại sinh, đường ống học máy đã tích hợp thành công 2 chuỗi vĩ mô tài chính nhân quả thời gian thực (Tỷ giá USD/VND và Giá dầu thô WTI) nhưng chưa kết nối trực tiếp dữ liệu viễn thám khí tượng thời gian thực (nhiệt độ, lượng mưa, chỉ số hạn hán NDVI tại Tây Nguyên và Lâm Đồng) hay thống kê xuất nhập khẩu hải quan hằng tuần do giới hạn nguồn cấp API mở miễn phí.


## 5.3. Hướng phát triển và mở rộng trong tương lai


### 5.3.1. Mở rộng nguồn dữ liệu đa phương thức và tích hợp dữ liệu viễn thám

1. Kết nối thêm các nguồn dữ liệu chính thống từ Cổng dữ liệu quốc gia (data.gov.vn), Tổng cục Hải quan và các sàn giao dịch nông sản quốc tế thông qua các API thương mại chuyên dụng để mở rộng độ dài lịch sử chuỗi ngày cho toàn bộ 8 mặt hàng.

2. Tích hợp dữ liệu thời tiết và khí hậu thời gian thực từ mạng lưới trạm quan trắc khí tượng địa phương và ảnh vệ tinh viễn thám (chỉ số thực vật NDVI, độ ẩm đất, lượng mưa tích lũy) để làm biến ngoại sinh đưa vào các mô hình XGBoost và LSTM, nâng cao độ chính xác dự báo khi thị trường gặp sốc thời tiết hoặc thiên tai cực đoan.


### 5.3.2. Nâng cấp kiến trúc mô hình học máy và triển khai ứng dụng di động

1. Nghiên cứu ứng dụng các kiến trúc học sâu tiên tiến chuyên biệt cho chuỗi thời gian như Temporal Fusion Transformer (TFT), N-BEATS và mô hình lai kết hợp Wavelet Transform với LSTM (Wavelet-LSTM) để nắm bắt đồng thời các chu kỳ ngắn hạn và xu hướng dài hạn của thị trường nông sản.

2. Phát triển ứng dụng di động đa nền tảng (Mobile App chạy trên iOS và Android bằng React Native hoặc Flutter) tích hợp tính năng gửi thông báo biến động giá tức thời (Push Notification) qua tin nhắn Zalo/SMS cho bà con nông dân ngay tại vườn rẫy.

3. Triển khai hệ thống lên hạ tầng điện toán đám mây (Cloud Infrastructure) với kiến trúc container hóa Kubernetes, tự động co giãn tải (Auto-scaling) và thiết lập đường ống MLOps tự động hóa hoàn toàn từ thu thập dữ liệu hằng ngày đến tái huấn luyện mô hình ban đêm (Continuous Training - CT).


## 5.4. Kết luận chung


### 5.4.1. Lời đúc kết của nhóm tác giả

Đề tài tốt nghiệp 'Xây dựng ứng dụng phân tích dữ liệu và dự báo biến động giá nông sản theo chuỗi thời gian sử dụng Học máy' đã hoàn thành trọn vẹn cả hai mục tiêu nghiên cứu học thuật và xây dựng sản phẩm phần mềm thực tế. Sự kết hợp giữa kỹ thuật phần mềm chuẩn mực, quy trình kiểm thử và an ninh mạng nghiêm ngặt cùng với các mô hình học máy có kiểm chứng đã tạo nên một nền tảng AgroForecast vững chắc, tin cậy.

Kết quả thực nghiệm toàn diện trên 8 mặt hàng nông sản giai đoạn 2024–2026 chốt mốc 23/11/2026 (tiêu biểu là PyTorch Stacked LSTM 7 kênh đạt Hạng 1 trên Cà phê Robusta với RMSE = 1.978,28 VNĐ/kg, MAPE = 1,79%, R² = 0,8972 và Hồ tiêu đen ARIMA MAPE = 0,74% / RMSE = 1.643,77 VNĐ/kg) cùng cơ chế kiểm soát toàn vẹn SHA-256, 3 nhóm nguồn minh bạch và dải khoảng tin cậy Conformal 95% là đóng góp thực nghiệm có giá trị khoa học cao. Nhóm tác giả tin tưởng rằng hệ thống AgroForecast sẽ là cơ sở nền tảng vững chắc để tiếp tục hoàn thiện, hướng tới giải pháp chuyển đổi số nông nghiệp toàn diện phục vụ thiết thực cho bà con nông dân và doanh nghiệp nông sản Việt Nam.


# DANH MỤC TÀI LIỆU THAM KHẢO

1. Box G. E. P., Jenkins G. M., Reinsel G. C., Ljung G. M., Time Series Analysis: Forecasting and Control, 5th Edition, John Wiley & Sons, Hoboken, New Jersey, 2015.

2. Breiman L., Random Forests, Machine Learning, Vol. 45, No. 1, 2001, pp. 5 - 32.

3. Bộ Nông nghiệp và Phát triển Nông thôn - Viện Chính sách và Chiến lược Phát triển Nông nghiệp Nông thôn (IPSARD / AGROINFO), Báo cáo thường niên thị trường nông sản Việt Nam và Hệ thống cơ sở dữ liệu giá nông sản nội địa, Hà Nội, 2025.

4. Chen T., Guestrin C., XGBoost: A Scalable Tree Boosting System, Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, San Francisco, California, USA, Aug. 13-17, 2016, pp. 785 - 794.

5. Dickey D. A., Fuller W. A., Distribution of the Estimators for Autoregressive Time Series with a Unit Root, Journal of the American Statistical Association, Vol. 74, No. 366a, 1979, pp. 427 - 431.

6. Hiệp hội Cà phê - Ca cao Việt Nam (VICOFA) và Hiệp hội Hồ tiêu và Cây gia vị Việt Nam (VPSA), Bản tin tổng hợp thị trường xuất khẩu và giá nông sản thu mua nội địa Tây Nguyên - Đông Nam Bộ, TP. Hồ Chí Minh, 2025.

7. Hochreiter S., Schmidhuber J., Long Short-Term Memory, Neural Computation, Vol. 9, No. 8, 1997, pp. 1735 - 1780.

8. Hyndman R. J., Athanasopoulos G., Forecasting: Principles and Practice, 3rd Edition, OTexts, Melbourne, Australia, 2021.

9. Lewis C. D., Industrial and Business Forecasting Methods: A Practical Guide to Exponential Smoothing and Curve Fitting, Butterworth Scientific, London, 1982.

10. Lundberg S. M., Lee S. I., A Unified Approach to Interpreting Model Predictions, Proceedings of the 31st International Conference on Neural Information Processing Systems (NeurIPS), Long Beach, California, USA, Dec. 4-9, 2017, pp. 4765 - 4774.

11. Open Worldwide Application Security Project (OWASP), OWASP Top 10: The Ten Most Critical Web Application Security Risks & OWASP Web Security Testing Guide (WSTG v4.2), OWASP Foundation, Wakefield, USA, 2021.

12. Paszke A., Gross S., Massa F., Lerer A., Bradbury J., et al., PyTorch: An Imperative Style, High-Performance Deep Learning Library, Advances in Neural Information Processing Systems (NeurIPS 32), Vancouver, Canada, Dec. 8-14, 2019, pp. 8024 - 8035.

13. Pedregosa F., Varoquaux G., Gramfort A., Michel V., Thirion B., et al., Scikit-learn: Machine Learning in Python, Journal of Machine Learning Research (JMLR), Vol. 12, 2011, pp. 2825 - 2830.

14. Taylor S. J., Letham B., Forecasting at Scale, The American Statistician, Vol. 72, No. 1, 2018, pp. 37 - 45.


# PHỤ LỤC


## PHỤ LỤC A: DANH MỤC VÀ ĐẶC TẢ CHI TIẾT 28 REST API ENDPOINTS


## PHỤ LỤC B: BẢNG KẾT QUẢ 72 KỊCH BẢN KIỂM THỬ TỰ ĐỘNG VÀ BẢO MẬT OWASP TOP 10


## PHỤ LỤC C: BẢNG TỔNG HỢP SỐ LIỆU THỰC NGHIỆM 5 MÔ HÌNH HỌC MÁY TRÊN 8 MẶT HÀNG


## PHỤ LỤC D: SƠ ĐỒ THIẾT KẾ KIẾN TRÚC, BIỂU ĐỒ TUẦN TỰ VÀ THIẾT KẾ CSDL ERD


### D.1. Sơ đồ Kiến trúc Phân tầng Tổng thể của Hệ thống AgroForecast (3-Tier Architecture)

Hệ thống AgroForecast được thiết kế theo mô hình kiến trúc phân tầng 3 tầng hiện đại, phân tách hoàn toàn giữa giao diện người dùng, máy chủ dịch vụ nghiệp vụ và lớp lưu trữ dữ liệu an toàn:


+---------------------------------------------------------------------------------------------------+
|                        TẦNG TRÌNH DIỄN (PRESENTATION TIER - CLIENT)                               |
|                                                                                                   |
|  [Trình duyệt Web Khách / Nông hộ]           [Chuyên viên phân tích dữ liệu]    [Quản trị viên]  |
|         |                                                   |                            |        |
|         +-----------------------+---------------------------+----------------------------+        |
|                                 | (HTTPS / WSS / REST API)                                        |
|                                 v                                                                 |
|  +---------------------------------------------------------------------------------------------+  |
|  |                     GIAO DIỆN FRONTEND (NEXT.JS 14 APP ROUTER / TYPESCRIPT)                 |  |
|  |                                                                                             |  |
|  |  +---------------------+  +----------------------+  +--------------------+  +------------+  |  |
|  |  | Trang Tra cứu       |  | Trang Phân tích      |  | Trang So sánh      |  | Dashboard  |  |  |
|  |  | Lịch sử Giá tại Vườn|  | Mô hình & Dự báo     |  | 5 Thuật toán AI    |  | Quản trị   |  |  |
|  |  +---------------------+  +----------------------+  +--------------------+  +------------+  |  |
|  |  * Bộ lọc khoảng ngày       * Đường dự báo 30 ngày    * Radar so sánh sai số  * Duyệt nguồn|  |
|  |  * Phân tách provenance    * Dải tin cậy 95%         * Biểu đồ thanh RMSE    * Kích hoạt  |  |
|  |  * Dynamic yDomain        * XAI Feature Drivers     * Bảng MAE/MAPE/R2      * RBAC & User|  |
|  +---------------------------------------------------------------------------------------------+  |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  | JSON RESTful API Requests (JWT Auth / HTTPS)
                                                  v
+---------------------------------------------------------------------------------------------------+
|                     TẦNG DỊCH VỤ VÀ NGHIỆP VỤ (BUSINESS LOGIC & APPLICATION TIER)                 |
|                                                                                                   |
|  +---------------------------------------------------------------------------------------------+  |
|  |                         MÁY CHỦ BACKEND FASTAPI (PYTHON 3.11 ASYNC)                         |  |
|  |                                                                                             |  |
|  |  [LỚP BẢO MẬT & GATEWAY]: CORS Policy | Rate Limiter (Sliding Window) | JWT Authenticator    |  |
|  |                                                                                             |  |
|  |  [LỚP BỘ ĐIỀU KHIỂN (API ROUTERS)]:                                                         |  |
|  |  * /auth (Đăng ký, Đăng nhập, Phân quyền RBAC)    * /commodities & /regions (Danh mục chuẩn)|  |
|  |  * /prices/historical (Lịch sử & Provenance)      * /forecast (Dự báo, Sai số, Snapshot)   |  |
|  |  * /scraper (Cào dữ liệu, Quản lý xung đột)       * /admin & /alerts (Giám sát hệ thống)    |  |
|  |                                                                                             |  |
|  |  [LỚP DỊCH VỤ NGHIỆP VỤ (SERVICE LAYER)]:                                                   |  |
|  |  * PriceService (Kiểm tra chất lượng, tính spread) * ForecastService (Điều phối 5 mô hình)  |  |
|  |  * ScraperService (Chống trùng, chuẩn hóa nhãn)   * SnapshotService (SHA-256 MLOps)         |  |
|  |  * AlertService (Giám sát ngưỡng biến động)       * SecurityService (Bcrypt, JWT Claims)    |  |
|  |                                                                                             |  |
|  |  [LỚP ĐIỀU PHỐI HỌC MÁY & MLOPS (ML PIPELINE)]:                                             |  |
|  |  * Tiền xử lý chuỗi: Lọc ngoại lai IQR | Điền khuyết có kiểm soát | Kiểm định dừng ADF     |  |
|  |  * Tạo đặc trưng: Trễ Lag 1..30 | Cửa sổ trượt Rolling 7, 14 | Lịch thời vụ mùa vụ          |  |
|  |  * 5 Động cơ AI: ARIMA(p,d,q) | Random Forest | XGBoost | Facebook Prophet | PyTorch LSTM |  |
|  |  * Tác vụ nền: APScheduler (Định kỳ cào dữ liệu lúc 06:00 & Huấn luyện ngầm ban đêm)       |  |
|  +---------------------------------------------------------------------------------------------+  |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  | SQLAlchemy 2.0 ORM / Connection Pool (Port 5432)
                                                  v
+---------------------------------------------------------------------------------------------------+
|                        TẦNG DỮ LIỆU VÀ LƯU TRỮ (DATA TIER - POSTGRESQL 15+)                       |
|                                                                                                   |
|  +---------------------------------------------------------------------------------------------+  |
|  |                 CƠ SỞ DỮ LIỆU QUAN HỆ AGROFORECAST_DB (11 BẢNG QUAN HỆ CHUẨN HOÁ)           |  |
|  |                                                                                             |  |
|  |  [Bảng Danh mục]:       commodities (8 mặt hàng) | regions (29 huyện) | market_sources (12) |  |
|  |  [Bảng Tài khoản]:      users (Tài khoản người dùng) | roles (Viewer, Analyst, Admin)       |  |
|  |  [Bảng Dữ liệu Giá]:    price_history (4.899 phiên) | regional_price_observations (9.079)   |  |
|  |  [Bảng MLOps & Dự báo]: training_runs (Lần huấn luyện, SHA-256) | price_forecasts (Dự báo) |  |
|  |  [Bảng Vận hành]:       background_tasks (Tiến trình cào AI) | system_settings | alerts     |  |
|  +---------------------------------------------------------------------------------------------+  |
+---------------------------------------------------------------------------------------------------+
            


### D.2. Biểu đồ Luồng Tuần tự (Sequence Diagram) - Quy trình Huấn luyện và Cảnh báo Dự báo Lỗi thời

Biểu đồ thể hiện sự tương tác tuần tự giữa Quản trị viên, Máy chủ Backend, Cơ sở dữ liệu PostgreSQL và Động cơ Học máy để đảm bảo tính toàn vẹn thông qua mã băm SHA-256:


Quản trị viên (Admin)       Frontend Client         FastAPI Backend         Database PostgreSQL     ML Engine (Worker)
      |                           |                        |                         |                      |
      | 1. Kích hoạt cào dữ liệu  |                        |                         |                      |
      |-------------------------->| POST /scraper/trigger  |                         |                      |
      |                           |----------------------->| 2. Tạo Background Task  |                      |
      |                           |                        |------------------------>|                      |
      |                           |                        | 3. Cào & Chuẩn hóa giá  |                      |
      |                           |                        |--+                      |                      |
      |                           |                        |  | Lọc IQR, gán reviewed|                      |
      |                           |                        |<-+                      |                      |
      |                           |                        | 4. Ghi 4.899 bản ghi    |                      |
      |                           |                        |------------------------>|                      |
      |                           |                        | 5. Tính SHA-256 chuỗi   |                      |
      |                           |                        |    H = SHA256(data)     |                      |
      |                           |                        |                         |                      |
      | 6. Kích hoạt huấn luyện   |                        |                         |                      |
      |-------------------------->| POST /forecast/train   |                         |                      |
      |                           |----------------------->| 7. Kiểm tra ngưỡng đủ   |                      |
      |                           |                        |    (N >= 60 ngày)       |                      |
      |                           |                        |                         |                      |
      |                           |                        | 8. Tạo Snapshot & Runs  |                      |
      |                           |                        |    Lưu dataset_hash     |                      |
      |                           |                        |------------------------>|                      |
      |                           |                        | 9. Gửi dữ liệu chuẩn    |                      |
      |                           |                        |----------------------------------------------->|
      |                           |                        |                         |   10. Huấn luyện     |
      |                           |                        |                         |       5 mô hình      |
      |                           |                        |                         |   * ARIMA(2,1,1)     |
      |                           |                        |                         |   * XGBoost / RF     |
      |                           |                        |                         |   * Prophet / LSTM   |
      |                           |                        | 11. Trả về kết quả      |       Sai số & Điểm  |
      |                           |                        |<-----------------------------------------------|
      |                           |                        | 12. Lưu 30 điểm dự báo  |                      |
      |                           |                        |     kèm dải tin cậy 95% |                      |
      |                           |                        |------------------------>|                      |
      |                           | HTTP 200 OK (Xong)     |                         |                      |
      |                           |<-----------------------|                         |                      |
      | 13. Hiển thị biểu đồ      |                        |                         |                      |
      |<--------------------------|                        |                         |                      |
      |                           |                        |                         |                      |
      | === TÌNH HUỐNG PHÁT HIỆN DỰ BÁO LỖI THỜI (STALE FORECAST DETECTION) ===                             |
      |                           |                        |                         |                      |
      | 14. Dữ liệu lịch sử bị sửa|                        |                         |                      |
      |-------------------------->| Sửa 1 điểm giá         |                         |                      |
      |                           |----------------------->| Cập nhật bản ghi        |                      |
      |                           |                        |------------------------>|                      |
      |                           | 15. Người dùng xem giá |                         |                      |
      |                           |     GET /forecast      |                         |                      |
      |                           |----------------------->| 16. Tính hash hiện tại  |                      |
      |                           |                        |     H_now = SHA256(DB)  |                      |
      |                           |                        | 17. Đọc hash lần train  |                      |
      |                           |                        |------------------------>|                      |
      |                           |                        | 18. So sánh:            |                      |
      |                           |                        |     H_now != H_train    |                      |
      |                           | 19. Bật cờ is_stale    |                         |                      |
      |                           |<-----------------------|                         |                      |
      | 20. Hiển thị cảnh báo     |                        |                         |                      |
      |     màu hổ phách          |                        |                         |                      |
      |<--------------------------|                        |                         |                      |
            


### D.3. Lược đồ Thực thể Liên kết Cơ sở Dữ liệu ERD 11 Bảng (Database ERD Specifications)

Bảng tổng hợp đặc tả cấu trúc 11 bảng dữ liệu trong CSDL quan hệ PostgreSQL của AgroForecast:


+-------------------+       1:N       +-------------------+       1:N       +----------------------+
|    commodities    |----------------<| historical_prices |>----------------|    market_sources    |
+-------------------+                 +-------------------+                 +----------------------+
| PK id (INT)       |                 | PK id (BIGINT)    |                 | PK id (INT)          |
|    code (VARCHAR) |                 | FK commodity_id   |                 |    code (VARCHAR)    |
|    name (VARCHAR) |                 | FK region_id      |                 |    name (VARCHAR)    |
|    unit (VARCHAR) |                 | FK source_id      |                 |    base_url (VARCHAR)|
|    category (STR) |                 |    price_date     |                 |    is_active (BOOL)  |
|    base_price     |                 |    price_value    |                 +----------------------+
+-------------------+                 |    provenance_stat|
          | 1                         |    audit_note     |
          |                           |    created_at     |
          | N                         +-------------------+
+-------------------+                           | 1
|  periodic_prices  |                           |
+-------------------+                           | N (Bản chụp tham chiếu)
| PK id (INT)       |                 +-------------------+       1:N       +----------------------+
| FK commodity_id   |                 |   training_runs   |----------------<|   price_forecasts    |
|    period_type    |                 +-------------------+                 +----------------------+
|    period_label   |                 | PK id (INT)       |                 | PK id (BIGINT)       |
|    avg_price      |                 | FK commodity_id   |                 | FK run_id            |
|    ccs_sugar      |                 | FK region_id      |                 |    model_name        |
+-------------------+                 |    model_names    |                 |    forecast_date     |
                                      |    dataset_hash   |                 |    forecast_value    |
+-------------------+                 |    sample_count   |                 |    confidence_lower  |
|      regions      |                 |    test_mae/rmse  |                 |    confidence_upper  |
+-------------------+                 |    created_at     |                 |    is_stale (BOOL)   |
| PK id (INT)       |                 +-------------------+                 +----------------------+
|    code (VARCHAR) |                           | 1
|    name (VARCHAR) |                           | N
|    province       |                 +-------------------+
|    spread_default |                 |   dataset_snaps   |
+-------------------+                 +-------------------+
                                      | PK id (INT)       |
+-------------------+       1:N       | FK run_id         |
|       roles       |----------------<|    snapshot_data  |
+-------------------+                 |    snapshot_hash  |
| PK id (INT)       |                 +-------------------+
|    name (VARCHAR) |
|    description    |                 +-------------------+                 +----------------------+
+-------------------+                 | background_tasks  |                 |        alerts        |
          | 1                         +-------------------+                 +----------------------+
          |                           | PK id (VARCHAR)   |                 | PK id (INT)          |
          | N                         |    task_type      |                 |    alert_level       |
+-------------------+                 |    status         |                 |    title (VARCHAR)   |
|       users       |                 |    progress_pct   |                 |    message (TEXT)    |
+-------------------+                 |    result_payload |                 |    is_acknowledged   |
| PK id (INT)       |                 |    created_at     |                 |    created_at        |
| FK role_id        |                 +-------------------+                 +----------------------+
|    email (VARCHAR)|
|    hashed_pass    |                 +-------------------+
|    full_name      |                 |  system_settings  |
|    is_active      |                 +-------------------+
|    created_at     |                 | PK key_name (STR) |
+-------------------+                 |    setting_val    |
                                      |    description    |
                                      +-------------------+
            


## PHỤ LỤC E: HƯỚNG DẪN KIỂM CHỨNG VÀ KỊCH BẢN TRÌNH BÀY HỆ THỐNG


### E.1. Hướng dẫn Kiểm chứng Dữ liệu Lịch sử và Nguồn gốc (Data Provenance Verification)

Bước 1: Trên trình duyệt Web, mở trang 'Lịch sử giá' (đường dẫn: http://localhost:3000/history). Chọn nông sản (ví dụ: 'Hồ tiêu đen') và chọn huyện trọng điểm (ví dụ: 'Cư M'gar, Đắk Lắk') với khoảng thời gian 365 ngày qua.

Bước 2: Hệ thống hiển thị biểu đồ diễn biến giá thực tế kèm bảng chi tiết bên dưới. Người kiểm chứng nhấp vào biểu tượng liên kết nguồn tại cột 'Nguồn công bố' của một ngày đại diện để đối chiếu trực tiếp với cổng thông tin thị trường (như Cổng thông tin AGROINFO thuộc Viện Chính sách và Chiến lược PTNT).

Bước 3: Kiểm tra định nghĩa quan sát, đơn vị niêm yết (VND/kg), loại giá (giá mua xô tại vườn) và danh sách các ngày thiếu được hệ thống liệt kê công khai. Trường hợp phát hiện điểm dữ liệu sai lệch do nguồn cập nhật lại, người kiểm chứng đăng nhập tài khoản quản trị để chuyển trạng thái bản ghi từ 'reviewed' sang 'needs_review' kèm bản ghi giải trình lịch sử, tuyệt đối không chỉnh sửa tùy tiện làm sai lệch dữ liệu gốc.


### E.2. Hướng dẫn Kiểm chứng Lần Huấn luyện Mô hình và Bản chụp Dữ liệu (MLOps Snapshot)

Bước 1: Từ thanh điều hướng chính, mở trang 'Mô hình & Dự báo' (http://localhost:3000/forecast). Ghi nhận các thông số trên thẻ thông tin MLOps: Mã lượt huấn luyện (Training Run ID), Ngày thực hiện, Điểm cắt thời gian (Train End Date: 23/11/2026), các biến ngoại sinh nhân quả (USD/VND + WTI) và Mã băm bảo mật SHA-256 của tập dữ liệu.

Bước 2: Mở công cụ kiểm thử API (Swagger UI tại http://localhost:8000/docs hoặc Postman), gọi endpoint: GET /api/v1/forecast/snapshot/{run_id}. Trình duyệt trả về bản chụp JSON chứa toàn văn các điểm quan sát được sử dụng trong lượt huấn luyện.

Bước 3: Đếm số lượng quan sát trong tập dữ liệu bản chụp và tính toán mã băm SHA-256 độc lập bằng câu lệnh hệ thống. So sánh mã băm tính toán độc lập với trường dataset_hash hiển thị trên giao diện; kết quả phải khớp nhau 100% từng ký tự để đảm bảo mô hình không bị huấn luyện sai lệch.


### E.3. Hướng dẫn Kiểm chứng Sai số Thực nghiệm và So sánh với Phương pháp Cơ sở

Bước 1: Trích xuất tập kiểm thử (Test Set) bao gồm các ngày quan sát thực tế nằm ngoài tập huấn luyện (Walk-Forward Validation Window) và chuỗi dự báo tương ứng của 5 mô hình.

Bước 2: Áp dụng độc lập các công thức toán học tính MAE, RMSE, MAPE và R² (đã trình bày chi tiết tại Chương 2). Lưu ý không tính điểm sai số trên những ngày dữ liệu bị khuyết chỉ được lấp đầy bằng phương pháp Forward-fill.

Bước 3: Tính toán sai số của Phương pháp cơ sở (Naive Last Value Baseline) bằng cách giữ nguyên giá trị ngày cuối cùng trước cửa sổ kiểm thử cho toàn bộ 7 bước tiếp theo trong quy trình Walk-Forward. Đối chiếu kết quả (mốc 23/11/2026): trên Cà phê Robusta (919 phiên), PyTorch Stacked LSTM (7 kênh) đạt Hạng 1 với RMSE = 1.978,28 VNĐ/kg, MAPE = 1,79% và R² = 0,8972 (vượt sâu Baseline 2.147,01 VNĐ/kg); trên Hồ tiêu đen (793 phiên), ARIMA đạt MAPE = 0,74% (RMSE 1.643,77 VNĐ/kg, vượt Baseline 1.646,34 VNĐ/kg).


### E.4. Hướng dẫn Kiểm chứng Cơ chế Tự động Phát hiện Dự báo Lỗi thời (Stale Forecast)

Bước 1: Ghi nhận mã băm dataset_hash hiện tại của lượt huấn luyện đang hiển thị trên giao diện dự báo.

Bước 2: Mở môi trường thử nghiệm kiểm thử an toàn, thực hiện chỉnh sửa 1 điểm giá lịch sử (ví dụ sửa giá ngày 15/09/2026 từ 150.000 lên 150.001 VND/kg) hoặc chuyển trạng thái kiểm duyệt provenance của 1 bản ghi.

Bước 3: Làm mới lại trang dự báo (F5) hoặc gọi lại API GET /api/v1/forecast/predict. Hệ thống Backend ngay lập tức phát hiện mã băm dữ liệu hiện thời khác với mã băm lưu trong lần huấn luyện (SHA-256 Avalanche Effect).

Bước 4: Quan sát trên giao diện: Toàn bộ đường dự báo lập tức xuất hiện biểu ngữ cảnh báo màu hổ phách 'Dự báo đã lỗi thời do dữ liệu lịch sử vừa có cập nhật mới', đồng thời nút 'Huấn luyện lại' nhấp nháy khuyến nghị người dùng cập nhật mô hình.


### E.5. Kịch bản Trình bày trước Hội đồng Chấm Khóa luận: Tình huống Dữ liệu Đủ điều kiện

Thao tác 1: Trình diễn trang 'Lịch sử giá', chọn mặt hàng 'Hồ tiêu đen' hoặc 'Cà phê Robusta' và chọn tỉnh/huyện trọng điểm (ví dụ Đắk Lắk). Giải thích cho Hội đồng chuỗi dữ liệu 2024–2026 (793 phiên Hồ tiêu đen, 919 phiên Cà phê Robusta), bấm trực tiếp liên kết bài báo tại cột 'Nguồn công bố' để đối chiếu ngày và mức giá gốc.

Thao tác 2: Chuyển sang trang 'Dự báo', quan sát hệ thống tự động chọn mô hình tối ưu ★ (PyTorch Stacked LSTM cho Cà phê Robusta với RMSE = 1.978,28 VNĐ/kg, MAPE = 1,79%, R² = 0,8972; ARIMA cho Hồ tiêu đen với MAPE = 0,74%) và dải tin cậy Conformal 95% mở rộng theo căn bậc hai chân trời dự báo trên 3 kỳ hạn chuẩn (7N, 14N, 30N).

Thao tác 3: Chuyển sang tab 'So sánh 5 mô hình', chỉ ra bảng xếp hạng trực diện 5 mô hình (ARIMA, Random Forest, XGBoost, Prophet, PyTorch Stacked LSTM) cùng 2 biến ngoại sinh vĩ mô nhân quả (USD/VND + WTI) và đối chiếu trực tiếp với Naive Last Value Baseline.


### E.6. Kịch bản Trình bày trước Hội đồng Chấm Khóa luận: Tình huống Cổng Kiểm soát Dữ liệu (Readiness Gate)

Thao tác 1: Giải thích cơ chế cổng kiểm soát dữ liệu Readiness Gate: cả 8/8 mặt hàng hiện tại đều đã vượt ngưỡng sẵn sàng (442–919 phiên), tuy nhiên khi quản trị viên tạo mới một mặt hàng chưa có đủ 60 quan sát xác thực (hoặc dữ liệu lịch sử bị chỉnh sửa làm lệch mã băm SHA-256), hệ thống tự động chặn sinh dự báo ảo và hiển thị cảnh báo minh bạch.

Thao tác 2: Chọn mặt hàng 'Mía đường' tại Khánh Hòa để minh chứng tính minh bạch nguồn gốc: bảng lịch sử ghi rõ nguồn quy đổi sàn quốc tế ICE Sugar #11 (Yahoo Finance SB=F) cho chuỗi 729 phiên hằng ngày và tách riêng các mốc khảo sát trực tiếp vụ ép 2024–2026 (Khánh Hòa, Phú Yên, Gia Lai) trong bảng regional_price_observations.

Thao tác 3: Chọn mặt hàng đặc sản 'Dâu tây Đà Lạt' (Phường 8, Đà Lạt) và 'Khoai tây Đà Lạt' (Phường 7, Đà Lạt) để trình diễn giải pháp neo giá khảo sát sống Việt Nam (Kamereo, Nam Tĩnh) kết hợp chuỗi tham chiếu Proxy Index ETF Yahoo Finance (DBA/MOO x USD/VND), với mô hình Prophet đạt MAPE 1,08% và 1,30%.


### E.7. Kịch bản Trình bày trước Hội đồng Chấm Khóa luận: Bảng Điều khiển Quản trị Hệ thống

Thao tác 1: Đăng xuất tài khoản khách vãng lai, đăng nhập tài khoản Quản trị viên (admin@agroforecast.vn).

Thao tác 2: Mở menu 'Quản trị hệ thống' (Admin Dashboard), trình bày giao diện Quản lý tác vụ nền (Background Tasks), kích hoạt tác vụ cào dữ liệu lịch sử tự động từ các nguồn trực tuyến và theo dõi thanh tiến trình thời gian thực (Progress Bar).

Thao tác 3: Mở bảng 'Quản lý người dùng' để minh họa cơ chế phân quyền RBAC 3 cấp (Viewer, Analyst, Administrator); trình bày nhật ký kiểm toán bảo mật (Security Audit Logs) ghi nhận toàn bộ các thao tác nhạy cảm.


## PHỤ LỤC F: HƯỚNG DẪN CÀI ĐẶT HỆ THỐNG VÀ CẤU TRÚC ĐĨA DVD (M08)


### F.1. Yêu cầu Môi trường Phần cứng và Phần mềm Tối thiểu

1. Yêu cầu Phần cứng:

- Bộ vi xử lý (CPU): Tối thiểu Intel Core i5 / AMD Ryzen 5 thế hệ 8 trở lên (khuyến nghị 6 nhân 12 luồng để huấn luyện song song 5 mô hình).

- Bộ nhớ RAM: Tối thiểu 8 GB RAM (khuyến nghị 16 GB RAM để chạy đồng thời PostgreSQL, máy chủ FastAPI và môi trường Node.js/Next.js).

- Ổ cứng lưu trữ: Còn trống tối thiểu 10 GB dung lượng (khuyến nghị ổ SSD NVMe để tăng tốc độ truy vấn cơ sở dữ liệu).

2. Yêu cầu Phần mềm và Môi trường thực thi:

- Hệ điều hành: Windows 10/11 (64-bit), Ubuntu Linux 20.04+ LTS, hoặc macOS 12+.

- Môi trường Python: Phiên bản Python 3.11.x (khuyến nghị 3.11.9 64-bit).

- Môi trường Node.js: Phiên bản Node.js 18.x hoặc 20.x LTS kèm npm 9.x+ hoặc yarn/pnpm.

- Hệ quản trị Cơ sở dữ liệu: PostgreSQL 14, 15 hoặc 16 (chạy tại cổng mặc định 5432).

- Bộ công cụ kiểm thử: Pytest 8.x, HTTPX, Playwright Chromium headless.


### F.2. Quy trình 4 Bước Cài đặt và Khởi chạy Hệ thống AgroForecast

Bước 1 (Khởi tạo Cơ sở Dữ liệu PostgreSQL):

Mở pgAdmin 4 hoặc công cụ dòng lệnh psql, tạo cơ sở dữ liệu mới mang tên 'agroforecast_db'. Thực thi tập tin kịch bản khởi tạo cấu trúc 11 bảng và dữ liệu mẫu có sẵn tại đường dẫn: AgroForecast/DATABASE/init.sql.

Bước 2 (Cài đặt và Khởi chạy Máy chủ Backend FastAPI):

Mở cửa sổ dòng lệnh Terminal tại thư mục AgroForecast/SOURCE/backend. Tạo môi trường ảo và cài đặt các gói phụ thuộc:

  python -m venv venv

  venv\Scripts\activate (trên Windows) hoặc source venv/bin/activate (trên Linux/macOS)

  pip install -r requirements.txt

Khởi chạy máy chủ API tại cổng 8000:

  uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

Kiểm tra máy chủ hoạt động tại tài liệu API tương tác Swagger UI: http://localhost:8000/docs.

Bước 3 (Cài đặt và Khởi chạy Giao diện Frontend Next.js 14):

Mở cửa sổ Terminal thứ hai tại thư mục AgroForecast/SOURCE/frontend. Cài đặt các gói giao diện và khởi chạy máy chủ phát triển:

  npm install

  npm run dev

Mở trình duyệt Web truy cập giao diện ứng dụng tại: http://localhost:3000.

Bước 4 (Kích hoạt Kiểm chứng Toàn bộ 125 Kịch bản Pytest Backend & 4 Playwright E2E):

Tại thư mục AgroForecast/SOURCE/backend, thực thi câu lệnh kiểm thử tự động toàn diện (bao gồm bộ 72 kịch bản nền tảng trong Phụ lục B và 53 kịch bản mở rộng về phủ nhánh 98%, kiểm toán sự thật dữ liệu, biến ngoại sinh Zero-Leakage và vá bảo mật OWASP):

  pytest tests/ -v --tb=short

  bandit -r app -ll && bandit -r ml_pipeline -ll

Hệ thống đạt 125/125 Pytest Backend PASSED, Bandit 0 lỗi Medium/High, kết hợp 3/3 Frontend Unit Tests và 4/4 Playwright E2E trên trình duyệt Chrome thật.


### F.3. Danh sách Tài khoản Thử nghiệm Dành cho Hội đồng Chấm Khóa luận

- Tài khoản Quản trị viên Toàn quyền (Administrator): Email: admin@agroforecast.vn | Mật khẩu: admin123 (Có toàn quyền quản lý CSDL, duyệt nguồn provenance, kích hoạt cào dữ liệu và quản lý người dùng).

- Tài khoản Chuyên viên Phân tích (Analyst): Email: anhnguyen@agroforecast.vn | Mật khẩu: analyst123 (Có quyền xem dữ liệu chuyên sâu, kích hoạt huấn luyện mô hình, kiểm tra sai số và xem mã băm MLOps).

- Tài khoản Khách xem tra cứu (Viewer / Guest): Không cần đăng nhập, truy cập tự do các trang Lịch sử giá, Biểu đồ dự báo, Bảng so sánh 5 mô hình.


### F.4. Cấu trúc Đóng gói Đĩa DVD Nộp Khóa luận theo Quy định Khoa CNTT - ĐH Đà Lạt

Tuân thủ nghiêm ngặt Mục 4.2 và Mẫu nhãn đĩa M08 của văn bản 'Một số qui định về hình thức trình bày Khóa luận Tốt nghiệp', đĩa DVD nộp về Khoa được tổ chức theo đúng cây thư mục tiêu chuẩn sau:


DVD_ROOT/
|-- HUONG_DAN_SU_DUNG_DIA_DVD.txt   (Tập tin văn bản thuần túy hướng dẫn sử dụng đĩa, email & SĐT liên hệ)
|-- THESIS/                         (Thư mục chứa toàn bộ văn bản và bài thuyết trình)
|   |-- KHOA_LUAN_TOT_NGHIEP_AGROFORECAST_DLU.docx  (Văn bản Khóa luận Word hoàn chỉnh chuẩn 75-100 trang)
|   |-- KHOA_LUAN_TOT_NGHIEP_AGROFORECAST_DLU.pdf   (Bản in điện tử PDF chuẩn nộp lưu trữ thư viện)
|   +-- BAI_TRINH_BAY_BAO_VE_AGROFORECAST.pptx      (Slide trình bày báo cáo trước Hội đồng chấm khóa luận)
+-- AgroForecast/                   (Thư mục chứa mã nguồn và sản phẩm phần mềm mang tên chương trình)
    |-- SETUP/                      (Thư mục chứa hướng dẫn cài đặt, sơ đồ triển khai và dữ liệu thử nghiệm)
    |   |-- HUONG_DAN_CAI_DAT.docx  (Tài liệu hướng dẫn triển khai từng bước chi tiết)
    |   |-- SO_DO_TRIEN_KHAI.png    (Sơ đồ kiến trúc triển khai hệ thống 3 tầng)
    |   +-- sample_test_data/       (Tập tin dữ liệu thử nghiệm chuẩn khớp số liệu trong báo cáo)
    |-- SOURCE/                     (Thư mục chứa toàn bộ mã nguồn sạch của chương trình)
    |   |-- backend/                (Mã nguồn máy chủ Python FastAPI, SQLAlchemy, APScheduler, Pytest)
    |   +-- frontend/               (Mã nguồn giao diện Next.js 14, React, TypeScript, TailwindCSS, Recharts)
    +-- DATABASE/                   (Thư mục chứa cơ sở dữ liệu)
        |-- init.sql                (Kịch bản SQL tạo cấu trúc 11 bảng và khóa chính, khóa ngoại)
        +-- agroforecast_real_2024_2026.sql (Bản sao lưu CSDL PostgreSQL đầy đủ 4.899 bản ghi lịch sử + 9.079 quan sát cấp tỉnh)
            
