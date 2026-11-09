"""Explicit product, market and cadence contracts from authoritative Vietnamese web sources."""

AGRO_URL = "https://agro.gov.vn/vn/nguonwmy.aspx"

SOURCES = {
    "COFFEE_ROBUSTA": dict(
        kind="daily",
        source_url="https://vinanet.vn",
        product="Cà phê nhân Robusta",
        market="Tây Nguyên (Đắk Lắk, Lâm Đồng)",
        price_type="Bán buôn",
        suggested_start="2024-01-01",
        limitation="Bộ Công Thương - Trung tâm Thông tin Công nghiệp và Thương mại (vinanet.vn) & Giacaphe: Bảng giá cà phê Robusta nội địa theo ngày tại Đắk Lắk, Lâm Đồng, Gia Lai (VNĐ/kg). Chuỗi lịch sử được lưu trữ minh bạch theo từng mốc công bố."
    ),
    "RICE_IR504": dict(
        kind="daily",
        source_url="https://vietfood.org.vn",
        product="Lúa IR 50404 - lúa tươi",
        market="An Giang",
        price_type="Bán tại hộ",
        suggested_start="2024-01-01",
        limitation="Hiệp hội Lương thực Việt Nam (VFA - vietfood.org.vn) & AGROINFO: Lúa IR 50404 tươi tại hộ/tại ruộng khu vực An Giang & ĐBSCL (VNĐ/kg). Dữ liệu được lưu trữ minh bạch theo từng mốc công bố."
    ),
    "PEPPER_BLACK": dict(
        kind="daily",
        source_url="https://vpsa.org.vn",
        product="Hạt tiêu đen trong nước|Black pepper (Domestic)",
        market="Đắk Lắk",
        price_type="Bán buôn",
        suggested_start="2024-01-01",
        limitation="Hiệp hội Hồ tiêu và Cây gia vị Việt Nam (VPSA - vpsa.org.vn) & AGROINFO: Bảng giá hồ tiêu đen xô khô đạt tiêu chuẩn độ ẩm 13% tại Đắk Lắk, Chư Sê, Bà Rịa - Vũng Tàu (VNĐ/kg)."
    ),
    "SUGARCANE": dict(
        kind="periodic",
        source_url="https://thuongmaibiengioimiennui.gov.vn",
        suggested_start="2024-01-01",
        limitation="Bộ Công Thương (thuongmaibiengioimiennui.gov.vn): Mía 7–10 chữ đường tại Tây Hòa, Phú Yên. Báo cáo giá mua/bán theo kỳ của Khuyến nông và Nhà máy đường; dự báo theo nhịp công bố định kỳ."
    ),
    "STRAWBERRY": dict(
        kind="daily",
        source_url="https://agri.lamdong.gov.vn",
        product="Dâu tây giống New Zealand / Mỹ đá",
        market="Đà Lạt (Lâm Đồng) & Sơn La",
        price_type="Bán buôn",
        suggested_start="2024-01-01",
        limitation="Sở NN&PTNT tỉnh Lâm Đồng (agri.lamdong.gov.vn), Cổng TTĐT Sơn La (sonla.gov.vn) & Chợ đầu mối Thủ Đức: Dâu tây tươi loại 1 chất lượng cao tại Đà Lạt và Mộc Châu (VNĐ/kg)."
    ),
    "SWEET_POTATO": dict(
        kind="daily",
        source_url="http://giaca.nsvl.com.vn",
        product="Khoai lang tím Vĩnh Long",
        market="Bình Tân, Vĩnh Long",
        price_type="Bán buôn / tại ruộng",
        suggested_start="2024-01-01",
        limitation="Cổng TT Giá cả Nông sản Vĩnh Long (giaca.nsvl.com.vn) & Chợ đầu mối Thủ Đức: Khoai lang tím thương phẩm loại 1 tại thủ phủ chuyên canh Bình Tân, Vĩnh Long (VNĐ/kg)."
    ),
    "POTATO": dict(
        kind="daily",
        source_url="https://agri.lamdong.gov.vn",
        product="Khoai tây hồng / vàng Đà Lạt",
        market="Đà Lạt, Lâm Đồng",
        price_type="Bán buôn",
        suggested_start="2024-01-01",
        limitation="Sở NN&PTNT tỉnh Lâm Đồng (agri.lamdong.gov.vn) & Chợ đầu mối Thủ Đức: Khoai tây thương phẩm hồng / vàng Đà Lạt loại 1 thu mua tại nông hộ (VNĐ/kg)."
    ),
    "CASHEW_NUT": dict(
        kind="daily",
        source_url="https://vinacas.com.vn",
        product="Hạt điều thô & điều nhân",
        market="Bình Phước & Đông Nam Bộ",
        price_type="Bán buôn / thu mua tại vườn",
        suggested_start="2024-01-01",
        limitation="Hiệp hội Điều Việt Nam (vinacas.com.vn), Cổng TTĐT tỉnh Bình Phước (binhphuoc.gov.vn) & Tổng cục Hải quan (customs.gov.vn): Giá thu mua điều thô tại vườn và giá nhân điều xuất khẩu (VNĐ/kg)."
    ),
}

COFFEE_ARCHIVE = dict(
    kind="daily",
    source_url="https://vinanet.vn",
    product="Cà phê nhân",
    market="Đắk Lắk",
    price_type="Bán buôn"
)

SUGARCANE_REPORTS = [
    "https://thuongmaibiengioimiennui.gov.vn/gia-hang-hoa/2020/8/bang-gia-hang-hoa-nong-san-tai-phu-yen",
    "https://thuongmaibiengioimiennui.gov.vn/gia-hang-hoa/2020/10/bang-gia-nong-san-tai-phu-yen",
    "https://thuongmaibiengioimiennui.gov.vn/gia-hang-hoa/2021/1/bang-gia-hang-hoa-nong-san-tai-phu-yen_271409",
    "https://thuongmaibiengioimiennui.gov.vn/gia-hang-hoa/2021/7/gia-ca-thi-truong-nong-san-tai-phu-yen",
    "https://thuongmaibiengioimiennui.gov.vn/su-kien/2021/9/bang-gia-hang-hoa-nong-san-tai-phu-yen",
    "https://thuongmaibiengioimiennui.gov.vn/gia-hang-hoa/2022/1/bang-gia-hang-hoa-nong-san-tai-phu-yen",
    "https://thuongmaibiengioimiennui.gov.vn/gia-hang-hoa/2022/12/tham-khao-gia-ca-thi-truong-nong-san-tai-phu-yen",
    "https://thuongmaibiengioimiennui.gov.vn/gia-hang-hoa/2023/12/tinh-hinh-gia-ca-thi-truong-nong-san-tai-phu-yen",
    "https://thuongmaibiengioimiennui.gov.vn/gia-hang-hoa/2024/2/tham-khao-gia-ca-thi-truong-nong-san-tai-phu-yen",
    "https://thuongmaibiengioimiennui.gov.vn/gia-hang-hoa/2024/5/tham-khao-gia-ca-thi-truong-nong-san-tai-phu-yen",
    "https://thuongmaibiengioimiennui.gov.vn/gia-hang-hoa/2024/6/tinh-hinh-gia-ca-hang-hoa-nong-san-tai-phu-yen",
    "https://thuongmaibiengioimiennui.gov.vn/gia-hang-hoa/2024/8/tham-khao-gia-ca-thi-truong-nong-san-tai-phu-yen",
    "https://thuongmaibiengioimiennui.gov.vn/gia-hang-hoa/2024/10/tham-khao-gia-ca-thi-truong-nong-san-tai-phu-yen",
    "https://thuongmaibiengioimiennui.gov.vn/gia-hang-hoa/2024/12/tham-khao-gia-ca-thi-truong-nong-san-tai-phu-yen",
    "https://thuongmaibiengioimiennui.gov.vn/gia-hang-hoa/2025/3/tham-khao-gia-ca-thi-truong-nong-san-tai-phu-yen",
]
