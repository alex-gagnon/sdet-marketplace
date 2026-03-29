# SDET Marketplace

A marketplace of Claude Code plugins — skills, agents, and MCP servers — for common software development and testing workflows. Plugins are organized by type and registered in `marketplace.json`.

## Plugin Types

| Type | Directory | Entrypoint | Invocation |
|------|-----------|------------|------------|
| **Skill** | `skills/<name>/` | `SKILL.md` | Slash command (e.g., `/source-control`) |
| **Agent** | `agents/<name>/` | `AGENT.md` | Agent tool or direct reference |
| **MCP** | `mcps/<name>/` | `MCP.md` | MCP server configuration |

## Available Plugins

### Skills

| Skill | Command | Description | Support Files |
|---|---|---|---|
| source-control | `/source-control` | Handles git workflow — routes to commit, branch, or diff summary based on context. | commit, branch, summarize-diff |
| review-pr | `/review-pr` | Reviews a pull request for logic errors, security issues, test coverage, and style — producing structured inline feedback. | `checklist.md` |
| simplify | `/simplify` | Refactors a code block or file to reduce complexity, improve readability, and eliminate redundancy without changing behavior. | `patterns.md` |
| add-tests | `/add-tests` | Generates tests for an existing function or module, covering happy paths, edge cases, and error conditions. | `test-strategies.md` |
| document | `/document` | Adds or improves inline documentation, docstrings, and README sections for a function, module, or project. | `templates.md` |
| explain | `/explain` | Explains a piece of code, architecture decision, or technical concept in plain language calibrated to the user's apparent expertise level. | — |
| grill | `/grill` | Challenges a design, plan, or idea using Socratic questioning and devil's-advocate critique to surface hidden assumptions and weaknesses. | `question-bank.md` |
| test | `/test` | Runs quality evaluations against one or all skills using their tests.md fixture files, scoring format compliance and semantic correctness. | — |

### Agents

| Agent | Description |
|---|---|
| plugin-architect | Assists with designing and scaffolding new marketplace plugins (skills, agents, and MCP servers) following marketplace conventions. |

### MCP Servers

_No MCP servers yet. Use the plugin-architect agent to design one._

## Marketplace Structure

```
sdet-marketplace/
├── marketplace.json          # Central plugin registry
├── skills/
│   └── <skill-name>/
│       ├── plugin.json       # Plugin metadata
│       ├── SKILL.md          # Entrypoint (prompt)
│       ├── tests.md          # Test scenarios and rubric
│       └── *.md              # Support files (Tier 3)
├── agents/
│   └── <agent-name>/
│       ├── plugin.json
│       ├── AGENT.md
│       └── tests.md
└── mcps/
    └── <mcp-name>/
        ├── plugin.json
        ├── MCP.md
        └── tests.md
```

## Testing

Each plugin has a `tests.md` file with scenarios, rubrics, and golden outputs. Two ways to test:

**Semantic quality (LLM-as-judge)** — run the `/test` skill:
```
/test                  # evaluate all skills
/test source-control   # evaluate one skill
```

**Format/schema assertions (CI)** — run promptfoo:
```bash
npx promptfoo eval           # run all format assertions
npx promptfoo eval --ci      # CI mode (exits non-zero on failure)
```

## Installation

Clone the repo and point Claude Code's `skillsDirectory` at the `skills/` folder:

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

## Adding a Plugin

See [CLAUDE.md](./CLAUDE.md) for conventions, or use the **plugin-architect** agent to interactively design and scaffold a new plugin.
