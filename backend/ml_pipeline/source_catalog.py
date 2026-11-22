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
        source_url="https://finance.yahoo.com/quote/SB=F/history/",
        suggested_start="2024-01-01",
        limitation="Chuỗi ngày quy đổi minh bạch từ sàn đường thô thế giới ICE #11 (Yahoo Finance SB=F × USD/VND) theo chuẩn mía 10 CCS, kết hợp các mốc khảo sát thu mua thực tế 2024–2026 tại Khánh Hòa, Phú Yên, Gia Lai (Bộ Công Thương, Báo Khánh Hòa, Báo Nhân Dân, Báo Nông nghiệp & Môi trường)."
    ),
    "STRAWBERRY": dict(
        kind="daily",
        source_url="https://kamereo.vn/blog/vi/gia-dau-tay-hom-nay/",
        product="Dâu tây Mỹ Đá / Giống Pháp Đà Lạt (giá sỉ tại vườn)",
        market="Phường 8, Đà Lạt, Lâm Đồng",
        price_type="Bán sỉ tại vườn",
        suggested_start="2024-11-21",
        limitation="Kamereo (bảng giá sỉ Dâu tây Đà Lạt & Mộc Châu) kết hợp chuỗi chỉ số nông sản thực tế Yahoo Finance DBA × USD/VND."
    ),
    "SWEET_POTATO": dict(
        kind="daily",
        source_url="https://banggianongsan.com/gia-khoai-lang/",
        product="Khoai lang tím Nhật (Bình Tân, Vĩnh Long / Chợ Bình Điền)",
        market="Huyện Bình Tân, Vĩnh Long",
        price_type="Thu mua / bán buôn",
        suggested_start="2024-11-21",
        limitation="Bảng Giá Nông Sản (banggianongsan.com) & Chợ Giá (chogia.vn) kết hợp chuỗi chỉ số thực tế Yahoo Finance CORN × USD/VND."
    ),
    "POTATO": dict(
        kind="daily",
        source_url="https://namtinhvegetable.com/san-pham/khoai-tay-hong-da-lat-vip/",
        product="Khoai tây hồng Đà Lạt loại 1 (sỉ tại vựa Lâm Đồng)",
        market="Phường 7, Đà Lạt, Lâm Đồng",
        price_type="Bán sỉ tại vựa",
        suggested_start="2024-11-21",
        limitation="Vựa nông sản Nam Tĩnh Lâm Đồng (namtinhvegetable.com) kết hợp chuỗi chỉ số thực tế Yahoo Finance MOO × USD/VND."
    ),
    "CASHEW_NUT": dict(
        kind="daily",
        source_url="https://banggianongsan.com/bang-gia-hat-dieu/",
        product="Hạt điều tươi thu mua tại vườn (7 tỉnh trọng điểm)",
        market="Huyện Bù Đăng, Bình Phước",
        price_type="Thu mua tại vườn",
        suggested_start="2024-11-21",
        limitation="Bảng Giá Nông Sản (khảo sát 7 tỉnh Bình Phước, Đắk Lắk, Đắk Nông, Gia Lai, Kon Tum, Lâm Đồng, BR-VT) kết hợp Yahoo Finance SOYB × USD/VND."
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
