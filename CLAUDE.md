# CLAUDE.md — Project Guide

## Project Overview

FastAPI demo app with full Playwright automation test coverage (API-level + browser UI).

## Stack

- **Backend**: FastAPI + Pydantic v2 + Uvicorn
- **Testing**: pytest + pytest-playwright + Playwright (Chromium)
- **Python**: 3.11 | **Venv**: `C:/Project/venv/`

## Project Structure

```
app/
├── main.py               # App entry point, routers registered here
├── models/
│   ├── user.py           # UserCreate / UserResponse / UserUpdate
│   └── item.py           # ItemCreate / ItemResponse / ItemUpdate
└── routers/
    ├── users.py          # CRUD  /users
    ├── items.py          # CRUD  /items
    └── frontend.py       # HTML UI served at GET /ui

tests/
├── conftest.py                    # Server spin-up + shared fixtures
├── test_api_playwright.py         # HTTP-level API tests
└── test_browser_playwright.py     # Real Chromium browser tests
```

## Common Commands

```bash
# Run the app
venv/Scripts/python -m uvicorn app.main:app --reload

# Run all tests
venv/Scripts/python -m pytest tests/ -v

# Browser tests — headless (default)
venv/Scripts/python -m pytest tests/test_browser_playwright.py -v

# Browser tests — visible window
venv/Scripts/python -m pytest tests/test_browser_playwright.py --headed

# Slow motion demo (600ms between steps)
venv/Scripts/python -m pytest tests/test_browser_playwright.py --headed --slowmo=600

# Install dependencies
venv/Scripts/pip install -r requirements.txt
venv/Scripts/playwright install chromium
```

## Test Fixtures (conftest.py)

| Fixture | Scope | What it does |
|---------|-------|--------------|
| `start_server` | session | Starts uvicorn on port 8001 in a daemon thread |
| `app_base_url` | session | Returns `http://127.0.0.1:8001` |
| `api_context` | session | Playwright `APIRequestContext` for HTTP tests |
| `page` | function | Real Chromium page — from pytest-playwright |

> **Never rename `app_base_url` to `base_url`** — `pytest-base-url` plugin
> owns that name and causes a `ScopeMismatch` error.

## Windows: greenlet Pin

`greenlet>=3.2.0` crashes on some Windows machines with a DLL error.
`requirements.txt` pins `greenlet==3.1.1` — do not upgrade it.

```bash
# Fix if broken:
venv/Scripts/pip install "greenlet==3.1.1" --force-reinstall
```

## Adding Features

### New API endpoint
1. Add Pydantic models to `app/models/`
2. Add router file `app/routers/<name>.py`
3. Register in `app/main.py` with `app.include_router(...)`
4. Add API tests to `tests/test_api_playwright.py`

### New UI page
1. Add route returning `HTMLResponse` in `app/routers/frontend.py`
2. Add browser tests to `tests/test_browser_playwright.py`

## Skills

Project-local skills live in `.claude/skills/`:

- `fastapi-templates` — FastAPI patterns and templates
- `playwright-automation` — Playwright test patterns for this project
