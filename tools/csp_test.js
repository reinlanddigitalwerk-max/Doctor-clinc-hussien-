// Lädt alle Seiten in allen Sprachen und meldet Verstöße gegen die Content-Security-Policy.
// Prüft außerdem, dass die Richtlinie aktiv ist (eingeschleustes Inline-Skript wird blockiert).
// Aufruf: node tools/csp_test.js  (lokaler Server: python3 -m http.server 8765)
const { chromium } = require('playwright');
const BASE = 'http://localhost:8765/';
const PAGES = ['index', 'praxis', 'leistungen', 'gutachten', 'team', 'sprechzeiten', 'kontakt', 'karriere', 'impressum', 'datenschutz'];
const LANGS = ['de', 'ar', 'uk', 'ro', 'en', 'tr', 'ru'];
(async () => {
  const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
  const viol = new Set(), errs = new Set(); let runs = 0;
  for (const l of LANGS) for (const pg of PAGES) {
    const ctx = await b.newContext({ viewport: { width: 1440, height: 900 } });
    await ctx.addInitScript(() => { window.__v = []; document.addEventListener('securitypolicyviolation', e => window.__v.push(e.violatedDirective + ' ' + (e.blockedURI || 'inline'))); });
    const p = await ctx.newPage(); p.on('pageerror', e => errs.add(pg + '/' + l + ' ' + e.message));
    await p.goto(BASE + pg + '.html?lang=' + l, { waitUntil: 'networkidle' });
    await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) { scrollTo(0, y); await new Promise(r => setTimeout(r, 30)); } });
    if (pg === 'kontakt' && l === 'de') { await p.click('.js-map-load'); await p.waitForTimeout(500); }
    (await p.evaluate(() => window.__v)).forEach(v => viol.add(pg + '/' + l + ': ' + v));
    runs++; await ctx.close();
  }
  const p = await b.newPage(); await p.goto(BASE + 'index.html', { waitUntil: 'networkidle' });
  const active = await p.evaluate(async () => { window.__ran = false; const s = document.createElement('script'); s.textContent = 'window.__ran = true'; document.body.appendChild(s); await new Promise(r => setTimeout(r, 200)); return !window.__ran; });
  console.log('pages loaded:', runs, '| CSP active:', active, '| violations:', viol.size ? [...viol] : 'none', '| errors:', errs.size ? [...errs] : 'none');
  await b.close();
  if (viol.size || errs.size || !active) process.exit(1);
})();
