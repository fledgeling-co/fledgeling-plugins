# Deploy log

Hand-kept. Fly.io deploys on push to `main`; this file records what was
set on the machine, which the deploy does not.

| Date | What |
|---|---|
| 2026-05-02 | First deploy. `DATABASE_URL` set. |
| 2026-05-19 | `SESSION_SECRET` rotated. |
| 2026-06-28 | `recurringInvoices` flag switched **off** in `config/production.json` after the Ardent Studio duplicate run. |
| 2026-07-04 | Last entry. |

`POSTMARK_TOKEN` has never been set on Fly. It is in `.env.example` and
it is set locally. Nobody has checked the live secret list since the
first deploy, and I do not have access to it.
