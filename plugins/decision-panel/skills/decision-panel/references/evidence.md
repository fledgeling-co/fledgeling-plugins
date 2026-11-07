# Evidence behind the procedure

Each rule in SKILL.md traces to a line here. The research corpus is reused rather than bought
again: a Dossier report on LLM juries, correlated errors and judge bias, run on 7 November 2026
for the Business-Automation project and read in full there. It is exported to
`docs/deep-research/panel-evidence-dr_90bf904baa94a544.md` with its source registry, so every
citation below can be checked from inside this plugin. Line numbers refer to that file.

| Rule | Evidence | Source |
|---|---|---|
| Evidence beats votes; a majority cannot make a claim true | Heterogeneous panels do not make independent errors: a nine-judge, seven-family panel carried about two effective votes, and the best single judge matched or beat the panel in every tested condition | Kohli et al., "Nine Judges, Two Effective Votes", Apple ML Research 2026, report lines 58, 92; [paper](https://machinelearning.apple.com/research/correlated-llm-evaluation-panels) |
| Different families still share mistakes, so read dissent closely | Models that both err choose the same wrong answer about 60% of the time, and agreement rises with capability | Kim et al., "Correlated Errors in Large Language Models", ICML 2025, report line 64; [paper](https://proceedings.mlr.press/v267/kim25e.html); "Great Models Think Alike", report line 96 |
| A diverse panel still earns its place on judgment calls | A panel of smaller models from three families tracked human judgment better than one large judge, at lower cost | Verga et al., PoLL, 2024, report line 44; [paper](https://arxiv.org/abs/2404.18796) |
| Round two only on the split, and a change must cite new evidence | Debate rounds can move models from right answers to wrong ones under peer reasoning; second rounds should be reserved for new evidence | Wynn, Satija and Hadfield, 2025, [paper](https://arxiv.org/abs/2509.05396); report lines 124-136 |
| Quote round-two positions as Reviewer A-D, not by model | Judges show self-preference (about 10% higher win rate for their own outputs) and affinity bias | Zheng et al., MT-Bench, report line 148 |
| Swap option order between lanes | Position bias is measurable in pairwise and multi-choice judging; presenting options in both orders cancels much of it | Zheng et al., report line 154; rubric study, report line 146 |
| A fixed answer shape with a VERDICT line | Structured outputs and clear rubrics reduce judge variance and make aggregation mechanical | Report lines 40, 156 |
| A failed or off-topic lane is not a vote | Measured on this machine: an agy lane run from inside a repo answered another project's question with a confident verdict; an empty answer file can come back with exit code 0 | `clarify` plugin `references/evidence.md` and `feedback-panel` `scripts/run_panel.sh` header |
| Fetch and quote an outside source a lane cites before round two | First live run, 7 Nov 2026: GPT-6 Astra alone cited Lovable and Bolt documentation that undercut the majority's premise; fetched, the vendor pages confirmed it, and the quotes went to all four lanes in round two | `EVALS.md`, live run |
| Find the VERDICT line anywhere, not only at a line start | First live run: grok printed a sentence of preamble with no newline before `VERDICT: B`, and a line-anchored parser counted a valid answer as a failed lane | `EVALS.md`, live run; `scripts/tally.py` |
| Lanes run the newest model, resolved at run time | Luke's instruction of 7 November 2026: use the latest available version of each model so the skills need fewer updates | Conversation, 7 November 2026; `scripts/latest_model.py` |
| Grok runs at `xhigh` | `grok --effort max` is refused: "use one of: xhigh, high, medium, low" (measured 7 November 2026) | `clarify` `references/evidence.md`, 7 Nov 2026 rows |
| Destructive, irreversible, outward-facing or costly actions still wait for the owner | The owner's standing instruction in `~/.claude/CLAUDE.md`: certainty is not a ticket past an unrecoverable action | Owner's global instructions |

## What the evidence does not settle

The corpus measures judges on question answering, preference and leaderboard tasks, not on
open-ended business or architecture decisions. Whether four families beat the best single lane
on decisions like the ones this skill handles is unmeasured; `EVALS.md` names the run that would
settle it.
