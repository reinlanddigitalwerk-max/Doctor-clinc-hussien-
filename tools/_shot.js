const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  for (const [w,h,n] of [[390,844,'m'],[1440,900,'d']]) {
    const p = await b.newPage({ viewport: { width: w, height: h }, reducedMotion: 'reduce' });
    await p.goto('http://localhost:8765/index.html?lang=' + (process.argv[2]||'de'), { waitUntil: 'networkidle' });
    await p.screenshot({ path: '/tmp/claude-0/-home-user-Doctor-clinc-hussien-/e6e2b86d-a63a-5b7d-b788-16fac2f925ac/scratchpad/home-' + n + '.png', clip: { x: 0, y: 0, width: w, height: n=='m'?1700:1300 } });
    await p.close();
  }
  await b.close();
})();
