# 分野4: ベクトル検索の性能と運用

インデックスの調整、スコアの合成、継続的な運用を扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.2.2](../../domain4.md#skill-4-2-2) | 検索の性能を高める |
| [4.3.5](../../domain4.md#skill-4-3-5) | ベクトルストアの運用管理 |

## 学習の順番 {#study-order}

1. [ベクトルインデックス](../../../../services/databases-specialized.md#vector-indexes): HNSW のパラメータの効果を確認します。
2. [検索の改善](../../../../services/genai-apps.md#retrieval-optimization)と [OpenSearch](../../../../services/genai-apps.md#opensearch-vectors): ハイブリッド検索とフィルターを押さえます。
3. [運用](../../../../services/genai-apps.md#vector-operations)と[同期と鮮度](../../../../services/genai-apps.md#kb-sync): 監視の項目を覚えます。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 再現率に余裕があり遅い | `ef_search` を下げる |
| キーワードとベクトルのスコアの尺度が違う | 正規化プロセッサで揃えて合成 |
| 候補が多すぎる | 問い合わせを前処理してフィルター |
| 更新と削除が多く精度が落ちる | 定期的な再構築 |
| 関連性の低下を検知する | 取得の評価を定期実行 |

## 引っかかりやすい点 {#traps}

- 遅延の監視では関連性の低下は分かりません。
- ジョブが完了しても一部の文書が失敗していることがあります。統計を確認します。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [vector-stores 問14](../../exercises/vector-stores.md#q14) | 4.2.2 | HNSW の索引で、再現率は要件を満たしていますが、検索の p99 が要件を超えています。データ量は… |
| [vector-stores 問15](../../exercises/vector-stores.md#q15) | 4.2.2 | OpenSearch のハイブリッド検索を自分で構成します。キーワードのスコアとベクトルのスコアをそ… |
| [vector-stores 問16](../../exercises/vector-stores.md#q16) | 4.2.2 | 数百万チャンクの検索が遅いと報告されています。問い合わせのほとんどは特定の製品と年度に関するもので、… |
| [vector-stores 問17](../../exercises/vector-stores.md#q17) | 4.3.5 | OpenSearch の HNSW 索引で、文書の更新と削除が頻繁にあります。数か月かけて再現率が少… |
| [vector-stores 問18](../../exercises/vector-stores.md#q18) | 4.3.5 | Knowledge Bases の日次の同期を、EventBridge のスケジュールで起動していま… |
| [vector-stores 問19](../../exercises/vector-stores.md#q19) | 4.3.5 | ベクトルストアの品質を継続して保証したいと考えています。CloudWatch で遅延とディスクは監視… |

<!-- questions:end -->
