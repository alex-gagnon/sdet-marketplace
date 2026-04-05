# Tests: add-tests

## Scenarios

### Scenario 1: simple pure function
**Input context:** A Python function `calculate_discount(price, pct)` that returns `price * (1 - pct/100)`. No existing tests. User runs `/add-tests` on it.
**Invoke:** `/add-tests`
**Expected format:** Test file content (or additions), followed by `### Test Coverage Added` with bullet points naming happy path, edge case(s), and error path(s).

### Scenario 2: function with external dependency
**Input context:** A TypeScript function `fetchUserProfile(userId: string)` that calls an HTTP API and returns parsed JSON. No existing tests.
**Invoke:** `/add-tests`
**Expected format:** Tests use mocking for the HTTP call. Coverage section names what's mocked and why.

### Scenario 3: appending to existing test file
**Input context:** A `test_orders.py` file exists with 2 tests for `create_order()`. User runs `/add-tests` on the new `cancel_order()` function in the same module.
**Invoke:** `/add-tests`
**Expected format:** Shows only the new test additions in context (not the full file). Coverage section lists only the new cases.

### Scenario 4: function with complex error conditions
**Input context:** A Go function `ParseConfig(path string) (*Config, error)` that reads a file, validates JSON, checks required fields, and returns typed errors for each failure mode.
**Invoke:** `/add-tests`
**Expected format:** Error path tests cover each distinct error mode (file not found, invalid JSON, missing required fields). Coverage section is specific.

## Rubric

1. **Coverage completeness** — happy path, at least one edge case, and at least one error path are all represented.
   - Pass: tests exist for normal input, boundary/edge input, and invalid/error input
   - Fail: only happy path tested, or error paths missing
2. **Test specificity** — test names and assertions describe what is being tested, not just "test_function".
   - Pass: `test_calculate_discount_returns_zero_for_100_pct_discount`
   - Fail: `test_calculate_discount_1`, `test_edge_case`
3. **Dependency handling** — external dependencies (HTTP, DB, filesystem) are mocked or stubbed.
   - Pass: `mock.patch('requests.get')` or Jest `jest.mock()` used appropriately
   - Fail: test makes real HTTP calls or requires live DB
4. **Coverage section accuracy** — the `### Test Coverage Added` section accurately names what was added (not generic).
   - Pass: "Edge case: price=0 returns 0 discount" — matches an actual test
   - Fail: "Edge case: various edge cases" — vague or doesn't match actual tests
5. **Append mode** — when a test file exists, only additions are shown (not full file rewrite).
   - Pass: shows new `def test_cancel_order_...` blocks with context
   - Fail: rewrites entire `test_orders.py` from scratch

## Golden Set

### Golden 1 — pure function
**Input:** Python function `def calculate_discount(price, pct): return price * (1 - pct / 100)`
**Ideal output:**
```python
def test_calculate_discount_standard():
    assert calculate_discount(100, 20) == 80.0

def test_calculate_discount_zero_percent():
    assert calculate_discount(100, 0) == 100.0

def test_calculate_discount_full_discount():
    assert calculate_discount(100, 100) == 0.0

def test_calculate_discount_negative_price():
    assert calculate_discount(-50, 10) == -45.0
```

```
### Test Coverage Added
- Happy path: standard discount applied to positive price
- Edge case: 0% discount returns original price
- Edge case: 100% discount returns 0
- Error path: negative price handled (returns negative result, not an error)
```
