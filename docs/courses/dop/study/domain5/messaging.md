# 分野5: イベントソースとワークフロー

イベントの受け方と、処理の失敗の設計を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [イベントソース](../../domain5.md#t5-1-event-sources) | イベントを生成、取得、処理するサービス、イベントソースの統合 |
| [アーキテクチャ](../../domain5.md#t5-1-architectures) | イベント駆動アーキテクチャ |
| [ワークフロー](../../domain5.md#t5-1-workflows) | イベント処理のワークフロー |

## 学習の順番 {#study-order}

1. [AWS Health イベントの自動化](../../../../services/operations.md#health-events): ルールの作り方と組織ビューを確認します。
2. [イベントバス](../../../../services/messaging.md#event-buses): 中央のバスへの転送を理解します。
3. [ファンアウト](../../../../services/messaging.md#fanout): ファンアウトの効果を押さえます。
4. [部分バッチレスポンス](../../../../services/lambda.md#partial-batch-response): 部分バッチレスポンスを確認します。
5. [ストリームのエラー処理の設定](../../../../services/lambda.md#esm-stream-errors): ストリームの失敗の扱いを確認します。
6. [ターゲットの再試行と DLQ](../../../../services/messaging.md#target-retry-dlq): 場所ごとの受け皿を覚えます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| SQS の可視性タイムアウト | 関数のタイムアウトの 6 倍以上 | 短いと重複が増える |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 組織全体の AWS Health | 組織ビューと委任管理者 |
| 読み取り専用の管理イベントを受ける | `ENABLED_WITH_ALL_CLOUDTRAIL_MANAGEMENT_EVENTS` |
| 再読み取りと順序が必要 | Kinesis Data Streams |
| 1 件の失敗でバッチ全体が戻る | 部分バッチレスポンス |

## 引っかかりやすい点 {#traps}

- CloudTrail 経由のイベントは既定のイベントバスに届きます。
- AWS Health API はサポートプランの条件があります。EventBridge での受信には不要です。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [messaging 問7](../../exercises/messaging.md#q7) | イベントソース | 組織の全アカウントの AWS Health のイベントを一か所に集めて担当へ通知します。アカウントご… |
| [messaging 問8](../../exercises/messaging.md#q8) | イベントソース | 本番の VPC で ModifyVpcAttribute が呼ばれたら通知します。また、読み取り専用… |
| [messaging 問9](../../exercises/messaging.md#q9) | イベントソース | 全アカウントの GuardDuty と AWS Config のイベントを、セキュリティアカウントの… |
| [messaging 問10](../../exercises/messaging.md#q10) | アーキテクチャ | EC サイトの注文のイベントを在庫、請求、通知の 3 つのチームが処理します。請求のシステムは月に一… |
| [messaging 問11](../../exercises/messaging.md#q11) | アーキテクチャ | 次の 2 つの処理のパターンを選びます。(1) クリックのログを順序どおりに複数のアプリが読み、過去… |
| [messaging 問12](../../exercises/messaging.md#q12) | アーキテクチャ | SaaS からのイベントと AWS のサービスのイベントを同じ仕組みで受け、内容のパターンで振り分け… |
| [messaging 問13](../../exercises/messaging.md#q13) | ワークフロー | SQS と Lambda のバッチ処理で、1 件の失敗でバッチ全体が再処理され、処理の重複が増えてい… |
| [messaging 問14](../../exercises/messaging.md#q14) | ワークフロー | イベント処理の失敗の受け皿を設計します。(1) EventBridge から Lambda への非同… |
| [messaging 問15](../../exercises/messaging.md#q15) | ワークフロー | Kinesis を読む Lambda で 1 件の不正なレコードのためにシャードの処理が止まっていま… |

<!-- questions:end -->
