# 分野2: メッセージングと API

部品を間に置いて切り離す判断と、API の種類の選択を扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [API の作成と管理](../../domain2.md#t2-1-api) | API の作成と管理 |
| [メッセージングとイベント駆動](../../domain2.md#t2-1-messaging) | イベント駆動アーキテクチャ、キューとメッセージングの概念、疎結合に必要なサービスの判断 |
| [ワークフローのオーケストレーション](../../domain2.md#t2-1-workflow) | ワークフローのオーケストレーション |

## 学習の順番 {#study-order}

1. [密結合と疎結合](../../../../services/messaging.md#coupling)と[選び方](../../../../services/messaging.md#how-to-choose): 疎結合の考え方と、3 つのサービスの選び方を確認します。
2. [標準と FIFO](../../../../services/messaging.md#standard-fifo)と[可視性タイムアウト](../../../../services/messaging.md#visibility-timeout): 順序、重複、可視性タイムアウトを押さえます。
3. [デッドレターキュー](../../../../services/messaging.md#sqs-dlq)と[ファンアウト](../../../../services/messaging.md#fanout): 失敗の隔離と 1 対多の配信を確認します。
4. [Standard と Express](../../../../services/step-functions.md#standard-express)と[エラー処理](../../../../services/step-functions.md#error-handling): ワークフローの種類とエラー処理を比べます。
5. [API の種類](../../../../services/api-gateway.md#api-types)と[プライベート統合](../../../../services/api-gateway.md#private-integration): API の種類と VPC 内への接続を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| SQS の保持 | 最大 14 日。既定は 4 日 | 急増のバッファ |
| 可視性タイムアウト | 既定 30 秒 | 処理時間より長くする |
| Step Functions | Standard は 1 年、Express は 5 分 | 長い業務フローか、短い大量の処理か |
| API Gateway の統合タイムアウト | 既定 29 秒 | 長い処理は非同期に |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 急増する注文を失わずに処理する | SQS |
| 順序と重複防止が必須 | FIFO キューとメッセージグループ ID |
| 1 つのイベントを複数の処理に渡す | SNS と SQS のファンアウト |
| 内容で振り分ける、SaaS 連携、スケジュール | EventBridge |
| 既存の JMS をコード変更なしで | Amazon MQ |
| 使用量プラン、API キー、キャッシュが要る | REST API |
| サーバーからクライアントへ送る | WebSocket API |

## 引っかかりやすい点 {#traps}

- 1 つの SQS キューを複数の処理で共有しても、全員には届きません。
- Lambda から Lambda を呼んで再試行を書いている構成の改善は Step Functions です。
- SNS に保持の機能はありません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [messaging 問1](../../exercises/messaging.md#q1) | メッセージング | セールの時に注文が急増し、注文処理のサーバーが追いつかずに注文を失っています。注文を失わず、後段のペ… |
| [messaging 問2](../../exercises/messaging.md#q2) | メッセージング | 1 つの注文イベントを、在庫、請求、通知の 3 つの処理に並列に渡します。各処理は別々に失敗しても再… |
| [messaging 問3](../../exercises/messaging.md#q3) | メッセージング | 銀行の取引の更新を、口座ごとに順番どおりに、重複なく処理します。どの設定が適切ですか。（2つ選択） |
| [messaging 問4](../../exercises/messaging.md#q4) | メッセージング | SQS のワーカーの処理に平均 2 分かかります。可視性タイムアウトは既定の 30 秒のままです。起… |
| [messaging 問5](../../exercises/messaging.md#q5) | メッセージング | 形式の不正なメッセージがキューに残り、ワーカーが何度も失敗して他の処理を妨げます。どう対応しますか。 |
| [messaging 問6](../../exercises/messaging.md#q6) | メッセージング | 複数の SaaS とアプリのイベントを受け、内容で別々の処理に振り分けます。毎日 3 時の定期実行も… |
| [messaging 問7](../../exercises/messaging.md#q7) | メッセージング | オンプレミスの JMS を使うアプリをコードの変更なしで AWS に移します。ブローカーの管理は減ら… |
| [messaging 問8](../../exercises/messaging.md#q8) | ワークフロー | Lambda が別の Lambda を呼び、再試行と分岐を自前で書いています。保守が難しくなりました… |
| [messaging 問9](../../exercises/messaging.md#q9) | ワークフロー | 毎秒数千件の短いイベントの処理を、ワークフローで 1 件ずつ数秒で実行します。実行回数あたりの費用を… |
| [messaging 問10](../../exercises/messaging.md#q10) | ワークフロー | ワークフローの途中の外部 API 呼び出しが一時的に失敗することがあります。再試行とエラー時の分岐を… |
| [messaging 問11](../../exercises/messaging.md#q11) | API の作成と管理 | API Gateway で、取引先ごとの呼び出し回数の制限と API キー、レスポンスのキャッシュが… |
| [messaging 問12](../../exercises/messaging.md#q12) | API の作成と管理 | チャットアプリで、サーバーからクライアントへメッセージを送ります。どの API の種類を選びますか。 |
| [messaging 問13](../../exercises/messaging.md#q13) | API の作成と管理 | API の処理に 3 分かかることがあり、呼び出し側でタイムアウトします。既定の統合タイムアウトは … |
| [messaging 問14](../../exercises/messaging.md#q14) | API の作成と管理 | プライベートサブネットの ALB の後ろのサービスを、REST API で公開します。ALB はイン… |

<!-- questions:end -->
