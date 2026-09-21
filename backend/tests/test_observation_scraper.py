from datetime import date
import pytest
from ml_pipeline.observation_scraper import PublicationUnavailable, parse_coffee_observation


def test_parse_published_coffee_average():
    html = """
    <html><h1>Giá cà phê ngày 11/09/2026</h1>
    <p>Giá cà phê ngày 11/09/2026 trung bình ở mức 95,700 đ/kg tăng nhẹ.</p></html>
    """
    assert parse_coffee_observation(html, date(2026, 9, 11)) == 95700


def test_rejects_wrong_published_date():
    html = "<h1>Giá cà phê ngày 10/09/2026</h1><p>trung bình ở mức 95,700 đ/kg</p>"
    with pytest.raises(PublicationUnavailable, match="Không có công bố"):
        parse_coffee_observation(html, date(2026, 9, 11))
