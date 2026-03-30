---
name: review-pr
description: Reviews a pull request for logic errors, security issues, test coverage, and style — producing structured inline feedback.
version: 1.0.0
tags: [review]
---

## When to Use

When the user provides a PR number, PR URL, branch name to review, or asks "review this diff". Requires either `gh` CLI access or a diff available in context.

## Steps

1. Load `checklist.md` from this skill's folder before proceeding
2. Fetch PR details: `gh pr view <number>` for metadata, `gh pr diff <number>` for the full diff
3. Read the diff carefully — understand what changed, not just what the lines say
4. Work through each section of `checklist.md` systematically
5. Classify each finding as **Blocking**, **Suggestion**, or **Nit**
6. Every **Blocking** issue must reference the specific file and line number
7. Format output as structured markdown (see Output Format)

## Rules

- Never approve (or say "looks good") if any Blocking issues are present
- Stay factual — cite specific lines, don't speak in generalities
- If a change's intent is unclear, ask a clarifying question rather than assuming bad intent
- Do not leave Nits without acknowledging they are low priority

## Output Format

```
## PR Review: <title> (#<number>)

### Summary
<2–3 sentence overview of what the PR does>

### Blocking
- `path/to/file.ts:42` — <issue description>

### Suggestions
- `path/to/file.ts:17` — <suggestion>

### Nits
- `path/to/file.ts:5` — <minor style note>
```

Omit any section that has no items.

## Notes

Review criteria live in `checklist.md` — load it before step 3.
