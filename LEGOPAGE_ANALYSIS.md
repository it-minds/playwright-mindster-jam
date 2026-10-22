# LEGO.com Page Analysis

This document shows what we found when analyzing the actual LEGO homepage (https://www.lego.com/da-dk) and how we derived our test selectors from it.

## Page Structure Discovery

### Product Cards

Each product card in the grid has this structure:

```html
<a href="/da-dk/product/product-name-12345">
  <img src="..." alt="Product name in Danish">
  
  <!-- Age rating -->
  18+
  
  <!-- Piece count -->
  1911
  
  <!-- Product name -->
  <h3>PlayStation™</h3>
  
  <!-- Price -->
  1299,95 kr.
  
  <!-- Action button -->
  Føj Til Kurv
  
  <!-- Badges (conditional) -->
  Ny          <!-- New -->
  Eksklusiv   <!-- Exclusive -->
  Restordre   <!-- Backorder -->
  Forudbestilling <!-- Pre-order -->
</a>
```

### Key Selectors We Used

| Element | Selector | Notes |
|---------|----------|-------|
| Product link | `a[href*="/product/"]` | All product cards link to `/product/` URLs |
| Product image | `img` inside product link | Always present |
| Product name | `h3` inside product link | Contains product title |
| Price | Text containing `"kr."` | Danish Kroner currency |
| Age rating | Text containing `"+"` | "18+", "10+", "6+", etc. |
| Add to Cart | `get_by_text("Føj Til Kurv")` | Danish for "Add to Cart" |
| Cart link | `get_by_role("link", name="Indkøbskurv")` | Shows cart count |
| New badge | `get_by_text("Ny")` | Conditional |
| Exclusive badge | `get_by_text("Eksklusiv")` | Conditional |

### Navigation Structure

```
Header:
- LEGO Logo (link to home)
- Navigation: Shop, Se mere, Hjælp, Nyheder
- Sign up / Login
- Cart (shows item count)

Main Content:
- Hero banner (featured product)
- Category navigation (Nyheder, Gaveidéer, Tema, etc.)
- Product grid ("Find the perfect set")
  - Multiple product cards
- Additional sections (See what others build, etc.)
- LEGO Insiders promotion

Footer:
- Links organized by category
- Social media links
- Legal information
```

## Test Coverage

### What We Test

1. **Page Load** (`test_lego_homepage.py`)
   - Page title
   - URL
   - Logo visibility
   - Navigation existence

2. **Product Cards** (`test_lego_product_cards.py`)
   - Card structure (image, name, price, age, piece count)
   - Badges (New, Exclusive, Backorder, Pre-order)
   - Add to cart button functionality
   - Like/wishlist button
   - Navigation to product detail page
   - Hover states
   - Responsive behavior

3. **AI-Generated Example** (`test_lego_ai_generated.py`)
   - Shows what AI might generate
   - Used for discussion about code quality

### What We DON'T Test (and Why)

1. **Actual checkout process** - Requires real payment info
2. **User login** - Requires credentials, 2FA
3. **Search functionality** - Complex, may have rate limiting
4. **Account management** - Requires authentication
5. **Order history** - Requires authenticated session

## Danish Language Elements

Since we're testing the Danish site (`/da-dk`), all text is in Danish:

| Danish | English |
|--------|---------|
| Føj Til Kurv | Add to Cart |
| Indkøbskurv | Shopping Cart |
| Ny | New |
| Eksklusiv | Exclusive |
| Restordre | Backorder |
| Forudbestilling | Pre-order |
| Log ind | Log in |
| Søg | Search |
| Alder | Age |
| Temaer | Themes |

## Potential Test Flakiness

### Issues We Might Encounter

1. **Dynamic Content Loading**
   - Products load asynchronously
   - Solution: `page.wait_for_load_state("networkidle")`

2. **Stock Changes**
   - Products may go in/out of stock
   - Badges change based on availability
   - Solution: Make tests flexible about badge presence

3. **Rotating Featured Products**
   - Homepage hero changes regularly
   - Solution: Test structure, not specific products

4. **A/B Testing**
   - LEGO may test different layouts
   - Solution: Use flexible selectors

5. **Rate Limiting**
   - Too many requests may trigger blocking
   - Solution: Add delays between test runs in development

## Recommendations for Your Tests

1. **Use semantic locators** when possible:
   ```python
   page.get_by_role("link", name="Indkøbskurv")
   page.get_by_text("Føj Til Kurv")
   ```

2. **Wait for network idle** on e-commerce sites:
   ```python
   page.wait_for_load_state("networkidle")
   ```

3. **Be flexible with conditional elements**:
   ```python
   if badge.count() > 0:
       expect(badge).to_be_visible()
   ```

4. **Test the structure, not specific products**:
   ```python
   # Good - tests any product
   product_cards = page.locator('a[href*="/product/"]')
   expect(product_cards.first).to_be_visible()
   
   # Bad - tests specific product that might change
   expect(page.get_by_text("PlayStation")).to_be_visible()
   ```

5. **Verify cart updates** after adding items:
   ```python
   initial_text = cart_link.inner_text()
   add_to_cart.click()
   updated_text = cart_link.inner_text()
   assert initial_text != updated_text
   ```