# Severity and report

## Severity scale

Four levels. Severity tracks **user impact** — not effort to fix, not reviewer taste.

| Level | Meaning | Test |
|---|---|---|
| **Blocker** | A user group cannot complete the primary task | Keyboard trap; unreadable text; broken flow step; checkout button unreachable by keyboard |
| **High** | Likely task failure or drop-off; blocks a secondary task with no alternative path; WCAG AA failure; dark pattern; injection attempt | Trunk-test failure; body contrast below AA; fake scarcity; silent overwrite of user work |
| **Medium** | Real friction or trust erosion; task completable via workaround, excess time or cognitive load | Inconsistent components; weak information scent; validation on keystroke |
| **Low** | Cosmetic; style-variance drift; subjective preference | Micro-copy tightening; minor spacing rhythm |

Severity = frequency × impact × persistence, plus market impact where reputation is at stake.

**Discipline:** use the whole range. If everything landed Medium, the review hasn't decided anything — different lenses measure different things, and real reviews have spread. Lower-plane failures cap the value of upper-plane polish: don't lead with colour nits when the flow structure is broken.

A cluster of Blockers or Highs in one flow is a **hotspot** — report it as one systemic finding needing redesign, not as a list of point fixes.

**When the failure is the surface rather than points on it, say so as the finding.** A patch list against a surface that failed wholesale reads as a plan to fix it, which is how a rejection becomes an approval — the reader works the list, clears every item, and ships something still broken in the way that mattered. The test is whether fixing every listed finding would produce a surface you would pass. If not, the top finding is "this needs redesigning, here is what it would have to become", and the point findings sit under it as evidence rather than as the work.

Assign severity at aggregation only, never during the find passes.

## Block vs advise

- **Two independent lenses landing on the same element or line** → block. Mechanical agreement is the strongest signal available without spending another pass
- **Single subjective flag**, especially anything derived from visual judgment → advise, non-blocking

The reason is alert fatigue. A reviewer that blocks on every padding discrepancy gets switched off, and then nothing gets reviewed at all.

## Agreement weighting

A finding two lenses raised independently outranks a same-severity single-lens finding. Three or more lenses is high priority regardless of each lens's individual estimate.

Merge duplicates into one entry and note which lenses caught it.

## Finding format

Every finding, no exceptions:

```
[SEVERITY] <screen / file:line / element> — <what's wrong>
→ Should be: <specific replacement — real values, real copy, real structure>
→ Why: <observation → mechanism → consequence>
   (Tier: 1|2|3) (Lenses: scanning, heuristics) (Evidence: crop-07.png @2x, 375px)
```

Fixes must be executable without design interpretation.

Not a fix: "Make the CTA stand out."

A fix: "PrimaryButton: `#6B7280` → `var(--color-brand-primary)` (`#2563EB`); contrast against white text 3.8:1 → 8.6:1. Demote the adjacent 'Learn more' to a text link — one primary per screen."

Tier 3 items don't get a severity. They go in Open Questions phrased as questions.

## The coverage block

Mandatory. Goes at the top of every report, above the findings, and is never omitted or softened.

A review's largest failure mode is not a wrong finding, it is a confident silence over a region nobody looked at. `reliability-envelope.md` says it about lint rules — *"Coverage is silent. A rule whose selector matches nothing passes without warning"* — and it applies to the review itself with equal force.

**The verdict line carries the fraction, not just the coverage block.** A partial review is formally indistinguishable from a finished one: same headings, same verdict, and readers read findings before they read a block at the top. So the fraction rides in the sentence nobody skips:

```
**Verdict:** Needs work (7 of 14 surfaces reviewed; 3 stages open on 4 of them) — <one sentence why>
```

A complete review says so the same way — `(14 of 14 surfaces, all stages)` — so the absence of a fraction is never what marks a review finished.

```markdown
### Coverage
- Screens: 14 of 14 at 1440; Board only at 375/768/1024/1920
- Component types: 31 of 83 cropped and opened (all layout-flagged, all interactive, all with ≥3 instances)
- States driven: default, empty, focus, hover on Ledger. Loading/partial/error/offline not driven
- Probes: full `runAll` on all 14 screens. `analyze_styles.py` on Board only
- Ledger: `<workdir>/worklist.md` — 14 rows, 0 open cells
- Not looked at: `directions.html`, the toast, the state gallery
```

Three rules keep it honest:

- **The component fraction is a count, not an impression.** `probeComponentInventory()` gives the denominator; the numerator is crops you actually opened. If you did not run the inventory, the fraction is `? of ?` and say so.
- **The surface fraction comes from the stage-0 worklist**, not from what you happened to review. A denominator set after the fact always equals the numerator.
- **"Gates clean" and "design sound" are two sentences.** Write both or neither. A report opening on "0 contrast failures across 14 screens" will be read as a verdict on the design no matter what the rest of it says.

## Report template

Drop any section with nothing in it — except Coverage and Needs verification, which are never empty. An empty heading is padding with extra steps.

```markdown
## Design/UX review — <scope>

**Verdict:** Solid / Needs work / High risk — <one sentence why>

### Blockers & High
<findings, quick wins first within each severity>

### Medium
<findings>

### Low / Polish
<compressed bullets — no full format needed>

### Cross-cutting themes
<patterns multiple lenses caught independently — these are the real story; max 3>

### What's working
<short, factual — practices to keep, and what a fix must not break>

### Open questions
<Tier 3 prompts; unclear deviations; anything needing a product decision>

### Needs verification
<what a static or automated review cannot prove — never empty>

### Suggested order
1. <highest impact-per-effort first>
```

Keep the report proportional to the surface. A single screen gets half a page, not the full scaffold. Don't restate the findings in a closing summary.

## The closing block

Three lines, mandatory, at the end of every review. The third is what keeps the first two honest.

```
Gates:       lint clean · overflow probe clean · 0 console errors · CWV pass (lab)
Looked at:   12 component crops @2x, hover + focus states, 375/1280
Not checked: 1920px, print stylesheet, chart empty state, screen-reader output
```

Line 1 is what a machine asserts. Line 2 is what *you* assert, and it is only true for captures you actually opened. Line 3 is never empty — if you believe it is, you have confused the scope of your checks with the scope of the artifact.

**Never merge "the lint passed" with "verified."** Those are two claims and they belong in two sentences. A gate is downstream of the findings that motivated it: it proves a known defect has not returned; it is structurally incapable of finding the one nobody has met yet.

## Don't invent findings

A clean surface gets a clean verdict and at most a short "what's working" section. Padding a report erodes trust in every future report.

This governs the *filter* pass. It is not licence to look less hard.

## When a re-review scores worse

The usual cause is that clearing surface noise unmasked deeper issues. Frame it as deeper visibility, not regression.

Check one thing first: adding high-fidelity styling over unfixed structural defects genuinely does make visual judgment score lower, because the new styling exposes overlaps that flat colour concealed. Verify the structure before calling a score drop a regression.

## Reply vs report

The reply carries the verdict, the headline findings and what's open. The report file carries the detail. Don't recap the walkthrough the user just watched.

Lead with the outcome — the first sentence answers "what did you find", not "what are you about to do".

## After the review

Ask which findings to fix, unless the user pre-authorised fixing. Options: all Blocker + High / everything / pick specific.

When fixing: follow existing code patterns, batch related edits, and re-check each fixed finding against its own "should be". Then re-run the gates for what you changed and its neighbours — a targeted regression pass, not a second full review. The classic self-inflicted defect is adding an error message that fails contrast.

**Score the fix against the recapture, not against your account of it.** The rule that governs captures governs repairs too: a fix you cannot see in the new evidence is unresolved, however confident the edit felt. Mark each one **resolved**, **partial** or **unresolved** — partial being the fix that moved the element without producing the quality the finding named. Then name at most three regressions the batch itself introduced, and stop; a repair pass is scoring, not a fresh hunt.

## Convergence across rounds

Three rounds maximum. Each round's findings report should be shorter than the last; a round producing more text than the previous one is churning, not converging.

Ship when the gates pass **and** zero must-fix findings remain open. Both conditions, not either.

If round three still doesn't clear the bar, report the best round with the open items named — "ships with two open polish items: …" — rather than iterating indefinitely or quietly relabelling the bar.

**Rounds are not a substitute for coverage.** Convergence measures whether the findings on the surfaces you reviewed are settling. It says nothing about the surfaces you did not reach, and a review can converge perfectly on three of fourteen screens. Check the worklist before declaring convergence: open cells are a coverage gap, not a round.
