"""
Automated Testing Suite - Part 4.1: Alert Rules CRUD, IDOR Defense & Threshold Trigger Engine
File: backend/tests/test_alerts.py
"""
from tests.test_alerts_api import (
    test_alerts_full_crud_and_test_email_trigger,
    test_alerts_idor_protection_between_analysts,
    test_alert_evaluation_engine_price_above_and_below,
)

__all__ = [
    "test_alerts_full_crud_and_test_email_trigger",
    "test_alerts_idor_protection_between_analysts",
    "test_alert_evaluation_engine_price_above_and_below",
]

