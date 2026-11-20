# -*- coding: utf-8 -*-
"""
Specialized daily observation collectors from official Vietnamese agricultural portals.
STRICT NO-SYNTHETIC POLICY:
- Only stores real prices successfully parsed from live portals with explicit source URL provenance.
- Never generates random/synthetic fallback prices when a portal is unavailable or blocks requests.
- Reports FAILED / PARTIAL status with transparent error details if live collection fails.
"""
import ipaddress
import re
import json
from datetime import date, datetime
from urllib.parse import urlparse
from bs4 import BeautifulSoup

from app.models.models import PriceHistory
from app.services.history_service import archive_price

ALLOWED_PORTAL_DOMAINS = (
    "giacaphe.com",
    "chogia.vn",
    "vietnambiz.vn",
    "vietfood.org.vn",
    "giatieu.com",
    "agri.lamdong.gov.vn",
    "sonla.gov.vn",
    "chodaumoithuduc.com.vn",
    "giaca.nsvl.com.vn",
    "vinacas.com.vn",
    "binhphuoc.gov.vn",
    "vinanet.vn",
)


def _is_safe_portal_url(url: str) -> bool:
    if not url or not isinstance(url, str):
        return False
    try:
        parsed = urlparse(url.strip())
    except Exception:
        return False
    if parsed.scheme.lower() not in ("https", "http") or not parsed.hostname:
        return False
    host = parsed.hostname.lower().rstrip(".")
    try:
        ipaddress.ip_address(host)
        return False
    except ValueError:
        pass
    if host in ("localhost", "localhost.localdomain"):
        return False
    return any(host == dom or host.endswith(f".{dom}") for dom in ALLOWED_PORTAL_DOMAINS)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 AgroForecast/2.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
}

PORTAL_CONFIGS = {
    "COFFEE_ROBUSTA": {
        "primary_url": "https://giacaphe.com/gia-ca-phe-noi-dia/",
        "fallback_urls": ["https://chogia.vn/gia-ca-phe/", "https://vietnambiz.vn/gia-ca-phe.html"],
        "keywords": ["cà phê", "robusta", "đắk lắk", "dak lak", "nhân xô"],
        "unit": "VNĐ/kg",
        "price_range": (40000.0, 200000.0),
        "market": "Tây Nguyên (Đắk Lắk, Lâm Đồng)",
    },
    "RICE_IR504": {
        "primary_url": "https://vietfood.org.vn/thi-truong/gia-noi-dia/",
        "fallback_urls": ["https://vietnambiz.vn/gia-lua-gao.html"],
        "keywords": ["lúa ir 504", "lúa tươi", "lúa thường", "ir50404", "an giang"],
        "unit": "VNĐ/kg",
        "price_range": (4000.0, 12000.0),
        "market": "An Giang & ĐBSCL",
    },
    "PEPPER_BLACK": {
        "primary_url": "https://giatieu.com/gia-tieu-hom-nay/",
        "fallback_urls": ["https://giacaphe.com/gia-tieu-noi-dia/", "https://vietnambiz.vn/gia-tieu.html"],
        "keywords": ["hồ tiêu", "tiêu đen", "tiêu xô", "chư sê", "đắk lắk"],
        "unit": "VNĐ/kg",
        "price_range": (60000.0, 250000.0),
        "market": "Đắk Lắk & Tây Nguyên",
    },
    "STRAWBERRY": {
        "primary_url": "https://agri.lamdong.gov.vn",
        "fallback_urls": ["https://sonla.gov.vn", "http://www.chodaumoithuduc.com.vn"],
        "keywords": ["dâu tây", "dau tay", "new zealand", "mỹ đá"],
        "unit": "VNĐ/kg",
        "price_range": (70000.0, 200000.0),
        "market": "Lâm Đồng & Sơn La",
    },
    "SWEET_POTATO": {
        "primary_url": "http://giaca.nsvl.com.vn",
        "fallback_urls": ["http://www.chodaumoithuduc.com.vn"],
        "keywords": ["khoai lang", "khoai lang tím", "bình tân"],
        "unit": "VNĐ/kg",
        "price_range": (5000.0, 15000.0),
        "market": "Bình Tân, Vĩnh Long",
    },
    "POTATO": {
        "primary_url": "https://agri.lamdong.gov.vn",
        "fallback_urls": ["http://www.chodaumoithuduc.com.vn"],
        "keywords": ["khoai tây", "khoai tay", "đà lạt"],
        "unit": "VNĐ/kg",
        "price_range": (10000.0, 30000.0),
        "market": "Đà Lạt, Lâm Đồng",
    },
    "CASHEW_NUT": {
        "primary_url": "https://vinacas.com.vn",
        "fallback_urls": ["https://binhphuoc.gov.vn"],
        "keywords": ["hạt điều", "điều thô", "cashew", "hạt điều nhân"],
        "unit": "VNĐ/kg",
        "price_range": (25000.0, 55000.0),
        "market": "Bình Phước & Đông Nam Bộ",
    },
}


def parse_portal_html(html: str, keywords: list, price_range: tuple = (1000.0, 500000.0)) -> float:
    """Parse HTML from agricultural portals to extract matching real commodity prices within expected bounds."""
    min_val, max_val = price_range
    soup = BeautifulSoup(html, "html.parser")
    for el in soup.find_all(["tr", "li", "div", "p"]):
        text = el.get_text(" ", strip=True).lower()
        if any(kw in text for kw in keywords):
            matches = re.findall(r"(\d{1,3}(?:[.,]\d{3})+)\s*(?:đ|vnd|vnđ|/kg)?", text)
            for m in matches:
                price_str = m.replace(".", "").replace(",", "")
                try:
                    price = float(price_str)
                    if min_val <= price <= max_val:
                        return price
                except ValueError:
                    continue
    return 0.0


def collect_specialized_portal_history(db, http, commodity, config, start, end, progress=None):
    """
    Collect real live observation from official Vietnamese portals.
    NEVER fabricates or randomizes missing historical days.
    """
    code = commodity.code
    portal_info = PORTAL_CONFIGS.get(code, {})
    primary_url = portal_info.get("primary_url", config.get("source_url", "https://vinanet.vn"))
    fallback_urls = portal_info.get("fallback_urls", [])
    all_urls = [primary_url] + fallback_urls
    keywords = portal_info.get("keywords", [commodity.name.lower()])
    price_bounds = portal_info.get("price_range", (1000.0, 500000.0))

    live_price = None
    successful_url = None
    errors = []

    for idx, url in enumerate(all_urls, start=1):
        if not _is_safe_portal_url(url):
            errors.append(f"{url}: URL bị từ chối bởi danh sách tên miền cho phép")
            continue
        try:
            resp = http.get(url, headers=HEADERS, timeout=(5, 12))
            if resp.status_code == 200:
                resp.encoding = "utf-8"
                parsed = parse_portal_html(resp.text, keywords, price_bounds)
                if parsed > 0:
                    live_price = parsed
                    successful_url = url
                    break
                errors.append(f"{url}: không tìm thấy bảng giá hợp lệ")
            else:
                errors.append(f"{url}: HTTP {resp.status_code}")
        except Exception as exc:
            errors.append(f"{url}: {type(exc).__name__}")
        if progress:
            progress(idx, len(all_urls))

    if not live_price or not successful_url:
        return {
            "count": 0,
            "status": "FAILED",
            "message": (
                f"Không thu thập được dữ liệu thật cho [{commodity.name}] từ các cổng nguồn "
                f"(không sinh dữ liệu giả). Chi tiết: {'; '.join(errors[:3])}"
            ),
        }

    obs_date = min(end, date.today())
    existing = (
        db.query(PriceHistory)
        .filter(PriceHistory.commodity_id == commodity.id, PriceHistory.record_date == obs_date)
        .first()
    )

    if existing and existing.provenance in ("collected", "reviewed"):
        return {
            "count": 0,
            "status": "SUCCESS",
            "message": f"[{commodity.name}] Đã có bản ghi xác minh ngày {obs_date} từ {successful_url} (giữ nguyên).",
        }

    details = json.dumps(
        {
            "provider": successful_url,
            "source_url": successful_url,
            "market": portal_info.get("market", commodity.region),
            "unit": commodity.unit,
            "cadence": "daily",
            "queried_at": datetime.now().isoformat(),
        },
        ensure_ascii=False,
    )

    if existing:
        archive_price(db, existing, actor="Scraper tự động", new_price=live_price, reason=f"Cập nhật từ {successful_url}")
        existing.price = live_price
        existing.source = successful_url[:100]
        existing.provenance = "collected"
        existing.source_details = details
    else:
        db.add(
            PriceHistory(
                commodity_id=commodity.id,
                record_date=obs_date,
                price=live_price,
                price_min=None,
                price_max=None,
                volume=None,
                source=successful_url[:100],
                provenance="collected",
                source_details=details,
            )
        )
    db.commit()

    return {
        "count": 1,
        "status": "SUCCESS",
        "message": f"[{commodity.name}] Ghi nhận 1 bản ghi thật ngày {obs_date}: {live_price:,.0f} {commodity.unit} từ {successful_url}.",
    }
