````pip-requirements
# PyTestxdist - Requirements

## Production Dependencies

```
pytest==8.3.2
pytest-xdist==3.8.0
playwright==1.40.0
allure-pytest==2.13.5
pytest-bdd==7.2.0
pytest-html==4.1.1
pytest-metadata==3.1.1
pytest-base-url==2.1.0
```

## Development Dependencies

```
# Testing
pytest==8.3.2
pytest-xdist==3.8.0
pytest-cov==4.1.0
pytest-timeout==2.1.0
allure-pytest==2.13.5

# Browser Automation
playwright==1.40.0

# BDD
pytest-bdd==7.2.0

# Reporting
pytest-html==4.1.1
pytest-metadata==3.1.1
allure-behave==2.13.5

# Code Quality
pylint==3.0.0
flake8==6.1.0
black==23.12.0
bandit==1.7.5
safety==2.3.5
pip-audit==2.6.1

# Code Analysis
radon==6.0.1
coverage==7.3.2

# Utilities
python-dotenv==1.0.0
requests==2.31.0
```

## Installation

### Quick Install

```bash
pip install -r requirements.txt
```

### Development Install

```bash
pip install -r requirements-dev.txt
```

### From Individual Groups

```bash
# Core testing
pip install pytest==8.3.2 pytest-xdist==3.8.0 playwright==1.40.0

# Reporting
pip install allure-pytest==2.13.5 pytest-html==4.1.1

# Code quality
pip install pylint flake8 black bandit
```

## Environment Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 2. Upgrade pip

```bash
python -m pip install --upgrade pip
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Install Playwright Browsers

```bash
playwright install chromium
```

### 5. Verify Installation

```bash
pytest --version
playwright --version
python -c "import allure_pytest; print('OK')"
```

## Version Constraints

### Python Versions

- Minimum: 3.11
- Tested: 3.11, 3.12
- Recommended: 3.12.10 (current)

### Browser Support

- Chromium: Latest
- Firefox: Optional (playwright install firefox)
- Safari: macOS only (playwright install webkit)

### OS Support

- Linux (Ubuntu, Debian, CentOS)
- Windows 10/11
- macOS 10.15+

## Optional Dependencies

### For Video Recording

```bash
pip install playwright-video
```

### For Performance Analysis

```bash
pip install pytest-benchmark
```

### For Mock Servers

```bash
pip install responses
```

### For Database Testing

```bash
pip install pytest-postgresql
```

## Dependency Updates

### Check Outdated Packages

```bash
pip list --outdated
pip-audit
```

### Update All Packages

```bash
pip install --upgrade -r requirements.txt
```

### Update Specific Package

```bash
pip install --upgrade pytest
```

## Troubleshooting

### pip SSL Error

```bash
pip install --trusted-host pypi.python.org -r requirements.txt
```

### Playwright Installation Issues

```bash
# Verbose installation
playwright install chromium --with-deps

# For Linux missing dependencies
sudo apt-get install -y libgconf-2-4 libdbus-1-3
```
````