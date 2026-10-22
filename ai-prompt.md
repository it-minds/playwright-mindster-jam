# AI Prompt for Generating Playwright Tests

Use this prompt template when asking an AI to write Playwright tests for a page.

---

## Prompt Template

```
I want you to write Playwright tests using Python for the following page:

URL: [INSERT URL HERE]

Please write pytest-style tests using Playwright's sync API. Follow these guidelines:

1. Use the `page` fixture from pytest-playwright
2. Use `expect()` assertions from `playwright.sync_api`
3. Test the most important user flows and functionality on the page
4. Use semantic locators (get_by_role, get_by_text, get_by_label) instead of CSS selectors when possible
5. Include tests for:
   - Page loads correctly
   - Key elements are visible
   - Interactive elements work (buttons, links, forms)
   - Error states or edge cases if applicable

6. Follow Playwright best practices:
   - Use descriptive test names
   - Keep tests independent
   - Use proper waiting (avoid hardcoded sleeps)

Here's an example of the style I want:

```python
from playwright.sync_api import Page, expect

def test_example(page: Page):
    page.goto("https://example.com")
    expect(page).to_have_title("Example Domain")
    
    heading = page.locator("h1")
    expect(heading).to_be_visible()
    expect(heading).to_contain_text("Example")
```

Please generate 3-5 comprehensive tests for the page.
```

---

## LEGO-Specific Example

Here's the exact prompt I used for testing the LEGO homepage:

```
I want you to write Playwright tests using Python for the following page:

URL: https://www.lego.com/da-dk

This is the LEGO Denmark homepage. It's an e-commerce site selling LEGO sets.

Please write pytest-style tests using Playwright's sync API. Follow these guidelines:

1. Use the `page` fixture from pytest-playwright
2. Use `expect()` assertions from `playwright.sync_api`
3. Test the most important elements on the homepage:
   - Page loads correctly with correct title
   - LEGO logo is visible
   - Navigation menu exists
   - Search functionality is accessible
   - Age categories are visible (0-12 måneder, 1½-3 år, etc.)
   - Theme categories (City, Star Wars, etc.)
   - Footer with links
   - Shopping cart and login buttons

4. Use semantic locators (get_by_role, get_by_text, get_by_label) instead of CSS selectors when possible

5. Include at least one responsive test with mobile viewport

6. Follow Playwright best practices:
   - Use descriptive test names
   - Keep tests independent
   - Use proper waiting (avoid hardcoded sleeps)
   - Organize tests in logical classes

Please generate 8-12 comprehensive tests for the homepage.
```

---

## Follow-up Prompts for Refinement

After getting initial results, use these prompts to refine:

### Make tests less explicit
```
The tests are too explicit/verbose. Please make them more concise while keeping them readable. Combine related assertions where appropriate.
```

### Match your coding style
```
Please rewrite these tests to match my preferred style:
- Use shorter variable names where context is clear
- Group related assertions together
- Use page-level methods instead of locators when possible
- [Add your specific preferences here]
```

### Improve test coverage
```
Add more tests that cover:
- Edge cases (empty states, error handling)
- Different user interactions
- Responsive behavior at different viewport sizes
```

### Fix flaky tests
```
Some of these tests might be flaky due to timing issues. Please add proper waiting mechanisms using Playwright's auto-wait features instead of hardcoded delays.
```

---

## Product Card Testing Patterns

When testing e-commerce product cards, include these elements:

```
For product card testing, make sure to test:

1. **Product Information**
   - Product name/title
   - Price (with currency)
   - Age rating (e.g., "18+", "10+")
   - Piece count or product code

2. **Interactive Elements**
   - "Add to Cart" button (verify it's clickable and updates cart)
   - Like/Wishlist button (heart icon)
   - Product link (navigates to detail page)

3. **Badges and Labels**
   - "New" badge
   - "Exclusive" badge
   - "Backorder" or "Pre-order" badges
   - Sale/discount badges

4. **Visual Elements**
   - Product image (visible, has alt text)
   - Hover states
   - Responsive behavior

5. **Cart Functionality**
   - Cart count updates after adding
   - Cart icon/button is accessible

Example test structure:
```python
def test_product_card_has_all_elements(self, page: Page):
    page.goto("https://example.com")
    page.wait_for_load_state("networkidle")
    
    # Find product card
    product_card = page.locator('a[href*="/product/"]').first
    
    # Verify image
    expect(product_card.locator("img")).to_be_visible()
    
    # Verify name
    expect(product_card.locator("h3")).to_be_visible()
    
    # Verify price
    expect(product_card).to_contain_text("kr.")
    
    # Verify add to cart button
    add_to_cart = product_card.get_by_text("Add to Cart")
    expect(add_to_cart).to_be_visible()
    expect(add_to_cart).to_be_enabled()
```
```