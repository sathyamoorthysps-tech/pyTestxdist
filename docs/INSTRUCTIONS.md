# PyTestxdist - Complete Usage Guide

## Table of Contents
1. [Setup & Installation](#setup--installation)
2. [Running Tests](#running-tests)
3. [Test Structure](#test-structure)
4. [Creating New Tests](#creating-new-tests)
5. [Page Object Pattern](#page-object-pattern)
6. [Debugging](#debugging)
7. [CI/CD Integration](#cicd-integration)
8. [Best Practices](#best-practices)

---

## Setup & Installation

### Quick Start (5 minutes)

```bash
# 1. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install all dependencies
pip install -r requirements.txt

# 3. Install Playwright browsers
playwright install chromium

# 4. Run a test to verify setup
pytest tests/test_search_iphone.py -v
```

### Full Installation Guide

```bash
# Clone repository
git clone <repository-url>
cd pyTestxdist

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install core dependencies
pip install pytest==8.3.2 pytest-xdist==3.8.0 playwright==1.40.0

# Install reporting and BDD tools
pip install allure-pytest==2.13.5 pytest-html==4.1.1 pytest-bdd==7.2.0

# Install optional: metadata and base-url
pip install pytest-metadata==3.1.1 pytest-base-url==2.1.0

# Download browser binaries (required once)
playwright install chromium

# Verify installation
pytest --version
```

---

## Running Tests

### Basic Commands

#### Run All Tests
```bash
pytest tests/
```

#### Run with Verbose Output
```bash
pytest tests/ -v
```

#### Run Specific Test File
```bash
pytest tests/test_search_iphone.py -v
```

#### Run Specific Test Case
```bash
pytest tests/test_search_iphone.py::test_search_and_sort_iphone -v
```

### Parallel Execution

#### Run with Auto-Detection of CPU Cores
```bash
pytest tests/ -n auto
```

#### Run with Specific Number of Workers
```bash
pytest tests/ -n 4  # 4 parallel workers
```

#### Run with Specific Number and Verbose Output
```bash
pytest tests/ -n 4 -v
```

### Filtering Tests

#### Run Only Regression Tests
```bash
pytest -m regression
```

#### Run Only Smoke Tests
```bash
pytest -m smoke
```

#### Run Only Regression (Exclude Flaky)
```bash
pytest -m regression -m "not flaky"
```

#### Run Tests by Pattern
```bash
pytest -k "search"  # Runs tests containing 'search'
pytest -k "not flaky"  # Exclude tests with 'flaky'
```

### Report Generation

#### Allure Report (Recommended)
```bash
# Generate test results
pytest tests/ --alluredir=allure-results

# View Allure report (opens in browser)
allure serve allure-results

# Generate and open report in one command
pytest tests/ --alluredir=allure-results && allure serve allure-results
```

#### HTML Report
```bash
pytest tests/ --html=report.html --self-contained-html
```

#### Both HTML and Allure
```bash
pytest tests/ --html=report.html --self-contained-html --alluredir=allure-results
```

### Advanced Execution Options

#### Stop on First Failure
```bash
pytest tests/ -x
```

#### Stop After N Failures
```bash
pytest tests/ --maxfail=2
```

#### Run Last Failed Tests
```bash
pytest tests/ --lf
```

#### Run Only Failed Tests
```bash
pytest tests/ --ff
```

#### Show Print Statements
```bash
pytest tests/ -v -s
```

#### Custom Timeout
```bash
pytest tests/ --timeout=300  # 5 minutes timeout
```

---

## Test Structure

### Current Test File: `test_search_iphone.py`

```python
import json
import pytest
from pages.amazon_search_page import AmazonSearchPage
from utils.browser_factory import create_context

@pytest.mark.regression
def test_search_and_sort_iphone():
    # Setup: Load test data
    with open("data/test_data.json") as f:
        data = json.load(f)
    
    # Initialize browser
    pw, browser, context, page = create_context()
    
    # Create page object
    amazon = AmazonSearchPage(page)
    
    # Execute test steps
    amazon.open()
    amazon.search_product(data["search_term"])
    amazon.sort_low_to_high()
    
    # Verify and collect results
    items = amazon.fetch_items()
    for item in items:
        print(item["name"], item["price"])
    
    # Cleanup
    context.close()
    browser.close()
    pw.stop()
```

### Test Lifecycle

1. **Setup**: Initialize test data and browser
2. **Execution**: Perform test actions
3. **Verification**: Assert expected outcomes
4. **Teardown**: Close browser and cleanup resources

---

## Creating New Tests

### Step 1: Create New Page Object (if needed)

Create `pages/new_page.py`:

```python
class NewPage:
    def __init__(self, page):
        self.page = page
    
    def navigate_to_url(self, url):
        self.page.goto(url)
    
    def click_element(self, selector):
        self.page.click(selector)
    
    def get_text(self, selector):
        return self.page.inner_text(selector)
```

### Step 2: Create Test File

Create `tests/test_new_feature.py`:

```python
import pytest
from pages.new_page import NewPage
from utils.browser_factory import create_context

@pytest.mark.regression
def test_new_feature():
    pw, browser, context, page = create_context()
    new_page = NewPage(page)
    
    # Test steps
    new_page.navigate_to_url("https://example.com")
    new_page.click_element("button#submit")
    result = new_page.get_text("div.result")
    
    # Assertions
    assert "success" in result.lower()
    
    # Cleanup
    context.close()
    browser.close()
    pw.stop()
```

### Step 3: Add Test Markers

```python
@pytest.mark.smoke  # For quick tests
def test_smoke_feature():
    pass

@pytest.mark.regression  # For full regression suite
def test_regression_feature():
    pass

@pytest.mark.flaky  # For unstable tests
def test_flaky_feature():
    pass
```

### Step 4: Update Test Data

Edit `data/test_data.json`:

```json
{
  "search_term": "iPhone 17 Pro Max",
  "sort_option": "Price: Low to High",
  "new_field": "new_value"
}
```

---

## Page Object Pattern

### Why Page Object Model?

- **Maintainability**: Changes to UI don't break tests
- **Reusability**: Multiple tests can use same page object
- **Readability**: Test code reads like business logic
- **Centralization**: All selectors in one place

### Creating a Page Object

```python
class AmazonSearchPage:
    # Define locators as class constants (recommended)
    SEARCH_BOX = "#twotabsearchtextbox"
    SEARCH_BUTTON = "#nav-search-submit-button"
    SORT_DROPDOWN = "select#s-result-sort-select"
    RESULTS_CONTAINER = "div[data-component-type='s-search-result']"
    
    def __init__(self, page):
        self.page = page
    
    def open(self):
        """Navigate to Amazon India"""
        self.page.goto("https://www.amazon.in")
    
    def search_product(self, product):
        """Search for a product"""
        self.page.fill(self.SEARCH_BOX, product)
        self.page.click(self.SEARCH_BUTTON)
    
    def sort_low_to_high(self):
        """Sort results by price ascending"""
        self.page.select_option(self.SORT_DROPDOWN, "price-asc-rank")
    
    def fetch_items(self):
        """Extract product information from search results"""
        items = []
        results = self.page.locator(self.RESULTS_CONTAINER)
        
        for i in range(min(5, results.count())):
            try:
                name = results.nth(i).locator("h2 a span").inner_text()
            except:
                name = "N/A"
            
            try:
                price = results.nth(i).locator(".a-price-whole").inner_text()
            except:
                price = "N/A"
            
            items.append({"name": name, "price": price})
        
        return items
```

### Locator Best Practices

✅ **Use stable locators:**
- Data attributes: `div[data-component-type='search-result']`
- Semantic HTML: `button[type='submit']`
- Accessible names: `get_by_role('button', name='Submit')`

❌ **Avoid unstable locators:**
- Class-based: `.search-result-item-1` (too specific)
- XPath: `//*[@class='...' and @id='...']` (brittle)
- Index-based: `:nth-child(3)` (depends on DOM order)

---

## Debugging

### Run Tests in Headed Mode

Edit `utils/browser_factory.py`:

```python
def create_context():
    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=False)  # See browser
    context = browser.new_context()
    page = context.new_page()
    return pw, browser, context, page
```

Then run test:
```bash
pytest tests/test_search_iphone.py -s
```

### Use Playwright Inspector

```bash
playwright codegen https://www.amazon.in
```

This opens an interactive inspector to record actions and generate code.

### Add Screenshots on Failure

```python
import pytest
from pathlib import Path

@pytest.fixture(autouse=True)
def take_screenshot_on_failure(page, request):
    yield
    if request.node.rep_call.failed:
        screenshots_dir = Path("screenshots")
        screenshots_dir.mkdir(exist_ok=True)
        page.screenshot(path=screenshots_dir / f"{request.node.name}.png")
```

### Enable Verbose Logging

```bash
pytest tests/ -vv --log-cli-level=DEBUG
```

### Slow Down Test Execution

```python
# In browser_factory.py
page.set_default_timeout(30000)  # 30 seconds
page.set_default_navigation_timeout(30000)  # 30 seconds

# Or add delay before assertions
import time
time.sleep(1)  # Wait 1 second
```

### Print Test Variables

```python
def test_example():
    items = amazon.fetch_items()
    print(f"Found items: {items}")  # Use -s flag to see output
    assert len(items) > 0
```

---

## CI/CD Integration

### GitHub Actions Example

Create `.github/workflows/tests.yml`:

```yaml
name: PyTestxdist Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.11, 3.12]
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        playwright install chromium
    
    - name: Run tests
      run: pytest tests/ -v --alluredir=allure-results
    
    - name: Upload Allure results
      if: always()
      uses: actions/upload-artifact@v2
      with:
        name: allure-results
        path: allure-results/
```

---

## Best Practices

### 1. Use Page Objects Consistently
```python
# ✅ Good
amazon = AmazonSearchPage(page)
amazon.search_product("iPhone")

# ❌ Bad
page.fill("#twotabsearchtextbox", "iPhone")
page.click("#nav-search-submit-button")
```

### 2. Handle Dynamic Waits
```python
# ✅ Good - Explicit wait for element
results = page.locator(".result").first
results.wait_for(state="visible")

# ❌ Bad - Hardcoded sleep
import time
time.sleep(5)
```

### 3. Use Context Managers
```python
# ✅ Good
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    # ...

# ❌ Bad
pw = sync_playwright().start()
browser = pw.chromium.launch()
# Forgot to close!
```

### 4. Organize Test Data
```python
# ✅ Good - External data file
with open("data/test_data.json") as f:
    data = json.load(f)

# ❌ Bad - Hardcoded in test
search_term = "iPhone 17 Pro Max"
```

### 5. Use Meaningful Test Names
```python
# ✅ Good
def test_search_iphone_and_sort_by_price():

# ❌ Bad
def test_1():
```

### 6. Add Assertions
```python
# ✅ Good - Clear assertion
items = amazon.fetch_items()
assert len(items) > 0, "No products found"
assert all("iPhone" in item["name"] for item in items)

# ❌ Bad - No verification
items = amazon.fetch_items()
print(items)
```

---

## Troubleshooting Common Issues

### Issue: `playwright: not found`
**Solution:**
```bash
pip install playwright
playwright install chromium
```

### Issue: `tests not discovered`
**Solution:**
- Ensure files start with `test_`
- Check `pytest.ini` configuration
- Run with: `pytest --collect-only`

### Issue: `timeout waiting for selector`
**Solution:**
```python
# Increase timeout
page.set_default_timeout(60000)  # 60 seconds

# Or use explicit wait
page.wait_for_selector(".result", timeout=60000)
```

### Issue: `tests pass locally but fail in CI`
**Solution:**
- Add explicit waits for dynamic content
- Use data attributes instead of classes
- Capture screenshots on failure
- Check different screen resolution

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `pytest tests/` | Run all tests |
| `pytest -v` | Verbose output |
| `pytest -n auto` | Parallel execution |
| `pytest -m regression` | Filter by marker |
| `pytest -k search` | Filter by name |
| `pytest -x` | Stop on first failure |
| `pytest --lf` | Run last failed |
| `pytest -s` | Show print output |
| `allure serve allure-results` | View report |

---

For more help, refer to README.md or ARCHITECTURE.md
