# Documentation Templates

Use these as starting skeletons. Fill in all `<...>` placeholders. Remove sections that don't apply.

## JSDoc (TypeScript / JavaScript)

### Function

```ts
/**
 * <One-sentence summary of what this function does.>
 *
 * <Optional: 1–2 sentences on non-obvious behavior, constraints, or why it works this way.>
 *
 * @param paramName - <Description. Include type if not obvious from signature.>
 * @returns <What is returned, including shape for objects.>
 * @throws {ErrorType} <When this error is thrown.>
 *
 * @example
 * functionName(input) // => expectedOutput
 */
```

### Class

```ts
/**
 * <One-sentence description of the class's responsibility.>
 *
 * <Optional context: lifecycle, ownership, thread safety, etc.>
 *
 * @example
 * const instance = new ClassName(args)
 * instance.method()
 */
```

---

## Python Docstrings

### Google Style

```python
def function_name(param: Type) -> ReturnType:
    """One-sentence summary.

    Optional longer explanation of non-obvious behavior.

    Args:
        param: Description of the parameter.

    Returns:
        Description of the return value.

    Raises:
        ValueError: When the input is invalid.

    Example:
        >>> function_name(input)
        expected_output
    """
```

### NumPy Style

```python
def function_name(param):
    """
    One-sentence summary.

    Parameters
    ----------
    param : type
        Description.

    Returns
    -------
    type
        Description.

    Raises
    ------
    ValueError
        When the input is invalid.
    """
```

---

## GoDoc

```go
// FunctionName does <one-sentence description starting with the function name>.
//
// Optional: explain non-obvious behavior, preconditions, or why an approach was chosen.
// GoDoc renders the first sentence as a summary, so make it count.
//
// Example:
//
//	result, err := FunctionName(input)
func FunctionName(param Type) (ReturnType, error) {
```

```go
// PackageName provides <one-sentence description of the package's purpose>.
//
// Optional: list primary types or entry points the caller should know about.
package packagename
```

---

## README Sections

### Installation

```markdown
## Installation

**Requirements:** <language/runtime version, platform constraints>

```bash
# Package manager
npm install <package>
pip install <package>
go get <module>
```

<Any post-install steps (env vars, migrations, etc.)>
```

### Usage

```markdown
## Usage

```language
<Minimal working example — the fastest path to "it works">
```

<Brief explanation of what the example does and where to go next.>
```

### API Reference

```markdown
## API Reference

### `functionName(param)`

<One-sentence description.>

**Parameters**

| Name | Type | Description |
|---|---|---|
| `param` | `type` | Description |

**Returns** `ReturnType` — <description>

**Example**

```language
functionName(input) // => output
```
```

### Contributing

```markdown
## Contributing

1. Fork the repository and create a branch: `git switch -c feature/<description>`
2. Make your changes and add tests
3. Run `<test command>` — all tests must pass
4. Open a pull request with a clear description of the change

Please follow the existing code style. For significant changes, open an issue first to discuss the approach.
```
