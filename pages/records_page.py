"""
Records Page Object
Encapsulates CRUD operations, modal forms, search/filtering, and CSV export.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time
from pages.base_page import BasePage

class RecordsPage(BasePage):
    # Search and Filter
    SEARCH_INPUT = (By.ID, "searchInput")
    CATEGORY_FILTER = (By.ID, "categorySelect")
    APPLY_FILTER_BTN = (By.ID, "applyFilterBtn")
    CLEAR_FILTER_BTN = (By.ID, "clearFilterBtn")

    # Create Modal
    OPEN_CREATE_MODAL_BTN = (By.CSS_SELECTOR, "button[data-bs-target='#createModal']")
    MODAL_TITLE_INPUT = (By.CSS_SELECTOR, "#createModal input[name='title']")
    MODAL_CATEGORY_SELECT = (By.CSS_SELECTOR, "#createModal select[name='category']")
    MODAL_PRIORITY_SELECT = (By.CSS_SELECTOR, "#createModal select[name='priority']")
    MODAL_DATE_INPUT = (By.CSS_SELECTOR, "#createModal input[name='date']")
    MODAL_SAVE_BTN = (By.CSS_SELECTOR, "#createModal button[type='submit']")

    # Table & Actions
    TABLE_ROWS = (By.CSS_SELECTOR, "tbody tr")
    TABLE_ROW_TITLES = (By.CSS_SELECTOR, "tbody tr td:nth-child(2)")
    EMPTY_STATE_CELL = (By.CSS_SELECTOR, "tbody tr td.text-center")
    EXPORT_CSV_BTN = (By.CSS_SELECTOR, "a[href='/records/export/csv']")

    def __init__(self, driver, base_url="http://127.0.0.1:5000"):
        super().__init__(driver, base_url)

    def load(self):
        self.open_url("/records")
        # Ensure page table is loaded
        self.find(self.APPLY_FILTER_BTN)
        return self

    def search(self, query):
        self.type(self.SEARCH_INPUT, query)
        self.click(self.APPLY_FILTER_BTN)
        # Wait for filtered request to complete
        time.sleep(0.3)
        return self

    def filter_by_category(self, category_name):
        select_elem = self.find(self.CATEGORY_FILTER)
        for option in select_elem.find_elements(By.TAG_NAME, "option"):
            if option.text.strip() == category_name:
                option.click()
                break
        self.click(self.APPLY_FILTER_BTN)
        time.sleep(0.3)
        return self

    def clear_filter(self):
        self.click(self.CLEAR_FILTER_BTN)
        time.sleep(0.3)
        return self

    def open_create_modal(self):
        self.click(self.OPEN_CREATE_MODAL_BTN)
        # Wait for modal title input to be visible and interactable
        self.find(self.MODAL_TITLE_INPUT)
        return self

    def create_record(self, title, category="Finance", priority="High", due_date="2026-11-25"):
        self.open_create_modal()
        self.type(self.MODAL_TITLE_INPUT, title)

        cat_elem = self.find(self.MODAL_CATEGORY_SELECT)
        for opt in cat_elem.find_elements(By.TAG_NAME, "option"):
            if opt.text.strip() == category:
                opt.click()
                break

        prio_elem = self.find(self.MODAL_PRIORITY_SELECT)
        for opt in prio_elem.find_elements(By.TAG_NAME, "option"):
            if opt.text.strip() == priority:
                opt.click()
                break

        if due_date:
            self.type(self.MODAL_DATE_INPUT, due_date)

        self.click(self.MODAL_SAVE_BTN)
        # Wait for modal to dismiss and page reload
        try:
            self.wait.until(EC.invisibility_of_element_located(self.MODAL_SAVE_BTN))
        except Exception:
            pass
        time.sleep(0.4)
        return self

    def get_table_record_titles(self):
        """Returns list of all title strings displayed in table with stale element retry."""
        for _ in range(3):
            try:
                elements = self.find_all(self.TABLE_ROW_TITLES)
                return [elem.text.strip() for elem in elements]
            except StaleElementReferenceException:
                time.sleep(0.3)
        return []

    def delete_first_record(self):
        """Click delete on the first row and accept browser confirmation."""
        first_delete_btn = (By.CSS_SELECTOR, "tbody tr td.text-end form button")
        self.click(first_delete_btn)
        alert_text = self.wait_for_alert_and_accept()
        time.sleep(0.4)
        return alert_text

    def get_empty_state_text(self):
        if self.is_displayed(self.EMPTY_STATE_CELL, custom_timeout=3):
            return self.get_text(self.EMPTY_STATE_CELL)
        return ""

    def get_export_csv_href(self):
        return self.get_attribute(self.EXPORT_CSV_BTN, "href")
