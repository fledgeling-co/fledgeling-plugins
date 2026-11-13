# Changelog

## 2.6.0 - 2026-11-13

Pinned items now carry provenance. Each Tier-1 item ends with the turn or event anchor it came from, so the verify step checks that every pinned item's anchor exists and says what the item claims, instead of re-reading the whole window. Each standing constraint names its source (a user message, an instruction file, or a tool or system refusal), after a test reader listed an agent's own receipt fields as project rules.

A new section covers windows the summariser cannot hold: a session from another CLI or model, or one larger than the reader's context. It routes to `resume-session:resume-session`, whose readers extract every instance with an anchor while the keep-or-drop call stays with one agent. The evidence for that split is one reader on one chunk, and the section says so.

`scripts/score_retention.py` accepts a `transcript.md` rendered by resume-session, so a handover of a Codex, Muse, Antigravity, Cursor or Grok session can be scored. For Claude Code transcripts it now counts messages typed while the agent was mid-turn, which Claude Code stores as `queue-operation` enqueue rows rather than user rows (2,556 such messages across 76 of the last 400 sessions on this machine, 489 of them also delivered as plain user rows and counted once), and it stops counting harness task notifications as user messages. The 121-event and head-to-head figures in `references/evidence.md` and `docs/` were measured with the earlier extractor; a re-run would change their user-message and correction denominators.

The eval prompts ran for the first time (`evals/results-2026-11-13.json`, summary at the top of `evals/EVALS.md`): skill 62 of 62 assertions against a no-skill baseline's 51 of 62 on the twelve text evals, graded blind by an in-family model because every out-of-family lane was down; seven of the twelve do not discriminate. The head-to-head against the built-in `/compact` (three usable transcripts) did not favour the skill: soft recall of rejected approaches 60.7% against 74.2%, with summaries 2.7 times shorter. `benchmark_vs_compact.py` gains `--bare`, because a first run let the operator's global brevity rules into the skill arm only, and it now keeps every arm's summary so `score_retention.py --against` can rank a pair.

Two pre-existing lint failures in SKILL.md were fixed in passing ("you must", "thorough").

## 2.5.0

Earlier releases predate this file; see the git history.
