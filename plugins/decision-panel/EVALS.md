# Evals

What was run, what it showed, and what hasn't been measured yet.

## No blind comparison was run

Luke chose one live run over the full eval loop when the skill was built on 7 November 2026. So there's no with-skill against no-skill benchmark here and no blind judge panel, and nothing below should be read as one. Three prompts are written down in `evals/evals.json` for when that run happens.

## What was checked mechanically

| Check | How | Result |
|---|---|---|
| The page builder refuses bad decisions | `build_decision.py --check` on the bundled example, then on five broken copies of it | example passes; all five fail with the right message: a failed lane counted as a vote, dissent on a page marked unanimous, a winner no model chose, a missing question, a single option |
| The tally applies one rule | `tally.py` on four fixture rounds | unanimous → decided (exit 0); 3 to 1 → decided with dissent (0); 2 to 2 → round two (3); one valid lane → too few lanes (1) |
| Lanes resolve the newest model | `latest_model.py` against the live CLIs, and once with the CLIs off `PATH` | grok → grok-4.7, gemini at high → gemini-4-argon-high; with no CLI it falls back to its pin and says so |
| The skill reads like the house | `agent_voice_lint.py --format skill` on SKILL.md | clean on the hard checks |

## The live run

**The decision:** which stack Luke's A$990 app health check should support first. It was a real open item in another project, raised by all four models in a separate review of that plan. The options were Next.js on Vercel with Supabase (A), Vite React on Supabase (B), any React front end on Supabase or Firebase (C), and no first stack (D).

**Round one.** Fable, Gemini Argon and Grok chose B, and GPT-6 Astra chose A. Astra alone cited current vendor documentation: Lovable's new apps use TanStack Start rather than Vite, and Bolt defaults to its own database rather than Supabase. That undercut B's premise. Fetched on 7 November 2026, the Lovable FAQ and Bolt's Supabase page both confirmed it.

**Round two,** with those quotes in front of all four. Every model left B. Astra and Argon chose A, Fable chose C, and Grok proposed a new option: any React front end on Supabase, any host. That's 2 to 2. The tie was broken towards A on the plan's own constraints: two benchmark seeds of identical composition, a recalibration for every new stack, and about five owner hours per check. v0's documentation, fetched to check Astra's last claim, confirmed that v0 defaults to Next.js.

**The page** is in Business-Automation at `docs/decisions/2026-11-08-first-stack.html`, with every brief and answer beside it. Nothing in that plan was changed; each next step waits for Luke.

## What the live run changed in the skill

- **A tally bug.** Grok printed a sentence of preamble with no newline before `VERDICT: B`, and the first `tally.py` only looked for the verdict at the start of a line, so it counted a valid answer as a failed lane. It now takes the first `VERDICT:` wherever it sits, and the four fixture rounds still behave.
- **A new rule.** When one model cites an outside source the others haven't read, fetch it and quote the exact sentences in the round-two brief. In this run, that one step is what moved the panel.

## What is still unmeasured

- Whether four families beat the best single model on decisions like these. The research corpus (`docs/deep-research/`) measured judges on question answering and preference tasks, not on open-ended business or architecture calls, and found the best single judge matched or beat panels there.
- Whether the tie-break, made by the orchestrating model, is biased towards its own family. In the live run the orchestrator shared a family with Fable and ruled against Fable's option, which is one data point, not a measurement.

The run that would settle the first: the three prompts in `evals/evals.json`, each answered by the full panel, by the best single lane alone, and by no skill, then judged blind by a family that took no part.
