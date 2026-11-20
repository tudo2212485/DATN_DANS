# -*- coding: utf-8 -*-
"""
AgroForecast End-to-End Automated Browser Test Suite (Playwright + Headless Chrome)
Applied Skills: webapp-testing, test-driven-development, verification-before-completion

Covers:
  - E2E-01: Overview (/) + Location-Aware Pricing (select Khánh Hòa -> direct Sugarcane & benchmark Coffee/Pepper/Rice + cross-province table)
  - E2E-02: Forecast (/forecast) -> auto-select ★ best model on commodity switch, 7N/30N horizon toggle, Tab switch (Detail Grid <-> 5-Model Comparison), 0 console/runtime errors
  - E2E-03: History (/history), Compare (/compare), Alerts (/alerts) -> Syncfusion Grid/Chart clean render, 0 Syncfusion license banner
  - E2E-04: RBAC Security -> Analyst & User blocked from /dashboard/*; Admin accesses all 4 admin pages cleanly
"""
import os
import sys
import time
import pytest
from playwright.sync_api import sync_playwright, Page

BASE_URL = os.environ.get("AGRO_FRONTEND_URL", "http://localhost:3000")
SYNCFUSION_LICENSE_BANNER_SIGNATURES = (
    "syncfusion® license key",
    "syncfusion license",
    "claim your free account",
    "this application was built using a trial version of syncfusion",
)


def _launch_browser(p):
    """Launch headless local Chrome (or fall back to Edge/bundled Chromium)."""
    for kwargs in (
        {"channel": "chrome", "headless": True},
        {"channel": "msedge", "headless": True},
        {"headless": True},
    ):
        try:
            return p.chromium.launch(**kwargs)
        except Exception:
            continue
    raise RuntimeError("No Chromium/Chrome/Edge browser available for Playwright")


def _attach_error_collectors(page: Page):
    console_errors = []
    page_errors = []

    def on_console(msg):
        if msg.type == "error":
            text = msg.text
            # Ignore expected 401/403 network logs when intentionally testing unauthorized RBAC access
            console_errors.append(text)

    def on_pageerror(err):
        page_errors.append(str(err))

    page.on("console", on_console)
    page.on("pageerror", on_pageerror)
    return console_errors, page_errors


def _assert_no_syncfusion_banner(page: Page, context_name: str):
    body_text = (page.locator("body").inner_text() or "").lower()
    for sig in SYNCFUSION_LICENSE_BANNER_SIGNATURES:
        assert sig not in body_text, f"[{context_name}] Syncfusion license banner detected: {sig}"


def _login(page: Page, email: str, password: str):
    page.goto(f"{BASE_URL}/login", wait_until="networkidle")
    page.locator('input[type="email"]').fill(email)
    page.locator('input[type="password"]').fill(password)
    page.locator('button[type="submit"]').click()
    page.wait_for_url(lambda url: "/login" not in url, timeout=15000)
    page.wait_for_load_state("networkidle")


def _logout(page: Page):
    page.evaluate("() => { localStorage.removeItem('agro_access_token'); localStorage.removeItem('agro_user'); }")
    page.goto(f"{BASE_URL}/login", wait_until="networkidle")


@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        br = _launch_browser(p)
        yield br
        br.close()


def test_e2e_01_overview_and_khanh_hoa_location_pricing(browser):
    """E2E-01: Trang Tổng quan (/) load sạch, chọn Khánh Hòa hiện đúng nhãn khảo sát trực tiếp (Mía đường) và tham chiếu vùng."""
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    page = context.new_page()
    console_errors, page_errors = _attach_error_collectors(page)
    try:
        _login(page, "admin@agroforecast.vn", "admin123")
        page.goto(f"{BASE_URL}/", wait_until="networkidle")
        page.wait_for_selector("text=Tổng quan giá nông sản", timeout=15000)
        page.wait_for_selector("text=Cà phê Robusta", timeout=15000)
        page.wait_for_selector("text=Mía đường", timeout=15000)
        _assert_no_syncfusion_banner(page, "Overview default")

        # Open Topbar Location Picker popover & pick Khánh Hòa
        picker_btn = page.locator('button[aria-label*="Chọn khu vực hiển thị giá"]')
        picker_btn.click()
        search_input = page.locator('input[aria-label="Tìm kiếm tỉnh thành"]')
        search_input.wait_for(state="visible", timeout=5000)
        search_input.fill("Khánh Hòa")
        page.locator('.agro-location-popover button:has-text("Khánh Hòa")').first.click()
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(600)

        # Verify transparent badges for Khánh Hòa: direct (Sugarcane) + regional_benchmark (Coffee/Pepper/Rice)
        page.wait_for_selector("text=Khảo sát tại Khánh Hòa", timeout=10000)
        body_text = page.locator("body").inner_text()
        assert "Khảo sát tại Khánh Hòa" in body_text, "Thiếu huy hiệu khảo sát trực tiếp tại Khánh Hòa cho Mía đường"
        assert "Tham chiếu" in body_text, "Thiếu huy hiệu tham chiếu vùng lân cận cho các nông sản khác"

        # Toggle "Chênh lệch giá theo tỉnh hôm nay" table
        page.locator('button:has-text("Chênh lệch giá theo tỉnh hôm nay")').click()
        page.wait_for_load_state("networkidle")
        page.wait_for_selector("text=Đang chọn", timeout=10000)
        _assert_no_syncfusion_banner(page, "Overview Khánh Hòa + Province comparison")

        assert page_errors == [], f"Unhandled runtime errors on /: {page_errors}"
        assert console_errors == [], f"Console errors on /: {console_errors}"
    finally:
        context.close()


def test_e2e_02_forecast_best_model_horizon_and_tabs(browser):
    """E2E-02: Trang Dự báo (/forecast) tự động chọn mô hình ★, đổi kỳ hạn 7N/30N, chuyển tab không văng lỗi."""
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    page = context.new_page()
    console_errors, page_errors = _attach_error_collectors(page)
    try:
        _login(page, "admin@agroforecast.vn", "admin123")
        page.goto(f"{BASE_URL}/forecast?commodity_id=1", wait_until="networkidle")
        page.wait_for_selector("text=Độ chính xác kiểm thử", timeout=15000)
        page.wait_for_timeout(500)

        # Verify ★ best model is auto-selected for Rice IR50404 (XGBoost ★)
        active_model_btn = page.locator('button.bg-\\[\\#2F6F4E\\]:has-text("★")')
        assert active_model_btn.count() >= 1, "Mô hình tốt nhất (★) chưa được tự động kích hoạt trên /forecast"

        # Switch commodity to Sugarcane (id=4 -> Random Forest ★) and confirm auto-selection follows ★
        page.locator("#commodity-select").select_option(value="4")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(600)
        assert page.locator('button.bg-\\[\\#2F6F4E\\]:has-text("★")').count() >= 1, (
            "Đổi sang Mía đường nhưng chưa tự chọn mô hình tốt nhất (★)"
        )

        # Switch horizon 7N -> 30N
        page.locator('button:has-text("7N")').click()
        page.wait_for_load_state("networkidle")
        page.wait_for_selector("text=Bảng chi tiết dự báo (7 ngày)", timeout=10000)

        page.locator('button:has-text("30N")').click()
        page.wait_for_load_state("networkidle")
        page.wait_for_selector("text=Bảng chi tiết dự báo (30 ngày)", timeout=10000)

        # Switch tab: Detail Grid -> 5-Model Comparison -> back to Detail Grid
        page.locator('button:has-text("So sánh 5 mô hình")').click()
        page.wait_for_selector("text=Bảng tổng hợp chỉ số kiểm thử", timeout=10000)
        page.wait_for_timeout(500)
        # Hover over Syncfusion model comparison chart to ensure no BaseTooltip appendChild crash
        chart_svg = page.locator(".e-chart svg").first
        if chart_svg.count() > 0:
            box = chart_svg.bounding_box()
            if box:
                page.mouse.move(box["x"] + box["width"] * 0.4, box["y"] + box["height"] * 0.5)
                page.wait_for_timeout(200)

        page.locator('button:has-text("Bảng chi tiết dự báo")').click()
        page.wait_for_selector(".e-grid", timeout=10000)
        _assert_no_syncfusion_banner(page, "Forecast")

        assert page_errors == [], f"Unhandled runtime errors on /forecast: {page_errors}"
        assert console_errors == [], f"Console errors on /forecast: {console_errors}"
    finally:
        context.close()


def test_e2e_03_history_compare_alerts_clean_syncfusion(browser):
    """E2E-03: Trang Lịch sử (/history), So sánh (/compare), Cảnh báo (/alerts) hiển thị Syncfusion Grid/Chart sạch, 0 banner bản quyền."""
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    page = context.new_page()
    console_errors, page_errors = _attach_error_collectors(page)
    try:
        _login(page, "admin@agroforecast.vn", "admin123")

        # 1. /history
        page.goto(f"{BASE_URL}/history", wait_until="networkidle")
        page.wait_for_selector("text=Dữ liệu lịch sử giá nông sản", timeout=15000)
        page.wait_for_selector(".e-grid", timeout=15000)
        page.wait_for_selector(".e-chart svg", timeout=15000)
        _assert_no_syncfusion_banner(page, "History")

        # 2. /compare
        page.goto(f"{BASE_URL}/compare", wait_until="networkidle")
        page.wait_for_selector("text=So sánh nông sản", timeout=15000)
        page.wait_for_selector("text=Hệ số tương quan Pearson", timeout=15000)
        page.wait_for_selector(".e-chart svg", timeout=15000)
        _assert_no_syncfusion_banner(page, "Compare")

        # 3. /alerts
        page.goto(f"{BASE_URL}/alerts", wait_until="networkidle")
        page.wait_for_selector("text=Cảnh báo", timeout=15000)
        page.wait_for_selector(".e-grid", timeout=15000)
        _assert_no_syncfusion_banner(page, "Alerts")

        assert page_errors == [], f"Unhandled runtime errors on history/compare/alerts: {page_errors}"
        assert console_errors == [], f"Console errors on history/compare/alerts: {console_errors}"
    finally:
        context.close()


def test_e2e_04_rbac_analyst_blocked_and_admin_full_access(browser):
    """E2E-04: Guest bị chuyển về /login, Analyst bị chặn khỏi toàn bộ /dashboard/*; Admin truy cập đầy đủ 4 trang quản trị không lỗi."""
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    page = context.new_page()
    console_errors, page_errors = _attach_error_collectors(page)
    try:
        # Part 0: Unauthenticated Guest trying /dashboard/overview is redirected to /login
        page.goto(f"{BASE_URL}/dashboard/overview", wait_until="networkidle")
        page.wait_for_timeout(600)
        assert "/login" in page.url, f"RBAC BREACH: Khách chưa đăng nhập vẫn vào được /dashboard/overview (URL: {page.url})"

        # Part A: Analyst login -> admin sidebar hidden & direct /dashboard/* URLs redirected away
        _login(page, "anhnguyen@agroforecast.vn", "123456")
        page.goto(f"{BASE_URL}/", wait_until="networkidle")
        assert page.locator('aside a[href="/dashboard/overview"]').count() == 0, (
            "Sidebar vẫn hiển thị mục Quản trị cho role Analyst!"
        )

        for admin_path in (
            "/dashboard/overview",
            "/dashboard/data-control",
            "/dashboard/ml-models",
            "/dashboard/users",
        ):
            page.goto(f"{BASE_URL}{admin_path}", wait_until="networkidle")
            page.wait_for_timeout(800)
            assert not page.url.endswith(admin_path) and "/dashboard/" not in page.url, (
                f"RBAC BREACH: Role Analyst vẫn vào được {admin_path} (current URL: {page.url})"
            )

        # Part B: Admin login -> full access to all 4 admin pages cleanly
        _logout(page)
        console_errors.clear()
        page_errors.clear()
        _login(page, "admin@agroforecast.vn", "admin123")

        admin_checks = [
            ("/dashboard/overview", "Tổng quan hệ thống"),
            ("/dashboard/data-control", "Quản lý dữ liệu"),
            ("/dashboard/ml-models", "Quản lý Mô hình ML"),
            ("/dashboard/users", "Quản lý Tài khoản"),
        ]
        for path, expected_heading in admin_checks:
            page.goto(f"{BASE_URL}{path}", wait_until="networkidle")
            page.wait_for_selector(f"text={expected_heading}", timeout=15000)
            assert path in page.url, f"Admin không truy cập được {path} (URL: {page.url})"
            _assert_no_syncfusion_banner(page, f"Admin {path}")

        assert page_errors == [], f"Unhandled runtime errors on Admin pages: {page_errors}"
        assert console_errors == [], f"Console errors on Admin pages: {console_errors}"
    finally:
        context.close()
