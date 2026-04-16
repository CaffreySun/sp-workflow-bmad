---
name: sp-finish
description: Use when verification is complete and you need to finalize the development branch, clean up commits, and create a PR
---

# Finish Development Branch

## Overview

Complete the development branch: clean up commits, ensure everything is committed, create a pull request, and clean up the worktree if applicable. The final step of the superpowers workflow.

**Announce at start:** "Using sp-finish to complete the development branch."

## Prerequisites

- **Check:** Was verification completed?
  - If not: warn strongly and suggest `[VF] sp-verify` first. Skipping verification means unverified code ships.
- **Check:** Are we on the correct feature branch?
  - `git branch --show-current` — should NOT be main/master.
  - If on main: warn that finishing should happen on a feature branch.
- **Check:** Working tree status?
  - `git status` — any uncommitted changes will need to be committed first.

## Execute

1. **Invoke the superpowers finishing skill:**

   Call `superpowers:finishing-a-development-branch` via the Skill tool.

   This skill will:
   - Clean up commit history if needed (squash, rebase)
   - Ensure all changes are committed
   - Push the branch to remote
   - Create a pull request with proper description
   - Clean up worktree if one was created
   - Provide next-step guidance

2. **After the superpowers skill completes**, verify outputs:

   | Expected Output | How to Verify |
   |----------------|---------------|
   | Clean commit history | Commits are logical and well-described |
   | Branch pushed | `git log origin/<branch>` matches local |
   | PR created | PR URL returned |
   | Worktree cleaned (if applicable) | `git worktree list` no longer shows it |
   | Working tree clean | `git status` shows no uncommitted changes |

## Next Steps

The development cycle is complete! Offer to start a new cycle.

```
🎉 Development branch complete!

PR: {pr-url}

Ready for the next feature?
[BR] sp-brainstorm — Start a new brainstorming session
```

Also remind the user about anytime skills if they want to continue with other work:
- `[WT] sp-worktrees` — Set up a new worktree for parallel work
- `[WG] sp-workflow-guide` — Check overall project status
