# Changelog

## 0.2.0 - 2026-11-07

Every lane now runs the newest model its CLI offers, so a new release needs no skill edit. `fable` uses the claude CLI alias (`--model fable`, Fable 5.1 today); `argon` and `grok` are resolved at run time by the new `scripts/latest_model.py`, which reads `agy models` and `grok models` and picks the highest version, falling back to a pin with a warning if the listing fails. Grok moves to `xhigh`, the highest effort its CLI accepts (it rejects `max`), and to grok-4.7. The panel runs all four lanes by default, and each lane log records `model=<id>`. Requested by Luke on 7 November 2026.

## 0.1.1 - 2026-11-07

`run_panel.sh` closes the Fable lane's input (`< /dev/null`). Without it the `claude` CLI waited three seconds for piped input on every run and printed a warning into the lane log.

## 0.1.0 - 2026-10-26

First release: grounded triage, a second-family check, a two-round panel across up to four families (`scripts/run_panel.sh`), a design and UX refinement pass, the questions report with preselected recommendations and JSON export (`scripts/build_report.py`), and the answers loop that builds the answers and turns the report into a record. Drawn from a review of website feedback in diolog-website-oct, 24-26 October 2026.
