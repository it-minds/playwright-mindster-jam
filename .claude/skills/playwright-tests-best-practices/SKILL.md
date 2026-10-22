---
name: playwright-tests-best-practices
description: Team best practices and coding standards for Playwright tests
allowed-tools: Read(*) Write(*) Edit(*)
---

# Playwright Tests - Best Practices

## When to Use This Skill

Use this skill when:
- ✍️ **Writing new tests** - Apply all rules to test names and structure
- 🔍 **Reviewing existing tests** - Check against naming conventions and standards
- 📝 **Refactoring tests** - Improve test names and organization
- 🎯 **Onboarding new team members** - Share coding standards

### Automatic Triggers
The AI should automatically apply these rules when:
- Generating new test files
- Suggesting test names
- Reviewing test code quality

---

## Project Conventions

### File Naming
- Test files: `test_<feature>.py`
- Test classes: `Test<FeatureName>`
- Test methods: `test_<specific_behavior>`

### Test Structure
```python
from playwright.sync_api import Page, expect
import pytest

class TestFeatureName:
    """Description of what this test class covers."""
    
    BASE_URL = "https://example.com"
    
    def test_specific_behavior(self, page: Page):
        """Clear description of what is being tested."""
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        
        # Arrange
        # Act
        # Assert
```

---

## Naming Conventions

**Reference:** See `references/naming_functions.md` for complete guidelines.

### Core Rules
1. All test methods must start with `test_should_`
2. Include the trigger event (when/after)
3. Use business language, not technical terms
4. Describe visible behavior from user perspective

### Examples
```python
# ✅ Good
def test_should_add_item_to_cart_when_add_button_clicked(self, page: Page):
    """Verify item is added when user clicks add button."""
    ...

def test_should_display_error_message_when_validation_fails(self, page: Page):
    """Verify error shown for invalid input."""
    ...

# ❌ Bad
def test_add_item(self, page: Page):  # Missing "should" and trigger
def test_validation(self, page: Page):  # Too vague
```

### When Writing Test Names
Always consult `references/naming_functions.md` for:
- 10 detailed naming rules with examples
- Python-specific naming conventions
- Complete checklist for test names

---

## Your Team Rules

### Selectors
- [ ] Use semantic locators first (`get_by_role`, `get_by_text`, `get_by_label`)
- [ ] Add data-testid attributes where needed
- [ ] Avoid XPath unless necessary

### Waits
- [ ] No hardcoded `time.sleep()` calls
- [ ] Use `wait_for_load_state("networkidle")` for page loads
- [ ] Use `expect()` for element waits

### Assertions
- [ ] Use Playwright `expect()` only
- [ ] Add custom error messages
- [ ] Test both positive and negative cases

### Code Quality
- [ ] DRY - extract common patterns
- [ ] Meaningful test names
- [ ] Docstrings on all tests
- [ ] No hardcoded values (use fixtures)

---

## Common Patterns

### Page Object Model
```python
class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.email_input = page.get_by_label("Email")
        self.password_input = page.get_by_label("Password")
        self.submit_button = page.get_by_role("button", name="Sign In")
    
    def goto(self):
        self.page.goto(f"{BASE_URL}/login")
    
    def login(self, email: str, password: str):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()
```

### Fixtures
```python
@pytest.fixture
def logged_in_page(page: Page) -> Page:
    """Fixture that logs in before each test."""
    page.goto(f"{BASE_URL}/login")
    page.get_by_label("Email").fill("test@example.com")
    page.get_by_label("Password").fill("password123")
    page.get_by_role("button", name="Sign In").click()
    page.wait_for_load_state("networkidle")
    return page
```

### API Interception
```python
def test_api_response(page: Page):
    """Test that UI matches API response."""
    def intercept_api(route):
        response = route.fetch()
        # Inspect or modify response
        route.fulfill(response=response)
    
    page.route("**/api/**", intercept_api)
```

---

## Checklist for Reviews

### Test Naming (from references/naming_functions.md)
- [ ] All tests start with `test_should_`
- [ ] Trigger event included (when/after)
- [ ] Business language used (not technical)
- [ ] Visible behavior described
- [ ] Name is specific enough for debugging

### Code Quality
- [ ] Tests are independent (no shared state)
- [ ] Tests are idempotent (can run multiple times)
- [ ] Proper waits (no time.sleep)
- [ ] Semantic selectors used
- [ ] Meaningful assertions
- [ ] Error messages are clear
- [ ] Edge cases covered
- [ ] No hardcoded credentials/URLs

---

## Resources

- **Naming Conventions:** `references/naming_functions.md`
- [Playwright Python Docs](https://playwright.dev/python/docs/intro)
- [Playwright Assertions](https://playwright.dev/python/docs/assertions)
- [Pytest Fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html)