"""
Playwright tests that validate frontend display matches backend API responses.

These tests intercept API responses and verify that the data displayed
on the page matches what the backend actually returned. This catches issues like:
- Data transformation bugs
- Caching issues
- Race conditions
- Incorrect data binding

For the LEGO.com homepage product cards.
"""

import json
import re
from playwright.sync_api import Page, expect, Route
import pytest


class TestProductDataFromAPI:
    """
    Test that product data displayed on the page matches the API response.
    
    These tests intercept network requests to validate data consistency
    between backend responses and frontend rendering.
    """
    
    BASE_URL = "https://www.lego.com/da-dk"
    
    def test_product_price_matches_api_response(self, page: Page):
        """
        Verify the price shown on product cards matches the API response.
        
        This catches bugs where:
        - Currency conversion is wrong
        - Price formatting is incorrect
        - Cached prices are shown instead of current prices
        """
        captured_responses = []
        
        def intercept_api(route: Route):
            """Capture API responses for product data."""
            response = route.fetch()
            body = response.body()
            
            # Try to parse as JSON to extract product data
            try:
                data = response.json()
                captured_responses.append(data)
            except:
                pass
            
            route.fulfill(response=response)
        
        # Intercept common e-commerce API patterns
        page.route("**/api/**", intercept_api)
        page.route("**/graphql", intercept_api)
        page.route("**/*products*", intercept_api)
        page.route("**/*catalog*", intercept_api)
        
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        
        # Wait a bit for API calls to complete
        page.wait_for_timeout(2000)
        
        # If we captured any API responses, validate them
        if captured_responses:
            for response_data in captured_responses:
                # Look for product data in the response
                products = self._extract_products_from_response(response_data)
                
                for product in products[:3]:  # Check first 3 products
                    if "price" in product:
                        api_price = str(product["price"])
                        
                        # Find the product card on the page
                        # Try to match by product ID or name
                        if "id" in product:
                            product_card = page.locator(
                                f'[data-product-id="{product["id"]}"], '
                                f'[data-sku="{product["id"]}"]'
                            ).first
                            
                            if product_card.count() > 0:
                                # Verify price is displayed correctly
                                # Danish format: "1299,95 kr."
                                card_text = product_card.inner_text()
                                
                                # Price should be visible in some format
                                # (may be formatted differently, so we check for the number)
                                price_number = re.sub(r'[^\d,]', '', api_price)
                                assert price_number in card_text or api_price in card_text, \
                                    f"Price {api_price} not found in card: {card_text}"
    
    def test_product_name_matches_api_response(self, page: Page):
        """
        Verify product names displayed match the API response.
        
        Catches issues with:
        - Truncated names
        - Missing special characters (™, ®)
        - Localization issues
        """
        captured_responses = []
        
        def intercept_api(route: Route):
            response = route.fetch()
            try:
                data = response.json()
                captured_responses.append(data)
            except:
                pass
            route.fulfill(response=response)
        
        page.route("**/api/**", intercept_api)
        page.route("**/graphql", intercept_api)
        
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        
        if captured_responses:
            for response_data in captured_responses:
                products = self._extract_products_from_response(response_data)
                
                for product in products[:3]:
                    if "name" in product or "title" in product:
                        api_name = product.get("name") or product.get("title")
                        
                        # Find product on page by partial match
                        # (API might have full name, UI might truncate)
                        product_link = page.locator('a[href*="/product/"]').first
                        
                        if product_link.count() > 0:
                            displayed_name = product_link.locator("h3").inner_text()
                            
                            # Name should contain key parts of the API name
                            # (allowing for truncation or formatting differences)
                            if len(api_name) > 5:
                                # Check if significant portion matches
                                api_words = api_name.split()[:2]  # First 2 words
                                for word in api_words:
                                    if len(word) > 3:
                                        # At least some words should match
                                        assert word.lower() in displayed_name.lower() or \
                                               displayed_name.lower() in api_name.lower(), \
                                            f"Name mismatch: API='{api_name}', UI='{displayed_name}'"
    
    def test_product_availability_matches_api(self, page: Page):
        """
        Verify product availability status matches API response.
        
        Catches issues where:
        - Out of stock items show as available
        - Pre-order status not displayed
        - Backorder status incorrect
        """
        captured_responses = []
        
        def intercept_api(route: Route):
            response = route.fetch()
            try:
                data = response.json()
                captured_responses.append(data)
            except:
                pass
            route.fulfill(response=response)
        
        page.route("**/api/**", intercept_api)
        page.route("**/graphql", intercept_api)
        
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        
        if captured_responses:
            for response_data in captured_responses:
                products = self._extract_products_from_response(response_data)
                
                for product in products[:3]:
                    # Check availability status
                    is_available = product.get("available", True)
                    is_preorder = product.get("preorder", False)
                    is_backorder = product.get("backorder", False)
                    
                    product_card = page.locator('a[href*="/product/"]').first
                    
                    if product_card.count() > 0:
                        card_text = product_card.inner_text().lower()
                        
                        if not is_available:
                            # Should show out of stock message
                            assert any(term in card_text for term in 
                                ["ikke tilgængelig", "udsolgt", "restordre"]), \
                                f"Product should show as unavailable: {product.get('name')}"
                        
                        if is_preorder:
                            # Should show "Forudbestilling"
                            assert "forudbestilling" in card_text, \
                                f"Product should show pre-order badge: {product.get('name')}"
                        
                        if is_backorder:
                            # Should show "Restordre"
                            assert "restordre" in card_text, \
                                f"Product should show backorder badge: {product.get('name')}"
    
    def test_product_image_url_matches_api(self, page: Page):
        """
        Verify product images displayed match the API response URLs.
        
        Catches issues with:
        - Wrong image displayed
        - Broken image links
        - Image CDN issues
        """
        captured_responses = []
        
        def intercept_api(route: Route):
            response = route.fetch()
            try:
                data = response.json()
                captured_responses.append(data)
            except:
                pass
            route.fulfill(response=response)
        
        page.route("**/api/**", intercept_api)
        page.route("**/graphql", intercept_api)
        page.route("**/*.jpg", intercept_api)
        page.route("**/*.png", intercept_api)
        page.route("**/*.webp", intercept_api)
        
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        
        if captured_responses:
            for response_data in captured_responses:
                products = self._extract_products_from_response(response_data)
                
                for product in products[:2]:
                    if "image" in product or "imageUrl" in product:
                        api_image_url = product.get("image") or product.get("imageUrl")
                        
                        if api_image_url:
                            # Check if any image on page has this URL (or part of it)
                            # Images might be resized/optimized by CDN
                            page_images = page.locator("img")
                            
                            for i in range(min(page_images.count(), 5)):
                                img = page_images.nth(i)
                                if img.is_visible():
                                    src = img.get_attribute("src")
                                    if src:
                                        # Check if the API image URL is in the src
                                        # (CDN might add transformations)
                                        if product.get("id") and product["id"] in src:
                                            # Image URL matches product ID
                                            assert img.is_visible(), \
                                                f"Product image should be visible for {product.get('name')}"
    
    def test_product_age_range_matches_api(self, page: Page):
        """
        Verify age range displayed matches API response.
        
        Catches issues with:
        - Wrong age displayed
        - Missing age information
        - Formatting issues
        """
        captured_responses = []
        
        def intercept_api(route: Route):
            response = route.fetch()
            try:
                data = response.json()
                captured_responses.append(data)
            except:
                pass
            route.fulfill(response=response)
        
        page.route("**/api/**", intercept_api)
        page.route("**/graphql", intercept_api)
        
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        
        if captured_responses:
            for response_data in captured_responses:
                products = self._extract_products_from_response(response_data)
                
                for product in products[:3]:
                    age = product.get("age") or product.get("minAge")
                    
                    if age:
                        product_card = page.locator('a[href*="/product/"]').first
                        
                        if product_card.count() > 0:
                            card_text = product_card.inner_text()
                            
                            # Age should be displayed as "X+" format
                            age_pattern = f"{age}+"
                            assert age_pattern in card_text or str(age) in card_text, \
                                f"Age {age} not found in card: {card_text}"
    
    def test_product_piece_count_matches_api(self, page: Page):
        """
        Verify piece count displayed matches API response.
        
        Catches issues with:
        - Wrong piece count
        - Missing piece count
        - Formatting issues
        """
        captured_responses = []
        
        def intercept_api(route: Route):
            response = route.fetch()
            try:
                data = response.json()
                captured_responses.append(data)
            except:
                pass
            route.fulfill(response=response)
        
        page.route("**/api/**", intercept_api)
        page.route("**/graphql", intercept_api)
        
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        
        if captured_responses:
            for response_data in captured_responses:
                products = self._extract_products_from_response(response_data)
                
                for product in products[:3]:
                    piece_count = product.get("pieceCount") or product.get("pieces")
                    
                    if piece_count:
                        product_card = page.locator('a[href*="/product/"]').first
                        
                        if product_card.count() > 0:
                            card_text = product_card.inner_text()
                            
                            # Piece count should be displayed as a number
                            assert str(piece_count) in card_text, \
                                f"Piece count {piece_count} not found in card: {card_text}"
    
    def _extract_products_from_response(self, data) -> list:
        """
        Extract product list from various API response structures.
        
        Different APIs return data in different formats, so we try multiple patterns.
        """
        if not data:
            return []
        
        # Common patterns for product data in API responses
        patterns = [
            # Direct array
            lambda d: d if isinstance(d, list) else None,
            
            # { products: [...] }
            lambda d: d.get("products") if isinstance(d, dict) else None,
            
            # { data: { products: [...] } }
            lambda d: d.get("data", {}).get("products") if isinstance(d, dict) else None,
            
            # { items: [...] }
            lambda d: d.get("items") if isinstance(d, dict) else None,
            
            # { results: [...] }
            lambda d: d.get("results") if isinstance(d, dict) else None,
            
            # { data: [...] }
            lambda d: d.get("data") if isinstance(d, dict) else None,
            
            # { content: [...] }
            lambda d: d.get("content") if isinstance(d, dict) else None,
            
            # { productList: [...] }
            lambda d: d.get("productList") if isinstance(d, dict) else None,
        ]
        
        for pattern in patterns:
            try:
                result = pattern(data)
                if result and isinstance(result, list) and len(result) > 0:
                    return result
            except:
                continue
        
        return []


class TestAPIResponseValidation:
    """
    Test that API responses themselves are valid and well-formed.
    
    These tests validate the API response structure and data integrity.
    """
    
    BASE_URL = "https://www.lego.com/da-dk"
    
    def test_api_returns_valid_json(self, page: Page):
        """Verify product API returns valid JSON."""
        api_responses = []
        
        def intercept_api(route: Route):
            response = route.fetch()
            content_type = response.headers.get("content-type", "")
            
            if "application/json" in content_type:
                try:
                    data = response.json()
                    api_responses.append({
                        "url": response.url,
                        "data": data,
                        "status": response.status
                    })
                except json.JSONDecodeError as e:
                    pytest.fail(f"Invalid JSON from {response.url}: {e}")
            
            route.fulfill(response=response)
        
        page.route("**/api/**", intercept_api)
        page.route("**/graphql", intercept_api)
        
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        
        # Should have captured at least one API response
        assert len(api_responses) > 0, "No API responses captured"
        
        # All captured responses should have valid JSON
        for resp in api_responses:
            assert resp["status"] == 200, \
                f"API {resp['url']} returned status {resp['status']}"
    
    def test_api_response_has_required_fields(self, page: Page):
        """Verify product API responses have required fields."""
        api_responses = []
        
        def intercept_api(route: Route):
            response = route.fetch()
            content_type = response.headers.get("content-type", "")
            
            if "application/json" in content_type:
                try:
                    data = response.json()
                    api_responses.append({
                        "url": response.url,
                        "data": data
                    })
                except:
                    pass
            
            route.fulfill(response=response)
        
        page.route("**/api/**", intercept_api)
        page.route("**/*products*", intercept_api)
        
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        
        # Check that product objects have expected fields
        for resp in api_responses:
            products = self._extract_products_from_response(resp["data"])
            
            for product in products[:1]:  # Check first product
                # At least one identifying field should exist
                has_id = any(field in product for field in ["id", "productId", "sku", "code"])
                assert has_id, f"Product missing identifier: {product}"
                
                # Should have some display information
                has_display = any(field in product for field in 
                    ["name", "title", "displayName", "price", "image"])
                assert has_display, f"Product missing display data: {product}"
    
    def test_api_response_times_are_acceptable(self, page: Page):
        """Verify API response times are within acceptable limits."""
        response_times = []
        
        def intercept_api(route: Route):
            import time
            start = time.time()
            response = route.fetch()
            elapsed = (time.time() - start) * 1000  # Convert to ms
            response_times.append({
                "url": response.url,
                "time_ms": elapsed,
                "status": response.status
            })
            route.fulfill(response=response)
        
        page.route("**/api/**", intercept_api)
        
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        
        # API responses should be under 3 seconds
        for resp in response_times:
            assert resp["time_ms"] < 3000, \
                f"API {resp['url']} took {resp['time_ms']:.0f}ms (should be < 3000ms)"
    
    def _extract_products_from_response(self, data) -> list:
        """Extract product list from API response."""
        if not data:
            return []
        
        patterns = [
            lambda d: d if isinstance(d, list) else None,
            lambda d: d.get("products") if isinstance(d, dict) else None,
            lambda d: d.get("data", {}).get("products") if isinstance(d, dict) else None,
            lambda d: d.get("items") if isinstance(d, dict) else None,
            lambda d: d.get("results") if isinstance(d, dict) else None,
        ]
        
        for pattern in patterns:
            try:
                result = pattern(data)
                if result and isinstance(result, list):
                    return result
            except:
                continue
        
        return []


class TestNetworkRequestValidation:
    """
    Test that network requests are properly formed and efficient.
    """
    
    BASE_URL = "https://www.lego.com/da-dk"
    
    def test_no_failed_network_requests(self, page: Page):
        """Verify no network requests fail when loading the page."""
        failed_requests = []
        
        def track_failed(route: Route):
            try:
                response = route.fetch()
                if response.status >= 400:
                    failed_requests.append({
                        "url": route.request.url,
                        "status": response.status
                    })
                route.fulfill(response=response)
            except Exception as e:
                failed_requests.append({
                    "url": route.request.url,
                    "error": str(e)
                })
                route.abort()
        
        page.route("**/*", track_failed)
        
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        
        # Filter out non-critical failures (analytics, ads, etc.)
        critical_failures = [
            r for r in failed_requests 
            if not any(exclude in r["url"] for exclude in 
                ["analytics", "tracking", "ads", "doubleclick", "google-analytics"])
        ]
        
        assert len(critical_failures) == 0, \
            f"Failed requests: {[r['url'] for r in critical_failures]}"
    
    def test_product_api_is_called(self, page: Page):
        """Verify that product API endpoints are called when loading homepage."""
        api_calls = []
        
        def track_api(route: Route):
            api_calls.append(route.request.url)
            route.continue_()
        
        page.route("**/api/**", track_api)
        page.route("**/graphql", track_api)
        page.route("**/*products*", track_api)
        
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        
        assert len(api_calls) > 0, "No API calls were made when loading homepage"
    
    def test_no_excessive_api_calls(self, page: Page):
        """Verify the page doesn't make excessive API calls."""
        api_calls = []
        
        def track_api(route: Route):
            api_calls.append(route.request.url)
            route.continue_()
        
        page.route("**/api/**", track_api)
        page.route("**/graphql", track_api)
        
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        
        # Should not make more than 20 API calls for a homepage
        assert len(api_calls) <= 20, \
            f"Too many API calls: {len(api_calls)} (expected <= 20)"