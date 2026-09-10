#!/usr/bin/env python3
"""Find same-project Claude Code memory and sessions for Codex handoff."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any


@dataclass
class MemoryFile:
    path: str
    modified: str
    bytes: int


@dataclass
class SessionCandidate:
    session_id: str
    title: str | None
    transcript: str
    modified: str
    bytes: int
    score: float


@dataclass
class CodexSessionCandidate:
    session_id: str
    title: str | None
    transcript: str
    cwd: str | None
    modified: str
    bytes: int
    score: float


def _home_path(env_name: str, fallback: str) -> Path:
    configured = os.environ.get(env_name)
    if configured:
        return Path(configured).expanduser()
    return Path.home() / fallback


def _norm(value: str | None) -> str:
    if not value:
        return ""
    chars = [ch.lower() if ch.isalnum() else " " for ch in value]
    return " ".join("".join(chars).split())


def _similarity(left: str, right: str) -> float:
    left_norm = _norm(left)
    right_norm = _norm(right)
    if not left_norm or not right_norm:
        return 0.0
    score = SequenceMatcher(None, left_norm, right_norm).ratio()
    if left_norm in right_norm or right_norm in left_norm:
        score = max(score, 0.9)
    return score


def _path_slug(path: Path) -> str:
    raw = str(path.resolve())
    return "".join(ch if ch.isalnum() else "-" for ch in raw).strip("-")


def _read_json(path: Path) -> dict[str, Any] | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else None
    except Exception:
        return None


def _project_score(project_dir: Path, project_path: Path) -> float:
    expected = _path_slug(project_path)
    if project_dir.name == expected:
        return 1.0
    score = _similarity(project_dir.name, str(project_path))
    score = max(score, _similarity(project_dir.name, project_path.name))
    if project_path.name and _norm(project_path.name) in _norm(project_dir.name):
        score = max(score, 0.75)
    return score


def find_project(claude_home: Path, project: Path) -> tuple[Path | None, list[tuple[Path, float]]]:
    projects_dir = claude_home / "projects"
    if not projects_dir.exists():
        return None, []
    scored = [
        (item, _project_score(item, project))
        for item in projects_dir.iterdir()
        if item.is_dir()
    ]
    scored.sort(key=lambda pair: (pair[1], pair[0].stat().st_mtime), reverse=True)
    best = scored[0][0] if scored and scored[0][1] >= 0.55 else None
    return best, scored[:8]


def list_memory_files(project_dir: Path) -> list[MemoryFile]:
    memory_dir = project_dir / "memory"
    if not memory_dir.exists():
        return []
    files = []
    for path in sorted(memory_dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True):
        stat = path.stat()
        files.append(
            MemoryFile(
                path=str(path),
                modified=_format_mtime(stat.st_mtime),
                bytes=stat.st_size,
            )
        )
    return files


def _format_mtime(timestamp: float) -> str:
    from datetime import datetime

    return datetime.fromtimestamp(timestamp).isoformat(timespec="seconds")


def _session_title(project_dir: Path, session_id: str) -> str | None:
    title_file = project_dir / session_id / "custom-title.json"
    data = _read_json(title_file)
    if not data:
        return None
    title = data.get("customTitle") or data.get("title")
    return str(title) if title else None


def _transcript_contains(path: Path, needle: str, max_bytes: int = 25_000_000) -> bool:
    if not needle or path.stat().st_size > max_bytes:
        return False
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            target = _norm(needle)
            for line in handle:
                if target and target in _norm(line):
                    return True
    except Exception:
        return False
    return False


def _transcript_contains_any(path: Path, needles: list[str], max_bytes: int = 25_000_000) -> bool:
    targets = [_norm(item) for item in needles if _norm(item)]
    if not targets or path.stat().st_size > max_bytes:
        return False
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            for line in handle:
                normalized = _norm(line)
                if any(target in normalized for target in targets):
                    return True
    except Exception:
        return False
    return False


def list_sessions(project_dir: Path, title: str | None) -> list[SessionCandidate]:
    sessions: list[SessionCandidate] = []
    for path in project_dir.glob("*.jsonl"):
        stat = path.stat()
        session_id = path.stem
        custom_title = _session_title(project_dir, session_id)
        score = 0.0
        if title:
            score = max(score, _similarity(custom_title or "", title))
            if _transcript_contains(path, title):
                score = max(score, 0.7)
        else:
            score = 0.1
        sessions.append(
            SessionCandidate(
                session_id=session_id,
                title=custom_title,
                transcript=str(path),
                modified=_format_mtime(stat.st_mtime),
                bytes=stat.st_size,
                score=score,
            )
        )
    sessions.sort(key=lambda item: (item.score, item.modified), reverse=True)
    return sessions


def _read_codex_index(codex_home: Path) -> dict[str, dict[str, Any]]:
    index_path = codex_home / "session_index.jsonl"
    result: dict[str, dict[str, Any]] = {}
    if not index_path.exists():
        return result
    try:
        with index_path.open("r", encoding="utf-8", errors="replace") as handle:
            for line in handle:
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                session_id = row.get("id")
                if not session_id:
                    continue
                key = str(session_id).lower()
                title = str(row.get("thread_name") or "")
                item = result.setdefault(key, {"title": "", "titles": [], "updated_at": ""})
                if title and title not in item["titles"]:
                    item["titles"].append(title)
                if title:
                    item["title"] = title
                item["updated_at"] = str(row.get("updated_at") or item.get("updated_at") or "")
    except Exception:
        return {}
    return result


def _ids_from_filename(path: Path) -> list[str]:
    ids = re.findall(
        r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
        path.name,
        flags=re.IGNORECASE,
    )
    return [item.lower() for item in ids]


def _codex_transcript_meta(path: Path) -> tuple[str, str | None]:
    session_id = _ids_from_filename(path)[0] if _ids_from_filename(path) else path.stem
    cwd = None
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            for index, line in enumerate(handle):
                if index > 300:
                    break
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if row.get("type") != "session_meta":
                    continue
                payload = row.get("payload")
                if not isinstance(payload, dict):
                    continue
                session_id = str(payload.get("session_id") or payload.get("id") or session_id)
                cwd_value = payload.get("cwd")
                cwd = str(cwd_value) if cwd_value else None
                break
    except Exception:
        pass
    return session_id, cwd


def _path_matches_project(candidate: str | None, project: Path) -> bool:
    if not candidate:
        return False
    try:
        return Path(candidate).expanduser().resolve() == project.resolve()
    except Exception:
        return _norm(candidate) == _norm(str(project))


def _codex_title_for_ids(index: dict[str, dict[str, Any]], ids: list[str]) -> str | None:
    for session_id in ids:
        item = index.get(session_id)
        if item and item.get("title"):
            return item["title"]
    return None


def _codex_title_score(index: dict[str, dict[str, Any]], ids: list[str], title: str | None) -> float:
    if not title:
        return 0.0
    scores: list[float] = []
    for session_id in ids:
        item = index.get(session_id) or {}
        values = [item.get("title", ""), *(item.get("titles") or [])]
        scores.extend(_similarity(str(value), title) for value in values)
    return max(scores, default=0.0)


def _codex_files_to_scan(
    sessions_dir: Path,
    *,
    index: dict[str, dict[str, Any]],
    title: str | None,
    max_files: int,
) -> list[Path]:
    all_files = list(sessions_dir.rglob("*.jsonl"))
    selected: list[Path] = []
    selected_keys: set[str] = set()
    if title:
        matching_ids = {
            session_id
            for session_id, item in index.items()
            if max(
                (_similarity(str(value), title) for value in [item.get("title", ""), *(item.get("titles") or [])]),
                default=0.0,
            )
            >= 0.7
        }
        for path in all_files:
            filename_ids = set(_ids_from_filename(path))
            if filename_ids & matching_ids:
                selected.append(path)
                selected_keys.add(str(path))

    recent = sorted(all_files, key=lambda item: item.stat().st_mtime, reverse=True)
    for path in recent[: max(1, max_files)]:
        key = str(path)
        if key not in selected_keys:
            selected.append(path)
            selected_keys.add(key)
    return selected


def list_codex_sessions(
    codex_home: Path,
    project: Path,
    title: str | None,
    *,
    max_files: int,
) -> list[CodexSessionCandidate]:
    sessions_dir = codex_home / "sessions"
    if not sessions_dir.exists():
        return []
    index = _read_codex_index(codex_home)
    files = _codex_files_to_scan(
        sessions_dir,
        index=index,
        title=title,
        max_files=max_files,
    )

    candidates: list[CodexSessionCandidate] = []
    for path in files:
        stat = path.stat()
        session_id, cwd = _codex_transcript_meta(path)
        ids = [session_id.lower(), *_ids_from_filename(path)]
        seen: set[str] = set()
        ids = [item for item in ids if not (item in seen or seen.add(item))]
        session_title = _codex_title_for_ids(index, ids)

        title_score = _codex_title_score(index, ids, title)

        project_score = 0.0
        if _path_matches_project(cwd, project):
            project_score = 1.0
        elif cwd and _norm(project.name) in _norm(cwd):
            project_score = 0.7

        if title:
            score = (title_score * 0.65) + (project_score * 0.35)
        else:
            score = project_score
        if score < 0.45 and project_score < 0.65 and title_score < 0.7:
            continue

        candidates.append(
            CodexSessionCandidate(
                session_id=session_id,
                title=session_title,
                transcript=str(path),
                cwd=cwd,
                modified=_format_mtime(stat.st_mtime),
                bytes=stat.st_size,
                score=score,
            )
        )
    candidates.sort(key=lambda item: (item.score, item.modified), reverse=True)
    return candidates[:10]


def _safe_markdown_name(memory_name: str, fallback: str) -> str:
    safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "-", memory_name).strip(".-")
    if not safe_name:
        safe_name = fallback
    if not safe_name.endswith(".md"):
        safe_name += ".md"
    return safe_name


def list_codex_handoff_files(codex_home: Path, project: Path) -> list[MemoryFile]:
    handoff_dir = codex_home / "memory-sync" / _path_slug(project)
    if not handoff_dir.exists():
        return []
    files = []
    for path in sorted(handoff_dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True):
        stat = path.stat()
        files.append(
            MemoryFile(
                path=str(path),
                modified=_format_mtime(stat.st_mtime),
                bytes=stat.st_size,
            )
        )
    return files


def write_claude_memory(project_dir: Path, source_path: Path, memory_name: str) -> Path:
    if not source_path.exists():
        raise FileNotFoundError(source_path)
    safe_name = _safe_markdown_name(memory_name, "codex-handoff.md")
    memory_dir = project_dir / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)
    target = memory_dir / safe_name
    content = source_path.read_text(encoding="utf-8", errors="replace").strip()
    from datetime import datetime

    section = (
        f"\n\n## Codex Handoff {datetime.now().isoformat(timespec='seconds')}\n\n"
        f"Source: `{source_path}`\n\n"
        f"{content}\n"
    )
    with target.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(section)
    return target


def write_codex_handoff(codex_home: Path, project: Path, source_path: Path, memory_name: str) -> Path:
    if not source_path.exists():
        raise FileNotFoundError(source_path)
    safe_name = _safe_markdown_name(memory_name, "claude-handoff.md")
    handoff_dir = codex_home / "memory-sync" / _path_slug(project)
    handoff_dir.mkdir(parents=True, exist_ok=True)
    target = handoff_dir / safe_name
    content = source_path.read_text(encoding="utf-8", errors="replace").strip()
    from datetime import datetime

    section = (
        f"\n\n## Claude Handoff {datetime.now().isoformat(timespec='seconds')}\n\n"
        f"Project: `{project}`\n\n"
        f"Source: `{source_path}`\n\n"
        f"{content}\n"
    )
    with target.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(section)
    return target


def _content_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, dict):
                text = item.get("text")
                if isinstance(text, str):
                    parts.append(text)
        return "\n".join(parts)
    return ""


def transcript_tail(path: Path, limit: int) -> list[dict[str, str]]:
    if limit <= 0 or not path.exists():
        return []
    turns: list[dict[str, str]] = []
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            for line in handle:
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                message = row.get("message")
                if not isinstance(message, dict):
                    continue
                role = message.get("role")
                if role not in {"user", "assistant"}:
                    continue
                text = _content_text(message.get("content")).strip()
                if not text or "system-reminder" in text:
                    continue
                turns.append(
                    {
                        "role": str(role),
                        "timestamp": str(row.get("timestamp") or ""),
                        "text": text[:2000],
                    }
                )
    except Exception:
        return []
    return turns[-limit:]


def _print_markdown(result: dict[str, Any], include_memory: bool, tail: int) -> None:
    print("# Claude/Codex Memory Lookup")
    print()
    print(f"- project: `{result['project']}`")
    print(f"- claude_home: `{result['claude_home']}`")
    print(f"- codex_home: `{result['codex_home']}`")
    if result.get("project_dir"):
        print(f"- matched_project_dir: `{result['project_dir']}`")
    else:
        print("- matched_project_dir: not found")
    if result.get("written_claude_memory"):
        print(f"- written_claude_memory: `{result['written_claude_memory']}`")
    if result.get("written_codex_handoff"):
        print(f"- written_codex_handoff: `{result['written_codex_handoff']}`")
    print()

    alternatives = result.get("project_candidates") or []
    if alternatives:
        print("## Project Candidates")
        for item in alternatives[:5]:
            print(f"- {item['score']:.2f} `{item['path']}`")
        print()

    memories = result.get("memory_files") or []
    print("## Memory Files")
    if memories:
        for item in memories:
            print(f"- `{item['path']}` ({item['modified']}, {item['bytes']} bytes)")
    else:
        print("- none")
    print()

    sessions = result.get("sessions") or []
    print("## Session Candidates")
    if sessions:
        for item in sessions[:5]:
            title = item.get("title") or "(untitled)"
            print(
                f"- score={item['score']:.2f} title=`{title}` id=`{item['session_id']}` "
                f"modified={item['modified']} transcript=`{item['transcript']}`"
            )
    else:
        print("- none")
    print()

    codex_sessions = result.get("codex_sessions") or []
    print("## Codex Session Candidates")
    if codex_sessions:
        for item in codex_sessions[:5]:
            title = item.get("title") or "(untitled)"
            cwd = item.get("cwd") or ""
            print(
                f"- score={item['score']:.2f} title=`{title}` id=`{item['session_id']}` "
                f"modified={item['modified']} cwd=`{cwd}` transcript=`{item['transcript']}`"
            )
    else:
        print("- none")
    print()

    codex_handoffs = result.get("codex_handoff_files") or []
    print("## Codex Handoff Files")
    if codex_handoffs:
        for item in codex_handoffs:
            print(f"- `{item['path']}` ({item['modified']}, {item['bytes']} bytes)")
    else:
        print("- none")
    print()

    if include_memory and result.get("memory_contents"):
        print("## Memory Contents")
        for item in result["memory_contents"]:
            print(f"\n### {item['path']}\n")
            print(item["content"])
            print()

    if tail and result.get("transcript_tail"):
        print("## Transcript Tail")
        for item in result["transcript_tail"]:
            role = item["role"]
            timestamp = item["timestamp"]
            print(f"\n### {role} {timestamp}\n")
            print(item["text"])


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", default=".", help="Project root, defaults to cwd")
    parser.add_argument("--title", default="", help="Conversation/session title to match")
    parser.add_argument("--claude-home", default="", help="Claude home, defaults to CLAUDE_HOME or ~/.claude")
    parser.add_argument("--codex-home", default="", help="Codex home, defaults to CODEX_HOME or ~/.codex")
    parser.add_argument("--include-memory", action="store_true", help="Print Claude memory markdown contents")
    parser.add_argument("--tail", type=int, default=0, help="Print last N text turns from best session")
    parser.add_argument("--max-codex-files", type=int, default=300, help="Recent Codex transcript files to scan")
    parser.add_argument(
        "--write-claude-memory-from",
        default="",
        help="Append this Markdown file to Claude project memory",
    )
    parser.add_argument(
        "--memory-name",
        default="codex-handoff.md",
        help="Claude memory file name used with --write-claude-memory-from",
    )
    parser.add_argument(
        "--write-codex-handoff-from",
        default="",
        help="Append this Markdown file to Codex handoff memory without touching Codex sqlite files",
    )
    parser.add_argument(
        "--codex-handoff-name",
        default="claude-handoff.md",
        help="Codex handoff file name used with --write-codex-handoff-from",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of markdown")
    args = parser.parse_args()

    project = Path(args.project).expanduser().resolve()
    claude_home = Path(args.claude_home).expanduser() if args.claude_home else _home_path("CLAUDE_HOME", ".claude")
    codex_home = Path(args.codex_home).expanduser() if args.codex_home else _home_path("CODEX_HOME", ".codex")
    project_dir, project_candidates = find_project(claude_home, project)
    codex_sessions = list_codex_sessions(
        codex_home,
        project,
        args.title.strip() or None,
        max_files=args.max_codex_files,
    )

    result: dict[str, Any] = {
        "project": str(project),
        "claude_home": str(claude_home),
        "codex_home": str(codex_home),
        "project_dir": str(project_dir) if project_dir else None,
        "project_candidates": [
            {"path": str(path), "score": score}
            for path, score in project_candidates
        ],
        "memory_files": [],
        "sessions": [],
        "codex_sessions": [asdict(item) for item in codex_sessions],
        "codex_handoff_files": [],
        "memory_contents": [],
        "transcript_tail": [],
        "written_claude_memory": None,
        "written_codex_handoff": None,
    }

    if args.write_codex_handoff_from:
        written = write_codex_handoff(
            codex_home,
            project,
            Path(args.write_codex_handoff_from).expanduser(),
            args.codex_handoff_name,
        )
        result["written_codex_handoff"] = str(written)

    result["codex_handoff_files"] = [
        asdict(item)
        for item in list_codex_handoff_files(codex_home, project)
    ]

    if project_dir:
        if args.write_claude_memory_from:
            written = write_claude_memory(
                project_dir,
                Path(args.write_claude_memory_from).expanduser(),
                args.memory_name,
            )
            result["written_claude_memory"] = str(written)
        memories = list_memory_files(project_dir)
        sessions = list_sessions(project_dir, args.title.strip() or None)
        result["memory_files"] = [asdict(item) for item in memories]
        result["sessions"] = [asdict(item) for item in sessions]
        if args.include_memory:
            for item in memories:
                path = Path(item.path)
                try:
                    content = path.read_text(encoding="utf-8", errors="replace")
                except Exception as exc:
                    content = f"[failed to read: {type(exc).__name__}]"
                result["memory_contents"].append(
                    {"path": item.path, "content": content[:12000]}
                )
        if args.tail and sessions:
            result["transcript_tail"] = transcript_tail(Path(sessions[0].transcript), args.tail)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        _print_markdown(result, args.include_memory, args.tail)
    return 0 if project_dir or codex_sessions or result.get("written_codex_handoff") else 2


if __name__ == "__main__":
    raise SystemExit(main())
