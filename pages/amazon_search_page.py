class AmazonSearchPage:

    def __init__(self, page):
        self.page = page

    def open(self):
        self.page.goto("https://www.amazon.in")

    def search_product(self, product):
        self.page.fill("#twotabsearchtextbox", product)
        self.page.click("#nav-search-submit-button")
        # Wait for search results to appear
        try:
            self.page.wait_for_selector("div[data-component-type='s-search-result']", timeout=10000)
        except Exception:
            # fallback to networkidle in case selector doesn't appear quickly
            try:
                self.page.wait_for_load_state("networkidle", timeout=10000)
            except Exception:
                pass

    def sort_low_to_high(self):
        self.page.select_option("select#s-result-sort-select", "price-asc-rank")
        try:
            self.page.wait_for_selector("div[data-component-type='s-search-result']", timeout=10000)
        except Exception:
            try:
                self.page.wait_for_load_state("networkidle", timeout=10000)
            except Exception:
                pass

    def fetch_items(self):
        items = []
        results = self.page.locator("div[data-component-type='s-search-result']")
        try:
            results_count = results.count()
        except Exception:
            results_count = 0
        for i in range(min(5, results_count)):
            try:
                name = results.nth(i).locator("h2 a span").inner_text()
            except:
                try:
                    name = results.nth(i).locator("h2").locator("span").first.inner_text()
                except:
                    name = "N/A"
            try:
                price = results.nth(i).locator(".a-price-whole").inner_text()
            except:
                try:
                    price = results.nth(i).locator(".a-price").inner_text()
                except:
                    price = "N/A"
            items.append({"name": name, "price": price})
        return items
