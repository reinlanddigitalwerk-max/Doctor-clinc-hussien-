(function () {
  "use strict";

  var P = window.PRAXIS;
  var I18N = window.I18N;
  var LANGS = ["de", "ar", "uk", "ro", "en"];
  var RTL = ["ar"];
  var DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"];
  var STORAGE_KEY = "praxis-lang";

  var lang = "de";

  function t(key) {
    var dict = I18N[lang] || I18N.de;
    return dict[key] != null ? dict[key] : (I18N.de[key] != null ? I18N.de[key] : key);
  }

  function each(selector, fn) {
    Array.prototype.forEach.call(document.querySelectorAll(selector), fn);
  }

  function telHref(phone) {
    var digits = phone.replace(/[^\d+]/g, "");
    if (digits.charAt(0) === "0") digits = "+49" + digits.slice(1);
    return "tel:" + digits;
  }

  // ---- Language ----

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

  function applyLang(next) {
    lang = next;
    var root = document.documentElement;
    root.lang = lang;
    root.dir = RTL.indexOf(lang) !== -1 ? "rtl" : "ltr";

    each("[data-i18n]", function (el) {
      el.textContent = t(el.getAttribute("data-i18n"));
    });
    each("[data-i18n-attr]", function (el) {
      var parts = el.getAttribute("data-i18n-attr").split(":");
      el.setAttribute(parts[0], t(parts[1]));
    });

    document.getElementById("lang-switch").value = lang;
    try { localStorage.setItem(STORAGE_KEY, lang); } catch (e) { /* ignore */ }

    renderHours();
    renderToday();
    renderMailLinks();
  }

  // ---- Practice data ----

  function renderContact() {
    var address = P.street + ", " + P.city;
    each(".js-address", function (el) {
      el.innerHTML = "";
      el.appendChild(document.createTextNode(P.street));
      el.appendChild(document.createElement("br"));
      el.appendChild(document.createTextNode(P.city));
    });
    each(".js-phone", function (el) { el.textContent = P.phone; });
    each(".js-phone-link", function (el) { el.href = telHref(P.phone); });
    each(".js-email", function (el) { el.textContent = P.email; });
    each(".js-fax", function (el) { el.textContent = P.fax; });
    each(".js-fax-row", function (el) { el.hidden = !P.fax; });

    each(".js-route", function (el) {
      el.href = "https://www.google.com/maps/dir/?api=1&destination=" + encodeURIComponent(P.name + ", " + address);
    });

    each(".js-book", function (el) {
      if (P.bookingUrl) {
        el.href = P.bookingUrl;
        el.target = "_blank";
        el.rel = "noopener";
      } else {
        el.href = telHref(P.phone);
      }
    });

    each(".js-year", function (el) { el.textContent = new Date().getFullYear(); });
  }

  function renderMailLinks() {
    var subject = encodeURIComponent(t("expert.mailSubject"));
    each(".js-mail-link", function (el) {
      el.href = "mailto:" + P.email + (el.closest("#gutachten") ? "?subject=" + subject : "");
    });
  }

  // ---- Opening hours ----

  // JS getDay(): 0 = Sunday … 6 = Saturday → index into DAYS
  function todayKey(now) {
    return DAYS[(now.getDay() + 6) % 7];
  }

  function parseSlot(slot) {
    var m = slot.match(/(\d{1,2}):(\d{2})\s*[–-]\s*(\d{1,2}):(\d{2})/);
    if (!m) return null;
    return { from: +m[1] * 60 + +m[2], to: +m[3] * 60 + +m[4] };
  }

  function renderHours() {
    var body = document.querySelector(".js-hours");
    var today = todayKey(new Date());
    body.innerHTML = "";
    DAYS.forEach(function (day) {
      var slots = P.hours[day] || [];
      var tr = document.createElement("tr");
      if (day === today) tr.className = "is-today";
      var th = document.createElement("th");
      th.scope = "row";
      th.textContent = t("day." + day);
      var td = document.createElement("td");
      if (slots.length) {
        slots.forEach(function (s) {
          var span = document.createElement("span");
          span.textContent = s;
          span.dir = "ltr";
          td.appendChild(span);
        });
      } else {
        td.textContent = t("hours.closed");
        td.className = "closed";
      }
      tr.appendChild(th);
      tr.appendChild(td);
      body.appendChild(tr);
    });
  }

  function renderToday() {
    var now = new Date();
    var key = todayKey(now);
    var slots = P.hours[key] || [];
    var minutes = now.getHours() * 60 + now.getMinutes();
    var openNow = slots.some(function (s) {
      var r = parseSlot(s);
      return r && minutes >= r.from && minutes < r.to;
    });

    var statusKey = !slots.length ? "status.closedToday" : openNow ? "status.openNow" : "status.closedNow";
    each(".js-status", function (el) {
      el.textContent = t(statusKey);
      el.classList.toggle("is-open", openNow);
    });
    each(".js-today-title", function (el) {
      el.textContent = t("info.today") + " · " + t("day." + key);
    });
    each(".js-today-hours", function (el) {
      el.textContent = slots.length ? slots.join("  ·  ") : t("hours.closed");
      el.dir = "ltr";
    });
  }

  // ---- Navigation ----

  function initNav() {
    var toggle = document.querySelector(".nav-toggle");
    var nav = document.getElementById("main-nav");
    function setOpen(open) {
      toggle.setAttribute("aria-expanded", String(open));
      document.body.classList.toggle("nav-open", open);
    }
    toggle.addEventListener("click", function () {
      setOpen(toggle.getAttribute("aria-expanded") !== "true");
    });
    nav.addEventListener("click", function (e) {
      if (e.target.tagName === "A") setOpen(false);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") setOpen(false);
    });
  }

  document.getElementById("lang-switch").addEventListener("change", function (e) {
    applyLang(e.target.value);
  });

  renderContact();
  initNav();
  applyLang(initialLang());
  setInterval(renderToday, 60 * 1000);
})();
