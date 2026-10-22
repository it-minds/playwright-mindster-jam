# Playwright Mindster Jam

This project demonstrates writing automated browser tests using Playwright with Python.

## Prerequisites

- Python 3.8+
- pip (Python package manager)

## Setup

### 1. Create a virtual environment (recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Playwright browsers

```bash
playwright install chromium
```

### 4. Install system dependencies (Linux only) ⚠️

On Linux, you need to install system dependencies for the browser. **This requires sudo access:**

```bash
# Ubuntu/Debian (requires sudo)
playwright install-deps chromium

# Or manually install:
sudo apt-get install -y libnspr4 libnss3 libdbus-1-3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2 libpango-1.0-0 libcairo2
```

> **Note:** If you don't have sudo access (like in some corporate environments), you can:
> - Use Docker with the Playwright image
> - Run tests on a machine with the dependencies installed
> - Use a CI/CD pipeline that has the dependencies pre-installed

## Running Tests

```bash
# Run all tests
pytest

# Run tests in headed mode (see the browser)
pytest --headed

# Run a specific test file
pytest tests/test_example.py

# Run with slow motion (great for demos!)
pytest --slowmo=1000

# Run in debug mode
pytest --debug
```

## Project Structure

```
playwright-mindster-jam/
├── tests/
│   └── test_example.py    # Example test file
├── requirements.txt
├── pytest.ini
└── README.md
```

## Writing Tests

Playwright tests use a simple pattern:

```python
from playwright.sync_api import Page

def test_example(page: Page):
    page.goto("https://example.com")
    assert "Example" in page.title()
```

## Useful Resources

- [Playwright Python Docs](https://playwright.dev/python/)
- [Playwright Code Generator](https://playwright.dev/python/docs/codegen)
- [Pytest Documentation](https://docs.pytest.org/)