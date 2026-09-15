# -*- coding: utf-8 -*-
"""v7 patch for build.py: password 7575, motion.css, intro/marquee/reveal classes, before-after, HPB photos, calendar booking page."""
import re, io, os
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build.py")
s = io.open(p, encoding="utf-8").read()

def rep(a, b, count=1):
    global s
    assert a in s, "NOT FOUND: " + a[:80]
    s = s.replace(a, b, count)

rep('VER = "12"', 'VER = "13"')
rep('GATE_PASS = "775775"', 'GATE_PASS = "7575"')
rep('<link rel="stylesheet" href="assets/style.css?v={VER}">\n{jsonld()}', '<link rel="stylesheet" href="assets/style.css?v={VER}">\n<link rel="stylesheet" href="assets/motion.css?v={VER}">\n{jsonld()}')

# ---- reveal classes: figures wipe in, grids stagger
rep('<div class="reason rv">\n  <figure><img src="{img}"', '<div class="reason rv">\n  <figure class="rv-img{" from-right" if int(n) % 2 == 0 else ""}"><img src="{img}"')
rep('<article class="card rv">\n  <figure><img', '<article class="card rv">\n  <figure class="rv-img from-up"><img')
rep('<article class="voice rv">\n  <figure><img', '<article class="voice rv">\n  <figure class="rv-img"><img')
rep('<a class="staff rv" href="staff.html#{s[\'en\'].split()[1].lower()}">\n  <figure><img', '<a class="staff rv" href="staff.html#{s[\'en\'].split()[1].lower()}">\n  <figure class="rv-img from-up"><img')
rep('<figure class="rv"><img src="img/collage.jpg"', '<figure class="rv-img"><img src="img/collage.jpg"')
rep('<figure class="rv"><img src="img/owner-work.jpg"', '<figure class="rv-img"><img src="img/owner-work.jpg"')
rep('<div class="igrid rv">{styles}</div>', '<div class="igrid stagger">{styles}</div>')
rep('<div class="concern">\n      <ul class="list rv">{concerns}</ul>', '<div class="concern">\n      <ul class="list stagger">{concerns}</ul>')
rep('<figure class="rv"><img src="img/access-1.png"', '<figure class="rv-img"><img src="img/access-1.png"')
rep('<figure class="rv"><img src="img/access-2.png"', '<figure class="rv-img from-right"><img src="img/access-2.png"')
rep('<figure class="rv"><img src="img/exterior.jpg" alt="店舗外観と駐車場"', '<figure class="rv-img"><img src="img/exterior.jpg" alt="店舗外観と駐車場"')
rep('<div class="profile rv" id="{pid}">\n  <figure><img', '<div class="profile rv" id="{pid}">\n  <figure class="rv-img"><img')
rep('<div class="gallery rv">{imgs}</div>', '<div class="gallery stagger">{imgs}</div>')

# ---- photos: newer HotPepper shots where they are better
rep('("02", "バリアフリー＆個室完備", "img/private-room.jpg",', '("02", "バリアフリー＆個室完備", "img/room-new.jpg",')
rep('("05", "メンズスタイルも得意です", "img/mens.jpg",', '("05", "メンズスタイルも得意です", "img/mens-style.jpg",')
rep('dict(tag="髪質改善", name="柔らかストレートエステ", img="img/menu-straight.jpg",', 'dict(tag="髪質改善", name="柔らかストレートエステ", img="img/style-straight.jpg",')
rep('"リボーンは高崎でも珍しいユニセックスサロン。オーナー廣上は理容の免許も持っています。顔そりの気持ち良さは、男性の至福の時間。幼い頃連れて行ってもらった理容室の醍醐味を味わえるお店です。"',
    '"リボーンは高崎でも珍しいユニセックスサロン。オーナー廣上は理容師免許も持ち、ツイストパーマ・フェードカット・韓国風フェザーパーマなどトレンドのメンズスタイルから、ビジネスシーンの清潔感あるスタイルまで対応します。顔そり（シェービング）の気持ち良さは、男性の至福の時間。学生さんからシニアの方まで、幼い頃連れて行ってもらった理容室の醍醐味を味わえるお店です。"')

# ---- index: intro overlay, marquee, before/after, style grid from HPB
rep('''    body = f\'\'\'
<section class="hero">
  <img class="bg" src="img/exterior.jpg" alt="RE・BORN hair & relax 店舗外観" fetchpriority="high">''',
    '''    body = f\'\'\'
<div class="intro" id="intro" aria-hidden="true"><img src="img/logo.png" alt=""><span class="line"></span><span class="en">Hair &amp; Relax — Takasaki</span></div>
<section class="hero">
  <img class="bg" src="img/exterior.jpg" alt="RE・BORN hair & relax 店舗外観" fetchpriority="high">''')
rep('''<div class="infostrip">
  <div class="wrap">
    <div class="cell">{ICON['clock']}''', '''<div class="marquee" aria-hidden="true"><div class="track">{marquee()}</div></div>
<div class="infostrip">
  <div class="wrap">
    <div class="cell">{ICON['clock']}''')
rep('''    styles = "".join(f'<a href="{SHOP["ig"]}" target="_blank" rel="noopener"><img src="{m["img"]}" alt="{esc(m["name"])}" loading="lazy"></a>' for m in RECOMMEND)''',
    '''    style_imgs = [("img/style-straight.jpg", "髪質改善ストレート"), ("img/menu-stcurl.jpg", "ふんわりストカール"), ("img/style-mens-perm-1.jpg", "メンズパーマ"), ("img/menu-color.jpg", "艶髪カラー"), ("img/style-mens-fade.jpg", "フェードカット"), ("img/style-mens-perm-2.jpg", "韓国風フェザーパーマ"), ("img/menu-perm.jpg", "ふんわり小顔パーマ"), ("img/style-mens-3.jpg", "大人メンズスタイル"), ("img/kitsuke-12.jpg", "成人式ヘアセット"), ("img/style-mens-5.jpg", "ウェーブパーマ"), ("img/menu-harikoshi.jpg", "ハリコシカラー"), ("img/style-mens-4.jpg", "ツイストパーマ")]
    styles = "".join(f'<a href="{SHOP["ig"]}" target="_blank" rel="noopener"><img src="{src}" alt="{esc(alt)}" loading="lazy"></a>' for src, alt in style_imgs)''')
rep('''<section class="sec alt">
  <div class="wrap">
    {sec_head("Recommended Menu", "おすすめメニュー", "初めての方は初回限定価格でお試しいただけます。すべてカット・シャンプー・スタイリング込みの価格です（税込）。")}
    <div class="cards">{cards}</div>''', '''<section class="sec alt">
  <div class="wrap">
    {sec_head("Before / After", "髪質改善で、髪はここまで変わります", "広がり・パサつき・うねり。カラーやストレートと同時に髪質を整える当店の看板メニューの実例です。")}
    {before_after()}
  </div>
</section>

<section class="sec">
  <div class="wrap">
    {sec_head("Recommended Menu", "おすすめメニュー", "初めての方は初回限定価格でお試しいただけます。すべてカット・シャンプー・スタイリング込みの価格です（税込）。")}
    <div class="cards">{cards}</div>''')
rep('''<section class="sec dark">
  <div class="wrap">
    {sec_head("Benefits", "初めての方へ、2つの安心")}''', '''<section class="sec dark">
  <div class="wrap">
    {sec_head("Benefits", "初めての方へ、2つの安心")}''')
rep('''<section class="sec">
  <div class="wrap">
    {sec_head("Voice", "お客様の声", "20代から60代まで''', '''<section class="sec alt">
  <div class="wrap">
    {sec_head("Voice", "お客様の声", "20代から60代まで''')
rep('''<section class="sec alt">
  <div class="wrap">
    {sec_head("Staff", "スタッフ紹介"''', '''<section class="sec">
  <div class="wrap">
    {sec_head("Staff", "スタッフ紹介"''')
rep('''<section class="sec">
  <div class="wrap">
    {sec_head("Style & Instagram"''', '''<section class="sec alt">
  <div class="wrap">
    {sec_head("Style & Instagram"''')
rep('''<section class="sec alt">
  <div class="wrap">
    {sec_head("Access", "アクセス", "高崎駅西口から''', '''<section class="sec">
  <div class="wrap">
    {sec_head("Access", "アクセス", "高崎駅西口から''')
rep('''<section class="ctaband">
  <img src="img/interior-1.jpg" alt="" loading="lazy">''', '''<section class="ctaband">
  <img class="plx" src="img/interior-2.jpg" alt="" loading="lazy">''')

# helpers: marquee + before/after
rep('def ctaband():', '''def marquee():
    words = ["Hair Quality Improvement", "Head Spa", "Men's Barber", "Kimono Dressing", "Private Rooms", "Since 1935 in Takasaki"]
    return "".join(f"<span>{w}</span>" for w in words * 2)

def before_after():
    items = [("img/ba-4.jpg", "髪質改善ストレート", "広がりとパサつきが、指どおりの良いまとまる髪に"), ("img/ba-3.jpg", "髪質改善カラートリートメント", "色を楽しみながら、艶とハリを同時に"),
             ("img/ba-2.jpg", "髪質改善カラー（ボブ）", "ダメージ毛でも柔らかい質感に"), ("img/ba-1.jpg", "髪質改善カラートリートメント（ロング）", "根元から毛先までなめらかな艶")]
    return '<div class="ba stagger">' + "".join(f'<figure class="ba-item"><img src="{src}" alt="{esc(t)} ビフォーアフター" loading="lazy"><figcaption><b>{esc(t)}</b>{esc(d)}</figcaption></figure>' for src, t, d in items) + '</div><p class="small text-muted center" style="margin-top:14px">写真は当店のお客様の施術例（左：施術前／右：施術後）。</p>'

def ctaband():''')

# menu page: before/after strip after recommended cards
rep('''    <div class="cards">{cards}</div>
    <div class="notice rv"><b>初回特典：</b>''', '''    <div class="cards">{cards}</div>
    <h3 class="center" style="margin:48px 0 18px;font-size:22px">髪質改善メニューの施術例</h3>
    {before_after()}
    <div class="notice rv"><b>初回特典：</b>''')

# ---- reserve page: calendar booking
start = s.index('def build_reserve():')
end = s.index('def build_privacy():')
new_reserve = '''def build_reserve():
    import json as _json
    menus = []
    for i, m in enumerate(RECOMMEND):
        mins = {"3〜3.5時間": 210, "2.5〜3時間": 180, "2〜2.5時間": 150, "2時間": 120, "1〜1.5時間": 90}[m["time"]]
        menus.append(dict(id=f"r{i}", group="初回限定（初めての方）", name=m["name"], price=m["first"], minutes=mins, first=True, cutOnly=False))
    regular = [("カット", 5700, 60, True), ("カット＋カラー", 13700, 120, False), ("カット＋艶めきハリコシカラー", 14700, 130, False), ("カット＋パーマ", 17700, 150, False),
               ("カット＋ストレートパーマ", 23700, 180, False), ("カット＋ヘッドスパ（30分）", 10700, 100, False), ("ヘッドスパ（45分）", 7500, 45, False), ("レディースシェービング", 4400, 40, False)]
    for i, (n, pr, mn, c) in enumerate(regular):
        menus.append(dict(id=f"g{i}", group="通常メニュー", name=n, price=pr, minutes=mn, first=False, cutOnly=c))
    mens = [("メンズカット＋シェービング＋眉毛カット", 5400, 60, True), ("カット＋フェザーパーマ（韓国風）＋シェービング", 12000, 150, False), ("カット＋スパイラル系パーマ＋シェービング", 12000, 150, False),
            ("メンズカット＋アイロンパーマ＋シェービング", 11000, 140, False), ("メンズカット＋カラー", 11400, 120, False)]
    for i, (n, pr, mn, c) in enumerate(mens):
        menus.append(dict(id=f"m{i}", group="メンズ・理容メニュー", name=n, price=pr, minutes=mn, first=False, cutOnly=c))
    stylists = [dict(id="any", name="指名なし", role="最も早い空きをご案内", img="")]
    for st in STAFF:
        if st["role"] in ("カインズパースン", "アシスタント"): continue
        stylists.append(dict(id=st["en"].split()[1].lower(), name=st["name"], role=st["role"], img=st["img"]))
    data = _json.dumps(dict(menus=menus, stylists=stylists), ensure_ascii=False)
    body = pagehead("Reservation", "WEB予約", "24時間いつでも、空き状況を見ながらご予約いただけます。当日のご予約はお電話が確実です。", "img/shampoo-new.jpg") + f\'\'\'
<section class="sec">
  <div class="wrap">
    <div class="resv">
      <div class="bk rv" id="booking" data-line-id="{SHOP['line_id']}" aria-live="polite"></div>
      <script type="application/json" id="booking-data">{data}</script>
      <aside class="side">
        <div class="box rv"><h2>お電話でのご予約</h2><a class="tel" href="{SHOP['tel_href']}">{SHOP['tel']}</a><p>受付 {SHOP['hours']}／定休日 {SHOP['closed']}<br>当日のご予約・お急ぎの方はお電話が確実です。</p><a class="btn btn-tel" href="{SHOP['tel_href']}" style="width:100%">{ICON['tel']}電話をかける</a></div>
        <div class="box rv"><h2>LINEでのご予約・ご相談</h2><p>個室をご希望の方、着付け・ブライダルシェービング、髪のお悩み相談は公式LINEからどうぞ。①お名前 ②ご希望日・時間 ③ご希望のメニュー（クーポンメニュー利用有り・無し）の3点をお知らせください。</p><a class="btn btn-line" href="{SHOP['line_add']}" target="_blank" rel="noopener" style="width:100%">{ICON['line']}友だち追加してトークする</a><p class="hp" style="margin-top:8px">ID検索：{SHOP['line_id']}（@を忘れずにご入力ください）</p></div>
        <div class="box rv"><h2>ご予約に関するお願い</h2><ol><li>ご連絡無しで予約時間から大幅に遅刻された場合、施術内容によりお断りすることがあります。</li><li>無断キャンセルの場合、次回からのご予約を制限させていただくことがあります。</li><li>早朝のご予約は別途料金にて承ります。前日のお問い合わせですと承れないことが多いため、お早めにご連絡ください。</li></ol></div>
        <p class="hp rv">ホットペッパービューティーからのネット予約は<a href="{SHOP['hpb']}" target="_blank" rel="noopener" style="text-decoration:underline">こちら</a>。</p>
      </aside>
    </div>
  </div>
</section>
<script src="assets/booking.js?v={VER}" defer></script>\'\'\'
    return page("reserve.html", "WEB予約", "RE・BORN hair & relax のWEB予約。空き状況カレンダーからメニュー・スタイリスト・日時を選んで24時間ご予約いただけます。", body)

'''
s = s[:start] + new_reserve + s[end:]

# nav / footer / sticky labels for the new booking
rep('<a href="reserve.html">ご予約・お問い合わせ<small>Reservation</small></a>', '<a href="reserve.html">WEB予約（空き状況カレンダー）<small>Reservation</small></a>')
rep('<ul>{links}<li><a href="reserve.html">ご予約・お問い合わせ</a></li></ul>', '<ul>{links}<li><a href="reserve.html">WEB予約</a></li></ul>')
rep('{ICON[\'cal\']}予約フォーム（LINEへ送信）</a></nav>', '{ICON[\'cal\']}WEB予約</a></nav>')
rep('<a class="btn btn-primary" href="reserve.html">{ICON[\'cal\']}予約フォーム（LINEへ送信）</a>\n    <a class="btn btn-line"', '<a class="btn btn-primary" href="reserve.html">{ICON[\'cal\']}WEB予約（空き状況カレンダー）</a>\n    <a class="btn btn-line"')
rep('{ICON[\'cal\']}予約フォーム（LINEへ送信）</a>\n      <a class="btn btn-line" href="{SHOP[\'line_add\']}" target="_blank" rel="noopener">{ICON[\'line\']}LINEで相談・予約</a>\n      <a class="btn btn-white"', '{ICON[\'cal\']}空き状況を見て予約する</a>\n      <a class="btn btn-line" href="{SHOP[\'line_add\']}" target="_blank" rel="noopener">{ICON[\'line\']}LINEで相談・予約</a>\n      <a class="btn btn-white"')
rep('<a class="btn btn-white" href="reserve.html">{ICON[\'cal\']}予約フォーム（LINEへ送信）</a>', '<a class="btn btn-white" href="reserve.html">{ICON[\'cal\']}WEB予約（空き状況カレンダー）</a>')
rep('<p>予約フォーム（入力内容をLINEで送信）・LINE・お電話からご予約いただけます。<br>初めての方も、髪のお悩み相談だけでも大歓迎です。</p>', '<p>空き状況カレンダーからのWEB予約・LINE・お電話からご予約いただけます。<br>初めての方も、髪のお悩み相談だけでも大歓迎です。</p>')
rep('{"入力欄へ戻る" if fname == "reserve.html" else "予約フォーム"}', '{"予約に戻る" if fname == "reserve.html" else "WEB予約"}')
rep('<a class="btn btn-primary" href="reserve.html">{ICON[\'cal\']}予約フォームへ</a>', '<a class="btn btn-primary" href="reserve.html">{ICON[\'cal\']}空き状況を見て予約する</a>')
rep('<a class="btn btn-primary" href="reserve.html">{ICON[\'cal\']}指名して予約する（指名料無料）</a>', '<a class="btn btn-primary" href="reserve.html">{ICON[\'cal\']}スタイリストを指名して予約する（指名料無料）</a>')
rep('<a class="go" href="reserve.html?menu={q}">このメニューで予約する →</a>', '<a class="go" href="reserve.html">空き状況を見て予約する →</a>')

io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("build.py patched")
