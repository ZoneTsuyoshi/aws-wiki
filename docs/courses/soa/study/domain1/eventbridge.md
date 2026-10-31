# 分野1: EventBridge と通知

通知が届かない原因と、ルールが動かないときの切り分けを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.1.5](../../domain1.md#skill-1-1-5) | SNS への通知 |
| [1.2.2](../../domain1.md#skill-1-2-2) | EventBridge のルーティングとルールの調査 |

## 学習の順番 {#study-order}

1. [トピックのアクセスポリシーと暗号化](../../../../services/messaging.md#sns-access): S3 や暗号化したトピックで必要な許可を確認します。
2. [AWS User Notifications](../../../../services/operations.md#user-notifications)と[Amazon Q Developer in chat applications](../../../../services/operations.md#q-chat): SNS と使い分ける通知の手段を確認します。
3. [イベントバス](../../../../services/messaging.md#event-buses)と[ルールとイベントパターン](../../../../services/messaging.md#eventbridge-rules): バスとパターンの誤りを切り分けます。
4. [ターゲットの再試行と DLQ](../../../../services/messaging.md#target-retry-dlq): 再試行の既定と DLQ の条件を覚えます。
5. [入力トランスフォーマー](../../../../services/messaging.md#input-transformer)と[Pipes](../../../../services/messaging.md#eventbridge-pipes): イベントの形を変える機能と、情報を足す機能を区別します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| ターゲットの再試行 | 185 回か 24 時間 | 権限不足は再試行しない |
| `MaximumEventAgeInSeconds` | 既定 86,400 秒 | 古いイベントを捨てる |
| DLQ | SQS の標準キュー | FIFO は使えない |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| S3 の通知の検証エラー | トピックのポリシーで `s3.amazonaws.com` を許可 |
| 暗号化したトピックに届かない | KMS のキーポリシーでサービスを許可 |
| AWS の通知を人に届ける | User Notifications |
| Slack へ通知する | SNS と Amazon Q Developer in chat applications |
| 一致するがターゲットが動かない | Lambda のリソースベースポリシーで `events.amazonaws.com` を許可 |
| 配信できないイベントを残す | ターゲットの DLQ とキューポリシー |
| 1 対 1 の連携の途中で情報を足す | Pipes のエンリッチメント |

## 引っかかりやすい点 {#traps}

- 実行ロールは、EventBridge が Lambda を呼ぶ権限ではありません。
- 一致しなかったイベントは DLQ に入りません。
- `ERROR_CODE` が `INVALID_JSON` なら、入力テンプレートを確認します。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [eventbridge 問1](../../exercises/eventbridge.md#q1) | 1.1.5 | S3 のイベント通知の送信先に SNS トピックを指定したところ、設定の保存時に送信先の検証エラーに… |
| [eventbridge 問2](../../exercises/eventbridge.md#q2) | 1.1.5 | KMS のカスタマー管理キーで暗号化した SNS トピックに、CloudWatch アラームの通知が… |
| [eventbridge 問3](../../exercises/eventbridge.md#q3) | 1.1.5 | AWS Health の通知を、担当者のメールとコンソールで一か所で管理したいと考えています。アプリ… |
| [eventbridge 問4](../../exercises/eventbridge.md#q4) | 1.1.5 | CloudWatch アラームの通知を、運用チームの Slack のチャンネルへ届けたいと考えていま… |
| [eventbridge 問5](../../exercises/eventbridge.md#q5) | 1.2.2 | EC2 の状態変化を受けるルールを作りましたが、ターゲットの Lambda が動きません。メトリクス… |
| [eventbridge 問6](../../exercises/eventbridge.md#q6) | 1.2.2 | EventBridge のターゲットに権限が足りず、イベントが失われています。原因の調査のために、配… |
| [eventbridge 問7](../../exercises/eventbridge.md#q7) | 1.2.2 | 宛先の API が停止している間に、古いイベントが配信されるのを避けたいと考えています。1 時間を過… |
| [eventbridge 問8](../../exercises/eventbridge.md#q8) | 1.2.2 | 入力トランスフォーマーを設定したところ、ターゲットが呼ばれなくなりました。DLQ のメッセージの属性… |
| [eventbridge 問9](../../exercises/eventbridge.md#q9) | 1.2.2 | SQS キューのメッセージに、顧客マスタの情報を Lambda で付け足してから、Step Func… |
| [eventbridge 問10](../../exercises/eventbridge.md#q10) | 1.2.2 | ルールの MatchedEvents が 0 のままです。パートナーのイベントが届くはずのルールを … |

<!-- questions:end -->
