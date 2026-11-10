/**
 * Tag padrão do Google Analytics 4 do ecossistema Cara Core no blog pessoal.
 *
 * Mesma trava da matriz: Consent Mode v2 com `analytics_storage` negado até o
 * aceite explícito (`cc-ga-consent`). Sem aceite não há download do gtag.js
 * nem cookie `_ga`.
 */
(function () {
  'use strict';

  var productionHosts = ['personal.caracore.com.br', 'www.caracore.com.br', 'caracore.com.br'];
  if (window.location.protocol === 'file:' || productionHosts.indexOf(window.location.hostname) === -1) {
    return;
  }

  var MEASUREMENT_ID = 'G-MKFC9G3CL0';
  var CONSENT_KEY = 'cc-ga-consent';
  var CONSENT_DATE_KEY = 'cc-ga-consent-date';
  var LEGACY_KEY = 'lgpd-consent';
  var COOKIE_DOMAIN = '.caracore.com.br';
  var PRIVACY_URL = 'https://caracore.com.br/politica/politica-privacidade.html';
  var BANNER_STYLE_ID = 'cc-consent-style';

  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () {
    window.dataLayer.push(arguments);
  };

  function readConsent() {
    try {
      var stored = localStorage.getItem(CONSENT_KEY);
      if (stored === 'granted' || stored === 'denied') {
        return stored;
      }
      var legacy = localStorage.getItem(LEGACY_KEY);
      if (legacy === 'accepted') {
        return 'granted';
      }
      if (legacy === 'declined') {
        return 'denied';
      }
    } catch (error) {
      /* localStorage indisponível: trata como sem decisão */
    }
    return null;
  }

  var initialConsent = readConsent();
  var tagLoaded = false;

  window.gtag('consent', 'default', {
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied',
    analytics_storage: initialConsent === 'granted' ? 'granted' : 'denied',
    functionality_storage: 'granted',
    security_storage: 'granted',
    wait_for_update: 500
  });

  window.gtag('js', new Date());
  window.gtag('config', MEASUREMENT_ID, {
    page_title: document.title,
    page_location: window.location.href,
    cookie_domain: COOKIE_DOMAIN,
    anonymize_ip: true,
    send_page_view: true,
    linker: { domains: ['caracore.com.br', 'personal.caracore.com.br'] }
  });

  function loadTag() {
    if (tagLoaded || readConsent() !== 'granted') {
      return;
    }
    tagLoaded = true;
    var script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(MEASUREMENT_ID);
    script.setAttribute('data-caracore-ga4', 'true');
    document.head.appendChild(script);
  }

  /* Só baixa o gtag.js depois de interação ou de o navegador ficar ocioso:
     poupa LCP/TBT em 4G, já que o dataLayer enfileira tudo até lá. */
  function scheduleLoad() {
    if (readConsent() !== 'granted') {
      return;
    }
    var interactionEvents = ['scroll', 'touchstart', 'pointerdown', 'keydown', 'mousemove'];
    function onFirstInteraction() {
      interactionEvents.forEach(function (eventName) {
        window.removeEventListener(eventName, onFirstInteraction);
      });
      loadTag();
    }
    interactionEvents.forEach(function (eventName) {
      window.addEventListener(eventName, onFirstInteraction, { passive: true });
    });

    if ('requestIdleCallback' in window) {
      window.requestIdleCallback(function () {
        setTimeout(loadTag, 3500);
      }, { timeout: 5000 });
    } else {
      setTimeout(loadTag, 4000);
    }
  }

  function deleteAnalyticsCookies() {
    if (!document.cookie) {
      return;
    }
    var hosts = [COOKIE_DOMAIN, window.location.hostname];
    document.cookie.split(';').forEach(function (entry) {
      var name = entry.split('=')[0].trim();
      if (!/^(_ga|_gid|_gat)/.test(name)) {
        return;
      }
      hosts.forEach(function (host) {
        document.cookie = name + '=; Max-Age=0; path=/; domain=' + host + '; SameSite=None; Secure';
      });
      document.cookie = name + '=; Max-Age=0; path=/';
    });
  }

  function setConsent(value) {
    try {
      localStorage.setItem(CONSENT_KEY, value);
      localStorage.setItem(CONSENT_DATE_KEY, new Date().toISOString());
      localStorage.removeItem(LEGACY_KEY);
    } catch (error) {
      /* sem persistência o aceite vale só para esta página */
    }

    window.gtag('consent', 'update', {
      ad_storage: 'denied',
      ad_user_data: 'denied',
      ad_personalization: 'denied',
      analytics_storage: value === 'granted' ? 'granted' : 'denied'
    });

    if (value === 'granted') {
      tagLoaded = false;
      loadTag();
    } else {
      deleteAnalyticsCookies();
    }

    hideBanner();
  }

  function ensureBannerStyles() {
    if (document.getElementById(BANNER_STYLE_ID)) {
      return;
    }
    var style = document.createElement('style');
    style.id = BANNER_STYLE_ID;
    style.textContent = [
      '.cc-consent{position:fixed;left:0;right:0;bottom:0;z-index:9999;background:#0f172a;color:#f8fafc;',
      'display:flex;gap:0.85rem;align-items:center;justify-content:center;flex-wrap:wrap;',
      'padding:0.9rem 1.1rem;box-shadow:0 -4px 18px rgba(0,0,0,.28);',
      'font:14px/1.45 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}',
      '.cc-consent p{margin:0;max-width:44rem}',
      '.cc-consent a{color:#93c5fd}',
      '.cc-consent button{font:inherit;font-weight:600;min-height:44px;padding:0.55rem 1.2rem;',
      'border-radius:999px;border:1px solid #93c5fd;cursor:pointer}',
      '.cc-consent .cc-accept{background:#2563eb;border-color:#2563eb;color:#fff}',
      '.cc-consent .cc-decline{background:transparent;color:#f8fafc}',
      '.cc-consent button:focus-visible{outline:3px solid #93c5fd;outline-offset:2px}'
    ].join('');
    document.head.appendChild(style);
  }

  function hideBanner() {
    var banner = document.getElementById('cc-consent');
    if (banner) {
      banner.parentNode.removeChild(banner);
    }
  }

  function showBanner() {
    if (document.getElementById('cc-consent')) {
      return;
    }
    ensureBannerStyles();

    var banner = document.createElement('div');
    banner.id = 'cc-consent';
    banner.className = 'cc-consent';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-live', 'polite');
    banner.setAttribute('aria-label', 'Preferências de medição de audiência');

    var text = document.createElement('p');
    text.appendChild(document.createTextNode('Medimos a audiência com Google Analytics para saber quais páginas são úteis. '));
    var link = document.createElement('a');
    link.href = PRIVACY_URL;
    link.textContent = 'Política de Privacidade';
    text.appendChild(link);
    text.appendChild(document.createTextNode('. Você pode recusar; o site funciona do mesmo jeito.'));

    var accept = document.createElement('button');
    accept.type = 'button';
    accept.className = 'cc-accept';
    accept.textContent = 'Aceitar';
    accept.addEventListener('click', function () {
      setConsent('granted');
    });

    var decline = document.createElement('button');
    decline.type = 'button';
    decline.className = 'cc-decline';
    decline.textContent = 'Recusar';
    decline.addEventListener('click', function () {
      setConsent('denied');
    });

    banner.appendChild(text);
    banner.appendChild(accept);
    banner.appendChild(decline);
    document.body.appendChild(banner);
  }

  function start() {
    if (initialConsent === null) {
      showBanner();
      return;
    }
    scheduleLoad();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
