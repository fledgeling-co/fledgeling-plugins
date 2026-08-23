# vouch, calibrated for Gemini

Written against a Claude model's failure modes, and this house's deliberate *removals* — verification scaffolding above all — leave a vacuum on this family
that fills with something plausible. Read this once, before `## The one rule the rest follow`, then follow the skill with the overrides below; each names the
line it lands on. What needs work here: ten scopes stated as a class rather than a count, seven stated maxima that nothing reads back off the artifact, the
best gate suite in this repo still unable to see whether the passes before it ran, and one skill invocation phrased as routing rather than as a file.

## Epistemic status

`[docs]` is Google's own guidance, quoted verbatim from geminify's `references/gemini-corpus.md`. `[measured-family]` is two single Gemini sessions of *other*
skills (`Egress Gemini`, `COD Dossier`; n=1 each) plus a 106-task benchmark scoring `gemini-3.7-flash` against `claude-opus-5` at both effort levels —
geminify's `references/evidence.md` §1 and §2. `[derived]` is reasoning from those, applied here. Real figures in the ledgers below (88 rows, 18 suppliers,
105 documents, `PASS 24 · WARN 1 · FAIL 0`) come from this skill's own `references/evidence.md`, an August 2026 run driven by a **Claude** model; they make a
shape concrete and say nothing about Gemini, and a cell with no such source reads `fill`. **Tier:** every measured claim here is flash-tier —
`gemini-3.7-flash`, plus one `gemini-3.7-flash-high` session — and none of the rates project onto the Pro tier, whose `thinking_level` default and knowledge
floor both differ; there these overrides stand as `[docs]` discipline with every rate open.

**Unmeasured on this skill:** no Gemini run of vouch has been observed at all — not one row decided, not one gate run, not one report rendered. The
six-rung census, the one-to-one assignment, the filename audit, the four hand-off kinds and the empty-population render are docs-and-family reasoning applied
to this subject rather than observations of it, and no run anywhere has been measured *with* a `gemini.md` against the same work without one.

`[docs]` A conditional side-file is itself a shape the health checklist warns about — "Avoid writing a prompt with non-linear logic or conditionals that
require the model to piece together fragmented instructions from multiple different places in the prompt." Hence one pass, up front, each override naming its
landing site. `HIGH` is right for what Google says the level is *for*, "multi-step planning, verified code generation", and 3.7 Flash defaults to `MEDIUM`
while "If thinking_level is not specified, Gemini 3 will default to high" — no remedy for anything below.

## Route out before the first script runs

`[docs]` Under **Task outside of model capabilities**: "Avoid using prompts that ask the model to perform a task for which it has a known, fundamental
limitation."

`[measured-family]` Across 106 benchmark tasks, four of eight work buckets are level or ahead and two collapse into hard zeros — brownfield edits to an
existing multi-file repo at 16 against opus's 46, zero on 79% of decided rows. `[derived]` A vouch run mostly *executes* shipped scripts, which is not the
measured shape. Two parts of it are:

| shape | this skill's work | measured |
|---|---|---|
| `brownfield-integration` | patching `build_csv.py`, `build_reports.py`, `validate.py` or a template to fit an employer's form, and the `assets/report.css` rules whose comments name the defect each one fixed | 16 against 46 · zero on 79% of decided rows |
| `regression-sensitive` | any edit to `scripts/` that must leave the 21 blocking checks and the re-runnable invariant green | 42 against 65 |

```bash
python3 <defer>/skills/defer/scripts/lane_pick.py --task implementation --shape brownfield-integration
```

`[derived]` Omitted deliberately: `static-page`, because both reports and the hand-off page are rendered by shipped builders out of `claim_rows.json` rather
than authored from a prose brief — where a run *does* author a new section or a new employer's template from prose, that row applies at 22 against 67; and
`visual-design`, because the rendered surface is graded by `design-review`'s deterministic gates rather than judged aesthetically. **This routes the code
edits, not the claim** — reading invoices, deciding rows and running the gates are not what that corpus measured.

## What transfers intact

`[derived]` Named so you do not spend effort where there is no gap. **The one rule is already an objective constraint** — `[docs]` **Ambiguity** asks you to
"Avoid using subjective or relative qualifiers that lack a concrete, measurable definition. Instead, provide objective constraints", and `examined=N` beside
`found=M` is exactly that. **The stage chain is already artifact-gated:** `claim_rows.json` feeds the CSV builder, both reports and the gate, so no stage is
satisfiable by writing plausible output instead of running. **And the negative control on check 15 is this file's `gate` rule, arrived at independently** —
swapping two filenames took the audit from 88/88 to 86/88.

## C1 — ten scopes carry a class where they need a count

`[measured-family]` On `Egress Gemini` every requirement the brief *enumerated* shipped — twelve named features, all present — and every requirement named
*categorically* shipped once or not at all: all surfaces → 5, all states → **1**, all menus → **0**. `[docs]` **Too many tasks** explains why one pass
cannot satisfy several categorical nouns: "Break the requests into separate prompts."

`[derived]` The scan raised 45 categorical occurrences over 16 phrases across the skill and its nine references; 24 are prose and drop — defect narratives in
`evidence.md`, the reference list at SKILL.md:252–253, a quoted broken sentence at `gates.md`:210. Twenty-one survive as the scopes below, and the one the
scan missed decides every downstream row: SKILL.md:66 asks for the owner of *every card ending you find*. **Write this ledger before Stage 2.**

| Scope | Where | Denominator, and where N comes from | Reported |
|---|---|---|---|
| every card ending gets an owner | SKILL.md:66 | distinct endings in the feed *and* on the documents | fill |
| every claimed row traces to a filed document | SKILL.md:22 · `gates.md`:23 | rows in `claim_rows.json` | `88 of 88 filed` |
| every filename matches an id printed inside it | SKILL.md:191 · `gates.md`:58 | filed files, all extensions | `88 matched · 0 mismatch · 0 unreadable · 0 orphans` |
| every row placed on the six-rung ladder | SKILL.md:141, 144, 266 | rows × 6 rungs, per supplier | `88 rows · 18 suppliers · rung 4 = 11 rows, A$1,579.45` |
| every row keyed to the invoice covering its own period | `inclusion-rules.md`:98 | rows | fill — 14 landed on the wrong month before this rule |
| every matched pair inside the FX band | SKILL.md:163 | pairs whose invoice is in a foreign currency | fill |
| every figure in both reports derived, none typed | SKILL.md:222 · `outputs.md`:30 | interpolated figures per template | fill — prose has rotted 5 times here |
| every count-bearing section rendered once at zero | `gates.md`:232 | sections carrying a denominator | fill |
| a contested supplier's whole series, not the missing month | `inclusion-rules.md`:234 | invoices it issued in and around the period | `17 of 17 · 19 of 19` |
| every row re-decided after an operator correction | SKILL.md:233–234 · `inclusion-rules.md`:268 | **every row**, not the ones under discussion | fill — one real correction held 4 |

`[derived]` The last row fails silently: an exclusion propagates forward, and a *correction* does not propagate backwards unless something re-asks every row
whose stored reason names the thing that changed — so report the count that came back into scope **including zero**. Two extensions of the count contract the
skill already keeps: **derive the count where the brief omits one**, and **cover the cells rather than the top-level items** — 88 rows on a six-rung ladder is
88 placements, not 6, and the hand-off page's `portal`, `mail`, `account` and `statement` are four problems with four repairs, so summing them makes the
page's own opening sentence untrue.

## `bounded-constraint` — the maxima are what get exceeded

`[measured-family]` Over the same 106 tasks, 58% of Gemini's failing UI assertions at `medium` and **86%** at `high` state a bound — `exactly N`, `no`, `not`,
`only` — against 8% for opus and 6% for the OpenAI lane. The most-repeated one failed on *every instance in its set* on a run that passed 37 of its 39 other
assertions: the rule was read and agreed with, and a default idiom supplied the value underneath it.

`[derived]` That is C1 pointing the other way, and it reaches an artifact that looks like it passed — on a reimbursement claim, a schedule somebody signs. Of
the scan's 12 bound rows and 130 prose prohibitions, these are the ones attached to a countable property, read back off the **produced** artifact:

| instance | property | stated bound | readback | within? |
|---|---|---|---|---|
| every row, every filed file | citations, both directions | exactly 1 each way, zero orphans (`outputs.md`:96) | `validate.py` checks 12–16 | fill |
| every row | `excl + tax` against `incl`, and tax against ex-tax | equal ±0.005, and tax the **smaller** (`gates.md` 21) | `validate.py` checks 6, 21 | fill |
| every credit | charges it settles | exactly one, the later one (`inclusion-rules.md`:124) | `match.py`, `used` set both sides | fill |
| every charge and every invoice | assignments | exactly one each way (SKILL.md:151) | `match.py` `used_c` / `used_i` | fill |
| report prose | integer and money literals, spelled forms included | **0** (`gates.md`:149) | grep the *built* HTML, not the builder | fill |

`[docs]` Google treats these as a component in their own right — **Constraints** are "Restrictions on what the model must adhere to when generating a
response, including what the model can and can't do." — and names where they go: **Recap** is a "Concise repeat of the key points of the prompt, especially
the constraints and response format, at the end of the prompt."

`[derived]` That ledger is the recap, carrying values. **A bound written as a prohibition reads as style advice**, which is why the last row was converted by
hand: `gates.md`:149's *no integer or money literal in report prose* is a zero, and the shape most likely to be agreed with and then exceeded.

## C2 — verification is asked for, with the command attached

`[docs]` "Include specific verification steps in either the system instructions or your prompts directly." And from the agentic template: "Verify your claims
by quoting the exact applicable information (including policies) when referring to them."

`[measured-family]` What filled the vacuum on `Egress Gemini` is this skill's own nightmare: a self-written review asserting a browser engine that had failed
on all four invocation attempts and never ran, and a `100% pass rate on contrast` from a probe never executed — measured afterwards at 3.65:1 on every
primary button, one glyph at 1.00:1. Five well-formed rows, all `PASS`, over 40 cells of work.

`[derived]` Set that beside SKILL.md:25–33, which names the same three failures from a real claim. The override is the removal reversed: **every count in the
delivery note and in either report carries the command that produced it and that command's output**, and a count with no command reads `not measured`. A
denominator of zero is a gate that never ran, and an unrun check in the accountant's *how each figure was established* section is that review one level up.

## `gate` — 21 blocking checks that cannot see the passes before them

`[measured-family]` On `COD Dossier` the deterministic auditor validated tags, citations and contrast floors thoroughly, returned `0 error(s)` and exit `0`,
and had **zero checks** for whether the upstream skills had run, so two skipped invocations passed cleanly. `[derived]` `validate.py` has the same blindspot
by construction: its 21 blocking checks all read the finished CSV, the filed folder and `claim_rows.json`, and nothing in it fails when
`find_blind_days.py`, `classify_accounts.py`, `cross_check.py` or `card_on_document.py` never ran — each the only instrument for a class of error the others
cannot see. Run the receipts first and paste the result:

```bash
for f in claim_rows.json blind_days.json ladder.json cross_check.json card_census.json design-review.json; do
  [ -s "$f" ] && echo "OK   $f" || { echo "MISS $f — the claim is ungated"; exit 1; }; done
```

`[derived]` **Paste the gate's output, not a claim about it**, with the denominator beside every pass: `PASS 24 · WARN 1 · FAIL 0` says more than
*validation passed*. **A pass line with a zero denominator is the gate reporting it found nothing to check** — `gates.md`:74–82 exactly, where the
extractor's `=== <path> ===` banner made every file match its own name and 88 of 88 was a vacuous green. `[measured-family]` And the gate's binary shape
earns its own warning: on the benchmark's backend tasks a Gemini run passed **44 of 46 tests and 4 of 6 groups and scored zero**, because the headline was an
AND across independent groups. `validate.py` is that shape with 21 conjuncts, so *nearly green* is red.

`[docs]` Counts come from a script, never from reading a table and adding up: code execution "should be enabled whenever the model needs to perform any kind
of arithmetic, counting, or calculation."

## C4 — the one composition phrased as routing is the one that gets skipped

`[derived]` The scan found **zero** qualitative skill references here, which is unusual and good — but one line is that shape by hand. SKILL.md:215 reads
*Route to `design-review` for the deterministic gates*, and `gates.md`:99 repeats it. `[measured-family]` On `COD Dossier` that phrasing was satisfied by
writing compliant-looking code: neither `design-craft` nor `ux-craft` was invoked, and the run's own diagnosis named the mechanism — the constraints were
already in context, and nothing downstream depended on a file only those skills produce.

`[docs]` The remedy is chaining: "make each step a prompt and chain the prompts together in a sequence", where "the output of one prompt in the sequence
becomes the input of the next prompt."

`[derived]` So make the review a phase with a file behind it, and make the gate require the file. `proctor` at SKILL.md:114 needs no such conversion — its
output is a downloaded invoice on disk, already an artifact a later stage consumes.

```javascript
await Skill({ skill: "design-review:design-review" })   // against a SERVED copy, never file:// → design-review.json
await Read({ file_path: "design-review.json" })         // contrast, overflow, the 375px pass
await Bash({ command: "python3 scripts/validate.py --require design-review.json" })
```

## `visual` — twelve captures, and check the instrument before the page

`[measured-family]` `Egress Gemini` made 3 render calls and opened **4 images** for a five-surface artifact, then reported a contrast pass rate that was the
inverse of the truth. `[derived]` The denominator here is 3 surfaces (`Approval.html`, `Accounting.html`, the hand-off page) × 2 viewports (375, 1440) × 2
populations (full, and the outstanding set emptied per `gates.md`:204) = **12 captures, all opened**, reported as `12 of 12`.

`[docs]` "Ask the model to describe the images before performing the task in the prompt", and "point out which parts of the image are most relevant to the
prompt." A prompt can fail "because the model did not understand the image at all, or because it did not perform the correct reasoning steps afterward" —
which is why description comes before verdict.

`[derived]` So name what is in the crop — the sign-off panel, the schedule's last column, the fact bar — before calling anything wrong. **Check the instrument
before the page**: a headless browser refused loopback access wrote a 70KB all-white PNG with no error, and computed-style shorthands report `0px` where the
longhands are correct. **Verify a rendered fix by re-reading the recomputed value**, never by confirming the rule exists.

`[docs]` One lever this skill can supply and the benchmark never tested: "For UI generation, the model shows high design adherence and parity based on a
reference input, whether it's a screenshot, an image, or a full design system." `assets/report.css` and a capture of the last approved report are that input —
hand them over rather than describing the house style. Every static-page task in the corpus was a prose brief with no reference, so that path is documented
and unmeasured, not a promise.

## `authorship` — the document is the limit of truth

`[docs]` Google publishes a strictly-grounded system instruction meant to be used verbatim where output must not exceed its sources, and two of its clauses
carry this skill: "Treat the provided context as the absolute limit of truth", and "If the exact answer is not explicitly written in the context, you must
state that the information is not available." **Underspecified task** asks the same in reverse — "provide instructions for handling missing data rather than
assuming inserted data will always be present and well-formed."

`[derived]` Adopt it with the invoice as the context and two of the skill's rules become the vendor's. R8 — where nothing settles an account, *escalate and
add nothing* — is that last clause exactly, and nineteen invoices with an empty bill-to block are the case it was written for. R10 means **a figure derived
from an inferred rate is your claim, not the document's**: implied FX is a consistency check on matching, never an input to an amount. The tax
characterisation belongs to the accountant — state the arithmetic and cite the document.

`[docs]` One more, because brevity is this family's resting state: "By default, Gemini 3 models provide direct and efficient answers. If you need a more
conversational or detailed response, you must explicitly request it in your instructions." Both reports need that fuller reply — an exclusion without its
reason is a number that reads as an assertion. Trim preamble, never a reason.

## C3, C5 and C7 — retry ceiling, one worked row, read rather than recall

`[docs]` "On *other* errors, you must change your strategy or arguments, not repeat the same failed call."

`[measured-family]` Reading a 28.6k-token file against a 25k harness ceiling, `COD Dossier` retried `Read` **four consecutive times** with minor parameter
tweaks before pivoting to a Python split; `Egress Gemini` invoked one absent tool four times unchanged. `[derived]` Two attempts per tool, then change
approach; a permanent error gets one; **a capacity error gets none** — pivot on attempt 1 to a line-ranged read or a Python splitter. Three tripwires here
have that shape: a 2,444-row feed and large statement PDFs against the same ceiling; a mail search whose `after`/`before` are silently ignored, so retrying
the query retries the wrong instrument; and Cloudflare on two supplier portals, where SKILL.md:118's *stop and emit the wanted-invoices page* is a rule for
the first refusal rather than the third.

`[docs]` "We recommend to always include few-shot examples in your prompts", and "you can remove instructions from your prompt if your examples are clear
enough in showing the task at hand." `[derived]` Which is why every ledger above ships filled. Extend it into the run: take **one** row end to end at full
fidelity — charge, invoice read, bill-to block, ladder rung, one-to-one pin, filed as `<YYYY-MM>/<invoice-number>.pdf`, CSV line, report row — before the
other 87.

`[measured-family]` **A file named in a prompt gets loaded before the answer is written.** Asked a question naming three skills, `COD Dossier` answered from
memory without loading any; asked to fix that, it inverted the error and launched a skill instead of answering. `[derived]` Read, then answer, as two ordered
steps — here that covers the operator naming `references/inclusion-rules.md` or a prior claim file as much as it covers a skill.

`[docs]` Recall is not a source for published values either: "Your knowledge cutoff date is January 2025", and the remedy is that "Grounding with Google
Search connects the Gemini model to real-time web content, and should be enabled whenever the model may need to know obscure or recent facts."

`[measured-family]` `Egress Gemini` shipped Windows 10's accent colour on a Windows 11 app — a previous-generation *published* value returned confidently.
`[derived]` Three classes of value rot that way here and all three are on disk: a vendor's invoice-id label (one changed from `Invoice number:` to `Invoice
reference:` mid-series, and the first parse returned nothing for 15 of 19 documents), the statement closing day (read by `statement_cadence()`), and the tax
rate, where `--tax-rate 0` is a real jurisdiction rather than a way past check 21.

## Modules not written

`[derived]` `states` — the skill enumerates document *kinds* and hand-off *kinds* rather than UI states, and C1's ledger carries both. `platform-values` — no
vendor design system is cited; the values that rot are in C7. `delegation` — did not fire, and SKILL.md:240 already caps subagents at four. `emphasis` — zero
shouted tokens in 1,918 lines. `injection` — did not fire on the trigger vocabulary, though the surface is real: every invoice PDF, mail body and portal page
is content this skill did not author; until it earns a module, C2 and `authorship` carry the rule.

## The delivery note, on this family

`[derived]` The skill already asks for reported-not-blocking counts; here they have to be asked for. Figures are the recorded run's, `<n>` where it has none:

```
Universe   feed 2,444 rows · card endings <n>, owners confirmed <n> of <n> · feed-blind days 82 in 2 windows (38, 44), backfilled
Scopes     88 rows · 18 suppliers · 11 months · ladder 88 of 88 placed · rung 4 = 11 rows, A$1,579.45
Bounds     row↔file 1:1 both ways · credits 1:1 · prose literals 0 · subagents <n> of 4
Receipts   claim_rows.json / blind_days.json / ladder.json / cross_check.json / card_census.json / design-review.json — all present
Gate       python3 scripts/validate.py → PASS 24 · WARN 1 · FAIL 0   (21 blocking checks, AND across all of them)
           negative control: swapped two filenames → audit 86 of 88, both named, so check 15 is armed
Audits     filenames 88 matched · 0 mismatch · 0 unreadable · 0 orphans · card-on-document 11 of 105, mask forms read listed
           cross_check 3 pairs on both piles, each settled from the document · hand-off 40 of 87 kept, 47 removed (A$6,489.02)
Renders    12 of 12 captured and opened (3 surfaces × 375/1440 × full/empty) · design-review.json read, 0 blocking
Not run    <the honest list — a portal that refused, a statement never supplied, a supplier still undecided>
```
