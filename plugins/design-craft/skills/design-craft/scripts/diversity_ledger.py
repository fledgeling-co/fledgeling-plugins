#!/usr/bin/env python3
"""Track recent design decisions so consecutive commissions can rotate."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1
DEFAULT_MAX_ENTRIES = 5
FIELDS = (
    "family",
    "display_face",
    "pairing",
    "topology",
    "signature",
    "palette_family",
    "motion",
    "flow_shape",
)


def empty_ledger() -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "max_entries": DEFAULT_MAX_ENTRIES,
        "entries": [],
    }


def load(path: Path) -> dict[str, Any]:
    if not path.exists():
        return empty_ledger()
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"cannot read diversity ledger {path}: {exc}")
    if not isinstance(data, dict) or not isinstance(data.get("entries", []), list):
        raise SystemExit(f"invalid diversity ledger shape: {path}")
    data.setdefault("schema_version", SCHEMA_VERSION)
    data.setdefault("max_entries", DEFAULT_MAX_ENTRIES)
    return data


def save(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def values_from(args: argparse.Namespace) -> dict[str, str]:
    values: dict[str, str] = {}
    for field in FIELDS:
        value = getattr(args, field, None)
        if value:
            values[field] = value
    return values


def cmd_init(path: Path) -> int:
    if path.exists():
        print(f"already exists: {path}")
        return 0
    save(path, empty_ledger())
    print(f"created: {path}")
    return 0


def cmd_show(path: Path) -> int:
    data = load(path)
    if not path.exists():
        print(f"history=unavailable path={path}")
        return 0
    print(json.dumps(data, indent=2, sort_keys=True))
    return 0


def cmd_check(path: Path, args: argparse.Namespace) -> int:
    data = load(path)
    entries = [entry for entry in data.get("entries", []) if entry.get("kind") == args.kind]
    print(f"ledger={path}")
    print(f"kind={args.kind} history_entries={len(entries)}")
    if not entries:
        print("history=unavailable-for-kind")
        return 0

    requested = values_from(args)
    conflicts: list[tuple[str, str, str]] = []
    for field, value in requested.items():
        matching = [entry for entry in entries if entry.get(field) == value]
        if matching:
            latest = matching[-1]
            conflicts.append((field, value, str(latest.get("artifact", "unknown"))))

    if not conflicts:
        print("rotation=available")
        return 0

    print("rotation=conflict")
    for field, value, artifact in conflicts:
        print(f"conflict={field}:{value} last_artifact={artifact}")
    return 1


def cmd_record(path: Path, args: argparse.Namespace) -> int:
    data = load(path)
    entry: dict[str, Any] = {
        "date": args.date or date.today().isoformat(),
        "kind": args.kind,
        "artifact": args.artifact,
    }
    entry.update(values_from(args))
    if args.note:
        entry["note"] = args.note
    entries = [item for item in data.get("entries", []) if isinstance(item, dict)]
    entries.append(entry)
    limit = max(1, int(data.get("max_entries", DEFAULT_MAX_ENTRIES)))
    data["entries"] = entries[-limit:]
    save(path, data)
    print(f"recorded={args.artifact} kind={args.kind} retained={len(data['entries'])}")
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    sub = root.add_subparsers(dest="command", required=True)

    for name, help_text in (
        ("init", "create an empty ledger"),
        ("show", "print the ledger"),
    ):
        command = sub.add_parser(name, help=help_text)
        command.add_argument("path", type=Path)

    check = sub.add_parser("check", help="check proposed values against recent entries")
    check.add_argument("path", type=Path)
    check.add_argument("--kind", required=True)
    add_value_args(check)

    record = sub.add_parser("record", help="append a completed commission")
    record.add_argument("path", type=Path)
    record.add_argument("--kind", required=True)
    record.add_argument("--artifact", required=True)
    record.add_argument("--date")
    record.add_argument("--note")
    add_value_args(record)
    return root


def add_value_args(command: argparse.ArgumentParser) -> None:
    for field in FIELDS:
        command.add_argument(f"--{field.replace('_', '-')}")


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.command == "init":
        return cmd_init(args.path)
    if args.command == "show":
        return cmd_show(args.path)
    if args.command == "check":
        return cmd_check(args.path, args)
    if args.command == "record":
        return cmd_record(args.path, args)
    return 2


if __name__ == "__main__":
    sys.exit(main())
