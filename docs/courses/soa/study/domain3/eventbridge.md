# 分野3: イベント駆動の自動化

きっかけごとの仕組みと、Lambda を動かす権限を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.2.2](../../domain3.md#skill-3-2-2) | イベント駆動の自動化 |

## 学習の順番 {#study-order}

1. [Event Notifications](../../../../services/s3.md#event-notifications)と[S3 イベント通知](../../../../services/messaging.md#s3-events): 2 つの経路の違いを確認します。
2. [スケジュール](../../../../services/messaging.md#eventbridge-schedule): 定期実行の方法を確認します。
3. [Lambda の実行ロール](../../../../services/iam.md#lambda-execution-role): 実行ロールとリソースベースポリシーを区別します。
4. [EventBridge による修復パターン](../../../../services/operations.md#eventbridge-remediation)と[AWS DevOps Agent](../../../../services/operations.md#devops-agent): 修復の起動を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| サフィックスで絞って Lambda を動かす | S3 Event Notifications |
| FIFO キューへ送る | バケットで EventBridge を有効にする |
| S3 の通知で Lambda が動かない | リソースベースポリシーで S3 を許可 |
| 夜に開発環境を止める | スケジュールと `AWS-StopEC2Instance` |
| 複数の手順と再試行 | Step Functions |

## 引っかかりやすい点 {#traps}

- Event Notifications の SQS は標準キューのみで、SNS の FIFO トピックも送信先にできません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [eventbridge 問11](../../exercises/eventbridge.md#q11) | 3.2.2 | 画像が S3 にアップロードされたら Lambda で処理します。.jpg だけを対象にしたいです。… |
| [eventbridge 問12](../../exercises/eventbridge.md#q12) | 3.2.2 | S3 のオブジェクト作成イベントを、SQS の FIFO キューへ順序付きで送りたいと考えています。… |
| [eventbridge 問13](../../exercises/eventbridge.md#q13) | 3.2.2 | S3 のイベント通知で Lambda を呼び出せません。担当者は関数の実行ロールに s3:* を追加… |
| [eventbridge 問14](../../exercises/eventbridge.md#q14) | 3.2.2 | 開発環境の EC2 を、平日の夜に自動で止めたいと考えています。対象はタグで決まっています。コードを… |
| [eventbridge 問15](../../exercises/eventbridge.md#q15) | 3.2.2 | セキュリティグループの変更を検知したら、変更内容の確認、元に戻す処理、通知を順番に実行します。途中の… |
| [eventbridge 問16](../../exercises/eventbridge.md#q16) | 3.2.2 | アラートをきっかけにインシデントの調査を自動で始めさせ、テレメトリとデプロイの情報から根本原因の候補… |

<!-- questions:end -->
