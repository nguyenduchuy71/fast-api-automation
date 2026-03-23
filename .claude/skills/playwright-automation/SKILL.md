---
name: playwright-automation
description: Load this skill when writing, running, debugging, or reviewing Playwright automation tests in this project. Triggers on: "playwright", "browser test", "automation test", "e2e test", "UI test", "headed", "headless", "page fixture", "APIRequestContext", "pytest-playwright", "slowmo", "screenshot", "greenlet DLL", "browser automation", or any file matching tests/test_browser*.py or tests/test_*playwright*.py.
---

# Playwright Automation Testing — Project Guide

## Project Layout

```
C:/Project/
├── app/
│   ├── main.py
│   └── routers/
│       └── frontend.py         # HTML UI at GET /ui
├── tests/
│   ├── conftest.py             # Server spin-up + shared fixtures
│   ├── test_api_playwright.py  # HTTP-level tests (no browser)
│   └── test_browser_playwright.py  # Real Chromium UI tests
├── requirements.txt
└── pytest.ini
```

---

## Key Fixtures (conftest.py)

| Fixture | Scope | Purpose |
|---------|-------|---------|
| `start_server` | session | Starts uvicorn on port 8001 in a daemon thread |
| `app_base_url` | session | Returns `http://127.0.0.1:8001` |
| `api_context` | session | `APIRequestContext` for HTTP tests |
| `page` | function | Real Chromium page — provided by pytest-playwright |

> **Critical:** Use `app_base_url`, NOT `base_url`.
> `pytest-base-url` plugin owns `base_url` — naming clash causes `ScopeMismatch`.

---

## Running Tests

```bash
# All tests
venv/Scripts/python -m pytest tests/ -v

# Browser tests only
venv/Scripts/python -m pytest tests/test_browser_playwright.py -v

# Open visible browser window
venv/Scripts/python -m pytest tests/test_browser_playwright.py --headed

# Slow motion (ms between steps) — good for demos/debugging
venv/Scripts/python -m pytest tests/test_browser_playwright.py --headed --slowmo=600

# Screenshot on failure
venv/Scripts/python -m pytest tests/ --screenshot=only-on-failure

# Record video
venv/Scripts/python -m pytest tests/ --video=on

# Different browser
venv/Scripts/python -m pytest tests/ --browser firefox
```

---

## API Tests Pattern

```python
from playwright.sync_api import APIRequestContext, Playwright
import pytest

@pytest.fixture(scope="session")
def api_context(playwright: Playwright, app_base_url: str) -> APIRequestContext:
    ctx = playwright.request.new_context(base_url=app_base_url)
    yield ctx
    ctx.dispose()

def test_create_item(api_context: APIRequestContext):
    res = api_context.post("/items/", data={"title": "Widget", "price": "9.99"})
    assert res.status == 201
    assert res.json()["title"] == "Widget"
```

---

## Browser Tests Pattern

```python
from playwright.sync_api import Page, expect

def test_add_item(page: Page, app_base_url: str):
    page.goto(app_base_url + "/ui")
    page.fill("#item-title", "Widget")
    page.fill("#item-price", "9.99")
    page.click("#item-form button[type='submit']")
    expect(page.locator("#status")).to_have_text("Item added!")
    expect(page.locator("#item-list")).to_contain_text("Widget")
```

---

## `expect()` Auto-Wait Assertions

```python
expect(page).to_have_title("FastAPI Demo")
expect(locator).to_be_visible()
expect(locator).to_have_text("exact")
expect(locator).to_contain_text("partial")
expect(locator).not_to_contain_text("gone")
expect(locator).to_have_count(3)
```

All auto-wait up to 5 s — never use `time.sleep()`.

---

## Locators

```python
page.locator("#id")
page.locator(".class")
page.get_by_role("button", name="Submit")
page.get_by_placeholder("Enter title")
page.locator("li", has_text="Widget")
page.locator("li", has_text="Widget").nth(0)
```

---

## Windows greenlet DLL Fix

`greenlet>=3.2.0` crashes on some Windows machines.

```
ImportError: DLL load failed while importing _greenlet
```

Fix (already applied):
```bash
venv/Scripts/pip install "greenlet==3.1.1" --force-reinstall
venv/Scripts/playwright install chromium
```

`requirements.txt` pins: `greenlet==3.1.1` — do not upgrade.

---

## Adding New Tests

1. **API test** → add to `tests/test_api_playwright.py`, use `api_context` fixture
2. **Browser test** → add to `tests/test_browser_playwright.py`, use `page` fixture
3. **New UI page** → add route in `app/routers/frontend.py`, import in `app/main.py`
