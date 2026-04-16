---
name: sp-review
description: Use when implementation is complete and code needs review for spec compliance and quality
---

# Code Review

## Overview

Request and receive a structured code review. Two-stage process: first check spec compliance (does the code do what was planned?), then check code quality (is it well-written?). After receiving feedback, address all issues.

**Announce at start:** "Using sp-review for code review."

## Prerequisites

- **Check:** Does implementation exist?
  - Run `git diff --stat` to see modified/added files
  - If no changes: warn — nothing to review. Direct to `[EX] sp-execute` first.
- **Check:** Do tests exist and pass?
  - If no tests: warn — code review without test coverage is incomplete. Suggest `[TD] sp-tdd` first.
  - Do NOT block, but make the risk clear.

## Execute

### Step 1: Request Review

1. Call `superpowers:requesting-code-review` via the Skill tool.

   This skill will:
   - Prepare the review context (changed files, test coverage, spec/plan reference)
   - Request a review covering spec compliance and code quality
   - Provide the reviewer with everything they need

### Step 2: Receive Review

2. Call `superpowers:receiving-code-review` via the Skill tool.

   This skill will:
   - Process the review feedback
   - Prioritize issues (critical, important, minor)
   - Address each issue with targeted fixes
   - Re-run tests after fixes

3. **After both skills complete**, verify outputs:

   | Expected Output | How to Verify |
   |----------------|---------------|
   | Review completed | Feedback was received and processed |
   | Critical issues addressed | All critical/high-priority items resolved |
   | Tests still pass | Full test suite passes after fixes |
   | Code quality improved | No major code smell flags remain |

4. **If review reveals significant issues** (spec drift, missing features):
   - May need to return to `[EX] sp-execute` for further implementation
   - Or `[DB] sp-debugging` for issues that look like bugs
   - Or `[TD] sp-tdd` for missing test coverage

## Next Steps

Recommend **[VF] sp-verify** for final verification against the original requirements.

```
✅ Code review complete — feedback addressed, tests passing.

Next: [VF] sp-verify — Final verification before shipping
Invoke: /sp-verify
```
