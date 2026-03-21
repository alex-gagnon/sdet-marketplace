---
name: commit
description: Creates a well-formatted git commit message from staged changes using imperative mood and conventional structure.
version: 1.0.0
tags: [git]
---

## When to Use

When the user asks to commit, create a commit message, or "save changes". Requires a git repository with staged changes. If nothing is staged, warn and stop — do not auto-stage files.

## Steps

1. Run `git diff --staged` to review exactly what will be committed
2. Identify the scope and nature of the change (feature, fix, refactor, chore, docs, test)
3. Draft a subject line: imperative mood, ≤72 characters, no trailing period
4. Add a body paragraph if the change is non-trivial or the "why" isn't obvious from the subject
5. Run `git commit -m "..."` (or with heredoc for multi-line messages)
6. Confirm success with the resulting commit hash and subject

## Rules

- Never use `--no-verify` or `--no-gpg-sign`
- Never amend a commit unless the user explicitly requests it
- Never commit `.env`, credential files, or files matching `.gitignore`
- If nothing is staged, say so and ask whether to stage specific files — do not run `git add .` unilaterally
- If a pre-commit hook fails, fix the underlying issue rather than bypassing it

## Output Format

The executed commit command followed by a one-line confirmation: what was committed and to which branch.
