# CLAUDE.md — internal-dashboard

## Deployment

This app deploys to **Vercel**, region **syd1**. The Vercel project is
`internal-dashboard`; it is not a monorepo and the app lives at the repo root.

Deploys require the git author to be `luke@rhodes.gg`. Any other author is
rejected by the org policy and the Vercel CLI reports the blocked state as
UNKNOWN, so a stalled deploy usually means the author is wrong rather than the
build failing.

## Package manager

pnpm. Do not use npm or yarn here; the lockfile is pnpm's.
