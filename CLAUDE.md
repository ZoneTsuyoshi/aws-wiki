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

## ディレクトリの役割

- `docs/services/`: サービスごとの解説。試験に依存しない内容を書き、複数のコースから参照する。
- `docs/courses/<試験>/`: 試験別コース。公式のスキルごとに要点を書き、詳細は `docs/services/` にリンクする。
- `docs/qa/index.md`: ユーザーの技術的な質問の一覧。

新しい試験のコースを作るときは、`docs/courses/dva/` と同じ構成にし、公式スキルとページの対応表（`coverage.md`）も作る。

`docs/services/` では、設定項目ごとに「何が変わるか、既定値と範囲、具体的な値を使った例、設定を誤ったときの症状」を書く。

問題集は `docs/courses/<試験>/exercises/` に置き、形式を `scripts/check_exercises.py` で検査する。問題はオリジナルで書き、正解は公式ドキュメントで確認する。過去問やダンプは使わない。各スキルに最低3問そろえる。

`docs/courses/<試験>/study/domainN/` は分野とサービスの組み合わせごとの学習ページで、事実は `docs/services/` の内容に合わせる。問題の一覧は手で書かず、問題を追加したら `python3 scripts/build_study_pages.py` を実行して更新する。

## 技術的な質問への対応

ユーザーから技術的な質問を受けたら、回答するだけでなく wiki に追記する。

1. 内容に合う `docs/services/` のページに追記する。合うページがなければ新しく作る。
2. `docs/qa/index.md` に、質問の要約と追記先へのリンクを1行で追加する。
3. ビルドを確認して commit し、`main` に push してサイトに反映する。

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
