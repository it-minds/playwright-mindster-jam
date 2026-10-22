# Playwright Testing Guidelines

This project uses Playwright with Python for end-to-end testing.

## Project Structure

```
tests/
├── test_lego_homepage.py      # LEGO homepage tests
├── test_lego_product_cards.py # Product card tests  
├── test_demoqa_products.py    # DemoQA tests (working alternative)
├── test_backend_data_validation.py  # API validation tests
└── test_lego_ai_generated.py  # AI-generated example
```

## Running Tests

```bash
# All tests
pytest tests/ -v

# Specific file
pytest tests/test_lego_homepage.py -v

# Specific test
pytest tests/test_lego_homepage.py::TestLEGOHomepage::test_page_loads_successfully -v

# With browser visible
pytest tests/ --headed

# Slow motion for demos
pytest tests/ --headed --slowmo=500

# Using Docker (recommended)
docker run --rm --network host \
  -v $(pwd):/work/ \
  -w /work/ \
  mcr.microsoft.com/playwright/python:v1.64.0-jammy \
  bash -c "pip install -q -r requirements.txt && pytest tests/ -v"
```

## Test Template

```python
from playwright.sync_api import Page, expect
import pytest

class TestFeatureName:
    """Description of test coverage."""
    
    BASE_URL = "https://example.com"
    
    def test_specific_behavior(self, page: Page):
        """Clear description of what is tested."""
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        
        # Test implementation
        element = page.get_by_role("button", name="Click me")
        expect(element).to_be_visible()
```

## Selector Priority

1. `get_by_role()` - Most accessible
2. `get_by_text()` - Human readable
3. `get_by_label()` - Form fields
4. `get_by_placeholder()` - Input fields
5. `get_by_test_id()` - When data-testid available
6. CSS/XPath - Last resort only

## Common Patterns

### Waiting for Elements
```python
# Wait for page load
page.wait_for_load_state("networkidle")

# Wait for specific element
expect(page.locator("selector")).to_be_visible()

# Wait for text
expect(page.locator("selector")).to_contain_text("expected text")
```

### Form Interactions
```python
page.fill('#email', 'test@example.com')
page.select_option('#country', 'DK')
page.check('#terms')
page.click('button[type="submit"]')
```

### Assertions
```python
expect(page).to_have_title("Expected Title")
expect(page).to_have_url("/expected-path")
expect(element).to_be_visible()
expect(element).to_contain_text("expected text")
expect(element).to_have_attribute("href", "/link")
```

## Important Notes

### Bot Protection
LEGO.com uses Cloudflare bot protection. Tests will fail with "Just a moment..." page.
Use DemoQA (`https://demoqa.com`) for live demos and testing.

### Test Independence
- Each test should be independent
- No shared state between tests
- Use fixtures for common setup

### Naming Conventions
- Test classes: `TestFeatureName`
- Test methods: `test_specific_behavior`
- Files: `test_feature_name.py`