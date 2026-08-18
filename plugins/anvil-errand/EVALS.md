# Evals

**Nothing in this file is a measured result about the skill.** The eval suite exists now, in [`evals/evals.json`](evals/evals.json), and it has not been run. No prompt has been executed with the skill loaded, no prompt has been executed without it, no judge has looked at anything, and no pass rate exists. That is a legitimate state to ship in, and it is written here plainly so nobody reads a defined suite as an evaluated one.

What follows is in three parts: what was checked mechanically and what those checks found, what the eval set would settle, and what none of it can tell you.

## What was checked, and what it found

These are the things a script or a shell can establish without running the skill. Each was run on 18 Aug 2026 and the result is what is written.

**The SKILL.md parses.** Its frontmatter reads as strict YAML, carries exactly `name` and `description`, and the name matches the plugin directory.

**The refusal contract is live.** `anvil errand --check` was run on this Mac. It exited **3** and printed a refusal in exactly the documented shape:

```
denied [node_unreachable]: the node this Mac is configured with (node 'node-LUKESFF' over
ssh://luke@192.168.3.91) did not answer ... Nothing was started.
```

So the central claim, that a refused errand exits non-zero and names its cause by a stable identifier, holds for at least one of the six kinds. `anvil errand --help` produced the same refusal and the same exit code, which incidentally confirms two more of the skill's claims at once: everything after the verb is the agent's own argv rather than a flag the verb reads, and a failed precondition starts nothing.

**The runbook the skill points at is not where the skill says it is.** This is the one real failure. `docs/ERRAND_RUNBOOK.md` is named twice in the SKILL.md as the source of record, and the binary's own refusal message cites it too. It does not exist in the anvil repository's main working tree: `~/Dev/anvil/docs/` holds no runbook under that name or any other. Copies exist only inside `~/Dev/anvil/.worktrees/ANV-*/docs/`, on unmerged branches. A reader who follows the pointer finds nothing.

The runbook's *content* does check out where it exists. Against the newest copy on disk (ANV-0373), all five numbered pointers in the refusal table land on the matching step:

| the skill says | the runbook's step |
|---|---|
| `image_absent`, step 1 | 1. Build the agent image on the node |
| `errand_proxy_unreachable`, step 2 | 2. Start the upstream that holds the credential |
| `errand_no_node`, step 3 | 3. Pair the node |
| `node_unreachable`, step 4 | 4. Start the daemon |
| `errand_ticket_unavailable`, step 5a | 5a. Have the daemon mint one |

**Three of the six refusal identifiers are not in the main checkout either.** Searching the anvil repository outside `.git`, `target/`, `node_modules/` and the worktrees, `node_unreachable`, `image_absent`, `image_unverified`, `egress_unenforceable`, `engine_refused` and `outside_window` all appear. `errand_no_node`, `errand_ticket_unavailable` and `errand_proxy_unreachable` appear in **zero** files there, and in 108, 642 and 108 files inside the worktrees. The installed `anvil` binary clearly has the newer behaviour, since it produced the documented refusal shape above. So the skill is written against a version of anvil that the repository has not merged to main, and half its refusal table cannot be checked against the source of record where a reader would look for it.

Neither of those two failures is the skill's own error, and neither is fixable from inside this plugin. They are recorded here because a reader deserves to know that following the skill's one external pointer currently leads nowhere.

**No prior run exists.** There is no `grading.json`, no `results/` directory, no `benchmark.json`, no committed judge log and no blind-panel key anywhere under `plugins/anvil-errand/`. This was checked rather than assumed.

## What the eval set would settle

Eight prompts, in `evals/evals.json`. Each runs twice, once with the skill and once with no skill at all, because there is no predecessor here and the honest question is whether the skill earns the context window it costs.

Three of them are where the answer would actually come from:

1. **`silence-is-not-a-hang`.** The user says the errand has printed nothing for two and a half minutes and asks whether to kill it. The right answer is that Claude Code's default text mode prints nothing until it terminates, so this is silence rather than a hang. A model with no skill has no way to know that, and the comfortable answer (stop it and retry) is the wrong one. Run it against both arms and grade one property: did anything get stopped.

2. **`image-unverified-is-not-image-absent`.** The user has read one refusal kind as the other and is about to spend twenty minutes rebuilding an image that may already exist. The two kinds are deliberately separate for exactly this reason. Grade whether the reply distinguishes them and whether it endorses the rebuild.

3. **`provisioning-goes-to-the-runbook`.** The user asks for the full setup recipe in one list. Being helpful here is the failure: a second copy of a recipe drifts, and the stale copy is the one people cite. Grade whether a recipe was written. This eval is the one worth running first, because a baseline will almost certainly write the list, and because the mechanical check above shows the runbook it should point at is currently missing from main, which makes the refusal harder rather than easier.

Grade with a subagent that never sees the skill, marking each assertion passed or failed with quoted evidence. No 1-to-10 scores: every assertion in the set is a property somebody can check by reading the reply or by looking at what ran.

## Caveats, stated rather than buried

- **Nothing here measures the skill.** Every finding above is about the SKILL.md, the anvil repository, or the installed binary. None of it is about what a model does after reading the skill.
- **One machine, one moment.** The `--check` run and the missing-runbook finding are both facts about this Mac and this checkout on 18 Aug 2026. The node was asleep, which is why `node_unreachable` was the kind that fired. The other five kinds are unexercised.
- **A defined eval set proves nothing on its own.** Written assertions are a plan for a measurement, not the measurement.
- **The set may contain assertions that cannot fail.** One is labelled as a control in the JSON, on the expectation that a capable model passes it without the skill. Whether the others discriminate is unknown until both arms have run, and any that a baseline also passes measure the model rather than the skill and should be relabelled or dropped.
