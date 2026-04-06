# Selenium Python Templates — Page Object Model

Reference these patterns when generating Selenium E2E tests in Python using `selenium.webdriver` with pytest.
Tests follow the **Page Object Model (POM)** with locator constants and component classes.

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
│   └── alert_component.py
└── test_login.py
```

---

## 1. BasePage Class

```python
# pages/base_page.py
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """Base class for all page objects. Owns the WebDriver and a shared WebDriverWait."""

    TIMEOUT = 10

    def __init__(self, driver: WebDriver, base_url: str) -> None:
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.wait = WebDriverWait(driver, self.TIMEOUT)

    def navigate(self, path: str = "/") -> None:
        """Navigate to a path relative to the application base URL."""
        self.driver.get(f"{self.base_url}{path}")

    def wait_for_url(self, fragment: str) -> None:
        """Block until the current URL contains the given fragment."""
        self.wait.until(EC.url_contains(fragment))

    def wait_for_element_visible(self, locator: tuple):
        """Return the element once it is visible in the viewport."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_for_element_clickable(self, locator: tuple):
        """Return the element once it is clickable."""
        return self.wait.until(EC.element_to_be_clickable(locator))
```

---

## 2. Page Object — LoginPage

Locators are declared as class-level constants using `(By.*, "selector")` tuples, keeping
selectors in one place and out of individual test methods.

```python
# pages/login_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage


class LoginPage(BasePage):
    """Encapsulates all interactions with the /login page."""

    PATH = "/login"

    # Locator constants — update selectors here, nowhere else
    EMAIL_INPUT    = (By.CSS_SELECTOR, "input[aria-label='Email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[aria-label='Password']")
    SUBMIT_BUTTON  = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_ALERT    = (By.CSS_SELECTOR, "[role='alert']")

    def __init__(self, driver: WebDriver, base_url: str) -> None:
        super().__init__(driver, base_url)

    def navigate(self) -> None:  # type: ignore[override]
        super().navigate(self.PATH)

    def login(self, email: str, password: str) -> None:
        """Navigate to login, fill credentials, and submit the form."""
        self.navigate()
        self.wait_for_element_visible(self.EMAIL_INPUT).send_keys(email)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.wait_for_element_clickable(self.SUBMIT_BUTTON).click()

    def get_error_text(self) -> str:
        """Return the text content of the error alert once visible."""
        element = self.wait_for_element_visible(self.ERROR_ALERT)
        return element.text
```

---

## 3. Page Object — DashboardPage

```python
# pages/dashboard_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage


class DashboardPage(BasePage):
    """Encapsulates assertions and interactions on the /dashboard page."""

    PATH = "/dashboard"
    WELCOME_HEADING = (By.CSS_SELECTOR, "h1")

    def __init__(self, driver: WebDriver, base_url: str) -> None:
        super().__init__(driver, base_url)

    def expect_loaded(self) -> None:
        """Assert the dashboard URL and the welcome heading are present."""
        self.wait_for_url(self.PATH)
        self.wait_for_element_visible(self.WELCOME_HEADING)
        assert self.PATH in self.driver.current_url
```

---

## 4. Component Class

```python
# components/alert_component.py
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AlertComponent:
    """Reusable component for banner/alert elements rendered anywhere in the app."""

    TIMEOUT = 10

    def __init__(self, driver: WebDriver, selector: str = "[role='alert']") -> None:
        self.driver = driver
        self.locator = (By.CSS_SELECTOR, selector)
        self.wait = WebDriverWait(driver, self.TIMEOUT)

    def expect_visible(self) -> None:
        element = self.wait.until(EC.visibility_of_element_located(self.locator))
        assert element.is_displayed()

    def expect_text(self, text: str) -> None:
        self.wait.until(
            EC.text_to_be_present_in_element(self.locator, text)
        )

    @property
    def text(self) -> str:
        return self.driver.find_element(*self.locator).text
```

---

## 5. conftest.py — Fixtures

```python
# conftest.py
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.environ.get("BASE_URL", "http://localhost:3000")


@pytest.fixture(scope="function")
def driver():
    """
    Headless Chrome WebDriver per test function.
    Use explicit WebDriverWait — never implicit waits or time.sleep.
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    drv = webdriver.Chrome(options=options)
    drv.implicitly_wait(0)  # always use explicit waits
    yield drv
    drv.quit()
```

---

## 6. Pytest Integration Patterns

### Reusing existing fixtures

Before generating any `conftest.py` content, **read the existing file** and use its fixture names and scopes verbatim. Never overwrite existing fixtures.

```python
# If conftest.py already defines these, reference them by name — do not redefine:
# base_url, driver, authenticated_driver
```

If the project already has an authenticated `driver` fixture, use it directly:

```python
def test_dashboard_shows_username(self, authenticated_driver, base_url):
    """Source: AC-4 — authenticated user sees their name in the nav."""
    dashboard = DashboardPage(authenticated_driver, base_url)
    dashboard.navigate()
    dashboard.wait_for_element_visible(DashboardPage.USERNAME_NAV)
```

### Authenticated driver fixture (add to conftest.py only if not already present)

```python
@pytest.fixture(scope="session")
def authenticated_driver(base_url):
    """
    Log in once per session.
    Use for tests that require an authenticated user.
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    drv = webdriver.Chrome(options=options)
    drv.implicitly_wait(0)

    login_page = LoginPage(drv, base_url)
    login_page.login(
        os.environ.get("TEST_USER_EMAIL", "user@example.com"),
        os.environ.get("TEST_USER_PASSWORD", "ValidPass123!"),
    )
    WebDriverWait(drv, 10).until(EC.url_contains("/dashboard"))
    yield drv
    drv.quit()
```

### Parametrize — data-driven UI tests

Use `@pytest.mark.parametrize` when the same UI flow must be exercised with multiple input combinations.

```python
@pytest.mark.parametrize("email,password,expected_error", [
    ("user@example.com", "wrongpass",   "Invalid credentials"),
    ("",                 "ValidPass1!", "Email is required"),
    ("user@example.com", "",            "Password is required"),
])
def test_login_error_cases(self, driver, base_url, email, password, expected_error):
    """
    Source: AC-2, AC-3, AC-4 — various invalid inputs each show a specific inline error.
    """
    login_page = LoginPage(driver, base_url)
    login_page.login(email, password)
    assert expected_error in login_page.get_error_text()
```

### Pytest markers

Read `pytest.ini` or `[tool.pytest.ini_options]` in `pyproject.toml` for declared markers before adding them. Only apply markers that are already registered.

```python
@pytest.mark.smoke
def test_valid_login_redirects_to_dashboard(self, driver, base_url):
    """Source: AC-1 — critical path smoke test."""
    ...

@pytest.mark.regression
@pytest.mark.parametrize("password", ["", " ", "short"])
def test_weak_passwords_blocked(self, driver, base_url, password):
    """Source: AC-5 — weak or empty passwords are rejected at the form level."""
    ...
```

---

## 7. Locator Strategies

```python
from selenium.webdriver.common.by import By

# 1. CSS selector — preferred for readability
(By.CSS_SELECTOR, "input[aria-label='Email']")
(By.CSS_SELECTOR, "button[type='submit']")
(By.CSS_SELECTOR, "[data-testid='submit-button']")
(By.CSS_SELECTOR, ".alert-error")

# 2. ID — when the element has a stable unique ID
(By.ID, "email-input")

# 3. Name — for form inputs with a name attribute
(By.NAME, "password")

# 4. XPath — last resort; avoid when CSS is sufficient
(By.XPATH, "//button[contains(text(), 'Log in')]")
(By.XPATH, "//label[text()='Email']/following-sibling::input")
```

---

## 8. Wait Patterns

Always use `WebDriverWait` with `expected_conditions`. Never use `time.sleep`.

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TIMEOUT = 10

# Element visible
WebDriverWait(driver, TIMEOUT).until(EC.visibility_of_element_located(locator))

# Element clickable before interacting
WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable(locator)).click()

# URL contains fragment
WebDriverWait(driver, TIMEOUT).until(EC.url_contains("/dashboard"))

# Text present in element
WebDriverWait(driver, TIMEOUT).until(
    EC.text_to_be_present_in_element(locator, "Invalid credentials")
)

# Element disappears (e.g. loading spinner)
WebDriverWait(driver, TIMEOUT).until(EC.invisibility_of_element_located(locator))
```

---

## 9. Assertion Patterns

```python
# URL
assert "/dashboard" in driver.current_url

# Element visibility (after explicit wait)
assert element.is_displayed()

# Text
assert "Invalid credentials" in element.text

# Count
items = driver.find_elements(By.CSS_SELECTOR, ".result-item")
assert len(items) == 5

# Input value
assert driver.find_element(*EMAIL_INPUT).get_attribute("value") == "user@example.com"

# Page title
assert "Dashboard" in driver.title
```

---

## 10. Complete Example — Login Feature (POM)

```python
# test_login.py
import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


class TestLogin:
    """Tests for the login feature (QA AC-1 through AC-3)."""

    def test_valid_credentials_redirect_to_dashboard(self, driver, base_url):
        """
        Source: QA AC-1
        Verifies: A user with valid credentials lands on /dashboard.
        """
        login_page = LoginPage(driver, base_url)
        login_page.login("user@example.com", "ValidPass123!")
        DashboardPage(driver, base_url).expect_loaded()

    def test_invalid_password_shows_error_message(self, driver, base_url):
        """
        Source: QA AC-2
        Verifies: An incorrect password surfaces a visible error message.
        """
        login_page = LoginPage(driver, base_url)
        login_page.login("user@example.com", "wrongpassword")
        assert "Invalid credentials" in login_page.get_error_text()

    def test_locked_account_shows_support_message(self, driver, base_url):
        """
        Source: QA AC-3
        Verifies: A locked account login attempt surfaces a support contact message.
        """
        login_page = LoginPage(driver, base_url)
        login_page.login("locked@example.com", "AnyPassword1!")
        assert "support" in login_page.get_error_text().lower()
```
