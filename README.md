# Hausarzt Praxis Hilden Nord

Website der Hausarztpraxis von Mohammad Hussein (Hausarzt · Ärztliche Gutachten).
Statische Seite ohne Build-Schritt, in 5 Sprachen: Deutsch, Arabisch (RTL), Ukrainisch, Rumänisch, Englisch.

Aufbau wie bei deutschen Hausarztpraxen üblich: Startseite, Praxis, Leistungen, Gutachten (Schwerpunkt),
Team, Sprechzeiten, Kontakt, Jobs, Impressum, Datenschutz.

## Seiten

| Datei | Inhalt |
|---|---|
| `index.html` | Startseite: Heute-Status, Wegweiser „Ihr Anliegen“, Leistungen, Sprachen, Kontakt |
| `praxis.html` | Werte, Räume (Fotos), erster Besuch, FAQ, Anfahrt |
| `leistungen.html` | Alle Leistungen im Detail |
| `gutachten.html` | Gutachten-Service: für wen, Ablauf, Unterlagen, Kosten |
| `team.html` | Arzt und Praxisteam |
| `sprechzeiten.html` | Sprechzeiten, Akutsprechstunde, Notdienst, Urlaub |
| `kontakt.html` | Kontakt, Rezepte & Überweisungen bestellen, Anfahrt |
| `karriere.html` | Stellenangebote |
| `impressum.html`, `datenschutz.html` | Rechtliches (nur Deutsch) |

## Vor der Veröffentlichung anpassen

Fast alles steht in **`js/config.js`** (alle `TODO`):

- Adresse, Telefon, E-Mail, optional Fax
- `bookingUrl`: Link zur Online-Buchung (z. B. Doctolib). Leer = „Termin buchen“ ruft die Praxis an.
- `hours` und `acuteHours`: Sprechzeiten und Akutsprechstunde. Daraus berechnet die Seite automatisch
  „Jetzt geöffnet · bis 12:00 Uhr“ bzw. „Wieder geöffnet: Montag ab 08:00 Uhr“.
- `notices`: Praxis-Hinweise (Urlaub, Grippeimpfung …) mit Start- und Enddatum – erscheinen nur in diesem Zeitraum.
- `directions`: Bus & Bahn, Parken, Barrierefreiheit (leer = ausgeblendet).
- `team`: Namen und Rollen des Teams.
- `jobs`: aktive Stellenangebote (`"mfa"`, `"trainee"`), leeres Array = Initiativbewerbung.

Außerdem: `impressum.html` und `datenschutz.html` – gelb markierte Platzhalter ersetzen und rechtlich prüfen lassen.

## Fotos

Fotos als `.jpg` in `assets/photos/` ablegen – sie erscheinen automatisch, bis dahin zeigt die Seite einen
dezenten Platzhalter. Empfohlen: Querformat 1600 × 1000 px, Porträts 800 × 1000 px, je unter 300 KB.

| Dateiname | Wo | Format |
|---|---|---|
| `praxis-team.jpg` | Startseite „Willkommen“ | quer |
| `gutachten.jpg` | Gutachten-Seite oben | quer |
| `praxis-empfang.jpg` | Praxis → Räume | quer |
| `praxis-wartebereich.jpg` | Praxis → Räume | quer |
| `praxis-behandlungsraum.jpg` | Praxis → Räume | quer |
| `praxis-labor.jpg` | Praxis → Räume | quer |
| `team-mohammad-hussein.jpg` | Team → Arzt | hoch |
| `team-2.jpg`, `team-3.jpg`, `team-4.jpg` | Team → Praxisteam (Namen in `config.js`) | hoch |

Eigenes Logo: `assets/logo-mark.svg` (Symbol, auch Favicon) und `assets/logo.svg` (mit Schriftzug) ersetzen.

## Texte und Sprachen

Alle Texte liegen in `js/lang/de.js`, `en.js`, `ar.js`, `uk.js`, `ro.js` – gleiche Schlüssel in jeder Datei.
Deutsch steht zusätzlich direkt im HTML (für Suchmaschinen und ohne JavaScript).
Eine andere Sprache direkt aufrufen: `?lang=ar`, `?lang=uk`, `?lang=ro`, `?lang=en`.

Farben: alle im `:root`-Block am Anfang von `css/styles.css`.

## Lokal ansehen

```
python3 -m http.server 8000
```

Dann <http://localhost:8000> öffnen.

## Datenschutz

Die Seite lädt keine externen Ressourcen (keine Google Fonts, keine eingebettete Karte, kein Tracking, keine Cookies).
Google Maps öffnet sich nur über den Link „Route planen“. Kein Kontaktformular – Anfragen laufen per Telefon oder E-Mail.
