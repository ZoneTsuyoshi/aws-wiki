# 分野2: ベクトルインデックスとベクトル化

ベクトルインデックスの種類と調整、チャンク化と埋め込みの概念を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.1.8](../../domain2.md#skill-2-1-8) | ベクトルインデックスの種類 |
| [2.4.6](../../domain2.md#skill-2-4-6) | ベクトル化の概念 |

## 学習の順番 {#study-order}

1. [ベクトルインデックス](../../../../services/databases-specialized.md#vector-indexes): Flat、HNSW、IVF を比べます。
2. [pgvector](../../../../services/genai-apps.md#pgvector): バージョンの条件を確認します。
3. [チャンク化](../../../../services/genai-apps.md#chunking): 大きさの影響を理解します。
4. [埋め込みの選び方](../../../../services/genai-apps.md#embedding-selection): 次元とモデルの変更を押さえます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| `ef_search` | 上げると精度が上がる | 検索が遅くなる |
| `m`、`ef_construction` | 構築時に指定 | 構築が遅くなる |
| `probes` | IVFFlat の検索時 | 上げると精度が上がる |
| pgvector の HNSW | 0.5.0 以上 |  |
| 100 万チャンク、1,024 次元、float32 | 約 4.1 GB | × 4 バイトで計算 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 速度と精度を優先し、メモリに余裕がある | HNSW |
| メモリを抑える | IVFFlat。データの投入後に作る |
| 埋め込みモデルを変える | 全データの再埋め込みと列の次元の変更 |
| 回答に文脈が足りない | チャンクの大きさを調整 |

## 引っかかりやすい点 {#traps}

- `vector(n)` の `n` がモデルと違うと取り込みエラーになります。
- チャンク化の後に埋め込みます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [genai-vector 問5](../../exercises/genai-vector.md#q5) | 2.1.8 | Aurora PostgreSQL で数百万件のベクトルを検索します。メモリに余裕があり、速度と精度… |
| [genai-vector 問6](../../exercises/genai-vector.md#q6) | 2.1.8 | HNSW の検索の精度が足りません。検索は多少遅くなってもかまいません。インデックスの再構築はしませ… |
| [genai-vector 問7](../../exercises/genai-vector.md#q7) | 2.1.8 | IVFFlat について正しいものはどれですか。 |
| [genai-vector 問8](../../exercises/genai-vector.md#q8) | 2.1.8 | RDS for PostgreSQL の pgvector で HNSW のインデックスを作ると、a… |
| [genai-vector 問9](../../exercises/genai-vector.md#q9) | 2.4.6 | Knowledge Bases で、回答に文脈が足りないことが多いです。チャンクの大きさの調整の説明… |
| [genai-vector 問10](../../exercises/genai-vector.md#q10) | 2.4.6 | 埋め込みモデルを 1,024 次元のものへ変更します。pgvector の列は vector(153… |
| [genai-vector 問11](../../exercises/genai-vector.md#q11) | 2.4.6 | 100 万チャンクを 1,024 次元、float32 で保存します。ベクトルだけの容量はおよそいく… |
| [genai-vector 問12](../../exercises/genai-vector.md#q12) | 2.4.6 | ベクトルの取り込みの流れの順序として正しいものはどれですか。 |

<!-- questions:end -->
