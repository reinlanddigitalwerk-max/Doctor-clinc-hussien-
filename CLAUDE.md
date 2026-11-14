# Hausarztpraxis Hilden Nord – Website

Statische Website (HTML/CSS/JS, kein Build-Server, keine Datenbank, keine Logins), ausgeliefert über
GitHub Pages vom Branch `claude/intelligent-babbage-6ilkwr` unter www.hausarztpraxishildennord.de.
Seiten werden aus `tools/pages_content.py` erzeugt (`python3 tools/build_pages.py`), Texte in `js/lang/*.js`
(7 Sprachen), Praxisdaten in `js/config.js`. Details: `README.md`, `tools/README.md`.

## Sicherheitsregeln

1. Keine Schlüssel, Tokens oder Passwörter in Code, Git oder Logs. Die Seite braucht keine; kommt ein Dienst
   mit Schlüssel dazu, gehört er auf einen Server, nie ins Frontend.
2. Keine Nutzereingaben oder URL-Parameter ungeprüft ins HTML: Texte mit `textContent` (Helfer `el()`),
   `innerHTML`/`outerHTML` nur mit eigenen Texten aus `js/lang` und `js/config.js`. URL-Parameter nur gegen
   feste Listen (`lang` ∈ LANGS, `palette` 1–6).
3. Content-Security-Policy (in `tools/build_pages.py`, Konstante `CSP`) nicht lockern: keine Inline-Skripte,
   keine `style="…"`-Attribute (stattdessen Klassen), neue externe Dienste nur gezielt freigeben und im
   Datenschutz eintragen. Nach jeder Änderung alle Seiten auf CSP-Verstöße prüfen.
4. Externe Links mit `target="_blank"` immer mit `rel="noopener"`.
5. Keine Drittanbieter-Inhalte ohne Einwilligung laden (Google Maps erst nach Klick). Schriften bleiben selbst gehostet.
6. Keine Daten löschen oder überschreiben, ohne vorher nachzusehen; keine erzwungenen Pushes, keine Änderung der
   Git-Historie auf dem Veröffentlichungs-Branch.
7. Sicherheits- und Zugangseinstellungen (GitHub, Domain/DNS bei united-domains, medatixx, Cloud-Umgebung)
   nicht ändern – nur Empfehlungen geben; der Inhaber entscheidet.
8. Vor jedem Push: `node tools/check.js`, `node tools/rules_audit.js`, `node tools/motion_test.js` und der
   CSP-Test; die Seite muss in allen 7 Sprachen fehlerfrei laden.
9. Zusammenfassungen für den Inhaber kurz, auf Arabisch (syrischer Dialekt), ohne unnötige Fachbegriffe.
