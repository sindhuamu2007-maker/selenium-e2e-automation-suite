"""
E2E Test Suite: Dashboard Widgets, Navigation & User Alerts
Maps to Task 1 Manual Test Cases:
- TC_DASH_001: Dynamic rendering of KPI cards
- TC_DASH_002: Sidebar expand and collapse toggle
- TC_DASH_003: Notification bell counter and mark as read
"""

import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

@pytest.fixture(autouse=True)
def authenticated_dashboard(driver, base_url):
    """Logs in as standard user before executing dashboard tests."""
    login_page = LoginPage(driver, base_url).load()
    login_page.login("john.doe@example.com", "Secure@2026!")
    dashboard = DashboardPage(driver, base_url)
    dashboard.wait_for_url_contains("/dashboard")
    return dashboard

@pytest.mark.e2e
@pytest.mark.smoke
def test_dashboard_kpis_render_with_values(authenticated_dashboard):
    """TC_DASH_001: Verify KPI cards load with valid numeric totals."""
    dashboard = authenticated_dashboard

    total_records = dashboard.get_total_records_count()
    critical_records = dashboard.get_critical_records_count()

    assert isinstance(total_records, int) and total_records >= 1
    assert isinstance(critical_records, int) and critical_records >= 0

@pytest.mark.e2e
@pytest.mark.regression
def test_sidebar_collapse_and_expand_toggle(authenticated_dashboard):
    """TC_DASH_002: Verify sidebar expands and collapses when hamburger is clicked."""
    dashboard = authenticated_dashboard

    # Initially not collapsed
    assert not dashboard.is_sidebar_collapsed()

    # Click toggle: becomes collapsed
    dashboard.toggle_sidebar()
    assert dashboard.is_sidebar_collapsed()

    # Click toggle again: expands back
    dashboard.toggle_sidebar()
    assert not dashboard.is_sidebar_collapsed()

@pytest.mark.e2e
@pytest.mark.regression
def test_notification_bell_clears_badge(authenticated_dashboard):
    """TC_DASH_003: Verify notification bell click marks items read and hides badge."""
    dashboard = authenticated_dashboard

    # Initially badge is visible
    assert dashboard.is_notif_badge_visible()

    # Click bell -> Alert accepted
    alert_message = dashboard.click_notifications()
    assert "Notifications marked as read" in alert_message

    # Badge is now dismissed
    assert not dashboard.is_notif_badge_visible()
