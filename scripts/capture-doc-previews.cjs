// Browser verification of documentation fixtures; never imports or runs R3CLI.
// Requires an existing Playwright installation and an installed Chromium.
const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');

function option(name, fallback) {
  const index = process.argv.indexOf(name);
  if (index < 0) return fallback;
  if (!process.argv[index + 1] || process.argv[index + 1].startsWith('--')) {
    throw new Error(`Missing value for ${name}`);
  }
  return process.argv[index + 1];
}

async function main() {
  const root = path.resolve(option('--root', path.join(__dirname, '..')));
  const playwright = require(option('--playwright-module', 'playwright'));
  const executablePath = option('--browser-executable', undefined);
  const report = option('--report', undefined);
  const previewDirectory = path.join(root, 'docs/assets/previews');
  const captureDirectory = path.join(root, 'docs/assets/captures');
  const pages = fs.readdirSync(previewDirectory).filter(name => name.endsWith('.html')).sort();
  const browser = await playwright.chromium.launch({ headless: true, ...(executablePath ? { executablePath } : {}) });
  const results = [];
  try {
    for (const name of pages) {
      const slug = path.basename(name, '.html');
      const page = await browser.newPage({ viewport: { width: 1120, height: 820 }, deviceScaleFactor: 1 });
      const errors = [];
      page.on('pageerror', error => errors.push(error.message));
      page.on('requestfailed', request => errors.push(`${request.url()}: ${request.failure()?.errorText}`));
      page.on('request', request => {
        if (/^https?:/.test(request.url())) errors.push(`Nonlocal preview request: ${request.url()}`);
      });
      try {
        await page.goto(pathToFileURL(path.join(previewDirectory, name)).href);
        await page.waitForFunction(() => window.previewStatus?.ready);
        await page.locator('main').screenshot({ path: path.join(captureDirectory, `${slug}.png`) });
        const wide = await page.evaluate(() => ({ width: document.documentElement.scrollWidth, viewport: innerWidth }));
        if (wide.width > wide.viewport) errors.push('Horizontal clipping at normal width');
        if (await page.locator('#update').count()) {
          const before = await page.locator('.screen').textContent();
          await page.locator('#update').click();
          const after = await page.locator('.screen').textContent();
          if (before === after) errors.push('Update did not change displayed content');
        }
        if (await page.locator('#play').count()) {
          await page.locator('#play').click();
          if (await page.locator('.frame').count()) {
            const before = await page.locator('.frame').first().textContent();
            await page.waitForFunction(previous => document.querySelector('.frame')?.textContent !== previous, before);
          }
          await page.locator('#play').click();
        }
        if (await page.locator('#remove').count()) {
          await page.locator('#remove').click();
          if (await page.locator('#view-region').count()) {
            const remaining = await page.locator('#view-region').textContent();
            if (remaining.trim()) errors.push('Remove left view content visible');
          }
        }
        await page.locator('#reset').click();
        await page.setViewportSize({ width: 360, height: 780 });
        await page.waitForFunction(() => document.documentElement.scrollWidth <= innerWidth);
        const narrow = await page.evaluate(() => ({ width: document.documentElement.scrollWidth, viewport: innerWidth }));
        results.push({ slug, wide, narrow, errors });
      } catch (error) {
        results.push({ slug, errors: [...errors, error.message] });
      } finally {
        await page.close();
      }
    }
  } finally {
    await browser.close();
  }
  const failed = results.filter(result => result.errors.length);
  if (report) fs.writeFileSync(path.resolve(report), JSON.stringify(results, null, 2) + '\n');
  console.log(JSON.stringify({ checked: results.length, failed }, null, 2));
  if (failed.length) process.exitCode = 1;
}

main().catch(error => { console.error(error.message); process.exitCode = 1; });
