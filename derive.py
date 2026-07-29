# -*- coding: utf-8 -*-
"""マスター(sodateru-shokutaku-poc.html)から index.html と sodateru-tap.html を生成する。
使い方: python derive.py  （リポジトリ直下で実行）
"""
import pathlib, sys

root = pathlib.Path(__file__).parent
master = root / "sodateru-shokutaku-poc.html"
src = master.read_text(encoding="utf-8")

# --- JSの構文チェック（type="module" は1つでも構文エラーがあると全体が動かなくなる）---
# 実際に「行末コメントが残りのコードを飲み込んで閉じ括弧が消える」事故が起きたため、
# 派生ファイルを書き出す前に必ず node --check を通す。
import subprocess, tempfile, os
_i = src.index('<script type="module">') + len('<script type="module">')
_j = src.rindex("</script>")
_tmp = root / "_syntax_check.mjs"
_tmp.write_text(src[_i:_j], encoding="utf-8", newline="\n")
_r = subprocess.run(["node", "--check", str(_tmp)], capture_output=True, text=True)
os.remove(_tmp)
if _r.returncode != 0:
    sys.exit("derive.py: JSの構文エラーで中断しました\n" + (_r.stderr or _r.stdout))

# index.html = マスターそのまま（手かざし版）
(root / "index.html").write_text(src, encoding="utf-8", newline="\n")

# sodateru-tap.html = カメラ不使用のタップ版
REPL = [
    ("<title>育てる食卓 PoC</title>", "<title>育てる食卓（タップ版）</title>"),
    ('<div class="eyebrow">そだてる しょくたく</div>',
     '<div class="eyebrow">そだてる しょくたく（タップ版）</div>'),
    ('<p class="prompt-big" id="prompt">ごはんを たべたら おててを かざしてね ✋</p>',
     '<p class="prompt-big" id="prompt">ごはんを たべたら ボタンを おしてね 🥄</p>'),
    ('const KEY="sodateru_v1";', 'const KEY="sodateru_tap_v1";'),
    ('camMode:true, showButton:false', 'camMode:false, showButton:true'),
]
tap = src
for a, b in REPL:
    if a not in tap:
        sys.exit("derive.py: 置換対象が見つかりません -> " + a[:60])
    tap = tap.replace(a, b, 1)

# カメラカードを隠し、ボタンを大きく（CSS末尾の直前アンカーに追記）
ANCHOR = "</style>"
CSS_ADD = "#camCard{display:none}\n.fallback{font-size:24px;padding:22px}\n"
i = tap.index(ANCHOR)
tap = tap[:i] + CSS_ADD + tap[i:]

(root / "sodateru-tap.html").write_text(tap, encoding="utf-8", newline="\n")
print("generated: index.html, sodateru-tap.html")
