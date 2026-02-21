---
description: Strict TDD Red-Green-Refactor Workflow
---

This workflow enforces strict Test-Driven Development (TDD) for the Aethelgard-QGF project.

## The TDD Cycle

### 1. RED: Write a Failing Test

Before writing any code, write a test that describes the new functionality.

- Place the test in `tests/test_[module_name].py`.
- Run the test to ensure it fails.
  // turbo

```powershell
pytest tests/
```

### 2. GREEN: Make it Pass

Write the minimum amount of code required to make the test pass.

- Do not add extra features yet.
- Ensure all tests pass.
  // turbo

```powershell
pytest tests/
```

### 3. REFACTOR: Clean Up

Refactor the code while ensuring tests remain green.

- Improve variable names, structure, and performance.
- Run tests again to verify no regressions.
  // turbo

```powershell
pytest tests/
```

## Quality Standards

- **Coverage**: Maintain 100% coverage on core logic.
- **Linting**: No `ruff` errors allowed.
  // turbo

```powershell
ruff check .
```
