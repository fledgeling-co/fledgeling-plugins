# Evidence

Where each rule in `SKILL.md` comes from. `[measured]` is a command run on 2026-11-09 against
asc 6.2.0 and the live accounts; `[asc]` is asc's own help text, quoted; `[Apple]` and
`[research]` point into `docs/deep-research/` in this plugin; `[owner]` is an answer the owner
gave during the build.

| Rule | Source |
| --- | --- |
| Two lanes, and which workflows need a web session | `[asc]` `asc capabilities`: app creation, App Groups, iCloud containers, Services IDs, Sign in with Apple keys and API keys are `web-session`; "creating app records is not exposed as a public REST operation" |
| Account details live in a private file, not the skill | `[owner]` asked whether the public plugin should carry team IDs, key IDs, Apple Accounts and Warden names; chose "Keep them local" |
| Name the team on every command | `[measured]` `asc auth status` marks one profile `isDefault: true`; an unqualified command resolves to it with no warning |
| `asc web apps create` needs `--profile` too | `[asc]` "If official ASC API authentication is available, the CLI will check or create the Bundle ID before app creation" |
| The Apple Account can differ per team | `[measured]` `asc users list` showed one owner account as DEVELOPER on one team and ACCOUNT_HOLDER on the other; `[asc]` App Groups "require a user-owned Apple web session with Account Holder or Admin access" |
| `--read-only` for discovery | `[asc]` "Refuse every mutating request (POST/PATCH/PUT/DELETE) before it is sent"; `[measured]` `ASC_READ_ONLY=1 … bundle-ids create` answered `refusing POST /v1/bundleIds` |
| Read flags from the binary, keep stderr out of JSON | `[measured]` `asc --help` lists 85 top-level commands; `bundle-ids list --limit 1` writes `Warning: showing 1 of 21 results` beside its JSON |
| Unattended sign-in needs Full Disk Access and SMS forwarding | `[asc]` `messages-code` setup notes; `[measured]` `messages-code` read `chat.db` without a permission error, and a real sign-in printed `Verification code sent to +61 …` with no code reaching Messages in 50 s or 4 min |
| One sign-in attempt, then stop | `[asc]` "after Apple reports the account locked for security reasons (403, service error -20209), other web commands pause automatic sign-in for 1 hour" |
| Chrome plus Warden does not beat asc for sign-in | `[measured]` asc already stores the web password in the keychain (`asc web auth status` → `passwordStored: true`); the browser meets the same two-factor step |
| Leave a guard variable set by someone else alone | `[measured]` iteration 1 of `evals/`: a run without this skill met `ASC_READ_ONLY=1`, ran `env -u ASC_READ_ONLY asc … bundle-ids create`, and created a real bundle ID on the owner's account |
| Leave the owner's browser alone while signing in | `[measured]` iteration 1: a run with this skill used AppleScript to read the owner's Chrome tab URLs looking for an Apple session, which asc cannot reuse |
| Apply reversible writes on request; ask before permanent ones | `[measured]` iteration 1: with "set up whatever Apple needs", both runs treated the request as covering the bundle ID and capabilities; the owner's standing rule reserves confirmation for irreversible actions |
| Plan by default, `--apply` to write | Inference from the two permanent effects below, and from the owner's standing rule that irreversible actions are confirmed first |
| `--auto-rename=false` on app creation | `[asc]` `--auto-rename` "Retry with unique name suffix if app name is already taken (default: true)" |
| An app record binds its bundle ID and reserves the name | `[asc]` `--if-exists skip` refuses when "the bundle ID or SKU belongs to a different app"; widely documented App Store behaviour, not re-measured here |
| An iCloud container is permanent; asc cannot attach one | `[asc]` "iCloud containers can never be deleted"; `[measured]` `asc web icloud-containers` offers only `list` and `create` |
| Capability enum names (`APPLE_ID_AUTH`, `PUSH_NOTIFICATIONS`, `APP_GROUPS`) | `[measured]` an invalid `--capability` returned Apple's enum list; `reconcile plan` mapped `com.apple.developer.applesignin` → `APPLE_ID_AUTH` and `com.apple.security.application-groups` → `APP_GROUPS` |
| The script stops when a profile reaches the wrong team | `[measured]` a deliberately wrong `team_id` in the accounts file exited 3 with `lists bundle IDs under team …, not …` |
| No API creates an APNs key | `[research]` `2026-11-09-apns-key-automation.md`; `[measured]` `asc certificates create` accepts 18 types, none for APNs, and `asc search "apns key"` finds none |
| One team key serves every app; topic keys are per environment; two team keys per environment | `[Apple]` `2026-11-09-apns-key-scope-addendum.md`, quoting "Establishing a token-based connection to APNs" |

## Held loosely

- Whether the portal still offers a new team-scoped key valid in both environments. Apple's page
  describes new team-scoped keys as single-environment and recommends that; OneSignal's guide
  still tells users to pick "Sandbox & Production". Recorded in the addendum.
- How long an asc web session lasts before Apple expires it. Not measured.
