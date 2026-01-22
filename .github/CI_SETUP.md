# PyTestxdist - GitHub Actions CI/CD Setup

## Overview

Your project now has automated CI/CD pipelines using GitHub Actions. Tests run automatically on:
- **Push** to main/develop branches
- **Pull Requests** to main/develop branches
- **Daily schedule** at 2 AM UTC

## Workflows

### 1. **tests.yml** - Main Test Pipeline

**Runs on:** Push, PR, and daily schedule

**What it does:**
- Tests on 3 OS: Ubuntu, Windows, macOS
- Tests on 2 Python versions: 3.11, 3.12
- Total: 6 test combinations
- Generates Allure reports
- Generates coverage reports
- Uploads artifacts

**Key Features:**
```yaml
- Parallel test matrix (6 combinations)
- Dependency caching for faster builds
- Test results upload (30 days retention)
- PR comments with test status
- Coverage reporting to Codecov
- Failure notifications
```

### 2. **quality.yml** - Code Quality Pipeline

**Runs on:** Push and PR

**What it does:**
- Security checks (Bandit)
- Dependency vulnerability check (Safety)
- Code complexity analysis (Radon)
- Maintainability index calculation
- Dependency freshness check (pip-audit)

## GitHub Secrets & Variables

### Required Secrets (Setup in GitHub)

1. **SLACK_WEBHOOK** (Optional)
   - For Slack notifications on failure
   - Get from: https://api.slack.com/messaging/webhooks
   - Set in: Settings → Secrets and variables → Actions → New repository secret

### Optional Variables

```
SLACK_WEBHOOK=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

## Initial Setup (First Time)

### Step 1: Push to GitHub

```bash
git remote add origin https://github.com/your-username/pyTestxdist.git
git branch -M main
git push -u origin main
```

### Step 2: Enable Actions

1. Go to: https://github.com/your-username/pyTestxdist
2. Click **Actions** tab
3. Click **"I understand my workflows, go ahead and enable them"**

### Step 3: Add Secrets (Optional)

1. Go to: Settings → Secrets and variables → Actions
2. Click **New repository secret**
3. Name: `SLACK_WEBHOOK`
4. Value: Your Slack webhook URL

### Step 4: Verify Workflows

1. Go to **Actions** tab
2. You should see workflow runs
3. Click on run to see details

## Workflow Details

### Test Workflow

**Status checks on PR:**
```
✅ All tests passed
✅ Coverage report generated
✅ Artifacts uploaded
```

**Test matrix:**
```
OS: [ubuntu-latest, windows-latest, macos-latest]
Python: [3.11, 3.12]

Combinations:
├─ ubuntu-latest + 3.11
├─ ubuntu-latest + 3.12
├─ windows-latest + 3.11
├─ windows-latest + 3.12
├─ macos-latest + 3.11
└─ macos-latest + 3.12
```

**Each test run:**
1. Checks out code
2. Sets up Python
3. Installs dependencies
4. Installs Playwright
5. Runs tests with Allure
6. Uploads results (30 days)
7. Uploads cache (7 days)
8. Comments on PR with results

### Coverage Workflow

**Steps:**
1. Runs pytest with coverage
2. Generates HTML report
3. Uploads to Codecov
4. Uploads HTML report as artifact

**Coverage threshold:** 0% (can be increased)

### Linting Workflow

**Tools:**
- **Black** - Code formatter check
- **Flake8** - PEP8 linter
- **Pylint** - Code quality (min score 7.0)

## GitHub Actions Files

### `.github/workflows/tests.yml`
Main test pipeline with:
- Matrix strategy (6 OS/Python combinations)
- Allure reporting
- Coverage calculation
- Codecov integration
- PR comments
- Slack notifications

### `.github/workflows/quality.yml`
Code quality pipeline with:
- Security scanning (Bandit)
- Dependency auditing
- Complexity analysis
- Maintainability metrics

## Artifacts Generated

### Test Workflow Artifacts

```
allure-results-ubuntu-latest-py3.11/    (30 days)
allure-results-ubuntu-latest-py3.12/    (30 days)
allure-results-windows-latest-py3.11/   (30 days)
... (6 total)
pytest-cache-*/                         (7 days)
coverage-report/                        (30 days)
security-report.json                    (30 days)
```

### Accessing Artifacts

1. Go to **Actions** → workflow run
2. Scroll to **Artifacts** section
3. Click to download

## Build Status Badge

Add to README.md:

```markdown
[![PyTestxdist Tests](https://github.com/YOUR-USERNAME/pyTestxdist/actions/workflows/tests.yml/badge.svg)](https://github.com/YOUR-USERNAME/pyTestxdist/actions)

[![Code Quality](https://github.com/YOUR-USERNAME/pyTestxdist/actions/workflows/quality.yml/badge.svg)](https://github.com/YOUR-USERNAME/pyTestxdist/actions)
```

## PR Status Checks

When you create a pull request:

```
✅ All checks passed
├─ tests.yml - Matrix tests (ubuntu-latest + python-3.11)
├─ tests.yml - Matrix tests (ubuntu-latest + python-3.12)
├─ tests.yml - Matrix tests (windows-latest + python-3.11)
├─ tests.yml - Matrix tests (windows-latest + python-3.12)
├─ tests.yml - Matrix tests (macos-latest + python-3.11)
├─ tests.yml - Matrix tests (macos-latest + python-3.12)
├─ tests.yml - Coverage
├─ tests.yml - Lint
├─ quality.yml - Security
├─ quality.yml - Code Quality
└─ quality.yml - Dependency Check
```

## Environment Variables in CI

Available in workflow:

```yaml
GITHUB_REPOSITORY      # owner/repo
GITHUB_SHA            # Commit SHA
GITHUB_REF            # Branch/tag ref
GITHUB_ACTOR          # User who triggered
GITHUB_RUN_ID         # Workflow run ID
GITHUB_WORKSPACE      # Working directory
```

## Running Tests Locally (Same as CI)

Simulate CI environment:

```bash
# Test on multiple Python versions
python3.11 -m pytest tests/ -v
python3.12 -m pytest tests/ -v

# With coverage
pytest tests/ --cov=pages --cov=utils

# With Allure
pytest tests/ --alluredir=allure-results
```

## Customization

### Change Test Triggers

Edit `.github/workflows/tests.yml`:

```yaml
on:
  push:
    branches: [main]           # Add/remove branches
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 2 * * *'        # Change time
```

### Change Python Versions

```yaml
strategy:
  matrix:
    python-version: ['3.11', '3.12']  # Add/remove versions
```

### Change OS Matrix

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
```

### Skip Workflow for Specific Commits

Add `[skip ci]` to commit message:

```bash
git commit -m "Update docs [skip ci]"
```

## Monitoring

### View Workflow Status

1. Go to **Actions** tab
2. Click workflow name
3. See all runs
4. Click run for details

### Failed Run Details

1. Click failed run
2. Click failed job
3. See error logs
4. Review stack trace

### Real-time Logs

Logs update in real-time while workflow runs.

## Cost Considerations

GitHub Actions free tier includes:
- 2,000 minutes/month
- Unlimited public repos
- Shared runners

Current usage estimate:
- ~5 minutes per test run
- 6 matrix combinations = ~30 minutes/run
- Estimated: 600 minutes/month

## Optimization Tips

### Speed Up Builds

```yaml
# Use cache
- uses: actions/setup-python@v4
  with:
    cache: 'pip'

# Minimize matrix
os: [ubuntu-latest]  # Instead of 3 OS
python-version: ['3.12']  # Latest only
```

### Reduce Artifacts

```yaml
retention-days: 7  # Instead of 30
```

### Run Only on PR

```yaml
on:
  pull_request:
    branches: [main]
```

## Troubleshooting

### Workflow not triggering

- Check `.github/workflows/` syntax (use validator)
- Ensure branch names match
- Check GitHub Actions enabled

### Tests failing in CI but passing locally

- Different Python version
- Different OS behavior
- Missing dependencies
- Path issues

### Slow builds

- Increase matrix (more parallel)
- Decrease artifact retention
- Cache dependencies

## Resources

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Recommended Workflows](https://github.com/actions)

## Next Steps

1. ✅ Push code to GitHub
2. ✅ Enable Actions
3. ✅ Add secrets (optional)
4. ✅ Create PR to trigger workflows
5. ✅ Monitor in Actions tab
6. ✅ Add status badges to README

---

For more information, see [README.md](../../README.md) or [INSTRUCTIONS.md](../../INSTRUCTIONS.md)
