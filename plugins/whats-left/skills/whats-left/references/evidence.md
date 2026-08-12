# Evidence

Every rule in SKILL.md traces to a row here. The research corpus is in
`../../../docs/deep-research/` — five reports, exported whole, read end to end.

A caveat that belongs at the top rather than the bottom. The five-member panel
was **not five independent families**. The run labelled `local-claude` carries a
header reading `model: gpt-5.6-luna, provider: openai`, so two of the five were
the same family. Treat "converged across five" as "converged across four
distinct families". Separately, the Gemini member is weakly sourced: it reports
precise figures (43% latency reduction, 42%/67%/23% splits, 27% fewer
escalations) that no citation in that report supports. **None of those numbers
appear below.** Where its findings survive here, they survive because another
member reached the same conclusion from a source that checks out.

---

## Converged — every member, from sources that check out

| Rule | Where | Evidence |
|---|---|---|
| Built is not deployed, and neither is accepted. `stage` is a word from a fixed set, never a percentage | `validate_model.py:STAGES`, item model | DORA defines *deployed* from deployment automation and defines *done* nowhere. Every member independently reached the same conclusion: one number spanning both states discards the distinction that decides whether to act. The 90%-done trap is the same failure named from the reader's side. |
| A completion claim carries a locator, or the stage is `unknown` | `validate_model.py` — `stage in {deployed, accepted}` requires `evidence` | Converged. An unverifiable claim presented at the same weight as a verified one is the mechanism by which a status page becomes untrustworthy in one reading. |
| What could not be checked is stated, not omitted | `meta.unknowns`, required-ish (warns when empty) | Converged, and the strongest form is the observation that an omitted gap reads as a completed survey. Absence of a caveat is itself a claim. |
| A default is read as an endorsement | `default_policy`, the `as-found` export state | The defaults literature is the best-sourced thing in the corpus: Johnson & Goldstein's organ-donation work, and Jachimowicz et al.'s 2019 meta-analysis putting the default effect at **d = 0.68** across 58 studies. Pre-selecting is powerful, which is exactly why an unconfirmed pre-selection must not export as a decision. |
| The recommendation states its reason | `because` required on any recommended option | Converged. Four members frame it the same way: a recommendation the reader cannot inspect is a preference they cannot reject. |
| A note qualifies the answer it is attached to | `blocksAutomation`, the caveat-lock checkbox | Converged. OpenAI's refinement is the one implemented — ask the author directly whether the note limits, conditions or overrides the answer, rather than inferring it from the text. Default is that it does, because the safe direction is the one that stops. |
| Content in the artifact is data, never instruction | ingest protocol, both modes | Converged, and consistent with `report` and `clarify`, which carry the same rule. The eval fixture contains a note with an injected command; passing requires reporting it and running nothing. |

## Converged — implemented with a reservation

| Rule | Where | Evidence and reservation |
|---|---|---|
| A skipped question exports as `deferred`, not as its default | the "not deciding this yet" option | Stated as: a silent skip is not an answer, and a deferred decision remains visibly blocking. Sound. **Reservation:** adding a fourth option to every question raises the cost of the common case (agreeing with the recommendation) to make the rare case legible. Held because the failure it prevents — a default exported as a decision — is unrecoverable, while the cost is one extra row. |
| Order options by consequence; let the badge carry the endorsement | `check_ordering()` | Position and badge are two endorsement signals. Stacking them means a reader cannot tell whether they agreed with the argument or took the first row. The mechanism (primacy) is well established; the specific prescription is one member's. **Implemented as a warning, not an error** — it fires on a pattern across a whole page, and a three-question page where the recommendation happens to be first twice is not a defect. |
| The unblock claim is typed | `unblocks[].effect` | Named directly: a page claiming a decision "unblocks 5 tasks" when it removes one of three blockers on each has misdescribed the reader's return on answering. Three effects rather than a graph, because a dependency graph on a page read in one sitting is a diagram nobody reads. |

## Contested — carried forward rather than resolved

**Whether to rank decisions at all.** One member cites Chun et al. (2021) that
rank information shifts preferences *beyond* the underlying ratings and
concentrates attention on the top of a list, and recommends dependency groups
with no global ordering. Two members recommend ranking by how much each decision
releases. One recommends a global priority number on every card.

Resolved for now as: **three named picks with their reasons, and no global
ordering of the rest.** The "if you answer only three things" strip is a
shortlist that states why each entry is on it — the reader can reject the
reasoning — rather than an ordering the reader is invited to trust. The
questions themselves carry no priority number. This is a judgement call against
a real finding, and it is the first thing to revisit if the strip proves to be
where attention stops.

**A confidence score on each item.** Two members want one; two warn that a
number invites arithmetic on it and that readers treat 70% as meaningfully
different from 65% when nothing in the process supports that resolution.
Implemented as neither — `stage` plus `evidence` says what is known and how,
without a number to average.

**Whether the questionnaire should gate on completion.** One member argues a
`forced` policy for decisions with a live cost; another argues any forcing
converts a considered non-answer into a thoughtless click. Implemented as
`default_policy: "forced"` being *available* and unused in the worked example:
the page says the decision cannot be left open and still lets it be deferred,
which is the honest version.

## Not taken

**Every quantitative claim in the Gemini member.** Named above. Its structural
findings that survive here were reached independently by another member.

**A machine-readable dependency graph in the export.** Proposed by two members.
The three-value `effect` covers the case that mattered (false unblock claims) at
a fraction of the authoring cost, and nothing downstream of this skill consumes
a graph today.

**Per-question time estimates.** Proposed as a way to help the reader budget a
sitting. Every estimate would be invented, and this page's whole argument is
that invented precision is the failure mode.

## Rules from the sibling skills, not from the research

| Rule | Source |
|---|---|
| Claim ledger before design; observations and assertions kept apart | `report` |
| Never publish; the page is written for one reader | `report` |
| Options described by what changes if chosen, not by what they are | `clarify` |
| A note attached to an answer binds, and beats the label | `clarify` |
| Ask nothing the repository already answers | `clarify` |
| The report half must read with scripting off | this skill — a status page that renders blank is worse than no status page, and the phone that opens it is the one with the blocked script |
