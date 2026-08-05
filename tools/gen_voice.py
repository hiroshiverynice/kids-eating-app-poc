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
  漏れは tests の「speak に渡る文言がすべて manifest にあるか」で検出できる。
"""
import json, pathlib, subprocess, sys, io, urllib.request, urllib.parse, tempfile, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
API = "http://127.0.0.1:50021"
SPEAKER = 1          # ずんだもん / あまあま
INTONATION = 1.25    # 掛け声なので抑揚は強め
SPEED = 0.97         # 幼児向けに気持ちゆっくり
BITRATE = "40k"      # 声だけなので40kで十分。本数が多いので容量を優先

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "voice"

# ───────── アプリ側の名前リスト（sodateru-shokutaku-poc.html と同期させること）─────────
BTL_MONS = ["ぷにモン","あわボール","けろまる","はりまる","もふりん","ぴこモン","つのすけ","ごまちゃん",
            "ほしまる","ぷるるん","もこモン","とびまる","にょろん","ころすけ","しろたん","かげまる"]
BTL_BOSSES = ["りゅうおう","キングもふ","やみのおう","うみのぬし","もりのぬし","ゆきのおう"]
SPA_ANIMALS = ["ぞうさん","きりんさん","かばさん","おさるさん","パンダさん",
               "オウムさん","ペンギンさん","ぶたさん","うさぎさん","へびさん"]
SWEET_TOPS = ["いちご","ブルーベリー","さくらんぼ","チョコ","キウイ","もも","おほし","ハート",
              "おはな","キャンディ","カップケーキ","ペロペロ","みかん","ココナッツ"]
SWEET_RARE = ["おうかん","ダイヤ","にじ","ユニコーン"]
DINOS = ["ティラノ","トリケラ","ブラキオ","スピノ","ステゴ","モササウルス","マンモス","ドラゴン","メガロドン"]
GFLOWERS = ["チューリップ","ひまわり","さくら","ハイビスカス","マーガレット","はす","バラ","うめ"]
GBUGS = ["チョウチョ","はち","てんとうむし","いもむし"]
GROW_FOODS = ["ごはん","にんじん","トマト","ブロッコリー","おさかな","おにく","たまご","おいも",
              "とうもろこし","はっぱ","きのこ","まめ","じゃがいも","パン"]
RIDES = ["バス","じどうしゃ","タクシー","トラック","おおがたトラック","ワゴン",
         "ピックアップ","トラクター","じてんしゃ","バイク","ジープ","オートさんりん"]
RIDES_RARE = ["しょうぼうしゃ","きゅうきゅうしゃ","パトカー","きかんしゃ","ヘリコプター","ロケット"]
DRESS_SLOTS = [
    ("ぼうし",   ["むぎわらぼうし","シルクハット","キャップ","おうかん","リボン"]),
    ("トップス", ["Tシャツ","ブラウス","コート","はおりもの","ベスト"]),
    ("ボトム",   ["ジーンズ","ショートパンツ","ワンピース","ロングスカート","レオタード"]),
    ("くつ",     ["スニーカー","ハイヒール","ブーツ","バレエシューズ","フラットシューズ"]),
    ("アクセ",   ["ゆびわ","ネックレス","サングラス","うでどけい","マフラー"]),
    ("バッグ",   ["ハンドバッグ","リュック","ポーチ","ショッパー","かご"]),
]
DRESS_RARE = ["きらきら","にじいろ","ダイヤ","ユニコーン","スター"]   # 装飾。say には出ない
DRESS_NAMES = ["おでかけ","おひめさま","げんき","ゆめかわ","おしゃれ",
               "スポーツ","おさんぽ","パーティ","カフェ","たびだち"]
BAND_MEMBERS = ["ドラム","ギター","ピアノ","バイオリン","トランペット","サックス",
                "アコーディオン","バンジョー","たいこ","ベル","ボーカル","しきしゃ"]

# ───────── 文言 ─────────
LINES = []          # (画面/コード上の文言, 読ませる文) のリスト
def add(*xs):
    for x in xs:
        if not any(k == x for k, _ in LINES):
            LINES.append((x, x))
def add_sp(key, speech):
    """キーと読ませる文が違うもの（絵文字を読ませたくない等）"""
    if not any(k == key for k, _ in LINES):
        LINES.append((key, speech))

# 共通の掛け声（CHEERS）
add("たべたね！","えらいね！","じょうずー！","もぐもぐ！","やったね！","おいしい！","ナイス！")
# 直接 speak() しているもの
add("レベルアップ！","ボスが あらわれた！","やさしさ アップ！")
# 食事のおわり（praise）
add("しんきろく！すごい！","ごちそうさま！")
# ③ チャレンジ（食べものの名前は画面に出るので 音声では省く）
add("チャレンジ できたね！","3かい ためせたね！ すごい！")
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
for n in BTL_MONS + BTL_BOSSES:
    add(n + " が なかまに なった！")
    add(n + " と なかよし に なった！")
    add(n + " と しんゆう に なった！")
# 🌸 げんきに なあれ
add("とびきり げんきに なあれ！","げんきに なあれ","もぐもぐ おすそわけ","いいこ いいこ",
    "あとすこし！","にこにこ","元気 わけてあげる")
for n in SPA_ANIMALS: add(n + " が げんきに なった！")
# 🛁 どうぶつスパ
add("あわあわ もこもこ！","ごしごし！","きもちいい〜","あわあわ！","きれいに なあれ")
for n in SPA_ANIMALS: add(n + " ピカピカ！")
# 🌱 モグをそだてよう
add("ぐんぐん そだつ！","はなが さいたよ！","うまれた！","おおきく なった！","つぼみに なった！")
for n in GROW_FOODS: add(n + " もぐもぐ！")
# 🏁 どうぶつレース
add("おいぬいた！","ダッシュ！","はやい！","がんばれ！","いいぞー！","びゅーん！")
# 🚀 うちゅうロケット
add("わくせい とうちゃく！","ブースト！","スターゲット！","ぐんぐん！")
# 🦖 かせきはっくつ
add("たからも！","コツッ！")
for n in DINOS: add(n + " はっけん！")
# 🌷 おはなガーデン
for n in GFLOWERS: add(n + " さいた！")
for n in GBUGS + ["にじのチョウ"]: add(n + " が きた！")   # にじのチョウは配列でなくインライン定義
# 🍰 スイーツデコ
add("ケーキ かんせい！")
for n in SWEET_TOPS + SWEET_RARE: add(n + "！")
# 🚌 のりものパレード
for n in RIDES: add(n + " が きたよ！")
for n in RIDES_RARE: add(n + " だ！ すごい！")
# 👗 きせかえコレクション
for label, items in DRESS_SLOTS:
    for it in items:
        add(label + " は " + it + "！")
        add("きらきらの " + it + "！")      # レア時は スロット名でなく「きらきらの」が付く
for n in DRESS_NAMES:
    add(n + "コーデ かんせい！")
    add(n + " キラキラコーデ かんせい！")
# 🎼 おんがくたい
add("がくだん かんせい！")
for n in BAND_MEMBERS: add(n + " が なかまに なったよ！")
# 🎣 ぬしつり（tier のラベル。絵文字は読ませない）
add("つれた！","いいサイズ！","おおもの！","ぬしだ！！")
add("ぬしを つったよ！","バケツ いっぱい！")     # finale は ぬしが釣れたかで変わる
add_sp("レア！ ✨", "レア！")
# 🗺️ たんけんマップ
add("ワープ！","たからだ！","なかまが きた！")
for i in range(1, 7): add("サイコロ " + str(i) + "！")


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
    for old in OUT.glob("*.ogg"):
        old.unlink()

    manifest, total = {}, 0
    tmpdir = tempfile.mkdtemp()
    for i, (key, speech) in enumerate(LINES, 1):
        name = "v%03d.ogg" % i
        q = json.loads(post("/audio_query", {"speaker": SPEAKER, "text": speech}))
        q["intonationScale"] = INTONATION
        q["speedScale"] = SPEED
        wav = post("/synthesis", {"speaker": SPEAKER}, q)
        wpath = os.path.join(tmpdir, "t.wav")
        with open(wpath, "wb") as f:
            f.write(wav)
        r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wpath,
                            "-ac", "1", "-c:a", "libvorbis", "-b:a", BITRATE, str(OUT / name)],
                           capture_output=True)
        if r.returncode != 0:
            sys.exit("ffmpeg 失敗: %s\n%s" % (speech, r.stderr.decode("utf-8", "replace")))
        manifest[key] = name
        total += (OUT / name).stat().st_size
        if i % 40 == 0:
            print("  %d / %d ..." % (i, len(LINES)))

    (OUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=0), encoding="utf-8")
    print("生成: %d本 / 合計 %.2f MB" % (len(LINES), total / 1024 / 1024))
    print("出力: %s" % OUT)


if __name__ == "__main__":
    main()
