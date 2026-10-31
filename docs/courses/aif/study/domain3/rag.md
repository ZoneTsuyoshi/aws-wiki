# 分野3: RAG とベクトルストア

RAG の流れと、埋め込みの保存先の選び方を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.1.3](../../domain3.md#obj-3-1-3) | RAG と業務での使い方 |
| [3.1.4](../../domain3.md#obj-3-1-4) | ベクトルデータベースに埋め込みを保存するサービス |

## 学習の順番 {#study-order}

1. [RAG](../../../../services/ai-fundamentals.md#rag): 質問から回答までの流れを図で理解します。
2. [取り込みの流れ](../../../../services/genai-apps.md#kb-ingestion)と[Managed と Customer-managed](../../../../services/genai-apps.md#managed-kb): 取り込みの順番と、公式が推奨する Managed Knowledge Base を確認します。
3. [ベクトルストア](../../../../services/genai-apps.md#vector-stores): ストアごとの向いている場面を覚えます。
4. [pgvector](../../../../services/genai-apps.md#pgvector)と[S3 Vectors](../../../../services/genai-apps.md#s3-vectors): 既存の PostgreSQL の活用と、大量で低頻度の場合を押さえます。
5. [モデルを業務に合わせる方法](../../../../services/ai-fundamentals.md#customization-options): RAG とファインチューニングの選び方を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 情報が頻繁に変わる、引用が必要 | RAG |
| 独特の文体で書かせる | ファインチューニング |
| 既に Aurora PostgreSQL を使っている | pgvector |
| 全文検索とベクトル検索を併用する | OpenSearch Service |
| 関係をたどる質問 | Neptune Analytics |
| 大量でアクセスが少ない | S3 Vectors |
| RAG をマネージドで作る | Bedrock Knowledge Bases |

## 引っかかりやすい点 {#traps}

- RAG はモデルの重みを変えません。
- 埋め込みの作成はチャンク化の後です。
- DocumentDB と S3 Vectors はガイドの例にありませんが、候補になります。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [rag 問1](../../exercises/rag.md#q1) | 3.1.3 | RAG の説明として正しいものはどれですか。 |
| [rag 問2](../../exercises/rag.md#q2) | 3.1.3 | RAG の事前準備の順番として正しいものはどれですか。 |
| [rag 問3](../../exercises/rag.md#q3) | 3.1.3 | 人事の規定が毎月更新されます。社員の質問に最新の規定で答え、根拠も示したいと考えています。適切な方法… |
| [rag 問4](../../exercises/rag.md#q4) | 3.1.3 | RAG の仕組みをマネージドで提供し、回答に引用も含められる AWS の機能はどれですか。 |
| [rag 問5](../../exercises/rag.md#q5) | 3.1.3 | RAG が業務に合う場面として適切なものを選んでください。（2つ選択） |
| [rag 問6](../../exercises/rag.md#q6) | 3.1.4 | 既に Aurora PostgreSQL で商品データを管理しています。新たなデータベースを増やさず… |
| [rag 問7](../../exercises/rag.md#q7) | 3.1.4 | キーワードの全文検索と k-NN のベクトル検索を組み合わせて、高い検索品質を得たいと考えています。… |
| [rag 問8](../../exercises/rag.md#q8) | 3.1.4 | 「この部品を使う製品の取引先はどこか」のように、関係をたどる質問が中心です。適切なベクトルストアはど… |
| [rag 問9](../../exercises/rag.md#q9) | 3.1.4 | 既に PostgreSQL の RDS を運用しているチームが、埋め込みの検索を追加します。最も運用… |
| [rag 問10](../../exercises/rag.md#q10) | 3.1.4 | 10 億件の古い文書を、検索の頻度は低いまま低コストで保存したいと考えています。適切な選択はどれです… |

<!-- questions:end -->
