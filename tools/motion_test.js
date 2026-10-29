const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: process.env.CHROMIUM || '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell' });
  const errs = [];
  for (const [pg, lang, w] of [['index','de',1440],['leistungen','ar',390],['gutachten','uk',1024]]) {
    const p = await b.newPage({ viewport: { width: w, height: 860 } });
    p.on('pageerror', e => errs.push(pg + ': ' + e.message));
    await p.goto(`http://localhost:8765/${pg}.html?lang=${lang}`, { waitUntil: 'networkidle' });
    const hidden0 = await p.evaluate(() => document.querySelectorAll('.reveal').length);
    const shadow0 = await p.evaluate(() => document.querySelector('.site-header').classList.contains('is-scrolled'));
    for (let y = 0; y < 12000; y += 400) { await p.mouse.wheel(0, 400); await p.waitForTimeout(60); }
    await p.waitForTimeout(1200);
    const r = await p.evaluate(() => ({
      left: document.querySelectorAll('.reveal').length,
      invisible: [...document.querySelectorAll('main *')].filter(e => getComputedStyle(e).opacity === '0').length,
      shadow: document.querySelector('.site-header').classList.contains('is-scrolled'),
    }));
    // contrast: text elements vs their effective background
    const low = await p.evaluate(() => {
      const parse = c => (c.match(/[\d.]+/g) || []).map(Number);
      const lum = ([r, g, bb]) => { const f = v => (v /= 255) <= .03928 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4; return .2126 * f(r) + .7152 * f(g) + .0722 * f(bb); };
      const bg = el => { for (let e = el; e; e = e.parentElement) { const c = parse(getComputedStyle(e).backgroundColor); if (c.length >= 3 && (c[3] === undefined || c[3] > .5)) return c; } return [255,255,255]; };
      const out = [];
      document.querySelectorAll('body *').forEach(el => {
        const own = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
        if (!own || !el.offsetParent) return;
        const cs = getComputedStyle(el); const fg = parse(cs.color);
        const L1 = lum(fg), L2 = lum(bg(el)); const ratio = (Math.max(L1, L2) + .05) / (Math.min(L1, L2) + .05);
        const large = parseFloat(cs.fontSize) >= 24 || (parseFloat(cs.fontSize) >= 18.6 && +cs.fontWeight >= 700);
        if (ratio < (large ? 3 : 4.5)) out.push(ratio.toFixed(2) + ' ' + el.tagName + '.' + el.className + ' "' + el.textContent.trim().slice(0, 30) + '"');
      });
      return [...new Set(out)].slice(0, 15);
    });
    console.log(pg, lang, w, 'revealed', hidden0, 'left', r.left, 'opacity0', r.invisible, 'shadow', shadow0, '->', r.shadow);
    if (low.length) console.log('  low contrast:', low);
    await p.close();
  }
  console.log('errors', errs);
  await b.close();
})();
