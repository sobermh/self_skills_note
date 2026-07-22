---
name: commit-convention
description: Plan, review, create, or push Git commits using a strict Conventional Commits workflow. Use when the user asks to split a dirty worktree into logical commits, write commit messages, stage files or hunks, commit changes, push commits, audit a CONTRIBUTING.md commit policy, or prevent unrelated, generated, or sensitive files from entering history.
---

# Commit Convention

用于规划和执行可审查、可回滚的 Git 提交。默认采用 Conventional Commits，并使用“英文标题、中文正文”的提交格式。

## 1. 规则优先级

开始前按顺序读取：

1. 用户当前要求。
2. 仓库的 `AGENTS.md`、`CLAUDE.md` 或同类项目规则。
3. 仓库根目录及当前模块适用的 `CONTRIBUTING.md`。
4. 本 Skill 的默认规范。

目标项目已有更严格或更具体的提交规范时，以项目规范为准。发现冲突时说明差异，不要静默覆盖项目约定。

## 2. 授权边界

- 分析工作区、建议拆分和生成 message 不等于 Git 授权。
- 只有用户明确要求提交时才能执行 `git add` 和 `git commit`。
- 只有用户明确要求推送、提交到远程或等价表达时才能执行 `git push`。
- 用户只授权某个模块或阶段时，不得暂存其他改动。
- 不修改、还原或删除用户已有改动来制造干净工作区。
- 不使用 `git reset --hard`、`git checkout --` 等破坏性命令处理混合改动。

## 3. 提交拆分

一个 commit 只做一件事。拆分依据是可独立理解、验证和回滚的逻辑变化，不是文件数量。

- 优先按阶段、模块和行为边界拆分，例如治理文档、测试基础设施、数据模型、后端 API、前端 UI、部署配置。
- 构建脚本、产品功能、测试资产和文档通常分别提交，除非它们共同构成一个不可分割的最小变化。
- 同一文件包含多个逻辑变化时使用分块暂存；不要因为共享文件难拆就把所有阶段塞进一个提交。
- 一个标题无法准确概括全部暂存内容时，继续拆分。
- 不按目录机械拆分，也不把无关格式化、清理或重构混入功能提交。
- 大型脏工作区先给出提交序列，只执行用户当前授权的阶段或模块。

## 4. Message 格式

```text
<type>[(scope)][!]: <英文标题，动词开头，尽量不超过 50 字符>

<中文正文（可选但推荐）：说明动机、背景和影响，重点解释为什么改。>

<注脚（可选）：BREAKING CHANGE、Closes 等>
```

标题要求：

- 使用英文。
- 使用动词开头的简洁祈使语气。
- 尽量不超过 50 个字符，不加句号。
- `scope` 可选，使用稳定的模块或领域名。
- 破坏性变更在 type 或 scope 后加 `!`。

正文要求：

- 使用中文。
- 单一变化用一到两句话说明动机和影响。
- 多项变化使用 `1. 2. 3.` 编号列表，一行一个要点。
- 不重复罗列 diff；说明为什么这样改、解决了什么问题、有什么兼容或运维影响。

注脚要求：

- 使用 `令牌: 说明` 格式。
- 破坏性变更必须写 `BREAKING CHANGE:` 并说明迁移方法。
- 需要关联问题时可写 `Closes: #123`。
- 不添加 `Co-Authored-By` 或其他署名尾注。

## 5. Type 选择

| type | 用途 |
|---|---|
| `feat` | 新功能、新脚本、新配置能力 |
| `fix` | 修复缺陷 |
| `refactor` | 行为不变的结构调整、重命名或拆分 |
| `perf` | 性能和效率优化 |
| `docs` | 只修改文档 |
| `test` | 只增加或调整测试 |
| `build` | 构建系统、镜像或打包流程 |
| `ci` | CI/CD 工作流 |
| `style` | 不改变行为的格式和样式调整 |
| `chore` | 依赖、忽略规则和低风险配置维护 |

类型按主要行为选择，不按文件扩展名猜测。测试随功能一起保证该功能可验证时可以进入同一个 `feat` 或 `fix`；独立补测试时使用 `test`。

## 6. 提交前检查

每次暂存前：

1. 读取 `git status --short --branch`。
2. 查看目标模块的 diff 和未跟踪文件。
3. 确认没有其他 Agent 或用户正在进行冲突的 Git 操作。
4. 检查 `.git/index.lock`；只有确认没有相关 Git 进程且锁已陈旧时才能删除。

禁止提交：

- `.env`、`.env.build`、`secrets/`、私钥、Token、真实密码和凭据。
- 模型文件、用户输入输出、运行日志、数据库、缓存和本地运行态数据。
- 无长期价值的截图、审计输出、覆盖率、构建产物和临时测试结果。
- 与当前提交目标无关的用户改动。

暂存后必须检查：

1. `git diff --cached --name-status`
2. `git diff --cached --stat`
3. `git diff --cached --check`
4. 高置信度敏感信息扫描
5. 与改动范围匹配的最小测试或验证

发现不属于本提交的文件或 hunks 时先从暂存区移除，不修改工作区内容。

## 7. 执行提交

- 使用非交互命令创建提交，避免打开交互式编辑器。
- 标题与正文分开传入，例如：

```text
git commit -m "docs(workflow): add commit convention" -m "将提交规则拆分为独立 Skill，统一原子提交、敏感文件检查与授权边界。"
```

- 多点正文使用多个编号行，确保最终 message 中保留换行。
- 提交完成后检查 `git log -1 --format=fuller` 和暂存区是否为空。
- 报告 commit hash、标题、验证结果和剩余未提交范围。

## 8. 推送

推送前确认：

1. 当前分支和远程跟踪关系。
2. 将要推送的提交序列，而不只检查最后一个提交。
3. 本地是否包含用户未要求推送的历史提交。
4. 远程没有需要先整合的新提交。

只有推送范围符合用户授权时才执行 `git push`。推送成功后报告远程、分支和最新 commit；失败时保留本地提交并说明原因，不用强推覆盖远程。

## 9. 与开发工作流协作

- Architect 在 Todo 任务卡中规划 1 到 N 个逻辑提交，记录英文标题和包含范围。
- Developer 按实际实现更新提交边界，但不能把提交计划当成 Git 授权。
- QA 验证代码状态，不为了拆提交重复验证未变化内容。
- 执行 Git 提交时由本 Skill 重新核对工作区、暂存内容、message 和授权范围。

任务卡中的提交规划使用：

```md
**提交规划**:
- `type(scope): english subject` — <逻辑范围与验证要求>
```
