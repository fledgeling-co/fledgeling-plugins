# Changelog

## 0.1.0 - 2026-11-07

First release. Put one decision to four model families (Fable, GPT-6 Astra, Gemini Argon and Grok, each resolved at run time to the newest model), in two option orders to cancel position bias, with a second round only on a split. `scripts/tally.py` applies the settle-or-split rule; `scripts/build_decision.py` refuses a page that counts a failed lane, hides dissent or names a winner nobody chose. The panel decides on the user's behalf and acts, except on anything destructive, irreversible, outward-facing or costly. Derived from feedback-panel 0.2.0 at Luke's request on 7 November 2026, for decisions that need no stakeholder feedback.
