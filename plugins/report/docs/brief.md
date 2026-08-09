# Brief — the agreed specification

Written before research and build, per `create-skill` Phase 0. This is the
spec the evals are written against and the thing to re-read when a later
phase drifts.

## What it is

Turn **the context a Claude session already has** into a designed, cited
report — HTML and PDF, in a full and a stripped-back variant. It performs
no new research. Its evidence is the session's own trail.

This is the sibling of `dossier-report`. That one *buys* a research
corpus and publishes one page to a subdomain. This one reads what the
session already did and produces a document that lands in the project.

## Trigger

`/report` for the full document, `/report tldr` for the one-pager. Also
fires on the plain-language forms Luke actually uses: "write this up as a
report", "give me a summary of what we found with a TLDR at the top",
"turn this session into something I can send", "make me a page about what
we just did".

Does **not** fire when the substance has to come from new research
(`dossier-report`), when the deliverable is a Diolog-branded A4 guide
(`create-diolog-guides`), or when it is a slide deck (`deck-craft`).

## Output

`<project>/docs/reports/<slug>/`

| File | What it is |
|---|---|
| `index.html` | The full report. Self-contained, one file. |
| `report.pdf` | The same document, paginated, motion stripped. |
| `tldr.html` / `tldr.pdf` | The one-pager. Same ledger, same brand. |
| `DESIGN.md` | Reused from the project if one exists, else generated from the topic and saved here. |
| `claims.json` | The claim ledger the citations are generated from. |
| `assets/` | Charts, and any `media-gen-pro` imagery. |

## The four settled decisions

1. **One source, page-safe blocks.** The report is built from discrete
   blocks that are page-break-safe. On screen it reads as one continuous
   report with motion; `@media print` paginates it to A4 and strips the
   motion. A scrubbed or pinned episode must carry an authored static
   frame, because it has no print equivalent.
2. **The whole session evidence trail is citable.** Files read (path +
   line), commands run and their output, research reports already in the
   repo, URLs fetched. A claim ledger is compiled before any design
   happens; a quantitative or attributed claim with no source does not
   ship, and a claim assembled by reasoning renders labelled as
   inference.
3. **The TLDR is a merged single page** — brand band, the finding in one
   sentence, one hero visual, 3–6 cited bullet claims, sources footer.
   One A4; two only when the source list is long.
4. **In-project, never publishes.** Writing files is the end of the run.

## Definition of done

- `index.html`, `report.pdf`, `tldr.html`, `tldr.pdf`, `claims.json` and
  a `DESIGN.md` all exist in `docs/reports/<slug>/`.
- The conclusion is reachable in the first screen and on page 1.
- Every quantitative or attributed claim resolves to a ledger entry with
  a locator; inferences are visibly labelled as inferences.
- Citations survive with JavaScript off: markers are `<a href="#rN">`,
  the registry is real DOM.
- Print output carries no motion, no clipped chart, no orphaned heading;
  the PDF's page count matches the block count.
- The auditor exits 0.
- A methods note states what the session did, what was read, what was
  verified, and what the report could not establish.

## Hard constraints

- Never invents evidence. "The session did not establish this" is a
  publishable sentence; a plausible number is not.
- Never publishes, deploys, or pushes.
- Never touches native scrolling. `normalizeScroll()` is prohibited.
- Motion never reaches the print output.
- Reduced-motion is the baseline, not an afterthought.
- Spending money (`media-gen-pro`) is announced before it happens.
- Subagents never run git operations.

## Checkability

Mixed, so evals are mixed. Structure, citation integrity, print
correctness and self-containment are objectively checkable and go in a
script. Whether the thing reads as authored rather than generated is a
judgment call and goes to a blind panel.

## Routing

| Concern | Goes to |
|---|---|
| Design system, layout, anti-slop | `design-craft` |
| Flow, states, comprehension | `ux-craft` |
| Every word of prose | `create-luke-content` |
| Rendered-UI audit | `design-review` |
| Charts and colour | `dataviz` |
| Imagery that earns its place | `media-gen-pro` MCP |
| Existing design system | the project's own `DESIGN.md` |

Reuses the citation markup contract, the claim-graph shape and the
auditor pattern from `dossier-report`; reuses the CDP-harness approach
from `create-diolog-guides`. Reimplements neither.

## Cost posture

Free by default. `media-gen-pro` is the only billed call, is used only
where an image genuinely improves the report, and never for charts,
numbers, labelled diagrams or anything with exact text — the MCP's own
guidance says image models garble those. The run says what it is about
to spend before it spends it.

## Stated assumptions

Proceeding on these; none were settled explicitly.

1. **No new research panel.** Luke's session instructions say not to use
   deep research unless requested, and his brief said "any dossier deep
   research that would be useful" — read as *use what is on disk*. The
   skill is built on `dossier-report`'s existing 225-source corpus and
   `create-diolog-guides`' typography research.
2. **The slug** derives from the report's subject, not the project name,
   so several reports can coexist in one project.
3. **A2 and wider formats are out of scope.** A4 portrait only.
4. **Light and dark** both ship for the HTML; the PDF is the light
   rendering.
