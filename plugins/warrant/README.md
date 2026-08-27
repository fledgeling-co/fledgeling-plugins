<p align="center">
  <img src="assets/banner.png" alt="warrant: a porcelain tile holding five slate bars of decreasing width, the narrowest one lit in teal and resting on the surface while the wider ones float above it, beside the wordmark and the line 'delegated authority, revoked automatically'" width="100%">
</p>

<h1 align="center"><img src="assets/icon-256.png" alt="" width="34" valign="middle" /> warrant</h1>

<p align="center"><strong>Delegated authority, revoked automatically.</strong><br />
Eight skills for Claude Code that take the human out of per-item verification, by writing down exactly what a machine may decide and taking that permission away the moment the evidence stops supporting it.</p>

<p align="center">
  <img alt="Version 0.1.0" src="https://img.shields.io/badge/version-0.1.0-186A73">
  <img alt="SWE skill: verification governance" src="https://img.shields.io/badge/SWE_skill-verification_governance-434A55">
  <img alt="Research: 22 sources, 4 backends" src="https://img.shields.io/badge/research-22_sources_%C2%B7_4_backends-756E60">
  <img alt="Scripts: stdlib only" src="https://img.shields.io/badge/scripts-stdlib_only-756E60">
  <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-A9A399">
</p>

---

## Why it exists

We had 194 finished items sitting in a queue, every one of them already passed by an automated
verifier, every one waiting on the same person to look at it. The obvious move was to let the
machines finish the job.

So I paid for a research panel to find out how other people had done it. Four independent backends,
22 sources, about $20. **Nobody has done it.** Not one regulated software vendor where an
all-machine verification step was accepted as the control of record, and no enforcement action
anywhere whose defence was "the automated checks passed".

The reason turned out to have nothing to do with how good the models are. It's a rule about names:
an electronic signature has to belong to one individual, and a model identifier isn't an individual.
There's a second rule that bites harder for software, from the audit standards; you can only lean on
last year's testing of an automatic check if you can show the check hasn't changed since. A model
behind an API that quietly gets a new version fails that every time.

Neither rule stops you delegating the decision. Both stop you delegating the signature.

`warrant` is the shape that survives both. One signature, once, on a policy file that says what the
machine may close and how much rope it has; nobody signs an item ever again.

## What's different, in one table

| | The instinct | warrant |
|---|---|---|
| How to trust a verdict more | Add more models and vote | One grader, out of family. Nine judges from seven families give about **two** effective independent votes, and the best single judge beat the whole panel in every tested condition |
| Where extra models go | A bigger jury on the same question | Lens lanes on **different** questions, plus an adjudicator that settles a disagreement by running arithmetic rather than by counting |
| What to build first | The screenshot judge | The deterministic checks. The worst thing our product can do is show a tidy page with a wrong number on it, and no vision judge can see that, because nothing on the screen looks wrong |
| Whether the tests are enough | They're green, so yes | Measured. Over half of 15,000 injected bugs survived somebody's passing suite, and nobody has measured that for browser tests at all |
| How the reviewer sees the machine's answer | Pre-filled, to save them time | Blind. The same radiologists reading with and without a computer aid **missed more** cancers with it |
| How permission is granted | Someone decides it's fine now | Earned per defect class from evidence, and dropped automatically on a model version change, a new escape, or a drifting control chart |

## The eight skills

`charter` writes and validates the warrant, which is the only thing a human signs. `oracle` is the
arithmetic: every number on a screen has to trace to the record it came from, and tie to it.
`assay` measures whether the test suite can actually detect a fault before anything downstream is
believed. `panel` produces the machine verdict, snapshotting the evidence first so the thing being
judged can't quietly edit it. `feedback` is the calibration; when the pipeline misses something you
tell it, and that miss becomes a permanent test it has to keep passing. `lot` handles a backlog as a
batch under a declared risk limit instead of one signature at a time. `ratchet` decides how much
authority each defect class has earned and takes it away without asking. `ledger` keeps the
hash-chained record an auditor reads instead of those 194 signatures.

Note: `ratchet` is a plain script rather than a model call, on purpose. The thing deciding how much
authority a model has shouldn't be the model.

## What it won't do

**It won't get rid of the last signature.** One person still owns the policy, and I'd rather that
than a system that quietly pretends otherwise. If you want it gone, the honest route is a legal
opinion, not a better prompt.

**It can't tell you how often it wrongly fails something.** It learns from what it missed, because
you tell it. If it wrongly rejects good work and nobody looks, nobody finds out; there's a churn
detector that infers candidates, and it's a proxy rather than a measurement.

**It won't give you a defect rate.** You learn about the escapes somebody noticed, which is a
numerator with no denominator, so the reports print counts and trends and refuse to print a
percentage. That refusal is deliberate: two published studies of the same kind of testing report
failure rates of 1.4% and 32.4%, and both are correct, because they counted different things.

**It won't let a machine sign off disclosure content.** There's a tier in the ladder for it and it's
unreachable on the evidence we have. Customer-written text renders into the very screenshot a judge
reads, and hidden instructions in an image have made production models miss what's in front of them
up to 9 times in 10.

## Install

```
/plugin marketplace add fledgeling-co/fledgeling-plugins
/plugin install warrant@fledgeling-plugins
```

`stocktake` calls this plugin at Done to decide whether a card may reach Verified; it
ships separately at [stocktake](../stocktake/README.md). Nothing here needs it.

## Getting started

```bash
python3 scripts/charter_init.py --root <your-repo>   # drafts the warrant, every class at tier 0
# fill in the owner, the risk appetite and the tier-3 thresholds; they're judgement calls
python3 scripts/charter_validate.py --root <your-repo>   # exit 0 before anything else runs
```

Then run the planes in order: `oracle`, `assay`, `panel`. `ratchet` after any of them.

## Where the depth is

Every rule in every skill traces to a claim id, and every claim id resolves in
`docs/deep-research/claims.json` alongside the five panel reports it came from.
`references/evidence.md` separates the measured findings from the reasoning, and says which of the
22 sources are still paywalled and unread. `references/why-not-a-jury.md` is the one to read before
anyone suggests adding another model.
