import { Module, ValidationPipe } from '@nestjs/common';
import { APP_GUARD, APP_PIPE } from '@nestjs/core';
import { ConfigModule } from '@nestjs/config';
import { ScheduleModule } from '@nestjs/schedule';
import { ThrottlerGuard, ThrottlerModule } from '@nestjs/throttler';
import { HealthController } from './health.controller';

// The platform baseline: global env config, in-process scheduling (a persistent
// process runs its own cron, so no CRON_SECRET endpoints for work it can do
// directly, BP §16), and a default rate limit on every route.
@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }),
    ScheduleModule.forRoot(),
    ThrottlerModule.forRoot([{ ttl: 60_000, limit: 120 }]),
  ],
  controllers: [HealthController],
  providers: [
    { provide: APP_GUARD, useClass: ThrottlerGuard },
    // Registered as APP_PIPE so it can take DI and so every DTO is enforced
    // (CP §2): whitelist strips undeclared fields, forbidNonWhitelisted rejects
    // them, transform materialises typed instances.
    {
      provide: APP_PIPE,
      useFactory: (): ValidationPipe => new ValidationPipe({ whitelist: true, forbidNonWhitelisted: true, transform: true }),
    },
  ],
})
export class AppModule {}
