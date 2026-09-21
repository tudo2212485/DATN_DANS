from datetime import date
from unittest.mock import Mock
import pytest
from app.models.models import Commodity, PriceHistory, PeriodicPrice
from ml_pipeline.agro_history import parse_page, fetch_history
from ml_pipeline.periodic_history import parse_sugarcane_report
from ml_pipeline.source_catalog import SOURCES

FORM = '<form><input type="hidden" name="__VIEWSTATE" value="state"/><select name="ctl00$maincontent$mathangnongsan"><option value="Lúa IR 50404 - lúa tươi">Rice</option></select><select name="ctl00$maincontent$Theo_thời_gian"><option value="ngay">Ngày</option></select><input name="ctl00$maincontent$tu_ngay"/><input name="ctl00$maincontent$den_ngay"/><input name="ctl00$maincontent$Xem" value="Tra cứu"/></form>'


def page(day='06-08-2025', unit='kg', market='An Giang', price_type='Bán tại hộ', next_page=False):
    headers='Tên_mặt_hàng Thị_trường Loại_giá Đơn_vị_tính Loại_tiền Nguồn Ngày Giá'.split()
    cells=['Lúa IR 50404 - lúa tươi',market,price_type,unit,'VND','',day,'5900']
    return FORM+'<table id="ctl00_maincontent_GridView1"><tr>'+''.join(f'<th>{x}</th>' for x in headers)+'</tr><tr>'+''.join(f'<td>{x}</td>' for x in cells)+'</tr></table>'+('''<a href="javascript:__doPostBack('ctl00$maincontent$GridView1','Page$2')">2</a>''' if next_page else '')


def test_agro_validates_market_type_currency_and_date():
    config=SOURCES['RICE_IR504'];start,end=date(2025,1,1),date(2025,8,31)
    _,rows,_=parse_page(page(),config,start,end)
    assert rows[0]['price']==5900 and rows[0]['details']['market']=='An Giang'
    assert not parse_page(page(market='Đồng Tháp'),config,start,end)[1]
    assert not parse_page(page(price_type='Xuất khẩu'),config,start,end)[1]
    for html in [page(unit='tấn'),page(day='01-01-2026')]:
        with pytest.raises(ValueError):parse_page(html,config,start,end)


def test_agro_follows_only_published_pager_and_rejects_repeated_page():
    http=Mock();http.get.return_value=Mock(text=FORM)
    http.post.side_effect=[Mock(text=page(next_page=True)),Mock(text=page(day='05-08-2025'))]
    rows=fetch_history(http,SOURCES['RICE_IR504'],date(2025,1,1),date(2025,8,31))
    assert len(rows)==2
    payload=http.post.call_args_list[1].kwargs['data']
    assert payload['__EVENTARGUMENT']=='Page$2' and 'ctl00$maincontent$Xem' not in payload
    http.post.side_effect=[Mock(text=page(next_page=True)),Mock(text=page(next_page=True))]
    with pytest.raises(ValueError,match='lặp trang'):
        fetch_history(http,SOURCES['RICE_IR504'],date(2025,1,1),date(2025,8,31))


REPORT='''<p>Ngày đăng: 05/02/2024</p><p>Từ ngày 21/01 đến ngày 30/01/2024</p><table><tr><td>21</td><td>Mía (từ 7 – 10 chữ đường)</td><td>tấn</td><td>750.000</td><td>1.100.000</td><td>Huyện Tây Hòa</td></tr></table>'''


def test_periodic_report_preserves_period_buying_and_selling():
    row=parse_sugarcane_report(REPORT,'https://example.test/report')
    assert row['period_start']==date(2024,1,21) and row['period_end']==date(2024,1,30)
    assert row['buying_price']==750000 and row['selling_price']==1100000
    with pytest.raises(ValueError):parse_sugarcane_report(REPORT.replace('tấn','kg'),'https://example.test/report')
    with pytest.raises(ValueError):parse_sugarcane_report(REPORT.replace('30/01/2024','30/03/2024'),'https://example.test/report')


def test_periodic_collection_never_creates_daily_observations(client,db_session,monkeypatch):
    import ml_pipeline.observation_scraper as scraper
    commodity=Commodity(code='SUGARCANE',name='Mía',unit='VNĐ/tấn',category='Nông sản',region='Phú Yên')
    db_session.add(commodity);db_session.commit()
    monkeypatch.setattr(scraper,'SUGARCANE_REPORTS',['https://example.test/report'])
    http=Mock();http.get.return_value=Mock(text=REPORT)
    first=scraper.collect_domestic_history(db_session,http,commodity,date(2024,1,1),date(2024,12,31))
    second=scraper.collect_domestic_history(db_session,http,commodity,date(2024,1,1),date(2024,12,31))
    assert first['count']==1 and second['count']==0
    assert db_session.query(PriceHistory).count()==0 and db_session.query(PeriodicPrice).count()==1
    data=client.get('/api/v1/history',params={'commodity_id':commodity.id,'start_date':'2024-01-01','end_date':'2024-12-31'}).json()
    assert not data['readiness']['ready'] and not data['records']
    assert len(data['periodic_records'])==1


def test_domestic_daily_collection_deduplicates_and_records_market(db_session,monkeypatch):
    import ml_pipeline.observation_scraper as scraper
    import ml_pipeline.agro_history as agro
    commodity=Commodity(code='RICE_IR504',name='Lúa',unit='VNĐ/kg',category='Nông sản',region='An Giang')
    db_session.add(commodity);db_session.commit()
    rows=parse_page(page(),SOURCES['RICE_IR504'],date(2025,1,1),date(2025,8,31))[1]
    monkeypatch.setattr(agro,'fetch_history',lambda *args:rows)
    for _ in range(2):scraper.collect_domestic_history(db_session,Mock(),commodity,date(2025,1,1),date(2025,8,31))
    record=db_session.query(PriceHistory).one()
    assert record.provenance=='collected' and 'An Giang' in record.source_details
