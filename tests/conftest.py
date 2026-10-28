"""
Pytest configuration and fixtures for Playwright tests.

This file provides custom fixtures that can be used across all tests.
"""

import pytest
from playwright.sync_api import Browser, BrowserContext, Page


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    Customize browser context arguments to make the browser appear more human-like.
    This can help avoid bot detection on some websites.
    """
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "locale": "da-DK",
        "timezone_id": "Europe/Copenhagen",
        "permissions": ["geolocation"],
        "geolocation": {"latitude": 55.6761, "longitude": 12.5683},  # Copenhagen
    }


@pytest.fixture(scope="function")
def human_page(page: Page):
    """
    A page fixture that adds human-like behavior to help avoid bot detection.
    Use this fixture instead of the default 'page' for sites with bot protection.
    """
    # Set viewport to common desktop size
    page.set_viewport_size({"width": 1920, "height": 1080})
    
    # Add some random mouse movements to appear more human
    def human_move(x, y, duration=500):
        """Simulate human-like mouse movement."""
        import random
        steps = 10
        for i in range(steps):
            page.mouse.move(
                x + random.randint(-5, 5),
                y + random.randint(-5, 5)
            )
            page.wait_for_timeout(duration // steps)
        page.mouse.move(x, y)
    
    page.human_move = human_move
    yield page