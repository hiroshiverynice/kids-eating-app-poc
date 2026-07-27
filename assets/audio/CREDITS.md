# 音素材のクレジットとライセンス

このフォルダの音はすべて **CC0 1.0 Universal（パブリックドメイン）** です。
CC0 は帰属表示（クレジット記載）が**不要**で、商用利用・改変・再配布が自由に行えます。
このファイルは記録のために残しているだけで、アプリ内にクレジット画面を置く義務はありません。

> 将来 CC-BY の素材を足す場合は義務が変わります。その時は親画面（👪）にクレジット欄を追加すること。

## 効果音

| ファイル | 用途 | 出典 | 元ファイル |
|---|---|---|---|
| `atk.ogg` | こうげき（剣の風切り） | Kenney "RPG Audio" | `knifeSlice.ogg` |
| `atk_crit.ogg` | かいしんの いちげき（振り） | Kenney "RPG Audio" | `knifeSlice2.ogg` |
| `hit.ogg` | 命中の打撃 | Kenney "Impact Sounds" | `impactGeneric_light_001.ogg` |
| `crit.ogg` | かいしんの 命中（重い一撃） | Kenney "Impact Sounds" | `impactMetal_heavy_000.ogg` |
| `boss.ogg` | ボス出現 | Kenney "Impact Sounds" | `impactBell_heavy_002.ogg` |
| `defeat.ogg` | てきを たおした | Kenney "Music Jingles" | `Pizzicato jingles/jingles_PIZZI05.ogg` |
| `ally.ogg` | なかまに なった | Kenney "Music Jingles" | `Pizzicato jingles/jingles_PIZZI02.ogg` |
| `levelup.ogg` | レベルアップ | Kenney "Music Jingles" | `8-Bit jingles/jingles_NES01.ogg` |
| `clear.ogg` | ぼうけん クリア | Kenney "Music Jingles" | `8-Bit jingles/jingles_NES00.ogg` |
| `appear.ogg` | てき出現 | Kenney "Interface Sounds" | `bong_001.ogg` |

出典: https://kenney.nl/assets/rpg-audio, /impact-sounds, /interface-sounds, /music-jingles
作者: Kenney Vleugels (Kenney.nl) — CC0 1.0

## BGM（ゲームごとに別の曲）

すべて OpenGameArt の **CC0** 曲。モノラル64kbpsの ogg に再エンコードして同梱している
（BGMは小音量で流すので十分。合計4MB程度に収まる）。

| ファイル | ゲーム | 曲・出典 |
|---|---|---|
| `battle_bgm.ogg` | ⚔️ もぐもぐクエスト | "8 Bit Battle Loop" by **Wolfgang_** — https://opengameart.org/content/8-bit-battle-loop |
| `fishing_bgm.ogg` | 🎣 ぬしつり | "Seaside Village" — https://opengameart.org/content/seaside-village |
| `sweets_bgm.ogg` | 🍰 スイーツデコ | "Happy Clappy Loop" — https://opengameart.org/content/happy-clappy-loop |
| `race_bgm.ogg` | 🏁 どうぶつレース | "As Fast As You Can" — https://opengameart.org/content/as-fast-as-you-can |
| `board_bgm.ogg` | 🗺️ たんけんマップ | "Chiptune Exploration" — https://opengameart.org/content/chiptune-exploration |
| `dig_bgm.ogg` | 🦖 かせきはっくつ | "Mysterious Cave Theme Loop" — https://opengameart.org/content/mysterious-cave-theme-loop |
| `rocket_bgm.ogg` | 🚀 うちゅうロケット | "Space Music Out There" — https://opengameart.org/content/space-music-out-there |
| `garden_bgm.ogg` | 🌷 おはなガーデン | "Flowerbed Fields Loop" — https://opengameart.org/content/flowerbed-fields-loop |

**BGMは選ばれたゲームの分だけ遅延で読み込む**（`loadBGM()`）。全部を起動時に読むと、
食卓のWi-Fiが弱いときに待たされるため。届くまでは従来の合成メロディが鳴り、
届いた時点で本物に切り替わる。

## 候補（alt/）

`alt/` には各スロットの差し替え候補を入れてある（同じく Kenney・CC0）。
`hit_a/b`, `crit_a/b`, `defeat_a/b`, `ally_a/b`, `levelup_a/b`, `clear_a/b`, `appear_a/b`。

## 差し替え方

`sodateru-shokutaku-poc.html` の `SFX_FILES` / `BGM_FILES` テーブルでファイル名を差し替えるだけで音が変わる。
音源候補を聴き比べたい場合は `tools/audition.html` をローカルサーバー経由で開く。

## 注意

- **FreePD.com は閉鎖済み**（2026-07 確認）。BGMの追加取得は OpenGameArt の CC0 フィルタか Kenney を使うこと。
  検索URLの例（音楽×CC0で絞り込み）:
  `https://opengameart.org/art-search-advanced?keys=<キーワード>&field_art_type_tid[]=12&field_art_licenses_tid[]=4`
  取得スクリプトの原型は `tools/` には置いていない（一時作業）。ライセンスは必ず各ページ本文で CC0 を確認すること。
- 形式は **Ogg Vorbis**。Safari は 17 以降で対応（それ以前の端末では合成音にフォールバックする）。
- 読み込みは HTTP 経由のみ（`file://` は fetch がブロックされる）。読み込めない場合は自動的に
  従来の WebAudio 合成音にフォールバックするので、オフラインでも無音にはならない。
