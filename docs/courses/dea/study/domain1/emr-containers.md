# 分野1: EMR、コンテナと分散処理

コンテナの資源の調整と、分散処理とデータ構造の考え方を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.2.1](../../domain1.md#skill-1-2-1) | コンテナの性能の最適化 |
| [1.4.10](../../domain1.md#skill-1-4-10) | 分散コンピューティング |
| [1.4.11](../../domain1.md#skill-1-4-11) | データ構造とアルゴリズム |

## 学習の順番 {#study-order}

1. [Fargate と EC2](../../../../services/containers.md#fargate-vs-ec2): サーバーの管理の有無で選びます。
2. [resources](../../../../services/containers.md#k8s-resources): Pod の要求と上限を確認します。
3. [EMR on EKS](../../../../services/data-engineering.md#emr-on-eks): 資源を共用する理由を理解します。
4. [Redshift の構成](../../../../services/data-engineering.md#redshift-architecture): リーダーとコンピュートの分担を覚えます。
5. [ベクトルインデックス](../../../../services/databases-specialized.md#vector-indexes): グラフの使われ方を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| OS を管理せずタスク単位で資源を指定する | Fargate |
| Kubernetes に集約して Spark も動かす | EMR on EKS |
| Pod が OOM で再起動する | `resources` の要求と上限 |
| HDFS のデータを障害から守る | `dfs.replication` を 2 以上 |
| 範囲の検索が多い | B ツリー |
| 依存関係の順序を表す | DAG（循環のないグラフ） |

## 引っかかりやすい点 {#traps}

- シャッフルは重い処理です。結合や集計で起きます。
- 性能は一番遅いノードで決まります。
- タスクノードは HDFS を持ちません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [emr-containers 問1](../../exercises/emr-containers.md#q1) | 1.2.1 | ECS で動く変換のコンテナは負荷が安定しません。OS とサーバーは管理せず、GPU も不要です。C… |
| [emr-containers 問2](../../exercises/emr-containers.md#q2) | 1.2.1 | EKS の変換 Pod が OOM で再起動を繰り返します。ノードには余裕があります。まず見直す設定… |
| [emr-containers 問3](../../exercises/emr-containers.md#q3) | 1.2.1 | 組織は Kubernetes に資源を集約済みです。Spark の処理も同じ基盤で動かし、使用率を上… |
| [emr-containers 問4](../../exercises/emr-containers.md#q4) | 1.4.10 | Redshift で結合の性能が悪く、計画に再配布が多く出ます。再配布の説明として正しいものはどれで… |
| [emr-containers 問5](../../exercises/emr-containers.md#q5) | 1.4.10 | 分散処理の用語とサービスの対応で、正しいものはどれですか。 |
| [emr-containers 問6](../../exercises/emr-containers.md#q6) | 1.4.10 | EMR のコアノードが 1 台停止すると、HDFS のデータが失われました。dfs.replicat… |
| [emr-containers 問7](../../exercises/emr-containers.md#q7) | 1.4.11 | 次の組み合わせのうち、どちらもグラフのデータ構造に基づくものはどれですか。 |
| [emr-containers 問8](../../exercises/emr-containers.md#q8) | 1.4.11 | データ構造の説明として正しいものはどれですか。（2つ選択） |
| [emr-containers 問9](../../exercises/emr-containers.md#q9) | 1.4.11 | 注文テーブルで、期間の範囲を指定する検索が多いです。行指向の RDS で範囲検索を速くするのに適した… |

<!-- questions:end -->
