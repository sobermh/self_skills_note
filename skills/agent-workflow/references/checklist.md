# 验证清单（audit 模式 / bootstrap-upgrade 收尾）

按变更范围选择最小验证；audit 模式在用户未要求修改时只报告、不写文件。

## 项目规则与入口

- 搜索确认项目规则（CLAUDE.md/AGENTS.md）包含工作流入口（指向 agent-workflow Skill 与 delta 文件）、开发流程和上下文装载规则。
- 检查 delta 文件 `develop/dev/workflow.md` 存在且头部含 `generated-by: agent-workflow v<version>`；版本落后于当前 Skill 版本时建议 upgrade。
- 检查 delta 文件只含项目专属内容（边界/命令/约束），没有复制通用角色骨架成为第二规则源。
- 检查项目没有保留 `templates/agent-workflow/` 一类通用模板包。
- 若项目仍用旧版 `develop/dev/agents/` 多文件布局：确认存在独立分发理由（不同平台启动 Prompt、显著不同的访问边界），否则建议收敛为单份 delta。

## Todo 台账

- 搜索确认已归档子 Todo 包含 `## 归档摘要`。
- 检查总览不再展开已完成里程碑，但索引仍可定位历史。
- 检查当前任务状态在总览和子 Todo 中一致（状态 token 逐字一致、徽标计数与行数相符）。
- 检查总览只有一个用户决策区，没有底部"当前待用户提供 / 决策"等重复区块。
- 检查总览没有纯文档维护流水。
- 检查路线图后没有已落地决策或日期化评审摘要；需求和设计入口位于台账索引。
- 检查 Todo schema 包含 Design Required、Design 文档和 Design Gate，且 Developer 在设计未批准时必须停止。

## 提交与安全

- 检查项目规则和任务卡包含 `commit-convention` 的英文标题/中文正文、原子提交、敏感内容排除规则与提交规划，并明确 Skill 未安装或用户未授权时禁止 Git 写操作。
- 检查 Beta 中包含 Security / Release Gate 和 GO 建议规则。

## 收尾

- 若项目保留结构测试，运行聚焦测试。
- 对修改过的文本运行 whitespace/diff 检查。
