"""Generates the static pages of the practice site from short body templates.

{{key}} is replaced by the German text of that key wrapped with data-i18n, so the
German page works without JavaScript and every text stays translatable.
"""
import json, re, subprocess, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
DE = json.loads(subprocess.check_output(
    ["node", "-e", "global.window={};require(process.argv[1]);process.stdout.write(JSON.stringify(window.I18N.de))",
     str(ROOT / "js/lang/de.js")]))

ICON = {
  "stetho": '<path d="M4.8 2.3A.3.3 0 1 0 5 2H4a2 2 0 0 0-2 2v5a6 6 0 0 0 6 6 6 6 0 0 0 6-6V4a2 2 0 0 0-2-2h-1a.2.2 0 1 0 .3.3"/><path d="M8 15v1a6 6 0 0 0 6 6 6 6 0 0 0 6-6v-4"/><circle cx="20" cy="10" r="2"/>',
  "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/><path d="m9 12 2 2 4-4"/>',
  "syringe": '<path d="m18 2 4 4M17 7l3-3M19 9 8.7 19.3a2.4 2.4 0 0 1-3.4 0l-.6-.6a2.4 2.4 0 0 1 0-3.4L15 5M9 11l4 4M5 19l-3 3M14 4l6 6"/>',
  "flask": '<path d="M9 2v6l-5 9a3 3 0 0 0 2.6 5h10.8A3 3 0 0 0 20 17l-5-9V2M8 2h8M7 15h10"/>',
  "pulse": '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>',
  "doc": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
  "clipboard": '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M9 3v2h6V3M9 12h6M12 9v6"/>',
  "home": '<path d="M3 10.5 12 3l9 7.5M5 9v11a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V9"/><path d="M12 11v6M9 14h6"/>',
  "euro": '<path d="M18 7a7 7 0 1 0 0 10M4 10h10M4 14h10"/>',
  "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
  "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M16 3v4M8 3v4M3 10h18"/>',
  "pill": '<path d="m10.5 20.5 10-10a4.95 4.95 0 1 0-7-7l-10 10a4.95 4.95 0 1 0 7 7ZM8.5 8.5l7 7"/>',
  "alert": '<path d="M12 3 2 20h20L12 3Z"/><path d="M12 10v4M12 17h.01"/>',
  "heart": '<path d="M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7Z"/>',
  "chat": '<path d="M21 12a8 8 0 0 1-11.8 7L3 21l2-6.2A8 8 0 1 1 21 12Z"/>',
  "award": '<circle cx="12" cy="8" r="6"/><path d="M8.2 13.1 7 22l5-3 5 3-1.2-8.9"/>',
  "building": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 22v-4h6v4M8 6h.01M16 6h.01M12 6h.01M12 10h.01M12 14h.01M16 10h.01M16 14h.01M8 10h.01M8 14h.01"/>',
  "briefcase": '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
  "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
  "globe": '<path d="M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18Zm-9-9h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3Z"/>',
  "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2Z"/>',
  "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
  "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
}

def icon(name):
    return f'<span class="icon" aria-hidden="true"><svg viewBox="0 0 24 24">{ICON[name]}</svg></span>'

def tr(m):
    key, spec = m.group(1), m.group(2) or "span"
    if key not in DE:
        sys.exit(f"missing key {key}")
    tag, _, cls = spec.partition(".")
    cls_attr = f' class="{cls.replace(".", " ")}"' if cls else ""
    return f'<{tag}{cls_attr} data-i18n="{key}">{escape(DE[key])}</{tag}>'

def escape(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def fill(body):
    # {{key}} → <span data-i18n>, {{key|h2}} → <h2 data-i18n>
    body = re.sub(r"\{\{([\w.]+)(?:\|([\w.-]+))?\}\}", tr, body)
    # German fallback for elements written as data-i18n="key">x<
    body = re.sub(r'data-i18n="([\w.]+)">x<', lambda m: f'data-i18n="{m.group(1)}">{escape(DE[m.group(1)])}<', body)
    body = re.sub(r"\[\[icon:(\w+)\]\]", lambda m: icon(m.group(1)), body)
    return body

SKELETON = """<!doctype html>
<html lang="de" dir="ltr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} – Hausarztpraxis Hilden Nord</title>
  <meta name="description" data-i18n-attr="content:meta.description" content="{description}">
  <meta name="theme-color" content="#124A87">{robots}
  <link rel="icon" href="assets/favicon-32.png" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
  <link rel="preload" href="assets/fonts/source-sans-3-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="assets/fonts/source-sans-3-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="css/styles.css">
  <script src="js/config.js"></script>
  <script src="js/lang/de.js"></script>
</head>
<body data-page="{page}"{data_title}>
  <div id="site-header"></div>
  <script src="js/app.js"></script>

  <main id="main">
{body}
  </main>

  <div id="site-footer"></div>
</body>
</html>
"""

def page_hero(title_key, lead_key, crumb_key, extra=""):
    return f"""    <section class="page-hero">
      <div class="container">
        <nav class="breadcrumb" aria-label="Breadcrumb"><a href="index.html">{{{{nav.home}}}}</a><span aria-hidden="true">/</span>{{{{{crumb_key}}}}}</nav>
        {{{{{title_key}|h1}}}}
        {{{{{lead_key}|p.lead}}}}{extra}
      </div>
    </section>"""

def write(filename, page, title_key, body, robots=False):
    html = SKELETON.format(
        title=escape(DE[title_key]) if title_key else page.capitalize(),
        description=escape(DE["meta.description"]),
        robots='\n  <meta name="robots" content="noindex">' if robots else "",
        page=page,
        data_title=f' data-title="{title_key}"' if title_key else "",
        body=fill(body).rstrip(),
    )
    (ROOT / filename).write_text(html)
    print("wrote", filename)

pages = __import__("pages_content")
for spec in pages.PAGES(page_hero):
    write(*spec)

# Legal pages: keep their German content, move them onto the shared layout.
for name in ("impressum", "datenschutz"):
    src = (pathlib.Path(__file__).parent / f"legal_{name}.html")
    if not src.exists():
        html = (ROOT / f"{name}.html").read_text()
        inner = re.search(r'<div class="container narrow">\n(.*?)\n    </div>\n  </main>', html, re.S).group(1)
        src.write_text(inner)
    inner = src.read_text()
    body = f'    <section class="legal">\n      <div class="container narrow">\n{inner}\n      </div>\n    </section>'
    write(f"{name}.html", name, None, body, robots=True)
