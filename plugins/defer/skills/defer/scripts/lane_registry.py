"""Lane registry — the single machine-readable copy of the routing policy.

`references/lanes.md` is the prose for a human; this file is what the scripts
read. When the two disagree the tests in `selftest.sh` fail, which is the point:
a policy that lives in two places drifts, and the drift is silent.

Effort is pinned per lane because a lane that inherits its config default is not
the lane anyone chose.

Two things decide a route. The **task class** decides which lanes may do the
work at all, and it is policy. The **work shape** decides which of those lanes
is good enough to do it, and it is measured — `capability_matrix.json` holds a
per-shape grade for every lane against opus, computed from 106 real tasks in
`~/Dev/diolog-swe-bench`. Between the lanes that survive both, headroom picks.
"""

import json
import os

_HERE = os.path.dirname(os.path.abspath(__file__))

# --- list prices -----------------------------------------------------------
# USD per million tokens, published rates as at 2026-08-21. Sourced, not
# inferred; `references/usage-sources.md` carries the citations. They set the
# cost tie-break, so a stale number here quietly changes routing — re-check them
# when a vendor moves, and note Gemini 3.7 Flash's introductory rate doubles on
# 2027-01-01 and Grok 4.6 doubles on any request whose prompt reaches 200K.
PRICES = {
    "gemini-3.7-flash-high": {"in": 0.75, "cached": 0.075, "out": 3.75, "blended": 4.50},
    "glm-5.3":               {"in": 1.40, "cached": 0.26,  "out": 4.40, "blended": 5.80},
    "grok-4.6":              {"in": 2.00, "cached": 0.50,  "out": 6.00, "blended": 8.00,
                              "long_context": {"in": 4.00, "cached": 1.00, "out": 12.00,
                                               "threshold_tokens": 200_000}},
    "gpt-5.6-terra":         {"in": 2.00, "cached": None,  "out": 12.00, "blended": 14.00},
    "gpt-5.6-sol":           {"in": None, "cached": None,  "out": None,  "blended": 35.00},
    # PLACEHOLDER. gpt-5.6-luna has no published rate here and the lane could not be
    # probed (codex is 401 on an expired refresh token), so this is terra's blended
    # figure standing in. It is never consulted while the lane is `unverified`.
    "gpt-5.6-luna":          {"in": None, "cached": None,  "out": None,  "blended": 14.00},
    "claude-opus-5":         {"in": 5.00, "cached": None,  "out": 25.00, "blended": 30.00},
    "claude-fable-5":        {"in": 10.00, "cached": None, "out": 50.00, "blended": 60.00},
}

# --- the lanes -------------------------------------------------------------
# family      : independence group. A verifier must differ from the writer's.
# cmd         : argv template. {PROMPT} is substituted; nothing else is.
# env         : extra environment, applied on top of the caller's.
# verify      : how to prove the lane ran as routed (see wire-verify.md).
# meter       : which usage source `lane_pick.py` reads for this lane.
# bench_key   : this lane's row in capability_matrix.json, or None.
# evidence    : how far that row transfers to this lane.
#   "exact"   — the bench ran this model, at this effort, through this CLI.
#   "proxy"   — a different version or a different harness. Advisory: the
#               capability gate reads it, but never lets it clear a lane to
#               drop-in, because the number was not produced by this lane.
#   "none"    — unmeasured. The gate abstains and headroom decides alone.

LANES = {
    "grok": {
        "model": "grok-4.6",
        "blended_usd_per_mtok": PRICES["grok-4.6"]["blended"],
        "family": "xai",
        "effort": "xhigh",
        "cmd": ["grok", "-m", "grok-4.6", "--effort", "xhigh", "-p", "{PROMPT}"],
        "fallback_cmd": ["cursor-agent", "-p", "--force", "--model", "grok-4.6", "{PROMPT}"],
        "env": {},
        "verify": "grok-store",
        "meter": "grok",
        # The bench measured grok-4.5 under mini, not 4.6 under the grok CLI.
        "bench_key": "grok-4.5@xhigh",
        "evidence": "proxy",
    },
    "gemini": {
        "model": "gemini-3.7-flash-high",
        "blended_usd_per_mtok": PRICES["gemini-3.7-flash-high"]["blended"],
        "family": "google",
        "effort": "baked-into-model-id",
        # --output-format json is not cosmetic: it is the ONLY place a token count
        # for this lane exists. Plain print mode records nothing, anywhere.
        "cmd": ["agy", "--model", "gemini-3.7-flash-high", "--output-format", "json",
                "-p", "{PROMPT}"],
        "fallback_cmd": None,
        "env": {},
        "verify": "output-nonempty",
        "meter": "gemini",
        # Same model, different harness: the bench ran gemini-3.7-flash under
        # mini-swe-agent in a container at temperature 0, and this lane runs it
        # under agy at default sampling. The bench numbers are a floor for this
        # lane, not a reading of it. Note WHICH confound still does that work:
        # a same-scaffold control (capability.md) showed the bash-only loop does
        # NOT explain the static-page collapse - seven other models cleared
        # 62-83% through it. What survives is temperature 0, which Google flags
        # as degrading for the 3.x family specifically.
        "bench_key": "gemini-3.7-flash@medium",
        "evidence": "proxy",
    },
    "glm": {
        "model": "glm-5.3",
        "blended_usd_per_mtok": PRICES["glm-5.3"]["blended"],
        "family": "zai",
        "effort": "high",
        # GLM is Claude Code pointed at the Perch proxy. The binding header is
        # what selects Z.AI; without it the same command silently runs Claude.
        "cmd": ["claude", "--effort", "high", "-p", "{PROMPT}"],
        "fallback_cmd": None,
        "env": {
            "ANTHROPIC_BASE_URL": "http://127.0.0.1:8858",
            "ANTHROPIC_API_KEY": "local-proxy-supplies-the-real-credential",
            "ANTHROPIC_CUSTOM_HEADERS": "X-Perch-Binding: glm",
        },
        "verify": "relay-ledger",
        "meter": "glm",
        # The bench measured glm-5.2-fast under mini, on 79% of the corpus.
        "bench_key": "glm-5.2-fast@max",
        "evidence": "proxy",
    },
    "codex-terra": {
        "model": "gpt-5.6-terra",
        "blended_usd_per_mtok": PRICES["gpt-5.6-terra"]["blended"],
        "family": "openai",
        "effort": "high",
        "cmd": ["codex", "exec", "-m", "gpt-5.6-terra",
                "-c", 'model_reasoning_effort="high"', "-s", "read-only",
                "-o", "{OUTFILE}", "{PROMPT}"],
        "fallback_cmd": None,
        "env": {},
        "verify": "codex-header",
        "meter": "codex",
        "bench_key": "codex/gpt-5.6-terra@high",
        "evidence": "exact",
    },
    "codex-sol": {
        "model": "gpt-5.6-sol",
        "blended_usd_per_mtok": PRICES["gpt-5.6-sol"]["blended"],
        "family": "openai",
        "effort": "medium",
        "cmd": ["codex", "exec", "-m", "gpt-5.6-sol",
                "-c", 'model_reasoning_effort="medium"', "-s", "read-only",
                "-o", "{OUTFILE}", "{PROMPT}"],
        "fallback_cmd": None,
        "env": {},
        "verify": "codex-header",
        "meter": "codex",
        "bench_key": "codex/gpt-5.6-sol@medium",
        "evidence": "exact",
    },
    # sol at high is the cheapest lane the bench found that holds opus's quality
    # on most shapes: 63.8 headline against opus's 67.1, at $0.25 a task against
    # $2.16. It exists as a separate lane from `codex-sol` because the referral
    # class wants medium and the implementation classes want this. Still not max
    # — that rule is unchanged, and `sol@high` captures most of what max buys.
    "codex-sol-high": {
        "model": "gpt-5.6-sol",
        "blended_usd_per_mtok": PRICES["gpt-5.6-sol"]["blended"],
        "family": "openai",
        "effort": "high",
        "cmd": ["codex", "exec", "-m", "gpt-5.6-sol",
                "-c", 'model_reasoning_effort="high"', "-s", "read-only",
                "-o", "{OUTFILE}", "{PROMPT}"],
        "fallback_cmd": None,
        "env": {},
        "verify": "codex-header",
        "meter": "codex",
        "bench_key": "codex/gpt-5.6-sol@high",
        "evidence": "exact",
    },
    # terra at max is the strongest OpenAI lane on brownfield work and the only
    # non-Claude lane that held opus on compound multi-group backend tasks.
    "codex-terra-max": {
        "model": "gpt-5.6-terra",
        "blended_usd_per_mtok": PRICES["gpt-5.6-terra"]["blended"],
        "family": "openai",
        "effort": "max",
        "cmd": ["codex", "exec", "-m", "gpt-5.6-terra",
                "-c", 'model_reasoning_effort="max"', "-s", "read-only",
                "-o", "{OUTFILE}", "{PROMPT}"],
        "fallback_cmd": None,
        "env": {},
        "verify": "codex-header",
        "meter": "codex",
        "bench_key": "codex/gpt-5.6-terra@max",
        "evidence": "exact",
    },
    # The bulk lane: $0.14 a task and 2.2 minutes, a sixth of what terra@high
    # costs in wall clock. It ranks 13th overall, so it earns work only on the
    # shapes where the matrix says the gap to opus closes.
    "codex-terra-medium": {
        "model": "gpt-5.6-terra",
        "blended_usd_per_mtok": PRICES["gpt-5.6-terra"]["blended"],
        "family": "openai",
        "effort": "medium",
        "cmd": ["codex", "exec", "-m", "gpt-5.6-terra",
                "-c", 'model_reasoning_effort="medium"', "-s", "read-only",
                "-o", "{OUTFILE}", "{PROMPT}"],
        "fallback_cmd": None,
        "env": {},
        "verify": "codex-header",
        "meter": "codex",
        "bench_key": "codex/gpt-5.6-terra@medium",
        "evidence": "exact",
    },
    # ADDED 2026-08-26. The value lane for implementation work, and the one to
    # reach for where gemini used to be the pick.
    #
    # This entry overturns half of its own DECLINED record, so both halves are
    # kept. The local bench had luna@max losing 9 of 11 shapes to terra@max AND
    # costing more; DeepSWE 1.1 (113 tasks, independent) puts it at 67% +/- 4%
    # for $0.61 a task -- statistically identical to grok-4.6@xhigh
    # (67% +/- 2%, $5.50) at 11% of the price, and ahead of gemini-3.7-flash
    # (65% +/- 2%, $2.18) at under a third. The CAPABILITY claim survives:
    # sol@max is 73% +/- 3% and genuinely ahead. The COST claim was inverted,
    # and cost is the whole argument for a lane that trades a few points for an
    # order of magnitude.
    #
    # `bench_key: None` is deliberate. The local matrix has no honest row for
    # this lane, and pointing at one measured under different conditions is how
    # a lane acquires a grade it never earned. It routes on policy; the shape
    # gate abstains rather than inventing a verdict.
    #
    # Every codex lane is unusable while `codex` returns 401 "Your access token
    # could not be refreshed" -- which is also why 19 of 20 codex calls failed
    # in the window this policy comes from. That is an outage, not a property of
    # this lane. Re-probe after `codex login`; a non-empty output file is the
    # pass, and an absent or empty one is a lane failure however clean the
    # header looks.
    "codex-luna-max": {
        "model": "gpt-5.6-luna",
        "blended_usd_per_mtok": PRICES["gpt-5.6-luna"]["blended"],
        "family": "openai",
        "effort": "max",
        "cmd": ["codex", "exec", "-m", "gpt-5.6-luna",
                "-c", 'model_reasoning_effort="max"', "-s", "read-only",
                "-o", "{OUTFILE}", "{PROMPT}"],
        "fallback_cmd": None,
        "env": {},
        "verify": "codex-header",
        "meter": "codex",
        "bench_key": None,
        "evidence": "none",
        "external_bench": "deepswe-1.1",
        "usd_per_task_external": 0.61,
    },
    "fable": {
        "model": "claude-fable-5",
        "blended_usd_per_mtok": PRICES["claude-fable-5"]["blended"],
        "family": "anthropic",
        "effort": "high",
        "cmd": ["claude", "--model", "claude-fable-5", "--effort", "high", "-p", "{PROMPT}"],
        "fallback_cmd": None,
        "env": {},
        "verify": "relay-ledger",
        "meter": "anthropic",
        "bench_key": "claude/fable@high",
        "evidence": "exact",
    },
    "opus": {
        "model": "claude-opus-5",
        "blended_usd_per_mtok": PRICES["claude-opus-5"]["blended"],
        "family": "anthropic",
        "effort": "xhigh",
        "cmd": ["claude", "--model", "claude-opus-5", "--effort", "xhigh", "-p", "{PROMPT}"],
        "fallback_cmd": None,
        "env": {},
        "verify": "relay-ledger",
        "meter": "anthropic",
        "bench_key": "claude/claude-opus-5@xhigh",
        "evidence": "exact",
    },
}

# --- task classes ----------------------------------------------------------
# `allow` is ordered only where the order carries meaning; where a class names
# several lanes together the balancer picks, not the order.
# `balance` marks the classes whose lane is chosen by measured usage.
# `shape_gated` marks the classes the capability matrix can speak to. The bench
#   measures a model BUILDING something, so it grades writers. It says nothing
#   about how well a model grades someone else's work, and the judged-dimension
#   scores carry no passing calibration artifact, so the judgement classes route
#   on policy alone and the gate abstains rather than inventing a verdict.

TASKS = {
    "implementation": {
        "label": "Writing code",
        "allow": ["glm", "grok", "codex-sol", "codex-luna-max", "codex-sol-high",
                  "codex-terra-max", "codex-terra-medium", "gemini", "opus"],
        "balance": True,
        "shape_gated": True,
        "why": "Nine lanes across four families can write code. Shape decides which are good "
               "enough for this piece; headroom picks between the survivors; Claude is the "
               "fail-back so a down lane never drops work. The order is the owner's tie-break "
               "of 2026-08-26 — glm, then grok, then sol at medium, ahead of gemini — and it "
               "only bites where two lanes tie on the measured number. gemini additionally "
               "carries a 12-point DELIVERY_PENALTY, which is a separate fact from its bench "
               "score and is lifted separately. codex-luna-max is the lane to prefer where "
               "gemini used to win, and it is `unverified` until somebody watches it answer.",
    },
    "completeness": {
        "label": "Completeness critic",
        "allow": ["glm", "grok", "gemini"],
        "balance": True,
        "shape_gated": False,
        "why": "Out of Claude's family by construction, and cheap enough to run on every item. "
               "glm and grok lead gemini here by the same 2026-08-26 evidence: a critic that "
               "fabricates a completion report is worse than no critic, and gemini produced "
               "one in the window this policy comes from.",
    },
    "general": {
        "label": "Non-referral, non-judgment work",
        "allow": ["codex-terra", "codex-terra-medium", "glm", "grok", "gemini"],
        "balance": False,
        "shape_gated": True,
        "why": "gpt-5.6-terra at high is the default worker for anything that is neither a "
               "referred decision nor a verdict; terra at medium takes the bulk work whose "
               "shape says the gap closes.",
    },
    "referral": {
        "label": "Referred decision / judgment / second opinion",
        "allow": ["codex-sol", "fable"],
        "balance": False,
        "shape_gated": False,
        "why": "A decision referred out needs a different reader, not a bigger one. sol at "
               "medium and fable at high are the two; sol never runs at max.",
    },
    "verification": {
        "label": "Task verification and same-family verification",
        "allow": ["opus"],
        "balance": False,
        "shape_gated": False,
        "why": "Acceptance verdicts run on claude-opus-5 at xhigh. Fable is a judge, not a "
               "verifier: it does not grade code or tickets.",
    },
    "design-review": {
        "label": "Design review",
        "allow": ["opus", "fable"],
        "balance": False,
        "shape_gated": False,
        "why": "Rendered-UI judgement stays on Claude. No other family reviews design here.",
    },
}

# --- work shapes -----------------------------------------------------------
# What a piece of work IS, in the terms the bench can actually distinguish. The
# `guard` is what to do when the only lane available for a shape is a guarded
# one: it is the condition under which the cheaper lane's known weakness stops
# mattering, and it is the caller's job to satisfy it.

SHAPES = {
    "brownfield-integration": {
        "label": "Change existing multi-file code under compound acceptance",
        "tell": "the work edits code that already exists, spans more than two files, or has to "
                "satisfy several independent acceptance criteria at once",
        "guard": "hand the lane the relevant files inline and name every acceptance criterion "
                 "separately; the measured failure here is satisfying one criterion and "
                 "silently dropping another, not writing bad code",
    },
    "greenfield-module": {
        "label": "New self-contained module behind one acceptance surface",
        "tell": "nothing exists yet, the surface is one file or one exported unit, and there is "
                "a single thing it has to do",
        "guard": "state the exported signature and the acceptance condition in the prompt",
    },
    "api-surface": {
        "label": "Route handler, server action or adapter wiring",
        "tell": "the work connects an existing contract to an existing consumer",
        "guard": "measured on five tasks only; treat any lane choice here as provisional and "
                 "check the result rather than the ranking",
    },
    "react-ui": {
        "label": "React component with interaction behaviour",
        "tell": "a component, its states, and what it does when someone uses it",
        "guard": "name every interactive state; the cheap lanes lose ground on states nobody "
                 "asked for explicitly",
    },
    "static-page": {
        "label": "From-scratch HTML and CSS page, no framework",
        "tell": "one self-contained page, authored rather than assembled",
        # The Gemini collapse here is measured, not a scaffold artifact, and its
        # mechanism is known: bounds are exceeded, requirements are not missed.
        "guard": "the OpenAI lanes beat opus here and Gemini collapses, so do not route this "
                 "shape on headroom alone; if you route it cheap, supply a reference input "
                 "and make the lane read each produced value back against every stated bound "
                 "(the measured failure is exceeding a cap on every instance while delivering "
                 "everything the brief asked for)",
    },
    "deck": {
        "label": "Slide and presentation authoring",
        "tell": "slides, a deck, a pitch, anything scored on the deck rubric",
        "guard": "every lane measured below opus on this shape; route it out only when the deck "
                 "is a draft somebody will edit",
    },
    "visual-design": {
        "label": "Work graded on aesthetic and design judgement",
        "tell": "the output will be judged on how it looks rather than on what it does",
        "guard": "supply the design language, the palette and a reference; the cheap lanes are "
                 "much closer to opus with a reference than without one, and state every cap "
                 "as a value to read back rather than as style advice",
    },
    "accessibility": {
        "label": "Semantics, keyboard paths and ARIA",
        "tell": "roles, labels, focus order, keyboard operation",
        "guard": "name the interaction that must work by keyboard",
    },
    "algorithmic": {
        "label": "Complexity-constrained or optimality-constrained implementation",
        "tell": "there is a stated bound, or an obviously wrong quadratic answer",
        "guard": "state the bound in the prompt; every lane measured at parity here, so this "
                 "shape is where the cheapest lane wins outright",
    },
    "tool-orchestration": {
        "label": "Multi-step tool calling against an audited log",
        "tell": "the lane has to drive tools in sequence and the trace matters",
        "guard": "measured on four tasks only; the reading is that this shape does not "
                 "discriminate, not that every lane is equal",
    },
    "regression-sensitive": {
        "label": "Must not break an existing passing contract",
        "tell": "there is a test suite, a public API or a live consumer that has to keep working",
        "guard": "name the contract that must not move and give the lane the command that "
                 "proves it; this is the shape with the widest spread between lanes",
    },
}

# --- the measured capability matrix ----------------------------------------


def _load_capability():
    """The per-shape grades, or None when the file is absent.

    Absent is a real state rather than an error: the matrix is evidence from a
    private benchmark, and a checkout without it should still route on policy
    and headroom. `capability()` returns None and every caller falls through.
    """
    try:
        with open(os.path.join(_HERE, "capability_matrix.json")) as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None


CAPABILITY = _load_capability()

#: Grades in descending order of what they permit.
GATE_ORDER = ["GOLD", "GREEN", "AMBER", "RED", "THIN", "REF"]
#: Grades that mean "send this work here without further thought".
DROP_IN = {"GOLD", "GREEN"}
#: Grades that mean "send it here once the shape's guard is satisfied".
GUARDED = {"AMBER", "THIN"}
#: The lane every other lane is measured against. It is the fail-back, never a
#: competitor: it grades REF on every shape by construction, and letting that
#: count as a drop-in result would hand it every route on the strength of being
#: the yardstick. Spreading work off this lane is the whole point of the gate.
REFERENCE_LANE = "opus"
#: How close two lanes have to score before their output counts as equivalent
#: and load-spreading takes over. Five points is not a new number: it is the
#: threshold GREEN already uses to call a lane a drop-in for opus, so "near
#: enough to opus to substitute" and "near enough to each other to swap" are the
#: same claim at the same size. Routing is score-led down to this margin and
#: usage-led inside it.
EQUIVALENCE_POINTS = 0.05


# --- first-party delivery evidence -----------------------------------------
# The bench measures a model BUILDING something under a graded rubric. It does
# not measure whether the artefact arrived, whether the run reported honestly,
# or what it cost to get there. Those are separate facts and they are recorded
# separately, so a reader can see which stage moved a lane and can lift a
# penalty without touching a bench score somebody else produced.
#
# A penalty is subtracted from the lane's bench mean before the equivalence
# filter runs, so a lane that measured level with the best on a shape can still
# fall out of the band on delivery. Every entry names its measurement.

DELIVERY_PENALTY = {
    "gemini": {
        "points": 12,
        "measured": "2026-08-26, ~/Dev/dAIolog/docs/retro-2026-08-26/",
        "why": "Running as an autonomous builder it failed 8 of 12 dispatches, and one of "
               "the completions was fabricated: a 4,406-byte report claiming four schedulers "
               "created, against a ground truth of nothing created. Separately it is 95% of "
               "the window's cash for 20% of the output. The bench cannot see any of that, "
               "because a fabricated report grades as a delivered artefact.",
        "lift_it_when": "a dispatch set of 12 or more completes with no fabricated report and "
                        "a failure rate under 20%, measured the same way",
    },
}

# Where two lanes survive every earlier stage, this order breaks the tie before
# cost does. Owner directive of 2026-08-26, and it agrees with the delivery
# evidence above rather than contradicting it.
PREFERENCE_ORDER = ["glm", "grok", "codex-sol", "codex-luna-max", "codex-sol-high",
                    "codex-terra", "codex-terra-max", "codex-terra-medium", "gemini"]


def delivery_adjusted(lane, mean):
    """A lane's bench mean after first-party delivery evidence.

    Returns the mean unchanged when nothing has been measured against the lane.
    """
    if mean is None:
        return None
    pen = DELIVERY_PENALTY.get(lane)
    return mean - pen["points"] if pen else mean


def preference_rank(lane):
    """Position in the owner's tie-break order; unlisted lanes sort last."""
    return PREFERENCE_ORDER.index(lane) if lane in PREFERENCE_ORDER else len(PREFERENCE_ORDER)


def equivalent_set(lanes, grades, margin=EQUIVALENCE_POINTS):
    """The lanes whose measured output is equivalent to the best on offer.

    Returns them in descending measured order, best first. A lane with no
    measured score for the shape cannot be shown equivalent to anything, so it
    joins only when nothing in `lanes` was measured at all — unmeasured is not
    endorsed, but it is also not a reason to route nowhere.
    """
    scored = {l: delivery_adjusted(l, grades[l]["mean"]) for l in lanes
              if grades.get(l) and grades[l].get("mean") is not None}
    scored = {l: m for l, m in scored.items() if m is not None}
    if not scored:
        return sorted(lanes, key=preference_rank)
    best = max(scored.values())
    keep = [l for l, m in scored.items() if m >= best - margin]
    # Measured order first, then the owner's preference where two lanes tie on
    # the number. Sorting on preference alone would let policy overrule a lane
    # that is genuinely better at this shape, which is the trade this file
    # refuses everywhere else.
    return sorted(keep, key=lambda l: (-scored[l], preference_rank(l)))


def shape_grade(lane, shape):
    """How a lane measured on a shape, after the evidence clamp.

    Returns None when there is nothing to say — no matrix, no bench row for the
    lane, or a shape the matrix does not carry. Otherwise a dict carrying the
    clamped `gate`, the `raw_gate` the numbers actually produced, and the
    supporting figures so a caller can print why.

    The clamp: a lane whose evidence is `proxy` is pulled into the guarded band
    from both directions. It cannot clear to drop-in, because the number came
    from a different version or a different harness and does not belong to this
    lane. It also cannot be hard-blocked, but read the reason carefully before
    relying on it: the scaffold argument that used to justify this half was
    tested on 2026-08-22 and failed. A same-scaffold control put seven other
    models at 62-83% on the tasks where Gemini scores 22, so the bash-only loop
    is not what makes `static-page` hard. What still blocks a hard block is the
    other confound — mini pins `temperature: 0`, which Google flags as degrading
    for the Gemini 3.x family specifically, while the `agy` lane and the opus
    reference set no temperature at all. Lifting the clamp needs the seven tasks
    re-run through `agy` at default sampling. See `references/capability.md`.
    """
    if CAPABILITY is None or shape not in CAPABILITY.get("shapes", {}):
        return None
    spec = LANES.get(lane) or {}
    key, evidence = spec.get("bench_key"), spec.get("evidence", "none")
    if not key or evidence == "none":
        return None
    cell = CAPABILITY["shapes"][shape]["lanes"].get(key)
    if not cell:
        return None
    raw = cell.get("gate", "THIN")
    gate = raw
    if evidence == "proxy" and raw != "REF":
        gate = "AMBER"
    return {
        "lane": lane, "shape": shape, "gate": gate, "raw_gate": raw,
        "evidence": evidence, "bench_key": key,
        "mean": cell.get("mean"), "delta": cell.get("delta"), "p": cell.get("p"),
        "n": cell.get("n"), "wins": cell.get("wins"), "losses": cell.get("losses"),
        "tier": CAPABILITY["lanes"].get(key, {}).get("tier"),
        "usd_per_task": CAPABILITY["lanes"].get(key, {}).get("usd_per_task"),
        "clamped": gate != raw,
    }


def gate_lanes(task, shape):
    """Split a class's allowed lanes into drop-in, guarded, refused and fail-back.

    A class that is not shape-gated, an unknown shape, or a missing matrix all
    produce the same answer: every allowed lane lands in `dropin` and nothing is
    refused, because abstaining is the honest result when there is no evidence.

    The reference lane is held out into `failback` whenever the class allows it.
    It is the yardstick, so it scores REF on every shape, and a band that
    counted REF as a pass would route everything back to the lane this gate
    exists to relieve.
    """
    allow = [l for l in TASKS[task]["allow"] if not LANES.get(l, {}).get("unverified")]
    if not TASKS[task].get("shape_gated") or shape not in SHAPES:
        return {"dropin": allow, "guarded": [], "refused": [], "failback": [], "grades": {}}
    dropin, guarded, refused, failback, grades = [], [], [], [], {}
    for lane in allow:
        g = shape_grade(lane, shape)
        grades[lane] = g
        if lane == REFERENCE_LANE:
            failback.append(lane)
        elif g is None:
            guarded.append(lane)          # unmeasured is not endorsed
        elif g["gate"] in DROP_IN:
            dropin.append(lane)
        elif g["gate"] in GUARDED:
            guarded.append(lane)
        else:
            refused.append(lane)
    if not failback:
        failback = [allow[-1]]
    return {"dropin": dropin, "guarded": guarded, "refused": refused,
            "failback": failback, "grades": grades}


# Lanes that must never be selected, with the reason, so a caller that tries
# gets a sentence rather than a silent substitution.
FORBIDDEN = {
    ("codex-sol", "max"): "gpt-5.6-sol never runs at max effort.",
    ("codex-sol-high", "max"): "gpt-5.6-sol never runs at max effort.",
    ("fable", "verification"): "fable does not verify code or tickets; route to opus.",
}

# --- external benchmark evidence -------------------------------------------
# Published figures from a bench this repo did not run. Kept apart from
# capability_matrix.json so nobody mistakes one for the other: the local matrix
# grades 11 shapes on a small corpus, this grades 113 tasks on someone else's.
# Where they disagree, both are recorded and the disagreement is the finding.

EXTERNAL_BENCH = {
    "deepswe-1.1": {
        "source": "https://deepswe.datacurve.ai/",
        "tasks": 113,
        "columns": "Model | Pass@1 | Avg cost (per task, USD) | Out tok | Steps",
        # Every row on the board, not only the lanes routed here — a lane we do
        # not run is the cheapest way to notice that the ordering moved.
        "rows": {
            "claude-opus-5@max":     {"pass_at_1": 0.74, "err": 0.04, "usd_per_task": 11.84},
            "gpt-5.6-sol@max":       {"pass_at_1": 0.73, "err": 0.03, "usd_per_task": 6.46},
            "claude-fable-5@max":    {"pass_at_1": 0.70, "err": 0.04, "usd_per_task": 21.63},
            "glm-5.3@max":           {"pass_at_1": 0.69, "err": 0.03, "usd_per_task": 3.99},
            "kimi-k3@max":           {"pass_at_1": 0.69, "err": 0.05, "usd_per_task": 4.65},
            "gpt-5.6-luna@max":      {"pass_at_1": 0.67, "err": 0.04, "usd_per_task": 0.61},
            "grok-4.6@xhigh":        {"pass_at_1": 0.67, "err": 0.02, "usd_per_task": 5.50},
            "gpt-5.5@xhigh":         {"pass_at_1": 0.67, "err": 0.06, "usd_per_task": 7.23},
            "gemini-3.7-flash@high": {"pass_at_1": 0.65, "err": 0.02, "usd_per_task": 2.18},
            "deepseek-v4-pro@max":   {"pass_at_1": 0.63, "err": 0.06, "usd_per_task": 1.67},
            "claude-opus-4.8@max":   {"pass_at_1": 0.59, "err": 0.02, "usd_per_task": 13.22},
            "qwen3.8-max@xhigh":     {"pass_at_1": 0.57, "err": 0.03, "usd_per_task": 3.73},
            "muse-spark-1.2@xhigh":  {"pass_at_1": 0.55, "err": 0.02, "usd_per_task": 3.70},
            "claude-sonnet-5@max":   {"pass_at_1": 0.54, "err": 0.04, "usd_per_task": 26.40},
            "deepseek-v4-flash@max": {"pass_at_1": 0.53, "err": 0.04, "usd_per_task": 0.46},
            "gemini-3.6-flash@high": {"pass_at_1": 0.47, "err": 0.04, "usd_per_task": 2.21},
            "glm-5.2@max":           {"pass_at_1": 0.44, "err": 0.02, "usd_per_task": 3.92},
            "gemini-3.5-flash@high": {"pass_at_1": 0.36, "err": 0.04, "usd_per_task": 3.45},
        },
        "not_on_the_board": ["gpt-5.6-terra"],
        "shown": "18 of 25 models, under the board's own \"Best\" effort-level filter",
        "reading": "luna@max and grok@xhigh are the same score to within their error bars, "
                   "and luna costs 11% of grok. luna is 6 points behind sol@max at a tenth "
                   "of the price, and 2 ahead of gemini-3.7-flash at 28% of it. Score per "
                   "dollar: luna 110, deepseek-v4-flash 115, gemini-3.7-flash 30, glm 17, "
                   "grok 12, sol 11, opus 6, fable 3 -- so luna is the only lane within 7 "
                   "points of the top that is not an order of magnitude dearer. "
                   "gpt-5.6-terra has no row at all, so the local bench's terra-versus-luna "
                   "comparison cannot be checked against this one.",
        "caveat": "Someone else's corpus and someone else's harness. Absolute costs differ "
                  "from the local matrix by an order of magnitude (sol@max is $6.46 here "
                  "against $0.47 there), so only the RELATIVE ordering transfers.",
    },
}

# Models that were measured and deliberately have no lane, so that adding one
# back is a decision somebody makes again rather than an oversight.
DECLINED = {
    # REVERSED 2026-08-26. luna@max now HAS a lane (`codex-luna-max`). The entry
    # stays because half of it was right and the half that was wrong is worth
    # keeping visible: this local bench had luna costing MORE than terra and sol,
    # and DeepSWE 1.1 measures it at $0.61 a task against sol@max's $6.46 — a
    # tenth, not more. The capability half stands on both benches; the cost half
    # was the whole argument, and it was inverted. See EXTERNAL_BENCH above.
    "gpt-5.6-luna": "SUPERSEDED — see EXTERNAL_BENCH['deepswe-1.1'] and the codex-luna-max "
                    "lane. Local finding, kept for the record: luna@max lost 9 of 11 shapes "
                    "to terra@max and 10 of 11 to sol@max while costing more than either "
                    "($0.72 a task against $0.67 and $0.47); luna@high lost 10 of 11 to "
                    "sol@high at $0.33 against $0.25. The relative COST ordering here does "
                    "not survive contact with a 113-task independent board and should not be "
                    "quoted onward without it.",
    "claude-sonnet-5": "Measured (52.9 headline, $1.61 a task) and genuinely strong on "
                       "greenfield modules and static pages, but it is an Anthropic lane, so "
                       "it relieves cost without relieving the dependency this routing exists "
                       "to spread. Add it deliberately if cost is the binding constraint.",
    "gpt-5.6-sol@max": "Ranked second overall at 66.6, statistically tied with opus, and the "
                       "best measured lane on regression-sensitive work. It stays out because "
                       "sol never runs at max, and sol@high holds 63.8 of that 66.6 at half "
                       "the price.",
}

