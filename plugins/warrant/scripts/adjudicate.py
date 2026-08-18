#!/usr/bin/env python3
"""Route a lane disagreement to the check that would settle it.

Two or more lanes conflict. This prints a routing decision, never a winner:
majority logic over lanes is exactly the failure the panel evidence measures —
nine frontier judges from seven families supply about two effective independent
votes, and the best single judge matched or outperformed the whole panel across
every tested condition. Counting lanes buys correlated error at panel prices.

The job instead is the software equivalent of stopping the reading and going to
look at the artifact: decide which deterministic check answers the disputed
claim.

    numeric claim            -> tick_and_tie.py       recompute the figure
    missing-element claim    -> lineage_gate.py       is it rendered and sourced
    classification claim     -> taxonomy_check.py     is the field the right field
    anything else            -> a named human, with the reason

`--majority` exits 1 rather than resolving. A disagreement this script cannot
route to a check is a disagreement for a person, not for a vote.

Exit 2 when the verdicts are not judging the same thing — different items, or
different evidence digests. That is not a disagreement to route; one of the two
verdicts is void, and lane_run.py's digest check is where that gets caught.
Digest agreement is all this checks: it does not re-derive the snapshot, because
adjudication may happen away from the machine that took it.
"""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import pathlib
import re
import shutil
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import _cli                                                   # noqa: E402
import _schema                                                # noqa: E402
import _state                                                 # noqa: E402

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
SCHEMA_PATH = PLUGIN / "schemas" / "verdict.schema.json"
FIXTURES = PLUGIN / "evals" / "fixtures" / "charter-panel-lot"

# Ordered: the first kind present among the disputed findings decides the route,
# because a numeric claim is the one a script can settle outright.
ROUTES: list[tuple[str, str, str]] = [
    ("numeric", "tick_and_tie.py",
     "a numeric claim is settled by recomputing the figure from the originating "
     "record, within the tolerance the warrant declares"),
    ("missing-element", "lineage_gate.py",
     "a missing-element claim is settled by walking the render tree for the "
     "element and its provenance token"),
    ("classification", "taxonomy_check.py",
     "a classification claim is settled by validating the field against the "
     "schema that governs it"),
]

# An `other` finding whose text carries a settleable claim is routed on the text
# rather than parked with a human. Recorded as inferred, so a reader can see the
# route did not come from the lane's own label.
INFERENCE: list[tuple[str, re.Pattern[str]]] = [
    ("numeric", re.compile(r"(\d[\d,.]*\s*%|\bdoes not tie\b|\bties? to\b|"
                           r"\btotals?\b|\bsums?\b|\brecomputed?\b|\bmismatch of\b)",
                           re.I)),
    ("missing-element", re.compile(r"\b(missing|absent|not rendered|no provenance|"
                                   r"not present|omitted)\b", re.I)),
    ("classification", re.compile(r"\b(wrong field|misclassif\w+|classified as|"
                                  r"category|taxonomy|schema field)\b", re.I)),
]


def load_schema() -> dict[str, object]:
    return json.loads(SCHEMA_PATH.read_text())


def _signature(finding: dict[str, object]) -> tuple[str, str]:
    statement = re.sub(r"\s+", " ", str(finding.get("statement", ""))).strip().lower()
    return str(finding.get("kind", "")), statement


def effective_kind(finding: dict[str, object]) -> tuple[str, bool]:
    """The finding's kind, or an inferred one when the lane said `other`."""
    kind = str(finding.get("kind", "other"))
    if kind != "other":
        return kind, False
    text = f"{finding.get('statement', '')} {finding.get('evidence', '')}"
    for candidate, pattern in INFERENCE:
        if pattern.search(text):
            return candidate, True
    return "other", False


def disputed_findings(verdicts: list[dict[str, object]]) -> list[dict[str, object]]:
    """Findings that some lanes report and others do not.

    A finding every lane reports is not in dispute, whatever the states say; a
    finding only one lane reports is the thing the check has to look at.
    """
    sets = [{_signature(f) for f in verdict["findings"]} for verdict in verdicts]
    shared = set.intersection(*sets) if sets else set()
    disputed: list[dict[str, object]] = []
    seen: set[tuple[str, str]] = set()
    for verdict in verdicts:
        for finding in verdict["findings"]:
            sig = _signature(finding)
            if sig in shared or sig in seen:
                continue
            seen.add(sig)
            kind, inferred = effective_kind(finding)
            disputed.append({
                "lane": verdict["lane"],
                "id": finding.get("id"),
                "declared_kind": finding.get("kind"),
                "kind": kind,
                "kind_inferred": inferred,
                "statement": finding.get("statement"),
                "locator": finding.get("locator"),
                "evidence": finding.get("evidence"),
            })
    return disputed


def human_route(root: pathlib.Path, verdicts: list[dict[str, object]],
                reason: str) -> tuple[dict[str, object], str | None]:
    """Resolve the escalation route for the class, by name.

    The warrant is what names a person. Without it there is no route, and a
    routing decision that names nobody is not a route — so that is exit 3.
    """
    classes = {str(v.get("defect_class")) for v in verdicts}
    try:
        warrant = _state.read_warrant(root)
    except _state.Absent as exc:
        return ({"type": "human", "target": None, "reason": reason,
                 "detail": f"no warrant at {exc}, so no escalation route is named"},
                f"no warrant at {exc}")
    owner = warrant.get("owner", {}) if isinstance(warrant.get("owner"), dict) else {}
    named = f"{owner.get('name', '')} <{owner.get('email', '')}>".strip()
    escalations: dict[str, str] = {}
    for cls in warrant.get("classes", []):
        if isinstance(cls, dict):
            escalations[str(cls.get("name"))] = str(cls.get("escalation", "owner"))
    targets: list[str] = []
    for cls in sorted(classes):
        route = escalations.get(cls, "owner")
        targets.append(named if route in ("owner", "", "None") else route)
    target = targets[0] if len(set(targets)) == 1 else ", ".join(sorted(set(targets)))
    if not target.strip(" <>"):
        return ({"type": "human", "target": None, "reason": reason,
                 "detail": "the warrant names no owner"},
                "the warrant names no owner")
    return ({"type": "human", "target": target, "reason": reason,
             "detail": "no deterministic check answers this claim, so it goes to a "
                       "person by name rather than to a vote"}, None)


def extra(p: argparse.ArgumentParser) -> None:
    p.add_argument("--verdict", action="append", default=[], metavar="PATH",
                   help="a lane verdict (repeat; two or more)")
    p.add_argument("--majority", action="store_true",
                   help="refused: see the exit-1 message")


def main(args: argparse.Namespace) -> int:
    root = pathlib.Path(args.root).expanduser().resolve()

    if args.majority:
        _cli.say(args, "refused: this script does not resolve a disagreement by "
                       "majority.")
        _cli.say(args, "  Nine frontier judges from seven families supply about two "
                       "effective independent votes, panel accuracy falls 8 to 22 "
                       "points short of genuinely independent voting, and the best "
                       "single judge matched or outperformed the whole panel across "
                       "every tested condition. Counting lanes buys correlated error.")
        _cli.say(args, "  Run again without --majority and route the disputed claim "
                       "to the check that settles it, or to a named person.")
        _cli.emit(args, {"ok": False, "reason": "majority-refused", "route": None,
                         "winner": None})
        return _cli.ERROR

    if len(args.verdict) < 2:
        _cli.say(args, "pass --verdict twice or more: there is no disagreement in one "
                       "verdict")
        _cli.emit(args, {"ok": False, "reason": "usage", "route": None, "winner": None})
        return _cli.ERROR

    schema = load_schema()
    verdicts: list[dict[str, object]] = []
    for raw in args.verdict:
        path = pathlib.Path(raw).expanduser().resolve()
        if not path.is_file():
            raise _state.Absent(str(path))
        try:
            verdict = json.loads(path.read_text())
        except json.JSONDecodeError as exc:
            _cli.say(args, f"{path} is not JSON: {exc}")
            _cli.emit(args, {"ok": False, "reason": "not-json", "route": None,
                             "winner": None})
            return _cli.ERROR
        violations = _schema.validate(verdict, schema)
        if violations:
            _cli.say(args, f"{path} is not a valid verdict, so it cannot be adjudicated:")
            for v in violations:
                _cli.say(args, f"  {v}")
            _cli.emit(args, {"ok": False, "reason": "schema", "violations": violations,
                             "route": None, "winner": None})
            return _cli.ERROR
        verdicts.append(verdict)

    items = {str(v["item"]) for v in verdicts}
    digests = {str(v["evidence_digest"]) for v in verdicts}
    lanes = [{"lane": v["lane"], "state": v["state"], "findings": len(v["findings"]),
              "defect_class": v["defect_class"]} for v in verdicts]
    lane_ids = [str(v["lane"]) for v in verdicts]
    if len(set(lane_ids)) != len(lane_ids):
        _cli.say(args, "two of these verdicts come from the same lane "
                       f"({', '.join(sorted(lane_ids))})")
        _cli.say(args, "  a lane disagreeing with itself is a re-run, not a "
                       "disagreement between lanes; pass one verdict per lane")
        _cli.emit(args, {"ok": False, "reason": "duplicate-lane", "lanes": lanes,
                         "route": None, "winner": None})
        return _cli.ERROR
    if len(items) > 1 or len(digests) > 1:
        detail = []
        if len(items) > 1:
            detail.append("items " + ", ".join(sorted(items)))
        if len(digests) > 1:
            detail.append("digests " + ", ".join(sorted(d[:12] + "…" for d in digests)))
        _cli.say(args, "these verdicts are not judging the same thing: "
                       + "; ".join(detail))
        _cli.say(args, "  that is not a disagreement to route — one verdict is void. "
                       "Re-run the lanes against one snapshot")
        _cli.emit(args, {"ok": False, "reason": "not-comparable", "detail": detail,
                         "lanes": lanes, "route": None, "winner": None})
        return _cli.FAILED

    states = {str(v["state"]) for v in verdicts}
    disputed = disputed_findings(verdicts)
    if len(states) == 1 and not disputed:
        _cli.say(args, f"no disagreement: {len(verdicts)} lane(s) all say "
                       f"{next(iter(states))} on {next(iter(items))}")
        _cli.emit(args, {"ok": True, "agreement": True, "item": next(iter(items)),
                         "lanes": lanes, "disagreement": None, "route": None,
                         "winner": None})
        return _cli.OK

    kinds = [d["kind"] for d in disputed]
    route: dict[str, object] | None = None
    missing_precondition: str | None = None
    for kind, script, why in ROUTES:
        if kind in kinds:
            picked = next(d for d in disputed if d["kind"] == kind)
            argv = [script, "--root", str(root), "--item", next(iter(items))]
            if picked.get("locator"):
                argv += ["--locator", str(picked["locator"])]
            route = {"type": "deterministic-check", "target": script, "kind": kind,
                     "reason": why, "claim": picked,
                     "argv": argv}
            break
    if route is None:
        reason = ("the disputed claim is perceptual or unclassified; no deterministic "
                  "check answers it"
                  if disputed else
                  "the lanes disagree on the state with no finding between them to "
                  "look at")
        route, missing_precondition = human_route(root, verdicts, reason)

    _cli.say(args, f"item {next(iter(items))}, evidence {next(iter(digests))[:12]}…")
    for lane in lanes:
        _cli.say(args, f"  {lane['lane']:<16} {lane['state']:<13} "
                       f"{lane['findings']} finding(s)")
    _cli.say(args, f"  states in dispute: {', '.join(sorted(states))}")
    for claim in disputed:
        mark = " (kind inferred from the statement)" if claim["kind_inferred"] else ""
        _cli.say(args, f"  disputed [{claim['kind']}]{mark} {claim['id']} "
                       f"from {claim['lane']}: {claim['statement']}")
    if route["type"] == "deterministic-check":
        _cli.say(args, f"route → {route['target']}")
        _cli.say(args, f"  {route['reason']}")
        _cli.say(args, "  " + " ".join(str(a) for a in route["argv"]))
    else:
        _cli.say(args, f"route → {route['target'] or 'NOBODY'} (human)")
        _cli.say(args, f"  {route['reason']}")
        _cli.say(args, f"  {route['detail']}")
    _cli.say(args, "  no winner: this is a route, not a verdict. The disagreement is "
                   "settled by the check or the person, never by counting lanes")

    payload = {
        "ok": missing_precondition is None,
        "agreement": False,
        "item": next(iter(items)),
        "evidence_digest": next(iter(digests)),
        "lanes": lanes,
        "disagreement": {"states": sorted(states), "disputed": disputed},
        "route": route,
        "winner": None,
    }
    if missing_precondition:
        payload["reason"] = missing_precondition
        _cli.say(args, f"  no route could be named: {missing_precondition}")
        _cli.emit(args, payload)
        return _cli.MISSING
    _cli.emit(args, payload)
    return _cli.OK


# ── selftest ─────────────────────────────────────────────────────────────────

def _call(*argv: str) -> tuple[int, str, str]:
    p = _cli.parser("selftest")
    extra(p)
    parsed = p.parse_args(list(argv))
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = _cli.run(main, None, parsed)
    return code, out.getvalue(), err.getvalue()


def F(name: str) -> str:
    return str(FIXTURES / name)


def selftest() -> list[tuple[str, bool]]:
    cases: list[tuple[str, bool]] = []
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="warrant-adjudicate-"))
    try:
        root = tmp / "repo"
        d = _state.state_dir(root, create=True)
        shutil.copy(FIXTURES / "warrant.valid.toml", d / "warrant.toml")

        # A numeric dispute routes to the arithmetic.
        code, out, _ = _call("--root", str(root), "--verdict", F("verdict.pass.json"),
                             "--verdict", F("verdict.fail-numeric.json"))
        cases.append(("a numeric dispute exits 0", code == _cli.OK))
        cases.append(("it routes to tick_and_tie.py", "route → tick_and_tie.py" in out))
        cases.append(("it names no winner",
                      "no winner" in out and "not a verdict" in out))

        # Missing element, classification, perceptual.
        code, out, _ = _call("--root", str(root), "--verdict", F("verdict.pass.json"),
                             "--verdict", F("verdict.fail-missing.json"))
        cases.append(("a missing-element dispute routes to lineage_gate.py",
                      code == _cli.OK and "route → lineage_gate.py" in out))
        code, out, _ = _call("--root", str(root), "--verdict", F("verdict.pass.json"),
                             "--verdict", F("verdict.fail-classification.json"))
        cases.append(("a classification dispute routes to taxonomy_check.py",
                      code == _cli.OK and "route → taxonomy_check.py" in out))
        code, out, _ = _call("--root", str(root), "--verdict", F("verdict.pass.json"),
                             "--verdict", F("verdict.fail-perceptual.json"))
        cases.append(("a perceptual dispute routes to a named human",
                      code == _cli.OK and "Ada Lovelace" in out and "(human)" in out))
        cases.append(("the human route says why no check applies",
                      "no deterministic check answers" in out))

        # An `other` finding whose text carries a numeric claim.
        code, out, _ = _call("--root", str(root), "--verdict", F("verdict.pass.json"),
                             "--verdict", F("verdict.fail-other-numeric.json"))
        cases.append(("an `other` finding with a numeric claim still routes to "
                      "tick_and_tie.py",
                      code == _cli.OK and "route → tick_and_tie.py" in out))
        cases.append(("the inference is disclosed", "kind inferred" in out))

        # A state disagreement with no finding to look at.
        stateless = tmp / "stateless.json"
        payload = json.loads((FIXTURES / "verdict.pass.json").read_text())
        payload["state"] = "fail"
        payload["lane"] = "lens-lineage"
        stateless.write_text(json.dumps(payload))
        code, out, _ = _call("--root", str(root), "--verdict", F("verdict.pass.json"),
                             "--verdict", str(stateless))
        cases.append(("a bare state disagreement routes to a human",
                      code == _cli.OK and "(human)" in out
                      and "no finding between them" in out))

        # Agreement is not a disagreement.
        same = tmp / "same.json"
        payload = json.loads((FIXTURES / "verdict.pass.json").read_text())
        payload["lane"] = "lens-lineage"
        same.write_text(json.dumps(payload))
        code, out, _ = _call("--root", str(root), "--verdict", F("verdict.pass.json"),
                             "--verdict", str(same))
        cases.append(("agreement exits 0 with no route",
                      code == _cli.OK and "no disagreement" in out))

        # A finding both lanes report is not in dispute.
        both = tmp / "both.json"
        payload = json.loads((FIXTURES / "verdict.fail-numeric.json").read_text())
        payload["lane"] = "grader-primary"
        both.write_text(json.dumps(payload))
        code, out, _ = _call("--root", str(root),
                             "--verdict", F("verdict.fail-numeric.json"),
                             "--verdict", str(both))
        cases.append(("a finding both lanes report is not a dispute",
                      code == _cli.OK and "no disagreement" in out))
        dupe = tmp / "dupe.json"
        payload = json.loads((FIXTURES / "verdict.fail-numeric.json").read_text())
        payload["state"] = "pass"
        payload["findings"] = []
        dupe.write_text(json.dumps(payload))
        code, out, _ = _call("--root", str(root),
                             "--verdict", F("verdict.fail-numeric.json"),
                             "--verdict", str(dupe))
        cases.append(("two verdicts from the same lane exit 1",
                      code == _cli.ERROR and "same lane" in out))

        # The refusal.
        code, out, _ = _call("--root", str(root), "--verdict", F("verdict.pass.json"),
                             "--verdict", F("verdict.fail-numeric.json"), "--majority")
        cases.append(("--majority exits 1", code == _cli.ERROR))
        cases.append(("the refusal gives the reason",
                      "does not resolve a disagreement by majority" in out
                      and "correlated error" in out))
        cases.append(("the refusal routes nothing", "route →" not in out))
        code, o, _ = _call("--root", str(root), "--verdict", F("verdict.pass.json"),
                           "--verdict", F("verdict.fail-numeric.json"), "--majority",
                           "--json")
        cases.append(("the refusal emits no winner under --json",
                      json.loads(o)["winner"] is None
                      and json.loads(o)["route"] is None))

        # Not comparable.
        other_item = tmp / "other-item.json"
        payload = json.loads((FIXTURES / "verdict.fail-numeric.json").read_text())
        payload["item"] = "WEB-9999"
        other_item.write_text(json.dumps(payload))
        code, out, _ = _call("--root", str(root), "--verdict", F("verdict.pass.json"),
                             "--verdict", str(other_item))
        cases.append(("verdicts on different items exit 2",
                      code == _cli.FAILED and "not judging the same thing" in out))
        other_digest = tmp / "other-digest.json"
        payload = json.loads((FIXTURES / "verdict.fail-numeric.json").read_text())
        payload["evidence_digest"] = "a" * 64
        other_digest.write_text(json.dumps(payload))
        code, out, _ = _call("--root", str(root), "--verdict", F("verdict.pass.json"),
                             "--verdict", str(other_digest))
        cases.append(("verdicts on different digests exit 2",
                      code == _cli.FAILED and "digests" in out))

        # Usage and preconditions.
        code, out, _ = _call("--root", str(root), "--verdict", F("verdict.pass.json"))
        cases.append(("one verdict exits 1", code == _cli.ERROR))
        code, out, _ = _call("--root", str(root), "--verdict", F("verdict.invalid.json"),
                             "--verdict", F("verdict.pass.json"))
        cases.append(("a verdict that fails the schema exits 1", code == _cli.ERROR))
        code, out, _ = _call("--root", str(root), "--verdict", str(tmp / "nope.json"),
                             "--verdict", F("verdict.pass.json"))
        cases.append(("a verdict file that does not exist exits 3", code == _cli.MISSING))
        bare = tmp / "bare"
        bare.mkdir()
        code, out, _ = _call("--root", str(bare), "--verdict", F("verdict.pass.json"),
                             "--verdict", F("verdict.fail-perceptual.json"))
        cases.append(("a human route with no warrant to name anyone exits 3",
                      code == _cli.MISSING and "no route could be named" in out))
        cases.append(("a check route needs no warrant",
                      _call("--root", str(bare), "--verdict", F("verdict.pass.json"),
                            "--verdict", F("verdict.fail-numeric.json"))[0] == _cli.OK))

        code, o, _ = _call("--root", str(root), "--verdict", F("verdict.pass.json"),
                           "--verdict", F("verdict.fail-numeric.json"), "--json")
        payload = json.loads(o)
        cases.append(("--json puts only JSON on stdout", o.lstrip().startswith("{")))
        cases.append(("the JSON route is a check, not a winner",
                      payload["route"]["target"] == "tick_and_tie.py"
                      and payload["winner"] is None))
        cases.append(("the JSON names the disputed claim",
                      payload["disagreement"]["disputed"][0]["kind"] == "numeric"))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return cases


if __name__ == "__main__":
    raise SystemExit(_cli.entry(__doc__ or "", main, selftest, extra))
