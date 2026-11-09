import 'server-only';

// The one sanctioned writer to the console (CP §5). Structured JSON lines, with
// sensitive keys redacted at any depth before anything is written (CP §4 A09):
// never log a token, a cookie, a header bag, a secret or an email address.
type Fields = Record<string, unknown>;
type Level = 'info' | 'warn' | 'error';

const SENSITIVE_KEY = /pass(word)?|secret|token|authorization|cookie|api[-_]?key|jwt|^code$|otp|email|headers/i;
const MAX_DEPTH = 6;

export function redact(value: unknown, depth = 0): unknown {
  if (depth > MAX_DEPTH) return '[truncated]';
  if (value instanceof Error) {
    return { name: value.name, message: value.message, cause: redact(value.cause, depth + 1) };
  }
  if (Array.isArray(value)) return value.map((item) => redact(item, depth + 1));
  if (value !== null && typeof value === 'object') {
    const out: Fields = {};
    for (const [key, item] of Object.entries(value)) {
      out[key] = SENSITIVE_KEY.test(key) ? '[redacted]' : redact(item, depth + 1);
    }
    return out;
  }
  return value;
}

function write(level: Level, fields: Fields, msg: string): void {
  const line = JSON.stringify({ level, msg, time: new Date().toISOString(), ...(redact(fields) as Fields) });
  if (level === 'error') console.error(line);
  else if (level === 'warn') console.warn(line);
  else console.log(line);
}

export const logger = {
  info: (fields: Fields, msg: string): void => write('info', fields, msg),
  warn: (fields: Fields, msg: string): void => write('warn', fields, msg),
  error: (fields: Fields, msg: string): void => write('error', fields, msg),
};
