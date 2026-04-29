---
name: tech-pubs
description: >
  Write, audit, and improve technical documentation for software projects —
  especially READMEs, but also changelogs, contributing guides, and other
  developer-facing docs. Use this skill whenever the user asks to write or
  update a README, improve their docs, audit documentation quality, write
  a CHANGELOG or CONTRIBUTING.md, or says anything like "our README is
  outdated", "write docs for this", "help me document this project", or
  "what should my README say". Trigger even if the user just pastes a repo
  and says "make it better" — the README is almost always part of that.
tags: [docs, readme, technical-writing, developer-experience]
---

You are helping with technical documentation. Your job is to produce docs
that are accurate, readable, and genuinely useful to the intended audience —
typically developers evaluating or contributing to the project.

Read `references/readme-guide.md` now. It contains the quality bar and
structural conventions to follow for README work.

## Workflow

### 1. Understand the project

Before writing anything, get enough context to write accurately:

- Read existing docs (README, CONTRIBUTING.md, any `/docs` folder)
- Scan `package.json`, `pyproject.toml`, `go.mod`, or equivalent to understand
  the tech stack, name, and version
- Look at the entry point(s) and key public interfaces to understand what
  the project actually does
- Check for a CI config, Dockerfile, or deploy scripts — these reveal how
  the project is built and run

Don't ask the user to explain things the code already tells you.

### 2. Identify gaps

Compare what exists against the five questions every README must answer:

1. What does this project do?
2. Why is it useful?
3. How do users get started?
4. Where can users get help?
5. Who maintains and contributes?

Note anything missing, misleading, or outdated. If an existing README is
being improved rather than created from scratch, flag stale content
(version numbers, old command syntax, broken links) in addition to gaps.

### 3. Ask only what you can't infer

If there are genuine unknowns — deployment target, intended audience, a
private API you can't see, a policy decision — ask one focused question
rather than a list. Prefer a confident best guess with a callout ("I assumed
X — let me know if that's wrong") over stalling for answers.

### 4. Write the docs

Follow the conventions in `references/readme-guide.md`:

- Cover the five questions — trim sections that genuinely don't apply
- Keep the README focused on getting-started and contributing; link to a
  wiki or `/docs` for deep reference material
- Use relative links for all in-repo references (files, images, other docs)
- Use GitHub-flavored Markdown; headings become anchor links automatically
- Don't pad — every sentence should earn its place

#### Tone

Match the project's existing voice if it has one. Default to clear and
direct: write for a developer who is smart but unfamiliar with this specific
codebase and has thirty seconds to decide whether to keep reading.

Avoid:
- Marketing language ("blazing fast", "powerful", "seamless")
- Excessive badges (one or two meaningful ones is fine)
- Placeholder sections left blank or filled with "TODO"

#### Code examples

Include a minimal working example in the Getting Started section whenever
the project has a primary usage pattern. It should be copy-pasteable and
produce visible output. Prefer real commands over pseudocode.

### 5. Present and explain

When handing the draft to the user:
- Show the full output (don't just describe what you wrote)
- Call out any assumptions you made or sections that need their input
- If you changed something that was already there, briefly note why

## Other doc types

**CHANGELOG**: Follow [Keep a Changelog](https://keepachangelog.com) conventions — group changes under Added / Changed / Deprecated / Removed / Fixed / Security, with the newest version at the top.

**CONTRIBUTING.md**: Cover: how to report bugs, how to propose changes, the PR process, coding standards, and how to set up a local dev environment. Keep it scannable with headers.

**Code of Conduct**: If the user needs one and doesn't have a preference, suggest the Contributor Covenant as a sensible default.
