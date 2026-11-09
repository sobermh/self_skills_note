# Self Skills

Reusable Codex skills maintained for personal and project use.

## Available Skills

### Commit Convention

- Skill name: `commit-convention`
- Path: `skills/commit-convention/`
- Purpose: plan and execute atomic Conventional Commits with English titles, Chinese bodies, sensitive-file checks, and explicit stage/commit/push authorization.

Use this Skill for dirty-worktree analysis, commit splitting, message generation, staged-diff verification, commits, and pushes.

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

### TokensCowork Plugin Development

- Skill name: `tokenscowork-plugin-dev`
- Path: `skills/tokens/TokensCowork/tokenscowork-plugin-dev/`
- Purpose: develop and maintain independent TokensCowork npm plugins, including host compatibility, bilingual metadata, functional regression and private registry releases.
- Structure: `SKILL.md` plus `references/layout.md`, `references/runtime.md`, `references/testing.md` and `references/release.md`.

Includes coordination for concurrent changes, two-file functional test organization, outer-project adaptation checks and release artifact verification. Git and release actions follow the user-authorized scope.

Use this single Skill for plugin development, writing regression cases, execution-only regression, and authorized CI/release work. Load the matching reference for the requested mode; running tests does not imply permission to edit or publish.

## Install With Codex

Ask Codex:

```text
Use $skill-installer to install the skill from https://github.com/sobermh/self_skills_note/tree/main/skills/commit-convention

Use $skill-installer to install the skill from https://github.com/sobermh/self_skills_note/tree/main/skills/learning-path-teacher

Use $skill-installer to install the skill from https://github.com/sobermh/self_skills_note/tree/main/skills/claude-codex-memory-sync

Use $skill-installer to install the skill from https://github.com/sobermh/self_skills_note/tree/main/skills/tokens/TokensCowork/tokenscowork-plugin-dev
```

After installation, start a new task and invoke it with:

```text
Use $commit-convention to split and commit the current worktree by logical module and stage.

Use $learning-path-teacher to create a complete Kubernetes learning path for someone who already knows Docker basics.

Use $claude-codex-memory-sync to read the same-project Claude Code memory for this Codex task.

Use $tokenscowork-plugin-dev to inspect and improve this TokensCowork plugin.

Use $tokenscowork-plugin-dev to create the standardized functional regression cases for this TokensCowork plugin.

Use $tokenscowork-plugin-dev to execute all pinned plugin test cases from TokensCowork without modifying code.
```

## Manual Install

Clone this repository and copy the Skill directory into the local Codex skills directory:

```text
~/.codex/skills/commit-convention/
  SKILL.md

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

~/.codex/skills/tokenscowork-plugin-dev/
  SKILL.md
  references/
    layout.md
    runtime.md
    testing.md
    release.md
```

`commit-convention` is a single `SKILL.md` skill; `tokenscowork-plugin-dev` ships its entrypoint plus all four reference files, which must be copied together; `learning-path-teacher` ships `SKILL.md` plus a `references/` directory that must be copied together (the routing layer loads reference files on demand). `claude-codex-memory-sync` ships `SKILL.md`, its helper script, storage reference, and UI metadata; copy the full directory so both lookup and write-back modes work.
