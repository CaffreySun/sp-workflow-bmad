---
name: sp-tdd
description: Use when implementing any feature or bugfix with test-driven development, before writing implementation code
---

# Test-Driven Development

## Overview

Apply strict TDD discipline (RED-GREEN-REFACTOR) to implement a feature or fix a bug. Useful standalone for small changes that don't need a full plan, or anytime during development.

**Announce at start:** "Using sp-tdd for test-driven development."

## When to Use

- Adding a small feature (doesn't warrant a full plan)
- Fixing a bug (write a failing test first)
- Refactoring (ensure existing tests pass, then refactor)
- Part of sp-execute workflow (TDD steps are in the plan)

## Prerequisites

- No hard prerequisites — TDD can start anytime.
- **Check:** Does the project have a test runner configured?
  - If not: help set up a minimal test configuration first.

## Execute

1. **Invoke the superpowers TDD skill:**

   Call `superpowers:test-driven-development` via the Skill tool.

   This skill enforces:
   - **RED:** Write a failing test first. Watch it fail.
   - **GREEN:** Write minimal code to make the test pass. Watch it pass.
   - **REFACTOR:** Clean up while keeping tests green.
   - **The Iron Law:** Never write implementation before a failing test. No exceptions.

2. **After the superpowers skill completes**, verify outputs:

   | Expected Output | How to Verify |
   |----------------|---------------|
   | Test file(s) | Tests exist covering the described behavior |
   | Implementation | Code that makes tests pass |
   | All tests green | Run the test suite and confirm pass |

3. **If tests are red**, do NOT proceed. Debug or adjust until green.

## Next Steps

Context-dependent:

- **If part of sp-execute workflow:** Return to the executing plan.
- **If standalone for a new feature:** Recommend `[RV] sp-review` for code review.
- **If fixing a bug during execution:** Return to the current workflow phase.

```
✅ TDD cycle complete — tests passing!

Where to next?
- Part of execution? → Continue with sp-execute
- Standalone? → [RV] sp-review for code review
- More TDD cycles? → Run sp-tdd again
```
