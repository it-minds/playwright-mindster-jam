"""
End-to-end checkout flow test using mock LEGO server.

This test runs against a local mock server that simulates the LEGO checkout flow,
avoiding bot protection issues while testing the same user journey.

Flow:
1. Navigate to mock LEGO homepage
2. Add first product to cart
3. Go to checkout
4. Click "gå til betaling som gæst" (guest checkout)
5. Fill out guest form
6. Click "gå til betaling" (proceed to payment)
7. Verify payment page is reached
"""

from playwright.sync_api import Page, expect
import pytest
import subprocess
import time
import sys
import os

# Mock server configuration
MOCK_SERVER_PORT = 8765
MOCK_BASE_URL = f"http://localhost:{MOCK_SERVER_PORT}"


@pytest.fixture(scope="session")
def mock_server():
    """Start the mock LEGO server for the test session."""
    # Get the directory where this test file is located
    test_dir = os.path.dirname(os.path.abspath(__file__))
    mock_server_path = os.path.join(test_dir, "mock_server.py")
    
    # Start the mock server as a subprocess
    process = subprocess.Popen(
        [sys.executable, mock_server_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    
    # Wait for server to start
    time.sleep(2)
    
    # Check if server started successfully
    if process.poll() is not None:
        stdout, stderr = process.communicate()
        pytest.fail(f"Mock server failed to start: {stderr.decode()}")
    
    print(f"\n✓ Mock server started on {MOCK_BASE_URL}")
    
    yield MOCK_BASE_URL
    
    # Cleanup: stop the server
    process.terminate()
    process.wait()
    print("\n✓ Mock server stopped")


@pytest.fixture(scope="function")
def mock_page(page: Page, mock_server):
    """Provide a page fixture configured for the mock server."""
    page.mock_server_url = mock_server
    yield page


class TestMockCheckoutFlow:
    """
    End-to-end checkout flow test using mock LEGO server.
    
    This test validates the complete checkout flow without hitting
    the production LEGO.com site (avoiding bot protection).
    """
    
    BASE_URL = MOCK_BASE_URL
    
    # Test data for guest checkout
    GUEST_DATA = {
        "email": "test@example.dk",
        "first_name": "Test",
        "last_name": "Testesen",
        "address": "Testvej 123",
        "city": "København",
        "postal_code": "1000",
        "phone": "12345678",
    }
    
    def test_complete_checkout_flow_as_guest(self, mock_page: Page):
        """
        Test the complete checkout flow from homepage to payment step
        using guest checkout (no login required).
        """
        page = mock_page
        
        # Step 1: Navigate to homepage
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        
        # Verify homepage loaded
        expect(page).to_have_title("LEGO® Danmark | Hjem")
        print("\n✓ Step 1: Homepage loaded")
        
        # Step 2: Add first product to cart
        self._add_first_product_to_cart(page)
        print("✓ Step 2: Product added to cart")
        
        # Step 3: Go to checkout
        self._navigate_to_checkout(page)
        print("✓ Step 3: Navigated to checkout")
        
        # Step 4: Click "gå til betaling som gæst" (guest checkout)
        self._select_guest_checkout(page)
        print("✓ Step 4: Selected guest checkout")
        
        # Step 5: Fill out guest form
        self._fill_guest_form(page)
        print("✓ Step 5: Filled guest form")
        
        # Step 6: Click "gå til betaling" (proceed to payment)
        self._proceed_to_payment(page)
        print("✓ Step 6: Proceeded to payment")
        
        # Step 7: Verify we reached the payment step
        self._verify_payment_step(page)
        print("✓ Step 7: Payment step verified")
        
        print("\n✅ Complete checkout flow test PASSED!\n")
    
    def _add_first_product_to_cart(self, page: Page):
        """Find and add the first available product to the cart."""
        # Wait for products to load
        page.wait_for_selector(".product-card")
        
        # Get the first product
        first_product = page.locator(".product-card").first
        
        # Scroll product into view
        first_product.scroll_into_view_if_needed()
        
        # Click "Føj Til Kurv" button
        add_to_cart_button = first_product.get_by_text("Føj Til Kurv")
        add_to_cart_button.click()
        
        # Verify cart was updated
        cart_count = page.locator("#cart-count")
        expect(cart_count).to_contain_text("(1)")
    
    def _navigate_to_checkout(self, page: Page):
        """Navigate from homepage to checkout page."""
        # Click on the shopping cart link
        cart_link = page.get_by_text("Indkøbskurv")
        cart_link.click()
        
        # Wait for cart page to load
        page.wait_for_load_state("networkidle")
        
        # Verify we're on the cart page
        expect(page.locator("body")).to_contain_text("Din Indkøbskurv")
        
        # Click checkout button
        checkout_button = page.get_by_text("Gå til kassen")
        checkout_button.first.click()
        
        # Wait for checkout page to load
        page.wait_for_load_state("networkidle")
    
    def _select_guest_checkout(self, page: Page):
        """Select guest checkout option."""
        # Look for "gå til betaling som gæst" button
        guest_checkout = page.get_by_text("gå til betaling som gæst")
        expect(guest_checkout).to_be_visible()
        guest_checkout.click()
        
        # Wait for guest form to appear
        page.wait_for_load_state("networkidle")
        
        # Verify guest form is displayed
        expect(page.locator("#guest-form")).to_be_visible()
    
    def _fill_guest_form(self, page: Page):
        """Fill out the guest checkout form with test data."""
        # Fill in all required fields
        page.locator("#email").fill(self.GUEST_DATA["email"])
        page.locator("#firstName").fill(self.GUEST_DATA["first_name"])
        page.locator("#lastName").fill(self.GUEST_DATA["last_name"])
        page.locator("#address").fill(self.GUEST_DATA["address"])
        page.locator("#city").fill(self.GUEST_DATA["city"])
        page.locator("#postalCode").fill(self.GUEST_DATA["postal_code"])
        page.locator("#phone").fill(self.GUEST_DATA["phone"])
        
        # Small delay to simulate human behavior
        page.wait_for_timeout(500)
    
    def _proceed_to_payment(self, page: Page):
        """Click the button to proceed to payment."""
        # Click "gå til betaling" button
        submit_button = page.get_by_text("gå til betaling")
        submit_button.click()
        
        # Wait for navigation
        page.wait_for_load_state("networkidle")
    
    def _verify_payment_step(self, page: Page):
        """Verify we have reached the payment step."""
        # Verify we're on the payment page
        expect(page).to_have_title("Betaling - LEGO®")
        
        # Verify payment methods are displayed
        expect(page.get_by_text("Vælg betalingsmetode")).to_be_visible()
        
        # Verify payment options exist (check first one is visible)
        expect(page.locator(".payment-option").first).to_be_visible()
        
        # Verify we have multiple payment options
        assert page.locator(".payment-option").count() >= 3
        
        # Verify payment page content
        expect(page.locator("body")).to_contain_text("Kreditkort")


class TestMockCheckoutValidation:
    """Test form validation in the checkout flow."""
    
    BASE_URL = MOCK_BASE_URL
    
    def test_guest_form_validation(self, mock_page: Page):
        """Test that the guest checkout form validates required fields."""
        page = mock_page
        
        # Navigate to guest checkout
        page.goto(f"{self.BASE_URL}/checkout/guest")
        page.wait_for_load_state("networkidle")
        
        # Try to submit without filling fields
        submit_button = page.get_by_text("gå til betaling")
        submit_button.click()
        
        # Form should not submit (HTML5 validation should prevent it)
        # The email field should be focused/highlighted as invalid
        email_field = page.locator("#email")
        
        # Check that email field is still empty (form didn't submit)
        value = email_field.input_value()
        assert value == "", "Form should not submit with empty required fields"
        
        print("✓ Form validation working correctly")
    
    def test_guest_form_success(self, mock_page: Page):
        """Test successful guest form submission."""
        page = mock_page
        
        # Navigate to guest checkout
        page.goto(f"{self.BASE_URL}/checkout/guest")
        page.wait_for_load_state("networkidle")
        
        # Fill in all required fields
        page.locator("#email").fill("valid@example.dk")
        page.locator("#firstName").fill("John")
        page.locator("#lastName").fill("Doe")
        page.locator("#address").fill("Vej 1")
        page.locator("#city").fill("København")
        page.locator("#postalCode").fill("1000")
        page.locator("#phone").fill("12345678")
        
        # Submit form
        page.get_by_text("gå til betaling").click()
        page.wait_for_load_state("networkidle")
        
        # Should redirect to payment page
        expect(page).to_have_title("Betaling - LEGO®")
        
        print("✓ Form submission successful")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])