import { NextResponse, type NextRequest } from 'next/server';
import { clearSession } from '@/lib/auth-server';
import { isAllowedOrigin, jsonError } from '@/lib/http';

export const runtime = 'nodejs';

export async function POST(req: NextRequest): Promise<Response> {
  if (!isAllowedOrigin(req)) return jsonError('Forbidden', 403);
  await clearSession();
  return NextResponse.json({ ok: true });
}
