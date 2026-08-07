import { NextResponse } from 'next/server';
import { rotateRefresh } from '@/lib/auth-server';

export const runtime = 'nodejs';

// BP §9: classify the failure — a 401 here means the session is dead (client
// signs out ONCE); transient/5xx elsewhere must not sign the user out.
export async function POST(): Promise<NextResponse> {
  const session = await rotateRefresh();
  if (!session) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  return NextResponse.json({ ok: true });
}
