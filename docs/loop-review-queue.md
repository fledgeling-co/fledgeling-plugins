# Loop review queue

Rounds the runner could not settle on its own. Each needs a human look.

## improve-skill r01 (material): RESOLVED by human review

The Pareto gate ACCEPTed at +0.1427 net, the largest gain of any round on this
fixture, and the round fixed two real defects: shadows that read blue in a scene
with no cool light, and the icon's brightest ground sitting furthest from its own
key light. It committed as PROVISIONAL because the blind panel did not agree.

- Gate: ACCEPT. 1024 0.3623 to 0.3950, 16px 0.7595 to 0.7748, nothing regressed.
- Panel: no majority on overall, material and silhouette (1-1, one judge failed);
  baseline won small sizes 2-0. Both judges independently described the block
  collapsing toward mid-grey with a weaker accent at 32 and 16px.
- Polarity +0.146 (was +0.177), sign intact. Rubric holds at 11/12.
- The new self-contrast floor does not fire here (2.7% and 1.6% drops against a
  6% threshold); see fidelity-loop.md for why it was not tuned to force it.

**Human verdict (2026-08-07):** tie on overall, silhouette and small sizes; no
defects ticked; action "Keep iterating". The round STANDS, so its PROVISIONAL
status is cleared and nothing is reverted.

Two specific mismatches were named, and they are now the queue for the next
rounds because neither is a metric the harness measures:

1. The wood/paper shaving curl is completely wrong against the reference.
2. The lighting and texture of the left side are completely different from
   the reference.

Both are fed into every subsequent brief for this fixture automatically.

## improve-skill r02: implement agent failed to run (RESOLVED, 4 duplicate entries collapsed)

Filed four times across restarts. Root cause found and fixed in commit acf908b: the child
agent inherited 13 MCP servers' tool definitions plus a truthy CLAUDE_CODE_DISABLE_1M_CONTEXT,
so it started near its context limit and autocompact thrashed after six tool calls.
--strict-mcp-config plus a stripped environment fixed it; measured 88s to 14s on the same task.
No action needed.

## improve-skill r04: gate and panel disagree

The Pareto gate ACCEPTed (1024 composite +0.0166) but the blind panel preferred the previous take. The runner committed it as PROVISIONAL and did not settle the rubric question.

Review sheet: `/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/loop-runs/r04/review.html`
Panel: `/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/loop-runs/r04/panel/panel.json`
Revert with: `git revert` the round's commit, or keep it and note why.

## improve-skill r06: gate and panel disagree

The Pareto gate ACCEPTed (1024 composite +0.0090) but the blind panel preferred the previous take. The runner committed it as PROVISIONAL and did not settle the rubric question.

Review sheet: `/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/loop-runs/r06/review.html`
Panel: `/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/loop-runs/r06/panel/panel.json`
Revert with: `git revert` the round's commit, or keep it and note why.

## improve-skill r11: gate and panel disagree

The Pareto gate ACCEPTed (1024 composite +0.0328) but the blind panel preferred the previous take. The runner committed it as PROVISIONAL and did not settle the rubric question.

Review sheet: `/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/loop-runs/r11/review.html`
Panel: `/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/loop-runs/r11/panel/panel.json`
Revert with: `git revert` the round's commit, or keep it and note why.

## improve-skill r12: gate and panel disagree

The Pareto gate ACCEPTed (1024 composite +0.0015) but the blind panel preferred the previous take. The runner committed it as PROVISIONAL and did not settle the rubric question.

Review sheet: `/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/loop-runs/r12/review.html`
Panel: `/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/loop-runs/r12/panel/panel.json`
Revert with: `git revert` the round's commit, or keep it and note why.

## improve-skill r13: gate and panel disagree

The Pareto gate ACCEPTed (1024 composite +0.0131) but the blind panel preferred the previous take. The runner committed it as PROVISIONAL and did not settle the rubric question.

Review sheet: `/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/loop-runs/r13/review.html`
Panel: `/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/loop-runs/r13/panel/panel.json`
Revert with: `git revert` the round's commit, or keep it and note why.

## improve-skill r14: gate and panel disagree

The Pareto gate ACCEPTed (1024 composite +0.0002) but the blind panel preferred the previous take. The runner committed it as PROVISIONAL and did not settle the rubric question.

Review sheet: `/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/loop-runs/r14/review.html`
Panel: `/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/loop-runs/r14/panel/panel.json`
Revert with: `git revert` the round's commit, or keep it and note why.

## improve-skill r16: gate and panel disagree

The Pareto gate ACCEPTed (1024 composite +0.0063) but the blind panel preferred the previous take. The runner committed it as PROVISIONAL and did not settle the rubric question.

Review sheet: `/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/loop-runs/r16/review.html`
Panel: `/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/loop-runs/r16/panel/panel.json`
Revert with: `git revert` the round's commit, or keep it and note why.

## improve-skill r18: gate and panel disagree

The Pareto gate ACCEPTed (1024 composite +0.0014) but the blind panel preferred the previous take. The runner committed it as PROVISIONAL and did not settle the rubric question.

Review sheet: `/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/loop-runs/r18/review.html`
Panel: `/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/loop-runs/r18/panel/panel.json`
Revert with: `git revert` the round's commit, or keep it and note why.

## improve-skill r13: gate and panel disagree

The Pareto gate ACCEPTed (1024 composite -0.0047) but the blind panel preferred the previous take. The runner committed it as PROVISIONAL and did not settle the rubric question.

Review sheet: `/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/loop-runs/r13/review.html`
Panel: `/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/loop-runs/r13/panel/panel.json`
Revert with: `git revert` the round's commit, or keep it and note why.
