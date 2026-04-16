---
name: sp-worktrees
description: Use when you need to create or manage git worktrees for isolated parallel development
---

# Git Worktrees

## Overview

Create and manage git worktrees for isolated development. Worktrees let you work on multiple features in parallel without stashing or branching conflicts. Often used at the start of a new feature cycle.

**Announce at start:** "Using sp-worktrees for worktree management."

## When to Use

- Starting a new feature that needs isolation from main work
- Working on multiple features in parallel
- Need a clean workspace for brainstorming/planning
- Exiting/cleaning up after a feature is complete

## Prerequisites

- **REQUIRED:** Must be in a git repository.
  - `git rev-parse --is-inside-work-tree` must succeed.
  - If not: cannot use worktrees. Suggest `git init` first.
- **Check:** Already in a worktree?
  - `git worktree list` — if already in a worktree, creating another is fine but be aware of nesting.

## Execute

1. **Invoke the superpowers worktree skill:**

   Call `superpowers:using-git-worktrees` via the Skill tool.

   This skill will:
   - Create a new worktree with a named branch
   - Set up the worktree for development
   - Provide instructions for working in the worktree
   - When exiting: offer to keep or remove the worktree

2. **After the superpowers skill completes**, verify outputs:

   | Expected Output | How to Verify |
   |----------------|---------------|
   | Worktree created | `git worktree list` shows new entry |
   | On correct branch | `git branch --show-current` in worktree matches expected |
   | Worktree is clean | `git status` in worktree shows clean state |

## Next Steps

After creating a worktree, recommend starting the workflow inside it:

```
✅ Worktree ready at {path}

Start developing:
[BR] sp-brainstorm — Begin ideation in the new worktree
[PL] sp-plan — Skip to planning if you already have a design
```

After exiting/cleaning up a worktree:
```
✅ Worktree cleaned up.

[WG] sp-workflow-guide — Check overall project status
[BR] sp-brainstorm — Start a new feature cycle
```
