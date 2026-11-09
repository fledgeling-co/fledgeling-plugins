import { CONNECT_SRC } from './csp-origins';

/**
 * The per-request Content-Security-Policy (CP §6.7, BP §12). Scripts are nonce +
 * 'strict-dynamic' with no 'unsafe-inline'. Styles keep 'unsafe-inline' for now:
 * a nonce does not cover React `style` attributes, and CP §6.7's posture is
 * nonce scripts first, styles as a follow-up after loading the page under a
 * stricter policy. 'unsafe-eval' is development-only (React's debug stacks).
 */
export function buildCsp(nonce: string, opts: { dev: boolean; https: boolean }): string {
  const directives = [
    "default-src 'self'",
    `script-src 'self' 'nonce-${nonce}' 'strict-dynamic'${opts.dev ? " 'unsafe-eval'" : ''}`,
    "style-src 'self' 'unsafe-inline'",
    "img-src 'self' blob: data:",
    "font-src 'self'",
    `connect-src 'self' ${CONNECT_SRC.join(' ')}`.trim(),
    "object-src 'none'",
    "base-uri 'self'",
    "form-action 'self'",
    "frame-ancestors 'none'",
  ];
  // Only meaningful on an HTTPS page; on plain-http local origins it would
  // rewrite same-origin asset URLs to https and break them.
  if (opts.https) directives.push('upgrade-insecure-requests');
  return directives.join('; ');
}
