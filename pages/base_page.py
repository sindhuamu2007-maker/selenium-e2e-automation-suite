"""
Base Page Object
Contains common WebDriver interactions, explicit waits, and utility methods.
Follows the Page Object Model (POM) design pattern.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
import time

class BasePage:
    def __init__(self, driver, base_url="http://127.0.0.1:5000", timeout=10):
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    def open_url(self, path=""):
        full_url = f"{self.base_url}/{path.lstrip('/')}"
        self.driver.get(full_url)
        return self

    def find(self, locator):
        """Wait for element to be present and visible before returning."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        """Find all matching elements present in DOM."""
        try:
            return self.wait.until(EC.presence_of_all_elements_located(locator))
        except TimeoutException:
            return []

    def click(self, locator):
        """Wait for element to be clickable and perform click."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def type(self, locator, text, clear_first=True):
        """Type text into an input element after ensuring visibility."""
        element = self.find(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        """Get visible inner text of element."""
        return self.find(locator).text.strip()

    def get_attribute(self, locator, attribute_name):
        """Get attribute value of element."""
        return self.find(locator).get_attribute(attribute_name)

    def is_displayed(self, locator, custom_timeout=3):
        """Check if element is displayed without throwing long timeout."""
        try:
            WebDriverWait(self.driver, custom_timeout).until(EC.visibility_of_element_located(locator))
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def wait_for_url_contains(self, text):
        """Wait until browser URL contains expected substring."""
        return self.wait.until(EC.url_contains(text))

    def wait_for_alert_and_accept(self):
        """Wait for JavaScript alert, return text, and accept it."""
        alert = self.wait.until(EC.alert_is_present())
        alert_text = alert.text
        alert.accept()
        return alert_text

    def take_screenshot(self, name):
        """Save a PNG screenshot in the screenshots directory."""
        screenshots_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)
        filename = f"{name}_{int(time.time())}.png"
        filepath = os.path.join(screenshots_dir, filename)
        self.driver.save_screenshot(filepath)
        return filepath
