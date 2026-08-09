import type { NextConfig } from "next";

/**
 * Baseline security headers, matching apps/website in fledgeling-app.
 *
 * The Content-Security-Policy is set per-request in `proxy.ts` instead, because a
 * strict script-src needs a nonce and a nonce can't be a static header.
 */
const securityHeaders = [
  {
    key: "Strict-Transport-Security",
    value: "max-age=63072000; includeSubDomains; preload",
  },
  { key: "X-Content-Type-Options", value: "nosniff" },
  { key: "X-Frame-Options", value: "DENY" },
  { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
  {
    key: "Permissions-Policy",
    value: "camera=(), microphone=(), geolocation=(), browsing-topics=()",
  },
  { key: "X-DNS-Prefetch-Control", value: "on" },
];

const nextConfig: NextConfig = {
  output: "standalone",
  reactStrictMode: true,
  poweredByHeader: false,
  // Deliberately no `outputFileTracingRoot`. The build reads ../plugins, but
  // only in the prebuild step — the app itself imports a generated JSON and
  // touches nothing outside site/ at runtime. Pointing the tracing root at the
  // repo relocates next-server.js.nft.json, and Vercel's onBuildComplete then
  // fails on a file it cannot find, after an otherwise clean build.
  async headers() {
    return [{ source: "/:path*", headers: securityHeaders }];
  },
};

export default nextConfig;
