# 分野4: メッセージング

SQS と SNS の API 呼び出しや無駄な処理を減らす方法と、連携の不具合の調べ方が問われます。サービスの選び方や基本の設計は[分野1](../domain1/messaging.md)で扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.1.1](../../domain4.md#skill-4-1-1) | サービス連携のデバッグ |
| [4.3.3](../../domain4.md#skill-4-3-3) | メッセージングの最適化 |

## 学習の順番 {#study-order}

1. [メッセージングの最適化](../../../../services/messaging.md#optimization): 目的と方法の対応を最初につかみます。
2. [ショートポーリングとロングポーリング](../../../../services/messaging.md#long-polling): 空の応答と料金を減らす設定を確認します。
3. [バッチ処理](../../../../services/messaging.md#batching): まとめて送る API の上限と、一部失敗の扱いを学びます。
4. [ファンアウト](../../../../services/messaging.md#fanout)と[フィルターポリシー](../../../../services/messaging.md#filter-policies): 消費者ごとに必要なものだけを届ける方法を学びます。
5. [Lambda から使うときの設定](../../../../services/messaging.md#sqs-lambda-settings): `BatchSize` やバッチウィンドウの調整を押さえます。
6. [処理中メッセージの上限](../../../../services/messaging.md#in-flight)と[サービス統合の問題](../../../../services/observability.md#debug-integration): 症状と確認先を結びつけます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| `WaitTimeSeconds` | 0 はショート、1〜20 はロング | 最大は 20 秒です |
| `MaxNumberOfMessages` | 既定 1、最大 10 | 10 件そろうまで待つわけではありません |
| バッチ API | 10 件まで、`SendMessageBatch` は合計 1 MiB | リクエスト数が減り、料金も下がります |
| `BatchSize`（Lambda） | 既定 10、標準は最大 10,000、FIFO は最大 10 | 10 を超えるならバッチウィンドウを 1 秒以上にします |
| 可視性タイムアウト | 関数のタイムアウト × 6 + バッチウィンドウ | 推奨値です |
| `maxReceiveCount` | 5 以上 | 1 だとスロットリング 1 回で DLQ に移ることがあります |
| 処理中メッセージ | 約 120,000 | 上限に達すると受信できなくなります |
| フィルターポリシー | キー 5 個、組み合わせ 150、反映まで最大 15 分 | 組み合わせは各配列の値の数の積です |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| キューにメッセージがあるのに空の応答が返る、受信の料金が高い | `ReceiveMessageWaitTimeSeconds` を 1〜20 にして、ロングポーリングにします |
| 送信と削除のリクエスト数を減らしたい | `SendMessageBatch` と `DeleteMessageBatch` で 10 件ずつ扱います |
| 購読者が一部のメッセージしか必要としない | SNS のフィルターポリシーを設定します。消費者側で捨てるより処理量と料金を減らせます |
| 本文の内容でフィルターしたい | `FilterPolicyScope` を `MessageBody` にします |
| 1 つのイベントを複数の処理に独立して渡したい | SNS から複数の SQS キューへファンアウトします |
| 処理が滞留するので消費者を自動で増やしたい | `ApproximateAgeOfOldestMessage` で滞留に気づき、インスタンスあたりのバックログでターゲット追跡します |
| 同じメッセージが 2 回処理される | 可視性タイムアウトを関数のタイムアウトの 6 倍以上にし、処理を冪等にします |
| SNS の購読は成功しているのに SQS に届かない | キューのアクセスポリシーで `sqs:SendMessage` を許可します。KMS で暗号化しているならキーポリシーも確認します |
| 受信で `OverLimit` になる | 処理中が上限に達しています。処理後の `DeleteMessage` を確認します |
| Lambda のバッチで一部だけ失敗すると全件を再処理してしまう | `ReportBatchItemFailures` で失敗分だけ戻します |

## 引っかかりやすい点 {#traps}

- **ロングポーリングにしたのに効かない:** コードの `WaitTimeSeconds=0` はキューの属性より優先されます。
- **受信がタイムアウトする:** SDK の読み取りタイムアウトが `WaitTimeSeconds` より短いと、待っている途中で切れます。20 秒より長くします。
- **バッチの一部が消える:** `SendMessageBatch` の応答の `Failed` を確認して再送します。
- **本文でフィルターしているつもりで何も届かない:** `FilterPolicyScope` の既定は `MessageAttributes` です。属性を付けずに発行すると一致しません。
- **SQS の `Body` が想定と違う:** raw メッセージ配信が無効だと SNS の JSON で包まれます。`Message` を取り出します。
- **フィルターを変えたのに効かない:** 反映まで最大 15 分は古いポリシーで判定されることがあります。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [messaging 問4](../../exercises/messaging.md#q4) | 4.1.1 | バッチ処理の消費者が、1 通のメッセージの可視性タイムアウトを繰り返し延長しています。受信から 12… |
| [messaging 問5](../../exercises/messaging.md#q5) | 4.3.3 | SQS キューを読むアプリケーションで、メッセージが残っているのに ReceiveMessage が… |
| [messaging 問9](../../exercises/messaging.md#q9) | 4.3.3 | FIFO キューを使う注文処理で、すべてのメッセージの MessageGroupId を "orde… |
| [messaging 問10](../../exercises/messaging.md#q10) | 4.3.3 | FIFO キューのスループットを上げるために、高スループットモードを有効にします。キューの属性の正し… |
| [messaging 問16](../../exercises/messaging.md#q16) | 4.1.1 | ある開発者は SNS トピックの MaximumMessageSize を 1 MiB に変更しよう… |

<!-- questions:end -->
