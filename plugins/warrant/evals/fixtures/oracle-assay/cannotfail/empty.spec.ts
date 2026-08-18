import { test } from '@playwright/test';

test('the dashboard loads', async ({ page }) => {
  await page.goto('/dashboard');
  await page.waitForLoadState('networkidle');
});
