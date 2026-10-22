# Hausarzt Praxis Hilden Nord

Website der Hausarztpraxis von Mohammad Hussein (Hausarzt · Ärztliche Gutachten).
Statische Seite ohne Build-Schritt, in 5 Sprachen: Deutsch, Arabisch (RTL), Ukrainisch, Rumänisch, Englisch.

## Struktur

```
index.html          Startseite (Leistungen, Gutachten, Arzt, Sprechzeiten, FAQ, Kontakt)
impressum.html      Impressum (Pflichtangaben für Ärzte, NRW)
datenschutz.html    Datenschutzerklärung (Muster)
assets/logo.svg     Logo mit Schriftzug
assets/logo-mark.svg  Logo-Symbol / Favicon
css/styles.css      Design
js/config.js        Praxisdaten: Adresse, Telefon, E-Mail, Sprechzeiten, Buchungslink
js/i18n.js          Alle Texte in allen Sprachen
js/main.js          Sprachumschaltung, Sprechzeiten, „Jetzt geöffnet“-Status
```

## Vor der Veröffentlichung anpassen

1. **`js/config.js`**: echte Adresse, Telefon, E-Mail und Sprechzeiten eintragen (alle `TODO`).
   Optional `bookingUrl` (z. B. Doctolib), dann führt „Termin buchen“ dorthin, sonst ruft der Button die Praxis an.
2. **`impressum.html` / `datenschutz.html`**: gelb markierte Platzhalter ersetzen und rechtlich prüfen lassen.
3. **Foto**: Bild als `assets/mohammad-hussein.jpg` ablegen und in `index.html` im Block `doctor-photo`
   das `<span>MH</span>` durch `<img src="assets/mohammad-hussein.jpg" alt="Mohammad Hussein">` ersetzen.

## Lokal ansehen

```
python3 -m http.server 8000
```

Dann <http://localhost:8000> öffnen. Eine Sprache direkt aufrufen: `?lang=ar`, `?lang=uk`, `?lang=ro`, `?lang=en`.

## Datenschutz-Hinweis

Die Seite lädt bewusst keine externen Ressourcen (keine Google Fonts, keine eingebettete Karte, kein Tracking, keine Cookies).
Google Maps wird nur über den Link „Route planen“ geöffnet.
