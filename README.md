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

## Install With Codex

Ask Codex:

```text
Use $skill-installer to install the skill from https://github.com/sobermh/self_skills_note/tree/main/skills/commit-convention

Use $skill-installer to install the skill from https://github.com/sobermh/self_skills_note/tree/main/skills/agent-workflow

Use $skill-installer to install the skill from https://github.com/sobermh/self_skills_note/tree/main/skills/learning-path-teacher
```

After installation, start a new task and invoke it with:

```text
Use $commit-convention to split and commit the current worktree by logical module and stage.

Use $agent-workflow to initialize this repository's project development workflow.

Use $learning-path-teacher to create a complete Kubernetes learning path for someone who already knows Docker basics.
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
```

`commit-convention` is a single `SKILL.md`; `agent-workflow` and `learning-path-teacher` ship `SKILL.md` plus a `references/` directory that must be copied together (the routing layer loads reference files on demand).
