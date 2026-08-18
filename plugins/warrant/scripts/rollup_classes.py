#!/usr/bin/env python3
"""Roll per-surface and per-target measurements up into per-defect-class answers.

This step exists because the producing planes and the consuming ones key their
state differently, and both are right to. `oracle` measures a surface, `assay`
measures a test target, and authority is held per defect class -- so something has
to map one onto the other, using the class-to-surface globs the warrant declares.

Without it the planes cannot talk: `charter_validate.py` and `ratchet.py` read
`{"classes": {...}}` while `lineage_gate.py` writes `{"surfaces": [...]}`, and a
class with no rollup reads as a class with no evidence. That is a safe failure
(the tier is refused) but a useless one, because nothing can ever be earned.

Run it after `oracle` and `assay`, before `ratchet`. See
references/script-contract.md for the state layout.
"""

from __future__ import annotations

import argparse
import fnmatch
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import _cli
import _state


def _classes(warrant: dict) -> list[dict]:
    return [c for c in warrant.get("classes", []) if isinstance(c, dict) and c.get("name")]


def _matches(path: str, globs: list[str]) -> bool:
    """A surface belongs to a class when it matches one of the class's globs.

    fnmatch treats `*` as crossing separators, which is what a `**/*.html` glob
    means to a reader, so the two agree closely enough for this purpose.
    """
    p = path.replace("\\", "/")
    return any(fnmatch.fnmatch(p, g) or fnmatch.fnmatch(pathlib.PurePath(p).name, g)
               for g in globs)


def rollup_oracle(warrant: dict, coverage: dict) -> dict:
    """Per-class coverage from per-surface rows, plus the class's own threshold."""
    surfaces = coverage.get("surfaces") or []
    out: dict[str, dict] = {}
    for cls in _classes(warrant):
        name = str(cls["name"])
        globs = [str(g) for g in (cls.get("surfaces") or [])]
        rows = [s for s in surfaces if _matches(str(s.get("file", "")), globs)] if globs else []
        figures = sum(int(s.get("figures", 0)) for s in rows)
        sourced = sum(int(s.get("sourced", 0)) for s in rows)
        gaps = sum(int(s.get("unsourced", 0)) for s in rows)
        threshold = float(cls.get("oracle_coverage_min", 1.0))
        cov = (sourced / figures) if figures else 0.0
        out[name] = {
            "total": figures,
            "covered": sourced,
            "coverage": round(cov, 4),
            "lineage_gaps": gaps,
            "surfaces_matched": len(rows),
            "threshold": threshold,
            # No matched surface means no evidence, which is not the same as a
            # pass. A class with nothing measured must not clear its threshold.
            "green": bool(rows) and gaps == 0 and cov >= threshold,
        }
    return out


def rollup_assay(warrant: dict, suite: dict) -> tuple[dict, bool]:
    """Per-class assay state, and the single `green` flag charter_validate reads."""
    mutation = suite.get("mutation") if isinstance(suite.get("mutation"), dict) else {}
    score = mutation.get("score")
    mark = mutation.get("high_water")
    measured = isinstance(score, (int, float))
    holding = measured and (mark is None or float(score) >= float(mark))
    out: dict[str, dict] = {}
    for cls in _classes(warrant):
        out[str(cls["name"])] = {
            "mutation_score": score if measured else None,
            "high_water": mark,
            "measured": measured,
            "green": bool(holding),
        }
    return out, bool(holding)


def main(args: argparse.Namespace) -> int:
    warrant = _state.read_warrant(args.root)
    d = _state.state_dir(args.root, create=True)

    cov_path = d / "oracle-coverage.json"
    suite_path = d / "suite-health.json"
    wrote = []

    if cov_path.exists():
        cov = _state.read_json(cov_path)
        cov["classes"] = rollup_oracle(warrant, cov)
        _state.write_json(cov_path, cov)
        wrote.append("oracle-coverage.json")
        for name, row in sorted(cov["classes"].items()):
            _cli.say(args, f"  {'green' if row['green'] else 'NOT green':<10} {name:<22} "
                           f"{_cli.rate(row['covered'], row['total'], 'figures sourced')}"
                           f", threshold {row['threshold']:.2f}, {row['surfaces_matched']} surface(s)")
    else:
        _cli.say(args, "  no oracle-coverage.json yet; run warrant:oracle first")

    if suite_path.exists():
        suite = _state.read_json(suite_path)
        classes, green = rollup_assay(warrant, suite)
        suite["classes"] = classes
        suite["green"] = green
        _state.write_json(suite_path, suite)
        wrote.append("suite-health.json")
        _cli.say(args, f"  assay green: {green}")
    else:
        _cli.say(args, "  no suite-health.json yet; run warrant:assay first")

    _cli.emit(args, {"rolled_up": wrote})
    if not wrote:
        return _cli.MISSING
    return _cli.OK


def selftest() -> list[tuple[str, bool]]:
    cases: list[tuple[str, bool]] = []
    w = {"classes": [
        {"name": "figure-lineage", "surfaces": ["**/*.html"], "oracle_coverage_min": 0.95},
        {"name": "layout-drift", "surfaces": ["**/*.tsx"], "oracle_coverage_min": 0.90},
        {"name": "unmapped", "surfaces": []},
    ]}
    cov = {"surfaces": [
        {"file": "a/b/page.html", "figures": 100, "sourced": 100, "unsourced": 0},
        {"file": "a/c/other.html", "figures": 100, "sourced": 90, "unsourced": 10},
        {"file": "a/d/view.tsx", "figures": 10, "sourced": 10, "unsourced": 0},
    ]}
    r = rollup_oracle(w, cov)
    cases.append(("html surfaces roll into figure-lineage", r["figure-lineage"]["total"] == 200))
    cases.append(("coverage is the ratio", r["figure-lineage"]["coverage"] == 0.95))
    cases.append(("a lineage gap withholds green", r["figure-lineage"]["green"] is False))
    cases.append(("tsx surface rolls into layout-drift", r["layout-drift"]["total"] == 10))
    cases.append(("a clean class is green", r["layout-drift"]["green"] is True))
    cases.append(("a class with no matched surface is not green", r["unmapped"]["green"] is False))
    cases.append(("a class with no matched surface reports zero coverage",
                  r["unmapped"]["coverage"] == 0.0))

    below = rollup_oracle({"classes": [{"name": "x", "surfaces": ["*.html"],
                                        "oracle_coverage_min": 0.99}]},
                          {"surfaces": [{"file": "p.html", "figures": 100, "sourced": 98,
                                         "unsourced": 0}]})
    cases.append(("coverage below the threshold withholds green", below["x"]["green"] is False))
    at = rollup_oracle({"classes": [{"name": "x", "surfaces": ["*.html"],
                                     "oracle_coverage_min": 0.98}]},
                       {"surfaces": [{"file": "p.html", "figures": 100, "sourced": 98,
                                      "unsourced": 0}]})
    cases.append(("coverage exactly at the threshold is green", at["x"]["green"] is True))

    ac, green = rollup_assay(w, {"mutation": {"score": 0.62, "high_water": 0.60}})
    cases.append(("a score at or above the mark is green", green is True))
    cases.append(("every class carries the assay state", set(ac) == {"figure-lineage", "layout-drift", "unmapped"}))
    _, dropped = rollup_assay(w, {"mutation": {"score": 0.55, "high_water": 0.60}})
    cases.append(("a score below the mark is not green", dropped is False))
    _, unmeasured = rollup_assay(w, {})
    cases.append(("no mutation measurement is not green", unmeasured is False))
    _, firstrun = rollup_assay(w, {"mutation": {"score": 0.41}})
    cases.append(("a first run with no mark is green on its own score", firstrun is True))
    return cases


def extra(p: argparse.ArgumentParser) -> None:
    p.description = (p.description or "") + " Run after oracle and assay, before ratchet."


if __name__ == "__main__":
    raise SystemExit(_cli.entry(__doc__ or "roll measurements up per defect class",
                                main, selftest, extra))
