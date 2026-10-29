# Werkzeuge

Hilfsskripte zum Erzeugen und Prüfen der Seite. Die Website selbst braucht sie nicht.

| Datei | Zweck | Aufruf |
|---|---|---|
| `build_pages.py` + `pages_content.py` | Erzeugt alle HTML-Seiten aus kurzen Vorlagen. `{{key}}` → Text aus `js/lang/de.js` mit `data-i18n`, `[[icon:name]]` → SVG-Symbol. **HTML-Seiten nie direkt bearbeiten, sondern hier.** | `python3 tools/build_pages.py` |
| `legal_impressum.html`, `legal_datenschutz.html` | Inhalt von Impressum und Datenschutz (nur Deutsch), wird von `build_pages.py` eingesetzt | – |
| `check.js` | Prüft, dass alle verwendeten Textschlüssel in allen 5 Sprachen existieren | `node tools/check.js` |
| `audit.js` | Ganzseiten-Screenshots Desktop (1440) und Handy (390) | `node tools/audit.js <ausgabe-ordner> [seiten] [sprache]` |
| `motion_test.js` | Prüft Einblenden beim Scrollen, Kopf-Schatten, Kontrast | `node tools/motion_test.js` |
| `rules_audit.js` | Prüft Regeln aus `ui-ux-pro-max`: Zielgröße ≥ 24 px, Text < 14 px, umbrechende Chips, Fokus unter festem Kopf, CLS | `node tools/rules_audit.js` |
| `spin_test.js` | Prüft das drehende 3D-Logo und „Bewegung reduzieren“ | `node tools/spin_test.js <ausgabe-ordner>` |
| `prep_preview.py` | Baut eine Kopie für die Artifact-Vorschau (index.html ohne Grundgerüst) | `python3 tools/prep_preview.py <ordner-außerhalb-des-repos>` |
| `logo_trace.py` | Vektorisiert das Praxislogo (vtracer) | siehe Kopf der Datei |

Die Browser-Tests brauchen einen lokalen Server im Repository-Ordner (`python3 -m http.server 8765`) und Playwright.
Chromium-Pfad: Umgebungsvariable `CHROMIUM`, sonst `/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell`.

Das 3D-Logo (Blender) liegt mit seinen Skripten in `assets/logo-3d/` (`praxis3d.py`, `assemble.py`).
