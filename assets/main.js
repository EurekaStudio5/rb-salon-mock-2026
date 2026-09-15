/* RE・BORN hair & relax — site scripts (mock v1) */
(function () {
  'use strict';

  /* mobile nav */
  var burger = document.querySelector('.burger');
  var drawer = document.querySelector('.drawer');
  if (burger && drawer) {
    burger.addEventListener('click', function () {
      var open = drawer.classList.toggle('open');
      document.body.classList.toggle('nav-open', open);
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    drawer.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        drawer.classList.remove('open');
        document.body.classList.remove('nav-open');
        burger.setAttribute('aria-expanded', 'false');
      });
    });
  }

  /* scroll reveal */
  var rv = document.querySelectorAll('.rv');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
    rv.forEach(function (el) { io.observe(el); });
    /* safety: never leave content hidden (e.g. observer stalled in a background tab) */
    setTimeout(function () { rv.forEach(function (el) { el.classList.add('in'); }); }, 3000);
  } else {
    rv.forEach(function (el) { el.classList.add('in'); });
  }

  /* lightbox (gallery) */
  var links = Array.prototype.slice.call(document.querySelectorAll('.gallery a'));
  var lb = document.querySelector('.lightbox');
  if (links.length && lb) {
    var img = lb.querySelector('img');
    var idx = 0;
    function show(i) {
      idx = (i + links.length) % links.length;
      img.src = links[idx].getAttribute('href');
      img.alt = links[idx].querySelector('img').alt || '';
      lb.classList.add('open');
    }
    links.forEach(function (a, i) {
      a.addEventListener('click', function (ev) { ev.preventDefault(); show(i); });
    });
    lb.querySelector('.close').addEventListener('click', function () { lb.classList.remove('open'); });
    lb.querySelector('.prev').addEventListener('click', function (ev) { ev.stopPropagation(); show(idx - 1); });
    lb.querySelector('.next').addEventListener('click', function (ev) { ev.stopPropagation(); show(idx + 1); });
    lb.addEventListener('click', function (ev) { if (ev.target === lb) lb.classList.remove('open'); });
    document.addEventListener('keydown', function (ev) {
      if (!lb.classList.contains('open')) return;
      if (ev.key === 'Escape') lb.classList.remove('open');
      if (ev.key === 'ArrowLeft') show(idx - 1);
      if (ev.key === 'ArrowRight') show(idx + 1);
    });
  }

  /* reservation form → LINE message */
  var form = document.getElementById('resv-form');
  if (form) {
    var LINE_ID = form.getAttribute('data-line-id'); // e.g. @gvx0556j
    var preview = document.getElementById('resv-preview');
    var copyBtn = document.getElementById('resv-copy');

    // default date = tomorrow, min = today
    var d1 = form.querySelector('[name="date1"]');
    var d2 = form.querySelector('[name="date2"]');
    var today = new Date();
    var pad = function (n) { return (n < 10 ? '0' : '') + n; };
    var iso = function (d) { return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()); };
    if (d1) { d1.min = iso(today); }
    if (d2) { d2.min = iso(today); }

    function val(name) {
      var el = form.querySelector('[name="' + name + '"]');
      if (!el) return '';
      if (el.type === 'radio') {
        var c = form.querySelector('[name="' + name + '"]:checked');
        return c ? c.value : '';
      }
      return (el.value || '').trim();
    }
    function fmtDate(s) {
      if (!s) return '';
      var p = s.split('-');
      if (p.length !== 3) return s;
      var d = new Date(+p[0], +p[1] - 1, +p[2]);
      var w = ['日', '月', '火', '水', '木', '金', '土'][d.getDay()];
      return +p[1] + '月' + +p[2] + '日(' + w + ')';
    }
    function buildText() {
      var lines = [];
      lines.push('【ご予約希望】ホームページから');
      lines.push('お名前：' + val('name') + ' 様');
      lines.push('ご利用：' + val('visit'));
      lines.push('メニュー：' + val('menu'));
      var t1 = fmtDate(val('date1')) + ' ' + val('time1');
      lines.push('第1希望：' + t1.trim());
      if (val('date2')) { lines.push('第2希望：' + (fmtDate(val('date2')) + ' ' + val('time2')).trim()); }
      lines.push('ご指名：' + (val('stylist') || '指名なし'));
      if (val('tel')) { lines.push('電話番号：' + val('tel')); }
      if (val('note')) { lines.push('ご要望：' + val('note')); }
      return lines.join('\n');
    }
    function validate() {
      var ok = true;
      ['name', 'menu', 'date1', 'time1'].forEach(function (n) {
        var el = form.querySelector('[name="' + n + '"]');
        if (el && !val(n)) { ok = false; el.setAttribute('aria-invalid', 'true'); el.focus(); }
        else if (el) { el.removeAttribute('aria-invalid'); }
      });
      return ok;
    }
    form.addEventListener('input', function () {
      if (preview && preview.classList.contains('show')) { preview.textContent = buildText(); }
    });
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      if (!validate()) { alert('必須項目（お名前・メニュー・第1希望日時）をご入力ください。'); return; }
      var text = buildText();
      if (preview) { preview.textContent = text; preview.classList.add('show'); }
      var url = 'https://line.me/R/oaMessage/' + encodeURIComponent(LINE_ID) + '/?' + encodeURIComponent(text);
      window.open(url, '_blank', 'noopener');
    });
    if (copyBtn) {
      copyBtn.addEventListener('click', function () {
        var text = buildText();
        if (preview) { preview.textContent = text; preview.classList.add('show'); }
        if (navigator.clipboard) {
          navigator.clipboard.writeText(text).then(function () {
            copyBtn.textContent = 'コピーしました';
            setTimeout(function () { copyBtn.textContent = '予約内容をコピー'; }, 1800);
          });
        }
      });
    }
  }
})();
