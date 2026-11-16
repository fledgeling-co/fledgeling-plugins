# Changelog

## 0.1.1 - 2026-11-10

The Fable lane is pinned to `claude-fable-5-1` at medium effort (owner directive), replacing the `fable` alias at high effort, and receives the brief's directories via `--add-dir` so it can open the files it is told to read from its `/tmp` working directory. A one-line probe at the lane's own model and effort now fails the lane before the round when the account cannot answer, and its output is kept in the lane log: the failure that prompted this was a fast terminal 409 `no-eligible-account` error on every Claude model, which the old probe discarded and misreported as a 60-second timeout and a 429. The probe tries default setting sources first and, only on that terminal signature, retries with `project,local` so the stored claude.ai login can answer (`FP_FABLE_SETTING_SOURCES` forces the sources); the log records `setting_sources=`. `latest_model.py fable` resolves to the pin.

## 0.1.0 - 2026-11-07

First release. Put one decision to four model families (Fable, GPT-6 Astra, Gemini Argon and Grok, each resolved at run time to the newest model), in two option orders to cancel position bias, with a second round only on a split. `scripts/tally.py` applies the settle-or-split rule; `scripts/build_decision.py` refuses a page that counts a failed lane, hides dissent or names a winner nobody chose. The panel decides on the user's behalf and acts, except on anything destructive, irreversible, outward-facing or costly. Derived from feedback-panel 0.2.0 at Luke's request on 7 November 2026, for decisions that need no stakeholder feedback.
