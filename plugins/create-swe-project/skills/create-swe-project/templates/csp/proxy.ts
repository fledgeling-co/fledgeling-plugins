import { NextResponse, type NextRequest } from 'next/server';
import { buildCsp } from '@/lib/csp';

// Next 16 proxy (formerly middleware). It mints a fresh nonce per request and
// puts the CSP on BOTH the forwarded request and the response, as Next's CSP
// guide and CP §6.7 prescribe (Next reads the nonce from the request it
// renders). What actually breaks the nonce is a page rendered at build time,
// which is why the root layout awaits headers() and the @smoke e2e checks a
// production build. Proxy coverage is defence in depth; route handlers still
// check auth themselves (CP §3).
export function proxy(request: NextRequest): NextResponse {
  const nonce = Buffer.from(crypto.randomUUID()).toString('base64');
  const forwardedProto = request.headers.get('x-forwarded-proto');
  const https = forwardedProto ? forwardedProto === 'https' : request.nextUrl.protocol === 'https:';
  const csp = buildCsp(nonce, { dev: process.env.NODE_ENV === 'development', https });

  const requestHeaders = new Headers(request.headers);
  requestHeaders.set('x-nonce', nonce);
  requestHeaders.set('Content-Security-Policy', csp);
  const response = NextResponse.next({ request: { headers: requestHeaders } });
  response.headers.set('Content-Security-Policy', csp);
  return response;
}

export const config = {
  matcher: [
    {
      source: '/((?!api|_next/static|_next/image|favicon.ico).*)',
      missing: [
        { type: 'header', key: 'next-router-prefetch' },
        { type: 'header', key: 'purpose', value: 'prefetch' },
      ],
    },
  ],
};
