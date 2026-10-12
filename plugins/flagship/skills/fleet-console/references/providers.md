# Provider controls — verified 2026-09-30

Re-probe the installed version and help each run. Advertised capability, reachable transport and completed delivery are separate claims.

| Provider/version observed | Review | Messaging/control | Measured limitation |
|---|---|---|---|
| Claude Code 2.1.285 | `claude agents --json`; `--all` includes completed background sessions; `claude logs <background-id>`; in-session `/list-agents` or `/peers` | Native `ListAgents` and `SendMessage` across independent sessions; `claude attach <id>` for background terminal | Native independent discovery/send and recipient readback were verified using an approved bounded bridge. Separate stale background rows returned ECONNREFUSED to daemon control.sock; metadata is not proof of a reachable process. |
| Codex 0.153.4 | `codex agents` interactive shared daemon; Codex app `list_threads` and `read_thread` | `codex queue --thread <UUID> --message <text>`; app `send_message_to_thread` for app-owned target | Queue support verified in help, not yet a live CLI send. App listing/reading verified; app and CLI endpoints must not be assumed identical. |
| Grok 1.0.41 | `grok sessions list --limit N` (history/search), `grok leader list`, `grok leader info --json`; in-session dashboard | Dashboard selected-agent reply queues busy work; `--resume` restores history, not a message transport | No reachable leader observed; remote search warned and printed no sessions. No standalone external send command verified. |
| cursor-agent 2026.09.15-d2fe57e | `cursor-agent persist list` for persistent sessions; `ls` is an interactive resume surface | `persist attach <session>` for persistent terminal; `--resume <chatId>` resumes a conversation | No persistent sessions observed. No standalone send command verified; other interactive sessions may still exist. |
| Muse Code 1.4.1 | `muse session-message list --json`; trace/export for history | `muse session-message send --target <UUID> --json < body`; optional reply token/display context | Listing returned `status: unavailable`, `error_code: external_agent_ingress_closed`; respect it. Do not open ingress or override policy. |

## Claude: three distinct mechanisms

Independent session messaging is now supported, not limited to teams. Official [cross-session documentation](https://code.claude.com/docs/en/cross-session-messaging) describes `ListAgents`/`SendMessage`, available from 2.1.224 on macOS/Linux (2.1.234 native Windows); same-machine support with other providers or feature fetching off requires 2.1.248. `/list-agents` lists reachable sessions, and `/status` exposes Peer address. A separate session inventory or process count does not prove message reachability.

Local transport uses per-session Unix sockets on macOS/Linux and named pipes on Windows; other-machine/cloud messages travel through Anthropic and depend on Remote Control. Runtime permission and provider egress restrictions remain in effect. `-p` sessions bind an inbox; `--bare` does not. The docs describe hook/socket authentication, but a reusable bridge must not guess an undocumented message envelope, read auth key files, impersonate an own-child sender, or bypass inbound controls. Use native tools unless a complete supported external protocol is verified.

`crossSessionInbound` can accept, hold or refuse messages. Default handling also depends on the two permission-mode classes. Queued/held text is not proof Claude read it; neither a sender success nor a recipient status establishes acknowledgement. Messages are plain text, slash commands arrive literally, permission boundaries remain per-session, and peer messages never count as user consent. Active recipients read between tool calls; idle recipients start a turn. An idle notice subscription can avoid repeated polling, when available and authorised.

[Agent teams](https://code.claude.com/docs/en/agent-teams) are a separate experimental feature enabled with `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`. Teammates share coordination/tasks and can communicate directly. Structured team protocol messages stay within the team. Do not write `~/.claude/teams` inboxes or transcripts to imitate `SendMessage`, and do not turn the feature on just to contact an existing independent session.

Resume/continue/attach bring a conversation or terminal back. They are not equivalent to sending a message, can create competing ownership, and require reconciliation. In this Claude version, background resume can start a copy if the original is already running; preserve the returned ID and do not assume the original was resumed.

## Grok and UI handling

Primary installed vendor references: `~/.grok/docs/user-guide/23-dashboard.md` and `03-keyboard-shortcuts.md`. The dashboard lists top-level sessions in the pager, including inactive records from other pagers; subagents belong to their parent. Selected-agent typed replies queue to busy agents. Some main-agent `Enter` cases cancel a blocked turn, and send-now chords cancel current work. Never guess the active input context.

Cursor primary documentation: [CLI parameters](https://cursor.com/docs/cli/reference/parameters). Installed help is authoritative for newer persist support. Muse's installed help explicitly exposes list/send, but available transport must be proved per run. Keep uncertain/no-leader/closed-ingress cases as blockers instead of inventing a universal CLI bridge.
