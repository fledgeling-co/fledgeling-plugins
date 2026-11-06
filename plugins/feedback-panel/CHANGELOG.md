# Changelog

## 0.1.1 - 2026-11-07

`run_panel.sh` closes the Fable lane's input (`< /dev/null`). Without it the `claude` CLI waited three seconds for piped input on every run and printed a warning into the lane log.

## 0.1.0 - 2026-10-26

First release: grounded triage, a second-family check, a two-round panel across up to four families (`scripts/run_panel.sh`), a design and UX refinement pass, the questions report with preselected recommendations and JSON export (`scripts/build_report.py`), and the answers loop that builds the answers and turns the report into a record. Drawn from a review of website feedback in diolog-website-oct, 24-26 October 2026.
