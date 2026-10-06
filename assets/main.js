/* RE・BORN hair & relax — site scripts (mock v2) */
(function () {
  'use strict';
  document.documentElement.classList.remove('no-js');
  document.documentElement.classList.add('js');

  /* mobile nav */
  var burger = document.querySelector('.burger');
  var drawer = document.querySelector('.drawer');
  var behind = Array.prototype.slice.call(document.querySelectorAll('main, footer, .stickybar'));
  function setNav(open) {
    drawer.classList.toggle('open', open);
    document.body.classList.toggle('nav-open', open);
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    burger.setAttribute('aria-label', open ? 'メニューを閉じる' : 'メニューを開く');
    // while the drawer is open, everything behind it leaves the tab order; on close, focus returns to the button
    behind.forEach(function (el) { if (open) el.setAttribute('inert', ''); else el.removeAttribute('inert'); });
    if (open) { drawer.removeAttribute('inert'); drawer.querySelector('a').focus(); }
    else { drawer.setAttribute('inert', ''); burger.focus(); }
  }
  if (burger && drawer) {
    drawer.setAttribute('inert', '');
    burger.addEventListener('click', function () { setNav(!drawer.classList.contains('open')); });
    drawer.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', function () { setNav(false); }); });
    document.addEventListener('keydown', function (ev) {
      if (ev.key === 'Escape' && drawer.classList.contains('open')) { setNav(false); }
    });
    // if the viewport grows past the mobile breakpoint while the drawer is open, the drawer and burger
    // disappear via CSS: release the background so the visible page stays usable
    if (window.matchMedia) {
      var mq = window.matchMedia('(min-width: 961px)');
      var onWide = function (e) {
        if (e.matches && drawer.classList.contains('open')) {
          setNav(false);
          var navLink = document.querySelector('.nav a');
          if (navLink) navLink.focus();
        }
      };
      if (mq.addEventListener) mq.addEventListener('change', onWide); else if (mq.addListener) mq.addListener(onWide);
      // belt and braces: some embedded/emulated viewports resize without firing the media-query change event
      window.addEventListener('resize', function () { onWide({ matches: window.innerWidth >= 961 }); });
    }
  }

  /* scroll reveal (elements start visible when JS is off; see .js .rv in CSS) */
  var rv = Array.prototype.slice.call(document.querySelectorAll('.rv'));
  function revealInView() {
    var limit = window.innerHeight * 1.12;
    rv = rv.filter(function (el) {
      if (el.getBoundingClientRect().top < limit) { el.classList.add('in'); return false; }
      return true;
    });
  }
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px 12% 0px', threshold: 0 });
    rv.forEach(function (el) { io.observe(el); });
    /* safety for a stalled observer: reveal only what is on screen now (never everything at once) */
    setTimeout(revealInView, 900);
    window.addEventListener('scroll', function () { if (rv.length) revealInView(); }, { passive: true });
  } else {
    revealInView();
    window.addEventListener('scroll', revealInView, { passive: true });
  }

  /* orphan killer: a paragraph whose last line holds only 1-3 characters gets a little right padding
     so the text re-wraps with a fuller last line (runs after fonts load and on resize) */
  function lineWidths(el) {
    var rects = [];
    var walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, null);
    var n;
    while ((n = walker.nextNode())) {
      if (!n.textContent.trim()) continue;
      var r = document.createRange(); r.selectNodeContents(n);
      Array.prototype.push.apply(rects, r.getClientRects());
    }
    var lines = {};
    rects.forEach(function (rc) {
      if (rc.width < 1) return;
      var k = Math.round(rc.top / 6);
      if (!lines[k]) lines[k] = { l: rc.left, r: rc.right };
      lines[k].l = Math.min(lines[k].l, rc.left); lines[k].r = Math.max(lines[k].r, rc.right);
    });
    return Object.keys(lines).sort(function (a, b) { return a - b; }).map(function (k) { return lines[k].r - lines[k].l; });
  }
  function fixOrphans() {
    var els = document.querySelectorAll('p, li, dd, dt, td, summary, figcaption, h1, h2, h3, .lead, .sub, .hint, .meta span, .faq .a');
    Array.prototype.forEach.call(els, function (el) {
      if (el.closest('.btn, .marquee, .stickybar, table, .nav, .drawer, .intro')) return;
      if (el.getAttribute('data-orphan') === 'skip') return;
      el.style.paddingRight = '';
      if ((el.textContent || '').trim().length < 8) return;
      var width = el.getBoundingClientRect().width;
      if (width < 80) return;
      for (var pad = 0; pad <= 24; pad += 2) {
        if (pad) el.style.paddingRight = pad + '%';
        var ws = lineWidths(el);
        if (ws.length < 2) break;
        if (ws[ws.length - 1] >= width * 0.2) break;
        if (pad === 24) el.style.paddingRight = '';
      }
    });
  }
  var orphanTimer;
  function scheduleOrphans() { clearTimeout(orphanTimer); orphanTimer = setTimeout(fixOrphans, 120); }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(scheduleOrphans); else scheduleOrphans();
  window.addEventListener('load', scheduleOrphans);
  window.addEventListener('resize', scheduleOrphans);
  window.fixOrphans = fixOrphans;

  /* lightbox (gallery) — native <dialog> for focus trapping */
  var links = Array.prototype.slice.call(document.querySelectorAll('.gallery a'));
  var lb = document.querySelector('dialog.lightbox');
  if (links.length && lb && typeof lb.showModal === 'function') {
    var img = lb.querySelector('img');
    var idx = 0;
    function show(i) {
      idx = (i + links.length) % links.length;
      img.src = links[idx].getAttribute('href');
      img.alt = links[idx].querySelector('img').alt || '';
      if (!lb.open) lb.showModal();
    }
    links.forEach(function (a, i) {
      a.addEventListener('click', function (ev) { ev.preventDefault(); show(i); });
    });
    lb.querySelector('.close').addEventListener('click', function () { lb.close(); });
    lb.querySelector('.prev').addEventListener('click', function () { show(idx - 1); });
    lb.querySelector('.next').addEventListener('click', function () { show(idx + 1); });
    lb.addEventListener('click', function (ev) { if (ev.target === lb) lb.close(); });
    lb.addEventListener('keydown', function (ev) {
      if (ev.key === 'ArrowLeft') show(idx - 1);
      if (ev.key === 'ArrowRight') show(idx + 1);
    });
    lb.addEventListener('close', function () { img.removeAttribute('src'); });
  }

})();
