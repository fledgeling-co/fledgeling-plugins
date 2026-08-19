# Capture lineage — proving a picture depicts what it is filed under

A screenshot on an evidence page carries two claims, and the campaign has always
checked only one of them:

| Claim | Checked by |
|---|---|
| *these pixels came off a display server* | `on-glass.md` — lane proof, artifact, attach witness |
| *these pixels are of SURF-005* | **nothing, until this reference existed** |

The second claim is the one a reader actually relies on. A wall of captures is
read as "this is what the product looks like", and every caption under it is a
sentence the reader did not verify.

## The measurement that produced this file

A campaign over a bonded-networking product published 20 surface captures, and
`campaign.py check` cleared it: every case accounted for, 46 of 49 checked, every
`-glass` lane proved and witnessed. The captures were of three unrelated
documents — a project status report, the mock browser's own index page, and a
design accessibility doc. Twenty files held **six distinct images**; four groups
of four were byte-identical. `FLOW-004.01 Open pairing QR code sheet` showed a
questionnaire about Apple developer credentials.

Nothing in the chain was broken. Every component did exactly what it was written
to do:

- `attach-shots.py` matched `SURF-005.png` to `SURF-005` on a slug of the
  filename, which is string identity and not evidence.
- `evidence-page.py` rendered `shot` with `alt` taken from the step **label**, so
  a wrong picture arrived under a right-sounding caption.
- `campaign.py check` ran `inspect_raster` and the shared-artifact detector over
  `RASTER_RUNGS` cases only. The 26 `outcome`-rung cases citing those images were
  never inspected, and the `shot` field on surfaces and flow steps — the two
  fields the page actually renders as pictures — was inspected by nothing.
- `strict-check.py` counted armed × effect-rung × pass, all of which were true.
- `witness-worklist.py` reported 20 judgeable pairs. No verdict was ever produced
  for any of them, and nothing required one.

**The gated part of the campaign was sound and the ungated part was the part
people look at.** That asymmetry is the failure this file removes.

Run `prescan.py` from `be-my-witness` against the worst of those captures and it
returns `isEvidence: true, settled: true`, exit 0 — a real, contentful, settled
image of the wrong document. Deterministic image statistics cannot answer the
subject question. Only provenance can, and provenance has to be recorded at
capture time because it cannot be recovered afterwards.

## The borrowed shape

`warrant`'s `oracle` plane solved the identical problem one domain over. Its
premise: the worst thing a data-dense product can do is render a figure no source
supports, and a vision judge structurally cannot catch it because nothing on the
screen looks wrong (`I7` in that plugin's claim set). Its remedy is not a better
judge — it is four attributes on every displayed figure, of which
`data-source-ref` is load-bearing, and the rule that **a figure without one is
the defect the plane exists to find**.

Substitute *picture* for *figure* and the whole apparatus transfers:

| `warrant:oracle` | here |
|---|---|
| `data-figure-id` | `subject` — the surface or flow-step id this capture claims to depict |
| `data-source-ref` | `target` — the URL, bundle path, window id or file the channel was pointed at |
| `data-source-field` | `channel` — what took the picture, and through which API |
| `data-source-expr` | `derivedFrom` — for a crop or a composite, the capture it came from |
| `lineage_gate.py` | `capture-lineage.py --gate` |
| `tick_and_tie.py` | `capture-lineage.py --tie` — recompute the subject from the target and compare |

The analogy holds down to the failure mode. Tick-and-tie catches a total that no
longer equals the sum of its parts; the tie pass here catches a capture whose
recorded target does not resolve to the route its subject declares.

## The four attributes

Written by the **capturing process**, into `evidence/shots/captures.json`, one
entry per image. Not inferred later, and never derived from the filename.

```json
{
  "path": "evidence/shots/SURF-005.png",
  "subject": "SURF-005",
  "target": "http://127.0.0.1:3130/devices",
  "channel": "obscura-0.2.0/browser_screenshot",
  "derivedFrom": null,
  "sha256": "67a259…",
  "capturedAt": "2026-08-20T07:58:03Z",
  "conditions": { "viewport": [1440, 900], "dpr": 2, "theme": "dark", "settleMs": 1200 },
  "witnessed": "node server.js pid 69919 listening on 127.0.0.1:3130 (lsof TCP LISTEN)"
}
```

`subject` is a claim. `target` and `channel` are what make it checkable. A
capture with a `subject` and no `target` is exactly the unsourced figure
`lineage_gate.py` exits 2 on, and it is treated the same way.

## The gate ladder

`capture-lineage.py` runs four passes, each of which can end the run. They are
ordered cheapest-first and every one is exact — no pass on this ladder needs a
model, and that is deliberate: a judgement inserted here would be the thing the
ladder exists to make unnecessary.

**1 · Unsourced.** An image under the shots directory with no entry in
`captures.json`, or an entry with no `target`. Exit 2 naming each. This alone
would have caught the measured failure, because those 20 files were produced by a
capture step that never wrote a manifest.

**2 · Untied.** The entry's `target` does not resolve to the route, bundle or
window the subject's inventory record declares. A surface whose `route` is
`/devices` and whose capture names `file:///…/whats-left.html` is untied, and an
untied capture is a defect regardless of what the picture shows.

Resolution is per-lane and deliberately loose on the parts a harness legitimately
varies — scheme, host, port and query are normalised away; path, bundle id and
window title are not. A source path as a target (`…/DevicesHostView.swift`) is
untied by construction: a browser cannot photograph a Swift file, and a lane
whose surfaces carry source-file routes needs the on-glass channel rather than
the browser one. **That mismatch is the mechanical reason the measured campaign's
capture step got improvised into screenshotting whatever HTML was to hand**, so
it is reported with that explanation rather than as a bare path error.

**3 · Shared.** Two subjects, one `sha256`. Exact to detect, so it is detected
rather than trusted — the existing rule for raster-rung case evidence, now
applied to every `shot` the evidence page renders. Four surfaces sharing one
image is not a near-miss; it is a capture step that ran once and was filed four
times.

A legitimate share exists — one window genuinely serving two surfaces — and it is
declared in the entry as `"sharesWith": ["SURF-004"]` with a reason. Undeclared
sharing fails; declared sharing passes and prints, so the reader sees that the
wall has fewer distinct pictures than it has cells.

**4 · Unjudged.** A capture rendered on the evidence page with no `be-my-witness`
verdict against its reference. This one does not block on first run — it
ratchets, for the reason `strict-check.py` ratchets: a gate that opens 97% red is
switched off within a week. It prints the judged fraction with its denominator
and fails when that fraction **falls**.

## Why the witness step must actually run

`witness-worklist.py` has always produced the worklist. In the measured campaign
it produced 20 judgeable pairs and reported `0 blind`, and no verdict for any of
them exists anywhere in the repository. Two things made that possible and both
are now closed:

- **Nothing consumed the worklist.** A file naming work to be done is not the
  work. `capture-lineage.py --gate` now reads `witness-verdicts.json` and counts
  every unjudged capture against the ratchet.
- **The worklist could not have been executed as written.** Its `reference`
  entries named `.html` source files, and `prescan.py --reference` needs a raster.
  `evidence/shots/mock/` did not exist, so the pair-capture template had never
  run and `pairs.json` was hand-authored metadata describing captures that were
  never taken. A reference that is not a raster is now a hard error at worklist
  time rather than a silent failure at judging time.

## What this deliberately does not do

**It does not score the picture.** Density, entropy and unique-colour floors
cannot separate a failed capture from a legitimately sparse screen, and the
measured failure passed every such floor comfortably. `inspect_raster` already
records `bytesPerPixel` as a regression signal that never gates, for the same
reason, and nothing here changes that.

**It does not ask a model whether the picture looks right.** Frontier multimodal
models reach roughly 40% recall on fine-grained UI diffs and under 23% on hard
cases (`mockup-fidelity`'s measurement-enforcement reference), so a vision pass
is an explanation layer and never the gate. The gate is provenance; the looking
says what changed and where. That is `be-my-witness`'s own governing sentence and
it is adopted here unchanged.

**It does not trust a manifest written after the fact.** An entry whose
`capturedAt` postdates the image's mtime by more than the run window, or whose
`sha256` disagrees with the bytes on disk, is reported as reconstructed. A
reconstructed manifest is not evidence of provenance; it is evidence that
somebody wrote down what they believed.

## The seeded check

Borrowed from `mockup-fidelity`'s seeded-defect eval, and it is what stops this
file becoming ceremony. The gate must be watched to fail, using the campaign's
own rule that an assertion nobody has seen go red is indistinguishable from one
that cannot go red.

```bash
python3 capture-lineage.py <dir> --seed-swap SURF-001,SURF-002
```

Swaps two subjects' manifest entries in a scratch copy, runs the tie pass, and
asserts it exits 2. A run where the swap passes means the tie pass is not reading
what it claims to read — and that is the exact state the campaign was in before
this file existed, so it is the one result that is never a curiosity.

The answer key is three-valued, as in `mockup-fidelity`: **caught**, **declared
inconclusive with its reason**, or **false pass**. Only the third fails. A lane
whose channel cannot record a target — a hand-delivered screenshot, a photograph
of a device — is inconclusive by capability rather than caught, and it says so in
the entry as `"channel": "manual"`, which is admissible and is counted apart.
