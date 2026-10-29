// Gemeinsame Logik aller Seiten: Kopf- und Fußbereich, Sprachen, Sprechzeiten, Team, Fotos.
// Wird direkt nach <div id="site-header"> geladen, damit der Kopf ohne Flackern erscheint.
(function () {
  "use strict";

  var P = window.PRAXIS;
  var I18N = window.I18N = window.I18N || {};
  var LANGS = ["de", "ar", "uk", "ro", "en"];
  var LANG_NAMES = { de: "Deutsch", ar: "العربية", uk: "Українська", ro: "Română", en: "English" };
  var RTL = ["ar"];
  var DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"];
  var STORAGE_KEY = "praxis-lang";
  // Seitenname aus <body data-page> – oder aus window.PRAXIS_PAGE, wo der <body> nicht selbst geschrieben wird.
  var PAGE = document.body.getAttribute("data-page") || window.PRAXIS_PAGE || "";
  var TITLE_KEY = document.body.getAttribute("data-title") || window.PRAXIS_TITLE || "";

  var NAV = [
    ["praxis.html", "nav.practice", "praxis"],
    ["leistungen.html", "nav.services", "leistungen"],
    ["gutachten.html", "nav.expert", "gutachten"],
    ["team.html", "nav.team", "team"],
    ["sprechzeiten.html", "nav.hours", "sprechzeiten"],
    ["kontakt.html", "nav.contact", "kontakt"]
  ];

  var lang = "de";

  // Farbpaletten-Vorschau: ?palette=1 … 4 (5 = gewählte Palette „Ozeanblau & Sand“). Bleibt beim Navigieren erhalten.
  // Mit PRAXIS.previewPalettes = true ist die Leiste immer sichtbar und die Wahl wird gespeichert.
  var palette = (function () {
    var p = new URLSearchParams(location.search).get("palette");
    if (/^[1-5]$/.test(p || "")) return p;
    if (!P.previewPalettes) return null;
    try { p = localStorage.getItem("praxis-palette"); } catch (e) { p = null; }
    return /^[1-5]$/.test(p || "") ? p : "5";
  })();
  function applyPalette(p) {
    palette = p;
    if (P.previewPalettes) { try { localStorage.setItem("praxis-palette", p); } catch (e) { /* ignore */ } }
    if (p && p !== "5") document.documentElement.setAttribute("data-palette", p);
    else document.documentElement.removeAttribute("data-palette");
    each(".palette-switch button", function (b) { b.setAttribute("aria-pressed", String(b.value === p)); });
  }
  if (palette) applyPalette(palette);

  function t(key) {
    var dict = I18N[lang] || I18N.de;
    if (dict[key] != null) return dict[key];
    return I18N.de[key] != null ? I18N.de[key] : key;
  }

  function each(selector, fn, root) {
    Array.prototype.forEach.call((root || document).querySelectorAll(selector), fn);
  }

  function el(tag, attrs, children) {
    var node = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) {
      if (k === "text") node.textContent = attrs[k];
      else if (k === "i18n") { node.setAttribute("data-i18n", attrs[k]); node.textContent = t(attrs[k]); }
      else node.setAttribute(k, attrs[k]);
    });
    (children || []).forEach(function (c) { if (c) node.appendChild(typeof c === "string" ? document.createTextNode(c) : c); });
    return node;
  }

  function telHref(phone) {
    var digits = phone.replace(/[^\d+]/g, "");
    if (digits.charAt(0) === "0") digits = "+49" + digits.slice(1);
    return "tel:" + digits;
  }

  var ICONS = {
    phone: '<path fill="currentColor" stroke="none" d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1l-2.3 2.2Z"/>',
    globe: '<path d="M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18Zm-9-9h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3Z"/>',
    calendar: '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M16 3v4M8 3v4M3 10h18"/>',
    alert: '<path d="M12 3 2 20h20L12 3Z"/><path d="M12 10v4M12 17h.01"/>',
    chevron: '<path d="m6 9 6 6 6-6"/>'
  };
  // Praxislogo (Herz aus Händen, Familie, Stethoskop) – vektorisiert aus der Visitenkarte.
  function logo(size) {
    return '<img class="logo-mark" src="assets/logo-praxis.svg" width="' + size + '" height="' + size + '" alt="" decoding="async">';
  }

  function icon(name, size) {
    var s = size || 18;
    return '<svg aria-hidden="true" viewBox="0 0 24 24" width="' + s + '" height="' + s + '" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">' + ICONS[name] + "</svg>";
  }

  // ---------------------------------------------------------------- Header

  function renderHeader() {
    var mount = document.getElementById("site-header");
    if (!mount) return;
    var nav = NAV.map(function (n) {
      var current = n[2] === PAGE ? ' aria-current="page"' : "";
      return '<a href="' + n[0] + '"' + current + ' data-i18n="' + n[1] + '">' + t(n[1]) + "</a>";
    }).join("");
    var langItems = LANGS.map(function (c) {
      return '<li><button type="button" role="menuitemradio" aria-checked="false" data-lang="' + c + '" lang="' + c + '">' +
        '<span class="lang-code">' + c.toUpperCase() + "</span>" + LANG_NAMES[c] + "</button></li>";
    }).join("");

    mount.outerHTML =
      '<a class="skip-link" href="#main" data-i18n="a11y.skip">' + t("a11y.skip") + "</a>" +
      '<header class="site-header"><div class="container header-inner">' +
        '<a class="brand" href="index.html" aria-label="' + P.name + '">' +
          logo(46) +
          '<span class="brand-text"><strong>Hausarztpraxis</strong><span>Hilden Nord</span></span>' +
        "</a>" +
        '<nav class="main-nav" id="main-nav" aria-label="Hauptnavigation">' + nav +
          '<div class="nav-extra">' +
            '<a class="js-phone-link" href="tel:">' + icon("phone", 16) + '<span class="js-phone"></span></a>' +
            '<p><span data-i18n="topbar.emergency">' + t("topbar.emergency") + '</span> <b dir="ltr">112</b> · ' +
            '<span data-i18n="topbar.oncall">' + t("topbar.oncall") + '</span> <b dir="ltr">116 117</b></p>' +
          "</div>" +
        "</nav>" +
        '<div class="header-tools">' +
          '<a class="status-chip js-status-chip" href="sprechzeiten.html"><span class="status-dot js-status-dot"></span><span class="js-status-short"></span></a>' +
          '<div class="lang-menu">' +
            '<button class="lang-btn" type="button" aria-haspopup="true" aria-expanded="false" aria-controls="lang-list">' +
              icon("globe", 17) + '<span class="js-lang-code">DE</span>' + icon("chevron", 14) +
              '<span class="sr-only" data-i18n="a11y.language">' + t("a11y.language") + "</span>" +
            "</button>" +
            '<ul class="lang-list" id="lang-list" role="menu" hidden>' + langItems + "</ul>" +
          "</div>" +
          '<a class="btn btn-primary btn-sm js-book" href="kontakt.html" data-i18n="cta.book">' + t("cta.book") + "</a>" +
          '<button class="nav-toggle" type="button" aria-controls="main-nav" aria-expanded="false">' +
            '<span class="sr-only" data-i18n="a11y.menu">' + t("a11y.menu") + "</span>" +
            '<span class="bar"></span><span class="bar"></span><span class="bar"></span>' +
          "</button>" +
        "</div>" +
      "</div></header>" +
      '<div class="notices js-notices" role="status"></div>';
  }

  function initLangMenu() {
    var btn = document.querySelector(".lang-btn");
    var list = document.getElementById("lang-list");
    if (!btn || !list) return;
    function open(state) {
      btn.setAttribute("aria-expanded", String(state));
      list.hidden = !state;
      if (state) list.querySelector('[aria-checked="true"]').focus();
    }
    btn.addEventListener("click", function () { open(list.hidden); });
    list.addEventListener("click", function (e) {
      var item = e.target.closest("[data-lang]");
      if (!item) return;
      open(false);
      btn.focus();
      setLang(item.getAttribute("data-lang"));
    });
    document.addEventListener("click", function (e) { if (!e.target.closest(".lang-menu")) open(false); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !list.hidden) { open(false); btn.focus(); } });
  }

  // ---------------------------------------------------------------- Footer

  function renderFooter() {
    var mount = document.getElementById("site-footer");
    if (!mount) return;
    var links = [["index.html", "nav.home"]].concat(NAV.map(function (n) { return [n[0], n[1]]; }), [["karriere.html", "nav.jobs"]]);
    mount.outerHTML =
      '<footer class="site-footer"><div class="container">' +
        '<div class="footer-grid">' +
          '<div class="footer-brand">' +
            '<a class="brand" href="index.html">' + logo(40) +
            '<span class="brand-text"><strong>Hausarztpraxis</strong><span>Hilden Nord</span></span></a>' +
            '<p data-i18n="footer.tagline">' + t("footer.tagline") + "</p>" +
            '<p class="footer-langs" dir="ltr">DE · AR · UK · RO · EN</p>' +
          "</div>" +
          '<div><h2 data-i18n="nav.contact">' + t("nav.contact") + "</h2>" +
            '<p class="js-address"></p>' +
            '<p><a class="js-phone-link" href="tel:"><span class="js-phone"></span></a><br>' +
            '<span class="js-fax-row"><span data-i18n="info.fax">' + t("info.fax") + '</span> <span class="js-fax"></span><br></span>' +
            '<span class="js-whatsapp-row"><a class="js-whatsapp-link" href="#" target="_blank" rel="noopener"><span data-i18n="info.whatsapp">' + t("info.whatsapp") + '</span> <span class="js-whatsapp"></span></a><br></span>' +
            '<a class="js-mail-link" href="mailto:"><span class="js-email"></span></a></p></div>' +
          '<div><h2 data-i18n="nav.hours">' + t("nav.hours") + "</h2>" +
            '<dl class="hours-compact js-hours-compact"></dl></div>' +
          '<div><h2 data-i18n="footer.links">' + t("footer.links") + "</h2>" +
            '<ul class="footer-links">' + links.map(function (l) {
              return '<li><a href="' + l[0] + '" data-i18n="' + l[1] + '">' + t(l[1]) + "</a></li>";
            }).join("") + "</ul></div>" +
        "</div>" +
        '<div class="footer-bottom">' +
          '<p>© <span class="js-year"></span> ' + P.name + " · " + P.doctor + "</p>" +
          '<p class="footer-emergency"><span data-i18n="topbar.emergency">' + t("topbar.emergency") + '</span> <b dir="ltr">112</b> · ' +
            '<span data-i18n="topbar.oncall">' + t("topbar.oncall") + '</span> <b dir="ltr">116 117</b></p>' +
          '<nav class="footer-legal" aria-label="Rechtliches">' +
            '<a href="impressum.html" data-i18n="footer.imprint">' + t("footer.imprint") + "</a>" +
            '<a href="datenschutz.html" data-i18n="footer.privacy">' + t("footer.privacy") + "</a>" +
          "</nav>" +
        "</div>" +
      "</div></footer>" +
      '<div class="action-bar">' +
        '<a class="js-phone-link" href="tel:">' + icon("phone", 18) + '<span data-i18n="cta.call">' + t("cta.call") + "</span></a>" +
        '<a class="is-primary js-book" href="kontakt.html">' + icon("calendar", 18) + '<span data-i18n="cta.book">' + t("cta.book") + "</span></a>" +
      "</div>";
  }

  // ---------------------------------------------------------------- Language

  function initialLang() {
    var fromUrl = new URLSearchParams(location.search).get("lang");
    if (LANGS.indexOf(fromUrl) !== -1) return fromUrl;
    try {
      var stored = localStorage.getItem(STORAGE_KEY);
      if (LANGS.indexOf(stored) !== -1) return stored;
    } catch (e) { /* storage unavailable */ }
    var nav = (navigator.language || "de").slice(0, 2).toLowerCase();
    return LANGS.indexOf(nav) !== -1 ? nav : "de";
  }

  function loadLang(code, done) {
    if (I18N[code]) return done();
    var s = document.createElement("script");
    s.src = "js/lang/" + code + ".js";
    s.onload = done;
    s.onerror = function () { done(); };
    document.head.appendChild(s);
  }

  function setLang(next) {
    loadLang(next, function () {
      lang = I18N[next] ? next : "de";
      var root = document.documentElement;
      root.lang = lang;
      root.dir = RTL.indexOf(lang) !== -1 ? "rtl" : "ltr";

      each("[data-i18n]", function (node) { node.textContent = t(node.getAttribute("data-i18n")); });
      each("[data-i18n-attr]", function (node) {
        node.getAttribute("data-i18n-attr").split(";").forEach(function (pair) {
          var parts = pair.split(":");
          node.setAttribute(parts[0], t(parts[1]));
        });
      });
      if (TITLE_KEY) document.title = t(TITLE_KEY) + " – " + P.name;

      each(".js-lang-code", function (node) { node.textContent = lang.toUpperCase(); });
      each(".lang-list [data-lang]", function (b) { b.setAttribute("aria-checked", String(b.getAttribute("data-lang") === lang)); });
      try { localStorage.setItem(STORAGE_KEY, lang); } catch (e) { /* ignore */ }

      renderDynamic();
      document.documentElement.classList.remove("i18n-pending");
    });
  }

  // Links innerhalb der Seite behalten Sprache und Paletten-Vorschau auch ohne Speicher.
  function keepLangInLinks(e) {
    var a = e.target.closest && e.target.closest("a[href$='.html'], a[href*='.html#']");
    if (!a || a.target || (lang === "de" && !palette)) return;
    var url = new URL(a.getAttribute("href"), location.href);
    if (url.origin !== location.origin) return;
    if (lang !== "de") url.searchParams.set("lang", lang);
    if (palette) url.searchParams.set("palette", palette);
    a.href = url.pathname + url.search + url.hash;
  }

  var PALETTE_COLORS = ["#1A6FB5", "#0B4F8A", "#0E7490", "#4F5BD5", "#2563A8"];
  function renderPaletteSwitch() {
    if (!palette) return;
    var bar = el("div", { class: "palette-switch", role: "group", "aria-label": "Farbpalette" });
    PALETTE_COLORS.forEach(function (c, i) {
      var b = el("button", { type: "button", value: String(i + 1), style: "background:" + c, text: String(i + 1) });
      b.addEventListener("click", function () {
        applyPalette(b.value);
        var url = new URL(location.href);
        url.searchParams.set("palette", b.value);
        history.replaceState(null, "", url);
      });
      bar.appendChild(b);
    });
    document.body.appendChild(bar);
    applyPalette(palette);
  }

  // ---------------------------------------------------------------- Practice data

  function renderContact() {
    each(".js-address", function (node) {
      node.innerHTML = "";
      // dir="ltr" je Zeile: sonst wird „40724 Hilden“ auf Arabisch zu „Hilden 40724“
      node.appendChild(el("span", { dir: "ltr", text: P.street }));
      node.appendChild(document.createElement("br"));
      node.appendChild(el("span", { dir: "ltr", text: P.city }));
    });
    each(".js-phone", function (node) { node.textContent = P.phone; });
    each(".js-phone-link", function (node) { node.href = telHref(P.phone); });
    each(".js-email", function (node) { node.textContent = P.email; });
    each(".js-fax", function (node) { node.textContent = P.fax; });
    each(".js-fax-row", function (node) { node.hidden = !P.fax; });
    each(".js-whatsapp", function (node) { node.textContent = P.whatsapp || ""; });
    each(".js-whatsapp-link", function (node) { if (P.whatsapp) node.href = "https://wa.me/" + telHref(P.whatsapp).replace(/^tel:\+/, ""); });
    each(".js-whatsapp-row", function (node) { node.hidden = !P.whatsapp; });
    each(".js-route", function (node) {
      node.href = "https://www.google.com/maps/dir/?api=1&destination=" + encodeURIComponent(P.name + ", " + P.street + ", " + P.city);
    });
    each(".js-book", function (node) {
      if (P.bookingUrl) {
        node.href = P.bookingUrl;
        node.target = "_blank";
        node.rel = "noopener";
      } else {
        node.href = telHref(P.phone);
      }
    });
    each(".js-year", function (node) { node.textContent = new Date().getFullYear(); });

    var d = P.directions || {};
    each(".js-direction", function (node) {
      var value = d[node.getAttribute("data-key")];
      node.hidden = !value;
      var target = node.querySelector(".js-direction-text");
      if (target) target.textContent = value || "";
    });
    each(".js-directions", function (node) {
      node.hidden = !(d.transit || d.parking || d.access);
    });
  }

  function renderMailLinks() {
    each(".js-mail-link", function (node) {
      var subjectKey = node.getAttribute("data-subject");
      node.href = "mailto:" + P.email + (subjectKey ? "?subject=" + encodeURIComponent(t(subjectKey)) : "");
    });
  }

  // ---------------------------------------------------------------- Hours

  // JS getDay(): 0 = Sonntag … 6 = Samstag → Index in DAYS
  function todayKey(now) { return DAYS[(now.getDay() + 6) % 7]; }

  function parseSlot(slot) {
    var m = slot.match(/(\d{1,2}):(\d{2})\s*[–-]\s*(\d{1,2}):(\d{2})/);
    return m ? { from: +m[1] * 60 + +m[2], to: +m[3] * 60 + +m[4] } : null;
  }

  function isOpen(slots, now) {
    var minutes = now.getHours() * 60 + now.getMinutes();
    return slots.some(function (s) {
      var r = parseSlot(s);
      return r && minutes >= r.from && minutes < r.to;
    });
  }

  function hasAny(table) {
    return DAYS.some(function (d) { return (table[d] || []).length; });
  }

  function renderHours() {
    var today = todayKey(new Date());
    each(".js-hours", function (body) {
      var table = P[body.getAttribute("data-source") || "hours"] || {};
      body.innerHTML = "";
      DAYS.forEach(function (day) {
        var slots = table[day] || [];
        var td = el("td", slots.length ? {} : { class: "closed" },
          slots.length ? slots.map(function (s) { return el("span", { dir: "ltr", text: s }); }) : [t("hours.closed")]);
        body.appendChild(el("tr", day === today ? { class: "is-today" } : {}, [
          el("th", { scope: "row", text: t("day." + day) }), td
        ]));
      });
    });

    // Kompakt: aufeinanderfolgende Tage mit gleichen Zeiten zusammenfassen.
    each(".js-hours-compact", function (dl) {
      dl.innerHTML = "";
      var groups = [];
      DAYS.forEach(function (day) {
        var slots = (P.hours[day] || []).join(" · ");
        var last = groups[groups.length - 1];
        if (last && last.slots === slots) last.to = day;
        else groups.push({ from: day, to: day, slots: slots });
      });
      groups.forEach(function (g) {
        if (!g.slots) return;
        var label = t("dayShort." + g.from) + (g.to !== g.from ? "–" + t("dayShort." + g.to) : "");
        dl.appendChild(el("div", {}, [el("dt", { text: label }), el("dd", { dir: "ltr" }, g.slots.split(" · ").map(function (s) { return el("span", { text: s }); }))]));
      });
    });

    each(".js-acute-section", function (node) { node.hidden = !hasAny(P.acuteHours || {}); });
  }

  function slotTimes(slot) {
    var m = slot.match(/(\d{1,2}:\d{2})\s*[–-]\s*(\d{1,2}:\d{2})/);
    return m ? { start: m[1], end: m[2] } : null;
  }

  function fmt(key, values) {
    return t(key).replace(/\{(\w)\}/g, function (_, k) { return values[k]; });
  }

  // Nächster Zeitpunkt, zu dem die Praxis öffnet (heute später oder an einem der nächsten Tage).
  function nextOpening(now) {
    var minutes = now.getHours() * 60 + now.getMinutes();
    var start = (now.getDay() + 6) % 7;
    for (var i = 0; i < 8; i++) {
      var day = DAYS[(start + i) % 7];
      var slots = P.hours[day] || [];
      for (var j = 0; j < slots.length; j++) {
        var r = parseSlot(slots[j]);
        if (r && (i > 0 || r.from > minutes)) return { offset: i, day: day, time: slotTimes(slots[j]).start };
      }
    }
    return null;
  }

  function statusDetail(now, slots) {
    var minutes = now.getHours() * 60 + now.getMinutes();
    for (var i = 0; i < slots.length; i++) {
      var r = parseSlot(slots[i]);
      if (r && minutes >= r.from && minutes < r.to) return fmt("status.until", { t: slotTimes(slots[i]).end });
    }
    var next = nextOpening(now);
    if (!next) return "";
    if (next.offset === 0) return fmt("status.opensAt", { t: next.time });
    var dayName = next.offset === 1 ? t("status.tomorrow") : t("day." + next.day);
    return fmt("status.nextOpen", { d: dayName, t: next.time });
  }

  function renderToday() {
    var now = new Date();
    var key = todayKey(now);
    var slots = P.hours[key] || [];
    var open = isOpen(slots, now);
    var statusKey = !slots.length ? "status.closedToday" : open ? "status.openNow" : "status.closedNow";

    each(".js-status-text, .js-status", function (node) { node.textContent = t(statusKey); });
    each(".js-status, .js-status-dot", function (node) { node.classList.toggle("is-open", open); });
    var detail = statusDetail(now, slots);
    each(".js-status-detail", function (node) { node.textContent = detail; });
    each(".js-status-short", function (node) { node.textContent = t(open ? "status.short.open" : "status.short.closed"); });
    each(".js-status-chip", function (node) {
      node.classList.toggle("is-open", open);
      node.title = t(statusKey) + (detail ? " · " + detail : "");
    });
    each(".js-today-title", function (node) { node.textContent = t("info.today") + " · " + t("day." + key); });
    each(".js-today-hours", function (node) { node.textContent = slots.length ? slots.join(" · ") : t("hours.closed"); });

    var acute = (P.acuteHours || {})[key] || [];
    each(".js-acute-today", function (node) {
      node.textContent = acute.join(" · ");
      var row = node.closest(".js-acute-row");
      if (row) row.hidden = !acute.length;
    });
  }

  // ---------------------------------------------------------------- Notices

  function renderNotices(code) {
    code = code || lang;
    var today = new Date().toISOString().slice(0, 10);
    var active = (P.notices || []).filter(function (n) { return (!n.from || n.from <= today) && (!n.to || today <= n.to); });
    each(".js-notices", function (box) {
      box.innerHTML = "";
      box.hidden = !active.length;
      active.forEach(function (n) {
        box.appendChild(el("p", { class: "container notice" }, [
          el("span", { class: "notice-label", i18n: "notice.label" }),
          el("span", { text: n.text[code] || n.text.de })
        ]));
      });
    });
  }

  // ---------------------------------------------------------------- Team & Jobs

  function renderTeam() {
    each(".js-team", function (grid) {
      grid.innerHTML = "";
      P.team.forEach(function (m) {
        if (m.role === "doctor") return; // Arzt hat einen eigenen Abschnitt
        var photo = el("div", { class: "photo photo-portrait", "data-photo": m.photo }, [
          el("span", { class: "photo-initials", text: initials(m.name) })
        ]);
        var langs = (m.langs || []).length
          ? el("p", { class: "team-langs", dir: "ltr", text: m.langs.map(function (c) { return c.toUpperCase(); }).join(" · ") })
          : null;
        grid.appendChild(el("article", { class: "team-card" }, [
          photo,
          el("h3", { text: m.name || t("team.namePending") }),
          el("p", { class: "team-role", text: t("role." + m.role) }),
          langs
        ]));
      });
      loadPhotos(grid);
    });
  }

  function initials(name) {
    if (!name) return "";
    return name.split(/\s+/).map(function (p) { return p.charAt(0); }).slice(0, 2).join("").toUpperCase();
  }

  function renderJobs() {
    each(".js-jobs", function (list) {
      list.innerHTML = "";
      var jobs = P.jobs || [];
      if (!jobs.length) {
        list.appendChild(el("article", { class: "job" }, [
          el("h3", { i18n: "jobs.open.title" }), el("p", { i18n: "jobs.open.desc" })
        ]));
        return;
      }
      jobs.forEach(function (id) {
        var apply = el("a", { class: "btn btn-primary js-mail-link", href: "mailto:", "data-subject": "job." + id + ".title", i18n: "jobs.apply" });
        list.appendChild(el("article", { class: "job" }, [
          el("p", { class: "job-meta", i18n: "job." + id + ".meta" }),
          el("h3", { i18n: "job." + id + ".title" }),
          el("p", { i18n: "job." + id + ".desc" }),
          apply
        ]));
      });
    });
  }

  // ---------------------------------------------------------------- Photos

  // Ein Foto erscheint automatisch, sobald assets/photos/<name>.jpg existiert.
  function loadPhotos(root) {
    each(".photo[data-photo]:not([data-loaded])", function (box) {
      box.setAttribute("data-loaded", "");
      var img = new Image();
      img.alt = box.getAttribute("data-alt") || "";
      img.decoding = "async";
      img.onload = function () { box.classList.add("has-img"); box.insertBefore(img, box.firstChild); };
      img.src = "assets/photos/" + box.getAttribute("data-photo") + ".jpg";
    }, root);
  }

  // ---------------------------------------------------------------- 3D-Emblem

  // Erst das Standbild (schnell sichtbar), nach dem Laden der Seite die Drehung – außer bei „Bewegung reduzieren“.
  // Startfoto: fehlt die Datei noch, zeigt der Rahmen das Praxislogo statt eines kaputten Bildes.
  function initHeroPhoto() {
    each(".js-hero-photo", function (fig) {
      var img = fig.querySelector(".hero-photo-img");
      function missing() { fig.classList.add("is-missing"); }
      if (img.complete && !img.naturalWidth) missing(); else img.addEventListener("error", missing);
    });
  }

  // ---------------------------------------------------------------- Bewegung

  // Schatten unter dem Kopf, sobald gescrollt wird.
  // Karte: Google Maps erst nach Klick laden (DSGVO). Google zentriert die Karte auf die Adresse –
  // dort sitzt der Thermometer-Pin, darum bleibt die Karte unbeweglich.
  function initMap() {
    each(".js-map-load", function (btn) {
      btn.addEventListener("click", function () {
        var map = btn.closest(".js-map");
        var frame = document.createElement("iframe");
        frame.src = "https://maps.google.com/maps?q=" + encodeURIComponent(P.street + ", " + P.city) + "&z=16&output=embed&hl=" + lang;
        frame.title = t("map.title");
        frame.setAttribute("data-i18n-attr", "title:map.title");
        frame.setAttribute("tabindex", "-1");
        frame.loading = "lazy";
        frame.referrerPolicy = "no-referrer-when-downgrade";
        var canvas = map.querySelector(".js-map-canvas");
        canvas.innerHTML = "";
        canvas.appendChild(frame);
        map.classList.add("is-loaded");
        var pin = map.querySelector(".map-pin");
        if (pin) pin.focus();
      });
    });
  }

  function initHeaderShadow() {
    var header = document.querySelector(".site-header");
    if (!header) return;
    var ticking = false;
    function update() { header.classList.toggle("is-scrolled", window.scrollY > 8); ticking = false; }
    window.addEventListener("scroll", function () {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }, { passive: true });
    update();
  }

  // Abschnitte unterhalb des ersten Bildschirms blenden sanft ein; Karten nacheinander (40 ms Versatz).
  function initReveal() {
    if (!("IntersectionObserver" in window) || (window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches)) return;
    var items = document.querySelectorAll(
      "main .section .section-head, main .section .card, main .section .route, main .section .greeting, " +
      "main .section .steps > li, main .section .panel, main .section .photo, main .section .contact-card"
    );
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        el.classList.add("is-in");
        observer.unobserve(el);
        // danach Klassen entfernen, damit Hover-Effekte wieder greifen
        setTimeout(function () { el.classList.remove("reveal", "is-in"); el.style.removeProperty("--reveal-delay"); }, 900);
      });
    }, { rootMargin: "0px 0px -8% 0px" });
    Array.prototype.forEach.call(items, function (el) {
      if (el.getBoundingClientRect().top < window.innerHeight) return; // schon sichtbar: nicht verstecken
      var index = Array.prototype.indexOf.call(el.parentNode.children, el);
      el.style.setProperty("--reveal-delay", Math.min(index, 6) * 40 + "ms");
      el.classList.add("reveal");
      observer.observe(el);
    });
  }

  // ---------------------------------------------------------------- Navigation

  function initNav() {
    var toggle = document.querySelector(".nav-toggle");
    if (!toggle) return;
    function setOpen(open) {
      toggle.setAttribute("aria-expanded", String(open));
      document.body.classList.toggle("nav-open", open);
    }
    toggle.addEventListener("click", function () { setOpen(toggle.getAttribute("aria-expanded") !== "true"); });
    document.getElementById("main-nav").addEventListener("click", function (e) { if (e.target.tagName === "A") setOpen(false); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") setOpen(false); });
  }

  // ---------------------------------------------------------------- Boot

  function renderDynamic() {
    renderHours();
    renderToday();
    renderNotices();
    renderTeam();
    renderJobs();
    renderMailLinks();
  }

  // Sprachdatei der Startsprache noch während des Ladens blockierend nachladen: So ist sie bei DOMContentLoaded
  // schon da und die Seite wechselt die Sprache vor dem ersten Bild statt danach (kein Verrutschen).
  (function () {
    var first = initialLang();
    // Andere Startsprache: Seite erst zeigen, wenn übersetzt ist (kein Aufblitzen der deutschen Texte, kein Verrutschen).
    if (first !== "de") {
      document.documentElement.classList.add("i18n-pending");
      setTimeout(function () { document.documentElement.classList.remove("i18n-pending"); }, 3000);
    }
    var FONTS = { uk: "source-sans-3-cyrillic", ar: "noto-sans-arabic-arabic" };
    if (FONTS[first]) ["400", "700"].forEach(function (w) {
      var l = document.createElement("link");
      l.rel = "preload"; l.as = "font"; l.type = "font/woff2"; l.crossOrigin = "anonymous";
      l.href = "assets/fonts/" + FONTS[first] + "-" + w + "-normal.woff2";
      document.head.appendChild(l);
    });
    if (!I18N[first] && document.readyState === "loading") document.write('<script src="js/lang/' + first + '.js"><\/script>');
  })();

  renderHeader();
  // Hinweise sofort zeigen (Text steht in config.js), damit der Inhalt darunter nicht nachträglich verrutscht.
  renderNotices(initialLang());

  document.addEventListener("DOMContentLoaded", function () {
    renderFooter();
    renderContact();
    renderPaletteSwitch();
    initNav();
    loadPhotos();
    initHeroPhoto();
    initHeaderShadow();
    initMap();
    initReveal();
    initLangMenu();
    document.addEventListener("click", keepLangInLinks);
    setLang(initialLang());
    setInterval(renderToday, 60 * 1000);
  });
})();
