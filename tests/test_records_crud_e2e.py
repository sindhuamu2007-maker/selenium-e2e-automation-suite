"""
E2E Test Suite: Core Entity CRUD Operations & Form Validations
Maps to Task 1 Manual Test Cases:
- TC_CRUD_001: Create new record with valid data
- TC_CRUD_003: Boundary Value Analysis (BVA) on Title field
- TC_CRUD_007: Delete record with confirmation dialog
- TC_SEC_002: Cross-Site Scripting (XSS) input encoding
"""

import pytest
import time
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
@pytest.mark.smoke
def test_create_record_persists_in_table(authenticated_records_page):
    """TC_CRUD_001: Verify creating a record appears immediately at the top of the table."""
    records_page = authenticated_records_page

    unique_title = f"Automated E2E Audit {int(time.time())}"
    records_page.create_record(
        title=unique_title,
        category="Security",
        priority="Critical",
        due_date="2026-12-15"
    )

    titles = records_page.get_table_record_titles()
    assert unique_title in titles

@pytest.mark.e2e
@pytest.mark.regression
def test_title_character_boundary_100_chars(authenticated_records_page):
    """TC_CRUD_003: Boundary Value Analysis (BVA) verifying 100 character max limit."""
    records_page = authenticated_records_page

    # 100-character string
    boundary_title = "A" * 100
    records_page.create_record(title=boundary_title, category="Finance", priority="Low")

    titles = records_page.get_table_record_titles()
    assert boundary_title in titles

@pytest.mark.e2e
@pytest.mark.security
def test_xss_payload_in_title_encoded_safely(authenticated_records_page, driver):
    """TC_SEC_002: Verify Cross-Site Scripting (XSS) payload is rendered as harmless text."""
    records_page = authenticated_records_page

    xss_payload = "E2E XSS Test <script>alert('pwned')</script>"
    records_page.create_record(title=xss_payload, category="DevOps", priority="Medium")

    page_html = driver.page_source
    # Must NOT execute raw unescaped script tags
    assert "&lt;script&gt;alert('pwned')&lt;/script&gt;" in page_html or "E2E XSS Test" in page_html
    # Ensure no unexpected alert box was triggered by unescaped scripts
    assert "<script>alert('pwned')</script>" not in page_html

@pytest.mark.e2e
@pytest.mark.smoke
def test_delete_record_with_confirmation_dialog(authenticated_records_page):
    """TC_CRUD_007: Verify record deletion triggers native confirmation and removes row."""
    records_page = authenticated_records_page

    # First create a temporary record to delete
    temp_title = f"Temporary Delete Item {int(time.time())}"
    records_page.create_record(title=temp_title)
    assert temp_title in records_page.get_table_record_titles()

    # Perform delete on the newly created top record
    alert_text = records_page.delete_first_record()
    assert "Are you sure you want to delete" in alert_text

    # Verify the deleted item is gone
    titles_after_delete = records_page.get_table_record_titles()
    assert temp_title not in titles_after_delete
