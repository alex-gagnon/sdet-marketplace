# What Makes a Good README

Source: GitHub Docs — "About READMEs"

## Purpose

A README is often the first thing a visitor sees when they land on a repository. It sets expectations, communicates value, and helps people decide whether to use or contribute to the project. A good README is also accompanied by a license, contribution guidelines, and a code of conduct — together these form the social contract of the project.

## What to Cover

A README should answer five questions:

1. **What does this project do?** — Describe it plainly. One or two sentences should be enough for most projects.
2. **Why is it useful?** — What problem does it solve? Who is it for?
3. **How do users get started?** — Installation, configuration, a minimal working example.
4. **Where can users get help?** — Issues tracker, discussion forum, contact info, wiki.
5. **Who maintains and contributes?** — Core maintainers, how to contribute, acknowledgments.

## Placement

GitHub surfaces a README automatically when it's placed in:
- `.github/` (highest priority)
- The repository root
- `docs/`

If multiple READMEs exist, GitHub uses this order of preference.

## Length and Scope

A README should contain only what developers need to **get started** and **contribute**. Longer documentation belongs in a wiki. Over-long READMEs bury the important parts — prefer linking out to docs for deep dives.

GitHub truncates READMEs beyond 500 KiB in the rendered view.

## Markdown Best Practices

**Table of contents**: GitHub auto-generates a TOC from headings for any Markdown file. Use meaningful heading names — they become anchor links.

**Section links**: Any heading automatically gets an anchor. Readers can link directly to sections; hovering over a heading exposes the link icon.

**Relative links**: Always prefer relative links over absolute URLs when linking to other files in the same repo. Relative links keep working across branches and forks; absolute links break in clones.

```markdown
# Good — relative link, survives forks and clones
[Contributing guidelines](docs/CONTRIBUTING.md)

# Risky — absolute link, breaks in clones
[Contributing guidelines](https://github.com/org/repo/blob/main/docs/CONTRIBUTING.md)
```

Link text must be on a single line — multi-line link text does not render as a link.

**Images**: Same rule applies — use relative paths for images committed to the repo.

## Structure Template

Use this as a starting point and trim what doesn't apply:

```markdown
# Project Name

One-sentence description of what this project does and who it's for.

## Why

Motivation — what problem does this solve, and why does it matter?

## Getting Started

### Prerequisites
...

### Installation
...

### Quick Example
...

## Usage
...

## Configuration
...

## Contributing

Link to CONTRIBUTING.md or inline brief guidelines.

## License

Link to LICENSE file.
```

## Profile READMEs

A public repository whose name matches your GitHub username gets special treatment — its README appears on your profile page. The same quality rules apply, but the audience is broader (not just developers evaluating the project).
