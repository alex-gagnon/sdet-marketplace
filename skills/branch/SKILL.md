---
name: branch
description: Creates or switches to a git branch following the repository's naming conventions and branch strategy.
version: 1.0.0
tags: [git]
---

## When to Use

When the user wants to start work on a new feature, fix, or task and needs a branch. Also use when the user says "create a branch for X" or "switch to a new branch". Requires a git repository.

## Steps

1. Check the working tree is clean (`git status`); if dirty, ask whether to stash or commit first
2. Read the local `CLAUDE.md` (if present) for branch naming conventions — follow them exactly
3. Determine branch type from context: `feature/`, `fix/`, `chore/`, `docs/`, or the project's own prefix scheme (e.g., this repo uses `claude/<description>-<id>`)
4. Slugify the description: lowercase, hyphens only, no special characters, keep it concise (3–6 words)
5. Run `git switch -c <branch-name>` (prefer `switch` over `checkout -b`)
6. Confirm the new branch name and current HEAD

## Rules

- Default to branching from `main` or `master` — never from another feature branch without explicit user confirmation
- If the branch already exists, ask whether to switch to it rather than creating a duplicate
- Do not push the branch unless the user explicitly asks

## Output Format

One-line confirmation: the new branch name and the commit it was branched from (short hash + subject).
