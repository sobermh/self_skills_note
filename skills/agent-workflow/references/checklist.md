# 验证清单（audit 模式 / bootstrap-upgrade 收尾）

按变更范围选择最小验证；audit 模式在用户未要求修改时只报告、不写文件。

## 项目规则与入口

- 搜索确认项目规则（CLAUDE.md/AGENTS.md）包含工作流入口（指向 agent-workflow Skill 与 delta 文件）、开发流程和上下文装载规则。
- 检查 delta 文件 `develop/dev/workflow.md` 存在且头部含 `generated-by: agent-workflow v<version>`；版本落后于当前 Skill 版本时建议 upgrade。
- 检查 delta 文件只含项目专属内容（边界/命令/约束），没有复制通用角色骨架成为第二规则源。
- 检查项目没有保留 `templates/agent-workflow/` 一类通用模板包。
- 若项目仍用旧版 `develop/dev/agents/` 多文件布局：确认存在独立分发理由（不同平台启动 Prompt、显著不同的访问边界），否则建议收敛为单份 delta。
- 回看 delta「项目特殊约束」：是否有换个项目也成立的通用教训（尤其同一教训已出现在多个项目 delta —— rule of three）；有则列为晋升候选报告用户，由用户决定是否收编进 Skill 并升版本号。

## Todo 台账

- 搜索确认已归档子 Todo 包含 `## 归档摘要`。
- 检查总览不再展开已完成里程碑，但索引仍可定位历史。
- 检查当前任务状态在总览和子 Todo 中一致（状态 token 逐字一致、徽标计数与行数相符）。
- 检查总览只有一个用户决策区，没有底部"当前待用户提供 / 决策"等重复区块。
- 检查总览没有纯文档维护流水。
- 检查路线图后没有已落地决策或日期化评审摘要；需求和设计入口位于台账索引。
- 检查 Todo schema 包含 Design Required、Design 文档和 Design Gate，且 Developer 在设计未批准时必须停止。

## Bug 台账

- 检查存在两层职责：全局索引只做状态投影，里程碑文件保存完整记录；项目路径如非默认值，已写入 delta。
- 检查新 Bug 使用永久唯一 ID，空号不回填，索引与明细的标题、严重级别、状态和里程碑计数一致。
- 检查记录至少包含发现/复现证据、现象、影响、Owner 和 QA 门；根因、修复和回归证据按状态补齐。
- 检查状态所有权：Developer 只能推进到 `fixed`，独立 QA 才能推进到 `verified`，`accepted` 有 Architect/用户决定与重触发条件。
- 检查 Todo、测试计划和发布清单只引用 BUG ID，完整事实没有多份漂移；新加入的 BUG 引用可解析到索引。
- 检查日常上下文只加载 Bug 总索引、当前里程碑和明确点名记录，不默认加载全部历史明细。
- 若项目保留 Bug 守门测试，运行并确认 ID 唯一、文件归属、投影一致、计数、必填字段和新引用解析均受保护。

## 提交与安全

- 检查项目规则和任务卡包含 `commit-convention` 的英文标题/中文正文、原子提交、敏感内容排除规则与提交规划，并明确 Skill 未安装或用户未授权时禁止 Git 写操作。
- 检查 Beta 中包含 Security / Release Gate 和 GO 建议规则。

## 收尾

- 若项目保留结构测试，运行聚焦测试。
- 对修改过的文本运行 whitespace/diff 检查。
