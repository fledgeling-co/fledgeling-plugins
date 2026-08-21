# Where usage comes from, per lane

Everything here runs on a subscription, so the scarce resource is plan headroom
in the current window rather than money. This file says, for each lane, exactly
where the number in `lane_pick.py --report` comes from and how much to trust it.

The split that matters: **four lanes report a real utilization percentage that
the vendor computed, and three do not.** A number counted locally and divided by
a budget you set is an estimate wearing a number, and the report labels it Tier 2
so nobody reads it as a quota reading.

## Tier 1 — the vendor's own figure, already on disk

### Claude — Opus and Fable

`~/Library/Application Support/Relay/usage.json`, keyed by account:

```json
{"<account-uuid>": {"fiveHour": {"utilization": 64, "resetsAt": 1787327999},
                    "sevenDay": {"utilization": 51, "resetsAt": 1787878799}}}
```

Anthropic publishes **no absolute token or message ceiling** for Pro, Max 5x or
Max 20x — only relative multipliers, and the 2026-05-06 increase gave no new
numbers. So this percentage is not merely the best available reading of Claude
headroom; it is the only one that exists. Third-party estimates of "24–40 Opus
hours a week on Max 20x" are pre-doubling 2025 figures and should not be used.

Two windows are tracked. `lane_pick.py` ranks on **sevenDay**, because that is
what makes Claude comparable to a seven-day lane, and carries `fiveHour` as a
warning when it passes 90% — a full session window blocks a call while the week
is still wide open.

**Fable is metered at 50% of the same weekly pool** (Anthropic support article
9797557: Claude Fable is metered separately at "50% of weekly limits"). It is not
a second allowance; the same account load costs Fable half the headroom Opus
costs, which is why the report shows Fable at half Opus's percentage.

One open question, unresolved and worth knowing: **how cache reads weigh against
Claude quota.** Anthropic's support docs say cached content "doesn't count
against your limits when reused"; `anthropics/claude-code#45756` shows exhaustion
consistent with full-rate counting and the maintainer reply does not answer.
Since cache reads are 96–99% of token volume on this machine, the answer changes
any token-based estimate by two orders of magnitude. It does not affect the
percentage above, which is why the percentage is what gets used.

### Codex — Sol and Terra

The codex CLI writes the real thing into its own transcripts. Last populated
`rate_limits` payload in `~/.codex/sessions/YYYY/MM/DD/*.jsonl`:

```json
{"limit_id": "codex", "plan_type": "pro",
 "primary": {"used_percent": 100.0, "window_minutes": 10080, "resets_at": 1787801400}}
```

`window_minutes: 10080` is seven days. Early turns in a session carry a null
`primary`, so read backwards from the newest file until one is populated.

The reset instant also arrives in the error text when the limit is hit — *"try
again at Aug 27th, 2026 1:30 PM"* — which is a useful cross-check that the epoch
above decodes correctly.

## Tier 2 — counted here, divided by a budget you set

None of these three vendors exposes a quota endpoint that the credential the CLI
already holds can read. `lane_budgets.json` has an `api` hook for the day one
appears; it is deliberately unwired, because pointing it at a guessed URL would
turn "we cannot measure this" into a confident wrong number, which is worse.

### Grok

Source: `~/.grok/sessions/*/*/updates.jsonl`, `turn_completed` records:

```json
{"usage": {"inputTokens": 1694926, "cachedReadTokens": 1325952,
           "outputTokens": 36372, "costUsdTicks": 2752565200}}
```

`costUsdTicks` is **1e-9 USD**, and that unit is derived rather than documented.
Fitting 807 recorded turns gives $3.78/M fresh input and $1.66/M cached, which
sits between Grok 4.6's standard $2.00/$0.50 and its ≥200K long-context
$4.00/$1.00 — exactly where a CLI carrying a large repo prefix should sit. At
1e-8 the same fit implies $37.77/M, which no published rate resembles. A future
CLI that changes the scale would move this silently, so re-fit if the totals ever
look an order of magnitude wrong.

Published allowances for SuperGrok and Heavy **disagree by an order of
magnitude** across every third-party source — 500 messages a day in one, 8,000 to
10,000 in another — and xAI publishes none. So the budget is calibrated instead:
the default of 4,100 is the API-equivalent dollars recorded across seven days
that consumed one full plan period end to end. That is the closest thing to a
Grok allowance that exists anywhere on this machine.

The CLI does announce exhaustion, at least: a 402 carrying `"Grok Build usage
balance exhausted"`, and a 503 `all-accounts-exhausted` when a pool is spent.

### GLM

Source: Relay's per-request ledger, `spend/YYYY-MM.jsonl`, filtered to
`bindingId == "glm"`. Each record carries real token counts and a computed
`costUsd`, because everything reaches GLM through the proxy.

The budget is in **plan prompts**: the GLM Coding Plan Max tier is about 1,600
prompts per 5 hours and 8,000 per week, and the weekly window starts when the
subscription activates. Two mismatches to hold:

- **Relay counts requests, Z.AI counts prompts**, and Z.AI's own docs say one
  prompt may invoke the model 15–20 times. This over-counts, so the lane looks
  fuller than it is. Erring toward "fuller" is the safe direction for a router.
- **Peak-hour multipliers exist** (3× peak, 2× off-peak on some models; peak is
  14:00–18:00 UTC+8). Nothing here models them.

The Z.AI API key lives in the login keychain under service
`dev.perch.account.zai:e714ccf64231`. Reading it prompts for keychain access;
`lane_budgets.json` documents the `key_cmd` shape for wiring a real endpoint if
Z.AI ever publishes one.

### Gemini

**Two paths reach Gemini and they share one Google sign-in, so they share one
pool.** Counting either alone understates the lane badly — in the week this was
written, Relay carried 18,711 model calls against the agy CLI's 5,218.

- `agy` CLI → `~/.gemini/antigravity-cli/brain/*/.system_generated/logs/transcript.jsonl`.
  agy authenticates straight to Google and **records no tokens and no cost
  anywhere**, so its side is counted in `MODEL` responses, the closest unit to a
  Relay request.
- Claude Code → Relay's `agy:default` binding, in the same spend ledger. Relay's
  own account record confirms the shared credential: `provider: antigravity`,
  `subscriptionType: "Google sign-in"`.

Because agy reports no tokens, this lane cannot be metered in dollars at all. The
budget is in model calls, defaulted to a week of observed traffic.

## List prices, for the tie-break only

Published rates as at 2026-08-21, USD per million tokens. These do not bill
anything on a subscription; they exist so that two lanes within 20% of each other
on headroom break the tie on price rather than on sort order.

| Model | Input | Cached | Output | Blended |
|---|---|---|---|---|
| `gemini-3.7-flash-high` | 0.75 | 0.075 | 3.75 | **4.50** |
| `glm-5.3` | 1.40 | 0.26 | 4.40 | **5.80** |
| `grok-4.6` | 2.00 | 0.50 | 6.00 | **8.00** |
| `gpt-5.6-terra` | 2.00 | 0.20 | 12.00 | **14.00** |
| `gpt-5.6-sol` | 5.00 | 0.50 | 30.00 | **35.00** |
| `claude-opus-5` | 5.00 | — | 25.00 | **30.00** |
| `claude-fable-5` | 10.00 | — | 50.00 | **60.00** |

Two of these move on a schedule. **Gemini 3.7 Flash's rate is introductory and
doubles on 2027-01-01.** **Grok 4.6 doubles every token in a request once the
prompt reaches 200K** — not just the excess, the whole request — which a CLI
carrying a repo prefix crosses easily.

Sources: [xAI pricing coverage](https://benchlm.ai/xai/api-pricing) ·
[Gemini 3.7 Flash pricing](https://venturebeat.com/technology/googles-gemini-3-7-flash-targets-coding-and-agents-with-a-50-introductory-price-cut) ·
[GLM-5.3 pricing](https://venturebeat.com/technology/glm-5-3-hits-the-api-at-1-4-4-4-per-million-tokens) ·
[GLM Coding Plan tiers](https://docs.z.ai/devpack/overview) ·
[Claude usage limits](https://claudelimit.com/claude-max-limits/) ·
[SuperGrok limits, conflicting](https://aiveed.io/blog/supergrok-heavy-300-usage-limits-2026) ·
OpenAI and Anthropic figures cross-checked against
`~/Dev/perch/docs/reference/plan-limits-and-api-equivalence.md`.

## What is still not known

- Absolute message or token ceilings for any Claude tier. Never published.
- How `cache_read` and `cache_creation` weigh against Claude quota.
- Any authoritative xAI or Google per-plan allowance for CLI use.
- Codex weekly limit numbers in absolute terms — only the percentage is exposed.

These are gaps in what vendors publish, not gaps in searching. A deep-research
run would confirm they are unpublished rather than produce numbers, which is why
the design leans on measured percentages and calibrated budgets instead.
