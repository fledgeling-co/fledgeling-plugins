# Evals

**Almost nothing in this file is a measured result about the skill,** and the one exception is a failure rather than a success. The eval suite exists now, in [`evals/evals.json`](evals/evals.json) — ten prompts — and it has not been run. No prompt has been executed with the skill loaded, none without it, no judge has looked at any output, and there is no pass rate. Saying so is the point: an unevaluated skill whose EVALS.md omits the subject reads to every later reader as though the pipeline ran.

This skill's own first rule is that a conclusion reached by looking is not a measurement, and it applies here first.

## Which numbers in this project are about this skill

None of them. The README and the references carry a lot of figures, all of them real and all of them about something else. Because this is a skill about denominators, the provenance is worth putting on the record in one table.

**Borrowed external research.** Published work about UI testing in general. It motivates the design and measures nothing here.

| figure | claim | source |
|---|---|---|
| 27% valuable, 50.5% duplicates, 22.5% invalid | LLM-generated QA plans against an application owner's own QA team | Mozilla Foundation / Mujahid et al., Jan 2026 |
| 49% over 71 bugs | a model's detection ceiling as a non-crash functional oracle | Ju et al., Jul 2024 |
| 42.5% to 47.6% across 214 components | behavioural relations exercised far more than validated | Pei, Zhang, Sohn, Papadakis, Aug 2026 preprint, no independent replication |
| DISTS +34.5%, LPIPS +36.8%, VIF +98.0%, HaarPSI +22.6% with human opinion flat or falling | perceptual metrics are gameable by imperceptible perturbation, which is why a similarity score is a tripwire here and never a verdict | metric-robustness work, via the Aug 2026 research panel |
| 1024×768 | the default screen resolution of a hosted `windows-latest` CI runner | `actions/runner-images` issue 2935 |
| "neither GetLastError nor the return value will indicate the failure was caused by UIPI blocking" | Windows silently discards synthetic input aimed at a higher-integrity process | Microsoft's own `SendInput` reference, fetched and read |

That third one is the weakest and the README says so already. It is directional, not a threshold. The last two are capability facts rather than measurements of anything; they say what a platform does, not how often a check catches a defect.

**Field observations from the campaign that motivated the skill.** Real, local, and measured *before* this skill existed, using the predecessor method. They are facts about those applications and about `acceptance-e2e`-era work, not about this skill's behaviour. The trace is in `skills/test-campaign/references/evidence.md` and `docs/meta-pass-gap-analysis.md`.

- 524 assertions across 13 tenants, all opening `/` at 1280px or wider against the reference build.
- Six screens on one console, five of which received none of the sweeps.
- **100% checked, 22 armed cases and 59 passing tests reported for a macOS app and a Windows app, neither of which had ever attached a GUI process to a window server.** Swift view structs initialised in memory, C# never compiled, and the evidence page's screenshots taken from an HTML mock in a browser. This is the observation the 0.5.0 work exists for, and every number in that report was individually true.
- Four live instances of the `errorPolicy: 'all'` confident-falsehood defect across three screens.
- Six working presets reported dead by a length-neutral dead-control sweep.
- **20 published surface captures showing three unrelated documents, with every gate in the skill passing.** Measured 20 Aug 2026 on a campaign built with test-campaign 0.7.0: `campaign.py check` cleared, `strict-check.py` reported 46 of 49 checked, both `-glass` lanes were proved and witnessed, and the images were of a project status report, the mock browser's own index page and a design accessibility doc. Twenty files held **six distinct images**, four groups of four byte-identical. This one is different in kind from the others above: it is a fact about a campaign *this skill produced*, not about the predecessor method, so it is the first observation here that measures a failure of the skill rather than a failure the skill was built to catch. It is what 0.8.0 exists for, and eval 10 is its reproduction.

- **230 cases, 220 of them armed, over a product with no network client — and a network policy recorded as observed.** Measured 20 Aug 2026 on a campaign built with test-campaign 0.8.0. `campaign.py check` cleared, `strict-check.py` reported a high checked fraction, and REQ-001 read "runner communication is outbound pull only over HTTPS/WSS on TCP 443". The dependency tree contains no HTTP client, no line of production code spawns a subprocess, `pfctl` and `nft` are never executed, and the daemon only binds loopback. The guarantee was true because nothing crosses the boundary it describes. Like the row above, this is a fact about a campaign *this skill produced*: the second observation here measuring a failure of the skill rather than one it was built to catch, and the more uncomfortable of the two, because the instrument that should have caught it — arming — was run 220 times and cannot see this class by construction. It is what 0.9.0 exists for, and eval 11 is its reproduction.

That last one is worth reading against the first entry in this table. The skill's whole design premise is that prose does not defend against a comfortable report, and here the prose defending the picture-to-surface binding was a filename-matching heuristic with a docstring saying a wrongly filed screenshot "is worse than one filed against none, because it looks right". The docstring was correct and the code only guarded the ambiguous case. A rule stated and not gated is a rule the next run does not have.
- A driving sweep writing to a live tenant record four times in one morning.
- One judging pass costing 178 calls, 1.69M input tokens, 65.6k output and roughly US$6, returning 11 pass, 13 fail and 36 inconclusive. That is in `assets/judge-contract.md` under Cost, stated.

**Measurements of this skill.** There are none. What they would be: the per-assertion results of the nine prompts in `evals/evals.json` across two arms, graded by an independent subagent. That is the gap this file exists to name rather than to fill.

The 0.6.0 gates are each proved to fire and then proved to clear, and that proof is a file rather than a paragraph: [`tests/run.sh`](tests/run.sh), 21 assertions, re-runnable. It builds a campaign designed to trip every new blocker (a non-image artifact, a zero-byte file, a 1×1 placeholder, two cases sharing one screenshot byte for byte, a pixel claim with no stated capture channel, a lane claiming on-glass with no proof, a case on the legacy `visual` rung, the inconclusive and blocked statuses, `interactive-glass` on a non-glass lane, and `--cannot-attach` used as a missing-build skip), asserts each one fires *with its own distinguishing message* rather than merely exiting non-zero, then resolves the same campaign and asserts it clears. The ratchet's three paths are covered too. A structural leftover (`no Windows host with an interactive desktop is reachable`) is recorded; `"no signed app is on disk"` and `"glass stays closed"` are refused.

The suite is itself armed, which is the only reason to believe it. Disabling the duplicate-artifact blocker in `campaign.py` turns it red; restoring the line turns it green. It also went red once on its own account, when a fixture edit stopped exercising the missing-capture-channel blocker and the suite noticed before I did. That is a test of the gate, not a measurement of the skill, and it belongs in this paragraph rather than in the table above.

Two further figures were withdrawn during the research pass when their only source turned out not to exist, and they appear nowhere in the skill. `references/evidence.md` records both.

## What was checked, and what it found

The scripts are testable without an agent. Everything below was run on 18 Aug 2026 against throwaway campaign directories under `/tmp`.

**The SKILL.md parses.** Frontmatter reads as strict YAML, carries exactly `name` and `description`, and the name matches the plugin directory.

**Everything it points at exists.** Twelve internal paths are cited in the SKILL.md across `references/`, `scripts/` and `assets/`, and all twelve resolve, including the three templates it tells you to copy into the project. Both scripts compile.

**The gate fires on a bad fixture, and it names the reason.** This is the central mechanical claim, so it was worked through case by case.

| the fixture | exit | what `campaign.py check` said |
|---|---|---|
| a critical flow whose only case is at the presence rung | 1 | `1 critical flow(s) proved only by presence-level cases`, naming FLOW-001 and instructing that a case at outcome, metamorphic or visual be added or the flag dropped with a reason |
| a case left open | 1 | `1 case(s) still open`, then `Open: CASE-0001` |
| a pass with no artifact attached | 1 | `Passes with no artifact: CASE-0001`, and "a pass you reached by looking is not a measurement" |
| a status of `probably-fine` | 1 | counted as **open**, exactly as documented, so an unrecognised status cannot slip through as a result |
| a requirement no case traces to | 1 | `Requirements nothing checks: REQ-001` |
| a case referencing a surface nobody enumerated | 1 | refused at `add` time: "a case against a surface nobody enumerated has no denominator" |
| a complete campaign, one armed outcome-rung pass, one surface, one requirement | **0** | the clear verdict, carrying the fraction and the armed ratio |

So the gate discriminates in both directions, which is the property that matters. `evidence-page.py` then built the page from that clear campaign and exited 0.

**The selection ladder holds.** `scope --selective` was refused with exit 1 when no full run had been recorded: "no lastFullRun recorded, so there is no full result for a selective run to carry". `carry` was refused with exit 1 outside a declared selective run. And on a properly declared selective run, `carry` reported `ran 1 · carried 0 · protected 1`, naming the critical flow's outcome-rung case as the always-run floor and refusing to carry it. That is the documented behaviour, measured.

### Two things failed, and both are now fixed

**An empty campaign passed the gate.** `campaign.py init` followed immediately by `campaign.py check` exited **0** on zero requirements, zero surfaces and zero cases. Every count on the page was a truthful zero and the verdict read clear. That is a gate that cannot fail on the emptiest possible input, in a skill whose first rule is that a check which matches nothing returns clean and is indistinguishable from a clean surface. It was not a false pass in the ordinary sense, because nothing was claimed, but a run that crashed after `init` left a workdir that cleared the gate. Fixed in 0.5.0: no cases and no surfaces are each a blocker, with the reason stated in the output. Re-tested in both directions, since a gate that now always fails would be no better.

**The case record's requirement field is `req`, and nothing documented it.** `add --kind case` validated the surface id and the oracle rung and accepted every other key silently. A case written with `"requirement": "REQ-001"`, which is the word the SKILL.md and every reference use, was stored intact and then reported by `check` as a requirement nothing checks. I hit this while building the fixtures above, and it cost a round of debugging on a blocker that pointed at the wrong thing. Fixed in 0.5.0 from both ends: `add` reads `requirement` as `req` and says so, and phase 5 of the SKILL.md now names the key. Eval 9 in the set still exists, because the general property, that the registry round-trips what the plan claims, is worth grading whatever the key is called.

**No prior run exists.** No `grading.json`, no `results/` directory, no `benchmark.json`, no committed judge log, no blind-panel key anywhere under `plugins/test-campaign/`. Checked, not assumed. The only judge artifact in the plugin is `assets/judge-contract.md`, which is a specification rather than a run.

## What the eval set would settle

Nine prompts, in `evals/evals.json`. Each runs twice, once with the skill and once with no skill at all, because there is no predecessor and the honest question is whether the skill earns its context. Run every one against a disposable target: several prompts drive sweeps that enumerate and actuate controls.

Three prompts are where the answer would come from:

1. **`a-selective-green-cannot-read-as-a-full-one`.** The user touched the pricing page and wants to know if they are good to deploy. The comfortable answer runs the pricing tests, sees green and says yes. Grade four properties off the registry: is the scope declared with a reproducible basis, are the unrun cases carried rather than left looking passed, is the always-run floor protected, and does the verdict decline to say the suite passes. Every one of those is a file on disk, so this grades without judgment.

2. **`uniform-zeros-are-the-instrument-first`.** A sweep reports zero failures across 41 surfaces. Grade whether the check was proved able to fail before the result was written up. A baseline will almost certainly write up the clean sweep, which is what makes this the clearest discriminator in the set.

3. **`the-registry-round-trips-what-the-plan-claims`.** The one the `req` finding produced. Grade whether `check` reports zero untraced requirements after loading, and whether an untraced requirement is reconciled against the case records rather than accepted as a coverage gap.

Grade with a subagent that never sees the skill, marking each assertion passed or failed with quoted evidence, and no 1-to-10 scores. Every assertion in the set is a property of the registry, an exit code, or the wording of the verdict.

## Caveats, stated rather than buried

- **Nothing above measures the skill.** The gate results are facts about `campaign.py`. None of them says anything about what a model does after reading the SKILL.md.
- **The two script defects found here are fixed, and the fix is the same kind of evidence as the finding.** Both were re-tested in both directions: the empty campaign now fails, and a fully-resolved campaign still clears. Neither says anything about the skill's behaviour under a model.
- **Only the web lane was exercised at all, and only through the registry.** No iOS, macOS, Windows, Linux, SwiftUI or React Native lane was touched, no browser was opened, no sweep was run, and no evidence page was reviewed by a person. The lane ceilings in `references/harness-lanes.md` are documentation, not observations made here: the Windows and Linux rows come from vendor references and issue trackers read during the research pass, and nobody has stood either lane up against a real application on this machine.
- **The judge is unexercised.** `assets/judge-contract.md` describes a judge; no judge ran.
- **A defined eval set proves nothing.** Written assertions are a plan for a measurement.
- **The set may contain assertions that cannot fail.** Which ones is unknown until both arms run, and any a baseline also passes measure the model rather than the skill and should be relabelled as regression guards or dropped.
