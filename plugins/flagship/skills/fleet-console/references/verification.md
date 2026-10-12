# Verification boundaries

The behavioral suite uses generic fixtures and contacts no live sessions.
Run `python3 -m unittest discover -s <this-skill>/scripts`.

Transport tests verify literal shell-looking text remains one argv value,
terminal/unknown targets and stale observations are refused, owner/scope
attestations are required, UUID/cwd reconciliation is enforced, closed ingress
stops preflight, and a durable locked journal suppresses retries after uncertain
sends. Partial native receipts survive wrapper timeouts without upgrading them
to delivery or completion.

Adoption tests verify the observed Claude array and Codex `installed` schemas;
empty/malformed/wrong-key and available-only snapshots cannot pass. Missing,
duplicate, disabled, uninstalled and old-version targets fail. Changed unrelated
installations, empty files and stale cached contents fail. A successful hash and
version check explicitly leaves active-session loading unestablished.

Waiting-choice tests keep queued receipts separate from callback resolution,
restrict agent-view controls to verified background targets, require ownership
of the same SDK query, reject permission prompts and unsettled/stale/changed
choices, and request current-control review before suggesting local input. The
choice planner is read-only and never answers the prompt itself.

Live validation has demonstrated native Claude `ListAgents`/`SendMessage` from
a bounded own bridge using an approved execution route, queued message IDs,
matching recipient readback, and one recipient acknowledgement with resumed
work under its own goal hook. Supported Claude/Codex local marketplace refresh
has produced installed skill bytes matching source, with unrelated installed
identities/enabled states preserved. Codex app supervision has also used this
skill through accepted native dispatch, acknowledgement and subsequent work.
These observations establish those tested routes, not universal reachability.

Runtime-specific unavailable daemon, closed Muse ingress, no Grok leader,
empty Cursor persistent listing and denied Ghostty access must be rechecked
permittedly each run. Record exact versions, identities, timestamps, queue IDs,
progress and remaining acceptance debt in private per-run evidence outside the
distributed plugin. Successful installation does not reload an active session;
queued dispatch does not prove acknowledgement; continued work does not prove
acceptance. No publisher, scheduler or persistent access service is installed
by this skill.
