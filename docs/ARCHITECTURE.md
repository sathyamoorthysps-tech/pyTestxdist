# PyTestxdist - Architecture & Design

## Table of Contents
1. [System Architecture](#system-architecture)
2. [Design Patterns](#design-patterns)
3. [Component Details](#component-details)
4. [Data Flow](#data-flow)
5. [Testing Strategy](#testing-strategy)
6. [Scalability](#scalability)
7. [Performance Optimization](#performance-optimization)

---

## System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────┐
│           PyTestxdist Test Framework                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │          Test Layer (tests/)                      │  │
│  │  ├── test_search_iphone.py                       │  │
│  │  ├── features/ (BDD)                             │  │
│  │  ├── steps/ (BDD step definitions)               │  │
│  │  └── flaky/ (Known unstable tests)               │  │
│  └──────────────────────────────────────────────────┘  │
│           ↓                                              │
│  ┌──────────────────────────────────────────────────┐  │
│  │     Page Object Model Layer (pages/)             │  │
│  │  └── amazon_search_page.py                       │  │
│  │      - open()                                    │  │
│  │      - search_product()                          │  │
│  │      - sort_low_to_high()                        │  │
│  │      - fetch_items()                             │  │
│  └──────────────────────────────────────────────────┘  │
│           ↓                                              │
│  ┌──────────────────────────────────────────────────┐  │
│  │    Utilities Layer (utils/)                       │  │
│  │  └── browser_factory.py (Playwright Setup)       │  │
│  │      - create_context()                          │  │
│  └──────────────────────────────────────────────────┘  │
│           ↓                                              │
│  ┌──────────────────────────────────────────────────┐  │
│  │      Browser Automation (Playwright)             │  │
│  │  ├── Chromium Browser                            │  │
│  │  ├── Page Navigation                             │  │
│  │  ├── Element Interaction                         │  │
│  │  └── DOM Querying                                │  │
│  └──────────────────────────────────────────────────┘  │
│           ↓                                              │
│  ┌──────────────────────────────────────────────────┐  │
│  │        Target Application (Amazon.in)            │  │
│  │  ├── Search UI                                   │  │
│  │  ├── Filters & Sorting                           │  │
│  │  └── Product Results                             │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Execution Flow

```
┌─────────────┐
│  pytest     │
│   start     │
└──────┬──────┘
       │
       ├─────→ pytest-xdist (Distribute to workers)
       │              ↓
       │       ┌──────┴──────┐
       │       ↓             ↓
       │   Worker 1      Worker 2
       │       │             │
       │       └──────┬──────┘
       │              ↓
       │    Load test_search_iphone.py
       │              ↓
       │    Create browser instance
       │              ↓
       │    Execute test steps
       │              │
       │    ├─ amazon.open()
       │    ├─ amazon.search_product()
       │    ├─ amazon.sort_low_to_high()
       │    ├─ amazon.fetch_items()
       │    │
       │    └─ Cleanup (close browser)
       │              ↓
       │    Allure Report Generation
       │              ↓
       │    HTML Report Generation
       │              ↓
       └─ Return Results
```

---

## Design Patterns

### 1. Page Object Model (POM)

**Purpose:** Separate test logic from UI interactions

**Implementation:**

```python
class AmazonSearchPage:
    # Locators
    SEARCH_BOX = "#twotabsearchtextbox"
    SEARCH_BUTTON = "#nav-search-submit-button"
    SORT_DROPDOWN = "select#s-result-sort-select"
    RESULTS_CONTAINER = "div[data-component-type='s-search-result']"
    
    def __init__(self, page):
        self.page = page
    
    # Methods encapsulate actions
    def open(self):
        """Navigate to application"""
        pass
    
    def search_product(self, product):
        """Search functionality"""
        pass
```

**Benefits:**
- Centralized locator management
- Easy maintenance when UI changes
- Reusable across multiple tests
- Improved readability

### 2. Factory Pattern

**Purpose:** Create and configure browser instances

**Implementation:**

```python
# browser_factory.py
def create_context():
    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    return pw, browser, context, page
```

**Benefits:**
- Centralized browser configuration
- Easy to switch browsers (chromium, firefox, webkit)
- Consistent setup across tests
- Easy to add proxy, cookies, headers

### 3. Fixture Pattern

**Purpose:** Setup and teardown test resources

**Potential Implementation:**

```python
@pytest.fixture
def browser_context():
    pw, browser, context, page = create_context()
    yield page
    context.close()
    browser.close()
    pw.stop()

def test_example(browser_context):
    page = browser_context
    # Test code
```

### 4. Data-Driven Testing

**Purpose:** Parameterize tests with different data

**Implementation:**

```python
# data/test_data.json
{
  "search_term": "iPhone 17 Pro Max",
  "sort_option": "Price: Low to High"
}

# test_search_iphone.py
with open("data/test_data.json") as f:
    data = json.load(f)
```

**Future Enhancement:**

```python
@pytest.mark.parametrize("product,expected", [
    ("iPhone", True),
    ("Samsung", True),
    ("xyz", False)
])
def test_search_product(browser_context, product, expected):
    # Test implementation
```

---

## Component Details

### 1. Test Layer (`tests/`)

**Responsibility:** Define test cases and assertions

```
tests/
├── test_search_iphone.py     # Main test logic
├── features/                  # BDD feature files
│   └── search_iphone.feature
├── steps/                     # BDD step implementations
│   └── search_steps.py
└── flaky/                     # Known unstable tests
    └── test_sort_price_flaky.py
```

**Test Execution Flow:**
1. Load test data
2. Initialize browser
3. Create page object
4. Execute test actions
5. Verify results
6. Cleanup resources

### 2. Page Object Layer (`pages/`)

**Responsibility:** Encapsulate UI interactions

**amazon_search_page.py:**
```python
class AmazonSearchPage:
    def __init__(self, page):
        # Store page reference
        self.page = page
    
    def open(self):
        # Navigate to application
        
    def search_product(self, product):
        # Perform search
        
    def sort_low_to_high(self):
        # Apply sorting
        
    def fetch_items(self):
        # Extract results with robust error handling
```

**Key Features:**
- Stable locators with fallbacks
- Exception handling for dynamic UI
- Returns structured data (dict/list)

### 3. Utilities Layer (`utils/`)

**Responsibility:** Provide helper functions

**browser_factory.py:**
```python
def create_context():
    # 1. Start Playwright
    pw = sync_playwright().start()
    
    # 2. Launch browser
    browser = pw.chromium.launch(headless=True)
    
    # 3. Create isolated context
    context = browser.new_context()
    
    # 4. Create page
    page = context.new_page()
    
    # 5. Return all components for lifecycle management
    return pw, browser, context, page
```

**Future Enhancements:**
- Add logging
- Add screenshot on failure
- Add custom wait conditions
- Add performance tracking

### 4. Configuration Layer (`pytest.ini`)

```ini
[pytest]
addopts =
  -n auto                      # Parallel execution
  --alluredir=allure-results   # Allure reports
markers =
  smoke                        # Quick tests
  regression                   # Full suite
  flaky                        # Unstable tests
```

### 5. Data Layer (`data/`)

```json
{
  "search_term": "iPhone 17 Pro Max",
  "sort_option": "Price: Low to High"
}
```

**Future Structure:**
```
data/
├── test_data.json
├── credentials.json
├── environments.json
└── bulk_test_data.csv
```

---

## Data Flow

### Test Execution Data Flow

```
┌─────────────────────────────────┐
│  data/test_data.json            │
│  {                              │
│    "search_term": "iPhone..."   │
│  }                              │
└──────────────┬──────────────────┘
               │
               ↓
┌─────────────────────────────────┐
│  test_search_iphone()           │
│  Load test data                 │
└──────────────┬──────────────────┘
               │
               ↓
┌─────────────────────────────────┐
│  AmazonSearchPage               │
│  1. open()                      │
│  2. search_product(data)        │
│  3. sort_low_to_high()          │
│  4. fetch_items()               │
└──────────────┬──────────────────┘
               │
               ↓
┌─────────────────────────────────┐
│  Playwright (page object)       │
│  goto() -> fill() -> click()     │
│  locator() -> inner_text()       │
└──────────────┬──────────────────┘
               │
               ↓
┌─────────────────────────────────┐
│  Browser Automation             │
│  Send commands to browser       │
└──────────────┬──────────────────┘
               │
               ↓
┌─────────────────────────────────┐
│  Amazon.in Application          │
│  Load page -> Render -> Respond  │
└──────────────┬──────────────────┘
               │
               ↓
┌─────────────────────────────────┐
│  Parsed Results (List[Dict])    │
│  [                              │
│    {"name": "...", "price": "..."}, │
│    ...                          │
│  ]                              │
└──────────────┬──────────────────┘
               │
               ↓
┌─────────────────────────────────┐
│  Test Assertions & Verification │
│  Validate results               │
└──────────────┬──────────────────┘
               │
               ↓
┌─────────────────────────────────┐
│  Report Generation              │
│  Allure + HTML Reports          │
└─────────────────────────────────┘
```

### Locator Resolution Flow

```
┌──────────────────────────────────┐
│  Primary Locator                 │
│  "h2 a span"                     │
└────────────┬─────────────────────┘
             │
             ├─ Try to find → SUCCESS? ✓
             │
             └─ No match → EXCEPTION
                         │
                         ↓
          ┌──────────────────────────────┐
          │  Fallback Locator 1          │
          │  "h2 span".first             │
          └────────────┬─────────────────┘
                       │
                       ├─ Try to find → SUCCESS? ✓
                       │
                       └─ No match → EXCEPTION
                                   │
                                   ↓
                        ┌──────────────────────────────┐
                        │  Fallback Locator 2          │
                        │  Return "N/A"                │
                        └──────────────────────────────┘
```

---

## Testing Strategy

### Test Pyramid

```
              /\              
             /  \      Unit Tests
            /    \     (Not applicable for E2E)
           /──────\    
          /        \   
         /          \  Integration/API Tests
        /____________\
       /              \
      /                \ E2E Tests (Current Focus)
     /──────────────────\
    /                    \
   /__________────________\
```

### Test Classification

**Smoke Tests** (`@pytest.mark.smoke`)
- Quick sanity checks
- Core functionality only
- < 2 minutes total

**Regression Tests** (`@pytest.mark.regression`)
- Full test suite
- Comprehensive coverage
- 5-15 minutes total

**Flaky Tests** (`@pytest.mark.flaky`)
- Known unstable tests
- Network-dependent
- Require investigation

### Current Test: test_search_and_sort_iphone

**Type:** Regression  
**Duration:** ~30 seconds  
**Coverage:**
- Navigation to Amazon.in
- Product search functionality
- Sort/filter functionality
- Result extraction and parsing

---

## Scalability

### Horizontal Scalability

**Parallel Execution (Current Implementation):**

```bash
# Auto-detection
pytest -n auto  # Uses available CPU cores

# Manual specification
pytest -n 8     # 8 parallel workers
```

**How it works:**
1. pytest-xdist distributes tests across workers
2. Each worker runs in isolated browser context
3. Results aggregated for final report
4. No test interference (independent contexts)

**Scaling Challenges:**
- Resource constraints (CPU, Memory, Network)
- Rate limiting from target website
- Database connection pools
- Screenshot/video storage

**Solutions:**
```bash
# Reduce worker count on limited systems
pytest -n 2

# Add delay between requests
import time
time.sleep(1)  # Between actions

# Implement retry logic
@pytest.fixture
def retry_test(request):
    if request.node.rep_call.failed:
        # Retry mechanism
        pass
```

### Vertical Scalability

**Test Infrastructure Improvements:**
1. Headless browser execution (already implemented)
2. Browser context reuse
3. Connection pooling
4. Local test execution cache

### Adding More Tests

**File Structure:**
```
tests/
├── test_search_iphone.py
├── test_product_filters.py      # New
├── test_checkout_flow.py         # New
├── test_payment.py               # New
└── flaky/
    ├── test_sort_price_flaky.py
    └── test_review_loading.py    # New
```

**Each test uses dedicated Page Object:**
```python
# pages/product_filter_page.py
class ProductFilterPage:
    def filter_by_rating(self, rating):
        pass

# pages/checkout_page.py
class CheckoutPage:
    def add_to_cart(self, item):
        pass
```

---

## Performance Optimization

### Current Performance Metrics

| Metric | Value | Status |
|--------|-------|--------|
| Test Execution Time | ~30 seconds | ✓ Good |
| Browser Startup | ~5 seconds | ⚠️ Average |
| Locator Resolution | <1 second | ✓ Good |
| Resource Usage (Memory) | ~200MB | ✓ Good |

### Optimization Strategies

### 1. Browser Reuse

```python
# Current: Browser closes after each test
def test_1():
    pw, browser, context, page = create_context()
    # Test
    context.close()
    browser.close()
    pw.stop()

# Future: Browser pooling
class BrowserPool:
    @staticmethod
    def get_browser():
        if not browser_instance:
            browser_instance = create_browser()
        return browser_instance
```

### 2. Lazy Loading

```python
# Current: Load all 5 items every time
items = amazon.fetch_items()  # Fetches 5 items

# Future: Load on demand
class LazyResultsIterator:
    def __next__(self):
        # Load one item at a time
        pass
```

### 3. Caching

```python
# Future: Cache page state
@cache
def get_search_results(search_term):
    return amazon.fetch_items()
```

### 4. Async Test Execution

```python
# Current: Synchronous
async def test_async_search():
    # Playwright async API
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        # Test implementation
```

### 5. Resource Management

```python
# Monitor memory usage
import psutil
memory_before = psutil.Process().memory_info().rss
# Test execution
memory_after = psutil.Process().memory_info().rss
print(f"Memory used: {(memory_after - memory_before) / 1024 / 1024}MB")
```

### Performance Monitoring

```python
import time

def test_performance():
    start = time.time()
    amazon.search_product("iPhone")
    duration = time.time() - start
    assert duration < 5, f"Search took {duration}s"
```

---

## Future Enhancements

### Phase 1: Robustness
- [ ] Add comprehensive error handling
- [ ] Implement retry mechanisms
- [ ] Add screenshot on failure
- [ ] Add video recording

### Phase 2: Scalability
- [ ] Implement database backend
- [ ] Add cloud execution support
- [ ] Create test data generator
- [ ] Add performance benchmarking

### Phase 3: Intelligence
- [ ] Add visual regression testing
- [ ] Implement ML-based flaky test detection
- [ ] Add smart wait conditions
- [ ] Implement automatic locator healing

### Phase 4: Integration
- [ ] CI/CD pipeline integration
- [ ] Slack notifications
- [ ] Test result dashboard
- [ ] Integration with APM tools

---

## Deployment Architecture

### Local Development
```
Developer → pytest → Playwright → Amazon.in
```

### CI/CD Pipeline
```
Git Push → GitHub Actions → pytest-xdist → Multiple Workers → Allure Report
```

### Cloud Execution
```
Cloud Service → Browser Cloud (BrowserStack) → Tests → Report
```

---

## Monitoring & Logging

### Current State
- Minimal logging
- No performance tracking
- No failure analysis

### Recommended Implementation
```python
import logging

logger = logging.getLogger(__name__)
logger.info("Starting test: test_search_iphone")
logger.debug(f"Found {len(items)} items")
logger.error("Failed to fetch items", exc_info=True)
```

---

For implementation details, see INSTRUCTIONS.md  
For usage guide, see README.md
