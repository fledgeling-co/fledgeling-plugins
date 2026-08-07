import { HealthController } from '../src/health.controller';

describe('HealthController', () => {
  it('reports ok with a timestamp', () => {
    const res = new HealthController().health();
    expect(res.ok).toBe(true);
    expect(new Date(res.ts).getTime()).toBeGreaterThan(0);
  });
});
