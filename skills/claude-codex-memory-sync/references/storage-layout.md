# Storage Layout

This reference documents the local storage conventions this skill expects. Use it only when the finder script cannot locate the right files or when manual verification is needed.

## Claude Code

Default home:

```text
%USERPROFILE%/.claude
```

Relevant paths:

```text
.claude/projects/<encoded-project-path>/
.claude/projects/<encoded-project-path>/memory/*.md
.claude/projects/<encoded-project-path>/<session-id>.jsonl
.claude/projects/<encoded-project-path>/<session-id>/custom-title.json
```

On Windows, Claude Code project directories are path-like slugs such as:

```text
C--Users-wzm-maohui-github-repo-psl-DogWatch-code
```

The slug is not a formal API. Prefer fuzzy matching and transcript `cwd` checks over assuming a single encoding rule.

`memory/MEMORY.md` is usually an index. Other Markdown files in `memory/` hold curated project notes and are the best first source for cross-session context.

For Codex -> Claude write-back, prefer:

```text
.claude/projects/<encoded-project-path>/memory/codex-handoff.md
```

Append concise dated sections unless the user asks to replace a specific memory file.

## Codex

Default home:

```text
%USERPROFILE%/.codex
```

Relevant read-only paths:

```text
.codex/session_index.jsonl
.codex/sessions/YYYY/MM/DD/*.jsonl
.codex/thread_history_*.sqlite
.codex/memories_*.sqlite
```

Do not mutate Codex sqlite files from this skill. For Claude -> Codex persistence, create or update a normal Markdown handoff under:

```text
.codex/memory-sync/<project-slug>/claude-handoff.md
```

This is intentionally outside Codex's internal sqlite state. Codex will not load it automatically in every task; when memory sync is needed, use the skill to locate and read the handoff.

## Dual Installation

For mutual use, keep the same skill installed in both:

```text
%USERPROFILE%/.codex/skills/claude-codex-memory-sync/
%USERPROFILE%/.claude/skills/claude-codex-memory-sync/
```

Both copies use the same storage lookup rules. When updating behavior, update the Codex copy first, validate it, then mirror it to the Claude Code copy.
