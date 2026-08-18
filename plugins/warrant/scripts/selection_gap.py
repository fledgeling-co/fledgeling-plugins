#!/usr/bin/env python3
"""Report the authored tests CI never runs, grouped by the surface they cover.

The selected set is what gates a merge, so it is the set whose sensitivity
matters -- and a test outside it is documentation rather than a gate. Grouping by
surface is the part that turns a number into a decision: a repository can select
most of its tests and still leave one whole surface with nothing running against
it, and the average will not say so.

Both inputs are lists of tests, in whichever form is to hand: a Playwright
--list dump, one id per line as file::title, or bare file paths. A bare path
means the whole file, so a selection expressed per file still matches tests
expressed per title. Anything in the selection that no longer exists in the
authored set is reported too, because a selection naming a renamed test is a gate
that quietly stopped running.

Surface is inferred from the spec path: the directory under a tests, specs, e2e
or __tests__ root, falling back to the containing directory and then to the file
stem. It exits 0 with the report; the ratchet decides what to do about it.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys
from typing import Any

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import _cli                                                        # noqa: E402
import _state                                                      # noqa: E402

# "[chromium] › apps/web/e2e/tests/a.spec.ts:14:5 › suite › name"
_PLAYWRIGHT = re.compile(r"^(?:\[(?P<project>[^\]]+)\]\s*›\s*)?"
                         r"(?P<file>[^\s›]+?\.[A-Za-z]+)(?::\d+(?::\d+)?)?"
                         r"\s*›\s*(?P<title>.+)$")
_NOISE = re.compile(r"^(Listing tests:|Total:\s|Running\s\d+\stest|\s*$)")
_TEST_ROOTS = ("tests", "test", "specs", "spec", "e2e", "__tests__")
_SPEC_SUFFIX = re.compile(r"\.(spec|test)\.[A-Za-z]+$|\.[A-Za-z]+$")


def surface_of(spec_path: str) -> str:
    """The surface a spec covers, inferred from where it sits."""
    parts = pathlib.PurePosixPath(spec_path.replace("\\", "/")).parts
    # The LAST test root wins: a path like apps/web/e2e/tests/campaign has two,
    # and the innermost is the one that names surfaces.
    roots = [i for i, part in enumerate(parts) if part in _TEST_ROOTS and i + 1 < len(parts)]
    if roots:
        index = roots[-1]
        nxt = parts[index + 1]
        # A file directly under the tests root names its own surface.
        if index + 2 < len(parts):
            return nxt
        return _SPEC_SUFFIX.sub("", nxt)
    if len(parts) > 1:
        return parts[-2]
    return _SPEC_SUFFIX.sub("", parts[-1]) if parts else "(unknown)"


def parse_list(path: pathlib.Path) -> dict[str, Any]:
    """One test list, in any of the three accepted forms."""
    if not path.exists():
        raise _state.Absent(str(path))
    tests: list[dict[str, Any]] = []
    whole_files: list[str] = []
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or _NOISE.match(line):
            continue
        if "::" in line:
            file, title = line.split("::", 1)
            tests.append({"id": f"{file.strip()}::{title.strip()}", "file": file.strip(),
                          "title": title.strip(), "project": None})
            continue
        match = _PLAYWRIGHT.match(line)
        if match:
            file = match.group("file")
            title = re.sub(r"\s*›\s*", " › ", match.group("title").strip())
            tests.append({"id": f"{file}::{title}", "file": file, "title": title,
                          "project": match.group("project")})
            continue
        whole_files.append(line)
    return {"tests": tests, "whole_files": whole_files}


def compare(authored: dict[str, Any], selected: dict[str, Any]) -> dict[str, Any]:
    """Which authored tests never run, and what that leaves ungated."""
    selected_ids = {t["id"] for t in selected["tests"]}
    selected_files = set(selected["whole_files"]) | {t["file"] for t in selected["tests"]}
    covered_files = set(selected["whole_files"])

    never_run: list[str] = []
    by_surface: dict[str, dict[str, Any]] = {}
    for test in authored["tests"]:
        surface = surface_of(test["file"])
        bucket = by_surface.setdefault(surface, {"authored": 0, "selected": 0,
                                                 "never_run": 0, "never_run_ids": [],
                                                 "files": set()})
        bucket["authored"] += 1
        bucket["files"].add(test["file"])
        if test["id"] in selected_ids or test["file"] in covered_files:
            bucket["selected"] += 1
        else:
            bucket["never_run"] += 1
            bucket["never_run_ids"].append(test["id"])
            never_run.append(test["id"])

    authored_ids = {t["id"] for t in authored["tests"]}
    authored_files = {t["file"] for t in authored["tests"]}
    orphans = sorted([t["id"] for t in selected["tests"] if t["id"] not in authored_ids]
                     + [f for f in selected["whole_files"] if f not in authored_files])

    for bucket in by_surface.values():
        bucket["files"] = sorted(bucket["files"])
        bucket["coverage_pct"] = round(100.0 * bucket["selected"] / bucket["authored"], 3) \
            if bucket["authored"] else None

    selected_count = sum(b["selected"] for b in by_surface.values())
    return {
        "authored": len(authored["tests"]),
        "selected": selected_count,
        "never_run": never_run,
        "never_run_count": len(never_run),
        "by_surface": dict(sorted(by_surface.items())),
        "unselected_surfaces": sorted(s for s, b in by_surface.items() if b["selected"] == 0),
        "orphan_selected": orphans,
        "selection_size": len(selected["tests"]) + len(selected["whole_files"]),
    }


def main(args: argparse.Namespace) -> int:
    if not args.authored or not args.selected:
        _cli.say(args, "--authored and --selected are both required")
        return _cli.ERROR
    root = pathlib.Path(args.root).expanduser().resolve()
    authored = parse_list((root / args.authored).resolve()
                          if not pathlib.Path(args.authored).is_absolute()
                          else pathlib.Path(args.authored))
    selected = parse_list((root / args.selected).resolve()
                          if not pathlib.Path(args.selected).is_absolute()
                          else pathlib.Path(args.selected))
    if not authored["tests"]:
        _cli.say(args, f"no tests parsed from {args.authored}")
        return _cli.MISSING

    result = compare(authored, selected)
    result["generated_at"] = _cli.now(args).isoformat()

    _cli.say(args, "CI runs " + _cli.rate(result["selected"], result["authored"],
                                          "authored tests"))
    for surface, bucket in result["by_surface"].items():
        _cli.say(args, f"  {surface}: "
                       + _cli.rate(bucket["selected"], bucket["authored"], "tests selected")
                       + (" -- nothing in this surface runs in CI" if bucket["selected"] == 0
                          else ""))
    for test_id in result["never_run"]:
        _cli.say(args, f"  never run: {test_id}")
    for orphan in result["orphan_selected"]:
        _cli.say(args, f"  selected but not authored (renamed or deleted?): {orphan}")
    _cli.emit(args, result)
    return _cli.OK


def _extra(p: argparse.ArgumentParser) -> None:
    p.add_argument("--authored", help="every authored test: a Playwright --list dump, "
                                      "file::title lines, or bare spec paths")
    p.add_argument("--selected", help="the tests CI actually selects, in the same forms")


def selftest() -> list[tuple[str, bool]]:
    """Every rule seen firing and seen not firing, on real fixture lists."""
    import contextlib
    import io
    import json
    import tempfile

    cases: list[tuple[str, bool]] = []
    fx = (pathlib.Path(__file__).resolve().parent.parent
          / "evals" / "fixtures" / "oracle-assay" / "selection")

    authored = parse_list(fx / "authored.list")
    selected = parse_list(fx / "selected.list")
    dump = parse_list(fx / "playwright-list.txt")

    cases.append(("file::title lines parse", len(authored["tests"]) == 8))
    cases.append(("a bare path parses as a whole file",
                  selected["whole_files"] == ["apps/web/e2e/tests/storyboard/sweeps.spec.ts"]))
    cases.append(("a playwright dump parses", len(dump["tests"]) == 3))
    cases.append(("the dump's banner and totals are ignored", dump["whole_files"] == []))
    cases.append(("line numbers and project tags are dropped from the id",
                  dump["tests"][0]["id"] == "apps/web/e2e/tests/campaign/coverage.spec.ts"
                                            "::campaign coverage › ledger rows carry a stable id"))
    cases.append(("the project is still recorded", dump["tests"][0]["project"] == "chromium"))

    cases.append(("surface comes from the directory under the tests root",
                  surface_of("apps/web/e2e/tests/campaign/coverage.spec.ts") == "campaign"))
    cases.append(("a spec directly under the tests root names its own surface",
                  surface_of("apps/web/e2e/tests/smoke.spec.ts") == "smoke"))
    cases.append(("with no tests root the parent directory is the surface",
                  surface_of("packages/ui/button.spec.ts") == "ui"))
    cases.append(("a bare filename falls back to its stem",
                  surface_of("button.spec.ts") == "button"))

    result = compare(authored, selected)
    cases.append(("authored and selected are counted",
                  result["authored"] == 8 and result["selected"] == 5))
    cases.append(("an unselected test is reported as never run",
                  result["never_run_count"] == 3))
    cases.append(("a selected test is not reported as never run",
                  all("ledger rows carry a stable id" not in i for i in result["never_run"])))
    cases.append(("a whole-file selection covers every test in that file",
                  result["by_surface"]["storyboard"]["selected"] == 2
                  and result["by_surface"]["storyboard"]["never_run"] == 0))
    cases.append(("a partially selected surface reports the remainder",
                  result["by_surface"]["tasks"]["selected"] == 1
                  and result["by_surface"]["tasks"]["never_run"] == 1))
    cases.append(("a surface with nothing selected is named",
                  result["unselected_surfaces"] == ["presentations"]))
    cases.append(("a fully selected surface is not named",
                  "campaign" not in result["unselected_surfaces"]))
    cases.append(("per-surface coverage carries its parts",
                  result["by_surface"]["tasks"]["coverage_pct"] == 50.0
                  and result["by_surface"]["tasks"]["authored"] == 2))
    cases.append(("a selection entry that is not authored is reported",
                  result["orphan_selected"] == ["apps/web/e2e/tests/tasks/dictation.spec.ts"
                                                "::dictation › a test that was renamed away"]))

    dump_result = compare(authored, dump)
    cases.append(("the dump form drives the same comparison",
                  dump_result["selected"] == 3 and dump_result["never_run_count"] == 5))
    cases.append(("two surfaces are ungated under the narrower selection",
                  dump_result["unselected_surfaces"] == ["presentations", "storyboard"]))
    cases.append(("a dump naming only authored tests leaves no orphans",
                  dump_result["orphan_selected"] == []))

    identical = compare(authored, authored)
    cases.append(("an identical selection leaves nothing never run",
                  identical["never_run"] == [] and identical["unselected_surfaces"] == []))

    def run(argv: list[str]) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            rc = _cli.entry("selftest", main, None, _extra, argv)
        return rc, out.getvalue(), err.getvalue()

    with tempfile.TemporaryDirectory() as tmp:
        rc, out, err = run(["--root", tmp, "--authored", str(fx / "authored.list"),
                            "--selected", str(fx / "selected.list"), "--json"])
        cases.append(("a gap-filled report still exits 0, because this reports",
                      rc == _cli.OK))
        cases.append(("stdout is the JSON report",
                      json.loads(out)["never_run_count"] == 3))
        cases.append(("the summary carries numerator and denominator",
                      "5 of 8 authored tests" in err))
        cases.append(("the ungated surface is called out on stderr",
                      "nothing in this surface runs in CI" in err))

        rc, _, _ = run(["--root", tmp, "--authored", str(fx / "nope.list"),
                        "--selected", str(fx / "selected.list"), "--json"])
        cases.append(("an absent list exits 3", rc == _cli.MISSING))
        rc, _, _ = run(["--root", tmp, "--json"])
        cases.append(("missing arguments exit 1, not 2", rc == _cli.ERROR))

        # --now has to reach the report, or a test cannot pin the timestamp.
        stamped = ["--root", tmp, "--authored", str(fx / "authored.list"),
                   "--selected", str(fx / "selected.list"), "--json",
                   "--now", "2026-08-19T00:00:00Z"]
        _, out, _ = run(stamped)
        cases.append(("--now overrides the clock",
                      json.loads(out)["generated_at"] == "2026-08-19T00:00:00+00:00"))
        _, out_real, _ = run(stamped[:-2])
        cases.append(("without --now the real clock is used",
                      json.loads(out_real)["generated_at"] != "2026-08-19T00:00:00+00:00"))

        empty = pathlib.Path(tmp) / "empty.list"
        empty.write_text("# nothing here\n")
        rc, _, _ = run(["--root", tmp, "--authored", str(empty),
                        "--selected", str(fx / "selected.list"), "--json"])
        cases.append(("an authored list with no tests exits 3", rc == _cli.MISSING))
    return cases


if __name__ == "__main__":
    raise SystemExit(_cli.entry(__doc__.splitlines()[0], main, selftest, _extra))
