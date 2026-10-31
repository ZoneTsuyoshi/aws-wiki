# 分野2: Auto Scaling

ポリシーの選択、起動の失敗の切り分け、ECS と Lambda のスケーリングを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.1.1](../../domain2.md#skill-2-1-1) | コンピューティングのスケーリング |

## 学習の順番 {#study-order}

1. [EC2 Auto Scaling](../../../../services/ec2-beanstalk.md#auto-scaling)と[スケーリングクールダウン](../../../../services/ec2-beanstalk.md#asg-cooldown): ポリシーの種類と待ち時間を確認します。
2. [予測スケーリング](../../../../services/operations.md#predictive-scaling)と[ウォームプール](../../../../services/operations.md#warm-pools): 先回りの手段を区別します。
3. [ライフサイクルフック](../../../../services/operations.md#lifecycle-hooks)と[プロセスの一時停止](../../../../services/operations.md#suspend-processes): 起動と終了の前後の処理、調査中の保護を確認します。
4. [混合インスタンスとキャパシティ再調整](../../../../services/operations.md#mixed-instances)と[スケーリングの失敗の調査](../../../../services/operations.md#asg-troubleshooting): スポットと失敗の調査を確認します。
5. [サービスの Auto Scaling](../../../../services/containers.md#service-auto-scaling)と[同時実行とスケーリング](../../../../services/lambda.md#concurrency): 他のコンピューティングの仕組みを確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| ヘルスチェックの猶予期間 | CLI、SDK は 0 秒、コンソールは 300 秒 | 短いと起動と終了を繰り返す |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 目標値を保つ | ターゲット追跡 |
| 毎朝 9 時に増やす | スケジュール |
| 周期的な負荷に先回りする | 予測 |
| SQS の処理 | インスタンスあたりのバックログでターゲット追跡 |
| 起動に時間がかかる | ウォームプール |
| 調査中のインスタンスを守る | `ReplaceUnhealthy` の一時停止、スタンバイ |
| 起動できない理由を調べる | `describe-scaling-activities` |

## 引っかかりやすい点 {#traps}

- シンプルは古い方式で、AWS は勧めていません。
- 予約済み同時実行では実行環境は準備されません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [auto-scaling 問1](../../exercises/auto-scaling.md#q1) | 2.1.1 | Web サーバーの平均 CPU を 50% に保つよう、台数を自動で調整したいと考えています。第一候… |
| [auto-scaling 問2](../../exercises/auto-scaling.md#q2) | 2.1.1 | SQS のキューを処理するワーカーの Auto Scaling グループを、処理の遅れに合わせて増減… |
| [auto-scaling 問3](../../exercises/auto-scaling.md#q3) | 2.1.1 | CLI で作成した Auto Scaling グループで ELB ヘルスチェックを有効にすると、起動… |
| [auto-scaling 問4](../../exercises/auto-scaling.md#q4) | 2.1.1 | 初期化に 10 分かかるアプリで、スケールアウトの間に合わないことがあります。初期化済みのインスタン… |
| [auto-scaling 問5](../../exercises/auto-scaling.md#q5) | 2.1.1 | スケールインで終了する前に、インスタンスのログを S3 へ退避したいと考えています。どの機能を使いま… |
| [auto-scaling 問6](../../exercises/auto-scaling.md#q6) | 2.1.1 | 異常と判定されたインスタンスを調査している間に、Auto Scaling が置き換えてしまいます。調… |
| [auto-scaling 問7](../../exercises/auto-scaling.md#q7) | 2.1.1 | Auto Scaling グループのインスタンスが起動しません。原因の確認に最初に使うものはどれです… |
| [auto-scaling 問8](../../exercises/auto-scaling.md#q8) | 2.1.1 | スポットを使う Auto Scaling グループで、中断のリスクが高いインスタンスを、中断の前に置… |
| [auto-scaling 問9](../../exercises/auto-scaling.md#q9) | 2.1.1 | ECS サービスのタスク数を CPU の使用率に応じて増減したいと考えています。何を使いますか。 |
| [auto-scaling 問10](../../exercises/auto-scaling.md#q10) | 2.1.1 | Lambda で初回の呼び出しの遅延を避け、決まった時刻の急増に備えて準備しておきたいと考えています… |
| [auto-scaling 問11](../../exercises/auto-scaling.md#q11) | 2.1.1 | 毎日決まった周期で負荷が増えるアプリケーションで、負荷が増える前に容量を増やしたいと考えています。た… |

<!-- questions:end -->
