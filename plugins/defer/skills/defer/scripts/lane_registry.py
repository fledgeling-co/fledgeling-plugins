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
#
# Two 2026-09-09 additions carry NO sourced rate and say so. `gpt-6-astra` and
# `gemini-3.8-flash-high` are routed on an owner directive, not on a bench or a
# price list, and inventing a number here would rank them on a figure nobody
# published. Each stands in at its predecessor's blended rate and is marked
# `price_evidence: "placeholder"` on the lane, so a reader can see the tie-break
# is running on a guess rather than on evidence.
PRICES = {
    "gemini-3.7-flash-high": {"in": 0.75, "cached": 0.075, "out": 3.75, "blended": 4.50},
    # PLACEHOLDER — no published rate read for the 3.8 tier. 3.7's blended rate
    # stands in; treat any cost comparison involving this lane as unmeasured.
    "gemini-3.8-flash-high": {"in": None, "cached": None, "out": None, "blended": 4.50},
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
    # PLACEHOLDER — no published rate read for GPT-6 Astra. terra's blended rate
    # stands in so the tie-break has a number; it is not a sourced figure, and
    # effort does not change a per-Mtok rate anyway (it changes token count).
    "gpt-6-astra":           {"in": None, "cached": None,  "out": None,  "blended": 14.00},
    "claude-opus-5":         {"in": 5.00, "cached": None,  "out": 25.00, "blended": 30.00},
    "claude-fable-5":        {"in": 10.00, "cached": None, "out": 50.00, "blended": 60.00},
}

#: Models whose blended rate above is a stand-in rather than a published figure.
#: Named here rather than inferred from a missing per-token field, because
#: `gpt-5.6-sol` has no per-token rate and a sourced blended one — inferring
#: would mark a real number as a guess and hide the two that are guesses.
#: A lane on one of these is `price_evidence: "placeholder"`, and the cost
#: tie-break abstains rather than ranking it against a measured figure.
PLACEHOLDER_PRICES = {"gpt-6-astra", "gemini-3.8-flash-high"}

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
#   "peer"    — a directive declares this lane level with one that WAS measured,
#               and the row is that lane's. Clamps exactly as "proxy" does.
#               `peer_of` and `peer_source` name whose row it is and who said so.
#   "none"    — unmeasured. The gate abstains and headroom decides alone.

# `frontier` marks a lane held back for the hardest work. It is excluded from
#   every ordinary route and reachable only when the caller asks for it, because
#   a lane that is always available is a lane that gets used by default.
# `route_guard` is the condition under which a lane's known weakness stops
#   mattering. It is printed with the route; satisfying it is the caller's job.
# `price_evidence` is "sourced" unless the blended rate is a stand-in.

LANES = {
    # --- the astra tiers ---------------------------------------------------
    # Owner directive of 2026-09-09: GPT-6 Astra is the OpenAI-family spine, and
    # the thinking level is the whole of the routing decision.
    #
    # PROBED 2026-09-09 from /tmp, codex-cli 0.153.4. `low`, `medium`, `high`
    # and `max` were each accepted and each returned a real answer; the header
    # echoed the requested effort in every case. The negative control ran the
    # same command with `-m gpt-6-bogus-xyz` and failed at the API with
    # `400 invalid_request_error ... not supported when using Codex with a
    # ChatGPT account` and NO output file — which is what makes the four
    # positives evidence rather than an echo of the flags.
    #
    # There is no bench row for astra at any effort, here or on DeepSWE, so
    # `bench_key` is None and `evidence` is "none": the shape gate abstains and
    # these lanes route on policy. Do not lend them a GPT-5.6 grade.
    "codex-astra-low": {
        "model": "gpt-6-astra",
        "blended_usd_per_mtok": PRICES["gpt-6-astra"]["blended"],
        "price_evidence": "placeholder",
        "family": "openai",
        "effort": "low",
        "cmd": ["codex", "exec", "-m", "gpt-6-astra",
                "-c", 'model_reasoning_effort="low"', "-s", "read-only",
                "--skip-git-repo-check", "-o", "{OUTFILE}", "{PROMPT}"],
        "fallback_cmd": None,
        "env": {},
        "verify": "codex-header",
        "meter": "codex",
        # A DECLARED peer, not a measurement. The 2026-09-09 directive puts
        # astra@low level with sol@high, fable@medium and grok@high, and
        # sol@high is the one of those three with an `exact` bench row. Reading
        # that row here is what "level with" means made checkable — and
        # `evidence: "peer"` is what stops it being mistaken for a reading of
        # astra. It clamps exactly as `proxy` does: never drop-in, never a hard
        # block. Delete the borrowed key the moment astra is measured directly.
        "bench_key": "codex/gpt-5.6-sol@high",
        "evidence": "peer",
        "peer_of": "codex-sol-high",
        "peer_source": "owner directive 2026-09-09",
        "tier": "workhorse",
        "probed": "2026-09-09",
    },
    "codex-astra-medium": {
        "model": "gpt-6-astra",
        "blended_usd_per_mtok": PRICES["gpt-6-astra"]["blended"],
        "price_evidence": "placeholder",
        "family": "openai",
        "effort": "medium",
        "cmd": ["codex", "exec", "-m", "gpt-6-astra",
                "-c", 'model_reasoning_effort="medium"', "-s", "read-only",
                "--skip-git-repo-check", "-o", "{OUTFILE}", "{PROMPT}"],
        "fallback_cmd": None,
        "env": {},
        "verify": "codex-header",
        "meter": "codex",
        "bench_key": None,
        "evidence": "none",
        "tier": "frontier",
        "frontier": True,
        "probed": "2026-09-09",
    },
    "codex-astra-high": {
        "model": "gpt-6-astra",
        "blended_usd_per_mtok": PRICES["gpt-6-astra"]["blended"],
        "price_evidence": "placeholder",
        "family": "openai",
        "effort": "high",
        "cmd": ["codex", "exec", "-m", "gpt-6-astra",
                "-c", 'model_reasoning_effort="high"', "-s", "read-only",
                "--skip-git-repo-check", "-o", "{OUTFILE}", "{PROMPT}"],
        "fallback_cmd": None,
        "env": {},
        "verify": "codex-header",
        "meter": "codex",
        "bench_key": None,
        "evidence": "none",
        "tier": "frontier",
        "frontier": True,
        "probed": "2026-09-09",
    },

    # --- the rest of the workhorse tier ------------------------------------
    # Named level with `codex-astra-low` by the same directive. They are peers,
    # not a descent: routing between them is a family and headroom choice.
    "codex-sol-high": {
        "model": "gpt-5.6-sol",
        "blended_usd_per_mtok": PRICES["gpt-5.6-sol"]["blended"],
        "price_evidence": "sourced",
        "family": "openai",
        "effort": "high",
        "cmd": ["codex", "exec", "-m", "gpt-5.6-sol",
                "-c", 'model_reasoning_effort="high"', "-s", "read-only",
                "--skip-git-repo-check", "-o", "{OUTFILE}", "{PROMPT}"],
        "fallback_cmd": None,
        "env": {},
        "verify": "codex-header",
        "meter": "codex",
        "bench_key": "codex/gpt-5.6-sol@high",
        "evidence": "exact",
        "tier": "workhorse",
    },
    "grok": {
        "model": "grok-4.6",
        "blended_usd_per_mtok": PRICES["grok-4.6"]["blended"],
        "price_evidence": "sourced",
        "family": "xai",
        # high, not xhigh, from 2026-09-09. The directive names grok-4.6 at high
        # as a workhorse peer and as a lane trusted to orchestrate; xhigh bought
        # thinking tokens above the tier this lane is being asked to hold.
        "effort": "high",
        "cmd": ["grok", "-m", "grok-4.6", "--effort", "high", "-p", "{PROMPT}"],
        "fallback_cmd": ["cursor-agent", "-p", "--force", "--model", "grok-4.6", "{PROMPT}"],
        "env": {},
        "verify": "grok-store",
        "meter": "grok",
        # The bench measured grok-4.5 under mini at xhigh — a different version,
        # a different harness AND now a different effort. Still `proxy`, and the
        # third gap is new: read the grade as a floor, not as this lane.
        "bench_key": "grok-4.5@xhigh",
        "evidence": "proxy",
        "tier": "workhorse",
    },
    "fable": {
        "model": "claude-fable-5",
        "blended_usd_per_mtok": PRICES["claude-fable-5"]["blended"],
        "price_evidence": "sourced",
        "family": "anthropic",
        # medium from 2026-09-09: named level with astra@low, and the effort the
        # directive puts design authoring on when a rough plan already exists.
        "effort": "medium",
        "cmd": ["claude", "--model", "claude-fable-5", "--effort", "medium", "-p", "{PROMPT}"],
        "fallback_cmd": None,
        "env": {},
        "verify": "relay-ledger",
        "meter": "anthropic",
        # Measured at high. Read down to medium it is a ceiling, not a reading.
        "bench_key": "claude/fable@high",
        "evidence": "proxy",
        "tier": "workhorse",
    },

    # --- orchestration-trusted ---------------------------------------------
    "glm": {
        "model": "glm-5.3",
        "blended_usd_per_mtok": PRICES["glm-5.3"]["blended"],
        "price_evidence": "sourced",
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
        "tier": "orchestration",
        # PROBED 2026-09-09 and DOWN: the proxy answered
        # `409 {"code":"no-eligible-account", ... "reason":"routing_forbidden"}`
        # — 1 of 1 account excluded from routing by Perch project settings. That
        # is a settings state, not a model or a capability fact, so the lane
        # keeps its policy place and `lane_probe.sh` is what says whether it is
        # reachable today. Allow the account in Perch, or add another, to clear.
        "probed": "2026-09-09",
        "probe_state": "409 routing_forbidden — no eligible Perch account",
    },

    # --- implementation, fast ----------------------------------------------
    "gemini": {
        "model": "gemini-3.8-flash-high",
        "blended_usd_per_mtok": PRICES["gemini-3.8-flash-high"]["blended"],
        "price_evidence": "placeholder",
        "family": "google",
        "effort": "baked-into-model-id",
        # --output-format json is not cosmetic: it is the ONLY place a token count
        # for this lane exists. Plain print mode records nothing, anywhere.
        "cmd": ["agy", "--model", "gemini-3.8-flash-high", "--output-format", "json",
                "-p", "{PROMPT}"],
        "fallback_cmd": None,
        "env": {},
        "verify": "output-nonempty",
        "meter": "gemini",
        # 3.8 from 2026-09-09; `agy models` lists gemini-3.8-flash-{high,medium,
        # low}, confirmed the same day. The bench measured 3.7 Flash, and a
        # predecessor's grade is not this lane's, so the key is dropped rather
        # than reused: the shape gate abstains and this lane routes on policy.
        "bench_key": None,
        "evidence": "none",
        "tier": "implementation-fast",
        # Its speed is the reason to pick it and the reason to bound it. The
        # 3.7 delivery measurement (8 of 12 dispatches failed, one fabricated
        # completion report) does not transfer to 3.8 — see DELIVERY_PENALTY,
        # which now checks the model it was measured on before it subtracts —
        # but the failure mode it found is exactly what an unspecified brief
        # invites, so the directive's condition is carried as a guard instead.
        "route_guard": "route implementation here only when a spec or plan already exists: "
                       "hand the lane the plan path, the files it owns and the acceptance "
                       "checks, and read the artefact back rather than the report",
    },

    # --- design, and the fail-back -----------------------------------------
    # Design work stays inside Anthropic's family. `opus-design` and `fable` at
    # medium are the authoring lanes when a rough plan exists; `fable-high` and
    # `opus` are what judge rendered UI, because judgement is the class where a
    # cheap pass is banked as a fact.
    "opus-design": {
        "model": "claude-opus-5",
        "blended_usd_per_mtok": PRICES["claude-opus-5"]["blended"],
        "price_evidence": "sourced",
        "family": "anthropic",
        "effort": "medium",
        "cmd": ["claude", "--model", "claude-opus-5", "--effort", "medium", "-p", "{PROMPT}"],
        "fallback_cmd": None,
        "env": {},
        "verify": "relay-ledger",
        "meter": "anthropic",
        # Measured at xhigh. Read down to medium it is a ceiling, not a reading.
        "bench_key": "claude/claude-opus-5@xhigh",
        "evidence": "proxy",
        "tier": "design",
    },
    "fable-high": {
        "model": "claude-fable-5",
        "blended_usd_per_mtok": PRICES["claude-fable-5"]["blended"],
        "price_evidence": "sourced",
        "family": "anthropic",
        "effort": "high",
        "cmd": ["claude", "--model", "claude-fable-5", "--effort", "high", "-p", "{PROMPT}"],
        "fallback_cmd": None,
        "env": {},
        "verify": "relay-ledger",
        "meter": "anthropic",
        "bench_key": "claude/fable@high",
        "evidence": "exact",
        "tier": "design",
    },
    "opus": {
        "model": "claude-opus-5",
        "blended_usd_per_mtok": PRICES["claude-opus-5"]["blended"],
        "price_evidence": "sourced",
        "family": "anthropic",
        "effort": "xhigh",
        "cmd": ["claude", "--model", "claude-opus-5", "--effort", "xhigh", "-p", "{PROMPT}"],
        "fallback_cmd": None,
        "env": {},
        "verify": "relay-ledger",
        "meter": "anthropic",
        "bench_key": "claude/claude-opus-5@xhigh",
        "evidence": "exact",
        "tier": "reference",
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
        "allow": ["gemini", "codex-astra-low", "codex-sol-high", "glm", "grok", "opus"],
        "balance": True,
        "shape_gated": True,
        "why": "Five lanes across four families write code, and Claude is the fail-back so a "
               "down lane never drops work. gemini leads where a spec or plan already exists "
               "— it is the fast lane by tokens per second, and its `route_guard` is the "
               "condition that makes the speed safe to take. Everything else is the workhorse "
               "tier, level with each other by the 2026-09-09 directive, so shape decides "
               "which are good enough and headroom picks between the survivors. The frontier "
               "astra tiers are not here: they are reached by asking for them.",
    },
    "hard": {
        "label": "The problems the workhorse tier could not hold",
        "allow": ["codex-astra-medium", "codex-astra-high", "opus"],
        "balance": False,
        "shape_gated": False,
        "why": "gpt-6-astra at medium and high is frontier capacity, and the directive of "
               "2026-09-09 reserves it for the most difficult problems. Reaching it is a "
               "decision somebody makes — `--task hard`, or `--hard` on another class — "
               "rather than a default a router drifts into. medium first; high is for the "
               "problem medium did not hold. opus stays as the in-family fail-back.",
    },
    "orchestration": {
        "label": "Running a multi-step piece of work and deciding what happens next",
        "allow": ["codex-astra-low", "grok", "glm"],
        "balance": True,
        "shape_gated": False,
        "why": "Three lanes are trusted to orchestrate as of 2026-09-09: astra at low in the "
               "GPT-6 role, grok-4.6 at high, and glm-5.3 through the Perch proxy, which the "
               "directive places level with opus-5 at high or xhigh. The bench cannot speak "
               "to orchestration — it grades a model building something — so this class is "
               "policy and headroom, and the gate abstains.",
    },
    "completeness": {
        "label": "Completeness critic",
        "allow": ["codex-astra-low", "glm", "grok", "gemini"],
        "balance": True,
        "shape_gated": False,
        "why": "Out of Claude's family by construction: Claude checking Claude is not an "
               "independent check, and it is the one thing the deeper Anthropic pool cannot "
               "buy. Four families are available here, which is what makes the exclusion "
               "affordable on every item.",
    },
    "general": {
        "label": "Non-referral, non-judgment work",
        "allow": ["codex-astra-low", "grok", "glm", "gemini"],
        "balance": True,
        "shape_gated": True,
        "why": "astra at low is the default worker for anything that is neither a referred "
               "decision nor a verdict. The other three are its named peers, so this class "
               "spreads rather than ranks, and shape narrows it where the bench can speak.",
    },
    "referral": {
        "label": "Referred decision / judgment / second opinion",
        "allow": ["codex-astra-low", "codex-sol-high", "fable", "grok"],
        "balance": True,
        "shape_gated": False,
        "why": "A decision referred out needs a different reader, not a bigger one. The four "
               "the 2026-09-09 directive names level with each other — astra at low, sol at "
               "high, fable at medium, grok at high — are exactly the panel this class wants, "
               "and they sit in three families, so independence is a lane choice rather than "
               "a compromise.",
    },
    "verification": {
        "label": "Task verification and same-family verification",
        "allow": ["opus"],
        "balance": False,
        "shape_gated": False,
        "why": "Acceptance verdicts run on claude-opus-5 at xhigh. This is the class where a "
               "wrong pass is banked as a fact, so it does not drop effort and it does not "
               "take the medium-effort design lanes. Fable is a judge, not a verifier.",
    },
    "design": {
        "label": "Design authoring",
        "allow": ["opus-design", "fable"],
        "balance": False,
        "shape_gated": False,
        "why": "Opus and Fable are the only lanes trusted to do design work, and the "
               "2026-09-09 directive puts that work at medium effort where a rough plan "
               "already exists.",
        # A class-level condition, because both lanes carry it and one of them
        # (fable) is also the referral lane, where no plan is wanted or implied.
        "condition": "medium effort here assumes a rough plan or design direction already "
                     "exists. Without one, the work is a different shape: give the lane the "
                     "direction first, or run it at design-review's efforts.",
    },
    "design-review": {
        "label": "Design review",
        "allow": ["opus", "fable-high"],
        "balance": False,
        "shape_gated": False,
        "why": "Rendered-UI judgement stays on Claude, and stays at the higher efforts. "
               "Authoring a design at medium is the directive; grading one is judgement, and "
               "the rule against cheapening a judgement class is unchanged.",
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
        # The model the measurement was taken on. A penalty applies only while
        # the lane still points at it. This field is the whole fix for a real
        # failure mode: the entry below was measured on Gemini 3.7 Flash, the
        # lane moved to 3.8 on 2026-09-09, and a penalty that kept subtracting
        # would be a predecessor's delivery record charged to a model nobody
        # measured. Point the lane back at 3.7 and it snaps on again.
        "applies_to_model": "gemini-3.7-flash-high",
        "measured": "2026-08-26, ~/Dev/dAIolog/docs/retro-2026-08-26/",
        "why": "Running as an autonomous builder it failed 8 of 12 dispatches, and one of "
               "the completions was fabricated: a 4,406-byte report claiming four schedulers "
               "created, against a ground truth of nothing created. Separately it is 95% of "
               "the window's cash for 20% of the output. The bench cannot see any of that, "
               "because a fabricated report grades as a delivered artefact.",
        "lift_it_when": "a dispatch set of 12 or more completes with no fabricated report and "
                        "a failure rate under 20%, measured the same way",
        "status_2026_09_09": "INERT — the lane runs gemini-3.8-flash-high, which nobody has "
                             "measured this way. The failure mode it found is carried instead "
                             "as that lane's `route_guard`, which is a condition on the brief "
                             "rather than a subtraction from a score.",
    },
}

# Where two lanes survive every earlier stage, this order breaks the tie before
# cost does. Owner directive of 2026-09-09: the workhorse tier is a set of peers,
# so this order is a tie-break between equals and never a ranking of them. It
# runs last, only between lanes already agreed equivalent on the measured number.
PREFERENCE_ORDER = ["gemini", "codex-astra-low", "grok", "glm", "codex-sol-high", "fable"]

#: Lanes held back for the hardest work. They are filtered out of every ordinary
#: route; `--hard`, or `--task hard`, is how a caller reaches them. A frontier
#: lane that is merely *allowed* becomes a frontier lane that is used by default,
#: which is the thing the directive reserving them is trying to prevent.
FRONTIER = {l for l, spec in LANES.items() if spec.get("frontier")}


def is_frontier(lane):
    """Whether reaching this lane has to be asked for."""
    return lane in FRONTIER


def delivery_penalty_for(lane):
    """The delivery penalty in force for a lane right now, or None.

    An entry that names `applies_to_model` is spent evidence about that model.
    It stops applying the moment the lane points somewhere else, because a
    measurement taken on one model is not a fact about its successor.
    """
    pen = DELIVERY_PENALTY.get(lane)
    if not pen:
        return None
    subject = pen.get("applies_to_model")
    if subject and (LANES.get(lane) or {}).get("model") != subject:
        return None
    return pen


def delivery_adjusted(lane, mean):
    """A lane's bench mean after first-party delivery evidence.

    Returns the mean unchanged when nothing in force has been measured against
    the lane.
    """
    if mean is None:
        return None
    pen = delivery_penalty_for(lane)
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

    The clamp: a lane whose evidence is `proxy` or `peer` is pulled into the
    guarded band from both directions. It cannot clear to drop-in, because the number came
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
    # A REF row on a lane that is NOT the reference lane. `opus-design` borrows
    # opus's row at a lower effort, so it grades REF by inheritance — and REF is
    # in neither DROP_IN nor GUARDED, so it would fall through to *refused*: the
    # most capable lane in its class, refused for scoring identical to the
    # yardstick. This is the "REF is not a verdict" rule, inverted. Guarded is
    # the honest band for it: measured as the yardstick, but not the yardstick.
    if raw == "REF" and lane != REFERENCE_LANE:
        gate = "AMBER"
    # `peer` clamps with `proxy` and for the same reason: the number was
    # produced by a different lane. A directive can say two lanes are level; it
    # cannot turn one lane's measurement into the other's.
    elif evidence in ("proxy", "peer") and raw != "REF":
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


def allowed_lanes(task, hard=False):
    """The lanes a class may use right now.

    Two lanes are dropped before anything else looks at them. An `unverified`
    lane is one nobody has watched answer. A `frontier` lane is one the owner
    reserved for the hardest work, and it stays out of every class — including
    the class that lists it — until the caller asks for it, because a lane a
    router can reach is a lane a router will reach.
    """
    lanes = [l for l in TASKS[task]["allow"] if not LANES.get(l, {}).get("unverified")]
    # Naming the `hard` class IS the request, so it authorizes itself. Nothing
    # else does: a frontier lane reached without somebody asking is the failure
    # this filter exists to prevent.
    if hard or task == "hard":
        return lanes
    return [l for l in lanes if not is_frontier(l)]


#: Classes `--hard` must not escalate, and why. Escalating one of these would
#: route work out of Anthropic's family, which is the invariant those classes
#: exist to hold — a harder design question is still a design question.
NO_ESCALATION = {
    "verification": "verification runs on claude-opus-5 at xhigh; a harder item does not "
                    "move it out of the family that grades it.",
    "design": "design work stays on opus and fable; a harder design is still a design.",
    "design-review": "rendered-UI judgement stays on opus and fable.",
}


def gate_lanes(task, shape, hard=False):
    """Split a class's allowed lanes into drop-in, guarded, refused and fail-back.

    A class that is not shape-gated, an unknown shape, or a missing matrix all
    produce the same answer: every allowed lane lands in `dropin` and nothing is
    refused, because abstaining is the honest result when there is no evidence.

    The reference lane is held out into `failback` whenever the class allows it.
    It is the yardstick, so it scores REF on every shape, and a band that
    counted REF as a pass would route everything back to the lane this gate
    exists to relieve.
    """
    allow = allowed_lanes(task, hard=hard)
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
    ("codex-sol-high", "max"): "gpt-5.6-sol never runs at max effort.",
    ("fable", "verification"): "fable does not verify code or tickets; route to opus.",
    ("fable-high", "verification"): "fable does not verify code or tickets; route to opus.",
    # gpt-6-astra accepts `max` — probed 2026-09-09, header echoed it and the run
    # answered. It is refused here anyway: the directive defines three tiers, and
    # a fourth nobody has placed would be a routing decision made by a CLI's
    # argument parser rather than by anybody.
    ("codex-astra-low", "max"): "the astra tiers are low, medium and high; max is unplaced.",
    ("codex-astra-medium", "max"): "the astra tiers are low, medium and high; max is unplaced.",
    ("codex-astra-high", "max"): "the astra tiers are low, medium and high; max is unplaced.",
    # Design authoring at medium is the directive's shape, and it rests on a
    # rough plan already existing. Judging rendered UI is not that shape.
    ("opus-design", "verification"): "verification runs opus at xhigh; opus-design is medium.",
    ("opus-design", "design-review"): "design review is judgement; use opus at xhigh or "
                                      "fable at high, not the medium authoring lane.",
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
    # RETIRED 2026-09-09, all four together. The owner directive makes gpt-6-astra
    # the OpenAI-family spine at three thinking levels, and these are GPT-5.6
    # lanes that no class routes to any more. They are recorded rather than
    # deleted because their measurements are still the best evidence anyone has
    # about that generation, and because putting one back should be a decision
    # somebody makes again rather than a line somebody restores.
    #
    # Nothing here was found wanting. `codex-sol-high` survives precisely because
    # the directive names sol@high as a peer of astra@low, which is the only
    # reason one GPT-5.6 lane is still routed and four are not.
    "gpt-5.6-terra@high": "RETIRED — was `codex-terra`, the default `general` worker at 62.0 "
                          "headline and $0.34 a task. astra@low holds that role now.",
    "gpt-5.6-terra@max": "RETIRED — was `codex-terra-max`, the strongest OpenAI lane on "
                         "brownfield work and the only non-Claude lane that held opus on "
                         "compound multi-group backend tasks, at $0.67 a task. The frontier "
                         "tiers are astra@medium and astra@high now. This row is the one to "
                         "re-read if astra ever measures short on brownfield integration.",
    "gpt-5.6-terra@medium": "RETIRED — was `codex-terra-medium`, the bulk lane at $0.14 a "
                            "task and 2.2 minutes. There is no cheap tier below the workhorse "
                            "tier any more; astra@low is both.",
    "gpt-5.6-luna@max": "RETIRED — was `codex-luna-max`, added 2026-08-26 on DeepSWE 1.1's "
                        "67% ±4 at $0.61 a task (110 points per dollar, the best on the "
                        "board) and probed answering the same day. It goes out with the rest "
                        "of the GPT-5.6 fleet rather than on its merits, and its cost record "
                        "is the strongest argument for re-reading this list if astra's own "
                        "cost is ever measured and comes back high. See EXTERNAL_BENCH.",
    "gpt-5.6-luna": "SUPERSEDED, then RETIRED — see EXTERNAL_BENCH['deepswe-1.1'] and the "
                    "row above. Local finding, kept for the record: luna@max lost 9 of 11 "
                    "shapes to terra@max and 10 of 11 to sol@max while costing more than "
                    "either ($0.72 a task against $0.67 and $0.47); luna@high lost 10 of 11 "
                    "to sol@high at $0.33 against $0.25. The relative COST ordering here did "
                    "not survive contact with a 113-task independent board and should not be "
                    "quoted onward without it.",
    "gpt-5.6-sol@medium": "RETIRED — was `codex-sol`, the referral lane. The 2026-09-09 "
                          "directive puts referral on the workhorse tier, which names sol at "
                          "HIGH; `codex-sol-high` carries that role.",
    "claude-sonnet-5": "Measured (52.9 headline, $1.61 a task) and genuinely strong on "
                       "greenfield modules and static pages, but it is an Anthropic lane, so "
                       "it relieves cost without relieving the dependency this routing exists "
                       "to spread. Add it deliberately if cost is the binding constraint.",
    "gpt-5.6-sol@max": "Ranked second overall at 66.6, statistically tied with opus, and the "
                       "best measured lane on regression-sensitive work. It stays out because "
                       "sol never runs at max, and sol@high holds 63.8 of that 66.6 at half "
                       "the price.",
    "gpt-6-astra@max": "Accepted by the CLI and answering — probed 2026-09-09, header echoed "
                       "`reasoning effort: max`. Unplaced: the directive defines three astra "
                       "tiers and this is not one of them, so FORBIDDEN refuses it rather "
                       "than letting an argument parser invent a fourth.",
}
