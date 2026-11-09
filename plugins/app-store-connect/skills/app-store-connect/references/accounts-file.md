# The accounts file

The skill is public and names no account. Everything account-specific lives on the machine, in
two files under `~/.config/app-store-connect/` (directory mode 700):

| File | Read by | Holds |
| --- | --- | --- |
| `accounts.json` | `scripts/provision-app.sh` and the runner | per team: asc profile, team ID, the Apple Account for web sessions |
| `accounts.md` | the runner, before the first command | everything else worth knowing: key IDs, which profile asc defaults to, role per Apple Account, Warden entry names, existing certificates and push keys, bundle ID prefixes |

Neither file holds a secret. Private keys stay in the system keychain under asc's profiles, and
web passwords stay in the keychain item asc writes. Set `ASC_ACCOUNTS_DIR` to read the files from
somewhere else.

## `accounts.json`

```json
{
  "default_profile": "acme",
  "teams": {
    "acme": {
      "name": "Acme Pty Ltd",
      "profile": "acme",
      "team_id": "ABCDE12345",
      "apple_id": "admin@acme.example"
    }
  }
}
```

The key under `teams` is what `provision-app.sh --team` takes. `default_profile` records which
profile `asc` uses when a command names none, because a command about another team's app that
forgets `--profile` lands on that default team without an error. `apple_id` is the account that
holds Account Holder or Admin on that team; a Developer-role account cannot create apps, App
Groups, iCloud containers or API keys.

## Building it from the live accounts

When the files are missing, build them from what asc already knows rather than asking:

```bash
asc auth status                                                        # profiles; which is default
asc --read-only --profile <p> bundle-ids list --limit 1 --output json  # attributes.seedId = team ID
asc --read-only --profile <p> users list --paginate --output table     # Apple Accounts and roles
asc web auth status --apple-id <apple id>                              # whether asc stored its password
```

Ask the owner only for what those cannot show: which team a profile is meant for when the names
do not say, and which Apple Account to use where two hold Admin.
