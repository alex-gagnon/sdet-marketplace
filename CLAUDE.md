# CLAUDE.md — Skills Repository

This repository stores **Claude Code skills** — reusable prompt-based capabilities that extend Claude Code's behavior within a workspace.

## What Are Skills?

Skills are named prompts invoked via slash commands (e.g., `/commit`, `/simplify`, `/loop`). When a user types `/<skill-name>`, Claude Code expands the skill into a full prompt and executes it in context. Skills are not executable scripts — they are structured natural-language instructions that Claude follows.

## Repository Structure

```
skills/
├── CLAUDE.md              # This file
├── <skill-name>.md        # One file per skill
└── ...
```

Each skill is a single Markdown file. The filename (without `.md`) is the slash command name used to invoke it.

## Skill File Format

A skill file should contain:

1. **Trigger conditions** — when Claude should use this skill
2. **Instructions** — what Claude should do when invoked
3. **Examples** (optional) — sample inputs and expected behavior
4. **Edge cases** (optional) — explicit guidance for unusual situations

### Minimal Example (`greet.md`)

```markdown
Greet the user warmly using their name if provided. Keep it brief (one sentence).
If no name is given, use "there" as a placeholder.
```

### Annotated Example (`commit.md`)

```markdown
Create a well-formatted git commit for staged changes.

Steps:
1. Run `git diff --staged` to review what will be committed
2. Draft a commit message: imperative mood, ≤72 chars subject line
3. Add a body paragraph if the change is non-trivial
4. Run `git commit -m "..."` — never skip hooks (--no-verify)

Do NOT commit if there are no staged changes. Warn the user instead.
```

## Naming Conventions

| Convention | Rule |
|---|---|
| File names | lowercase, hyphens only (e.g., `review-pr.md`) |
| Slash command | matches filename without `.md` |
| Verbs | prefer imperative verbs (`commit`, `simplify`, `loop`) |
| Scope | one skill per file; no combined/multi-purpose skill files |

## Development Workflow

### Adding a New Skill

1. Create `<skill-name>.md` in the repo root
2. Write clear, unambiguous instructions (see format above)
3. Test locally by invoking `/<skill-name>` in a Claude Code session
4. Commit with a descriptive message: `add <skill-name> skill`
5. Push to a `claude/` prefixed branch and open a PR

### Editing an Existing Skill

1. Read the current file before editing
2. Keep changes minimal and focused
3. Commit: `update <skill-name>: <what changed>`

### Removing a Skill

1. Delete the `.md` file
2. Commit: `remove <skill-name> skill`
3. Update any references in other skill files or documentation

## Writing Good Skills

**Be explicit, not implicit.** Claude cannot infer unstated requirements. If a skill should never do X, say so.

**One responsibility per skill.** A skill that does too many things is hard to invoke correctly and hard to maintain.

**Use numbered steps for multi-step workflows.** This ensures consistent execution order.

**State preconditions.** If a skill requires a git repo, a specific file type, or other context, state it upfront so Claude can fail fast with a useful message.

**Avoid ambiguity around destructive actions.** If a skill can delete, overwrite, or publish something, explicitly require user confirmation or warn the user first.

## Key Conventions for AI Assistants

- **Do not generate code** unless a skill explicitly calls for it — most skills are workflow/orchestration prompts
- **Do not create new skill files** unless the user explicitly requests a new skill
- **Prefer editing** existing skill files over creating new ones
- **Never rename** skill files without updating all references, as the filename is the slash command
- **Test your understanding**: if a skill's purpose is unclear, re-read the file before invoking or editing it
- **Branch naming**: all development branches must start with `claude/` (enforced by remote)

## Git Practices

- Branch format: `claude/<description>-<id>`
- Push: `git push -u origin <branch-name>`
- Never force-push, never skip hooks
- Keep commits atomic: one logical change per commit
