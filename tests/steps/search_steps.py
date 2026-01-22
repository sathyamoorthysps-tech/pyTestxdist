from pytest_bdd import given, when, then
from pages.amazon_search_page import AmazonSearchPage

@given("user is on Amazon homepage")
def open_amazon(auth_page):
    AmazonSearchPage(auth_page).open()

@when('user searches for "iPhone 17 Pro Max"')
def search(auth_page):
    AmazonSearchPage(auth_page).search_product("iPhone 17 Pro Max")

@when("user sorts results by low to high price")
def sort(auth_page):
    AmazonSearchPage(auth_page).sort_low_to_high()

@then("user should see product names with prices")
def validate(auth_page):
    items = AmazonSearchPage(auth_page).fetch_items()
    assert len(items) > 0
