---
name: add-tests
description: Generates tests for an existing function or module, covering happy paths, edge cases, and error conditions.
version: 1.0.0
tags: [quality]
---

## When to Use

When the user asks to add tests, "test this function", "write tests for X", or "improve test coverage". Target must be existing code — do not write tests for code that hasn't been written yet.

## Steps

1. Load `test-strategies.md` from this skill's folder before proceeding
2. Read the target function or module in full
3. Detect the testing framework from existing test files, `package.json`, `pyproject.toml`, `go.mod`, or similar — do not introduce a new framework
4. Identify test cases:
   - Happy paths (typical valid inputs → expected outputs)
   - Boundary conditions (empty, zero, max, min, exact boundary)
   - Error / exception paths (invalid input, missing dependency, network failure)
   - Any documented behavior in comments or types
5. Match existing test file naming convention (e.g., `foo.test.ts`, `test_foo.py`, `foo_test.go`)
6. Write tests using the patterns from `test-strategies.md` for the detected framework
7. Note which test cases cover which behaviors

## Rules

- Never modify the code under test to make tests pass — fix the tests or flag a bug in the code
- Do not introduce mocks for things that don't need to be mocked (prefer real implementations where practical)
- Match the existing test style exactly: assertion library, describe/it nesting depth, helper patterns
- If the framework cannot be detected, ask before choosing one

## Output Format

The test file content (full file if new, additions if appending), followed by:

```
### Test Coverage Added
- Happy path: <what scenario>
- Edge case: <what scenario>
- Error path: <what scenario>
```
