# Key画像シリーズ 検索ガイド

放射線科・画像診断の医学書18冊のページ別テキストインデックスです。

## 検索方法

疾患名や所見を質問すると、どの書籍の何ページに記載があるかを答えます。

**例:**
- 「気胸はどこに載っていますか？」
- 「肺癌の画像所見を調べたい」
- 「骨軟部腫瘍について」

## インデックスファイルの場所

`index/` フォルダに書籍ごとのJSONファイルがあります。

| ファイル | 書籍名 | 分野 |
|---------|--------|------|
| index/胸部Key.json | 胸部Key | 胸部 |
| index/胸部勘ドコロNEO.json | 胸部勘ドコロNEO | 胸部 |
| index/心臓血管Key.json | 心臓血管Key | 心臓・血管 |
| index/脳MRI Key.json | 脳MRI Key | 頭部 |
| index/脳MRI正常解剖.json | 脳MRI正常解剖 | 頭部 |
| index/頭部勘ドコロ.json | 頭部勘ドコロ | 頭部 |
| index/頭頸部Key.json | 頭頸部Key | 頭頸部 |
| index/歯科Key.json | 歯科Key | 頭頸部 |
| index/消化管Key.json | 消化管Key | 腹部 |
| index/肝胆膵Key.json | 肝胆膵Key | 腹部 |
| index/泌尿器Key.json | 泌尿器Key | 腹部 |
| index/脊椎脊髄疾患.json | 脊椎脊髄疾患 | 脊椎 |
| index/骨軟部Key.json | 骨軟部Key | 骨軟部 |
| index/骨軟部勘ドコロ.json | 骨軟部勘ドコロ | 骨軟部 |
| index/乳房Key.json | 乳房Key | 乳腺 |
| index/産婦人科Key.json | 産婦人科Key | 産婦人科 |
| index/小児Key.json | 小児Key | 小児 |
| index/救急Key.json | 救急Key | 救急 |

## JSONフォーマット

```json
{
  "book": "胸部Key",
  "pages": [
    {"p": 1, "t": "ページのテキスト（200文字）"},
    ...
  ]
}
```

## 検索の進め方

1. 疾患が関係する分野の書籍ファイルを読む
2. テキスト中に疾患名が含まれるページ番号を返す
3. 複数の書籍にまたがる場合はすべて列挙する
