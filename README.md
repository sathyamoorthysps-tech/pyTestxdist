# PyTestxdist - E2E Test Automation Framework

## Project Overview

**PyTestxdist** is an end-to-end test automation framework for web applications, specifically designed to test e-commerce search and filtering functionalities. This project leverages **Playwright** for browser automation and **pytest** with **xdist** for parallel test execution.

### Key Features

- ✅ **Web UI Automation** - Automated browser interactions using Playwright
- ✅ **Parallel Execution** - Run tests concurrently using pytest-xdist
- ✅ **Page Object Model** - Clean separation of test logic and UI interactions
- ✅ **Allure Reporting** - Generate detailed test reports with allure-pytest
- ✅ **BDD Support** - Behavior-driven development with pytest-bdd
- ✅ **Test Organization** - Structured test hierarchy with smoke, regression, and flaky markers
- ✅ **Robust Locators** - Stable CSS and data-attribute selectors with fallback mechanisms

## Project Structure

```
pyTestxdist/
├── main.py                          # Entry point (placeholder)
├── pytest.ini                       # Pytest configuration
├── README.md                        # This file
├── INSTRUCTIONS.md                  # Detailed usage guide
├── ARCHITECTURE.md                  # Technical architecture
├── data/
│   └── test_data.json              # Test data (search terms, options)
├── pages/
│   └── amazon_search_page.py        # Page Object Model for Amazon
├── tests/
│   ├── test_search_iphone.py       # Main test cases
│   ├── features/
│   │   └── search_iphone.feature   # BDD feature file
│   ├── steps/
│   │   └── search_steps.py         # BDD step definitions
│   └── flaky/
│       └── test_sort_price_flaky.py # Flaky test examples
├── utils/
│   └── browser_factory.py          # Playwright browser setup
├── mcp/
│   └── context.yaml                # MCP configuration
└── allure-results/                 # Allure test reports (generated)
```

## Technology Stack

| Component | Version | Purpose |
|-----------|---------|---------|
| Python | 3.12.10 | Programming language |
| pytest | 8.3.2 | Test framework |
| pytest-xdist | 3.8.0 | Parallel test execution |
| Playwright | Latest | Browser automation |
| allure-pytest | 2.13.5 | Test reporting |
| pytest-bdd | 7.2.0 | BDD support |

## Prerequisites

- Python 3.12 or higher
- pip (Python package manager)
- Git

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd pyTestxdist
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install pytest==8.3.2
pip install pytest-xdist==3.8.0
pip install playwright==1.40.0
pip install allure-pytest==2.13.5
pip install pytest-bdd==7.2.0
pip install pytest-html==4.1.1
```

### 4. Install Playwright Browsers
```bash
playwright install chromium
```

## Running Tests

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test File
```bash
pytest tests/test_search_iphone.py -v
```

### Run Tests in Parallel (8 workers)
```bash
pytest tests/ -n auto
```

### Run Only Regression Tests
```bash
pytest -m regression
```

### Run Only Smoke Tests
```bash
pytest -m smoke
```

### Generate HTML Report
```bash
pytest tests/ --html=report.html --self-contained-html
```

### Generate Allure Report
```bash
pytest tests/ --alluredir=allure-results
allure serve allure-results
```

## Test Cases

### test_search_iphone.py
**Purpose:** Search for iPhones on Amazon and sort by price (low to high)

**Workflow:**
1. Open Amazon.in
2. Search for "iPhone 17 Pro Max"
3. Apply price sorting (low to high)
4. Fetch top 5 product items with name and price

**Result:** ✅ PASSED - Extracts product information successfully

## Page Object Model

### AmazonSearchPage Class
Encapsulates all Amazon search page interactions:

| Method | Description |
|--------|-------------|
| `open()` | Navigate to Amazon.in |
| `search_product(product)` | Search for a specific product |
| `sort_low_to_high()` | Sort results by ascending price |
| `fetch_items()` | Extract product names and prices |

**Locators Used:**
- Product Container: `div[data-component-type='s-search-result']`
- Product Name: `h2 a span` (primary) / `h2 span` (fallback)
- Product Price: `.a-price-whole` (primary) / `.a-price` (fallback)

## Configuration

### pytest.ini
```ini
[pytest]
addopts =
  -n auto              # Run tests in parallel
  --alluredir=allure-results  # Generate allure reports
markers =
  smoke       # Quick smoke tests
  regression  # Full regression suite
  flaky       # Known flaky tests
```

## Locator Strategy

This project uses robust locators to handle dynamic Amazon UI:

1. **Primary Locator**: `div[data-component-type='s-search-result']` - Stable data attribute
2. **Fallback Mechanism**: Multiple selector attempts with exception handling
3. **First Element Priority**: `.first` selector to handle multiple matches
4. **Graceful Degradation**: Returns "N/A" if element not found

## Troubleshooting

### Tests Timing Out
- Increase Playwright timeout in browser_factory.py
- Check network connectivity
- Verify Amazon.in is accessible

### Locators Not Found
- Run in headed mode: `headless=False` in browser_factory.py
- Use Playwright Inspector: `playwright codegen https://www.amazon.in`
- Check Amazon UI changes

### Parallel Execution Issues
- Reduce number of workers: `pytest -n 4`
- Check system resources
- Review flaky tests

## Contributing

1. Follow Page Object Model pattern
2. Add stable, maintainable locators
3. Mark tests with appropriate markers (@pytest.mark.regression, etc.)
4. Include error handling and fallbacks
5. Update test data in `data/test_data.json`

## Reports

- **Allure Reports**: View detailed test execution reports
  ```bash
  allure serve allure-results
  ```
- **HTML Reports**: Standard pytest-html reports
- **Console Output**: Verbose test execution details

## License

This project is provided as-is for testing and educational purposes.

## Support

For issues or questions, refer to INSTRUCTIONS.md or ARCHITECTURE.md for detailed guidance.
