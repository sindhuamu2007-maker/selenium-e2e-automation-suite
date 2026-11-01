"""
Dashboard Page Object
Encapsulates KPI widgets, navigation bar, sidebar drawer, and notification elements.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class DashboardPage(BasePage):
    # Locators
    PAGE_HEADING = (By.CSS_SELECTOR, "h3.fw-bold")
    STAT_TOTAL_RECORDS = (By.CSS_SELECTOR, ".stat-card h2.text-primary")
    STAT_CRITICAL_TASKS = (By.CSS_SELECTOR, ".stat-card h2.text-danger")
    SIDEBAR_TOGGLE_BTN = (By.ID, "toggleSidebarBtn")
    SIDEBAR = (By.ID, "mainSidebar")
    NOTIF_BELL_BTN = (By.ID, "notifBell")
    NOTIF_BADGE = (By.ID, "notifBadge")
    LOGOUT_LINK = (By.CSS_SELECTOR, "a[href='/logout']")
    NAV_RECORDS_LINK = (By.CSS_SELECTOR, "a[href='/records']")
    NAV_ADMIN_LINK = (By.CSS_SELECTOR, "a[href='/admin']")
    BREADCRUMB_ACTIVE = (By.CSS_SELECTOR, ".breadcrumb-item.active")

    def __init__(self, driver, base_url="http://127.0.0.1:5000"):
        super().__init__(driver, base_url)

    def load(self):
        self.open_url("/dashboard")
        return self

    def get_heading_text(self):
        return self.get_text(self.PAGE_HEADING)

    def get_total_records_count(self):
        text = self.get_text(self.STAT_TOTAL_RECORDS)
        return int(text) if text.isdigit() else text

    def get_critical_records_count(self):
        text = self.get_text(self.STAT_CRITICAL_TASKS)
        return int(text) if text.isdigit() else text

    def toggle_sidebar(self):
        self.click(self.SIDEBAR_TOGGLE_BTN)
        return self

    def is_sidebar_collapsed(self):
        classes = self.get_attribute(self.SIDEBAR, "class")
        return "collapsed" in classes.split()

    def click_notifications(self):
        self.click(self.NOTIF_BELL_BTN)
        # JavaScript triggers alert('Notifications marked as read!')
        alert_text = self.wait_for_alert_and_accept()
        return alert_text

    def is_notif_badge_visible(self):
        return self.is_displayed(self.NOTIF_BADGE, custom_timeout=1)

    def navigate_to_records(self):
        self.click(self.NAV_RECORDS_LINK)
        return self

    def navigate_to_admin(self):
        self.click(self.NAV_ADMIN_LINK)
        return self

    def logout(self):
        self.click(self.LOGOUT_LINK)
        return self
