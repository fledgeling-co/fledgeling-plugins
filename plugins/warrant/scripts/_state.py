"""State resolution for the warrant plugin.

One place decides where state lives and what it means for a precondition to be
absent, so no script invents a second answer. See references/script-contract.md.
"""

from __future__ import annotations

import json
import pathlib
import tomllib
from typing import Any


class Absent(FileNotFoundError):
    """A precondition is missing. Callers surface this as exit 3."""


def state_dir(root: str | pathlib.Path, create: bool = False) -> pathlib.Path:
    d = pathlib.Path(root).expanduser().resolve() / ".warrant"
    if create:
        d.mkdir(parents=True, exist_ok=True)
        (d / "regression").mkdir(exist_ok=True)
        (d / "reports").mkdir(exist_ok=True)
    return d


def warrant_path(root: str | pathlib.Path) -> pathlib.Path:
    return state_dir(root) / "warrant.toml"


def lanes_path(root: str | pathlib.Path) -> pathlib.Path:
    return state_dir(root) / "lanes.toml"


def read_toml(path: pathlib.Path) -> dict[str, Any]:
    if not path.exists():
        raise Absent(str(path))
    with path.open("rb") as fh:
        return tomllib.load(fh)


def read_warrant(root: str | pathlib.Path) -> dict[str, Any]:
    """The warrant, or Absent. Every script that acts on authority reads this."""
    return read_toml(warrant_path(root))


def read_lanes(root: str | pathlib.Path) -> dict[str, Any]:
    return read_toml(lanes_path(root))


def read_json(path: pathlib.Path, default: Any = None) -> Any:
    if not path.exists():
        if default is not None:
            return default
        raise Absent(str(path))
    return json.loads(path.read_text())


def write_json(path: pathlib.Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=1, sort_keys=True) + "\n")
    tmp.replace(path)


def append_jsonl(path: pathlib.Path, row: dict[str, Any]) -> None:
    """Append one row. Append-only by contract: nothing here rewrites a file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as fh:
        fh.write(json.dumps(row, sort_keys=True) + "\n")


def read_jsonl(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            # A malformed line is data about the file, not a reason to lose the
            # rest of it. Callers that care report the count.
            rows.append({"_malformed": line[:200]})
    return rows


def tier_of(warrant: dict[str, Any], defect_class: str) -> int:
    """The tier a class currently holds, or 0 when the warrant does not name it.

    Defaulting an unnamed class to 0 rather than to the warrant's top tier is
    the whole safety property: a class nobody wrote down is a class no machine
    may close.
    """
    for entry in warrant.get("classes", []):
        if entry.get("name") == defect_class:
            return int(entry.get("tier", 0))
    return 0


def toml_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def toml_kv(key: str, value: Any) -> str:
    """Serialise one key. Deliberately narrow: this plugin only ever writes the
    fixed warrant schema, so arbitrary data is out of scope."""
    if isinstance(value, bool):
        return f"{key} = {'true' if value else 'false'}"
    if isinstance(value, (int, float)):
        return f"{key} = {value}"
    if isinstance(value, list):
        inner = ", ".join(f'"{toml_escape(str(v))}"' for v in value)
        return f"{key} = [{inner}]"
    return f'{key} = "{toml_escape(str(value))}"'
