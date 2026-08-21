"""Lane registry — the single machine-readable copy of the routing policy.

`references/lanes.md` is the prose for a human; this file is what the scripts
read. When the two disagree the tests in `selftest.sh` fail, which is the point:
a policy that lives in two places drifts, and the drift is silent.

Effort is pinned per lane because a lane that inherits its config default is not
the lane anyone chose.
"""

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
    "claude-opus-5":         {"in": 5.00, "cached": None,  "out": 25.00, "blended": 30.00},
    "claude-fable-5":        {"in": 10.00, "cached": None, "out": 50.00, "blended": 60.00},
}

# --- the lanes -------------------------------------------------------------
# family      : independence group. A verifier must differ from the writer's.
# cmd         : argv template. {PROMPT} is substituted; nothing else is.
# env         : extra environment, applied on top of the caller's.
# verify      : how to prove the lane ran as routed (see wire-verify.md).
# meter       : which usage source `lane_pick.py` reads for this lane.

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
    },
}

# --- task classes ----------------------------------------------------------
# `allow` is ordered only where the order carries meaning; where a class names
# grok/gemini/glm together the balancer picks, not the order.
# `balance` marks the classes whose lane is chosen by measured usage.

TASKS = {
    "implementation": {
        "label": "Writing code",
        "allow": ["gemini", "grok", "glm", "opus"],
        "balance": True,
        "why": "Four families can write code. Spread the load; keep Claude as the fail-back "
               "so a down lane never drops work.",
    },
    "completeness": {
        "label": "Completeness critic",
        "allow": ["grok", "glm", "gemini"],
        "balance": True,
        "why": "Out of Claude's family by construction, and cheap enough to run on every item.",
    },
    "general": {
        "label": "Non-referral, non-judgment work",
        "allow": ["codex-terra", "gemini", "grok", "glm"],
        "balance": False,
        "why": "gpt-5.6-terra at high is the default worker for anything that is neither a "
               "referred decision nor a verdict.",
    },
    "referral": {
        "label": "Referred decision / judgment / second opinion",
        "allow": ["codex-sol", "fable"],
        "balance": False,
        "why": "A decision referred out needs a different reader, not a bigger one. sol at "
               "medium and fable at high are the two; sol never runs at max.",
    },
    "verification": {
        "label": "Task verification and same-family verification",
        "allow": ["opus"],
        "balance": False,
        "why": "Acceptance verdicts run on claude-opus-5 at xhigh. Fable is a judge, not a "
               "verifier: it does not grade code or tickets.",
    },
    "design-review": {
        "label": "Design review",
        "allow": ["opus", "fable"],
        "balance": False,
        "why": "Rendered-UI judgement stays on Claude. No other family reviews design here.",
    },
}

# Lanes that must never be selected, with the reason, so a caller that tries
# gets a sentence rather than a silent substitution.
FORBIDDEN = {
    ("codex-sol", "max"): "gpt-5.6-sol never runs at max effort.",
    ("fable", "verification"): "fable does not verify code or tickets; route to opus.",
}
