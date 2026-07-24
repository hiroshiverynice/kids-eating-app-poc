# -*- coding: utf-8 -*-
"""マスター(sodateru-shokutaku-poc.html)から index.html と sodateru-tap.html を生成する。
使い方: python derive.py  （リポジトリ直下で実行）
"""
import pathlib, sys

root = pathlib.Path(__file__).parent
master = root / "sodateru-shokutaku-poc.html"
src = master.read_text(encoding="utf-8")

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
