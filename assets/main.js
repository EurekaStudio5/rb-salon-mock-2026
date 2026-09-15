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

  /* reservation form → LINE message */
  var form = document.getElementById('resv-form');
  if (form) {
    var LINE_ID = form.getAttribute('data-line-id'); // e.g. @gvx0556j
    var LINE_ADD = form.getAttribute('data-line-add');
    var preview = document.getElementById('resv-preview');
    var copyBtn = document.getElementById('resv-copy');
    var fallback = document.getElementById('resv-fallback');
    var errBox = document.getElementById('resv-error');
    var CLOSED_DAYS = [1, 2]; // 月・火
    var LAST_CUT = '18:30', LAST_OTHER = '18:00';

    var pad = function (n) { return (n < 10 ? '0' : '') + n; };
    var iso = function (d) { return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()); };
    var today, now;
    function refreshClock() {
      now = new Date(); today = new Date(now); today.setHours(0, 0, 0, 0);
      ['date1', 'date2'].forEach(function (n) { var el = form.querySelector('[name="' + n + '"]'); if (el) el.min = iso(today); });
    }
    refreshClock();
    // enable submit only once JS is ready (no-JS users get the LINE/phone links instead)
    var submitBtn = form.querySelector('button[type="submit"]');
    if (submitBtn) submitBtn.disabled = false;
    var noJsNote = document.getElementById('resv-nojs');
    if (noJsNote) noJsNote.hidden = true;
    function mins(t) { var m = /^(\d{1,2}):(\d{2})$/.exec(t || ''); return m ? (+m[1]) * 60 + (+m[2]) : NaN; }

    // preselect menu from ?menu=...
    try {
      var q = new URLSearchParams(location.search).get('menu');
      var sel = form.querySelector('[name="menu"]');
      if (q && sel) {
        Array.prototype.forEach.call(sel.options, function (o) { if (o.value === q) sel.value = q; });
      }
    } catch (e) { /* ignore */ }

    function val(name) {
      var el = form.querySelector('[name="' + name + '"]');
      if (!el) return '';
      if (el.type === 'radio') {
        var c = form.querySelector('[name="' + name + '"]:checked');
        return c ? c.value : '';
      }
      return (el.value || '').trim();
    }
    function parseDate(s) {
      var p = s.split('-');
      if (p.length !== 3) return null;
      var d = new Date(+p[0], +p[1] - 1, +p[2]);
      return isNaN(d.getTime()) ? null : d;
    }
    function fmtDate(s) {
      var d = parseDate(s);
      if (!d) return s;
      var w = ['日', '月', '火', '水', '木', '金', '土'][d.getDay()];
      return d.getFullYear() + '年' + (d.getMonth() + 1) + '月' + d.getDate() + '日(' + w + ')';
    }
    function isCutOnly(menu) { return menu === 'カット' || menu === 'メンズカット＋シェービング'; }
    function buildText() {
      var lines = [];
      lines.push('【ご予約希望】ホームページの予約フォームから');
      lines.push('お名前：' + val('name') + ' 様');
      lines.push('ご利用：' + val('visit'));
      lines.push('メニュー：' + val('menu'));
      lines.push('クーポン（初回限定価格）：' + (/^初回限定/.test(val('menu')) ? '利用あり' : '利用なし'));
      lines.push('第1希望：' + (fmtDate(val('date1')) + ' ' + val('time1')).trim());
      if (val('date2') || val('time2')) { lines.push('第2希望：' + (fmtDate(val('date2')) + ' ' + val('time2')).trim()); }
      lines.push('ご指名：' + (val('stylist') || '指名なし'));
      if (val('tel')) { lines.push('電話番号：' + val('tel')); }
      if (val('note')) { lines.push('ご要望：' + val('note')); }
      return lines.join('\n');
    }
    function fieldEl(n) { return form.querySelector('[name="' + n + '"]'); }
    function validate() {
      var errors = [];
      refreshClock();
      form.querySelectorAll('[aria-invalid]').forEach(function (el) { el.removeAttribute('aria-invalid'); el.removeAttribute('aria-describedby'); });
      function bad(n, msg) { errors.push({ el: fieldEl(n), msg: msg }); }
      if (!val('name')) bad('name', 'お名前をご入力ください。');
      if (!val('menu')) bad('menu', 'ご希望メニューを選択してください。');
      if (val('visit') === '2回目以降' && /^初回限定/.test(val('menu'))) bad('menu', '初回限定メニューは初めての方限定です。通常メニューをお選びください。');
      var checkSlot = function (dn, tn, label, required) {
        var ds = val(dn), ts = val(tn);
        if (!ds && !ts) { if (required) { bad(dn, label + 'の日にちを選択してください。'); bad(tn, label + 'の時間を選択してください。'); } return; }
        if (!ds) { bad(dn, label + 'の日にちを選択してください。'); return; }
        if (!ts) { bad(tn, label + 'の時間を選択してください。'); return; }
        var d = parseDate(ds);
        if (!d) { bad(dn, label + 'の日付が正しくありません。'); return; }
        if (d < today) { bad(dn, label + 'は今日以降の日付を選択してください。'); return; }
        if (CLOSED_DAYS.indexOf(d.getDay()) >= 0) { bad(dn, label + '：月曜日・火曜日は定休日です。別の日をお選びください。'); return; }
        var last = isCutOnly(val('menu')) ? LAST_CUT : LAST_OTHER;
        var tm = mins(ts);
        if (isNaN(tm)) { bad(tn, label + 'の時間が正しくありません。'); return; }
        if (tm > mins(last)) { bad(tn, label + '：このメニューの最終受付は ' + last + ' です。'); return; }
        if (d.getTime() === today.getTime()) {
          if (tm <= now.getHours() * 60 + now.getMinutes()) bad(tn, label + '：本日のこの時間は過ぎています。当日のご予約はお電話が確実です。');
        }
      };
      checkSlot('date1', 'time1', '第1希望', true);
      checkSlot('date2', 'time2', '第2希望', false);
      if (buildText().length > 1500) bad('note', 'ご要望が長すぎます。1,500文字以内にまとめるか、お電話でご相談ください。');
      if (errors.length) {
        var seen = {};
        errors.forEach(function (e) { if (e.el) { e.el.setAttribute('aria-invalid', 'true'); e.el.setAttribute('aria-describedby', 'resv-error'); } });
        var msgs = errors.map(function (e) { return e.msg; }).filter(function (m) { if (seen[m]) return false; seen[m] = true; return true; });
        if (errBox) { errBox.innerHTML = '<b>ご確認ください</b><ul>' + msgs.map(function (m) { return '<li>' + m.replace(/[<>&]/g, '') + '</li>'; }).join('') + '</ul>'; errBox.hidden = false; }
        // focus the first invalid field in DOM order
        var first = form.querySelector('[aria-invalid="true"]');
        if (first) { first.focus(); first.scrollIntoView({ block: 'center' }); }
        // any previously generated link/preview is no longer valid
        if (fallback) { fallback.hidden = true; fallback.innerHTML = ''; }
        if (preview && preview.classList.contains('show')) { preview.textContent = buildText() + '\n（上の項目を修正して、もう一度ボタンを押してください）'; }
        return false;
      }
      if (errBox) errBox.hidden = true;
      return true;
    }
    function lineUrl(text) { return 'https://line.me/R/oaMessage/' + encodeURIComponent(LINE_ID) + '/?' + encodeURIComponent(text); }
    function showPreview(text) {
      if (preview) { preview.textContent = text; preview.classList.add('show'); }
      if (fallback) {
        fallback.innerHTML = 'LINEが開かない場合は、<a href="' + lineUrl(text) + '" class="retry" target="_blank" rel="noopener">こちらをタップ</a>するか、上の内容をコピーして公式LINE（<a href="' + LINE_ADD + '" target="_blank" rel="noopener">友だち追加</a>）のトークに貼り付けて送信してください。';
        fallback.hidden = false;
        // the retry link re-validates at click time (the slot may have expired meanwhile)
        var retry = fallback.querySelector('a.retry');
        if (retry) {
          retry.addEventListener('click', function (ev) {
            if (!validate()) { ev.preventDefault(); return; }
            retry.setAttribute('href', lineUrl(buildText()));
          });
        }
      }
    }
    function invalidateOutputs() {
      // anything shown so far may be stale after an edit: hide the LINE link until re-validated
      if (fallback) { fallback.hidden = true; fallback.innerHTML = ''; }
      if (preview && preview.classList.contains('show')) { preview.textContent = buildText() + '\n（内容を変更しました。もう一度ボタンを押してください）'; }
    }
    form.addEventListener('input', invalidateOutputs);
    form.addEventListener('change', invalidateOutputs);
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      if (!validate()) return;
      var text = buildText();
      showPreview(text);
      var w = window.open(lineUrl(text), '_blank', 'noopener');
      if (!w) { /* popup blocked: fallback link is already visible */ }
    });
    if (copyBtn) {
      copyBtn.addEventListener('click', function () {
        if (!validate()) return;
        var text = buildText();
        showPreview(text);
        var done = function () { copyBtn.textContent = 'コピーしました'; setTimeout(function () { copyBtn.textContent = '予約内容をコピー'; }, 1800); };
        var fail = function () {
          copyBtn.textContent = '長押しでコピーしてください';
          if (preview && window.getSelection) { var r = document.createRange(); r.selectNodeContents(preview); var s = window.getSelection(); s.removeAllRanges(); s.addRange(r); }
          setTimeout(function () { copyBtn.textContent = '予約内容をコピー'; }, 2500);
        };
        if (navigator.clipboard && navigator.clipboard.writeText) { navigator.clipboard.writeText(text).then(done, fail); } else { fail(); }
      });
    }
  }
})();
