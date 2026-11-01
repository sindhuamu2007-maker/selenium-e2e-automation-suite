"""
PyTest Configuration & WebDriver Fixtures
Manages browser lifecycle, command line options, and automatic failure screenshots.
"""

import pytest
import os
import time
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions

def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default="edge", help="Browser choice: edge or chrome"
    )
    parser.addoption(
        "--headless", action="store", default="true", help="Run browser in headless mode: true or false"
    )
    parser.addoption(
        "--base-url", action="store", default="http://127.0.0.1:5000", help="Base URL of application under test"
    )

@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("--base-url").rstrip("/")

@pytest.fixture(scope="function")
def driver(request):
    """Initializes WebDriver instance per test function and performs teardown."""
    browser_name = request.config.getoption("--browser").lower()
    is_headless = request.config.getoption("--headless").lower() == "true"

    if browser_name == "chrome":
        options = ChromeOptions()
        if is_headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver_instance = webdriver.Chrome(options=options)
    else:  # default to edge
        options = EdgeOptions()
        if is_headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver_instance = webdriver.Edge(options=options)

    driver_instance.implicitly_wait(3)

    yield driver_instance

    # Teardown
    try:
        driver_instance.quit()
    except Exception:
        pass

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture screenshot on test failure and attach to report."""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver_fixture = item.funcargs.get("driver", None)
        if driver_fixture:
            screenshots_dir = os.path.join(os.path.dirname(__file__), "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshots_dir, f"FAIL_{item.name}_{int(time.time())}.png")
            driver_fixture.save_screenshot(screenshot_path)
            # Add to pytest-html if present
            extra = getattr(rep, "extra", [])
            pytest_html = item.config.pluginmanager.getplugin("html")
            if pytest_html:
                extra.append(pytest_html.extras.image(screenshot_path))
                rep.extra = extra
