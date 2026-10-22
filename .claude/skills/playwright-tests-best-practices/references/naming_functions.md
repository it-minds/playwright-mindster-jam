## Rule 1: Always Use "should" + Verb

Every test name should start with "should" followed by an action verb.

```python
# ❌ Bad
def test_displays_error_message(self, page: Page): ...
def test_modal_visibility(self, page: Page): ...
def test_form_validation_working(self, page: Page): ...

# ✅ Good
def test_should_display_error_message_when_validation_fails(self, page: Page): ...
def test_should_show_modal_when_trigger_button_clicked(self, page: Page): ...
def test_should_validate_form_when_user_submits(self, page: Page): ...
```

**Generic Pattern:** `test_should_[verb]_[expected_outcome]`

---

## Rule 2: Include the Trigger Event

Specify what causes the behavior you're testing.

```python
# ❌ Bad
def test_should_update_counter(self, page: Page): ...
def test_should_validate_email(self, page: Page): ...
def test_should_show_dropdown(self, page: Page): ...

# ✅ Good
def test_should_increment_counter_when_plus_button_clicked(self, page: Page): ...
def test_should_show_error_when_email_format_invalid(self, page: Page): ...
def test_should_open_dropdown_when_toggle_clicked(self, page: Page): ...
```

**Generic Pattern:** `test_should_[verb]_[expected_outcome]_when_[trigger_event]`

---

## Rule 3: Group Related Tests with Descriptive Contexts

Use test class names and docstrings to create clear test hierarchies.

```python
# ❌ Bad
class TestAuthForm:
    def test_should_test_empty_state(self, page: Page): ...
    def test_should_test_invalid_state(self, page: Page): ...
    def test_should_test_success_state(self, page: Page): ...

# ✅ Good
class TestAuthForm:
    """Tests for authentication form behavior."""
    
    def test_should_disable_submit_button_when_form_empty(self, page: Page):
        """Verify submit button is disabled when no data entered."""
        ...
    
    def test_should_not_show_validation_errors_when_form_empty(self, page: Page):
        """Verify no errors shown on initial load."""
        ...
    
    def test_should_show_validation_errors_when_submitting_invalid_data(self, page: Page):
        """Verify error messages appear for invalid input."""
        ...
```

**Generic Pattern:**
```python
class Test[ComponentFeature]:
    """Tests for [feature description]."""
    
    def test_should_[expected_behavior]_when_[specific_condition](self, page: Page):
        """Verify [detailed description]."""
        ...
```

---

## Rule 4: Name State Changes Explicitly

Clearly describe the before and after states in your test names.

```python
# ❌ Bad
def test_should_change_status(self, page: Page): ...
def test_should_update_todo(self, page: Page): ...
def test_should_modify_permissions(self, page: Page): ...

# ✅ Good
def test_should_change_status_from_pending_to_approved(self, page: Page): ...
def test_should_mark_todo_as_completed_when_checkbox_clicked(self, page: Page): ...
def test_should_upgrade_user_from_basic_to_premium(self, page: Page): ...
```

**Generic Pattern:** `test_should_change_[attribute]_from_[initial_state]_to_[final_state]`

---

## Rule 5: Describe Async Behavior Clearly

Include loading and result states for asynchronous operations.

```python
# ❌ Bad
def test_should_load_data(self, page: Page): ...
def test_should_handle_api_call(self, page: Page): ...
def test_should_fetch_user(self, page: Page): ...

# ✅ Good
def test_should_show_skeleton_while_loading_data(self, page: Page): ...
def test_should_display_error_message_when_api_call_fails(self, page: Page): ...
def test_should_render_profile_after_user_data_loads(self, page: Page): ...
```

**Generic Pattern:** `test_should_[verb]_[expected_outcome]_[during_after]_[async_operation]`

---

## Rule 6: Name Error Cases Specifically

Be explicit about the type of error and what causes it.

```python
# ❌ Bad
def test_should_show_error(self, page: Page): ...
def test_should_handle_invalid_input(self, page: Page): ...
def test_should_validate_form(self, page: Page): ...

# ✅ Good
def test_should_show_invalid_card_error_when_card_number_wrong(self, page: Page): ...
def test_should_display_required_error_when_password_empty(self, page: Page): ...
def test_should_show_network_error_when_api_unreachable(self, page: Page): ...
```

**Generic Pattern:** `test_should_show_[specific_error]_when_[error_condition]`

---

## Rule 7: Use Business Language, Not Technical Terms

Write tests using domain language rather than implementation details.

```python
# ❌ Bad
def test_should_update_state(self, page: Page): ...
def test_should_dispatch_action(self, page: Page): ...
def test_should_modify_dom(self, page: Page): ...

# ✅ Good
def test_should_save_customer_order(self, page: Page): ...
def test_should_update_cart_total(self, page: Page): ...
def test_should_mark_order_as_delivered(self, page: Page): ...
```

**Generic Pattern:** `test_should_[business_action]_[business_entity]`

---

## Rule 8: Include Important Preconditions

Specify conditions that affect the behavior being tested.

```python
# ❌ Bad
def test_should_enable_button(self, page: Page): ...
def test_should_show_message(self, page: Page): ...
def test_should_apply_discount(self, page: Page): ...

# ✅ Good
def test_should_enable_checkout_when_cart_has_items(self, page: Page): ...
def test_should_show_free_shipping_when_total_exceeds_100(self, page: Page): ...
def test_should_apply_discount_when_user_is_premium_member(self, page: Page): ...
```

**Generic Pattern:** `test_should_[expected_behavior]_when_[precondition]`

---

## Rule 9: Name UI Feedback Tests from User Perspective

Describe visual changes as users would perceive them.

```python
# ❌ Bad
def test_should_set_error_class(self, page: Page): ...
def test_should_toggle_visibility(self, page: Page): ...
def test_should_update_styles(self, page: Page): ...

# ✅ Good
def test_should_highlight_search_box_in_red_when_empty(self, page: Page): ...
def test_should_show_green_checkmark_when_password_strong(self, page: Page): ...
def test_should_disable_submit_button_while_processing(self, page: Page): ...
```

**Generic Pattern:** `test_should_[visual_change]_when_[user_action_condition]`

---

## Rule 10: Structure Complex Workflows Step by Step

Break down complex processes into clear test classes and methods.

```python
# ❌ Bad
class TestCheckout:
    def test_should_process_checkout(self, page: Page): ...
    def test_should_handle_shipping(self, page: Page): ...
    def test_should_complete_order(self, page: Page): ...

# ✅ Good
class TestCheckoutProcess:
    """Tests for the complete checkout workflow."""
    
    def test_should_first_validate_items_in_stock(self, page: Page):
        """Step 1: Verify all items are available before checkout."""
        ...
    
    def test_should_then_collect_shipping_address(self, page: Page):
        """Step 2: Navigate to shipping form and validate fields."""
        ...
    
    def test_should_finally_process_payment(self, page: Page):
        """Step 3: Submit payment and verify transaction."""
        ...
    
    def test_should_display_order_confirmation_after_payment(self, page: Page):
        """Post-condition: Show confirmation page with order details."""
        ...
    
    def test_should_send_confirmation_email_after_order(self, page: Page):
        """Post-condition: Verify email sent to customer."""
        ...
```

**Generic Pattern:**
```python
class Test[ComplexProcess]:
    """Tests for [process description]."""
    
    def test_should_first_[initial_step](self, page: Page): ...
    def test_should_then_[next_step](self, page: Page): ...
    def test_should_finally_[final_step](self, page: Page): ...
    
    def test_should_[follow_up_action]_after_[key_milestone](self, page: Page): ...
```

---

## Complete Example

Here's a comprehensive example showing how to combine all these rules:

```python
# ❌ Bad
class TestShoppingCart:
    def test_test_adding_item(self, page: Page): ...
    def test_check_total(self, page: Page): ...
    def test_handle_checkout(self, page: Page): ...

# ✅ Good
class TestShoppingCart:
    """Tests for shopping cart functionality."""
    
    def test_should_add_item_to_cart_when_add_button_clicked(self, page: Page):
        """Verify item is added to cart when user clicks add button."""
        ...
    
    def test_should_update_total_price_immediately_after_adding_item(self, page: Page):
        """Verify cart total updates without delay."""
        ...
    
    def test_should_show_item_count_badge_when_items_added(self, page: Page):
        """Verify badge displays correct item count."""
        ...
    
    def test_should_display_empty_cart_message_when_no_items(self, page: Page):
        """Verify user-friendly message shown for empty cart."""
        ...
    
    def test_should_disable_checkout_button_when_cart_empty(self, page: Page):
        """Prevent checkout with no items."""
        ...
    
    def test_should_validate_stock_before_proceeding_to_checkout(self, page: Page):
        """Step 1: Check all items available before payment."""
        ...
    
    def test_should_show_loading_indicator_while_processing_payment(self, page: Page):
        """Step 2: Display feedback during async operation."""
        ...
    
    def test_should_display_success_message_after_checkout_completion(self, page: Page):
        """Step 3: Confirm order successful to user."""
        ...
```

---

## Test Name Checklist

Before committing your test, verify that its name:

- [ ] Starts with `test_should_`
- [ ] Uses a clear action verb
- [ ] Specifies the trigger condition (when/after)
- [ ] Uses business language (not technical terms)
- [ ] Describes visible behavior (what user sees)
- [ ] Is specific enough for debugging from name alone
- [ ] Groups logically with related tests in same class

---

## Python Naming Conventions

### File Names
```bash
# ✅ Good
test_shopping_cart.py
test_checkout_process.py
test_user_authentication.py

# ❌ Bad
testShoppingCart.py          # camelCase
test-shopping-cart.py        # kebab-case
TestShoppingCart.py          # PascalCase
```

### Class Names
```python
# ✅ Good (PascalCase, starts with Test)
class TestShoppingCart:
class TestCheckoutProcess:
class TestUserAuthentication:

# ❌ Bad
class test_shopping_cart:    # snake_case
class ShoppingCartTests:     # doesn't start with Test
class TestshoppingCart:      # inconsistent casing
```

### Method Names
```python
# ✅ Good (snake_case, starts with test_should_)
def test_should_add_item_when_button_clicked(self, page: Page):
def test_should_validate_email_format(self, page: Page):

# ❌ Bad
def testShouldAddItem(self, page: Page):     # camelCase
def test_add_item(self, page: Page):         # missing "should"
def testShould_Add_Item(self, page: Page):   # mixed case
```

---

## Conclusion

Thoughtful test naming is a fundamental building block in the broader landscape of writing better tests. To maintain consistency across your team:

1. **Document your naming conventions** in detail (like this file!)
2. **Share these guidelines** with all team members
3. **Integrate the guidelines** into your development workflow
4. **Use AI tools** to help generate consistent names

### For AI Tools (GitHub Copilot, Claude Code, OpenCode)

Incorporate these guidelines into your project documentation:
- Add this file to `.claude/skills/playwright-tests-best-practices/references/`
- Reference it in your main SKILL.md file
- AI tools will read and follow these conventions

Example integration in SKILL.md:
```markdown
## Naming Conventions

Follow the guidelines in `references/naming_functions.md`:
- All tests start with `test_should_`
- Include trigger events (when/after)
- Use business language, not technical terms
```

By following these steps, you can ensure consistent, high-quality test naming across your entire project!