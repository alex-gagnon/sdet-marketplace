# Tests: simplify

## Scenarios

### Scenario 1: nested conditionals
**Input context:** A Python function with 4 levels of nested `if` statements that checks user permissions. Equivalent to a guard-clause pattern but written as nested ifs.
**Invoke:** `/simplify`
**Expected format:** Simplified code using early returns (guard clauses), followed by `### Changes Made` and `### Risks / Things to Verify`.

### Scenario 2: redundant variable reassignment
**Input context:** JavaScript function that assigns a value to `result`, then immediately overwrites it in the next line, then returns it. Dead assignment on the first line.
**Invoke:** `/simplify`
**Expected format:** Simplified code removes the dead assignment. Changes Made notes the removal. Risks section is minimal (straightforward elimination).

### Scenario 3: behavior-preserving constraint
**Input context:** A complex sorting function with an obscure comparison logic that is actually correct. User asks to simplify it, but the "obvious" simplification would change sort stability.
**Invoke:** `/simplify`
**Expected format:** If the code can't be meaningfully simplified without risk, says so. Risks section is honest about the tradeoff. Does NOT introduce a breaking simplification.

### Scenario 4: repeated code block
**Input context:** A file with the same 10-line "fetch and parse response" block copy-pasted 3 times in different functions.
**Invoke:** `/simplify`
**Expected format:** Extracts the repeated block into a helper function. Changes Made explains the extraction. Risks notes that callers should be verified.

## Rubric

1. **Behavior preservation** — simplified code produces the same output for all inputs as the original.
   - Pass: guard-clause refactor is semantically equivalent; tests would still pass
   - Fail: early return added at wrong condition level changes behavior
2. **Actual reduction** — the simplified version is measurably simpler (fewer lines, less nesting, or clearer intent).
   - Pass: nesting depth reduced from 4 to 1; dead code removed
   - Fail: "simplification" that is the same length or more complex
3. **Changes Made specificity** — each bullet names the specific pattern changed and why.
   - Pass: "Replaced nested if-else with guard clauses: reduces indentation and makes exit conditions explicit"
   - Fail: "Made code cleaner" / "Refactored for readability"
4. **Risks section honesty** — flags things that warrant a test run; doesn't claim zero risk when risk exists.
   - Pass: "Verify that the extracted helper handles all three call sites' error expectations identically"
   - Fail: empty Risks section after a complex extraction, or overly alarming risks for a trivial change
5. **Restraint** — does not over-refactor. Only changes what's needed to achieve the simplification, not a full rewrite.
   - Pass: touches 3 lines for a dead-assignment removal; leaves surrounding code alone
   - Fail: reformats entire file, renames variables, restructures unrelated logic

## Golden Set

### Golden 1 — nested conditionals to guard clauses
**Input:**
```python
def get_user_data(user):
    if user is not None:
        if user.is_active:
            if user.has_permission('read'):
                return fetch_data(user.id)
            else:
                return None
        else:
            return None
    else:
        return None
```
**Ideal output:**
```python
def get_user_data(user):
    if user is None or not user.is_active or not user.has_permission('read'):
        return None
    return fetch_data(user.id)
```

```
### Changes Made
- Replaced nested if-else with guard clauses: all early-exit conditions are collapsed into a single guard, reducing nesting from 3 levels to 0.

### Risks / Things to Verify
- Run existing tests for `get_user_data` to confirm all three rejection conditions still behave identically.
```
