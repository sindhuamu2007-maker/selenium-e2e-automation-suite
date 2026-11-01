"""
E2E Test Suite: Search, Multi-Criteria Filtering & Data Export
Maps to Task 1 Manual Test Cases:
- TC_SRCH_001: Global keyword search
- TC_SRCH_002: Zero-match empty state illustration
- TC_SRCH_003: Multi-criteria filtering (Category)
- TC_EXPRT_001: Data table CSV export link
"""

import pytest
from pages.login_page import LoginPage
from pages.records_page import RecordsPage

@pytest.fixture(autouse=True)
def authenticated_records_page(driver, base_url):
    """Logs in and navigates to the records table."""
    login_page = LoginPage(driver, base_url).load()
    login_page.login("john.doe@example.com", "Secure@2026!")
    login_page.wait_for_url_contains("/dashboard")
    records_page = RecordsPage(driver, base_url).load()
    return records_page

@pytest.mark.e2e
@pytest.mark.regression
def test_keyword_search_filters_table(authenticated_records_page):
    """TC_SRCH_001: Verify searching by keyword returns only matching records."""
    records_page = authenticated_records_page

    records_page.search("SOC-2")
    titles = records_page.get_table_record_titles()

    assert len(titles) >= 1
    for title in titles:
        assert "SOC-2" in title

@pytest.mark.e2e
@pytest.mark.regression
def test_non_existent_search_shows_empty_state(authenticated_records_page):
    """TC_SRCH_002: Verify searching for a non-existent keyword displays empty state."""
    records_page = authenticated_records_page

    records_page.search("xyznonexistent99999")
    empty_text = records_page.get_empty_state_text()

    assert "No records found" in empty_text

    # Clear filter returns records
    records_page.clear_filter()
    assert len(records_page.get_table_record_titles()) > 0

@pytest.mark.e2e
@pytest.mark.regression
def test_filter_by_category(authenticated_records_page, driver):
    """TC_SRCH_003: Verify filtering records by Category."""
    records_page = authenticated_records_page

    records_page.filter_by_category("Finance")
    page_text = driver.page_source

    assert "Finance" in page_text

@pytest.mark.e2e
@pytest.mark.smoke
def test_csv_export_endpoint_accessible(authenticated_records_page):
    """TC_EXPRT_001: Verify CSV export button is present with correct download endpoint."""
    records_page = authenticated_records_page
    csv_url = records_page.get_export_csv_href()

    assert "/records/export/csv" in csv_url
