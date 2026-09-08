# Evidence

Two kinds of claim in this skill, kept apart on purpose.

**Field findings** come from the research panel in
`docs/deep-research/panel-local-claude-agent-review-pipelines.md` (10 cited sources, run
2026-09-08, free lane, $0.00). **Atlas measurements** were taken in one monorepo by one team
and are labelled as such; they are evidence about this repo, not about software generally.

## Field findings

| Claim | Figure | Where it is used |
|---|---|---|
| LLM-written tests that compile but are vacuous | 75% filtered by Meta's TestGen-LLM | The mutation rule in SKILL.md |
| Generated tests carrying structural smells | 30-54% | Same |
| Static reading at catching swallowing mocks and empty-collection guards | rated Low | Why reading is not the oracle |
| Raw LLM review false positives | 40-70% | Verify before acting |
| Error reduction from cross-model verification | up to 50% | The out-of-family step |
| Clean textual merges carrying a semantic conflict | 20-35% | Gate the merged tree |
| Exit-code masking in subshell pipelines | named failure mode | Never pipe a gate |
| Turborepo and pnpm cache replay | named failure mode | Always `--force` |

The panel also names an approach this skill does not take: speculative merge trains, which
integrate candidate merges before landing them. Worth revisiting if the PR volume ever
justifies the machinery.

## Atlas measurements

Each was taken during a single long session and is reproducible in the repo.

| Measurement | Value |
|---|---|
| Checks found that could not fail | 21, none found by running the tests |
| Of those, found by deliberately breaking code | all |
| Verdicts overturned by re-measuring through a repaired rig | 5 of 37 |
| Conflicts where both sides were true | 5 of 5 |
| Commands that destroyed work | `git checkout --`, `git add -A` in a conflict, `pkill -f` |
| Coverage runners whose failure made covered files read as untested | 3 in one pass, 16 files |
| Questions put to the owner that the repo already answered | 1, and it was documented twice |

## What is not evidenced

- That rebase is better than a merge commit here. It is the owner's stated preference and is
  followed as an instruction, not as a finding.
- That the nine-stage order is optimal. It is the order the owner asks for, and stages 6 to 8
  exist because they were repeatedly needed, not because a study says so.
- Any claim about how this performs against not using it. See `evals/EVALS.md`, which says
  plainly whether a comparison was run.
