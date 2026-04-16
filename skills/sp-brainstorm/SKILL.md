---
name: sp-brainstorm
description: Use when starting a new feature or project and need to explore ideas and produce a design document
---

# Brainstorm

## Overview

Start the superpowers workflow with creative ideation. Produces a design specification and optionally sets up a worktree for isolated development.

**Announce at start:** "Using sp-brainstorm to kick off ideation."

## Prerequisites

- **Check:** Is this a git repository? Run `git rev-parse --is-inside-work-tree`
  - If no:warn that git is recommended. User can proceed but workflow will be limited.
- **Check:** Already in a worktree? Run `git worktree list`
  - If yes: note the worktree path. A new worktree is optional.

## Execute

1. **Invoke the superpowers brainstorming skill:**

   Call `superpowers:brainstorming` via the Skill tool.

   This skill will:
   - Facilitate creative exploration of your idea
   - Help narrow scope and define architecture
   - Optionally create a git worktree for the project
   - Produce a design specification document

2. **After the superpowers skill completes**, verify outputs:

   | Expected Output | How to Verify |
   |----------------|---------------|
   | Design document | Check for `docs/superpowers/plans/*-design.md` or similar |
   | Worktree (if created) | `git worktree list` shows new entry |

3. **If outputs are missing**, ask the user:
   - Was the brainstorming session productive?
   - Should we save a design document before moving on?

## Next Steps

Recommend **[PL] sp-plan** to translate the design into a detailed implementation plan.

```
✅ Brainstorm complete!

Next: [PL] sp-plan — Create your implementation plan
Invoke: /sp-plan
```
