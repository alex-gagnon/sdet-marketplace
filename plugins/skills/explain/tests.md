# Tests: explain

## Scenarios

### Scenario 1: beginner asking about recursion
**Input context:** User is learning Python, has no CS background. Asks `/explain` on a recursive `factorial(n)` function.
**Invoke:** `/explain`
**Expected format:** Plain prose explanation. No template required. Length fits complexity. No "Note:" line (no bugs in the code).

### Scenario 2: senior engineer asking about an unfamiliar pattern
**Input context:** Experienced developer encounters a Haskell-style `Maybe` monad pattern implemented in TypeScript. Asks `/explain`.
**Invoke:** `/explain`
**Expected format:** Plain prose, calibrated to expert level. Uses correct terminology. Shorter than Scenario 1 — doesn't over-explain basics.

### Scenario 3: code with a bug
**Input context:** User asks for an explanation of a Python snippet with an off-by-one error in a loop: `for i in range(len(arr) - 1)` when the last element should be included.
**Invoke:** `/explain`
**Expected format:** Plain prose explanation of what the code does AND a `Note:` line flagging the off-by-one issue.

### Scenario 4: architectural concept (no code)
**Input context:** User asks: "Explain event sourcing vs CQRS — when would I use one vs both?"
**Invoke:** `/explain`
**Expected format:** Plain prose. No code block required. Covers both concepts and the relationship between them.

## Rubric

1. **Expertise calibration** — explanation depth and vocabulary match the user's apparent level.
   - Pass: beginner gets analogies and plain language; expert gets precise terminology without hand-holding
   - Fail: explains closures to a senior engineer as if they've never heard of functions; or uses jargon with a beginner
2. **Accuracy** — the explanation is factually correct.
   - Pass: recursive factorial explanation correctly describes base case and call stack behavior
   - Fail: incorrect description of execution order, wrong claim about return values
3. **Bug flagging** — a `Note:` line appears when (and only when) there's a bug or significant concern.
   - Pass: off-by-one gets flagged; clean code gets no Note
   - Fail: Note appears on clean code (false positive), or bug is missed (false negative)
4. **Length fit** — explanation is as long as the subject requires, not longer.
   - Pass: simple factorial gets ~100 words; event sourcing vs CQRS gets ~250 words
   - Fail: 500-word essay on a 3-line function; one sentence on a complex architectural pattern
5. **No template rigidity** — output is prose, not a bullet-list template or fixed structure.
   - Pass: flowing paragraphs
   - Fail: `### What it does\n### Why it works\n### Key takeaways` — templated when not needed

## Golden Set

### Golden 1 — beginner recursion
**Input:** Beginner asking about `def factorial(n): return 1 if n == 0 else n * factorial(n-1)`
**Ideal output:**
```
This function calculates the factorial of a number — that is, n × (n-1) × (n-2) × … × 1.

It works by calling itself with a smaller number each time: `factorial(5)` calls `factorial(4)`, which calls `factorial(3)`, and so on until it reaches 0, where it stops and returns 1. Then all those calls "unwind" — each one multiplies its `n` by the result below it.

So `factorial(3)` becomes `3 × (2 × (1 × 1))` = 6.

The `n == 0` case is called the base case — without it, the function would call itself forever.
```
