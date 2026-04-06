## Jira Flow

### When to Use
When the user provides a Jira epic key, story key, or Jira URL.

### Steps
1. Parse the Jira key from the input (e.g. PROJ-123)
2. If Jira MCP is available: call `get_epic` or `get_story` to fetch acceptance criteria
   If Jira MCP is not available: ask the user to paste the acceptance criteria from Jira
3. Parse ACs into testable behaviors:
   - Each "Given/When/Then" → one test function
   - Each bullet point → one or more test functions (one per assertion)
4. **Filter by test value** — classify each AC before generating:
   - High/medium value → include
   - Low value (static headings, copy, styling, icon presence) → skip; log in summary
   - If an AC is ambiguous about whether it describes behavior or appearance, assume behavioral and ask one clarifying question
5. Identify whether kept ACs describe UI flows (→ E2E) or API contracts (→ REST) — use both if mixed
6. For each kept AC: generate a test using the loaded template file
7. Collect all tests into a single file named `test_<epic-or-story-slug>.py`

### Rules
- If an AC is ambiguous (e.g. "user sees success message"), ask: what element / text exactly — and is this server-driven or always static?
- Do not generate tests for ACs that have no verifiable behavioral outcome
- Do not generate tests for ACs whose only assertion is static content (headings, labels, marketing copy)
- Include the Jira key + AC number in each test's docstring

### Output Format
The generated test file, then:
### Tests Generated
- File: `test_<slug>.py`
- Source: <key> (<N> acceptance criteria → <M> test functions)
- Framework: <framework>
- Coverage: <list of AC summaries>
