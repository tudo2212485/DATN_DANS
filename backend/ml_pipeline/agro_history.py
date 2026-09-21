"""Read AGROINFO's public ASP.NET search form, including its published pager."""
import re
import time
from datetime import datetime
from bs4 import BeautifulSoup
from .source_catalog import AGRO_URL

HEADERS = {"User-Agent": "AgroForecast/1.0 academic price history collector"}


def search_fields(soup, config, start, end):
    fields = {i['name']: i.get('value', '') for i in soup.select('input[type=hidden][name]')}
    for select in soup.select('select[name]'):
        name = select['name']
        if 'mathangnongsan' in name:
            if config['product'] not in [o.get('value') for o in select.select('option')]:
                raise ValueError("Nguồn không còn mặt hàng đúng quy cách yêu cầu")
            fields[name] = config['product']
        elif 'Theo_' in name:
            fields[name] = 'ngay'
    for item in soup.select('input[name]'):
        name = item['name']
        if 'tu_ngay' in name:
            fields[name] = start.strftime('%d/%m/%Y')
        elif 'den_ngay' in name:
            fields[name] = end.strftime('%d/%m/%Y')
        elif name.endswith('$Xem'):
            fields[name] = item.get('value', 'Tra cứu')
        elif item.get('type') == 'checkbox':
            fields[name] = 'on'
    if not any('mathangnongsan' in name for name in fields):
        raise ValueError("Không tìm thấy biểu mẫu tra cứu lịch sử AGROINFO")
    return fields


def parse_page(html, config, start, end):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', id=re.compile(r'GridView1$'))
    if table is None:
        raise ValueError("Nguồn không trả bảng lịch sử; không thay bằng dữ liệu giả")
    if 'Không có dữ liệu' in table.get_text():
        return soup, [], []
    headers = [c.get_text(' ', strip=True) for c in table.find('tr').find_all(['th', 'td'], recursive=False)]
    expected = ['Tên_mặt_hàng', 'Thị_trường', 'Loại_giá', 'Đơn_vị_tính', 'Loại_tiền', 'Nguồn', 'Ngày', 'Giá']
    if headers != expected:
        raise ValueError("Cấu trúc cột AGROINFO thay đổi, cần kiểm tra lại bộ đọc")
    result, all_dates = [], []
    for tr in table.find_all('tr')[1:]:
        cells = [c.get_text(' ', strip=True) for c in tr.find_all('td', recursive=False)]
        if len(cells) != 8:
            continue
        product, market, price_type, unit, currency, upstream, day, price = cells
        day = datetime.strptime(day, '%d-%m-%Y').date()
        all_dates.append(day)
        if not start <= day <= end:
            raise ValueError("Nguồn trả ngày ngoài bộ lọc yêu cầu")
        if product != config['product'].split('|')[0] or market != config['market']:
            continue
        # The public table can contain several price types for the same product
        # and market. Only retain the explicitly contracted series.
        if price_type != config['price_type']:
            continue
        if unit != 'kg' or currency != 'VND':
            raise ValueError("Loại giá/đơn vị không khớp hợp đồng dữ liệu")
        if not re.fullmatch(r'\d+(?:[.,]\d{3})*', price):
            raise ValueError("Giá không phải số tiền VNĐ hợp lệ")
        price = float(price.replace('.', '').replace(',', ''))
        if not 0 < price < 1e9:
            raise ValueError("Giá nguồn ngoài giới hạn hợp lệ")
        result.append(dict(date=day, price=price, source=AGRO_URL,
                           details=dict(provider='AGROINFO', product=product, market=market,
                                        price_type=price_type, unit='VND/kg', upstream=upstream,
                                        query_start=str(start), query_end=str(end))))
    return soup, result, all_dates


def fetch_history(http, config, start, end, progress=None, max_pages=300):
    response = http.get(AGRO_URL, headers=HEADERS, timeout=(10, 40))
    response.raise_for_status(); response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    fields = search_fields(soup, config, start, end)
    seen, previous = {}, None
    for page in range(1, max_pages + 1):
        response = http.post(AGRO_URL, data=fields, headers=HEADERS, timeout=(10, 60))
        response.raise_for_status(); response.encoding = 'utf-8'
        soup, rows, dates = parse_page(response.text, config, start, end)
        signature = [(str(r['date']), r['price']) for r in rows], [str(d) for d in dates]
        if signature == previous and dates:
            raise ValueError("Nguồn lặp trang; dừng để tránh đếm trùng lịch sử")
        previous = signature
        for row in rows:
            old = seen.get(row['date'])
            if old and old['price'] != row['price']:
                raise ValueError("Nguồn có hai giá khác nhau cùng ngày/thị trường")
            seen[row['date']] = row
        if progress and dates:
            progress((end-min(dates)).days+1, (end-start).days+1)
        next_link = next((a for a in soup.select('a[href]') if re.search(rf"'Page\${page+1}'", a['href'])), None)
        if not next_link:
            return list(seen.values())
        if page == max_pages:
            raise ValueError("Khoảng quá lớn cho một tác vụ (300 trang); hãy chia nhỏ khoảng ngày")
        match = re.search(r"__doPostBack\('([^']+)','([^']+)'\)", next_link['href'])
        if not match:
            raise ValueError("Liên kết phân trang không hợp lệ")
        fields = search_fields(soup, config, start, end)
        fields = {key: value for key, value in fields.items() if not key.endswith('$Xem')}
        fields.update(__EVENTTARGET=match[1], __EVENTARGUMENT=match[2])
        time.sleep(.3)
