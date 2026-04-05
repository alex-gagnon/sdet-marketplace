---
name: test
version: 1.0.0
description: Runs quality evaluations against one or all skills using their tests.md fixture files, scoring format compliance and semantic correctness.
tags: [special]
---

# /test — Skill Test Runner

Evaluate the quality of one or all skills using their `tests.md` fixture files. Acts as both a format checker and an LLM-as-judge evaluator.

## Usage

- `/test` — runs all skills
- `/test <skill-name>` — runs only that skill (e.g., `/test commit`)

## What to Load

For each skill under test, load its `tests.md` file from the skill's folder (Tier 3). That file contains:
- **Scenarios** — realistic input contexts and what to invoke
- **Rubric** — named criteria with pass/fail descriptions
- **Golden Set** — 1–2 human-curated ideal responses for regression comparison

## Evaluation Protocol

For each scenario in `tests.md`:

1. **Simulate the skill** — mentally (or actually) apply the skill's `SKILL.md` instructions to the scenario's input context, producing an output.
2. **Format check** — verify the output matches the structural requirements in the skill's Output Format section. Score: Pass / Fail.
3. **Rubric score** — for each rubric criterion, score the output 1–3:
   - 3 = clearly meets the criterion
   - 2 = partially meets
   - 1 = does not meet
4. **Golden comparison** (if a golden exists for this scenario) — note whether the output meaningfully diverges from the golden. This is a flag, not a hard fail.

Run each scenario **independently** — do not carry state between scenarios.

## Output Format

```
## Skill Test Report

### <skill-name>
| Scenario | Format | Rubric Score | Golden Flag |
|---|---|---|---|
| <name> | ✓ Pass / ✗ Fail | <score>/<max> | — or ⚑ Diverges |

**Rubric breakdown** (for any scenario scoring below 70%):
- <criterion>: <score> — <one-line reason>

---
```

After all skills:

```
## Summary
| Skill | Scenarios | Format Pass | Avg Rubric | Flags |
|---|---|---|---|---|
| commit | 3 | 3/3 | 2.7/3 | — |
| ... | | | | |

**Action items:**
- <skill>: <what to fix if anything failed or scored low>
```

## Scoring Guidance

- **Format failures** are always actionable — the skill's output instructions may need clarification.
- **Rubric score < 2.0** average across a skill = likely needs prompt revision.
- **Golden flags** on unchanged skills = worth reviewing whether the model has drifted.
- **Golden flags** after a skill edit = expected; verify the change was intentional.

## Notes

- This skill evaluates skills by applying them to test scenarios. It does **not** actually run git commands or modify files — scenarios are evaluated as text-in/text-out exercises.
- For skills that require real repo context (e.g., `/commit`, `/branch`), the scenario provides a simulated git state description.
- If `tests.md` is missing for a skill, report: `<skill-name>: no tests.md found — skip`.
