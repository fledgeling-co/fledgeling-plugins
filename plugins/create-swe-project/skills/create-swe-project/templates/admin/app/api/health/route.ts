import { NextResponse } from 'next/server';

export const runtime = 'nodejs';

// Health + warm target for the vercel.json cron (BP §16: a persistent surface
// without a health check can deploy "green" while broken).
export function GET(): NextResponse {
  return NextResponse.json({ ok: true, ts: new Date().toISOString() });
}
