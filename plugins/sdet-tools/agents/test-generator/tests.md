# Tests: agentic-test-creator

## Scenarios

### 1. Jira epic → Playwright E2E tests
**Input:** User says "Generate tests for PROJ-1" and provides ACs for a login feature with 3 acceptance criteria.
**Framework detected:** playwright.config.py present in repo.
**Expected:** Agent loads jira-flow.md, uses Jira MCP or prompts for ACs, generates `test_login.py` with 3+ test functions using playwright.sync_api.Page. Output ends with `### Tests Generated` summary block.

### 2. PR number → REST API tests
**Input:** User says "Write tests for PR #42" where PR modifies a `/auth/login` route handler.
**Framework detected:** `swagger.yaml` found in repo root.
**Expected:** Agent loads pr-flow.md, runs `gh pr view 42`, identifies changed API file, generates `test_login_api.py` with happy path + error tests using `requests`. Docstrings cite PR #42.

### 3. QA engineer text → Selenium tests
**Input:** User pastes: "1. User can log in with valid credentials. 2. Invalid password shows error. 3. Locked account shows support message."
**Framework detected:** `selenium` in requirements.txt.
**Expected:** Agent loads qa-flow.md, parses 3 ACs, asks for base_url, generates `test_login.py` with 3 test functions using WebDriverWait. Each has `# QA:` traceability comment.

### 4. No framework detected → agent asks
**Input:** Fresh repo with no test config. User says "Create tests from these ACs: [paste]".
**Expected:** Agent detects no framework, asks exactly one question: "Which test type? (1) Playwright E2E  (2) Selenium E2E  (3) REST API  (4) pytest unit/integration". After user answers, proceeds with correct template.

### 5. QA text → pytest unit tests
**Input:** User pastes 3 ACs describing business logic for a `UserService`. Repo has `pytest.ini` present.
**Framework detected:** `pytest.ini` found in repo root.
**Expected:** Agent loads qa-flow.md, detects pytest framework, generates `conftest.py` with mock fixtures and `tests/unit/test_user_service.py` with a `class TestUserService` containing 3 test methods. Each method uses injected fixtures, has a docstring citing the AC, and uses `pytest.raises` for error cases. Output ends with `### Tests Generated` summary block.

## Rubric

| Criterion | Pass | Fail |
|-----------|------|------|
| Correct flow loaded | Agent loads the flow file matching the input type | Agent uses wrong flow or skips flow files |
| Framework detection | Correctly identifies framework from repo signals or asks | Silently picks wrong framework |
| Test function structure | Each test has a clear name, docstring citing source, and at least one assertion | Missing docstrings, vague names, or no assertions |
| Template fidelity | Generated code matches the loaded template patterns | Mixes frameworks, wrong API used (e.g. JS Playwright) |
| pytest fixture usage | pytest tests inject dependencies via fixtures; no inline instantiation of real dependencies | Real DB/network calls or hardcoded dependencies in test bodies |
| Output summary | Ends with `### Tests Generated` block with file, source, framework, coverage | Missing or incomplete summary |
| One question rule | If info is missing, asks exactly one focused question | Asks multiple questions at once or proceeds without needed info |

## Golden Set

### Golden 1 — Playwright E2E from QA text
**Input:** "1. User can log in with valid email and password — redirected to /dashboard. 2. Invalid password shows error message."

**Ideal output:**
```python
# test_login.py
import pytest
from playwright.sync_api import Page, expect

def test_valid_credentials_redirect_to_dashboard(page: Page):
    # QA: User can log in with valid email and password — redirected to /dashboard
    page.goto("/login")
    page.get_by_label("Email").fill("user@example.com")
    page.get_by_label("Password").fill("ValidPass123!")
    page.get_by_role("button", name="Log in").click()
    expect(page).to_have_url("/dashboard")

def test_invalid_password_shows_error(page: Page):
    # QA: Invalid password shows error message
    page.goto("/login")
    page.get_by_label("Email").fill("user@example.com")
    page.get_by_label("Password").fill("wrongpassword")
    page.get_by_role("button", name="Log in").click()
    expect(page.get_by_role("alert")).to_be_visible()
```

### Tests Generated
- File: `test_login.py`
- Source: QA input (2 acceptance criteria → 2 test functions)
- Framework: Playwright Python (pytest-playwright)
- Assumptions made: base_url configured in conftest.py, login form uses label="Email" and label="Password"

---

### Golden 2 — pytest unit tests from QA text

**Input:**
```
1. UserService.get_user returns the user dict when found.
2. UserService.get_user raises NotFoundError when the user does not exist.
3. UserService.create_user hashes the password before saving.
```
**Framework detected:** `pytest.ini` present.

**Ideal conftest.py:**
```python
# conftest.py
import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mock_repo():
    repo = MagicMock()
    repo.find_by_id.return_value = {"id": 1, "email": "user@example.com"}
    return repo
```

**Ideal test file:**
```python
# tests/unit/test_user_service.py
import pytest
from unittest.mock import MagicMock

from myapp.services.user_service import UserService, NotFoundError


class TestUserService:

    def test_get_user_returns_user_when_found(self, mock_repo):
        """
        Source: AC-1 — UserService.get_user returns the user dict when found.
        """
        service = UserService(repo=mock_repo)

        result = service.get_user(user_id=1)

        mock_repo.find_by_id.assert_called_once_with(1)
        assert result["id"] == 1

    def test_get_user_raises_not_found_when_missing(self, mock_repo):
        """
        Source: AC-2 — UserService.get_user raises NotFoundError when user does not exist.
        """
        mock_repo.find_by_id.return_value = None
        service = UserService(repo=mock_repo)

        with pytest.raises(NotFoundError):
            service.get_user(user_id=99)

    def test_create_user_hashes_password_before_saving(self, mock_repo):
        """
        Source: AC-3 — UserService.create_user hashes the password before saving.
        """
        service = UserService(repo=mock_repo)

        service.create_user(email="new@example.com", password="secret")

        saved = mock_repo.save.call_args[0][0]
        assert saved["password"] != "secret"
```

### Tests Generated
- Files: `conftest.py`, `tests/unit/test_user_service.py`
- Source: QA input (3 acceptance criteria → 3 test methods)
- Framework: pytest (unit/integration, fixture-based isolation)
- Pattern: Fixture-based isolation
- Coverage: get_user happy path, get_user not-found error, create_user password hashing
