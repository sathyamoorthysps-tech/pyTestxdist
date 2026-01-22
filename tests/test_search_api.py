import json
import re
import requests
from bs4 import BeautifulSoup
import pytest


@pytest.mark.api
@pytest.mark.regression
def test_amazon_search_api_returns_results():
    """Simple HTTP-level check of Amazon search results page for the configured search term.
    - performs a GET to `https://www.amazon.in/s` with query param `k=<term>`
    - parses results to ensure at least one product title exists and one contains the search term
    """
    # read test data
    with open("data/test_data.json", encoding="utf-8") as f:
        data = json.load(f)
    term = data.get("search_term")
    assert term, "search_term not found in test data"

    url = "https://www.amazon.in/s"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    resp = requests.get(url, params={"k": term}, headers=headers, timeout=30)
    assert resp.status_code == 200, f"Unexpected status code: {resp.status_code}"

    soup = BeautifulSoup(resp.text, "html.parser")

    results = []
    for div in soup.select("div[data-component-type='s-search-result']"):
        # Title
        title_el = div.select_one("h2 a span") or div.select_one("h2 span")
        title = title_el.get_text(strip=True) if title_el else ""
        # Price (attempt)
        price_el = div.select_one(".a-price-whole") or div.select_one(".a-price")
        price = price_el.get_text(strip=True) if price_el else ""
        if title:
            results.append({"title": title, "price": price})

    assert results, "No product results found on search response"

    # Check if any title includes the search term (case-insensitive, partial match)
    term_re = re.compile(re.escape(term), re.IGNORECASE)
    assert any(term_re.search(r["title"]) for r in results), f"No product title contained the search term '{term}'"

    # Optionally assert at least one product has a price
    assert any(r["price"] for r in results), "No product contained a price in parsed results" 
