# -*- coding: utf-8 -*-
"""掛け声を VOICEVOX（ずんだもん／あまあま）で事前生成して assets/voice/ に置く。

なぜ事前生成か:
  端末の合成音声(speechSynthesis)は抑揚が乏しく、端末によって声も変わる。
  クラウドTTSは通信が要る＝食卓のWi-Fiが弱いと鳴らない（CDN起因の起動不能を実際に踏んだ）。
  固定の掛け声なら事前に作って同梱できる。費用ゼロ・オフライン・端末差なし。

使い方:
  1. VOICEVOX を起動（またはエンジンだけ: vv-engine/run.exe）
  2. python tools/gen_voice.py
  3. assets/voice/*.ogg と manifest.json が出来る

※ 文言はアプリ側のコードと手で同期させること。
  ここに無い文言は、アプリ側で従来どおり端末の合成音声にフォールバックする。
"""
import json, pathlib, subprocess, sys, io, urllib.request, urllib.parse, tempfile, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
API = "http://127.0.0.1:50021"
SPEAKER = 1          # ずんだもん / あまあま
INTONATION = 1.25    # 掛け声なので抑揚は強め
SPEED = 0.97         # 幼児向けに気持ちゆっくり

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "voice"

BTL_MONS = ["ぷにモン","あわボール","けろまる","はりまる","もふりん","ぴこモン","つのすけ","ごまちゃん",
            "ほしまる","ぷるるん","もこモン","とびまる","にょろん","ころすけ","しろたん","かげまる"]
BTL_BOSSES = ["りゅうおう","キングもふ","やみのおう","うみのぬし","もりのぬし","ゆきのおう"]
SPA_ANIMALS = ["ぞうさん","きりんさん","かばさん","おさるさん","パンダさん",
               "オウムさん","ペンギンさん","ぶたさん","うさぎさん","へびさん"]

LINES = []
def add(*xs):
    for x in xs:
        if x not in LINES: LINES.append(x)

# 共通の掛け声（CHEERS）
add("たべたね！","えらいね！","じょうずー！","もぐもぐ！","やったね！","おいしい！","ナイス！")
# 直接 speak() しているもの
add("レベルアップ！","ボスが あらわれた！","やさしさ アップ！")
# 完結（finale の title）
add("ぼうけん クリア！","もりが げんきに なった！","はなが さいた！","スパ おしまい！",
    "パレード かんせい！","コーデ かんせい！","えんそう かんせい！","おしろに ついた！",
    "きょうりゅう はくぶつかん！","うちゅう たんけん かんりょう！","ガーデンパーティ！",
    "ゴール！ 1ちゃく！","スイーツやさん かんせい！")
# あそびを えらんだとき（ゲーム名）
add("もぐもぐクエスト","げんきに なあれ","モグをそだてよう","どうぶつスパ","のりものパレード",
    "きせかえコレクション","おんがくたい","ぬしつり","スイーツデコ","どうぶつレース",
    "たんけんマップ","かせきはっくつ","うちゅうロケット","おはなガーデン")
# ⚔️ もぐもぐクエスト
add("かいしんの いちげきー！","それっ！","えいっ！","たあっ！","いくぞー！","つよい！","もういっぱつ！")
for n in BTL_MONS + BTL_BOSSES: add(n + " が なかまに なった！")
# 🌸 げんきに なあれ
add("とびきり げんきに なあれ！","げんきに なあれ","もぐもぐ おすそわけ","いいこ いいこ",
    "あとすこし！","にこにこ","元気 わけてあげる")
for n in SPA_ANIMALS: add(n + " が げんきに なった！")
# その他のあそびの固定の掛け声
add("おいぬいた！","ダッシュ！","はやい！","がんばれ！","いいぞー！","びゅーん！")          # レース
add("わくせい とうちゃく！","ブースト！","スターゲット！","ぐんぐん！")                     # ロケット
add("たからも！","コツッ！")                                                              # はっくつ
add("あわあわ もこもこ！","ごしごし！","きもちいい〜","あわあわ！","きれいに なあれ")        # スパ
for n in SPA_ANIMALS: add(n + " ピカピカ！")
add("ぐんぐん そだつ！","はなが さいたよ！","うまれた！","おおきく なった！","つぼみに なった！")  # そだてる
add("ケーキ かんせい！","がくだん かんせい！")


def post(path, params, body=None):
    url = API + path + "?" + urllib.parse.urlencode(params)
    data = json.dumps(body).encode("utf-8") if body is not None else b""
    req = urllib.request.Request(url, data=data, method="POST",
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def main():
    try:
        urllib.request.urlopen(API + "/version", timeout=5)
    except Exception:
        sys.exit("VOICEVOX エンジンが起動していません（%s）。VOICEVOX を起動してから実行してください。" % API)

    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.ogg"): old.unlink()

    manifest, total = {}, 0
    tmpdir = tempfile.mkdtemp()
    for i, text in enumerate(LINES, 1):
        name = "v%03d.ogg" % i
        q = json.loads(post("/audio_query", {"speaker": SPEAKER, "text": text}))
        q["intonationScale"] = INTONATION
        q["speedScale"] = SPEED
        wav = post("/synthesis", {"speaker": SPEAKER}, q)
        wpath = os.path.join(tmpdir, "t.wav")
        with open(wpath, "wb") as f:
            f.write(wav)
        # モノラル 64kbps ogg（掛け声は短いので1本10KB前後に収まる）
        r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wpath,
                            "-ac", "1", "-c:a", "libvorbis", "-b:a", "64k", str(OUT / name)],
                           capture_output=True)
        if r.returncode != 0:
            sys.exit("ffmpeg 失敗: %s\n%s" % (text, r.stderr.decode("utf-8", "replace")))
        manifest[text] = name
        total += (OUT / name).stat().st_size
        if i % 20 == 0:
            print("  %d / %d ..." % (i, len(LINES)))

    (OUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=0), encoding="utf-8")
    print("生成: %d本 / 合計 %.2f MB" % (len(LINES), total / 1024 / 1024))
    print("出力: %s" % OUT)


if __name__ == "__main__":
    main()
