// Praxisdaten – hier anpassen. Alle Seiten lesen aus diesem Objekt.
// Werte mit "TODO" sind Platzhalter und müssen vor der Veröffentlichung ersetzt werden.
window.PRAXIS = {
  name: "Hausarztpraxis Hilden Nord",
  doctor: "Wahbeh Mohammad Hussein",
  specialty: "Hausarzt – Internistische Diagnostik",
  website: "www.hausarztpraxishildennord.de",

  street: "Gustav-Mahler-Str. 1",
  city: "40724 Hilden",
  phone: "02103 3375590",
  fax: "02103 9083251",             // leer = ausgeblendet
  whatsapp: "02103 9083252",        // leer = ausgeblendet
  email: "info@hausarztpraxishildennord.de",

  // Nur für Vorschauen: zeigt unten links die Leiste zum Umschalten der Farbpaletten.
  previewPalettes: false,

  // Online-Terminbuchung (z. B. Doctolib-Link). Leer = Button ruft die Praxis an.
  bookingUrl: "",

  // Erst auf true setzen, wenn "hours" und "acuteHours" die echten Zeiten enthalten. Bis dahin zeigt die Seite
  // keine Zeiten und keinen „Geöffnet/Geschlossen“-Status, sondern bittet um einen Anruf.
  hoursConfirmed: false,

  // Sprechzeiten (TODO: echte Zeiten eintragen). Leeres Array = geschlossen.
  hours: {
    mon: ["08:00–12:00", "15:00–18:00"],
    tue: ["08:00–12:00", "15:00–18:00"],
    wed: ["08:00–12:00"],
    thu: ["08:00–12:00", "15:00–18:00"],
    fri: ["08:00–12:00"],
    sat: [],
    sun: []
  },

  // Akutsprechstunde ohne Termin (TODO). Komplett leer = Abschnitt wird ausgeblendet.
  acuteHours: {
    mon: ["08:00–09:30"],
    tue: ["08:00–09:30"],
    wed: ["08:00–09:30"],
    thu: ["08:00–09:30"],
    fri: ["08:00–09:30"],
    sat: [],
    sun: []
  },

  // Praxis-Hinweise (Urlaub, Grippeimpfung …). Werden nur zwischen "from" und "to" angezeigt.
  // Texte pro Sprache; fehlt eine Sprache, wird Deutsch gezeigt.
  notices: [
    {
      from: "2026-10-01",
      to: "2026-12-31",
      text: {
        de: "Grippeimpfung 2026/27: Ab sofort in der Praxis – sprechen Sie uns an.",
        en: "Flu vaccination 2026/27: now available in the practice – just ask us.",
        ar: "لقاح الإنفلونزا 2026/27: متوفر الآن في العيادة – اسألونا.",
        uk: "Щеплення від грипу 2026/27: вже доступне в практиці – звертайтеся.",
        ro: "Vaccinarea antigripală 2026/27: disponibilă acum în cabinet – întrebați-ne."
      }
    }
  ],

  // Anfahrt (nur Deutsch, leer = ausgeblendet). TODO
  directions: {
    transit: "",   // z. B. "Bus 781/782, Haltestelle … (2 Min. Fußweg)"
    parking: "",   // z. B. "Kostenlose Parkplätze direkt vor dem Haus"
    access: ""     // z. B. "Barrierefreier Zugang, Aufzug vorhanden"
  },

  // Praxisteam. "photo" = Dateiname in assets/photos/ (ohne Endung, .jpg).
  // role: doctor | lead | mfa | trainee
  team: [
    { name: "Wahbeh Mohammad Hussein", role: "doctor", photo: "team-mohammad-hussein", langs: ["de", "ar", "uk", "ro", "en"] },
    { name: "", role: "lead", photo: "team-2", langs: [] },     // TODO: Name eintragen
    { name: "", role: "mfa", photo: "team-3", langs: [] },      // TODO
    { name: "", role: "mfa", photo: "team-4", langs: [] }       // TODO
  ],

  // Stellenangebote. Leeres Array = Seite zeigt „Initiativbewerbung“.
  jobs: ["mfa", "trainee"]
};
