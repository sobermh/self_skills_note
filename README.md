# Self Skills

Reusable Codex skills maintained for personal and project use.

## Available Skills

### Commit Convention

- Skill name: `commit-convention`
- Path: `skills/commit-convention/`
- Purpose: plan and execute atomic Conventional Commits with English titles, Chinese bodies, sensitive-file checks, and explicit stage/commit/push authorization.

Use this Skill for dirty-worktree analysis, commit splitting, message generation, staged-diff verification, commits, and pushes.

### Project Development Workflow

- Skill name: `agent-workflow` (formerly `agent-workflow-bootstrap`)
- Path: `skills/agent-workflow/`
- Purpose: cross-project development workflow harness — governance (bootstrap / upgrade / audit) plus daily role startup (Architect / Developer / UI / QA / Beta).
- Structure: `SKILL.md` is a thin routing layer (mode table, standard flow, invariants, project-delta contract, version anchor); heavy reference material is loaded on demand from `references/` (`roles.md`, `todo-templates.md`, `bug-ledger.md`, `bootstrap.md`, `checklist.md`).
- Includes: Architect / Developer / UI / QA / Beta roles, Design Gate, commit planning, two-layer Todo and Bug governance, defect lifecycle ownership, context loading, archive rules, and release gates.

The Skill is the single reusable rule source. Each target project keeps only a thin delta file (`develop/dev/workflow.md`, with a `generated-by: agent-workflow v<version>` header) recording project-specific boundaries, verification commands, and constraints — generic role definitions are never copied into projects. Git write operations require the separately installed `commit-convention` Skill; without it the workflow stops at commit planning.

### Learning Path Teacher

- Skill name: `learning-path-teacher`
- Path: `skills/learning-path-teacher/`
- Purpose: create and run structured learning programs for any topic from the learner's baseline to a target level, with staged roadmaps, lesson-by-lesson teaching, exercises, grading records, Todo progress, milestone projects, and production/interview framing.
- Structure: `SKILL.md` is the teaching workflow entry; detailed reusable templates and curriculum examples live in `references/` (`learning-artifacts.md`, `curriculum-patterns.md`).

Use this Skill when a user says they want to learn a topic, gives a baseline such as "I have Docker basics", asks for a complete path to Kubernetes or another target, wants the assistant to act as a teacher, or needs answer grading and progress tracking.

### Claude/Codex Memory Sync

- Skill name: `claude-codex-memory-sync`
- Path: `skills/claude-codex-memory-sync/`
- Purpose: bidirectionally read, compare, and hand off same-project memory between Claude Code and Codex, including same-name session lookup and safe Markdown write-back.
- Structure: `SKILL.md` is the sync workflow entry; `scripts/find_memory.py` locates Claude/Codex project memory and session candidates; `references/storage-layout.md` documents the local storage layout.

Use this Skill when a Codex task needs to read the same project's Claude Code memory, when Claude Code needs to find the matching Codex session, or when either side needs a safe Markdown handoff without mutating Codex internal sqlite files.

### TokensCowork Plugin Test Cases

- Skill names: `plugin-testcases-create`, `plugin-testcases-exec`
- Paths: `skills/tokens/TokensCowork/plugin-testcases-create/`, `skills/tokens/TokensCowork/plugin-testcases-exec/`
- Purpose: create the standard test inventory and runner in each TokensCowork plugin, then discover and execute all pinned plugin suites from the build-only outer project.

Use `plugin-testcases-create` inside an individual plugin repository. Use `plugin-testcases-exec` from the TokensCowork outer project after plugin or upstream upgrades.

## Install With Codex

Ask Codex:

```text
Use $skill-installer to install the skill from https://github.com/sobermh/self_skills_note/tree/main/skills/commit-convention

Use $skill-installer to install the skill from https://github.com/sobermh/self_skills_note/tree/main/skills/agent-workflow

Use $skill-installer to install the skill from https://github.com/sobermh/self_skills_note/tree/main/skills/learning-path-teacher

Use $skill-installer to install the skill from https://github.com/sobermh/self_skills_note/tree/main/skills/claude-codex-memory-sync

Use $skill-installer to install the skill from https://github.com/sobermh/self_skills_note/tree/main/skills/tokens/TokensCowork/plugin-testcases-create

Use $skill-installer to install the skill from https://github.com/sobermh/self_skills_note/tree/main/skills/tokens/TokensCowork/plugin-testcases-exec
```

After installation, start a new task and invoke it with:

```text
Use $commit-convention to split and commit the current worktree by logical module and stage.

Use $agent-workflow to initialize this repository's project development workflow.

Use $learning-path-teacher to create a complete Kubernetes learning path for someone who already knows Docker basics.

Use $claude-codex-memory-sync to read the same-project Claude Code memory for this Codex task.

Use $plugin-testcases-create to create the standardized test cases for this TokensCowork plugin.

Use $plugin-testcases-exec to execute all pinned plugin test cases from TokensCowork.
```

For an existing project:

```text
Use $agent-workflow to incrementally upgrade this repository's project development workflow. Preserve existing paths, history, and project-specific rules.
```

For daily development sessions in a bootstrapped project:

```text
Use $agent-workflow to start this session as the Developer role for the current task.
```

## Manual Install

Clone this repository and copy the Skill directory into the local Codex skills directory:

```text
~/.codex/skills/commit-convention/
  SKILL.md

~/.codex/skills/agent-workflow/
  SKILL.md
  references/
    roles.md
    todo-templates.md
    bug-ledger.md
    bootstrap.md
    checklist.md

~/.codex/skills/learning-path-teacher/
  SKILL.md
  references/
    learning-artifacts.md
    curriculum-patterns.md

~/.codex/skills/claude-codex-memory-sync/
  SKILL.md
  scripts/
    find_memory.py
  references/
    storage-layout.md
  agents/
    openai.yaml

~/.codex/skills/plugin-testcases-create/
  SKILL.md

~/.codex/skills/plugin-testcases-exec/
  SKILL.md
```

`commit-convention`, `plugin-testcases-create`, and `plugin-testcases-exec` are single `SKILL.md` skills; `agent-workflow` and `learning-path-teacher` ship `SKILL.md` plus a `references/` directory that must be copied together (the routing layer loads reference files on demand). `claude-codex-memory-sync` ships `SKILL.md`, its helper script, storage reference, and UI metadata; copy the full directory so both lookup and write-back modes work.
