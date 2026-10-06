# patch_v8.py (2026-10-06) — 予約カレンダーのデモを撤去し、予約ページを現行サイトと同じ LINE・電話の案内に戻す
# Shingo「もともとのウェブサイトにはなかった機能…消しておいていい。ややこしいので」
import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))

def rd(p):
    return open(os.path.join(ROOT, p), encoding="utf-8").read()

def wr(p, s):
    open(os.path.join(ROOT, p), "w", encoding="utf-8", newline="\n").write(s)

def rep(s, old, new, n=1):
    c = s.count(old)
    assert c == n, (old[:70], c)
    return s.replace(old, new)

# ---------- build.py ----------
b = rd("build.py")
b = rep(b, 'VER = "23"', 'VER = "24"')
b = rep(b, """href="reserve.html">{ICON['cal']}WEB予約</a></nav>""", """href="reserve.html">{ICON['cal']}ご予約</a></nav>""")
b = rep(b, """<a href="reserve.html">WEB予約<small>Reservation</small></a>""", """<a href="reserve.html">ご予約<small>Reservation</small></a>""")
b = rep(b, "{ICON['cal']}空き状況を見て予約する</a>", "{ICON['cal']}ご予約はこちら</a>", n=4)
b = rep(b, '<a class="go" href="reserve.html">空き状況を見て予約する →</a>', '<a class="go" href="reserve.html">ご予約はこちら →</a>')
b = rep(b, "{ICON['cal']}指名して予約する</a>", "{ICON['cal']}ご予約はこちら</a>")
b = rep(b, "<p>空き状況カレンダーからのWEB予約・LINE・お電話からご予約いただけます。初めての方も、髪のお悩み相談だけでも大歓迎です。</p>",
        "<p>ご予約は、LINE公式アカウントまたはお電話で承ります。初めての方も、髪のお悩み相談だけでも大歓迎です。</p>")
b = rep(b, """<ul>{links}<li><a href="reserve.html">WEB予約</a></li></ul>""", """<ul>{links}<li><a href="reserve.html">ご予約</a></li></ul>""")

# sticky bar: 予約ページでは「電話・LINE」の2つだけにする（自分自身へのリンクを出さない）
b = rep(b, """    links = "".join('<li><a href="%s">%s</a></li>' % (h, esc(ja)) for h, ja, en in NAV)
    return f'''
<footer class="footer">""", """    links = "".join('<li><a href="%s">%s</a></li>' % (h, esc(ja)) for h, ja, en in NAV)
    on_resv = fname == "reserve.html"
    web = "" if on_resv else f'\\n  <a class="web" href="reserve.html">{ICON["cal"]}<b>ご予約</b></a>'
    return f'''
<footer class="footer">""")
b = rep(b, """<nav class="stickybar" aria-label="予約・お問い合わせ">""", """<nav class="stickybar{' two' if on_resv else ''}" aria-label="予約・お問い合わせ">""")
b = rep(b, """  <a class="line" href="{SHOP['line_add']}" target="_blank" rel="noopener">{ICON['line']}<b>LINE予約</b></a>
  <a class="web" href="{"#resv-form" if fname == "reserve.html" else "reserve.html"}">{ICON['cal']}<b>{"予約に戻る" if fname == "reserve.html" else "WEB予約"}</b></a>
</nav>""", """  <a class="line" href="{SHOP['line_add']}" target="_blank" rel="noopener">{ICON['line']}<b>LINE予約</b></a>{web}
</nav>""")

# gate: カレンダーの注記を差し替え／A案（写真差し替えのみ5万円）と食い違う「この内容で公開しない」「何度でも調整」を外す
b = rep(b, "<p>「新しいホームページはこんな雰囲気・こんな機能にできます」というデザインの見本です。写真・文言・メニューはすべて差し替え可能で、この内容で公開するものではありません。<br>ご確認用のパスワードを入力してください。</p>",
        "<p>新しいホームページのデザインの見本です。<br>ご確認用のパスワードを入力してください。</p>")
b = rep(b, "<li>ご確認が終わりましたら、このプレビューは削除します。写真・文言の差し替えはご要望に合わせて何度でも調整できます。</li>",
        "<li>ご確認が終わりましたら、このプレビューは削除します。</li>")
b = rep(b, "<li>「WEB予約」ページのカレンダーの空き状況はデモ用のダミーです。実際の予約は現在どおりお電話・LINE・ホットペッパーで承ります。</li>",
        "<li>ご予約の案内は、現在のホームページと同じくLINE公式アカウントとお電話を中心にしています。</li>")

# reserve page: カレンダー（booking.js）を撤去し、現行サイトの「ご予約に関するお願い」に沿った案内ページにする
new_reserve = '''def build_reserve():
    body = pagehead("Reservation", "ご予約", "ご予約・お問い合わせは、LINE公式アカウントまたはお電話で承ります。", "img/shampoo-new.jpg") + f\'\'\'
<section class="sec">
  <div class="wrap">
    <div class="resv">
      <div class="side">
        <div class="box rv" id="resv-line"><h2>LINEでのご予約・お問い合わせ</h2><p>当サロンへのご予約・お問い合わせは、LINE公式アカウントからご連絡ください。個室のご希望や髪のお悩み相談もお気軽にどうぞ。</p><p style="margin-top:10px">はじめてご連絡いただく場合は、次の3点をお知らせください。</p><ol style="margin-top:6px"><li>お名前</li><li>ご希望日・時間</li><li>ご希望のメニュー（クーポンメニュー利用有り・無し）</li></ol><a class="btn btn-line" href="{SHOP['line_add']}" target="_blank" rel="noopener" style="width:100%;margin-top:14px">{ICON['line']}LINEで友だち追加</a><p class="hp" style="margin-top:8px">LINE ID検索：{SHOP['line_id']}（@を忘れずにご入力ください）</p></div>
        <div class="box rv"><h2>LINEでご予約いただく際のお願い</h2><p>メッセージをいただいただけでは、ご予約は完了ではございません。当店からの折り返しをもって、ご予約完了とさせていただきます。返信は3営業日以内とさせていただきますので、お時間に余裕をもってご予約くださいませ。</p><p style="margin-top:10px">当日のご連絡ですと、施術中の場合すぐに返信ができません。お急ぎのお問い合わせは、営業時間内に直接お電話ください。</p></div>
      </div>
      <aside class="side">
        <div class="box rv"><h2>お電話でのご予約</h2><a class="tel" href="{SHOP['tel_href']}">{SHOP['tel']}</a><p>受付 {SHOP['hours']}／定休日 {SHOP['closed']}。当日のご予約・お急ぎの方はお電話が確実です。</p><a class="btn btn-tel" href="{SHOP['tel_href']}" style="width:100%;margin-top:12px">{ICON['tel']}電話をかける</a></div>
        <div class="box rv"><h2>ご予約に関するお願い</h2><ol><li>ご連絡無しで予約時間から大幅に遅刻された場合、施術内容によりお断りすることがあります。</li><li>無断キャンセルの場合、次回からのご予約を制限させていただくことがあります。</li><li>早朝のご予約は別途料金にて承ります。前日のお問い合わせですと承れないことが多いため、お早めにご連絡ください。</li></ol></div>
        <p class="hp rv">ホットペッパービューティーからのネット予約は<a href="{SHOP['hpb']}" target="_blank" rel="noopener" style="text-decoration:underline">こちら</a>。</p>
      </aside>
    </div>
  </div>
</section>\'\'\'
    return page("reserve.html", "ご予約", "RE・BORN hair & relax のご予約・お問い合わせ。LINE公式アカウントまたはお電話（0800-800-8835）で承ります。", body)

'''
m = re.search(r"def build_reserve\(\):.*?\n\nNEWS = \[", b, flags=re.S)
assert m, "build_reserve not found"
b = b[:m.start()] + new_reserve + "NEWS = [" + b[m.end():]
assert "booking" not in b, "booking reference left in build.py"
wr("build.py", b)

# ---------- motion.css: カレンダー用CSSを削除 ----------
c = rd("assets/motion.css")
c = rep(c, "/* ===== v7: intro / motion / booking ===== */", "/* ===== v7: intro / motion ===== */")
i = c.index("/* ===== booking (calendar) ===== */")
j = c.index("/* before / after */")
c = c[:i] + c[j:]
assert ".bk" not in c
wr("assets/motion.css", c)

# ---------- style.css: 予約ページのスティッキーバーは2列 ----------
s = rd("assets/style.css")
s = rep(s, ".stickybar a svg{width:20px;height:20px}", ".stickybar.two{grid-template-columns:1fr 1fr}\n.stickybar a svg{width:20px;height:20px}")
wr("assets/style.css", s)

# ---------- main.js: 旧LINE送信フォーム（v6まで）の死にコードとカレンダー用セレクタを削除 ----------
js = rd("assets/main.js")
js = rep(js, ", .faq .a, .bk-menu .nm, .bk-stylist .rl, .bk-p, .bk-note, .bk-legend, .bk-summary dd, .bk-confirm td');", ", .faq .a');")
js = rep(js, "if (el.closest('.btn, .marquee, .stickybar, .bk-steps, table, .nav, .drawer, .intro')) return;", "if (el.closest('.btn, .marquee, .stickybar, table, .nav, .drawer, .intro')) return;")
i = js.index("\n  /* reservation form → LINE message */")
j = js.rindex("\n})();")
js = js[:i] + js[j:]
assert "resv-" not in js and ".bk" not in js
wr("assets/main.js", js)
print("patched OK")
