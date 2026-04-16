---
name: sp-debugging
description: Use when encountering bugs, failing tests, or unexpected behavior that needs systematic root cause analysis
---

# Systematic Debugging

## Overview

Debug using a hypothesis-driven approach: form a hypothesis, test it, conclude. No random code changes. No "spray and pray." Available anytime bugs arise.

**Announce at start:** "Using sp-debugging for systematic root cause analysis."

## When to Use

- Tests fail unexpectedly during execution
- Runtime errors in development
- Regression after code changes
- Any behavior that doesn't match expectations

## Prerequisites

- No prerequisites — bugs don't wait for workflow phases.
- **Check:** Is there an error message or failing test?
  - If yes: pass it as context to the superpowers skill.
  - If no: help the user articulate the symptom first.

## Execute

1. **Invoke the superpowers systematic-debugging skill:**

   Call `superpowers:systematic-debugging` via the Skill tool.

   This skill will:
   - Form a specific hypothesis about the root cause
   - Design a minimal test to confirm or refute
   - Run the test and conclude based on evidence
   - Repeat until root cause is identified
   - Implement a targeted fix
   - Verify the fix resolves the original symptom without regressions

2. **After the superpowers skill completes**, verify outputs:

   | Expected Output | How to Verify |
   |----------------|---------------|
   | Root cause identified | A clear explanation of why the bug occurred |
   | Fix implemented | Code changed to address root cause (not symptoms) |
   | Original test passes | The symptom that triggered debugging is resolved |
   | No regressions | Run full test suite and confirm all pass |

3. **If the bug persists**, do NOT add more patches. Re-enter the hypothesis cycle.

## Next Steps

Return to the workflow phase where the bug was discovered.

```
✅ Bug fixed — root cause addressed, tests passing.

Returning to: {phase where debugging was triggered}
```

If debugging was triggered during:
- **sp-execute:** Resume execution from the failed task
- **sp-review:** Continue addressing review feedback
- **sp-verify:** Retry verification
- **Standalone:** Suggest `[RV] sp-review` or `[VF] sp-verify`
