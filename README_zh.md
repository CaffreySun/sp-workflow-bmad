# Superpowers Workflow — BMad 模块

[English](README.md) | **中文**

一个阶段感知的 BMad 工作流模块，封装 [superpowers](https://github.com/obra/superpowers) 插件，通过 BMad 的编排能力让 superpowers 的规范开发流程可靠且省心。

## 为什么需要这个模块？

superpowers 插件提供了优秀的规范开发技能——头脑风暴、计划编写、TDD 执行、代码审查、验证交付。但在实际使用中，AI agent 是根据当前对话上下文自行判断该调用哪个技能的。一旦 agent 疏忽遗漏了某个步骤，流程就会出问题：关键步骤被跳过、质量门控被绕过、开发流程偏离轨道。

BMad 解决了这个问题。它的流程编排强制执行阶段顺序、前置条件检查和必需的质量门控——确保 AI agent 按部就班地执行 superpowers 流程，而非即兴发挥。而 `/bmad-help` 让一切更简单：一条命令就能告诉你当前处于哪个阶段、下一步该做什么，你完全不需要自己追踪工作流。

## 工作方式

**`/bmad-help`** 是你的唯一入口——它检测你在工作流中的位置，告诉你接下来该做什么。每个技能完成后也会推荐下一步，让你始终知道该运行什么。

## 快速开始

```bash
# 1. 安装
npx bmad-method install --custom-source https://github.com/CaffreySun/sp-workflow-bmad --tools claude-code --yes

# 2. 初始化（仅首次）
/sp-setup

# 3. 就这些——让 bmad-help 引导你
/bmad-help
```

`/bmad-help` 会告诉你当前处于哪个阶段、已完成什么、下一步该调用什么。按照它的推荐操作，每个技能完成后再重复即可。

## 工作流概览

```
[BR] 头脑风暴 → [PL] 编写计划 → [EX] 执行 → [RV] 代码审查 → [VF] 验证 → [FN] 完成
                                    (内联 / 子代理)        ↑ 必需门控
随时可用：[WG] 工作流导航 | [TD] TDD | [DB] 调试 | [WT] 工作树
```

工作流是线性的，包含两个必需门控——必须先有计划才能执行，必须先验证才能完成。其他阶段为软门控（会警告但可覆盖）。随时可用的技能可在任何阶段使用。

### 阶段详情

| 阶段 | 技能 | 门控 | 说明 |
|------|------|------|------|
| 1-头脑风暴 | sp-brainstorm | 软 | 探索想法，产出设计文档 |
| 2-编写计划 | sp-plan | **阻断** | 创建含 TDD 步骤的实现计划——执行前的必需步骤 |
| 3-执行 | sp-execute | 软 | 逐任务执行计划（子代理或内联模式） |
| 4-代码审查 | sp-review | 软 | 两阶段审查：规格合规性 + 代码质量 |
| 5-验证 | sp-verify | **阻断** | 验证所有需求已实现——完成前的必需步骤 |
| 6-完成 | sp-finish | 软 | 清理提交、创建 PR、清理工作树 |

**随时可用的技能**：sp-tdd（严格 TDD 循环）、sp-debugging（系统性根因分析）、sp-worktrees（隔离的并行开发）——无需前置条件，任何阶段可用。

## 技能参考

以下技能已注册到 bmad-help。你可以直接调用它们，但 `/bmad-help` 会在正确的时间推荐正确的技能。

| 代码 | 技能 | 何时使用 |
|------|------|----------|
| WG | sp-workflow-guide | 不知道自己在哪？检测当前阶段并推荐下一步（自包含，不委托其他技能） |
| BR | sp-brainstorm | 开始新功能——探索想法，产出设计文档 |
| PL | sp-plan | 已有设计——创建含 TDD 步骤的详细实现计划 |
| EX | sp-execute | 已有计划——逐任务执行（子代理或内联模式） |
| TD | sp-tdd | 小改动——不需要完整计划的严格 RED-GREEN-REFACTOR |
| DB | sp-debugging | 测试失败、运行时错误——假设驱动的根因分析 |
| RV | sp-review | 实现完成——两阶段审查（规格 + 质量） |
| VF | sp-verify | 审查完成——验证所有需求已实现并测试 |
| FN | sp-finish | 验证通过——清理提交、推送、创建 PR、清理工作树 |
| WT | sp-worktrees | 需要隔离——创建/管理 git 工作树进行并行开发 |

## 前置条件

- 已安装 [superpowers](https://github.com/obra/superpowers) 插件的 [Claude Code](https://claude.ai/code)
- Git

## 安装

```bash
# 交互式
npx bmad-method install

# 非交互式
npx bmad-method install --custom-source https://github.com/CaffreySun/sp-workflow-bmad --tools claude-code --yes
```

安装后，在项目中运行 `/sp-setup` 注册模块并配置选项。

## 配置

| 变量 | 默认值 | 用户设置 | 说明 |
|------|--------|----------|------|
| `sp_plans_folder` | `{project-root}/docs/superpowers/plans` | 否 | 计划文档保存位置 |
| `sp_default_execution_mode` | `subagent` | 是 | sp-execute 的默认执行模式（`subagent` 或 `inline`） |

技能运行时从 `_bmad/config.yaml` 读取 `sp_plans_folder`；未配置时使用默认值。

## 许可证

MIT
