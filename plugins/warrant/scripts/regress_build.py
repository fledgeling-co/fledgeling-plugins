"""Turn a recorded escape into a permanent regression case.

An escape in `escapes.jsonl` is a description of a mistake. A case in
`.warrant/regression/<escape-id>/` is that mistake made re-runnable: the inputs
the wrong verdict was written from, plus the verdict that should have been
returned. regress_run.py replays every case against the current lanes, and a
class may only be closed by machine while every case in it is still caught.

The expected verdict is `fail` for both kinds of escape, and the two get there
by different routes worth keeping apart. A missed defect should have failed
because the defect was there. An outcome mismatch should have failed because the
delivered thing was not the asked-for thing — the pipeline read not-as-specified
as complete, which is how roughly half of a 110-ticket corpus shipped (C24).
`--expected-verdict` overrides both, for the case where the honest answer was
`inconclusive`.

Idempotent: a case whose content already matches is left alone, including its
build timestamp, so re-running over the whole corpus does not churn the tree.
Inputs are only ever added. Nothing here deletes a case or an artefact, because
a regression corpus that can shrink is one that can be made to pass.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import os
import pathlib
import shutil
import sys
import tempfile
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _cli import ERROR, FAILED, MISSING, OK, emit, entry, parser, say
from _cli import run as dispatch
from _cli import now as clock
from _state import Absent, read_json, read_jsonl, state_dir, write_json
from feedback_record import FIXTURES, escapes_path

_DESC = "Turn a recorded escape into a permanent regression case"

VERDICTS = ("pass", "fail", "inconclusive")


def regression_dir(root: str | pathlib.Path) -> pathlib.Path:
    return state_dir(root) / "regression"


def case_dir(root: str | pathlib.Path, escape_id: str) -> pathlib.Path:
    return regression_dir(root) / escape_id


def file_digest(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def expected_verdict(escape: dict[str, Any], override: str | None) -> dict[str, Any]:
    verdict = override or escape.get("expected_verdict") or "fail"
    why = {
        "missed_defect": "the defect was present in these inputs and the pipeline passed them",
        "outcome_mismatch": "the delivered outcome did not match what the task asked for, "
                            "and the pipeline read it as complete",
    }.get(str(escape.get("kind")), "the pipeline returned the wrong verdict on these inputs")
    out: dict[str, Any] = {"verdict": verdict, "why": why}
    if verdict != "pass":
        out["defect_class"] = escape.get("defect_class")
        out["must_mention"] = [escape.get("defect_class")]
    return out


def _copy_in(sources: list[pathlib.Path], dest: pathlib.Path) -> list[dict[str, Any]]:
    """Copy artefacts under dest and return the manifest, digests included."""
    dest.mkdir(parents=True, exist_ok=True)
    inputs: list[dict[str, Any]] = []

    def record(target: pathlib.Path) -> None:
        inputs.append({"path": str(target.relative_to(dest.parent)),
                       "sha256": file_digest(target),
                       "bytes": target.stat().st_size})

    for src in sources:
        if not src.exists():
            raise Absent(str(src))
        if src.is_dir():
            target_dir = dest / src.name
            for item in sorted(src.rglob("*")):
                if item.is_file():
                    out = target_dir / item.relative_to(src)
                    out.parent.mkdir(parents=True, exist_ok=True)
                    if not out.exists() or file_digest(out) != file_digest(item):
                        shutil.copy2(item, out)
                    record(out)
            continue
        target = dest / src.name
        if target.exists() and file_digest(target) != file_digest(src):
            target = dest / f"{src.stem}-{file_digest(src)[:8]}{src.suffix}"
        if not target.exists():
            shutil.copy2(src, target)
        record(target)
    return inputs


def build(root: str | pathlib.Path, escape: dict[str, Any], *, artifacts: list[pathlib.Path],
          evidence_root: pathlib.Path | None, override: str | None,
          when: Any) -> dict[str, Any]:
    """Write or refresh one case. Returns a result record, never raises on an
    already-written case."""
    cid = str(escape["escape_id"])
    path = case_dir(root, cid)
    path.mkdir(parents=True, exist_ok=True)
    warnings: list[str] = []

    sources = list(artifacts)
    digest = str(escape.get("evidence_digest", ""))
    if evidence_root is not None and digest:
        snapshot = evidence_root / digest
        if snapshot.exists():
            sources.append(snapshot)

    inputs = _copy_in(sources, path / "inputs") if sources else []
    existing_inputs = []
    case_path = path / "case.json"
    previous: dict[str, Any] | None = None
    if case_path.exists():
        try:
            previous = read_json(case_path)
            existing_inputs = previous.get("inputs", [])
        except json.JSONDecodeError:
            warnings.append("the existing case.json was unreadable and has been rewritten")

    merged = {i["path"]: i for i in existing_inputs}
    merged.update({i["path"]: i for i in inputs})
    inputs = [merged[k] for k in sorted(merged)]

    if not inputs:
        warnings.append("no input artefacts: this case records the escape but cannot be "
                        "replayed until the snapshot for its evidence digest is supplied")

    case: dict[str, Any] = {
        "case_id": cid,
        "defect_class": escape.get("defect_class"),
        "item": escape.get("item"),
        "kind": escape.get("kind"),
        "source_evidence_digest": digest,
        "expected_verdict": expected_verdict(escape, override),
        "escape": escape,
        "inputs": inputs,
        "built_at": when.isoformat(),
    }

    unchanged = False
    if previous is not None:
        if {k: v for k, v in previous.items() if k != "built_at"} == \
           {k: v for k, v in case.items() if k != "built_at"}:
            case["built_at"] = previous.get("built_at", case["built_at"])
            unchanged = True

    if not unchanged:
        write_json(case_path, case)
    return {"case_id": cid, "path": str(path), "unchanged": unchanged,
            "inputs": len(inputs), "warnings": warnings,
            "expected_verdict": case["expected_verdict"]["verdict"]}


def _extra(p: argparse.ArgumentParser) -> None:
    p.add_argument("--escape-id", action="append", default=[],
                   help="repeatable; the escape to build a case from")
    p.add_argument("--all", action="store_true", help="build a case for every recorded escape")
    p.add_argument("--artifact", action="append", default=[], metavar="PATH",
                   help="repeatable; a file or directory to copy into the case's inputs")
    p.add_argument("--evidence-dir", help="where evidence snapshots live, one directory per "
                                          "digest; defaults to .warrant/evidence")
    p.add_argument("--expected-verdict", help=f"one of {', '.join(VERDICTS)}; defaults to fail")


def main(args: argparse.Namespace) -> int:
    if args.expected_verdict and args.expected_verdict not in VERDICTS:
        say(args, f"--expected-verdict must be one of {', '.join(VERDICTS)}")
        return ERROR
    if not args.all and not args.escape_id:
        say(args, "nothing selected: pass --escape-id ID (repeatable) or --all")
        return ERROR

    path = escapes_path(args.root)
    rows = read_jsonl(path)
    if not path.exists():
        say(args, f"no escapes recorded at {path}")
        return MISSING
    by_id = {str(r.get("escape_id")): r for r in rows if r.get("escape_id")}

    if args.all:
        selected = [by_id[k] for k in sorted(by_id)]
    else:
        unknown = [i for i in args.escape_id if i not in by_id]
        if unknown:
            say(args, f"no such escape: {', '.join(unknown)}")
            return ERROR
        selected = [by_id[i] for i in args.escape_id]

    evidence_root = pathlib.Path(args.evidence_dir) if args.evidence_dir \
        else state_dir(args.root) / "evidence"
    artifacts = [pathlib.Path(a).expanduser() for a in args.artifact]
    for a in artifacts:
        if not a.exists():
            say(args, f"--artifact does not exist: {a}")
            return ERROR

    state_dir(args.root, create=True)
    when = clock(args)
    results = [build(args.root, escape, artifacts=artifacts, evidence_root=evidence_root,
                     override=args.expected_verdict, when=when)
               for escape in selected]

    built = sum(1 for r in results if not r["unchanged"])
    for r in results:
        state = "unchanged" if r["unchanged"] else "built"
        say(args, f"{state}: {r['case_id']} ({r['inputs']} input artefact(s), "
                  f"expects {r['expected_verdict']})")
        for w in r["warnings"]:
            say(args, f"  warning: {w}")
    say(args, f"{len(results)} case(s), {built} written, {len(results) - built} already current")
    emit(args, {"cases": results, "written": built,
                "unchanged": len(results) - built,
                "regression": str(regression_dir(args.root))})
    return OK


def _parse(argv: list[str]) -> argparse.Namespace:
    p = parser(_DESC)
    _extra(p)
    return p.parse_args(argv)


def _run(argv: list[str]) -> tuple[int, str, str]:
    """Run one invocation through the real dispatcher, so the selftest observes
    the exit code a caller would see rather than the one main() returns."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = dispatch(main, None, _parse(argv))
    return code, out.getvalue(), err.getvalue()


def _seed(tmp: str, *, new: bool = False) -> pathlib.Path:
    d = pathlib.Path(tmp) / ".warrant"
    d.mkdir(parents=True, exist_ok=True)
    shutil.copy(FIXTURES / "warrant.toml", d / "warrant.toml")
    shutil.copy(FIXTURES / "lanes.toml", d / "lanes.toml")
    rows = (FIXTURES / "escapes.jsonl").read_text()
    if new:
        rows += (FIXTURES / "escapes-new.jsonl").read_text()
    (d / "escapes.jsonl").write_text(rows)
    return d


def selftest() -> list[tuple[str, bool]]:
    cases: list[tuple[str, bool]] = []
    missed = "esc-20260411-1a2b3c4d"          # kind: missed_defect
    mismatch = "esc-20260602-4d5e6f70"        # kind: outcome_mismatch

    with tempfile.TemporaryDirectory() as tmp:
        _seed(tmp)
        base = ["--root", tmp, "--json", "--now", "2026-08-18T06:00:00+00:00"]
        art = pathlib.Path(tmp) / "diff.patch"
        art.write_text("--- a\n+++ b\n@@ -1 +1 @@\n-old\n+new\n")

        code, out, _ = _run(base + ["--escape-id", missed, "--artifact", str(art)])
        payload = json.loads(out)
        case = read_json(case_dir(tmp, missed) / "case.json")
        cases.append(("one escape builds one case", code == OK and payload["written"] == 1))
        cases.append(("the case id is the escape id", case["case_id"] == missed))
        cases.append(("a missed defect expects fail",
                      case["expected_verdict"]["verdict"] == "fail"))
        cases.append(("the expected verdict names the class",
                      case["expected_verdict"]["must_mention"] == ["figure-lineage"]))
        cases.append(("the escape row is kept whole in the case",
                      case["escape"]["evidence_digest"] == "1" * 64))
        cases.append(("the artefact is copied in",
                      (case_dir(tmp, missed) / "inputs" / "diff.patch").exists()))
        cases.append(("the artefact digest is recorded",
                      case["inputs"][0]["sha256"] == file_digest(art)))

        code, out, _ = _run(base + ["--escape-id", missed, "--artifact", str(art),
                                    "--now", "2026-09-01T00:00:00+00:00"])
        cases.append(("a second identical build writes nothing",
                      code == OK and json.loads(out)["unchanged"] == 1))
        cases.append(("and does not move the build timestamp",
                      read_json(case_dir(tmp, missed) / "case.json")["built_at"]
                      == case["built_at"]))

        extra = pathlib.Path(tmp) / "capture.txt"
        extra.write_text("1280x720 capture stand-in")
        code, out, _ = _run(base + ["--escape-id", missed, "--artifact", str(extra)])
        after = read_json(case_dir(tmp, missed) / "case.json")
        cases.append(("a new artefact updates the case", json.loads(out)["written"] == 1))
        cases.append(("without dropping the artefacts already there",
                      len(after["inputs"]) == 2))

        code, out, err = _run(base + ["--escape-id", mismatch])
        mcase = read_json(case_dir(tmp, mismatch) / "case.json")
        cases.append(("an outcome mismatch also expects fail",
                      mcase["expected_verdict"]["verdict"] == "fail"))
        cases.append(("with a different reason recorded",
                      "did not match what the task asked for" in mcase["expected_verdict"]["why"]))
        cases.append(("a case with no artefacts warns that it cannot be replayed",
                      any("cannot be replayed" in w for w in json.loads(out)["cases"][0]["warnings"])))

        code, out, _ = _run(base + ["--all"])
        cases.append(("--all covers every recorded escape",
                      len(json.loads(out)["cases"]) == 5))

    with tempfile.TemporaryDirectory() as tmp:
        _seed(tmp)
        base = ["--root", tmp, "--json"]
        snap = pathlib.Path(tmp) / ".warrant" / "evidence" / ("1" * 64)
        (snap / "specs").mkdir(parents=True)
        (snap / "specs" / "acceptance.md").write_text("the figure must tie to its source")
        (snap / "render.html").write_text("<p>$1.2m</p>")
        code, out, _ = _run(base + ["--escape-id", missed])
        built = read_json(case_dir(tmp, missed) / "case.json")
        paths = [i["path"] for i in built["inputs"]]
        cases.append(("a snapshot for the evidence digest is found without being named",
                      code == OK and len(paths) == 2))
        cases.append(("a directory artefact is copied as a tree",
                      any(p.endswith("specs/acceptance.md") for p in paths)))

        code, out, _ = _run(base + ["--escape-id", missed, "--expected-verdict", "inconclusive"])
        overridden = read_json(case_dir(tmp, missed) / "case.json")
        cases.append(("--expected-verdict overrides the default",
                      overridden["expected_verdict"]["verdict"] == "inconclusive"))

        cases.append(("an unknown escape id exits 1",
                      _run(base + ["--escape-id", "esc-nope"])[0] == ERROR))
        cases.append(("selecting nothing exits 1", _run(base)[0] == ERROR))
        cases.append(("an artefact that does not exist exits 1",
                      _run(base + ["--escape-id", missed, "--artifact", "/nope/nothing"])[0] == ERROR))
        cases.append(("an invalid --expected-verdict exits 1",
                      _run(base + ["--all", "--expected-verdict", "probably"])[0] == ERROR))

    with tempfile.TemporaryDirectory() as tmp:
        cases.append(("no escapes file at all exits 3",
                      _run(["--root", tmp, "--all"])[0] == MISSING))

    return cases


if __name__ == "__main__":
    raise SystemExit(entry(_DESC, main, selftest, _extra))
