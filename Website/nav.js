/* Site-wide nav bar — one solid, always-visible menu bar for every page.
   Include with <script src="nav.js"></script> (or ../nav.js from adult/).
   Detects its own path depth and theme: pages under /adult/ get the navy bar.

   i18n: labels fork EN/ES via gywbtLang() (the same ~6-line helper duplicated
   in index.html/story-config.js/adult-config.js — reads localStorage
   ['gywbt-lang'], with a ?lang=en|es URL override that wins and re-stores).
   Labels are looked up by a stable `key`, not by the displayed text, so the
   inline-vs-menu filter and the "is-here" matching stay language-agnostic.
   EN is unchanged byte-for-byte from before this pass — the ES branch is
   purely additive. */
(function () {
  "use strict";

  function gywbtLang() {
    var m = /[?&]lang=(en|es)/.exec(location.search);
  if (m) return m[1];
  return 'en';   // no stored preference (user direction): explicit ?lang= only
  }

  var path = location.pathname;
  var inAdult = /\/adult\//.test(path);
  var root = inAdult ? "../" : "";
  var adult = inAdult ? "" : "adult/";
  var file = path.split("/").pop() || "index.html";
  var dark = inAdult;
  var lang = gywbtLang();

  var NAV_LABELS = {
    en: { home: "Home", story: "Story", crashers: "Crashers", store: "Party Store",
          hire: "Hire the Crew", mission: "Our Mission", irl: "In Real Life", crew: "The Crew",
          menu: "Menu", brandHome: "Glad You Were Born Today — home" },
    es: { home: "Inicio", story: "Historia", crashers: "Los Crashers", store: "La Tienda de Fiestas",
          hire: "Contrata a la Tripulación", mission: "Nuestra Misión", irl: "En la Vida Real", crew: "La Tripulación",
          menu: "Menú", brandHome: "Glad You Were Born Today — inicio" },
  };
  var T = NAV_LABELS[lang];

  var LINKS = [
    { key: "home",     label: T.home,     href: root + "index.html",  match: !inAdult && file === "index.html" },
    { key: "story",    label: T.story,    href: root + "story.html",  match: file === "story.html" },
    { key: "crashers", label: T.crashers, href: root + "crashers.html", match: file === "crashers.html" },
    { key: "store",    label: T.store,    href: root + "store.html",  match: file === "store.html" },
    { key: "hire",     label: T.hire,     href: root + "hire.html",   match: file === "hire.html" },
    { key: "mission",  label: T.mission,  href: root + "mission.html", match: file === "mission.html" },
    { key: "irl",      label: T.irl,      href: adult || "index.html", match: inAdult && file === "index.html" },
    { key: "crew",     label: T.crew,     href: adult + "crew.html",  match: file === "crew.html" },
  ];
  // No stored preference: a page that resolved Spanish (?lang=es) forwards
  // the choice explicitly on every nav link, so the language survives
  // navigation without any storage. Brand link stays clean - the envelope
  // always greets in English.
  if (lang === 'es') LINKS.forEach(function (l) {
    if (l.key === 'home') return;   // the envelope ALWAYS greets in English
    l.href += (l.href.indexOf('?') >= 0 ? '&' : '?') + 'lang=es';
  });
  // the bar shows the essentials inline; the menu always carries everything
  var INLINE = ["story", "crashers", "store", "hire", "mission"];

  var css = [
    "body{padding-top:56px;}",
    ".gnav{position:fixed;top:0;left:0;right:0;z-index:1000;height:56px;display:flex;align-items:center;",
    "  justify-content:space-between;gap:12px;padding:0 clamp(14px,4vw,40px);",
    "  font-family:'Baloo 2',ui-rounded,'SF Pro Rounded','Segoe UI',system-ui,sans-serif;",
    "  background:rgba(255,253,246,.92);-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);",
    "  border-bottom:1px solid rgba(201,162,39,.35);box-shadow:0 4px 18px rgba(29,43,80,.10);}",
    ".gnav--dark{background:rgba(18,27,52,.92);border-bottom-color:rgba(230,196,106,.35);box-shadow:0 4px 18px rgba(0,0,0,.35);}",
    ".gnav a{text-decoration:none;}",
    ".gnav__brand{display:flex;align-items:center;gap:9px;color:#1D2B50;font-weight:700;font-size:1.02rem;white-space:nowrap;min-width:0;}",
    ".gnav--dark .gnav__brand{color:#FFF9EE;}",
    ".gnav__brand b{overflow:hidden;text-overflow:ellipsis;}",
    ".gnav__mark{flex:none;width:33px;height:33px;object-fit:contain;",
    "  filter:drop-shadow(0 2px 6px rgba(29,43,80,.22));}",
    ".gnav--dark .gnav__mark{filter:drop-shadow(0 2px 6px rgba(0,0,0,.45));}",
    ".gnav__links{display:flex;align-items:center;gap:2px;}",
    ".gnav__links a{color:#3E5580;font-weight:600;font-size:.88rem;padding:7px 11px;border-radius:999px;white-space:nowrap;}",
    ".gnav__links a:hover{background:rgba(29,43,80,.08);color:#1D2B50;}",
    ".gnav--dark .gnav__links a{color:#c9c4d8;}",
    ".gnav--dark .gnav__links a:hover{background:rgba(255,255,255,.10);color:#fff;}",
    ".gnav__links a.is-here{background:#1D2B50;color:#fff;}",
    ".gnav--dark .gnav__links a.is-here{background:#e6c46a;color:#1D2B50;}",
    ".gnav__burger{flex:none;display:flex;flex-direction:column;justify-content:center;gap:4px;width:42px;height:42px;",
    "  padding:0 10px;border:1px solid rgba(29,43,80,.22);border-radius:12px;background:transparent;cursor:pointer;}",
    ".gnav__burger i{display:block;height:2px;border-radius:2px;background:#1D2B50;transition:transform .2s ease,opacity .2s ease;}",
    ".gnav--dark .gnav__burger{border-color:rgba(255,255,255,.28);}",
    ".gnav--dark .gnav__burger i{background:#FFF9EE;}",
    ".gnav__burger[aria-expanded=true] i:nth-child(1){transform:translateY(6px) rotate(45deg);}",
    ".gnav__burger[aria-expanded=true] i:nth-child(2){opacity:0;}",
    ".gnav__burger[aria-expanded=true] i:nth-child(3){transform:translateY(-6px) rotate(-45deg);}",
    ".gnav__burger:focus-visible{outline:3px solid #FFC93C;outline-offset:2px;}",
    ".gnav__panel{position:fixed;top:56px;left:0;right:0;z-index:999;display:none;flex-direction:column;padding:10px clamp(14px,4vw,40px) 16px;",
    "  background:rgba(255,253,246,.97);-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);",
    "  border-bottom:1px solid rgba(201,162,39,.35);box-shadow:0 18px 30px rgba(29,43,80,.18);",
    "  font-family:'Baloo 2',ui-rounded,'SF Pro Rounded','Segoe UI',system-ui,sans-serif;}",
    ".gnav__panel.open{display:flex;}",
    ".gnav__panel a{color:#1D2B50;font-weight:600;font-size:1.02rem;padding:12px 6px;border-bottom:1px solid rgba(29,43,80,.08);}",
    ".gnav__panel a:last-child{border-bottom:0;}",
    ".gnav__panel a.is-here{color:#E84A9B;}",
    ".gnav--darkpanel{background:rgba(18,27,52,.97);border-bottom-color:rgba(230,196,106,.35);}",
    ".gnav--darkpanel a{color:#FFF9EE;border-bottom-color:rgba(255,255,255,.08);}",
    ".gnav--darkpanel a.is-here{color:#e6c46a;}",
    "@media (max-width:1080px){.gnav__links{display:none;}}",
    "@media (min-width:1081px){.gnav__burger{display:none;}.gnav__panel{display:none !important;}}",
    "a.gnav__skip{position:absolute;left:-9999px;}",
  ].join("\n");

  function el(tag, cls) { var n = document.createElement(tag); if (cls) n.className = cls; return n; }

  function build() {
    var style = document.createElement("style");
    style.textContent = css;
    document.head.appendChild(style);

    // Site icon on every page that carries the nav (the envelope page sets
    // its own <link> tags in markup — it doesn't load nav.js).
    var fav = document.createElement("link");
    fav.rel = "icon"; fav.type = "image/png"; fav.href = "/assets/favicon.png?v=1";
    document.head.appendChild(fav);
    var ati = document.createElement("link");
    ati.rel = "apple-touch-icon"; ati.href = "/assets/apple-touch-icon.png?v=1";
    document.head.appendChild(ati);

    var bar = el("header", "gnav" + (dark ? " gnav--dark" : ""));

    var brand = el("a", "gnav__brand");
    brand.href = root + "index.html";
    brand.setAttribute("aria-label", T.brandHome);
    var mark = document.createElement("img");
    mark.className = "gnav__mark";
    mark.src = "/assets/logo.webp?v=1";
    mark.alt = "";
    brand.appendChild(mark);
    bar.appendChild(brand);

    var links = el("nav", "gnav__links");
    LINKS.forEach(function (l) {
      if (INLINE.indexOf(l.key) < 0) return;
      var a = document.createElement("a");
      a.href = l.href; a.textContent = l.label;
      if (l.match) a.className = "is-here";
      links.appendChild(a);
    });
    bar.appendChild(links);

    var burger = el("button", "gnav__burger");
    burger.setAttribute("aria-label", T.menu);
    burger.setAttribute("aria-expanded", "false");
    burger.appendChild(document.createElement("i"));
    burger.appendChild(document.createElement("i"));
    burger.appendChild(document.createElement("i"));
    bar.appendChild(burger);

    var panel = el("nav", "gnav__panel" + (dark ? " gnav--darkpanel" : ""));
    LINKS.forEach(function (l) {
      var a = document.createElement("a");
      a.href = l.href; a.textContent = l.label;
      if (l.match) a.className = "is-here";
      panel.appendChild(a);
    });

    function setOpen(open) {
      burger.setAttribute("aria-expanded", open ? "true" : "false");
      panel.classList.toggle("open", open);
    }
    burger.addEventListener("click", function () {
      setOpen(burger.getAttribute("aria-expanded") !== "true");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") setOpen(false);
    });
    document.addEventListener("click", function (e) {
      if (!panel.contains(e.target) && !burger.contains(e.target)) setOpen(false);
    });

    document.body.insertBefore(panel, document.body.firstChild);
    document.body.insertBefore(bar, document.body.firstChild);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", build);
  } else {
    build();
  }
})();
