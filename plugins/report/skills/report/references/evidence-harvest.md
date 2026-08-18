# Evidence harvest — turning a session into a ledger

The phase that separates this skill from a nicely-typeset summary. A
session's conclusions are only worth publishing if a reader can tell
which of them were established, which were reasoned, and from what.

## Why a ledger and not just careful writing

Careful writing does not survive editing. A sentence gets tightened, a
hedge gets dropped for rhythm, two findings get merged into one clause,
and the claim quietly strengthens while the citation stays put. The
resulting page cites a source that supports something adjacent — which is
worse than an uncited claim, because the citation resolves and the reader
stops checking.

A ledger fixes the claim before the prose exists. The prose then renders
the ledger; when a sentence and its row disagree, the row wins or the row
changes, and either way the disagreement is visible.

## What to walk back through

Reconstruct the session in this order, because later items are only
trustworthy in light of earlier ones:

1. **Commands run and their output.** The strongest evidence available:
   a measurement someone can re-run. Record the command verbatim.
2. **Files read.** Path plus the line range that carries the point. A
   path alone is not a locator — it points at a file, not a fact.
3. **Tests, builds, benchmarks.** Record what passed, what failed, and
   the run's own summary line.
4. **Research already in the repo.** Reports under `docs/deep-research/`,
   prior `docs/reports/`, ADRs, specs. These are documents with their own
   provenance — cite the document, and where it matters, the section.
5. **URLs actually fetched in this session.** With an access date. A URL
   the session did not open is not a source; it is a lead.
6. **Screenshots and renders**, where the claim is visual.
7. **What the user said.** A constraint, a decision or a piece of
   domain knowledge the user supplied is legitimate evidence about *the
   user's position and requirements*, and is never independent
   corroboration that the position is correct. Attribute it as such.

## The row

```json
{
  "id": "c7",
  "text": "The ingest worker retries three times before dropping an event.",
  "kind": "direct",
  "confidence": "high",
  "sources": ["s3"],
  "support": "lib/ingest/worker.ts:88-104 — `maxRetries = 3` guards the catch",
  "limits": "Read from source. No runtime measurement; a deploy-time override would not be visible here.",
  "blocks": ["b2"]
}
```

- **`text`** is the claim as the reader will meet it. Write it at the
  strength the evidence carries, then let the prose render it — not the
  other way round.
- **`kind`** is `direct` or `inference`.
- **`confidence`** is `high`, `medium` or `low`, and it is about the
  evidence, not about how sure you feel.
- **`support`** names the specific passage, line range, output line or
  table cell. "See the worker file" is not support.
- **`limits`** is the sentence a sceptical reader would otherwise have to
  work out for themselves. Filling this in honestly is what stops a
  claim from drifting past its evidence.

Sources live in their own array so one source can back several claims and
the registry can deduplicate:

```json
{
  "id": "s3",
  "kind": "file",
  "locator": "lib/ingest/worker.ts:88-104",
  "title": "ingest worker retry guard",
  "accessed": "2026-08-09"
}
```

`kind` is one of `file`, `command`, `test`, `document`, `url`, `render`,
`asset`, `user`.

`asset` is an image, diagram or clip the report displays — a captured
render, a press-kit photograph, a licensed figure, a generated
illustration. It gets a row like anything else, because an image on an
evidence page asserts something and a reader is owed its origin. The row
carries the licence basis alongside the locator:

```json
{
  "id": "s9",
  "kind": "asset",
  "locator": "assets/queue-depth-panel.png",
  "title": "staging dashboard at 3,000 events/min",
  "basis": "captured here",
  "accessed": "2026-08-09"
}
```

`basis` is one of `captured here`, `press kit`, `CC BY 4.0`, `public
domain`, `vendor drawing`, `generated`. Where the basis cannot be stated,
the image does not ship — `references/source-imagery.md` carries why, and
what to write instead.

## Independent testing behind a paywall

A lab that publishes its ranking and keeps the measurements paid — Which?,
RTINGS, Consumer Reports, Choice, Stiftung Warentest, and the software
equivalents — is a `document` or `url` source, and a strong one. The row
shape is what keeps it honest:

```json
{
  "id": "c22",
  "text": "Which? rates the C3 a Best Buy and measured the highest carpet pickup in its 2026 group test.",
  "kind": "direct",
  "confidence": "medium",
  "sources": ["s14"],
  "support": "Published verdict and Best Buy badge; group test of 14 machines, same carpet and fill level across units.",
  "limits": "Score and ranking published; the underlying measurements are paywalled. Test year 2026."
}
```

The claim is about *what the organisation published*, which is precise and
checkable, rather than about a number you have seen — and `limits` says so
in a clause. Refusing such a source because the table is unreachable leaves
the report arguing from affiliate roundups and vendor claims, which is
worse evidence rather than more rigorous. Never redraw their tables.

## Inference rows

An inference names the claims it rests on, and the reasoning step is
written out. If the step cannot be written in one sentence, it is
probably two inferences and should be split.

```json
{
  "id": "c12",
  "kind": "inference",
  "text": "A burst above 3,000 events/min will drop events rather than queue them.",
  "from": ["c7", "c9"],
  "reasoning": "Three retries at the measured backoff exhausts inside the window that c9 measured the burst to occupy.",
  "confidence": "medium",
  "limits": "Neither claim was measured under burst; c9's figure is a single sample."
}
```

On the page this renders visibly as reasoning — a different marker, a
different type treatment, an explicit word. A reader skimming should
never mistake the model's arithmetic for the system's behaviour.

## The three ways this fails

Each of these has spoiled a real document, and the auditor checks for all
three because none is catchable by reading the prose alone.

**A quantitative or attributed claim with no source.** Numbers, dates,
percentages, versions, and anything of the form "X says" or "the team
decided". If it has no row, it does not ship. Saying "we did not measure
this" costs a sentence and buys the reader's trust in the rest.

**A source that supports something adjacent.** The classic shape is a
real, checkable statistic wearing a claim it does not carry — a study
that measured a screening proxy cited for the diagnosis, a benchmark on
one workload cited for workloads generally, a config default cited for
production behaviour. The citation resolves, so it survives every check
except reading the source against the sentence. When writing `support`,
quote or name the exact thing, and if that exact thing does not say what
the claim says, the claim changes.

**An inference rendered as a finding.** Usually accidental: the
reasoning was sound, the sentence came out declarative, and the marker
went on anyway. The `kind` field is what prevents it, which is why it is
not optional.

## Confidence and disagreement

Where sources in the repo disagree, the disagreement is a finding. Carry
it into the report as stated uncertainty rather than picking a side
silently — and characterise it no more strongly than the evidence does.
"Two specs give different figures and neither cites a measurement" is
accurate; "the spec is wrong" usually is not.

Where the session itself changed its mind, say so. A report that shows
the correction is more useful than one that presents the final answer as
though it arrived first, and it is the only version that lets a reader
judge whether the correction was sound.

## What the ledger feeds

- The citation markers and the source registry, generated rather than
  written.
- The TLDR section at the top of the report and the TLDR one-pager, whose
  claims are selected from the same rows so the two cannot disagree.
- The verdict layer, where the report recommends something: every pick is
  an inference row naming the claims it rests on
  (`references/product-verdicts.md`).
- Every image's caption and provenance line, from its `asset` row.
- The methods note, which is largely a summary of this file's contents
  for the specific run.
- The auditor, which reads `claims.json` and the built page and checks
  they agree in both directions.
