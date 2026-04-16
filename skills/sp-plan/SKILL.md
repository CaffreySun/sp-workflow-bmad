---
name: sp-plan
description: Use when you have a design or spec and need a detailed implementation plan with TDD steps before writing code
---

# Write Plan

## Overview

Create a comprehensive, bite-sized implementation plan following superpowers' exacting format: no placeholders, exact file paths, TDD steps, and complete code in every step.

**Announce at start:** "Using sp-plan to create the implementation plan."

**This is a required phase** — execution cannot proceed without a plan.

## Configuration

Resolve the plans folder path before proceeding:
1. Read `{project-root}/_bmad/config.yaml` → look for `sp.sp_plans_folder`
2. If not configured, fall back to `{project-root}/docs/superpowers/plans`
3. Use the resolved path for all file checks and save locations below

## Prerequisites

- **Check:** Does a design document or spec exist?
  - Look in `{plans-folder}/*-design.md` or `*-brainstorm*.md`
  - Also check for any markdown file in `{plans-folder}/` that describes the feature
  - If found: proceed.
  - If NOT found: warn the user and suggest `[BR] sp-brainstorm` first. Do NOT block — user may have the design in mind.
- **Check:** Are we in the correct worktree? (if applicable)
  - If a worktree was created during brainstorming, confirm we're in it.

## Execute

1. **Invoke the superpowers writing-plans skill:**

   Call `superpowers:writing-plans` via the Skill tool.

   This skill will:
   - Write a plan with bite-sized tasks (2-5 min each)
   - Include exact file paths, complete code, and exact commands
   - Follow TDD discipline: failing test → run → implement → run → commit
   - Include a self-review step for spec coverage
   - Save the plan to `{plans-folder}/YYYY-MM-DD-<feature-name>.md`

2. **After the superpowers skill completes**, verify outputs:

   | Expected Output | How to Verify |
   |----------------|---------------|
   | Plan file created | Check `{plans-folder}/*.md` for new file |
   | Plan has task structure | File contains `### Task N:` headings with checkbox steps |
   | No placeholders | Scan for TBD, TODO, "implement later", "add appropriate" |

3. **If plan has placeholders or is incomplete**, flag it to the user. The superpowers writing-plans skill should have caught these, but double-check.

## Next Steps

Recommend **[EX] sp-execute** to execute the plan.

```
✅ Plan written and saved!

Next: [EX] sp-execute — Execute your implementation plan
Invoke: /sp-execute
```

Also note: the plan document itself will offer the execution mode choice (subagent-driven vs inline), which sp-execute will handle.
