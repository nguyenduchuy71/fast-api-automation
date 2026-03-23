import pytest
import uvicorn
import threading
import time
import httpx
from app.main import app


SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8001
BASE_URL = f"http://{SERVER_HOST}:{SERVER_PORT}"


def run_server():
    uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT, log_level="error")


@pytest.fixture(scope="session", autouse=True)
def start_server():
    """Start the FastAPI server in a background thread for Playwright tests."""
    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()
    # Wait until the server is ready
    for _ in range(20):
        try:
            httpx.get(f"{BASE_URL}/health")
            break
        except Exception:
            time.sleep(0.3)
    yield
    # Thread is daemon so it stops with the process


@pytest.fixture(scope="session")
def app_base_url():
    return BASE_URL
