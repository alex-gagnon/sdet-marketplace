# Playwright Python Templates — Page Object Model

Reference these patterns when generating Playwright E2E tests in Python using `playwright.sync_api`.
Tests follow the **Page Object Model (POM)** with component classes for reusable UI elements.

---

## Directory Structure

```
tests/
├── conftest.py
├── pages/
│   ├── __init__.py
│   ├── base_page.py
│   ├── login_page.py
│   └── dashboard_page.py
├── components/
│   ├── __init__.py
│   ├── nav_bar.py
│   └── alert_component.py
└── test_login.py
```

---

## 1. BasePage Class

All page objects extend `BasePage`, which owns the `Page` instance and exposes common navigation helpers.

```python
# pages/base_page.py
from playwright.sync_api import Page, expect


class BasePage:
    """Base class for all page objects. Wraps a Playwright Page instance."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def navigate(self, path: str = "/") -> None:
        """Navigate to a path relative to the application root."""
        self.page.goto(path)

    def wait_for_url(self, pattern: str) -> None:
        """Wait until the current URL matches the given glob or regex pattern."""
        self.page.wait_for_url(pattern)

    def reload(self) -> None:
        self.page.reload()
```

---

## 2. Page Object — LoginPage

```python
# pages/login_page.py
from playwright.sync_api import Page, Locator, expect
from .base_page import BasePage


class LoginPage(BasePage):
    """Encapsulates all interactions with the /login page."""

    PATH = "/login"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.email_input: Locator = page.get_by_label("Email")
        self.password_input: Locator = page.get_by_label("Password")
        self.submit_button: Locator = page.get_by_role("button", name="Log in")
        self.error_alert: Locator = page.get_by_role("alert")

    def navigate(self) -> None:  # type: ignore[override]
        super().navigate(self.PATH)

    def login(self, email: str, password: str) -> None:
        """Fill credentials and submit the login form."""
        self.navigate()
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()

    def expect_redirected_to_dashboard(self) -> None:
        expect(self.page).to_have_url("/dashboard")

    def expect_error(self, text: str) -> None:
        expect(self.error_alert).to_be_visible()
        expect(self.error_alert).to_contain_text(text)
```

---

## 3. Page Object — DashboardPage

```python
# pages/dashboard_page.py
from playwright.sync_api import Page, Locator, expect
from .base_page import BasePage


class DashboardPage(BasePage):
    """Encapsulates assertions and interactions on the /dashboard page."""

    PATH = "/dashboard"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.welcome_heading: Locator = page.get_by_role("heading", name="Welcome")
        self.nav_bar: Locator = page.get_by_role("navigation")

    def expect_loaded(self) -> None:
        expect(self.page).to_have_url(self.PATH)
        expect(self.welcome_heading).to_be_visible()
```

---

## 4. Component Class

Components are reusable UI fragments shared across multiple page objects.

```python
# components/alert_component.py
from playwright.sync_api import Page, Locator, expect


class AlertComponent:
    """Reusable component for banner/alert elements rendered anywhere in the app."""

    def __init__(self, page: Page, locator_selector: str = "[role='alert']") -> None:
        self.locator: Locator = page.locator(locator_selector)

    def expect_visible(self) -> None:
        expect(self.locator).to_be_visible()

    def expect_text(self, text: str) -> None:
        expect(self.locator).to_contain_text(text)

    def expect_hidden(self) -> None:
        expect(self.locator).to_be_hidden()

    @property
    def text(self) -> str:
        return self.locator.inner_text()
```

---

## 5. conftest.py — Fixtures

```python
# conftest.py
import os
import pytest
from playwright.sync_api import Playwright, BrowserContext, Page


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.environ.get("BASE_URL", "http://localhost:3000")


@pytest.fixture(scope="session")
def browser_context(playwright: Playwright, base_url: str) -> BrowserContext:
    """Single browser context shared across the test session."""
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(base_url=base_url)
    yield context
    context.close()
    browser.close()


@pytest.fixture()
def page(browser_context: BrowserContext) -> Page:
    """Fresh page per test; closed automatically after the test."""
    p = browser_context.new_page()
    yield p
    p.close()


@pytest.fixture(scope="session")
def authenticated_context(playwright: Playwright, base_url: str) -> BrowserContext:
    """
    Log in once per session and store browser storage state.
    Use this fixture for tests that require an authenticated user.
    """
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(base_url=base_url)
    setup_page = context.new_page()
    setup_page.goto(f"{base_url}/login")
    setup_page.get_by_label("Email").fill(os.environ.get("TEST_USER_EMAIL", "user@example.com"))
    setup_page.get_by_label("Password").fill(os.environ.get("TEST_USER_PASSWORD", "ValidPass123!"))
    setup_page.get_by_role("button", name="Log in").click()
    setup_page.wait_for_url("**/dashboard")
    setup_page.close()
    yield context
    context.close()
    browser.close()


@pytest.fixture()
def authenticated_page(authenticated_context: BrowserContext) -> Page:
    """Page with an already-authenticated session."""
    p = authenticated_context.new_page()
    yield p
    p.close()
```

---

## 6. Pytest Integration Patterns

### Reusing existing fixtures

Before generating any `conftest.py` content, **read the existing file** and use its fixture names and scopes verbatim. Never overwrite existing fixtures.

```python
# If conftest.py already defines these, import and reference them by name — do not redefine:
# base_url, page, browser_context, authenticated_page, authenticated_context
```

If the existing `conftest.py` defines an `authenticated_page` fixture, use it directly in tests that require auth:

```python
def test_dashboard_shows_username(self, authenticated_page: Page):
    """Source: AC-4 — authenticated user sees their name in the nav."""
    dashboard = DashboardPage(authenticated_page)
    dashboard.navigate()
    expect(authenticated_page.get_by_role("navigation")).to_contain_text("Alice")
```

### Parametrize — data-driven UI tests

Use `@pytest.mark.parametrize` when the same UI flow must be exercised with multiple input combinations. Never repeat the same page interaction logic in separate test methods when only the data differs.

```python
@pytest.mark.parametrize("email,password,expected_error", [
    ("user@example.com", "wrongpass",   "Invalid credentials"),
    ("",                 "ValidPass1!", "Email is required"),
    ("user@example.com", "",            "Password is required"),
])
def test_login_error_cases(self, page: Page, email: str, password: str, expected_error: str):
    """
    Source: AC-2, AC-3, AC-4 — various invalid inputs each show a specific error.
    """
    login_page = LoginPage(page)
    login_page.login(email, password)
    login_page.expect_error(expected_error)
```

Parametrize IDs: use `ids=` when the default string representation is unclear.

```python
@pytest.mark.parametrize("role,destination", [
    ("admin",  "/admin/dashboard"),
    ("viewer", "/dashboard"),
], ids=["admin-redirected", "viewer-redirected"])
def test_post_login_redirect_by_role(self, page: Page, role: str, destination: str):
    """Source: AC-5 — each role lands on their designated page after login."""
    ...
```

### Pytest markers

Read `pytest.ini` or `[tool.pytest.ini_options]` in `pyproject.toml` for declared markers before adding them. Only apply markers that are already registered to avoid warnings.

```python
@pytest.mark.smoke
def test_valid_login_redirects_to_dashboard(self, page: Page):
    """Source: AC-1 — critical path smoke test."""
    ...

@pytest.mark.regression
@pytest.mark.parametrize("password", ["", " ", "short"])
def test_weak_passwords_blocked(self, page: Page, password: str):
    """Source: AC-6 — weak passwords are rejected."""
    ...
```

### Custom fixture in conftest.py (only if not already present)

Only add these to `conftest.py` when they do not already exist.

```python
@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """Return a navigated LoginPage instance."""
    lp = LoginPage(page)
    lp.navigate()
    return lp
```

---

## 7. Locator Strategies

Prefer locators in this order (most accessible → least):

```python
# 1. By role — most robust, matches accessible name
page.get_by_role("button", name="Submit")
page.get_by_role("heading", name="Welcome")
page.get_by_role("link", name="Sign up")

# 2. By label — for form inputs
page.get_by_label("Email")
page.get_by_label("Password")

# 3. By visible text
page.get_by_text("Order placed successfully")

# 4. By placeholder
page.get_by_placeholder("Search products...")

# 5. By test ID (when app exposes data-testid)
page.get_by_test_id("submit-button")

# Last resort — CSS or XPath (avoid; break on style changes)
# page.locator("button.submit-btn")
# page.locator("//button[@type='submit']")
```

---

## 8. Assertion Patterns

```python
from playwright.sync_api import Page, expect

# Page-level
# IMPORTANT: to_have_url requires a full URL string, a substring, or re.compile()
# Never use glob patterns like "**/path" — they are not supported and will fail
import re
expect(page).to_have_url("http://localhost:3000/dashboard")   # exact match
expect(page).to_have_url(re.compile(r"/dashboard$"))          # regex — preferred for path checks
expect(page).to_have_title("Dashboard — MyApp")

# Locator-level
expect(locator).to_be_visible()
expect(locator).to_be_hidden()
expect(locator).to_contain_text("Success")
expect(locator).to_have_text("Exact text")   # exact match
expect(locator).to_have_value("user@example.com")  # input value
expect(locator).to_be_enabled()
expect(locator).to_be_disabled()
expect(locator).to_be_checked()              # checkbox / radio

# Count
expect(page.get_by_role("listitem")).to_have_count(5)
```

---

## 9. Complete Example — Login Feature (POM)

```python
# test_login.py
import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


class TestLogin:
    """Tests for the login feature (QA AC-1 through AC-3)."""

    def test_valid_credentials_redirect_to_dashboard(self, page: Page):
        """
        Source: QA AC-1
        Verifies: A user with valid credentials lands on /dashboard.
        """
        login_page = LoginPage(page)
        login_page.login("user@example.com", "ValidPass123!")
        login_page.expect_redirected_to_dashboard()
        DashboardPage(page).expect_loaded()

    def test_invalid_password_shows_error_alert(self, page: Page):
        """
        Source: QA AC-2
        Verifies: An incorrect password surfaces a visible error alert.
        """
        login_page = LoginPage(page)
        login_page.login("user@example.com", "wrongpassword")
        login_page.expect_error("Invalid credentials")

    def test_empty_email_keeps_user_on_login_page(self, page: Page):
        """
        Source: QA AC-3
        Verifies: Submitting without an email does not navigate away from /login.
        """
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.password_input.fill("SomePassword1!")
        login_page.submit_button.click()
        login_page.expect_error("")  # any validation message
        # page stays on /login
        import re
        from playwright.sync_api import expect
        expect(page).to_have_url(re.compile(r"/login"))
```
