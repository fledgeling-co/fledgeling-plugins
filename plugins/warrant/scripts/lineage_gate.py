#!/usr/bin/env python3
"""Fail the build when a rendered figure has no source behind it.

The gate half of lineage. lineage_extract.py answers what is on the page; this
decides whether that is acceptable and writes .warrant/oracle-coverage.json,
which is the evidence the tier ladder reads when it asks whether a surface has
earned tier 1.

Three things fail here, and each one is a different mistake:

- a figure with no source ref, self-declared or inherited -- the figure the
  vision plane cannot see is wrong;
- two figures claiming the same id, because then the coverage number counts one
  of them twice and the percentage stops meaning anything;
- with --require-figures, a surface that renders no figures at all, which is how
  a broken data fetch reads as perfect coverage.

Coverage is judged per surface as well as overall, because the ladder grants
authority per surface and an otherwise-clean repository can hide one ungated
page inside a good average.
"""

from __future__ import annotations

import argparse
import pathlib
import sys
from typing import Any

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import _cli                                                        # noqa: E402
import _state                                                      # noqa: E402
import lineage_extract                                             # noqa: E402


def coverage_of(report: dict[str, Any]) -> dict[str, Any]:
    """Per-surface and overall coverage, carrying both parts of every rate."""
    figures = len(report["figures"])
    sourced = figures - len(report["unsourced"])
    surfaces = []
    for surface in report["surfaces"]:
        n, d = surface["sourced"], surface["figures"]
        surfaces.append({
            **surface,
            # None rather than 100.0: a surface with no figures has no
            # denominator, and that is a different answer from complete.
            "coverage_pct": round(100.0 * n / d, 3) if d else None,
        })
    return {
        "figures": figures,
        "sourced": sourced,
        "coverage_pct": round(100.0 * sourced / figures, 3) if figures else None,
        "surfaces": surfaces,
    }


def evaluate(report: dict[str, Any], min_coverage: float,
             allow_duplicate_ids: bool, require_figures: bool) -> tuple[dict[str, Any], list[str]]:
    """Return (coverage, violations). A violation names the figure to go and fix."""
    cov = coverage_of(report)
    unsourced_by_file: dict[str, list[dict[str, Any]]] = {}
    for figure in report["unsourced"]:
        unsourced_by_file.setdefault(figure["file"], []).append(figure)

    violations: list[str] = []
    for surface in cov["surfaces"]:
        pct = surface["coverage_pct"]
        if pct is None:
            if require_figures:
                violations.append(
                    f"{surface['file']}: renders no figures at all, so nothing is "
                    f"gated on this surface")
            continue
        if pct < min_coverage:
            named = ", ".join(f"{f['id']} (line {f['line']}, {f['selector']})"
                              for f in unsourced_by_file.get(surface["file"], []))
            violations.append(
                f"{surface['file']}: "
                + _cli.rate(surface["sourced"], surface["figures"], "figures sourced")
                + f", below the required {min_coverage:.1f}% -- unsourced: {named}")
        if surface["duplicate_ids"] and not allow_duplicate_ids:
            violations.append(
                f"{surface['file']}: duplicate figure id(s) "
                f"{', '.join(surface['duplicate_ids'])}; two elements claiming one id "
                f"make the coverage count for this surface meaningless")
    return cov, violations


def main(args: argparse.Namespace) -> int:
    root = pathlib.Path(args.root).expanduser().resolve()

    if args.report:
        report = _state.read_json(pathlib.Path(args.report).expanduser().resolve())
        source_label = args.report
    else:
        target = pathlib.Path(args.input).expanduser().resolve() if args.input else root
        paths = lineage_extract.surfaces_for(target, args.glob)
        if not paths:
            _cli.say(args, f"no files matching {args.glob} under {target}")
            return _cli.MISSING
        report = lineage_extract.extract(paths, root if target.is_dir() else None)
        source_label = str(target)

    cov, violations = evaluate(report, args.min_coverage,
                               args.allow_duplicate_ids, args.require_figures)
    payload: dict[str, Any] = {
        **cov,
        "input": source_label,
        "min_coverage": args.min_coverage,
        "violations": violations,
        "generated_at": _cli.now(args).isoformat(),
    }

    out = _state.state_dir(root, create=True) / "oracle-coverage.json"
    try:
        _state.write_json(out, payload)
        payload["written_to"] = str(out)
    except OSError as exc:
        # The check itself already ran; losing the record is worth reporting but
        # not worth raising over, because the caller's exit code is the verdict.
        payload["written_to"] = None
        payload["write_error"] = f"{type(exc).__name__}: {exc}"
        _cli.say(args, f"could not write {out}: {exc}")

    _cli.say(args, "oracle lineage: "
                   + _cli.rate(cov["sourced"], cov["figures"], "figures sourced")
                   + f" across {len(cov['surfaces'])} surface(s)")
    for line in violations:
        _cli.say(args, f"  FAIL {line}")
    if not violations:
        _cli.say(args, "  every rendered figure resolves to a source")
    _cli.emit(args, payload)
    return _cli.FAILED if violations else _cli.OK


def _extra(p: argparse.ArgumentParser) -> None:
    p.add_argument("--input", help="HTML file or directory of them (default: --root)")
    p.add_argument("--glob", default="*.html", help="filename pattern when --input is a directory")
    p.add_argument("--report", help="a lineage_extract JSON report to judge instead of re-walking")
    p.add_argument("--min-coverage", type=float, default=100.0,
                   help="required sourced-figure percentage per surface (default: 100)")
    p.add_argument("--allow-duplicate-ids", action="store_true",
                   help="report duplicate figure ids without failing on them")
    p.add_argument("--require-figures", action="store_true",
                   help="also fail a surface that renders no figures at all")


def _run_captured(argv: list[str]) -> tuple[int, str, str]:
    """Run main() with both streams captured.

    A nested run inside --selftest must not write to the real streams, and
    capturing them is also how the contract's own output rule gets tested: under
    --json, stdout carries the object and nothing else.
    """
    import contextlib
    import io

    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = _cli.entry("selftest", main, None, _extra, argv)
    return rc, out.getvalue(), err.getvalue()


def selftest() -> list[tuple[str, bool]]:
    """Each rule seen firing and seen not firing, on real fixture surfaces."""
    import json
    import tempfile

    cases: list[tuple[str, bool]] = []
    fx = (pathlib.Path(__file__).resolve().parent.parent
          / "evals" / "fixtures" / "oracle-assay" / "lineage")

    sound = lineage_extract.extract([fx / "sound" / "dashboard.html"])
    gap = lineage_extract.extract([fx / "unsourced" / "kpi.html"])
    dupe = lineage_extract.extract([fx / "duplicate" / "dupe.html"])
    plain = lineage_extract.extract([fx / "nofigures" / "plain.html"])

    cov, viol = evaluate(sound, 100.0, False, True)
    cases.append(("a fully sourced surface passes", viol == []))
    cases.append(("coverage is 100% with both parts recorded",
                  cov["coverage_pct"] == 100.0 and cov["figures"] == 3 and cov["sourced"] == 3))

    cov, viol = evaluate(gap, 100.0, False, False)
    cases.append(("an unsourced figure fails", len(viol) == 1))
    cases.append(("the failure names every unsourced figure",
                  "guidance-fy27" in viol[0] and "npat" in viol[0]))
    cases.append(("the failure carries its numerator and denominator",
                  "1 of 3 figures sourced" in viol[0]))
    cases.append(("partial coverage is computed, not rounded to pass",
                  cov["coverage_pct"] == 33.333))

    _, viol_loose = evaluate(gap, 30.0, False, False)
    cases.append(("a lower --min-coverage lets the same surface pass", viol_loose == []))
    _, viol_tight = evaluate(sound, 100.0, False, False)
    cases.append(("--min-coverage does not fail a complete surface", viol_tight == []))

    _, viol = evaluate(dupe, 100.0, False, False)
    cases.append(("duplicate figure ids fail",
                  any("duplicate figure id" in v for v in viol)))
    _, viol = evaluate(dupe, 100.0, True, False)
    cases.append(("--allow-duplicate-ids stops that failing", viol == []))

    _, viol = evaluate(plain, 100.0, False, True)
    cases.append(("--require-figures fails a surface with no figures",
                  any("no figures at all" in v for v in viol)))
    _, viol = evaluate(plain, 100.0, False, False)
    cases.append(("without --require-figures an empty surface passes", viol == []))
    cases.append(("a surface with no figures has no coverage percentage",
                  coverage_of(plain)["surfaces"][0]["coverage_pct"] is None))

    # End to end through main(), including the coverage file it has to leave behind.
    with tempfile.TemporaryDirectory() as tmp:
        rc_ok, out_ok, err_ok = _run_captured(
            ["--root", tmp, "--input", str(fx / "sound"), "--json"])
        written = pathlib.Path(tmp) / ".warrant" / "oracle-coverage.json"
        cases.append(("a sound surface exits 0 through main", rc_ok == _cli.OK))
        cases.append(("oracle-coverage.json is written", written.exists()))
        cases.append(("under --json stdout carries only the JSON object",
                      isinstance(json.loads(out_ok), dict)))
        cases.append(("under --json the human summary goes to stderr",
                      "oracle lineage" in err_ok and "oracle lineage" not in out_ok))
        if written.exists():
            payload = json.loads(written.read_text())
            cases.append(("the coverage file records per-surface figures",
                          payload["surfaces"][0]["figures"] == 3))

        rc_bad, _, err_bad = _run_captured(
            ["--root", tmp, "--input", str(fx / "unsourced"), "--json"])
        cases.append(("an unsourced surface exits 2 through main", rc_bad == _cli.FAILED))
        cases.append(("the failing run names the figure on stderr",
                      "guidance-fy27" in err_bad))
        cases.append(("the coverage file records the violation",
                      bool(json.loads(written.read_text())["violations"])))

        rc_missing, _, _ = _run_captured(
            ["--root", tmp, "--input", str(fx / "nowhere"), "--json"])
        cases.append(("an absent input exits 3", rc_missing == _cli.MISSING))
    return cases


if __name__ == "__main__":
    raise SystemExit(_cli.entry(__doc__.splitlines()[0], main, selftest, _extra))
