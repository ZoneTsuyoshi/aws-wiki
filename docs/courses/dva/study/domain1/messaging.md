# 分野1: メッセージング

分野1では、SQS、SNS、EventBridge でシステムを疎結合にする設計と、それぞれの設定を問われます。メッセージの滞留や配信失敗の調査は[分野4](../domain4/messaging.md)で扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.1.1](../../domain1.md#skill-1-1-1) | 密結合と疎結合、サービスの切り離し |
| [1.1.2](../../domain1.md#skill-1-1-2) | 同期と非同期の選択 |
| [1.1.3](../../domain1.md#skill-1-1-3) | 再試行と DLQ による耐障害性 |
| [1.1.5](../../domain1.md#skill-1-1-5) | SDK でのメッセージの送受信 |
| [1.1.8](../../domain1.md#skill-1-1-8) | イベント駆動パターン |
| [1.2.3](../../domain1.md#skill-1-2-3) | Lambda から使うときの失敗の扱い |
| [1.2.4](../../domain1.md#skill-1-2-4) | Lambda との統合 |
| [1.3.1](../../domain1.md#skill-1-3-1) | メッセージの保持期間 |

## 学習の順番 {#study-order}

1. [密結合と疎結合](../../../../services/messaging.md#coupling)、[同期と非同期](../../../../services/messaging.md#sync-async): 問題文のどこで疎結合や非同期を選ぶのかをつかみます。
2. [選び方](../../../../services/messaging.md#how-to-choose): SQS、SNS、EventBridge の違いを比べます。
3. [標準と FIFO](../../../../services/messaging.md#standard-fifo): 順序と重複の違い、`MessageGroupId` と `MessageDeduplicationId` を覚えます。
4. [可視性タイムアウト](../../../../services/messaging.md#visibility-timeout)、[ショートポーリングとロングポーリング](../../../../services/messaging.md#long-polling): 重複処理と空の応答の原因を理解します。
5. [デッドレターキュー](../../../../services/messaging.md#sqs-dlq)、[メッセージ保持期間](../../../../services/messaging.md#retention-period)、[Lambda から使うときの設定](../../../../services/messaging.md#sqs-lambda-settings): 失敗の退避と、Lambda トリガーの値を押さえます。
6. [ファンアウト](../../../../services/messaging.md#fanout)、[サブスクリプションフィルターポリシー](../../../../services/messaging.md#filter-policies)、[配信の再試行](../../../../services/messaging.md#sns-retries): SNS で複数の宛先に配る方法を学びます。
7. [ルールとイベントパターン](../../../../services/messaging.md#eventbridge-rules)、[ターゲットの再試行と DLQ](../../../../services/messaging.md#target-retry-dlq)、[スケジュール](../../../../services/messaging.md#eventbridge-schedule): 内容による振り分けと失敗の扱いを学びます。
8. [S3 イベント通知](../../../../services/messaging.md#s3-events): 送信先の制約とループの防ぎ方を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| 可視性タイムアウト | 既定 30 秒、0 秒〜12 時間 | 処理時間より長くします |
| Lambda トリガーの可視性タイムアウト | 関数のタイムアウトの 6 倍 + バッチウィンドウ | 60 秒の関数なら 360 秒以上です |
| 保持期間 | 既定 4 日、60 秒〜14 日 | DLQ は元のキューより長くします |
| 遅延 | 既定 0、最大 15 分 | 超える予約は EventBridge Scheduler です |
| `WaitTimeSeconds` | 既定 0、最大 20 秒 | 1 以上でロングポーリングです |
| SQS のメッセージサイズ | 最大 1 MiB | 超えるなら Extended Client で S3 に置きます |
| SQS のバッチ | 10 件、合計 1 MiB | `MaxNumberOfMessages` も最大 10 です |
| FIFO の重複排除 | 5 分 | |
| FIFO のスループット | 300 回/秒、バッチで 3,000 件/秒（パーティションあたり） | 上げるならグループ ID を増やし、高スループットモードを有効にします |
| SNS のメッセージサイズ | 既定 256 KiB、最大 1 MiB | `MaximumMessageSize` で上げます。購読が 100 個以下で、すべて SQS、Firehose、Lambda のときだけです |
| フィルターポリシーの反映 | 最大 15 分 | 変更がすぐ効かない理由です |
| EventBridge のターゲット | ルールあたり 5 個（引き上げ不可） | |
| EventBridge の再試行（ルールのターゲット） | 既定 185 回、24 時間 | `RetryPolicy` で短くできます |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 下流の障害で呼び出し元まで止まる | 間に SQS を挟み、復旧後に処理できるようにします |
| 同じメッセージが2回処理される | 可視性タイムアウトを延ばし、処理を冪等にします |
| 処理が長引くメッセージ | `ChangeMessageVisibility` で延長します |
| 順序と重複防止が必須 | FIFO キューで `MessageGroupId` と `MessageDeduplicationId` を使います |
| 何度も失敗するメッセージを分離する | DLQ と `maxReceiveCount` を設定します |
| 1つのイベントを、独立した複数の処理に渡す | SNS + SQS のファンアウトにします |
| 購読者ごとに一部のメッセージだけ受け取る | SNS のフィルターポリシーを使います。本文で絞るなら `FilterPolicyScope` を `MessageBody` にします |
| SaaS のイベントや AWS の状態変化で起動する | EventBridge を使います |
| ターゲットに必要な項目だけ渡す | 入力トランスフォーマーを使います |
| 日本時間の 9 時に実行する | Scheduler の `ScheduleExpressionTimezone` を指定します |

## 引っかかりやすい点 {#traps}

- キューにメッセージがあるのに受信が空で返るよくある原因は、ショートポーリングです。`WaitTimeSeconds` はキューの属性より優先されるので、コードで 0 を渡すとショートポーリングになります。
- SDK の読み取りタイムアウトを `WaitTimeSeconds` より短くすると、待っている途中でタイムアウトします。
- 標準キューの DLQ では、元の送信時刻のまま保持期間を数えます。予定より早く消えるなら DLQ の保持期間を長くします。
- 購読は成功しているのに SNS からキューに届かないときは、キューのアクセスポリシーの `sqs:SendMessage` を確認します。暗号化キューならキーポリシーも確認します。
- raw メッセージ配信が無効だと、SQS の `Body` は SNS の JSON になります。`Message` を取り出してさらに解析します。
- S3 イベントの送信先に FIFO キューは指定できません。EventBridge を経由します。トリガーのバケットに書き込むと無限ループになります。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [messaging 問1](../../exercises/messaging.md#q1) | 1.2.4 | ある開発者は、SQS キューをイベントソースとする Lambda 関数を作成しています。関数のタイム… |
| [messaging 問2](../../exercises/messaging.md#q2) | 1.1.3 | ある EC2 のワーカーは SQS 標準キューからメッセージを受信して動画を変換します。変換は通常 … |
| [messaging 問3](../../exercises/messaging.md#q3) | 1.1.5 | メッセージを受信してから 15 秒後に、消費者が ChangeMessageVisibility を… |
| [messaging 問6](../../exercises/messaging.md#q6) | 1.3.1 | SQS 標準キューの DLQ を次のように設定しました。元のキューの保持期間は 4 日、DLQ の保… |
| [messaging 問8](../../exercises/messaging.md#q8) | 1.1.8 | SQS FIFO キューで ContentBasedDeduplication を有効にしています。… |
| [messaging 問11](../../exercises/messaging.md#q11) | 1.3.1 | SQS について正しい説明はどれですか。（2つ選択） |
| [messaging 問14](../../exercises/messaging.md#q14) | 1.1.8 | SNS のサブスクリプションに次のフィルターポリシーを設定しました。発行者はメッセージ属性を付けず、… |
| [messaging 問15](../../exercises/messaging.md#q15) | 1.1.3 | SNS トピックが HTTPS エンドポイントに配信しています。障害時の再試行が足りず、また、復旧時… |
| [messaging 問17](../../exercises/messaging.md#q17) | 1.1.8 | EventBridge のイベントの detail.region が us- で始まるもの以外を選ぶ… |
| [messaging 問18](../../exercises/messaging.md#q18) | 1.2.3 | EventBridge のルールのターゲットとして Lambda 関数を設定しています。通知は 1 … |
| [messaging 問19](../../exercises/messaging.md#q19) | 1.1.8 | EventBridge Scheduler で毎日日本時間の 9 時に Lambda 関数を実行する… |
| [messaging 問20](../../exercises/messaging.md#q20) | 1.1.3 | 障害で一部のイベントが処理できませんでした。修正後、昨日の 2 時間分のイベントをアーカイブから再送… |
| [messaging 問21](../../exercises/messaging.md#q21) | 1.1.1 | 注文 API の Lambda 関数は、在庫、メール送信、分析の 3 つのサービスを順に HTTP … |
| [messaging 問22](../../exercises/messaging.md#q22) | 1.1.1 | 次の設計のうち、密結合の兆候はどれですか。（2つ選択） |
| [messaging 問23](../../exercises/messaging.md#q23) | 1.1.1 | Web 層が受けた画像変換の要求を、固定台数のワーカーへ送っています。セールの時間帯は要求が平常の … |
| [messaging 問24](../../exercises/messaging.md#q24) | 1.1.2 | 決済画面では、カードの与信結果を利用者にすぐ表示します。その後の請求書 PDF の生成には約 3 分… |
| [messaging 問25](../../exercises/messaging.md#q25) | 1.1.2 | 開発者は boto3 で lambda_client.invoke(FunctionName="ca… |

<!-- questions:end -->
