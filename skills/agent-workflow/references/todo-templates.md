# 两层 Todo 与台账规则

## 总览层

总览只保留：

- 里程碑路线图。
- 用户待决策区。
- 当前和未完成里程碑的状态投影。
- 子 Todo 索引。

总览不是完整历史包，不展开已完成里程碑的全部任务卡。

不要在总览长期保存"文档维护记录"流水。文档拆分、搬家和格式整理由 Git 历史追踪；确实影响架构、范围或执行的变化，应进入对应任务卡、设计决策或归档摘要。

总览只能有一个用户待决策区。不要在文件底部再生成"当前待用户提供 / 决策""待补充信息"等重复区块：

- 真正需要用户拍板的事项进入唯一决策表。
- 缺少外部条件且阻塞执行的事项建立 `blocked` 卡，写明所缺信息和解除条件。
- 已提供、已决定或已完成的信息留在对应子 Todo、设计决策或需求文档，不继续占用总览。
- 已落地产品决策、日期化架构评审摘要和历史调研结论不放在路线图后重复展示。
- 需求、设计注册表和全局架构基线只作为链接放进台账索引，不在总览复制摘要。

## 子 Todo 层

每个里程碑一个明细文件，保存：

- 当前任务卡及权威状态。
- 目标、范围、非范围、依赖和决策。
- 实现步骤、负责人和实际代码位置。
- 验收标准、验证证据、结果、风险和备注。
- 已完成里程碑顶部的 `## 归档摘要`。

## 任务卡最小字段

```md
### <step-id> <title>

**状态**: planned | in-progress | implemented | qa-pass | qa-fail | blocked | decision | deferred | dropped
**Owner**: Architect | Developer | UI | QA | Beta
**目标**:
**范围**:
**非范围**:
**Design Required**: yes | no
**Design 文档**: <path | —>
**Design Gate**: not-required | draft | approved
**提交规划**:
- `type(scope): english subject` — <逻辑范围与验证要求>
**依赖/决策**:
**实现步骤**:
**验收标准**:
**实际修改位置**:
**验证证据**:
**结果/风险**:
```

项目已有成熟 schema 时保留原字段，只补齐缺失的职责、上下文和归档规则，不强制改名。

## Design Gate 规则

- Todo 必须记录 Design 判断；不能让 Developer 自己猜是否需要设计。
- `Design Required: no` 必须写简短理由，且不得涉及模块/API/数据/权限/部署等契约变化。
- `Design Required: yes` 时，优先创建独立 Architect 设计任务；已有等价设计时可以引用并复核，无需重复写文档。
- 设计正文放在项目的 design/ADR/architecture 目录，Todo 只保存任务状态、路径、关键决策和 Gate 结果，不复制全文。
- Design Gate 至少确认：模块边界、数据与 API 契约、安全/租户、失败与并发、兼容/迁移/回滚、验证策略。
- 实现任务必须依赖设计任务或已批准设计；`draft` 不得进入 Developer。
- 存量卡不批量补字段；新卡必须执行本规则，存量卡在重新进入开发前由 Architect 按当前风险补齐。

## 提交规划与 Conventional Commits

项目默认使用 `commit-convention` Skill 管理提交拆分、message、敏感文件检查、stage、commit 和 push。执行前必须确认该 Skill 可用；不可用时进入 fail-closed：只允许在项目规则和 Todo 中写提交规划，不得执行任何会修改 Git 索引、历史或远程的操作。

下面的兼容基线只用于生成项目规则和任务卡，不是缺少 `commit-convention` 时的提交执行替代品：

```text
<type>[(scope)][!]: <English subject, verb first, preferably <= 50 chars>

<中文正文：说明为什么修改以及影响>
```

- 常用 `type`：`feat`、`fix`、`refactor`、`perf`、`docs`、`test`、`build`、`ci`、`style`、`chore`。
- 标题使用英文祈使语气，正文使用中文说明动机和影响；多点正文使用 `1. 2. 3.` 编号列表。
- Architect 在建卡时规划 1 到 N 个逻辑提交；每项写英文标题、逻辑范围和验证要求。
- 一个提交只表达一个可回滚、可审查的逻辑变化；不要按文件机械拆分，也不要把无关清理混入功能提交。
- 破坏性变更使用 `type(scope)!:`，并在 footer 写 `BREAKING CHANGE:` 和迁移方法。
- 不提交敏感信息、运行产物或无长期价值的生成内容，不添加 `Co-Authored-By` 等署名尾注。
- Developer 按计划组织实现；实际边界变化时在任务卡或报告中更新建议并说明原因。
- QA 验证的是代码状态，不为了满足提交计划重复测试未变化内容。
- 提交规划不是 Git 授权。只有 `commit-convention` 已安装且用户明确要求时，Agent 才能执行 stage、commit 或 push；缺少任一条件都必须停止在规划阶段。

## 状态和所有权

- 子 Todo 的状态是权威来源；总览仅投影当前/未完成任务状态。
- Architect 拥有目标、范围、决策、验收标准、schema 和任务创建。
- Developer 拥有实现状态、实际代码位置和功能测试证据。
- UI 拥有视觉实现和视觉验证证据。
- QA 拥有 QA 结果、失败记录和 `PASS/FAIL/BLOCKED/PARTIAL`。
- Beta 拥有真实工作流、Security/Release Gate 和 `GO/CONDITIONAL GO/NO-GO` 建议。
- 决策记录追加保存；延期、放弃和重新触发条件必须明确。

## 默认上下文装载

日常 Agent 只读取：

1. 项目规则。
2. Todo 总览。
3. 当前或用户明确指定的里程碑子 Todo。
4. 当前任务卡明确引用的设计、BUG、测试和代码文件。

已完成里程碑属于归档上下文。只有当前任务明确依赖其历史决策、BUG、实现边界或证据时才打开，不能每次把全部历史 Todo 丢给 Agent。

## 归档规则

收敛总览时不能直接删除历史摘要：

1. 从总览移除已完成里程碑的展开任务行。
2. 在对应子 Todo 顶部新增或更新 `## 归档摘要`。
3. 把移除的摘要内容移动到该归档区。
4. 总览保留一句归档提示和子 Todo 索引。
5. 不重写原始历史任务卡；只移动摘要和调整导航。

## Canonical Todo 模板

新项目使用以下固定结构，只替换项目名称、里程碑和任务内容。不要增加第二个决策区、维护流水或历史说明区。

### 总览模板

```md
# <PROJECT> Todo / Trace Log

> 第一层 Plan：只用于导航、决策和活跃状态投影。
> 日常上下文读取本文件、当前里程碑子 Todo，以及任务卡明确引用的文档。

## 里程碑路线图

| 里程碑 | 目标 | 状态 |
|---|---|---|
| M0 <name> | <goal> | planned |

## 待决策（用户）

| 来源 | 决策点 | 选项与 Architect 建议 | 提出日期 |
|---|---|---|---|

## 状态总览

### M0 <name>

| step_id | name | 描述 | 状态 | 结果 |
|---|---|---|---|---|
| M0-01 | <task> | <summary> | planned | — |

## 任务台账索引

- Schema：`<todo-root>/README.md`
- Requirements：`<requirements-path>`
- Design registry：`<design-index-path>`
- M0：`<todo-root>/<project>-todo-M0.md`
```

### 子 Todo 模板

```md
# <PROJECT> <MILESTONE> Todo / Trace Log

> 第二层执行规格；本文件中的任务卡是状态权威来源。

## 归档摘要

<!-- 仅在里程碑完成并从总览收敛时保留；活跃里程碑可省略。 -->

## 任务台账

### <step-id> <title>

<!-- 使用上文"任务卡最小字段"；每张卡只保存本任务的设计、实现、验收和证据。 -->
```

Bootstrap 必须按此模板生成同构 Todo。Upgrade 不强制重命名已有文件，但应把章节职责收敛为同一结构，并删除重复决策区、维护流水和路线图后的历史摘要。
