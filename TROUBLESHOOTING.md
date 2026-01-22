# PyTestxdist - Troubleshooting Guide

## Common Issues & Solutions

### 🔴 Issue: Tests Timeout (30000ms exceeded)

**Symptoms:**
```
TimeoutError: Locator.inner_text: Timeout 30000ms exceeded
```

**Root Causes:**
1. Element not found on page
2. Page still loading
3. Network latency
4. Selector incorrect
5. Element hidden/invisible

**Solutions:**

**Option 1: Increase Timeout**
```python
# In utils/browser_factory.py
def create_context():
    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.set_default_timeout(60000)  # Increase to 60 seconds
    page.set_default_navigation_timeout(60000)
    return pw, browser, context, page
```

**Option 2: Debug in Headed Mode**
```bash
# Edit browser_factory.py: headless=False
# Then run:
pytest tests/test_search_iphone.py -s -v
```

You'll see the browser running and can identify the issue.

**Option 3: Use Explicit Waits**
```python
# In page object
def fetch_items(self):
    # Wait for results container to appear
    self.page.wait_for_selector("div[data-component-type='s-search-result']", timeout=60000)
    
    results = self.page.locator("div[data-component-type='s-search-result']")
    # ... rest of code
```

**Option 4: Verify Locator**
```bash
# Use Playwright Inspector to find correct locator
playwright codegen https://www.amazon.in
```

---

### 🔴 Issue: pytest Not Found

**Symptoms:**
```
pytest : The term 'pytest' is not recognized
```

**Root Causes:**
1. pytest not installed
2. Wrong Python environment
3. PATH not updated

**Solutions:**

**Option 1: Install pytest**
```bash
pip install pytest==8.3.2
```

**Option 2: Verify Installation**
```bash
python -m pip list | grep pytest
pytest --version
```

**Option 3: Use Python Module**
```bash
# Instead of: pytest
# Use: python -m pytest
python -m pytest tests/test_search_iphone.py -v
```

**Option 4: Check Virtual Environment**
```bash
# Verify you're using correct Python
which python  # Linux/Mac
where python  # Windows

# Should show path in your venv folder
```

---

### 🔴 Issue: Playwright Not Installed

**Symptoms:**
```
ModuleNotFoundError: No module named 'playwright'
```

**Solution:**
```bash
# Install Playwright
pip install playwright==1.40.0

# Install browser binaries
playwright install chromium

# Verify installation
python -c "from playwright.sync_api import sync_playwright; print('OK')"
```

---

### 🔴 Issue: Browser Launch Fails

**Symptoms:**
```
Error: Chromium launch failed
```

**Root Causes:**
1. Browser not installed
2. System dependencies missing
3. Permission denied

**Solutions:**

**Option 1: Install Chromium**
```bash
playwright install chromium
```

**Option 2: Check System Dependencies (Linux)**
```bash
# Install required libraries
sudo apt-get install -y \
  libgconf-2-4 \
  libdbus-1-3 \
  fonts-liberation \
  libnss3
```

**Option 3: Run as Admin (Windows)**
```bash
# Run command prompt as Administrator
playwright install chromium
```

---

### 🔴 Issue: Locator Strict Mode Error

**Symptoms:**
```
Error: strict mode violation: locator resolved to 2 elements
```

**Root Cause:**
Locator matches multiple elements instead of one

**Solutions:**

**Option 1: Make Locator More Specific**
```python
# ❌ Bad: Matches multiple "span" elements
results.nth(i).locator("h2 span")

# ✅ Good: Specific path
results.nth(i).locator("h2 a span")

# ✅ Good: Use first() method
results.nth(i).locator("h2 span").first
```

**Option 2: Use get_by_role (Recommended)**
```python
# More robust and accessible
name = results.nth(i).get_by_role("link").inner_text()
```

**Option 3: Disable Strict Mode**
```python
# Not recommended, but possible
page.locator("h2 span").first.inner_text()  # Use .first()
```

---

### 🔴 Issue: Tests Pass Locally But Fail in CI/CD

**Root Causes:**
1. Different screen resolution
2. Network/proxy issues
3. Different OS behavior
4. Browser version differences
5. Timing issues

**Solutions:**

**Option 1: Set Explicit Screen Size**
```python
# In browser_factory.py
def create_context():
    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080}
    )
    page = context.new_page()
    return pw, browser, context, page
```

**Option 2: Add Explicit Waits**
```python
# Instead of relying on automatic waits
self.page.wait_for_load_state('networkidle')
```

**Option 3: Increase Timeouts in CI**
```bash
# In GitHub Actions or CI script
pytest tests/ --timeout=300  # 5 minute timeout
```

**Option 4: Add Screenshots on Failure**
```python
@pytest.fixture(autouse=True)
def take_screenshot_on_failure(page, request):
    yield
    if request.node.rep_call.failed:
        page.screenshot(path=f"screenshots/{request.node.name}.png")
```

**Option 5: Check Console Errors**
```python
page.on("console", lambda msg: print(f"Console: {msg.text}"))
```

---

### 🔴 Issue: Tests Too Slow

**Symptoms:**
- Individual test takes > 60 seconds
- Parallel execution not improving overall time

**Root Causes:**
1. Unnecessary waits
2. Inefficient locators
3. Slow network
4. Browser overhead

**Solutions:**

**Option 1: Profile Test Execution**
```python
import time

def test_with_timing():
    start = time.time()
    
    step1_start = time.time()
    amazon.open()
    print(f"Open took {time.time() - step1_start:.2f}s")
    
    step2_start = time.time()
    amazon.search_product("iPhone")
    print(f"Search took {time.time() - step2_start:.2f}s")
    
    print(f"Total: {time.time() - start:.2f}s")
```

**Option 2: Remove Unnecessary Waits**
```python
# ❌ Bad: Hardcoded sleep
import time
time.sleep(5)

# ✅ Good: Wait for element
page.wait_for_selector(".result")
```

**Option 3: Use Fast Selectors**
```python
# ❌ Slow: XPath
page.locator("//h2/span")

# ✅ Fast: CSS selector
page.locator("h2 span")

# ✅ Fastest: Data attributes
page.locator("[data-id='123']")
```

**Option 4: Enable Parallel Execution**
```bash
pytest tests/ -n auto  # Use all CPU cores
```

---

### 🔴 Issue: Allure Report Not Generated

**Symptoms:**
```
allure-results directory is empty
```

**Root Causes:**
1. allure-pytest not installed
2. Tests failed before reporting
3. --alluredir flag not used

**Solutions:**

**Option 1: Install allure-pytest**
```bash
pip install allure-pytest==2.13.5
```

**Option 2: Run with Correct Flag**
```bash
pytest tests/ --alluredir=allure-results
```

**Option 3: Check Report Generation**
```bash
# Verify files were created
ls allure-results/  # Linux/Mac
dir allure-results\  # Windows
```

**Option 4: Install Allure CLI**
```bash
# macOS
brew install allure

# Ubuntu
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure

# Windows (Chocolatey)
choco install allure
```

---

### 🔴 Issue: Parallel Execution Hangs

**Symptoms:**
- Tests start but don't complete
- No output for several minutes
- High CPU usage

**Root Causes:**
1. Deadlock in test code
2. Too many workers for system
3. Resource exhaustion
4. Infinite loop in test

**Solutions:**

**Option 1: Reduce Worker Count**
```bash
# Instead of: pytest -n auto
# Use: pytest -n 2
pytest tests/ -n 2 -v
```

**Option 2: Run with Timeout**
```bash
# Install pytest-timeout
pip install pytest-timeout

# Run with timeout
pytest tests/ -n 4 --timeout=120  # 2 minute timeout per test
```

**Option 3: Debug Sequential First**
```bash
# Run without parallel to isolate issue
pytest tests/ -v  # No -n flag
```

**Option 4: Check System Resources**
```bash
# Check CPU/Memory usage
htop  # Linux
top   # Mac
taskmgr  # Windows
```

---

### 🔴 Issue: Test Data Not Found

**Symptoms:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'data/test_data.json'
```

**Root Cause:**
Running test from wrong directory

**Solutions:**

**Option 1: Run from Project Root**
```bash
cd pyTestxdist
pytest tests/test_search_iphone.py
```

**Option 2: Use Absolute Path**
```python
from pathlib import Path

data_path = Path(__file__).parent.parent / "data" / "test_data.json"
with open(data_path) as f:
    data = json.load(f)
```

**Option 3: Check Working Directory**
```python
import os
print(f"Current directory: {os.getcwd()}")
print(f"Files: {os.listdir('.')}")
```

---

## Debugging Techniques

### Method 1: Print Debug Information

```python
def fetch_items(self):
    items = []
    results = self.page.locator("div[data-component-type='s-search-result']")
    
    print(f"Found {results.count()} results")  # Debug: count
    
    for i in range(min(5, results.count())):
        try:
            name = results.nth(i).locator("h2 a span").inner_text()
            print(f"Item {i}: {name}")  # Debug: each item
        except Exception as e:
            print(f"Error on item {i}: {e}")  # Debug: errors
```

**Run with output:**
```bash
pytest tests/test_search_iphone.py -s
```

### Method 2: Playwright Inspector

```bash
# Interactive browser debugging
playwright codegen https://www.amazon.in

# Inspect elements
playwright inspector
```

### Method 3: Screenshots

```python
# Take screenshot at specific point
page.screenshot(path="debug_screenshot.png")
```

### Method 4: Browser DevTools

```python
# Open DevTools in headed mode
context = browser.new_context()
page = context.new_page()

# Headed mode shows DevTools
browser = pw.chromium.launch(headless=False, devtools=True)
```

### Method 5: Logging Framework

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Starting test")
logger.info("Found items")
logger.error("Failed to extract price")
```

---

## Performance Troubleshooting

### Check if Network is Bottleneck

```python
import time

# Measure different phases
start = time.perf_counter()
page.goto("https://www.amazon.in")
navigation_time = time.perf_counter() - start
print(f"Navigation: {navigation_time:.2f}s")

# If navigation > 10s, network is likely bottleneck
```

### Check if Locator is Bottleneck

```python
import time

start = time.perf_counter()
results = page.locator("div[data-component-type='s-search-result']").count()
locator_time = time.perf_counter() - start
print(f"Locator query: {locator_time:.2f}s")

# If > 5s, consider caching or optimizing selector
```

### Memory Leak Detection

```python
import psutil
import os

process = psutil.Process(os.getpid())

start_memory = process.memory_info().rss
# Run test
end_memory = process.memory_info().rss

print(f"Memory used: {(end_memory - start_memory) / 1024 / 1024:.2f}MB")
```

---

## Getting Help

### Where to Find Answers

1. **Official Documentation**
   - [Playwright Docs](https://playwright.dev/python/)
   - [pytest Docs](https://docs.pytest.org/)

2. **Community Support**
   - Stack Overflow (tag: `playwright`)
   - GitHub Issues

3. **Project Documentation**
   - [README.md](README.md)
   - [INSTRUCTIONS.md](INSTRUCTIONS.md)
   - [ARCHITECTURE.md](ARCHITECTURE.md)

---

## Quick Reference

| Issue | Command |
|-------|---------|
| Install deps | `pip install -r requirements.txt` |
| Run tests | `pytest tests/ -v` |
| Headed mode | Edit `browser_factory.py` headless=False |
| Debug mode | `pytest tests/ -s -vv` |
| Help | `pytest --help` |
| Clear cache | `pytest --cache-clear` |

---

**Still stuck?** Refer to official Playwright documentation or create an issue in the repository.
