# Superpowers Workflow — BMad Module

**English** | [中文](README_zh.md)

A phase-aware BMad workflow module that wraps the [superpowers](https://github.com/obra/superpowers) plugin, using BMad's orchestration to make superpowers' disciplined development process reliable and effortless.

## Why This Module?

The superpowers plugin provides excellent skills for disciplined development — brainstorming, planning, TDD execution, code review, verification. But in practice, the AI agent decides which skill to invoke based on the current conversation context. When the agent overlooks or skips a skill, the process breaks: steps get missed, quality gates are bypassed, and the workflow drifts off track.

BMad solves this problem. Its workflow orchestration enforces phase ordering, prerequisite checking, and required quality gates — ensuring the AI agent follows the superpowers process step by step instead of improvising. And `/bmad-help` keeps it simple: one command tells you where you are and what to do next, so you never have to track the workflow yourself.

## How It Works

**`/bmad-help`** is your single entry point — it detects where you are in the workflow and tells you exactly what to do next. Every skill also recommends the next step when it completes, so you always know what to run.

## Quick Start

```bash
# 1. Install
npx bmad-method install --custom-source https://github.com/CaffreySun/sp-workflow-bmad --tools claude-code --yes
```

After installation, open Claude Code in your project and run `/bmad-help`. It will detect that the module needs configuration and guide you through setup — you don't need to remember any commands.

Once configured, `/bmad-help` tells you which phase you're in, what's already done, and what to do next. Follow its recommendation after each skill completes.

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

After installation, run `/bmad-help` in your project — it will guide you through first-time setup and then navigate you through the workflow.

## Configuration

| Variable | Default | User Setting | Description |
|----------|---------|-------------|-------------|
| `sp_plans_folder` | `{project-root}/docs/superpowers/plans` | no | Where plan documents are saved |
| `sp_default_execution_mode` | `subagent` | yes | Default execution mode for sp-execute (`subagent` or `inline`) |

Skills read `sp_plans_folder` from `_bmad/config.yaml` at runtime; the default is used as fallback if not configured.

## License

MIT
