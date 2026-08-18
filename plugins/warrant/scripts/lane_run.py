#!/usr/bin/env python3
"""Run one lane against the evidence snapshot, and record what answered.

The lane is a command template in `.warrant/lanes.toml` with `{prompt_file}` and
`{model}` placeholders (and `{verdict_file}` when the command writes a file rather
than printing). This script substitutes, shells out, and validates what comes back
against `schemas/verdict.schema.json`. It makes no API call of its own — the model
is whatever the operator's command reaches, and the id and version recorded are
the operator's pin rather than anything the lane reported about itself.

Exit 2 on a verdict that fails the schema, or whose digest does not match the
snapshot: the snapshot is re-derived from the files on disk, so a snapshot edited
after it was taken cannot authorise anything either.

Exit 1 when the lane could not be run at all — a command that exits non-zero,
times out, or returns something that is not JSON. That is deliberately not exit 2:
a broken lane is not a failed item.

`inconclusive` is a terminal state and is reported as one. It routes to the class's
escalation, never to a retry, because forcing it to pass or fail would manufacture
certainty the pipeline does not have.
"""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import pathlib
import shlex
import shutil
import subprocess
import sys
import tempfile
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import _cli                                                   # noqa: E402
import _schema                                                # noqa: E402
import _state                                                 # noqa: E402
import snapshot_evidence                                      # noqa: E402

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
SCHEMA_PATH = PLUGIN / "schemas" / "verdict.schema.json"
FIXTURES = PLUGIN / "evals" / "fixtures" / "charter-panel-lot"
RUNS = "lane-runs.jsonl"


def load_schema() -> dict[str, object]:
    return json.loads(SCHEMA_PATH.read_text())


def find_lane(root: pathlib.Path, lane_id: str) -> dict[str, object]:
    lanes = _state.read_lanes(root)                            # Absent -> exit 3
    for lane in lanes.get("lanes", []):
        if isinstance(lane, dict) and str(lane.get("id")) == lane_id:
            return lane
    known = ", ".join(str(l.get("id")) for l in lanes.get("lanes", [])
                      if isinstance(l, dict)) or "none"
    raise ValueError(f"lanes.toml has no lane {lane_id!r}; it carries: {known}")


def build_argv(cmd: str, prompt_file: pathlib.Path, model: str,
               verdict_file: pathlib.Path | None) -> list[str]:
    """Split the template first, then substitute, so a path with a space in it
    stays one argument instead of becoming two."""
    argv: list[str] = []
    for token in shlex.split(cmd):
        token = token.replace("{prompt_file}", str(prompt_file))
        token = token.replace("{model}", model)
        if verdict_file is not None:
            token = token.replace("{verdict_file}", str(verdict_file))
        argv.append(token)
    return argv


def extra(p: argparse.ArgumentParser) -> None:
    p.add_argument("--lane", help="lane id from .warrant/lanes.toml")
    p.add_argument("--prompt", help="the prompt file handed to the lane")
    p.add_argument("--digest", help="the evidence digest the verdict must carry")
    p.add_argument("--verdict-file", default=None,
                   help="read the verdict from this path instead of stdout; also "
                        "substituted into {verdict_file} in the lane's cmd")
    p.add_argument("--timeout", type=float, default=900.0,
                   help="seconds before the lane is abandoned (default: 900)")


def main(args: argparse.Namespace) -> int:
    root = pathlib.Path(args.root).expanduser().resolve()
    if not args.lane or not args.prompt:
        _cli.say(args, "--lane and --prompt are both required")
        _cli.emit(args, {"ok": False, "reason": "usage"})
        return _cli.ERROR

    try:
        lane = find_lane(root, args.lane)
    except ValueError as exc:
        _cli.say(args, str(exc))
        _cli.emit(args, {"ok": False, "reason": "unknown-lane", "detail": str(exc)})
        return _cli.ERROR

    model = str(lane.get("model", "")).strip()
    version = str(lane.get("version", "")).strip()
    cmd = str(lane.get("cmd", "")).strip()
    if not model or not version:
        _cli.say(args, f"lane {args.lane}: model and version must both be pinned "
                       "before it may run (charter_validate.py gates this)")
        _cli.emit(args, {"ok": False, "reason": "unpinned-lane"})
        return _cli.ERROR
    if not cmd:
        _cli.say(args, f"lane {args.lane} has no cmd; give it a command template "
                       "with {prompt_file} and {model}")
        _cli.emit(args, {"ok": False, "reason": "no-cmd"})
        return _cli.ERROR
    if "{prompt_file}" not in cmd:
        _cli.say(args, f"lane {args.lane}: cmd has no {{prompt_file}} placeholder, so "
                       "the prompt would never reach the model")
        _cli.emit(args, {"ok": False, "reason": "no-prompt-placeholder"})
        return _cli.ERROR

    prompt = pathlib.Path(args.prompt).expanduser().resolve()
    if not prompt.is_file():
        raise _state.Absent(str(prompt))

    verdict_file = pathlib.Path(args.verdict_file).expanduser().resolve() \
        if args.verdict_file else None
    argv = build_argv(cmd, prompt, model, verdict_file)
    env = dict(os.environ)
    env.update({"WARRANT_LANE": args.lane, "WARRANT_MODEL": model,
                "WARRANT_MODEL_VERSION": version,
                "WARRANT_PROMPT_FILE": str(prompt),
                "WARRANT_EVIDENCE_DIGEST": args.digest or ""})

    started = time.monotonic()
    timed_out = False
    try:
        proc = subprocess.run(argv, capture_output=True, text=True, cwd=str(root),
                              env=env, timeout=args.timeout, check=False)
        stdout, stderr, returncode = proc.stdout, proc.stderr, proc.returncode
    except FileNotFoundError as exc:
        stdout, stderr, returncode = "", f"{exc}", 127
    except subprocess.TimeoutExpired:
        stdout, stderr, returncode, timed_out = "", "timed out", 124, True
    duration_ms = int((time.monotonic() - started) * 1000)

    row: dict[str, object] = {
        "ts": _cli.now(args).isoformat(),
        "lane": args.lane,
        "role": lane.get("role"),
        "model": model,
        "model_version": version,
        "evidence_digest": args.digest,
        "prompt_file": str(prompt),
        "argv": argv,
        "exit_code": returncode,
        "duration_ms": duration_ms,
        "timed_out": timed_out,
        "state": None,
        "schema_ok": None,
        "digest_ok": None,
    }
    runs_path = _state.state_dir(root, create=True) / RUNS

    def record(reason: str, code: int, payload: dict[str, object]) -> int:
        # The call has already happened, so the row is written whatever the
        # outcome and a later failure is reported rather than raised.
        row["reason"] = reason
        problems: list[str] = []
        try:
            _state.append_jsonl(runs_path, row)
        except OSError as exc:
            problems.append(f"could not record the run: {type(exc).__name__}: {exc}")
            _cli.say(args, f"  problem: {problems[-1]}")
        _cli.emit(args, {**payload, "lane": args.lane, "model": model,
                         "model_version": version, "duration_ms": duration_ms,
                         "recorded": str(runs_path), "problems": problems})
        return code

    if returncode != 0:
        detail = (stderr or stdout or "").strip().splitlines()[:3]
        _cli.say(args, f"lane {args.lane} did not run: exit {returncode}"
                       + (f" ({'timed out' if timed_out else '; '.join(detail)})"
                          if detail or timed_out else ""))
        _cli.say(args, "  a broken lane is not a failed item, so this is exit 1")
        return record("command-failed", _cli.ERROR,
                      {"ok": False, "reason": "command-failed",
                       "exit_code": returncode, "timed_out": timed_out})

    raw = stdout
    if verdict_file is not None:
        if not verdict_file.is_file():
            _cli.say(args, f"lane {args.lane} exited 0 but wrote no verdict at "
                           f"{verdict_file}")
            return record("no-verdict-file", _cli.ERROR,
                          {"ok": False, "reason": "no-verdict-file"})
        raw = verdict_file.read_text()

    try:
        verdict = json.loads(raw)
    except json.JSONDecodeError as exc:
        _cli.say(args, f"lane {args.lane} returned something that is not JSON: {exc}")
        _cli.say(args, f"  first 120 char(s): {raw.strip()[:120]!r}")
        _cli.say(args, "  the lane's cmd must emit only the verdict, or write it to "
                       "--verdict-file")
        return record("not-json", _cli.ERROR, {"ok": False, "reason": "not-json"})

    violations = _schema.validate(verdict, load_schema())
    row["schema_ok"] = not violations
    if isinstance(verdict, dict):
        row["state"] = verdict.get("state")
        row["item"] = verdict.get("item")
        row["defect_class"] = verdict.get("defect_class")
    if violations:
        _cli.say(args, f"verdict REJECTED: {len(violations)} schema violation(s)")
        for v in violations:
            _cli.say(args, f"  {v}")
        return record("schema", _cli.FAILED,
                      {"ok": False, "reason": "schema", "violations": violations,
                       "state": row["state"]})

    claimed = str(verdict["evidence_digest"])
    digest_problems: list[str] = []
    if args.digest and claimed != args.digest:
        digest_problems.append(
            f"the verdict cites {claimed[:12]}… and the snapshot is {args.digest[:12]}…")
    if str(verdict["lane"]) != args.lane:
        digest_problems.append(
            f"the verdict was written for lane {verdict['lane']!r}, not {args.lane!r}")
    snapshot_ok, snapshot_problems = snapshot_evidence.verify(root, claimed)
    digest_problems.extend(snapshot_problems)
    row["digest_ok"] = not digest_problems

    if digest_problems:
        _cli.say(args, "verdict VOID: it does not rest on the snapshot")
        for problem in digest_problems:
            _cli.say(args, f"  {problem}")
        _cli.say(args, "  take the snapshot before judging, and hand the lane its "
                       "digest; a verdict whose evidence cannot be re-derived "
                       "authorises nothing")
        return record("digest", _cli.FAILED,
                      {"ok": False, "reason": "digest", "problems": digest_problems,
                       "state": verdict["state"]})

    state = str(verdict["state"])
    _cli.say(args, f"lane {args.lane} ({model} @ {version}) → {state}"
                   f" on {verdict['item']} / {verdict['defect_class']}")
    _cli.say(args, f"  evidence {claimed[:16]}… re-derived from "
                   f"{len(json.loads((_state.state_dir(root) / 'snapshots' / claimed / 'manifest.json').read_text())['files'])} "
                   "snapshotted file(s)")
    for finding in verdict["findings"]:
        _cli.say(args, f"  [{finding['kind']}] {finding['id']}: {finding['statement']}")
    if state == "inconclusive":
        _cli.say(args, "  inconclusive is terminal: it routes to the class's "
                       "escalation, not to a retry")
    return record("ok", _cli.OK,
                  {"ok": True, "state": state, "item": verdict["item"],
                   "defect_class": verdict["defect_class"],
                   "evidence_digest": claimed, "verdict": verdict,
                   "findings": len(verdict["findings"])})


# ── selftest ─────────────────────────────────────────────────────────────────

def _call(*argv: str) -> tuple[int, str, str]:
    p = _cli.parser("selftest")
    extra(p)
    parsed = p.parse_args(list(argv))
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = _cli.run(main, None, parsed)
    return code, out.getvalue(), err.getvalue()


def _stub(*parts: str) -> str:
    return " ".join([sys.executable, str(FIXTURES / "lane_stub.py"), *parts])


def _lanes(root: pathlib.Path, cmd: str, *, model: str = "example/grader-v2",
           version: str = "2026-06-01", lane_id: str = "grader-primary") -> None:
    d = _state.state_dir(root, create=True)
    lines = ["[[lanes]]", _state.toml_kv("id", lane_id),
             _state.toml_kv("role", "grader"), _state.toml_kv("model", model),
             _state.toml_kv("version", version), _state.toml_kv("cmd", cmd)]
    (d / "lanes.toml").write_text("\n".join(lines) + "\n")


def selftest() -> list[tuple[str, bool]]:
    cases: list[tuple[str, bool]] = []
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="warrant-lane-run-"))
    try:
        root = tmp / "repo"
        (root / "e2e").mkdir(parents=True)
        (root / "work.diff").write_text("--- a/x\n+++ b/x\n+one\n")
        (root / "e2e" / "inbox.spec.ts").write_text("expect(total).toBe(12.4)\n")
        prompt = root / "prompt.txt"
        prompt.write_text("The evidence is above. State the verdict.\n")

        # A real snapshot, so the digest check is against something re-derivable.
        sp = _cli.parser("snap")
        snapshot_evidence.extra(sp)
        snap_args = sp.parse_args(["--root", str(root), "--diff", "work.diff",
                                   "--tests", "e2e"])
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(io.StringIO()):
            _cli.run(snapshot_evidence.main, None, snap_args)
        digest = buf.getvalue().strip().splitlines()[-1].strip()
        cases.append(("the fixture snapshot exists", len(digest) == 64))

        schema = load_schema()
        cases.append(("the schema is valid JSON and an object", isinstance(schema, dict)))
        cases.append(("a pass verdict satisfies the schema",
                      _schema.validate(json.loads((FIXTURES / "verdict.pass.json")
                                                  .read_text()), schema) == []))
        cases.append(("a fail verdict with findings satisfies the schema",
                      _schema.validate(json.loads((FIXTURES / "verdict.fail-numeric.json")
                                                  .read_text()), schema) == []))
        cases.append(("an inconclusive verdict with its reason satisfies the schema",
                      _schema.validate(json.loads((FIXTURES / "verdict.inconclusive.json")
                                                  .read_text()), schema) == []))
        bare = _schema.validate(json.loads((FIXTURES / "verdict.inconclusive-bare.json")
                                           .read_text()), schema)
        cases.append(("an inconclusive verdict with no reason is rejected", bool(bare)))
        cases.append(("a verdict with an invented state is rejected",
                      bool(_schema.validate(
                          json.loads((FIXTURES / "verdict.invalid.json").read_text()),
                          schema))))
        cases.append(("a verdict cannot smuggle in a confidence field",
                      any("confidence" in v for v in _schema.validate(
                          json.loads((FIXTURES / "verdict.invalid.json").read_text()),
                          schema))))

        # The happy path.
        _lanes(root, _stub("--verdict", str(FIXTURES / "verdict.pass.json"),
                           "--digest", digest, "--model", "{model}",
                           "--prompt", "{prompt_file}"))
        code, out, _ = _call("--root", str(root), "--lane", "grader-primary",
                             "--prompt", str(prompt), "--digest", digest,
                             "--now", "2026-08-19T00:00:00+00:00")
        cases.append(("a valid verdict on a matching snapshot exits 0", code == _cli.OK))
        cases.append(("the report names the pinned model and version",
                      "example/grader-v2" in out and "2026-06-01" in out))
        runs = _state.read_jsonl(_state.state_dir(root) / RUNS)
        cases.append(("the run is recorded with lane, model and version",
                      runs and runs[-1]["lane"] == "grader-primary"
                      and runs[-1]["model"] == "example/grader-v2"
                      and runs[-1]["model_version"] == "2026-06-01"))
        cases.append(("the record carries the evidence digest",
                      runs[-1]["evidence_digest"] == digest))

        # inconclusive is terminal, not a retry.
        _lanes(root, _stub("--verdict", str(FIXTURES / "verdict.inconclusive.json"),
                           "--digest", digest, "--lane", "grader-primary",
                           "--model", "{model}", "--prompt", "{prompt_file}"))
        code, out, _ = _call("--root", str(root), "--lane", "grader-primary",
                             "--prompt", str(prompt), "--digest", digest)
        cases.append(("an inconclusive verdict exits 0", code == _cli.OK))
        cases.append(("it is reported as terminal, routed to a person",
                      "terminal" in out and "not to a retry" in out))

        # Exit 2: the schema.
        _lanes(root, _stub("--verdict", str(FIXTURES / "verdict.invalid.json"),
                           "--digest", digest, "--model", "{model}",
                           "--prompt", "{prompt_file}"))
        code, out, _ = _call("--root", str(root), "--lane", "grader-primary",
                             "--prompt", str(prompt), "--digest", digest)
        cases.append(("a verdict that fails the schema exits 2", code == _cli.FAILED))
        cases.append(("the violations are named",
                      "not one of" in out and "$.state" in out))
        cases.append(("a rejected verdict is still recorded",
                      _state.read_jsonl(_state.state_dir(root) / RUNS)[-1]["schema_ok"]
                      is False))

        # Exit 2: the digest.
        _lanes(root, _stub("--verdict", str(FIXTURES / "verdict.pass.json"),
                           "--digest", "f" * 64, "--model", "{model}",
                           "--prompt", "{prompt_file}"))
        code, out, _ = _call("--root", str(root), "--lane", "grader-primary",
                             "--prompt", str(prompt), "--digest", digest)
        cases.append(("a verdict citing another digest exits 2", code == _cli.FAILED))
        cases.append(("the mismatch is named", "does not rest on the snapshot" in out))

        _lanes(root, _stub("--verdict", str(FIXTURES / "verdict.pass.json"),
                           "--digest", "e" * 64, "--model", "{model}",
                           "--prompt", "{prompt_file}"))
        code, out, _ = _call("--root", str(root), "--lane", "grader-primary",
                             "--prompt", str(prompt))
        cases.append(("a verdict citing a snapshot that does not exist exits 2",
                      code == _cli.FAILED and "no snapshot" in out))

        # Exit 2: a snapshot edited after it was taken.
        tampered = (_state.state_dir(root) / "snapshots" / digest / "files"
                    / "e2e" / "inbox.spec.ts")
        tampered.chmod(0o644)
        tampered.write_text("expect(total).toBe(99.9)\n")
        _lanes(root, _stub("--verdict", str(FIXTURES / "verdict.pass.json"),
                           "--digest", digest, "--model", "{model}",
                           "--prompt", "{prompt_file}"))
        code, out, _ = _call("--root", str(root), "--lane", "grader-primary",
                             "--prompt", str(prompt), "--digest", digest)
        cases.append(("a verdict on an edited snapshot exits 2",
                      code == _cli.FAILED and "modified after the snapshot" in out))
        tampered.write_text("expect(total).toBe(12.4)\n")
        tampered.chmod(0o444)

        # Exit 2: a verdict written for another lane.
        _lanes(root, _stub("--verdict", str(FIXTURES / "verdict.inconclusive.json"),
                           "--digest", digest, "--model", "{model}",
                           "--prompt", "{prompt_file}"))
        code, out, _ = _call("--root", str(root), "--lane", "grader-primary",
                             "--prompt", str(prompt), "--digest", digest)
        cases.append(("a verdict written for another lane exits 2",
                      code == _cli.FAILED and "written for lane" in out))

        # Exit 1: the lane could not be run.
        _lanes(root, _stub("--mode", "garbage", "--model", "{model}",
                           "--prompt", "{prompt_file}"))
        code, out, _ = _call("--root", str(root), "--lane", "grader-primary",
                             "--prompt", str(prompt), "--digest", digest)
        cases.append(("output that is not JSON exits 1",
                      code == _cli.ERROR and "not JSON" in out))
        _lanes(root, _stub("--mode", "fail", "--model", "{model}",
                           "--prompt", "{prompt_file}"))
        code, out, _ = _call("--root", str(root), "--lane", "grader-primary",
                             "--prompt", str(prompt), "--digest", digest)
        cases.append(("a command that exits non-zero exits 1",
                      code == _cli.ERROR and "not a failed item" in out))
        _lanes(root, _stub("--mode", "slow", "--model", "{model}",
                           "--prompt", "{prompt_file}"))
        code, out, _ = _call("--root", str(root), "--lane", "grader-primary",
                             "--prompt", str(prompt), "--digest", digest,
                             "--timeout", "1")
        cases.append(("a lane that hangs exits 1 on --timeout",
                      code == _cli.ERROR and "timed out" in out))
        cases.append(("the timeout is recorded",
                      _state.read_jsonl(_state.state_dir(root) / RUNS)[-1]["timed_out"]
                      is True))
        _lanes(root, "definitely-not-on-path {prompt_file} {model}")
        code, out, _ = _call("--root", str(root), "--lane", "grader-primary",
                             "--prompt", str(prompt), "--digest", digest)
        cases.append(("a cmd that is not on PATH exits 1", code == _cli.ERROR))

        # --verdict-file, for a command that cannot keep stdout clean.
        vf = root / "verdict.out.json"
        _lanes(root, _stub("--verdict", str(FIXTURES / "verdict.pass.json"),
                           "--digest", digest, "--out", "{verdict_file}",
                           "--model", "{model}", "--prompt", "{prompt_file}"))
        code, out, _ = _call("--root", str(root), "--lane", "grader-primary",
                             "--prompt", str(prompt), "--digest", digest,
                             "--verdict-file", str(vf))
        cases.append(("--verdict-file is read instead of stdout", code == _cli.OK))
        vf.unlink()
        _lanes(root, _stub("--mode", "empty", "--model", "{model}",
                           "--prompt", "{prompt_file}"))
        code, out, _ = _call("--root", str(root), "--lane", "grader-primary",
                             "--prompt", str(prompt), "--digest", digest,
                             "--verdict-file", str(vf))
        cases.append(("a lane that writes no verdict file exits 1",
                      code == _cli.ERROR and "wrote no verdict" in out))

        # Usage and preconditions.
        code, out, _ = _call("--root", str(root), "--lane", "nope",
                             "--prompt", str(prompt))
        cases.append(("an unknown lane id exits 1",
                      code == _cli.ERROR and "no lane" in out))
        code, out, _ = _call("--root", str(root), "--lane", "grader-primary")
        cases.append(("no --prompt exits 1", code == _cli.ERROR))
        code, out, _ = _call("--root", str(root), "--lane", "grader-primary",
                             "--prompt", str(root / "absent.txt"))
        cases.append(("a prompt file that does not exist exits 3", code == _cli.MISSING))
        bare_root = tmp / "bare"
        bare_root.mkdir()
        code, out, _ = _call("--root", str(bare_root), "--lane", "grader-primary",
                             "--prompt", str(prompt))
        cases.append(("no lanes.toml exits 3", code == _cli.MISSING))
        _lanes(root, _stub("--model", "{model}"))
        code, out, _ = _call("--root", str(root), "--lane", "grader-primary",
                             "--prompt", str(prompt), "--digest", digest)
        cases.append(("a cmd with no {prompt_file} exits 1",
                      code == _cli.ERROR and "would never reach the model" in out))
        _lanes(root, _stub("--verdict", str(FIXTURES / "verdict.pass.json"),
                           "--prompt", "{prompt_file}"), version="")
        code, out, _ = _call("--root", str(root), "--lane", "grader-primary",
                             "--prompt", str(prompt), "--digest", digest)
        cases.append(("an unpinned lane refuses to run",
                      code == _cli.ERROR and "pinned" in out))

        # Argument splitting: a path with a space stays one argument.
        argv = build_argv("run {prompt_file} --model {model}",
                          pathlib.Path("/tmp/a dir/prompt.txt"), "x/y", None)
        cases.append(("a prompt path with a space stays one argument",
                      argv == ["run", "/tmp/a dir/prompt.txt", "--model", "x/y"]))

        _lanes(root, _stub("--verdict", str(FIXTURES / "verdict.pass.json"),
                           "--digest", digest, "--model", "{model}",
                           "--prompt", "{prompt_file}"))
        code, o, e = _call("--root", str(root), "--lane", "grader-primary",
                           "--prompt", str(prompt), "--digest", digest, "--json")
        cases.append(("--json puts only JSON on stdout",
                      o.lstrip().startswith("{") and json.loads(o)["state"] == "pass"))
    finally:
        for path in tmp.rglob("*"):
            with contextlib.suppress(OSError):
                path.chmod(0o755)
        shutil.rmtree(tmp, ignore_errors=True)
    return cases


if __name__ == "__main__":
    raise SystemExit(_cli.entry(__doc__ or "", main, selftest, extra))
