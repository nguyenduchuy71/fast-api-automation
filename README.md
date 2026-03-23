# FastAPI Automation Demo

A FastAPI demo application with full Playwright test coverage at both the HTTP API level and real browser UI level.

## Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI + Pydantic v2 + Uvicorn |
| Testing | pytest + pytest-playwright + Playwright (Chromium) |
| Python | 3.11 |
| Venv | `C:/Project/venv/` |

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

## Setup

```bash
# Install dependencies
venv/Scripts/pip install -r requirements.txt

# Install Playwright browser
venv/Scripts/playwright install chromium
```

## Running the App

```bash
venv/Scripts/python -m uvicorn app.main:app --reload
```

The app runs on `http://127.0.0.1:8000` by default.

| URL | Description |
|-----|-------------|
| `GET /` | Root health check |
| `GET /health` | Health status |
| `GET /ui` | Browser UI |
| `GET /docs` | Interactive Swagger UI |
| `GET /redoc` | ReDoc documentation |

## API Endpoints

### Users — `/users`

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/users/` | List all users |
| `GET` | `/users/{id}` | Get user by ID |
| `POST` | `/users/` | Create user |
| `PUT` | `/users/{id}` | Update user |
| `DELETE` | `/users/{id}` | Delete user |

### Items — `/items`

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/items/` | List all items |
| `GET` | `/items/{id}` | Get item by ID |
| `POST` | `/items/` | Create item |
| `PUT` | `/items/{id}` | Update item |
| `DELETE` | `/items/{id}` | Delete item |

> **Note:** Data is stored in-memory and resets on each server restart.

## Running Tests

```bash
# Run all tests
venv/Scripts/python -m pytest tests/ -v

# API tests only
venv/Scripts/python -m pytest tests/test_api_playwright.py -v

# Browser tests — headless (default)
venv/Scripts/python -m pytest tests/test_browser_playwright.py -v

# Browser tests — visible window
venv/Scripts/python -m pytest tests/test_browser_playwright.py --headed

# Slow motion demo (600ms between steps)
venv/Scripts/python -m pytest tests/test_browser_playwright.py --headed --slowmo=600
```

Tests spin up the server automatically on port `8001` via a session-scoped fixture — no manual server startup required.

## Windows: greenlet Pin

`greenlet>=3.2.0` crashes on some Windows machines with a DLL error. `requirements.txt` pins `greenlet==3.1.1`.

```bash
# Fix if broken:
venv/Scripts/pip install "greenlet==3.1.1" --force-reinstall
```

## Extending the Project

### New API endpoint
1. Add Pydantic models to `app/models/`
2. Add router file `app/routers/<name>.py`
3. Register in `app/main.py` with `app.include_router(...)`
4. Add API tests to `tests/test_api_playwright.py`

### New UI page
1. Add route returning `HTMLResponse` in `app/routers/frontend.py`
2. Add browser tests to `tests/test_browser_playwright.py`
