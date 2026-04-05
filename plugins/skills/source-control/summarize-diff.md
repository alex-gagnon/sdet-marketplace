# Summarize Diff Sub-Behavior

## When to Use

When the user has a diff and needs a description: PR body, changelog entry, release notes, or a standup update. Works with staged changes, between-commit diffs, branch diffs, or a pasted diff.

## Steps

1. Obtain the diff:
   - Staged: `git diff --staged`
   - Between commits: `git diff <base>..<head>`
   - Branch vs main: `git diff main...<current-branch>`
   - Or use a diff already provided in the conversation
2. Identify categories of change present: new features, bug fixes, refactoring, configuration, tests, documentation
3. Write a one-paragraph prose summary (3–5 sentences)
4. Write a bulleted change list, grouping related changes under category headings if more than 5 items

## Rules

- Stay factual — do not invent intent or embellish scope
- If a change's purpose is unclear from the diff alone, say "apparent purpose unclear" rather than guessing
- Do not include implementation details (variable names, line numbers) in the summary — describe behavior and outcomes
- Keep the prose summary under 100 words

## Output Format

```
### Summary
<1 paragraph, ≤100 words>

### Changes
- **Feature:** <what was added>
- **Fix:** <what was corrected>
- **Refactor:** <what was restructured>
- **Tests:** <what was tested>
- **Config/Docs:** <what was configured or documented>
```

Omit categories with no entries. Ready to paste directly into a PR description.
