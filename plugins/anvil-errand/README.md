# anvil-errand

<p align="center">
  <img alt="Version 0.1.0" src="https://img.shields.io/badge/version-0.1.0-D33C21">
  <img alt="SWE skill: orchestration" src="https://img.shields.io/badge/SWE_skill-orchestration-434A55">
  <img alt="Evals: 8 defined, not yet run" src="https://img.shields.io/badge/evals-8_defined,_not_run-756E60">
  <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-A9A399">
</p>

Send a Claude Code agent to work in a container on a machine that is not this
one, through [Anvil](https://github.com/lprhodes/anvil), and read the refusal
correctly when it cannot.

## What it is for

Anvil can run an agent on a paired node: a spare PC, a second Mac, a WSL2
distro on a Windows box. Every piece of that path was built and proved on real
hardware separately: a workload running on the node, the Mac app watching one,
a real provider call going out through the credential-holding proxy.

What was missing was one name for them. `anvil errand` is that name, and this
skill is the human-facing side of it.

```bash
anvil errand --check                    # can this work? changes nothing
anvil errand -p "review /work and list the three worst bugs"
```

## The part that earns its keep

Not starting the errand: reading the refusal.

The verb asks whether every piece is in place *before* anything starts, and
when one is missing it answers with a stable identifier rather than a symptom.
`errand_no_node` and `node_unreachable` are different facts with opposite next
steps; so are `image_absent` and `image_unverified`, and telling someone to
build an image they already have is exactly the nearest-fit failure that split
exists to prevent.

The skill carries the table that turns each kind into the one step that clears
it, plus the two refusals from further down the path whose cause is usually not
what they first look like.

## What it deliberately does not do

It starts nothing on your behalf: not the proxy, not a pairing, not a
provision, not an install. It reports what is missing and stops, because
setting the path up has real consequences on someone else's machine.

When a precondition fails nothing is started: no container, and no idempotency
key spent, so re-running after the fix is a clean first attempt.

## Install

```text
/plugin marketplace add fledgeling-co/fledgeling-plugins
/plugin install anvil-errand@fledgeling-plugins
```

## Where the recipe lives

`docs/ERRAND_RUNBOOK.md`, in the anvil repo. That is the source of record for
provisioning, it carries the evidence behind each of its claims, and this skill
does not replace or reproduce it; a second copy of a recipe drifts, and the
one everybody cites ends up being the stale one.

Use this skill for the verb and its refusals. Send anyone provisioning a
machine to the runbook.

## Status

Version 0.1.0. Shipped alongside the `anvil errand` verb (ANV-0365).

This plugin carries no icon, banner or eval suite yet. The pieces of the
standard `create-skill` brand treatment that need a human-chosen concept, or
that spend money, were left for a later pass rather than guessed at. The
substance (the SKILL.md, checked line by line against the verb's actual
behaviour) is complete.
