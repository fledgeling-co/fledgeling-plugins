# Changelog

## 0.2.0 — 2026-09-01

- Parse Codex Desktop `response_item` transcripts as well as Claude message transcripts.
- Attribute a subagent audit from the first `agent_message` addressed to its declared
  `agent_path`, excluding inherited parent history and reporting the boundary explicitly.
- Advance model identity only from owned `turn_context` records and attach the current model to
  each call, including model changes within one session, so T7 cannot inherit the parent's family.
- Seed the first owned call from Codex's governing `turn_context` immediately before the addressed
  task message, but only when no intervening `response_item` makes that context parent history.
- Refuse to infer a model-less reviewer call's family from any later session model; T7 now reports
  the unknown call line as a probe that could not run and makes the scan exit 4.
- Apply the same refusal to nonempty models outside the known family vocabulary, on either side of
  the reviewer comparison; every reviewer call is now either compared or named as uncheckable.
- Record stable call ordinals and exact call/output pairing; fail closed when a Codex
  transcript has no recognized activity or contains orphan calls or outputs.
- Scope repository probes to transcript-attributable paths and distinguish accessed paths
  from modified paths, so unrelated concurrent commits and captures cannot clear or create a
  finding.
- Teach `slice.py` to render Codex messages, agent messages, calls, and outputs.
- Keep the Claude fixture suite green and add synthetic, redacted Codex schema, attribution,
  pairing, zero-recognition, and repository-scope controls.
- Adds a Gemini-calibrated `gemini.md`, so the conditional pointer already in `SKILL.md` now resolves to a real file instead of a missing one. Written by the `geminify` Mode A procedure and gated by `verify_quotes.py`.

## 0.1.0 — 2026-08-25

First release. Built from the forensic audit in `docs/gemini-audit/`: 18
Gemini-driven Claude Code sessions across 13 repositories, 148
adversarially-refuted findings, against a 37-session Claude control drawn from
the same repositories in the same window.

- `signals.py` — 16 transcript probes, alias-resolving before any "never ran"
  claim, output grouped so one shape is one row.
- `crossref.py` — 7 repository probes against an explicit git window.
- `worklist.py` — the eight-class total partition and its gate (exit 3 blocks on
  a standing `contradicted` or `laundered` row).
- `selftest.py` — 36 paired fixtures; every probe must fire on a dirty input and
  stay silent on a clean one.

Three probes were rewritten after firing on correct behaviour in real
repositories, and one was found matching nothing at all:

- `T10` never matched: the field arrives inside a JSON string, so `"armed"` did
  not match `\"armed\"`. A live run would have reported a clean pass.
- `T11` matched a `cat -n` line number as a gate denominator. Anchored to a single
  line, it went from three false hits to one true one.
- `R1` produced 13 hits against one repository, all of them correct behaviour —
  that repo commits ledger updates separately from the work by design. Re-asked
  over the item rather than the commit, it found one real case.
- `R10` and `R11` flagged test files, where "referenced only by its own test" is
  circular and a literal secret is how you test that literals are rejected.
