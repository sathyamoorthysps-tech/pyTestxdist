import json
import pytest
import os
from playwright.sync_api import sync_playwright
from pages.amazon_search_page import AmazonSearchPage

# Load MCP context loader from the run_mcp script
from scripts.run_mcp import load_context


@pytest.mark.regression
@pytest.mark.mcp
def test_search_and_sort_iphone_mcp():
    # Load test data
    with open("data/test_data.json") as f:
        data = json.load(f)

    # Load MCP context (falls back to simple parser if PyYAML not present)
    ctx = load_context()
    pw_cfg = ctx.get("playwright", {})

    headless = bool(pw_cfg.get("headless", True))
    no_sandbox = bool(pw_cfg.get("no_sandbox", False))
    args = pw_cfg.get("args") or ([] if not no_sandbox else ["--no-sandbox"]) 
    # Ensure args is a Python list for Playwright.launch; the MCP context may store it as a JSON string
    if isinstance(args, str):
        try:
            args = json.loads(args)
        except Exception:
            args = [args]

    viewport = pw_cfg.get("viewport", {})
    vw = int(viewport.get("width", 1920))
    vh = int(viewport.get("height", 1080))

    timeout_ms = int(pw_cfg.get("timeout_ms", 30000))

    results_dir = pw_cfg.get("results_dir") or os.getenv("PW_RESULTS_DIR") or "allure-results/mcp"

    # Run Playwright using MCP configuration (synchronous API)
    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=headless, args=args)
    context = browser.new_context(viewport={"width": vw, "height": vh})
    page = context.new_page()

    page.set_default_timeout(timeout_ms)
    page.set_default_navigation_timeout(timeout_ms)

    try:
        amazon = AmazonSearchPage(page)

        amazon.open()
        amazon.search_product(data["search_term"])
        amazon.sort_low_to_high()

        items = amazon.fetch_items()

        # Minimal assertions: at least one item with price should be found
        assert isinstance(items, list) and len(items) > 0, "No items found on search results"
        assert any(item.get("price") for item in items), "No item had a price"

        # Write a small artifact for debugging (optional)
        os.makedirs(results_dir, exist_ok=True)
        with open(os.path.join(results_dir, "mcp_test_search_iphone_results.json"), "w", encoding="utf-8") as out:
            json.dump(items, out, indent=2)

    finally:
        context.close()
        browser.close()
        pw.stop()
