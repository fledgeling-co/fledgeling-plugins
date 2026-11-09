import { NextResponse } from 'next/server';

export const runtime = 'nodejs';
// A cron target, so its ceiling is explicit (CP §6.12).
export const maxDuration = 10;

// Health + warm target for the vercel.json cron (BP §16: a persistent surface
// without a health check can deploy "green" while broken). It reports liveness
// only; detailed health stays out of production (CP §4 A02).
export function GET(): Response {
  return NextResponse.json({ ok: true, ts: new Date().toISOString() });
}
