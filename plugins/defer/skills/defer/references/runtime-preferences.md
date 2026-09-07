# Resolve the current workflow before using compatibility lanes

The owner's preferred roles are Claude Opus 5 for intake, triage and planning,
Gemini 3.8 for implementation after those artifacts exist, and GPT-6 for
orchestration. A task's explicit choice overrides these defaults. Keep an already
running orchestrator unless the task calls for a handoff. The role names are not
API selectors: Gemini variants, GPT-6 variants and effort settings depend on the
serving harness and account.

## Preferred-model path

1. Read current conversation authorization and applicable project instructions.
   Honor active external-model restrictions unless the current user explicitly
   supersedes them. Recognize `OPT-OUT: external-models` and the legacy exact
   directive lines `ANTHROPIC-ONLY`, `NO EXTERNAL MODEL CLIS`, and
   `external-model-clis: off`. Match whole directive lines outside fenced examples,
   blockquotes and historical notes; mentioning a marker in prose is not an opt-out.
   Do not treat a Claude CLI carrying a non-Anthropic proxy binding as Anthropic
   execution. If external use is opted out, continue in an authorized in-session
   lane and record any unavailable independent review instead of dispatching.
2. Identify the role and read its inputs. An implementation handoff includes the
   real intake, triage and plan paths, scope, file ownership and acceptance tests.
3. Discover the harness's advertised model inventory and its current dispatch
   schema or documented CLI options. Use the current inventory, not a remembered
   command or a static registry row. Match the preferred role to an exact supported
   model selector and permitted effort value. Record the discovery source.
4. Check current availability, authorization and relevant account headroom using
   that harness's status tools. Unknown quota is unknown, not zero or unlimited.
   A live request proves availability only for the model/account actually serving it.
5. Dispatch through the available native model tool or CLI using that discovered
   selector and supported parameters. Give it the bounded brief and a unique output
   path. For orchestration/intake/triage/plan, use a read-only or advisory contract
   unless that stage explicitly owns edits. Implementation owns only its assigned
   files. Respect sandbox and approval controls.
6. Capture the returned serving-model identity when available, run/session ID,
   output location, completion status and evidence required by the task. A header
   containing requested flags is not proof of serving-model identity. A successful
   exit with empty/missing output is an incomplete dispatch. If runtime identity
   cannot be observed, label it unverified; do not claim an independent family.

Write a route record before dispatch and append the execution receipt afterward:

```json
{
  "role": "implementation",
  "requested_model": "Gemini 3.8",
  "selector": "<exact selector from this harness>",
  "inventory_source": "<tool result or documented installed-runtime inventory>",
  "effort": "<supported value, or omit this field>",
  "route_source": "user-preference",
  "inputs": ["<intake path>", "<triage path>", "<plan path>"],
  "output_path": "<unique result path>",
  "serving_model": null,
  "run_id": null,
  "status": "resolved"
}
```

This is a template, not a runnable request. Replace the placeholders with observed
values; use the native tool's real schema rather than passing this record to it.
Do not invent a selector to fill a gap. If the preferred model is unavailable,
report that fact and resolve an authorized fallback with the same scope. Keep
requested, selected and observed model identities separate in the final result.

## Compatibility-lane path

`scripts/lane_registry.py`, `lane_pick.py` and `lane_run.sh` retain the previously
calibrated lanes. Their IDs, prices, shape scores and delivery penalty describe
the recorded configurations; the `gemini` lane currently names Gemini 3.7 Flash,
not Gemini 3.8, and the Codex lanes name GPT-5.6 variants, not GPT-6.

The bundled compatibility scripts do not inspect project opt-out directives;
the conductor must apply the authorization step above before calling them.

Use this path when the caller asks for one of those lanes, no newer preferred role
applies, or an authorized fallback resolves there. Run `lane_pick.py` for its live
meters and exact argv; never reconstruct that argv from prose. Confirm the model is
still advertised before executing it. The preferred-model path does not wait for
a legacy matrix to contain a new model, and it does not relabel an old score as a
new measurement. Unknown capability calls for explicit acceptance criteria and
honest reporting, not an automatic ban or a fabricated ranking.

Update a registry entry only when its exact selector and parameter support have
been observed and applicable regression checks can run. Updating prose alone does
not migrate the executable registry. Static callers of `lane_run.sh` keep the
compatibility policy until they explicitly adopt this preferred-model path.
