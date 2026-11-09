import 'server-only';
import { appEnv } from './env';

/** True only on a development runtime with DEV_LOGIN_ENABLED=true, decided on the server (BP §24). */
export function devLoginEnabled(): boolean {
  return appEnv() === 'development' && process.env.DEV_LOGIN_ENABLED === 'true';
}
