# 構成図の作り方

AWS アイコンを使う構成図は Python の [diagrams](https://diagrams.mingrammer.com/) で、処理の流れなどの説明図は Mermaid で書きます。

| 描きたいもの | 使うもの | 置き場所 |
|---|---|---|
| AWS の構成図 | diagrams | `diagrams_src/*.py` |
| 処理の流れ、シーケンス、権限の関係 | Mermaid | md に直接書く |
| 項目の比較 | 表 | md に直接書く |

## 構成図を追加する

1. `diagrams_src/` に Python ファイルを追加します。[web_app.py](https://github.com/ZoneTsuyoshi/aws-wiki/blob/main/diagrams_src/web_app.py) をひな形にしてください。
2. 出力先は `filename="docs/assets/diagrams/<図の名前>"` とします。
3. md から画像を参照します。画像をリンクにしておくと、スマホでタップして拡大できます。

```markdown
[![Webアプリ構成](../assets/diagrams/web-app.png)](../assets/diagrams/web-app.png)
```

## プレビューする

Docker を起動した状態でリポジトリのルートで実行し、`http://127.0.0.1:8000` を開きます。Graphviz と日本語フォントは CI と同じものがコンテナに入ります。

```bash
docker run --rm -p 8000:8000 -v "$PWD":/w -w /w python:3.13-slim bash -c '
  apt-get update -qq && apt-get install -y -qq graphviz fonts-noto-cjk &&
  pip install -q --root-user-action=ignore -r requirements.txt &&
  for f in diagrams_src/*.py; do python "$f"; done &&
  mkdocs serve -a 0.0.0.0:8000'
```

md の変更は自動で反映されます。図のコードを変えたときは、止めて実行し直します。

生成した PNG は Git に入れません。CI が毎回作り直します。

!!! note "`brew install graphviz` について"
    古い macOS ではビルド済みパッケージが使えず、依存パッケージをソースからビルドするため、時間がかかったり失敗したりします。macOS 14.1 と Command Line Tools 15.3 の環境では、`python@3.15` のビルドで失敗しました。そのためローカルでは Docker を使います。

## 決めごと

- **出力は PNG にします。** diagrams の SVG はアイコンをローカルのファイルパスで参照するため、そのまま公開するとアイコンが表示されません。
- **ディレクトリ名は `diagrams_src` にします。** `diagrams` にすると、Python パッケージの `diagrams` と名前が衝突することがあります。
- **ノードは要点だけに絞ります。** スマホで読めるよう、1枚あたり10個程度を目安にして、多くなる場合は図を分けます。
- **Mermaid は横幅を抑えます。** タップで拡大できないので、シーケンス図の参加者は4つまでにし、フローチャートは項目が多ければ縦向き（`flowchart TD`）にします。
