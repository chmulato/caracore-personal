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

  var script = document.createElement('script');
  script.async = true;
  script.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(measurementId);
  script.setAttribute('data-caracore-ga4', 'true');
  document.head.appendChild(script);

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
})();
