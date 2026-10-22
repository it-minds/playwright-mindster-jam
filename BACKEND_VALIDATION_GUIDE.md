# Backend Data Validation Testing Guide

This guide explains how to test that the data displayed on your frontend matches what the backend API returns.

## Why Test Backend Data?

Frontend tests that only check if elements exist can miss critical bugs:

| Bug Type | UI Test | Backend Data Test |
|----------|---------|-------------------|
| Wrong price displayed | ✅ Passes | ❌ Fails |
| Cached stale data | ✅ Passes | ❌ Fails |
| Currency conversion error | ✅ Passes | ❌ Fails |
| Missing product info | ✅ Passes | ❌ Fails |
| Wrong image shown | ✅ Passes | ❌ Fails |

## How It Works

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Backend   │────▶│   Playwright │────▶│   Browser   │
│     API     │     │  Intercepts  │     │    Page     │
│             │     │  Response    │     │             │
└─────────────┘     └──────────────┘     └─────────────┘
                           │
                    ┌──────▼──────┐
                    │   Compare   │
                    │   API Data  │
                    │   vs UI     │
                    └─────────────┘
```

## Test Patterns

### 1. Intercept API Responses

```python
captured_responses = []

def intercept_api(route: Route):
    response = route.fetch()
    try:
        data = response.json()
        captured_responses.append(data)
    except:
        pass
    route.fulfill(response=response)

# Intercept common API patterns
page.route("**/api/**", intercept_api)
page.route("**/graphql", intercept_api)
page.route("**/*products*", intercept_api)
```

### 2. Extract Product Data from Response

APIs return data in different structures. Handle multiple patterns:

```python
def _extract_products_from_response(self, data) -> list:
    patterns = [
        lambda d: d if isinstance(d, list) else None,           # [products]
        lambda d: d.get("products") if isinstance(d, dict) else None,  # {products: []}
        lambda d: d.get("data", {}).get("products"),            # {data: {products: []}}
        lambda d: d.get("items") if isinstance(d, dict) else None,
        lambda d: d.get("results") if isinstance(d, dict) else None,
    ]
    
    for pattern in patterns:
        result = pattern(data)
        if result and isinstance(result, list):
            return result
    return []
```

### 3. Compare API Data to UI

```python
for product in products[:3]:  # Check first 3 products
    api_price = str(product["price"])
    
    # Find matching product card on page
    product_card = page.locator(f'[data-product-id="{product["id"]}"]').first
    
    if product_card.count() > 0:
        card_text = product_card.inner_text()
        
        # Verify price matches
        assert api_price in card_text, \
            f"Price {api_price} not found in card: {card_text}"
```

## Test Examples

### Price Validation

```python
def test_product_price_matches_api_response(self, page: Page):
    """Verify displayed price matches API."""
    captured = []
    
    def intercept(route: Route):
        resp = route.fetch()
        try:
            captured.append(resp.json())
        except:
            pass
        route.fulfill(response=resp)
    
    page.route("**/api/**", intercept)
    page.goto("https://www.lego.com/da-dk")
    page.wait_for_load_state("networkidle")
    
    # Validate each product's price
    for response in captured:
        products = extract_products(response)
        for product in products:
            api_price = product.get("price")
            ui_price = get_displayed_price(product["id"])
            assert api_price == ui_price
```

### Availability Status Validation

```python
def test_product_availability_matches_api(self, page: Page):
    """Verify stock status matches API."""
    captured = []
    
    def intercept(route: Route):
        resp = route.fetch()
        try:
            captured.append(resp.json())
        except:
            pass
        route.fulfill(response=resp)
    
    page.route("**/api/**", intercept)
    page.goto("https://www.lego.com/da-dk")
    page.wait_for_load_state("networkidle")
    
    for response in captured:
        products = extract_products(response)
        for product in products:
            is_available = product.get("available", True)
            card_text = get_card_text(product["id"]).lower()
            
            if not is_available:
                assert "udsolgt" in card_text or "restordre" in card_text
```

### Image URL Validation

```python
def test_product_image_matches_api(self, page: Page):
    """Verify displayed image matches API URL."""
    captured = []
    
    def intercept(route: Route):
        resp = route.fetch()
        try:
            captured.append(resp.json())
        except:
            pass
        route.fulfill(response=resp)
    
    page.route("**/api/**", intercept)
    page.route("**/*.jpg", intercept)
    page.route("**/*.webp", intercept)
    
    page.goto("https://www.lego.com/da-dk")
    page.wait_for_load_state("networkidle")
    
    for response in captured:
        products = extract_products(response)
        for product in products:
            api_image = product.get("imageUrl")
            if api_image:
                # Check if image URL is used on page
                images = page.locator("img")
                for i in range(images.count()):
                    src = images.nth(i).get_attribute("src")
                    if src and product["id"] in src:
                        assert images.nth(i).is_visible()
```

## Common API Response Patterns

### REST API Pattern
```json
{
  "products": [
    {
      "id": "72306",
      "name": "PlayStation™",
      "price": 1299.95,
      "currency": "DKK",
      "age": 18,
      "pieceCount": 1911,
      "image": "https://.../72306.jpg",
      "available": true
    }
  ]
}
```

### GraphQL Pattern
```json
{
  "data": {
    "products": [
      {
        "id": "72306",
        "displayName": "PlayStation™",
        "pricing": {
          "amount": 1299.95,
          "currency": "DKK"
        },
        "attributes": {
          "ageRange": "18+",
          "pieceCount": 1911
        }
      }
    ]
  }
}
```

### Nested Pattern
```json
{
  "data": {
    "productList": {
      "items": [
        {
          "code": "72306",
          "name": "PlayStation™",
          "price": {"value": 1299.95}
        }
      ]
    }
  }
}
```

## Debugging Tips

### Log API Responses
```python
def intercept_api(route: Route):
    response = route.fetch()
    try:
        data = response.json()
        print(f"API Response from {response.url}:")
        print(json.dumps(data, indent=2))
    except:
        pass
    route.fulfill(response=response)
```

### Save Responses to File
```python
import json

def intercept_api(route: Route):
    response = route.fetch()
    try:
        data = response.json()
        with open(f"/tmp/api_response_{route.request.url.split('/')[-1]}.json", "w") as f:
            json.dump(data, f, indent=2)
    except:
        pass
    route.fulfill(response=response)
```

### Screenshot on Mismatch
```python
try:
    assert api_price in card_text
except AssertionError:
    page.screenshot(path="debug_price_mismatch.png")
    raise
```

## Running These Tests

```bash
# Run backend validation tests
pytest tests/test_backend_data_validation.py -v

# Run with headed mode to see what's happening
pytest tests/test_backend_data_validation.py --headed

# Run with slow motion
pytest tests/test_backend_data_validation.py --slowmo=500

# Run specific test
pytest tests/test_backend_data_validation.py::TestProductDataFromAPI::test_product_price_matches_api_response -v
```

## Adapting to Your API

1. **Identify your API endpoints**
   - Open browser DevTools → Network tab
   - Filter by "XHR" or "Fetch"
   - Look for product/catalog endpoints

2. **Update the route patterns**
   ```python
   # Replace these with your actual endpoints
   page.route("**/api/products**", intercept_api)
   page.route("**/graphql**", intercept_api)
   ```

3. **Update the extraction function**
   ```python
   def _extract_products_from_response(self, data) -> list:
       # Match your API's structure
       if isinstance(data, dict) and "products" in data:
           return data["products"]
       return []
   ```

4. **Update field names**
   ```python
   # Match your API's field names
   api_price = product.get("price") or product.get("amount")
   api_name = product.get("name") or product.get("displayName")
   ```

## Benefits

✅ **Catches data transformation bugs** - API says 100kr, UI shows 10kr  
✅ **Catches caching issues** - Old prices still displayed  
✅ **Catches race conditions** - UI updates before data loads  
✅ **Catches localization bugs** - Wrong currency or format  
✅ **Documents expected API structure** - Tests serve as documentation  

## Limitations

⚠️ **Brittle if API changes** - Update tests when API changes  
⚠️ **Slower than UI-only tests** - Intercepting adds overhead  
⚠️ **May need updates for different environments** - Staging vs prod APIs differ  

## Best Practices

1. **Test critical data only** - Price, availability, key info
2. **Sample a few products** - Don't validate every single one
3. **Be flexible with formatting** - "1299.95" vs "1299,95 kr."
4. **Log failures with context** - Include API response in error message
5. **Run in CI with mocked APIs** - For faster, more reliable tests