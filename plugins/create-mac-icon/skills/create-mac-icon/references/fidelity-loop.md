# The fidelity loop — closing a hand-authored SVG against a raster reference

The single most consistent finding across this marketplace's icon commissions:
at equal audit scores, the raster take's *material* (volumetric shading,
lighting, contact shadows, translucency) beats the hand-authored SVG's, while
the SVG wins composition, silhouette and 16px survival. The deep-research
panel (three verified reports, committed in the marketplace's
`docs/deep-research/`) confirmed the mechanism: SVG can express everything the
rasters show — models fail because they author flat paths, and naïve
"look at a screenshot and improve it" loops measurably make output *worse*.
This loop is the structured alternative. Its full evidence base:
`docs/svg-icon-fidelity-plan.md` at the marketplace root.

## When to run it

Whenever a raster take (Engine C) wins the material judgment and the Engine A
master must be rebuilt to match it — which the pipeline requires before
shipping (a flat raster master re-creates rubric failure #10). Also usable
against any raster reference the user supplies ("make the icon look like
this").

## The mechanics

`scripts/fidelity.py` is the deterministic core. Per round:

```bash
python3 scripts/fidelity.py structure --candidate icon.svg          # static gate FIRST
python3 scripts/fidelity.py score --candidate icon.svg \
    --reference engineC.png --outdir runs/r03 --label "round 3: material"
python3 scripts/fidelity.py gate --candidate runs/r03/score.json \
    --baseline runs/r02/score.json                                  # Pareto accept/reject
```

- `structure` runs **before** any render: it rejects `<image>` embeds (the
  base64 mimicry exploit), scripts, missing layer groups, and candidates over
  the complexity envelope (defaults 400 paths / 200KB — raise the flags
  deliberately for programmatic builds, never silently).
- `score` renders both sides at 1024/256/128/32/16 on a canvas the harness
  owns (the candidate's viewBox is never trusted), computes luminance-field
  delta + SSIM + edge F1 + mask IoU per size (plus LPIPS when torch+lpips are
  installed — the JSON's `tier` field records which stack ran), and writes
  `residual-1024.png` + edge maps for the critique step.
- `gate` is **Pareto, not a weighted total**: ACCEPT only if no size's
  composite regresses beyond tolerance and the 32/16px edge floors hold. It
  also rejects edits whose render hash didn't change (oscillation guard).

Interpreting the numbers: small-size composites converge early (composition
is the easy half); the 1024 composite is the material gap. On the calibration
fixture (improve-skill A vs its C1 raster) a well-composed but materially
flat master scored 0.83 at 16px and only 0.45 at 1024 — the loop's job is to
raise the 1024 number without letting the small sizes slip.

## Briefing the implement agent (Opus 5)

Each round is one background Opus agent. How the brief is written changes
what comes back, and two failure modes have already cost rounds here: an
agent that ran 7 iterations against a 4-round cap, and briefs that spent
tokens re-checking work the model had already checked. Anthropic's
[Opus 5 prompting guide][opus5] and [prompting best practices][best]
name both mechanisms; these patterns follow them.

[opus5]: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5.md
[best]: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md

- **Structure the brief with XML tags, longform state first, the task
  last.** Context, fixture, baseline numbers and prior learnings up top;
  the ask at the end. Queries placed after long context measurably beat
  the reverse.
- **No verification scaffolding.** Opus 5 verifies its own work; "double
  check", "re-verify before reporting" and "use a subagent to confirm"
  compound with that and burn tokens for nothing. Instrument runs
  (`structure`, `score`, `gate`, `measure.py`) are measurements the round
  is *made of*, not self-checks, and stay.
- **Cap delegation explicitly.** Opus 5 delegates readily; a round is a
  single track. Say "do not delegate to subagents; spawn none."
- **Constrain scope in the brief's own words.** State the edit class, what
  is out of scope this round, and: deliver what was asked at the scope
  intended, make routine judgment calls yourself, and if the brief looks
  mistaken say so in a sentence and carry on rather than widening it.
- **Give the vision work its tools.** Vision performance is strongest when
  the model can crop, zoom and re-render rather than reason about what a
  render probably looks like. Point the brief at the residual and edge
  maps and ask for pixel values sampled out of both images. This is not
  "check your work"; it is where the round's evidence comes from.
- **Name the metric-gaming risk.** A loop that optimises a proxy invites
  tuning constants against the composite. Ask for the material to be made
  physically right, with the score following, and say the score is a proxy
  for a human judgment.
- **Calibrate deliverable length.** Written notes run long by default; ask
  for the substance without padding, and give the final report a rough
  word budget.
- **Calm trigger language.** "Use X when…" outperforms "CRITICAL: you
  MUST…", which overtriggers on current models.

## Running the loop headlessly

`scripts/loop_runner.py` drives rounds with no session attached, and
`scripts/loop_watchdog.sh` keeps it alive. Five failures were needed to get
that working, every one invisible to code review and only findable by
running it. They are recorded here because they are environment traps, not
logic bugs, and the next person will hit the same ones.

- **Give the child a clean context, or it starves before it starts.** A
  round died reporting autocompact thrashing after six tool calls and about
  10k tokens of results. The cause was what it inherited: 13 configured MCP
  servers whose tool definitions consume a large share of the window, plus
  `CLAUDE_CODE_DISABLE_1M_CONTEXT` set to the string `"0"`, which is
  non-empty and therefore truthy, capping the child at the small window.
  Run with `--strict-mcp-config` and strip the session-scoped variables.
  Measured on one identical task: 88s inherited, 14s clean.
- **Hand the agent the brief's path, not its text.** Passing ~7KB of brief
  as the `-p` argument fails in 13 seconds with "Prompt is too long", every
  time, while the same bytes plus a one-line suffix succeed. It is not
  length. Write the brief to disk and tell the agent to read it.
- **Never read the generated master.** A 300KB SVG is about 88k tokens, and
  an agent that re-reads it after each rebuild exhausts the window. The
  brief should name every generated file over ~60KB in the fixture and say
  to judge from PNG renders instead.
- **A harness failure is not a rejected edit.** Counting it as one burns the
  fixture's edit-class rotation and can "converge" a fixture that was never
  worked on.
- **Bound the error handler.** A bug that throws every round will spend a
  100-iteration budget in about one second. Stop after three consecutive
  errors and file the reason.
- **Validate the fixture queue against disk before running.** A fixture
  whose master was hand-authored has no build script, so the
  author-through-the-script rule cannot hold and the round has nothing to
  edit. Check every declared path exists at startup.
- **Watch out for `pkill -f`.** A pattern like `loop_runner.py` also matches
  any monitor whose command string mentions it, so a cleanup can kill its
  own supervision.

## The judged layers — human sheet and blind panel

The metrics are necessary, not sufficient; two judged instruments ride on top:

- **`scripts/review_sheet.py`** — the human's round review. Renders candidate
  and baseline blinded (seeded random order) beside the reference, serves a
  mini web page (default port 8490), and the Submit button **writes
  `review-feedback.json` straight into the round directory** (multi-choice
  first: overall/material/silhouette/small-size winner, next-action, defect
  checkboxes; typing optional). Run it in the background each round and fold
  any feedback file into the next round's brief — never block waiting on it.
- **`scripts/judge_panel.py`** — the blind multi-family panel. Builds an
  anonymised A/B bundle and asks up to three judge families (claude CLI at
  high effort, grok-4.5 via cursor-agent at high effort, gpt-5.6-sol via the
  OpenAI API at medium reasoning — key from an env file, never hardcoded) to
  pick the take closer to the reference per dimension. Per-judge verdicts and
  the unblinded majority tally land in `panel.json`; a failed judge is
  recorded, never silently dropped. Judges see only the renders — never the
  SVG source, the build script, or which take is the candidate.

Use the panel where the stakes justify three model calls (shipping decisions,
loop exit); the metric gate alone carries the cheap inner rounds.

## The round schedule — bounded, one edit class per round

| Round | Edit class | Allowed changes | Exit check |
|-------|-----------|-----------------|------------|
| 1 | Coarse structure | Silhouette, centring, object scale, major colour fields | edge F1 at 1024/256 improves |
| 2 | Material | Gradient stacks, opacity stops, blur radii, highlight/shadow shapes | 1024 composite improves, 32/16 stable |
| 3 | Detail | Micro-geometry, texture accents, local control points | residual shrinks in the edited region, nothing regresses |
| 4 | Small-size repair | Simplify/strengthen what aliases at 32/16 | 32/16 gates pass, 1024 within tolerance |
| +N | Only while the gate keeps accepting | One class per extra round | Hard ceiling: 10 rounds total |

Rules that make it converge (each one earned by a documented failure mode):

- **One edit class per round.** Unconstrained edits oscillate; a rejected
  round rolls back to the accepted state and the next round tries a different
  class or a smaller change.
- **Critique from residuals, not raw screenshots.** Read
  `residual-1024.png` and the edge maps beside the renders; name localised,
  non-overlapping defects (silhouette / proportions / layer order / shadow /
  highlight / material / small-size legibility). Score each 0-2 against the
  reference independently — never side-by-side comparison scoring, never 1-5
  scales (both are documented bias sources).
- **Edit the parameters, not the paths.** Author the master through a build
  script (`build_icon.py` pattern: geometry and material as named constants,
  script emits the SVG) so each round is a named parameter change the log can
  record. Free-form path surgery is how masters rot.
- **The gate informs; the rubric decides shipping.** The gate measures
  similarity to the reference — and the reference can itself fail a rubric
  check (raster engines routinely render frost at ~1.4:1 figure-ground,
  which dissolves at 32px). On a real commission the gate ACCEPTED a round
  that hard-failed rubric #7/#4 and REJECTED its fix. When they disagree,
  treat the gate's verdict as information, the 12-point rubric as authority,
  and bound the next edit to regions the rubric doesn't police (see the
  bounded-frost-fade recipe).
- **Similarity is not legibility, and the panel sees the difference first.**
  On improve-skill r01 the composite rose at 32 and 16px while two
  independent blind judges (Claude and gpt-5.6-sol, in separate harnesses)
  both said the block collapsed toward mid-grey and the accent weakened.
  The mechanism: small-size scoring rewards matching the reference's edges,
  and the reference's own contrast is weaker than the master's (measured
  0.449 against 0.556 at 32px), so converging on it trades legibility for
  similarity. `score` now reports `self_contrast`, an absolute
  reference-free p90-p10 luminance spread, and `gate` rejects a candidate
  whose 32/16px self-contrast falls more than `--contrast-drop` (default 6%)
  below the baseline's.
  **Its honest limit:** on r01 that floor did *not* fire (drops of 2.7% and
  1.6%), because a whole-image spread is dominated by the tile ground rather
  than by the object the judges were describing. It catches gross collapse,
  not localised object-level flattening. The threshold was left at its
  principled value rather than tuned until it fired on one case, which would
  be exactly the metric-gaming this loop warns implement agents against. For
  object-level flattening the blind panel remains the authority, which is why
  an accepted round whose panel disagrees ships as PROVISIONAL into the
  review queue rather than being settled by the machine.
- **Two consecutive rejections = stop or branch.** Grinding one scaffold past
  two rejects buys nothing (documented plateau behaviour); branch to a fresh
  scaffold or ship the accepted state with the gap stated.
- **Keep round state on disk** (`runs/rNN/` with score.json per round). Each
  round's editor works from the accepted SVG + the latest residuals + the
  open defect list — not the accumulated conversation (context bloat degrades
  editing quality by round 8-10).

## After the loop — feed the skill

A win is not finished until it is generalised:

1. **Record the recipe.** Whatever material construction closed the gap
   (gradient stack, blur discipline, contact-shadow recipe) gets added to
   `references/material-recipes.md` with the fixture it came from — same
   session, while the diff is fresh.
2. **Keep the trajectory.** The `runs/` directory (candidates, scores,
   accept/reject, critiques) is training data for a future vector model —
   the marketplace plan's Phase 4. Don't delete it; leave it in the
   commission's working directory.
3. **A recurring recipe becomes a build-script default.** If three
   commissions all hand-write the same soft-shadow construction, it belongs
   in the scaffold every Engine A master starts from.
