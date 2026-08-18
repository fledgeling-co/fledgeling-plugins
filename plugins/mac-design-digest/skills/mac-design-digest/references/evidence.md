# Evidence behind this skill's rules

Every structural rule in `SKILL.md` and `scripts/` that came from research rather than from the
skill's own history is cited here. Sourced by a four-backend Dossier panel run **2026-08-18**
(xAI Grok, Perplexity Sonar Deep Research, Google Gemini Deep Research, OpenAI gpt-5.6), fast
tier, 113 sources; full reports in `../../../docs/deep-research/`.

Read this file when a rule looks arbitrary, when you are tempted to relax one, or when a
downstream skill asks why a value carries the mark it does. **Where the panel disagreed, the
disagreement is recorded rather than resolved** — a held-loosely item is more useful than a
confident wrong one.

---

## 1. The capsule radius — the panel split 3–1, and this skill's predecessor held the losing view

**What the old skill said**, flatly, in prose: "Sketch encodes 'capsule' as ~3.4e38."

**What the panel found.** No vendor documentation defines any sentinel value for a fully-rounded
corner in the Sketch format.

| Backend | Position | Source root |
|---|---|---|
| OpenAI gpt-5.6 | No universal sentinel exists; `fixedRadius` and point `cornerRadius` are declared as plain numbers with no special-value semantics. Explicitly warns against canonizing `999`, `9999` or `0.5`. | `sketch-hq/sketch-document` schema YAML (rectangle, curve-point, points-radius-behaviour) |
| xAI Grok | Fully-rounded shapes use a **maximum corner radius toggle** computing `min(width/2, height/2)`, "rather than a fixed sentinel float (e.g. -1 or 999)". | sketch.com's own corners documentation |
| Perplexity Sonar | Marks the sentinel question `<INSUFFICIENT_EVIDENCE>`; recommends classifying capsules "based on measured relationships (for example, radius equal to or exceeding half the shape height within a tolerance)" to avoid "undocumented sentinel semantics". | Sketch file-format spec + JSON Schema |
| Google Gemini | Claims `9999.0` is a standard capsule sentinel. | A Flutter/Dart *widget library* changelog — a different ecosystem, not Sketch |

Three roots agree; the fourth's evidence is about a rendering library rather than the file format,
and its own wording is "rendering engines and UI frameworks frequently utilize", not "Sketch
specifies". **Held loosely:** it remains possible that a given Sketch build writes a
recognisable value for a maximum-corners shape. That would be a version-scoped observation, and
establishing it needs the controlled experiment OpenAI's report describes — author rectangles at
known dimensions with inspector radii at `0`, `r`, `min(w,h)/2` and above, save, extract, render,
compare — not a claim in a skill file.

**What this skill does.** `scripts/sketch_extract.py` reads a capsule from geometry (declared
radius reaching half the shorter side) and names the basis on every reading. That test subsumes
every claimed sentinel — `3.4e38`, `9999` and any other value above half the shorter side all
classify correctly without asserting that any float *means* capsule. A caller who has verified a
value against a specific kit may pass `--capsule-sentinel`; a negative radius is reported
unreadable rather than guessed at. **A capsule is `(inferred)`, never `(specified)`.**

Corroborating note from inside this marketplace: `mac-craft`'s `references/kit-macos-27.md`,
deconstructed from Apple's own macOS 27 Sketch JSON, records the push-button bezel as
"capsule `(estimated)` — no shape data in JSON". That extraction did not find a sentinel either.

## 2. `(specified)` is artifact-scoped, not universally normative

Apple specifies control sizes **semantically** — mini, small, regular/medium, large, extra large —
and tells developers not to hard-code heights; AppKit exposes `prefersCompactControlSizeMetrics`
for pre-macOS-26 metrics, and WWDC25 session 310 notes mini-through-medium became taller in
macOS 26. So an observed control height is versioned render behaviour, not a portable constant.

Consequence for the corpus: a control ladder extracted from a kit is authoritative **about that
kit revision**. Record `meta.json`'s `appVersion` and `build` plus the ingest date, per §4.

*Sources: Apple HIG Typography; WWDC25 session 310; AppKit updates documentation (via the OpenAI
and Perplexity members).*

### What Apple does specify numerically

Useful because it separates a mark from a guess. The macOS type ramp is published: Large Title
26/32, Title 1 22/26, Title 2 17/22, Title 3 15/20, Headline 13/16 Bold, Body 13/16, Callout
12/15, Subheadline 11/14, Footnote 10/13, Caption 1 10/13, Caption 2 10/13 Medium — with 13 pt the
recommended default and 10 pt the minimum, and no Dynamic Type on macOS. Clear Liquid Glass over
bright content carries a specified **35% dark dimming layer** recommendation. Concentric radius is
a specified *formula* — container radius minus the distance between corresponding corners, clamped
at zero — exposed as SwiftUI's `Edge.Corner.Style.concentric`, not a fixed token.

These corroborate the values already in `mac-craft`'s `native-foundation.md`, which is the
downstream consumer of this skill's marks.

*Sources: Apple HIG Typography and Materials; SwiftUI `Edge.Corner.Style.concentric`.*

### What stays render-measured, whatever the corpus grows to

Glass blur, lensing and refraction parameters, shadow hue and opacity, window and toolbar-shell
radius, sidebar width, toolbar height and item gap. Apple publishes adaptive *behaviour* for
these, not optical constants; Liquid Glass responds to the pixels behind the window, so its final
state is emergent. All four members agree on this boundary. It is why the skill's `Known limits`
says a token cannot be verified against a running app from here.

## 3. Prior-session prose is not evidence

Recursive training or conditioning on model-generated output degrades a distribution: tails
disappear, diversity falls, early-generation errors amplify. Shumailov et al., *Nature*, 2024
("AI models collapse when trained on recursively generated data") is the load-bearing citation;
self-consuming-loop analyses corroborate it, and the mitigation in the literature is **additive
accumulation with fresh real data, not replacement**.

Consequence, and the reason the synthesis rule reads the way it does: TASTE.md and ICONS.md are
*projections* of `apps/` and `patterns/`, which are only ever appended to from images and
archives. A synthesis pass that reads the previous synthesis and rewrites it is the corpus
consuming its own output, and the specific loss predicted by that literature — rare,
edge-case observations collapsing into a smoother, more confident, less true rule set — is exactly
what a design corpus exists to prevent. Perplexity's member names the symptom directly: earlier
versions recording several distinct radius values, later versions consolidating them into one
"canonical" value with no new primary evidence.

**Held loosely:** the panel also carries a genuine conflict here. Other work finds stability when
sufficient fresh real data, curation or controlled mixing is present, so the honest reading is
"never let synthesis become its own source", not "synthetic material is unusable".

## 4. Freshness has to be stamped because the upstream is mutable

Apple's HIG pages are live documents, not immutable versioned publications: they carry selected
update dates and change without a version number. The panel's recommendation is to preserve the
displayed change date where present, record the retrieval timestamp, and hash the exact response;
for a downloaded Sketch kit, additionally keep `meta.json`'s version, `compatibilityVersion`,
`appVersion` and `build`.

This is why every synthesis file carries `Updated <ISO date>` and the gate fails one that does
not. The failure it prevents is not confusion inside a session — it is a later reader, human or
skill, citing a year-old value as current because nothing on the page said otherwise.

## 5. The injection fence, and why it travels in the brief

Indirect prompt injection through content an agent reads is demonstrated rather than
hypothetical: **InjecAgent** (Zhan et al., ACL Findings 2024) benchmarks attacks where
instructions embedded in external content manipulate tool-integrated agents, and later work
evaluates the same risk arriving through *persistent memory*, which is precisely the shape of a
corpus written by earlier sessions of itself.

Two panel members independently recommend the same control: mark all ingested bytes as untrusted
at the boundary, wrap them in explicit delimiters with a preamble stating they are inert data, and
allow only a deterministic validator — never the model reading the content — to promote anything.
That maps onto this skill as three things: the fence sentence in `SKILL.md`, carried verbatim into
every subagent brief because the subagent cannot see the skill; `sketch_extract.py` flagging and
counting instruction-shaped strings while acting on none; and `corpus_check.py` as the only thing
that certifies a corpus write.

## 6. Independence, and the honesty of the 3-app bar

The bar is a governance threshold, not a discovered constant, and both the OpenAI and Grok
members say so in as many words — the latter noting that a nine-mark scheme with a three-source
rule "lacks a single peer-reviewed canonical reference" in the 2023–2026 literature. It is
defensible as conservative, and the skill should present it that way.

What the research does sharpen is **independence**. Sources are not independent because their URLs
differ; they share a root when they derive from the same assertion, artifact, editorial pipeline or
model output. Dependent evidence carries less probative value than independent evidence and
double-counting inflates belief. Applied here:

| Pair | Independent? | Why |
|---|---|---|
| Two surfaces of one app | No | One artifact, one root — which is why the profile accumulates rather than counting twice |
| Two apps, one developer | No | Already the skill's rule ("same developer counts once"); this is the general principle behind it |
| A kit value and a measurement of that kit | No | The second is a transformation of the first |
| Apple HIG and an Apple WWDC session | No, for corroboration | Different medium, one publisher and one internal design decision |
| A kit `(specified)` value and a shipping app's `(measured)` one | Yes | Different pipelines — and their disagreement is a finding, not noise |

*Sources: Strittmatter, Pilditch & Lagnado on reasoning about (in)dependent evidence; ProVe
(Amaral, Rodrigues & Simperl, Semantic Web 2023) on provenance that does not support the triple it
is attached to; WikiContradict (NeurIPS 2024) on models handling real knowledge conflicts poorly.*

The ProVe finding earns its own line in the limits: a citation that resolves is not a citation
that supports the claim. This skill's analogue is that a mark records how a value was obtained,
never that it was read correctly — which is what `Known limits` says about the gate.

## 7. Considered and not adopted

- **SMT solvers (Z3, Vampire) for corpus invariants**, recommended by the Gemini member. Rejected:
  the invariants here are arithmetic and regular expressions over markdown — count distinct
  members, compare a hash to a pattern, check a section is non-empty. A first-order solver adds a
  heavy dependency and answers questions this corpus does not ask. If the corpus ever carries
  logical rules that can contradict each other in non-obvious ways, revisit it.
- **A separate atomic-claim JSON store with markdown as a generated projection**, recommended by
  the OpenAI member as the stronger architecture. Genuinely stronger on paper, and rejected for
  this skill on purpose: the corpus is also read by humans and by sibling skills that load
  `TASTE.md` directly, and a format change would break `mac-craft` and every corpus already on
  disk. The projection discipline is adopted in the one place it costs nothing — synthesis reads
  profiles, never the previous synthesis (§3).
- **Content-addressed evidence blobs.** Partially adopted: the ledger already content-addresses
  every input by SHA-1 prefix and dedupes on it, which is the property that matters here. Storing
  the bytes is out of scope for a skill that does not own the user's screenshots.

## 8. The two mark families, and the interface with `mac-craft`

Recorded here because it was nearly got wrong twice, independently, in the same direction.

The marks are **two orthogonal families that compose**, not one family of four. `(estimated)(confirmed)` — a guess seen twice inside one app — is not interchangeable with `(specified)(canon)` — a published kit value corroborated across three independent apps. Both this rebuild's brief and the first draft of the `mac-craft` rebuild flattened them the same way; the source skill's own `corpus-templates.md` had them right all along, which is what caught it here.

Flattening is not a cosmetic error. It is the mechanism by which a single-surface guess becomes a platform value one file downstream — the exact failure the skill exists to prevent, since a wrong number in the corpus outlives the conversation that created it.

**The interface, verified against `mac-craft` as shipped** (checked 2026-08-18):

| | This skill writes | `mac-craft` reads |
|---|---|---|
| Precision | `(specified)` `(measured)` `(estimated)` `(assumed)` | same four, named *Precision* |
| Strength | `(inferred)` `(confirmed)` `(recurring)` `(canon)` `(contested)` | same five, named *Evidence strength* |
| Files | `TASTE.md` · `ICONS.md` · `apps/` · `patterns/` · `icons/` · `kit/` · `ledger.md` | `TASTE.md`, `patterns/*.md`, `kit/macos-27.md`, per-app profiles |
| Precedence | `(specified)` overrides estimates corpus-wide | Apple kit `(specified)` and HIG → corpus canon → direction tokens |

`mac-craft/SKILL.md` states outright that "the provenance marks are `mac-design-digest`'s", enumerates both families with the same values, and re-emits them unchanged. **Nothing in the vocabulary or the file shapes changed in this rebuild.** The one divergence is a label: that skill calls the first axis *Precision*; `corpus-templates.md` here calls it *measurement quality*. Same four values, same ordering, no behavioural consequence — worth aligning the wording eventually, not worth a breaking change now.

### Why precision is pinned and strength is not

Strength genuinely improves with diligence: see more independent apps, earn a higher mark. Precision does not — it is a property of *where the number came from*, so the only thing that moves it is finding a better source. An `(estimated)` reading never becomes `(specified)` by being seen more often.

A stateless check cannot enforce that. Both the before and after states are perfectly well-formed marks, and the mutation between them is invisible; there is no history to compare against. So the un-improvable axis is pinned: `corpus_check.py` writes `design-corpus/.precision-lock.json` on first run and fails a later strengthening until a better source is named in the ledger and `--accept-precision-change` is passed. A weakening passes with a note, because an honest downgrade is the measurement-honesty rule working.

The pin lives **inside the corpus rather than inside the script**, which is where this diverges from the analogous fix in `mac-craft`. That skill pins values inside its own gate because its references are files it ships and controls. This corpus is the user's and it grows without limit, so a baseline compiled into the gate could never cover it — the gate generates the lock instead, and nobody maintains it by hand.

### Where the composed-pair rule is scoped, and why it is not applied flat

A pair is required in `apps/`, `patterns/` and `icons/`. It is **not** required in `kit/`, and a strength mark there is refused outright: strength counts independent *app* sightings, and a kit is not an app, so a strength mark on a kit value asserts corroboration that does not exist. In `TASTE.md` and `ICONS.md` the strength mark is required and precision only when the rule states a number.

That scoping was measured rather than assumed. On the live 134-app corpus, 79 of 88 marked rows already carry both families; all 8 precision-only exceptions are `kit-macos-27.md` rows, and the single strength-only row is a qualitative canon rule about selection *geometry* with no number to qualify. A flat "always require both" would have failed nine correct rows and taught the next session to add a mark that means nothing.

## 9. Where the research contradicts a bundled reference

`references/macos-native-analysis.md` §4 says window corner radius is "fragmented across
frameworks in the macOS 26 era ... always record the observed radius per app; never assume a
constant." The Gemini member reports that macOS 27 enforced a **uniform** window corner radius
system-wide, and that macOS 27 reverted Tahoe's floating sidebars to edge-to-edge. The
first-party corroboration is partial: WWDC26 session 289 is cited by the OpenAI member for
sidebars reaching window edges, while the uniform-radius claim rests on press coverage
(9to5Mac, MacRumors).

**Held loosely, and the reference is deliberately unchanged.** "Record the observed radius" stays
correct under either reading, and it is the instruction that cannot go wrong. If a macOS 27 kit is
ingested and its window radii agree across window styles, that is the evidence that settles it —
and it will arrive as `(specified)` from the kit rather than from this file.
