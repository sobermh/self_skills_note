---
name: plugin-testcases-exec
description: Execute standardized test cases for one, multiple, or all pinned TokensCowork plugins from the build-only outer project after plugin or upstream upgrades. Use when asked to validate selected plugins or run all plugin test/test_cases.csv suites.
---

# Execute TokensCowork Plugin Test Cases

Use this Skill in the TokensCowork build-only outer project after a plugin, Desktop, Harness, Electron, or other pinned upstream dependency changes.

Resolve the execution scope first:

- If the user names one plugin, test only that plugin.
- If the user names multiple plugins, test only those plugins.
- If the user explicitly asks for all plugins or provides no plugin scope, test every pinned plugin that has the standardized test entrypoint.

Match requested plugins against the outer project's manifest, pins, and submodule paths. Report an unresolved name instead of silently testing a different plugin. Never expand an explicit plugin scope.

1. Discover `test/test_cases.csv` only for the resolved plugin scope.
2. For each plugin, run `test/run-test-cases.mjs` with that plugin as the working directory.
3. Read the CSV and continue any `部分自动化` or `Agent验收` steps that are safe and possible with available tools.
4. Run the outer project's own build, staging, packaging, and compatibility checks relevant to the upgrade.
5. Evaluate results by CSV case ID, not by the test framework's assertion count. Assign every case one execution result:
   - `通过`: every required step and expected result was verified.
   - `失败`: an executed step or expected result failed.
   - `部分验证`: mapped automation passed, but required case steps remain unverified. This is a non-passing result.
   - `未执行`: the case could not be run.
6. Report the resolved scope and, per tested plugin: total CSV cases and the counts for `通过`, `失败`, `部分验证`, and `未执行`. Also report `未通过总数` as `失败 + 部分验证 + 未执行`.
7. List every `失败`, `部分验证`, and `未执行` case by ID with the concrete reason and evidence. Mention raw automated assertion totals only as supporting evidence, never as the primary result.
8. Give the plugin an overall result of `通过` only when every CSV case is `通过`. If any case is `失败`, `部分验证`, or `未执行`, the overall result is `未通过`; state which remaining work or failure prevents acceptance.

Treat all submodules as read-only. Never patch plugin source inside `plugins/`; make test changes in the independent plugin repository and update the outer pin only when explicitly requested.

Do not equate an automated test count such as `191/191` with completed CSV cases. Never describe mapped automation as a passed CSV case when required real operations remain. Never say a plugin passed merely because its test command exited successfully. Do not modify product code, commit, push, package, or publish while performing an execution-only request.
