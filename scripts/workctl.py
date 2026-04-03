#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path


VALID_STATUSES = ("inbox", "active", "blocked", "completed", "archive")
VALID_PRIORITIES = ("high", "medium", "low")
TASK_FILES = ("TASK.md", "CONTEXT.md", "PLAN.md", "TODO.md", "LOG.md", "DECISIONS.md")
TASK_DIRS = ("OUTPUT", "REFERENCES", "SCRATCH")
TEMPLATE_DIR = Path("templates/work_item")

TREE = [
    ("PROJECT_FORM.md", "user-owned project brief", []),
    ("PROJECT_STATE.md", "agent-owned execution state", []),
    ("RUN_PROMPT.md", "single repeated run prompt", []),
    ("AGENTS.md", "shared Codex-style rules", []),
    ("CLAUDE.md", "shared Claude Code rules", []),
    ("docs/", "structure and workflow docs", []),
    (
        "work/",
        "generic work area",
        [
            ("inbox/", "not started"),
            ("active/", "in progress"),
            ("blocked/", "blocked"),
            ("completed/", "completed"),
            ("archive/", "archived"),
        ],
    ),
    ("templates/work_item/", "generic work template", []),
]

GUIDE = {
    "root": {
        "path": ".",
        "purpose": "A generic-work workspace template shared by Codex and Claude CLI.",
        "store": [
            "`docs/`: structural and workflow guidance",
            "`work/`: status-based work items",
            "`templates/work_item/`: template for new work items",
        ],
        "avoid": [
            "Do not leave work state only in chat.",
            "Do not scatter one-off task files directly at the root.",
        ],
    },
    "work": {
        "path": "work/",
        "purpose": "Store generic work in status-based folders.",
        "store": [
            "`inbox/`: not started",
            "`active/`: in progress",
            "`blocked/`: blocked",
            "`completed/`: completed",
            "`archive/`: long-term storage",
        ],
        "avoid": [
            "Do not mix unrelated tasks in one folder.",
            "Do not create copies when status changes.",
        ],
    },
    "work/inbox": {
        "path": "work/inbox/",
        "purpose": "Store work that has been scoped but not started.",
        "store": [
            "background notes and initial planning",
        ],
        "avoid": [
            "Do not leave active work here for long.",
        ],
    },
    "work/active": {
        "path": "work/active/",
        "purpose": "Store work currently in progress.",
        "store": [
            "the currently active work folder",
            "actively updated TODO, LOG, and DECISIONS files",
        ],
        "avoid": [
            "Do not leave completed work here.",
        ],
    },
    "work/blocked": {
        "path": "work/blocked/",
        "purpose": "Store work blocked by approvals, missing information, or dependencies.",
        "store": [
            "why the work is blocked and how it can resume",
        ],
        "avoid": [
            "Do not keep progress-ready work blocked.",
        ],
    },
    "work/completed": {
        "path": "work/completed/",
        "purpose": "Store completed work worth referencing later.",
        "store": [
            "final outputs and decision records",
        ],
        "avoid": [
            "Do not close work without recording important follow-up publishing steps.",
        ],
    },
    "work/archive": {
        "path": "work/archive/",
        "purpose": "Store long-term archived work.",
        "store": [
            "past work no longer actively tracked",
        ],
        "avoid": [
            "Do not archive still-relevant active work too early.",
        ],
    },
    "templates/work_item": {
        "path": "templates/work_item/",
        "purpose": "Store the template copied when a new work item is created.",
        "store": [
            "default document skeletons and helper files",
        ],
        "avoid": [
            "Do not store real work outputs inside the template folder.",
        ],
    },
}


def default_workspace() -> Path:
    return Path(__file__).resolve().parent.parent


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def today_utc() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "_", value.strip().lower()).strip("_")
    return slug or "task"


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def dump_json(path: Path, payload: dict) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def require_workspace(root: Path) -> list[str]:
    issues = []
    required_paths = [
        root / "PROJECT_FORM.md",
        root / "PROJECT_STATE.md",
        root / "RUN_PROMPT.md",
        root / "README.md",
        root / "AGENTS.md",
        root / "CLAUDE.md",
        root / "docs" / "WORKFLOW.md",
        root / "docs" / "FILE_INDEX.md",
        root / "work" / "INDEX.md",
        root / TEMPLATE_DIR / "TASK.md",
        root / "scripts",
    ]
    for path in required_paths:
        if not path.exists():
            issues.append(f"missing workspace path: {path}")
    for status in VALID_STATUSES:
        if not (root / "work" / status).exists():
            issues.append(f"missing work status directory: {root / 'work' / status}")
    return issues


def iter_tasks(root: Path):
    work_root = root / "work"
    for status in VALID_STATUSES:
        status_dir = work_root / status
        if not status_dir.exists():
            continue
        for child in sorted(status_dir.iterdir()):
            if child.name.startswith(".") or not child.is_dir():
                continue
            yield child


def find_task(root: Path, token: str) -> Path:
    candidate = Path(token)
    if not candidate.is_absolute():
        candidate = (root / token).resolve()
    if candidate.exists() and (candidate / "task.json").exists():
        return candidate

    suffix = slugify(token)
    matches = []
    for task_dir in iter_tasks(root):
        if task_dir.name == token or task_dir.name == suffix or task_dir.name.endswith(f"_{suffix}"):
            matches.append(task_dir)

    if not matches:
        raise SystemExit(f"task not found: {token}")
    if len(matches) > 1:
        joined = ", ".join(str(path.relative_to(root)) for path in matches)
        raise SystemExit(f"task reference is ambiguous: {token} -> {joined}")
    return matches[0]


def render_template(text: str, replacements: dict[str, str]) -> str:
    for key, value in replacements.items():
        text = text.replace(f"{{{{{key}}}}}", value)
    return text


def build_metadata(args: argparse.Namespace, task_id: str) -> dict:
    return {
        "task_id": task_id,
        "title": args.title or task_id,
        "owner": args.owner or "unassigned",
        "date": args.date,
        "status": args.status,
        "priority": args.priority,
        "created_at": utc_now(),
        "updated_at": utc_now(),
        "tags": [],
    }


def write_task_files(root: Path, task_dir: Path, metadata: dict) -> None:
    template_root = root / TEMPLATE_DIR
    relative_task_root = task_dir.relative_to(root).as_posix()
    replacements = {
        "TASK_ID": metadata["task_id"],
        "TITLE": metadata["title"],
        "OWNER": metadata["owner"],
        "DATE": metadata["date"],
        "STATUS": metadata["status"],
        "PRIORITY": metadata["priority"],
        "TASK_ROOT": relative_task_root,
    }

    for template_path in template_root.rglob("*"):
        relative = template_path.relative_to(template_root)
        if relative == Path("README.md"):
            continue
        target = task_dir / relative
        if template_path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        text = template_path.read_text(encoding="utf-8")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render_template(text, replacements), encoding="utf-8")


def update_line_block(text: str, label: str, value: str) -> str:
    pattern = rf"^- {re.escape(label)}:.*$"
    replacement = f"- {label}: {value}"
    if re.search(pattern, text, flags=re.MULTILINE):
        return re.sub(pattern, replacement, text, flags=re.MULTILINE)
    return text


def sync_task_summary(root: Path, task_dir: Path, metadata: dict) -> None:
    task_md = task_dir / "TASK.md"
    if not task_md.exists():
        return
    text = task_md.read_text(encoding="utf-8")
    relative_task_root = task_dir.relative_to(root).as_posix()
    replacements = {
        "Task ID": metadata["task_id"],
        "Title": metadata["title"],
        "Owner": metadata["owner"],
        "Date": metadata["date"],
        "Status": f"`{metadata['status']}`",
        "Priority": f"`{metadata['priority']}`",
        "Task Root": relative_task_root,
    }
    for label, value in replacements.items():
        text = update_line_block(text, label, value)
    task_md.write_text(text, encoding="utf-8")


def sync_index(root: Path) -> None:
    work_root = root / "work"
    lines = [
        "# Work Index",
        "",
        "This file is synchronized by `scripts/workctl.py`.",
        "",
    ]

    headings = {
        "inbox": "Inbox",
        "active": "Active",
        "blocked": "Blocked",
        "completed": "Completed",
        "archive": "Archive",
    }

    task_map: dict[str, list[dict]] = {status: [] for status in VALID_STATUSES}
    for task_dir in iter_tasks(root):
        metadata_path = task_dir / "task.json"
        if not metadata_path.exists():
            continue
        metadata = load_json(metadata_path)
        task_map[task_dir.parent.name].append(
            {
                "id": metadata.get("task_id", task_dir.name),
                "title": metadata.get("title", task_dir.name),
                "owner": metadata.get("owner", "unknown"),
                "priority": metadata.get("priority", "unknown"),
                "path": task_dir.relative_to(root).as_posix(),
            }
        )

    for status in VALID_STATUSES:
        lines.append(f"## {headings[status]}")
        lines.append("")
        entries = task_map[status]
        if not entries:
            lines.append("- None")
            lines.append("")
            continue
        for entry in entries:
            lines.append(
                f"- `{entry['id']}` | {entry['title']} | owner={entry['owner']} | "
                f"priority={entry['priority']} | path=`{entry['path']}`"
            )
        lines.append("")

    (work_root / "INDEX.md").write_text("\n".join(lines), encoding="utf-8")


def validate_task(root: Path, task_dir: Path) -> list[str]:
    issues = []
    if task_dir.parent.name not in VALID_STATUSES:
        issues.append(f"{task_dir}: parent directory is not a valid work status")
        return issues

    metadata_path = task_dir / "task.json"
    if not metadata_path.exists():
        issues.append(f"{task_dir}: missing task.json")
        return issues

    try:
        metadata = load_json(metadata_path)
    except json.JSONDecodeError as exc:
        issues.append(f"{task_dir}: invalid task.json ({exc})")
        return issues

    required_fields = ("task_id", "title", "owner", "date", "status", "priority")
    for field in required_fields:
        if not metadata.get(field):
            issues.append(f"{task_dir}: missing metadata field `{field}`")

    if metadata.get("status") != task_dir.parent.name:
        issues.append(
            f"{task_dir}: metadata status `{metadata.get('status')}` does not match parent directory `{task_dir.parent.name}`"
        )
    if metadata.get("task_id") != task_dir.name:
        issues.append(
            f"{task_dir}: metadata task_id `{metadata.get('task_id')}` does not match directory name `{task_dir.name}`"
        )
    if metadata.get("priority") and metadata["priority"] not in VALID_PRIORITIES:
        issues.append(f"{task_dir}: invalid priority `{metadata['priority']}`")

    for filename in TASK_FILES:
        if not (task_dir / filename).exists():
            issues.append(f"{task_dir}: missing required file `{filename}`")
    for dirname in TASK_DIRS:
        if not (task_dir / dirname).is_dir():
            issues.append(f"{task_dir}: missing required directory `{dirname}/`")

    task_md = task_dir / "TASK.md"
    if task_md.exists():
        text = task_md.read_text(encoding="utf-8")
        expected_status_line = f"- Status: `{task_dir.parent.name}`"
        match = re.search(r"^- Status:.*$", text, flags=re.MULTILINE)
        if match and match.group(0) != expected_status_line:
            issues.append(
                f"{task_dir}: TASK.md status line `{match.group(0)}` does not match expected `{expected_status_line}`"
            )
    return issues


def resolve_guide_key(root: Path, target: str | None) -> str:
    if not target:
        return "root"
    cleaned = target.strip().strip("/")
    if cleaned in GUIDE:
        return cleaned

    candidate = Path(cleaned)
    if not candidate.is_absolute():
        candidate = (root / cleaned).resolve()
    try:
        relative = candidate.relative_to(root).as_posix().strip("/")
    except ValueError:
        relative = cleaned
    if relative in GUIDE:
        return relative
    raise SystemExit(f"unknown guide target: {target}")


def cmd_tree(args: argparse.Namespace) -> int:
    print(args.workspace)
    for name, description, children in TREE:
        print(f"- {name:<22} {description}")
        for child, child_description in children:
            print(f"  - {child:<18} {child_description}")
    return 0


def cmd_guide(args: argparse.Namespace) -> int:
    key = resolve_guide_key(args.workspace, args.target)
    entry = GUIDE[key]
    print(entry["path"])
    print(f"Purpose: {entry['purpose']}")
    print("Store here:")
    for item in entry["store"]:
        print(f"- {item}")
    print("Avoid:")
    for item in entry["avoid"]:
        print(f"- {item}")
    return 0


def cmd_init(args: argparse.Namespace) -> int:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.date):
        raise SystemExit("--date must be in YYYY-MM-DD format")

    task_id = f"{args.date}_{slugify(args.name)}"
    task_dir = args.workspace / "work" / args.status / task_id
    if task_dir.exists() and not args.force:
        raise SystemExit(f"task already exists: {task_dir}")

    if args.dry_run:
        print(task_dir)
        return 0

    task_dir.mkdir(parents=True, exist_ok=True)
    metadata = build_metadata(args, task_id)
    write_task_files(args.workspace, task_dir, metadata)
    dump_json(task_dir / "task.json", metadata)
    sync_task_summary(args.workspace, task_dir, metadata)
    sync_index(args.workspace)
    print(task_dir.relative_to(args.workspace))
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    results = []
    for task_dir in iter_tasks(args.workspace):
        status = task_dir.parent.name
        if args.status and status != args.status:
            continue
        metadata = load_json(task_dir / "task.json") if (task_dir / "task.json").exists() else {}
        results.append(
            {
                "id": metadata.get("task_id", task_dir.name),
                "title": metadata.get("title", task_dir.name),
                "owner": metadata.get("owner", "unknown"),
                "priority": metadata.get("priority", "unknown"),
                "status": status,
                "path": task_dir.relative_to(args.workspace).as_posix(),
            }
        )

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return 0

    if not results:
        print("no tasks found")
        return 0

    for item in results:
        print(
            f"{item['status']:<10} {item['priority']:<6} {item['owner']:<12} "
            f"{item['id']:<32} {item['title']}"
        )
    return 0


def cmd_move(args: argparse.Namespace) -> int:
    task_dir = find_task(args.workspace, args.task)
    metadata = load_json(task_dir / "task.json")
    target_dir = args.workspace / "work" / args.status / task_dir.name
    if task_dir == target_dir:
        print(task_dir.relative_to(args.workspace))
        return 0
    if target_dir.exists():
        raise SystemExit(f"target task directory already exists: {target_dir}")

    shutil.move(str(task_dir), str(target_dir))
    metadata["status"] = args.status
    metadata["updated_at"] = utc_now()
    dump_json(target_dir / "task.json", metadata)
    sync_task_summary(args.workspace, target_dir, metadata)
    sync_index(args.workspace)
    print(target_dir.relative_to(args.workspace))
    return 0


def cmd_sync_index(args: argparse.Namespace) -> int:
    sync_index(args.workspace)
    print((args.workspace / "work" / "INDEX.md").relative_to(args.workspace))
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    issues = require_workspace(args.workspace)
    if args.all:
        targets = list(iter_tasks(args.workspace))
    elif args.target:
        targets = [find_task(args.workspace, args.target)]
    else:
        targets = []

    seen_ids: set[str] = set()
    for task_dir in targets:
        if task_dir.name in seen_ids:
            issues.append(f"duplicate task directory name detected: {task_dir.name}")
        seen_ids.add(task_dir.name)
        issues.extend(validate_task(args.workspace, task_dir))

    if issues:
        print("validation failed")
        for issue in issues:
            print(f"- {issue}")
        return 1

    if args.all:
        print(f"validation passed for workspace and {len(targets)} task(s)")
    elif args.target:
        print(f"validation passed for {targets[0].relative_to(args.workspace)}")
    else:
        print("workspace structure looks valid")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manage generic work items in the agent workspace."
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        default=default_workspace(),
        help="workspace root path (default: script parent)",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    tree_parser = subparsers.add_parser("tree", help="print the generic workspace tree")
    tree_parser.set_defaults(func=cmd_tree)

    guide_parser = subparsers.add_parser("guide", help="print guidance for a folder")
    guide_parser.add_argument("target", nargs="?", help="folder name or path")
    guide_parser.set_defaults(func=cmd_guide)

    init_parser = subparsers.add_parser("init", help="create a new generic work item")
    init_parser.add_argument("name", help="task slug or short name")
    init_parser.add_argument("--title", help="human-readable task title")
    init_parser.add_argument("--owner", help="owner name")
    init_parser.add_argument("--date", default=today_utc(), help="date prefix in YYYY-MM-DD format")
    init_parser.add_argument("--status", choices=VALID_STATUSES, default="active")
    init_parser.add_argument("--priority", choices=VALID_PRIORITIES, default="medium")
    init_parser.add_argument("--dry-run", action="store_true", help="print the target path without creating files")
    init_parser.add_argument("--force", action="store_true", help="overwrite an existing task directory")
    init_parser.set_defaults(func=cmd_init)

    list_parser = subparsers.add_parser("list", help="list work items")
    list_parser.add_argument("--status", choices=VALID_STATUSES, help="filter by status")
    list_parser.add_argument("--json", action="store_true", help="print machine-readable JSON")
    list_parser.set_defaults(func=cmd_list)

    move_parser = subparsers.add_parser("move", help="move a work item to another status")
    move_parser.add_argument("task", help="task path, id, or unique slug")
    move_parser.add_argument("status", choices=VALID_STATUSES, help="target work status")
    move_parser.set_defaults(func=cmd_move)

    sync_parser = subparsers.add_parser("sync-index", help="rewrite work/INDEX.md from current tasks")
    sync_parser.set_defaults(func=cmd_sync_index)

    validate_parser = subparsers.add_parser("validate", help="validate workspace or task structure")
    validate_parser.add_argument("target", nargs="?", help="task path or task id")
    validate_parser.add_argument("--all", action="store_true", help="validate all tasks in the workspace")
    validate_parser.set_defaults(func=cmd_validate)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    args.workspace = args.workspace.resolve()

    workspace_issues = require_workspace(args.workspace)
    if workspace_issues and args.command not in {"tree", "guide", "validate"}:
        for issue in workspace_issues:
            print(issue, file=sys.stderr)
        return 1

    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
