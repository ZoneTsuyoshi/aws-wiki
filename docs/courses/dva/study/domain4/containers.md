# 分野4: コンテナ

Kubernetes のプローブ、ECS のヘルスチェック、タスクが動かないときの調べ方、CPU とメモリの決め方が問われます。イメージの作成やデプロイの手順は[分野3](../domain3/containers.md)で扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.1.4](../../domain4.md#skill-4-1-4) | デプロイの失敗の調査 |
| [4.2.5](../../domain4.md#skill-4-2-5) | プローブとヘルスチェック |
| [4.3.1](../../domain4.md#skill-4-3-1) | サービスの Auto Scaling |
| [4.3.2](../../domain4.md#skill-4-3-2) | CPU とメモリの割り当て |

## 学習の順番 {#study-order}

1. [ヘルスチェックとプローブ](../../../../services/containers.md#probes): 3 種類のプローブの役割と、ECS との対応を覚えます。
2. [プローブのタイミング](../../../../services/containers.md#probe-timing): 既定値と、起動時間からの計算を確認します。
3. [ECS の healthCheck](../../../../services/containers.md#ecs-healthcheck)と[サービスの設定](../../../../services/containers.md#service-settings): `startPeriod` と猶予期間の使いどころを学びます。
4. [memory と memoryReservation](../../../../services/containers.md#memory-settings)と [Kubernetes の resources](../../../../services/containers.md#k8s-resources): 上限を超えたときの症状を結びつけます。
5. [Fargate と EC2](../../../../services/containers.md#fargate-vs-ec2): CPU とメモリの組み合わせの制約を確認します。
6. [サービスの Auto Scaling](../../../../services/containers.md#service-auto-scaling): タスク数を増減する設定を学びます。
7. [デプロイサーキットブレーカー](../../../../services/containers.md#circuit-breaker)と[デプロイ失敗の診断](../../../../services/cicd.md#troubleshooting-deployments): 失敗の検知方法と確認先を押さえます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| プローブ | 間隔 10 秒、タイムアウト 1 秒、失敗 3 回 | 応答が遅いエンドポイントはタイムアウトで失敗します |
| ECS `healthCheck` | 間隔 30 秒、タイムアウト 5 秒、再試行 3 回 | 異常の判定までおよそ 90 秒です |
| `startPeriod` | 既定はオフ、0〜300 秒 | この間の失敗は回数に数えません |
| `healthCheckGracePeriodSeconds` | 既定 0 | 起動の遅いタスクでは伸ばします |
| サーキットブレーカー | 希望数の 50%、最小 3、最大 200 | ローリング更新でのみ使えます |
| Fargate の一時ストレージ | 既定 20 GiB、最大 200 GiB | `ephemeralStorage` で増やします |
| Fargate の CPU とメモリ | 1 vCPU は 2〜8 GB、2 vCPU は 4〜16 GB など | 組み合わせ以外は登録時にエラーです |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 固まった Pod を自動で再起動したい | ライブネスプローブを使います |
| Pod を再起動せず、トラフィックだけ止めたい | レディネスプローブを使います。起動完了や DB 接続の確認もこちらです |
| 最長 5 分で起動するアプリが再起動を繰り返す | `startupProbe` を `failureThreshold: 30`、`periodSeconds: 10` にします |
| 起動に 90 秒かかる ECS タスクが ALB のチェックで置き換えられ続ける | `healthCheckGracePeriodSeconds` を 120 にします |
| 起動に 2 分かかるアプリがコンテナのチェックで失敗する | `startPeriod: 120` にします |
| タスクの停止理由に `OutOfMemoryError` が出る | `memory` のハードリミットを超えています。値を見直します |
| Pod が `OOMKilled` で再起動する | `limits.memory` を超えています |
| Pod が `Pending` のまま | `requests` を満たす空きのあるノードがありません |
| サービスイベントに `unable to place a task` が出る | 配置の制約に合うインスタンスがありません |
| 負荷に応じてタスク数を増減したい | Application Auto Scaling で `ECSServiceAverageCPUUtilization` のターゲット追跡を設定します |

## 引っかかりやすい点 {#traps}

- **DB 障害で全 Pod が再起動を繰り返す:** ライブネスに依存先の確認を入れています。依存先はレディネスで確認します。
- **2 秒で応答するのに再起動を繰り返す:** プローブの `timeoutSeconds` の既定は 1 秒です。
- **アプリは正常なのにタスクが置き換えられる:** イメージに `curl` がないと、`CMD-SHELL` の `curl -f` は常に失敗します。
- **ECS でレディネスとライブネスを分けようとする:** ECS には分ける仕組みがありません。コンテナの `healthCheck` とターゲットグループのヘルスチェックで確認します。
- **ログが出ない、タスクが起動しない:** 実行ロールに `logs:CreateLogStream` と `logs:PutLogEvents` がありません。
- **`No space left on device` が出る:** Fargate の一時ストレージが既定の 20 GiB のままです。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [containers 問8](../../exercises/containers.md#q8) | 4.3.2 | EC2 で動く ECS タスクのコンテナは、普段 128 MiB で、まれに 256 MiB まで使… |
| [containers 問9](../../exercises/containers.md#q9) | 4.3.2 | Fargate のタスク定義を登録します。cpu と memory の組み合わせとして、**有効な*… |
| [containers 問11](../../exercises/containers.md#q11) | 4.2.5 | タスク定義の healthCheck の既定値と範囲について、正しいものはどれですか。（2つ選択） |
| [containers 問17](../../exercises/containers.md#q17) | 4.3.1 | ECS サービスのタスク数を CPU 使用率 60% に保ちたいと考えています。使う仕組みとして最も… |
| [containers 問19](../../exercises/containers.md#q19) | 4.2.5 | Kubernetes で起動に最長 5 分かかるアプリがライブネスプローブの失敗で再起動を繰り返して… |

<!-- questions:end -->
