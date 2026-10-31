# 分野3: ワークロードの分離

前段と後段を別々にスケールさせるために、何を間に置くかを判断します。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [ワークロードの分離](../../domain3.md#t3-2-decoupling) | キューとメッセージングの概念、部品が別々にスケールできるようにワークロードを分離する |

## 学習の順番 {#study-order}

1. [密結合と疎結合](../../../../services/messaging.md#coupling)と[ファンアウト](../../../../services/messaging.md#fanout): キューとファンアウトで部品を切り離す方法を確認します。
2. [Kinesis Data Streams](../../../../services/streaming.md#kinesis-data-streams): 順序付きで複数のアプリが読む場面を押さえます。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 受付と重い処理を分ける | SQS とワーカーの Auto Scaling |
| 処理をあとから追加する | SNS に SQS キューの購読を足す |
| 順序付きで複数のアプリが読み直す | Kinesis Data Streams |

## 引っかかりやすい点 {#traps}

- 同じサーバーのサイズを上げるだけでは、結合は残ります。
- SQS のメッセージは 1 つのコンシューマーが処理します。全員に届けるなら SNS を前に置きます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [messaging 問15](../../exercises/messaging.md#q15) | ワークロードの分離 | 動画のアップロードの受付と変換が同じサーバーにあり、変換の CPU で受付まで遅くなります。部品を別… |
| [messaging 問16](../../exercises/messaging.md#q16) | ワークロードの分離 | 同じストリームを、不正検知と集計の 2 つのアプリが順序どおりに、別々に読みます。読み直しも必要です… |
| [messaging 問17](../../exercises/messaging.md#q17) | ワークロードの分離 | 注文イベントに新しい分析の処理をあとから追加します。既存の処理を変更せず、新しい処理は別にスケールさ… |

<!-- questions:end -->
