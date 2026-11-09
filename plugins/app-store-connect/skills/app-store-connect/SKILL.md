---
name: app-store-connect
description: >-
  Drive App Store Connect and the Apple Developer Portal from the terminal with the Rork `asc` CLI, for the Apple teams recorded in a private accounts file on the machine. Says which credential every call uses and where it lives (API keys in the system keychain behind asc profiles, Apple Account web sessions with SMS two-factor codes read from Messages, Warden for the rest), and provisions a new app through a bundled script that plans before it writes: bundle ID, capabilities reconciled from an entitlements file (push included), and the App Store Connect app record. Covers App Groups, iCloud containers and signing profiles as commands, and the one piece Apple keeps manual, the APNs push key, which a team creates once and every app reuses. Use when someone asks to create a bundle ID or App ID, register a new app in App Store Connect, enable push notifications or another capability, create an App Group or iCloud container, make a provisioning profile or certificate, create an App Store Connect API key, upload a build, or do anything else in App Store Connect from the terminal. Not for compiling or archiving the binary itself.
---

# App Store Connect

`asc` (Rork, 6.2.0 when this was written) reaches Apple through two lanes, and the lane decides
the credential:

- **The API-key lane** signs a JWT with an App Store Connect API key. It needs no human and
  covers bundle IDs, capabilities, certificates, profiles, devices, builds, TestFlight,
  versions, metadata and review submission.
- **The web-session lane** (`asc web …`) signs in as an Apple Account and needs a two-factor
  code. It covers what Apple's public API refuses: creating app records, App Groups, iCloud
  containers, Services IDs, Sign in with Apple keys and API keys themselves.

`asc capabilities --status web-session --output table` lists every web-lane workflow.

## Step 1: Read the accounts file

This skill is public and names no account. The machine carries two private files in
`~/.config/app-store-connect/` (or `$ASC_ACCOUNTS_DIR`): `accounts.json`, which maps each team
to its asc profile, team ID and web-session Apple Account, and `accounts.md`, which records the
rest (key IDs, which profile is the asc default, roles, Warden entry names, existing
certificates and push keys). Read both before the first command of a session.

When they are missing, build them from the live accounts as `references/accounts-file.md`
describes, and ask the owner only for what asc cannot show.

## Step 2: Name the team on every command

Pass `--profile <team's profile>` on every `asc` call, including `asc web` calls. asc falls back
to its default profile (named in `accounts.json` as `default_profile`) when a command names
none, so a command about another team's app reads or writes the default team instead, and
nothing errors. `asc web apps create` is the easy one to get wrong: it creates the app through
the web session but checks and creates the bundle ID through the API profile.

Add `--read-only` to anything exploratory. asc refuses every POST, PATCH, PUT and DELETE before
sending it, so a discovery command cannot change an account.

When asc refuses because something else set a guard (`ASC_READ_ONLY`, `ASC_WEB_NO_AUTO_LOGIN`,
`ASC_WEB_DONT_STORE_PASSWORD`), report the refusal and the command you would have run, and leave
the variable alone. Whoever set it decided this session should not write or sign in, and
`env -u` around it overrides that decision without asking them.

`asc auth status` lists the stored profiles; `asc auth doctor` reports whether each private key
is present and valid.

## Step 3: Find the command rather than recalling it

asc 6.2.0 has 85 top-level commands and its flags change between releases, so read them from
the installed binary:

```bash
asc search "create an app group" --output json     # ranked commands with summaries
asc web app-groups create --help                   # exact flags for the version installed
asc schema "POST /v1/bundleIdCapabilities"         # API field names and allowed values
```

asc prints JSON to stdout and warnings such as `showing 1 of 21 results` to stderr. Keep stderr
out of anything that parses the JSON, and pass `--paginate` when a list must be complete. Any
flag value accepts `@env:NAME` or `@file:PATH`, which keeps a secret off the command line.

## Step 4: Know where each credential lives

| Credential | Where it lives | How it is used |
| --- | --- | --- |
| App Store Connect API key | system keychain, one asc profile per team | automatically, through `--profile` |
| Apple Account web password | keychain item, service `asc-web-password`, written by asc after one interactive sign-in | read by asc during sign-in |
| Two-factor code | SMS forwarded from the iPhone into Messages | `asc web auth messages-code` reads it |
| APNs key, key IDs, other team secrets | Warden, under the names `accounts.md` lists | `warden_get_key` with a reason, only when a task needs the value |

Private keys never go into a repo, a config file, an `env` block or a shell export that a hook
or subagent inherits. To add or rotate an API key: create it with
`asc --profile <p> web api-keys create --name "<name>" --output-dir <private dir>` (team keys
only, Admin or Account Holder, and the `.p8` downloads exactly once), register it with
`asc auth login --name <profile> --key-id <id> --issuer-id <issuer> --private-key <path>`, run
`asc auth doctor`, then delete the `.p8` file. Warden has no write tool, so a secret that
belongs in Warden is added by the owner in the Warden app, with the key ID and team ID in its
name.

## Step 5: Sign in a web session only when a web-lane command needs one

Check first; most web commands also sign in again on their own when a cached session expires:

```bash
asc web auth status --apple-id <apple_id> --output json   # authenticated, providerId
```

A web session is bound to one App Store Connect provider, and an Apple Account on several teams
has several. Select it with the team's `provider_id` from `accounts.json`, Apple's numeric
App Store Connect ID. It is not the Developer Portal team ID: passing the team ID to
`--public-provider-id` fails with "did not match any available providers", and that error is
also the quickest way to list an account's real provider IDs. Developer Portal commands
(`app-groups`, `icloud-containers`, `service-ids`, `sign-in-keys`) select the team separately,
with `--developer-team <team_id>`.

To sign in without a person, ask Apple to text the code and read it from Messages:

```bash
asc web auth login --apple-id <apple_id> --provider-id <provider_id> \
  --two-factor-method sms \
  --two-factor-code-command "asc web auth messages-code --timeout 50s"
```

Then confirm `asc web auth status` reports `"authenticated": true` and the expected
`providerId` before any web command runs.

This has two prerequisites: the app running asc needs Full Disk Access so `messages-code` can
read `chat.db`, and the iPhone must forward SMS to this Mac (Settings → Messages → Text Message
Forwarding). Measured on 2026-11-09: with forwarding off, Apple's text never reached Messages
at all; with it on, two sign-ins read the code and finished within ten seconds. When the code
step times out, check for the text itself before blaming the reader:

```bash
/usr/bin/sqlite3 -readonly ~/Library/Messages/chat.db "SELECT datetime(m.date/1000000000+978307200,'unixepoch','localtime') FROM message m JOIN handle h ON h.ROWID=m.handle_id WHERE h.id='Apple' ORDER BY m.date DESC LIMIT 3;"
```

No recent row means the text never arrived, which is forwarding, not asc. When unattended
sign-in is not available, or the account has no stored password yet, the owner signs in once
by typing this into the prompt:

```bash
! asc web auth login --apple-id <apple_id> --provider-id <provider_id> --two-factor-method sms
```

The session is cached and later commands reuse it until Apple expires it. That first interactive
sign-in also stores the account's password for later unattended ones. asc's help also describes
entering a wrong trusted-device code to make Apple fall back to SMS; `--two-factor-method sms`
asks for the text up front, so that workaround is never needed here.

Make one sign-in attempt per task. When it fails, report the error and stop rather than
retrying: repeated failures lock the Apple Account (service error -20209, after which asc pauses
automatic sign-in for an hour and the owner unlocks it at iforgot.apple.com), and each attempt
texts the owner's phone.

Driving the Developer Portal in Chrome with a password from Warden does not avoid any of this.
The browser meets the same two-factor step, the password is already in the keychain through
asc, and the portal's markup is the least stable surface of the three. asc cannot reuse a
browser's Apple session either, so leave the owner's browser alone while signing in: no
AppleScript, DevTools protocol or tab-reading to look for one. `asc web auth status` is the
session check. Chrome is the route for the APNs key alone (Step 7).

## Step 6: Provision a new app

Run the bundled script. It plans by default, with every asc call read-only, and writes only with
`--apply`:

```bash
scripts/provision-app.sh --team <key from accounts.json> --identifier com.example.app --name "Example" \
  --entitlements path/to/Example.entitlements --app-record --sku example-ios
```

In order, it confirms the asc profile reaches the team ID the accounts file gives (exit 3 if
not), finds or creates the bundle ID, reconciles capabilities from the entitlements file (adds
and updates, preserves settings such as broadcast push, and lists capabilities it does not
manage), adds any `--capability TYPE` given, and with `--app-record` creates the App Store
Connect app record with `--if-exists skip --auto-rename=false`, so a re-run is safe and a taken
name fails rather than producing a renamed app. Each write is read back and reported with its
resource ID.

Run the plan first and show it. When the user has asked for the setup, apply the reversible
part without asking again: a bundle ID can be deleted and a capability removed, so
`--apply` without `--app-record` is covered by the request. Stop before the permanent part and
end the reply with a direct question that names the exact identifier and name, because an app
record permanently binds its bundle ID and reserves its name on the App Store. For example:
"Create the App Store Connect record Tally for app.fledgeling.tally? That can't be undone." On a
yes, re-run with `--app-record --apply`.

Capability names follow Apple's enum, not the Xcode labels: Sign in with Apple is
`APPLE_ID_AUTH`, push is `PUSH_NOTIFICATIONS`. A capability outside the public enum shows as
`unmanaged` in the reconcile plan and is enabled in the portal instead.

The pieces the script leaves to direct commands, all on the web lane, are in
`references/new-app.md`: App Groups, iCloud containers, provisioning profiles, and a manual
equivalent of every script step. An iCloud container can never be deleted, so its identifier is
confirmed with the user before `--confirm`.

## Step 7: Push notifications need a capability and a team key

The capability is the API-lane part, and Step 6 handles it whenever the entitlements carry
`aps-environment` or `--capability PUSH_NOTIFICATIONS` is passed.

The APNs authentication key (`.p8`) cannot be created by any API or by asc. Apple's
App Store Connect API has no key resource for it, its certificate types include no APNs type
(asc 6.2.0 accepts 18, none for push), and asc's private-portal key commands cover Sign in with
Apple keys only. So treat the key as a team asset, not an app asset:

- **A team-scoped key signs pushes for every bundle ID on the team**, so a new app needs no new
  key. Apple's current guidance restricts a new team-scoped key to Sandbox or Production and
  recommends one per environment; keys made before 17 February 2025 that cover both keep
  working. Some push providers still ask for a single key valid in both, so check what the
  provider accepts before choosing.
- **Each environment holds at most two team-scoped keys**, so check before creating one.
  `accounts.md` records where each team's existing keys are known to live, including keys
  uploaded to a push provider and never stored locally.
- **Topic-specific keys** cover up to 400 bundle IDs in one environment. Create them only when a
  key must be handed to a party that should reach those apps alone.

Sources and the one point still held loosely are in `references/evidence.md`.

Creating a key is an owner action at
`https://developer.apple.com/account/resources/authkeys/add`, or, with the owner signed in to
the DevTools Chrome, a Chrome DevTools MCP session the agent drives through the same page. The
`.p8` downloads once. The owner then stores it in Warden as `<Team>: APNs key (team-scoped)`,
with the key ID and team ID in the entry, adds that entry name to `accounts.md`, and every
backend or push service reads it from Warden.

## Constraints

- Confirm with the user before any command that creates something permanent or consumes a
  one-time download: `asc web apps create`, `asc web icloud-containers create`,
  `asc web api-keys create`, `asc web sign-in-keys create`, and `provision-app.sh --app-record --apply`.
- Confirm before anything carrying `--confirm` that deletes, revokes or unassigns: bundle IDs,
  certificates, profiles, App Groups, Services IDs.
- When a task includes a permanent step (an app record, an iCloud container, a one-time key
  download), say in the reply that it cannot be undone, even when an earlier step stopped the
  run before it. The user decides the next go-ahead with that fact in hand.
- Report each created resource by the ID asc read back, never by the command having exited 0.
- After provisioning, reply with one table row per resource touched: resource, identifier,
  resource ID as read back, and whether it was created, already existed, or was only planned.
- Reuse a team's existing distribution certificate where `accounts.md` records one, rather than
  creating another.
- Keep account details out of anything committed: team IDs, key IDs, Apple Account emails and
  Warden entry names belong in the accounts files, not in a repo, a commit message or a PR.
