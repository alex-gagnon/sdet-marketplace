# Code Simplification Patterns

Reference this list when reviewing code for simplification opportunities. Apply the most impactful patterns first.

## Structure

- **Deep nesting** — more than 2–3 levels of indent is a signal. Apply early-return / guard clauses to flatten.
- **Inverted conditions** — `if (!x) { ... } else { doMainThing() }` → invert and return early.
- **Long functions** — if a function has more than ~30 lines and multiple responsibilities, consider extracting named helpers (only if the extracted piece has a clear name and is reused or tested independently).
- **Switch/if-else chains on type** — consider a dispatch map or polymorphism if there are ≥4 branches and they all follow the same shape.

## Duplication

- **Repeated literal values** — extract to a named constant.
- **Repeated logic blocks** — extract to a function if the block appears ≥2 times and has a clear purpose.
- **Similar conditional branches** — if two branches differ only in one variable, parameterize.

## Naming

- **Vague names** — `data`, `result`, `tmp`, `val`, `obj` hide intent. Rename to describe what the value represents.
- **Boolean flag parameters** — `doThing(true)` is unreadable. Replace with two named functions or an options object.
- **Misleading names** — if a variable named `user` contains a user ID (not a user object), fix the name.
- **Abbreviations** — unless they are universal in the domain (e.g., `id`, `url`), spell them out.

## Dead Code

- **Unused variables** — remove them.
- **Unreachable branches** — conditions that can never be true given the types/invariants above them.
- **Commented-out code** — delete it (version control preserves history).
- **Redundant default values** — assigning a value that is already the default.

## Overengineering

- **Premature abstraction** — a helper function used exactly once that doesn't simplify the call site.
- **Unnecessary indirection** — a wrapper that does nothing but delegate.
- **Configuration for things that never vary** — hardcode it until there's a real second case.
- **Over-generic types** — `Map<string, any>` when the shape is always the same structured object.
