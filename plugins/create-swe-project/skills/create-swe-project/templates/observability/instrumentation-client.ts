import * as Sentry from '@sentry/nextjs';

// No DSN → disabled: the module ships wired but inert until SENTRY_DSN is set
// (dAIolog pattern: observability from day one, spend when you opt in).
Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  enabled: Boolean(process.env.NEXT_PUBLIC_SENTRY_DSN),
  tracesSampleRate: 0.1,
});

export const onRouterTransitionStart = Sentry.captureRouterTransitionStart;
