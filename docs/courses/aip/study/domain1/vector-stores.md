# 分野1: ベクトルストア

要件に合うストアを選び、メタデータと規模の設計を決めます。何を選ぶと何を諦めるかが問われます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.4.1](../../domain1.md#skill-1-4-1) | ベクトル DB の構成 |
| [1.4.2](../../domain1.md#skill-1-4-2) | メタデータの枠組み |
| [1.4.3](../../domain1.md#skill-1-4-3) | 大規模で高速なベクトル DB |
| [1.5.3](../../domain1.md#skill-1-5-3) | ベクトル検索のデプロイと設定 |

## 学習の順番 {#study-order}

1. [ベクトルストア](../../../../services/genai-apps.md#vector-stores)の表: ストアごとの向き不向きを覚えます。
2. [OpenSearch](../../../../services/genai-apps.md#opensearch-vectors)と [pgvector](../../../../services/genai-apps.md#pgvector): 必須の設定と誤ったときの症状を確認します。
3. [S3 Vectors](../../../../services/genai-apps.md#s3-vectors): Knowledge Bases で使うときの制約を押さえます。
4. [メタデータ](../../../../services/genai-apps.md#kb-metadata): `.metadata.json` とフィルター、`nmslib` の落とし穴を理解します。
5. [埋め込みの選び方](../../../../services/genai-apps.md#embedding-selection): 次元と容量の計算をします。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| シャード数の目安 | (元データ + 増加分) × 1.1 ÷ 1 シャード | 66 GiB を 30 GiB ずつなら 3 |
| 生データの大きさ | 件数 × 次元 × 4 バイト | 100 万件 1,024 次元で約 4.1 GB |
| HNSW の pgvector | 0.5.0 以上 | ハイブリッド検索には GIN も |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 運用を減らし、多くのコネクタを使う | Managed Knowledge Base。`RetrieveAndGenerate` は使えない |
| 既存の PostgreSQL と SQL で結合する | Aurora / RDS + pgvector |
| 大量で低頻度、低コスト | S3 Vectors。ハイブリッド検索は不可 |
| 関係をたどる質問 | Neptune Analytics |
| 属性と埋め込みを別のストアに置く | DynamoDB Streams で同期する |

## 引っかかりやすい点 {#traps}

- `dimension` がモデルと違うと取り込みエラーになります。
- 次元を変えるなら全データの再埋め込みです。
- `ef_search` を上げると精度が上がって遅くなります。
- プライマリシャードの数は後から簡単に変えられません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [vector-stores 問1](../../exercises/vector-stores.md#q1) | 1.4.1 | 小さなチームが社内文書の RAG を作ります。ベクトル DB の運用担当はおらず、SharePoin… |
| [vector-stores 問2](../../exercises/vector-stores.md#q2) | 1.4.1 | ある企業は業務データを Aurora PostgreSQL に持っています。契約の状態や期限と文書の… |
| [vector-stores 問3](../../exercises/vector-stores.md#q3) | 1.4.1 | 10 億件の古い技術文書を、低頻度の検索用に低コストで保管します。一方、この 1 年分の文書は頻繁に… |
| [vector-stores 問4](../../exercises/vector-stores.md#q4) | 1.4.1 | 文書の属性（所有部署、公開範囲）を DynamoDB でキー検索し、埋め込みは別のベクトル DB に… |
| [vector-stores 問5](../../exercises/vector-stores.md#q5) | 1.4.2 | 社内規定の RAG で、旧版の規定が返ることと、他部署の文書が返ることが問題になっています。文書は … |
| [vector-stores 問6](../../exercises/vector-stores.md#q6) | 1.4.2 | Knowledge Bases のベクトルストアに OpenSearch Serverless を使… |
| [vector-stores 問7](../../exercises/vector-stores.md#q7) | 1.4.2 | カスタム変換の Lambda で、チャンクごとに章番号のメタデータを付けました。同じ文書の .met… |
| [vector-stores 問8](../../exercises/vector-stores.md#q8) | 1.4.3 | OpenSearch Service のドメインで検索の遅延を重視したベクトル索引を設計します。元デ… |
| [vector-stores 問9](../../exercises/vector-stores.md#q9) | 1.4.3 | 1,000 万チャンクのベクトル索引でメモリの費用が問題です。Titan Text Embeddin… |
| [vector-stores 問10](../../exercises/vector-stores.md#q10) | 1.4.3 | 製造、法務、人事の文書を 1 つの索引で検索しており、件数が増えて遅くなりました。問い合わせのほとん… |
| [vector-stores 問11](../../exercises/vector-stores.md#q11) | 1.5.3 | Knowledge Bases の取り込み先として OpenSearch の索引を自分で作ります。埋… |
| [vector-stores 問12](../../exercises/vector-stores.md#q12) | 1.5.3 | Knowledge Bases のベクトルストアに Aurora PostgreSQL を使います。… |
| [vector-stores 問13](../../exercises/vector-stores.md#q13) | 1.5.3 | 小規模なチームが、数週間で RAG を公開します。ベクトル検索の調整の知識を持つ人はいません。一方、… |

<!-- questions:end -->
