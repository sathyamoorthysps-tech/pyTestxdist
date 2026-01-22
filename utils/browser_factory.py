import os
from playwright.sync_api import sync_playwright


def create_context():
    pw = sync_playwright().start()

    # Read environment variables for configuration
    headless = os.getenv("PW_HEADLESS", "true").lower() in ("true", "1", "yes")
    no_sandbox = os.getenv("PW_NO_SANDBOX", "false").lower() in ("true", "1", "yes")
    launch_args = ["--no-sandbox"] if no_sandbox else []

    browser = pw.chromium.launch(headless=headless, args=launch_args)

    viewport_width = int(os.getenv("PW_VIEWPORT_WIDTH", 1920))
    viewport_height = int(os.getenv("PW_VIEWPORT_HEIGHT", 1080))
    context = browser.new_context(viewport={"width": viewport_width, "height": viewport_height})

    page = context.new_page()

    timeout_ms = int(os.getenv("PW_TIMEOUT_MS", 30000))
    page.set_default_timeout(timeout_ms)
    page.set_default_navigation_timeout(timeout_ms)

    return pw, browser, context, page
