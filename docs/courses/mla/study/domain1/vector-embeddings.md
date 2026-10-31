# 分野1: ベクトルストアと埋め込み

ベクトルストアを要件で選び、次元とコストを計算できるようにします。テキストの前処理も含みます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.1.7](../../domain1.md#skill-1-1-7) | ベクトルデータベースの設定 |
| [1.2.5](../../domain1.md#skill-1-2-5) | 埋め込みモデルの設定と利用 |
| [1.2.6](../../domain1.md#skill-1-2-6) | 高度なテキストの前処理 |

## 学習の順番 {#study-order}

1. [ベクトルストア](../../../../services/genai-apps.md#vector-stores): ストアごとの向いている場面を比べます。
2. [OpenSearch](../../../../services/genai-apps.md#opensearch-vectors)、[pgvector](../../../../services/genai-apps.md#pgvector)、[S3 Vectors](../../../../services/genai-apps.md#s3-vectors): 設定の値と制約を確認します。
3. [埋め込みの選び方](../../../../services/genai-apps.md#embedding-selection): 次元とコストの計算を押さえます。
4. [テキストの前処理](../../../../services/ai-fundamentals.md#text-preprocessing): TF-IDF やドメイン固有の拡張を覚えます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| Titan Text Embeddings V2 の次元 | 1,024（既定）、512、256 | インデックスと一致させる |
| V2 の入力の上限 | 8,192 トークン、50,000 文字 | チャンクを超えないように |
| 100 万チャンク、float32 | 1,024 次元で約 4.1 GB、256 次元で約 1.0 GB | 次元 × 4 バイト × 件数 |
| S3 Vectors の次元 | 1〜4,096 | ハイブリッド検索は不可 |
| pgvector の HNSW | 0.5.0 以上 | `ef_search` は精度と速度のトレードオフ |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| まず選ぶ、ハイブリッド検索が要る | OpenSearch Serverless |
| 既に PostgreSQL で、SQL と結合する | pgvector |
| 大量で低頻度、低コスト | S3 Vectors |
| 取り込みエラーで次元が合わない | インデックスの次元をモデルに合わせる |
| 埋め込みの API がスロットリングされる | SQS と Lambda で流量を制御、バッチ推論 |
| 専門用語が学習データに少ない | 同義語を足して拡張する |

## 引っかかりやすい点 {#traps}

- 埋め込みモデルを変えると、全データの再埋め込みが必要です。
- Knowledge Bases で OpenSearch のメタデータを使うなら、エンジンは `faiss` です。
- HNSW は速くて高精度ですが、メモリを使います。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [vector-embeddings 問1](../../exercises/vector-embeddings.md#q1) | 1.1.7 | 10 億件の古い文書を低コストで保存し、検索はまれです。ハイブリッド検索は不要で、1 秒未満の応答で… |
| [vector-embeddings 問2](../../exercises/vector-embeddings.md#q2) | 1.1.7 | Titan Text Embeddings V2 を既定のまま使い、OpenSearch のインデッ… |
| [vector-embeddings 問3](../../exercises/vector-embeddings.md#q3) | 1.1.7 | 既存の PostgreSQL の業務テーブルと結合して検索したいです。Aurora の pgvect… |
| [vector-embeddings 問4](../../exercises/vector-embeddings.md#q4) | 1.2.5 | テキストの FAQ を検索する RAG で、保存コストを抑えたいです。Titan Text Embe… |
| [vector-embeddings 問5](../../exercises/vector-embeddings.md#q5) | 1.2.5 | 100 万チャンクを float32 で保存します。次元を 1,024 から 256 に下げたとき、… |
| [vector-embeddings 問6](../../exercises/vector-embeddings.md#q6) | 1.2.5 | 数百万件の文書を初回に埋め込みます。API が RPM の制限でスロットリングされます。対応として適… |
| [vector-embeddings 問7](../../exercises/vector-embeddings.md#q7) | 1.2.6 | カスタマーの問い合わせ文から、話題の分類に使う特徴を作ります。よく出る語より、その文書に特有の語の重… |
| [vector-embeddings 問8](../../exercises/vector-embeddings.md#q8) | 1.2.6 | 医療の略語を含む問い合わせの分類モデルです。一般のモデルが略語を知らず、学習データも少ないです。ドメ… |
| [vector-embeddings 問9](../../exercises/vector-embeddings.md#q9) | 1.2.6 | 社内の専門用語を含む大量の文書から、単語の埋め込みを SageMaker AI で学習します。適切な… |

<!-- questions:end -->
