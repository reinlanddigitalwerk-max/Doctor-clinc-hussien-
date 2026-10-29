import json, re, shutil, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
# Usage: python3 tools/prep_preview.py <output-dir>  (outside the repo, e.g. a scratch folder)
PV = pathlib.Path(sys.argv[1]).resolve() / "preview"
shutil.rmtree(PV, ignore_errors=True); PV.mkdir(parents=True)
files = {}
def cp(rel):
    (PV / rel).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(ROOT / rel, PV / rel)
    if rel != "index.html":
        files[rel] = rel
for p in ["css/styles.css", "js/app.js", "js/config.js"] + [f"js/lang/{c}.js" for c in "de en ar uk ro".split()]:
    cp(p)
for p in sorted(ROOT.glob("assets/fonts/*.woff2")):
    cp(str(p.relative_to(ROOT)))
for p in ["assets/logo-praxis.svg", "assets/logo-mono.png", "assets/favicon-32.png", "assets/apple-touch-icon.png",
          "assets/logo-3d/emblem-spin.webp", "assets/logo-3d/emblem-spin-poster.webp"]:
    cp(p)
for p in sorted(ROOT.glob("*.html")):
    if p.name != "index.html":
        cp(p.name)
# index.html as fragment: no html/head/body skeleton, page id via window.PRAXIS_PAGE
html = (ROOT / "index.html").read_text()
head = re.search(r"<head>\n(.*?)\n</head>", html, re.S).group(1)
head = re.sub(r"\s*<meta (charset|name=\"viewport\")[^>]*>", "", head).strip()
body = re.search(r"<body[^>]*>\n(.*?)\n</body>", html, re.S).group(1)
(PV / "index.html").write_text(head + '\n<script>window.PRAXIS_PAGE = "home"; window.PRAXIS_TITLE = "page.home";</script>\n' + body + "\n")
for gone in ["assets/logo.svg", "assets/logo-mark.svg"] + [f"assets/logo-3d/emblem-p{i}.webp" for i in range(1, 6)]:
    files[gone] = None
(PV.parent / "preview_files.json").write_text(json.dumps(files, indent=0))
print(len(files), "files")
