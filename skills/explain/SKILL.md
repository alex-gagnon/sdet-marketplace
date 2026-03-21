---
name: explain
description: Explains a piece of code, architecture decision, or technical concept in plain language calibrated to the user's apparent expertise level.
version: 1.0.0
tags: [docs]
---

## When to Use

When the user asks "what does this do", "explain this", "how does X work", "walk me through this", or pastes code with a question. No preconditions — works on any code snippet, file, concept, or architecture.

## Steps

1. Read the target in full before writing anything
2. Infer the user's expertise level from how they asked:
   - Beginner phrasing ("what does this even do") → use analogies, avoid jargon
   - Intermediate ("how does X work") → explain mechanisms and data flow
   - Advanced ("why does it do X instead of Y") → focus on tradeoffs and edge cases
3. Structure the explanation:
   - One-sentence summary of what the thing does
   - Key mechanisms or steps (in order of importance, not code order)
   - A concrete example if it makes the concept clearer
4. If the code has a bug, smell, or concern, note it briefly at the end — do not let it derail the explanation

## Rules

- Prefer prose over bullet points — bullets fragment reasoning and hide the connections between ideas
- Never over-explain things the user clearly already knows based on how they asked
- Calibrate length to complexity: a 3-line function gets 2–3 sentences; a 200-line module may warrant several paragraphs
- Do not moralize about code style unless asked — the task is to explain, not critique

## Output Format

Plain prose explanation. No fixed template — length and structure should fit the complexity of the target. End with a "Note:" line only if there's a bug or significant concern worth flagging.
