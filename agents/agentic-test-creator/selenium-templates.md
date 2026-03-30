# Selenium Python Templates

Reference these patterns when generating Selenium E2E tests in Python using `selenium.webdriver` with pytest.

---

## 1. Basic Test Function Pattern

```python
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_descriptive_behavior_name(driver, base_url):
    """
    Source: <Jira key AC-N | PR #N | QA: original AC text>
    Verifies: <brief one-line description of the behavior under test>
    """
    driver.get(f"{base_url}/target-path")
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    )
    button.click()
    WebDriverWait(driver, 10).until(EC.url_contains("/expected-path"))
    assert "/expected-path" in driver.current_url
```

---

## 2. conftest.py — Chrome WebDriver Setup (Headless)

```python
# conftest.py
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


@pytest.fixture(scope="session")
def base_url() -> str:
    """Return the base URL for the application under test."""
    return os.environ.get("BASE_URL", "http://localhost:3000")


@pytest.fixture(scope="function")
def driver():
    """
    Provide a headless Chrome WebDriver instance for each test function.
    Quits the driver after the test completes.
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    drv = webdriver.Chrome(options=options)
    drv.implicitly_wait(0)  # Rely on explicit WebDriverWait — never implicit waits
    yield drv
    drv.quit()
```

---

## 3. Wait Pattern — WebDriverWait + expected_conditions

Always use `WebDriverWait` with `expected_conditions`. Never use `time.sleep`.

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TIMEOUT = 10  # seconds

# Wait for an element to be visible
element = WebDriverWait(driver, TIMEOUT).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-error"))
)

# Wait for an element to be clickable before interacting
button = WebDriverWait(driver, TIMEOUT).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
)
button.click()

# Wait for URL to change
WebDriverWait(driver, TIMEOUT).until(EC.url_contains("/dashboard"))

# Wait for text to be present in an element
WebDriverWait(driver, TIMEOUT).until(
    EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".alert"), "Invalid credentials")
)

# Wait for an element to disappear
WebDriverWait(driver, TIMEOUT).until(
    EC.invisibility_of_element_located((By.CSS_SELECTOR, ".loading-spinner"))
)
```

---

## 4. Locator Strategies

Prefer CSS selectors for readability. Fall back to XPath only when CSS cannot express the selector.

```python
# 1. CSS selector — preferred
driver.find_element(By.CSS_SELECTOR, "input[aria-label='Email']")
driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
driver.find_element(By.CSS_SELECTOR, ".alert-error")
driver.find_element(By.CSS_SELECTOR, "#login-form")

# 2. By ID — use when the element has a stable, unique ID
driver.find_element(By.ID, "email-input")

# 3. By NAME — for form inputs with a name attribute
driver.find_element(By.NAME, "password")

# 4. By XPATH — last resort when CSS is insufficient
driver.find_element(By.XPATH, "//button[contains(text(), 'Log in')]")
driver.find_element(By.XPATH, "//label[text()='Email']/following-sibling::input")

# Tip: use data-testid attributes when the app exposes them
driver.find_element(By.CSS_SELECTOR, "[data-testid='submit-button']")
```

---

## 5. Assertion Patterns

```python
# URL assertion
assert "/dashboard" in driver.current_url

# Element visibility
element = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert"))
)
assert element.is_displayed()

# Text content
assert "Invalid credentials" in element.text

# Element presence (exists in DOM, may not be visible)
elements = driver.find_elements(By.CSS_SELECTOR, ".result-item")
assert len(elements) == 5

# Input value
email_input = driver.find_element(By.CSS_SELECTOR, "input[aria-label='Email']")
assert email_input.get_attribute("value") == "user@example.com"

# Page title
assert "Dashboard" in driver.title
```

---

## 6. Complete Example — Login Feature

```python
# test_login.py
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TIMEOUT = 10


def test_valid_credentials_redirect_to_dashboard(driver, base_url):
    """
    Source: QA AC-1
    Verifies: A user with valid credentials is redirected to /dashboard after login.
    """
    # QA: User can log in with valid credentials
    driver.get(f"{base_url}/login")
    WebDriverWait(driver, TIMEOUT).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input[aria-label='Email']"))
    ).send_keys("user@example.com")
    driver.find_element(By.CSS_SELECTOR, "input[aria-label='Password']").send_keys("ValidPass123!")
    WebDriverWait(driver, TIMEOUT).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    ).click()
    WebDriverWait(driver, TIMEOUT).until(EC.url_contains("/dashboard"))
    assert "/dashboard" in driver.current_url


def test_invalid_password_shows_error_message(driver, base_url):
    """
    Source: QA AC-2
    Verifies: An incorrect password causes a visible error message to appear.
    """
    # QA: Invalid password shows error message
    driver.get(f"{base_url}/login")
    WebDriverWait(driver, TIMEOUT).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input[aria-label='Email']"))
    ).send_keys("user@example.com")
    driver.find_element(By.CSS_SELECTOR, "input[aria-label='Password']").send_keys("wrongpassword")
    WebDriverWait(driver, TIMEOUT).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    ).click()
    error = WebDriverWait(driver, TIMEOUT).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-error"))
    )
    assert error.is_displayed()
    assert "Invalid credentials" in error.text


def test_locked_account_shows_support_message(driver, base_url):
    """
    Source: QA AC-3
    Verifies: A locked account login attempt surfaces a support contact message.
    """
    # QA: Locked account shows support message
    driver.get(f"{base_url}/login")
    WebDriverWait(driver, TIMEOUT).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input[aria-label='Email']"))
    ).send_keys("locked@example.com")
    driver.find_element(By.CSS_SELECTOR, "input[aria-label='Password']").send_keys("AnyPassword1!")
    WebDriverWait(driver, TIMEOUT).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    ).click()
    message = WebDriverWait(driver, TIMEOUT).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-error"))
    )
    assert message.is_displayed()
    assert "support" in message.text.lower()
```
