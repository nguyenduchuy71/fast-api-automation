"""
Playwright-based API automation tests for the FastAPI application.
These tests use Playwright's APIRequestContext for HTTP-level testing,
which is ideal for REST API automation.
"""
import pytest
from playwright.sync_api import APIRequestContext, Playwright


@pytest.fixture(scope="session")
def api_context(playwright: Playwright, app_base_url: str) -> APIRequestContext:
    context = playwright.request.new_context(base_url=app_base_url)
    yield context
    context.dispose()


class TestRoot:
    def test_root_returns_ok(self, api_context: APIRequestContext):
        response = api_context.get("/")
        assert response.ok
        body = response.json()
        assert body["status"] == "ok"
        assert "message" in body

    def test_health_check(self, api_context: APIRequestContext):
        response = api_context.get("/health")
        assert response.ok
        assert response.json()["status"] == "healthy"


class TestUsers:
    def test_list_users_empty(self, api_context: APIRequestContext):
        response = api_context.get("/users/")
        assert response.ok
        assert response.json() == []

    def test_create_user(self, api_context: APIRequestContext):
        payload = {
            "email": "alice@example.com",
            "username": "alice",
            "password": "secret123",
        }
        response = api_context.post("/users/", data=payload)
        assert response.status == 201
        body = response.json()
        assert body["username"] == "alice"
        assert body["email"] == "alice@example.com"
        assert "id" in body
        assert "password" not in body  # password must never leak

    def test_get_user(self, api_context: APIRequestContext):
        # Create first
        response = api_context.post(
            "/users/",
            data={"email": "bob@example.com", "username": "bob", "password": "secret123"},
        )
        user_id = response.json()["id"]

        # Fetch it
        response = api_context.get(f"/users/{user_id}")
        assert response.ok
        assert response.json()["username"] == "bob"

    def test_get_nonexistent_user_returns_404(self, api_context: APIRequestContext):
        response = api_context.get("/users/99999")
        assert response.status == 404

    def test_update_user(self, api_context: APIRequestContext):
        response = api_context.post(
            "/users/",
            data={"email": "carol@example.com", "username": "carol", "password": "secret123"},
        )
        user_id = response.json()["id"]

        response = api_context.put(
            f"/users/{user_id}",
            data={"username": "carol_updated"},
        )
        assert response.ok
        assert response.json()["username"] == "carol_updated"

    def test_delete_user(self, api_context: APIRequestContext):
        response = api_context.post(
            "/users/",
            data={"email": "dave@example.com", "username": "dave", "password": "secret123"},
        )
        user_id = response.json()["id"]

        response = api_context.delete(f"/users/{user_id}")
        assert response.status == 204

        response = api_context.get(f"/users/{user_id}")
        assert response.status == 404


class TestItems:
    def test_list_items_empty(self, api_context: APIRequestContext):
        response = api_context.get("/items/")
        assert response.ok
        assert response.json() == []

    def test_create_item(self, api_context: APIRequestContext):
        payload = {"title": "Widget", "description": "A nice widget", "price": 9.99}
        response = api_context.post("/items/", data=payload)
        assert response.status == 201
        body = response.json()
        assert body["title"] == "Widget"
        assert body["price"] == 9.99
        assert "id" in body

    def test_get_item(self, api_context: APIRequestContext):
        response = api_context.post(
            "/items/", data={"title": "Gadget", "price": 19.99}
        )
        item_id = response.json()["id"]

        response = api_context.get(f"/items/{item_id}")
        assert response.ok
        assert response.json()["title"] == "Gadget"

    def test_get_nonexistent_item_returns_404(self, api_context: APIRequestContext):
        response = api_context.get("/items/99999")
        assert response.status == 404

    def test_update_item(self, api_context: APIRequestContext):
        response = api_context.post(
            "/items/", data={"title": "OldTitle", "price": 5.0}
        )
        item_id = response.json()["id"]

        response = api_context.put(f"/items/{item_id}", data={"price": 7.5})
        assert response.ok
        assert response.json()["price"] == 7.5

    def test_delete_item(self, api_context: APIRequestContext):
        response = api_context.post(
            "/items/", data={"title": "ToDelete", "price": 1.0}
        )
        item_id = response.json()["id"]

        response = api_context.delete(f"/items/{item_id}")
        assert response.status == 204

        response = api_context.get(f"/items/{item_id}")
        assert response.status == 404

    def test_create_item_invalid_price(self, api_context: APIRequestContext):
        response = api_context.post(
            "/items/", data={"title": "Bad", "price": -1}
        )
        assert response.status == 422  # validation error
