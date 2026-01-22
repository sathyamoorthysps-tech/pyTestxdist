# MCP Quickstart ⚡️

This quickstart explains how to run the MCP Playwright integration tests added under `tests/mcp/`.

Prerequisites
- Python (3.11 / 3.12 recommended)
- Project requirements installed (development deps):

  ```bash
  python -m pip install --upgrade pip
  pip install -r requirements-dev.txt
  playwright install chromium
  ```

Run the full MCP suite (recommended)
- This uses `mcp/context.yaml` and the `scripts/run_mcp.py` helper to export Playwright env vars and run pytest with shards.

```bash
python scripts/run_mcp.py
```

- The command will read `mcp/context.yaml`, set PW_* env vars, and run `pytest tests/ -n <shards> --alluredir=allure-results/mcp`.
- Results are written to the path defined in `mcp/context.yaml` (default: `allure-results/mcp`).

Run a single MCP test locally
- Useful for fast iteration on the new test `tests/mcp/test_search_iphone_mcp.py`:

```bash
python -m pytest tests/mcp/test_search_iphone_mcp.py -v
```

Override runtime configuration
- You can temporarily override Playwright settings with environment variables:

```bash
# Example: run with visible browser and longer timeout
set PW_HEADLESS=false
set PW_TIMEOUT_MS=60000
python scripts/run_mcp.py
```

Or (bash):

```bash
PW_HEADLESS=false PW_TIMEOUT_MS=60000 python scripts/run_mcp.py
```

Notes
- The MCP runner respects `mcp/context.yaml` values such as `playwright.headless`, `playwright.timeout_ms`, and `execution.shards` (parallelism).
- Artifacts created by the MCP run (e.g., the JSON file created by `test_search_iphone_mcp`) are written into the `results_dir` defined in the MCP context.
- A small validator script `scripts/validate_requirements.py` is included and runs in CI to prevent malformed `requirements.txt` files from breaking CI.

Happy testing! ✅
