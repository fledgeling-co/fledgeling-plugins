# Native recovery and installed adoption

## Bounded Claude bridge

Read current `claude --help` and version first. When no existing Claude tool
surface is available, a bounded own `-p` session can call the supported native
`ListAgents` tool. Do not resume a recipient to inject a message.

```sh
claude -p --tools ListAgents --allowedTools ListAgents \
  --output-format stream-json --verbose \
  'Call ListAgents once. Return exact peer names, addresses and states. Do not send, resume or start peer work.'
```

Use a subprocess timeout, retain stream output and private per-run receipts.
Keep the configured model route. This bridge is a new discovery session, not
new implementation work; verify it will not incur unapproved spending. After
reconciliation and ownership review, a controlled continuation of **your own
bridge** may allow only `ListAgents,SendMessage` and request one bounded packet
per exact peer. Re-list before sending. The bridge's peer address can change
when resumed, and its inbox may disappear when it exits; record the actual
sender address and verify acknowledgement at the recipient when replies
cannot reach that ephemeral sender. Do not claim it is a persistent listener.

`ListAgents` can return name/short address without UUID or cwd. Reconcile these
with permitted session metadata, matching project transcript and current task
artifacts before steering. Read only needed identity/state fields; session
records may contain sensitive authentication material. Never dump records,
read key files or modify records/transcripts. Exclude your own bridge, another
supervisor's targets, shell states, completed objectives and explicit pauses.
A stale background `agents --json` row is not an independent reachable peer.
An ECONNREFUSED daemon control endpoint with no workers is a stale route;
record it rather than restarting saved tasks.

### Diagnose the actual failure

No tool calls plus repeated `api_retry` events is insufficient to diagnose
credentials or provider outage. Check permitted endpoint configuration without
printing secrets. Distinguish sandbox `Operation not permitted` from connection
refused, provider HTTP 429/rate limit, HTTP authentication rejection and inbound
hold/refuse. If the execution environment offers an approved one-shot sandbox
or network escalation, use that supported approval path for the same bounded
operation; it changes no persistent settings. Otherwise report the restriction.
Do not switch to denied computer use, forge protocol frames, open ingress,
change credentials, unlock keychains or relax session permissions.

A wrapper timeout can happen after native tools and a final success frame,
while shutdown hooks linger. Inspect actual tool-result frames and message IDs;
keep timeout/uncertainty recorded and never resend automatically. Conversely,
a model summary or successful process exit without actual native tool evidence
proves neither discovery nor dispatch.

| Evidence | Established claim |
|---|---|
| Native `SendMessage` success with message ID and queue notice | Queued dispatch only |
| Recipient's matching received-message wrapper/readback | Delivered/readback; not yet accepted task |
| Recipient explicitly acknowledges packet | Acknowledged |
| Fresh task artifacts/runner action or recipient progress report | Progress, with attributed versus independently verified evidence distinguished |
| Task acceptance evidence | Completed objective |

Hold/refuse notices remain receiver/user decisions. A nonblocking owner decision
must stay open while independent authorised work continues. Respect the target's
own goal hooks, fleet governor and stuck stops; oversight does not create a
second implementation conductor.

## A waiting clarification is a different control surface

Verified against Claude Code **2.1.285** and current official documentation.
Recheck help, session kind and advertised controls on later runtimes; these are
observed control boundaries, not a claim that external answering can never exist.

A queued `SendMessage` is plain peer text, not the result of another session's
pending `AskUserQuestion`. The recipient reads peer text between tools; an open
question can therefore leave a decision queued until its own input handler
returns. Do not infer resolution from a queue receipt or send the decision again.
See [cross-session messaging](https://code.claude.com/docs/en/cross-session-messaging).

[Agent-view peek](https://code.claude.com/docs/en/agent-view) supports choosing
numbered answers on verified **background** rows. Interactive sessions open in
other terminals are excluded until backgrounded. `claude attach` is also a
background-session control. Do not background, respawn or resume a productive
interactive target to manufacture access to its question.

The [SDK input callback](https://code.claude.com/docs/en/agent-sdk/user-input)
returns answers for the query its host owns. It does not document attaching a
new host to another live interactive callback. Installed help's `--input-format`
and `--permission-prompts` concern print/SDK operation; no cross-session answer
command was verified. [Remote Control requirements](https://code.claude.com/docs/en/remote-control)
exclude custom `ANTHROPIC_BASE_URL` endpoints and Bedrock routing in the observed
runtime. Do not change endpoints, authentication or permissions to unlock it.

Once the user has explicitly settled the choice, first check for a supported
control owned by this exact runtime. If none is available, provide one actionable
handoff: identify the existing session and question, give its exact emitted
choice label, and ask the operator to select it there and submit. This is applying
an existing answer, not a new decision question. Use `clarify:clarify`'s evidence
sweep; record `referral: not needed` when the axis is already settled. Do not
re-ask the preference. Do not forge results, edit inbox/transcript/queue files,
answer permission prompts or use denied computer access. After submission,
verify recipient readback/acknowledgement and fresh work separately.

The helper's read-only `choice --packet <file>` plans this handoff. Its packet
requires a full `session_id`, `provider: claude`, `cli_version`, fresh
`observed_at`, `state: waiting`, `waiting_tool: AskUserQuestion`, runtime `kind`
(`interactive`, `background`, `sdk`), exact `choices` and `selected_label`.
Attest `identity_verified`, `original_scope_reviewed`, `explicit_user_decision`
and `supported_controls_reviewed`. Mark `owns_sdk_query` or
`agent_view_peek_available` only after verifying that control. It performs no
input, send, resume or configuration change. Missing control review returns a
reverification step; a peer receipt never upgrades `prompt_answered` to true.

## Source, installation and active loading

Source version, installed version, installed skill bytes and active-session
loading are separate checks. Read documented `plugin list --json` and details;
do not equate a repo file or `up_to_date` response from an old marketplace
source with adoption. Preserve a nonempty before snapshot and the exact installed
identity/scope. Check the skill is exposed (Claude details includes `fleet-console`),
then compare source and the runtime-reported installed cache content. Codex list
uses `installed` and `available`, not `plugins`; a zero-versus-zero comparison is
not validation. A cache path must be permitted and tied to the exact runtime
installation; do not invent or enter withheld package paths.

For an already approved local-directory marketplace, the observed supported
update commands are:

```sh
claude plugin update flagship@fledgeling-plugins --json
codex plugin add flagship@fledgeling-plugins --json
```

When authorised to adopt a tested local checkout instead of a stale remote
source, validate the checkout's declared marketplace name and exact plugin ID.
`claude plugin marketplace add /path/to/marketplace` updates the same named
source. Codex refuses a different source under an existing name: record the
old source and installed/enabled snapshot, remove **only that marketplace
source**, then add the approved local directory and reinstall only the target.
Use `codex plugin marketplace remove NAME --json` and
`codex plugin marketplace add /path/to/marketplace --json`. If addition fails,
restore the recorded source through those supported commands; never edit cache
or registry files directly. Do not publish/commit/push just to refresh a cache.
Ask before any route requiring new auth, persistent access/service, security
permissions or interruption of productive sessions.

Run the bundled verifier with actual snapshots and permitted cache/source files:

```sh
python3 <this-skill>/scripts/verify_adoption.py \
  --provider codex --before /run/before.json --after /run/after.json \
  --target flagship@fledgeling-plugins --version VERSION \
  --source-skill /path/to/source/SKILL.md --cached-skill /path/to/cache/SKILL.md
```

It rejects empty/wrong-schema snapshots, ambiguous or disabled targets, old
versions, changed unrelated installations and empty/mismatched skill content.
It verifies installation, not loading inside an already running process. Use
hot reload only when documented; otherwise leave productive sessions running
and report next-session adoption or arrange an approved idle restart. CLI
plugin authentication failures and Muse closed ingress/withheld store paths
remain provider-specific blockers. A local install producing a second identity
is not an update to the existing one.
