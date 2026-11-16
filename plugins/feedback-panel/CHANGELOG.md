# Changelog

## 0.3.0 - 2026-11-16

The Google lane is now `carbon` and takes Gemini Carbon, never Hydrogen (owner directive, 16 November 2026). `latest_model.py gemini` had been picking `gemini-4-hydrogen-high`, because at an equal version it compared model names and "hydrogen" sorts after "argon". It now takes the newest `gemini-<version>-carbon-<effort>` that `agy models` lists. agy 1.5.9, the current release, listed no Carbon on 16 November and refuses `gemini-4-carbon-high`, so until Carbon is listed again the lane runs Argon at the same effort and writes `agy offers no carbon model at high; using argon` to the lane log; it never falls back to Hydrogen. `argon` still works as a lane name and runs the same lane, and `FP_CARBON_MODEL` overrides the model (`FP_ARGON_MODEL` is still read).

## 0.2.1 - 2026-11-10

The Fable lane is pinned to `claude-fable-5-1` at medium effort (owner directive), replacing the `fable` alias at high effort, and receives the brief's directories via `--add-dir` so it can open the files it is told to read from its `/tmp` working directory. A one-line probe at the lane's own model and effort now fails the lane before the round when the account cannot answer, and its output is kept in the lane log: the failure that prompted this was a fast terminal 409 `no-eligible-account` error on every Claude model, which the old probe discarded and misreported as a 60-second timeout and a 429. The probe tries default setting sources first and, only on that terminal signature, retries with `project,local` so the stored claude.ai login can answer (`FP_FABLE_SETTING_SOURCES` forces the sources); the log records `setting_sources=`. `latest_model.py fable` resolves to the pin.

## 0.2.0 - 2026-11-07

Every lane now runs the newest model its CLI offers, so a new release needs no skill edit. `fable` uses the claude CLI alias (`--model fable`, Fable 5.1 today); `argon` and `grok` are resolved at run time by the new `scripts/latest_model.py`, which reads `agy models` and `grok models` and picks the highest version, falling back to a pin with a warning if the listing fails. Grok moves to `xhigh`, the highest effort its CLI accepts (it rejects `max`), and to grok-4.7. The panel runs all four lanes by default, and each lane log records `model=<id>`. Requested by Luke on 7 November 2026.

## 0.1.1 - 2026-11-07

`run_panel.sh` closes the Fable lane's input (`< /dev/null`). Without it the `claude` CLI waited three seconds for piped input on every run and printed a warning into the lane log.

## 0.1.0 - 2026-10-26

First release: grounded triage, a second-family check, a two-round panel across up to four families (`scripts/run_panel.sh`), a design and UX refinement pass, the questions report with preselected recommendations and JSON export (`scripts/build_report.py`), and the answers loop that builds the answers and turns the report into a record. Drawn from a review of website feedback in diolog-website-oct, 24-26 October 2026.
