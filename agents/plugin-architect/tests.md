# plugin-architect — Tests

## Scenarios

### 1. Design a new skill from scratch
**Input:** "I want a skill that generates API documentation from OpenAPI specs."
**Expected:** Agent checks marketplace.json for overlap, recommends `skill` type, drafts plugin.json with appropriate tags (`docs`), creates SKILL.md with clear trigger description, and proposes tests.md with at least 3 scenarios.

### 2. Overlap detection
**Input:** "I want a skill that explains code to me."
**Expected:** Agent identifies overlap with the existing `explain` skill, suggests extending it rather than creating a new plugin.

### 3. Recommend plugin type
**Input:** "I need something that connects to Jira and creates tickets from test failures."
**Expected:** Agent recommends `mcp` type (external API integration requiring a tool server), explains why skill/agent would be less appropriate.

### 4. Design an agent
**Input:** "I want an agent that runs a full regression suite, triages failures, and opens GitHub issues."
**Expected:** Agent recommends `agent` type (multi-step orchestration), drafts AGENT.md with clear workflow steps, identifies support files if needed.

## Rubric

| Criterion | Pass | Fail |
|-----------|------|------|
| Overlap check | Always checks marketplace.json before designing | Skips overlap check or creates duplicate |
| Type recommendation | Provides rationale for chosen plugin type | Picks type without explanation |
| plugin.json completeness | All required fields present and valid | Missing fields or invalid values |
| Description quality | Precise, serves as Tier 1 relevance signal | Vague or overly broad |
| Test coverage | At least 3 scenarios with rubric | Fewer than 3 scenarios or no rubric |

## Golden Set

### Golden 1 — New skill design
**Input:** "Create a skill that lints commit messages against Conventional Commits."

**Expected output (summary):**
- Name: `lint-commit`
- Type: `skill`
- Tags: `[git, quality]`
- Description: "Validates commit messages against the Conventional Commits specification, reporting violations and suggesting fixes."
- Tier: 2 (no support files needed)
- tests.md with scenarios: valid commit, invalid commit, breaking change notation
