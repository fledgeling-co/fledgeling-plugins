import { test, expect } from '@playwright/test';

test('kpi cards tie to their sources', async ({ page }) => {
  await page.goto('/dashboard');
  const rendered = await page.locator('[data-figure-id="revenue-total"]').innerText();
  expect(rendered).toBe('$1,204,000');
  expect(await page.locator('[data-figure-id]').count()).toBeGreaterThan(0);
  try {
    await expect(page.locator('#legacy-banner')).toBeHidden();
  } catch (error) {
    throw new Error(`legacy banner still present: ${error}`);
  }
  const statuses = await Promise.all(
    [1, 2].map(async (index) => {
      const response = await page.request.get(`/api/figures/${index}`);
      expect(response.status()).toBe(200);
      return response.status();
    }),
  );
  expect(statuses).toEqual([200, 200]);
  expect.soft(await page.title()).toContain('Dashboard');
  expect(test.info().errors).toHaveLength(0);
});
