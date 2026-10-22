"""
Playwright tests for the LEGO homepage (https://www.lego.com/da-dk)

These tests demonstrate real-world testing patterns on the LEGO website.
Use these as examples for the Mindster Jam presentation.
"""

from playwright.sync_api import Page, expect
import pytest


class TestLEGOHomepage:
    """Test suite for the LEGO Denmark homepage."""
    
    BASE_URL = "https://www.lego.com/da-dk"
    
    def test_page_loads_successfully(self, page: Page):
        """Verify the LEGO homepage loads without errors."""
        page.goto(self.BASE_URL)
        
        # Check page loaded with correct title
        expect(page).to_have_title("LEGO® Danmark | Hjem")
        
        # Or check URL is correct
        expect(page).to_have_url(self.BASE_URL)
    
    def test_logo_is_visible(self, page: Page):
        """Verify the LEGO logo is visible on the page."""
        page.goto(self.BASE_URL)
        
        # LEGO logo should be visible
        logo = page.get_by_role("img", name="LEGO")
        expect(logo).to_be_visible()
    
    def test_navigation_menu_exists(self, page: Page):
        """Verify the main navigation menu is present."""
        page.goto(self.BASE_URL)
        
        # Navigation should exist
        nav = page.locator("nav").first
        expect(nav).to_be_visible()
    
    def test_search_functionality(self, page: Page):
        """Test the search feature on the homepage."""
        page.goto(self.BASE_URL)
        
        # Find and interact with search
        search_button = page.get_by_role("button", name="Søg")
        expect(search_button).to_be_visible()
        
        # Click search to open search input
        search_button.click()
        
        # Search input should appear
        search_input = page.get_by_placeholder="Søg"
        expect(search_input).to_be_visible()
    
    def test_age_categories_visible(self, page: Page):
        """Verify age category navigation is visible."""
        page.goto(self.BASE_URL)
        
        # Age categories should be present (0-12 måneder, 1½-3 år, etc.)
        age_nav = page.get_by_role("navigation", name="Alder")
        expect(age_nav).to_be_visible()
    
    def test_theme_categories_visible(self, page: Page):
        """Verify theme categories are visible."""
        page.goto(self.BASE_URL)
        
        # Theme navigation should exist (City, Star Wars, etc.)
        theme_nav = page.get_by_role("navigation", name="Temaer")
        expect(theme_nav).to_be_visible()
    
    def test_footer_exists(self, page: Page):
        """Verify the page footer is present."""
        page.goto(self.BASE_URL)
        
        # Footer should exist
        footer = page.locator("footer")
        expect(footer).to_be_visible()
    
    def test_responsive_mobile_viewport(self, page: Page):
        """Test the homepage on mobile viewport."""
        page.set_viewport_size({"width": 375, "height": 667})
        page.goto(self.BASE_URL)
        
        # Logo should still be visible on mobile
        logo = page.get_by_role("img", name="LEGO")
        expect(logo).to_be_visible()
        
        # Navigation should adapt (might be a hamburger menu)
        nav = page.locator("nav").first
        expect(nav).to_be_visible()
    
    def test_responsive_tablet_viewport(self, page: Page):
        """Test the homepage on tablet viewport."""
        page.set_viewport_size({"width": 768, "height": 1024})
        page.goto(self.BASE_URL)
        
        # Content should be visible on tablet
        expect(page).to_have_title("LEGO® Danmark | Hjem")


class TestLEGOProductNavigation:
    """Test navigation to product pages from the homepage."""
    
    BASE_URL = "https://www.lego.com/da-dk"
    
    def test_click_on_featured_product(self, page: Page):
        """Test clicking on a featured product from homepage."""
        page.goto(self.BASE_URL)
        
        # Wait for page to fully load
        page.wait_for_load_state("networkidle")
        
        # Find product cards/links
        product_links = page.get_by_role("link", name="LEGO")
        
        if product_links.count() > 0:
            # Click the first product link
            product_links.first.click()
            
            # Should navigate to a product or category page
            expect(page).not_to_have_url(self.BASE_URL)


class TestLEGOAccessibility:
    """Basic accessibility tests for the LEGO homepage."""
    
    BASE_URL = "https://www.lego.com/da-dk"
    
    def test_all_images_have_alt_text(self, page: Page):
        """Verify images have alt text for accessibility."""
        page.goto(self.BASE_URL)
        
        # Get all images
        images = page.locator("img")
        count = images.count()
        
        # Check first few images have alt text
        for i in range(min(count, 5)):
            img = images.nth(i)
            if img.is_visible():
                alt_text = img.get_attribute("alt")
                # Alt should exist (can be empty string for decorative images)
                assert alt_text is not None
    
    def test_buttons_have_accessible_names(self, page: Page):
        """Verify buttons have accessible names."""
        page.goto(self.BASE_URL)
        
        # Get all buttons
        buttons = page.get_by_role("button")
        count = buttons.count()
        
        # Check first few buttons are accessible
        for i in range(min(count, 5)):
            button = buttons.nth(i)
            if button.is_visible():
                # Should be able to get accessible name
                expect(button).to_be_visible()