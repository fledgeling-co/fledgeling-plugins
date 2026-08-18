# Structure & content diff — the layout/missing-node defects a style diff can't see

A per-property style comparison matches elements by **text** and compares **computed style**. That makes
it structurally blind to the *highest-frequency* real defects — a 2×2 grid rendered 1×4, a card laid out
`row` where the mock is `column` (icon **beside** vs **above** its label), a missing icon/divider/badge
node, a reordered or app-extra child, dash-vs-check bullets. The words and colours match, so the style
pass scores those "close" while the layout is wrong — exactly the gap a human reads as "looks very
different". This is anti-pattern #9 (style-without-structure) made mechanical.

> **Where this lives now.** The structural pass is no longer a separate script you run first. It is
> inside `analyze.js` MODE B, which emits it as the `structure` and `layout` finding classes alongside
> the style classes, from the same single capture. `structure-diff.mjs` and `extract-mock.js` were the
> standalone versions and **no longer exist**; the checks they carried are all in `analyze.js`. Read the
> sections below for what each check does and what it is blind to — the mechanics transferred, the
> invocation did not.
>
> Two of the three companions ARE still standalone scripts and still worth running:
> `content-diff.mjs` (content/data gaps that belong in the content pipeline, not in CSS) and
> `overlay.mjs` (a `mix-blend-mode:difference` view, used as the visual TRIGGER to go and measure).
>
> **The ordering rule survives the refactor, in a stronger form.** "Structure before style" used to mean
> "run this script first"; it now means what THE LAW says — fill the present/divergent/ABSENT breadth
> ledger before you read `findings` at all. A clean style list was never a section verdict, and a single
> merged findings array makes that easier to forget, not harder.

## Layout props and the `data-fid` anchor

`analyze.js` captures, per node, the **layout props** the structural checks consume —
`gridTemplateColumns`, `gridTemplateRows`, `gridAutoFlow`, `columnGap`/`rowGap`, `flexDirection`,
`flexWrap`, `position` — and a **`fid`** field read from `data-fid` / `data-fidelity-id` /
`data-testid`. Run both sides at the **same viewport** so geometry and grid tracks compare like-for-like.

Note `gap` is deliberately absent from that list: it returns `normal` in this engine while `rowGap` and
`columnGap` are correct (`engine-capability-matrix.md`).

### `data-fid` — kill text-collision mispairs

Pairing falls back to text, and text mispairs when a short string repeats across roles (nav "diolog" ↔ a
footer wordmark; a card heading ↔ a nav link). Put the **same** `data-fid="x"` on the matching ref **and**
target nodes and the matcher uses it first — exact, layout-stable, text-independent. Add it to any region
where you see a role collision.

## The structural checks — layout · missing · extra · child-count

*(now `analyze.js` MODE B; the block below is the historical invocation, kept because it documents the
flags and the report shape those checks still produce as findings)*

```bash
# HISTORICAL — this script was removed; the checks below now run inside analyze.js MODE B and
# arrive as `structure` / `layout` findings. Kept for the flag and report-shape documentation.
# node structure-diff.mjs --mock ref.json --app target.json [--anchor "<section text>"] \
  [--out .mockup-fidelity/diff/structure-report.md]
```

It consumed two capture dumps and wrote a `structure-report.md` plus a `.json` sidecar; the same
checks now land in `target.findings.json`'s `findings` array under the `structure` and `layout` classes.
Matches nodes by **`fid` → normalized text+tag → structural tag-path**. `--anchor "<text>"`
scopes both trees to the section whose nearest container (climbs ≤4 parents) holds that text.
The report's four buckets:

- **❌ Layout mismatches** — on matched containers: `grid-columns` (column **count**, so
  `repeat(4,1fr)` rendered as a 2-col grid flags), `flex-direction`, `gap`/`columnGap`/`rowGap`,
  `flex-wrap`, `justify-content`, `align-items`. Gap/justify/align/wrap are only reported on a
  flex/grid container (ignored on a block). Each row = `container · property · target vs mock`.
- **◑ Child-count differences** — a matched container with a different number of children =
  a missing or extra row/icon/divider *inside* it.
- **⊖ MISSING** — a mock node (meaningful text, **or** a visual element: svg/img/hr, or a small
  empty box with a background/border) that never matched a target node. A missing icon, divider,
  badge, or tile. **Build these — mock wins.**
- **⊕ EXTRA** — a target node no mock node claimed. An app-extra badge/line/wrapper. **Remove,
  or cite why it stays** (anti-pattern #1: a citation is external evidence, not a reason you
  author now).

Read it like the differ report: every layout/missing/extra finding is a structural defect →
fix it, or attach an external citation.

## content-diff.mjs — separate the CONTENT/DATA gaps from CSS

```bash
node content-diff.mjs --mock ref.json --app target.json \
  [--out .mockup-fidelity/diff/content-report.md]
```

Some "looks different" gaps are not CSS — they are **content/data**: a footer rendering
SEO-long page titles where the mock shows the short nav label, a closing band stored `light`
when the mock is dark, a missing heading. A computed-style diff can never see these (it
compares how text is *painted*, not what it *says*). This script LCS-diffs the ordered visible
text of both dumps and reports:

- **◑ Label-length mismatches** — same element, one text **contains** the other (SEO title vs
  short label). A **derivation/DATA bug** — fix the content pipeline, not the stylesheet.
- **⊖ mock-only** — copy/headings in the mock, missing from the target (add via content).
- **⊕ app-only** — copy the app renders the mock doesn't (remove or cite).

Fix every finding in the **content store** (DB seed, nav/footer derivation, source JSON) — ideal
end-state is to seed the target's content *from* the reference text, so content parity holds by
construction and only presentation is variable. Don't chase these in CSS.

## overlay.mjs — the fast VISUAL trigger (not proof)

```bash
node overlay.mjs --ref ref.png --app target.png [--out .mockup-fidelity/diff/overlay.html]
obscura fetch "file://$PWD/.mockup-fidelity/diff/overlay.html" --screenshot overlay.png
```

Zero-dep: reads two PNGs, writes a self-contained `overlay.html` with three views — a
`mix-blend-mode:difference` overlay (identical pixels → **black**, any divergence → **bright
edges**, so a missing icon/shifted card lights up instantly), an opacity-fade slider, and
side-by-side. The agent opens it and screenshots it. Use it as the **TRIGGER** to go *measure*
a region — never as the proof of a match (frontier vision recall is too low; anti-pattern #11).

## The order, and the verdict rule

1. **The structural findings** (`structure` / `layout` classes) → fix layout / missing / extra / child-count.
2. `content-diff.mjs` → fix content/data gaps in the content pipeline.
3. `overlay.mjs` → a visual trigger to go and measure, never a verdict.
4. **Then** the per-property computed-style findings.

A clean style list is **necessary, not sufficient**: it only style-checks elements present on both sides,
and it says nothing about any class the preflight silenced.

**A section's verdict is admissible only once the structural findings, the content gaps and the style
findings are all clean or every finding is cited — AND `capture.mjs --assert` exited 0.** A green style
list on its own is the failure THE LAW exists to prevent.
