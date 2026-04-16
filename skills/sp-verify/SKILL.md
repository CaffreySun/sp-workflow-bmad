---
name: sp-verify
description: Use when code is implemented and reviewed, and you need to verify all requirements are met before shipping
---

# Verify Before Completion

## Overview

Final quality gate. Verify every requirement from the spec/plan has been implemented, tested, and reviewed. No partial verification — if something is missing, it must be addressed before proceeding.

**Announce at start:** "Using sp-verify to verify all requirements are met."

**This is a required phase** — do not skip to sp-finish without verifying.

## Configuration

Resolve the plans folder path before proceeding:
1. Read `{project-root}/_bmad/config.yaml` → look for `sp.sp_plans_folder`
2. If not configured, fall back to `{project-root}/docs/superpowers/plans`
3. Use the resolved path to locate the plan/spec document

## Prerequisites

- **Check:** Was code review completed?
  - If not: warn and suggest `[RV] sp-review` first. This is a soft gate — user can proceed but the risk is higher.
- **REQUIRED:** A spec or plan document must exist to verify against.
  - Check `{plans-folder}/*.md`
  - If no plan found: **BLOCK** — cannot verify without requirements. Direct to `[PL] sp-plan`.

## Execute

1. **Invoke the superpowers verification skill:**

   Call `superpowers:verification-before-completion` via the Skill tool.

   This skill will:
   - Check spec traceability: every requirement has corresponding implementation
   - Verify test coverage: every feature has tests
   - Run full test suite: all tests pass, no regressions
   - Check edge cases: boundary conditions handled
   - Verify documentation: README, comments, API docs updated if needed

2. **After the superpowers skill completes**, verify outputs:

   | Expected Output | How to Verify |
   |----------------|---------------|
   | All requirements traced | Each spec item maps to code + tests |
   | Full test suite passes | `npm test` / `pytest` / etc. exits 0 |
   | No regressions | Previously passing tests still pass |
   | Edge cases covered | Boundary/empty/error cases have tests |
   | Verification report | Document or checklist confirming all checks |

3. **If verification fails:**
   - **Missing requirements** → Return to `[EX] sp-execute` for further implementation
   - **Test failures** → Use `[DB] sp-debugging` to investigate
   - **Missing tests** → Use `[TD] sp-tdd` to add test coverage
   - **Design issues** → May need `[PL] sp-plan` to rethink approach

## Next Steps

Recommend **[FN] sp-finish** to complete the development branch.

```
✅ Verification passed — all requirements met, tests green.

Next: [FN] sp-finish — Complete your development branch
Invoke: /sp-finish
```
