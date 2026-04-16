---
name: sp-execute
description: Use when you have an implementation plan ready and need to execute it task-by-task with TDD discipline
---

# Execute Plan

## Overview

Execute the implementation plan task-by-task. Choose between two execution modes: subagent-driven (recommended) or inline. TDD discipline is built into the plan format — every task follows RED-GREEN-REFACTOR.

**Announce at start:** "Using sp-execute to implement the plan."

## Prerequisites

- **REQUIRED:** A plan file must exist.
  - Check `docs/superpowers/plans/*.md` for a file with task checkboxes.
  - If no plan found: **BLOCK** — direct user to `[PL] sp-plan` first. Cannot execute without a plan.
- **Check:** Correct git branch?
  - `git branch --show-current` should match the feature branch.
  - If on main/master: warn that execution should happen on a feature branch.

## Mode Selection

Present this choice at the start:

```
📊 Execution Mode

1. Subagent-Driven (recommended)
   - Fresh subagent per task
   - Review between tasks for quality
   - Better isolation, easier to rerun failed tasks
   - Best for: plans with many tasks, complex implementations

2. Inline Execution
   - Execute tasks sequentially in this session
   - Batch execution with checkpoint reviews
   - Faster for small plans
   - Best for: small plans (1-3 tasks), quick fixes

Choose [1/2]:
```

**Config default:** If `sp_default_execution_mode` is set (in `_bmad/config.yaml`), use that as default but still allow override.

## Execute

### If Subagent-Driven Mode:

1. Call `superpowers:subagent-driven-development` via the Skill tool.

   This skill will:
   - Dispatch a fresh subagent for each plan task
   - Run two-stage review between tasks (spec compliance, then code quality)
   - Track progress via plan checkbox updates
   - Handle failures gracefully — can rerun individual tasks

### If Inline Mode:

1. Call `superpowers:executing-plans` via the Skill tool.

   This skill will:
   - Execute tasks sequentially with checkpoint reviews
   - Batch related steps for efficiency
   - Track progress via plan checkbox updates

### After execution completes:

2. **Verify outputs:**

   | Expected Output | How to Verify |
   |----------------|---------------|
   | Implementation files | Source files exist as specified in plan |
   | Test files | Test files exist with passing tests |
   | Plan checkboxes updated | Tasks marked `[x]` in plan file |
   | Git commits | Logical commits for each task |

3. **Run full test suite** to confirm no regressions:
   ```bash
   # Use the project's test command
   npm test / pytest / go test ./... / etc.
   ```

4. **If tests fail**, recommend `[DB] sp-debugging` to investigate.

## Monitoring During Execution

While executing, if bugs arise:
- **Pause execution** — do not push through failing tests
- Recommend `[DB] sp-debugging` for systematic investigation
- After bug is fixed, resume execution from the failed task

## Next Steps

Recommend **[RV] sp-review** for code review.

```
✅ Plan executed! All tasks complete, tests passing.

Next: [RV] sp-review — Get your code reviewed
Invoke: /sp-review
```
