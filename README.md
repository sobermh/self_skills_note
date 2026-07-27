# Self Skills

Reusable Codex skills maintained for personal and project use.

## Available Skills

### Commit Convention

- Skill name: `commit-convention`
- Path: `skills/commit-convention/`
- Purpose: plan and execute atomic Conventional Commits with English titles, Chinese bodies, sensitive-file checks, and explicit stage/commit/push authorization.

Use this Skill for dirty-worktree analysis, commit splitting, message generation, staged-diff verification, commits, and pushes.

### Project Development Workflow

- Skill name: `agent-workflow-bootstrap`
- Path: `skills/agent-workflow-bootstrap/`
- Purpose: initialize, audit, or incrementally upgrade a project's multi-agent development workflow.
- Includes: Architect / Developer / UI / QA / Beta roles, Design Gate, commit planning, two-layer Todo governance, context loading, archive rules, and release gates.

This Skill establishes project-specific governance documents. Git write operations require the separately installed `commit-convention` Skill; without it the workflow stops at commit planning.

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

Use $skill-installer to install the skill from https://github.com/sobermh/self_skills_note/tree/main/skills/agent-workflow-bootstrap

Use $skill-installer to install the skill from https://github.com/sobermh/self_skills_note/tree/main/skills/learning-path-teacher
```

After installation, start a new task and invoke it with:

```text
Use $commit-convention to split and commit the current worktree by logical module and stage.

Use $agent-workflow-bootstrap to initialize this repository's project development workflow.

Use $learning-path-teacher to create a complete Kubernetes learning path for someone who already knows Docker basics.
```

For an existing project:

```text
Use $agent-workflow-bootstrap to incrementally upgrade this repository's project development workflow. Preserve existing paths, history, and project-specific rules.
```

## Manual Install

Clone this repository and copy the Skill directory into the local Codex skills directory:

```text
~/.codex/skills/commit-convention/
  SKILL.md

~/.codex/skills/agent-workflow-bootstrap/
  SKILL.md

~/.codex/skills/learning-path-teacher/
  SKILL.md
  references/
    learning-artifacts.md
    curriculum-patterns.md
```

`commit-convention` and `agent-workflow-bootstrap` are single `SKILL.md` skills; `learning-path-teacher` ships `SKILL.md` plus a `references/` directory that must be copied together.
