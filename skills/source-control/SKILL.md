---
name: source-control
version: 1.0.0
description: Handles git workflow operations — committing staged changes, creating or switching branches, and summarizing diffs — routing to the right sub-behavior from context.
tags: [git]
---

# /source-control — Git Workflow

Handles three related git operations. Detect which one the user needs, load the matching support file, and follow its instructions.

## Intent Detection

Read the user's request and current repository state:

- **Commit** — user wants to save staged changes, create a commit, or says "commit this": load `commit.md` from this skill's folder
- **Branch** — user wants to create a branch, switch branches, or start work on a feature/fix: load `branch.md` from this skill's folder
- **Summarize** — user has a diff and needs a description for a PR, changelog, or standup: load `summarize-diff.md` from this skill's folder
- **Unclear** — ask exactly one question: "Are you looking to commit staged changes, create/switch a branch, or summarize a diff?"

Load the matching file, then follow its instructions exactly as if they were written here.

## Notes

Sub-behaviors and their triggers:
- `commit.md` — commit staged changes with a well-formatted message
- `branch.md` — create or switch to a branch following repo conventions
- `summarize-diff.md` — produce a plain-English diff summary for PR descriptions or changelogs
