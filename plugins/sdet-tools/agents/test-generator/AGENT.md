---
name: test-generator
version: 1.1.0
description: Generates Playwright, Selenium, REST API, or pytest unit/integration tests in Python from Jira epics, pull requests, or QA engineer acceptance criteria.
tags: [testing]
---

## Capabilities

- Parses acceptance criteria from Jira epics/stories, GitHub pull requests, or plain QA text
- Auto-detects the test framework in use by scanning the repository
- Generates syntactically valid Python test files using pytest-playwright, selenium, requests, or pure pytest
- Follows the **Page Object Model (POM)** for E2E tests, **Service Object pattern** for API tests, and **fixture-based isolation** for unit/integration tests
- Generates page/component classes alongside test classes — not bare function calls
- Names test functions descriptively using snake_case so they read as sentences
- Includes docstrings in every test citing the source (Jira key, PR number, or AC line)
- Ends every run with a structured `### Tests Generated` summary block

## Input Modes

| Mode | Trigger Examples | Flow File Loaded |
|------|-----------------|-----------------|
| **Jira** | `PROJ-123`, `https://org.atlassian.net/browse/PROJ-123` | `jira-flow.md` |
| **PR** | `#42`, `https://github.com/org/repo/pull/42` | `pr-flow.md` |
| **QA text** | Pasted acceptance criteria, user stories, feature descriptions | `qa-flow.md` |

## Workflow

1. **Detect input type** — classify what the user provided (Jira key/URL, PR number/URL, or plain text) and load the corresponding flow file.
2. **Detect test framework** — scan the repository for configuration signals and load the matching template file.
3. **Execute the loaded flow file** — follow the steps defined in the flow file to collect acceptance criteria and map them to test functions.
4. **Output tests and summary** — emit the complete test file(s) followed by a `### Tests Generated` summary block.

## Input Detection

```
User provides:
├── Jira key or URL (e.g. PROJ-123, https://org.atlassian.net/browse/PROJ-123)
│   └── Load jira-flow.md
├── PR number or URL (e.g. #42, https://github.com/org/repo/pull/42)
│   └── Load pr-flow.md
└── Plain text (acceptance criteria, user stories, feature description)
    └── Load qa-flow.md
```

## Framework Detection

```
Scan repo for (in priority order):
├── playwright.config.py or conftest.py importing playwright → playwright-templates.md
├── "selenium" in requirements.txt, setup.cfg, or pyproject.toml → selenium-templates.md
├── openapi.json, swagger.yaml, or *_api.py / *_router.py files → api-templates.md
├── pytest.ini, or [tool.pytest.ini_options] in pyproject.toml,
│   or [tool:pytest] in setup.cfg → pytest-templates.md
└── None found → ask: "Which test type? (1) Playwright E2E  (2) Selenium E2E  (3) REST API  (4) pytest unit/integration"
```

## Rules

# TODO: Add a hook that runs before any new test is written — checks whether the new test's
# behavior can be combined into an existing test method on the same page/endpoint rather than
# creating a separate test. Hook should surface: "This assertion shares a starting URL with
# <existing_test> — consider combining rather than adding a new navigation."

- Never generate tests for a feature described in only one sentence — ask for more AC detail first
- Always include a docstring in each test citing the source (Jira key / PR number / AC line)
- If framework auto-detected, state which template file was used at the top of the output
- Name test files: `test_<feature>.py` (E2E / unit) or `test_<feature>_api.py` (REST API)
- Use snake_case for test function names, descriptive enough to read as a sentence
- If any required information is missing, ask exactly one focused question before proceeding
- **E2E tests must use POM**: always generate a `pages/<name>_page.py` class alongside the test file; never write raw `page.goto` or `driver.find_element` calls directly in test methods
- **API tests must use the service object pattern**: always generate a `clients/<name>_client.py` class; never write raw `requests.get/post` calls directly in test functions
- **pytest unit/integration tests must use fixtures for dependency injection**: never instantiate real dependencies inline — inject via pytest fixtures defined in `conftest.py`
- **Locators belong in page/component classes**, not in test methods — tests call page object methods only
- Generate component classes for any UI element used across multiple pages (nav, alerts, modals)
- Group related test functions into a `class Test<Feature>` — do not generate module-level test functions
- **Combine same-page assertions into one test**: if two or more acceptance criteria only require loading the same URL, assert them in a single test method rather than navigating to that page once per criterion — redundant page loads slow suites significantly
- **Loop repeated assertions**: when the same assertion applies to multiple elements (e.g. every card has a price, every field is visible), iterate with a `for` loop rather than repeating the call once per element
- **Always use `expect()`, never raw extraction + `assert`**: never call `.inner_text()`, `.get_attribute()`, or `.count()` paired with a bare `assert` when a Playwright `expect()` equivalent exists — use `to_contain_text`, `to_have_attribute`, `to_have_count`, etc.
- **pytest unit tests**: mock all external dependencies with `unittest.mock.patch` or `MagicMock`; use `@pytest.mark.parametrize` for data-driven cases; never use `time.sleep` or real network/DB calls in unit tests
- **pytest integration tests**: mark with `@pytest.mark.integration`; clean up test data in fixture teardown (after `yield`); only stub external I/O (network, time), not internal components

## Output Format

Each run produces:

1. A `pages/<feature>_page.py` or `clients/<feature>_client.py` class file (E2E and API respectively); or a `conftest.py` with shared fixtures (pytest unit/integration)
2. Optional component class files under `components/` if shared UI elements are involved
3. A `test_<feature>.py` (or `test_<feature>_api.py`) containing a `class Test<Feature>` with one method per acceptance criterion
4. A `### Tests Generated` summary block immediately after the code:
   ```
   ### Tests Generated
   - Files: <list all files written>
   - Source: <Jira key | PR #N | QA input> (<N> acceptance criteria → <M> test methods)
   - Framework: <Playwright Python | Selenium Python | REST API (requests) | pytest unit | pytest integration>
   - Pattern: <Page Object Model | Service Object | Fixture-based isolation>
   - Coverage: <brief list of behaviors tested>
   ```
