---
name: panel
description: >-
  Produce the machine verdict on one item — one out-of-family grader on the verdict, lens lanes on
  orthogonal questions, and an adjudicator that routes a disagreement to the deterministic check
  that settles it. Deliberately not a jury and never a majority vote. Use per item once the oracle
  and assay planes are green, when a verdict needs an evidence digest that ties it to what was
  actually judged, or when two lanes disagree. It is the only plane in the plugin that calls a model.
---

# Panel — the verdict, and the evidence channel

The design problem here is not accuracy. It is that every artefact the verdict rests on is
reachable by the thing being judged. Frontier coding agents modify tests, overwrite timers and
monkey-patch evaluators to return success. On RE-Bench, a research-engineering benchmark, 30.4%
of runs exhibited reward hacking, and on some tasks every successful run did (`C14`). An audit of
a benchmark built specifically to be
trustworthy found 59.4% of the audited subset materially flawed and retired it (`C15`).

So the sequence below snapshots the evidence before anything judges it, and the verdict is void if
its digest does not match.

## Procedure

1. **Snapshot first, judge second.**

   ```bash
   python3 scripts/snapshot_evidence.py --root <repo> --diff <patch> --tests <dir> --captures <dir>
   ```

   Prints a content-addressed digest over sorted paths and contents, writes the snapshot read-only,
   and that digest travels with every verdict. A verdict whose digest does not match its snapshot is
   void rather than suspect.

2. **Neutralise tenant text before a vision lane reads a capture.**

   ```bash
   python3 scripts/neutralise_render.py --root <repo> --html <surface.html> \
       --out-judge <judge.html> --out-human <human.html>
   ```

   Elements marked `data-tenant-text` are replaced with length-matched neutral filler for the
   judge's capture, and left untouched for the human-facing one. The mitigation is for `C16`:
   image-borne prompt injection defeated four production vision-language models with lesion miss
   rates of 70%, 57%, 89% and 92% and attack success rates of 33%, 40%, 67% and 51% over 81 to 162
   cases each, as a black-box attack needing only control of part of the input. That was oncology
   imaging, and the transfer to a screenshot carrying customer-authored disclosure text is an
   argument rather than a measurement. Treat it as a mitigation, not a fix.

3. **Run the grader.**

   ```bash
   python3 scripts/lane_run.py --root <repo> --lane grader --digest <digest> \
       --prompt <brief.txt> --verdict-file <verdict.json>
   ```

   One lane, from a family other than the one that built the work. The out-of-family requirement is
   not about accuracy: author-judged acceptance is how roughly half of a 110-ticket corpus shipped
   not-as-specified while reading as complete (`C24`), and one grader that did not write the code
   fixes that. A second grader on the same question does not fix it twice.

4. **Run the lenses.** One lane per orthogonal question, in parallel. A lens is only a lens if its
   question can be answered without reference to the other lanes' answers.

5. **Adjudicate a disagreement by routing, not by counting.**

   ```bash
   python3 scripts/adjudicate.py --root <repo> --verdict <a.json> --verdict <b.json>
   ```

   It maps the disagreement to the check that settles it: a numeric claim to `tick_and_tie.py`, a
   missing-element claim to `lineage_gate.py`, a classification claim to `taxonomy_check.py`, and
   anything else to a named human with the reason. Asked to resolve by majority it exits 1, because
   majority logic is the failure `C2` measures.

6. **Write the verdict to the ledger** through `warrant:ledger`, with the digest, the lane ids, the
   model ids and versions, and the authorising tier.

## Three lane roles, and none of them vote

Read `references/why-not-a-jury.md` before adding a lane. The short form: nine frontier judges from
seven families supply about two effective independent votes, panel accuracy falls 8 to 22 percentage
points short of independent voting, the best single judge matches or outperforms the whole panel
across every tested condition, and established aggregation closes at most 11% of that gap even when
given the correct answers (`C2`). A second lane asking the same question buys an effect the
measurement did not find.

Lens lanes are different in kind, because they are not voting on one proposition. Two rules keep
that honest: a lens whose question depends on another lane's answer is a second vote wearing a
lens's name, and a lens whose question a script could answer belongs in `warrant:oracle` instead.

Keep lane counts even, or a single grader plus lenses. An odd number invites someone to count them.

## Output

`snapshot_evidence.py` prints the digest. `neutralise_render.py` writes two HTML files and prints
both paths. `lane_run.py` prints the verdict JSON and exits 2 on a schema or digest mismatch.
`adjudicate.py` prints the routing decision: which check to run, or which human to ask and why.

## Constraints

`inconclusive` is a terminal state that routes to a person, not a retry. ISO/IEC 17025, the
laboratory-competence standard, requires measurement uncertainty to be declared and treats an
inconclusive result as a valid result (`C13`), and forcing one to binary manufactures certainty
the pipeline does not have.

Run the grader against a read-only checkout with no write, commit or test-execution tools. A judge
that can edit the thing it judges fixes rather than reports, and the finding disappears from the
record.

Ask the find pass to report everything and filter in a separate pass. A review prompt saying "only
report high-severity issues" or "be conservative" is followed literally and reports less, which for
a verification pipeline is the worst available failure. `references/opus5-authoring.md` carries the
prompt shape.
