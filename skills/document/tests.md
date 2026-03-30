# Tests: document

## Scenarios

### Scenario 1: undocumented function
**Input context:** A Python function `def merge_intervals(intervals)` with no docstring. The function merges overlapping intervals in a list of `[start, end]` pairs.
**Invoke:** `/document`
**Expected format:** Documented code inline — the function with a docstring added. No full-file rewrite if the function was shown in isolation.

### Scenario 2: README section for a module
**Input context:** A `utils/` directory with helper functions. User asks for a README section describing the module's purpose and key functions.
**Invoke:** `/document`
**Expected format:** Standalone markdown (not inline code). Describes the module's purpose and at least the top 2–3 functions.

### Scenario 3: already-documented function needing improvement
**Input context:** A TypeScript function has a one-line JSDoc comment `/** Gets user */` on a `getUser(id, options)` function with 4 parameters and 2 possible return types.
**Invoke:** `/document`
**Expected format:** Improved inline documentation — expanded JSDoc with `@param`, `@returns`, and a meaningful description. Shows only the addition/change, not the full file.

### Scenario 4: complex function with side effects
**Input context:** A Go function `SyncInventory(ctx context.Context, storeID string)` that calls an external API, updates a DB, and emits events. No existing docs.
**Invoke:** `/document`
**Expected format:** Docstring/comment clearly notes the side effects (DB write, external call, event emission). Parameters and return type documented.

## Rubric

1. **Accuracy** — documentation correctly describes what the code actually does (not what it sounds like it might do).
   - Pass: docstring for `merge_intervals` correctly describes the merging behavior and return type
   - Fail: generic description that could apply to any function, or factually wrong description
2. **Completeness** — parameters, return values, and notable behaviors (side effects, errors thrown) are all documented.
   - Pass: all params named and described; return type and shape explained
   - Fail: "Args: intervals" with no type or description
3. **Format fit** — uses the correct documentation format for the language (Python docstring, JSDoc, Go comment, Markdown for README).
   - Pass: Python gets `"""..."""`, TypeScript gets `/** ... @param ... @returns ... */`
   - Fail: language-agnostic comments, or wrong style for the target language
4. **Additions only** — shows only the new/changed documentation in context, not the full surrounding file.
   - Pass: shows function with new docstring; surrounding code omitted
   - Fail: outputs 200+ lines of unmodified surrounding code
5. **Side-effect disclosure** — functions with side effects (DB, network, events) have those noted in the docs.
   - Pass: "This function writes to the inventory table and emits an `inventory.synced` event."
   - Fail: side effects undocumented or buried

## Golden Set

### Golden 1 — undocumented Python function
**Input:** `def merge_intervals(intervals): ...` (merges overlapping [start, end] pairs)
**Ideal output:**
```python
def merge_intervals(intervals):
    """Merge overlapping intervals in a list of [start, end] pairs.

    Sorts intervals by start point, then merges any that overlap or are
    adjacent. Returns a new list; does not modify the input.

    Args:
        intervals: List of [start, end] pairs (ints or floats). May be unsorted.

    Returns:
        List of merged [start, end] pairs, sorted by start point.

    Example:
        merge_intervals([[1,3],[2,6],[8,10]]) -> [[1,6],[8,10]]
    """
```
