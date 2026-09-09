# Changelog

## 1.6.0 - 2026-09-09

Gate 4's lanes move to the 2026-09-09 model roster, and the thinking level becomes part of what a lane *is* rather than a setting on top of it.

- **Four referral lanes, named level with each other, across three families.** `gpt-6-astra` at low, `gpt-5.6-sol` at high, `grok-4.6` at high and `claude-fable-5` at medium. Picking between them is a family and headroom question rather than a capability one, which is what makes an independent second opinion reachable without trading down — and what makes a three-family panel buildable out of the workhorse tier alone.
- **The frontier tiers are named and then ruled out for this job.** Astra at medium and high is for the most difficult *problems*; a fork that survived three gates is real but rarely hard in that sense. Length, stakes and your own uncertainty are not difficulty, and a panel of frontier lanes is not a better panel — three readings from three families beat one deeper reading from one, which is the finding the panel rung already rests on.
- **Two roles carried over from `defer` because they change what a referral is for.** Design questions go to Opus or Fable and nowhere else. `gemini-3.8-flash-high` is the fast implementation lane *once a spec or plan exists*, which makes it the wrong instrument for an open fork — an unspecified brief is the condition its guard exists for.
- **The CLI-facts block is re-measured and dated per row.** `agy` now lists `gemini-3.8-flash-high`; `codex exec` refuses to start outside a trusted directory without `--skip-git-repo-check`; codex 0.153.4 warns on an unknown model before the API refuses it. That warning narrows the empty-`-o` check without replacing it, because a *known* model still prints a clean header on a run that produced nothing. The astra row is backed by a negative control — a bogus model failed with a 400 and no output file — so it is evidence of acceptance rather than an echo of the flags.
- **The trigger check had three defects and reported nothing trustworthy through any of them.** Its parser assumed the transcript's `message` is always a dict; a `permission_denied` control event carries a bare string, and that crashed the whole check on a run whose only real problem was the gateway being briefly down. It read *any* `Skill` call as this skill firing, so a near-miss that correctly declined and invoked `agent-voice:agent-voice` was recorded as a false trigger. And the fix for that compared against the bare name `clarify` when the Skill tool reports `clarify:clarify` — the same `plugin:skill` naming mistake this repo documents elsewhere, made inside the check meant to catch it, and it scored a correct positive run as a miss. Rescored from the same transcripts, the check now reports what it always expected: **positive fires, near-miss does not**.

## 1.4.0 - 2026-08-21

Lane assignments move to `defer`. This skill no longer names a model or an effort of its own — it points at `lane_pick.py` for the model, the effort and the argv, and at `lane_run.sh` to run and wire-verify one in a step. A pinned lane restated in seven files is a policy nobody can change, and this one had already drifted.

- **The referral lanes are `defer`'s classes now.** Gate 4 routes a technical fork to `--task referral`; a panel is still three families, chosen by the same measured headroom rather than by a list written here.
- **`gpt-5.6-sol` drops from `max` to `medium` and grok moves to `4.6` at `xhigh`.** The measured `grok models` listing in the CLI-facts block is left at what it actually printed on 16 Aug.

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
