"""
Mock server for testing checkout flow without hitting production LEGO.com.

This creates a local server that simulates the LEGO checkout flow,
allowing tests to run reliably without bot protection issues.
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os
from pathlib import Path

# Mock data for the checkout flow
MOCK_DATA = {
    "products": [
        {
            "id": "10497",
            "name": "LEGO® Creator 3-in-1",
            "price": 299.95,
            "currency": "kr.",
            "image": "/images/product-10497.jpg",
            "age": "8+",
            "pieces": 132,
        }
    ],
    "checkout": {
        "required_fields": ["email", "firstName", "lastName", "address", "city", "postalCode", "phone"],
        "guest_checkout_available": True,
    }
}


class MockLEGOHandler(SimpleHTTPRequestHandler):
    """HTTP request handler that serves mock LEGO pages."""
    
    def do_GET(self):
        """Handle GET requests."""
        path = self.path.split('?')[0]  # Remove query params
        
        # Route handling
        if path == '/' or path == '/da-dk':
            self.serve_homepage()
        elif path.startswith('/product/'):
            self.serve_product_page()
        elif path == '/cart' or path == '/da-dk/cart':
            self.serve_cart_page()
        elif path == '/checkout' or path == '/da-dk/checkout':
            self.serve_checkout_page()
        elif path == '/checkout/guest' or path == '/da-dk/checkout/guest':
            self.serve_guest_checkout_page()
        elif path == '/checkout/payment' or path == '/da-dk/checkout/payment':
            self.serve_payment_page()
        elif path.startswith('/api/'):
            self.serve_api_response()
        elif path.endswith(('.css', '.js', '.png', '.jpg', '.svg')):
            self.serve_static_file()
        else:
            self.send_error(404, "Not Found")
    
    def do_POST(self):
        """Handle POST requests (for form submissions)."""
        path = self.path.split('?')[0]
        
        if path == '/api/cart/add':
            self.serve_json({"success": True, "cart_count": 1})
        elif path == '/api/checkout/guest':
            self.serve_json({"success": True, "redirect": "/checkout/payment"})
        elif path == '/api/checkout/validate':
            self.serve_json({"valid": True})
        else:
            self.send_error(404, "Not Found")
    
    def serve_json(self, data, status=200):
        """Send a JSON response."""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def serve_html(self, html_content):
        """Send an HTML response."""
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def serve_homepage(self):
        """Serve mock homepage with products."""
        html = """
        <!DOCTYPE html>
        <html lang="da">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>LEGO® Danmark | Hjem</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
                header { background: #ffcc00; padding: 20px; margin-bottom: 20px; }
                nav { display: flex; justify-content: space-between; align-items: center; }
                .logo { font-size: 24px; font-weight: bold; }
                .cart-link { background: #000; color: #fff; padding: 10px 20px; text-decoration: none; border-radius: 5px; }
                .products { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 20px; }
                .product-card { border: 1px solid #ddd; padding: 20px; border-radius: 8px; text-align: center; }
                .product-card img { max-width: 100%; height: 200px; object-fit: contain; }
                .product-name { font-size: 18px; margin: 10px 0; }
                .product-price { font-size: 20px; font-weight: bold; color: #000; }
                .add-to-cart { background: #000; color: #fff; border: none; padding: 10px 20px; cursor: pointer; margin-top: 10px; border-radius: 5px; }
                .add-to-cart:hover { background: #333; }
                .badge { background: #ff0000; color: #fff; padding: 2px 8px; border-radius: 3px; font-size: 12px; }
            </style>
        </head>
        <body>
            <header>
                <nav>
                    <div class="logo">LEGO®</div>
                    <div>
                        <a href="/da-dk" style="margin-right: 15px;">Shop</a>
                        <a href="/da-dk/cart" class="cart-link" id="cart-link">Indkøbskurv <span id="cart-count">(0)</span></a>
                    </div>
                </nav>
            </header>
            <main>
                <h1>Velkommen til LEGO® Danmark</h1>
                <div class="products" id="products">
                    <div class="product-card" data-product-id="10497">
                        <img src="/images/product-10497.jpg" alt="LEGO Creator 3-in-1" onerror="this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 width=%22200%22 height=%22200%22><rect fill=%22%23ddd%22 width=%22200%22 height=%22200%22/><text x=%2250%25%22 y=%2250%25%22 text-anchor=%22middle%22>Product</text></svg>'">
                        <div class="product-name">LEGO® Creator 3-in-1</div>
                        <div class="product-info">
                            <span class="age">8+</span> | <span class="pieces">132 dele</span>
                        </div>
                        <div class="product-price">299,95 kr.</div>
                        <button class="add-to-cart" onclick="addToCart('10497')">Føj Til Kurv</button>
                    </div>
                </div>
            </main>
            <script>
                let cartCount = 0;
                function addToCart(productId) {
                    cartCount++;
                    document.getElementById('cart-count').textContent = '(' + cartCount + ')';
                    // Simulate API call
                    fetch('/api/cart/add', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({productId: productId})
                    });
                }
            </script>
        </body>
        </html>
        """
        self.serve_html(html)
    
    def serve_product_page(self):
        """Serve mock product page."""
        html = """
        <!DOCTYPE html>
        <html lang="da">
        <head>
            <meta charset="UTF-8">
            <title>LEGO® Product</title>
        </head>
        <body>
            <h1>LEGO® Creator 3-in-1</h1>
            <p>Price: 299,95 kr.</p>
            <button onclick="window.location.href='/cart'">Gå til kassen</button>
        </body>
        </html>
        """
        self.serve_html(html)
    
    def serve_cart_page(self):
        """Serve mock cart page."""
        html = """
        <!DOCTYPE html>
        <html lang="da">
        <head>
            <meta charset="UTF-8">
            <title>Indkøbskurv - LEGO®</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
                .cart-item { border: 1px solid #ddd; padding: 20px; margin-bottom: 10px; }
                .checkout-btn { background: #000; color: #fff; padding: 15px 30px; border: none; cursor: pointer; font-size: 16px; }
                .guest-checkout { margin-top: 20px; padding: 20px; background: #f5f5f5; border-radius: 8px; }
            </style>
        </head>
        <body>
            <h1>Din Indkøbskurv</h1>
            <div class="cart-item">
                <h3>LEGO® Creator 3-in-1</h3>
                <p>Price: 299,95 kr.</p>
                <p>Quantity: 1</p>
            </div>
            <div class="total">
                <h2>Total: 299,95 kr.</h2>
            </div>
            <button class="checkout-btn" onclick="window.location.href='/checkout'">Gå til kassen</button>
            
            <div class="guest-checkout">
                <h3>Ønsker du ikke at oprette en konto?</h3>
                <button class="checkout-btn" onclick="window.location.href='/checkout/guest'">gå til betaling som gæst</button>
            </div>
        </body>
        </html>
        """
        self.serve_html(html)
    
    def serve_checkout_page(self):
        """Serve mock checkout page with login/guest options."""
        html = """
        <!DOCTYPE html>
        <html lang="da">
        <head>
            <meta charset="UTF-8">
            <title>Checkout - LEGO®</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
                .checkout-options { display: flex; gap: 20px; margin-top: 20px; }
                .option { border: 1px solid #ddd; padding: 30px; border-radius: 8px; text-align: center; flex: 1; }
                .btn { background: #000; color: #fff; padding: 15px 30px; border: none; cursor: pointer; font-size: 16px; margin-top: 15px; }
            </style>
        </head>
        <body>
            <h1>Checkout</h1>
            <div class="checkout-options">
                <div class="option">
                    <h2>Log ind</h2>
                    <p>Log ind for at bruge dine gemte oplysninger</p>
                    <button class="btn" onclick="alert('Login not implemented in mock')">Log ind</button>
                </div>
                <div class="option">
                    <h2>Gæst Checkout</h2>
                    <p>Betal uden at oprette en konto</p>
                    <button class="btn" onclick="window.location.href='/checkout/guest'">gå til betaling som gæst</button>
                </div>
            </div>
        </body>
        </html>
        """
        self.serve_html(html)
    
    def serve_guest_checkout_page(self):
        """Serve mock guest checkout form."""
        html = """
        <!DOCTYPE html>
        <html lang="da">
        <head>
            <meta charset="UTF-8">
            <title>Gæst Checkout - LEGO®</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 20px; max-width: 600px; margin: 0 auto; }
                .form-group { margin-bottom: 15px; }
                label { display: block; margin-bottom: 5px; font-weight: bold; }
                input { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
                .btn { background: #000; color: #fff; padding: 15px 30px; border: none; cursor: pointer; font-size: 16px; width: 100%; margin-top: 20px; }
                .btn:hover { background: #333; }
                .order-summary { background: #f5f5f5; padding: 20px; margin-bottom: 20px; border-radius: 8px; }
            </style>
        </head>
        <body>
            <h1>Gæst Checkout</h1>
            
            <div class="order-summary">
                <h3>Ordresammendrag</h3>
                <p>LEGO® Creator 3-in-1</p>
                <p><strong>Total: 299,95 kr.</strong></p>
            </div>
            
            <form id="guest-form" onsubmit="submitForm(event)">
                <div class="form-group">
                    <label for="email">E-mail *</label>
                    <input type="email" id="email" name="email" required placeholder="din@email.dk">
                </div>
                
                <div class="form-group">
                    <label for="firstName">Fornavn *</label>
                    <input type="text" id="firstName" name="firstName" required placeholder="Fornavn">
                </div>
                
                <div class="form-group">
                    <label for="lastName">Efternavn *</label>
                    <input type="text" id="lastName" name="lastName" required placeholder="Efternavn">
                </div>
                
                <div class="form-group">
                    <label for="address">Adresse *</label>
                    <input type="text" id="address" name="address" required placeholder="Vejnavn og husnummer">
                </div>
                
                <div class="form-group">
                    <label for="city">By *</label>
                    <input type="text" id="city" name="city" required placeholder="By">
                </div>
                
                <div class="form-group">
                    <label for="postalCode">Postnummer *</label>
                    <input type="text" id="postalCode" name="postalCode" required placeholder="1000" pattern="[0-9]{4}">
                </div>
                
                <div class="form-group">
                    <label for="phone">Telefon *</label>
                    <input type="tel" id="phone" name="phone" required placeholder="12345678">
                </div>
                
                <button type="submit" class="btn">gå til betaling</button>
            </form>
            
            <script>
                function submitForm(event) {
                    event.preventDefault();
                    const formData = new FormData(event.target);
                    const data = Object.fromEntries(formData.entries());
                    
                    fetch('/api/checkout/guest', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify(data)
                    })
                    .then(response => response.json())
                    .then(result => {
                        if (result.success) {
                            window.location.href = result.redirect;
                        }
                    });
                }
            </script>
        </body>
        </html>
        """
        self.serve_html(html)
    
    def serve_payment_page(self):
        """Serve mock payment page."""
        html = """
        <!DOCTYPE html>
        <html lang="da">
        <head>
            <meta charset="UTF-8">
            <title>Betaling - LEGO®</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 20px; max-width: 600px; margin: 0 auto; }
                .payment-methods { border: 1px solid #ddd; padding: 20px; border-radius: 8px; }
                .payment-option { padding: 15px; border: 1px solid #ddd; margin-bottom: 10px; border-radius: 4px; cursor: pointer; }
                .payment-option:hover { background: #f5f5f5; }
                .payment-option.selected { border-color: #000; background: #f0f0f0; }
                .btn { background: #000; color: #fff; padding: 15px 30px; border: none; cursor: pointer; font-size: 16px; width: 100%; margin-top: 20px; }
                .success { background: #4CAF50; color: white; padding: 20px; border-radius: 8px; text-align: center; }
            </style>
        </head>
        <body>
            <h1>Betaling</h1>
            
            <div class="payment-methods">
                <h3>Vælg betalingsmetode</h3>
                <div class="payment-option" onclick="selectPayment(this)">
                    <strong>Kreditkort</strong>
                    <p>Visa, Mastercard, Dankort</p>
                </div>
                <div class="payment-option" onclick="selectPayment(this)">
                    <strong>MobilePay</strong>
                    <p>Betal med MobilePay</p>
                </div>
                <div class="payment-option" onclick="selectPayment(this)">
                    <strong>Klarna</strong>
                    <p>Delbetaling med Klarna</p>
                </div>
            </div>
            
            <div id="payment-form" style="display:none; margin-top: 20px;">
                <div class="form-group">
                    <label>Kortnummer</label>
                    <input type="text" placeholder="1234 5678 9012 3456" style="width: 100%; padding: 10px; margin-top: 5px;">
                </div>
                <button class="btn" onclick="completePayment()">Betal nu</button>
            </div>
            
            <script>
                function selectPayment(element) {
                    document.querySelectorAll('.payment-option').forEach(el => el.classList.remove('selected'));
                    element.classList.add('selected');
                    document.getElementById('payment-form').style.display = 'block';
                }
                
                function completePayment() {
                    document.body.innerHTML = '<div class="success"><h1>✓ Ordren er gennemført!</h1><p>Tak for din bestilling.</p><p>Ordrenummer: #' + Math.floor(Math.random() * 100000) + '</p></div>';
                }
            </script>
        </body>
        </html>
        """
        self.serve_html(html)
    
    def serve_api_response(self):
        """Serve API responses."""
        self.serve_json({"success": True})
    
    def serve_static_file(self):
        """Serve static files (images, css, js)."""
        # For simplicity, return placeholder for missing files
        if self.path.endswith(('.png', '.jpg', '.svg')):
            self.send_response(200)
            self.send_header('Content-Type', 'image/svg+xml')
            self.end_headers()
            svg = '<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200"><rect fill="#ddd" width="200" height="200"/><text x="50%" y="50%" text-anchor="middle">Image</text></svg>'
            self.wfile.write(svg.encode())
        else:
            self.send_error(404, "Not Found")


def start_mock_server(port=8765):
    """Start the mock LEGO server."""
    server = HTTPServer(('localhost', port), MockLEGOHandler)
    print(f"🧱 Mock LEGO server running at http://localhost:{port}")
    print("Press Ctrl+C to stop")
    server.serve_forever()


if __name__ == "__main__":
    start_mock_server()