# PyTestxdist - Quick Start Guide

Get up and running with PyTestxdist in 5 minutes!

## 1️⃣ Installation (2 minutes)

```bash
# Clone repository
git clone <repository-url>
cd pyTestxdist

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install pytest==8.3.2 pytest-xdist==3.8.0 playwright==1.40.0 allure-pytest==2.13.5

# Install browser
playwright install chromium
```

## 2️⃣ Run First Test (1 minute)

```bash
# Navigate to project
cd pyTestxdist

# Run test
pytest tests/test_search_iphone.py -v
```

**Expected Output:**
```
✓ test_search_and_sort_iphone PASSED (30s)
```

## 3️⃣ View Test Report (2 minutes)

```bash
# Generate Allure report
pytest tests/ --alluredir=allure-results

# View in browser
allure serve allure-results
```

## 📋 Common Commands

| Task | Command |
|------|---------|
| Run all tests | `pytest tests/ -v` |
| Run in parallel | `pytest tests/ -n auto` |
| Run with report | `pytest tests/ --alluredir=allure-results` |
| View report | `allure serve allure-results` |
| Stop on first fail | `pytest tests/ -x` |
| Show print output | `pytest tests/ -s` |

## 🎯 Test Details

**Test:** `test_search_and_sort_iphone`
- **What it does:** Searches for iPhones on Amazon, sorts by price, and extracts product info
- **Duration:** ~30 seconds
- **Status:** ✅ PASSING

## 🔧 Troubleshooting

### Test times out
```bash
# Run in headed mode to debug
# Edit utils/browser_factory.py, change headless=True to headless=False
pytest tests/test_search_iphone.py -s
```

### pytest not found
```bash
pip install pytest
pytest --version
```

### playwright not installed
```bash
pip install playwright
playwright install chromium
```

## 📚 Learn More

- [README.md](README.md) - Full project overview
- [INSTRUCTIONS.md](INSTRUCTIONS.md) - Detailed usage guide
- [ARCHITECTURE.md](ARCHITECTURE.md) - Technical architecture

## 💡 Next Steps

1. ✅ Run the test to verify installation
2. 📖 Read INSTRUCTIONS.md for detailed usage
3. 🏗️ Review ARCHITECTURE.md to understand design
4. ✍️ Create your own test following the pattern
5. 🚀 Integrate with CI/CD pipeline

---

**Happy Testing! 🎉**
