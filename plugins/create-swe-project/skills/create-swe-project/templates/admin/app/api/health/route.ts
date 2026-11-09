import { NextResponse } from 'next/server';

export const runtime = 'nodejs';
export const maxDuration = 10;

// Liveness for the vercel.json warm cron (BP §16); no detail in production (CP §4 A02).
export function GET(): Response {
  return NextResponse.json({ ok: true, ts: new Date().toISOString() });
}
