# Checkout Flow Test Solution

## Problem
Testing the LEGO.com checkout flow directly is blocked by **Cloudflare bot protection**, which detects automated browsers and shows a security verification page instead of the actual website.

## Solution
Created a **mock server** that simulates the LEGO checkout flow locally, allowing reliable end-to-end testing without hitting the production site.

## Files Created

### 1. `tests/mock_server.py`
A local HTTP server that simulates the LEGO checkout flow:
- Homepage with products
- Shopping cart
- Checkout page (login vs guest options)
- Guest checkout form
- Payment page

**Start the server manually:**
```bash
python3 tests/mock_server.py
```

### 2. `tests/test_checkout_mock.py` ⭐ **RECOMMENDED**
Complete E2E checkout tests using the mock server:
- ✅ `test_complete_checkout_flow_as_guest` - Full checkout flow
- ✅ `test_guest_form_validation` - Form validation
- ✅ `test_guest_form_success` - Successful submission

**Run the tests:**
```bash
cd /home/gustavemilnobert/playwright-mindster-jam
python3 -m pytest tests/test_checkout_mock.py -v
```

### 3. `tests/test_checkout_flow.py`
Original test designed for production LEGO.com (blocked by Cloudflare).
Keep as reference for selector patterns and flow structure.

### 4. `tests/test_checkout_demo.py`
Alternative test using Playwright's demo e-commerce site (demo.playwright.dev).
Good for testing against a real (but test-friendly) e-commerce site.

## Test Coverage

The mock test covers the complete flow you requested:

1. ✅ Navigate to homepage
2. ✅ Add first product to cart
3. ✅ Go to checkout
4. ✅ Click "gå til betaling som gæst" (guest checkout)
5. ✅ Fill out guest form (email, name, address, city, postal code, phone)
6. ✅ Click "gå til betaling" (proceed to payment)
7. ✅ Verify payment page reached

## Running All Tests

```bash
# Run all checkout tests
python3 -m pytest tests/test_checkout_*.py -v

# Run with visible browser
python3 -m pytest tests/test_checkout_mock.py -v --headed

# Run with slow motion
python3 -m pytest tests/test_checkout_mock.py -v --slowmo=500
```

## Expected Output

```
tests/test_checkout_mock.py::TestMockCheckoutFlow::test_complete_checkout_flow_as_guest[chromium] PASSED
tests/test_checkout_mock.py::TestMockCheckoutValidation::test_guest_form_validation[chromium] PASSED
tests/test_checkout_mock.py::TestMockCheckoutValidation::test_guest_form_success[chromium] PASSED

============================== 3 passed in 6.72s ===============================
```

## Why This Approach?

| Approach | Pros | Cons |
|----------|------|------|
| **Mock Server** (✅ Recommended) | Fast, reliable, no bot protection, offline-capable | Doesn't test real site |
| **Demo Site** | Real e-commerce site, no bot protection | Different UI/flow than LEGO |
| **Production Site** | Tests real user experience | Blocked by Cloudflare, flaky |

## Adapting for Production

When you need to test the real LEGO.com site:

1. **Use a staging environment** without bot protection
2. **Use API testing** for backend validation
3. **Run tests in production-like environment** with proper authentication
4. **Consider visual regression testing** with screenshots

## Test Data

The mock tests use Danish test data matching the LEGO.com flow:

```python
GUEST_DATA = {
    "email": "test@example.dk",
    "first_name": "Test",
    "last_name": "Testesen",
    "address": "Testvej 123",
    "city": "København",
    "postal_code": "1000",
    "phone": "12345678",
}
```

## Next Steps

1. Run the tests: `python3 -m pytest tests/test_checkout_mock.py -v`
2. Review the mock server code to understand the flow
3. Adapt selectors if testing against a different environment
4. Add more test cases (edge cases, error handling, etc.)