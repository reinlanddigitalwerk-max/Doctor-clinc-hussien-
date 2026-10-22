// Praxisdaten – hier anpassen. Alle Stellen der Website lesen aus diesem Objekt.
// Werte mit "TODO" sind Platzhalter und müssen vor der Veröffentlichung ersetzt werden.
window.PRAXIS = {
  name: "Hausarzt Praxis Hilden Nord",
  doctor: "Mohammad Hussein",

  street: "Musterstraße 1",          // TODO: echte Straße + Hausnummer
  city: "40721 Hilden",              // TODO: PLZ prüfen
  phone: "02103 000000",             // TODO: echte Telefonnummer
  fax: "",                           // optional, leer = ausgeblendet
  email: "info@hausarzt-hilden-nord.de", // TODO: echte E-Mail

  // Online-Terminbuchung (z. B. Doctolib-Link). Leer = Button ruft die Praxis an.
  bookingUrl: "",

  // Sprechzeiten (TODO: echte Zeiten eintragen). Leeres Array = geschlossen.
  hours: {
    mon: ["08:00–12:00", "15:00–18:00"],
    tue: ["08:00–12:00", "15:00–18:00"],
    wed: ["08:00–12:00"],
    thu: ["08:00–12:00", "15:00–18:00"],
    fri: ["08:00–12:00"],
    sat: [],
    sun: []
  }
};
