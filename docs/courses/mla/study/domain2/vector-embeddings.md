# 分野2: 検索の最適化

検索の症状から調整の手段を選びます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.2.9](../../domain2.md#skill-2-2-9) | 検索コンポーネントと埋め込みモデルの最適化 |

## 学習の順番 {#study-order}

1. [検索の改善](../../../../services/genai-apps.md#retrieval-optimization): 手法と設定を確認します。
2. [埋め込みの選び方](../../../../services/genai-apps.md#embedding-selection): 次元の増減の影響を押さえます。

## こう問われたらこう考える {#decisions}

| 症状 | 調整 |
|---|---|
| 製品番号など固有の語で外れる | ハイブリッド検索 |
| 上位に関係のない文書が混ざる | リランク、メタデータフィルター |
| 複雑な質問で文書が足りない | クエリ分解 |
| 同義語で見つからない | クエリ拡張 |
| 保存と検索のコストが高い | 次元を下げ、精度を評価で確かめる |

## 引っかかりやすい点 {#traps}

- ハイブリッド検索は RDS、OpenSearch Serverless、MongoDB で使えます。S3 Vectors では使えません。
- リランクは取得済みの結果を並べ替えるので、取得できなかった文書は補えません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [vector-embeddings 問10](../../exercises/vector-embeddings.md#q10) | 2.2.9 | RAG で、製品番号「AB-123」を含む質問だけ関係のない文書が返ります。OpenSearch S… |
| [vector-embeddings 問11](../../exercises/vector-embeddings.md#q11) | 2.2.9 | 上位の検索結果に関係の薄い文書が混ざり、プロンプトのトークンも多いです。検索を速くすることより、精度… |
| [vector-embeddings 問12](../../exercises/vector-embeddings.md#q12) | 2.2.9 | 「A 社と B 社で売上が高いのはどちらですか」のような質問で、片方の文書しか取得できません。どの機… |

<!-- questions:end -->
