# PR Review Checklist

Use this checklist systematically when reviewing a PR. Each item that surfaces an issue becomes a finding in the review output.

## Correctness

- [ ] Does the logic correctly implement the stated intent?
- [ ] Are there off-by-one errors in loops or index operations?
- [ ] Are null/undefined/nil values handled at all entry points?
- [ ] Are error return values checked (not silently discarded)?
- [ ] Are concurrent operations safe (race conditions, shared mutable state)?
- [ ] Does the change handle the empty/zero/edge case inputs?

## Security

- [ ] Is any user-supplied input validated before use?
- [ ] Are there SQL, command, or template injection risks?
- [ ] Are secrets, tokens, or credentials absent from the diff?
- [ ] Are authentication and authorization checks present where needed?
- [ ] Are file paths sanitized to prevent path traversal?
- [ ] Are dependencies being added from trusted sources with pinned versions?

## Tests

- [ ] Do new code paths have corresponding tests?
- [ ] Are happy paths, error paths, and edge cases covered?
- [ ] Are tests meaningful, or do they just assert the implementation mirrors itself?
- [ ] Do existing tests still pass with these changes (no silent breakage)?

## Performance

- [ ] Are there N+1 query patterns introduced (database, API calls in loops)?
- [ ] Are large allocations or copies avoidable?
- [ ] Is caching invalidated correctly where it applies?
- [ ] Does the change introduce blocking I/O in a performance-sensitive path?

## Style and Consistency

- [ ] Does naming follow the conventions in the rest of the codebase?
- [ ] Is the code style consistent with the surrounding file?
- [ ] Are there unused imports, variables, or dead code branches?
- [ ] Is the diff free of unintentional whitespace or formatting changes?

## Documentation

- [ ] Are public API changes reflected in documentation or type signatures?
- [ ] Is a CHANGELOG entry included if the project maintains one?
- [ ] Are non-obvious decisions explained with a comment?
