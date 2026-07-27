# 画像素材のクレジットとライセンス

すべて **CC0 1.0 Universal**（パブリックドメイン／帰属表示不要・商用利用可・改変自由）。
このファイルは記録用で、アプリ内にクレジット画面を置く義務はない。

## 情景（`scenery/`）

各ゲームの背景に置く飾り。雲・木・城・柵・草・月と、うちゅうの星・隕石。

| ファイル | 出典 |
|---|---|
| `cloud*.png` `tree*.png` `castle_grey.png` `tower_grey.png` `house_beige_front.png` `fence.png` `grass*.png` `moon_full.png` | Kenney "Background Elements" — https://kenney.nl/assets/background-elements |
| `star_*.png` `meteor_detailedLarge.png` | Kenney "Simple Space" — https://kenney.nl/assets/simple-space |

使いどころ:

- ⚔️ バトル … 月＋丘の向こうの木と城（暗く落として夜のシルエットにしている）
- 🏁 レース … 空の雲＋地平線の木と柵
- 🗺️ たんけんマップ … 島の雲と木＋ゴールの城（絵文字🏰から差し替え）
- 🌷 おはなガーデン … 雲・奥の木・足元の草
- 🚀 うちゅうロケット … 星と隕石

表示サイズに合わせて最大220pxへ縮小済み（元素材はもっと大きい）。

## 惑星（`planets/`）

🚀 うちゅうロケット の到達目標と、集めた惑星コレクション。絵文字🌕🪐から差し替え。

出典: Kenney "Planets" — https://kenney.nl/assets/planets （CC0）
元は1280px・1枚280KBあるので、**160pxへ縮小して同梱している**（2.8MB → 310KB）。

## モンスター（`monsters/`）

⚔️ もぐもぐクエスト のモンスター22体（＋たおれた顔22枚 = 計44ファイル）。

**出典**: Kenney "Monster Builder Pack" — https://kenney.nl/assets/monster-builder-pack
**作者**: Kenney Vleugels (Kenney.nl)
**ライセンス**: CC0 1.0 Universal（パブリックドメイン／帰属表示不要・商用利用可・改変自由）

元パックは「体・目・口・腕・脚・角」のパーツ集で、完成したモンスター画像は入っていない。
本プロジェクトでは `tools/compose_monsters.py` でパーツを合成して22体を作っている。
スクリプトは指定を全部べた書きしているので、**実行すれば毎回まったく同じ絵が再生成される**。

```
python tools/compose_monsters.py     # cc0/monster-builder-pack/ を隣に置いて実行
```

### 命名

| ファイル | 内容 |
|---|---|
| `puni.png` 〜 `kage.png` | 通常モンスター16体 |
| `boss_*.png` | ボス6体（大きめ・大きな角） |
| `*_ko.png` | たおれた顔（目をまわしている状態）。各体1枚 |

### 絵づくりのガードレール

リサーチ由来の「こわい／痛そうな演出を作らない」を素材選定の段階で担保している。

- **使わないパーツ**: `eye_angry_*`（おこり顔）、`eye_psycho_*`（こわい目）、
  `mouthD` / `mouth_closed_fangs` / `mouth_closed_sad`（への字＝悲しい顔）
- **×目（`eye_dead`）は健康なモンスターに絶対に付けない。** たおれた瞬間の `_ko.png` だけに使う。
  たおれても口は笑ったままにして「気絶＝目をまわしている」と読ませ、そのまま仲間になる流れにしている
- ボスは「角を大きく・体を大きく」で強さを表現する。こわい顔では表現しない

### 差し替え・追加

`tools/compose_monsters.py` の `SPECS` に1行足すだけで新しいモンスターが増える。
体の色は blue / green / red / yellow / white / dark、体型は A〜F。
アプリ側は `sodateru-shokutaku-poc.html` の `BTL_MONS` / `BTL_BOSSES` に
`[id, 表示名, 画像が出ない時の絵文字]` を追加する。

画像が読み込めない環境では `onerror` で絵文字にフォールバックするので、表示が消えることはない。
