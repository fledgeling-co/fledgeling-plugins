import 'server-only';
import { appEnv } from './env';

/**
 * Outside production, outbound email and push reach only addresses whose domain
 * is on OUTBOUND_ALLOWED_DOMAINS (BP §24): a staging or local run must never
 * email a real customer. An empty list outside production means nobody. The
 * decision is the server's, from its own runtime environment.
 */
export function canReceiveOutbound(email: string): boolean {
  if (appEnv() === 'production') return true;
  const domain = email.slice(email.lastIndexOf('@') + 1).toLowerCase();
  const allowed = (process.env.OUTBOUND_ALLOWED_DOMAINS ?? '')
    .split(',')
    .map((d) => d.trim().toLowerCase())
    .filter(Boolean);
  return allowed.includes(domain);
}
