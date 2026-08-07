import { Controller, Get } from '@nestjs/common';

// A health endpoint from day one: a persistent server with no HTTP health check
// can deploy "green" while crash-looping (BP §15/§16).
@Controller('health')
export class HealthController {
  @Get()
  health(): { ok: true; ts: string } {
    return { ok: true, ts: new Date().toISOString() };
  }
}
