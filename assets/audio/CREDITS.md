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

## BGM

| ファイル | 用途 | 出典 |
|---|---|---|
| `battle_bgm.ogg` | ⚔️ もぐもぐクエスト の戦闘BGM（ループ前提のチップチューン） | "8 Bit Battle Loop" by **Wolfgang_** — https://opengameart.org/content/8-bit-battle-loop — CC0 1.0 |

## 候補（alt/）

`alt/` には各スロットの差し替え候補を入れてある（同じく Kenney・CC0）。
`hit_a/b`, `crit_a/b`, `defeat_a/b`, `ally_a/b`, `levelup_a/b`, `clear_a/b`, `appear_a/b`。

## 差し替え方

`sodateru-shokutaku-poc.html` の `SFX_FILES` / `BGM_FILES` テーブルでファイル名を差し替えるだけで音が変わる。
音源候補を聴き比べたい場合は `tools/audition.html` をローカルサーバー経由で開く。

## 注意

- **FreePD.com は閉鎖済み**（2026-07 確認）。BGMの追加取得は OpenGameArt の CC0 フィルタか Kenney を使うこと。
- 読み込みは HTTP 経由のみ（`file://` は fetch がブロックされる）。読み込めない場合は自動的に
  従来の WebAudio 合成音にフォールバックするので、オフラインでも無音にはならない。
