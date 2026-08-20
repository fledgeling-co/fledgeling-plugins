#!/usr/bin/env python3
"""Gates for a stocktake sweep. Each is judged on exit code alone.

Scoped to what THIS run is answerable for. In a shared checkout a repo-wide
cleanliness check fails for another session's edits and blocks a run on work it
cannot fix, so nothing here reads the whole tree.

  gates.py <gate> <ledger-dir> [--verified-config PATH]

Gates: covered · evidence · inconclusive-reported · ungraded-reported ·
       briefs-written · dispatched · classified · banked · verified-gate · all

`classified` and `banked` decide whether the run FED the warrant or only consulted it.
A sweep produced 241 machine verdicts and appended none of them, so the tier-3 entry
condition — N items closed in a class over a window — counted zero and the ladder could
never move however good the grading was. `warrant_column.py` returns a column and writes
nothing; the append is a separate act, and these gates are what remembers it.

`dispatched` refuses a run that audited the board and handed none of it over. It once
accepted a recorded deferral as equal to a dispatch — which let the party writing the
reasons excuse itself, and one run marked all 61 of its needs-work cards deferred with a
single invented sentence and passed. Words the subject authors cannot gate the subject.

`dispatched` is the one that decides whether the RUN is finished rather than whether the
AUDIT is. Without it every gate here goes green on a sweep that graded the board and
dispatched none of it, because a run that handed 108 cards to ship-fleet and a run that
handed over nothing produce identical output. That happened, which is why it exists.
"""
import argparse, json, os, subprocess, sys

def load(d):
    p = os.path.join(d, "board-triage-ledger.json")
    if not os.path.exists(p):
        fail(f"no ledger at {p} — the sweep has not started")
    with open(p) as f:
        return json.load(f)

def _repo_root(d):
    """Walk up from the ledger dir to the checkout it sits in."""
    cur = os.path.abspath(d)
    while cur != os.path.dirname(cur):
        if os.path.exists(os.path.join(cur, ".git")):
            return cur
        cur = os.path.dirname(cur)
    return None

def resolve_brief(d, b):
    """Briefs are recorded repo-relative, so a bare exists() answers a question about
    the CWD rather than about the brief. Try the path as given, then against the ledger
    dir, then against the checkout — and report not-found only when all three miss."""
    if os.path.isabs(b):
        return b if os.path.exists(b) else None
    root = _repo_root(d)
    for cand in (b, os.path.join(d, b), os.path.join(root, b) if root else None):
        if cand and os.path.exists(cand):
            return cand
    return None

def fail(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)

def g_covered(d, _):
    data = load(d)
    pending = [r["key"] for r in data["rows"] if r["verdict"] is None]
    if pending:
        fail(f"{len(pending)} of {len(data['rows'])} cards have no verdict yet:\n  "
             + "\n  ".join(pending))
    print(f"{len(data['rows'])} cards, all with a verdict")

def g_evidence(d, _):
    data = load(d)
    bad = []
    for r in data["rows"]:
        v = r["verdict"]
        if v == "done" and not (r.get("lane") and r.get("sha")):
            bad.append(f"{r['key']}: done without a lane and a sha")
        if v == "needs-info" and not r.get("question"):
            bad.append(f"{r['key']}: needs-info without a question")
        if v == "inconclusive" and not r.get("note"):
            bad.append(f"{r['key']}: inconclusive without a reason")
        if v == "needs-work" and not r.get("brief"):
            bad.append(f"{r['key']}: needs-work without a brief")
        if v == "ungraded" and not r.get("note"):
            bad.append(f"{r['key']}: ungraded without a note saying which steps were "
                       f"not run — it would read as a graded defect")
        if v and r.get("work_at") is None:
            bad.append(f"{r['key']}: no work-at — where the work lives was never established")
    if bad:
        fail(f"{len(bad)} row(s) claim more than they carry:\n  " + "\n  ".join(bad))
    print(f"{len(data['rows'])} rows check out")

def g_inconclusive_reported(d, _):
    data = load(d)
    inc = [r for r in data["rows"] if r["verdict"] == "inconclusive"]
    thin = [r["key"] for r in inc if len((r.get("note") or "")) < 30]
    if thin:
        fail("an inconclusive row must say what could not be gathered, at length "
             f"enough to act on:\n  " + "\n  ".join(thin))
    # Not a failure — a statement. Inconclusive blocks promotion, not the gate.
    print(f"{len(inc)} inconclusive row(s), each with a reason"
          + (" — these BLOCK promotion" if inc else ""))

def g_briefs_written(d, opts):
    """A brief has to be dispatchable, not merely present.

    The previous version asserted two things: the row carries a brief string, and that
    path exists. Both held for a sweep whose 57 cards all pointed at one 48KB file — and
    ship-fleet fans out per brief, so that is one work item covering 57 cards rather than
    57 items. The gate read as coverage and guaranteed nothing.
    """
    data = load(d)
    cap = getattr(opts, "max_cards_per_brief", None) or 3
    missing, unnamed = [], []
    per_brief = {}
    for r in data["rows"]:
        if r["verdict"] != "needs-work":
            continue
        b = r.get("brief") or ""
        real = resolve_brief(d, b) if b else None
        if not real:
            missing.append(f"{r['key']}: brief {b!r} is not on disk, under the ledger "
                           f"dir, or under the checkout")
            continue
        per_brief.setdefault(b, []).append(r["key"])
        try:
            if r["key"] not in open(real, encoding="utf-8", errors="replace").read():
                unnamed.append(f"{r['key']}: {b} never names this card")
        except OSError as e:
            missing.append(f"{r['key']}: {b} could not be read ({e})")
    crowded = {b: ks for b, ks in per_brief.items() if len(ks) > cap}
    problems = missing + unnamed
    if crowded:
        problems += [f"{b}: serves {len(ks)} cards, over the {cap}-card cap — ship-fleet "
                     f"fans out per brief, so this is one work item, not {len(ks)}"
                     for b, ks in sorted(crowded.items())]
    if problems:
        fail(f"{len(problems)} brief problem(s) — these are not dispatchable:\n  "
             + "\n  ".join(problems))
    n = sum(1 for r in data["rows"] if r["verdict"] == "needs-work")
    print(f"{n} card(s) with work remaining, each with a brief that names it "
          f"and serves at most {cap} card(s)")


def g_ungraded_reported(d, _):
    """Cards the method was never run on, counted out loud.

    Reported rather than failed: a card whose corroboration does not execute is a real
    finding. What it must never do is sit inside the needs-work count, where it reads as
    a defect somebody could go and fix.
    """
    data = load(d)
    ung = [r for r in data["rows"] if r["verdict"] == "ungraded"]
    thin = [r["key"] for r in ung if len((r.get("note") or "")) < 30]
    if thin:
        fail("an ungraded row must say which of steps 1-6 were not run and why:\n  "
             + "\n  ".join(thin))
    print(f"{len(ung)} card(s) were never graded"
          + (" — these are NOT defects and must not be dispatched as work" if ung else ""))


def g_dispatched(d, _):
    """Was the work handed over — actually, not in words?

    Step 9 is two acts: write the briefs, then hand the directory to ship-fleet. Every
    other gate here measures the first.

    The first version of this gate accepted a recorded deferral as equal to a dispatch,
    and said so in its own docstring as though it were a feature. It is not. The author of
    a sweep also writes the deferral reasons, so that rule let the graded party grant
    itself the exemption: one run marked all 61 needs-work cards `deferred` with a single
    invented reason, passed this gate, and reported the sweep complete with no work handed
    over. A gate cannot measure the honesty of a sentence its subject wrote.

    So the rule is now about acts rather than words:

    1. A needs-work card with neither a dispatch nor a deferral still fails, as before.
    2. **Zero dispatches fails.** A run that handed nothing over has not performed step 9's
       second half, whatever it recorded. There is deliberately no override — an audit-only
       run is a real thing, and the honest way to declare one is to skip this gate visibly
       rather than to make it pass falsely.
    3. **A reason repeated across more than three cards fails.** One sentence covering the
       whole set is a policy, not a per-card decision, and a policy is the owner's to make.
    4. A deferral must name who decided it (`--deferred-by`). Attribution does not prove
       authority, but it converts an anonymous default into a claim someone can check.
    """
    data = load(d)
    rows = data["rows"]
    work = [r for r in rows if r["verdict"] == "needs-work"]

    undecided = [r["key"] for r in work if not (r.get("dispatch") or r.get("deferred"))]
    if undecided:
        fail(f"{len(undecided)} card(s) have work to do and no record of it being "
             f"dispatched or deferred:\n  " + "\n  ".join(undecided)
             + "\n\nRecord where each went with `board_ledger.py record --dispatch <run/"
               "branch/PR>`, or why it is waiting with `--deferred <reason> --deferred-by "
               "<who decided>`.")

    if not work:
        print("no card has work remaining — nothing to dispatch")
        return

    dispatched = [r for r in work if r.get("dispatch")]
    deferred = [r for r in work if not r.get("dispatch") and r.get("deferred")]

    if not dispatched:
        fail(f"{len(work)} card(s) need work and NOT ONE was dispatched — all "
             f"{len(deferred)} were deferred.\n\nWriting the briefs is step 9's first "
             f"half; handing them to ship-fleet is the second, and this run stopped "
             f"between them. Deferral covers a card that cannot go now, not the whole set: "
             f"the party writing the reasons is the party being measured, so a blanket "
             f"deferral is a self-granted exemption rather than a decision.\n\n"
             f"Dispatch at least one card, or declare an audit-only run by skipping this "
             f"gate deliberately — `gates.py covered evidence classified banked` rather "
             f"than `all`. Skipping it says so out loud; passing it falsely does not.")

    unattributed = [r["key"] for r in deferred if not (r.get("deferred_by") or "").strip()]
    if unattributed:
        fail(f"{len(unattributed)} deferral(s) name nobody who decided them:\n  "
             + "\n  ".join(unattributed)
             + "\n\nPass `--deferred-by <who>`. Attribution does not prove authority, but "
               "an unattributed deferral is indistinguishable from the running agent "
               "excusing itself.")

    by_reason = {}
    for r in deferred:
        by_reason.setdefault((r.get("deferred") or "").strip(), []).append(r["key"])
    blanket = {reason: keys for reason, keys in by_reason.items() if len(keys) > 3}
    if blanket:
        lines = [f"{len(keys)} cards share this reason: {reason[:120]!r}\n      "
                 + ", ".join(sorted(keys)[:8]) + ("…" if len(keys) > 8 else "")
                 for reason, keys in blanket.items()]
        fail("a reason repeated across more than three cards is a policy, not a per-card "
             "decision:\n  " + "\n  ".join(lines)
             + "\n\nA policy about the whole set is the owner's to make, so it belongs in "
               "their words rather than the sweep's. Defer these individually with what is "
               "true of each, or dispatch them.")

    print(f"{len(work)} card(s) with work remaining: {len(dispatched)} dispatched, "
          f"{len(deferred)} deferred individually and attributed")


def g_classified(d, _):
    """Every graded card names the class whose warrant authorised the grading.

    Without it the verdict is uncountable: tier 3 counts closed items per defect class,
    and a row with no class is reported by the ratchet as unattributed rather than
    credited. An auditor also cannot tell which policy covered the decision.
    """
    data = load(d)
    graded = [r for r in data["rows"] if r["verdict"] in ("done", "needs-work", "no-change")]
    missing = [r["key"] for r in graded if not r.get("defect_class")]
    if missing:
        fail(f"{len(missing)} graded card(s) name no defect class:\n  "
             + "\n  ".join(missing)
             + "\n\nRecord it with `board_ledger.py record --defect-class <name>`, using a "
               "class the warrant names. An unnamed class holds tier 0 by default, so a "
               "sweep that skips this can grade the whole board and move the ladder nothing.")
    classes = sorted({r.get("defect_class") or "?" for r in graded})
    print(f"{len(graded)} graded card(s) across {len(classes)} class(es): {', '.join(classes)}")


def g_banked(d, _):
    """Did each terminal verdict reach the warrant's ledger, with a real digest?

    Inert where the repo has no `.warrant/` — stocktake runs without warrant installed and
    falls back to refusing promotion, which is a complete answer. Where a warrant IS present,
    a verdict that never became a ledger row is work the ladder cannot see.
    """
    data = load(d)
    root = _repo_root(d)
    if not root or not os.path.isdir(os.path.join(root, ".warrant")):
        print("no .warrant/ in this checkout — nothing to bank against")
        return
    terminal = [r for r in data["rows"] if r["verdict"] in ("done", "no-change")]
    unbanked = [r["key"] for r in terminal if not r.get("warrant_row")]
    undigested = [r["key"] for r in terminal
                  if r.get("warrant_row") and not r.get("evidence_digest")]
    problems = []
    if unbanked:
        problems += [f"{k}: no warrant ledger row" for k in unbanked]
    if undigested:
        problems += [f"{k}: banked with no evidence digest — the snapshot was not taken "
                     f"before the lane judged, so the verdict is void under warrant:panel"
                     for k in undigested]
    if problems:
        fail(f"{len(problems)} verdict(s) the warrant cannot count:\n  "
             + "\n  ".join(problems)
             + "\n\n`warrant_column.py` decides the column and writes nothing. Append the "
               "row yourself with warrant's `ledger.py --class … --item … --verdict … "
               "--tier … --evidence-digest …`, and record the index it returns with "
               "`board_ledger.py record --warrant-row`.")
    print(f"{len(terminal)} terminal verdict(s), each banked with a digest")


def g_verified_gate(d, opts):
    cfg = getattr(opts, "verified_config", None)
    data = load(d)
    promoted = [r["key"] for r in data["rows"]
                if (r.get("landed") or "").strip().lower() == "verified"]
    if not promoted:
        print("no card promoted past Done — the Verified gate does not apply")
        return
    here = os.path.dirname(os.path.abspath(__file__))
    cmd = [sys.executable, os.path.join(here, "check_verified_gate.py")]
    if cfg:
        cmd.append(cfg)
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        fail(f"{len(promoted)} card(s) were promoted to Verified and the gate refuses:\n"
             + r.stdout + r.stderr)
    print(f"{len(promoted)} promoted, and all eight preconditions hold")

GATES = {
    "covered": g_covered,
    "evidence": g_evidence,
    "inconclusive-reported": g_inconclusive_reported,
    "ungraded-reported": g_ungraded_reported,
    "briefs-written": g_briefs_written,
    "dispatched": g_dispatched,
    "classified": g_classified,
    "banked": g_banked,
    "verified-gate": g_verified_gate,
}


# --------------------------------------------------------------------------------------
# Selftest
#
# Every case here has been checked to FAIL when the gate it exercises is reverted. A gate
# case that passes both with and against its own logic measures nothing, and this file
# shipped one for months: `briefs-written` asserted a path existed, so 57 cards pointing
# at a single 48KB file satisfied it. Add a case only alongside the revert that proves it.
# --------------------------------------------------------------------------------------

def _fixture(tmp, rows, briefs=None, marks=()):
    """Write a ledger dir. `briefs` maps filename -> contents, written alongside it.

    `marks` creates directories that make the fixture look like a checkout — pass
    `(".git",)` for a repo the gates can find, `(".git", ".warrant")` for one under a
    warrant. `banked` is inert without the second, so a case testing it needs both.
    """
    import json as _json
    os.makedirs(tmp, exist_ok=True)
    for m in marks:
        os.makedirs(os.path.join(tmp, m), exist_ok=True)
    for name, body in (briefs or {}).items():
        with open(os.path.join(tmp, name), "w") as f:
            f.write(body)
    full = []
    for r in rows:
        row = {"key": r.get("key", "WEB-1"), "title": "", "column_at_intake": "Todo",
               "verdict": None, "lane": None, "sha": None, "landed": None,
               "requirements": None, "work_at": None, "brief": None,
               "question": None, "note": None, "finished": None,
               "dispatch": None, "deferred": None}
        row.update(r)
        if row.get("brief"):
            row["brief"] = os.path.join(tmp, row["brief"])
        full.append(row)
    with open(os.path.join(tmp, "board-triage-ledger.json"), "w") as f:
        _json.dump({"started": "", "columns_in_scope": [], "role_map": {}, "rows": full}, f)
    return tmp


class _Opts:
    verified_config = None
    max_cards_per_brief = 3


def _run(gate, d):
    """Run one gate, returning (passed, output). Gates talk through stdout/stderr+exit.

    An unexpected exception is reported as a crash rather than folded into "failed". A
    mutation harness that reads a traceback as a caught mutation certifies the case that
    was supposed to catch it, and one case here was passing on exactly that — a `KeyError`
    on a ledger written before `defect_class` existed, which is also a bug the gate had.
    """
    import io, contextlib, traceback
    out, err = io.StringIO(), io.StringIO()
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            GATES[gate](d, _Opts())
        return True, out.getvalue()
    except SystemExit as e:
        return (e.code in (None, 0)), out.getvalue() + err.getvalue()
    except Exception:
        return "crash", out.getvalue() + err.getvalue() + traceback.format_exc()


# Each case: (name, gate, expected_pass, rows, briefs)
_A_BRIEF = "WEB-1 — the card this brief is for.\nWhat is missing: the producer."
CASES = [
    # covered
    ("covered rejects a pending row", "covered", False,
     [{"key": "WEB-1", "verdict": "done"}, {"key": "WEB-2", "verdict": None}], None),
    ("covered accepts a fully graded board", "covered", True,
     [{"key": "WEB-1", "verdict": "done"}], None),

    # evidence
    ("evidence rejects done without a lane", "evidence", False,
     [{"key": "WEB-1", "verdict": "done", "sha": "abc", "work_at": "merged"}], None),
    ("evidence rejects done without a sha", "evidence", False,
     [{"key": "WEB-1", "verdict": "done", "lane": "grok", "work_at": "merged"}], None),
    ("evidence rejects needs-info without a question", "evidence", False,
     [{"key": "WEB-1", "verdict": "needs-info", "work_at": "not built"}], None),
    ("evidence rejects needs-work without a brief", "evidence", False,
     [{"key": "WEB-1", "verdict": "needs-work", "work_at": "merged"}], None),
    ("evidence rejects a verdict with no work-at", "evidence", False,
     [{"key": "WEB-1", "verdict": "done", "lane": "grok", "sha": "abc"}], None),
    ("evidence rejects ungraded without a note", "evidence", False,
     [{"key": "WEB-1", "verdict": "ungraded", "work_at": "merged"}], None),
    ("evidence accepts a complete row", "evidence", True,
     [{"key": "WEB-1", "verdict": "done", "lane": "grok", "sha": "abc",
       "work_at": "merged"}], None),

    # ungraded-reported — the verdict that must never read as a defect
    ("ungraded-reported rejects a thin note", "ungraded-reported", False,
     [{"key": "WEB-1", "verdict": "ungraded", "note": "skipped"}], None),
    ("ungraded-reported accepts a note that says what was not run", "ungraded-reported", True,
     [{"key": "WEB-1", "verdict": "ungraded",
       "note": "steps 3-5 not run: the lane was out of credits for the whole window"}], None),

    # briefs-written — three distinct ways a brief is not dispatchable
    ("briefs-written rejects a brief that is not on disk", "briefs-written", False,
     [{"key": "WEB-1", "verdict": "needs-work", "brief": "gone.md"}], {}),
    ("briefs-written rejects a brief that never names the card", "briefs-written", False,
     [{"key": "WEB-9", "verdict": "needs-work", "brief": "b.md"}], {"b.md": _A_BRIEF}),
    ("briefs-written rejects one brief serving more cards than the cap", "briefs-written", False,
     [{"key": f"WEB-{i}", "verdict": "needs-work", "brief": "all.md"} for i in range(1, 6)],
     {"all.md": "".join(f"WEB-{i} " for i in range(1, 6))}),
    ("briefs-written accepts one brief per card", "briefs-written", True,
     [{"key": "WEB-1", "verdict": "needs-work", "brief": "b.md"}], {"b.md": _A_BRIEF}),

    # dispatched — the gate the whole hardening exists for
    ("dispatched rejects work that was never handed anywhere", "dispatched", False,
     [{"key": "WEB-1", "verdict": "needs-work", "brief": "b.md"}], {"b.md": _A_BRIEF}),
    ("dispatched accepts work handed to a fleet run", "dispatched", True,
     [{"key": "WEB-1", "verdict": "needs-work", "dispatch": "ship-fleet run 2026-08-20-a"}], None),
    # Isolates the undecided rule: one card IS dispatched, so the zero-dispatch rule
    # cannot fire and only the undecided check can catch the second card.
    ("dispatched refuses an undecided card even when another was dispatched",
     "dispatched", False,
     [{"key": "WEB-1", "verdict": "needs-work", "dispatch": "ship-fleet run-a"},
      {"key": "WEB-2", "verdict": "needs-work", "brief": "b.md"}], {"b.md": _A_BRIEF}),
    ("dispatched refuses a deferral with no dispatch anywhere", "dispatched", False,
     [{"key": "WEB-1", "verdict": "needs-work",
       "deferred": "owner wants the security cards first", "deferred_by": "Luke"}], None),
    ("dispatched accepts a deferral alongside a real dispatch", "dispatched", True,
     [{"key": "WEB-1", "verdict": "needs-work", "dispatch": "ship-fleet run-a"},
      {"key": "WEB-2", "verdict": "needs-work",
       "deferred": "blocked on the vendor's reply", "deferred_by": "Luke"}], None),
    ("dispatched refuses an unattributed deferral", "dispatched", False,
     [{"key": "WEB-1", "verdict": "needs-work", "dispatch": "ship-fleet run-a"},
      {"key": "WEB-2", "verdict": "needs-work", "deferred": "waiting"}], None),
    # The exact shape of the failure this gate was rewritten for: one invented sentence
    # applied to the whole set, self-authored, which the previous version passed.
    ("dispatched refuses one reason blanketed across the set", "dispatched", False,
     [{"key": "WEB-0", "verdict": "needs-work", "dispatch": "ship-fleet run-a"}]
     + [{"key": f"WEB-{i}", "verdict": "needs-work",
         "deferred": "awaiting the owner's call on running ship-fleet",
         "deferred_by": "orchestrator"} for i in range(1, 6)], None),
    ("dispatched allows the same reason on three or fewer", "dispatched", True,
     [{"key": "WEB-0", "verdict": "needs-work", "dispatch": "ship-fleet run-a"}]
     + [{"key": f"WEB-{i}", "verdict": "needs-work",
         "deferred": "blocked on the same vendor ticket", "deferred_by": "Luke"}
        for i in range(1, 4)], None),
    ("dispatched ignores cards with no work to do", "dispatched", True,
     [{"key": "WEB-1", "verdict": "done"}, {"key": "WEB-2", "verdict": "no-change"}], None),
    ("dispatched does not demand dispatch for an ungraded card", "dispatched", True,
     [{"key": "WEB-1", "verdict": "ungraded", "note": "the lane never ran on this one"}], None),

    # inconclusive-reported
    ("inconclusive-reported rejects a thin reason", "inconclusive-reported", False,
     [{"key": "WEB-1", "verdict": "inconclusive", "note": "unclear"}], None),
    ("inconclusive-reported accepts a reason with substance", "inconclusive-reported", True,
     [{"key": "WEB-1", "verdict": "inconclusive",
       "note": "the producer sits behind a vendor API nobody here has credentials for"}], None),

    # classified — the class that makes a verdict countable
    ("classified rejects a graded card with no class", "classified", False,
     [{"key": "WEB-1", "verdict": "done"}], None),
    ("classified rejects a needs-work card with no class", "classified", False,
     [{"key": "WEB-1", "verdict": "needs-work"}], None),
    ("classified accepts a graded card naming its class", "classified", True,
     [{"key": "WEB-1", "verdict": "done", "defect_class": "spec-conformance"}], None),
    ("classified does not demand a class of an ungraded card", "classified", True,
     [{"key": "WEB-1", "verdict": "ungraded", "note": "the lane never ran"}], None),
    ("classified does not demand a class of a needs-info card", "classified", True,
     [{"key": "WEB-1", "verdict": "needs-info", "question": "which tenant?"}], None),

    # banked — the append that feeds the tier-3 counter
    ("banked is inert with no warrant in the checkout", "banked", True,
     [{"key": "WEB-1", "verdict": "done"}], None, (".git",)),
    ("banked rejects a done verdict that never reached the warrant ledger", "banked", False,
     [{"key": "WEB-1", "verdict": "done", "defect_class": "spec-conformance"}], None,
     (".git", ".warrant")),
    ("banked rejects a row banked without an evidence digest", "banked", False,
     [{"key": "WEB-1", "verdict": "done", "warrant_row": "7"}], None, (".git", ".warrant")),
    ("banked accepts a verdict banked with a digest", "banked", True,
     [{"key": "WEB-1", "verdict": "done", "warrant_row": "7",
       "evidence_digest": "a" * 64}], None, (".git", ".warrant")),
    ("banked ignores a card whose verdict is not terminal", "banked", True,
     [{"key": "WEB-1", "verdict": "needs-work"}], None, (".git", ".warrant")),

    # verified-gate
    ("verified-gate is inert when nothing was promoted", "verified-gate", True,
     [{"key": "WEB-1", "verdict": "done"}], None),
]


def selftest():
    import shutil, tempfile
    root = tempfile.mkdtemp(prefix="stocktake-gates-selftest-")
    failures = []
    try:
        for i, case in enumerate(CASES):
            name, gate, want_pass, rows, briefs = case[:5]
            marks = case[5] if len(case) > 5 else ()
            d = _fixture(os.path.join(root, f"c{i}"), rows, briefs, marks)
            got_pass, output = _run(gate, d)
            if got_pass == "crash":
                failures.append(f"{name}\n    the gate raised instead of deciding\n    "
                                + output.strip().replace("\n", "\n    "))
            elif got_pass != want_pass:
                failures.append(f"{name}\n    expected {'pass' if want_pass else 'FAIL'}, "
                                f"got {'pass' if got_pass else 'FAIL'}\n    "
                                + output.strip().replace("\n", "\n    "))
    finally:
        shutil.rmtree(root, ignore_errors=True)
    for f in failures:
        print("  x " + f)
    print(f"{len(CASES)} cases, {len(failures)} failure(s)")
    return 1 if failures else 0


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("gate", choices=list(GATES) + ["all", "selftest"], nargs="?")
    p.add_argument("dir", nargs="?")
    p.add_argument("--verified-config")
    p.add_argument("--max-cards-per-brief", type=int, default=3,
                   help="how many cards one brief may serve before it stops being a "
                        "dispatchable unit (default 3)")
    a = p.parse_args()
    if a.gate == "selftest":
        sys.exit(selftest())
    if not a.gate or not a.dir:
        p.error("both a gate and a ledger directory are needed (or `selftest`)")
    names = list(GATES) if a.gate == "all" else [a.gate]
    for n in names:
        print(f"--- {n}")
        GATES[n](a.dir, a)

if __name__ == "__main__":
    main()
