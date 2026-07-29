---
name: agent-workflow
description: Multi-agent engineering workflow harness for project development. Two trigger classes. (1) Governance — initialize (bootstrap), audit, or upgrade a repository's development governance; define Architect/Developer/UI/QA/Beta responsibilities; add Design and release gates; standardize commit planning; create or migrate two-layer todo ledgers; enforce context-loading and archive rules. (2) Daily role startup — when the user asks to start or continue a session as Architect, Developer, UI, QA, or Beta (e.g. "以 Developer 角色开工", "作为 QA 验收这张卡", "按工作流开发这个功能"), load the matching role section and the project's workflow delta before working. Do not use for ordinary feature implementation when no role or governance context is requested.
---

# Agent Workflow

**version: 1.2.1**

本 Skill 是跨项目复用的开发工作流引擎，也是**唯一的可复用规则源**：角色职责、流程、台账 schema、Design Gate、提交规划规则都只在这里维护。目标项目不复制通用规则，只保留一份薄 delta 文件（`develop/dev/workflow.md`，见下文契约）记录项目专属边界，以及项目自己的 Todo 台账。禁止把通用模板目录复制进项目或制造第二套模板源。

## 执行模式

先判断本次属于哪种模式，再按表装载最小必要内容；不要默认读完所有 references。

| 模式 | 触发场景 | 装载 |
|---|---|---|
| **role-startup** | 日常开发：用户要求以某角色开工/验收/设计 | `references/roles.md` 对应角色节 + 项目 delta + 项目规则 |
| **bootstrap** | 新项目建立治理 | `references/bootstrap.md` + `roles.md` + `todo-templates.md` |
| **upgrade** | 旧项目补齐/收敛到本工作流 | `references/bootstrap.md`（升级章）+ `todo-templates.md` + `checklist.md` |
| **audit** | 只检查治理现状，不改文件 | `references/checklist.md`（用户未要求修改时不写文件） |

## role-startup（日常角色启动）

1. 读项目规则（`CLAUDE.md` / `AGENTS.md`）。
2. 读项目 delta：`develop/dev/workflow.md`。缺失时：若存在旧版 `develop/dev/agents/` 角色文件则按其启动（旧布局仍有效）；两者都没有说明项目未 bootstrap，向用户确认是否执行 bootstrap。
3. 读 `references/roles.md` 中**对应角色一节**（不读全文件）。
4. 按台账上下文装载规则读当前任务卡（Todo 总览 + 当前里程碑 + 卡显式引用的文档；历史里程碑默认不读）。

**优先级**：用户当前要求 > 项目 delta 的边界 > 本 Skill 通用规则。项目 delta 与通用规则冲突时以 delta 为准并向用户提示差异。

## 标准开发流程

默认顺序；核心循环是 **Architect（planner）→ Developer（coder）→ QA（reviewer + tester）**。UI 是 Developer 的可选视觉子阶段（UI pass），仅在有界面工作时执行、视觉量大时才单开会话；Beta 默认不是常驻角色，而是里程碑收口/上线前由 Architect 建的 release-checklist 卡。任何任务不得跳过 QA。

1. **用户提出目标**：功能、问题、缺陷或里程碑。
2. **Architect 接单**：读取最小上下文，澄清范围、边界、风险和需要用户决定的事项。
3. **Design 判断**：Architect 在 Todo 标记 `Design Required: yes/no` 并写明理由。局部、无契约变化的修改可以为 `no`；跨模块、新数据模型/API/服务、权限/租户/密钥、迁移/部署/HA 或重大 UI 重构必须为 `yes`。
4. **Design Gate**：需要设计时，先创建或更新项目设计文档；在 Todo 中记录设计任务、文档路径和 `draft/approved`。设计未批准时不得交给 Developer。
5. **Architect 建实现任务卡**：更新两层 Todo，引用已批准设计，给出实现步骤、文件/模块范围、验收标准、QA 重点、停止条件和提交规划。
6. **Developer 实现**：检查 Design Gate 后，只在任务卡边界内开发，完成聚焦测试并回填实际证据。
7. **UI pass（可选）**：仅在存在用户界面时执行；属 Developer 阶段的视觉子阶段，保持功能行为不变并回填视觉证据；视觉工作量大或需要设计语言聚焦时才单开 UI 会话。
8. **QA 验证（review + test）**：独立执行，两步走——先**代码审查**（读 diff：可维护性、隐藏耦合、安全反模式、与项目惯例的一致性；代码质量问题同样可 FAIL），再**行为验收**（按验收标准实测）；失败则退回 Developer、UI 或 Architect，不允许带失败进入发布。
9. **Release Gate（Beta 清单卡）**：里程碑收口或上线前，由 Architect 建 release-checklist 卡执行真实工作流和发布就绪检查（安全/备份/回滚/长链路），给出 GO 建议；不重跑 QA 已验内容。高风险项目可将其升格为独立 Beta 会话。
10. **决策与发布**：自动化条件清晰且低风险时按门禁结果推进；符合用户拍板规则时等待用户确认。
11. **归档**：任务和里程碑完成后，收敛总览，把历史摘要移动到对应子 Todo 的 `## 归档摘要`；设计文档作为架构基线保留，废弃方案标记为 superseded 或归档。

## 核心不变量（所有模式必须遵守）

- **提交规划 ≠ 提交授权**。提交拆分、message、敏感检查和实际 stage/commit/push 一律走 `commit-convention` Skill，且需用户明确要求；该 Skill 不可用时 fail-closed——只写规划，不执行任何 Git 写操作。
- **不重写历史**。不为统一格式重写历史任务卡；不删除历史摘要，除非已移入对应子 Todo 的归档区。
- **单一规则源**。项目里不落地通用模板包（`templates/agent-workflow/` 之类）；发现即在 upgrade 中删除（先确认项目文档已具备等价规则）。
- **不越权**。不覆盖用户未提交改动；不输出秘密、真实凭据和敏感部署配置。
- **反馈回路（lessons loop）**。会话中暴露的流程问题——规则模糊、边界踩坑、harness 缺口——不许随会话蒸发：项目专属教训沉淀进项目 delta 的「项目特殊约束」，跨项目的方法论教训作为 Skill 改进建议报告给用户（由用户决定是否升级 Skill 与版本号）。判据：同一个坑第二次出现，说明第一次没有沉淀。拿不准是否跨项目的教训先落 delta（低成本，不需审批）；audit 时回看各项目 delta，同一教训出现在多个项目 delta 即为晋升信号（rule of three），报告用户决定是否收编进 Skill。

## 项目 delta 文件契约

bootstrap/upgrade 在目标项目生成**一份** `develop/dev/workflow.md`（不再生成多份角色文件），只写本 Skill 装不下的项目专属内容，schema：

```md
# <项目名> Workflow Delta

> generated-by: agent-workflow v<当前 Skill 版本>
> 通用角色职责/流程/台账规则见 agent-workflow Skill（唯一规则源）。
> 本 Skill 缺席时的 fail-closed：本文件 + 项目规则（CLAUDE.md）即最小可执行规则；
> 不得执行 Git 写操作（commit-convention 同样缺席时只输出规划）。

## 验证命令
<项目的测试/构建/守门命令，含路径与已知环境坑>

## 各角色项目边界
### Architect
### Developer
### UI
### QA
<每角色只写：目录/模块边界、不可触碰区、本项目分工线、停止点——十几行以内>

## 项目特殊约束
<如上游最小侵入、部署形态、密钥纪律等本项目独有规则>
```

版本锚点用途：引擎升级后，audit 模式对比 delta 头部的 `generated-by` 版本即可发现需要 upgrade 的项目。

## References

- `references/roles.md` — 五角色（Architect/Developer/UI/QA/Beta）完整职责、边界、交接与停止条件；交接纪律。
- `references/todo-templates.md` — 两层 Todo 规则、任务卡字段、Design Gate、提交规划、状态所有权、归档规则、Canonical 模板。
- `references/bootstrap.md` — 项目落地文件布局、bootstrap/upgrade 执行要求、完成报告格式。
- `references/checklist.md` — audit/收尾验证清单。

## Changelog

- **1.2.1** — lessons loop 补晋升通道：拿不准归属的教训先落 delta；audit 回看各 delta，多项目重复出现的教训（rule of three）列为晋升候选报告用户。
- **1.2** — 角色对齐主流四件套（planner/coder/reviewer/tester）：UI 从平级角色降为 Developer 的可选视觉子阶段（UI pass，视觉量大才单开会话）；QA 补上 reviewer 职责（先 diff 代码审查后行为验收，质量问题同样可 FAIL）；Beta 默认定位为里程碑收口的 release-checklist 卡而非常驻角色（高风险项目可升格）。
- **1.1** — 一卡收口一提交（禁攒批混合工作树；提交点按隔离形态：主分支直接工作 → qa-pass 后，branch/worktree 隔离 → 可前移 implemented）；QA 默认 fresh-context 隔离（新会话/subagent，只喂卡+验收+diff）；Architect 验收标准测试化（spec-driven，可断言项落测试骨架）；新增反馈回路不变量（教训沉淀进 delta / Skill 建议，同坑不二踩）。
- **1.0** — 从单文件 `agent-workflow-bootstrap` 重构为路由层 + references 结构；新增 role-startup 模式与项目 delta 契约。
