"""Collect a small summary of one day of agent sessions for a retrospective.

Reads the JSONL transcripts that Claude Code writes (one file per session, subagents in
<session>/subagents/*.jsonl) and writes a short markdown summary: sessions, relative
cost in tokens (subagents included), tool failures, denied permissions, hook blocks,
re-reads, repeated commands, large outputs, interruptions, heuristic correction signals,
skills triggered and skill files read.

This depends on the Claude Code transcript format. Another agent needs an adapter that
produces the same event shape (type, timestamp, message.content blocks).

Usage:
  python collect.py --project-dir ~/.claude/projects/<project> [--date YYYY-MM-DD]
                    [--out DIR] [--tz NAME] [--correction-file FILE] [--revision-file FILE]

Read-only on transcripts. Standard library only. Output is ASCII.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import date, datetime, time, timedelta, timezone, tzinfo
from pathlib import Path

LARGE_OUTPUT_CHARS = 20_000  # tool results at least this long count as "large"
# Approximate weights in input-token units. Prices differ by model and change over time:
# use the result to rank days and sessions against each other, never as a bill.
COST_WEIGHTS = {
    "input_tokens": 1.0,
    "cache_creation_input_tokens": 1.25,
    "cache_read_input_tokens": 0.1,
    "output_tokens": 5.0,
}
MAX_ITEMS = 8  # items listed per bullet group
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
SECRET = re.compile(r"(?i)(token|password|secret|api[_-]?key)\s*[:=]\s*\S+")
EMPTY_RESULT = ("No files found", "No matches found", "Found 0")


def clean(text: str, limit: int = 220) -> str:
    """Redact obvious secrets, drop harness reminders, collapse space, cut, force ASCII."""
    text = SECRET.sub(r"\1=***", EMAIL.sub("<email>", text))
    text = re.sub(r"<system-reminder>.*?</system-reminder>", "", text, flags=re.S)
    text = " ".join(text.split())
    text = text[:limit] + ("..." if len(text) > limit else "")
    return text.encode("ascii", "replace").decode("ascii")


def load_patterns(flags: list[str] | None, path: Path | None) -> list[re.Pattern]:
    """Compile case-insensitive patterns from repeatable flags and a one-per-line file."""
    raw = list(flags or [])
    if path:
        raw += [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines()
                if ln.strip() and not ln.startswith("#")]
    return [re.compile(p, re.I) for p in raw]


def local_time(value: str | None, zone: tzinfo) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(zone)
    except ValueError:
        return None


def text_of(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(
            b.get("text", "") if isinstance(b, dict) else str(b)
            for b in content
            if isinstance(b, str) or (isinstance(b, dict) and b.get("type") == "text")
        )
    return ""


def human_prompt(event: dict) -> str | None:
    """Text typed by the user (not meta lines, tool results or harness notices)."""
    if event.get("type") != "user" or event.get("isMeta") or event.get("isSidechain"):
        return None
    content = (event.get("message") or {}).get("content")
    if isinstance(content, list) and any(
        isinstance(b, dict) and b.get("type") == "tool_result" for b in content
    ):
        return None
    text = text_of(content).strip()
    if not text or text.startswith(("<local-command", "<command-name>", "<task-notification>")):
        return None
    return text


def skill_path(raw: str) -> str:
    """'<dir>/skills/<skill>/...' -> '<skill>/...' ('' when the path is not a skill file)."""
    parts = raw.replace("\\", "/").split("/")
    return "/".join(parts[len(parts) - parts[::-1].index("skills"):]) if "skills" in parts else ""


def analyze_file(path: Path, start: datetime, end: datetime, zone: tzinfo,
                 corrections: list[re.Pattern], revisions: list[re.Pattern]) -> dict | None:
    s = {
        "file": path.name, "title": "", "first": None, "last": None, "prompts": 0,
        "tokens": Counter(), "model_messages": 0, "tools": Counter(), "failures": [],
        "denials": 0, "hook_blocks": 0, "reads": Counter(), "commands": Counter(),
        "large": [], "corrections": [], "revision_signals": [], "interrupts": 0,
        "compactions": 0, "skills_used": Counter(), "skill_files_read": set(),
        "skill_files_edited": set(), "empty_searches": [],
    }
    seen: set[str] = set()
    names: dict[str, str] = {}
    inputs: dict[str, dict] = {}
    had_event = False
    with path.open(encoding="utf-8", errors="replace") as handle:
        for line in handle:
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("type") == "ai-title":
                s["title"] = event.get("aiTitle") or s["title"]
            moment = local_time(event.get("timestamp"), zone)
            if moment is None or not (start <= moment < end):
                continue
            had_event = True
            s["first"] = min(filter(None, [s["first"], moment]))
            s["last"] = max(filter(None, [s["last"], moment]))
            kind = event.get("type")
            if kind == "system" and "compact" in str(event.get("subtype", "")):
                s["compactions"] += 1
            if event.get("toolDenialKind"):
                s["denials"] += 1
            if "hook" in str(event.get("subtype", "")).lower() and "block" in json.dumps(event)[:2000].lower():
                s["hook_blocks"] += 1
            message = event.get("message") or {}
            if kind == "assistant" and isinstance(message, dict):
                mid = message.get("id")
                if mid and mid not in seen and message.get("usage"):
                    seen.add(mid)
                    s["model_messages"] += 1
                    for key in COST_WEIGHTS:
                        s["tokens"][key] += int(message["usage"].get(key) or 0)
                for block in message.get("content") or []:
                    if not isinstance(block, dict):
                        continue
                    if block.get("type") == "text":
                        for pat in revisions:
                            hit = pat.search(block.get("text", ""))
                            if hit:
                                t = block["text"]
                                snippet = t[max(0, hit.start() - 80):hit.end() + 140]
                                s["revision_signals"].append(f"{moment:%H:%M} agent: {clean(snippet)}")
                                break
                    if block.get("type") != "tool_use":
                        continue
                    name = block.get("name", "?")
                    args = block.get("input") or {}
                    names[block.get("id", "")] = name
                    inputs[block.get("id", "")] = args
                    s["tools"][name] += 1
                    target = args.get("file_path") or args.get("notebook_path") or ""
                    if name == "Skill" and args.get("skill"):
                        s["skills_used"][str(args["skill"])] += 1
                    rel = skill_path(target)
                    if rel:
                        bucket = "skill_files_read" if name == "Read" else (
                            "skill_files_edited" if name in {"Write", "Edit", "MultiEdit"} else None)
                        if bucket:
                            s[bucket].add(rel)
                    if name == "Read" and target:
                        s["reads"][target] += 1
                    if name in {"Bash", "PowerShell"} and args.get("command"):
                        s["commands"][clean(args["command"], 160)] += 1
            if kind != "user":
                continue
            content = message.get("content") if isinstance(message, dict) else None
            for block in content if isinstance(content, list) else []:
                if not (isinstance(block, dict) and block.get("type") == "tool_result"):
                    continue
                name = names.get(block.get("tool_use_id", ""), "?")
                raw = block.get("content")
                body = raw if isinstance(raw, str) else text_of(raw)
                if block.get("is_error"):
                    s["failures"].append(f"{moment:%H:%M} {name}: {clean(body, 180)}")
                if len(body) >= LARGE_OUTPUT_CHARS:
                    s["large"].append((len(body), f"{moment:%H:%M} {name}"))
                if name in {"Grep", "Glob"} and body.strip().startswith(EMPTY_RESULT):
                    pattern = (inputs.get(block.get("tool_use_id", "")) or {}).get("pattern", "")
                    s["empty_searches"].append(f"{moment:%H:%M} {name} '{clean(str(pattern), 80)}'")
            text = human_prompt(event)
            if text is None:
                continue
            if text.startswith("[Request interrupted"):
                s["interrupts"] += 1
                continue
            s["prompts"] += 1
            if any(p.search(text) for p in corrections):
                s["corrections"].append(f"{moment:%H:%M} {clean(text)}")
            if any(p.search(text) for p in revisions):
                s["revision_signals"].append(f"{moment:%H:%M} user: {clean(text)}")
    return s if had_event else None


def collect(project: Path, day: date, zone: tzinfo, corrections, revisions) -> dict:
    start = datetime.combine(day, time.min, zone)
    end = start + timedelta(days=1)
    cutoff = start.timestamp() - 3600
    sessions: list[dict] = []
    subagents: dict[str, Counter] = defaultdict(Counter)
    for path in sorted(project.glob("*.jsonl")):
        if path.stat().st_mtime >= cutoff and (s := analyze_file(path, start, end, zone, corrections, revisions)):
            sessions.append(s)
    for path in sorted(project.glob("*/subagents/*.jsonl")):
        if path.stat().st_mtime < cutoff:
            continue
        s = analyze_file(path, start, end, zone, corrections, revisions)
        if not s:
            continue
        parent = path.parent.parent.name + ".jsonl"
        subagents[parent] += s["tokens"]
        subagents[parent]["agents"] += 1
        owner = next((x for x in sessions if x["file"] == parent), None)
        if owner:  # a subagent's work counts for the session that launched it
            owner["skills_used"] += s["skills_used"]
            owner["skill_files_read"] |= s["skill_files_read"]
            owner["skill_files_edited"] |= s["skill_files_edited"]
            owner["revision_signals"] += [f"{x} (subagent)" for x in s["revision_signals"]]
    return {"day": day.isoformat(), "sessions": sessions, "subagents": subagents,
            "has_user_patterns": bool(corrections), "has_revision_patterns": bool(revisions)}


def tokens_total(t: Counter) -> int:
    return sum(t[k] for k in COST_WEIGHTS)


def cost(t: Counter) -> int:
    return round(sum(t[k] * w for k, w in COST_WEIGHTS.items()))


def render(data: dict) -> str:
    out = [f"# Retrospective - collection for {data['day']}", ""]
    sessions = data["sessions"]
    if not sessions:
        return "\n".join(out + ["No sessions on this day."]) + "\n"
    total = Counter()
    for s in sessions:
        total += s["tokens"]
    for t in data["subagents"].values():
        total += Counter({k: v for k, v in t.items() if k != "agents"})
    weights = " / ".join(f"{k.removesuffix('_tokens').replace('_input', '').replace('_', ' ')} {w}"
                         for k, w in COST_WEIGHTS.items())
    out += [
        f"- Sessions: {len(sessions)} | user prompts: {sum(s['prompts'] for s in sessions)}"
        f" | tool failures: {sum(len(s['failures']) for s in sessions)}"
        f" | correction signals: {sum(len(s['corrections']) for s in sessions)}",
        f"- Relative cost (sessions + subagents; approximate weights {weights}): {cost(total):,}",
        f"- Tokens (sessions + subagents): {tokens_total(total):,}",
    ]
    if not data["has_user_patterns"]:
        out.append("- NOTE: no correction patterns given; correction signals were not computed")
    if not data["has_revision_patterns"]:
        out.append("- NOTE: no revision patterns given; revised-conclusion signals were not computed")
    out.append("")
    for s in sorted(sessions, key=lambda x: cost(x["tokens"]), reverse=True):
        sub = data["subagents"].get(s["file"])
        out += [
            f"## {clean(s['title'] or s['file'], 80)} ({s['file'][:8]})",
            f"- {s['first']:%H:%M}-{s['last']:%H:%M} | prompts {s['prompts']} | model replies {s['model_messages']}"
            f" | relative cost {cost(s['tokens']):,}"
            + (f" | subagents {sub['agents']} cost {cost(sub):,}" if sub else ""),
            "- Tools: " + ", ".join(f"{n} {c}" for n, c in s["tools"].most_common(MAX_ITEMS)),
        ]
        extras = [f"{label} {s[key]}" for key, label in (
            ("denials", "permissions denied"), ("hook_blocks", "hook blocks"),
            ("interrupts", "interruptions"), ("compactions", "compactions")) if s[key]]
        if extras:
            out.append("- " + " | ".join(extras))
        rereads = sorted(((p, c) for p, c in s["reads"].items() if c > 1), key=lambda x: -x[1])
        if rereads:
            out.append("- Re-reads: " + "; ".join(f"{Path(p).name} x{c}" for p, c in rereads[:6]))
        repeated = sorted(((c, n) for c, n in s["commands"].items() if n > 1), key=lambda x: -x[1])
        if repeated:
            out.append("- Repeated commands: " + "; ".join(f"x{n} {c[:90]}" for c, n in repeated[:4]))
        if s["large"]:
            out.append("- Large outputs (chars): " + "; ".join(f"{q:,} {d}" for q, d in sorted(s["large"], reverse=True)[:5]))
        for label, key in (("Failures", "failures"),
                           ("Correction signals (heuristic, confirm in transcript)", "corrections"),
                           ("Revised-conclusion signals (heuristic, confirm at the source)", "revision_signals")):
            if s[key]:
                out.append(f"- {label}:")
                out += [f"  - {x}" for x in s[key][:MAX_ITEMS]]
                if len(s[key]) > MAX_ITEMS:
                    out.append(f"  - (+{len(s[key]) - MAX_ITEMS} omitted)")
        if s["empty_searches"]:
            out.append("- Searches with no result: " + "; ".join(s["empty_searches"][:6]))
        if s["skills_used"] or s["skill_files_read"] or s["skill_files_edited"]:
            out.append("- Skills triggered: " + (", ".join(f"{n} x{c}" for n, c in s["skills_used"].most_common()) or "-"))
            out.append("- Skill files read: " + (", ".join(sorted(s["skill_files_read"])) or "-"))
            out.append("- Skill files edited: " + (", ".join(sorted(s["skill_files_edited"])) or "-"))
        out.append("")
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--project-dir", type=Path, required=True,
                        help="folder with the agent's JSONL transcripts, e.g. ~/.claude/projects/<project>")
    parser.add_argument("--date", type=date.fromisoformat, help="YYYY-MM-DD (default: today)")
    parser.add_argument("--out", type=Path, help="folder for collection.md (default: print to stdout)")
    parser.add_argument("--tz", help="IANA time zone name (default: system time zone)")
    parser.add_argument("--correction-regex", action="append", help="user-correction pattern, repeatable")
    parser.add_argument("--correction-file", type=Path, help="one correction regex per line")
    parser.add_argument("--revision-regex", action="append", help="revised-conclusion pattern, repeatable")
    parser.add_argument("--revision-file", type=Path, help="one revised-conclusion regex per line")
    args = parser.parse_args()
    if not args.project_dir.is_dir():
        print(f"ERROR: not a folder: {args.project_dir}")
        return 2
    try:
        if args.tz and args.tz.upper() == "UTC":
            zone: tzinfo = timezone.utc  # works without the tz database (e.g. on Windows)
        elif args.tz:
            from zoneinfo import ZoneInfo  # needs the tz database; pip install tzdata on Windows
            zone = ZoneInfo(args.tz)
        else:
            zone = datetime.now().astimezone().tzinfo
        corrections = load_patterns(args.correction_regex, args.correction_file)
        revisions = load_patterns(args.revision_regex, args.revision_file)
    except (re.error, OSError, KeyError, ImportError) as exc:
        print(f"ERROR: invalid option ({type(exc).__name__}: {exc})")
        return 2
    day = args.date or datetime.now(zone).date()
    data = collect(args.project_dir, day, zone, corrections, revisions)
    text = render(data)
    if not args.out:
        sys.stdout.write(text)
        return 0
    args.out.mkdir(parents=True, exist_ok=True)
    target = args.out / "collection.md"
    partial = target.with_name(target.name + ".partial")
    partial.write_text(text, encoding="utf-8", newline="\n")
    partial.replace(target)
    print(f"OK: {len(data['sessions'])} session(s) on {data['day']} -> {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
