#!/usr/bin/env python3
"""Grade the eval outputs against the assertions in evals.json.

Each assertion is checked by a pattern over the produced plan rather than by reading it, so
the grade is repeatable and a later iteration can be compared to this one. Patterns are
deliberately generous about wording and strict about the thing being claimed: an assertion
about promoting a transcript passes on any phrasing that names the mechanism, and fails when
the plan only says the word "promote" about something else.

Usage: python3 scripts/grade_evals.py <workspace/iteration-N>
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent


def rx(*alts: str) -> re.Pattern:
    return re.compile("|".join(alts), re.I | re.M)


# assertion index -> (pattern that must match, pattern that must NOT match)
CHECKS: dict[int, list[tuple[re.Pattern, re.Pattern | None]]] = {
    0: [
        (rx(r"aaaaaaaa"), None),
        (rx(r"bbbbbbbb|perch-live"), None),
        (rx(r"cccccccc"), None),
        (rx(r"wf_done9999ghi"), None),
        (rx(r"-Users-someone-Dev-orderly"), None),
        (rx(r"a0002"), rx(r"a0002[^.\n]{0,80}(failed|rate.?limited\b)(?![^.\n]{0,40}mention)")),
        (rx(r"Connection lost"), None),
        (rx(r"promot\w+", r"rewrite\w*\s+sessionId", r"sidechain"), None),
        (rx(r"--resume\s+(aaaaaaaa|\"?\$)", r"original session id", r"resume the (conductor|original|same) session"),
         rx(r"^[^\n]*claude[^\n]*--fork-session")),
        (rx(r"dry.?run", r"opened.{0,20}false", r"no (ghostty )?tabs? (were )?opened",
            r"(executed|launched|opened) nothing", r"no (session|tab) (was )?(launched|opened)",
            r"ran the guards only"), None),
    ],
    1: [
        (rx(r"(not|never|refus\w+|left.{0,20}alone|did not)[^.\n]{0,80}(resum|touch)", r"is (still )?(alive|live|running)"), None),
        (rx(r"registry|sessions/4\d+\.json|status.{0,10}busy"), None),
        (rx(r"quiet|without writing|long .{0,20}(call|task)|writes nothing"), None),
        (rx(r"wf_live0000aaa"), rx(r"relaunch\w*\s+wf_live0000aaa")),
        (rx(r"aaaaaaaa"), None),
        (rx(r"."), rx(r"^[^\n]*claude[^\n]*--fork-session")),
        (rx(r"ORD-0096"), None),
    ],
    2: [
        (rx(r"started[^.\n]{0,40}(no|without)[^.\n]{0,20}result", r"started line and no result",
            r"result was never written", r"never (wrote|written|returned) (a )?result",
            r"no result (was )?(written|recorded)"), None),
        (rx(r"first (cache )?miss|cache miss"), None),
        (rx(r"sticky"), None),
        (rx(r"isSidechain"), None),
        (rx(r"agent-a0002\.jsonl"), None),
        (rx(r"python3 scripts/|promote_agent\.py|claude --resume"), None),
    ],
}


def grade(text: str, eval_id: int, assertions: list[str]) -> list[dict]:
    out = []
    for i, a in enumerate(assertions):
        must, must_not = CHECKS[eval_id][i]
        hit = bool(must.search(text))
        bad = bool(must_not.search(text)) if must_not else False
        passed = hit and not bad
        m = must.search(text)
        ev = (text[max(0, m.start() - 60): m.end() + 60].replace("\n", " ") if m else "")
        if bad:
            b = must_not.search(text)
            ev = "VIOLATION: " + text[max(0, b.start() - 60): b.end() + 60].replace("\n", " ")
        out.append({"text": a, "passed": passed, "evidence": ev.strip()[:220]})
    return out


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    ws = Path(sys.argv[1])
    evals = json.loads((HERE / "evals" / "evals.json").read_text())["evals"]

    summary = []
    for e in evals:
        for cfg in ("with_skill", "without_skill"):
            d = next((p for p in ws.glob(f"eval-{e['id']}-*/{cfg}") if p.is_dir()), None)
            plan = d / "outputs" / "recovery-plan.md" if d else None
            if not plan or not plan.is_file():
                print(f"eval {e['id']} {cfg}: NO OUTPUT")
                summary.append({"eval": e["id"], "config": cfg, "passed": 0,
                                "total": len(e["assertions"])})
                continue
            # grade against everything the run produced, not just the prose file: a command
            # in a bootstrap script counts as having been given.
            text = plan.read_text(errors="replace")
            for extra in (d / "outputs").rglob("*"):
                if extra.is_file() and extra != plan and extra.stat().st_size < 200_000:
                    try:
                        text += "\n" + extra.read_text(errors="replace")
                    except Exception:
                        pass
            rows = grade(text, e["id"], e["assertions"])
            (d / "grading.json").write_text(json.dumps(
                {"eval_id": e["id"], "config": cfg, "expectations": rows}, indent=1))
            n = sum(1 for r in rows if r["passed"])
            summary.append({"eval": e["id"], "config": cfg, "passed": n, "total": len(rows)})
            print(f"eval {e['id']} {cfg:<14} {n}/{len(rows)}")
            for r in rows:
                if not r["passed"]:
                    print(f"    MISS  {r['text']}")
                    if r["evidence"].startswith("VIOLATION"):
                        print(f"          {r['evidence'][:160]}")

    print()
    for cfg in ("with_skill", "without_skill"):
        rows = [s for s in summary if s["config"] == cfg]
        p, t = sum(r["passed"] for r in rows), sum(r["total"] for r in rows)
        print(f"{cfg:<14} {p}/{t}  ({100*p//t if t else 0}%)")
    (ws / "benchmark.json").write_text(json.dumps({"summary": summary}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
