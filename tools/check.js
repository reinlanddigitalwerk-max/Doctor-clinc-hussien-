// Validates that every key used in the site exists in de.js, and every language has all de keys.
const fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..');
global.window = { I18N: {} };
for (const f of fs.readdirSync(path.join(ROOT, 'js/lang'))) require(path.join(ROOT, 'js/lang', f));
const de = window.I18N.de;
const html = fs.readdirSync(ROOT).filter(f => f.endsWith('.html')).map(f => fs.readFileSync(path.join(ROOT, f), 'utf8')).join('');
const app = fs.readFileSync(path.join(ROOT, 'js/app.js'), 'utf8');
const used = new Set([...html.matchAll(/data-i18n="([\w.]+)"/g)].map(m => m[1]).concat([...html.matchAll(/data-(?:title|subject)="([\w.]+)"/g)].map(m => m[1]), [...app.matchAll(/(?:i18n|t)\(?["':\s]+([a-z]+\.[\w.]+)["']/gi)].map(m => m[1])));
const missing = [...used].filter(k => !de[k] && !/^(day|dayShort|role|job)\.$/.test(k));
console.log('used keys:', used.size, 'missing in de:', missing);
for (const [code, d] of Object.entries(window.I18N)) {
  const miss = Object.keys(de).filter(k => d[k] == null);
  console.log(code, Object.keys(d).length, 'missing:', miss.length ? miss : 'none');
}
