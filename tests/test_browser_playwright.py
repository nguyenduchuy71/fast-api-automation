"""
Browser automation tests using Playwright's Page fixture.
Run headed (visible browser):   pytest tests/test_browser_playwright.py --headed
Run headless (default/CI):       pytest tests/test_browser_playwright.py
Slow motion (watch steps):       pytest tests/test_browser_playwright.py --headed --slowmo=600
"""
import pytest
from playwright.sync_api import Page, expect


UI_PATH = "/ui"


class TestFrontendLoads:
    def test_page_title(self, page: Page, app_base_url: str):
        page.goto(app_base_url + UI_PATH)
        expect(page).to_have_title("FastAPI Demo")

    def test_headings_visible(self, page: Page, app_base_url: str):
        page.goto(app_base_url + UI_PATH)
        expect(page.get_by_role("heading", name="FastAPI Demo")).to_be_visible()
        expect(page.get_by_role("heading", name="Items")).to_be_visible()
        expect(page.get_by_role("heading", name="Users")).to_be_visible()

    def test_forms_visible(self, page: Page, app_base_url: str):
        page.goto(app_base_url + UI_PATH)
        expect(page.locator("#item-form")).to_be_visible()
        expect(page.locator("#user-form")).to_be_visible()


class TestItemsBrowser:
    def test_add_item_appears_in_list(self, page: Page, app_base_url: str):
        page.goto(app_base_url + UI_PATH)

        page.fill("#item-title", "Test Widget")
        page.fill("#item-price", "12.50")
        page.fill("#item-desc", "A test item")
        page.click("#item-form button[type='submit']")

        # Status message flashes green
        expect(page.locator("#status")).to_have_text("Item added!")

        # Item appears in list
        expect(page.locator("#item-list")).to_contain_text("Test Widget")
        expect(page.locator("#item-list")).to_contain_text("$12.50")

    def test_add_item_without_description(self, page: Page, app_base_url: str):
        page.goto(app_base_url + UI_PATH)

        page.fill("#item-title", "Minimal Item")
        page.fill("#item-price", "5.00")
        page.click("#item-form button[type='submit']")

        expect(page.locator("#item-list")).to_contain_text("Minimal Item")

    def test_delete_item(self, page: Page, app_base_url: str):
        page.goto(app_base_url + UI_PATH)

        # Add an item first
        page.fill("#item-title", "To Be Deleted")
        page.fill("#item-price", "1.00")
        page.click("#item-form button[type='submit']")
        expect(page.locator("#item-list")).to_contain_text("To Be Deleted")

        # Click its delete button
        item_li = page.locator("#item-list li", has_text="To Be Deleted")
        item_li.get_by_role("button", name="Delete").click()

        expect(page.locator("#status")).to_have_text("Item deleted")
        expect(page.locator("#item-list")).not_to_contain_text("To Be Deleted")

    def test_form_requires_title_and_price(self, page: Page, app_base_url: str):
        page.goto(app_base_url + UI_PATH)

        # Try submitting with empty fields — browser validation blocks it
        page.click("#item-form button[type='submit']")
        # Page stays on the same URL (form did not submit)
        assert page.url == app_base_url + UI_PATH


class TestUsersBrowser:
    def test_add_user_appears_in_list(self, page: Page, app_base_url: str):
        page.goto(app_base_url + UI_PATH)

        page.fill("#user-name",  "playwright_user")
        page.fill("#user-email", "playwright@example.com")
        page.fill("#user-pass",  "secret123")
        page.click("#user-form button[type='submit']")

        expect(page.locator("#status")).to_have_text("User added!")
        expect(page.locator("#user-list")).to_contain_text("playwright_user")
        expect(page.locator("#user-list")).to_contain_text("playwright@example.com")

    def test_password_not_visible(self, page: Page, app_base_url: str):
        page.goto(app_base_url + UI_PATH)
        pw_input = page.locator("#user-pass")
        assert pw_input.get_attribute("type") == "password"

    def test_delete_user(self, page: Page, app_base_url: str):
        page.goto(app_base_url + UI_PATH)

        page.fill("#user-name",  "delete_me")
        page.fill("#user-email", "deleteme@example.com")
        page.fill("#user-pass",  "secret123")
        page.click("#user-form button[type='submit']")
        expect(page.locator("#user-list")).to_contain_text("delete_me")

        user_li = page.locator("#user-list li", has_text="delete_me")
        user_li.get_by_role("button", name="Delete").click()

        expect(page.locator("#status")).to_have_text("User deleted")
        expect(page.locator("#user-list")).not_to_contain_text("delete_me")
