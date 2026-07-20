# Self Skills

Reusable Codex skills maintained for personal and project use.

## Available Skills

### Project Development Workflow

- Skill name: `agent-workflow-bootstrap`
- Path: `skills/agent-workflow-bootstrap/`
- Purpose: initialize, audit, or incrementally upgrade a project's multi-agent development workflow.
- Includes: Architect / Developer / UI / QA / Beta roles, Design Gate, Conventional Commit planning, two-layer Todo governance, context loading, archive rules, and release gates.

This Skill establishes project-specific governance documents. It does not copy a reusable template pack into the target project and is not used for ordinary feature implementation.

## Install With Codex

Ask Codex:

```text
Use $skill-installer to install the skill from https://github.com/sobermh/self_skills_note/tree/main/skills/agent-workflow-bootstrap
```

After installation, start a new task and invoke it with:

```text
Use $agent-workflow-bootstrap to initialize this repository's project development workflow.
```

For an existing project:

```text
Use $agent-workflow-bootstrap to incrementally upgrade this repository's project development workflow. Preserve existing paths, history, and project-specific rules.
```

## Manual Install

Clone this repository and copy the Skill directory into the local Codex skills directory:

```text
~/.codex/skills/agent-workflow-bootstrap/
  SKILL.md
```

The Skill is intentionally distributed as a single `SKILL.md` file inside its required named directory.
