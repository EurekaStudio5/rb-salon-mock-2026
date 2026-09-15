/* RE・BORN hair & relax — カレンダー予約（デモ）
   空き状況は日付・スタイリスト・時間から決定論的に生成したダミー。実運用では予約台帳APIに置き換える。 */
(function () {
  'use strict';
  var root = document.getElementById('booking');
  if (!root) return;

  var DATA = JSON.parse(document.getElementById('booking-data').textContent);
  var LINE_ID = root.getAttribute('data-line-id');
  var CLOSED = [1, 2]; // 月・火
  var OPEN_MIN = 9 * 60, LAST_CUT = 18 * 60 + 30, LAST_OTHER = 18 * 60;
  var W = ['日', '月', '火', '水', '木', '金', '土'];

  var state = { step: 1, menu: null, stylist: null, date: null, time: null, name: '', tel: '', visit: '初めて', note: '', month: null };

  var pad = function (n) { return (n < 10 ? '0' : '') + n; };
  var iso = function (d) { return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()); };
  var today = new Date(); today.setHours(0, 0, 0, 0);
  var maxDate = new Date(today); maxDate.setDate(maxDate.getDate() + 60);
  function hm(m) { return Math.floor(m / 60) + ':' + pad(m % 60); }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function fmtDate(d) { return d.getFullYear() + '年' + (d.getMonth() + 1) + '月' + d.getDate() + '日(' + W[d.getDay()] + ')'; }

  // --- ダミー空き状況（決定論的） ---
  function h32(str) { var h = 2166136261; for (var i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = Math.imul(h, 16777619) >>> 0; } return h; }
  function slotBusy(dateStr, stylistId, minutes) {
    var r = h32(dateStr + '|' + stylistId + '|' + minutes) % 100;
    var d = new Date(dateStr + 'T00:00:00');
    var weekend = d.getDay() === 0 || d.getDay() === 6;
    return r < (weekend ? 38 : 22);
  }
  function lastStart(menu) { return menu.cutOnly ? LAST_CUT : LAST_OTHER; }
  function slotsFor(dateStr, menu, stylist) {
    var out = [];
    var d = new Date(dateStr + 'T00:00:00');
    var isToday = d.getTime() === today.getTime();
    var now = new Date(); var nowMin = now.getHours() * 60 + now.getMinutes();
    var need = Math.ceil(menu.minutes / 30);
    for (var m = OPEN_MIN; m <= lastStart(menu); m += 30) {
      var ok = true;
      if (isToday && m <= nowMin + 60) ok = false;           // 当日は1時間前まで
      for (var k = 0; k < need && ok; k++) {
        var mm = m + k * 30;
        if (mm > 18 * 60 + 30) { ok = false; break; }         // 18:30枠まで
        if (stylist.id === 'any') {
          // 誰でも: いずれかのスタイリストが空いていればOK
          var anyFree = DATA.stylists.some(function (s) { return s.id !== 'any' && !slotBusy(dateStr, s.id, mm); });
          if (!anyFree) ok = false;
        } else if (slotBusy(dateStr, stylist.id, mm)) ok = false;
      }
      out.push({ m: m, label: hm(m), ok: ok });
    }
    return out;
  }
  function dayStatus(dateStr, menu, stylist) {
    var d = new Date(dateStr + 'T00:00:00');
    if (d < today || d > maxDate) return 'na';
    if (CLOSED.indexOf(d.getDay()) >= 0) return 'closed';
    var s = slotsFor(dateStr, menu, stylist), free = s.filter(function (x) { return x.ok; }).length;
    if (free === 0) return 'full';
    if (free <= 3) return 'few';
    if (free <= 7) return 'some';
    return 'many';
  }
  var MARK = { many: '◎', some: '○', few: '△', full: '×', closed: '休', na: '' };

  // --- 描画 ---
  function stepsBar() {
    var names = ['メニュー', 'スタイリスト', '日時', 'お客様情報', '確認'];
    return '<ol class="bk-steps" aria-label="予約の手順">' + names.map(function (n, i) {
      var k = i + 1, cls = k < state.step ? 'done' : (k === state.step ? 'now' : '');
      return '<li class="' + cls + '"><span class="n">' + k + '</span><span class="t">' + n + '</span></li>';
    }).join('') + '</ol>';
  }
  function summaryBox() {
    var rows = [];
    if (state.menu) rows.push(['メニュー', state.menu.name + '　¥' + state.menu.price.toLocaleString() + '（約' + state.menu.minutes + '分）']);
    if (state.stylist) rows.push(['スタイリスト', state.stylist.name]);
    if (state.date && state.time !== null) rows.push(['日時', fmtDate(new Date(state.date + 'T00:00:00')) + ' ' + hm(state.time) + '〜']);
    if (!rows.length) return '';
    return '<div class="bk-summary"><b>選択中</b><dl>' + rows.map(function (r) { return '<dt>' + esc(r[0]) + '</dt><dd>' + esc(r[1]) + '</dd>'; }).join('') + '</dl></div>';
  }
  function backBtn() { return state.step > 1 ? '<button type="button" class="btn btn-outline btn-sm" data-act="back">← 戻る</button>' : ''; }

  function viewMenu() {
    var groups = {};
    DATA.menus.forEach(function (m) { (groups[m.group] = groups[m.group] || []).push(m); });
    var html = '<h2 class="bk-h">メニューを選ぶ</h2><p class="bk-p">初回限定価格は初めての方のみ。所要時間の目安を表示しています。</p>';
    Object.keys(groups).forEach(function (g) {
      html += '<h3 class="bk-g">' + esc(g) + '</h3><div class="bk-menus">' + groups[g].map(function (m) {
        return '<button type="button" class="bk-menu' + (state.menu && state.menu.id === m.id ? ' sel' : '') + '" data-act="menu" data-id="' + m.id + '">' +
          '<span class="nm">' + esc(m.name) + (m.first ? '<em>初回限定</em>' : '') + '</span>' +
          '<span class="pr">¥' + m.price.toLocaleString() + '</span><span class="tm">約' + m.minutes + '分</span></button>';
      }).join('') + '</div>';
    });
    return html;
  }
  function viewStylist() {
    return '<h2 class="bk-h">スタイリストを選ぶ</h2><p class="bk-p">指名料はいただいておりません。「指名なし」は最も早い空きをご案内します。</p>' +
      '<div class="bk-stylists">' + DATA.stylists.map(function (s) {
        return '<button type="button" class="bk-stylist' + (state.stylist && state.stylist.id === s.id ? ' sel' : '') + '" data-act="stylist" data-id="' + s.id + '">' +
          (s.img ? '<img src="' + s.img + '" alt="">' : '<span class="ph">✦</span>') + '<span class="nm">' + esc(s.name) + '</span><span class="rl">' + esc(s.role) + '</span></button>';
      }).join('') + '</div>' + summaryBox();
  }
  function viewCalendar() {
    var m = state.month || new Date(today.getFullYear(), today.getMonth(), 1);
    state.month = m;
    var first = new Date(m.getFullYear(), m.getMonth(), 1), last = new Date(m.getFullYear(), m.getMonth() + 1, 0);
    var cells = '';
    for (var i = 0; i < first.getDay(); i++) cells += '<td></td>';
    for (var d = 1; d <= last.getDate(); d++) {
      var dt = new Date(m.getFullYear(), m.getMonth(), d), ds = iso(dt);
      var st = dayStatus(ds, state.menu, state.stylist);
      var selectable = st === 'many' || st === 'some' || st === 'few';
      var cls = 'st-' + st + (state.date === ds ? ' sel' : '') + (dt.getTime() === today.getTime() ? ' today' : '');
      cells += '<td class="' + cls + '">' + (selectable ? '<button type="button" data-act="date" data-d="' + ds + '"><b>' + d + '</b><span>' + MARK[st] + '</span></button>' : '<div><b>' + d + '</b><span>' + MARK[st] + '</span></div>') + '</td>';
      if (dt.getDay() === 6 && d !== last.getDate()) cells += '</tr><tr>';
    }
    var prevOk = new Date(m.getFullYear(), m.getMonth(), 0) >= today;
    var nextOk = new Date(m.getFullYear(), m.getMonth() + 1, 1) <= maxDate;
    var html = '<h2 class="bk-h">日時を選ぶ</h2>' + summaryBox() +
      '<div class="bk-cal"><div class="bk-calhead"><button type="button" class="nav" data-act="prev"' + (prevOk ? '' : ' disabled') + ' aria-label="前の月">‹</button><b>' + m.getFullYear() + '年' + (m.getMonth() + 1) + '月</b><button type="button" class="nav" data-act="next"' + (nextOk ? '' : ' disabled') + ' aria-label="次の月">›</button></div>' +
      '<table><thead><tr>' + W.map(function (w, i) { return '<th class="' + (i === 0 ? 'sun' : i === 6 ? 'sat' : '') + '">' + w + '</th>'; }).join('') + '</tr></thead><tbody><tr>' + cells + '</tr></tbody></table>' +
      '<p class="bk-legend">◎ 空きあり　○ やや空き　△ 残りわずか　× 満席　休 定休日（月・火）</p></div>';
    if (state.date) {
      var slots = slotsFor(state.date, state.menu, state.stylist);
      html += '<h3 class="bk-g">' + fmtDate(new Date(state.date + 'T00:00:00')) + ' の空き時間</h3><div class="bk-slots">' + slots.map(function (s) {
        return s.ok ? '<button type="button" class="slot' + (state.time === s.m ? ' sel' : '') + '" data-act="time" data-m="' + s.m + '">' + s.label + '</button>' : '<span class="slot ng">' + s.label + '</span>';
      }).join('') + '</div><p class="bk-note">最終受付：' + (state.menu.cutOnly ? 'カット 18:30' : 'カラー・パーマ・スパ 18:00') + '。当日は1時間前までのお時間をご案内しています。</p>';
    }
    return html;
  }
  function viewInfo() {
    return '<h2 class="bk-h">お客様情報</h2>' + summaryBox() +
      '<form class="bk-form" id="bk-form" novalidate>' +
      '<fieldset><legend>ご利用</legend><div class="radios"><label><input type="radio" name="visit" value="初めて"' + (state.visit === '初めて' ? ' checked' : '') + '>初めて</label><label><input type="radio" name="visit" value="2回目以降"' + (state.visit === '2回目以降' ? ' checked' : '') + '>2回目以降</label></div></fieldset>' +
      '<div class="row2"><div class="field"><label for="bk-name">お名前<i>必須</i></label><input id="bk-name" name="name" type="text" autocomplete="name" maxlength="40" value="' + esc(state.name) + '" placeholder="例）高崎 花子"></div>' +
      '<div class="field"><label for="bk-tel">電話番号<i>必須</i></label><input id="bk-tel" name="tel" type="tel" inputmode="tel" autocomplete="tel" maxlength="20" value="' + esc(state.tel) + '" placeholder="例）090-1234-5678"></div></div>' +
      '<div class="field"><label for="bk-note">ご要望・ご相談</label><textarea id="bk-note" name="note" maxlength="400" placeholder="髪のお悩み、お子様連れ、車椅子でのご来店など">' + esc(state.note) + '</textarea></div>' +
      '<div class="errbox" id="bk-err" hidden></div>' +
      '<div class="actions"><button type="submit" class="btn btn-primary">確認画面へ</button></div></form>';
  }
  function viewConfirm() {
    var d = new Date(state.date + 'T00:00:00');
    var end = state.time + state.menu.minutes;
    var rows = [['メニュー', state.menu.name], ['料金', '¥' + state.menu.price.toLocaleString() + '（税込）'], ['スタイリスト', state.stylist.name],
      ['日時', fmtDate(d) + ' ' + hm(state.time) + '〜' + hm(end) + '（約' + state.menu.minutes + '分）'], ['お名前', state.name + ' 様'], ['電話番号', state.tel], ['ご利用', state.visit]];
    if (state.note) rows.push(['ご要望', state.note]);
    return '<h2 class="bk-h">ご予約内容の確認</h2><div class="bk-confirm"><table>' + rows.map(function (r) { return '<tr><th>' + esc(r[0]) + '</th><td>' + esc(r[1]) + '</td></tr>'; }).join('') + '</table>' +
      '<p class="bk-note">ご連絡無しで予約時間から大幅に遅刻された場合、施術内容によりお断りすることがあります。無断キャンセルの場合、次回からのご予約を制限させていただくことがあります。</p>' +
      '<div class="actions"><button type="button" class="btn btn-primary" data-act="confirm">この内容で予約を確定する</button></div></div>';
  }
  function viewDone() {
    var d = new Date(state.date + 'T00:00:00');
    var no = 'RB' + String(h32(state.date + state.time + state.name) % 900000 + 100000);
    var text = ['【予約完了】RE・BORN hair & relax', '予約番号：' + no, 'メニュー：' + state.menu.name, 'スタイリスト：' + state.stylist.name, '日時：' + fmtDate(d) + ' ' + hm(state.time) + '〜', 'お名前：' + state.name + ' 様'].join('\n');
    var lineUrl = 'https://line.me/R/oaMessage/' + encodeURIComponent(LINE_ID) + '/?' + encodeURIComponent(text);
    var gcal = 'https://calendar.google.com/calendar/render?action=TEMPLATE&text=' + encodeURIComponent('RE・BORN ' + state.menu.name) + '&dates=' + state.date.replace(/-/g, '') + 'T' + pad(Math.floor(state.time / 60)) + pad(state.time % 60) + '00/' + state.date.replace(/-/g, '') + 'T' + pad(Math.floor((state.time + state.menu.minutes) / 60)) + pad((state.time + state.menu.minutes) % 60) + '00&location=' + encodeURIComponent('群馬県高崎市聖石町13-1') + '&ctz=Asia/Tokyo';
    return '<div class="bk-done"><div class="mark">✓</div><h2 class="bk-h">ご予約を受け付けました</h2>' +
      '<p class="bk-p">予約番号 <b>' + no + '</b><br>' + esc(fmtDate(d)) + ' ' + hm(state.time) + '〜　' + esc(state.menu.name) + '／' + esc(state.stylist.name) + '</p>' +
      '<div class="actions"><a class="btn btn-outline" href="' + gcal + '" target="_blank" rel="noopener">Googleカレンダーに追加</a><a class="btn btn-line" href="' + lineUrl + '" target="_blank" rel="noopener">予約内容をLINEにも送る</a></div>' +
      '<p class="bk-note">※これはデモ画面です。本番では予約が店舗の予約台帳に登録され、確認のメール／LINEが自動で届きます。変更・キャンセルは前日までにお電話またはLINEでご連絡ください。</p>' +
      '<p class="center"><button type="button" class="btn btn-sm btn-outline" data-act="restart">最初に戻る</button></p></div>';
  }

  function render() {
    var v = state.step === 1 ? viewMenu() : state.step === 2 ? viewStylist() : state.step === 3 ? viewCalendar() : state.step === 4 ? viewInfo() : state.step === 5 ? viewConfirm() : viewDone();
    root.innerHTML = (state.step <= 5 ? stepsBar() : '') + '<div class="bk-body">' + v + '</div>' + (state.step <= 5 ? '<div class="bk-foot">' + backBtn() + '</div>' : '');
    var hd = root.querySelector('.bk-h'); if (hd) { hd.setAttribute('tabindex', '-1'); hd.focus({ preventScroll: true }); }
    if (state.step > 1) root.scrollIntoView({ block: 'start', behavior: 'smooth' });
    if (window.fixOrphans) setTimeout(window.fixOrphans, 30);
  }

  root.addEventListener('click', function (ev) {
    var b = ev.target.closest('[data-act]'); if (!b || b.disabled) return;
    var act = b.getAttribute('data-act');
    if (act === 'menu') { state.menu = DATA.menus.filter(function (m) { return m.id === b.getAttribute('data-id'); })[0]; state.date = null; state.time = null; state.step = 2; }
    else if (act === 'stylist') { state.stylist = DATA.stylists.filter(function (s) { return s.id === b.getAttribute('data-id'); })[0]; state.date = null; state.time = null; state.step = 3; }
    else if (act === 'prev') { state.month = new Date(state.month.getFullYear(), state.month.getMonth() - 1, 1); }
    else if (act === 'next') { state.month = new Date(state.month.getFullYear(), state.month.getMonth() + 1, 1); }
    else if (act === 'date') { state.date = b.getAttribute('data-d'); state.time = null; }
    else if (act === 'time') { state.time = +b.getAttribute('data-m'); state.step = 4; }
    else if (act === 'back') { state.step = Math.max(1, state.step - 1); }
    else if (act === 'confirm') { state.step = 6; }
    else if (act === 'restart') { state = { step: 1, menu: null, stylist: null, date: null, time: null, name: '', tel: '', visit: '初めて', note: '', month: null }; }
    render();
  });
  root.addEventListener('submit', function (ev) {
    var f = ev.target; if (f.id !== 'bk-form') return;
    ev.preventDefault();
    state.name = f.name.value.trim(); state.tel = f.tel.value.trim(); state.note = f.note.value.trim();
    state.visit = (f.querySelector('[name="visit"]:checked') || {}).value || '初めて';
    var errs = [];
    if (!state.name) errs.push('お名前をご入力ください。');
    if (!/^[0-9０-９\-\s()（）]{10,15}$/.test(state.tel)) errs.push('電話番号を正しくご入力ください。');
    if (state.visit === '2回目以降' && state.menu.first) errs.push('初回限定メニューは初めての方限定です。「戻る」からメニューを選び直してください。');
    var eb = f.querySelector('#bk-err');
    if (errs.length) { eb.innerHTML = '<b>ご確認ください</b><ul>' + errs.map(function (e) { return '<li>' + esc(e) + '</li>'; }).join('') + '</ul>'; eb.hidden = false; eb.scrollIntoView({ block: 'center' }); return; }
    state.step = 5; render();
  });

  render();
})();
