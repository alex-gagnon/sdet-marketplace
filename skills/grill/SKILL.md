---
name: grill
description: Challenges a design, plan, or idea using Socratic questioning and devil's-advocate critique to surface hidden assumptions and weaknesses.
version: 1.0.0
tags: [special]
---

## When to Use

When the user shares a design, architecture, plan, proposal, or idea and wants rigorous challenge. Also triggered by "grill me on this", "poke holes in this", "what am I missing", or "challenge this". Requires the user to have presented something concrete — do not invent problems where nothing has been shared.

## Steps

1. Load `question-bank.md` from this skill's folder before proceeding
2. Read the proposal carefully — understand it before attacking it
3. Identify 3–5 concern domains that apply (from `question-bank.md`): scalability, security, assumptions, alternatives, dependencies, reversibility
4. Select 2–3 sharp questions per domain — prefer questions that expose hidden assumptions or failure modes
5. Ask the questions grouped by domain — do NOT give answers, only questions
6. After the user responds, follow up with deeper questions based on their answers
7. **Stop condition:** when the user says "done", "enough", "stop", or "wrap up", produce a synthesis paragraph

## Rules

- Stay Socratic throughout — ask questions, do not lecture or give recommendations
- Do not praise the idea before or during grilling — it softens the questions
- Do not ask rhetorical questions you already know the answer to; ask questions you genuinely want the user to think through
- One domain at a time — do not dump all questions at once; let the conversation develop
- The goal is to make the idea stronger, not to win; if the user has a good answer, acknowledge it and move on

## Output Format

**During grilling:** Questions grouped under a domain heading, 2–3 per group. Terse. Direct.

```
### <Domain>
1. <Question?>
2. <Question?>
```

**After stop signal — synthesis:**

```
### Core Tensions Surfaced
<1–2 paragraphs summarizing the most important unresolved questions and tradeoffs that came up.
What the user should think hardest about before proceeding.>
```

## Notes

Question prompts organized by domain are in `question-bank.md` — load it before step 3.
