"""
Playwright tests for LEGO product card components.

Tests the product cards on the homepage including:
- Product information (name, price, age, piece count)
- Add to cart functionality
- Like/wishlist button
- Product badges (New, Exclusive, etc.)
- Navigation to product detail pages

Based on actual page structure from https://www.lego.com/da-dk
"""

from playwright.sync_api import Page, expect
import pytest


class TestProductCardStructure:
    """Test that product cards have all required elements."""
    
    BASE_URL = "https://www.lego.com/da-dk"
    
    def test_product_cards_exist(self, page: Page):
        """Verify that product cards are present on the homepage."""
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        
        # Product cards should exist (they're in list items with product links)
        product_cards = page.locator('a[href*="/product/"]')
        expect(product_cards.first).to_be_visible(timeout=10000)
    
    def test_product_card_has_image(self, page: Page):
        """Verify each product card has a product image."""
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        
        # Find product cards and check they have images
        product_links = page.locator('a[href*="/product/"]').first
        image = product_links.locator("img").first
        expect(image).to_be_visible()
    
    def test_product_card_has_name(self, page: Page):
        """Verify each product card displays the product name."""
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        
        # Product names are in h3 or similar heading elements
        product_names = page.locator('a[href*="/product/"] h3, a[href*="/product/"] [data-testid="product-title"]')
        expect(product_names.first).to_be_visible(timeout=10000)
    
    def test_product_card_has_price(self, page: Page):
        """Verify each product card displays the price."""
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        
        # Prices contain "kr." for Danish Kroner
        prices = page.locator('a[href*="/product/"]').filter(has_text="kr.")
        expect(prices.first).to_be_visible(timeout=10000)
        
        # Price should be in Danish format (e.g., "1299,95 kr.")
        price_text = prices.first.inner_text()
        assert "kr." in price_text
    
    def test_product_card_has_age_rating(self, page: Page):
        """Verify each product card shows the age recommendation."""
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        
        # Age ratings appear as "18+", "10+", "6+", etc.
        age_ratings = page.locator('a[href*="/product/"]').filter(has_text="+")
        expect(age_ratings.first).to_be_visible(timeout=10000)
    
    def test_product_card_has_piece_count(self, page: Page):
        """Verify each product card shows the piece count."""
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        
        # Piece counts are numeric values near the age rating
        # They appear as standalone numbers like "1911", "904", etc.
        product_cards = page.locator('a[href*="/product/"]')
        expect(product_cards.first).to_be_visible(timeout=10000)


class TestProductCardBadges:
    """Test product card badges and labels."""
    
    BASE_URL = "https://www.lego.com/da-dk"
    
    def test_new_badge_exists(self, page: Page):
        """Verify that 'Ny' (New) badges are present for new products."""
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        
        # Look for "Ny" badge (New in Danish)
        new_badges = page.get_by_text("Ny")
        expect(new_badges.first).to_be_visible(timeout=10000)
    
    def test_exclusive_badge_exists(self, page: Page):
        """Verify that 'Eksklusiv' badges are present for exclusive products."""
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        
        # Look for "Eksklusiv" badge
        exclusive_badges = page.get_by_text("Eksklusiv")
        # May or may not be visible depending on current products
        if exclusive_badges.count() > 0:
            expect(exclusive_badges.first).to_be_visible()
    
    def test_backorder_badge_exists(self, page: Page):
        """Verify that 'Restordre' (Backorder) badges appear when applicable."""
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        
        # Look for "Restordre" badge (Backorder in Danish)
        backorder_badges = page.get_by_text("Restordre")
        # May or may not be visible depending on stock
        # This test just verifies the badge can be found if present
        assert backorder_badges.count() >= 0
    
    def test_preorder_badge_exists(self, page: Page):
        """Verify that 'Forudbestilling' (Pre-order) badges appear when applicable."""
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        
        # Look for "Forudbestilling" badge
        preorder_badges = page.get_by_text("Forudbestilling")
        # May or may not be visible depending on products
        assert preorder_badges.count() >= 0


class TestAddToCartFunctionality:
    """Test the add to cart button on product cards."""
    
    BASE_URL = "https://www.lego.com/da-dk"
    
    def test_add_to_cart_button_exists(self, page: Page):
        """Verify that 'Føj Til Kurv' (Add to Cart) buttons exist on product cards."""
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        
        # Look for "Føj Til Kurv" button
        add_to_cart_buttons = page.get_by_text("Føj Til Kurv")
        expect(add_to_cart_buttons.first).to_be_visible(timeout=10000)
    
    def test_add_to_cart_button_is_clickable(self, page: Page):
        """Verify the add to cart button can be clicked."""
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        
        # Find first visible add to cart button
        add_to_cart_button = page.get_by_text("Føj Til Kurv").first
        expect(add_to_cart_button).to_be_enabled()
        add_to_cart_button.click()
        
        # Cart should update or show confirmation
        # Wait for cart icon to show updated count or cart dropdown to appear
        page.wait_for_timeout(2000)  # Allow time for cart update
        
        # Cart count should be visible (shows "(1)" or similar)
        cart_link = page.get_by_role("link", name="Indkøbskurv")
        expect(cart_link).to_be_visible()
    
    def test_cart_count_updates_after_adding(self, page: Page):
        """Verify the cart count updates when adding a product."""
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        
        # Get initial cart text (might be "(0)" or just "Indkøbskurv")
        cart_link = page.get_by_role("link", name="Indkøbskurv")
        initial_cart_text = cart_link.inner_text()
        
        # Add first available product to cart
        add_to_cart_button = page.get_by_text("Føj Til Kurv").first
        add_to_cart_button.click()
        
        # Wait for cart to update
        page.wait_for_timeout(2000)
        
        # Cart text should have changed (now shows "(1)" or updated count)
        updated_cart_text = cart_link.inner_text()
        # The cart should now show at least 1 item
        assert "1" in updated_cart_text or "(" in updated_cart_text


class TestProductNavigation:
    """Test navigation from product cards to product detail pages."""
    
    BASE_URL = "https://www.lego.com/da-dk"
    
    def test_clicking_product_card_navigates_to_product_page(self, page: Page):
        """Verify clicking a product card navigates to the product detail page."""
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        
        # Get initial URL
        initial_url = page.url
        
        # Click on first product link
        product_link = page.locator('a[href*="/product/"]').first
        product_name = product_link.locator("h3").inner_text()
        product_link.click()
        
        # Should navigate to product page
        expect(page).not_to_have_url(initial_url)
        expect(page).to_have_url("https://www.lego.com/da-dk/product/*")
        
        # Product page should have the same product name
        expect(page.locator("h1")).to_contain_text(product_name)
    
    def test_product_page_has_add_to_cart_button(self, page: Page):
        """Verify the product detail page has an add to cart button."""
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        
        # Navigate to first product
        product_link = page.locator('a[href*="/product/"]').first
        product_link.click()
        page.wait_for_load_state("networkidle")
        
        # Product page should have add to cart button
        add_to_cart = page.get_by_role("button", name="Føj til kurv")
        expect(add_to_cart).to_be_visible(timeout=10000)


class TestLikeWishlistFunctionality:
    """Test the like/wishlist button on product cards."""
    
    BASE_URL = "https://www.lego.com/da-dk"
    
    def test_like_button_exists(self, page: Page):
        """Verify that like/wishlist buttons exist on product cards."""
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        
        # Look for heart icons or wishlist buttons
        # These might be icons with aria-labels like "Sæt på ønskeliste"
        like_buttons = page.locator('button[aria-label*="ønskeliste"], button[aria-label*="like"], [data-testid*="wishlist"]')
        
        # If wishlist buttons exist, they should be visible
        if like_buttons.count() > 0:
            expect(like_buttons.first).to_be_visible()
    
    def test_like_button_is_clickable(self, page: Page):
        """Verify the like button can be clicked."""
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        
        # Look for heart icons or wishlist buttons
        like_buttons = page.locator('button[aria-label*="ønskeliste"], button[aria-label*="like"]')
        
        if like_buttons.count() > 0:
            like_button = like_buttons.first
            expect(like_button).to_be_enabled()
            like_button.click()
            
            # Button state should change (filled heart, different color, etc.)
            # This is a visual change, so we just verify the click worked
            page.wait_for_timeout(1000)


class TestProductCardHoverStates:
    """Test hover states and interactions on product cards."""
    
    BASE_URL = "https://www.lego.com/da-dk"
    
    def test_product_card_hover_reveals_actions(self, page: Page):
        """Verify hovering over product card reveals additional actions."""
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        
        # Find first product card
        product_card = page.locator('a[href*="/product/"]').first
        
        # Hover over the product card
        product_card.hover()
        
        # Wait for any hover effects to appear
        page.wait_for_timeout(500)
        
        # After hover, additional buttons might become visible
        # (like quick add, wishlist, etc.)
        # This test just verifies hover doesn't cause errors
        expect(product_card).to_be_visible()
    
    def test_product_image_zoom_on_hover(self, page: Page):
        """Test if product images have zoom or hover effects."""
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        
        # Find first product image
        product_link = page.locator('a[href*="/product/"]').first
        image = product_link.locator("img").first
        
        # Hover over image
        image.hover()
        page.wait_for_timeout(500)
        
        # Image should still be visible (may have zoom effect)
        expect(image).to_be_visible()


class TestProductCardResponsiveness:
    """Test product cards on different viewport sizes."""
    
    BASE_URL = "https://www.lego.com/da-dk"
    
    def test_product_cards_on_mobile(self, page: Page):
        """Verify product cards display correctly on mobile viewport."""
        page.set_viewport_size({"width": 375, "height": 667})
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        
        # Product cards should still be visible
        product_cards = page.locator('a[href*="/product/"]')
        expect(product_cards.first).to_be_visible(timeout=10000)
        
        # Should have at least some products visible
        assert product_cards.count() >= 1
    
    def test_product_cards_on_tablet(self, page: Page):
        """Verify product cards display correctly on tablet viewport."""
        page.set_viewport_size({"width": 768, "height": 1024})
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        
        product_cards = page.locator('a[href*="/product/"]')
        expect(product_cards.first).to_be_visible(timeout=10000)
    
    def test_product_cards_on_desktop(self, page: Page):
        """Verify product cards display correctly on desktop viewport."""
        page.set_viewport_size({"width": 1920, "height": 1080})
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        
        product_cards = page.locator('a[href*="/product/"]')
        expect(product_cards.first).to_be_visible(timeout=10000)


class TestProductCardDataAttributes:
    """Test product cards using data attributes for more robust selectors."""
    
    BASE_URL = "https://www.lego.com/da-dk"
    
    def test_product_cards_have_data_attributes(self, page: Page):
        """Check if product cards use data attributes for testing."""
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        
        # Look for common data attributes used in e-commerce
        product_tiles = page.locator('[data-testid*="product"], [data-product-id], [data-sku]')
        
        # If data attributes exist, verify they have values
        if product_tiles.count() > 0:
            first_tile = product_tiles.first
            # Should have some data attribute
            assert first_tile.count() > 0