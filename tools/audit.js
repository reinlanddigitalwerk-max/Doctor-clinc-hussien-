const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
  const out = process.argv[2];
  const pages = (process.argv[3] || 'index,praxis,leistungen,gutachten,team,sprechzeiten,kontakt,karriere').split(',');
  const errs = [];
  for (const [w, h, tag] of [[1440, 900, 'd'], [390, 844, 'm']]) {
    const ctx = await b.newContext({ viewport: { width: w, height: h }, reducedMotion: 'reduce' });
    for (const pg of pages) {
      const p = await ctx.newPage();
      p.on('pageerror', e => errs.push(pg + ': ' + e.message));
      await p.goto(`http://localhost:8765/${pg}.html?lang=${process.argv[4] || 'de'}`, { waitUntil: 'networkidle' });
      await p.waitForTimeout(300);
      const sw = await p.evaluate(() => document.documentElement.scrollWidth);
      if (sw > w) errs.push(`${pg} ${tag} overflow ${sw}`);
      await p.screenshot({ path: `${out}/${pg}-${tag}.png`, fullPage: true });
      await p.close();
    }
  }
  console.log('errors', errs);
  await b.close();
})();
