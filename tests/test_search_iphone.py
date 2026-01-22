import json
import pytest
from pages.amazon_search_page import AmazonSearchPage
from utils.browser_factory import create_context

@pytest.mark.regression
def test_search_and_sort_iphone():
    with open("data/test_data.json") as f:
        data = json.load(f)

    pw, browser, context, page = create_context()
    amazon = AmazonSearchPage(page)

    amazon.open()
    amazon.search_product(data["search_term"])
    amazon.sort_low_to_high()

    items = amazon.fetch_items()

    for item in items:
        print(item["name"], item["price"])

    context.close()
    browser.close()
    pw.stop()
