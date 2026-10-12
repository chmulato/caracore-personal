(function () {
  'use strict';

  var productionHosts = ['personal.caracore.com.br', 'www.caracore.com.br', 'caracore.com.br'];
  if (window.location.protocol === 'file:' || productionHosts.indexOf(window.location.hostname) === -1) {
    return;
  }

  var measurementId = 'G-MKFC9G3CL0';
  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () {
    window.dataLayer.push(arguments);
  };

  // Enfileira a configuração e pageview imediatamente no dataLayer (sem perda de métricas)
  window.gtag('js', new Date());
  window.gtag('config', measurementId, {
    page_title: document.title,
    page_location: window.location.href,
    cookie_domain: '.caracore.com.br',
    cookie_flags: 'SameSite=None;Secure',
    cookie_update: true,
    anonymize_ip: true,
    send_page_view: true,
    linker: {
      domains: ['caracore.com.br', 'personal.caracore.com.br']
    }
  });

  // Carrega o script externo do GTM de forma diferida para não bloquear a thread principal mobile
  var loaded = false;
  function loadGtag() {
    if (loaded) return;
    loaded = true;
    var script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(measurementId);
    script.setAttribute('data-caracore-ga4', 'true');
    document.head.appendChild(script);
  }

  var interactionEvents = ['scroll', 'touchstart', 'pointerdown', 'keydown', 'mousemove'];
  function onUserInteraction() {
    interactionEvents.forEach(function (e) {
      window.removeEventListener(e, onUserInteraction, { passive: true });
    });
    loadGtag();
  }

  interactionEvents.forEach(function (e) {
    window.addEventListener(e, onUserInteraction, { passive: true, once: true });
  });

  // Fallback para tráfego sem interação humana (executa quando o navegador estiver ocioso)
  if ('requestIdleCallback' in window) {
    window.requestIdleCallback(function () {
      setTimeout(loadGtag, 3500);
    }, { timeout: 5000 });
  } else {
    setTimeout(loadGtag, 4000);
  }
})();
