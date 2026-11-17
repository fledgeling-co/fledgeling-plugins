# Changelog

## 0.3.0 - 2026-11-18

The panel is five lanes on the owner's 18 November 2026 roster. Fable moves to `claude-fable-5-2` at medium. Astra moves to `gpt-6.2-astra` at medium (from `gpt-6-astra` at high). A new `wonder` lane runs Meta's `muse-wonder-full-1.0` at high through the `muse` CLI, read-only with `--disable-write`. Grok stays on the newest Grok at xhigh, `grok-4.7` today. The Google lane is Gemini Argon at medium (from high), and runs the newest Gemini Hydrogen at xhigh when agy lists no Argon at medium or the Argon run fails or writes nothing; the lane log says `falling back to <model>`. A pinned `FP_ARGON_MODEL` skips the fallback, and `FP_WONDER_MODEL` overrides the new lane.

The Astra lane now runs the newest `codex` binary on the machine (`latest_model.py codex`, or `FP_CODEX_BIN`). Measured 18 November, the standalone codex 0.163.0 refused `gpt-6.2-astra` on a ChatGPT account, and the codex 0.169.0 the ChatGPT app bundles served it. Round one sends `r1a` to fable, argon and wonder and `r1b` to astra and grok; round two quotes Reviewer A to E. The tally rule is unchanged and covers five lanes: 4 to 1 is decided with dissent, 3 to 2 goes to round two.

Tested live on one brief: all five lanes answered. Argon at medium returned agy's 429 "Individual quota reached", and the lane answered on `gemini-4-hydrogen-xhigh`; a fake agy that refused Argon produced the same fallback.

## 0.2.1 - 2026-11-16

The Google lane is Gemini Argon again, and still never Hydrogen (owner directive, 16 November 2026, replacing the Carbon directive the same day). `latest_model.py gemini` takes the newest `gemini-<version>-argon-<effort>` that `agy models` lists, so a newer Hydrogen release is never picked. The lane is `argon` again; `carbon`, its name in the previous release, still runs it, and `FP_ARGON_MODEL` overrides the model (`FP_CARBON_MODEL` is still read).

## 0.2.0 - 2026-11-16

The Google lane is now `carbon` and takes Gemini Carbon, never Hydrogen (owner directive, 16 November 2026). `latest_model.py gemini` had been picking `gemini-4-hydrogen-high`, because at an equal version it compared model names and "hydrogen" sorts after "argon". It now takes the newest `gemini-<version>-carbon-<effort>` that `agy models` lists. agy 1.5.9, the current release, listed no Carbon on 16 November and refuses `gemini-4-carbon-high`, so until Carbon is listed again the lane runs Argon at the same effort and writes `agy offers no carbon model at high; using argon` to the lane log; it never falls back to Hydrogen. `argon` still works as a lane name and runs the same lane, and `FP_CARBON_MODEL` overrides the model (`FP_ARGON_MODEL` is still read).

## 0.1.1 - 2026-11-10

The Fable lane is pinned to `claude-fable-5-1` at medium effort (owner directive), replacing the `fable` alias at high effort, and receives the brief's directories via `--add-dir` so it can open the files it is told to read from its `/tmp` working directory. A one-line probe at the lane's own model and effort now fails the lane before the round when the account cannot answer, and its output is kept in the lane log: the failure that prompted this was a fast terminal 409 `no-eligible-account` error on every Claude model, which the old probe discarded and misreported as a 60-second timeout and a 429. The probe tries default setting sources first and, only on that terminal signature, retries with `project,local` so the stored claude.ai login can answer (`FP_FABLE_SETTING_SOURCES` forces the sources); the log records `setting_sources=`. `latest_model.py fable` resolves to the pin.

## 0.1.0 - 2026-11-07

First release. Put one decision to four model families (Fable, GPT-6 Astra, Gemini Argon and Grok, each resolved at run time to the newest model), in two option orders to cancel position bias, with a second round only on a split. `scripts/tally.py` applies the settle-or-split rule; `scripts/build_decision.py` refuses a page that counts a failed lane, hides dissent or names a winner nobody chose. The panel decides on the user's behalf and acts, except on anything destructive, irreversible, outward-facing or costly. Derived from feedback-panel 0.2.0 at Luke's request on 7 November 2026, for decisions that need no stakeholder feedback.
