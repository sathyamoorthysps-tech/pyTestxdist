# VS Code Configuration Guide

## Setup Instructions

### Step 1: Install VS Code Extensions

Required:
- **Python** (Microsoft) - Essential for Python development
- **Pylance** (Microsoft) - Optional but recommended for IntelliSense

Optional but helpful:
- **Python Test Explorer** (Little Fox Key)
- **Better Comments** (Aaron Bond)
- **Thunder Client** or **REST Client** for API testing

### Step 2: Automatic Configuration

The following files are already configured:
- `.vscode/settings.json` - Test discovery and editor settings
- `.vscode/launch.json` - Debug configurations
- `.vscode/tasks.json` - Build and test tasks

### Step 3: Verify Setup

1. Open Command Palette (Ctrl+Shift+P)
2. Run: `Python: Select Interpreter`
3. Choose your virtual environment
4. Run: `Python: Discover Tests`

## Using Test Explorer

### Open Test Explorer

1. Click the **Test Explorer** icon in the left sidebar (beaker icon)
2. Or use Command Palette (Ctrl+Shift+P) → "Test: Focus on Test Explorer"

### Run Tests from UI

**Option 1: Run Single Test**
- Hover over test name
- Click the ▶️ (play) icon

**Option 2: Run Test File**
- Click play icon next to file name

**Option 3: Run All Tests**
- Click play icon at the top

**Option 4: Debug Test**
- Right-click test → "Debug"

### Test Filtering

- Click **Filter** icon to show/hide tests
- Search for specific tests in search box

## Debug Configurations

Available in VS Code Debug menu (Ctrl+Shift+D):

1. **Pytest: Current File** - Run current test file
2. **Pytest: All Tests** - Run entire suite
3. **Pytest: All Tests with Allure** - Generate Allure reports
4. **Pytest: Regression Tests** - Run @pytest.mark.regression only
5. **Pytest: Smoke Tests** - Run @pytest.mark.smoke only
6. **Pytest: Parallel (Auto)** - Run with all CPU cores

### Debug a Test

1. Set breakpoint in code (F9)
2. Run Debug configuration
3. Use Debug toolbar (Continue, Step Over, Step Into, etc.)

## Terminal Tasks

Available in Terminal → Run Task:

1. **Python: Pytest Current File** - Test current file
2. **Python: Pytest All Tests** - Run all tests
3. **Python: Pytest Parallel** - Parallel execution
4. **Python: Pytest with Report** - Generate Allure report
5. **Python: View Allure Report** - Open in browser

## Settings Explanation

### Test Discovery
```json
"python.testing.pytestEnabled": true
```
Enables pytest as the test framework.

### Test Arguments
```json
"python.testing.pytestArgs": ["tests", "--tb=short", "-v"]
```
- `tests` - Discover tests in tests/ folder
- `--tb=short` - Short traceback format
- `-v` - Verbose output

### File Exclusions
```json
"files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true,
    "**/.pytest_cache": true
}
```
Hide generated files from explorer.

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Shift+D` | Open Debug view |
| `F5` | Start debugging |
| `F9` | Toggle breakpoint |
| `F10` | Step over |
| `F11` | Step into |
| `Shift+F11` | Step out |
| `Ctrl+Shift+P` | Command Palette |
| `Ctrl+Shift+Y` | Debug console |

## Troubleshooting

### Tests Not Discovered

1. Ensure `python.testing.pytestEnabled` is `true`
2. Run Command Palette → "Python: Discover Tests"
3. Check test file names start with `test_`
4. Verify pytest is installed: `pip install pytest`

### Wrong Python Interpreter

1. Click Python version in bottom status bar
2. Select correct interpreter (should be in venv)
3. Run "Python: Discover Tests" again

### Test Explorer Not Showing

1. Click beaker icon in left sidebar
2. Or use Command Palette → "Test: Focus on Test Explorer"
3. Reload VS Code if necessary

### Breakpoints Not Working

1. Ensure `"justMyCode": false` in launch.json
2. Check test file is in tests/ directory
3. Verify pytest is installed

## Tips & Tricks

### Run Tests on Save
Add to `.vscode/settings.json`:
```json
"python.testing.pytestEnabled": true,
"files.autoSave": "afterDelay"
```

### Show Test Output Always
In launch.json, all configs use:
```json
"console": "integratedTerminal"
```
This shows output in VS Code terminal.

### Debug Failed Tests
1. Run test and let it fail
2. VS Code shows failure details
3. Click on stack trace to jump to code
4. Add breakpoint and re-run with debugging

### Profile Test Performance
Use built-in Python profiler:
```json
{
    "name": "Pytest with Profile",
    "type": "python",
    "request": "launch",
    "module": "pytest",
    "args": ["tests/", "-v", "--profile"]
}
```

## Next Steps

1. ✅ Reload VS Code
2. ✅ Open Test Explorer (beaker icon)
3. ✅ Click "Discover Tests"
4. ✅ Run a test from UI
5. ✅ Set breakpoint and debug

---

For more information, see [README.md](../README.md) or [INSTRUCTIONS.md](../INSTRUCTIONS.md)
