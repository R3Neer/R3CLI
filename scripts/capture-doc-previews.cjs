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
        if (slug === 'separator') {
          const actual = await page.evaluate(() => {
            const rule = document.querySelector('.rule');
            const text = rule.firstElementChild;
            const context = document.createElement('canvas').getContext('2d');
            context.font = getComputedStyle(text).font;
            rule.dataset.pattern = '=-';
            rule.style.width = `${context.measureText('M').width * 15}px`;
            fitRules();
            return text.textContent;
          });
          if (actual !== '=-=-=-=-=-=-=-=') errors.push(`Separator discarded a partial final cycle: ${JSON.stringify(actual)}`);
        }
        if (slug === 'tab-leader') {
          const probe = async (label, width, pattern, expected) => {
            await page.locator('#leader-label').fill(label);
            await page.locator('#leader-width').fill(String(width));
            await page.locator('#leader-pattern').fill(pattern);
            const actual = await page.locator('[data-leader] .leader-fill').first().textContent();
            if (actual !== expected) errors.push(`TabLeader(${JSON.stringify(label)}, ${width}, ${JSON.stringify(pattern)}): expected ${JSON.stringify(expected)}, received ${JSON.stringify(actual)}`);
          };
          await probe('Project', 14, '', '       ');
          await probe('Project', 14, '.', '.......');
          await probe('Files', 14, '.', '.........');
          await probe('Note', 13, '_-\\_', '_-\\__-\\__');
          await probe('Name', 5, '界-', ' ');
          await probe('Project (local)', 14, '.', ' ');
          await probe('Name', 0, '.', ' ');
          await page.evaluate(() => {
            const owner = document.querySelector('[data-leader]');
            owner.querySelector('.leader-prefix').innerHTML = '<span>Pro</span><span>ject</span>';
            owner.dataset.width = '14';
            owner.dataset.pattern = '.';
            fitLeaders();
          });
          const multiple = await page.locator('[data-leader] .leader-fill').first().textContent();
          if (multiple !== '.......') errors.push('TabLeader did not measure the whole segmented prefix');
          await page.locator('#reset').click();
          const reset = await page.locator('[data-leader] .leader-fill').first().textContent();
          if (reset !== '.......') errors.push('TabLeader reset did not restore the fixture');
        }
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
