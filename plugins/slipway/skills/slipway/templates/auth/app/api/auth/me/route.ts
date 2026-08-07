import { NextResponse } from 'next/server';
import { getSession } from '@/lib/auth-server';

export const runtime = 'nodejs';

export async function GET(): Promise<NextResponse> {
  const session = await getSession();
  if (!session) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  return NextResponse.json({ user: session });
}
