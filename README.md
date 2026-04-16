# Superpowers Workflow — BMad Module

A phase-aware BMad workflow module that wraps the [superpowers](https://github.com/obra/superpowers) plugin, combining BMad's workflow orchestration with superpowers' disciplined execution capabilities.

## How It Works

You don't need to memorize skill names or phase order. **`/bmad-help`** is your single entry point — it detects where you are in the workflow and tells you exactly what to do next.

Every skill also recommends the next step when it completes, so you always know what to run.

## Quick Start

```bash
# 1. Install
npx bmad-method install --custom-source https://github.com/CaffreySun/sp-workflow-bmad --tools claude-code --yes

# 2. Setup (first time only)
/sp-setup

# 3. That's it — let bmad-help guide you
/bmad-help
```

`/bmad-help` will tell you which phase you're in, what's already done, and what to invoke next. Follow its recommendation, and repeat after each skill completes.

## Workflow Overview

```
[BR] Brainstorm → [PL] Write Plan → [EX] Execute → [RV] Review → [VF] Verify → [FN] Finish
                                       (inline / subagent)      ↑ required gate
Anytime: [WG] Workflow Guide | [TD] TDD | [DB] Debugging | [WT] Worktrees
```

The workflow is linear with two required gates — you must have a plan to execute, and you must verify before finishing. Other phases are soft gates (warned but overridable). Anytime skills can be used at any point.

### Phase Details

| Phase | Skill | Gate | What It Does |
|-------|-------|------|-------------|
| 1-brainstorm | sp-brainstorm | soft | Explore ideas, produce design doc |
| 2-plan | sp-plan | **BLOCK** | Create implementation plan with TDD steps — required before execution |
| 3-execute | sp-execute | soft | Implement plan task-by-task (subagent or inline mode) |
| 4-review | sp-review | soft | Two-stage code review: spec compliance then code quality |
| 5-verify | sp-verify | **BLOCK** | Verify all requirements met — required before finishing |
| 6-finish | sp-finish | soft | Clean commits, create PR, cleanup worktree |

**Anytime skills**: sp-tdd (strict TDD cycles), sp-debugging (systematic root cause analysis), sp-worktrees (isolated parallel development) — available at any phase, no prerequisites.

## Skill Reference

These are the skills registered with bmad-help. You can invoke them directly, but `/bmad-help` will recommend the right one at the right time.

| Code | Skill | When to Use |
|------|-------|-------------|
| WG | sp-workflow-guide | Don't know where you are? Detects current phase and recommends next step (self-contained, no delegation) |
| BR | sp-brainstorm | Starting a new feature — explore ideas, produce design doc |
| PL | sp-plan | Have a design — create detailed implementation plan with TDD steps |
| EX | sp-execute | Have a plan — implement it task-by-task (subagent or inline) |
| TD | sp-tdd | Small change — strict RED-GREEN-REFACTOR without a full plan |
| DB | sp-debugging | Failing tests, runtime errors — hypothesis-driven root cause analysis |
| RV | sp-review | Implementation done — two-stage review (spec + quality) |
| VF | sp-verify | Review done — verify every requirement is implemented and tested |
| FN | sp-finish | Verified — clean commits, push, create PR, cleanup worktree |
| WT | sp-worktrees | Need isolation — create/manage git worktrees for parallel work |

## Prerequisites

- [Claude Code](https://claude.ai/code) with the [superpowers](https://github.com/obra/superpowers) plugin installed
- Git

## Installation

```bash
# Interactive
npx bmad-method install

# Non-interactive
npx bmad-method install --custom-source https://github.com/CaffreySun/sp-workflow-bmad --tools claude-code --yes
```

After installation, run `/sp-setup` in your project to register the module and configure options.

## Configuration

| Variable | Default | User Setting | Description |
|----------|---------|-------------|-------------|
| `sp_plans_folder` | `{project-root}/docs/superpowers/plans` | no | Where plan documents are saved |
| `sp_default_execution_mode` | `subagent` | yes | Default execution mode for sp-execute (`subagent` or `inline`) |

Skills read `sp_plans_folder` from `_bmad/config.yaml` at runtime; the default is used as fallback if not configured.

## License

MIT
