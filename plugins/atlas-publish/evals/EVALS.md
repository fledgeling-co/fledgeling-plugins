# Evals

**Nothing in this file is a measured result about how well this skill works.** The eval suite exists now, in [`evals.json`](evals.json), and it has not been run. No prompt has been executed with the skill loaded, none without it, no judge has looked at any output, and there is no pass rate. Shipping in that state is honest; shipping a file that quietly omits the subject is not, because it reads as though the pipeline ran.

What follows is what was checked mechanically, what the eval set would settle, and what none of it can tell you.

## What was checked, and what it found

Every figure below was measured on 20 August 2026 against the files in this plugin.

**The SKILL.md parses and carries the three expected keys.** `name` matches its directory, the description runs to 1,262 characters, and `allowed-tools` is declared. Its sibling in the same build did not parse, which is how the check earned its place: a bare colon inside a plain-scalar description made the YAML parser read a nested mapping, and no gate in this repo opens the second skill of a two-skill plugin. That skill has since been split out into [code-review](../../code-review/README.md), and the finding travels with it.

**It sits inside the length target.** 231 lines, 178 of them non-empty, against a 300-line target. Depth sits in references: 666 lines across 6 files, opened per step rather than carried on every call.

**The voice gates pass.** `agent_voice_lint.py --format skill` exits 0 on the SKILL.md with no hard-check failures. `voice_lint.py --format marketing` exits 0 on the plugin README, including its alt text.

**The Opus 5 prompting rules hold.** A search for verification scaffolding ("double check", "re-verify", "confirm your answer") returns nothing across the skill and its references. A search for pressure language ("CRITICAL:", "you MUST") returns nothing. The delegation cap is explicit at 3 subagents for one release run, and the output length is calibrated at 20 lines for the hand-off.

**The brand artifacts pass their own gates.** `audit_sheet.py check` exits 0; every image the sheet references resolves and the takes match the master. `banner_sheet.py check` exits 0. The banner is exactly 3200x1040. At 16px the icon measures a luminance spread of 0.2415 against a family median of 0.2146 across its siblings, and its accent gate is 2.07px wide, over the 1.5px floor. Ink sits at 8.64:1 against the ground.

**One finding in the Atlas repo was verified by reading the source.** `apps/atlas-api/tests/unit/lib/ota-cert-parity.test.ts` guards its only real certificate-to-key comparison behind `it.runIf(!!parityKey)` and pairs it with a companion asserting `expect(true).toBe(true)`. With `OTA_CERT_PARITY_KEY` unset, the file exits 0 having compared nothing. That is deliberate in the test and keeps a key-less CI run honest; it was not deliberate in the release skill, which read the green as a parity gate. Eval 4 is written to force exactly that case.

**Every cited report resolves.** All six links in the README return 200 at `dossier.fledgeling.app`, checked on the day of writing; *vacuous* and *deputy* had been unpublished earlier in the same build and went live before it shipped. All six are exported into `docs/deep-research/` regardless, so the citations in [`references/evidence.md`](../skills/atlas-publish/references/evidence.md) stay readable without leaving the repo and survive a page being pulled.

## What the eval set would settle

Five prompts, in `evals.json`. Two of them carry most of the weight:

- **Eval 0** puts the classification rule under pressure from a user who has already decided the answer. The rebuild claims the lane comes from the fingerprint rather than from intent, and this is the case where those two disagree.
- **Eval 4**, the adversarial one, hands the skill a green test suite and a confident user and asks it to record a gate as verified. This is the failure the whole three-state gate model exists to prevent, and it is the one case where the honest answer costs the user something.

The other three cover the founder gate holding against a reaffirmed instruction, the read-back rule after an irreversible step, and not-run reported apart from passed when the key is simply absent from the shell.

## Caveats, stated rather than buried

**The comparison that matters has not been made.** This skill replaces a working predecessor. Whether the rebuild is better than the 99-line skill it came from is exactly the question the eval set was written to answer, and it is unanswered. Everything above is a property of the files, not of the results they produce.

**A mechanical pass is a weak guarantee.** Frontmatter parsing, line counts and lint exits say the artifact is well formed. They say nothing about whether the classification logic is right, or whether a runner holds the founder gate when a user pushes back twice.

**Two icon measurements never ran.** The perceptual material metric could not run because torch is absent, so material was never measured. The blind judge panel could not form a majority: there was no OpenAI key and the cursor lane exited 1, leaving only the generator's own family, which protocol excludes. Both are recorded on the audit sheet rather than papered over.

**The pipeline has never been run end to end.** No release has been shipped through this text. The `@vercel/blob` call shape is written against the installed 2.4.0 type signature, and no upload was executed to confirm it at runtime.

**Single runs would carry sampling noise.** When these evals are run, one execution per arm is a data point and not a result. The prompts are written to be run more than once.
