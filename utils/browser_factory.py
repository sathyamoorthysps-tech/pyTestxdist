from playwright.sync_api import sync_playwright

def create_context():
    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    return pw, browser, context, page
