# Superpowers Workflow — BMad Module

A phase-aware BMad workflow module that wraps the [superpowers](https://github.com/obra/superpowers) plugin, combining BMad's workflow orchestration with superpowers' disciplined execution capabilities.

## Workflow

```
[BR] Brainstorm → [PL] Write Plan → [EX] Execute → [RV] Review → [VF] Verify → [FN] Finish
                                       (inline / subagent)      ↑ required gate
Anytime: [WG] Workflow Guide | [TD] TDD | [DB] Debugging | [WT] Worktrees
```

Each skill delegates to the corresponding superpowers skill while adding:
- **Prerequisite checking** — warns if prior phase is incomplete
- **Output validation** — confirms expected artifacts were produced
- **Next-step guidance** — recommends the next skill in the workflow

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

| Menu Code | Skill | Phase | Delegates To |
|-----------|-------|-------|-------------|
| WG | sp-workflow-guide | anytime | (self-contained) |
| BR | sp-brainstorm | 1-brainstorm | superpowers:brainstorming |
| PL | sp-plan | 2-plan | superpowers:writing-plans |
| EX | sp-execute | 3-execute | superpowers:executing-plans / subagent-driven-development |
| TD | sp-tdd | anytime | superpowers:test-driven-development |
| DB | sp-debugging | anytime | superpowers:systematic-debugging |
| RV | sp-review | 4-review | superpowers:requesting-code-review + receiving-code-review |
| VF | sp-verify | 5-verify | superpowers:verification-before-completion |
| FN | sp-finish | 6-finish | superpowers:finishing-a-development-branch |
| WT | sp-worktrees | anytime | superpowers:using-git-worktrees |

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `sp_plans_folder` | `{project-root}/docs/superpowers/plans` | Where plan documents are saved |
| `sp_default_execution_mode` | `subagent` | Default execution mode for sp-execute (subagent or inline) |

## License

MIT
