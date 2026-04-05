# Tests: review-pr

## Scenarios

### Scenario 1: PR with a clear security bug
**Input context:** PR adds a new API endpoint that reads a user ID from query params and queries the database directly: `db.query(f"SELECT * FROM users WHERE id = {user_id}")` — a SQL injection vulnerability. PR also renames a variable from `data` to `payload` in an unrelated function.
**Invoke:** `/review-pr`
**Expected format:** Output follows the `## PR Review: <title> (#<number>)` structure with Summary, Blocking (SQL injection), and optionally Nits (rename). Suggestions section omitted if empty.

### Scenario 2: clean PR, minor style issues only
**Input context:** PR adds a well-tested utility function `format_currency(amount, currency)` with docstring, unit tests, and no logic errors. One nit: a trailing whitespace on line 14.
**Invoke:** `/review-pr`
**Expected format:** Summary praises the quality. No Blocking or Suggestions sections. Nits section has one entry for trailing whitespace.

### Scenario 3: PR missing tests
**Input context:** PR adds a 200-line `PaymentProcessor` class with no tests. Complex branching logic for retry and rollback behavior.
**Invoke:** `/review-pr`
**Expected format:** Blocking or Suggestions section raises missing test coverage. Specific methods or branches called out, not just "add tests".

### Scenario 4: PR description mismatch
**Input context:** PR title says "Fix null pointer in user loader" but the diff also adds a brand-new feature: an `impersonate_user()` admin function with no auth checks.
**Invoke:** `/review-pr`
**Expected format:** Blocking section calls out the unauthorized impersonation endpoint. Summary notes the scope mismatch from the PR title.

## Rubric

1. **Structure compliance** — output uses the exact section headers from the Output Format spec.
   - Pass: `## PR Review:`, `### Summary`, `### Blocking`, etc. present and correctly formatted
   - Fail: free-form prose without headers, or wrong header names
2. **File + line citations** — each issue cites `path/to/file:line` format.
   - Pass: `` `api/users.py:23` — SQL injection via unsanitized user_id ``
   - Fail: "there's a SQL injection somewhere" with no location
3. **Severity calibration** — blocking items are genuinely blocking; nits are genuinely minor.
   - Pass: SQL injection → Blocking; trailing whitespace → Nits
   - Fail: SQL injection in Nits, or trailing whitespace in Blocking
4. **Omits empty sections** — sections with no items are omitted entirely (not left empty or with "None").
   - Pass: clean PR has only Summary + Nits
   - Fail: `### Blocking\n(none)` appears in output
5. **Actionable feedback** — each item describes the problem AND what to do about it.
   - Pass: "Use parameterized queries: `db.query('SELECT * FROM users WHERE id = ?', [user_id])`"
   - Fail: "This is a SQL injection" with no remediation

## Golden Set

### Golden 1 — SQL injection PR
**Input:** PR #17 "Add user lookup endpoint" — diff shows `db.query(f"SELECT * FROM users WHERE id = {user_id}")` in `api/users.py` line 23.
**Ideal output:**
```
## PR Review: Add user lookup endpoint (#17)

### Summary
Adds a GET endpoint for fetching user records by ID. The implementation has a critical SQL injection vulnerability that must be fixed before merging.

### Blocking
- `api/users.py:23` — SQL injection: `user_id` is interpolated directly into the query string. Use a parameterized query: `db.query("SELECT * FROM users WHERE id = ?", [user_id])`.
```
