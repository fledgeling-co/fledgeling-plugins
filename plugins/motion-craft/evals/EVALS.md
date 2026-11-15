# motion-craft evaluation

Two briefs, each run with the skill and with no skill, judged blind by four model families from one-frame-per-second contact sheets. The first round went against the skill on both briefs. After rules were added in response, the second round won the data clip 4-0 and tied the launch film 2-2. On the launch film the plain film still made the stronger case for the product.

This is a two-brief evaluation with one run per arm. It shows the direction of the effect on these two briefs, not its size or how often it holds.

## The two briefs

A decision panel chose both briefs before anything was generated (`docs/decisions/2026-11-15-motion-craft-proof.html` at the repo root): one representative and one adversarial.

1. **Launch film.** "Make a 20-second 16:9 launch video for the design-craft plugin… I won't be around to answer questions, so make the calls yourself and give me the MP4." Real material: the plugin's README, icon, banner and skill.
2. **CSV to vertical clip.** "turn this into a 15 second vertical clip for instagram <path>". No context, and a 12-row CSV of a fictional coffee roaster's 2025 online orders (7,145 orders, a November peak of 1,187, January to December up 119%, average order $38.20 to $42.80, repeat customers 31% to 42%).

## Results

### Blind panel: which film would you rather send?

Each judge picked A or B on four questions: **specific** (made for this subject, not a template), **craft** (type, hierarchy, contrast, framing, readability), **story** (frames a stranger can follow, with a payoff) and **overall**. The figures are votes for the skill's film against the no-skill film, out of four.

| Brief | Round | Specific | Craft | Story | Overall |
|---|---|---|---|---|---|
| Launch film | 1 | 0-4 | 4-0 | 0-4 | **0-4** |
| Launch film | 2 | 0-4 | 3-1 | 0-4 | **2-2** |
| CSV clip | 1 | 3-1 | 1-3 | 3-1 | **1-3** |
| CSV clip | 2 | 4-0 | 2-2 | 4-0 | **4-0** |

Round 2 compares the revised skill's new films against the round-1 no-skill films, which were not re-run. Both rounds used the same prompts and judges; each round seeded its own A/B order.

### Structural checks

Assertions are listed in `evals.json`. Script checks come from `grade_eval.py`, and judged checks were graded by reading the outputs.

| Brief | Arm | Script checks | Judged checks | What failed |
|---|---|---|---|---|
| Launch film | no skill (round 1) | 4/6 | 2/2 | no audio stream; frame 0 a near-flat field (luma range 17) |
| Launch film | skill, round 1 | 6/6 | 2/2 | none |
| Launch film | skill, round 2 | 6/6 | 2/2 | none |
| CSV clip | no skill (round 1) | 2/4 | 2/3 | frame 0 near-flat (24); almost no change in the first 3 s (0.95); the November callout in the bottom 20% |
| CSV clip | skill, round 1 | 4/4 | 3/3 | none |
| CSV clip | skill, round 2 | 4/4 | 3/3 | none |

The CSV counts exclude a fifth script check that was dropped after round 1 (see the assertions note below).

### Cost and time

| Run | Tokens | Time |
|---|---|---|
| Launch film, no skill | 184,679 | 19.4 min |
| Launch film, skill round 1 | 319,920 | 35.5 min |
| Launch film, skill round 2 | 352,724 | 39.2 min |
| CSV clip, no skill | 183,623 | 14.8 min |
| CSV clip, skill round 1 | 323,662 | 36.4 min |
| CSV clip, skill round 2 | 350,240 | 36.9 min |

With the skill, a film costs roughly 1.9 times the tokens and 2-2.5 times the wall-clock time. The extra time goes on the planning files, sound and the review pass. The judge panel runs on the owner's subscriptions and cost no metered money.

## What changed between the rounds

Round 1's judges agreed on why the skill lost. The launch film had the design-craft icon acting out an idea and never showed what the product does or the evidence that it works. The data clip left the lower 40% of the frame as an unchanging colour block and dropped two of the data's four headline figures. The skill's films were better made and said less.

Added the same day:

- a numbered list of 3-5 must-carry facts in `BRIEF.md`, mapped to shots in `SPEC.md`, with a missing fact as a P0;
- the proof beats show the product doing its job, never a metaphor for it;
- the whole canvas works: no region over about a quarter of the frame stays empty for the whole film;
- two review questions: "is every must-carry fact on screen, legible and held?" and "would a plain version of this brief say more?"

In round 2 both films carried their facts. The launch film showed design-craft's real lint output and its 23-against-9 gate result. The data clip put all five figures on screen, each checked against the CSV.

## What round 2 still found

On the launch film all four judges preferred the plain film on specificity and story. That film opens on twelve identical dark cards, the generic output design-craft exists to fight. The skill's film opens on its icon with the caption "The rut.", which names the problem instead of showing it. The judges also flagged two craft defects in the skill's films: the "23" smeared behind the lint card at a 14 s transition, and chart labels cropped to "RS" at the frame edge during a pan in the data clip.

Added after round 2 and **not yet tested by a third round**:

- `story-and-rhythm.md`: the problem is shown, not named;
- `craft.md` tells: edge labels cropped mid-pan (check the range of every pan, not only its ends), and transition frames where the incoming element collides with content still on screen.

## Caveats

- **One run per arm, two briefs.** Every result above can move with sampling noise. A 2-2 tie is a tie, not a lean.
- **The baseline was not re-run for round 2.** The skill's films were regenerated, the no-skill films were not, so round 2 measures the revised skill against one draw of the baseline.
- **Judges see frames only.** Contact sheets cannot show easing, smoothness, timing or sound. The skill's sound was measured (loudness, onsets against cues) and never heard by anyone. Judges were told not to guess at motion.
- **One judge shares a family with the runs.** The films were made by Claude, and the panel includes a Claude Opus judge. Leaving its vote out would turn the round-2 launch-film tie into 1-2 for the no-skill film, and would change no other overall result.
- **Grading.** Round 1's judged assertions were graded by an independent agent. Round 2's were graded by the session that wrote the skill, against the CSV row by row, file birth times and the plugin's README line numbers. Its evidence strings are in the results files.
- **Most structural assertions don't discriminate.** Every skill run passed all of them, and the no-skill runs passed most. They catch silent films, empty first frames and dead openings, which is real but coarse. The difference in quality showed up only in the blind panel.

## Assertions note

One script check was dropped after round 1: "no number in the composition source contradicts the CSV". It fired on both arms for layout coordinates (`YBASE = 1150`, `y: 1194`), not on-screen claims, so it measured the code rather than the film. Figure accuracy is now a judged assertion. The reason is recorded in `evals.json` under `dropped_assertions`.

## Judges and records

| Lane | Model | Harness |
|---|---|---|
| Anthropic | claude-opus (alias), effort high | `claude -p --add-dir <blind>` |
| Google | gemini-4-hydrogen-high | `agy --new-project` |
| xAI | grok-4.7, effort high | `grok -p` |
| OpenAI | gpt-6-astra, reasoning high | `codex exec --skip-git-repo-check -s read-only`, images by `-i` |

Records are in `results/iteration-1/` and `results/iteration-2/`: the blind contact sheets, each judge's prompt and answer, `unblinding.json` (which letter was which arm), `panel-unblinded.json` (votes by arm), and each run's `grading-script.json`, `grading-judged.json` and `timing.json`. The films and projects themselves stay in the session workspace and are not committed.
