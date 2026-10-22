# Workshop Task: Checkout Flow Test

## What to Test

We want to test the complete checkout flow on LEGO.com:

### Part 1: Product to Checkout
1. **Find a product** on the homepage and click on it
2. **Verify** you're taken to the correct product page
3. **Click "Føj Til Kurv"** (Add to Cart)
4. **Open the cart** and verify the product is there
5. **Click "Gå til sikker betaling"** (Go to secure payment)
6. **Verify** you're redirected to the login or create account page
7. **Click "Checkout as guest"** (or equivalent option)
8. **Verify** you're taken to the checkout page

### Part 2: Checkout Page Validation
9. **Verify** the checkout page shows the product(s) you added
10. **Fill out** the checkout form (name, address, etc.)
11. **Verify** the email field shows the correct email
12. **Verify** "Levering" (delivery) is selected as the default shipping method
13. **Click "Continue to payment"** and verify you're redirected to the payment page

This is where we stop - no need to complete the actual payment!

## Expected result

By the end, you should have a working test that:
- Starts at the homepage
- Adds a product to the cart
- Verifies the cart contains the product
- Successfully reaches the checkout/login page
- Completes guest checkout flow to the checkout page
- Validates the checkout page shows the correct products
- Fills out the checkout form
- Verifies email and delivery method ("Levering")
- Clicks through to payment page

## Tips

### One Step at a Time
Don't try to write the entire test in one go! Build it incrementally:
1. Write the first step (navigate to homepage)
2. Run the test - make sure it passes
3. Add the next step (click product)
4. Run again - verify it still works
5. Continue adding one step at a time


### 📖 Keep It Readable
- Follow naming conventions from `naming_functions.md`
- If you find the tests complicated, what is it you don't like?

Have fun gutter