"""
Automated Testing Suite - Part 4.1: Authentication, Session Security & RBAC Authorization
File: backend/tests/test_auth_rbac.py
"""
from tests.test_auth_and_rbac import (
    test_register_new_account_and_prevent_password_leak,
    test_login_success_and_wrong_password_rejected,
    test_locked_account_cannot_login_or_access_api,
    test_unauthenticated_requests_return_401,
    test_analyst_blocked_from_admin_mutations_with_403,
)

__all__ = [
    "test_register_new_account_and_prevent_password_leak",
    "test_login_success_and_wrong_password_rejected",
    "test_locked_account_cannot_login_or_access_api",
    "test_unauthenticated_requests_return_401",
    "test_analyst_blocked_from_admin_mutations_with_403",
]
