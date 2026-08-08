#!/usr/bin/env python3
"""benchmark_vs_compact.py — head-to-head: this skill against Claude Code's own /compact.

The baseline is free and already on disk. Every real /compact event under
~/.claude/projects is a summary the CLI actually wrote for a transcript that
actually happened, so the honest comparison is: take the same pre-compaction
transcript, have the skill write a summary, and score both the same way.

Why span recall is the primary metric and not judge scores
----------------------------------------------------------
ConstraintRot (arXiv:2606.22528, 1,323 episodes across seven model families)
found constraint-violation rates of 0% when the governing constraint was in
full context and 30% after compaction, and the conditional decomposition is
the load-bearing part: violation stayed at 0% when the constraint SURVIVED
into the summary and hit 38% when it was dropped. Presence in the summary
nearly determines downstream compliance, which makes deterministic span
recall close to a direct measure rather than a proxy.

Confounds this reports because the literature says they will otherwise
decide the result:
  - LENGTH. Verbosity bias inflates judge scores, and a longer summary
    mechanically retains more spans.
  - EXTRACTIVENESS. Faithfulness gains often turn out to be extractiveness
    artifacts (arXiv:2108.13684), and judges score copied text generously.
    A skill that "wins" by copying more has not won.
Both are printed beside every score. A win that disappears once they are
matched is not a win.

Arms (three, per the research's recommendation, not two):
  cli        the /compact summary already on disk           (free)
  skill      the skill's summary, generated now             (costs a call)
  pinning    incumbent structure + a verbatim pinned block  (costs a call)
The pinning arm exists to answer "is the rest of the skill decoration?" If
it captures most of the gain, ship the smaller thing.

Usage:
  python3 benchmark_vs_compact.py --list                 # what's available
  python3 benchmark_vs_compact.py --arms cli             # baseline only, free
  python3 benchmark_vs_compact.py --arms cli,skill -n 8  # head-to-head
"""
import argparse
import glob
import io
import json
import os
import pathlib
import re
import statistics
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
SKILL_MD = HERE.parent / "SKILL.md"

PATH_RE = re.compile(r'(?:/[\w.\-]+){2,}\.\w{1,6}\b')
IDENT_RE = re.compile(r'`([A-Za-z_][\w./\-]{2,60})`')
CORRECTION_RE = re.compile(
    r"\b(no,|not that|actually|wrong|incorrect|don'?t |stop |instead|i said|"
    r"that's not|revert|undo|you (?:mis|missed|forgot))", re.I)
# Negative knowledge: the category nobody has published survival rates for.
REJECTION_RE = re.compile(
    r"\b(didn'?t work|doesn'?t work|failed|rejected|abandoned|dead end|"
    r"tried .{0,40} but|reverted|backed out|gave up on|ruled out|"
    r"turned out (?:not|to be wrong))", re.I)
CONSTRAINT_RE = re.compile(
    r"\b(always |never |must not|do not |don'?t ever|only ever|make sure (?:to|you)|"
    r"under no circumstances|it'?s critical that|non-negotiable)", re.I)


def text_of(o):
    m = o.get("message") or {}
    c = m.get("content")
    if isinstance(c, str):
        return c
    out = []
    if isinstance(c, list):
        for b in c:
            if not isinstance(b, dict):
                continue
            t = b.get("type")
            if t == "text":
                out.append(b.get("text") or "")
            elif t == "tool_use":
                out.append(json.dumps(b.get("input") or {})[:4000])
            elif t == "tool_result":
                cc = b.get("content")
                out.append(cc if isinstance(cc, str) else json.dumps(cc)[:4000])
    return "\n".join(out)


def load(path):
    rows = []
    with io.open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if len(line) > 4_000_000:
                continue
            try:
                rows.append(json.loads(line))
            except Exception:
                pass
    return rows


def find_events(limit=None, max_chars=1_500_000):
    """Real /compact events small enough to re-summarise in one context."""
    out = []
    for f in glob.glob(os.path.expanduser("~/.claude/projects/*/*.jsonl")):
        try:
            rows = load(f)
        except Exception:
            continue
        cut = next((i for i, o in enumerate(rows) if o.get("isCompactSummary")), None)
        if cut is None or cut < 20:
            continue
        pre = rows[:cut]
        chars = sum(len(json.dumps(r)) for r in pre)
        if chars > max_chars:
            continue
        summ = (rows[cut].get("message") or {}).get("content")
        summ = summ if isinstance(summ, str) else json.dumps(summ)
        out.append({"file": f, "cut": cut, "pre_chars": chars,
                    "cli_summary": summ, "rows": pre})
    out.sort(key=lambda e: e["pre_chars"])
    return out[:limit] if limit else out


def label_spans(rows):
    """The four load-bearing categories. Labelled once, scored per arm."""
    paths, idents = set(), set()
    corrections, rejections, constraints = [], [], []
    for p in rows:
        if p.get("isCompactSummary"):
            continue
        t = text_of(p)
        if not t:
            continue
        for m in PATH_RE.findall(t):
            if len(m) < 90:
                paths.add(m)
        idents.update(IDENT_RE.findall(t))
        if REJECTION_RE.search(t[:2000]):
            for sent in re.split(r"(?<=[.!?])\s+", t[:2000]):
                if REJECTION_RE.search(sent) and 25 < len(sent) < 300:
                    rejections.append(sent.strip()[:60])
        if p.get("type") == "user":
            c = (p.get("message") or {}).get("content")
            if isinstance(c, str) and c.strip() and not c.startswith("[{"):
                s = c.strip()
                if CORRECTION_RE.search(s[:600]) and len(s) > 25:
                    corrections.append(s[:60])
                if CONSTRAINT_RE.search(s[:600]) and len(s) > 25:
                    constraints.append(s[:60])
    return {"file paths": sorted(paths), "identifiers": sorted(idents),
            "CORRECTIONS": corrections, "constraints": constraints,
            "rejected approaches": rejections}


def recall(items, summary):
    items = list(dict.fromkeys(items))
    if not items:
        return None, 0, []
    missing = [x for x in items if x not in summary]
    return (len(items) - len(missing)) / len(items), len(items), missing


def extractiveness(summary, rows):
    """Fraction of the summary's 8-grams that appear verbatim in the source.

    High extractiveness is not automatically good: the faithfulness literature
    shows apparent gains are often copying, and judges reward it regardless.
    """
    src = " ".join(text_of(r) for r in rows)
    words = summary.split()
    if len(words) < 16:
        return 0.0
    grams = [" ".join(words[i:i + 8]) for i in range(0, len(words) - 8, 4)]
    if not grams:
        return 0.0
    return sum(1 for g in grams if g in src) / len(grams)


def summarise_with(arm, rows, workdir):
    """Generate a summary for one arm via `claude -p`, brief passed by path.

    Clean child context: no MCP servers, session vars stripped. Both are
    measured requirements, not caution (see create-mac-icon's fidelity-loop
    reference for the numbers).
    """
    transcript = "\n\n".join(f"[{r.get('type','?')}] {text_of(r)[:6000]}" for r in rows)
    tpath = workdir / f"transcript-{arm}.txt"
    tpath.write_text(transcript)
    if arm == "skill":
        instr = (f"Read {SKILL_MD} and follow it exactly to write the compaction "
                 f"summary for the transcript at {tpath}.")
    else:  # pinning-only: the minimum change that might capture the gain
        instr = (
            f"Read the transcript at {tpath} and write a compaction summary for a fresh "
            f"session, in Claude Code's nine standard sections (Primary Request and Intent; "
            f"Key Technical Concepts; Files and Code Sections; Errors and fixes; Problem "
            f"Solving; All user messages; Pending Tasks; Current Work; Optional Next Step).\n\n"
            f"One addition: open with a PINNED block reproducing VERBATIM, word for word, "
            f"every standing constraint, every user correction, and every rejected approach "
            f"with its reason. Quote them; do not paraphrase them. Everything else may be "
            f"summarised normally.")
    instr += "\n\nOutput only the summary itself. Do not use any tool other than Read."
    env = {k: v for k, v in os.environ.items()
           if k not in ("CLAUDE_CODE_DISABLE_1M_CONTEXT", "CLAUDE_CODE_SESSION_ID",
                        "CLAUDE_CODE_CHILD_SESSION", "CLAUDE_EFFORT")}
    r = subprocess.run(
        ["claude", "-p", instr, "--model", "opus", "--allowedTools", "Read",
         "--permission-mode", "acceptEdits", "--strict-mcp-config",
         "--add-dir", str(workdir), "--add-dir", str(SKILL_MD.parent)],
        cwd=str(pathlib.Path.home()), capture_output=True, text=True,
        stdin=subprocess.DEVNULL, timeout=1800, env=env)
    return (r.stdout or "").strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--arms", default="cli", help="comma list of cli,skill,pinning")
    ap.add_argument("-n", "--limit", type=int, default=6)
    ap.add_argument("--max-chars", type=int, default=1_500_000)
    ap.add_argument("--out", default="")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()

    events = find_events(limit=args.limit, max_chars=args.max_chars)
    if args.list:
        print(f"{len(events)} usable events (pre-transcript under {args.max_chars:,} chars)")
        for e in events:
            print(f"  {os.path.basename(e['file'])[:16]}  rows={e['cut']:4}  "
                  f"pre={e['pre_chars']/1e6:.2f}M  cli_summary={len(e['cli_summary']):,}")
        return
    if not events:
        print("no usable events found")
        return

    arms = [a.strip() for a in args.arms.split(",") if a.strip()]
    results, workdir = [], pathlib.Path(tempfile.mkdtemp(prefix="compaction-bench-"))
    print(f"{len(events)} transcripts x {len(arms)} arms; workdir {workdir}\n")

    for i, e in enumerate(events, 1):
        spans = label_spans(e["rows"])
        row = {"file": os.path.basename(e["file"]), "spans": {k: len(v) for k, v in spans.items()},
               "arms": {}}
        print(f"[{i}/{len(events)}] {row['file'][:16]}  "
              f"corrections={len(spans['CORRECTIONS'])} constraints={len(spans['constraints'])} "
              f"rejections={len(spans['rejected approaches'])}")
        for arm in arms:
            summary = e["cli_summary"] if arm == "cli" else summarise_with(arm, e["rows"], workdir)
            if not summary:
                print(f"    {arm:8} FAILED to produce a summary")
                continue
            scores = {}
            for cat, items in spans.items():
                r, n, missing = recall(items, summary)
                scores[cat] = {"recall": r, "n": n, "missed": len(missing)}
            row["arms"][arm] = {
                "chars": len(summary),
                "extractiveness": round(extractiveness(summary, e["rows"]), 3),
                "scores": scores,
            }
            cr = scores["CORRECTIONS"]["recall"]
            print(f"    {arm:8} corrections {('%.0f%%' % (cr*100)) if cr is not None else '  n/a'}"
                  f"   {len(summary):,} chars   extractiveness {row['arms'][arm]['extractiveness']:.2f}")
        results.append(row)

    print("\n" + "=" * 72)
    print("PAIRED RESULT (per-transcript deltas, not two independent means)")
    print("=" * 72)
    for cat in ("CORRECTIONS", "constraints", "rejected approaches", "file paths", "identifiers"):
        line = f"  {cat:<22}"
        for arm in arms:
            vals = [r["arms"][arm]["scores"][cat]["recall"] for r in results
                    if arm in r["arms"] and r["arms"][arm]["scores"][cat]["recall"] is not None]
            line += f"  {arm}: {statistics.mean(vals)*100:5.1f}% (n={len(vals)})" if vals else f"  {arm}:   n/a"
        print(line)
    print("\n  CONFOUNDS (a win that vanishes when these match is not a win)")
    for arm in arms:
        ch = [r["arms"][arm]["chars"] for r in results if arm in r["arms"]]
        ex = [r["arms"][arm]["extractiveness"] for r in results if arm in r["arms"]]
        if ch:
            print(f"    {arm:8} median {statistics.median(ch):,.0f} chars   "
                  f"mean extractiveness {statistics.mean(ex):.2f}")
    if len(arms) > 1:
        a, b = arms[0], arms[1]
        wins = sum(1 for r in results if a in r["arms"] and b in r["arms"]
                   and (r["arms"][b]["scores"]["CORRECTIONS"]["recall"] or 0)
                   > (r["arms"][a]["scores"]["CORRECTIONS"]["recall"] or 0))
        both = sum(1 for r in results if a in r["arms"] and b in r["arms"])
        print(f"\n  {b} beat {a} on correction recall in {wins} of {both} paired transcripts.")
        print(f"  With n={both}, only a large effect is resolvable; report the MDE, not just the gap.")

    if args.out:
        pathlib.Path(args.out).write_text(json.dumps(results, indent=2))
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
