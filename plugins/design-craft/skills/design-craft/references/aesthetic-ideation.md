# Aesthetic Ideation: Widen the World Before You Commit a Look

Use this before `frontend-aesthetic-direction.md` commits a direction on any greenfield hi-fi surface, and again when a build came back as generic, bland, or "looks like the last one".

Subject-mining and Mobbin answer *what the page is made of*. They do not answer *which world this product lives in*. When those two are the only inputs, consecutive sites converge: cream editorial, dark-plus-acid, or three equal feature cards on a navy ground. That is the complaint this file exists to close.

The instrument is `trawl:trawl`, not a second pass of the same model asking itself to be creative. Diversity does not come from raising temperature or from "be distinctive". It comes from isolated parallel frames, an explicit textbook baseline, and a boss-gate that refuses a dazzling look that cannot do the page's job.

## When to run

| Situation | Tier | Why |
|---|---|---|
| Greenfield hi-fi, no brand, aesthetic axis free | `--any` (2 frames × 3–5 ideas) | Default. Standard tier is 8–14 Agent calls; that cost is for a brand identity that will last years, not every landing page. |
| Named brand identity, a campaign that has to be unlike anything in the category, or the user rejected a build as generic | `--standard` (5 frames) | The complaint is already evidence that `--any` would have been the right spend earlier. |
| Small tweak, copy change, Operate/Read surface matching an incumbent system, or a brief that already names a look | skip | A settled identity is not an ideation problem. |

State the tier in the direction contract's FORM block (the candidate you took and its rank). A silent skip is a skip; write `trawl: n/a — incumbent system` or `trawl: not installed` rather than implying a pass happened.

**Cap.** Invoke `trawl:trawl` once per commission. Do not spawn extra subagents on top of the ones that skill already launches. Do the looking of its shortlist yourself.

## What to hand `trawl:trawl`

Write a brief to disk and tell the skill to read it. The packet is the problem, not the question "what should this look like?".

```
PROBLEM: pick an aesthetic world for <product>, a <page-kind> for <audience>,
whose single job is <job>. Visitor mode is <Persuade|Operate|Read|Experience>.

NATIVE STACK: HTML/CSS (or the project's actual stack), the subject's materials
and vernacular, any incumbent tokens named below.

TEXTBOOK BASELINE (freeze this verbatim — it is the ban list):
The category-default page: centered hero, three equal feature cards, Inter-class
sans, one electric accent on a near-black or cream ground, logo-wall-as-proof,
and a zigzag of image/text splits. Name the category's own version of that
page in one sentence.

CONSTRAINTS:
- Mechanisms transfer; trade dress does not. No cloning a named product's marks.
- Consecutive commissions this session already used: <families / signatures>.
  Those are banned as the winning pick.
- The page still has to do the job. A look that cannot convert / operate / be
  read is a trap, not a win.
- Output worlds, not CSS. Each idea is a named world, a physical or graphic
  referent, one signature move, and where the analogy breaks.
```

Then invoke `trawl:trawl` with the chosen flag (`--any` or `--standard`) and that packet. If the user already typed `/trawl` or invoked `trawl:trawl`, do not invoke it a second time — take that run's shortlist.

## Design-specific frame seats

When you *are* the one filling frames (trawl not installed, or you are briefing its branches), the five seats are these, not software-architecture personas:

1. **Ordinary stakeholder** — a named person who will live with the page (night-shift operator, first-time buyer, hiring manager skimming a portfolio, a parent on a phone at the school gate).
2. **Operational constraint** — one font, one colour, print-only, no photography, 400px wide, or a 12-column newspaper grid. Constraint is what breaks the category default.
3. **Adversary** — the look this category must never be mistaken for, inverted into a positive: "guarantee this is not another AI-tool dark mesh" becomes a world that cannot be that mesh.
4. **Cross-domain mechanism** — architecture, cartography, a score, a kitchen, a workshop drawing, a railway timetable, a garment's construction. Name the mechanism, map it onto the page, and say where the analogy breaks.
5. **Wild seat** — one unfit-looking frame, exempt from fit judgment. Occasionally this is the reframe.

`--any` takes seat 4 plus the wild seat. That pairing is deliberate: the cross-domain seat is the one that actually moves a landing page off the category default, and the wild seat is the one that occasionally invents the brief.

## What comes back, and how to use it

Trawl returns a shortlist of mechanisms, a recommended pick, and the baseline. Translate that into this skill's direction procedure — do not ship trawl's prose as the page.

- Each surviving idea becomes one of the seven candidates in `frontend-aesthetic-direction.md` Phase 2, or replaces that list when the shortlist is already three mutually different worlds.
- The **baseline is banned as the committed direction** unless the user takes the standing exit (the category standard, played straight).
- The **boss-gate** still applies: if the dazzling pick cannot do the visitor-mode job (Persuade cannot convert, Operate cannot be scanned, Read cannot be read), take the baseline and say so. Novelty is not a floor.
- Record `TOOK` / `LEFT` the way `mobbin-trawl.md` does. `LEFT` is the line where you declined a world that would have cloned a named studio.

Write four lines into the artifact, next to the Mobbin ledger:

```
AESTHETIC IDEATION
  tier    --any
  frames  cartographer × wild (child's sticker album)
  TOOK    contour-survey sheet as the page grid (cross-domain)
  LEFT    Field.io generative mesh — launch-film grammar, this is a tools page
```

## When `trawl:trawl` is not installed

Say so in one line. Substitute with the verbalized-sampling already in `frontend-aesthetic-direction.md` Phase 2 (seven candidates, probabilities, take a lower-ranked one). That substitute is weaker: it is one model talking to itself, which is the failure trawl was built to prevent. Do not imply a parallel-frame pass happened.

## Session and project ledger

Before picking, read `references/diversity-ledger.md`. The project file at `<project>/.design-craft/diversity-ledger.json` retains the last five visual decisions. Initialise it if it is absent.

```bash
python3 scripts/diversity_ledger.py show <project>/.design-craft/diversity-ledger.json
python3 scripts/diversity_ledger.py check <project>/.design-craft/diversity-ledger.json   --kind visual --family industrial-utilitarian --topology "index-led split"
```

`check` exiting 1 is a conflict: rotate family, display face, topology, signature, palette family, or motion unless product truth or an explicit request overrides it. After the direction contract is settled, record the chosen values. A missing ledger, a skipped check, and a deliberate conflict are three different states; report which one it was.

Also list families and signatures already shipped **this session** in the artifact comment (`<!-- session-used: editorial-literary, swiss -->`). The project file is what survives the session; the comment is what a later turn in the same session can see without opening JSON.

## Boundaries

- **Worlds, not costumes.** A cartographic grid with Inter, a purple accent and three cards is the baseline wearing a hat. The mechanism has to change layout, type, density or material — at least two of those four.
- **Operate and Read still invert the anti-slop reflex.** On those modes, category convention is often a feature. Run ideation only when the brief asked for a distinct shell, or when chrome is allowed to carry identity; never to make a settings panel "memorable".
- **IP.** Extract mechanisms. Wordmarks, illustration style, a signature colour, a proprietary component's exact look stay under LEFT.
