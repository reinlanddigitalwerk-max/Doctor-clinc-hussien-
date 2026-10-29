const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
  const pages = 'index,praxis,leistungen,gutachten,team,sprechzeiten,kontakt,karriere'.split(',');
  for (const [w, h, lang] of [[390, 844, 'uk'], [1440, 900, 'de']]) {
    const small = new Set(), tiny = new Set(), wraps = new Set(), cls = {}, obscured = new Set();
    for (const pg of pages) {
      const ctx = await b.newContext({ viewport: { width: w, height: h }, reducedMotion: 'reduce' });
      await ctx.addInitScript(() => { window.__cls = 0; new PerformanceObserver(l => l.getEntries().forEach(e => { if (!e.hadRecentInput) window.__cls += e.value; })).observe({ type: 'layout-shift', buffered: true }); });
      const p = await ctx.newPage();
      await p.goto(`http://localhost:8765/${pg}.html?lang=${lang}`, { waitUntil: 'networkidle' });
      await p.waitForTimeout(500);
      cls[pg] = +(await p.evaluate(() => window.__cls)).toFixed(3);
      const r = await p.evaluate((w) => {
        const out = { small: [], tiny: [], wraps: [] };
        document.querySelectorAll('a, button, [role=menuitemradio]').forEach(el => {
          const rc = el.getBoundingClientRect(); if (!rc.width || !el.offsetParent) return;
          const label = (el.textContent.trim() || el.getAttribute('aria-label') || el.className).slice(0, 28);
          const inline = getComputedStyle(el).display === 'inline' && el.closest('p, li, dd');
          if ((rc.height < 24 || rc.width < 24) && !inline) out.small.push(`${label} ${Math.round(rc.width)}x${Math.round(rc.height)}`);
        });
        document.querySelectorAll('body *').forEach(el => {
          const own = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()); if (!own || !el.offsetParent) return;
          const fs = parseFloat(getComputedStyle(el).fontSize); if (fs < 14) out.tiny.push(`${fs}px ${el.tagName}.${el.className} "${el.textContent.trim().slice(0, 20)}"`);
        });
        document.querySelectorAll('.status, .notice-label, .status-chip, .chip, .chips li, .eyebrow, .btn').forEach(el => {
          if (!el.offsetParent) return; const lh = parseFloat(getComputedStyle(el).lineHeight) || 20;
          if (el.getBoundingClientRect().height > lh * 1.8 + 24 && !el.matches('.eyebrow')) out.wraps.push(`${el.className} "${el.textContent.trim().slice(0, 30)}"`);
        });
        return out;
      }, w);
      r.small.forEach(x => small.add(x)); r.tiny.forEach(x => tiny.add(x)); r.wraps.forEach(x => wraps.add(pg + ': ' + x));
      // focus not obscured: tab through 40 stops
      const header = await p.evaluate(() => document.querySelector('.site-header').getBoundingClientRect().height);
      for (let i = 0; i < 45; i++) {
        await p.keyboard.press('Tab');
        const f = await p.evaluate((hh) => { const el = document.activeElement; if (!el || el === document.body) return null; const rc = el.getBoundingClientRect(); const ab = document.querySelector('.action-bar'); const abTop = ab && getComputedStyle(ab).display !== 'none' ? ab.getBoundingClientRect().top : innerHeight;
          if (el.closest('.site-header, .action-bar, .skip-link')) return null; return (rc.bottom <= hh + 2 || rc.top >= abTop - 2) ? (el.textContent.trim() || el.className).slice(0, 30) + ` top=${Math.round(rc.top)}` : null; }, header);
        if (f) obscured.add(pg + ': ' + f);
      }
      await ctx.close();
    }
    console.log(`\n=== ${w}px ${lang}`);
    console.log('CLS', cls);
    console.log('targets <24px:', [...small].slice(0, 20));
    console.log('text <14px:', [...tiny].slice(0, 25));
    console.log('chips/buttons wrapping:', [...wraps].slice(0, 15));
    console.log('focus obscured:', [...obscured].slice(0, 15));
  }
  await b.close();
})();
