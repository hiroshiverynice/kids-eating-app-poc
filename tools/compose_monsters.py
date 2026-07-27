# -*- coding: utf-8 -*-
"""Kenney Monster Builder Pack (CC0) のパーツを合成して、もぐもぐクエストの
モンスター画像を作る。指定は全部べた書き＝何度実行しても同じ絵が出る。

ガードレール:
  - こわい目（psycho）は使わない。おこり目も使わない。全部やさしい顔にする。
  - ×目（eye_dead）は「たおれた瞬間＝目をまわしている」状態だけに使う（_ko.png）。
    健康なモンスターには絶対に付けない。
"""
import os, glob
from PIL import Image

SRC = "cc0/monster-builder-pack/PNG/Default"
OUT = "monsters"
SHEET = "contact_sheet.png"
KO_EYE = "eye_dead.png"          # ×目＝目をまわしている（たおれた時だけ）

def P(n): return os.path.join(SRC, n)
def load(n): return Image.open(P(n)).convert("RGBA")

# id, 表示名, 色, ボディ, 目, 口, 角/耳, 腕, 脚, ボス
SPECS = [
    # 目視で同定済みのパーツだけを使う。使わないもの:
    #   eye_angry_* (おこり顔) / eye_psycho_* (こわい) / eye_blue・eye_dead (×目=気絶)
    #   mouthD・mouth_closed_fangs・mouth_closed_sad (への字＝悲しい顔)
    ("puni",  u"ぷにモン",   "blue",   "A", "eye_cute_light",      "mouthA", None,            "A", "A", False),
    ("awa",   u"あわボール", "white",  "B", "eye_human",           "mouthC", None,            "B", "B", False),
    ("kero",  u"けろまる",   "green",  "A", "eye_human_green",     "mouthE", "ear_round",     "C", "C", False),
    ("hari",  u"はりまる",   "yellow", "C", "eye_yellow",          "mouthB", "horn_small",    "D", "D", False),
    ("mofu",  u"もふりん",   "red",    "B", "eye_cute_dark",       "mouthG", "ear",           "E", "E", False),
    ("piko",  u"ぴこモン",   "blue",   "D", "eye_human_blue",      "mouthA", "antenna_small", "A", "A", False),
    ("tsuno", u"つのすけ",   "green",  "C", "eye_closed_happy",    "mouthH", "horn_large",    "B", "B", False),
    ("goma",  u"ごまちゃん", "dark",   "A", "eye_cute_light",      "mouthC", None,            "C", "C", False),
    ("hoshi", u"ほしまる",   "yellow", "B", "eye_human",           "mouthG", "antenna_large", "D", "D", False),
    ("puru",  u"ぷるるん",   "white",  "D", "eye_cute_dark",       "mouthE", None,            "E", "E", False),
    ("moko",  u"もこモン",   "red",    "A", "eye_red",             "mouthH", "ear_round",     "A", "A", False),
    ("tobi",  u"とびまる",   "blue",   "C", "eye_human_red",       "mouthB", "ear",           "B", "B", False),
    ("nyoro", u"にょろん",   "green",  "E", "eye_closed_feminine", "mouth_closed_happy", None, "C", "C", False),
    ("koro",  u"ころすけ",   "yellow", "A", "eye_cute_dark",       "mouthJ", "horn_small",    "D", "D", False),
    ("shiro", u"しろたん",   "white",  "C", "eye_human_green",     "mouthE", "antenna_small", "E", "E", False),
    ("kage",  u"かげまる",   "dark",   "B", "eye_cute_light",      "mouthA", "horn_small",    "A", "A", False),
    # ---- ボス（大きい・大きな角。こわくはしない）----
    ("boss_ryu",  u"りゅうおう", "red",    "F", "eye_human_red",   "mouthJ", "horn_large", "B", "B", True),
    ("boss_king", u"キングもふ", "yellow", "E", "eye_yellow",      "mouthF", "horn_large", "C", "C", True),
    ("boss_dark", u"やみのおう", "dark",   "F", "eye_cute_dark",   "mouthJ", "horn_large", "D", "D", True),
    ("boss_aqua", u"うみのぬし", "blue",   "E", "eye_human_blue",  "mouthG", "horn_large", "E", "E", True),
    ("boss_leaf", u"もりのぬし", "green",  "F", "eye_human_green", "mouthF", "horn_large", "A", "A", True),
    ("boss_snow", u"ゆきのおう", "white",  "E", "eye_cute_light",  "mouthC", "horn_large", "B", "B", True),
]

def compose(spec, ko=False):
    _id, name, color, bodyL, eye, mouth, detail, armL, legL, boss = spec
    if ko:
        eye = KO_EYE[:-4]
    body = load("body_%s%s.png" % (color, bodyL))
    bw, bh = body.size
    pad = int(bw * 0.55)
    W, H = bw + pad * 2, bh + pad + int(bh * 0.18)
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bx, by = pad, pad

    def put(img, cx, cy):
        canvas.alpha_composite(img, (int(cx - img.width / 2), int(cy - img.height / 2)))

    def fit(img, frac):
        s = frac * bw / max(img.size)
        return img.resize((max(1, int(img.width * s)), max(1, int(img.height * s))), Image.LANCZOS)

    # 角・耳・アンテナ（体の後ろ・左右対称）
    if detail:
        d = fit(load("detail_%s_%s.png" % (color, detail)), 0.52 if boss else 0.40)
        put(d, bx + bw * 0.17, by + bh * 0.03)
        put(d.transpose(Image.FLIP_LEFT_RIGHT), bx + bw * 0.83, by + bh * 0.03)

    # 脚
    lg = fit(load("leg_%s%s.png" % (color, legL)), 0.30)
    put(lg,                                     bx + bw * 0.32, by + bh + lg.height * 0.12)
    put(lg.transpose(Image.FLIP_LEFT_RIGHT),     bx + bw * 0.68, by + bh + lg.height * 0.12)

    # 腕（体に少し重ねて生やす）
    am = fit(load("arm_%s%s.png" % (color, armL)), 0.32)
    put(am.transpose(Image.FLIP_LEFT_RIGHT), bx + am.width * 0.22,        by + bh * 0.52)
    put(am,                                  bx + bw - am.width * 0.22,   by + bh * 0.52)

    canvas.alpha_composite(body, (bx, by))

    ey = load(eye + ".png"); s = 0.46 * bw / ey.width
    ey = ey.resize((max(1, int(ey.width * s)), max(1, int(ey.height * s))), Image.LANCZOS)
    put(ey, bx + bw / 2, by + bh * 0.32)

    mo = fit(load(mouth + ".png"), 0.26)
    put(mo, bx + bw / 2, by + bh * 0.62)

    canvas = canvas.crop(canvas.getbbox())
    target = 340 if boss else 280
    r = target / max(canvas.size)
    return canvas.resize((max(1, int(canvas.width * r)), max(1, int(canvas.height * r))), Image.LANCZOS)


def main():
    os.makedirs(OUT, exist_ok=True)
    imgs, total = [], 0
    for sp in SPECS:
        for ko in (False, True):
            im = compose(sp, ko)
            p = os.path.join(OUT, sp[0] + ("_ko" if ko else "") + ".png")
            im.save(p, optimize=True)
            total += os.path.getsize(p)
            if not ko:
                imgs.append(im)
    print("%d files, %.1f MB" % (len(SPECS) * 2, total / 1048576.0))

    cols, cell = 6, 200
    rows = (len(imgs) + cols - 1) // cols
    sheet = Image.new("RGBA", (cols * cell, rows * cell), (250, 246, 238, 255))
    for i, im in enumerate(imgs):
        t = im.copy(); t.thumbnail((cell - 16, cell - 16), Image.LANCZOS)
        sheet.alpha_composite(t, ((i % cols) * cell + (cell - t.width) // 2,
                                  (i // cols) * cell + (cell - t.height) // 2))
    sheet.save(SHEET)

    # たおれた顔の確認シート
    kos = [compose(sp, True) for sp in SPECS[:6]]
    ks = Image.new("RGBA", (6 * cell, cell), (250, 246, 238, 255))
    for i, im in enumerate(kos):
        t = im.copy(); t.thumbnail((cell - 16, cell - 16), Image.LANCZOS)
        ks.alpha_composite(t, (i * cell + (cell - t.width) // 2, (cell - t.height) // 2))
    ks.save("ko_sheet.png")
    print("sheets written")


main()
