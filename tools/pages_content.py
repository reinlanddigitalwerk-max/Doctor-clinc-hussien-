# Body templates for each page. {{key}} / {{key|tag}} = translated text, [[icon:name]] = icon.

def checklist(prefix, n):
    return "\n".join(f"              {{{{{prefix}.i{i}|li}}}}" for i in range(1, n + 1))


def service_block(anchor, icon, title, prefix, n, extra=""):
    return f"""        <article class="service-block" id="{anchor}">
          <div>
            [[icon:{icon}]]
            {{{{{title}|h2}}}}
            {{{{{prefix}.d|p}}}}{extra}
          </div>
          <ul class="checklist">
{checklist(prefix, n)}
          </ul>
        </article>"""


# Karte: erst gezeichnete Vorschau (keine Daten an Dritte), nach Klick Google Maps. Der Thermometer-Pin sitzt
# immer in der Mitte – genau dort, wo Google die Adresse zentriert. Die Karte ist deshalb nicht verschiebbar.
MAP = """
        <div class="map js-map">
          <div class="map-canvas js-map-canvas">
            <svg class="map-bg" aria-hidden="true" viewBox="0 0 800 400" preserveAspectRatio="xMidYMid slice">
              <rect width="800" height="400" class="mb-ground"/>
              <rect x="30" y="30" width="200" height="120" rx="14" class="mb-block"/>
              <rect x="270" y="20" width="90" height="140" rx="14" class="mb-block"/>
              <rect x="460" y="30" width="150" height="120" rx="14" class="mb-park"/>
              <rect x="650" y="20" width="140" height="150" rx="14" class="mb-block"/>
              <rect x="20" y="250" width="160" height="130" rx="14" class="mb-block"/>
              <rect x="220" y="250" width="140" height="120" rx="14" class="mb-park"/>
              <rect x="460" y="250" width="110" height="130" rx="14" class="mb-block"/>
              <rect x="610" y="240" width="180" height="140" rx="14" class="mb-block"/>
              <path class="mb-road-edge" d="M-20 200H820M410 -20V420M-20 60 260 200M560 420 640 200 820 150"/>
              <path class="mb-road" d="M-20 200H820M410 -20V420M-20 60 260 200M560 420 640 200 820 150"/>
              <path class="mb-lane" d="M-20 200H820M410 -20V420"/>
            </svg>
          </div>
          <a class="map-pin js-route" href="#" target="_blank" rel="noopener" aria-label="Route zur Praxis planen" data-i18n-attr="aria-label:map.pin">
            <svg aria-hidden="true" viewBox="0 0 48 106" width="48" height="106">
              <ellipse class="t-shadow" cx="24" cy="103" rx="14" ry="3"/>
              <path class="t-body" d="M9 17a15 15 0 0 1 30 0v47.5a21 21 0 1 1-30 0Z"/>
              <path class="t-glass" d="M17 17a7 7 0 0 1 14 0v52a12.5 12.5 0 1 1-14 0Z"/>
              <rect class="t-column" x="20" y="14" width="8" height="66" rx="4"/>
              <circle class="t-bulb" cx="24" cy="81" r="9.5"/>
              <path class="t-ticks" d="M33 24h3M33 34h3M33 44h3M33 54h3"/>
              <circle class="t-shine" cx="20.5" cy="77.5" r="2.4"/>
            </svg>
          </a>
          <div class="map-card js-map-card">
            <strong dir="ltr">Hausarztpraxis Hilden Nord</strong>
            <span class="js-address">–</span>
          </div>
          <div class="map-consent js-map-consent">
            {{map.consent|p}}
            <button class="btn btn-primary btn-sm js-map-load" type="button" data-i18n="map.load">Karte laden</button>
          </div>
        </div>"""


def PAGES(page_hero):
    home = """    <section class="hero">
      <!-- Hintergrund: Foto aus assets/photos/hero-arzt.jpg, weichgezeichnet (fehlt es, bleibt der helle Verlauf) -->
      <div class="hero-bg" aria-hidden="true"></div>
      <div class="container hero-grid">
        <div class="hero-copy">
          {{home.eyebrow|p.eyebrow}}
          {{hero.title|h1}}
          {{hero.lead|p.lead}}
          <div class="hero-cta">
            <a class="btn btn-primary js-book" href="kontakt.html" data-i18n="cta.book">Termin buchen</a>
            <a class="btn btn-ghost js-phone-link" href="tel:">
              <svg aria-hidden="true" viewBox="0 0 24 24" width="18" height="18"><path fill="currentColor" d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1l-2.3 2.2Z"/></svg>
              <span class="js-phone">–</span>
            </a>
          </div>
          <ul class="badges">
            <li><span class="dot"></span>{{hero.badge1}}</li>
            <li><span class="dot"></span>{{hero.badge2}}</li>
            <li><span class="dot"></span>{{hero.badge3}}</li>
          </ul>
        </div>

        <div class="hero-visual">
          <div class="hero-logo">
            <span class="logo-shine"><img src="assets/logo-praxis.svg" width="964" height="988" alt="Praxislogo: Herz aus Händen mit Familie, Kreuz, Stethoskop und EKG-Linie" data-i18n-attr="alt:hero.emblemAlt" fetchpriority="high"></span>
          </div>
        </div>
      </div>
      <div class="container">
        <div class="today-strip" role="group" aria-labelledby="today-title">
          <span class="status js-status"></span>
          <p class="today-main"><strong id="today-title" class="js-today-title">Heute</strong> <span class="js-today-hours" dir="ltr">–</span></p>
          <p class="status-detail js-status-detail"></p>
          <p class="today-acute js-acute-section js-acute-row">{{home.acuteToday}} <b class="js-acute-today" dir="ltr">–</b></p>
          <a class="link-arrow" href="sprechzeiten.html" data-i18n="info.allHours">Alle Sprechzeiten</a>
        </div>
      </div>
    </section>

    <section class="section" id="anliegen">
      <div class="container">
        <header class="section-head">
          {{guide.eyebrow|p.eyebrow}}
          {{guide.title|h2}}
          {{guide.lead|p.lead}}
        </header>
        <div class="routes">
          <a class="route" href="sprechzeiten.html#akut">[[icon:clock]]{{guide.acute.t|h3}}{{guide.acute.d|p}}<span class="link-arrow" data-i18n="guide.acute.l">Zeiten ansehen</span></a>
          <a class="route js-book" href="kontakt.html">[[icon:calendar]]{{guide.book.t|h3}}{{guide.book.d|p}}<span class="link-arrow" data-i18n="guide.book.l">Termin buchen</span></a>
          <a class="route" href="kontakt.html#rezepte">[[icon:pill]]{{guide.rx.t|h3}}{{guide.rx.d|p}}<span class="link-arrow" data-i18n="guide.rx.l">So geht's</span></a>
          <a class="route" href="gutachten.html">[[icon:doc]]{{guide.expert.t|h3}}{{guide.expert.d|p}}<span class="link-arrow" data-i18n="guide.expert.l">Mehr erfahren</span></a>
          <a class="route route-emergency" href="tel:112">[[icon:alert]]{{guide.emergency.t|h3}}{{guide.emergency.d|p}}<span class="link-arrow" data-i18n="guide.emergency.l">112 anrufen</span></a>
        </div>
      </div>
    </section>

    <section class="section section-tint">
      <div class="container split">
        <div class="photo photo-wide" data-photo="praxis-team" role="img" data-i18n-attr="aria-label:welcome.title"></div>
        <div>
          {{welcome.eyebrow|p.eyebrow}}
          {{welcome.title|h2}}
          {{welcome.text|p}}
          <a class="btn btn-ghost" href="praxis.html" data-i18n="welcome.link">Mehr über unsere Praxis</a>
        </div>
      </div>
    </section>

    <section class="section" id="leistungen">
      <div class="container">
        <header class="section-head">
          {{services.eyebrow|p.eyebrow}}
          {{services.title|h2}}
          {{services.lead|p.lead}}
        </header>
        <div class="cards">
          <a class="card" href="leistungen.html#allgemein">[[icon:stetho]]{{s1.t|h3}}{{s1.d|p}}</a>
          <a class="card" href="leistungen.html#vorsorge">[[icon:shield]]{{s2.t|h3}}{{s2.d|p}}</a>
          <a class="card" href="leistungen.html#impfungen">[[icon:syringe]]{{s3.t|h3}}{{s3.d|p}}</a>
          <a class="card" href="leistungen.html#labor">[[icon:flask]]{{s4.t|h3}}{{s4.d|p}}</a>
          <a class="card" href="leistungen.html#chronisch">[[icon:pulse]]{{s5.t|h3}}{{s5.d|p}}</a>
          <a class="card card-highlight" href="gutachten.html">[[icon:doc]]{{s6.t|h3}}{{s6.d|p}}<span class="more" data-i18n="guide.expert.l">Mehr erfahren</span></a>
          <a class="card" href="leistungen.html#krankschreibung">[[icon:clipboard]]{{s7.t|h3}}{{s7.d|p}}</a>
          <a class="card" href="leistungen.html#hausbesuche">[[icon:home]]{{s8.t|h3}}{{s8.d|p}}</a>
        </div>
        <p style="margin-top:28px"><a class="btn btn-ghost" href="leistungen.html" data-i18n="cta.allServices">Alle Leistungen</a></p>
      </div>
    </section>

    <section class="section section-tint">
      <div class="container">
        <header class="section-head">
          {{langs.eyebrow|p.eyebrow}}
          {{langs.title|h2}}
          {{langs.lead|p.lead}}
        </header>
        <div class="greetings">
          <div class="greeting" lang="de"><b>Willkommen</b>{{lang.de}}</div>
          <div class="greeting" lang="ar" dir="rtl"><b>أهلاً وسهلاً</b>{{lang.ar}}</div>
          <div class="greeting" lang="uk"><b>Ласкаво просимо</b>{{lang.uk}}</div>
          <div class="greeting" lang="ro"><b>Bine ați venit</b>{{lang.ro}}</div>
          <div class="greeting" lang="en"><b>Welcome</b>{{lang.en}}</div>
        </div>
      </div>
    </section>

    <section class="section section-dark">
      <div class="container split">
        <div>
          {{contact.eyebrow|p.eyebrow}}
          {{contact.title|h2}}
          {{contact.lead|p.lead}}
          <div class="hero-cta">
            <a class="btn btn-accent js-book" href="kontakt.html" data-i18n="cta.book">Termin buchen</a>
            <a class="btn btn-outline-light js-route" href="#" target="_blank" rel="noopener" data-i18n="contact.route">Route planen</a>
          </div>
        </div>
        <dl class="contact-list">
          <div><dt>{{info.address}}</dt><dd class="js-address">–</dd></div>
          <div><dt>{{info.phone}}</dt><dd><a class="js-phone-link" href="tel:"><span class="js-phone">–</span></a></dd></div>
          <div class="js-whatsapp-row"><dt>{{info.whatsapp}}</dt><dd><a class="js-whatsapp-link" href="#" target="_blank" rel="noopener"><span class="js-whatsapp">–</span></a></dd></div>
          <div><dt>{{info.email}}</dt><dd><a class="js-mail-link" href="mailto:"><span class="js-email">–</span></a></dd></div>
        </dl>
      </div>
    </section>"""

    praxis = page_hero("page.practice", "practice.lead", "nav.practice") + """

    <section class="section">
      <div class="container">
        <header class="section-head">
          {{values.eyebrow|p.eyebrow}}
          {{values.title|h2}}
        </header>
        <div class="cards cards-3">
          <article class="card">[[icon:heart]]{{v1.t|h3}}{{v1.d|p}}</article>
          <article class="card card-highlight">[[icon:chat]]{{v2.t|h3}}{{v2.d|p}}</article>
          <article class="card">[[icon:award]]{{v3.t|h3}}{{v3.d|p}}</article>
        </div>
      </div>
    </section>

    <section class="section section-tint">
      <div class="container">
        <header class="section-head">
          {{rooms.eyebrow|p.eyebrow}}
          {{rooms.title|h2}}
        </header>
        <div class="gallery">
          <figure><div class="photo" data-photo="praxis-empfang"></div>{{photo.reception|figcaption}}</figure>
          <figure><div class="photo" data-photo="praxis-wartebereich"></div>{{photo.waiting|figcaption}}</figure>
          <figure><div class="photo" data-photo="praxis-behandlungsraum"></div>{{photo.treatment|figcaption}}</figure>
          <figure><div class="photo" data-photo="praxis-labor"></div>{{photo.lab|figcaption}}</figure>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <header class="section-head">
          {{first.eyebrow|p.eyebrow}}
          {{first.title|h2}}
        </header>
        <ol class="steps">
          <li>{{step1.t|h3}}{{step1.d|p}}</li>
          <li>{{step2.t|h3}}{{step2.d|p}}</li>
          <li>{{step3.t|h3}}{{step3.d|p}}</li>
          <li>{{step4.t|h3}}{{step4.d|p}}</li>
        </ol>
      </div>
    </section>

    <section class="section section-tint" id="faq">
      <div class="container narrow">
        <header class="section-head">
          {{faq.eyebrow|p.eyebrow}}
          {{faq.title|h2}}
        </header>
        <div class="faq">
          <details>{{faq.q1|summary}}{{faq.a1|p}}</details>
          <details>{{faq.q2|summary}}{{faq.a2|p}}</details>
          <details>{{faq.q3|summary}}{{faq.a3|p}}</details>
          <details>{{faq.q4|summary}}{{faq.a4|p}}</details>
          <details>{{faq.q5|summary}}{{faq.a5|p}}</details>
        </div>
      </div>
    </section>

    <section class="section" id="anfahrt">
      <div class="container split">
        <div>
          {{directions.eyebrow|p.eyebrow}}
          {{directions.title|h2}}
          <p class="js-address" style="font-size:1.15rem;font-weight:600">–</p>
          <a class="btn btn-primary js-route" href="#" target="_blank" rel="noopener" data-i18n="contact.route">Route planen</a>
        </div>
        <ul class="info-list js-directions">
          <li class="js-direction" data-key="transit"><b data-i18n="directions.transit">Bus &amp; Bahn</b><span class="js-direction-text"></span></li>
          <li class="js-direction" data-key="parking"><b data-i18n="directions.parking">Parken</b><span class="js-direction-text"></span></li>
          <li class="js-direction" data-key="access"><b data-i18n="directions.access">Barrierefreiheit</b><span class="js-direction-text"></span></li>
        </ul>
      </div>
      <div class="container map-wrap">""" + MAP + """
      </div>
    </section>"""

    chips = """
        <nav class="chips" aria-label="Leistungen">
          <a href="#allgemein" data-i18n="s1.t">x</a><a href="#innere" data-i18n="svc.intern.t">x</a><a href="#vorsorge" data-i18n="s2.t">x</a><a href="#impfungen" data-i18n="s3.t">x</a>
          <a href="#labor" data-i18n="s4.t">x</a><a href="#chronisch" data-i18n="s5.t">x</a><a href="#gutachten" data-i18n="s6.t">x</a>
          <a href="#krankschreibung" data-i18n="s7.t">x</a><a href="#hausbesuche" data-i18n="s8.t">x</a><a href="#privat" data-i18n="svc.private.t">x</a>
        </nav>"""
    expert_link = '\n            <a class="btn btn-primary" href="gutachten.html" data-i18n="guide.expert.l">Mehr erfahren</a>'
    leistungen = page_hero("page.services", "services.pageLead", "nav.services", chips) + f"""

    <section class="section" style="padding-top:24px">
      <div class="container">
{service_block("allgemein", "stetho", "s1.t", "svc.general", 4)}
{service_block("innere", "heart", "svc.intern.t", "svc.intern", 4)}
{service_block("vorsorge", "shield", "s2.t", "svc.prevent", 4)}
{service_block("impfungen", "syringe", "s3.t", "svc.vacc", 4)}
{service_block("labor", "flask", "s4.t", "svc.lab", 4)}
{service_block("chronisch", "pulse", "s5.t", "svc.chronic", 4)}
{service_block("gutachten", "doc", "s6.t", "expert", 4, expert_link)}
{service_block("krankschreibung", "clipboard", "s7.t", "svc.admin", 4)}
{service_block("hausbesuche", "home", "s8.t", "svc.home", 2)}
{service_block("privat", "euro", "svc.private.t", "svc.private", 4)}
      </div>
    </section>

    <section class="section section-tint">
      <div class="container narrow" style="text-align:center">
        {{{{services.askTitle|h2}}}}
        {{{{services.askText|p}}}}
        <div class="hero-cta" style="justify-content:center">
          <a class="btn btn-primary js-phone-link" href="tel:"><span data-i18n="cta.call">Anrufen</span></a>
          <a class="btn btn-ghost js-book" href="kontakt.html" data-i18n="cta.book">Termin buchen</a>
        </div>
      </div>
    </section>"""
    # expert block uses expert.lead-style description key "svc.expert.d" and expert.i1-4 items
    leistungen = leistungen.replace("{{expert.d|p}}", "{{svc.expert.d|p}}")

    gutachten = """    <section class="page-hero">
      <div class="container page-hero-grid">
        <div>
          <nav class="breadcrumb" aria-label="Breadcrumb"><a href="index.html">{{nav.home}}</a><span aria-hidden="true">/</span>{{nav.expert}}</nav>
          {{page.expert|h1}}
          {{expert.pageLead|p.lead}}
          <div class="hero-cta">
            <a class="btn btn-primary js-mail-link" href="mailto:" data-subject="expert.mailSubject" data-i18n="expert.cta">Gutachten anfragen</a>
            <a class="btn btn-ghost js-phone-link" href="tel:"><span class="js-phone">–</span></a>
          </div>
        </div>
        <div class="photo photo-wide" data-photo="gutachten"></div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <header class="section-head">{{expert.for.title|h2}}</header>
        <div class="cards">
          <article class="card">[[icon:shield]]{{expert.for1.t|h3}}{{expert.for1.d|p}}</article>
          <article class="card">[[icon:building]]{{expert.for2.t|h3}}{{expert.for2.d|p}}</article>
          <article class="card">[[icon:briefcase]]{{expert.for3.t|h3}}{{expert.for3.d|p}}</article>
          <article class="card">[[icon:user]]{{expert.for4.t|h3}}{{expert.for4.d|p}}</article>
        </div>
      </div>
    </section>

    <section class="section section-tint">
      <div class="container">
        <header class="section-head">{{expert.process.title|h2}}</header>
        <ol class="steps">
          <li>{{ep1.t|h3}}{{ep1.d|p}}</li>
          <li>{{ep2.t|h3}}{{ep2.d|p}}</li>
          <li>{{ep3.t|h3}}{{ep3.d|p}}</li>
          <li>{{ep4.t|h3}}{{ep4.d|p}}</li>
        </ol>
      </div>
    </section>

    <section class="section">
      <div class="container split">
        <div class="panel">
          {{expert.docs.title|h3}}
          <ul class="checklist">
""" + checklist("expert.docs", 4) + """
          </ul>
        </div>
        <div>
          [[icon:euro]]
          {{expert.costs.title|h3}}
          {{expert.costs.d|p}}
          [[icon:globe]]
          {{expert.lang.title|h3}}
          {{expert.lang.d|p}}
        </div>
      </div>
    </section>

    <section class="section section-dark">
      <div class="container narrow" style="text-align:center">
        {{expert.ctaTitle|h2}}
        <p class="lead" style="margin-inline:auto" data-i18n="expert.ctaText">x</p>
        <div class="hero-cta" style="justify-content:center">
          <a class="btn btn-accent js-mail-link" href="mailto:" data-subject="expert.mailSubject" data-i18n="expert.cta">Gutachten anfragen</a>
          <a class="btn btn-outline-light js-phone-link" href="tel:"><span class="js-phone">–</span></a>
        </div>
      </div>
    </section>"""

    team = page_hero("page.team", "team.pageLead", "nav.team") + """

    <section class="section">
      <div class="container doctor-feature">
        <div class="photo photo-portrait" data-photo="team-mohammad-hussein" data-alt="Mohammad Hussein"><span class="photo-initials">MH</span></div>
        <div>
          {{doctor.eyebrow|p.eyebrow}}
          {{doctor.name|h2}}
          <p class="role" data-i18n="doctor.role">x</p>
          {{doctor.bio|p}}
          <h3 class="langs-title" data-i18n="doctor.focusTitle">x</h3>
          <ul class="checklist">
""" + checklist("doctor", 0) + """              {{doctor.f1|li}}
              {{doctor.f2|li}}
              {{doctor.f3|li}}
              {{doctor.f4|li}}
          </ul>
          <h3 class="langs-title" data-i18n="doctor.langsTitle">x</h3>
          <ul class="langs">
            <li><span class="code">DE</span>{{lang.de}}</li>
            <li><span class="code">AR</span>{{lang.ar}}</li>
            <li><span class="code">UK</span>{{lang.uk}}</li>
            <li><span class="code">RO</span>{{lang.ro}}</li>
            <li><span class="code">EN</span>{{lang.en}}</li>
          </ul>
        </div>
      </div>
    </section>

    <section class="section section-tint">
      <div class="container">
        <header class="section-head">
          {{team.staffTitle|h2}}
          {{team.staffLead|p.lead}}
        </header>
        <div class="team-grid js-team"></div>
        <a class="card" href="karriere.html" style="margin-top:28px;display:flex;align-items:center;gap:18px;flex-wrap:wrap">
          [[icon:briefcase]]
          <div style="flex:1;min-width:200px">{{team.jobsT|h3}}{{team.jobsD|p}}</div>
          <span class="more" data-i18n="team.jobsL">x</span>
        </a>
      </div>
    </section>"""

    sprechzeiten = page_hero("page.hours", "hours.pageLead", "nav.hours") + """

    <section class="section">
      <div class="container split">
        <div>
          {{hours.title|h2}}
          <table class="hours"><tbody class="js-hours" data-source="hours"></tbody></table>
          <p class="note" data-i18n="hours.byAppointment">x</p>
          <a class="btn btn-primary js-book" href="kontakt.html" data-i18n="cta.book">Termin buchen</a>
        </div>
        <div class="panel js-acute-section" id="akut">
          [[icon:clock]]
          {{acute.title|h3}}
          {{acute.d|p}}
          <table class="hours"><tbody class="js-hours" data-source="acuteHours"></tbody></table>
        </div>
      </div>
    </section>

    <section class="section section-tint">
      <div class="container split">
        <div class="emergency">
          <h3>[[icon:alert]]<span data-i18n="emergency.title">x</span></h3>
          <div class="emergency-numbers">
            <a href="tel:116117"><b>116 117</b>{{emergency.oncall}}</a>
            <a href="tel:112"><b>112</b>{{emergency.112}}</a>
          </div>
        </div>
        <div>
          {{holidays.title|h3}}
          {{holidays.d|p}}
          <div class="panel" style="margin-top:22px">
            {{visit.title|h3}}
            <ul class="checklist">
""" + checklist("visit", 5) + """
            </ul>
          </div>
        </div>
      </div>
    </section>"""

    kontakt = page_hero("page.contact", "contact.pageLead", "nav.contact") + """

    <section class="section">
      <div class="container">
        <div class="contact-cards">
          <div class="contact-card">[[icon:phone]]{{info.phone|h3}}<p><a class="js-phone-link" href="tel:"><span class="js-phone">–</span></a></p>
            <p class="contact-sub js-fax-row">{{info.fax}} <span class="js-fax">–</span></p>
            <p class="contact-sub js-whatsapp-row"><a class="js-whatsapp-link" href="#" target="_blank" rel="noopener">{{info.whatsapp}} <span class="js-whatsapp">–</span></a></p></div>
          <div class="contact-card">[[icon:mail]]{{info.email|h3}}<p><a class="js-mail-link" href="mailto:"><span class="js-email">–</span></a></p></div>
          <div class="contact-card">[[icon:pin]]{{info.address|h3}}<p class="js-address">–</p></div>
        </div>
        <div class="hero-cta">
          <a class="btn btn-primary js-book" href="tel:" data-i18n="cta.book">Termin buchen</a>
          <a class="btn btn-ghost js-route" href="#" target="_blank" rel="noopener" data-i18n="contact.route">Route planen</a>
        </div>
      </div>
    </section>

    <section class="section section-tint" id="rezepte">
      <div class="container split">
        <div>
          [[icon:pill]]
          {{rx.title|h2}}
          {{rx.d|p}}
          <a class="btn btn-primary js-mail-link" href="mailto:" data-subject="rx.mailSubject" data-i18n="rx.cta">Per E-Mail bestellen</a>
          <p class="note" data-i18n="rx.note">x</p>
        </div>
        <div class="panel">
          <ul class="checklist">
""" + checklist("rx", 4) + """
          </ul>
        </div>
      </div>
    </section>

    <section class="section" id="anfahrt">
      <div class="container split">
        <div>
          {{nav.hours|h2}}
          <table class="hours"><tbody class="js-hours" data-source="hours"></tbody></table>
        </div>
        <div>
          {{directions.title|h2}}
          <ul class="info-list js-directions">
            <li class="js-direction" data-key="transit"><b data-i18n="directions.transit">Bus &amp; Bahn</b><span class="js-direction-text"></span></li>
            <li class="js-direction" data-key="parking"><b data-i18n="directions.parking">Parken</b><span class="js-direction-text"></span></li>
            <li class="js-direction" data-key="access"><b data-i18n="directions.access">Barrierefreiheit</b><span class="js-direction-text"></span></li>
          </ul>
          <div class="emergency" style="margin-top:22px">
            <h3>[[icon:alert]]<span data-i18n="emergency.title">x</span></h3>
            <div class="emergency-numbers">
              <a href="tel:116117"><b>116 117</b>{{emergency.oncall}}</a>
              <a href="tel:112"><b>112</b>{{emergency.112}}</a>
            </div>
          </div>
        </div>
      </div>
      <div class="container map-wrap">""" + MAP + """
      </div>
    </section>"""

    karriere = page_hero("page.jobs", "jobs.pageLead", "nav.jobs") + """

    <section class="section">
      <div class="container split">
        <div>
          {{jobs.openings|h2}}
          <div class="jobs js-jobs"></div>
        </div>
        <div class="panel">
          {{jobs.offer.title|h3}}
          <ul class="checklist">
""" + checklist("jobs.offer", 4) + """
          </ul>
          <p class="note" data-i18n="jobs.how">x</p>
          <p><a class="js-mail-link" href="mailto:"><span class="js-email">–</span></a></p>
        </div>
      </div>
    </section>"""

    return [
        ("index.html", "home", "page.home", home),
        ("praxis.html", "praxis", "page.practice", praxis),
        ("leistungen.html", "leistungen", "page.services", leistungen),
        ("gutachten.html", "gutachten", "page.expert", gutachten),
        ("team.html", "team", "page.team", team),
        ("sprechzeiten.html", "sprechzeiten", "page.hours", sprechzeiten),
        ("kontakt.html", "kontakt", "page.contact", kontakt),
        ("karriere.html", "karriere", "page.jobs", karriere),
    ]
