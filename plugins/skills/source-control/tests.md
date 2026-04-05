# Tests: source-control

## Scenarios

### Scenario 1: commit — staged changes present
**Input context:** Repo has staged changes: a Python file where a `None` check was added to prevent a crash in `process_order()`. `git diff --staged` shows ~10 lines changed.
**Invoke:** `/source-control`
**Expected format:** Routes silently to commit sub-behavior. Executes a commit. Output includes a one-line confirmation naming what was committed and which branch.

### Scenario 2: commit — nothing staged
**Input context:** `git status` shows modified files but `git diff --staged` is empty.
**Invoke:** `/source-control`
**Expected format:** Does NOT commit. Tells the user nothing is staged and asks whether to stage specific files. Does not run `git add .` unilaterally.

### Scenario 3: branch — explicit branch request
**Input context:** User says "I want to create a branch for adding dark mode support". Repo is on `main`, working tree is clean.
**Invoke:** `/source-control`
**Expected format:** Routes silently to branch sub-behavior. One-line confirmation naming the created branch and the commit it was branched from (short hash + subject).

### Scenario 4: summarize — diff provided
**Input context:** User pastes a git diff spanning 4 files: a new `export_csv.py` module, a fix to `null` handling in `parse_row()`, and 2 updated test files.
**Invoke:** `/source-control`
**Expected format:** Routes silently to summarize sub-behavior. Output has `### Summary` (≤100 words) and `### Changes` with labeled categories. No `**Refactor:**` entry (nothing refactored).

### Scenario 5: intent unclear
**Input context:** User just invokes `/source-control` with no other context. No staged changes. No diff provided.
**Invoke:** `/source-control`
**Expected format:** Asks exactly one clarifying question: "Are you looking to commit staged changes, create/switch a branch, or summarize a diff?" No further assumptions.

### Scenario 6: commit — breaking change
**Input context:** Staged diff removes the public function `getUserById()` from a shared utility module.
**Invoke:** `/source-control`
**Expected format:** Commits with a message that signals the breaking nature (e.g., `feat!:` or `BREAKING CHANGE:` in body).

## Rubric

1. **Silent routing for unambiguous intent** — when context clearly indicates one sub-behavior, routes without asking.
   - Pass: staged changes present + no branch or diff mention -> commits without asking "did you mean commit?"
   - Fail: asks a clarifying question when context is obvious
2. **Single clarifying question for ambiguous intent** — when context is absent, asks exactly one question covering all three options.
   - Pass: "Are you looking to commit, branch, or summarize a diff?" (one question, three options)
   - Fail: multiple questions, or proceeds with a guess without asking
3. **Commit accuracy** — commit message accurately describes the actual code change.
   - Pass: subject names the specific function, file, or behavior changed
   - Fail: generic subject like "fix stuff" or "updates"
4. **Branch name quality** — branch slug is descriptive and follows repo conventions.
   - Pass: `feature/dark-mode-support` or `claude/dark-mode-support-X1y2`
   - Fail: `new-branch`, `feature`, or violates detected convention
5. **Summarize output format** — summary uses exact section headers; omits empty categories.
   - Pass: `### Summary` + `### Changes` with only populated categories
   - Fail: empty `**Refactor:** —` entry, or missing headers

## Golden Set

### Golden 1 — commit route
**Input:** Staged diff adds `if order is None: raise ValueError("order required")` in `orders.py`.
**Ideal output:**
```
git commit -m "Fix crash when process_order receives None input"
Committed to main: Fix crash when process_order receives None input
```

### Golden 2 — intent unclear route
**Input:** `/source-control` with no context.
**Ideal output:**
```
Are you looking to commit staged changes, create/switch a branch, or summarize a diff?
```

### Golden 3 — summarize route
**Input:** Diff adds `export_csv.py` (feature), fixes null handling in `parse_row()` (fix), adds tests.
**Ideal output:**
```
### Summary
Adds CSV export functionality to the data pipeline and fixes a null-handling bug in the row parser that caused crashes on empty fields. Test coverage added for both changes.

### Changes
- **Feature:** New `export_csv.py` module with `ExportJob` class and CLI entry point
- **Fix:** `parse_row()` now returns an empty string instead of raising on null fields
- **Tests:** Unit tests for `ExportJob` and the null-handling fix
```
