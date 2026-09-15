/* RE・BORN hair & relax — motion (intro curtain, hero, reveals, parallax, header) */
(function () {
  'use strict';
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* intro curtain: once per browser session, index only */
  var intro = document.getElementById('intro');
  var hero = document.querySelector('.hero');
  function goLive() { if (hero) hero.classList.add('live'); }
  if (intro) {
    var seen = false;
    try { seen = sessionStorage.getItem('rb_intro') === '1'; } catch (e) { /* ignore */ }
    if (seen || reduce) {
      intro.parentNode.removeChild(intro);
      requestAnimationFrame(goLive);
    } else {
      document.body.classList.add('intro-lock');
      try { sessionStorage.setItem('rb_intro', '1'); } catch (e) { /* ignore */ }
      setTimeout(function () {
        intro.classList.add('out');
        document.body.classList.remove('intro-lock');
        setTimeout(goLive, 150);
        setTimeout(function () { if (intro.parentNode) intro.parentNode.removeChild(intro); }, 900);
      }, 1150);
    }
  } else {
    requestAnimationFrame(goLive);
  }

  /* reveal on scroll for wipe-in photos, staggered grids and section heads */
  var targets = Array.prototype.slice.call(document.querySelectorAll('.rv-img, .stagger, .sec-head'));
  // reveal only what is at/near the viewport now; elements further down wait for the scroll (never a blanket reveal)
  function revealInView() {
    var limit = window.innerHeight * 1.12;
    targets = targets.filter(function (el) {
      if (el.getBoundingClientRect().top < limit) { el.classList.add('in'); return false; }
      return true;
    });
  }
  if (reduce || !('IntersectionObserver' in window)) {
    if (reduce) { targets.forEach(function (el) { el.classList.add('in'); }); targets = []; }
    else { revealInView(); window.addEventListener('scroll', revealInView, { passive: true }); }
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px 12% 0px', threshold: 0 });
    targets.forEach(function (el) { io.observe(el); });
    // safety for a stalled observer: only elements already on screen, checked on a timer and on scroll
    setTimeout(revealInView, 900);
    window.addEventListener('scroll', function () { if (targets.length) revealInView(); }, { passive: true });
  }

  /* parallax (transform only, rAF-throttled) */
  var plx = Array.prototype.slice.call(document.querySelectorAll('.plx'));
  var header = document.querySelector('.header');
  var ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      var y = window.scrollY || window.pageYOffset;
      if (header) header.classList.toggle('scrolled', y > 24);
      if (!reduce) {
        plx.forEach(function (el) {
          var box = el.parentNode.getBoundingClientRect();
          if (box.bottom < 0 || box.top > window.innerHeight) return;
          var rel = (box.top + box.height / 2 - window.innerHeight / 2) / window.innerHeight; // -1..1
          el.style.transform = 'translate3d(0,' + (rel * -8).toFixed(2) + '%,0) scale(1.18)';
        });
      }
      ticking = false;
    });
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  onScroll();
})();
