## PR Flow

### When to Use
When the user provides a GitHub PR number or URL.

### Steps
1. Run: `gh pr view <number> --json title,body,files,headRefName`
2. Read the PR title and body to understand the intent
3. Read changed files:
   - UI files (*.html, */components/*, */pages/*, */views/*) → E2E template
   - API files (*/api/*, */routes/*, *_router.py, *_handler.py) → REST API template
   - Mixed: generate both types
4. **Filter by test value** — for each changed behavior, classify before generating:
   - High/medium value → include (logic changes, new user interactions, auth, validation, state)
   - Low value → skip; log in summary (copy/text changes, CSS-only diffs, icon swaps, heading text, static markup)
   - If a diff only touches static content or styling with no behavioral change, skip it entirely
5. For each kept behavior, generate a test:
   - New endpoint added → test happy path + error path
   - Modified component → test the UI interaction it enables, not the rendered markup
6. Check for existing `test_*.py` / `*_test.py` files to match naming and fixture conventions
7. Collect tests into appropriate file(s)

### Rules
- Read the actual changed file content — do not guess behavior from filenames alone
- If the PR diff is too large (>500 lines), focus on the highest-impact changed files
- Cite the PR number and changed file in each test docstring
- If the entire PR is low value (e.g. a copy/text-only change), generate no tests and explain why in the summary

### Output Format
Generated test file(s), then:
### Tests Generated
- File(s): `test_<slug>.py`
- Source: PR #<N> — <title>
- Changed files covered: <list>
- Framework: <framework>
