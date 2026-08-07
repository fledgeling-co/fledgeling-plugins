import { NextResponse } from 'next/server';
import { clearSession } from '@/lib/auth-server';

export const runtime = 'nodejs';

export async function POST(): Promise<NextResponse> {
  await clearSession();
  return NextResponse.json({ ok: true });
}
