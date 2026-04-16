# Superpowers Workflow — BMad Module

A phase-aware BMad workflow module that wraps the [superpowers](https://github.com/obra/superpowers) plugin, combining BMad's workflow orchestration with superpowers' disciplined execution capabilities.

## Workflow

```
[BR] Brainstorm → [PL] Write Plan → [EX] Execute → [RV] Review → [VF] Verify → [FN] Finish
                                       (inline / subagent)      ↑ required gate
Anytime: [WG] Workflow Guide | [TD] TDD | [DB] Debugging | [WT] Worktrees
```

### Phase Rules

| Phase | Skill | Gate | Description |
|-------|-------|------|-------------|
| 1-brainstorm | sp-brainstorm | soft | No design doc? Warn but allow override |
| 2-plan | sp-plan | **BLOCK** | Execution cannot start without a plan |
| 3-execute | sp-execute | soft | No plan file? Block; wrong branch? Warn |
| 4-review | sp-review | soft | No changes or no tests? Warn but allow |
| 5-verify | sp-verify | **BLOCK** | No plan/spec to verify against? Block |
| 6-finish | sp-finish | soft | Verification not done? Strong warn |

**Anytime skills** (no prerequisites): sp-tdd, sp-debugging, sp-worktrees — available at any phase.

Each skill delegates to the corresponding superpowers skill while adding:
- **Prerequisite checking** — warns or blocks if prior phase is incomplete
- **Output validation** — confirms expected artifacts were produced
- **Next-step guidance** — recommends the next skill in the workflow

## Quick Start

```bash
# 1. Install the module
npx bmad-method install --custom-source https://github.com/CaffreySun/sp-workflow-bmad --tools claude-code --yes

# 2. In your project, run setup to register and configure
/sp-setup

# 3. Start the workflow — brainstorm a new feature
/sp-brainstorm

# 4. Follow the recommended next steps after each skill completes:
#    brainstorm → plan → execute → review → verify → finish

# Feeling lost? Check where you are:
/sp-workflow-guide
```

### Typical Session

```
/sp-brainstorm        → produces design doc
/sp-plan              → produces implementation plan with TDD steps
/sp-execute           → implements plan (subagent-driven by default)
  ↳ bug found? → /sp-debugging   (anytime, returns to execution)
  ↳ need TDD?  → /sp-tdd         (anytime, returns to execution)
/sp-review            → two-stage code review (spec + quality)
/sp-verify            → final quality gate against requirements
/sp-finish            → clean commits, PR, worktree cleanup

# Want isolated development? Use worktrees:
/sp-worktrees         → create worktree before brainstorm
```

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

## Skills

| Menu Code | Skill | Phase | Delegates To | When to Use |
|-----------|-------|-------|-------------|-------------|
| WG | sp-workflow-guide | anytime | (self-contained) | Don't know where you are or what's next? Run this. |
| BR | sp-brainstorm | 1-brainstorm | superpowers:brainstorming | Starting a new feature — explore ideas, produce design doc. |
| PL | sp-plan | 2-plan | superpowers:writing-plans | Have a design — create a detailed implementation plan with TDD steps. |
| EX | sp-execute | 3-execute | superpowers:subagent-driven-development / executing-plans | Have a plan — implement it task-by-task. Two modes: subagent (recommended) or inline. |
| TD | sp-tdd | anytime | superpowers:test-driven-development | Small feature or bugfix that doesn't need a full plan — strict RED-GREEN-REFACTOR. |
| DB | sp-debugging | anytime | superpowers:systematic-debugging | Failing tests, runtime errors, regressions — hypothesis-driven root cause analysis. |
| RV | sp-review | 4-review | superpowers:requesting-code-review + receiving-code-review | Implementation done — two-stage review: spec compliance then code quality. |
| VF | sp-verify | 5-verify | superpowers:verification-before-completion | Review done — verify every requirement is implemented and tested. |
| FN | sp-finish | 6-finish | superpowers:finishing-a-development-branch | Verified — clean commits, push, create PR, cleanup worktree. |
| WT | sp-worktrees | anytime | superpowers:using-git-worktrees | Need isolated workspace — create/manage git worktrees for parallel development. |

## Configuration

| Variable | Default | User Setting | Description |
|----------|---------|-------------|-------------|
| `sp_plans_folder` | `{project-root}/docs/superpowers/plans` | no | Where plan documents are saved |
| `sp_default_execution_mode` | `subagent` | yes | Default execution mode for sp-execute (`subagent` or `inline`) |

Skills read `sp_plans_folder` from `_bmad/config.yaml` at runtime; the default is used as fallback if not configured.

## License

MIT
