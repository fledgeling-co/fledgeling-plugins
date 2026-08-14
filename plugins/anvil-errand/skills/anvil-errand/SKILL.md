---
name: anvil-errand
description: Send a Claude Code agent to work in a container on another machine through Anvil, using the single `anvil errand` verb, and read its refusals correctly when a piece of the path is missing. Covers the whole loop — check the preconditions, start the errand, watch it, stop it — and translates each stable refusal kind (errand_no_node, node_unreachable, image_absent, image_unverified, errand_ticket_unavailable, errand_proxy_unreachable) into the one next step that clears it. Use when someone wants to run an agent on their node, spare PC, or second machine rather than on this Mac — "run an errand", "send this to the node", "run Claude Code on the other machine", "offload this to the PC", "why was my errand refused", "anvil errand says image_absent". Not for setting the path up from nothing: provisioning the node, the engine, the image, the pairing and the proxy is docs/ERRAND_RUNBOOK.md in the anvil repo, which stays the source of record.
---

# anvil-errand

Run a Claude Code agent in a container on a machine that is not this one.

`anvil errand` is one name for a path whose pieces already existed and were
proved on hardware separately. The verb's own contribution is small and
specific: it asks whether every piece is in place **before** anything starts,
and when one is missing it says which, by a stable identifier, with the step
that fixes it.

That is the whole reason to prefer it over typing the underlying commands. The
failure it removes is not "the errand did not work" — it is discovering the
missing piece halfway through a container start, from a symptom that points
somewhere else.

## The loop

```bash
anvil errand --check                    # can this work? changes nothing
anvil errand -p "review /work and list the three worst bugs"
```

`--check` runs the preflight and stops. Everything after the verb is the
agent's own argv, appended to the image's entrypoint — so `-p`, `--model`,
`--output-format stream-json --verbose` and the rest reach Claude Code itself.

`--check` is positional and taken only immediately after the verb, so a prompt
that happens to contain the word (`anvil errand -p "explain --check to me"`)
still runs.

Watch and stop it with the ordinary verbs — the errand is a normal job:

```bash
anvil ls                      # the job id
anvil attach <job-id>         # its own stdout, streamed; read-only by design
anvil wait <job-id>           # blocks, exits with the workload's own code
anvil stop <job-id>
```

`anvil attach` will not accept keystrokes and that is not a fault: the
container is started detached, so PID 1's stdin is at EOF from the first
instant. Use `anvil exec <job-id> -- <cmd>` to open a *separate* process beside
the agent.

Claude Code's default `-p` text mode prints nothing until it terminates, which
has been measured at around three minutes across twenty-odd provider calls. An
empty log during that window is silence, not a hang. Add `--output-format
stream-json --verbose` when you want it to narrate while it works.

## Reading a refusal

A refused errand exits non-zero and prints `denied [<kind>]: <sentence>`. Branch
on the kind; the sentence is for the human and may be reworded.

| kind | what is missing | the next step |
|---|---|---|
| `errand_no_node` | This daemon is not driving another machine at all — it is Mac-as-node. | Pair a machine and name it in `$ANVIL_STATE_DIR/node.toml`. Runbook step 3. |
| `node_unreachable` | A node **is** configured and did not answer. Includes the case where it went to sleep. | Wake it, or check `anvil-node serve` is running there. Runbook step 4. |
| `image_absent` | The node answered and has not got the agent image. | Build it **on that machine**, in the store the node's own engine reads. Runbook step 1. |
| `image_unverified` | Anvil could not establish either way. | Read the reason it carries. Deliberately not `image_absent` — do not go and build an image you may already have. |
| `errand_ticket_unavailable` | The template needs a job-scoped ticket and this Mac has no `$ANVIL_STATE_DIR/errand.toml`. | Write the file, then restart the daemon — it is read once, at start-up. Runbook step 5a. |
| `errand_proxy_unreachable` | The file is there and nothing is listening where it says tickets are minted. | Start the credential-holding proxy. Runbook step 2. |

Two refusals come from further down the same path and are worth recognising
because their cause is not what they first look like:

- `egress_unenforceable` — the node cannot hold the network posture the errand
  asks for. Most often the engine there is **rootless**, which advertises no
  egress backend at all. The sentence names the engine the node picked, which
  is usually the whole cause.
- `engine_refused` — Apple `container` cannot deliver `[env]`, and it is first
  in the macOS probe order. On a Mac node, name podman.

## What this verb deliberately does not do

It starts nothing on your behalf. It will not start the proxy, pair a node,
provision a machine, or install anything — it reports what is missing and
stops. Setting the path up is a separate, human job with real consequences on
another machine.

When a precondition fails, nothing is started: no container is created and no
idempotency key is spent, so re-running after you fix the piece is a clean
first attempt rather than a retry.

## Where the real recipe lives

`docs/ERRAND_RUNBOOK.md`, in the anvil repo, is the source of record for
setting the path up: the engine, the image, the pairing, the proxy, the ticket
file, and which node shapes are proved to work. It is current, it carries the
evidence for each claim, and this skill does not replace it.

Read it rather than reproducing it here. A second copy of a recipe drifts from
the first, and the version everyone cites ends up being the stale one — which
has already happened once in that repo, with two errand runbooks and every
reference pointing at the wrong one.

Use this skill for the verb and its refusals. Send anyone provisioning a
machine to the runbook.

## Working notes

Answer from the refusal kind first. It is the fact; the prose around it is
support, and one of the refusals in that repo (`outside_window`) is on record
as suggesting a cause that is wrong in two of its three cases.

If the check passes and the errand still fails, say what you measured rather
than naming a likely cause. The `--check` passing means the pieces are present,
which is a different claim from the workload working.

Keep replies short — the state and the next step. Reach for a subagent only if
you are searching a large tree for something; a single errand and its refusal
needs no delegation.
