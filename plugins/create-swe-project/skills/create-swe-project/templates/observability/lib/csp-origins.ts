// External origins the browser talks to directly (CP §6.7). @vercel/blob's
// client upload() PUTs to blob.vercel-storage.com; the Sentry browser SDK posts
// events to its regional ingest hosts. Add an origin in the same change that
// adds the integration, or the CSP blocks it silently.
export const CONNECT_SRC: readonly string[] = [
  'https://blob.vercel-storage.com',
  'https://*.ingest.sentry.io',
  'https://*.ingest.us.sentry.io',
  'https://*.ingest.de.sentry.io',
];
