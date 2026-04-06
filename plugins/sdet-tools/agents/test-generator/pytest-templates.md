# pytest Unit & Integration Test Templates

Use these patterns when generating **pure pytest unit or integration tests** — i.e., when the codebase has no Playwright, Selenium, or REST API test signals, but has a pytest setup (pytest.ini, pyproject.toml [tool.pytest.ini_options], or setup.cfg [tool:pytest]).

---

## Project Layout

```
tests/
├── conftest.py          # Shared fixtures
├── unit/
│   └── test_<module>.py
└── integration/
    └── test_<feature>.py
src/
└── <package>/
    └── <module>.py
```

---

## conftest.py — Shared Fixtures

```python
# conftest.py
import pytest
from unittest.mock import MagicMock

# --- Session-scoped fixtures (expensive setup, shared across all tests) ---

@pytest.fixture(scope="session")
def db_connection():
    """Real or stubbed DB connection reused for the whole test session."""
    conn = _create_test_db()
    yield conn
    conn.close()


# --- Function-scoped fixtures (fresh per test, safest default) ---

@pytest.fixture
def user_data():
    return {"id": 1, "email": "user@example.com", "role": "admin"}


@pytest.fixture
def mock_repo():
    """Return a MagicMock shaped like the repository interface."""
    repo = MagicMock()
    repo.find_by_id.return_value = {"id": 1, "email": "user@example.com"}
    return repo
```

**Rules:**
- Default fixture scope is **function** (fresh state per test).
- Use `scope="session"` only for truly shared, read-only resources (DB connections, config).
- Never use `scope="module"` unless you have a specific reason — it creates hidden coupling.

---

## Unit Test File Structure

```python
# tests/unit/test_user_service.py
import pytest
from unittest.mock import MagicMock, patch, call

from myapp.services.user_service import UserService


class TestUserService:
    """Unit tests for UserService — all external dependencies mocked."""

    def test_get_user_returns_user_when_found(self, mock_repo):
        """
        Source: AC-1 — system retrieves user by ID.
        """
        service = UserService(repo=mock_repo)

        result = service.get_user(user_id=1)

        mock_repo.find_by_id.assert_called_once_with(1)
        assert result["id"] == 1
        assert result["email"] == "user@example.com"

    def test_get_user_raises_not_found_when_missing(self, mock_repo):
        """
        Source: AC-2 — missing user raises NotFoundError.
        """
        mock_repo.find_by_id.return_value = None
        service = UserService(repo=mock_repo)

        with pytest.raises(NotFoundError, match="User 99 not found"):
            service.get_user(user_id=99)

    def test_create_user_hashes_password_before_saving(self, mock_repo):
        """
        Source: AC-3 — password must be hashed, never stored in plaintext.
        """
        service = UserService(repo=mock_repo)

        service.create_user(email="new@example.com", password="secret")

        saved = mock_repo.save.call_args[0][0]
        assert saved["password"] != "secret"
        assert saved["password"].startswith("$2b$")  # bcrypt prefix
```

**Rules:**
- Group tests in `class Test<Subject>` — one class per module/class under test.
- Never import the real collaborator in a unit test — inject via constructor or `patch`.
- Arrange → Act → Assert with a blank line separating each phase.
- Test function names: `test_<method>_<condition>_<expected_outcome>` in snake_case.

---

## Parametrize Pattern

Use `@pytest.mark.parametrize` when the same behaviour is exercised with multiple inputs.

```python
@pytest.mark.parametrize("email,valid", [
    ("user@example.com", True),
    ("user@", False),
    ("", False),
    ("no-at-sign", False),
])
def test_validate_email(email, valid):
    """
    Source: AC-4 — email validation rejects malformed addresses.
    """
    assert validate_email(email) is valid
```

**Rules:**
- Use parametrize instead of looping inside a test — pytest reports each case individually.
- Keep the parametrize ID readable; for complex objects use `ids=` parameter.
- Never put assertions inside helper functions; always assert in the test body.

---

## Mocking Patterns

### Patch via decorator
```python
@patch("myapp.services.email_service.smtplib.SMTP")
def test_sends_welcome_email(mock_smtp, user_data):
    """Source: AC-5 — welcome email sent on registration."""
    send_welcome_email(user_data["email"])
    mock_smtp.return_value.__enter__.return_value.sendmail.assert_called_once()
```

### Patch via context manager (preferred for short patches)
```python
def test_get_current_time_uses_utc():
    """Source: AC-6 — timestamps are always UTC."""
    fixed = datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)
    with patch("myapp.utils.time.datetime") as mock_dt:
        mock_dt.now.return_value = fixed
        result = get_current_timestamp()
    assert result == fixed
```

### MagicMock attribute chaining
```python
def test_audit_log_records_actor(mock_repo):
    """Source: AC-7 — audit log captures user ID."""
    mock_repo.audit.log.return_value = {"id": 42}
    service = AuditService(repo=mock_repo)

    service.record_action(actor_id=7, action="delete")

    mock_repo.audit.log.assert_called_once_with(actor=7, action="delete")
```

---

## Integration Test File Structure

Integration tests exercise multiple real components together; only external I/O (network, disk, time) is stubbed.

```python
# tests/integration/test_user_registration.py
import pytest

from myapp.services.user_service import UserService
from myapp.repositories.user_repo import UserRepository


class TestUserRegistration:
    """Integration tests — real service + real repository, stubbed email sender."""

    @pytest.fixture(autouse=True)
    def setup(self, db_connection):
        self.repo = UserRepository(db_connection)
        self.service = UserService(repo=self.repo, email_sender=MagicMock())
        yield
        db_connection.execute("DELETE FROM users WHERE email LIKE 'test_%'")

    def test_register_new_user_persists_to_db(self):
        """
        Source: AC-1 — new registrations are persisted.
        """
        self.service.register(email="test_alice@example.com", password="Pass1!")

        user = self.repo.find_by_email("test_alice@example.com")
        assert user is not None
        assert user["email"] == "test_alice@example.com"

    def test_duplicate_email_raises_conflict(self):
        """
        Source: AC-2 — registering an existing email raises ConflictError.
        """
        self.service.register(email="test_bob@example.com", password="Pass1!")

        with pytest.raises(ConflictError):
            self.service.register(email="test_bob@example.com", password="Other1!")
```

**Rules:**
- Clean up test data in the fixture teardown (after `yield`), not in the test itself.
- Use `autouse=True` sparingly — only when every test in the class needs the same setup.
- Integration tests are slower; mark them with `@pytest.mark.integration` and configure pytest to skip them by default with `-m "not integration"`.

---

## Markers

```python
# pytest.ini or pyproject.toml [tool.pytest.ini_options]
# markers =
#     integration: marks tests as integration tests (slow, requires DB)
#     smoke: marks tests as smoke tests (critical path only)

@pytest.mark.integration
def test_full_login_flow(db_connection): ...

@pytest.mark.smoke
def test_health_check(): ...
```

---

## Assertion Cheatsheet

| Scenario | Pattern |
|----------|---------|
| Equality | `assert result == expected` |
| Type check | `assert isinstance(result, MyClass)` |
| Exception | `with pytest.raises(ValueError, match="must be positive"):` |
| Approx float | `assert result == pytest.approx(3.14, abs=1e-2)` |
| Dict subset | `assert expected.items() <= result.items()` |
| List contains | `assert item in result` |
| List length | `assert len(result) == 3` |
| Called once | `mock.method.assert_called_once_with(arg)` |
| Not called | `mock.method.assert_not_called()` |
| Any call with arg | `mock.method.assert_any_call(arg)` |

---

## File Naming Conventions

| Test type | File name |
|-----------|-----------|
| Unit tests for `src/myapp/services/user_service.py` | `tests/unit/test_user_service.py` |
| Integration tests for registration flow | `tests/integration/test_user_registration.py` |
| conftest for all tests | `tests/conftest.py` |
| conftest scoped to unit only | `tests/unit/conftest.py` |

- Always prefix test files with `test_`.
- Always prefix test functions and methods with `test_`.
- Class names: `Test<Subject>` (no `Test` suffix on the subject itself).
