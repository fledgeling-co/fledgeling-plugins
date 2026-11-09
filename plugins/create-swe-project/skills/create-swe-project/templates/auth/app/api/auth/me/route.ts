import { NextResponse } from 'next/server';
import { getSession } from '@/lib/auth-server';
import { jsonError } from '@/lib/http';

export const runtime = 'nodejs';

export async function GET(): Promise<Response> {
  const session = await getSession();
  if (!session) return jsonError('Unauthorized', 401);
  return NextResponse.json({ user: { email: session.email } });
}
