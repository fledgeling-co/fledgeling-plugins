Rate limiting is live on the public routes, in-memory, at 100 requests per minute per API key.

`api/middleware/rate-limit.ts` implements the limiter with an in-memory Map keyed by the `X-API-Key` header, falling back to the socket address. `api/routes/public.ts` mounts it ahead of auth. `pnpm test api/middleware` reported 12 passed, 0 failed. I did not run the full test suite.

Open: the limiter is per-process, so with N instances the effective limit is N x 100. The Redis store you mentioned in passing would resolve that, so I placed the storage layer behind an interface for a future drop-in implementation. `api/routes/admin.ts` also has no rate limiting; I left it untouched since the task was scoped to the public routes.
