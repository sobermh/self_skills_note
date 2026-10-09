# 功能回归规范

按任务选择以下模式：编写或完善用例时读取第一节；仅执行现有用例时读取第二节。执行模式不隐含修改测试、构建或发布授权。

## 编写与完善功能用例

Resolve the named plugin or current plugin repository. Modify only that scope in its independent repository; outer-project submodules are read-only.

Keep two entry files: `test/test_cases.csv` and `test/run-test-cases.mjs`. Expose `npm run test:cases` where applicable.

CSV columns:

```text
用例编号,所属模块,用例标题,前置条件,测试数据,操作步骤,预期结果,优先级,自动化状态,对应测试
```

Cover observable functionality: configuration, commands, APIs, downloads, integrity, errors, retries, concurrency, lifecycle, persistence and upstream compatibility. Choose case counts by behavior, not a fixed quota.

Implement checks in code. Prefer unit tests and mocks for logic, local HTTP servers and temporary files for workflows, and API/RPC integration or actual dependency contracts for boundaries. Simulate platform branches and installer handoff without installing software or restarting applications.

For upstream compatibility, identify the actual upstream entrypoints the plugin calls and test the currently selected dependency version or pinned commit. Prefer a small integration/contract test that invokes the real implementation while mocking only network, OS actions and other external effects. Assert arguments, return shapes, asynchronous completion, errors and binary fidelity where relevant. Typechecks supplement runtime checks; they do not prove runtime behavior. Mocks copied from an old contract cannot detect all upstream changes. Preserve regressions for known failures, such as binary data passing through a text-only bridge or incorrect success responses. Report the tested upstream version/commit and any mock-only boundaries; a missing actual dependency check is not proof of upstream compatibility.

Use the existing test framework's coverage support to measure plugin-owned executable source when available. Report line and branch coverage with the measured file scope; exclude test fixtures, dependencies and generated output, and identify source omitted by the instrumentation. Inspect uncovered paths before adding tests. Prioritize meaningful success, failure, cancellation, retry and compatibility branches and known regressions. Do not add redundant assertions to inflate counts or impose an arbitrary percentage gate. If coverage cannot be collected, report it as unmeasured with the reason, never infer it from passed cases.

Include UI behavior only when code can deterministically assert it, such as command dispatch, disabled states, progress and retry. Exclude visual alignment, aesthetics and cases requiring Agent/human visual judgment. Source-text/CSS matching does not prove rendered behavior.

Do not add CI jobs, VM runners, actual installation/upgrade checks, visual acceptance queues, execution maps or record templates. Existing release infrastructure is outside this workflow. Explain excluded boundaries without adding permanent manual cases.

Map each case using `path :: exact test name` in `对应测试`, separated by ` | ` for multiple tests. Preserve useful existing tests. Mark `已自动化` only when assertions cover every expectation. Temporary `待自动化` gaps must report incomplete.

The runner reads the CSV automatically, validates unique IDs and mappings, and runs the test suites, including mapped upstream compatibility tests. Report only the case result by default: all cases passed, or the failed/incomplete IDs and reasons. Skipped, TODO, missing and failed mapped tests are not passes; exit nonzero for failed/incomplete cases. Coverage analysis is a test-authoring aid, not an extra acceptance gate or mandatory execution report.

Keep standalone checks independent of an outer checkout. Resolve genuine upstream checks against the supplied outer root or installed dependencies; report missing dependencies explicitly. Run the entrypoint and relevant local type/build checks before finishing.

Do not commit, push, publish or update outer pins unless requested.

## 仅执行功能回归

Resolve scope against the outer manifest and pins: one named plugin, explicitly listed plugins, or all pinned plugins with the standard entrypoint when requested. With no scope, use all such pinned plugins in the outer project, or only the current plugin in an independent plugin repository. Report unresolved names instead of silently expanding scope.

1. Find `test/test_cases.csv` and `test/run-test-cases.mjs` in selected plugins.
2. Run the entrypoint from each plugin directory. It reads the CSV automatically.
3. Let the case runner execute mapped upstream compatibility tests against the selected dependencies. Supply the outer root (for example TOKENS_HARNESS_ROOT) when the runner needs it. Do not add separate build, coverage or compatibility gates to a normal request to run the cases.
4. Report case totals and passed/failed/incomplete counts, then each unsuccessful ID with its cause and evidence. Skipped/TODO/missing tests and unavailable dependencies are incomplete.
5. Overall pass requires every in-scope case to pass. Raw technical test totals are supporting evidence.

Use code-based functional checks: unit tests, mocks, local HTTP/filesystem fixtures, API/RPC integration and actual dependency contracts. Do not require or add release CI jobs, VMs, real installation, application restarts or visual Agent/manual acceptance. Report legacy visual-only/system installation cases as excluded from functional scope, not passed.

Mocks prove behavior against their stated contract, not compatibility with every changed upstream implementation. Prefer current upstream dependencies for compatibility checks. Source-text/CSS assertions do not establish visual correctness. Deterministic UI behavior tests may be included without visual judgment.

Treat submodules as read-only. Execution alone does not authorize product edits, new tests, commits, pin updates, packaging or publishing. When the user also requests test implementation, edit the independent plugin repo and authorized outer test infrastructure.

Report simply: "N/N cases passed; all passed." If anything fails or remains unexecuted, list those case IDs and reasons. Do not routinely report raw assertion counts, coverage percentages or separate compatibility conclusions. Coverage analysis belongs to writing/improving cases or an explicit coverage request. "All passed" refers to the current case inventory, not a claim that untested behavior is guaranteed.
