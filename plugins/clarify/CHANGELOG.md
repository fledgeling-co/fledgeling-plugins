# Changelog

## 1.3.0 - 2026-08-16

The gate stops being a filter that ends in a question and becomes one that ends in a decision. Referral to another model family is now a step rather than an option, and a fork you can settle is one you settle.

- **A fifth gate, and its predicate is the axis rather than your confidence.** When the fork sits on your axis — craft, convention, anything reversible, anything where the alternative loses on every count — you take it and report the call in a clause. When it sits on theirs, you ask however certain you are. The obvious phrasing (*if you can name a recommendation, take it*) was written, reviewed and rejected: you can almost always name one, and a reason manufactured after the fact turns someone else's trade-off into your decision. The operational test is to name what the losing option would have been **better** at.
- **Gate 4 is mandatory for what reaches it.** Every technical fork surviving gates 1-3 goes to another model before the user. One lane by default, a three-family panel when the call is high-leverage and open. Panels are now also asked directly whether a better approach exists than the ones listed, because a missing option is a research failure and an out-of-family model is the cheapest thing that finds one.
- **Lanes pin their model and their effort.** `claude --model claude-fable-5 --effort high`, `codex exec -m gpt-5.6-sol` at high, `agy --model gemini-3.7-flash-high`, `grok -m grok-4.6 --effort xhigh`. The last two were previously unpinned and inherited whatever the CLI config held. Three CLI facts are recorded with how they were established, including that codex validates neither flag — so an empty output file, not a clean header, is that lane's real failure signal.
- **Dossier is a branch, not a rung.** Escalate to research when the answer lives outside the repo and needs sourcing; residual uncertainty about a design call is not a research question. Free lanes first (`research_plan`, `research_local_start`), the paid panel when the decision earns it, and say what it cost.
- **The marked recommendation has one home left.** A grounded fork no longer reaches the user, so `(Recommended)` now appears only on an unrecoverable-action question, on the reversible path. Everywhere else the mark is an error: the fork was either yours to take, or theirs to decide without a thumb on the scale.
- **`"irreversible": true` is a declared field, and the linter checks the two against each other.** Destructiveness cannot be read out of prose — *"delete the flags this week, or quarantine them?"* is a scope question containing a destructive verb — so keyword matching would demand a mark on exactly the question that must not carry one. The same flag exempts the stem from the plain-language rule, because naming the actual table is required there.
- **Two options by default, a third when the referral earns it.** Narrowing is what gate 4 now does, so a shape it rules out gets named in the preamble rather than taking a slot. The linter warns at three rather than erroring.
- **The review that shaped this release is committed under `docs/deep-research/`.** The codex lane hit a usage limit and is recorded as a failure rather than dropped; grok-4.6 and gemini-3.7 both answered, and both refused two of the proposed items for the same reasons. One of those refusals changed the design (gate 5's predicate). The other is shipped against their advice, with the cost written into `references/evidence.md`: a two-option default sharpens the one eval this skill loses 4-0, and whether gate 4's new question recovers it is unmeasured.

## 1.2.0 - 2026-08-15

Gate 4 grows from two lanes to the full decision stack, matching the shipyard pipeline's second-opinion canon.

- Four ordered lanes: fable (speed), then codex, agy and grok (independence), with per-lane wire verification, fallback on failure, harness substitution named, and the egress opt-out respected per invocation.
- A three-family panel for genuinely open, high-leverage forks: swapped option order, verdict-line answers, non-responses reported rather than dropped, and a split carried to the user as the finding.
- Dossier deep research for questions about the world rather than the repo: plan free, run the panel, verify citations, say the cost.

## 1.1.0 - 2026-08

- Gate 4 added: settle technical questions with a second model (fable-5 or gpt-5.6-sol via codex) before asking the user.

## 1.0.0 - 2026-08

Initial release: the gate, the craft, the handling; the payload linter; evals with a four-family blind panel (15-5).
