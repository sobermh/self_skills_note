---
name: plugin-testcases-create
description: Create or update the standardized test case inventory and execution entrypoint for a specified TokensCowork plugin. Use when asked to add plugin test cases or maintain test/test_cases.csv and test/run-test-cases.mjs for a named plugin or the current plugin repository.
---

# TokensCowork Plugin Test Cases

Use this Skill for one specified TokensCowork plugin. If the user provides a plugin name, repository, or path, resolve and modify only that plugin. If no target is provided, use the current plugin repository. Never create test cases in unrelated plugins.

Keep these fixed entry files:

```text
test/test_cases.csv
test/run-test-cases.mjs
```

`test/test_cases.csv` must use these columns:

```text
用例编号,所属模块,用例标题,前置条件,测试数据,操作步骤,预期结果,优先级,自动化状态,对应测试
```

Cover the plugin's meaningful functions, configuration, errors, interfaces, lifecycle, compatibility, security, and UI where applicable. Preserve existing test files and map them from `对应测试` as `path :: exact test name`. Do not create duplicate execution maps, record templates, or test documentation files.

Use these status values consistently:

- `已自动化`: the mapped test fully verifies the case.
- `部分自动化`: automation exists, but the whole business case is not proven.
- `Agent验收`: an Agent must execute the CSV steps with available tools.
- `人工验收`: only a person can complete the remaining step.
- `待自动化`: a known temporary automation gap.

`test/run-test-cases.mjs` must run the plugin's existing checks, read the CSV automatically, validate unique case IDs and referenced test names, and report unmapped or incomplete cases. A successful script run must never claim that every CSV case passed unless every case was actually completed.

Expose `npm run test:cases` when the plugin has `package.json`. Add candidate-mode support only when the plugin genuinely has a packaged or Electron candidate environment.

Run the new entrypoint in the target plugin before finishing. Report the resolved plugin name and path. Do not change product behavior merely to satisfy tests. Do not commit, push, publish, or update an outer-project pin unless the user asks.
