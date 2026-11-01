## ⚡ How to Execute the Projects

### 🛠️ Prerequisites & Setup

Ensure Python 3.10+ is installed, then install the required dependencies:

```bash
pip install selenium pytest pytest-html flask
```

**Note:** WebDriver binaries for Microsoft Edge and Google Chrome are automatically resolved and managed via Selenium 4.

---

### 🚀 Execution Method 1: One-Click Automated Runner (Recommended)

The standalone runner automatically boots the target web application (`app.py`) in the background, checks server health on port 5000, runs the entire Selenium suite, generates an interactive HTML report, and terminates the background server cleanly.

```bash
cd automation_selenium

python run_selenium_tests.py
```

---

### 🖥️ Execution Method 2: Live Browser Mode (Headed / Watch Live on Screen)

By default, tests run in headless mode. To watch Microsoft Edge or Chrome open on your desktop and automatically execute every test case in real time:

```bash
cd automation_selenium

python run_selenium_tests.py --headless false
```

---

### 🧪 Execution Method 3: Direct PyTest CLI Commands (All Variations)

You can run PyTest directly inside the `automation_selenium/` directory.

**Note:** Ensure `python app.py` is running in a separate terminal if executing PyTest directly.

#### A. Run the Complete Test Suite

```bash
# Run all 18 tests with verbose output and self-contained HTML report
python -m pytest -v --html=reports/e2e_test_report.html --self-contained-html

# Run tests with concise progress summary
python -m pytest -q
```

#### B. Run Specific Test Modules

```bash
# Run Authentication & RBAC tests (7 tests)
python -m pytest tests/test_auth_e2e.py -v

# Run Dashboard KPI & Navigation tests (3 tests)
python -m pytest tests/test_dashboard_e2e.py -v

# Run Core Entity CRUD & BVA tests (4 tests)
python -m pytest tests/test_records_crud_e2e.py -v

# Run Search, Filter & CSV Export tests (4 tests)
python -m pytest tests/test_search_export_e2e.py -v
```

#### C. Run Tests by PyTest Markers

The framework defines custom test markers in `pytest.ini`.

```bash
# Run only Smoke tests (critical path verification)
python -m pytest -m smoke -v

# Run only Security tests (SQL Injection & XSS sanitization)
python -m pytest -m security -v

# Run only Regression tests
python -m pytest -m regression -v

# Run all End-to-End tests
python -m pytest -m e2e -v
```

#### D. Run Specific Test Cases by Keyword (-k)

```bash
# Run only the SQL injection sanitization test
python -m pytest -k "test_sql_injection" -v

# Run only the RBAC authorization boundary test
python -m pytest -k "test_rbac" -v

# Run only the 100-character BVA limit test
python -m pytest -k "test_title_character_boundary" -v

# Run only CSV export test
python -m pytest -k "test_csv_export" -v
```

#### E. Cross-Browser Execution

```bash
# Run tests using Microsoft Edge (Default)
python -m pytest --browser edge -v

# Run tests using Google Chrome
python -m pytest --browser chrome -v
```

#### F. Advanced Debugging & Execution Flags

```bash
# Stop immediately upon first test failure (Fail-Fast)
python -m pytest -x -v

# Run with concise, short traceback formatting
python -m pytest --tb=short -v

# Run against a custom base URL or staging server
python -m pytest --base-url http://127.0.0.1:5000 -v
```

---

### 📊 Execution Method 4: View Interactive HTML Test Report

After running the test suite, open the generated HTML report in your default browser.

**Windows (PowerShell / CMD):**

```powershell
start reports/e2e_test_report.html
```

**macOS:**

```bash
open reports/e2e_test_report.html
```

**Linux:**

```bash
xdg-open reports/e2e_test_report.html
```

**Report Features:**

* Visual test pass/fail results.
* Test execution duration and timestamps.
* System environment metadata.
* Embedded screenshots for failed assertions.

---

### 🌐 Execution Method 5: Run the Live Web Portal for Manual Testing (Task 1)

To explore and manually verify the web portal features in your browser:

```bash
python app.py
```

**Application URL:** http://127.0.0.1:5000

**Test Credentials:**

| Role          | Email                                                   | Password            |
| ------------- | ------------------------------------------------------- | ------------------- |
| Standard User | [john.doe@example.com](mailto:john.doe@example.com)     | `Secure@2026!`      |
| SuperAdmin    | [admin.test@example.com](mailto:admin.test@example.com) | `AdminSecure@2026!` |

---

### ⚡ Execution Method 6: Fast In-Process Test Runner (Task 1 Backend Check)

To execute fast in-memory functional tests without launching a browser:

```bash
python run_test_suite.py
```

---

### 📂 Project Execution Summary

| Method   | Description               | Command                                         |
| -------- | ------------------------- | ----------------------------------------------- |
| Method 1 | One-Click Selenium Runner | `python run_selenium_tests.py`                  |
| Method 2 | Live Browser Mode         | `python run_selenium_tests.py --headless false` |
| Method 3 | Direct PyTest Execution   | `python -m pytest -v`                           |
| Method 4 | View HTML Report          | `start reports/e2e_test_report.html`            |
| Method 5 | Launch Web Portal         | `python app.py`                                 |
| Method 6 | In-Process Test Runner    | `python run_test_suite.py`                      |

---

### 📤 How to Push README Updates to GitHub

After updating the README.md file, execute the following commands from your main project directory:

```powershell
cd "C:\Users\Admin\.gemini\antigravity\scratch\Manual_Test_Plan_Suite"

git add README.md

git commit -m "Update README with complete Selenium execution guide"

git push origin main
```

Your updated README will now be available in your GitHub repository.
