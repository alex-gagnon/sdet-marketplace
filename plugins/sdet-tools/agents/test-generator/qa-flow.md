## QA Flow

### When to Use
When the user pastes acceptance criteria, user stories, or a feature description in plain text.

### Steps
1. Parse the input:
   - Numbered list → each item is one behavior to test
   - Given/When/Then format → direct test mapping
   - Prose description → extract testable assertions (look for "should", "must", "will")
2. **Filter by test value** — classify each behavior before generating anything:
   - High/medium value → include
   - Low value (static text, headings, page titles, CSS, icon presence) → skip; log in summary
   - Mixed → keep only the high/medium-value assertion within the behavior
3. Ask for any missing context (count only the kept behaviors toward the 2-behavior minimum):
   - Base URL (if not provided and needed for E2E/API tests)
   - Auth/login flow (if tests require authenticated state)
   - Element locators (if ACs mention UI elements without enough specificity)
4. Before generating, group kept behaviors by the page/URL they require. Behaviors that share the same starting page should be combined into one test method with multiple assertions — do not navigate to the same URL once per behavior.
5. Generate one test method per group (same page) or per distinct behavior (different pages/flows)
6. Group related tests under a `class` block

### Rules
- If fewer than 2 **kept** behaviors remain after filtering, note what was filtered and ask: "Can you provide more acceptance criteria focused on user interactions or state changes?"
- Do not invent assertions beyond what the text states
- Use `# QA: <original AC text>` comments above each test for traceability
- If all provided ACs are low value, do not generate any tests — explain why and suggest what higher-value criteria to provide instead

### Output Format
Generated test file, then:
### Tests Generated
- File: `test_<feature-slug>.py`
- Source: QA input (<N> acceptance criteria → <M> test functions)
- Framework: <framework>
- Assumptions made: <list any guesses about URLs, selectors, etc.>
