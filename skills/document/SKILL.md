---
name: document
description: Adds or improves inline documentation, docstrings, and README sections for a function, module, or project.
version: 1.0.0
tags: [docs]
---

## When to Use

When the user asks to document code, add docstrings, improve comments, write a README, or update API documentation. Target can be a function, a module, or a prose section of a README.

## Steps

1. Load `templates.md` from this skill's folder before proceeding
2. Read the target code or existing documentation in full
3. Detect the language and the documentation style already in use (JSDoc, Google-style Python docstrings, GoDoc, etc.) — match it exactly, do not introduce a different style
4. Select the appropriate template from `templates.md`
5. Write documentation that explains the "why" and the non-obvious parts — not just what the code does
6. For README sections: identify the audience (user vs. contributor) and write accordingly

## Rules

- Never document the self-evident — `// increments counter` above `counter++` is noise
- Always document parameters, return values, and thrown errors for public-facing functions
- Do not remove existing documentation without reading it first — it may contain intent not visible in the code
- Match the capitalization, punctuation, and tone of existing docs in the file
- If the project has a documentation generator (Typedoc, Sphinx, Godoc), format for that tool

## Output Format

The documented code inline (for function/module docs) or standalone markdown (for README sections). If adding to an existing file, show only the additions in context, not the full file.

## Notes

Documentation templates (JSDoc, Python docstrings, GoDoc, README sections) are in `templates.md` — load it before writing.
