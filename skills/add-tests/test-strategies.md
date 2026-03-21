# Test Strategies by Framework

Reference this file when writing tests to match the conventions of the detected framework.

## Jest / Vitest (TypeScript / JavaScript)

```ts
import { describe, it, expect, vi, beforeEach } from 'vitest' // or jest

describe('functionName', () => {
  it('returns X given valid input', () => {
    expect(functionName(input)).toBe(expected)
  })

  it('throws when input is invalid', () => {
    expect(() => functionName(badInput)).toThrow('expected message')
  })
})
```

- Use `vi.fn()` / `jest.fn()` only for dependencies that have side effects (I/O, time, randomness)
- Prefer `toBe` for primitives, `toEqual` for objects/arrays
- Async tests: use `async/await` with `resolves` / `rejects` matchers
- Reset mocks in `beforeEach` with `vi.clearAllMocks()`

## pytest (Python)

```python
import pytest

def test_returns_expected_for_valid_input():
    assert function_name(input) == expected

def test_raises_on_invalid_input():
    with pytest.raises(ValueError, match="expected message"):
        function_name(bad_input)

@pytest.mark.parametrize("input,expected", [
    (case1_in, case1_out),
    (case2_in, case2_out),
])
def test_parameterized(input, expected):
    assert function_name(input) == expected
```

- Use `conftest.py` for shared fixtures
- Prefer `@pytest.mark.parametrize` over loops in tests
- Use `monkeypatch` for mocking; avoid `unittest.mock` unless already in use

## Go

```go
func TestFunctionName(t *testing.T) {
    tests := []struct {
        name     string
        input    InputType
        expected OutputType
        wantErr  bool
    }{
        {"valid input", validInput, expectedOutput, false},
        {"invalid input", badInput, zero, true},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := FunctionName(tt.input)
            if (err != nil) != tt.wantErr {
                t.Errorf("unexpected error: %v", err)
            }
            if got != tt.expected {
                t.Errorf("got %v, want %v", got, tt.expected)
            }
        })
    }
}
```

- Always use table-driven tests
- Use `testify/assert` if it's already a dependency; otherwise use standard `t.Errorf`
- File naming: `foo_test.go` in the same package

## RSpec (Ruby)

```ruby
RSpec.describe ClassName do
  describe '#method_name' do
    context 'when input is valid' do
      it 'returns the expected value' do
        expect(subject.method_name(input)).to eq(expected)
      end
    end

    context 'when input is invalid' do
      it 'raises an error' do
        expect { subject.method_name(bad) }.to raise_error(ArgumentError)
      end
    end
  end
end
```

- Use `let` for lazily evaluated setup, `let!` for eager
- Use `subject` for the object under test
- Use `shared_examples` for behavior shared across multiple describes
- Prefer `expect(x).to eq(y)` over `x.should eq(y)`
