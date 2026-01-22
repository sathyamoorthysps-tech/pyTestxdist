import os, json, pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def storage_state_path(tmp_path_factory):
    p = tmp_path_factory.mktemp("auth") / "storage.json"
    if p.exists():
        return str(p)
    # create storage state once (headless) using creds from secrets/env
    with sync_playwright().start() as pw:
        browser = pw.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        from pages.login_page import LoginPage
        lp = LoginPage(page)
        lp.open()
        lp.login(os.environ["TEST_USER"], os.environ["TEST_PASS"])
        context.storage_state(path=str(p))
        context.close()
        browser.close()
    return str(p)

@pytest.fixture
def page_with_auth(storage_state_path):
    from playwright.sync_api import sync_playwright
    pw = sync_playwright().start()
    browser = pw.chromium.launch()
    context = browser.new_context(storage_state=storage_state_path)
    page = context.new_page()
    yield page
    context.close(); browser.close(); pw.stop()

@pytest.fixture
def auth_page(request, page):
    """
    Return an authenticated page when TEST_USER/TEST_PASS are present,
    otherwise return the default `page` fixture so tests keep working locally.
    """
    if os.environ.get("TEST_USER") and os.environ.get("TEST_PASS"):
        return request.getfixturevalue("page_with_auth")
    return page