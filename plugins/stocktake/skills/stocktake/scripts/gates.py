#!/usr/bin/env python3
"""Gates for a stocktake sweep. Each is judged on exit code alone.

Scoped to what THIS run is answerable for. In a shared checkout a repo-wide
cleanliness check fails for another session's edits and blocks a run on work it
cannot fix, so nothing here reads the whole tree.

  gates.py <gate> <ledger-dir> [--verified-config PATH]

Gates: covered · evidence · inconclusive-reported · briefs-written · verified-gate · all
"""
import argparse, json, os, subprocess, sys

def load(d):
    p = os.path.join(d, "board-triage-ledger.json")
    if not os.path.exists(p):
        fail(f"no ledger at {p} — the sweep has not started")
    with open(p) as f:
        return json.load(f)

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

def g_briefs_written(d, _):
    data = load(d)
    missing = []
    for r in data["rows"]:
        if r["verdict"] == "needs-work":
            b = r.get("brief") or ""
            if not b or not os.path.exists(b):
                missing.append(f"{r['key']}: brief {b!r} does not exist on disk")
    if missing:
        fail(f"{len(missing)} card(s) need work and have no brief to hand to ship-fleet:\n  "
             + "\n  ".join(missing))
    n = sum(1 for r in data["rows"] if r["verdict"] == "needs-work")
    print(f"{n} card(s) with work remaining, each with a brief on disk")

def g_verified_gate(d, cfg):
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
    "briefs-written": g_briefs_written,
    "verified-gate": g_verified_gate,
}

def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("gate", choices=list(GATES) + ["all"])
    p.add_argument("dir")
    p.add_argument("--verified-config")
    a = p.parse_args()
    names = list(GATES) if a.gate == "all" else [a.gate]
    for n in names:
        print(f"--- {n}")
        GATES[n](a.dir, a.verified_config)

if __name__ == "__main__":
    main()
