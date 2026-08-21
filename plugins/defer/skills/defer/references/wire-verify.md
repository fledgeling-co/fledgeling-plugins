# Proving a lane ran as routed

Launch parameters have been observed not to stick. A lane's evidence is its own
captured output, never the flags you passed — so every lane in the registry
carries a `verify` method, and this file is what each one means.

The rule underneath all four: **an absent or empty output file is a lane failure,
not a quiet pass.** A gate that produced no verdict did not pass; it did not run.

## `codex-header` — codex-sol, codex-terra

Codex prints a header, and it is trustworthy for what it claims:

```
model: gpt-5.6-terra
reasoning effort: high
```

Grep for both lines. Then **check the `-o` file is non-empty**, because the
header prints correctly on a run that never produced a token. This is exactly how
codex fails when it is out of allowance — model and effort as requested, output
file empty, and the real reason only in the log tail:

```
ERROR: You've hit your usage limit. ... try again at Aug 27th, 2026 1:30 PM.
```

Codex validates neither `-m` nor the effort config, so a clean header proves the
flags parsed, nothing more.

One trap that is not a lane failure: `Not inside a trusted directory and
--skip-git-repo-check was not specified`. Codex refuses to run outside a git
repo. Run it from the repo, or pass `--skip-git-repo-check`.

## `relay-ledger` — glm, opus, fable

Tail Relay's per-request ledger and read back the model that actually served it:

```bash
tail -3 ~/Library/Application\ Support/Relay/spend/$(date +%Y-%m).jsonl \
  | python3 -c 'import sys,json;[print(json.loads(l)["model"], json.loads(l).get("bindingId")) for l in sys.stdin]'
```

For GLM this is the check that matters, and it is not optional. Without
`X-Perch-Binding: glm` the same command runs Claude, succeeds, and returns
something plausible — so the ledger saying `glm-5.3 glm` is the only thing that
distinguishes a GLM answer from a Claude answer wearing one.

## `grok-store` — grok

The grok CLI records each completed turn under
`~/.grok/sessions/<encoded-cwd>/<uuid>/`. `summary.json` carries
`current_model_id`, and `updates.jsonl` carries the turn's usage and cost. A
session directory with no `turn_completed` record is a turn that never landed.

Grok announces exhaustion in its own transport rather than on stdout — a 402
carrying `Grok Build usage balance exhausted`, or a 503 `all-accounts-exhausted`
— so check `updates.jsonl` rather than trusting an empty-looking success.

## `output-nonempty` — gemini

`agy` writes no session metadata worth reading back: its transcripts record no
model id, no tokens and no cost. The only available check is that the redirected
output file is non-empty and does not contain an error banner. `--print` buffers
to exit, so never poll its stdout mid-run — wait for the process.

This is the weakest verification of the four, and it is worth saying so plainly
rather than treating gemini's silence as agreement.

## One artefact that affects every Claude lane

A `claude -p` one-shot inherits the session's `SessionStart` hooks, so a response
can arrive with a marker glyph prepended:

```
🫥 LANE OK
```

A strict parser looking for `VERDICT:` on the first line will miss it. Strip a
leading non-ASCII marker before matching, or match the verdict anywhere in the
first line rather than anchoring to its start.

The same inheritance is why a lane call is never a clean-room baseline: `claude
-p`, and the grok CLI too, both load the repo's instruction files. A grok session
opened with roughly 35KB of `CLAUDE.md` and workspace rules before the prompt
itself in the week this was written — which is both a cost and a contamination,
and is why a lane asked to judge blind must be handed its evidence inline rather
than pointed at the repo.
