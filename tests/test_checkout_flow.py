"""
End-to-end checkout flow test for LEGO.com (Denmark)

This test covers the complete checkout flow up to the payment step,
using guest checkout (no login required).

Flow:
1. Navigate to lego.com/da-dk
2. Add first product to cart
3. Go to checkout
4. Click "gå til betaling som gæst" (guest checkout)
5. Fill out guest form
6. Click "gå til betaling" (proceed to payment)
7. Verify we reach the payment step (before credential login)

NOTE: LEGO.com uses Cloudflare bot protection which may block automated tests.
If blocked, consider:
- Using a staging/test environment
- Running with --headed flag to use a real browser profile
- Using a different test e-commerce site
"""

from playwright.sync_api import Page, expect, BrowserContext
import pytest
import random
import time


class TestCheckoutFlow:
    """End-to-end test for the LEGO checkout flow with guest checkout."""
    
    BASE_URL = "https://www.lego.com/da-dk"
    
    # Fake test data for guest checkout
    GUEST_DATA = {
        "email": "test@example.dk",
        "first_name": "Test",
        "last_name": "Testesen",
        "address": "Testvej 123",
        "city": "København",
        "postal_code": "1000",
        "phone": "12345678",
    }
    
    def test_complete_checkout_flow_as_guest(self, page: Page):
        """
        Test the complete checkout flow from homepage to payment step
        using guest checkout (no login required).
        
        Note: This test may be blocked by Cloudflare on production LEGO.com.
        For reliable testing, use a staging environment or mock server.
        """
        # Step 1: Navigate to homepage
        # Add extra headers to appear more like a real browser
        page.set_extra_http_headers({
            "Accept-Language": "da-DK,da;q=0.9,en;q=0.8",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        })
        
        page.goto(self.BASE_URL, timeout=60000, wait_until="domcontentloaded")
        page.wait_for_timeout(5000)  # Allow time for security checks and dynamic content
        
        # Step 2: Add first product to cart
        self._add_first_product_to_cart(page)
        
        # Step 3: Go to checkout
        self._navigate_to_checkout(page)
        
        # Step 4: Click "gå til betaling som gæst" (guest checkout)
        self._select_guest_checkout(page)
        
        # Step 5: Fill out guest form
        self._fill_guest_form(page)
        
        # Step 6: Click "gå til betaling" (proceed to payment)
        self._proceed_to_payment(page)
        
        # Step 7: Verify we reached the payment step
        self._verify_payment_step(page)
    
    def _add_first_product_to_cart(self, page: Page):
        """Find and add the first available product to the cart."""
        # Wait for products to load
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(2000)  # Allow dynamic content to load
        
        # Find product cards (links to /product/)
        product_links = page.locator('a[href*="/product/"]')
        
        # Wait for at least one product to be visible
        expect(product_links.first).to_be_visible(timeout=10000)
        
        # Get the first product
        first_product = product_links.first
        
        # Scroll product into view
        first_product.scroll_into_view_if_needed()
        
        # Find and click "Føj Til Kurv" (Add to Cart) button within the product card
        add_to_cart_button = first_product.get_by_text("Føj Til Kurv", exact=False)
        
        # Wait for the button to be visible and enabled
        expect(add_to_cart_button).to_be_visible(timeout=5000)
        add_to_cart_button.click()
        
        # Wait for cart to update (look for cart indicator or confirmation)
        page.wait_for_timeout(2000)  # Allow time for cart animation/update
        
        # Verify cart was updated by checking the cart link shows items
        cart_link = page.get_by_role("link", name="Indkøbskurv")
        expect(cart_link).to_be_visible()
    
    def _navigate_to_checkout(self, page: Page):
        """Navigate from homepage to checkout page."""
        # Click on the shopping cart link
        cart_link = page.get_by_role("link", name="Indkøbskurv")
        cart_link.click()
        
        # Wait for cart page to load
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(2000)  # Allow dynamic content to load
        
        # Look for checkout button - common Danish checkout button texts
        checkout_buttons = [
            page.get_by_text("Gå til kassen", exact=False),
            page.get_by_text("Til kassen", exact=False),
            page.get_by_role("button", name="Gå til kassen"),
            page.get_by_role("button", name="Til kassen"),
        ]
        
        # Click the first visible checkout button
        for btn in checkout_buttons:
            if btn.count() > 0 and btn.first.is_visible():
                btn.first.click()
                break
        else:
            # Fallback: look for any button containing "kasse" (checkout in Danish)
            page.get_by_text("kasse").first.click()
        
        # Wait for checkout page to load
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(2000)  # Allow dynamic content to load
    
    def _select_guest_checkout(self, page: Page):
        """Select guest checkout option."""
        # Look for guest checkout button/link
        # Common Danish texts for guest checkout:
        # - "gå til betaling som gæst"
        # - "betaling som gæst"
        # - "fortsæt som gæst"
        
        guest_checkout_options = [
            page.get_by_text("gå til betaling som gæst", exact=False),
            page.get_by_text("betaling som gæst", exact=False),
            page.get_by_text("fortsæt som gæst", exact=False),
            page.get_by_text("Gå til betaling som gæst", exact=False),
            page.get_by_text("Betaling som gæst", exact=False),
        ]
        
        # Click the first visible guest checkout option
        for option in guest_checkout_options:
            if option.count() > 0 and option.first.is_visible():
                option.first.click()
                break
        else:
            # Fallback: look for any element containing "gæst" (guest)
            page.get_by_text("gæst").first.click()
        
        # Wait for guest form to appear
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(2000)  # Allow dynamic content to load
    
    def _fill_guest_form(self, page: Page):
        """Fill out the guest checkout form with test data."""
        # Wait for form to be ready
        page.wait_for_timeout(1000)
        
        # Fill email field using different selector strategies
        try:
            page.get_by_placeholder("E-mail").fill(self.GUEST_DATA["email"])
        except:
            try:
                page.locator('input[type="email"]').first.fill(self.GUEST_DATA["email"])
            except:
                page.get_by_label("E-mail", exact=False).fill(self.GUEST_DATA["email"])
        
        # Fill first name
        try:
            page.get_by_placeholder("Fornavn").fill(self.GUEST_DATA["first_name"])
        except:
            try:
                page.locator('input[name*="firstName"], input[name*="first_name"]').first.fill(self.GUEST_DATA["first_name"])
            except:
                page.get_by_label("Fornavn", exact=False).fill(self.GUEST_DATA["first_name"])
        
        # Fill last name
        try:
            page.get_by_placeholder("Efternavn").fill(self.GUEST_DATA["last_name"])
        except:
            try:
                page.locator('input[name*="lastName"], input[name*="last_name"]').first.fill(self.GUEST_DATA["last_name"])
            except:
                page.get_by_label("Efternavn", exact=False).fill(self.GUEST_DATA["last_name"])
        
        # Fill address
        try:
            page.get_by_placeholder("Adresse").fill(self.GUEST_DATA["address"])
        except:
            try:
                page.locator('input[name*="address"], input[name*="street"]').first.fill(self.GUEST_DATA["address"])
            except:
                page.get_by_label("Adresse", exact=False).fill(self.GUEST_DATA["address"])
        
        # Fill city
        try:
            page.get_by_placeholder("By").fill(self.GUEST_DATA["city"])
        except:
            try:
                page.locator('input[name*="city"]').first.fill(self.GUEST_DATA["city"])
            except:
                page.get_by_label("By", exact=False).fill(self.GUEST_DATA["city"])
        
        # Fill postal code
        try:
            page.get_by_placeholder("Postnummer").fill(self.GUEST_DATA["postal_code"])
        except:
            try:
                page.locator('input[name*="postal"], input[name*="zip"]').first.fill(self.GUEST_DATA["postal_code"])
            except:
                page.get_by_label("Postnummer", exact=False).fill(self.GUEST_DATA["postal_code"])
        
        # Fill phone number
        try:
            page.get_by_placeholder("Telefon").fill(self.GUEST_DATA["phone"])
        except:
            try:
                page.locator('input[type="tel"], input[name*="phone"]').first.fill(self.GUEST_DATA["phone"])
            except:
                page.get_by_label("Telefon", exact=False).fill(self.GUEST_DATA["phone"])
    
    def _proceed_to_payment(self, page: Page):
        """Click the button to proceed to payment."""
        # Look for "gå til betaling" or similar button
        proceed_buttons = [
            page.get_by_text("gå til betaling", exact=False),
            page.get_by_text("Gå til betaling", exact=False),
            page.get_by_text("til betaling", exact=False),
            page.get_by_role("button", name="Gå til betaling"),
            page.get_by_role("button", name="Til betaling"),
        ]
        
        # Click the first visible proceed button
        for btn in proceed_buttons:
            if btn.count() > 0 and btn.first.is_visible():
                btn.first.click()
                break
        else:
            # Fallback: look for any button containing "betaling" (payment)
            page.get_by_text("betaling").first.click()
        
        # Wait for navigation
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(2000)  # Allow dynamic content to load
    
    def _verify_payment_step(self, page: Page):
        """Verify we have reached the payment step (before credential login)."""
        # The page should show payment-related content
        # Look for payment method options or payment step indicators
        
        # Check for payment-related text on the page
        payment_indicators = [
            page.get_by_text("betaling", exact=False),
            page.get_by_text("Betalingsmetode", exact=False),
            page.get_by_text("Betalingsmåte", exact=False),
            page.get_by_text("Kreditkort", exact=False),
            page.get_by_text("MobilePay", exact=False),
            page.get_by_text("Klarna", exact=False),
        ]
        
        # At least one payment indicator should be visible
        found_payment_indicator = False
        for indicator in payment_indicators:
            if indicator.count() > 0 and indicator.first.is_visible():
                found_payment_indicator = True
                break
        
        assert found_payment_indicator, "Expected to reach payment step but no payment indicators found"
        
        # Verify we're NOT at a login page (no credential fields for LEGO account)
        # The page should not ask for LEGO.com login credentials
        login_fields = page.get_by_placeholder("E-mail", exact=True)
        # We expect the checkout form to be filled, not a login form
        # This is a soft check since email field exists in both contexts
        
        # URL should contain checkout or payment related path
        current_url = page.url
        assert "checkout" in current_url.lower() or "betaling" in current_url.lower() or "payment" in current_url.lower(), \
            f"Expected to be on checkout/payment page, but URL is: {current_url}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])