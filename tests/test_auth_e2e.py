"""
E2E Test Suite: User Authentication & Role-Based Access Control (RBAC)
Maps directly to Task 1 Manual Test Cases:
- TC_AUTH_001: Valid user login
- TC_AUTH_002: Unregistered user error handling
- TC_AUTH_003: Incorrect password handling
- TC_AUTH_006: Password visibility masking toggle
- TC_AUTH_009: Session logout
- TC_AUTH_010: RBAC standard user access restriction
- TC_SEC_001: SQL injection sanitization
"""

import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

@pytest.mark.e2e
@pytest.mark.smoke
def test_valid_login_redirects_to_dashboard(driver, base_url):
    """TC_AUTH_001: Verify successful user login with valid credentials."""
    login_page = LoginPage(driver, base_url).load()
    login_page.login("john.doe@example.com", "Secure@2026!")

    dashboard = DashboardPage(driver, base_url)
    assert dashboard.wait_for_url_contains("/dashboard")
    assert "QA Executive Dashboard" in dashboard.get_heading_text()

@pytest.mark.e2e
@pytest.mark.regression
def test_unregistered_email_shows_error(driver, base_url):
    """TC_AUTH_002: Verify error message when attempting login with unregistered email."""
    login_page = LoginPage(driver, base_url).load()
    login_page.login("unknown_user_999@example.com", "DummyPassword123")

    assert login_page.is_error_displayed()
    assert "Invalid email or password" in login_page.get_error_message()

@pytest.mark.e2e
@pytest.mark.regression
def test_incorrect_password_shows_error(driver, base_url):
    """TC_AUTH_003: Verify error message when entering an incorrect password."""
    login_page = LoginPage(driver, base_url).load()
    login_page.login("john.doe@example.com", "WrongPassword123")

    assert login_page.is_error_displayed()
    assert "Invalid email or password" in login_page.get_error_message()

@pytest.mark.e2e
@pytest.mark.regression
def test_password_visibility_toggle(driver, base_url):
    """TC_AUTH_006: Verify password masking and eye visibility toggle."""
    login_page = LoginPage(driver, base_url).load()
    login_page.enter_password("SecretPassword123")

    # Initial state: masked
    assert login_page.get_password_field_type() == "password"

    # Click toggle: unmasked
    login_page.click_password_visibility_toggle()
    assert login_page.get_password_field_type() == "text"

    # Click toggle again: re-masked
    login_page.click_password_visibility_toggle()
    assert login_page.get_password_field_type() == "password"

@pytest.mark.e2e
@pytest.mark.security
def test_sql_injection_login_payload_sanitized(driver, base_url):
    """TC_SEC_001: Verify SQL injection payload in login is neutralized."""
    login_page = LoginPage(driver, base_url).load()
    login_page.login("' OR '1'='1' --", "anypass")

    assert login_page.is_error_displayed()
    assert "SQLi prevented" in login_page.get_error_message()
    assert "/dashboard" not in driver.current_url

@pytest.mark.e2e
@pytest.mark.security
def test_rbac_standard_user_blocked_from_admin(driver, base_url):
    """TC_AUTH_010: Verify Role-Based Access Control blocks standard user from /admin."""
    login_page = LoginPage(driver, base_url).load()
    login_page.login("john.doe@example.com", "Secure@2026!")
    login_page.wait_for_url_contains("/dashboard")

    # Standard user attempts direct access to admin URL
    driver.get(f"{base_url}/admin")
    login_page.wait_for_url_contains("/admin")
    page_source = driver.page_source

    assert "403" in page_source
    assert "Access Denied" in page_source

@pytest.mark.e2e
@pytest.mark.smoke
def test_logout_invalidates_session(driver, base_url):
    """TC_AUTH_009: Verify user logout clears session and redirects to login."""
    login_page = LoginPage(driver, base_url).load()
    login_page.login("john.doe@example.com", "Secure@2026!")

    dashboard = DashboardPage(driver, base_url)
    dashboard.logout()

    assert dashboard.wait_for_url_contains("/login")

    # Attempting to re-enter dashboard directly without logging in
    driver.get(f"{base_url}/dashboard")
    assert "/login" in driver.current_url
