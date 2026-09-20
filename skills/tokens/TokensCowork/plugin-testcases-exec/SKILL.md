---
name: plugin-testcases-exec
description: Discover and execute every pinned TokensCowork plugin's standardized test cases from the build-only outer project after plugin or upstream upgrades. Use when asked to validate all plugins from TokensCowork or run their test/test_cases.csv suites.
---

# Execute TokensCowork Plugin Test Cases

Use this Skill in the TokensCowork build-only outer project after a plugin, Desktop, Harness, Electron, or other pinned upstream dependency changes.

1. Discover every `plugins/*/test/test_cases.csv` included by the outer project's actual plugin manifest or pins.
2. For each plugin, run `test/run-test-cases.mjs` with that plugin as the working directory.
3. Read the CSV and continue any `部分自动化` or `Agent验收` steps that are safe and possible with available tools.
4. Run the outer project's own build, staging, packaging, and compatibility checks relevant to the upgrade.
5. Report per plugin: total cases, completed, failed, and not executed with reasons.

Treat all submodules as read-only. Never patch plugin source inside `plugins/`; make test changes in the independent plugin repository and update the outer pin only when explicitly requested.

Do not equate an automated test count with completed CSV cases. Do not modify product code, commit, push, package, or publish while performing an execution-only request.
