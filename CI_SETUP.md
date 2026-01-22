# CI/CD Configuration Guide

## What's Configured

Your project now has complete GitHub Actions CI/CD with:

### 1. ✅ Automated Testing Pipeline
- **tests.yml** - Runs on push, PR, and daily schedule
- Tests on 6 combinations (3 OS × 2 Python versions)
- Generates Allure and coverage reports
- Posts results to pull requests

### 2. ✅ Code Quality Checks
- **quality.yml** - Security, linting, dependency checks
- Bandit security scanning
- Code complexity analysis
- Dependency vulnerability checking

### 3. ✅ Dependency Management
- **requirements.txt** - Production dependencies
- **requirements-dev.txt** - Development dependencies

## Getting Started

### Step 1: Prepare Your Repository

```bash
cd d:\Repo\pyTestxdist

# Initialize git if not already done
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Add tests, docs, and CI/CD"

# Add GitHub remote
git remote add origin https://github.com/YOUR-USERNAME/pyTestxdist.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 2: Enable GitHub Actions

1. Go to: https://github.com/YOUR-USERNAME/pyTestxdist
2. Click **Actions** tab
3. Click **"I understand my workflows, go ahead and enable them"** (if shown)

### Step 3: Verify Workflows

1. Go to **Actions** tab
2. You should see:
   - ✅ PyTestxdist Tests
   - ✅ Code Quality

3. Click on a workflow to see details

## CI Pipelines Explained

### Pipeline 1: PyTestxdist Tests (tests.yml)

**Triggers:** Push to main/develop, PR, Daily 2 AM UTC

**Matrix Strategy:**
```
OS Versions:     [ubuntu-latest, windows-latest, macos-latest]
Python Versions: [3.11, 3.12]
Total Jobs:      6
```

**Each job:**
1. Checks out code
2. Sets up Python version
3. Installs dependencies
4. Installs Playwright browsers
5. Runs pytest with Allure
6. Uploads artifacts (30 days)
7. Comments on PR with results

**Artifacts:**
- `allure-results-*` - Test reports
- `pytest-cache-*` - Build cache
- `coverage-report` - Code coverage

**PR Comments:**
```
## Test Results for Python 3.12 on ubuntu-latest
- Status: success
- Tests: 1
- View Results: [Link to artifacts]
```

### Pipeline 2: Code Quality (quality.yml)

**Triggers:** Push to main/develop, PR

**Checks:**
1. **Security Scanning** (Bandit)
   - Finds security issues in code
   - Reports on artifact

2. **Dependency Auditing** (Safety, pip-audit)
   - Finds vulnerable dependencies
   - Checks for outdated packages

3. **Code Complexity** (Radon)
   - Measures complexity
   - Calculates maintainability index

**Artifacts:**
- `security-report.json` - Security findings

## File Structure

```
.github/
├── workflows/
│   ├── tests.yml          # Main test pipeline
│   └── quality.yml        # Code quality pipeline
└── CI_SETUP.md            # This file

requirements.txt           # Production dependencies
requirements-dev.txt       # Development dependencies
```

## Managing Secrets

### For Slack Notifications (Optional)

1. Go to: **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `SLACK_WEBHOOK`
4. Value: `https://hooks.slack.com/services/YOUR/WEBHOOK/URL`
5. Click **Add secret**

### Getting Slack Webhook

1. Go to: https://api.slack.com/apps
2. Create new app
3. Enable "Incoming Webhooks"
4. Create webhook for desired channel
5. Copy webhook URL

## Monitoring CI Status

### View Workflow Runs

1. Go to **Actions** tab
2. See all workflow runs
3. Green ✅ = Passed
4. Red ❌ = Failed
5. Yellow ⏳ = Running

### View Job Details

1. Click on workflow run
2. Click on job to see logs
3. Click on step for details
4. Use search to find errors

### PR Checks

When you create a PR:
- Workflows automatically run
- Status appears in PR
- Must pass before merge (if configured)

## Performance Optimization

### Current Setup

```
- 6 test jobs (parallel)
- ~5 minutes per job
- Total: ~10 minutes
- Estimated usage: 600 minutes/month
```

### To Speed Up

**Option 1: Reduce matrix**
```yaml
# Only test latest Python on Ubuntu
os: [ubuntu-latest]
python-version: ['3.12']
```

**Option 2: Selective testing**
```yaml
on:
  pull_request:
    paths:
      - 'tests/**'
      - 'pages/**'
```

**Option 3: Cache more aggressively**
```yaml
- uses: actions/setup-python@v4
  with:
    cache: 'pip'
```

## Customization Examples

### Run Only on Main Branch

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
```

### Skip Workflow

Add `[skip ci]` to commit message:
```bash
git commit -m "Update docs [skip ci]"
```

### Custom Python Versions

```yaml
matrix:
  python-version: ['3.9', '3.10', '3.11', '3.12']
```

### Run on Schedule

```yaml
schedule:
  - cron: '0 2 * * *'  # Daily 2 AM UTC
  - cron: '0 18 * * 0' # Weekly Sunday 6 PM UTC
```

## Troubleshooting CI

### Workflow Not Running

**Check:**
1. Branch name matches (main/develop)
2. YAML syntax valid
3. Actions enabled in repo
4. Recent push/PR created

**Fix:**
```bash
# Validate YAML
pip install yamllint
yamllint .github/workflows/tests.yml
```

### Tests Fail in CI but Pass Locally

**Reasons:**
1. Different Python version
2. Different OS behavior
3. Missing dependencies
4. Environment variables
5. Timing issues

**Debug:**
1. Check logs in GitHub Actions
2. Run same Python version locally
3. Check for OS-specific code
4. Add explicit waits

### Tests Too Slow

**Solutions:**
1. Reduce matrix (fewer combinations)
2. Run lint separately
3. Cache dependencies
4. Use faster runners (faster hardware)

### Artifacts Not Generated

**Check:**
1. Tests passed (failed tests can skip upload)
2. Correct path in upload action
3. Retention days not expired

## Access CI Reports

### Allure Report

1. Go to **Actions** → workflow run
2. Scroll to **Artifacts**
3. Download `allure-results-*`
4. Extract and run:
   ```bash
   allure serve allure-results
   ```

### Coverage Report

1. Download `coverage-report` artifact
2. Open `index.html` in browser

### Security Report

1. Download `security-report.json`
2. Review findings

## CI Status Badge

Add to README.md:

```markdown
## Status

[![Tests](https://github.com/YOUR-USERNAME/pyTestxdist/actions/workflows/tests.yml/badge.svg)](https://github.com/YOUR-USERNAME/pyTestxdist/actions/workflows/tests.yml)
[![Code Quality](https://github.com/YOUR-USERNAME/pyTestxdist/actions/workflows/quality.yml/badge.svg)](https://github.com/YOUR-USERNAME/pyTestxdist/actions/workflows/quality.yml)
```

## Advanced Configuration

### Branch Protection Rules

1. Go to **Settings** → **Branches**
2. Add rule for `main` branch
3. **Require status checks to pass**
4. Select CI workflows
5. **Dismiss stale PR approvals**
6. Save

### Dependabot Updates (Optional)

Create `.github/dependabot.yml`:

```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
```

### Build Matrix Configuration

To modify test matrix, edit `.github/workflows/tests.yml`:

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    python-version: ['3.11', '3.12']
```

## Cost & Usage

### GitHub Actions Pricing

- **Public repos:** Free (unlimited minutes)
- **Private repos:** 2,000 minutes/month free

### Current Usage Estimate

```
Tests per month:        ~30 runs
Minutes per run:        ~10 (6 jobs × 5 min)
Total estimated:        ~300 minutes/month
Status:                 ✅ Well under quota
```

## Next Steps

1. ✅ Push code to GitHub
2. ✅ Verify workflows run
3. ✅ Check PR status checks
4. ✅ Add Slack webhook (optional)
5. ✅ Add status badges
6. ✅ Configure branch protection (optional)

## Resources

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Python Setup Action](https://github.com/actions/setup-python)
- [Upload Artifacts](https://github.com/actions/upload-artifact)

---

**Your project now has professional CI/CD! 🚀**

Questions? See [README.md](../README.md) or [INSTRUCTIONS.md](../INSTRUCTIONS.md)
