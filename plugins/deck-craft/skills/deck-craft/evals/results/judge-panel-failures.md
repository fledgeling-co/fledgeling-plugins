# Panel members that failed, recorded rather than dropped

Two of four families did not return a verdict. Neither was retried into the ground.

| family | lane | outcome |
|---|---|---|
| OpenAI (`gpt-5.6-sol` via `codex exec`) | `codex exec --skip-git-repo-check -m gpt-5.6-sol -c model_reasoning_effort=high -s read-only` | **failed** — `You've hit your usage limit … try again at Aug 20th, 2026`. No other OpenAI lane is configured on this machine, so no same-model substitution was possible. |
| xAI (`grok-4.6`) | `grok -m grok-4.6 --effort xhigh -p` | **failed** — killed by the 900s deadline (rc 143) with no output. |
| xAI (`grok-4.6`), fallback harness | `cursor-agent -p --force --model grok-4.6` | **failed** — `ActionRequiredError: … You're out of usage.` |

A first attempt at `codex exec` also failed with `Not inside a trusted directory and
--skip-git-repo-check was not specified`, because the judging bundle lives outside a git repo. That
one was a harness error rather than a capacity limit and was corrected before the usage limit was hit.

So the panel is **two independent families, not four**, and that is the honest denominator for the
result. Both returned complete verdicts on all seven cases.
