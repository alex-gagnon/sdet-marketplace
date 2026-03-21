---
name: simplify
description: Refactors a code block or file to reduce complexity, improve readability, and eliminate redundancy without changing behavior.
version: 1.0.0
tags: [quality]
---

## When to Use

When the user points at code and asks to simplify, clean up, reduce complexity, or says "this feels messy". Target can be a selected snippet, a function, or a whole file.

## Steps

1. Load `patterns.md` from this skill's folder before proceeding
2. Read the target code carefully — understand what it does before touching it
3. Identify which patterns from `patterns.md` apply
4. Apply simplifications one category at a time: structure first, then naming, then duplication
5. If tests exist, note that they should be run after the change to verify no behavior change
6. Annotate the output with what changed and why

## Rules

- Never change observable behavior — if a simplification would alter output, side effects, or error handling, flag it and ask first
- If simplification requires changing a public API signature or exported interface, stop and ask for confirmation
- Preserve all comments that explain intent or non-obvious decisions
- Do not simplify things that are already clear — a short, obvious function doesn't need to be made "simpler"
- Do not add new abstractions unless they eliminate significant duplication (≥3 identical or near-identical sites)

## Output Format

The simplified code, followed by:

```
### Changes Made
- <what changed>: <why>
- ...

### Risks / Things to Verify
- <anything that warrants a test run or manual check>
```
