// External origins the browser talks to directly, kept in one list so the CSP
// can't drift from what the app actually loads (CP §6.7). @vercel/blob's client
// upload() PUTs bytes to blob.vercel-storage.com; without it in connect-src the
// upload fails as a bare "Failed to fetch". Add an origin here in the same
// change that adds the integration.
export const CONNECT_SRC: readonly string[] = ['https://blob.vercel-storage.com'];
