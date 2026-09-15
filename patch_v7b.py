# -*- coding: utf-8 -*-
"""v7b: harden the preview gate (Codex v6) + reassuring copy on the gate page."""
import io, os
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build.py")
s = io.open(p, encoding="utf-8").read()

def rep(a, b):
    global s
    assert a in s, "NOT FOUND: " + a[:90]
    s = s.replace(a, b, 1)

# page-side check: accept localStorage OR sessionStorage token, keep hash, default index.html
rep("""    return ('<script>(function(){try{if(localStorage.getItem("rb_gate")==="%s")return;}catch(e){}'
            'document.documentElement.style.visibility="hidden";location.replace("gate.html?next="+encodeURIComponent(location.pathname.split("/").pop()+location.search));})();</script>' % gate_hash(GATE_PASS))""",
    """    return ('<script>(function(){var T="%s";try{if(localStorage.getItem("rb_gate")===T)return;}catch(e){}try{if(sessionStorage.getItem("rb_gate")===T)return;}catch(e){}'
            'document.documentElement.style.visibility="hidden";location.replace("gate.html?next="+encodeURIComponent((location.pathname.split("/").pop()||"index.html")+location.search+location.hash));})();</script>' % gate_hash(GATE_PASS))""")

# gate page: copy + robust storage handling
rep("""    <h1>サイト案の閲覧用パスワード</h1>
    <p>このページは制作中のサイト案です。パスワードを入力してください。</p>
    <input type="password" name="pw" inputmode="numeric" autocomplete="off" autofocus aria-label="パスワード">
    <button type="submit" class="btn btn-primary">開く</button>
    <p class="err" id="gate-err" aria-live="polite"></p>
  </form>""",
    """    <h1>新しいホームページ案（非公開プレビュー）</h1>
    <p>ご確認用のパスワードを入力してください。</p>
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
    </div>
  </form>""")
rep(""".gate .err{{color:#c0392b;font-size:13px;text-align:center;margin:10px 0 0;min-height:1.5em}}</style>""",
    """.gate .err{{color:#c0392b;font-size:13px;text-align:center;margin:10px 0 0;min-height:1.5em}}.gate .safe{{margin-top:22px;padding-top:18px;border-top:1px dashed var(--line);font-size:12.5px;color:#3d3a34;line-height:1.7}}.gate .safe b{{display:block;color:var(--green);font-size:13px;margin-bottom:6px}}.gate .safe ul{{padding-left:18px;list-style:disc;margin:0}}.gate .safe li{{margin-bottom:4px}}</style>""")
rep("""  if(!/^[a-z0-9_-]+\\.html(\\?.*)?$/i.test(next))next="index.html";
  try{{if(localStorage.getItem("rb_gate")===EXPECT){{location.replace(next);return;}}}}catch(e){{}}
  f.addEventListener("submit",function(ev){{ev.preventDefault();var pw=f.pw.value.trim();
    if(hash(pw)===EXPECT){{try{{localStorage.setItem("rb_gate",EXPECT);}}catch(e){{}}location.replace(next);}}
    else{{err.textContent="パスワードが違います。";f.pw.select();}}}});""",
    """  if(!/^[a-z0-9_-]+\\.html(\\?[^#]*)?(#[a-z0-9_-]*)?$/i.test(next))next="index.html";
  function has(){{try{{if(localStorage.getItem("rb_gate")===EXPECT)return true;}}catch(e){{}}try{{if(sessionStorage.getItem("rb_gate")===EXPECT)return true;}}catch(e){{}}return false;}}
  if(has()){{location.replace(next);return;}}
  if(location.protocol==="file:"){{err.textContent="ローカルファイルとして開いています。ブラウザによってはパスワードの保存が効かないため、公開URLからご覧ください。";}}
  f.addEventListener("submit",function(ev){{ev.preventDefault();var pw=f.pw.value.trim();
    if(hash(pw)!==EXPECT){{err.textContent="パスワードが違います。";f.pw.select();return;}}
    try{{localStorage.setItem("rb_gate",EXPECT);}}catch(e){{}}
    try{{sessionStorage.setItem("rb_gate",EXPECT);}}catch(e){{}}
    if(!has()){{err.textContent="ブラウザの設定（プライベートモードやサイトデータのブロック）により保存できませんでした。通常のブラウザでお試しください。";return;}}
    location.replace(next);}});""")

io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("v7b patched")
