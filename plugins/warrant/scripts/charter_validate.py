#!/usr/bin/env python3
"""The plugin's outermost gate on `.warrant/warrant.toml`.

Everything else refuses to run if this exits non-zero, so it fails loudly and
names the key. Exit 2 on any of:

  owner.unnamed              [owner] has no name or no email
  renewal.expired            the renewal date has passed, or is not a date
  lot.tolerable_error_rate   the rate is missing, or outside (0,1)
  version.missing            no warrant version for a ledger row to cite
  lanes.model-unpinned       a lane has no model id, no version, or a floating one
  lanes.class-absent         a lane names a class the warrant does not carry
  lanes.absent               a class sits above tier 0 with no pinned lane at all
  classes.tier-unearned      a class holds a tier whose entry condition is unmet

Exit 3 when there is no warrant at all: a missing file is not a failed gate, and
a caller that treats them alike either blocks on nothing or passes on nothing.

Tier entry is judged from evidence the other planes write. The shapes read here,
all under `.warrant/` and all optional-with-consequence (absent evidence is an
unmet condition, never a pass):

  oracle-coverage.json  {"classes": {"<class>": {"figures": N,
                                                 "figures_with_source": K}}}
                        or {"classes": {"<class>": {"coverage": 0.98}}}
  suite-health.json     {"green": true}         (or "assay_green")
  regression-run.json   {"classes": {"<class>": {"cases": N, "recaught": K}}}
                        or {"cases": N, "missed": 0}
  ledger.jsonl          rows with a class, a tier, a state and a timestamp
  escapes.jsonl         rows with a class and a timestamp
"""

from __future__ import annotations

import argparse
import contextlib
import datetime as _dt
import io
import pathlib
import shutil
import sys
import tempfile
from typing import Any

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import _cli                                                   # noqa: E402
import _state                                                 # noqa: E402

FIXTURES = pathlib.Path(__file__).resolve().parent.parent / "evals" / "fixtures" / "charter-panel-lot"

# A version that moves under the warrant is a control that changed, so an alias
# that can point somewhere new tomorrow is not a pin.
FLOATING = {"latest", "stable", "current", "head", "main", "*", "", "auto", "default"}


def _as_date(value: Any) -> _dt.date | None:
    if isinstance(value, _dt.datetime):
        return value.date()
    if isinstance(value, _dt.date):
        return value
    if isinstance(value, str):
        try:
            return _dt.date.fromisoformat(value.strip()[:10])
        except ValueError:
            return None
    return None


def _as_ts(value: Any) -> _dt.datetime | None:
    if isinstance(value, _dt.datetime):
        return value if value.tzinfo else value.replace(tzinfo=_dt.timezone.utc)
    if isinstance(value, _dt.date):
        return _dt.datetime(value.year, value.month, value.day, tzinfo=_dt.timezone.utc)
    if isinstance(value, str):
        try:
            out = _dt.datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
        except ValueError:
            return None
        return out if out.tzinfo else out.replace(tzinfo=_dt.timezone.utc)
    return None


def _first(mapping: dict[str, Any], *keys: str, default: Any = None) -> Any:
    for key in keys:
        if key in mapping:
            return mapping[key]
    return default


# ── evidence readers ─────────────────────────────────────────────────────────

class Evidence:
    """Whatever the other planes have written, read defensively.

    Nothing here raises on an absent or malformed file. An unreadable piece of
    evidence is reported as unavailable, and an unmet condition, because a gate
    that treats missing evidence as a pass is not a gate.
    """

    def __init__(self, root: pathlib.Path) -> None:
        self.root = root
        self.d = _state.state_dir(root)
        self.notes: list[str] = []
        self.coverage = self._read("oracle-coverage.json")
        self.suite = self._read("suite-health.json")
        self.regression = self._read("regression-run.json")
        self.ledger = _state.read_jsonl(self.d / "ledger.jsonl")
        self.escapes = _state.read_jsonl(self.d / "escapes.jsonl")

    def _read(self, name: str) -> dict[str, Any] | None:
        path = self.d / name
        if not path.exists():
            return None
        try:
            payload = _state.read_json(path)
        except Exception as exc:                               # noqa: BLE001
            self.notes.append(f"{name} is unreadable ({type(exc).__name__}); "
                              "treated as absent")
            return None
        return payload if isinstance(payload, dict) else None

    def _class_block(self, payload: dict[str, Any] | None, name: str) -> dict[str, Any] | None:
        if not payload:
            return None
        classes = payload.get("classes")
        if isinstance(classes, dict) and isinstance(classes.get(name), dict):
            return classes[name]
        if isinstance(payload.get(name), dict):
            return payload[name]
        return None

    def oracle_coverage(self, name: str) -> tuple[float | None, int | None, int | None]:
        block = self._class_block(self.coverage, name)
        if block is None:
            return None, None, None
        num = _first(block, "figures_with_source", "sourced", "with_source", "recaught")
        den = _first(block, "figures", "total", "rendered_figures")
        if isinstance(num, int) and isinstance(den, int) and den > 0:
            return num / den, num, den
        cov = block.get("coverage")
        if isinstance(cov, (int, float)) and not isinstance(cov, bool):
            return float(cov), None, None
        return None, None, None

    def assay_green(self) -> bool | None:
        if not self.suite:
            return None
        value = _first(self.suite, "green", "assay_green", "ratchet_ok")
        return bool(value) if isinstance(value, bool) else None

    def recatch(self, name: str) -> tuple[float | None, int | None, int | None]:
        block = self._class_block(self.regression, name)
        if block is None:
            block = self.regression if isinstance(self.regression, dict) else None
            if block is None or "cases" not in block:
                return None, None, None
        cases = _first(block, "cases", "total")
        recaught = _first(block, "recaught", "caught")
        if recaught is None and isinstance(cases, int) and isinstance(_first(block, "missed"), int):
            recaught = cases - int(_first(block, "missed"))
        if isinstance(cases, int) and isinstance(recaught, int) and cases > 0:
            return recaught / cases, recaught, cases
        if isinstance(cases, int) and cases == 0:
            # No historical escape in the class is not evidence that the machine
            # re-catches them; it is an empty corpus.
            return None, 0, 0
        return None, None, None

    def closed_in_window(self, name: str, since: _dt.datetime) -> int:
        total = 0
        for row in self.ledger:
            if not isinstance(row, dict) or "_malformed" in row:
                continue
            if _first(row, "defect_class", "class") != name:
                continue
            state = str(_first(row, "state", "verdict", default="")).lower()
            if state not in ("pass", "fail", "closed"):
                continue
            tier = _first(row, "tier", "authorised_tier", default=0)
            try:
                tier_i = int(tier)
            except (TypeError, ValueError):
                tier_i = 0
            if tier_i < 1:
                continue
            ts = _as_ts(_first(row, "ts", "at", "timestamp"))
            if ts is None or ts < since:
                continue
            total += 1
        return total

    def escapes_in_window(self, name: str, since: _dt.datetime) -> int:
        total = 0
        for row in self.escapes:
            if not isinstance(row, dict) or "_malformed" in row:
                continue
            if _first(row, "defect_class", "class") != name:
                continue
            ts = _as_ts(_first(row, "ts", "at", "timestamp"))
            if ts is None or ts < since:
                continue
            total += 1
        return total


# ── the checks ───────────────────────────────────────────────────────────────

def _fail(findings: list[dict[str, str]], rule: str, key: str, detail: str, fix: str) -> None:
    findings.append({"rule": rule, "key": key, "detail": detail, "fix": fix})


def check_owner(warrant: dict[str, Any], findings: list[dict[str, str]]) -> None:
    owner = warrant.get("owner")
    if not isinstance(owner, dict):
        _fail(findings, "owner.unnamed", "owner",
              "there is no [owner] table",
              "add [owner] with a name and an email for the person answerable")
        return
    if not str(owner.get("name", "")).strip():
        _fail(findings, "owner.unnamed", "owner.name",
              "the warrant names nobody",
              "set owner.name to a person; a role with no current holder is a "
              "warrant with no signature")
    if not str(owner.get("email", "")).strip():
        _fail(findings, "owner.unnamed", "owner.email",
              "the owner has no contact address",
              "set owner.email so an escalation has somewhere to go")


def check_renewal(warrant: dict[str, Any], today: _dt.date,
                  findings: list[dict[str, str]]) -> None:
    raw = warrant.get("renewal")
    if raw is None:
        _fail(findings, "renewal.expired", "renewal", "no renewal date",
              "set renewal to an ISO date in the future")
        return
    when = _as_date(raw)
    if when is None:
        _fail(findings, "renewal.expired", "renewal",
              f"{raw!r} is not an ISO date",
              "set renewal to YYYY-MM-DD")
        return
    if when < today:
        _fail(findings, "renewal.expired", "renewal",
              f"expired {(today - when).days} day(s) ago on {when.isoformat()}",
              "re-sign the warrant and move renewal forward; a warrant past "
              "renewal is not a warrant")


def check_rate(warrant: dict[str, Any], findings: list[dict[str, str]]) -> None:
    lot = warrant.get("lot")
    if not isinstance(lot, dict) or "tolerable_error_rate" not in lot:
        _fail(findings, "lot.tolerable_error_rate", "lot.tolerable_error_rate",
              "absent, so no sample size can be computed",
              "set lot.tolerable_error_rate to a proportion in (0,1) — it is the "
              "risk you are choosing to run on the queue")
        return
    raw = lot["tolerable_error_rate"]
    if isinstance(raw, bool) or not isinstance(raw, (int, float)):
        _fail(findings, "lot.tolerable_error_rate", "lot.tolerable_error_rate",
              f"{raw!r} is not a number",
              "set it to a proportion in (0,1), for example 0.05")
        return
    if not (0.0 < float(raw) < 1.0):
        _fail(findings, "lot.tolerable_error_rate", "lot.tolerable_error_rate",
              f"{raw} is outside (0,1)",
              "0 means nothing is tolerable and 1 means everything is; neither "
              "sizes a sample. Use a proportion, not a percentage")


def check_version(warrant: dict[str, Any], findings: list[dict[str, str]]) -> None:
    if not str(warrant.get("version", "")).strip():
        _fail(findings, "version.missing", "version",
              "no warrant version",
              "set version; every ledger row cites it, and a warrant that cannot "
              "be cited cannot be audited")


def check_lanes(root: pathlib.Path, warrant: dict[str, Any],
                findings: list[dict[str, str]]) -> dict[str, Any] | None:
    warrant_classes = {str(c.get("name")) for c in warrant.get("classes", [])
                       if isinstance(c, dict)}
    above_zero = sorted(str(c.get("name")) for c in warrant.get("classes", [])
                        if isinstance(c, dict) and int(c.get("tier", 0) or 0) > 0)
    path = _state.lanes_path(root)
    if not path.exists():
        if above_zero:
            _fail(findings, "lanes.absent", "lanes.toml",
                  "no lanes file, yet " + ", ".join(above_zero)
                  + " sit above tier 0",
                  "write .warrant/lanes.toml pinning a model id and version per "
                  "lane, or drop those classes to tier 0 — a class the machine "
                  "may close with no pinned lane is an unpinned control")
        return None
    try:
        lanes = _state.read_toml(path)
    except Exception as exc:                                   # noqa: BLE001
        _fail(findings, "lanes.model-unpinned", "lanes.toml",
              f"unreadable: {type(exc).__name__}: {exc}",
              "fix the TOML; the gate cannot confirm any model is pinned")
        return None

    entries = lanes.get("lanes")
    if not isinstance(entries, list) or not entries:
        _fail(findings, "lanes.model-unpinned", "lanes",
              "lanes.toml carries no [[lanes]] block",
              "add one [[lanes]] block per lane with id, model and version")
        return lanes

    for i, lane in enumerate(entries):
        if not isinstance(lane, dict):
            _fail(findings, "lanes.model-unpinned", f"lanes[{i}]",
                  "not a table", "each lane is a [[lanes]] table")
            continue
        lane_id = str(lane.get("id") or f"lanes[{i}]")
        model = str(lane.get("model", "")).strip()
        version = str(lane.get("version", "")).strip()
        if not model:
            _fail(findings, "lanes.model-unpinned", f"lanes.{lane_id}.model",
                  "no model id",
                  "pin the model id; a lane whose model moves has changed the control")
        elif model.rsplit(":", 1)[-1].lower() in FLOATING or model.endswith("*"):
            _fail(findings, "lanes.model-unpinned", f"lanes.{lane_id}.model",
                  f"{model!r} is a floating alias",
                  "pin an immutable model id, not an alias that can point "
                  "somewhere else tomorrow")
        if not version:
            _fail(findings, "lanes.model-unpinned", f"lanes.{lane_id}.version",
                  "no model version",
                  "pin the version. An auditor leaning on last period's testing "
                  "has to see the control has not changed")
        elif version.lower() in FLOATING:
            _fail(findings, "lanes.model-unpinned", f"lanes.{lane_id}.version",
                  f"{version!r} is a floating version",
                  "pin a concrete version string")

        for name in lane.get("classes", []) or []:
            if str(name) not in warrant_classes:
                _fail(findings, "lanes.class-absent", f"lanes.{lane_id}.classes",
                      f"lane names the class {str(name)!r}, which the warrant "
                      "does not carry",
                      f"add a [[classes]] block for {str(name)!r} to the warrant, "
                      "or remove it from the lane — an unnamed class defaults to "
                      "tier 0 and no machine may close it")
    return lanes


def check_tiers(warrant: dict[str, Any], ev: Evidence, now: _dt.datetime,
                findings: list[dict[str, str]]) -> list[dict[str, Any]]:
    """A class may hold a tier only where the tier's entry condition is met."""
    tiers = warrant.get("tiers", {}) if isinstance(warrant.get("tiers"), dict) else {}
    oracle = warrant.get("oracle", {}) if isinstance(warrant.get("oracle"), dict) else {}
    cov_min = float(_first(tiers, "tier1_oracle_coverage_min",
                           default=_first(oracle, "lineage_coverage_min", default=0.95)))
    recatch_min = float(_first(tiers, "tier2_regression_recatch_min", default=1.0))
    needs_assay = bool(_first(tiers, "tier2_requires_assay_green", default=True))
    items_min = int(_first(tiers, "tier3_items_closed_min", default=200))
    window_days = int(_first(tiers, "tier3_window_days", default=90))
    tier4_reachable = bool(_first(tiers, "tier4_reachable", default=False))
    since = now - _dt.timedelta(days=window_days)

    ladder: list[dict[str, Any]] = []
    for i, cls in enumerate(warrant.get("classes", [])):
        if not isinstance(cls, dict):
            _fail(findings, "classes.tier-unearned", f"classes[{i}]",
                  "not a table", "each class is a [[classes]] table")
            continue
        name = str(cls.get("name", "")).strip()
        key = f"classes.{name or i}.tier"
        if not name:
            _fail(findings, "classes.tier-unearned", f"classes[{i}].name",
                  "a class with no name", "name the class")
            continue
        if not str(cls.get("escalation", "")).strip():
            _fail(findings, "classes.tier-unearned", f"classes.{name}.escalation",
                  "no escalation route",
                  "name where a failed or inconclusive item in this class goes")
        try:
            tier = int(cls.get("tier", 0))
        except (TypeError, ValueError):
            _fail(findings, "classes.tier-unearned", key,
                  f"tier {cls.get('tier')!r} is not an integer", "use 0-4")
            continue

        row: dict[str, Any] = {"class": name, "tier": tier, "evidence": []}
        ladder.append(row)

        if tier < 0 or tier > 4:
            _fail(findings, "classes.tier-unearned", key,
                  f"tier {tier} is not on the ladder", "use 0-4")
            continue
        if tier == 0:
            row["evidence"].append("tier 0 is advisory; no entry condition")
            continue

        # tier 1 and above: the oracle plane must be green on this class.
        cov, num, den = ev.oracle_coverage(name)
        if cov is None:
            _fail(findings, "classes.tier-unearned", key,
                  f"tier {tier} needs oracle coverage for {name!r} and "
                  ".warrant/oracle-coverage.json carries none",
                  f"run the oracle plane until coverage for {name!r} is recorded, "
                  "or set tier = 0")
            continue
        row["evidence"].append(
            _cli.rate(num, den, f"figures on {name} carry a source")
            if num is not None and den is not None
            else f"coverage {cov:.3f} for {name} (no population recorded)")
        if cov < cov_min:
            _fail(findings, "classes.tier-unearned", key,
                  f"tier {tier} needs coverage >= {cov_min}; "
                  + (_cli.rate(num, den, "figures carry a source")
                     if num is not None and den is not None else f"have {cov:.3f}"),
                  "close the lineage gaps or set tier = 0. Any lineage gap is also "
                  "the automatic exit from tier 1")
            continue

        if tier >= 2:
            green = ev.assay_green()
            if needs_assay and green is not True:
                _fail(findings, "classes.tier-unearned", key,
                      f"tier {tier} needs a green assay and "
                      ".warrant/suite-health.json says "
                      + ("nothing" if green is None else str(green)),
                      "run the assay plane. Every downstream verdict inherits the "
                      "suite's fault sensitivity, and a green suite can have little")
                continue
            row["evidence"].append("assay green")
            recatch, recaught, cases = ev.recatch(name)
            if recatch is None:
                _fail(findings, "classes.tier-unearned", key,
                      f"tier {tier} needs every historical escape in {name!r} "
                      "re-caught, and .warrant/regression-run.json records "
                      + ("an empty corpus" if cases == 0 else "no result for it"),
                      "run regress_run.py against the current lanes; an empty "
                      "corpus is not evidence that the machine re-catches anything")
                continue
            row["evidence"].append(_cli.rate(recaught, cases,
                                             f"historical escapes in {name} re-caught"))
            if recatch < recatch_min:
                _fail(findings, "classes.tier-unearned", key,
                      f"tier {tier} needs re-catch >= {recatch_min}; "
                      + _cli.rate(recaught, cases, "escapes re-caught"),
                      "a class may only be closed by machine while the machine "
                      "catches everything it has previously missed in that class")
                continue

        if tier >= 3:
            closed = ev.closed_in_window(name, since)
            escaped = ev.escapes_in_window(name, since)
            row["evidence"].append(
                f"{closed} item(s) closed in {name} over {window_days} day(s), "
                f"{escaped} escape(s)")
            if closed < items_min:
                _fail(findings, "classes.tier-unearned", key,
                      f"tier 3 needs {items_min} item(s) closed in {name!r} over "
                      f"{window_days} day(s); the ledger carries {closed}",
                      "keep the class at tier 2 until the count is there. This "
                      "condition is absence of escapes rather than a measured "
                      "sensitivity, so it gains weight from volume and time")
                continue
            if escaped:
                _fail(findings, "classes.tier-unearned", key,
                      f"tier 3 needs zero escapes in {name!r} over "
                      f"{window_days} day(s); the corpus carries {escaped}",
                      "one escape in a tier-3 class is its automatic exit; drop "
                      "to tier 2 and recalibrate")
                continue

        if tier >= 4 and not tier4_reachable:
            _fail(findings, "classes.tier-unearned", key,
                  "tier 4 is unreachable on current evidence "
                  "(tiers.tier4_reachable = false)",
                  "nothing supports letting a machine close disclosure content: "
                  "tenant-authored text renders into the very capture a vision "
                  "judge reads, and that channel is unmeasured here")
    return ladder


# ── main ─────────────────────────────────────────────────────────────────────

def main(args: argparse.Namespace) -> int:
    root = pathlib.Path(args.root).expanduser().resolve()
    path = _state.warrant_path(root)
    if not path.exists():
        _cli.say(args, f"no warrant at {path}")
        _cli.say(args, "run charter_init.py to draft one, then have a named person "
                       "sign it by committing it")
        _cli.emit(args, {"ok": False, "warrant": str(path), "reason": "absent",
                         "findings": []})
        return _cli.MISSING

    warrant = _state.read_toml(path)
    now = _cli.now(args)
    ev = Evidence(root)
    findings: list[dict[str, str]] = []

    check_version(warrant, findings)
    check_owner(warrant, findings)
    check_renewal(warrant, now.date(), findings)
    check_rate(warrant, findings)
    check_lanes(root, warrant, findings)
    ladder = check_tiers(warrant, ev, now, findings)

    for note in ev.notes:
        _cli.say(args, f"note: {note}")
    for row in ladder:
        _cli.say(args, f"  tier {row['tier']}  {row['class']}"
                       + ("  — " + "; ".join(row["evidence"]) if row["evidence"] else ""))

    if findings:
        _cli.say(args, f"warrant REJECTED: {len(findings)} finding(s)")
        for f in findings:
            _cli.say(args, f"  [{f['rule']}] {f['key']}: {f['detail']}")
            _cli.say(args, f"      fix: {f['fix']}")
    else:
        _cli.say(args, f"warrant accepted: {path}")
        _cli.say(args, f"  owner {warrant['owner']['name']} <{warrant['owner']['email']}>"
                       f", renewal {_as_date(warrant['renewal'])}")

    _cli.emit(args, {
        "ok": not findings,
        "warrant": str(path),
        "version": warrant.get("version"),
        "checked_at": now.isoformat(),
        "ladder": ladder,
        "findings": findings,
        "notes": ev.notes,
    })
    return _cli.FAILED if findings else _cli.OK


# ── selftest ─────────────────────────────────────────────────────────────────

def _call(*argv: str) -> tuple[int, str, str]:
    parsed = _cli.parser("selftest").parse_args(list(argv))
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = _cli.run(main, None, parsed)
    return code, out.getvalue(), err.getvalue()


NOW = "2026-08-19T00:00:00+00:00"


def _root(tmp: pathlib.Path, name: str, *, lanes: bool = True,
          evidence: tuple[str, ...] = ("oracle-coverage.json", "suite-health.json",
                                       "regression-run.json")) -> pathlib.Path:
    root = tmp / name
    d = _state.state_dir(root, create=True)
    shutil.copy(FIXTURES / "warrant.valid.toml", d / "warrant.toml")
    if lanes:
        shutil.copy(FIXTURES / "lanes.valid.toml", d / "lanes.toml")
    for item in evidence:
        shutil.copy(FIXTURES / item, d / item)
    return root


def _edit(root: pathlib.Path, old: str, new: str, which: str = "warrant.toml") -> None:
    path = _state.state_dir(root) / which
    text = path.read_text()
    if old not in text:
        raise AssertionError(f"fixture drift: {old!r} not in {which}")
    path.write_text(text.replace(old, new, 1))


def _fired(rule: str, code: int, out: str) -> bool:
    return code == _cli.FAILED and f"[{rule}]" in out


def selftest() -> list[tuple[str, bool]]:
    cases: list[tuple[str, bool]] = []
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="warrant-charter-validate-"))
    try:
        # The baseline every failure case is measured against.
        base = _root(tmp, "valid")
        code, out, _ = _call("--root", str(base), "--now", NOW)
        cases.append(("a sound warrant is accepted", code == _cli.OK))
        cases.append(("acceptance names the owner", "Ada Lovelace" in out))

        empty = tmp / "empty"
        empty.mkdir()
        code, out, _ = _call("--root", str(empty), "--now", NOW)
        cases.append(("no warrant at all exits 3", code == _cli.MISSING))
        cases.append(("exit 3 is not exit 2", code != _cli.FAILED))

        # 1. an unpinned model in lanes.toml
        r = _root(tmp, "unpinned-version")
        _edit(r, 'version = "2026-06-01"', 'version = "latest"', "lanes.toml")
        code, out, _ = _call("--root", str(r), "--now", NOW)
        cases.append(("floating lane version fires",
                      _fired("lanes.model-unpinned", code, out)))
        r = _root(tmp, "unpinned-missing")
        _edit(r, 'version = "2026-06-01"\n', "", "lanes.toml")
        code, out, _ = _call("--root", str(r), "--now", NOW)
        cases.append(("absent lane version fires",
                      _fired("lanes.model-unpinned", code, out)))
        r = _root(tmp, "unpinned-alias")
        _edit(r, 'model = "example/grader-v2"', 'model = "example/grader:latest"',
              "lanes.toml")
        code, out, _ = _call("--root", str(r), "--now", NOW)
        cases.append(("floating model alias fires",
                      _fired("lanes.model-unpinned", code, out)))
        cases.append(("a pinned lane does not fire the unpinned rule",
                      "[lanes.model-unpinned]" not in _call("--root", str(base),
                                                            "--now", NOW)[1]))

        # 2. a class at a tier whose entry condition is unmet
        r = _root(tmp, "tier1-no-evidence", evidence=("suite-health.json",
                                                      "regression-run.json"))
        code, out, _ = _call("--root", str(r), "--now", NOW)
        cases.append(("tier 1 with no oracle coverage fires",
                      _fired("classes.tier-unearned", code, out)))
        r = _root(tmp, "tier1-low")
        (_state.state_dir(r) / "oracle-coverage.json").write_text(
            '{"classes": {"figure-lineage": {"figures": 120, '
            '"figures_with_source": 90}, "render-fidelity": '
            '{"figures": 100, "figures_with_source": 97}}}')
        code, out, _ = _call("--root", str(r), "--now", NOW)
        cases.append(("tier 1 below the coverage threshold fires",
                      _fired("classes.tier-unearned", code, out)))
        cases.append(("the coverage finding carries its denominator",
                      "90 of 120" in out))
        r = _root(tmp, "tier2-no-assay")
        (_state.state_dir(r) / "suite-health.json").write_text('{"green": false}')
        code, out, _ = _call("--root", str(r), "--now", NOW)
        cases.append(("tier 2 without a green assay fires",
                      _fired("classes.tier-unearned", code, out)))
        r = _root(tmp, "tier2-miss")
        (_state.state_dir(r) / "regression-run.json").write_text(
            '{"classes": {"render-fidelity": {"cases": 12, "recaught": 11}}}')
        code, out, _ = _call("--root", str(r), "--now", NOW)
        cases.append(("tier 2 with an escape no longer caught fires",
                      _fired("classes.tier-unearned", code, out)
                      and "11 of 12" in out))
        r = _root(tmp, "tier3-thin")
        _edit(r, 'name = "render-fidelity"\ntier = 2', 'name = "render-fidelity"\ntier = 3')
        code, out, _ = _call("--root", str(r), "--now", NOW)
        cases.append(("tier 3 without the declared item count fires",
                      _fired("classes.tier-unearned", code, out)))
        r = _root(tmp, "tier3-met")
        _edit(r, 'name = "render-fidelity"\ntier = 2', 'name = "render-fidelity"\ntier = 3')
        _edit(r, "tier3_items_closed_min = 200", "tier3_items_closed_min = 2")
        led = _state.state_dir(r) / "ledger.jsonl"
        for i in range(3):
            _state.append_jsonl(led, {"item": f"I-{i}", "defect_class": "render-fidelity",
                                      "state": "pass", "tier": 2,
                                      "ts": "2026-08-15T00:00:00+00:00"})
        code, out, _ = _call("--root", str(r), "--now", NOW)
        cases.append(("tier 3 with the count met is accepted", code == _cli.OK))
        _state.append_jsonl(_state.state_dir(r) / "escapes.jsonl",
                            {"defect_class": "render-fidelity",
                             "ts": "2026-08-16T00:00:00+00:00"})
        code, out, _ = _call("--root", str(r), "--now", NOW)
        cases.append(("one escape in a tier-3 class fires",
                      _fired("classes.tier-unearned", code, out)))
        r = _root(tmp, "tier4")
        _edit(r, 'name = "disclosure-content"\ntier = 0',
              'name = "disclosure-content"\ntier = 4')
        code, out, _ = _call("--root", str(r), "--now", NOW)
        cases.append(("tier 4 is unreachable and fires",
                      _fired("classes.tier-unearned", code, out)))
        r = _root(tmp, "tier-nonsense")
        _edit(r, 'name = "figure-lineage"\ntier = 1', 'name = "figure-lineage"\ntier = 9')
        code, out, _ = _call("--root", str(r), "--now", NOW)
        cases.append(("a tier off the ladder fires",
                      _fired("classes.tier-unearned", code, out)))

        # 3. a missing or unnamed owner
        r = _root(tmp, "owner-blank")
        _edit(r, 'name = "Ada Lovelace"', 'name = ""')
        code, out, _ = _call("--root", str(r), "--now", NOW)
        cases.append(("a blank owner name fires", _fired("owner.unnamed", code, out)))
        r = _root(tmp, "owner-noemail")
        _edit(r, 'email = "ada@example.test"', 'email = "   "')
        code, out, _ = _call("--root", str(r), "--now", NOW)
        cases.append(("a blank owner email fires", _fired("owner.unnamed", code, out)))
        r = _root(tmp, "owner-absent")
        _edit(r, '[owner]\nname = "Ada Lovelace"\nemail = "ada@example.test"\n', "")
        code, out, _ = _call("--root", str(r), "--now", NOW)
        cases.append(("no [owner] table at all fires",
                      _fired("owner.unnamed", code, out)))

        # 4. an expired renewal date
        r = _root(tmp, "renewal-past")
        _edit(r, 'renewal = "2030-02-01"', 'renewal = "2026-08-18"')
        code, out, _ = _call("--root", str(r), "--now", NOW)
        cases.append(("a renewal one day past fires",
                      _fired("renewal.expired", code, out)))
        cases.append(("the same warrant passes before that date",
                      _call("--root", str(r), "--now",
                            "2026-08-17T00:00:00+00:00")[0] == _cli.OK))
        r = _root(tmp, "renewal-junk")
        _edit(r, 'renewal = "2030-02-01"', 'renewal = "soon"')
        code, out, _ = _call("--root", str(r), "--now", NOW)
        cases.append(("a renewal that is not a date fires",
                      _fired("renewal.expired", code, out)))

        # 5. a tolerable error rate outside (0,1)
        for label, value in (("zero", "0.0"), ("one", "1.0"), ("a percentage", "5"),
                             ("negative", "-0.1")):
            r = _root(tmp, f"rate-{label.replace(' ', '-')}")
            _edit(r, "tolerable_error_rate = 0.05", f"tolerable_error_rate = {value}")
            code, out, _ = _call("--root", str(r), "--now", NOW)
            cases.append((f"a tolerable error rate of {label} fires",
                          _fired("lot.tolerable_error_rate", code, out)))
        r = _root(tmp, "rate-absent")
        _edit(r, "tolerable_error_rate = 0.05\n", "")
        code, out, _ = _call("--root", str(r), "--now", NOW)
        cases.append(("an absent tolerable error rate fires",
                      _fired("lot.tolerable_error_rate", code, out)))

        # 6. a class named in lanes.toml but absent from the warrant
        r = _root(tmp, "lane-orphan")
        _edit(r, 'classes = ["figure-lineage", "render-fidelity"]',
              'classes = ["figure-lineage", "tenant-isolation"]', "lanes.toml")
        code, out, _ = _call("--root", str(r), "--now", NOW)
        cases.append(("a lane class absent from the warrant fires",
                      _fired("lanes.class-absent", code, out)))
        cases.append(("the finding names the orphan class", "tenant-isolation" in out))

        # 7. no lanes at all, with a class above tier 0
        r = _root(tmp, "no-lanes", lanes=False)
        code, out, _ = _call("--root", str(r), "--now", NOW)
        cases.append(("no lanes file with a class above tier 0 fires",
                      _fired("lanes.absent", code, out)))
        r = _root(tmp, "no-lanes-tier0", lanes=False)
        _edit(r, 'name = "figure-lineage"\ntier = 1', 'name = "figure-lineage"\ntier = 0')
        _edit(r, 'name = "render-fidelity"\ntier = 2', 'name = "render-fidelity"\ntier = 0')
        code, out, _ = _call("--root", str(r), "--now", NOW)
        cases.append(("no lanes file with every class at tier 0 is accepted",
                      code == _cli.OK))

        # 8. no version
        r = _root(tmp, "no-version")
        _edit(r, 'version = "1"\n', "")
        code, out, _ = _call("--root", str(r), "--now", NOW)
        cases.append(("a warrant with no version fires",
                      _fired("version.missing", code, out)))

        # Reporting shape.
        r = _root(tmp, "json-mode")
        _edit(r, 'name = "Ada Lovelace"', 'name = ""')
        code, o, e = _call("--root", str(r), "--now", NOW, "--json")
        cases.append(("--json puts only JSON on stdout", o.lstrip().startswith("{")
                      and "owner.unnamed" in o and "REJECTED" in e))
        r = _root(tmp, "unreadable-evidence")
        (_state.state_dir(r) / "oracle-coverage.json").write_text("{not json")
        code, out, _ = _call("--root", str(r), "--now", NOW)
        cases.append(("unreadable evidence is an unmet condition, not a pass",
                      _fired("classes.tier-unearned", code, out)
                      and "unreadable" in out))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return cases


if __name__ == "__main__":
    raise SystemExit(_cli.entry(__doc__ or "", main, selftest))
