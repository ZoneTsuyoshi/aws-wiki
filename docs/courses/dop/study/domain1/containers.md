# 分野1: コンテナのデプロイ

コンテナ固有のデプロイの仕組みと、起動の失敗の切り分けを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [終了コード](../../domain1.md#t1-2-exit-codes) | 終了コードによる健全性の測定 |
| [アクセス権限](../../domain1.md#t1-4-permissions) | リポジトリへのアクセス権限 |
| [デプロイ方式](../../domain1.md#t1-4-methods) | 各プラットフォームのデプロイ方式、さまざまなデプロイ方式の使用 |
| [ミュータブルとイミュータブル](../../domain1.md#t1-4-mutable-immutable) | ミュータブルとイミュータブル |
| [デプロイの問題の解決](../../domain1.md#t1-4-troubleshooting) | デプロイの問題の解決 |

## 学習の順番 {#study-order}

1. [デプロイ](../../../../services/containers.md#ecs-deployments): ローリング、Blue/Green、カナリア、線形の指定を確認します。
2. [デプロイサーキットブレーカー](../../../../services/containers.md#circuit-breaker): 起動できないデプロイを止めて戻す仕組みを理解します。
3. [タスクロールと実行ロール](../../../../services/containers.md#task-role-vs-execution-role): 2 つのロールの違いを覚えます。
4. [dependsOn](../../../../services/containers.md#depends-on): `START`、`COMPLETE`、`SUCCESS` の違いを押さえます。
5. [ヘルスチェックとプローブ](../../../../services/containers.md#probes): Readiness と Liveness の役割を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| イメージの取得に失敗する | タスク実行ロールと経路 |
| 新しいタスクが起動を繰り返す | サーキットブレーカーとロールバック |
| 移行が成功してからアプリを起動する | `dependsOn` の `SUCCESS` |
| 準備前の Pod に通信を流さない | Readiness プローブ |

## 引っかかりやすい点 {#traps}

- `COMPLETE` は終了コードを問わないので、失敗でも後続が起動します。
- コンテナの中を直接変更しても、タスクの置き換えで消えます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [containers 問1](../../exercises/containers.md#q1) | 終了コード | ECS のタスクで、最初に初期化コンテナがスキーマの移行を実行し、成功した場合にだけアプリのコンテナ… |
| [containers 問2](../../exercises/containers.md#q2) | アクセス権限 | Fargate のタスクが CannotPullContainerError で起動しません。アプリ… |
| [containers 問3](../../exercises/containers.md#q3) | デプロイ方式 | ECS（Fargate）の本番サービスで、新しい版を本番の通信の 10% に 15 分流して確認して… |
| [containers 問4](../../exercises/containers.md#q4) | デプロイ方式 | EKS の Deployment を更新すると、準備の整っていない Pod に通信が流れて 503 … |
| [containers 問5](../../exercises/containers.md#q5) | ミュータブルとイミュータブル | コンテナで動くアプリで、障害の調査のために本番のコンテナへ入ってライブラリを更新する運用があり、タス… |
| [containers 問6](../../exercises/containers.md#q6) | デプロイの問題の解決 | ECS の更新で新しいタスクが起動と停止を繰り返し、デプロイが何時間も完了しません。タスクの停止理由… |

<!-- questions:end -->
