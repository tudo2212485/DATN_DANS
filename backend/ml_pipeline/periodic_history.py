"""Keep published buying/selling prices and reporting periods distinct."""
import re
from datetime import date, datetime
from bs4 import BeautifulSoup


def parse_sugarcane_report(html, source_url):
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text(' ', strip=True)
    published = re.search(r'Ngày đăng:\s*(\d{2}/\d{2}/\d{4})', text)
    period = re.search(r'Từ ngày\s+(\d{1,2})/(\d{1,2})(?:/(\d{4}))?\s+đến ngày\s+(\d{1,2})/(\d{1,2})/(\d{4})', text, re.I)
    if not published or not period:
        raise ValueError("Báo cáo không có ngày công bố và kỳ giá rõ ràng")
    d1, m1, explicit_start_year, d2, m2, end_year = period.groups()
    d1, m1, d2, m2, end_year = map(int, (d1, m1, d2, m2, end_year))
    start_year = int(explicit_start_year) if explicit_start_year else (end_year if m1 <= m2 else end_year - 1)
    start, end = date(start_year, m1, d1), date(end_year, m2, d2)
    published = datetime.strptime(published[1], '%d/%m/%Y').date()
    if not start <= end or published > date.today() or abs((published - end).days) > 31:
        raise ValueError("Kỳ báo cáo/ngày công bố không hợp lệ")
    for tr in soup.select('table tr'):
        cells = [c.get_text(' ', strip=True) for c in tr.find_all(['td','th'],recursive=False)]
        if len(cells) != 6 or not re.match(r'Mía\s*\(\s*từ', cells[1], re.I):
            continue
        _, product, unit, buying, selling, market = cells
        normalized_market = re.sub(r'[.\s]+', '', market).lower()
        if unit.strip().lower() != 'tấn' or normalized_market not in ('huyệntâyhòa', 'htâyhòa') or not re.search(r'7\s*[–-]\s*10 chữ đường', product):
            raise ValueError("Báo cáo mía không khớp quy cách/địa bàn/đơn vị đã xác minh")
        def money(value):
            value = value.strip()
            if not re.fullmatch(r'\d{1,3}(?:\.\d{3})+', value):
                raise ValueError("Giá mua/bán mía không hợp lệ")
            return float(value.replace('.',''))
        return dict(period_start=start, period_end=end, published_date=published,
                    buying_price=money(buying), selling_price=money(selling), unit='VND/tấn',
                    specification=product, market='Tây Hòa, Phú Yên', source_url=source_url,
                    attribution='Trang thông tin điện tử Thương mại biên giới, miền núi, hải đảo – Bộ Công Thương; nguồn báo cáo: Khuyến nông Phú Yên')
    raise ValueError("Không tìm thấy dòng giá mía đúng quy cách trong báo cáo")
