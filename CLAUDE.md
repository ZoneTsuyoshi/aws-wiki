# AWS Wiki

AWS の構成や運用をまとめる wiki。`docs/` の md を MkDocs Material でサイト化し、GitHub Actions から Cloudflare Pages に公開する。

## ページを書くときのルール

- 本文は日本語で、スマホでも読みやすいよう短い段落で書く。
- 新しいページは `mkdocs.yml` の `nav` と `docs/index.md` に追加する。
- AWS の構成が出てきたら diagrams で構成図を作る。手順は `docs/setup/diagrams.md` を参照する。
- 処理の流れ、シーケンス、権限の関係が出てきたら Mermaid 図を入れる。
- 比較は表にする。
- 図の中身は要点に絞る。1枚あたりノード10個程度を目安にし、多ければ図を分ける。
- Mermaid はスマホで拡大できないので、シーケンス図の参加者は4つまでにする。フローチャートは項目が多ければ `flowchart TD` にする。

## 実環境の情報

実環境の構成図は、Terraform や CloudFormation のコード、またはユーザーが示した情報をもとに作る。書かれていないリソースを推測で足さない。

リポジトリとサイトは公開される可能性があるので、次の情報は md にも図にも書かない。

- AWS アカウント ID、ARN、IP アドレス、内部ドメイン名
- 認証情報、トークン、シークレット

## 確認コマンド

ローカルの Graphviz には頼らず、Docker で実行する。

```bash
docker run --rm -v "$PWD":/w -w /w python:3.13-slim bash -c '
  apt-get update -qq && apt-get install -y -qq graphviz fonts-noto-cjk &&
  pip install -q --root-user-action=ignore -r requirements.txt &&
  for f in diagrams_src/*.py; do python "$f"; done &&
  mkdocs build --strict'
```
