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
  // The indexer reads ../plugins and ../.claude-plugin at build time. Trace that
  // so `output: standalone` doesn't prune files the build genuinely touched.
  outputFileTracingRoot: new URL("..", import.meta.url).pathname,
  async headers() {
    return [{ source: "/:path*", headers: securityHeaders }];
  },
};

export default nextConfig;
