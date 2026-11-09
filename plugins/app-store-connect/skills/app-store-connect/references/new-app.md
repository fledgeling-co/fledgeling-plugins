# New app: the commands behind each step

`scripts/provision-app.sh` covers the bundle ID, capabilities and app record. This file holds
the manual equivalent of each of those, plus the web-lane pieces the script leaves out. Every
command takes the team's `--profile`; `<p>` below stands for that profile, and `<team>` and
`<apple id>` are the team's `team_id` and `apple_id` from `accounts.json`. Flags were read from asc 6.2.0;
run the command with `--help` when one is rejected.

## Bundle ID and capabilities (API lane)

```bash
asc --profile <p> --read-only bundle-ids list --identifier com.example.app --output json
asc --profile <p> bundle-ids create --identifier com.example.app --name "Example" --platform UNIVERSAL
asc --profile <p> bundle-ids capabilities reconcile plan  --bundle <RESOURCE_ID> --entitlements App.entitlements
asc --profile <p> bundle-ids capabilities reconcile apply --bundle <RESOURCE_ID> --entitlements App.entitlements --confirm
asc --profile <p> bundle-ids capabilities add --bundle <RESOURCE_ID> --capability PUSH_NOTIFICATIONS --if-exists skip
```

`--bundle` takes the resource ID (`ABCDE12345`), never the reverse-DNS identifier. The list
filter can match more than one identifier, so compare `attributes.identifier` exactly.

A capability the public enum lacks fails with `ENTITY_ERROR.ATTRIBUTE.TYPE`. The two
portal-only routes asc offers are `asc web bundle-ids capabilities enable` (currently
`PRIVATE_CLOUD_COMPUTE`) and `asc web bundle-ids capabilities sync-app-clip`. Anything else is
enabled in the Developer Portal by the owner.

## App record (web lane)

```bash
asc --profile <p> --read-only apps list --bundle-id com.example.app --output json
asc --profile <p> web apps create --apple-id <apple id> --name "Example" --bundle-id com.example.app \
  --sku example-ios --platform IOS --primary-locale en-AU --if-exists skip --auto-rename=false
```

The record lands on whichever provider the web session selected, so check
`asc web auth status --apple-id <apple id> --output json` shows the team's `providerId` first.
`--auto-rename` defaults to true, which retries a taken name with a suffix and creates the app
under a name nobody chose; pass `--auto-rename=false` every time. The record binds the bundle ID
permanently and reserves the name, so confirm both with the user first.

## App Groups (web lane, Account Holder or Admin)

```bash
asc --profile <p> web app-groups list --apple-id <apple id> --developer-team <team> --output table
asc --profile <p> web app-groups create --apple-id <apple id> --developer-team <team> \
  --name "Example Shared" --identifier group.com.example.shared --confirm
asc --profile <p> web app-groups assign --apple-id <apple id> --developer-team <team> \
  --group <GROUP_RESOURCE_ID> --bundle-id <BUNDLE_RESOURCE_ID> --confirm
```

The bundle ID needs the `APP_GROUPS` capability before the assignment means anything; the
reconcile above adds it when the entitlements list
`com.apple.security.application-groups`. `asc web app-groups set` replaces a bundle ID's whole
group set, so prefer `assign` when other groups are already attached.

## iCloud containers (web lane, permanent)

```bash
asc --profile <p> web icloud-containers list --apple-id <apple id> --developer-team <team> --output table
asc --profile <p> web icloud-containers create --apple-id <apple id> --developer-team <team> \
  --identifier iCloud.com.example.app --name "Example" --confirm
```

A container can never be deleted and its identifier stays reserved for the team, so confirm the
exact identifier with the user before `--confirm`. asc 6.2.0 has no command that assigns a
container to a bundle ID; after creating one, the owner selects it on the bundle ID's iCloud
capability in the Developer Portal.

## Signing (API lane)

```bash
asc --profile <p> --read-only certificates list --certificate-type DISTRIBUTION --output table
asc --profile <p> profiles create --name "Example App Store" --profile-type IOS_APP_STORE \
  --bundle <BUNDLE_RESOURCE_ID> --certificate <CERT_ID>
```

Profile types include `IOS_APP_STORE`, `IOS_APP_DEVELOPMENT`, `IOS_APP_ADHOC`, `MAC_APP_STORE`,
`MAC_APP_DEVELOPMENT` and `MAC_APP_DIRECT`; `asc schema "POST /v1/profiles"` lists all 14.
Reuse an existing distribution certificate where one is valid. A new one comes from
`asc certificates create --certificate-type DISTRIBUTION --generate-csr --key-out <private path> --csr-out <path>`,
and its private key is then a secret that belongs in a keychain, never in the repo.

## Other identifiers

Merchant IDs (`asc merchant-ids`) and Pass Type IDs (`asc pass-type-ids`) are API-lane. Services
IDs (`asc web service-ids`), Website Push IDs (`asc web website-push-ids`) and Sign in with Apple
keys (`asc web sign-in-keys`) are web-lane. A Website Push ID is for Safari web push, not for
app push notifications.
