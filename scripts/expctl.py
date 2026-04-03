#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path


VALID_STATUSES = ("planned", "running", "completed", "published", "archive")
VALID_PRIORITIES = ("high", "medium", "low")
EXPERIMENT_CHILDREN = ("configs", "scripts", "logs", "results", "figures", "publish")

TOP_LEVEL_TREE = [
    ("PROJECT_FORM.md", "user-owned project brief", []),
    ("PROJECT_STATE.md", "agent-owned execution state", []),
    ("RUN_PROMPT.md", "single repeated run prompt", []),
    ("AGENTS.md", "shared Codex-style rules", []),
    ("CLAUDE.md", "shared Claude Code rules", []),
    ("docs/", "structure and workflow docs", []),
    (
        "work/",
        "generic work",
        [
            ("inbox/", "not started"),
            ("active/", "in progress"),
            ("blocked/", "blocked"),
            ("completed/", "completed"),
            ("archive/", "archived"),
        ],
    ),
    (
        "configs/",
        "shared experiment configs",
        [
            ("baselines/", "baseline configs"),
            ("variants/", "variant configs"),
            ("shared/", "shared config fragments"),
        ],
    ),
    (
        "experiments/",
        "experiment workspace",
        [
            ("planned/", "not started"),
            ("running/", "running"),
            ("completed/", "completed"),
            ("published/", "published"),
            ("archive/", "archived"),
        ],
    ),
    (
        "logs/",
        "shared logs",
        [
            ("system/", "system logs"),
            ("batches/", "batch logs"),
            ("debug/", "debug logs"),
        ],
    ),
    (
        "notes/",
        "notes and interpretations",
        [
            ("ideas/", "experiment ideas"),
            ("interpretations/", "result interpretation"),
            ("decisions/", "decision records"),
        ],
    ),
    (
        "publish/",
        "publish materials",
        [
            ("drafts/", "drafts"),
            ("final/", "final"),
            ("assets/", "attached assets"),
        ],
    ),
    (
        "reports/",
        "reports and slides",
        [
            ("internal/", "internal"),
            ("external/", "external"),
            ("slides/", "slides"),
        ],
    ),
    (
        "results/",
        "experiment results",
        [
            ("raw/", "raw outputs"),
            ("processed/", "processed outputs"),
            ("tables/", "tables"),
            ("figures/", "figures"),
        ],
    ),
    (
        "scripts/",
        "workspace scripts",
        [
            ("run/", "run"),
            ("collect/", "collect"),
            ("analyze/", "analyze"),
            ("publish/", "publish"),
        ],
    ),
    ("scratch/", "scratch space", []),
    ("templates/", "reusable templates", []),
]

GUIDE = {
    "root": {
        "path": ".",
        "purpose": "An agent workspace that manages generic work and code experiments together.",
        "store": [
            "`docs/` for structure and workflow docs",
            "`work/` for generic work folders",
            "`experiments/` for experiment folders",
            "`configs/`, `scripts/`, `results/`, and similar shared assets",
            "`templates/` for reusable templates",
        ],
        "avoid": [
            "Do not dump experiment-specific logs or outputs directly at the root.",
            "Do not track experiment status only through ad hoc notes.",
        ],
    },
    "configs": {
        "path": "configs/",
        "purpose": "Store baseline, variant, and shared config reused across experiments.",
        "store": [
            "`baselines/`: baseline experiment configs",
            "`variants/`: changed configs",
            "`shared/`: config fragments reused by multiple setups",
        ],
        "avoid": [
            "Put one-off configs inside the relevant experiment `configs/` folder.",
        ],
    },
    "experiments": {
        "path": "experiments/",
        "purpose": "Store experiments by lifecycle status.",
        "store": [
            "Use one directory per experiment.",
            "Prefer the name format `YYYY-MM-DD_<experiment_name>`.",
            "Each experiment should contain `README.md`, `experiment.json`, `configs/`, `scripts/`, `logs/`, `results/`, `figures/`, and `publish/`.",
        ],
        "avoid": [
            "Do not mix unrelated experiments in one directory.",
            "Move a directory instead of copying it when status changes.",
        ],
    },
    "experiments/planned": {
        "path": "experiments/planned/",
        "purpose": "Store experiment drafts that have not started yet.",
        "store": [
            "README files with design, hypothesis, and run plan",
            "configs prepared before execution",
        ],
        "avoid": [
            "Do not leave already-running experiments here.",
        ],
    },
    "experiments/running": {
        "path": "experiments/running/",
        "purpose": "Store experiments currently in progress.",
        "store": [
            "active logs and intermediate outputs",
            "experiment-local scripts being updated during execution",
        ],
        "avoid": [
            "Do not leave finished experiments here.",
        ],
    },
    "experiments/completed": {
        "path": "experiments/completed/",
        "purpose": "Store experiments whose runs and first-pass interpretation are finished.",
        "store": [
            "organized results",
            "README files with interpretation and follow-up actions",
        ],
        "avoid": [
            "Do not leave already-published experiments here.",
        ],
    },
    "experiments/published": {
        "path": "experiments/published/",
        "purpose": "Store experiments that have already been shared.",
        "store": [
            "publish links or final summary",
            "final figures and tables",
        ],
        "avoid": [
            "Do not classify draft material as published output.",
        ],
    },
    "experiments/archive": {
        "path": "experiments/archive/",
        "purpose": "Store experiments kept only for reference.",
        "store": [
            "closed experiments",
            "past reference experiments",
        ],
        "avoid": [
            "Do not archive experiments still used for active decision-making.",
        ],
    },
    "logs": {
        "path": "logs/",
        "purpose": "Store logs shared across experiments.",
        "store": [
            "`system/`: machine, environment, and infra logs",
            "`batches/`: grouped run logs",
            "`debug/`: shared debugging logs",
        ],
        "avoid": [
            "Do not store one-experiment-only logs here; keep them in that experiment folder first.",
        ],
    },
    "notes": {
        "path": "notes/",
        "purpose": "Store notes and reasoning around experiments.",
        "store": [
            "`ideas/`: new experiment ideas",
            "`interpretations/`: interpretation notes",
            "`decisions/`: accept / defer / reject decisions",
        ],
        "avoid": [
            "Do not keep polished formal reports here; use `reports/`.",
        ],
    },
    "publish": {
        "path": "publish/",
        "purpose": "Store materials near publication.",
        "store": [
            "`drafts/`: publication drafts",
            "`final/`: final shared versions",
            "`assets/`: attached assets such as images, tables, and appendices",
        ],
        "avoid": [
            "Do not mix experiment working notes into `publish/`.",
        ],
    },
    "reports": {
        "path": "reports/",
        "purpose": "Store formal reports and slide decks.",
        "store": [
            "`internal/`: internal reports",
            "`external/`: external-facing reports",
            "`slides/`: presentations",
        ],
        "avoid": [
            "Do not store source metrics here; use `results/`.",
        ],
    },
    "results": {
        "path": "results/",
        "purpose": "Store experiment results in raw and processed form.",
        "store": [
            "`raw/`: outputs before post-processing",
            "`processed/`: cleaned outputs",
            "`tables/`: table artifacts",
            "`figures/`: figures and visualizations",
        ],
        "avoid": [
            "Do not store config files or run scripts under `results/`.",
        ],
    },
    "scripts": {
        "path": "scripts/",
        "purpose": "Store experiment and workspace automation scripts.",
        "store": [
            "`expctl.py`: create, describe, validate, and move experiments",
            "`run/`: run scripts",
            "`collect/`: log/result collection scripts",
            "`analyze/`: analysis scripts",
            "`publish/`: publication prep scripts",
        ],
        "avoid": [
            "Put one-off experiment scripts inside that experiment's `scripts/` folder.",
        ],
    },
    "scratch": {
        "path": "scratch/",
        "purpose": "Store temporary outputs and one-off scratch material.",
        "store": [
            "deletable temporary files",
            "short-lived validation outputs",
        ],
        "avoid": [
            "Do not keep canonical reproducible results here.",
        ],
    },
    "templates": {
        "path": "templates/",
        "purpose": "Store reusable document and structure templates.",
        "store": [
            "`experiment_workflow_template.md`: planning-to-publish experiment template",
        ],
        "avoid": [
            "Do not store real experiment results inside a template.",
        ],
    },
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def default_workspace() -> Path:
    return Path(__file__).resolve().parent.parent


def slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "_", value.strip().lower()).strip("_")
    return slug or "experiment"


def today_utc() -> str:
    return datetime.now(timezone.utc).date().isoformat()


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
        root / "templates" / "experiment_workflow_template.md",
        root / "experiments",
        root / "configs",
        root / "logs",
        root / "results",
        root / "notes",
        root / "reports",
        root / "publish",
        root / "scripts",
        root / "scratch",
        root / "templates",
    ]
    for path in required_paths:
        if not path.exists():
            issues.append(f"missing workspace path: {path}")
    for status in VALID_STATUSES:
        status_dir = root / "experiments" / status
        if not status_dir.exists():
            issues.append(f"missing experiment status directory: {status_dir}")
    return issues


def iter_experiments(root: Path):
    experiments_root = root / "experiments"
    for status in VALID_STATUSES:
        status_dir = experiments_root / status
        if not status_dir.exists():
            continue
        for child in sorted(status_dir.iterdir()):
            if child.name.startswith(".") or not child.is_dir():
                continue
            yield child


def find_experiment(root: Path, token: str) -> Path:
    candidate_path = Path(token)
    if not candidate_path.is_absolute():
        candidate_path = (root / token).resolve()
    if candidate_path.exists() and (candidate_path / "experiment.json").exists():
        return candidate_path

    matches = []
    suffix = slugify(token)
    for exp_dir in iter_experiments(root):
        if exp_dir.name == token:
            matches.append(exp_dir)
        elif exp_dir.name == suffix:
            matches.append(exp_dir)
        elif exp_dir.name.endswith(f"_{suffix}"):
            matches.append(exp_dir)

    if not matches:
        raise SystemExit(f"experiment not found: {token}")
    if len(matches) > 1:
        joined = ", ".join(str(path.relative_to(root)) for path in matches)
        raise SystemExit(f"experiment reference is ambiguous: {token} -> {joined}")
    return matches[0]


def experiment_metadata(exp_dir: Path) -> dict:
    return load_json(exp_dir / "experiment.json")


def update_line_block(text: str, label: str, value: str) -> str:
    pattern = rf"^- {re.escape(label)}:.*$"
    replacement = f"- {label}: {value}"
    if re.search(pattern, text, flags=re.MULTILINE):
        return re.sub(pattern, replacement, text, flags=re.MULTILINE)
    return text


def apply_metadata_to_readme(text: str, metadata: dict, relative_dir: Path) -> str:
    relative_text = relative_dir.as_posix()
    replacements = {
        "Experiment ID": metadata["experiment_id"],
        "Title": metadata["title"],
        "Owner": metadata["owner"],
        "Date": metadata["date"],
        "Status": f"`{metadata['status']}`",
        "Priority": f"`{metadata['priority']}`",
        "Experiment root": relative_text,
        "Config path": f"{relative_text}/configs",
        "Log path": f"{relative_text}/logs",
        "Result path": f"{relative_text}/results",
        "Figure path": f"{relative_text}/figures",
        "Publish path": f"{relative_text}/publish",
    }
    for label, value in replacements.items():
        text = update_line_block(text, label, value)
    return text


def write_experiment_readme(root: Path, exp_dir: Path, metadata: dict, use_existing: bool) -> None:
    template_path = root / "templates" / "experiment_workflow_template.md"
    if use_existing and (exp_dir / "README.md").exists():
        readme_text = (exp_dir / "README.md").read_text(encoding="utf-8")
    else:
        readme_text = template_path.read_text(encoding="utf-8")
    relative_dir = exp_dir.relative_to(root)
    readme_text = apply_metadata_to_readme(readme_text, metadata, relative_dir)
    (exp_dir / "README.md").write_text(readme_text, encoding="utf-8")


def ensure_experiment_dirs(exp_dir: Path) -> None:
    exp_dir.mkdir(parents=True, exist_ok=True)
    for child in EXPERIMENT_CHILDREN:
        child_dir = exp_dir / child
        child_dir.mkdir(parents=True, exist_ok=True)
        gitkeep = child_dir / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.write_text("", encoding="utf-8")


def validate_experiment(root: Path, exp_dir: Path) -> list[str]:
    issues = []
    if exp_dir.parent.name not in VALID_STATUSES:
        issues.append(f"{exp_dir}: parent directory is not a valid status")
        return issues

    metadata_path = exp_dir / "experiment.json"
    if not metadata_path.exists():
        issues.append(f"{exp_dir}: missing experiment.json")
        return issues

    try:
        metadata = load_json(metadata_path)
    except json.JSONDecodeError as exc:
        issues.append(f"{exp_dir}: invalid experiment.json ({exc})")
        return issues

    required_fields = ("experiment_id", "title", "owner", "date", "status", "priority")
    for field in required_fields:
        if not metadata.get(field):
            issues.append(f"{exp_dir}: missing metadata field `{field}`")

    if metadata.get("status") != exp_dir.parent.name:
        issues.append(
            f"{exp_dir}: metadata status `{metadata.get('status')}` does not match parent directory `{exp_dir.parent.name}`"
        )
    if metadata.get("experiment_id") != exp_dir.name:
        issues.append(
            f"{exp_dir}: metadata experiment_id `{metadata.get('experiment_id')}` does not match directory name `{exp_dir.name}`"
        )
    if metadata.get("priority") and metadata["priority"] not in VALID_PRIORITIES:
        issues.append(f"{exp_dir}: invalid priority `{metadata['priority']}`")

    readme_path = exp_dir / "README.md"
    if not readme_path.exists():
        issues.append(f"{exp_dir}: missing README.md")
    else:
        readme_text = readme_path.read_text(encoding="utf-8")
        expected_status_line = f"- Status: `{exp_dir.parent.name}`"
        if re.search(r"^- Status:.*$", readme_text, flags=re.MULTILINE):
            actual_line = re.search(r"^- Status:.*$", readme_text, flags=re.MULTILINE).group(0)
            if actual_line != expected_status_line:
                issues.append(
                    f"{exp_dir}: README status line `{actual_line}` does not match expected `{expected_status_line}`"
                )
        relative_dir = exp_dir.relative_to(root).as_posix()
        expected_root_line = f"- Experiment root: {relative_dir}"
        if re.search(r"^- Experiment root:.*$", readme_text, flags=re.MULTILINE):
            actual_line = re.search(r"^- Experiment root:.*$", readme_text, flags=re.MULTILINE).group(0)
            if actual_line != expected_root_line:
                issues.append(
                    f"{exp_dir}: README experiment root line `{actual_line}` does not match expected `{expected_root_line}`"
                )

    for child in EXPERIMENT_CHILDREN:
        if not (exp_dir / child).is_dir():
            issues.append(f"{exp_dir}: missing required directory `{child}/`")
    return issues


def cmd_tree(args: argparse.Namespace) -> int:
    print(args.workspace)
    for top_level, description, children in TOP_LEVEL_TREE:
        print(f"- {top_level:<13} {description}")
        for child, child_description in children:
            print(f"  - {child:<11} {child_description}")
    return 0


def resolve_guide_key(root: Path, target: str | None) -> str:
    if not target:
        return "root"
    cleaned = target.strip().strip("/")
    if cleaned in GUIDE:
        return cleaned

    target_path = Path(cleaned)
    if not target_path.is_absolute():
        target_path = (root / cleaned).resolve()
    try:
        relative = target_path.relative_to(root).as_posix().strip("/")
    except ValueError:
        relative = cleaned
    if relative in GUIDE:
        return relative
    raise SystemExit(f"unknown guide target: {target}")


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


def build_metadata(args: argparse.Namespace, experiment_id: str) -> dict:
    return {
        "experiment_id": experiment_id,
        "title": args.title or experiment_id,
        "owner": args.owner or "unassigned",
        "date": args.date,
        "status": args.status,
        "priority": args.priority,
        "created_at": utc_now(),
        "updated_at": utc_now(),
        "tags": [],
    }


def cmd_init(args: argparse.Namespace) -> int:
    date_prefix = args.date
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_prefix):
        raise SystemExit("--date must be in YYYY-MM-DD format")

    experiment_id = f"{date_prefix}_{slugify(args.name)}"
    exp_dir = args.workspace / "experiments" / args.status / experiment_id
    if exp_dir.exists() and not args.force:
        raise SystemExit(f"experiment already exists: {exp_dir}")

    if args.dry_run:
        print(exp_dir)
        return 0

    ensure_experiment_dirs(exp_dir)
    metadata = build_metadata(args, experiment_id)
    dump_json(exp_dir / "experiment.json", metadata)
    write_experiment_readme(args.workspace, exp_dir, metadata, use_existing=False)
    print(exp_dir.relative_to(args.workspace))
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    results = []
    for exp_dir in iter_experiments(args.workspace):
        status = exp_dir.parent.name
        if args.status and status != args.status:
            continue
        metadata_path = exp_dir / "experiment.json"
        title = exp_dir.name
        owner = "unknown"
        priority = "unknown"
        if metadata_path.exists():
            metadata = load_json(metadata_path)
            title = metadata.get("title", title)
            owner = metadata.get("owner", owner)
            priority = metadata.get("priority", priority)
        results.append(
            {
                "id": exp_dir.name,
                "status": status,
                "owner": owner,
                "priority": priority,
                "title": title,
                "path": exp_dir.relative_to(args.workspace).as_posix(),
            }
        )

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return 0

    if not results:
        print("no experiments found")
        return 0

    for item in results:
        print(
            f"{item['status']:<10} {item['priority']:<6} {item['owner']:<12} "
            f"{item['id']:<32} {item['title']}"
        )
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    issues = require_workspace(args.workspace)
    if args.all:
        targets = list(iter_experiments(args.workspace))
    elif args.target:
        targets = [find_experiment(args.workspace, args.target)]
    else:
        targets = []

    seen_ids: set[str] = set()
    for exp_dir in targets:
        if exp_dir.name in seen_ids:
            issues.append(f"duplicate experiment directory name detected: {exp_dir.name}")
        seen_ids.add(exp_dir.name)
        issues.extend(validate_experiment(args.workspace, exp_dir))

    if issues:
        print("validation failed")
        for issue in issues:
            print(f"- {issue}")
        return 1

    if args.all:
        print(f"validation passed for workspace and {len(targets)} experiment(s)")
    elif args.target:
        print(f"validation passed for {targets[0].relative_to(args.workspace)}")
    else:
        print("workspace structure looks valid")
    return 0


def cmd_move(args: argparse.Namespace) -> int:
    exp_dir = find_experiment(args.workspace, args.experiment)
    metadata = experiment_metadata(exp_dir)
    target_dir = args.workspace / "experiments" / args.status / exp_dir.name
    if exp_dir == target_dir:
        print(exp_dir.relative_to(args.workspace))
        return 0
    if target_dir.exists():
        raise SystemExit(f"target experiment directory already exists: {target_dir}")

    shutil.move(str(exp_dir), str(target_dir))
    metadata["status"] = args.status
    metadata["updated_at"] = utc_now()
    dump_json(target_dir / "experiment.json", metadata)
    write_experiment_readme(args.workspace, target_dir, metadata, use_existing=True)
    print(target_dir.relative_to(args.workspace))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manage the experiment workspace structure and experiment lifecycle."
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        default=default_workspace(),
        help="workspace root path (default: script parent)",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    tree_parser = subparsers.add_parser("tree", help="print the workspace tree with short descriptions")
    tree_parser.set_defaults(func=cmd_tree)

    guide_parser = subparsers.add_parser("guide", help="print guidance for a folder")
    guide_parser.add_argument("target", nargs="?", help="folder name or path, for example `experiments`")
    guide_parser.set_defaults(func=cmd_guide)

    init_parser = subparsers.add_parser("init", help="create a new experiment scaffold")
    init_parser.add_argument("name", help="experiment slug or short name")
    init_parser.add_argument("--title", help="human-readable experiment title")
    init_parser.add_argument("--owner", help="owner name")
    init_parser.add_argument("--date", default=today_utc(), help="date prefix in YYYY-MM-DD format")
    init_parser.add_argument("--status", choices=VALID_STATUSES, default="planned")
    init_parser.add_argument("--priority", choices=VALID_PRIORITIES, default="medium")
    init_parser.add_argument("--dry-run", action="store_true", help="print the target path without creating files")
    init_parser.add_argument("--force", action="store_true", help="overwrite an existing experiment directory")
    init_parser.set_defaults(func=cmd_init)

    list_parser = subparsers.add_parser("list", help="list experiments")
    list_parser.add_argument("--status", choices=VALID_STATUSES, help="filter by status")
    list_parser.add_argument("--json", action="store_true", help="print machine-readable JSON")
    list_parser.set_defaults(func=cmd_list)

    validate_parser = subparsers.add_parser("validate", help="validate workspace or experiment structure")
    validate_parser.add_argument("target", nargs="?", help="experiment path or experiment id")
    validate_parser.add_argument("--all", action="store_true", help="validate all experiments in the workspace")
    validate_parser.set_defaults(func=cmd_validate)

    move_parser = subparsers.add_parser("move", help="move an experiment to another lifecycle state")
    move_parser.add_argument("experiment", help="experiment path, id, or unique slug")
    move_parser.add_argument("status", choices=VALID_STATUSES, help="target lifecycle state")
    move_parser.set_defaults(func=cmd_move)

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
