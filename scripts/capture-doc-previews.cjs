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
      const page = await browser.newPage({ viewport: { width: 1120, height: 820 }, deviceScaleFactor: 1, reducedMotion: "no-preference" });
      const errors = [];
      page.on('pageerror', error => errors.push(error.message));
      page.on('requestfailed', request => errors.push(`${request.url()}: ${request.failure()?.errorText}`));
      page.on('request', request => {
        if (/^https?:/.test(request.url())) errors.push(`Nonlocal preview request: ${request.url()}`);
      });
      try {
        const url = pathToFileURL(path.join(previewDirectory, name)).href;
        await page.goto(url);
        await page.waitForFunction(() => window.previewStatus?.ready);
        if (await page.locator('.frame').count()) {
          if (await page.locator('#play').getAttribute('aria-pressed') !== 'true') errors.push('Live indicators did not start automatically');
          const before = await page.locator('.frame').first().textContent();
          await page.waitForFunction(previous => document.querySelector('.frame')?.textContent !== previous, before);
        }
        if (slug === 'spinner') {
          await page.emulateMedia({ reducedMotion: 'reduce' });
          await page.waitForFunction(() => window.previewStatus.animationPaused);
          await page.emulateMedia({ reducedMotion: 'no-preference' });
        }
        await page.goto(url + '?capture=1');
        await page.waitForFunction(() => window.previewStatus?.ready);
        if (!(await page.evaluate(() => window.previewStatus.animationPaused))) errors.push('Capture mode did not freeze the first frame');
        await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
        await page.locator('main').screenshot({ path: path.join(captureDirectory, `${slug}.png`) });
        const wide = await page.evaluate(() => ({ width: document.documentElement.scrollWidth, viewport: innerWidth }));
        if (wide.width > wide.viewport) errors.push('Horizontal clipping at normal width');
        if (slug === 'table' || slug === 'structure') {
          const tables = await page.locator('[data-table]').count();
          if (tables !== (slug === 'table' ? 2 : 1)) errors.push('Missing table fixture');
          const rules = await page.evaluate(() => [...document.querySelectorAll('[data-table]')].map(table => {
            const rule = table.querySelector('[data-table-header-rule]');
            const lines = [...table.children];
            const glyphs = rule?.textContent || '';
            const expected = parseInt(table.style.width, 10);
            return !!rule && lines[1] === rule && /^─+$/.test(glyphs) && glyphs.length === expected
              && getComputedStyle(rule.firstElementChild).color === getComputedStyle(lines[0].firstElementChild).color;
          }));
          if (rules.some(valid => !valid)) errors.push('Table header rule must follow headers, span the table and use subtext');
        }
        if (slug === 'section' || slug === 'structure') {
          const layoutErrors = await page.evaluate(() => {
            const issues = [];
            const gap = (before, after) => after.getBoundingClientRect().top - before.getBoundingClientRect().bottom;
            const close = (a, b) => Math.abs(a - b) < 1;
            for (const section of document.querySelectorAll('section.block')) {
              const heading = section.firstElementChild;
              const rule = heading.nextElementSibling;
              const lineHeight = parseFloat(getComputedStyle(heading).lineHeight);
              if (!close(gap(heading, rule), 0)) issues.push('Section heading must touch its rule');
              for (const subsection of section.querySelectorAll(':scope > .indent > section.block')) {
                const preceding = subsection.previousElementSibling || rule;
                if (!close(gap(preceding, subsection), lineHeight)) issues.push('Subsection needs exactly one preceding blank line');
              }
              const following = section.nextElementSibling;
              if (following && !close(gap(section, following), lineHeight)) issues.push('Completed section needs exactly one following blank line');
            }
            // Probe a first-child subsection and adjacent subsections as well as the visible specimen.
            const probe = document.createElement('section');
            probe.className = 'block';
            probe.innerHTML = '<div class="line">Parent</div><div class="line">Rule</div><div class="indent"><section class="block"><div class="line">First</div></section><section class="block"><div class="line">Second</div></section></div>';
            document.querySelector('.screen').append(probe);
            const [heading, rule, body] = probe.children;
            const [first, second] = body.children;
            const lineHeight = parseFloat(getComputedStyle(heading).lineHeight);
            if (!close(gap(rule, first), lineHeight)) issues.push('First-child subsection needs one blank after parent rule');
            if (!close(gap(first, second), lineHeight)) issues.push('Adjacent subsection margins must collapse to one blank');
            probe.remove();
            return issues;
          });
          errors.push(...layoutErrors);
        }
        const initialPreset = await page.locator('.screen').getAttribute('data-preset');
        if (initialPreset !== 'catppuccin-mocha') errors.push('Initial fixture must use Catppuccin Mocha');
        if (slug === 'structure') {
          const choices = await page.locator('#theme-preset option').evaluateAll(options => options.map(o => o.value));
          if (choices.length !== 10) errors.push('Combined example must expose all ten built-in profiles');
          for (const preset of choices) {
            await page.selectOption('#theme-preset', preset);
            const consistent = await page.evaluate(() => {
              const screen = document.querySelector('.screen');
              const preset = window.documentaryThemes[screen.dataset.preset];
              const expected = document.createElement('span');
              expected.style.color = preset.tokens['text.foreground'];
              expected.style.backgroundColor = preset['reference-background'];
              document.body.append(expected);
              const a = getComputedStyle(screen), b = getComputedStyle(expected);
              const matches = a.color === b.color && a.backgroundColor === b.backgroundColor;
              expected.remove();
              return matches;
            });
            if (!consistent) errors.push(`Preset did not update foreground and backdrop: ${preset}`);
          }
          await page.selectOption('#theme-preset', 'catppuccin-mocha');
        } else if (await page.locator('#theme-preset').count()) {
          errors.push('Individual component previews must not expose a theme selector');
        }
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
        if (await page.locator('#play').count()) {
          await page.locator('#play').click();
          if (await page.locator('.frame').count()) {
            const before = await page.locator('.frame').first().textContent();
            await page.waitForFunction(previous => document.querySelector('.frame')?.textContent !== previous, before);
          }
          await page.locator('#play').click();
          const frozen = await page.locator('.frame').first().textContent();
          await page.waitForTimeout(220);
          if (await page.locator('.frame').first().textContent() !== frozen) errors.push('Pause did not freeze the indicator');
        }
        if (await page.locator('#update').count()) {
          const before = await page.locator('.screen').textContent();
          await page.locator('#update').click();
          const after = await page.locator('.screen').textContent();
          if (before === after) errors.push('Update did not change displayed content');
        }
        if (await page.locator('#remove').count()) {
          if (slug === 'structure') await page.locator('#play').click();
          await page.locator('#remove').click();
          if (slug === 'structure') {
            const before = await page.locator('.frame').first().textContent();
            await page.waitForFunction(previous => document.querySelector('.frame')?.textContent !== previous, before);
          }
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
