# Skills

A collection of Claude Code skills for common development workflows. Skills are invoked as slash commands in any Claude Code session where this repository is configured as the skills directory.

## Available Skills

| Skill | Command | Description | Support Files |
|---|---|---|---|
| commit | `/commit` | Creates a well-formatted git commit message from staged changes using imperative mood and conventional structure. | — |
| branch | `/branch` | Creates or switches to a git branch following the repository's naming conventions and branch strategy. | — |
| review-pr | `/review-pr` | Reviews a pull request for logic errors, security issues, test coverage, and style — producing structured inline feedback. | `checklist.md` |
| summarize-diff | `/summarize-diff` | Produces a concise plain-English summary of a git diff or set of changes, suitable for PR descriptions or changelogs. | — |
| simplify | `/simplify` | Refactors a code block or file to reduce complexity, improve readability, and eliminate redundancy without changing behavior. | `patterns.md` |
| add-tests | `/add-tests` | Generates tests for an existing function or module, covering happy paths, edge cases, and error conditions. | `test-strategies.md` |
| document | `/document` | Adds or improves inline documentation, docstrings, and README sections for a function, module, or project. | `templates.md` |
| explain | `/explain` | Explains a piece of code, architecture decision, or technical concept in plain language calibrated to the user's apparent expertise level. | — |
| grill | `/grill` | Challenges a design, plan, or idea using Socratic questioning and devil's-advocate critique to surface hidden assumptions and weaknesses. | `question-bank.md` |

## Installation

Point Claude Code's skills directory at `skills/` in this repo:

```jsonc
// ~/.claude/settings.json
{
  "skillsDirectory": "/path/to/this/repo/skills"
}
```

Or symlink:

```bash
ln -s /path/to/this/repo/skills ~/.claude/skills
```

## Adding a Skill

See [CLAUDE.md](./CLAUDE.md) for conventions and the `skills/commit/SKILL.md` file as a template.
