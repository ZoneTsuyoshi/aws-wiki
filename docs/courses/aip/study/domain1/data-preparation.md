# 分野1: データの検証と前処理

FM に渡す前に品質を止め、複雑なデータを扱える形にします。データエンジニアリングそのものではなく、品質ゲートの置き方が焦点です。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.3.1](../../domain1.md#skill-1-3-1) | データ検証のワークフロー |
| [1.3.2](../../domain1.md#skill-1-3-2) | 複雑なデータ型の処理 |
| [1.3.3](../../domain1.md#skill-1-3-3) | モデルが要求する形式に整える |
| [1.3.4](../../domain1.md#skill-1-3-4) | 入力の質を高める |

## 学習の順番 {#study-order}

1. [Glue Data Quality](../../../../services/data-engineering.md#glue-data-quality)と [Data Wrangler](../../../../services/sagemaker.md#data-wrangler): 宣言的なルールと画面での試行の違いを押さえます。
2. [Textract](../../../../services/ai-managed-services.md#textract)、[Transcribe](../../../../services/ai-managed-services.md#transcribe)、[Bedrock Data Automation](../../../../services/genai-apps.md#bda): データの種類ごとの処理を選べるようにします。
3. [API の選び方](../../../../services/ai.md#invoke-apis)と[バッチの設定](../../../../services/ai.md#throughput-options): モデルが要求する形式を確認します。
4. [Comprehend](../../../../services/ai-managed-services.md#comprehend): 抽出の機能と、PII の対応言語を覚えます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| バッチ推論の入力 | S3 の JSONL。`recordId` と `modelInput` | 出力の順序は同じとは限らない |
| Comprehend の PII 検出 | 英語、スペイン語 | 日本語には別の手段 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 宣言的なルールでデータを検査する | Glue Data Quality |
| 独自の形式を 1 件ずつ同期で検査する | Lambda |
| 定型の帳票を大量に決定的に抽出する | Textract |
| 図の意味の解釈が要る | マルチモーダルの FM |
| 文書、画像、音声、動画を一括で構造化する | Bedrock Data Automation |
| 任意のコンテナで大規模に変換する | SageMaker Processing |
| 日付や単位を規則で揃える | Lambda の正規化 |

## 引っかかりやすい点 {#traps}

- `InvokeModel` の本文はモデルごとに違います。`Converse` なら共通です。
- モデルは前回の内容を覚えていないので、履歴はアプリが渡します。
- `ValidationException` は再試行しても成功しません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [data-preparation 問1](../../exercises/data-preparation.md#q1) | 1.3.1 | Data Catalog に登録した顧客の問い合わせ履歴を、毎週 FM の要約に使います。必須列の欠… |
| [data-preparation 問2](../../exercises/data-preparation.md#q2) | 1.3.1 | API で届く文書を 1 件ずつ FM に渡す前に検査します。要件は、文字数が上限以内であること、社… |
| [data-preparation 問3](../../exercises/data-preparation.md#q3) | 1.3.1 | データサイエンティストが、埋め込みに渡す前のデータの傾向を調べ、前処理の案を画面で試したいと考えてい… |
| [data-preparation 問4](../../exercises/data-preparation.md#q4) | 1.3.2 | ある保険会社は、形式の決まった請求書を毎日 10 万枚処理します。抽出する項目は決まっており、結果は… |
| [data-preparation 問5](../../exercises/data-preparation.md#q5) | 1.3.2 | コールセンターの録音を FM で要約します。誰の発言かを区別する必要があり、自社の製品名が誤認識され… |
| [data-preparation 問6](../../exercises/data-preparation.md#q6) | 1.3.2 | 独自形式の測定データと文書を、社内のライブラリで変換してから FM に渡します。データは数 TB で… |
| [data-preparation 問7](../../exercises/data-preparation.md#q7) | 1.3.3 | あるアプリは InvokeModel で提供者 A のモデルを呼んでいます。本文に別の提供者の形式の… |
| [data-preparation 問8](../../exercises/data-preparation.md#q8) | 1.3.3 | 10 万件の要約をバッチ推論で実行します。ジョブが入力の形式の検証で失敗しました。入力の用意の仕方と… |
| [data-preparation 問9](../../exercises/data-preparation.md#q9) | 1.3.3 | チャットの 2 回目の質問で、モデルが前の質問の内容を覚えていないと報告されました。アプリは毎回、最… |
| [data-preparation 問10](../../exercises/data-preparation.md#q10) | 1.3.4 | 英語の技術レポートが大量にあり、取り込みのときに製品名や組織名をメタデータとして付け、検索の絞り込み… |
| [data-preparation 問11](../../exercises/data-preparation.md#q11) | 1.3.4 | 利用者の質問は口語で崩れており、誤字も多く、検索と回答の品質を下げています。質問は日本語です。遅延が… |
| [data-preparation 問12](../../exercises/data-preparation.md#q12) | 1.3.4 | 全社の文書で日付は「2026/4/1」「令和8年4月1日」、金額は全角と半角が混在し、検索の絞り込み… |
| [data-preparation 問13](../../exercises/data-preparation.md#q13) | 1.3.2, 1.3.3 | 数百ページの PDF の帳票から項目を抽出し、夜間にまとめて FM で要約します。担当者は同期の A… |

<!-- questions:end -->
