"""Explicit product, market and cadence contracts; never substitute sugar for cane."""
AGRO_URL = "https://agro.gov.vn/vn/nguonwmy.aspx"
SOURCES = {
    "COFFEE_ROBUSTA": dict(kind="daily", source_url="https://giacaphe.com/gia-ca-phe-noi-dia/",
        limitation="Giacaphe: giá trung bình nội địa. Lịch sử xa có thể yêu cầu tài khoản nguồn."),
    "RICE_IR504": dict(kind="daily", source_url=AGRO_URL, product="Lúa IR 50404 - lúa tươi",
        market="An Giang", price_type="Bán tại hộ", suggested_start="2024-01-01",
        limitation="AGROINFO: lúa IR50404 tươi, bán tại hộ ở An Giang (VNĐ/kg). Có lịch sử cũ, ngày công bố không liên tục; không thay bằng gạo thành phẩm hay lúa khô."),
    "PEPPER_BLACK": dict(kind="daily", source_url=AGRO_URL,
        product="Hạt tiêu đen trong nước|Black pepper (Domestic)", market="Đắk Lắk", price_type="Bán buôn",
        limitation="AGROINFO: tiêu đen, giá bán buôn tại Đắk Lắk (VNĐ/kg). Giữ một thị trường cố định, không trộn tiêu trắng hoặc giá xuất khẩu."),
    "SUGARCANE": dict(kind="periodic", source_url="https://thuongmaibiengioimiennui.gov.vn",
        suggested_start="2024-01-01",
        limitation="Mía 7–10 chữ đường tại Tây Hòa, Phú Yên: báo cáo giá mua/bán theo kỳ của Bộ Công Thương. Đã tích hợp hai báo cáo năm 2024; không coi là chuỗi giá hằng ngày để huấn luyện."),
}

SUGARCANE_REPORTS = [
    "https://thuongmaibiengioimiennui.gov.vn/gia-hang-hoa/2024/2/tham-khao-gia-ca-thi-truong-nong-san-tai-phu-yen",
    "https://thuongmaibiengioimiennui.gov.vn/gia-hang-hoa/2024/5/tham-khao-gia-ca-thi-truong-nong-san-tai-phu-yen",
]
