# -*- coding: utf-8 -*-
"""RE・BORN hair & relax — 静的サイト生成（mock v1）
実行: python build.py  → 同フォルダに index.html ほか各ページを出力
文言は現行サイト（re-born2005.com）を基本に逐語保持し、構成・導線・デザインを刷新。
"""
import os, json, html
BASE = os.path.dirname(os.path.abspath(__file__))
VER = "15"
GATE_PASS = "7575"  # 仮公開のパスワード（Shingo指示 2026-09-15）

def gate_hash(pw):
    # 軽量ハッシュ（gate.html の JS と同じ計算式）: 平文をHTMLに置かないためのもの。暗号強度は求めていない
    h = 5381
    for ch in pw:
        h = ((h * 33) ^ ord(ch)) & 0xFFFFFFFF
    return format(h, "x") + str(len(pw))
BASE_URL = "https://eurekastudio5.github.io/rb-salon-mock-2026/"  # 本番公開時は本番ドメインに変更

SHOP = dict(
    name="RE・BORN hair & relax",
    name_ja="リ・ボーン ヘア＆リラックス",
    tel="0800-800-8835",
    tel_href="tel:0800-800-8835",
    tel2="027-326-3738",
    zip="370-0863",
    addr="群馬県高崎市聖石町13-1",
    hours="9:00〜18:30",
    last="カット 18:30／カラー・パーマ 18:00",
    closed="月曜日・火曜日",
    parking="店舗目の前に10台",
    access="高崎駅より車で3分（聖石橋を渡ってすぐ）",
    line_add="https://lin.ee/s59kRdt",
    line_id="@gvx0556j",
    ig="https://www.instagram.com/reborn84/",
    ig_id="@reborn84",
    hpb="https://beauty.hotpepper.jp/slnH000210137/",
    recruit="https://高崎美容室求人.com/",
    map_embed="https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d12859.421112338769!2d138.98995859252926!3d36.315816204016734!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x1ff3731fe45f2166!2zUkXvvaVCT1JOIGhhaXIgJiByZWxheCjpq5jltI7luIIg576O5a656ZmiIOOBiuOBmeOBmeOCgSk!5e0!3m2!1sja!2sjp!4v1659191296513!5m2!1sja!2sjp",
    map_link="https://www.google.com/maps/search/?api=1&query=RE%E3%83%BBBORN+hair+%26+relax+%E9%AB%98%E5%B4%8E%E5%B8%82%E8%81%96%E7%9F%B3%E7%94%BA13-1",
    site_url="https://re-born2005.com/",
)

NAV = [
    ("index.html", "ホーム", "Home"),
    ("menu.html", "メニュー・料金", "Menu"),
    ("staff.html", "スタッフ", "Staff"),
    ("voice.html", "お客様の声", "Voice"),
    ("kitsuke.html", "着付け", "Kimono"),
    ("faq.html", "よくある質問", "FAQ"),
    ("access.html", "アクセス", "Access"),
]

ICON = dict(
    tel='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.6a2 2 0 0 1-.5 2.1L8.1 9.6a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.8.3 1.7.5 2.6.7a2 2 0 0 1 1.7 2z"/></svg>',
    line='<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.5 2 2 5.7 2 10.2c0 4 3.6 7.4 8.4 8.1.3.1.8.2.9.5.1.3.1.7 0 1l-.1.9c0 .3-.2 1 .9.6 1.1-.5 5.8-3.4 7.9-5.9 1.4-1.6 2-3.2 2-5.2C22 5.7 17.5 2 12 2zM8.1 12.8H6.2c-.3 0-.5-.2-.5-.5V8.6c0-.3.2-.5.5-.5s.5.2.5.5v3.2h1.4c.3 0 .5.2.5.5s-.2.5-.5.5zm1.8-.5c0 .3-.2.5-.5.5s-.5-.2-.5-.5V8.6c0-.3.2-.5.5-.5s.5.2.5.5v3.7zm4.5 0c0 .2-.1.4-.3.5h-.2c-.2 0-.3-.1-.4-.2l-1.9-2.6v2.3c0 .3-.2.5-.5.5s-.5-.2-.5-.5V8.6c0-.2.1-.4.3-.5h.2c.2 0 .3.1.4.2l1.9 2.6V8.6c0-.3.2-.5.5-.5s.5.2.5.5v3.7zm3-2.4c.3 0 .5.2.5.5s-.2.5-.5.5h-1.4v.9h1.4c.3 0 .5.2.5.5s-.2.5-.5.5h-1.9c-.3 0-.5-.2-.5-.5V8.6c0-.3.2-.5.5-.5h1.9c.3 0 .5.2.5.5s-.2.5-.5.5h-1.4v.9h1.4z"/></svg>',
    cal='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>',
    ig='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>',
    clock='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>',
    pin='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>',
    car='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 17h14M3 11l2-6h14l2 6M3 11v6h18v-6M3 11h18"/><circle cx="7" cy="17" r="2"/><circle cx="17" cy="17" r="2"/></svg>',
    map='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18l-6 3V6l6-3 6 3 6-3v15l-6 3-6-3z"/><path d="M9 3v15M15 6v15"/></svg>',
)

# ---------------- データ ----------------
CONCERNS = [
    "最近老けて見える気がする…",
    "ハリコシ・ボリュームがない",
    "綺麗がもっと長持ちしてほしい",
    "スタッフがコロコロ変わると落ち着かない",
    "子供がいると、なかなか美容室にいけない",
    "このまま年を取ってもこのサロンに通い続けられるのかな…",
    "私に合うアットホームな美容室がないかしら…",
]

REASONS = [
    ("01", "コンセプトは、もうひとつのリビング", "img/interior-1.jpg",
     "居心地の良い時間をお過ごしいただく為、空間作りにこだわりました。空に抜けるような高い天井、移動のないシャンプー台、大型空気清浄機完備、冬は足元から暖かい床暖房も完備しています。こだわりの極上空間であなたをお迎えいたします。"),
    ("02", "バリアフリー＆個室完備", "img/room-new.jpg",
     "店内はバリアフリーで段差もなく、車椅子、ストレッチャーの方でもご利用いただけます。また、個室も2部屋完備していますので、小さなお子様連れのママさんも安心。自慢のヘッドスパ、着付け、ブライダルシェービングも個室でゆったりお過ごしいただけます。"),
    ("03", "優しさ溢れる女性スタッフ", "img/staff-group.jpg",
     "三世代で安心して通える所以は、世代を超えた女性スタッフ。まるで昔懐かしい大家族のような明るく楽しい私たちがお出迎えいたします。「スタイリストが最後まで担当してくれるのも嬉しい！」とご好評をいただいております。"),
    ("04", "最新の技術や薬剤をご提供します", "img/products.jpg",
     "最新のデザインや技術・薬剤を求め、毎月都内まで勉強しに行くほどのこだわり。群馬県初の整体スパや髪質改善メニューなど、高崎にいながら最新のクオリティーを提供することをお約束します。年代に合わせたお悩み解決メニューでいつまでも美しく！カッコ良く！をお手伝いします。"),
    ("05", "メンズスタイルも得意です", "img/mens-style.jpg",
     "リボーンは高崎でも珍しいユニセックスサロン。オーナー廣上は理容師免許も持ち、ツイストパーマ・フェードカット・韓国風フェザーパーマなどトレンドのメンズスタイルから、ビジネスシーンの清潔感あるスタイルまで対応します。顔そり（シェービング）の気持ち良さは、男性の至福の時間。学生さんからシニアの方まで、幼い頃連れて行ってもらった理容室の醍醐味を味わえるお店です。"),
]

# おすすめメニュー（初回限定価格つき）
RECOMMEND = [
    dict(tag="髪質改善", name="ふんわり柔らかストカールエステ", img="img/menu-stcurl.jpg", normal=25000, first=23000, time="3〜3.5時間",
         desc="柔らかストレートエステで髪質改善した後、毛先にふんわりカールをデザインします。顔まわりに動きが出ることで、女性らしいとても優しい印象になります。雑誌で人気のモテ髪度NO1メニューです。",
         inc="ストレート＆カール／カット／シャンプー／ブロー／スタイリング"),
    dict(tag="髪質改善", name="柔らかストレートエステ", img="img/style-straight.jpg", normal=22999, first=21000, time="2.5〜3時間",
         desc="日本人のなんと約7割がくせ毛と言われているのをご存知ですか？そんな日本人特有のお悩みである、艶がなく広がり易いといった方にオススメです。今注目の髪質改善ストレートで、自然な艶と柔らかい髪へ導きます。永遠の憧れヘアをお手伝いいたします。",
         inc="ストレート／カット／シャンプー／ブロー／スタイリング"),
    dict(tag="髪修復", name="ふんわり小顔パーマ＆カラーエステ", img="img/menu-perm.jpg", normal=22000, first=19999, time="2〜2.5時間",
         desc="トップにボリュームが欲しい方にオススメです。修復ハリコシカラーと同時に、根元から自然なボリュームを叶えます。トップが3cm高くなると小顔効果もバッチリ。カラーとパーマを短時間で同時に行う当店オススメのメニューです。",
         inc="髪修復カラー／ふんわりパーマ／カット／シャンプー／ブロー／スタイリング"),
    dict(tag="髪質改善", name="艶髪カラーエステ", img="img/menu-color.jpg", normal=18000, first=16000, time="2時間",
         desc="透明感のあるカラーで色を楽しみながら、同時に髪質改善する当店の看板メニューです。ハリコシ・質感・艶などお客様のお悩みに合わせ施術致します。学生さん、OLさん、ママさんなど幅広い方に人気の髪質改善カラーメニューです。",
         inc="髪質改善カラー／艶髪トリートメント／カット／シャンプー／ブロー／スタイリング"),
    dict(tag="髪修復", name="ハリコシカラーエステ", img="img/menu-harikoshi.jpg", normal=15000, first=14000, time="2時間",
         desc="ただ白髪を染めるのはもう古い！年齢を重ねると細くなってしまう髪を太らせながらカラーリングする業界でも珍しい修復メニューです。ハリ・コシ・艶で若返りを目指します。",
         inc="髪修復カラー／ハリコシトリートメント／カット／シャンプー／ブロー／スタイリング"),
    dict(tag="頭皮整体スパ", name="頭皮整体スパ 癒しコース", img="img/menu-spa.jpg", normal=11000, first=10000, time="1〜1.5時間",
         desc="群馬県初！全国300カ所の整体師さんとコラボした人気の整体スパとカットがセットになったコースです。副交感神経と交感神経を交互にマッサージし、自律神経を整えます。お仕事や家事からくる日々の疲れを癒し、毛髪はもちろん、頭皮・身体・心まで美しく整えていきます。",
         inc="頭皮整体スパ／カット／シャンプー／スタイリング"),
]

PRICES = [
    ("カット", "Cut", [("ショート", "", 5400), ("ロング", "", 5700)], ""),
    ("カラー", "Color", [("カラー（ショート）", "", 8000), ("カラー（ロング）", "", 9000), ("艶めきハリコシカラー", "", 10000),
                         ("ザクロペインター", "ノンジアミンカラー", 9000), ("ハーブカラー", "", 8000), ("マニキュアカラー", "", 8500)],
     "カラーはお客様一人一人に合わせたサプリメントを入れてオーダーメイドの技術をお届けしています。カットとカラーの場合、1,000円引きになります。"),
    ("トリートメント", "Treatment", [("ラメラメ", "ホームケア付き", 4000), ("プチラメ", "", 2500), ("トステア", "", 3600)], ""),
    ("パーマ", "Perm", [("ストレートパーマ（ロング）", "スーパーケラチン・弱アルカリ配合", 23000), ("ストレートパーマ（ミドル）", "スーパーケラチン・弱アルカリ配合", 20000),
                        ("ストレートパーマ（ショート）", "スーパーケラチン・弱アルカリ配合", 18000), ("パーマ（ベリーロング）", "炭酸付", 15000),
                        ("パーマ（ロング）", "炭酸付", 13500), ("パーマ（ショート）", "炭酸付", 12000), ("トリートメントカール", "", "14,000〜")],
     "パーマはお客様一人一人に合わせたサプリメントを入れてオーダーメイドの技術をお届けしています。"),
    ("ヘッドスパ", "Head Spa", [("ヘッドスパ（45分）", "", 7500), ("ヘッドスパ（30分）", "", 6000), ("ヘッドスパ（20分）", "", 4500), ("ヘッドスパ（15分）", "", 3500)],
     "ヘアメニューと一緒の場合、1,000円引きになります。"),
    ("その他", "Others", [("レディースシェービング", "", 4400), ("レディースシェービング", "その他オプション時", 3000), ("まつ毛カール", "", 3000)], ""),
    ("メンズ・理容メニュー", "Men's / Barber", [("メンズカット＋シェービング＋眉毛カット", "フェード対応", 5400),
                                          ("カット＋フェザーパーマ（韓国風）＋シェービング＋眉カット", "", 12000),
                                          ("カット＋スパイラル系パーマ＋シェービング＋眉カット", "", 12000),
                                          ("メンズカット＋アイロンパーマ＋シェービング＋眉カット", "", 11000),
                                          ("メンズカット＋カラー", "", 11400)],
     "ツイストパーマ・フェードカットなど本格的なメンズスタイルもお任せください。オーナーは理容師免許を保有しています。※価格はホットペッパービューティー掲載のクーポン価格を掲載しています（要確認）。"),
]

STAFF = [
    dict(role="サロンオーナー", name="廣上 猶造", en="Hirokami Yuzo", img="img/staff-yuzo.jpg",
         msg="当店のホームページをご覧くださりありがとうございます。リボーン・オーナーの廣上です。当店は高崎に4代続く創業90年の理美容室です。地域の皆様には長年支えて頂き、心から感謝申し上げます。現在は娘二人も加わり、年代・性別を問わず、幅広い年代層のご要望に対応できるスタッフで営業しております。また技術や接客についても常に成長志向でチャレンジし、より良いものを提供していきます。素敵なヘアスタイルを通し、沢山の方に笑顔を届けてまいります。どうぞよろしくお願い致します。",
         birth="9/26", from_="高崎市", sign="てんびん座", hobby="ゴルフ・ワイン", lic="理容師免許・管理理容師免許・ハホニコヘアケアリスト", good="オシャレメンズヘア"),
    dict(role="カインズパースン", name="廣上 由美子", en="Hirokami Yumiko", img="img/staff-yumiko.jpg",
         msg="小さい頃、両親が美容室や床屋さんへ行くのに良く連れて行って貰いました。そこは非日常的でとても楽しくて居心地の良い場所でした。中学生になり、1人で美容室に行った時の緊張と期待と不安。でもその時の美容師さんに感動し、私もいつかお客様を綺麗にするお手伝いをしたい！と思い憧れの職業になりました。私は主にオーナーのサポート役なので、お客様のご来店からお帰りになるまで気持ち良く居心地の良い場所になるように、そして笑顔で帰って頂けるように心がけています。",
         birth="10/21", from_="富岡市", sign="てんびん座", hobby="美味しい料理で美味しいお酒をいただく事、孫達と遊ぶ事", lic="美容師免許・管理美容師免許", good="笑顔でおもてなし"),
    dict(role="トップスタイリスト", name="佐藤 未倫", en="Sato Misato", img="img/staff-misato.jpg",
         msg="私の小さい頃の夢は、保育士でした。成長していくなかで高校生の時に文化祭や体育祭で友達の髪の毛をアレンジしたりしているうちにやっぱり美容師になりたいと志すようになりました。普段の生活を考えセットしやすい髪型、やりたい事を我慢させないように時間短縮、美容室に来た時は普段自分ではできないアレンジなどをして可愛くなってもらう。お子さんには夢を与えられるような存在でいたいです。",
         birth="9/2", from_="高崎市", sign="おとめ座", hobby="旅行です。計画を立てるところからが大好きです。", lic="美容師免許・理容師免許・管理美容師免許・管理理容師免許", good="可愛いスタイル。ショートもミディアムも可愛い感じ、前髪・顔まわりを可愛くするのが得意です。"),
    dict(role="スタイリスト", name="小宮山 奈津己", en="Komiyama Natsuki", img="img/staff-natsuki.jpg",
         msg="美容師になるきっかけは、両親がこの職業についていたからです。毎日お客様が素敵になって、笑顔になるのを見て、私も美容師になりたいと強く思いました。お客様が髪だけではなく何でも気軽に相談したり話せたりする存在になりたいです。美容室に来た時だけではなく、毎日のセットをやりやすく、身近で寄り添い、すぐに思い出してもらえるような美容師でありたいです。",
         birth="10/13", from_="高崎市", sign="てんびん座", hobby="ドライブ（助手席）笑", lic="美容師免許", good="ショートスタイル。自分自身の長年のショート経験を生かして、どこにバランスをもっていくとキレイなのか、どうやったら首がキレイにみえるか考えながらカットさせていただいております。"),
    dict(role="スタイリスト・着付け師", name="林 まり子", en="Hayashi Mariko", img="img/staff-mariko.jpg",
         msg="私が美容師になったきっかけは父の言葉でした。将来何をしたいかあまり考えていなかった私に、これからは女性も手に職を持った方が良いのではないかと、そして女性が女性を美しくする事が良いのではと美容師になりました。私もそうですが、誰にでもコンプレックスがあり、その悩みを少しでも解決でき、髪のことだけでなく何でも相談できる美容師でありたいと思っています。",
         birth="5/7", from_="渋川市", sign="おうし座", hobby="孫と遊ぶ事・色々な料理を作ってみる事", lic="美容師免許・着付け技能免許", good="骨格を生かしたショートスタイル・着付け"),
    dict(role="スタイリスト", name="狩野 沙也加", en="Kano Sayaka", img="img/staff-sayaka.jpg",
         msg="美容師になりたいと思ったのは、おばあちゃんがきっかけです。小さい頃は髪の毛がすごく長かったので、おばあちゃんが毎日髪の毛を結んだり編んだりしてくれました。それを見よう見まねでお人形で遊んだり、母が知り合いからマネキンを貰ってきてハサミで切ってみたり、美容師という職業を知ってからはずっとなりたい夢でした。お客様のなりたいスタイルを作るだけでなく、頭皮や髪の毛のお悩みを解決できるような美容師になりたいです。",
         birth="3/30", from_="前橋市", sign="おひつじ座", hobby="美味しいもの巡りです。とにかく食べることが大好きです。", lic="美容師免許", good="お客様の雰囲気に合わせて可愛くアレンジをしたり、可愛い巻き方をレクチャーすることが得意です。"),
    dict(role="アシスタント", name="白石 絵理奈", en="Shiraishi Erina", img="img/staff-erina.jpg",
         msg="私が美容師を目指したきっかけは、何よりお客様に喜んで頂く仕事がしたかったからです。自分も髪型を変えることで気分が上がったり、心機一転新たな気持ちになる事が出来ます。美容師という仕事を通し、沢山の笑顔のお手伝いが出来るよう頑張ります。",
         birth="9/22", from_="高崎市", sign="おとめ座", hobby="旅行", lic="美容師免許", good="笑顔とヘッドスパ"),
]

VOICES = [
    dict(title="次も来たい！と思える居心地のいいサロンです！", who="M.F様（20代）", img="img/voice-1.jpg",
         q1="きっかけは家族の紹介です。",
         q2="髪質を考えて、髪型や行うプランを一緒に考えてくださり、いつでも髪質を把握してもらってるので、普段ヘアセットする時のちょっとした悩みも相談しやすい。親身になって話を聞いてくれるので、次も来たい！！と毎回思う。",
         q3="ヘッドスパがとっても気持ちよく、全ての施術を個室で行なってもらえるところが、とってもお気に入りです♡ 担当の方以外のスタッフさんも親身に話しかけてくださるので、居心地が良いです。"),
    dict(title="技術はもちろん髪へのこだわりが魅力！", who="H.T様（30代）", img="img/voice-2.jpg",
         q1="群馬に来てから美容室を何件も試しましたが、どこも普通（想定内）でした。そのような状況でたまたま見つけたこちらのお店と出会い、以後8年近く通う信頼の店になりました。",
         q2="カットの技術はもちろん、美容や栄養の面から髪のことにこだわるオーナーの仕事ぶりが素敵です。ここ以外に行く理由がありません！",
         q3="好きなところは、居心地の良い空間とスタッフの方の心遣いです。"),
    dict(title="新しい提案で毎回行くのが楽しみになるサロン！", who="S様ファミリー", img="img/voice-3.jpg",
         q1="近所に引っ越してきて、お店の前をよく通るようになり素敵なお店だったので、一度来て見たいと思っていました。",
         q2="アットホームな雰囲気と常に新しい事を取り入れて提案してくれるので、いつも行くのが楽しみになります。",
         q3="こちらの希望に応えてくれるところや、お店の皆さんが親切に対応してくれるところです。子供達には、みさとさんが良き相談相手であり、いつも可愛くしてくれるカリスマの様な存在です！"),
    dict(title="居心地がよく、カット、スタッフの方、すべてがお気に入りです！", who="M.S様（60代）", img="img/voice-4.jpg",
         q1="石原にきて美容室を探していて見つけました。",
         q2="カット、その他全てが気に入っています。",
         q3="スタッフのみなさんの笑顔、親切なところです。"),
    dict(title="個室でリラックスできるサロン！", who="F.M様（60代）", img="img/voice-5.jpg",
         q1="ヘッドスパをしているお店を探していたら、孫が紹介してくれたので。",
         q2="リラックスできるし、カラーとカットがとっても素敵です！",
         q3="個室でリラックスできることと、流していただける音楽がお気に入りです。"),
]

FAQ = [
    ("それぞれのメニューの最終受付時間を教えてください。", "最終受付時間は、カット 18:30、カラー・パーマ 18:00 となります。"),
    ("クレジットカードは使えますか？", "はい、すべて使えるようにしてございます。VISA・Mastercard・JCB・American Express がご利用いただけます。"),
    ("当日予約でも大丈夫ですか？", "はい、可能です。当店は予約優先制となっておりますが、空きがあれば当日でもご案内が可能です。どうぞお気軽にお問い合わせください。"),
    ("担当者の指名はできますか？", "はい、可能です。当店では指名料は頂いておりませんので、どうぞお気軽にお申し付けください。"),
    ("早朝も受け付けていますか？", "はい、早朝も別途料金にて承っております。前日のお問い合わせですと承れないことが多いので、お手数ですがお早めにご連絡いただけますと幸いです。"),
    ("家に帰ると美容院でやってもらったようにはセットできません。", "ご自宅でも簡単に再現ができるように、スタイリングの仕方やアレンジ方法などもご紹介しております！お気軽にお申し付けください。"),
    ("お直しはしてもらえますか？", "はい、当店では1週間以内のお直しを無料で承っております。また、お直しすることのないよう、はじめのカウンセリングにてお客様のお悩みやイメージをきちんとお伺いすることを大切にしております。"),
    ("駐車場はありますか？", "はい、店舗目の前に10台分の駐車場をご用意しています。高崎駅からはお車で約3分です。"),
    ("子供と一緒に行っても大丈夫ですか？", "はい、個室を2部屋ご用意しておりますので、小さなお子様連れの方も安心してご利用いただけます。店内はバリアフリーで、車椅子・ストレッチャーの方もご利用いただけます。"),
    ("男性でも利用できますか？", "もちろんです。当店は高崎でも珍しいユニセックスサロンで、オーナーは理容師免許も保有しています。シェービング（顔そり）やツイストパーマ・フェードカットなどメンズスタイルもお任せください。"),
]

# ---------------- ヘルパ ----------------
def yen(v):
    return v if isinstance(v, str) else "{:,}".format(v)

def esc(s):
    return html.escape(s, quote=True)

def header(active):
    links = "".join(
        '<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if h == active else "", esc(ja))
        for h, ja, en in NAV)
    drawer = "".join('<a href="%s">%s<small>%s</small></a>' % (h, esc(ja), en) for h, ja, en in NAV)
    return f'''
<header class="header">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="RE・BORN hair & relax ホーム"><img src="img/logo.png" alt="RE・BORN hair &amp; relax" width="320" height="72"><small>Takasaki</small></a>
    <nav class="nav" aria-label="メインメニュー">{links}<a class="btn btn-primary btn-sm" href="reserve.html">{ICON['cal']}WEB予約</a></nav>
    <button class="burger" aria-label="メニューを開く" aria-expanded="false" aria-controls="drawer"><span></span><span></span><span></span></button>
  </div>
</header>
<div class="drawer" id="drawer" inert>
  {drawer}
  <a href="reserve.html">WEB予約（空き状況カレンダー）<small>Reservation</small></a>
  <div class="cta">
    <a class="btn btn-primary" href="reserve.html">{ICON['cal']}WEB予約（空き状況カレンダー）</a>
    <a class="btn btn-line" href="{SHOP['line_add']}" target="_blank" rel="noopener">{ICON['line']}LINEで相談・予約</a>
    <a class="btn btn-tel" href="{SHOP['tel_href']}">{ICON['tel']}{SHOP['tel']}</a>
  </div>
</div>'''

def marquee():
    words = ["Hair Quality Improvement", "Head Spa", "Men's Barber", "Kimono Dressing", "Private Rooms", "Since 1935 in Takasaki"]
    return "".join(f"<span>{w}</span>" for w in words * 2)

def before_after():
    items = [("img/ba-4.jpg", "髪質改善ストレート", "広がりとパサつきが、指どおりの良いまとまる髪に"), ("img/ba-3.jpg", "髪質改善カラートリートメント", "色を楽しみながら、艶とハリを同時に"),
             ("img/ba-2.jpg", "髪質改善カラー（ボブ）", "ダメージ毛でも柔らかい質感に"), ("img/ba-1.jpg", "髪質改善カラートリートメント（ロング）", "根元から毛先までなめらかな艶")]
    return '<div class="ba stagger">' + "".join(f'<figure class="ba-item"><img src="{src}" alt="{esc(t)} ビフォーアフター" loading="lazy"><figcaption><b>{esc(t)}</b>{esc(d)}</figcaption></figure>' for src, t, d in items) + '</div><p class="small text-muted center" style="margin-top:14px">写真は当店のお客様の施術例（左：施術前／右：施術後）。</p>'

def ctaband():
    return f'''
<section class="ctaband">
  <img class="plx" src="img/interior-2.jpg" alt="" loading="lazy">
  <div class="wrap">
    <h2>ご予約・ご相談はお気軽に</h2>
    <p>空き状況カレンダーからのWEB予約・LINE・お電話からご予約いただけます。<br>初めての方も、髪のお悩み相談だけでも大歓迎です。</p>
    <div class="cta">
      <a class="btn btn-white" href="reserve.html">{ICON['cal']}WEB予約（空き状況カレンダー）</a>
      <a class="btn btn-line" href="{SHOP['line_add']}" target="_blank" rel="noopener">{ICON['line']}LINEで相談・予約</a>
    </div>
    <a class="tel" href="{SHOP['tel_href']}">{SHOP['tel']}</a>
    <div class="hours">受付 {SHOP['hours']}（定休日：{SHOP['closed']}）</div>
  </div>
</section>'''

def footer(fname=""):
    links = "".join('<li><a href="%s">%s</a></li>' % (h, esc(ja)) for h, ja, en in NAV)
    return f'''
<footer class="footer">
  <div class="wrap">
    <div class="cols">
      <div>
        <a class="brand" href="index.html"><img src="img/logo.png" alt="RE・BORN hair &amp; relax" width="320" height="72"></a>
        <p>〒{SHOP['zip']} {SHOP['addr']}</p>
        <p>TEL <a href="{SHOP['tel_href']}">{SHOP['tel']}</a></p>
        <p>営業時間 {SHOP['hours']}（最終受付 {SHOP['last']}）</p>
        <p>定休日 {SHOP['closed']}　／　駐車場 10台</p>
        <div class="sns">
          <a href="{SHOP['ig']}" target="_blank" rel="noopener" aria-label="Instagram">{ICON['ig']}</a>
          <a href="{SHOP['line_add']}" target="_blank" rel="noopener" aria-label="LINE">{ICON['line']}</a>
          <a href="{SHOP['tel_href']}" aria-label="電話">{ICON['tel']}</a>
        </div>
      </div>
      <div>
        <h4>Menu</h4>
        <ul>{links}<li><a href="reserve.html">WEB予約</a></li></ul>
      </div>
      <div>
        <h4>Links</h4>
        <ul>
          <li><a href="{SHOP['ig']}" target="_blank" rel="noopener">Instagram {SHOP['ig_id']}</a></li>
          <li><a href="{SHOP['hpb']}" target="_blank" rel="noopener">ホットペッパービューティー</a></li>
          <li><a href="{SHOP['recruit']}" target="_blank" rel="noopener">美容師求人募集</a></li>
          <li><a href="privacy.html">プライバシーポリシー</a></li>
        </ul>
      </div>
    </div>
    <div class="copy"><span>© RE・BORN hair &amp; relax</span><span>高崎に4代続く創業90年の理美容室</span></div>
  </div>
</footer>
<nav class="stickybar" aria-label="予約・お問い合わせ">
  <a href="{SHOP['tel_href']}">{ICON['tel']}<b>電話する</b></a>
  <a class="line" href="{SHOP['line_add']}" target="_blank" rel="noopener">{ICON['line']}<b>LINE予約</b></a>
  <a class="web" href="{"#resv-form" if fname == "reserve.html" else "reserve.html"}">{ICON['cal']}<b>{"予約に戻る" if fname == "reserve.html" else "WEB予約"}</b></a>
</nav>'''

def jsonld():
    data = {
        "@context": "https://schema.org",
        "@type": ["HairSalon", "BeautySalon"],
        "name": SHOP["name"],
        "alternateName": SHOP["name_ja"],
        "url": BASE_URL,
        "telephone": "+81-800-800-8835",
        "image": BASE_URL + "img/exterior.jpg",
        "address": {"@type": "PostalAddress", "postalCode": SHOP["zip"], "addressRegion": "群馬県", "addressLocality": "高崎市", "streetAddress": "聖石町13-1", "addressCountry": "JP"},
        "geo": {"@type": "GeoCoordinates", "latitude": 36.3158, "longitude": 138.9900},
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": "09:00", "closes": "18:30"}],
        "priceRange": "¥¥",
        "paymentAccepted": "Cash, Credit Card",
        "currenciesAccepted": "JPY",
        "sameAs": [SHOP["ig"], SHOP["hpb"]],
    }
    return '<script type="application/ld+json">%s</script>' % json.dumps(data, ensure_ascii=False, indent=1)

def gate_script(fname):
    """仮公開用の簡易ゲート。localStorage にハッシュ一致トークンが無ければ gate.html へ。"""
    return ('<script>(function(){var T="%s";try{if(localStorage.getItem("rb_gate")===T)return;}catch(e){}try{if(sessionStorage.getItem("rb_gate")===T)return;}catch(e){}'
            'document.documentElement.style.visibility="hidden";location.replace("gate.html?next="+encodeURIComponent((location.pathname.split("/").pop()||"index.html")+location.search+location.hash));})();</script>' % gate_hash(GATE_PASS))

def build_gate():
    h = gate_hash(GATE_PASS)
    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>閲覧用パスワード｜RE・BORN hair & relax（サイト案）</title>
<meta name="robots" content="noindex,nofollow">
<link rel="icon" href="img/logo-s.png">
<link rel="stylesheet" href="assets/style.css?v={VER}">
<style>.gate{{min-height:100svh;display:flex;align-items:center;justify-content:center;padding:24px}}.gate .box{{background:#fff;border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);padding:34px 28px;max-width:420px;width:100%}}.gate img{{height:34px;margin:0 auto 18px}}.gate h1{{font-size:20px;text-align:center;margin-bottom:6px}}.gate p{{font-size:13px;color:var(--muted);text-align:center;margin-bottom:18px}}.gate input{{width:100%;font:inherit;font-size:18px;letter-spacing:.2em;text-align:center;padding:12px 14px;border:1px solid #cfc8b9;border-radius:10px;background:#fbfaf7}}.gate .btn{{width:100%;margin-top:12px}}.gate .err{{color:#c0392b;font-size:13px;text-align:center;margin:10px 0 0;min-height:1.5em}}.gate .safe{{margin-top:22px;padding-top:18px;border-top:1px dashed var(--line);font-size:12.5px;color:#3d3a34;line-height:1.7}}.gate .safe b{{display:block;color:var(--green);font-size:13px;margin-bottom:6px}}.gate .safe ul{{padding-left:18px;list-style:disc;margin:0}}.gate .safe li{{margin-bottom:4px}}</style>
</head>
<body>
<main class="gate">
  <form class="box" id="gate">
    <img src="img/logo.png" alt="RE・BORN hair &amp; relax">
    <h1>新しいホームページ案（非公開プレビュー）</h1>
    <p>「新しいホームページはこんな雰囲気・こんな機能にできます」というデザインの見本です。写真・文言・メニューはすべて差し替え可能で、この内容で公開するものではありません。<br>ご確認用のパスワードを入力してください。</p>
    <input type="password" name="pw" inputmode="numeric" autocomplete="off" autofocus aria-label="パスワード">
    <button type="submit" class="btn btn-primary">開く</button>
    <p class="err" id="gate-err" aria-live="polite"></p>
    <div class="safe">
      <b>このページは一般には公開されていません</b>
      <ul>
        <li>このURLとパスワードの両方を知っている方だけが閲覧できます。</li>
        <li>Google などの検索エンジンに登録されない設定（noindex）にしており、検索しても出てきません。</li>
        <li>現在のホームページ（re-born2005.com）には一切影響ありません。そのまま通常どおり表示されています。</li>
        <li>ご確認が終わりましたら、このプレビューは削除します。写真・文言の差し替えはご要望に合わせて何度でも調整できます。</li>
      </ul>
      <b style="margin-top:14px">この見本の作り方</b>
      <ul>
        <li>現在のホームページ（re-born2005.com）とホットペッパービューティーの掲載内容・写真をもとに構成しています。Instagram（@reborn84）はリンク先として掲載しています。</li>
        <li>営業時間・料金・スタッフ紹介は上記からの転記です。メンズ・理容メニューの価格はホットペッパー掲載のクーポン価格を載せています（要確認）。</li>
        <li>「WEB予約」ページのカレンダーの空き状況はデモ用のダミーです。実際の予約は現在どおりお電話・LINE・ホットペッパーで承ります。</li>
      </ul>
    </div>
  </form>
</main>
<script>
(function(){{
  var EXPECT="{h}";
  function hash(pw){{var h=5381;for(var i=0;i<pw.length;i++){{h=((Math.imul(h,33))^pw.charCodeAt(i))>>>0;}}return h.toString(16)+pw.length;}}
  var f=document.getElementById("gate"),err=document.getElementById("gate-err");
  var next=new URLSearchParams(location.search).get("next")||"index.html";
  if(!/^[a-z0-9_-]+\.html(\?[^#]*)?(#[a-z0-9_-]*)?$/i.test(next))next="index.html";
  function has(){{try{{if(localStorage.getItem("rb_gate")===EXPECT)return true;}}catch(e){{}}try{{if(sessionStorage.getItem("rb_gate")===EXPECT)return true;}}catch(e){{}}return false;}}
  if(has()){{location.replace(next);return;}}
  if(location.protocol==="file:"){{err.textContent="ローカルファイルとして開いています。ブラウザによってはパスワードの保存が効かないため、公開URLからご覧ください。";}}
  f.addEventListener("submit",function(ev){{ev.preventDefault();var pw=f.pw.value.trim();
    if(hash(pw)!==EXPECT){{err.textContent="パスワードが違います。";f.pw.select();return;}}
    try{{localStorage.setItem("rb_gate",EXPECT);}}catch(e){{}}
    try{{sessionStorage.setItem("rb_gate",EXPECT);}}catch(e){{}}
    if(!has()){{err.textContent="ブラウザの設定（プライベートモードやサイトデータのブロック）により保存できませんでした。通常のブラウザでお試しください。";return;}}
    location.replace(next);}});
}})();
</script>
</body>
</html>'''

def page(fname, title, desc, body, active=None, og_title=None):
    full_title = title + "｜RE・BORN hair & relax（高崎市聖石町）" if fname != "index.html" else title
    return f'''<!DOCTYPE html>
<html lang="ja" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="noindex,nofollow">
<meta name="theme-color" content="#161514">
<meta property="og:type" content="website">
<meta property="og:site_name" content="RE・BORN hair &amp; relax">
<meta property="og:title" content="{esc(og_title or full_title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{BASE_URL}{fname}">
<meta property="og:image" content="{BASE_URL}img/og-image.jpg">
<meta property="og:locale" content="ja_JP">
<link rel="icon" href="img/logo-s.png">
{gate_script(fname)}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@400;600;700&family=Noto+Sans+JP:wght@400;500;700&family=Cormorant+Garamond:ital,wght@0,500;1,500;1,600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css?v={VER}">
<link rel="stylesheet" href="assets/motion.css?v={VER}">
{jsonld()}
</head>
<body>
{header(active or fname)}
<main>
{body}
</main>
{footer(fname)}
<script src="assets/main.js?v={VER}" defer></script>
<script src="assets/motion.js?v={VER}" defer></script>
</body>
</html>'''

def pagehead(en, h1, lead, img):
    return f'''
<section class="pagehead">
  <img src="{img}" alt="" fetchpriority="high">
  <div class="wrap"><span class="en">{en}</span><h1>{esc(h1)}</h1><p>{lead}</p></div>
</section>'''

def sec_head(en, h2, p="", center=False):
    return f'<div class="sec-head{" center" if center else ""} rv"><span class="en">{en}</span><h2>{esc(h2)}</h2>{("<p>"+p+"</p>") if p else ""}</div>'

def menu_card(m):
    from urllib.parse import quote
    q = quote("初回限定：" + m["name"])
    return f'''
<article class="card rv">
  <figure class="rv-img from-up"><img src="{m['img']}" alt="{esc(m['name'])}" loading="lazy" width="300" height="450"><span class="tag">{esc(m['tag'])}</span></figure>
  <div class="body">
    <h3>{esc(m['name'])}</h3>
    <div class="price"><s>通常 {yen(m['normal'])}円</s><b>¥{yen(m['first'])}</b><em>初回限定</em></div>
    <p>{esc(m['desc'])}</p>
    <div class="meta"><span>⏱ {esc(m['time'])}</span><span>含：{esc(m['inc'])}</span></div>
    <a class="go" href="reserve.html">空き状況を見て予約する →</a>
  </div>
</article>'''

def voice_card(v, full=False, h="h3"):
    body = f'''<dl>
      <dt>ご来店のキッカケ</dt><dd>{esc(v['q1'])}</dd>
      <dt>長く通ってくださる理由</dt><dd>{esc(v['q2'])}</dd>
      <dt>当店の好きなところ</dt><dd>{esc(v['q3'])}</dd>
    </dl>''' if full else f'<p class="quote">「{esc(v["q2"])}」</p>'
    return f'''
<article class="voice rv">
  <figure class="rv-img"><img src="{v['img']}" alt="{esc(v['who'])}" loading="lazy"></figure>
  <div class="body"><{h}>{esc(v['title'])}</{h}><div class="who">{esc(v['who'])}</div>{body}</div>
</article>'''

def staff_card(s):
    return f'''
<a class="staff rv" href="staff.html#{s['en'].split()[1].lower()}">
  <figure class="rv-img from-up"><img src="{s['img']}" alt="{esc(s['name'])}" loading="lazy"></figure>
  <div class="body"><div class="role">{esc(s['role'])}</div><h3>{esc(s['name'])}<small>{esc(s['en'])}</small></h3><p>得意：{esc(s['good'][:28])}{'…' if len(s['good'])>28 else ''}</p></div>
</a>'''

def access_block(with_route=True):
    route = f'''
<div class="route mt40">
  <figure class="rv-img"><img src="img/access-1.png" alt="国道17号 聖石橋交差点" loading="lazy"><figcaption><b>Step 1</b>国道17号線の聖石橋の交差点を観音様方面に進みます。</figcaption></figure>
  <figure class="rv-img from-right"><img src="img/access-2.png" alt="店舗前の様子" loading="lazy"><figcaption><b>Step 2</b>聖石橋を渡り一つ目の信号手前、左側に茶色の木の格子が見えてきましたら、こちらが当店です。</figcaption></figure>
  <figure class="rv-img"><img src="img/exterior.jpg" alt="店舗外観と駐車場" loading="lazy"><figcaption><b>Parking</b>駐車場は店舗目の前に広々10台。皆様のご来店を心よりお待ちしております。</figcaption></figure>
</div>''' if with_route else ""
    return f'''
<div class="access">
  <div class="rv">
    <table>
      <tr><th>住所</th><td>〒{SHOP['zip']}<br>{SHOP['addr']}</td></tr>
      <tr><th>電話</th><td><a class="tel" href="{SHOP['tel_href']}">{SHOP['tel']}</a><br><span class="small text-muted">タップで発信できます</span></td></tr>
      <tr><th>営業時間</th><td>{SHOP['hours']}<br><span class="small text-muted">最終受付：{SHOP['last']}</span></td></tr>
      <tr><th>定休日</th><td>{SHOP['closed']}</td></tr>
      <tr><th>アクセス</th><td>{SHOP['access']}</td></tr>
      <tr><th>駐車場</th><td>{SHOP['parking']}</td></tr>
      <tr><th>お支払い</th><td>現金／VISA・Mastercard・JCB・American Express</td></tr>
    </table>
    <div class="acts">
      <a class="btn btn-outline btn-sm" href="{SHOP['map_link']}" target="_blank" rel="noopener">{ICON['map']}Googleマップで開く</a>
      <a class="btn btn-tel btn-sm" href="{SHOP['tel_href']}">{ICON['tel']}電話をかける</a>
    </div>
  </div>
  <div class="rv"><iframe src="{SHOP['map_embed']}" title="RE・BORN hair & relax の地図" loading="lazy" allowfullscreen referrerpolicy="no-referrer-when-downgrade"></iframe></div>
</div>{route}'''

# ---------------- ページ ----------------
def build_index():
    concerns = "".join(f"<li>{esc(c)}</li>" for c in CONCERNS)
    reasons = "".join(f'''
<div class="reason rv">
  <figure class="rv-img{" from-right" if int(n) % 2 == 0 else ""}"><img src="{img}" alt="{esc(t)}" loading="lazy"></figure>
  <div><div class="num">Reason {n}</div><h3>{esc(t)}</h3><p>{esc(d)}</p></div>
</div>''' for n, t, img, d in REASONS)
    cards = "".join(menu_card(m) for m in RECOMMEND[:3])
    voices = "".join(voice_card(v) for v in VOICES[:3])
    staff = "".join(staff_card(s) for s in STAFF[:4])
    style_imgs = [("img/style-straight.jpg", "髪質改善ストレート"), ("img/menu-stcurl.jpg", "ふんわりストカール"), ("img/style-mens-perm-1.jpg", "メンズパーマ"), ("img/menu-color.jpg", "艶髪カラー"), ("img/style-mens-fade.jpg", "フェードカット"), ("img/style-mens-perm-2.jpg", "韓国風フェザーパーマ"), ("img/menu-perm.jpg", "ふんわり小顔パーマ"), ("img/style-mens-3.jpg", "大人メンズスタイル"), ("img/kitsuke-12.jpg", "成人式ヘアセット"), ("img/style-mens-5.jpg", "ウェーブパーマ"), ("img/menu-harikoshi.jpg", "ハリコシカラー"), ("img/style-mens-4.jpg", "ツイストパーマ")]
    styles = "".join(f'<a href="{SHOP["ig"]}" target="_blank" rel="noopener"><img src="{src}" alt="{esc(alt)}" loading="lazy"></a>' for src, alt in style_imgs)
    badges = "".join(f"<li>{b}</li>" for b in ["当日予約OK", "個室2部屋", "お子様同伴OK", "メンズ大歓迎", "駐車場10台", "バリアフリー"])
    body = f'''
<div class="intro" id="intro" aria-hidden="true"><img src="img/logo.png" alt=""><span class="line"></span><span class="en">Hair &amp; Relax — Takasaki</span></div>
<section class="hero">
  <img class="bg" src="img/exterior.jpg" alt="RE・BORN hair & relax 店舗外観" fetchpriority="high">
  <div class="wrap">
    <div class="eyebrow">Hair &amp; Relax Salon, Takasaki</div>
    <h1>地域に愛されて90年。<br>三世代で通える、<br>もうひとつのリビング。</h1>
    <p class="lead">高崎市聖石町の髪質改善が得意なリラックスサロン。高い天井と個室のある居心地のよい空間で、お子様からシニアの方、メンズまで、家族みんなの「きれい」と「かっこいい」をお手伝いします。</p>
    <ul class="badges">{badges}</ul>
    <div class="cta">
      <a class="btn btn-primary" href="reserve.html">{ICON['cal']}空き状況を見て予約する</a>
      <a class="btn btn-line" href="{SHOP['line_add']}" target="_blank" rel="noopener">{ICON['line']}LINEで相談・予約</a>
      <a class="btn btn-white" href="{SHOP['tel_href']}">{ICON['tel']}{SHOP['tel']}</a>
    </div>
  </div>
  <div class="scroll">Scroll</div>
</section>

<div class="marquee" aria-hidden="true"><div class="track">{marquee()}</div></div>
<div class="infostrip">
  <div class="wrap">
    <div class="cell">{ICON['clock']}<div><b>Open</b><span>{SHOP['hours']}<br>最終受付 {SHOP['last']}</span></div></div>
    <div class="cell">{ICON['cal']}<div><b>Closed</b><span>定休日：{SHOP['closed']}</span></div></div>
    <div class="cell">{ICON['pin']}<div><b>Access</b><span>{SHOP['addr']}<br>高崎駅より車で3分・駐車場10台</span></div></div>
    <div class="cell">{ICON['tel']}<div><b>Tel</b><a class="tel" href="{SHOP['tel_href']}">{SHOP['tel']}</a><span>タップで発信できます</span></div></div>
  </div>
</div>

<section class="sec">
  <div class="wrap">
    {sec_head("Concerns", "こんなお悩みありませんか？")}
    <div class="concern">
      <ul class="list stagger">{concerns}</ul>
      <div>
        <figure class="rv-img"><img src="img/collage.jpg" alt="店内の様子" loading="lazy"></figure>
        <div class="note rv mt24">もし1つでも当てはまれば、<br>当サロンへお越しください。<small>髪質改善・ヘッドスパ・個室・三世代で通えるスタッフ。あなたの「困った」に、90年の技術と居心地で応えます。</small></div>
      </div>
    </div>
  </div>
</section>

<section class="sec alt">
  <div class="wrap">
    <div class="greet">
      <figure class="rv-img"><img src="img/owner-work.jpg" alt="オーナー 廣上 猶造" loading="lazy"></figure>
      <div class="rv">
        <span class="sec-head"><span class="en">Greeting</span></span>
        <h2 class="lead">高崎に4代続く、<br>創業90年の理美容室です。</h2>
        <div class="msg">
          <p>当店のホームページをご覧いただきありがとうございます。リボーン・オーナーの廣上です。当店は、高崎に4代続く創業90年の理美容室です。地域の皆様には長年支えて頂き、心から感謝申し上げます。</p>
          <p>現在は娘二人も加わり、年代・性別を問わず、幅広い年代層のご要望に対応できるスタッフで営業しております。常により良いものを提供する姿勢を忘れずに、技術や接客についても、常に成長志向でチャレンジし続けております。</p>
          <p>素敵なヘアスタイルを通し、沢山の方に笑顔をお届けできるよう、日々精進してまいります。どうぞよろしくお願いいたします。</p>
        </div>
        <div class="sign">廣上 猶造<small>サロンオーナー / Hirokami Yuzo</small></div>
      </div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    {sec_head("Reasons", "当サロンが選ばれる5つの理由", "居心地・設備・人・技術。長く通っていただくために、私たちが大切にしていること。")}
    {reasons}
  </div>
</section>

<section class="sec alt">
  <div class="wrap">
    {sec_head("Before / After", "髪質改善で、髪はここまで変わります", "広がり・パサつき・うねり。カラーやストレートと同時に髪質を整える当店の看板メニューの実例です。")}
    {before_after()}
  </div>
</section>

<section class="sec">
  <div class="wrap">
    {sec_head("Recommended Menu", "おすすめメニュー", "初めての方は初回限定価格でお試しいただけます。すべてカット・シャンプー・スタイリング込みの価格です（税込）。")}
    <div class="cards">{cards}</div>
    <div class="more"><a class="btn btn-outline" href="menu.html">メニュー・料金をすべて見る</a></div>
  </div>
</section>

<section class="sec dark">
  <div class="wrap">
    {sec_head("Benefits", "初めての方へ、2つの安心")}
    <div class="offers">
      <div class="offer rv"><span class="en">First Visit Gift</span><h3>「ホームページをみました」で<br>高濃度炭酸泉をプレゼント</h3><p>初回限定で、通常<b>1,000円</b>の高濃度炭酸泉を無料でサービス。ご予約時またはご来店時に「ホームページをみました」とお伝えください。</p></div>
      <div class="offer rv"><span class="en">1 Week Guarantee</span><h3>ヘアスタイル1週間保証</h3><p>ヘアスタイルに満足していただけない場合は、<b>1週間以内でしたら無料</b>でお直しさせていただきます。お気軽にご相談ください。</p></div>
    </div>
  </div>
</section>

<section class="sec alt">
  <div class="wrap">
    {sec_head("Voice", "お客様の声", "20代から60代まで、ご家族三世代で通ってくださるお客様の声をご紹介します。")}
    <div class="voices">{voices}</div>
    <div class="more"><a class="btn btn-outline" href="voice.html">お客様の声をもっと見る</a></div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    {sec_head("Staff", "スタッフ紹介", "世代を超えたスタッフが、カウンセリングから仕上げまで最後まで担当します。指名料はいただきません。")}
    <div class="staffgrid">{staff}</div>
    <div class="more"><a class="btn btn-outline" href="staff.html">スタッフをすべて見る</a></div>
  </div>
</section>

<section class="sec alt">
  <div class="wrap">
    {sec_head("Style & Instagram", "スタイル・最新情報はInstagramで", "髪質改善のビフォーアフター、メンズパーマ、着付けなど最新のスタイルを日々更新しています。")}
    <div class="igrid stagger">{styles}</div>
    <div class="more"><a class="btn btn-primary" href="{SHOP['ig']}" target="_blank" rel="noopener">{ICON['ig']}Instagram {SHOP['ig_id']} をフォロー</a></div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    {sec_head("Access", "アクセス", "高崎駅西口から聖石橋方面へ。橋を渡り切った先の左手、茶色の木の格子が目印です。")}
    {access_block(with_route=False)}
    <div class="more"><a class="btn btn-outline" href="access.html">道順・駐車場の写真を見る</a></div>
  </div>
</section>
{ctaband()}'''
    return page("index.html", "RE・BORN hair & relax｜高崎市聖石町の髪質改善が得意な美容室・理容室",
                "群馬県高崎市聖石町の理美容室 RE・BORN hair & relax（リボーン）。創業90年・三世代で通える個室完備のリラックスサロン。髪質改善・ヘッドスパ・メンズカット・着付け。当日予約OK・駐車場10台。WEB予約・LINE予約に対応。", body)

def build_menu():
    cards = "".join(menu_card(m) for m in RECOMMEND)
    groups = ""
    for ja, en, items, note in PRICES:
        gid = "g-" + en.lower().replace(" ", "-").replace("'", "").replace("/", "")
        lis = "".join(f'<li><span>{esc(n)}{("<small>"+esc(s)+"</small>") if s else ""}</span><b>¥{yen(p)}</b></li>' for n, s, p in items)
        groups += f'<div class="pricegroup rv" id="{gid}"><h3>{esc(ja)}<small>{en}</small></h3><ul>{lis}</ul>{("<p class=note>※"+esc(note)+"</p>") if note else ""}</div>'
    jump = '<div class="jump">' + "".join(f'<a href="#{ "g-" + en.lower().replace(" ", "-").replace(chr(39), "").replace("/", "") }">{esc(ja)}</a>' for ja, en, items, note in PRICES) + '<a href="#recommend">初回限定</a></div>'
    body = pagehead("Menu &amp; Price", "メニュー・料金", "初めての方は「おすすめメニュー」の初回限定価格（税込）をご利用ください。" + jump, "img/products.jpg") + f'''
<section class="sec" id="recommend">
  <div class="wrap">
    {sec_head("Recommended", "おすすめメニュー（初回限定価格あり）", "カット・シャンプー・ブロー・スタイリング込み。施術時間の目安も記載しています。")}
    <div class="cards">{cards}</div>
    <h3 class="center" style="margin:48px 0 18px;font-size:22px">髪質改善メニューの施術例</h3>
    {before_after()}
    <div class="notice rv"><b>初回特典：</b>「ホームページをみました」とお伝えいただくと、高濃度炭酸泉（通常1,000円）をプレゼント。<b>1週間保証：</b>仕上がりにご満足いただけない場合は1週間以内なら無料でお直しします。</div>
  </div>
</section>
<section class="sec alt">
  <div class="wrap">
    {sec_head("Price List", "通常メニュー")}
    <div class="pricegrid">{groups}</div>
    <div class="notice rv">指名料はいただいておりません。早朝のご予約は別途料金にて承ります（前日のお問い合わせですと承れないことが多いため、お早めにご連絡ください）。</div>
    <div class="more"><a class="btn btn-primary" href="reserve.html">{ICON['cal']}空き状況を見て予約する</a></div>
  </div>
</section>
{ctaband()}'''
    return page("menu.html", "メニュー・料金", "RE・BORN hair & relax のメニュー・料金表。髪質改善・ストレート・カラー・パーマ・ヘッドスパ・メンズ理容メニュー。初回限定価格あり。", body)

def build_staff():
    profs = ""
    for s in STAFF:
        pid = s['en'].split()[1].lower()
        profs += f'''
<div class="profile rv" id="{pid}">
  <figure class="rv-img"><img src="{s['img']}" alt="{esc(s['name'])}" loading="lazy"></figure>
  <div>
    <div class="role">{esc(s['role'])}</div>
    <h2>{esc(s['name'])}<small>{esc(s['en'])}</small></h2>
    <p class="msg">{esc(s['msg'])}</p>
    <table>
      <tr><th>誕生日</th><td>{esc(s['birth'])}</td></tr>
      <tr><th>出身地</th><td>{esc(s['from_'])}</td></tr>
      <tr><th>星座</th><td>{esc(s['sign'])}</td></tr>
      <tr><th>趣味</th><td>{esc(s['hobby'])}</td></tr>
      <tr><th>保有免許</th><td>{esc(s['lic'])}</td></tr>
      <tr><th>得意なこと</th><td>{esc(s['good'])}</td></tr>
    </table>
  </div>
</div>'''
    body = pagehead("Staff", "スタッフ紹介", "世代を超えた女性スタッフと理容師免許を持つオーナー。カウンセリングから仕上げまで、最後まで同じスタイリストが担当します。", "img/staff-group.jpg") + f'''
<section class="sec">
  <div class="wrap">{profs}
    <div class="more"><a class="btn btn-primary" href="reserve.html">{ICON['cal']}スタイリストを指名して予約する（指名料無料）</a></div>
  </div>
</section>
{ctaband()}'''
    return page("staff.html", "スタッフ紹介", "RE・BORN hair & relax のスタッフ紹介。オーナー廣上猶造ほか、三世代で通えるスタッフをご紹介。指名料無料。", body)

def build_voice():
    cards = "".join(voice_card(v, full=True, h="h2") for v in VOICES)
    body = pagehead("Voice", "お客様の声", "ご家族の紹介、近所に引っ越してきて、お孫さんの紹介で。長く通ってくださる理由をお聞きしました。", "img/voice-3.jpg") + f'''
<section class="sec"><div class="wrap"><div class="voices">{cards}</div></div></section>
{ctaband()}'''
    return page("voice.html", "お客様の声", "RE・BORN hair & relax に通ってくださるお客様の声。20代〜60代、ご家族三世代のリアルなご感想。", body)

def build_access():
    body = pagehead("Access", "アクセス", "高崎駅より車で3分。聖石橋を渡ってすぐ、店舗目の前に10台分の駐車場があります。", "img/exterior.jpg") + f'''
<section class="sec"><div class="wrap">{access_block(with_route=True)}</div></section>
{ctaband()}'''
    return page("access.html", "アクセス", "RE・BORN hair & relax（高崎市聖石町13-1）へのアクセス・道順・駐車場のご案内。高崎駅より車で3分、駐車場10台。", body)

def build_faq():
    items = "".join(f'<details class="rv"><summary>{esc(q)}</summary><div class="a">{esc(a)}</div></details>' for q, a in FAQ)
    body = pagehead("FAQ", "よくある質問", "ご予約・お支払い・お子様連れ・メンズのご利用など、よくいただくご質問にお答えします。", "img/interior-1.jpg") + f'''
<section class="sec"><div class="wrap"><div class="faq">{items}</div>
<p class="center mt40 rv">その他のご質問は、LINE またはお電話でお気軽にどうぞ。</p>
<div class="more" style="margin-top:12px"><a class="btn btn-line" href="{SHOP['line_add']}" target="_blank" rel="noopener">{ICON['line']}LINEで質問する</a></div></div></section>
{ctaband()}'''
    return page("faq.html", "よくある質問", "RE・BORN hair & relax によくいただくご質問。最終受付時間・クレジットカード・当日予約・指名・お直し保証など。", body)

def build_kitsuke():
    order = [20, 11, 12, 17, 13, 9, 19, 6, 4, 15, 2, 5, 10, 3, 18, 16, 1, 14, 7, 8]
    imgs = "".join(f'<a href="img/kitsuke-{i:02d}.jpg"><img src="img/kitsuke-{i:02d}.jpg" alt="着付け・ヘアセット事例 {n+1}" loading="lazy"></a>' for n, i in enumerate(order))
    body = pagehead("Kimono &amp; Hair Set", "着付け（成人式・卒業式）", "着付け技能免許を持つスタイリストが、着付けからヘアセットまで個室でゆったりと承ります。", "img/kitsuke-12.jpg") + f'''
<section class="sec">
  <div class="wrap">
    {sec_head("Gallery", "当店で着付けをされた方のギャラリー", "画像をタップすると拡大します。成人式・卒業式・ブライダルシェービングもご相談ください。")}
    <div class="gallery stagger">{imgs}</div>
    <div class="notice rv">成人式・卒業式は毎年ご予約が集中します。お日にちが決まりましたら、お早めにLINEまたはお電話でご相談ください。</div>
  </div>
</section>
<dialog class="lightbox" aria-label="画像の拡大表示"><button class="close" aria-label="閉じる">×</button><button class="prev" aria-label="前へ">‹</button><img alt=""><button class="next" aria-label="次へ">›</button></dialog>
{ctaband()}'''
    return page("kitsuke.html", "着付け（成人式・卒業式）", "RE・BORN hair & relax の着付け・ヘアセット事例ギャラリー。成人式・卒業式の着付けは個室で。着付け技能免許保有スタイリストが担当。", body)

def build_reserve():
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
    body = pagehead("Reservation", "WEB予約", "24時間いつでも、空き状況を見ながらご予約いただけます。当日のご予約はお電話が確実です。", "img/shampoo-new.jpg") + f'''
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
<script src="assets/booking.js?v={VER}" defer></script>'''
    return page("reserve.html", "WEB予約", "RE・BORN hair & relax のWEB予約。空き状況カレンダーからメニュー・スタイリスト・日時を選んで24時間ご予約いただけます。", body)

def build_privacy():
    raw = open(os.path.join(BASE, "..", "素材", "privacy.txt"), encoding="utf-8").read().strip().splitlines()
    out = ""
    for line in raw[1:]:
        line = line.strip()
        if not line: continue
        if line.startswith("## "): out += f"<h2>{esc(line[3:])}</h2>"
        else: out += f"<p>{esc(line)}</p>"
    body = pagehead("Privacy Policy", "プライバシーポリシー", "個人情報保護方針", "img/interior-1.jpg") + f'<section class="sec"><div class="wrap"><div class="prose rv">{out}</div></div></section>'
    return page("privacy.html", "プライバシーポリシー", "RE・BORN hair & relax の個人情報保護方針。", body)

def main():
    pages = {
        "index.html": build_index(), "menu.html": build_menu(), "staff.html": build_staff(), "voice.html": build_voice(),
        "access.html": build_access(), "faq.html": build_faq(), "kitsuke.html": build_kitsuke(), "reserve.html": build_reserve(), "privacy.html": build_privacy(),
        "gate.html": build_gate(),
    }
    for f, h in pages.items():
        with open(os.path.join(BASE, f), "w", encoding="utf-8", newline="\n") as fp:
            fp.write(h)
        print("wrote", f, len(h))

if __name__ == "__main__":
    main()
