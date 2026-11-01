"""
Login Page Object
Encapsulates web elements and user interactions on the Login screen.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    # Locators
    EMAIL_INPUT = (By.NAME, "email")
    PASSWORD_INPUT = (By.ID, "loginPassword")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_ALERT = (By.CSS_SELECTOR, ".alert-danger")
    TOGGLE_PASS_BTN = (By.ID, "togglePassBtn")
    CARD_TITLE = (By.CSS_SELECTOR, "h4.fw-bold")

    def __init__(self, driver, base_url="http://127.0.0.1:5000"):
        super().__init__(driver, base_url)

    def load(self):
        """Navigate to the login page."""
        self.open_url("/login")
        return self

    def enter_email(self, email):
        self.type(self.EMAIL_INPUT, email)
        return self

    def enter_password(self, password):
        self.type(self.PASSWORD_INPUT, password)
        return self

    def click_submit(self):
        self.click(self.SUBMIT_BUTTON)
        return self

    def login(self, email, password):
        """Convenience method to execute a complete login flow."""
        self.enter_email(email)
        self.enter_password(password)
        self.click_submit()
        return self

    def get_error_message(self):
        """Fetch error banner text upon login failure."""
        return self.get_text(self.ERROR_ALERT)

    def is_error_displayed(self):
        return self.is_displayed(self.ERROR_ALERT)

    def click_password_visibility_toggle(self):
        self.click(self.TOGGLE_PASS_BTN)
        return self

    def get_password_field_type(self):
        """Returns 'password' when masked, 'text' when unmasked."""
        return self.get_attribute(self.PASSWORD_INPUT, "type")
