# FastAPI Automation Demo

> A FastAPI demo application with full Playwright test coverage at both the HTTP API level and real browser UI level.

---

## Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI + Pydantic v2 + Uvicorn |
| Testing | pytest + pytest-playwright + Playwright (Chromium) |
| Python | 3.11 |
| Venv | `C:/Project/venv/` |

---

## Project Structure

```
fast-api-automation/
│
├── app/
│   ├── main.py               # App entry point, routers registered here
│   ├── models/
│   │   ├── user.py           # UserCreate / UserResponse / UserUpdate
│   │   └── item.py           # ItemCreate / ItemResponse / ItemUpdate
│   └── routers/
│       ├── users.py          # CRUD  /users
│       ├── items.py          # CRUD  /items
│       └── frontend.py       # HTML UI served at GET /ui
│
└── tests/
    ├── conftest.py                    # Server spin-up + shared fixtures
    ├── test_api_playwright.py         # HTTP-level API tests
    └── test_browser_playwright.py     # Real Chromium browser tests
```

---

## Setup

```bash
# Install dependencies
venv/Scripts/pip install -r requirements.txt

# Install Playwright browser
venv/Scripts/playwright install chromium
```

---

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

---

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

---

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

> Tests spin up the server automatically on port `8001` via a session-scoped fixture — no manual server startup required.

---

## Windows: greenlet Pin

`greenlet>=3.2.0` crashes on some Windows machines with a DLL error. `requirements.txt` pins `greenlet==3.1.1`.

```bash
# Fix if broken:
venv/Scripts/pip install "greenlet==3.1.1" --force-reinstall
```

---

## Extending the Project

### New API endpoint

1. Add Pydantic models to `app/models/`
2. Add router file `app/routers/<name>.py`
3. Register in `app/main.py` with `app.include_router(...)`
4. Add API tests to `tests/test_api_playwright.py`

### New UI page

1. Add route returning `HTMLResponse` in `app/routers/frontend.py`
2. Add browser tests to `tests/test_browser_playwright.py`

---

## GSD Best Practices

### Project Setup

- Run `/gsd:map-codebase` **before** `/gsd:new-project` on existing codebases — gives Claude deep context for better planning
- Choose **YOLO mode** for solo work, **Interactive mode** when you want to review each decision

### Planning Cycle

- Always `/clear` between major phases to avoid context pollution
- Use `/gsd:discuss-phase N` before planning when you have a specific vision — don't skip it
- Run `/gsd:list-phase-assumptions N` to catch misalignments before Claude writes the whole plan
- Pass `--prd path/to/file.md` to `/gsd:plan-phase` if you already have written acceptance criteria

### Execution

- Let `/gsd:execute-phase` run fully — it updates `REQUIREMENTS.md`, `ROADMAP.md`, and `STATE.md` automatically
- Use `--wave N` to re-run a single failed wave rather than the whole phase

### Context Management

```
/gsd:new-project   → /clear
/gsd:plan-phase N  → /clear
/gsd:execute-phase N
```

> The `/clear` between steps is intentional — it prevents accumulated context from degrading output quality.

### Staying on Track

- `/gsd:progress` is your daily driver — run it first every session instead of `/gsd:resume-work`
- Capture distractions immediately: `/gsd:add-todo` keeps you moving without losing the idea
- Use `/gsd:insert-phase` for urgent unplanned work — never hack a phase mid-execution

### PR / Shipping

- Use `/gsd:pr-branch` before creating PRs — strips `.planning/` commits so reviewers see only code
- Run `/gsd:audit-uat` before `/gsd:complete-milestone` to catch untested items

### Model Profiles

| Profile | When to use |
|---------|-------------|
| `quality` | Complex architecture phases |
| `balanced` | Default — good cost/quality tradeoff |
| `budget` | Mechanical tasks, simple CRUD, docs |

Switch with: `/gsd:set-profile budget`

### Anti-Patterns to Avoid

- Don't skip `/clear` — stale context causes plan drift
- Don't run `/gsd:execute-phase` without a `PLAN.md` — use `/gsd:quick` for unplanned work instead
- Don't accumulate phases — run `/gsd:cleanup` after milestones or `.planning/phases/` grows unwieldy
