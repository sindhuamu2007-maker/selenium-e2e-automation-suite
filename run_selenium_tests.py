"""
Selenium E2E Test Suite Orchestrator & Runner
Automatically starts local app.py (if not running), executes PyTest Selenium suite,
generates a rich HTML report, and handles teardown.
"""

import sys
import os
import subprocess
import time
import urllib.request
import urllib.error

# Set terminal UTF-8 encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Colorama / ANSI formatting
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

APP_URL = "http://127.0.0.1:5000"
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUTOMATION_DIR = os.path.dirname(os.path.abspath(__file__))

def is_server_running(url):
    try:
        with urllib.request.urlopen(f"{url}/login", timeout=2) as response:
            return response.status in [200, 302]
    except Exception:
        return False

def start_portal_server():
    print(f"{CYAN}>> Checking if Enterprise Web Portal is running at {APP_URL}...{RESET}")
    if is_server_running(APP_URL):
        print(f"{GREEN}✔ Web Portal is already active on {APP_URL}{RESET}\n")
        return None

    app_script = os.path.join(PROJECT_DIR, "app.py")
    print(f"{CYAN}>> Starting background portal server: python app.py ...{RESET}")
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    proc = subprocess.Popen([sys.executable, app_script], cwd=PROJECT_DIR, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Wait up to 10 seconds for portal to become healthy
    for _ in range(20):
        time.sleep(0.5)
        if is_server_running(APP_URL):
            print(f"{GREEN}✔ Web Portal successfully booted on PID {proc.pid}!{RESET}\n")
            return proc

    print(f"{RED}✖ Failed to start web portal within 10 seconds.{RESET}")
    return proc

def main():
    print(f"\n{BOLD}{CYAN}{'=' * 75}{RESET}")
    print(f"{BOLD}🚀 TASK 2: SELENIUM & WEBDRIVER AUTOMATED E2E TEST SUITE RUNNER{RESET}")
    print(f"{BOLD}{CYAN}{'=' * 75}{RESET}\n")

    server_process = start_portal_server()

    try:
        # Run pytest inside automation_selenium directory
        pytest_cmd = [
            sys.executable, "-m", "pytest",
            "-v",
            "--html=reports/e2e_test_report.html",
            "--self-contained-html"
        ]

        # Allow passing custom CLI flags (e.g. -k test_auth, --browser chrome, --headless false)
        if len(sys.argv) > 1:
            pytest_cmd.extend(sys.argv[1:])

        print(f"{CYAN}>> Executing command: {' '.join(pytest_cmd)}{RESET}\n")
        exit_code = subprocess.call(pytest_cmd, cwd=AUTOMATION_DIR)

        report_path = os.path.join(AUTOMATION_DIR, "reports", "e2e_test_report.html")

        print(f"\n{BOLD}{CYAN}{'=' * 75}{RESET}")
        print(f"{BOLD}📊 AUTOMATION RUN COMPLETE{RESET}")
        print(f"{BOLD}{CYAN}{'=' * 75}{RESET}")
        if exit_code == 0:
            print(f"  {GREEN}{BOLD}✔ ALL E2E SELENIUM TEST CASES PASSED SUCCESSFULLY!{RESET}")
        else:
            print(f"  {RED}{BOLD}✖ ONE OR MORE TESTS FAILED (Exit Code: {exit_code}){RESET}")

        if os.path.exists(report_path):
            print(f"  📄 Interactive HTML Report: {BOLD}{report_path}{RESET}")
        print(f"{CYAN}{'=' * 75}{RESET}\n")

        return exit_code

    finally:
        if server_process:
            print(f"{CYAN}>> Cleaning up: Stopping background portal server (PID {server_process.pid})...{RESET}")
            server_process.terminate()
            try:
                server_process.wait(timeout=3)
            except Exception:
                server_process.kill()

if __name__ == "__main__":
    sys.exit(main())
