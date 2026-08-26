#!/usr/bin/env python3
"""Pick the least-loaded lane for a task class, from measured plan headroom.

    lane_pick.py --task completeness            # → lane + ready-to-run argv
    lane_pick.py --task implementation --shape brownfield-integration
    lane_pick.py --task implementation --json
    lane_pick.py --report                       # every lane, every meter
    lane_pick.py --matrix                       # measured capability, every shape

Routing is two filters and a ranking. The task CLASS says which lanes may do the
work; the work SHAPE says which of those are good enough for this particular
piece, read out of `capability_matrix.json`; and headroom picks between whatever
survives. Pass no shape and the middle filter abstains, which is the old
behaviour exactly.

Everything here runs on subscriptions, so the scarce thing is plan headroom in
the current window, not dollars. The rule is "least usage, recalculated for the
days left until reset": a lane holding 60% with six days to run is tighter than
one holding 80% that resets tonight, so raw usage is the wrong comparison. What
gets ranked is headroom per remaining day,

    allowance = (1 - used_pct) / days_left

and the largest wins. Where two lanes are within 20% of each other the meters
cannot tell them apart honestly, so the tie breaks on MEASURED cost per task,
taken from the capability matrix. List price per Mtok cannot break that tie: the
codex lanes all bill at one rate and differ by nearly 5x on what a task costs,
because effort buys tokens. A lane with no measured row falls back to list price.

Meters come in two tiers and the report always says which:

  TIER 1  a real utilization percentage the vendor already computed, read out of
          local state — Claude via Relay's usage.json, Codex via the rate_limits
          payload its own session store records. These need no budget.
  TIER 2  consumption this script counts itself, divided by a budget you set in
          lane_budgets.json. Grok, GLM and Gemini publish no quota API and no
          reliable allowance, so their numbers are estimates wearing a number.

A lane whose usage cannot be measured never wins on a zero it did not earn.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from lane_registry import (  # noqa: E402
    CAPABILITY, DROP_IN, EQUIVALENCE_POINTS, FORBIDDEN, LANES, SHAPES, TASKS,
    DELIVERY_PENALTY, delivery_adjusted, equivalent_set, gate_lanes, preference_rank,
    shape_grade,
)

RELAY = os.path.expanduser("~/Library/Application Support/Relay")
GROK_SESSIONS = os.path.expanduser("~/.grok/sessions")
AGY_BRAIN = os.path.expanduser("~/.gemini/antigravity-cli/brain")
CODEX_SESSIONS = os.path.expanduser("~/.codex/sessions")

# Tier-2 budgets only, and each is calibrated rather than guessed:
#   grok   — API-equivalent dollars recorded across seven days that consumed one
#            full plan period end to end, which is the closest thing to a Grok
#            allowance that exists anywhere on this machine.
#   glm    — the GLM Coding Plan Max weekly figure, 8,000 prompts.
#   gemini — a week of observed model calls across both Gemini paths, rounded.
# Override any of them in lane_budgets.json; a budget is what you are willing to
# spend, and only you know that.
DEFAULT_BUDGETS = {
    "grok":   {"window_days": 7, "budget": 4100.0, "unit": "usd"},
    "glm":    {"window_days": 7, "budget": 8000.0, "unit": "prompts"},
    "gemini": {"window_days": 7, "budget": 30000.0, "unit": "calls"},
}
# Lanes whose usage figure is a real vendor-computed percentage rather than a
# locally counted estimate. Derived, for the reason CODEX_LANES is.
TIER1 = {l for l, v in LANES.items() if v.get("meter") in ("codex", "anthropic")}
#: Every lane metered off the one Codex account. They share a rate limit, so they
#: share a reading — adding an effort variant must never look like new headroom.
# Derived rather than listed: a literal here silently omitted `codex-luna-max`
# on the day it was added, and the omission surfaced as a KeyError in the
# meter rather than as a routing bug, which is the lucky version.
CODEX_LANES = {l for l, v in LANES.items() if v.get("meter") == "codex"}
CLAUDE_LANES = {l for l, v in LANES.items() if v.get("meter") == "anthropic"}


def load_budgets():
    budgets = {k: dict(v) for k, v in DEFAULT_BUDGETS.items()}
    configured = set()
    try:
        with open(os.path.join(HERE, "lane_budgets.json")) as fh:
            user = json.load(fh)
    except (OSError, ValueError):
        return budgets, configured
    for name, cfg in (user.get("lanes") or {}).items():
        if isinstance(cfg, dict):
            budgets.setdefault(name, {}).update(cfg)
            configured.add(name)
    return budgets, configured


# ------------------------------------------------------------------ tier 1 --

def relay_claude_utilization():
    """Anthropic computes the number; Relay stores what the account reports.

    Two windows are tracked, a rolling 5-hour session and a 7-day week, and the
    binding one is whichever is fuller. Anthropic publishes no absolute token
    ceiling for any Max tier — only relative multipliers — so this percentage is
    the only honest reading of Claude headroom that exists on the machine.
    """
    try:
        with open(os.path.join(RELAY, "usage.json")) as fh:
            accounts = json.load(fh)
    except (OSError, ValueError):
        return None, "Relay usage.json not found — is Perch running?"
    now = time.time()
    best = None
    gate = None
    for acct in accounts.values():
        seven = acct.get("sevenDay") or {}
        util = seven.get("utilization")
        if util is None:
            continue
        resets = seven.get("resetsAt")
        days_left = max((resets - now) / 86400.0, 1 / 96) if resets else 7.0
        # Relay routes to whichever account has room, so the pool's headroom is
        # the emptiest account's rather than the average of all of them.
        if best is None or float(util) < best[0]:
            best = (float(util), days_left)
            five = acct.get("fiveHour") or {}
            gate = five.get("utilization")
    if best is None:
        return None, "no Anthropic account reported a utilization figure"
    # The weekly cap is what makes Claude comparable to a 7-day lane. The 5-hour
    # session is a separate gate that can block a call while the week is wide
    # open, so it rides along as a warning rather than driving the ranking.
    note = None if gate is None or gate < 90 else f"5-hour session at {gate:.0f}% — expect a short block"
    return {"used_pct": best[0], "days_left": best[1], "window": "sevenDay", "gate": note}, None


def codex_rate_limit():
    """Codex writes the real thing into its own transcripts: used_percent, the
    window in minutes, and the epoch it resets. Read the newest one that is
    populated — early turns in a session carry a null."""
    files = sorted(glob.glob(os.path.join(CODEX_SESSIONS, "*", "*", "*", "*.jsonl")))[::-1]
    now = time.time()
    for path in files[:400]:
        try:
            lines = open(path, errors="ignore").read().splitlines()
        except OSError:
            continue
        for line in reversed(lines):
            if '"rate_limits"' not in line:
                continue
            try:
                rl = json.loads(line)["payload"].get("rate_limits") or {}
            except (ValueError, KeyError, AttributeError):
                continue
            primary = rl.get("primary")
            if not primary or primary.get("used_percent") is None:
                continue
            resets = primary.get("resets_at")
            window_days = (primary.get("window_minutes") or 10080) / 1440.0
            days_left = max((resets - now) / 86400.0, 1 / 96) if resets else window_days
            return {"used_pct": float(primary["used_percent"]),
                    "days_left": days_left,
                    "plan": rl.get("plan_type") or "?"}, None
    return None, "no populated rate_limits in the codex session store"


# ------------------------------------------------------------------ tier 2 --

def meter_grok(since):
    """xAI exposes no quota to the CLI, and third-party allowance figures for
    SuperGrok/Heavy disagree by an order of magnitude. What is real is the cost
    the CLI records per turn, so grok is metered in dollars against a budget."""
    if not os.path.isdir(GROK_SESSIONS):
        return 0.0, "usd", "no grok session store at ~/.grok/sessions"
    total, turns = 0.0, 0
    for path in glob.glob(os.path.join(GROK_SESSIONS, "*", "*", "updates.jsonl")):
        try:
            if os.path.getmtime(path) < since - 86400:
                continue
        except OSError:
            continue
        for line in open(path, errors="ignore"):
            if "turn_completed" not in line:
                continue
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            if (rec.get("timestamp") or 0) < since:
                continue
            usage = ((rec.get("params") or {}).get("update") or {}).get("usage") or {}
            # costUsdTicks is 1e-9 USD. Fitted against 807 recorded turns: the
            # implied rates land at $3.78/M fresh and $1.66/M cached, between
            # Grok 4.6's standard $2.00/$0.50 and its ≥200K long-context
            # $4.00/$1.00 — which is where a CLI carrying a large repo prefix
            # should sit. xAI documents no unit, so a scale change moves silently.
            total += (usage.get("costUsdTicks") or 0) / 1e9
            turns += 1
    return total, "usd", None if turns else "no grok turns recorded in the window"


def _relay_count(since, predicate):
    month = time.strftime("%Y-%m", time.localtime())
    path = os.path.join(RELAY, "spend", f"{month}.jsonl")
    if not os.path.exists(path):
        return None, "Relay spend ledger not found — is Perch running?"
    n = 0
    for line in open(path, errors="ignore"):
        try:
            rec = json.loads(line)
        except ValueError:
            continue
        if (rec.get("ts") or 0) >= since and predicate(rec):
            n += 1
    return n, None


def meter_glm(since):
    """The GLM Coding Plan meters in prompts, not tokens: Max is about 1,600 per
    5 hours and 8,000 per week. Relay counts REQUESTS, and one plan prompt can
    be 15-20 model calls, so this over-counts against the plan's own unit — it
    is a load signal, not a quota reading."""
    n, note = _relay_count(since, lambda r: r.get("bindingId") == "glm")
    return float(n or 0), "requests", note or "requests, not plan prompts — over-counts"


LEDGER = os.environ.get("DEFER_LEDGER", os.path.expanduser("~/.claude/defer-usage.jsonl"))


def ledger_tokens(lane, since):
    """Total tokens this lane spent through lane_run.sh since `since`.

    The wrapper records what each call actually cost, which for Gemini is the
    only token record that exists anywhere — `agy` writes none of its own, and
    the count only appears at all because the wrapper asks for --output-format
    json. Calls made outside the wrapper are invisible here, so this returns
    None until the ledger has something, rather than reporting a confident zero.
    """
    if not os.path.exists(LEDGER):
        return None, 0
    total = calls = 0
    for line in open(LEDGER, errors="ignore"):
        try:
            rec = json.loads(line)
        except ValueError:
            continue
        if rec.get("lane") != lane or (rec.get("ts") or 0) < since:
            continue
        u = rec.get("usage") or {}
        total += u.get("total_tokens") or (
            (u.get("input_tokens") or 0) + (u.get("output_tokens") or 0))
        calls += 1
    return (total or None), calls


def meter_gemini(since):
    """Two paths reach Gemini and they share one Google sign-in, so they share
    one pool: the `agy` CLI directly, and Claude Code through Relay's
    `agy:default` binding. Counting only one of them understates the lane badly
    — Relay carried 38x the agy CLI's volume in the week this was written.

    agy records no tokens or cost anywhere, so its side is counted in MODEL
    responses from the transcript, which is the closest unit to a Relay request.
    """
    tokens, ledger_calls = ledger_tokens("gemini", since)
    if tokens:
        return float(tokens), "tokens", (
            f"{ledger_calls} calls through lane_run.sh, real token counts; any agy call made "
            f"outside the wrapper is invisible")
    relay_n, note = _relay_count(since, lambda r: str(r.get("model", "")).startswith("gemini"))
    if not os.path.isdir(AGY_BRAIN):
        return float(relay_n or 0), "calls", "no antigravity brain dir; agy CLI side unmeasured"
    agy_n = 0
    for path in glob.glob(os.path.join(AGY_BRAIN, "*", ".system_generated", "logs", "transcript.jsonl")):
        try:
            if os.path.getmtime(path) < since:
                continue
            for line in open(path, errors="ignore"):
                if '"MODEL"' in line:
                    agy_n += 1
        except OSError:
            continue
    return float(agy_n + (relay_n or 0)), "calls", (
        f"{agy_n} agy CLI + {relay_n or 0} via Relay, one Google sign-in — model calls, not tokens")


METERS = {"grok": meter_grok, "glm": meter_glm, "gemini": meter_gemini}


def vendor_api(cfg):
    """Hook for a real quota endpoint, once one exists to point at.

    Nothing is wired by default: neither xAI, Google nor Z.AI exposes a quota
    endpoint that the credential these CLIs already hold can read, and aiming
    one at a guessed URL would report a confident wrong number. The Z.AI key
    lives in the login keychain under `dev.perch.account.zai:e714ccf64231`;
    `references/usage-sources.md` has the shape to fill in.
    """
    api = cfg.get("api") or {}
    if not api.get("url"):
        return None
    import urllib.request
    key = ""
    if api.get("key_cmd"):
        try:
            key = subprocess.run(api["key_cmd"], capture_output=True, text=True,
                                 timeout=20).stdout.strip()
        except (OSError, subprocess.SubprocessError):
            return None
        if not key:
            return None
    req = urllib.request.Request(api["url"])
    for hdr in api.get("headers") or []:
        if ":" in hdr:
            k, v = hdr.split(":", 1)
            req.add_header(k.strip(), v.strip().replace("{KEY}", key))
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = json.load(resp)
    except Exception:
        return None
    node = body
    for part in (api.get("used_pct_path") or "").split("."):
        if part:
            node = node.get(part) if isinstance(node, dict) else None
    return float(node) if isinstance(node, (int, float)) else None


# --------------------------------------------------------------------- rank

def measure(now=None):
    now = now or time.time()
    budgets, configured = load_budgets()
    rows = {}

    claude, claude_note = relay_claude_utilization()
    codex, codex_note = codex_rate_limit()

    for lane, spec in LANES.items():
        cfg = budgets.get(lane, {})
        row = {"lane": lane, "model": spec["model"], "family": spec["family"],
               "price": spec["blended_usd_per_mtok"], "tier": 1 if lane in TIER1 else 2,
               "budget_source": "lane_budgets.json" if lane in configured else "built-in default"}

        if lane in CLAUDE_LANES:
            if claude is None:
                row.update(used_pct=None, days_left=7, allowance=0.0, measured=False,
                           note=claude_note, used="—", unit="%", source="—")
            else:
                # Anthropic meters Fable at 50% of the same weekly pool, so the
                # same account load costs Fable half the headroom Opus costs.
                pct = claude["used_pct"] * (0.5 if lane == "fable" else 1.0)
                row.update(used_pct=round(pct, 1), days_left=round(claude["days_left"], 2),
                           measured=True, note=claude.get("gate"), used=f"{pct:.1f}", unit="%",
                           source=f"Relay usage.json ({claude['window']})")
        elif lane in CODEX_LANES:
            if codex is None:
                row.update(used_pct=None, days_left=7, allowance=0.0, measured=False,
                           note=codex_note, used="—", unit="%", source="—")
            else:
                row.update(used_pct=round(codex["used_pct"], 1),
                           days_left=round(codex["days_left"], 2), measured=True, note=None,
                           used=f"{codex['used_pct']:.1f}", unit="%",
                           source=f"codex rate_limits (plan {codex['plan']})")
        else:
            window = float(cfg.get("window_days", 7))
            since = now - window * 86400
            used, unit, note = METERS[lane](since)
            override = vendor_api(cfg)
            budget = float(cfg.get("budget", 1))
            if override is not None:
                pct, note, src = override, None, "vendor API"
            else:
                pct = min(100.0 * used / budget, 100.0) if budget else 100.0
                src = "local ledger vs configured budget"
            reset = cfg.get("reset_epoch")
            days_left = max((float(reset) - now) / 86400.0, 1 / 96) if reset else window
            row.update(used_pct=round(pct, 1), days_left=round(days_left, 2),
                       measured=True, note=note, used=f"{used:.1f} {unit}",
                       unit=unit, source=src, budget=budget)

        if row.get("used_pct") is not None:
            row["allowance"] = round((1.0 - min(row["used_pct"], 100.0) / 100.0)
                                     / max(row["days_left"], 1 / 96), 5)
        rows[lane] = row
    return rows


def task_cost(lane):
    """What one piece of work on this lane actually cost, in dollars.

    The blended per-Mtok price cannot separate effort levels: terra at max and
    terra at medium bill at the same rate and differ by 4.8x on the bill,
    because the expensive one spends far more tokens thinking. The bench
    measured the thing that matters — mean cost of one whole task — so the
    tie-break uses that and falls back to list price only for a lane with no
    measured row.
    """
    ext = LANES.get(lane, {}).get("usd_per_task_external")
    if ext is not None:
        # No local bench row, but a published per-task figure exists. Using the
        # blended per-Mtok price here instead would compare a rate against a cost
        # and rank the cheapest lane on the board as one of the dearest.
        return ext

    key = (LANES[lane] or {}).get("bench_key")
    if key and CAPABILITY:
        usd = CAPABILITY["lanes"].get(key, {}).get("usd_per_task")
        if usd:
            return usd
    return LANES[lane]["blended_usd_per_mtok"]


def choose(task, now=None, tolerance=0.20, shape=None, require_dropin=False):
    """Pick a lane for `task`, narrowed by `shape` where there is evidence.

    Returns `(lane, rows, why, verdict)`. `verdict` carries the capability
    decision: which band the chosen lane sits in, what the shape's guard is when
    that band is `guarded`, and which lanes the matrix refused. It is None when
    no shape was given or the class is not shape-gated, so a caller that ignores
    it keeps the old behaviour.

    The bands run drop-in, then guarded, then the class's own fail-back. Work is
    never dropped and never routed down to a refused lane to get around a limit:
    when nothing clears, the last resort is the class's first allowed lane, and
    the verdict says so rather than the caller discovering it from the output.
    """
    spec = TASKS[task]
    rows = measure(now)
    gated = gate_lanes(task, shape) if shape else None
    verdict = None
    allow = list(spec["allow"])

    if gated is not None and shape in SHAPES:
        # Bands in the order they may be spent. Descend on two conditions, and
        # only these two: the band is empty, or every lane in it is at its cap.
        # A spent band is not a reason to send work to a lane the matrix refused
        # — the descent ends at the reference lane, never below it.
        ladder = [("drop-in", gated["dropin"])]
        if not require_dropin:
            ladder.append(("guarded", gated["guarded"]))
        ladder.append(("fail-back", gated["failback"]))
        chosen_band, band = ladder[-1][0], list(ladder[-1][1])
        for name, lanes in ladder:
            live = [l for l in lanes if l in rows and rows[l]["allowance"] > 0]
            if live:
                chosen_band, band = name, live
                break
        # Score leads, usage follows. Narrow the live band to the lanes whose
        # measured output is equivalent to the best available, and only then let
        # headroom choose. Ranking on headroom across the whole band would trade
        # real output quality for load-spreading: on greenfield work it once
        # picked a lane 13 points behind because the better one was near its
        # budget. Inside the equivalence margin that trade is free, which is
        # exactly where spreading load belongs.
        equivalent = equivalent_set(band, gated["grades"])
        outranked = [l for l in band if l not in equivalent]
        verdict = {
            "shape": shape, "band": chosen_band, "considered": equivalent,
            "outranked": outranked,
            "refused": gated["refused"], "failback": gated["failback"],
            "skipped_spent": [l for n, ls in ladder if n != chosen_band for l in ls
                              if l in rows and rows[l]["allowance"] <= 0],
            "guard": SHAPES[shape]["guard"] if chosen_band != "drop-in" else None,
            "grades": {l: gated["grades"].get(l) for l in spec["allow"]},
        }
        allow = equivalent

    eligible = [l for l in allow if l in rows]
    if not spec["balance"]:
        # Fixed order still skips a spent lane. The policy says which lanes may
        # do this work; it does not say to send it somewhere that will refuse.
        for lane in allow:
            if rows[lane]["allowance"] > 0:
                first = allow[0]
                why = ("fixed by policy" if lane == first else
                       f"fixed by policy, but {first} is at {rows[first]['used_pct']:.0f}% "
                       f"— next allowed lane with headroom")
                return lane, rows, why, verdict
        return allow[0], rows, (
            f"every lane allowed for {task} is at its cap — expect a limit"), verdict
    usable = [l for l in eligible if rows[l]["measured"]] or eligible
    best = max(rows[l]["allowance"] for l in usable)
    if best <= 0:
        return usable[0], rows, (
            "every eligible lane is at its cap — first allowed lane, expect a limit"), verdict
    band = [l for l in usable if rows[l]["allowance"] >= best * (1 - tolerance)]
    # Cheapest wins, and the owner's preference order breaks a cost tie. Both
    # only ever run inside a band already agreed to be equivalent on output.
    top = min(band, key=lambda l: (round(task_cost(l), 2), preference_rank(l)))
    others = ", ".join(f"{l} {rows[l]['allowance']:.4f}"
                       for l in sorted(usable, key=lambda l: -rows[l]["allowance"]) if l != top)
    if len(band) > 1:
        why = (f"within {int(tolerance * 100)}% on headroom ({'/'.join(sorted(band))}), so the "
               f"cheapest wins at ${task_cost(top):.2f} a task — {rows[top]['allowance']:.4f}/day"
               + (f" vs {others}" if others else ""))
    else:
        why = f"most headroom per remaining day ({rows[top]['allowance']:.4f}/day vs {others})"
    if verdict and len(usable) == 1 and verdict["outranked"]:
        # One lane survived the equivalence filter, so score decided and headroom
        # never got a vote. Saying "most headroom" here would credit the wrong
        # stage for the choice.
        why = (f"top measured lane on this shape; "
               f"{', '.join(verdict['outranked'])} more than "
               f"{EQUIVALENCE_POINTS * 100:.0f} points behind it")
    return top, rows, why, verdict


def calibrate(pairs):
    """Pin a Tier-2 budget from a percentage you can actually see.

        lane_pick.py --calibrate gemini=62 grok=99

    None of these three vendors exposes its quota to the CLI, but every one of
    them shows a percentage in a dashboard a human can read. Given that reading
    and the consumption this script already counts, the budget falls out:

        budget = counted_usage / (observed_pct / 100)

    which is worth more than any published allowance figure, because it is
    calibrated against this account on this machine rather than against someone
    else's estimate of the plan. Re-run it whenever the reading drifts.
    """
    budgets, _ = load_budgets()
    now = time.time()
    path = os.path.join(HERE, "lane_budgets.json")
    try:
        doc = json.load(open(path))
    except (OSError, ValueError):
        doc = {"lanes": {}}
    doc.setdefault("lanes", {})
    for pair in pairs:
        if "=" not in pair:
            print(f"skip {pair!r}: expected lane=percent", file=sys.stderr)
            continue
        lane, raw = pair.split("=", 1)
        if lane in TIER1:
            print(f"skip {lane}: tier 1, its percentage is already measured", file=sys.stderr)
            continue
        if lane not in METERS:
            print(f"skip {lane}: no meter", file=sys.stderr)
            continue
        try:
            pct = float(raw)
        except ValueError:
            print(f"skip {pair!r}: {raw!r} is not a number", file=sys.stderr)
            continue
        if not 0 < pct <= 100:
            print(f"skip {lane}: {pct} is not a percentage between 0 and 100", file=sys.stderr)
            continue
        cfg = budgets.get(lane, {})
        window = float(cfg.get("window_days", 7))
        used, unit, _ = METERS[lane](now - window * 86400)
        if used <= 0:
            print(f"skip {lane}: counted no usage in the last {window:g} days, "
                  f"so there is nothing to calibrate against", file=sys.stderr)
            continue
        budget = round(used / (pct / 100.0), 1)
        entry = doc["lanes"].setdefault(lane, {})
        entry.update({"budget": budget, "window_days": window, "unit": unit,
                      "calibrated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                      "calibrated_from_pct": pct})
        print(f"{lane}: {used:.1f} {unit} observed at {pct:g}% → budget {budget:g} {unit}")
    with open(path, "w") as fh:
        json.dump(doc, fh, indent=2)
        fh.write("\n")
    print(f"written to {path}")
    return 0


def argv_for(lane, prompt="{PROMPT}", outfile="/tmp/lane-out.md"):
    return [a.replace("{PROMPT}", prompt).replace("{OUTFILE}", outfile)
            for a in LANES[lane]["cmd"]]


SYMBOL = {"GOLD": "++", "GREEN": "+", "AMBER": "~", "RED": "x", "THIN": "?", "REF": "."}
#: Column headings for --matrix. Truncating lane names collides three codex
#: lanes into one heading, and a table whose columns cannot be told apart is
#: worse than no table.
ABBREV = {"codex-sol": "sol@med", "codex-sol-high": "sol@high", "codex-terra": "terra@high",
          "codex-terra-max": "terra@max", "codex-terra-medium": "terra@med",
          "gemini": "gemini", "grok": "grok", "glm": "glm", "fable": "fable", "opus": "OPUS"}


def print_matrix(shape=None):
    """The measured capability table, one row per shape, one column per lane.

    Prints what was measured, not what the router would do with it, so that a
    surprising route can be checked against the evidence behind it.
    """
    if CAPABILITY is None:
        print("no capability_matrix.json — routing falls back to policy and headroom alone")
        return 1
    src = CAPABILITY["source"]
    shapes = [shape] if shape else list(CAPABILITY["shapes"])
    keys = [(l, LANES[l]["bench_key"]) for l in LANES if LANES[l].get("bench_key")]
    print(f"bench {src['bench']} — {src['visible_tasks']} tasks, measured {src['measured']}, "
          f"reference {src['reference_lane']}")
    print("cell = mean score on that shape, then the grade "
          "(++ beats opus, + drop-in, ~ guarded, x refused, ? too thin, . reference)\n")
    print(f"{'shape':<24}{'n':>3} " + "".join(f"{ABBREV.get(l, l)[:11]:>12}" for l, _ in keys))
    for s in shapes:
        ent = CAPABILITY["shapes"].get(s)
        if not ent:
            print(f"{s}: not in the matrix")
            continue
        line = f"{s:<24}{ent['n']:>3} "
        for lane, _ in keys:
            g = shape_grade(lane, s)
            if g is None or g.get("mean") is None:
                line += f"{'—':>12}"
            else:
                mark = SYMBOL[g["gate"]] + ("*" if g["clamped"] else "")
                line += f"{g['mean'] * 100:>8.0f}{mark:>4}"
        print(line)
    print("\n* the grade was clamped into the guarded band because the lane's evidence is a "
          "proxy:\n  a different model version or a different harness than the lane runs.")
    print("\nlane                 tier   $/task   min   evidence   harness")
    for lane, key in keys:
        L = CAPABILITY["lanes"].get(key, {})
        usd = f"${L['usd_per_task']:.2f}" if L.get("usd_per_task") else "—"
        print(f"{lane:<20} {L.get('tier', '?'):>4}{usd:>9}{L.get('mean_minutes', 0):>6}"
              f"   {LANES[lane]['evidence']:<10} {L.get('harness', '')}")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--task", choices=sorted(TASKS))
    ap.add_argument("--shape", choices=sorted(SHAPES),
                    help="what the work IS. Narrows the class to the lanes measured good "
                         "enough for that shape before headroom picks between them.")
    ap.add_argument("--require-dropin", action="store_true",
                    help="refuse to route to a guarded lane; fall back to the class's "
                         "fail-back instead")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--matrix", nargs="?", const="", metavar="SHAPE",
                    help="print the measured capability matrix, all shapes or one")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--prompt", default="{PROMPT}")
    ap.add_argument("--outfile", default="/tmp/lane-out.md")
    ap.add_argument("--calibrate", nargs="+", metavar="LANE=PCT",
                    help="pin a tier-2 budget from a percentage you read in the vendor's "
                         "dashboard, e.g. --calibrate gemini=62")
    args = ap.parse_args()

    if args.calibrate:
        return calibrate(args.calibrate)

    if args.matrix is not None:
        if args.json:
            print(json.dumps(CAPABILITY, indent=2))
            return 0
        return print_matrix(args.matrix or None)

    if args.report or not args.task:
        rows = measure()
        if args.json:
            print(json.dumps(rows, indent=2))
            return 0
        print(f"{'lane':<20}{'model':<24}{'tier':>5}{'used':>16}{'used%':>7}"
              f"{'days left':>11}{'allowance':>11}  source")
        for r in sorted(rows.values(), key=lambda r: (-r["tier"], -r["allowance"])):
            pct = "—" if r["used_pct"] is None else f"{r['used_pct']:.1f}%"
            print(f"{r['lane']:<20}{r['model']:<24}{r['tier']:>5}{r['used']:>16}{pct:>7}"
                  f"{r['days_left']:>11.2f}{r['allowance']:>11.4f}  {r['source']}")
            if r["note"]:
                print(f"{'':<20}└─ {r['note']}")
        print("\nTier 1 is a vendor-computed utilization read out of local state. Tier 2 is counted "
              "here and divided by a budget you set — an estimate, not a quota reading.")
        print("Every codex lane reads one account's rate limit, so their allowances move together.")
        return 0

    lane, rows, why, verdict = choose(args.task, shape=args.shape,
                                      require_dropin=args.require_dropin)
    spec = LANES[lane]
    payload = {"task": args.task, "shape": args.shape, "lane": lane, "model": spec["model"],
               "family": spec["family"], "effort": spec["effort"], "reason": why,
               "capability": verdict,
               "argv": argv_for(lane, args.prompt, args.outfile), "env": spec["env"],
               "verify": spec["verify"], "meters": rows}
    if args.json:
        print(json.dumps(payload, indent=2))
        return 0
    print(f"task     {args.task} — {TASKS[args.task]['label']}")
    if args.shape:
        print(f"shape    {args.shape} — {SHAPES[args.shape]['label']}")
    print(f"lane     {lane} ({spec['model']}, {spec['family']} family, effort {spec['effort']})")
    print(f"why      {why}")
    if verdict:
        g = verdict["grades"].get(lane)
        if g and g.get("mean") is not None and g["gate"] != "REF":
            print(f"measured {g['mean'] * 100:.0f} on this shape against opus's "
                  f"{CAPABILITY['shapes'][args.shape]['opus_mean'] * 100:.0f} "
                  f"({g['delta'] * 100:+.0f} pts, p={g['p']:.2f}, n={g['n']}, "
                  f"tier {g['tier']}, {g['evidence']} evidence)")
        print(f"band     {verdict['band']}"
              + ("  — no cheaper lane measured up on this shape"
                 if verdict["band"] == "fail-back" else ""))
        if len(verdict["considered"]) > 1:
            print(f"equal    {', '.join(verdict['considered'])} — within "
                  f"{EQUIVALENCE_POINTS * 100:.0f} points of each other, so headroom chose")
        if verdict["outranked"]:
            print(f"outrank  {', '.join(verdict['outranked'])} — eligible but measured further "
                  f"behind, so not considered on headroom")
        if verdict["refused"]:
            print(f"refused  {', '.join(verdict['refused'])} — measured too far behind on this shape")
        if verdict["guard"]:
            print(f"guard    {verdict['guard']}")
    if spec["env"]:
        print("env      " + "  ".join(f"{k}={v!r}" for k, v in spec["env"].items()))
    print("run      " + " ".join(a if " " not in a else repr(a)
                                 for a in argv_for(lane, args.prompt, args.outfile)))
    print(f"verify   {spec['verify']} (see references/wire-verify.md)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
