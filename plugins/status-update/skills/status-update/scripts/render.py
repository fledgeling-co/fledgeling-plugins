#!/usr/bin/env python3
"""Render status reports from data, and keep the portfolio dashboard in step.

One project writes one file — .status/project.json — and everything else is derived:
its own STATUS.html, its row in ~/Dev/.status/portfolio.json, and ~/Dev/STATUS.html.
Deriving the dashboard row rather than asking anyone to write it twice is what stops
the two files disagreeing.

  render.py project   <project-dir>   rebuild that project's STATUS.html
  render.py sync      <project-dir>   the above, then merge its row and rebuild the dashboard
  render.py portfolio                 rebuild ~/Dev/STATUS.html from portfolio.json
  render.py rebuild                   rescan every ~/Dev project for .status/project.json
  render.py validate  <json-file>      check a data file against the contract
  render.py --self-test                prove the checks can fail

Exit codes: 0 ok · 1 invalid data · 2 missing file · 3 self-test failure.
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
ASSETS = SKILL_DIR / "assets"
DEV = Path(os.environ.get("STATUS_DEV_ROOT", Path.home() / "Dev"))

DATA_BLOCK = re.compile(
    r'(<script[^>]*type="application/json"[^>]*id="report-data"[^>]*>)(.*?)(</script>)',
    re.S,
)

# The six columns of the dashboard heatmap. A project's checks are grouped into these
# so every project contributes the same number of cells and the grid stays rectangular.
GATE_KINDS = ["build", "tests", "types", "security", "design", "sign-off"]
KIND_HINTS = {
    "build": ("build", "compile", "bundle", "turbo"),
    "tests": ("test", "spec", "suite", "e2e", "vitest", "jest", "pytest"),
    "types": ("type", "tsc", "typecheck", "mypy"),
    "security": ("security", "audit", "vuln", "secret", "licence", "license"),
    "design": ("design", "visual", "contrast", "a11y", "accessib", "lint", "ux"),
    "sign-off": ("sign", "review", "approve", "verify", "acceptance"),
}

STATES = ["done", "in-flight", "needs-work", "blocked", "unmeasured", "waived"]
# Worst-first: when several checks collapse into one heatmap cell, the worst one shows.
SEVERITY = {"needs-work": 0, "blocked": 1, "unmeasured": 2, "in-flight": 3, "waived": 4, "done": 5}


class DataError(Exception):
    pass


# --------------------------------------------------------------------------- validate

def _require(cond, msg):
    if not cond:
        raise DataError(msg)


def validate_project(d: dict) -> list[str]:
    """Return warnings; raise DataError on anything that would render wrongly."""
    warn = []
    _require(isinstance(d, dict), "project.json must be a JSON object")
    _require(d.get("project"), 'missing "project" (the project name)')
    _require(d.get("updated"), 'missing "updated" (ISO-8601 timestamp)')
    v = d.get("verdict") or {}
    _require(isinstance(v, dict) and v.get("token"), 'missing "verdict.token"')
    _require(v["token"] in STATES, f'verdict.token "{v["token"]}" is not one of {STATES}')

    for key in ("tasks", "gates", "armed", "findings", "corrections", "coverage",
                "not_checked", "not_done", "artifacts", "needs_you", "remaining", "roadmap"):
        if key in d and not isinstance(d[key], list):
            raise DataError(f'"{key}" must be a list')

    if "estimate_remaining" in d and not isinstance(d["estimate_remaining"], dict):
        raise DataError('"estimate_remaining" must be a JSON object')

    for i, rd in enumerate(d.get("roadmap", [])):
        if not isinstance(rd, dict):
            raise DataError(f"roadmap[{i}] must be an object")
        if not rd.get("round") or not rd.get("goal"):
            raise DataError(f'roadmap[{i}] missing "round" or "goal"')
        if "estimate_min" in rd and isinstance(rd["estimate_min"], list):
            if len(rd["estimate_min"]) != 2:
                warn.append(f'roadmap[{i}].estimate_min should be a [low, high] range, not a single point')

    for i, g in enumerate(d.get("gates", [])):
        if g.get("state") not in STATES:
            raise DataError(f'gates[{i}].state "{g.get("state")}" is not one of {STATES}')
        # A check that examined nothing is not a pass. The corpus carries this exact
        # error being retracted later, so it is corrected here rather than trusted.
        if g.get("state") == "done" and _examined_nothing(g.get("counts")):
            warn.append(f'gates[{i}] "{g.get("name")}" claims done over a zero count '
                        f'({g.get("counts")!r}) — forced to unmeasured')
            g["state"] = "unmeasured"

    for i, a in enumerate(d.get("armed", [])):
        # An alarm that caught nothing when the code was deliberately broken is not armed,
        # whatever the file says.
        if a.get("armed") and int(a.get("red") or 0) == 0:
            warn.append(f'armed[{i}] "{a.get("check")}" claims armed with red=0 — forced to false')
            a["armed"] = False

    for i, c in enumerate(d.get("coverage", [])):
        den = c.get("denominator")
        if den in (None, 0):
            warn.append(f'coverage[{i}] "{c.get("axis")}" has no denominator — '
                        f'shown as undeclared, never as covered')
    return warn


def _examined_nothing(counts) -> bool:
    if counts in (None, "", "0", 0):
        return True
    m = re.match(r"^\s*(\d+)\s*/\s*(\d+)\s*$", str(counts))
    return bool(m) and int(m.group(2)) == 0


def validate_portfolio(d: dict) -> list[str]:
    _require(isinstance(d, dict), "portfolio.json must be a JSON object")
    _require(isinstance(d.get("projects"), list), 'missing "projects" list')
    return []


# --------------------------------------------------------------------------- derive

def gate_kind(g: dict) -> str:
    if g.get("kind") in GATE_KINDS:
        return g["kind"]
    hay = f"{g.get('name','')} {g.get('command','')}".lower()
    for kind, hints in KIND_HINTS.items():
        if any(h in hay for h in hints):
            return kind
    return "build"


def derive_row(p: dict) -> dict:
    """Build one dashboard row from a project's own data.

    Nobody writes this by hand. That is the point: a row and a report that are
    written separately drift, and the drift is invisible until someone reads both.
    """
    tasks = p.get("tasks", [])
    done = sum(1 for t in tasks if t.get("outcome") == "done")

    by_kind: dict[str, str] = {}
    for g in p.get("gates", []):
        k = gate_kind(g)
        s = g.get("state", "unmeasured")
        if k not in by_kind or SEVERITY[s] < SEVERITY[by_kind[k]]:
            by_kind[k] = s
    gates = [{"name": k, "state": by_kind.get(k, "unmeasured")} for k in GATE_KINDS]

    cov = p.get("coverage", [])
    covered = sum(int(c.get("covered") or 0) for c in cov if c.get("denominator"))
    denom = sum(int(c.get("denominator") or 0) for c in cov if c.get("denominator"))

    stuck = [t for t in tasks if t.get("outcome") == "stuck"]

    next_rd = None
    for rd in p.get("roadmap", []):
        if rd.get("status") in ("next", "queued"):
            est_str = ""
            if rd.get("estimate_min"):
                lo, hi = rd["estimate_min"]
                est_str = f"{lo}–{hi}m" if hi < 60 else f"{lo}m–{hi/60:.1f}h"
            next_rd = {
                "round": rd.get("round", ""),
                "goal": rd.get("goal", ""),
                "tier": rd.get("tier", "M"),
                "estimate": est_str,
                "status": rd.get("status", "next"),
            }
            break

    time_rem = ""
    er = p.get("estimate_remaining") or {}
    if er.get("parallel_min"):
        plo, phi = er["parallel_min"]
        if phi < 60:
            time_rem = f"{plo}–{phi}m"
        else:
            time_rem = f"{plo}m–{phi/60:.1f}h" if plo < 60 else f"{plo/60:.1f}–{phi/60:.1f}h"
    elif er.get("median_min"):
        med = er["median_min"]
        time_rem = f"~{med}m" if med < 60 else f"~{med/60:.1f}h"

    return {
        "project": p["project"],
        "updated": p["updated"],
        "verdict": {"token": p["verdict"]["token"], "number": p["verdict"].get("number", "")},
        "gates": gates,
        "done_of_total": {"done": done, "total": len(tasks)},
        "defects_open": sum(1 for f in p.get("findings", []) if f.get("state") != "done"),
        "corrections": p.get("corrections", []),
        "remaining": [
            {"id": t.get("id"), "title": t.get("title"),
             "blocked_on": t.get("blocked_by") or t.get("note") or "",
             "waiting_hours": t.get("waiting_hours")}
            for t in stuck
        ],
        "needs_you": p.get("needs_you", []),
        "coverage": ([{"axis": "work watched by tests",
                       "covered": covered, "denominator": denom}] if denom else []),
        "next_round": next_rd,
        "time_remaining": time_rem,
    }


# --------------------------------------------------------------------------- render

def inject(template: Path, data: dict, out: Path) -> Path:
    if not template.exists():
        raise DataError(f"template missing: {template}")
    html = template.read_text(encoding="utf-8")
    if not DATA_BLOCK.search(html):
        raise DataError(f'no <script id="report-data"> block in {template}')
    payload = json.dumps(data, indent=1, ensure_ascii=False)
    # </script> inside a string would close the block early.
    payload = payload.replace("</", "<\\/")
    html = DATA_BLOCK.sub(lambda m: m.group(1) + "\n" + payload + "\n" + m.group(3), html, count=1)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    return out


def read_json(p: Path) -> dict:
    if not p.exists():
        print(f"missing: {p}", file=sys.stderr)
        sys.exit(2)
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"{p}: invalid JSON — {e}", file=sys.stderr)
        sys.exit(1)


def project_paths(d: str):
    root = Path(d).resolve()
    return root, root / ".status" / "project.json", root / "STATUS.html"


def cmd_project(d: str, quiet=False) -> dict:
    root, data_p, out_p = project_paths(d)
    data = read_json(data_p)
    for w in validate_project(data):
        print(f"  corrected: {w}", file=sys.stderr)
    inject(ASSETS / "project-template.html", data, out_p)
    if not quiet:
        print(out_p)
    return data


def cmd_portfolio(quiet=False) -> Path:
    pf = read_json(DEV / ".status" / "portfolio.json")
    validate_portfolio(pf)
    pf["projects"] = sorted(pf["projects"], key=lambda r: r.get("project", ""))
    out = inject(ASSETS / "dashboard-template.html", pf, DEV / "STATUS.html")
    if not quiet:
        print(out)
    return out


def cmd_sync(d: str):
    data = cmd_project(d, quiet=True)
    row = derive_row(data)

    pf_path = DEV / ".status" / "portfolio.json"
    pf = json.loads(pf_path.read_text(encoding="utf-8")) if pf_path.exists() else {}
    pf.setdefault("projects", [])
    pf.setdefault("machine", {})
    pf.setdefault("flight", {})
    pf["updated"] = datetime.now(timezone.utc).isoformat(timespec="seconds")

    others = [r for r in pf["projects"] if r.get("project") != row["project"]]
    replaced = len(others) != len(pf["projects"])
    pf["projects"] = sorted(others + [row], key=lambda r: r.get("project", ""))

    pf_path.parent.mkdir(parents=True, exist_ok=True)
    pf_path.write_text(json.dumps(pf, indent=1, ensure_ascii=False), encoding="utf-8")

    _, _, out_p = project_paths(d)
    print(out_p)
    print(cmd_portfolio(quiet=True))
    print(f"{row['project']}: row {'updated' if replaced else 'added'} "
          f"({len(pf['projects'])} projects on the dashboard)")


def cmd_rebuild():
    """Rescan every ~/Dev project. The recovery path when portfolio.json is lost."""
    pf_path = DEV / ".status" / "portfolio.json"
    pf = json.loads(pf_path.read_text(encoding="utf-8")) if pf_path.exists() else {}
    pf.setdefault("machine", {})
    pf.setdefault("flight", {})
    rows, skipped = [], []
    for cand in sorted(DEV.iterdir()):
        f = cand / ".status" / "project.json"
        if not (cand.is_dir() and f.exists()):
            continue
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            validate_project(data)
            rows.append(derive_row(data))
        except (DataError, json.JSONDecodeError) as e:
            skipped.append(f"{cand.name}: {e}")
    pf["projects"] = sorted(rows, key=lambda r: r["project"])
    pf["updated"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    pf_path.parent.mkdir(parents=True, exist_ok=True)
    pf_path.write_text(json.dumps(pf, indent=1, ensure_ascii=False), encoding="utf-8")
    print(cmd_portfolio(quiet=True))
    print(f"rebuilt from {len(rows)} projects")
    for s in skipped:
        print(f"  skipped {s}", file=sys.stderr)


def cmd_validate(f: str):
    data = read_json(Path(f))
    try:
        warns = validate_portfolio(data) if "projects" in data else validate_project(data)
    except DataError as e:
        print(f"INVALID: {e}", file=sys.stderr)
        sys.exit(1)
    for w in warns:
        print(f"corrected: {w}")
    print(f"valid — {len(warns)} correction(s)")


# --------------------------------------------------------------------------- self-test

def self_test() -> int:
    """Each case proves one check can actually fail. A gate that cannot fail is not a gate."""
    cases, failed = [], 0

    def check(name, fn, want_raise):
        nonlocal failed
        try:
            fn()
            ok = not want_raise
        except DataError:
            ok = want_raise
        cases.append((name, ok))
        if not ok:
            failed += 1

    good = {"project": "p", "updated": "2026-01-01T00:00:00Z",
            "verdict": {"token": "done", "number": "1 of 1"}}
    check("a well-formed file passes", lambda: validate_project(dict(good)), False)
    check("a missing project name fails",
          lambda: validate_project({"updated": "x", "verdict": {"token": "done"}}), True)
    check("an unknown state word fails",
          lambda: validate_project({**good, "verdict": {"token": "green"}}), True)
    check("a non-list tasks field fails", lambda: validate_project({**good, "tasks": {}}), True)
    check("an unknown check state fails",
          lambda: validate_project({**good, "gates": [{"name": "g", "state": "ok"}]}), True)

    d = {**good, "gates": [{"name": "acceptance", "counts": "0/0", "state": "done"}]}
    validate_project(d)
    passed = d["gates"][0]["state"] == "unmeasured"
    cases.append(("a check over zero counts is forced to unmeasured", passed))
    failed += not passed

    d = {**good, "armed": [{"check": "c", "red": 0, "green": 9, "armed": True}]}
    validate_project(d)
    passed = d["armed"][0]["armed"] is False
    cases.append(("an alarm that caught nothing is forced to unarmed", passed))
    failed += not passed

    check("an invalid roadmap item fails",
          lambda: validate_project({**good, "roadmap": [{"round": "R1"}]}), True)
    check("a non-object estimate_remaining fails",
          lambda: validate_project({**good, "estimate_remaining": "5 hours"}), True)

    row = derive_row({**good, "tasks": [{"outcome": "done"}, {"outcome": "stuck"}],
                      "findings": [{"state": "needs-work"}, {"state": "done"}],
                      "gates": [{"name": "pnpm test", "state": "needs-work"},
                                {"name": "tsc", "state": "done"}],
                      "roadmap": [{"round": "Round 2", "goal": "Next wave", "status": "next",
                                   "estimate_min": [20, 50]}],
                      "estimate_remaining": {"parallel_min": [30, 90], "median_min": 45}})
    ok = (row["done_of_total"] == {"done": 1, "total": 2}
          and row["defects_open"] == 1
          and len(row["gates"]) == len(GATE_KINDS)
          and dict((g["name"], g["state"]) for g in row["gates"])["tests"] == "needs-work"
          and dict((g["name"], g["state"]) for g in row["gates"])["design"] == "unmeasured"
          and row["next_round"]["round"] == "Round 2"
          and "–" in row["time_remaining"])
    cases.append(("a dashboard row derives next round and time range", ok))
    failed += not ok

    for t in (ASSETS / "project-template.html", ASSETS / "dashboard-template.html"):
        ok = t.exists() and bool(DATA_BLOCK.search(t.read_text(encoding="utf-8")))
        cases.append((f"{t.name} has a data block", ok))
        failed += not ok

    width = max(len(n) for n, _ in cases)
    for n, ok in cases:
        print(f"  {'pass' if ok else 'FAIL'}  {n:<{width}}")
    print(f"\n{len(cases) - failed} of {len(cases)} checks passed")
    return 3 if failed else 0


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if a[0] == "--self-test":
        return self_test()
    try:
        if a[0] == "project" and len(a) > 1:
            cmd_project(a[1])
        elif a[0] == "sync" and len(a) > 1:
            cmd_sync(a[1])
        elif a[0] == "portfolio":
            cmd_portfolio()
        elif a[0] == "rebuild":
            cmd_rebuild()
        elif a[0] == "validate" and len(a) > 1:
            cmd_validate(a[1])
        else:
            print(__doc__)
            return 1
    except DataError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
