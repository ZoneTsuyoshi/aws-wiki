# メッセージングとイベント（SQS、SNS、EventBridge）

サービス同士を直接呼ばずにつなぐ仕組み。キューの Amazon SQS、通知の Amazon SNS、イベントルーターの Amazon EventBridge を、用途に応じて選んで使う。

[![SNS + SQS のファンアウト](../assets/diagrams/messaging-fanout.png)](../assets/diagrams/messaging-fanout.png)

## 密結合と疎結合 {#coupling}

| | 密結合 | 疎結合 |
| --- | --- | --- |
| つなぎ方 | 呼び出し先を直接呼ぶ | キューやイベントを間に挟む |
| 相手の障害 | 自分も失敗する | メッセージがたまり、復旧後に処理できる |
| 負荷の急増 | そのまま相手に届く | キューがバッファになる |
| 変更 | 呼び出し元の修正が必要 | 購読者を増やすだけで済む場合が多い |
| 動作の追跡 | 単純 | 分散するので X-Ray などが要る |

密結合のサインは「A の障害で B も止まる」「消費者を追加するたびに発行者のコードを変える」「B のピークに合わせて A も増やす」など。

| 解決したい問題 | 使うサービス |
| --- | --- |
| 処理を後回しにして負荷を平準化 | SQS |
| 1つの出来事を複数の宛先へ | SNS または EventBridge |
| 内容に応じて宛先を振り分け、SaaS とも連携 | EventBridge |
| 手順の順序や分岐を管理 | [Step Functions](step-functions.md) |
| 大量のデータを順序付きで複数の消費者へ | [Kinesis Data Streams](streaming.md) |

## 同期と非同期 {#sync-async}

| | 同期 | 非同期 |
| --- | --- | --- |
| 呼び出し元 | 結果が返るまで待つ | 受け付けだけ確認して先に進む |
| 例 | API Gateway + Lambda | SQS ベースの処理、EventBridge のイベント駆動 |
| 向いている場面 | 結果がすぐ必要、読み取り、短い処理 | 長い処理、ピークがある処理、複数の処理に広げたいとき |
| エラーの扱い | 呼び出し元がその場で扱う | DLQ、再試行、後からの処理 |
| 注意点 | 下流の遅延がそのまま伝わる | 結果の通知方法、重複、順序を考える必要がある |

```mermaid
sequenceDiagram
    participant C as クライアント
    participant A as API Gateway
    participant Q as SQS
    participant W as Lambda
    C->>A: POST /orders
    A->>Q: SendMessage
    A-->>C: 202 受付 ID
    Q->>W: バッチで処理
    C->>A: GET /orders/ID で状態確認
```

API Gateway の統合タイムアウト（REST API の既定は 29 秒）を超えそうな処理は、この形にする。呼び出し方の違いは [Lambda](lambda.md) を参照する。

## SQS {#sqs}

メッセージをためるキュー。消費者が **取りに行く** プル型で、1つのメッセージは基本的に1つの消費者が処理する。

```python
import boto3

sqs = boto3.client("sqs")
url = sqs.get_queue_url(QueueName="orders")["QueueUrl"]

sqs.send_message(QueueUrl=url, MessageBody='{"orderId": "1"}')

res = sqs.receive_message(
    QueueUrl=url,
    MaxNumberOfMessages=10,
    WaitTimeSeconds=20,   # ロングポーリング
    VisibilityTimeout=60,
)
for m in res.get("Messages", []):
    process(m["Body"])
    # 処理後に自分で削除する。削除しないとまた受信される
    sqs.delete_message(QueueUrl=url, ReceiptHandle=m["ReceiptHandle"])
```

### 標準と FIFO {#standard-fifo}

| | 標準キュー | FIFO キュー |
| --- | --- | --- |
| 配信 | 少なくとも1回。重複があり得る | 重複を持ち込まない（5 分の重複排除） |
| 順序 | ベストエフォート | メッセージグループ内で保証 |
| スループット | ほぼ無制限 | パーティションごとに API アクションあたり 300 回/秒。バッチで 3,000 件/秒。高スループットモードあり |
| 名前 | 自由 | `.fifo` で終わる |
| 向いている場面 | スループット優先 | 順序や重複防止が必須 |

FIFO の属性は次の2つを押さえる。

| 属性 | 役割 |
| --- | --- |
| `MessageGroupId` | 順序を守る単位で、FIFO では必須。同じグループは同時に処理されない。処理中のメッセージがあると、同じグループの次のメッセージは渡されない |
| `MessageDeduplicationId` | 5 分間の重複排除に使う。明示するか、本文の SHA-256 を使う `ContentBasedDeduplication` を有効にする |

```python
sqs.send_message(
    QueueUrl=fifo_url,
    MessageBody='{"orderId": "1"}',
    MessageGroupId="customer-123",
    MessageDeduplicationId="order-1",
)
```

スループットを上げるには、グループ ID の種類を増やし、高スループットモードを有効にする（`DeduplicationScope` を `messageGroup`、`FifoThroughputLimit` を `perMessageGroupId`）。

標準キューでも `MessageGroupId` を指定すると **フェアキュー** になり、特定のテナントの大量メッセージが他のテナントの遅延を招く問題を和らげられる。

### FIFO の設定の詳細 {#fifo-settings}

#### MessageGroupId

順序を守る単位。FIFO では送信のたびに必須で、省くと `SendMessage` が失敗する。128 文字まで。グループ数に上限はない。

同じグループのメッセージは1つずつしか処理されない。たとえば全メッセージのグループ ID を `"orders"` に固定すると、消費者を 10 台に増やしても同時に処理されるのは 1 件だけになる。顧客 ID や注文 ID のように種類の多い値を使う。

処理中のメッセージが削除されるか可視性タイムアウトが切れるまで、そのグループの次のメッセージは渡されない。1件の処理が失敗し続けると、そのグループ全体が止まる。

#### MessageDeduplicationId と ContentBasedDeduplication

同じ ID のメッセージは、5 分間は受け付けられても配信されない。ID は 128 文字まで。最初のメッセージを受信して削除した後でも、5 分間は ID が追跡され続ける。

| 状況 | 結果 |
| --- | --- |
| ID を指定した | その ID で重複を判定する |
| `ContentBasedDeduplication` が有効で ID を省略 | 本文の SHA-256 を ID にする。**属性は含まれない** |
| 有効で、かつ ID を指定した | 指定した ID が優先される |
| 無効で ID を省略 | 送信がエラーになる |

具体例を示す。本文が `{"sku":"a-1"}` で、属性 `channel` だけが `web` と `store` で違う2通を 1 分以内に送ると、内容ベースでは同じ ID になるので 2 通目は配信されない。別物として扱うなら ID を明示するか、違いを本文に入れる。

逆に、送信成功の応答を失った後、5 分を過ぎてから同じ ID で再送すると、重複として検出できない。

#### DeduplicationScope と FifoThroughputLimit

| 属性 | 値 | 意味 |
| --- | --- | --- |
| `DeduplicationScope` | `queue`、`messageGroup` | 重複を判定する範囲 |
| `FifoThroughputLimit` | `perQueue`、`perMessageGroupId` | スループットの上限をかける単位 |

高スループットモードには両方の組み合わせ（`messageGroup` と `perMessageGroupId`）が必要で、片方でも変えると通常のスループットに戻る。`perMessageGroupId` は `DeduplicationScope` が `messageGroup` のときだけ指定できる。

`messageGroup` にすると判定はグループごとになる。同じ `MessageDeduplicationId` でもグループが違えば別のメッセージとして配信される。

高スループットモードの上限はリージョンで異なる。たとえばバージニア北部では、バッチなしで 70,000 件/秒、バッチありで 700,000 件/秒。パーティションあたりは 300 件/秒（バッチで 3,000 件/秒）なので、グループ ID の種類が少ないと出せない。

!!! note "ReceiveRequestAttemptId"
    FIFO で `ReceiveMessage` の応答がネットワーク障害で失われたとき、同じ `ReceiveRequestAttemptId` で再試行すると、可視性タイムアウトが切れる前でも同じメッセージの組を受け取り直せる。

### 主な設定と上限 {#sqs-limits}

| 項目 | 属性 | 既定 | 範囲 |
| --- | --- | --- | --- |
| メッセージサイズ | `MaximumMessageSize` | 1,048,576 バイト（1 MiB） | 1,024 バイト〜1 MiB |
| 保持期間 | `MessageRetentionPeriod` | 345,600 秒（4 日） | 60 秒〜1,209,600 秒（14 日） |
| 可視性タイムアウト | `VisibilityTimeout` | 30 秒 | 0〜43,200 秒（12 時間） |
| 遅延 | `DelaySeconds` | 0 秒 | 0〜900 秒（15 分） |
| ロングポーリングの待ち時間 | `ReceiveMessageWaitTimeSeconds` | 0 秒（ショートポーリング） | 0〜20 秒 |
| 1 回の受信件数 | `MaxNumberOfMessages` | 1 件 | 1〜10 件 |
| バッチの件数 | | | 最大 10 件 |
| 処理中（in-flight）メッセージ | | | 標準は約 120,000、FIFO は 120,000 |
| メッセージ属性 | | | 10 個まで |

1 MiB を超えるものは、Extended Client Library で本体を S3 に置く。

属性を変えると反映までに最大 60 秒かかる。`MessageRetentionPeriod` だけは最大 15 分かかる。

```bash
aws sqs set-queue-attributes \
  --queue-url "$QUEUE_URL" \
  --attributes VisibilityTimeout=360,ReceiveMessageWaitTimeSeconds=20,MessageRetentionPeriod=1209600
```

!!! warning "古い教材の 256 KB"
    SQS のメッセージの上限は現在 1 MiB。古い教材には 256 KB と書かれたものがあり、AWS の Extended Client の説明にも 256 KB の記述が残っている。設問で値が出たら 1 MiB を基準に考える。

### メッセージ保持期間 {#retention-period}

`MessageRetentionPeriod` を過ぎたメッセージは、受信されていなくても自動で削除される。

週末に消費者を止めるシステムで既定の 4 日のままだと、連休中の障害で失う可能性がある。復旧にかかる最長の時間より長くする。

短くする変更は **既存のメッセージにも効く**。14 日から 1 日に変えると、1 日より古いメッセージは期限切れとして消えることがある。

### 最大メッセージサイズと Extended Client {#max-message-size}

`MaximumMessageSize` を超えるメッセージは拒否される。既定で上限の 1 MiB なので、通常は変更しない。`SendMessageBatch` では、10 件の **合計** が 1 MiB まで。800 KiB を 2 件まとめて送ると上限を超える。

| Extended Client Library | 内容 |
| --- | --- |
| 対応言語 | Java、Python |
| 最大サイズ | 2 GB |
| 仕組み | 本体を S3 に保存し、キューには S3 の参照を送る |
| 権限 | キューに加えて S3 バケットへのアクセスが必要 |
| 制限 | 同期クライアントのみ |

受信側も同じライブラリで読む。普通のクライアントで受けると、本体ではなく参照が見える。

### 処理中メッセージの上限 {#in-flight}

処理中（受信済みで未削除）のメッセージには上限がある。キューにためられるメッセージ数には上限がない。

| キュー | 上限 | 上限に達したとき |
| --- | --- | --- |
| 標準（ショートポーリング） | 約 120,000 | `OverLimit` エラー |
| 標準（ロングポーリング） | 約 120,000 | エラーなし。新しいメッセージが返らない |
| FIFO | 120,000 | エラーなし。処理に影響が出ることがある |

症状は「キューにメッセージがあるのに受信できない」。処理後の `DeleteMessage` を忘れていないか確認する。対処は早めの削除、キューの追加、クォータの引き上げ申請。

### 暗号化 {#sqs-encryption}

| 方式 | 属性 | 鍵 |
| --- | --- | --- |
| SSE-SQS | `SqsManagedSseEnabled` | SQS が管理する |
| SSE-KMS | `KmsMasterKeyId` | KMS キー |

1つのキューで使えるのはどちらか一方だけ。

- 暗号化されるのは **本文のみ**。キュー名、メッセージ ID、タイムスタンプ、属性は暗号化されない。機密情報を属性に入れない。
- 有効にした後に送られたメッセージだけが暗号化される。滞留中のメッセージは対象外。
- 暗号化キューへのリクエストは HTTPS と署名バージョン 4 が必須で、匿名リクエストは拒否される。

`KmsDataKeyReusePeriodSeconds` はデータキーを再利用する時間で、60〜86,400 秒（既定 300 秒）。短いほど安全だが KMS の呼び出しと料金が増える。KMS のスロットリングが出るなら長くする。

| 操作する側 | 必要な KMS の権限 |
| --- | --- |
| 送信側 | `kms:GenerateDataKey`、`kms:Decrypt` |
| 受信側 | `kms:Decrypt` |
| AWS サービス（SNS、EventBridge など） | キーポリシーで `kms:GenerateDataKey`、`kms:Decrypt` を許可 |

AWS マネージドキー（`alias/aws/sqs`）のキューは、別アカウントの Lambda を呼べない。サービスのプリンシパルを許可する必要があるなら、キーポリシーを編集できるカスタマーマネージドキーを使う。鍵の基本は [KMS](kms.md) を参照する。

### 可視性タイムアウト {#visibility-timeout}

受信されたメッセージは消えず、この時間だけ他の消費者から見えなくなる。時間内に `DeleteMessage` しないと再び見えるようになる。

```mermaid
sequenceDiagram
    participant C as 消費者
    participant Q as SQS
    C->>Q: ReceiveMessage
    Q-->>C: メッセージ（見えなくなる）
    C->>C: 処理
    alt 時間内に完了
        C->>Q: DeleteMessage
    else 時間切れ
        Q-->>C: 再び受信可能に（重複の原因）
    end
```

- 処理時間より長く設定する。短いと重複処理の原因になる。
- 処理が長引くなら `ChangeMessageVisibility` で延長する。
- 処理をやめるなら 0 にして、すぐ他の消費者に渡す。
- Lambda のトリガーでは、関数のタイムアウトの 6 倍以上に設定する。
- ショートポーリングで処理中の上限に達すると `OverLimit` エラーになる。

#### 値の決め方

処理の最大時間を基準にする。処理に最大 90 秒かかる EC2 のワーカーで既定の 30 秒のままだと、処理中に別のワーカーへ再配信され、二重に処理される。

長すぎても問題がある。12 時間にすると、ワーカーが落ちたメッセージは 12 時間後まで再処理されない。処理時間のばらつきが大きいなら、短めに設定して、処理中に定期的に延長する（ハートビート）。

SQS は少なくとも1回の配信なので、タイムアウトが十分でも重複はあり得る。処理は [冪等](sdk-resilience.md#idempotency) にする。

#### 3 か所の指定と優先順位

| 指定の場所 | 範囲 |
| --- | --- |
| キューの属性 `VisibilityTimeout` | そのキューの既定 |
| `ReceiveMessage` の `VisibilityTimeout` | その受信で返るメッセージ |
| `ChangeMessageVisibility` | 受信済みの1通 |

#### ChangeMessageVisibility の動き

```python
# 受信時の残りに足すのではなく、呼び出した時点から 120 秒に置き換わる
sqs.change_message_visibility(
    QueueUrl=url,
    ReceiptHandle=m["ReceiptHandle"],
    VisibilityTimeout=120,
)
```

- 新しい値は **呼び出した時点から** 数える。キューの設定が 60 秒で、受信の 15 秒後に 10 を指定すると、受信から 25 秒で見えるようになる。
- 上限の 12 時間は **最初に受信した時点から** の時間で、延長してもリセットされない。残り時間を超える値を指定するとエラーになる。
- 変更はその受信にだけ効く。削除せずに次に受信されたときは、元の値に戻る。

12 時間を超える処理は、1つのメッセージで扱わない。[Step Functions](step-functions.md) を使うか、処理を分割する。

#### Lambda の 6 倍の根拠

関数のタイムアウトがキューの可視性タイムアウトより長いと、イベントソースマッピングの作成や更新がエラーになる。AWS はさらに、関数のタイムアウトの **6 倍以上**、バッチウィンドウを使うなら **その値を足した時間** を勧めている。スロットリング時に Lambda が再試行する余裕を持たせるためである。

```text
関数のタイムアウト 60 秒、バッチウィンドウ 20 秒
可視性タイムアウト = 60 × 6 + 20 = 380 秒
```

足りないと、バッチの処理中にメッセージが再び見えるようになり、同じメッセージが同時に処理される。

### Lambda から使うときの設定 {#sqs-lambda-settings}

設定はキューではなくイベントソースマッピングに持つ。全体の仕組みは [Lambda](lambda.md#event-source-mapping) を参照する。

| 設定 | 既定 | 範囲 | 効果 |
| --- | --- | --- | --- |
| `BatchSize` | 10 | 標準は最大 10,000、FIFO は最大 10 | 1回で渡す件数 |
| `MaximumBatchingWindowInSeconds` | 0 | 0〜300 秒。標準キューのみ | 件数がそろうまで待つ時間 |
| `MaximumConcurrency` | なし | 2〜1,000 | このキューから同時に動かす関数の数 |
| `FunctionResponseTypes` | なし | `ReportBatchItemFailures` | 失敗したメッセージだけを戻す |

- `BatchSize` を 10 より大きくするなら、バッチウィンドウを 1 秒以上にする必要がある。
- 1回の呼び出しの合計は同期呼び出しの上限（6 MB）に収まる範囲に限られる。
- 既定ではバッチの1件でも失敗すると全件がキューに戻る。[部分バッチレスポンス](lambda.md#partial-batch-response) で失敗分だけ戻す。
- `maxReceiveCount` は 5 以上にすることを AWS は勧めている。1 だとスロットリング1回で DLQ に移ることがある。
- 暗号化キューなら実行ロールに `kms:Decrypt` が要る。`AWSLambdaSQSQueueExecutionRole` には含まれない。
- `MaximumConcurrency` とプロビジョンドモードは同時に使えない。

### ショートポーリングとロングポーリング {#long-polling}

| | ショート | ロング |
| --- | --- | --- |
| 設定 | `WaitTimeSeconds` が 0 | 1〜20 |
| 動き | サーバーの一部だけ見てすぐ返す | 全サーバーを見て、メッセージが来るか時間切れまで待つ |
| 空の応答 | 多い | 少ない |
| 料金 | リクエストが多いと高くなる | 下げられる |

キュー全体には `ReceiveMessageWaitTimeSeconds` を設定する。特別な理由がなければロングポーリングを使う。

`ReceiveMessage` の `WaitTimeSeconds` はキューの属性より優先される。属性を 20 にしていても、コードで `WaitTimeSeconds=0` を渡すとショートポーリングになる。

SDK のクライアントで読み取りタイムアウトを `WaitTimeSeconds` より短くすると、メッセージを待っている途中でタイムアウトする。読み取りタイムアウトは 20 秒より長くする。

ショートポーリングでは一部のサーバーしか見ないので、メッセージがあっても空の応答（false empty）が返ることがある。「メッセージがあるのに受信できない」「空の受信が多く料金が高い」は、ロングポーリングで解決する。

`MaxNumberOfMessages` の既定は 1。10 にすると1回の受信で最大 10 件取れるが、10 件そろうまで待つわけではなく、少なく返ることもある。

### デッドレターキュー {#sqs-dlq}

繰り返し失敗するメッセージを別のキューに移し、処理全体が詰まらないようにする。

```python
import json

sqs.set_queue_attributes(
    QueueUrl=url,
    Attributes={
        "RedrivePolicy": json.dumps(
            {
                "deadLetterTargetArn": "arn:aws:sqs:ap-northeast-1:111122223333:orders-dlq",
                "maxReceiveCount": "5",
            }
        )
    },
)
```

- `maxReceiveCount` は移動までに受信できる回数。少なすぎると一時的なエラーでも移動する。
- DLQ は元のキューと同じ種類にする（FIFO なら FIFO）。
- 原因を直したら **DLQ リドライブ** で元のキューに戻せる。
- 標準キューの有効期限は元の送信時刻のまま。DLQ の保持期間は元のキューより長くする。FIFO はここでリセットされる。
- 順序を厳密に守る必要がある FIFO では、DLQ が順序を崩すので注意する。
- `ApproximateAgeOfOldestMessage` などで監視し、[アラーム](observability.md) を設定する。

#### maxReceiveCount の決め方

受信されるたびにカウントが増え、`maxReceiveCount` を超えると DLQ に移る。API の説明では既定は 10。DLQ は元のキューと同じアカウント、同じリージョンに置く。

| 値 | 起きること |
| --- | --- |
| 1 | 一時的なエラー1回で DLQ に移る。消費者が受信だけして落ちても移る |
| 3〜5 | 一般的な範囲。Lambda なら 5 以上 |
| 1000 | 毒メッセージが長く居座り、保持期間が切れて DLQ に届かず消える恐れがある |

処理の失敗だけでなく、**受信した回数** で数える点に注意する。可視性タイムアウトが短くて再配信が続くと、処理が正常でも DLQ に移ることがある。

標準キューで `maxReceiveCount` が 3 より大きいとき、削除されないまま 3 回以上受信されたメッセージはキューの後ろに回される。このとき `ApproximateAgeOfOldestMessage` は、次のメッセージの経過時間を示す。

#### DLQ の保持期間

標準キューでは、DLQ に移っても期限は最初の送信時刻のまま。

```text
元のキューに 1 日いた後で DLQ に移動。DLQ の保持期間は 4 日
標準キュー: DLQ に残るのは 3 日
FIFO キュー: 時刻がリセットされ、DLQ に 4 日残る
```

元のキューの保持期間が 14 日で、DLQ も 14 日だと、13 日目に移ったメッセージは DLQ に 1 日しか残らない。DLQ の保持期間は常に元のキューより長くする。

#### リドライブ許可ポリシー {#redrive-allow-policy}

DLQ 側に `RedriveAllowPolicy` を設定し、どのキューが自分を DLQ にできるかを決める。

| `redrivePermission` | 意味 |
| --- | --- |
| `allowAll`（既定） | 同じアカウントとリージョンのどのキューでも可 |
| `byQueue` | `sourceQueueArns` に書いたキューだけ可（10 個まで） |
| `denyAll` | DLQ として使えない |

```json
{
  "redrivePermission": "byQueue",
  "sourceQueueArns": ["arn:aws:sqs:ap-northeast-1:111122223333:orders"]
}
```

`RedrivePolicy` は元のキューに、`RedriveAllowPolicy` は DLQ に設定する。

#### DLQ リドライブの動き

既定では元のキューに戻すが、同じ種類の別のキューも指定できる。

- 戻したメッセージは新しいメッセージとして扱われ、新しいメッセージ ID と時刻が付く。**保持期間もリセットされる**。
- 古いメッセージから順に戻すが、送信先では新着と混ざるので、順序は保証されない。
- FIFO から FIFO の DLQ に移るとき、重複排除 ID は元のメッセージ ID に置き換わる。

DLQ のアラームは `ApproximateNumberOfMessagesVisible` に設定する。`NumberOfMessagesSent` は失敗で移動したメッセージを数えないので使えない。

### 遅延キューとメッセージタイマー {#delay}

| | 遅延キュー | メッセージタイマー |
| --- | --- | --- |
| 範囲 | キュー全体（`DelaySeconds`） | メッセージごと（送信時の `DelaySeconds`） |
| 優先 | | タイマーが優先 |
| FIFO | 使える | 使えない |

どちらも最大 15 分。もっと先の予約には [EventBridge Scheduler](#eventbridge-schedule) を使う。可視性タイムアウトとの違いは、遅延が受信前に隠すのに対し、可視性タイムアウトは受信後に隠すこと。

```python
# 注文の 45 秒後に在庫確認を走らせる。標準キューでのみ指定できる
sqs.send_message(QueueUrl=url, MessageBody=body, DelaySeconds=45)
```

- 標準キューでキューの遅延を変えても、**すでに入っているメッセージには効かない**。FIFO では効く。
- FIFO で送信時に `DelaySeconds` を指定することはできない。
- 遅延中のメッセージは受信されないので、`ApproximateNumberOfMessagesDelayed` に数えられる。
- 900 秒（15 分）を超える値はエラーになる。

### バッチ処理 {#batching}

`SendMessageBatch`、`DeleteMessageBatch`、`ChangeMessageVisibilityBatch` で 10 件までまとめて扱える。リクエスト数が減るので、スループットが上がり料金も下がる。

```python
res = sqs.send_message_batch(
    QueueUrl=url,
    Entries=[{"Id": str(i), "MessageBody": body} for i, body in enumerate(bodies[:10])],
)
# 一部だけ失敗することがある
for failed in res.get("Failed", []):
    print("再送が必要", failed["Id"], failed["Code"])
```

バッチ全体が成功とは限らないので、`Failed` を確認する。

- `SendMessageBatch` の合計サイズは 1 MiB まで。
- 各エントリの `Id` はバッチ内で一意にする。80 文字まで、英数字とハイフン、アンダースコアのみ。
- IAM に `SendMessageBatch` という権限はない。`sqs:SendMessage` を与えればバッチにも効く。`DeleteMessageBatch` と `ChangeMessageVisibilityBatch` も同じ。
- FIFO でパーティションを有効に使うには、`SendMessageBatch` で同じグループ ID をまとめる。
- コンソールからバッチ操作はできない。

## SNS {#sns}

トピックに発行すると、購読者全員に **プッシュ** するサービス。1対多の配信に使う。

```python
import boto3

sns = boto3.client("sns")
sns.publish(
    TopicArn="arn:aws:sns:ap-northeast-1:111122223333:orders",
    Message='{"orderId": "1"}',
    MessageAttributes={"event_type": {"DataType": "String", "StringValue": "created"}},
)
```

| 項目 | 内容 |
| --- | --- |
| 購読者 | SQS、Lambda、Data Firehose、HTTP/S、メール、SMS、モバイルプッシュ |
| メッセージサイズ | 既定 256 KiB。`MaximumMessageSize` 属性で 1 MiB まで |
| バッチ | `PublishBatch` で 10 件まで |
| 保持 | しない。届かない場合の再試行のみ |
| リトライ | 配信ポリシーによる。詳しくは[配信の再試行](#sns-retries) |
| 失敗の退避 | サブスクリプションごとの DLQ（SQS。同じアカウントとリージョン） |

### サブスクリプションの種類 {#sns-subscriptions}

| プロトコル | 備考 |
| --- | --- |
| `sqs` | キューのポリシーで SNS に `sqs:SendMessage` を許可する |
| `lambda` | SNS に呼び出しを許可するリソースベースポリシーが要る。非同期で呼ばれる |
| `firehose` | トピック、サブスクリプション所有者ごとに 5 個まで |
| `http`、`https` | 購読の確認が必要。`SubscribeURL` にアクセスするか `ConfirmSubscription` を呼ぶ |
| `email`、`email-json` | 購読の確認が必要。10 件/秒が上限（引き上げ不可） |
| `sms` | 1 回の `Publish` は 1,600 文字まで |
| `application` | モバイルプッシュ |

`Subscribe` の応答は、確認が済むまで `pending confirmation` という文字列になる。ARN を受け取りたいなら `ReturnSubscriptionArn` を true にする。

HTTP/S の購読が保留のままなら、エンドポイントが確認の要求を処理していない。`SubscribeURL` に GET する処理を実装する。

### メッセージのサイズと属性 {#sns-message-attributes}

トピックの `MaximumMessageSize` 属性で、受け付ける最大サイズを決める。

| 項目 | 値 |
| --- | --- |
| 既定 | 262,144 バイト（256 KiB） |
| 範囲 | 1,024〜1,048,576 バイト（1 MiB） |
| 超えたとき | `Publish` が `InvalidParameter` エラー |
| 数えるもの | 本文と属性の合計 |
| 256 KiB を超える設定の条件 | 購読 100 個以下で、すべて SQS、Firehose、Lambda |

つまり、HTTP/S やメールの購読があるトピックは 256 KiB を超えられない。

メッセージ属性は本文とは別のメタデータで、受信側が本文を解析せずに判断したり、フィルターに使ったりする。

| データ型 | 内容 |
| --- | --- |
| `String` | UTF-8 の文字列 |
| `String.Array` | 配列を文字列にしたもの。`["a","b"]` |
| `Number` | 整数か浮動小数点数。±10^9 の範囲で、小数点以下 5 桁 |
| `Binary` | バイナリ。Lambda の購読には `String` として渡される |

属性を送れるのは `MessageStructure` が文字列のときだけで、`json` のときは送られない。

raw 配信の SQS 購読では、属性は 10 個まで。11 個以上のメッセージはクライアント側エラーとして **破棄される**。

### ファンアウト {#fanout}

SNS から複数の SQS キューに配信し、それぞれ独立して処理する。消費者が止まってもメッセージはキューに残る。消費者を増やすときは購読を追加するだけでよい。

- キューの **アクセスポリシー** で、トピックに `sqs:SendMessage` を許可する。
- **raw メッセージ配信** を有効にすると、SNS の JSON で包まれずに本文だけ届く。SQS と HTTP/S、Firehose で使える。
- 無効の場合、SQS の `Body` は SNS の JSON になるので、`Message` を取り出してさらに解析する。

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": { "Service": "sns.amazonaws.com" },
    "Action": "sqs:SendMessage",
    "Resource": "arn:aws:sqs:ap-northeast-1:111122223333:orders-q",
    "Condition": {
      "ArnEquals": { "aws:SourceArn": "arn:aws:sns:ap-northeast-1:111122223333:orders" }
    }
  }]
}
```

`aws:SourceArn` がないと、他のトピックからも送れてしまう。購読は成功しているのにメッセージが届かないときは、このポリシーをまず確認する。キューが KMS で暗号化されているなら、キーポリシーで SNS に `kms:GenerateDataKey` と `kms:Decrypt` も許可する。

### raw メッセージ配信の詳細 {#sns-raw-delivery}

サブスクリプションの `RawMessageDelivery` を `true` にする。

```bash
aws sns set-subscription-attributes \
  --subscription-arn "$SUB_ARN" \
  --attribute-name RawMessageDelivery \
  --attribute-value true
```

| 宛先 | 有効にしたときの動き |
| --- | --- |
| SQS | SNS のメタデータが取り除かれ、本文がそのまま `Body` になる。属性は SQS の属性になる（10 個まで） |
| HTTP/S | 本文が届き、ヘッダー `x-amz-sns-rawdelivery: true` が付く。属性は送られない |
| Firehose | 本文が届く。属性は送られない |

Lambda には raw 配信の設定はない。有効にすると `TopicArn` や `Timestamp` は受け取れなくなるので、必要なら本文に入れる。

### トピックのアクセスポリシーと暗号化 {#sns-access}

トピックのリソースポリシーで、誰が `sns:Publish` できるかを決める。別アカウントや AWS サービス（S3、CloudWatch アラームなど）からの発行にはこの許可が要る。

```json
{
  "Effect": "Allow",
  "Principal": { "Service": "s3.amazonaws.com" },
  "Action": "sns:Publish",
  "Resource": "arn:aws:sns:ap-northeast-1:111122223333:uploads",
  "Condition": { "StringEquals": { "aws:SourceAccount": "111122223333" } }
}
```

SSE は `KmsMasterKeyId` で有効にする。暗号化されるのは本文のみで、件名、属性、メッセージ ID は暗号化されない。AWS サービスから暗号化トピックに発行するなら、キーポリシーを編集できるカスタマーマネージドキーを使う。

### サブスクリプションフィルターポリシー {#filter-policies}

既定では購読者は全メッセージを受け取る。フィルターポリシーを設定すると、必要なものだけ受け取れる。消費者側で捨てるより、処理量と料金を減らせる。

```json
{
  "event_type": ["created", "paid"],
  "price_usd": [{ "numeric": [">=", 100] }],
  "store": [{ "anything-but": "test" }]
}
```

- `FilterPolicyScope` で対象を選ぶ。`MessageAttributes`（既定）か `MessageBody`。
- プロパティの間は AND、値の配列は OR で評価する。
- 発行者は購読者が増えても変更不要で、トピックを分ける必要も減る。

#### FilterPolicyScope

| 値 | 判定の対象 | 注意点 |
| --- | --- | --- |
| `MessageAttributes`（既定） | メッセージ属性 | 属性を付けずに発行すると一致しない。入れ子は不可 |
| `MessageBody` | 本文の JSON | 本文が正しい JSON である前提。入れ子も書ける |

本文でフィルターしているつもりが既定のままだと、属性がないので何も届かない。`aws sns set-subscription-attributes` で `FilterPolicyScope` を `MessageBody` にする。

```json
{ "order": { "status": ["paid"], "total": [{ "numeric": [">=", 1000] }] } }
```

上のポリシーは `MessageBody` のスコープで、`{"order":{"status":"paid","total":1500}}` に一致する。`"total":999` には一致しない。

#### 上限

| 項目 | 値 |
| --- | --- |
| キーの数 | 1 ポリシーに 5 個（入れ子は末端のキーを数える） |
| 値の組み合わせ | 150 まで（各配列の値の数の積） |
| ポリシーのサイズ | 256 KB |
| ポリシーの数 | トピックごとに 200、アカウントごとに 10,000 |
| 反映までの時間 | 最大 15 分 |

組み合わせの例を示す。`a` に 3 個、`b` に 5 個、`c` に 10 個の値なら 3 × 5 × 10 = 150 で上限ちょうど。`c` に 1 つ足すと 165 で超える。

ポリシーを変えた直後は最大 15 分の間、古いポリシーで判定されることがある。

### 配信の再試行 {#sns-retries}

失敗の種類で動きが分かれる。

| 失敗 | 例 | 動き |
| --- | --- | --- |
| クライアント側エラー | 購読先の削除、ポリシーで拒否 | 再試行しない。DLQ がなければ破棄 |
| サーバー側エラー | 宛先の障害、HTTP の 5XX と 429 | 配信ポリシーに従って再試行 |

| 宛先 | 既定の再試行 | 変更 |
| --- | --- | --- |
| SQS、Lambda、Firehose（AWS 管理） | 最大 100,015 回、23 日間 | 不可 |
| SMTP、SMS、モバイルプッシュ | 50 回、6 時間 | 不可 |
| HTTP/S | 既定は 3 回（20 秒間隔、linear） | 配信ポリシーで可 |

Firehose のスロットリングエラーには、顧客管理の宛先と同じポリシーが使われる。

HTTP/S の配信ポリシーはトピックかサブスクリプションに設定する。

```json
{
  "healthyRetryPolicy": {
    "minDelayTarget": 1,
    "maxDelayTarget": 60,
    "numRetries": 50,
    "numNoDelayRetries": 3,
    "numMinDelayRetries": 2,
    "numMaxDelayRetries": 35,
    "backoffFunction": "exponential"
  },
  "throttlePolicy": { "maxReceivesPerSecond": 10 }
}
```

| 項目 | 範囲（既定） |
| --- | --- |
| `numRetries` | 0〜100（3） |
| `minDelayTarget` | 1〜最大遅延、秒（20） |
| `maxDelayTarget` | 最小遅延〜3,600、秒（20） |
| `backoffFunction` | `arithmetic`、`exponential`、`geometric`、`linear`（`linear`） |
| `maxReceivesPerSecond` | 1 以上（制限なし） |

上の例のバックオフの回数は 50 − 3 − 2 − 35 = 10 回。合計の再試行時間は 3,600 秒が上限（引き上げ不可）。

`maxReceivesPerSecond` は平均の目安で、厳密な上限ではない。これを超えた分は再試行を消費せずに待たされるので、発行が速いと遅延が増える。

#### サブスクリプションの DLQ

SQS と違い、SNS の DLQ はトピックではなく **サブスクリプションごと** に設定する。

```json
{ "deadLetterTargetArn": "arn:aws:sqs:ap-northeast-1:111122223333:sns-orders-dlq" }
```

- `RedrivePolicy` 属性に設定する。`maxReceiveCount` はない。
- DLQ は同じアカウントと同じリージョンの SQS。標準トピックには標準キュー、FIFO トピックには FIFO キュー。
- 暗号化した DLQ には、SNS を許可したカスタム KMS キーが要る。
- DLQ がないと、再試行を使い切ったメッセージとクライアント側エラーのメッセージは失われる。
- AWS は DLQ の保持期間を最大の 14 日にすることを勧めている。

### SNS FIFO {#sns-fifo}

| 項目 | 内容 |
| --- | --- |
| 順序 | メッセージグループごとに保証 |
| 重複排除 | 5 分間 |
| 購読者 | SQS の標準または FIFO キュー |
| Lambda への配信 | 直接は不可。SQS を挟む |
| 購読者数 | トピックあたり 100 |
| HTTP/S、メール、SMS | 購読しようとするとエラーになる |
| トピック名 | `.fifo` で終わる |

厳密な順序と重複防止が必要なら、SNS FIFO と SQS FIFO を組み合わせる。

```python
sns.publish(
    TopicArn="arn:aws:sns:ap-northeast-1:111122223333:orders.fifo",
    Message=body,
    MessageGroupId="customer-123",       # FIFO では必須
    MessageDeduplicationId="order-1",    # 内容ベースが無効なら必須
)
```

| 属性 | 内容 |
| --- | --- |
| `ContentBasedDeduplication` | 既定は false。true なら本文の SHA-256 を ID にする。属性は含まれない |
| `FifoThroughputScope` | `Topic`（既定。トピック全体で重複排除し、3,000 件/秒または 20 MB/秒）か `MessageGroup`（グループごとに重複排除し、グループあたり 300 件/秒） |

フィルターポリシーを設定すると、FIFO トピックは「最大1回」の配信になる。フィルターで落とされるメッセージがあるので、そのキューには届かない前提で作る。

標準トピックでも `MessageGroupId` を指定できる。これは SQS 標準キューの購読にだけ転送され、[フェアキュー](#standard-fifo) を有効にする。

## EventBridge {#eventbridge}

イベントをルールに従って振り分けるサービス。AWS のサービス、自前のアプリ、SaaS のイベントを扱える。

[![EventBridge によるイベントルーティング](../assets/diagrams/messaging-eventbridge.png)](../assets/diagrams/messaging-eventbridge.png)

```python
import json

import boto3

events = boto3.client("events")
res = events.put_events(
    Entries=[
        {
            "EventBusName": "orders",
            "Source": "com.example.orders",
            "DetailType": "OrderCreated",
            "Detail": json.dumps({"orderId": "1", "amount": 1200}),
        }
    ]
)
# 一部だけ失敗することがある
if res["FailedEntryCount"] > 0:
    print(res["Entries"])
```

| 項目 | 内容 |
| --- | --- |
| `PutEvents` | 1 回あたり 10 エントリまで、合計 1 MB 未満 |
| 応答 | エントリ単位で成否が返る。`FailedEntryCount` を確認する |
| イベントパターン | 2,048 文字まで（引き上げ可） |
| ルールあたりのターゲット | 5 個 |
| ルール数 | バスごとに既定 300（一部のリージョンは 100） |
| ターゲットの再試行 | 既定で 24 時間、最大 185 回（指数バックオフとジッター） |

!!! note "Custom Event Bus と Classic"
    このページは、ルールとターゲットで動く既定のバスと **Custom Event Bus - Classic** を説明する。新しい **Custom Event Bus** はサブスクライバーを作る方式で、イベントを選んだ期間（1〜365 日）保持する。順序はサブスクライバーの設定、重複排除は発行時の設定で、`PutEvents` は 1 回に 100 エントリまで。両方とも利用できる。

!!! warning "古い教材の 256 KB"
    `PutEvents` のサイズの上限は、リクエスト全体で 1 MB 未満。1 エントリだけならほぼ 1 MB まで使える。古い教材の 256 KB という値は現在のものではない。

### イベントバス {#event-buses}

| バス | 受け取るもの | 備考 |
| --- | --- | --- |
| 既定のバス | AWS サービスのイベント、自分のアプリのイベント | アカウントに最初からある |
| カスタムバス | 自分のアプリ、他アカウントのイベント | アカウントごとに最大 100（引き上げ可）。Classic の場合 |
| パートナーバス | SaaS のイベント | パートナーのイベントソースに関連付ける |

ルールは特定のバスに属し、そのバスのイベントだけを評価する。カスタムバスに送ったのに既定のバスのルールが動かない、という間違いが多い。`PutEvents` で `EventBusName` を省くと既定のバスに入る。

別アカウントからの送信はバスのリソースポリシーで `events:PutEvents` を許可する。

`Detail` は JSON の **文字列** で渡す。オブジェクトのままや不正な JSON は受け付けられない。エントリのエラーは例外ではなく、`Entries` の `ErrorCode` で返る。

### ルールとイベントパターン {#eventbridge-rules}

ルールはイベントとパターンが一致すると、ターゲットに送る。

```json
{
  "source": ["com.example.orders"],
  "detail-type": ["OrderCreated"],
  "detail": {
    "amount": [{ "numeric": [">", 1000] }],
    "region": [{ "prefix": "ap-" }],
    "status": [{ "anything-but": "test" }]
  }
}
```

| 演算 | 書き方 |
| --- | --- |
| 一致 | `"state": ["running"]` |
| 前方一致、後方一致 | `{"prefix": "us-"}`、`{"suffix": ".png"}` |
| 否定 | `{"anything-but": "test"}` |
| 数値 | `{"numeric": [">", 0, "<=", 5]}` |
| 存在 | `{"exists": true}` |
| 大文字小文字を無視 | `{"equals-ignore-case": "alice"}` |

- パターンはコンソールのサンドボックスで試せる。
- 入力トランスフォーマーでターゲットへの入力を整形できる。
- 配信できないイベントはターゲットの **DLQ**（SQS 標準）に送れる。権限不足や宛先がない場合は再試行せず、直接 DLQ に送られる。
- ターゲットが Lambda なら、関数のリソースベースポリシーで `events.amazonaws.com` を許可する。ターゲットに `lambda:InvokeFunction` を持つ実行ロールを設定する方法もあり、その場合リソースベースポリシーは不要。

#### パターンの評価のしかた

- パターンに書いたフィールドだけを見る。書いていないフィールドは無視する。
- パターンに書いたフィールドは、イベントに同じ階層で存在する必要がある。
- 配列の中は OR、フィールドの間は AND。
- 文字列の一致は大文字と小文字を区別する。
- 比較演算子は末端のノードにだけ書ける。例外は `$or` と `anything-but`。

具体例で動きを確認する。

| パターン | 一致する | 一致しない |
| --- | --- | --- |
| `"state": ["running", "stopped"]` | `"running"` | `"Running"`、`"pending"` |
| `"region": [{"prefix": "ap-"}]` | `"ap-northeast-1"` | `"us-east-1"` |
| `"file": [{"suffix": ".png"}]` | `"a/b.png"` | `"a/b.PNG"` |
| `"file": [{"suffix": {"equals-ignore-case": ".png"}}]` | `"a/b.PNG"` | `"a/b.jpg"` |
| `"file": [{"wildcard": "dir/*.png"}]` | `"dir/a.png"` | `"x/a.png"` |
| `"amount": [{"numeric": [">", 0, "<=", 5]}]` | `3`、`5` | `0`、`6`、`"3"` |
| `"status": [{"anything-but": ["test", "dev"]}]` | `"prod"` | `"test"` |
| `"region": [{"anything-but": {"prefix": "us-"}}]` | `"ap-northeast-1"` | `"us-east-1"` |
| `"code": [{"exists": true}]` | `code` がある | `code` がない |
| `"code": [{"exists": false}]` | `code` がない | `code` がある |
| `"name": [""]` | 空文字 | `null`、フィールドなし |
| `"name": [null]` | `null` | 空文字、フィールドなし |

`exists` は末端のノードだけで使える。`"detail": {"exists": true}` のように中間のノードには書けない。空文字、`null`、フィールドなしは別物として扱われる。

別のフィールドとの OR は `$or` で書く。

```json
{
  "detail": {
    "$or": [
      { "amount": [{ "numeric": [">", 10000] }] },
      { "priority": ["high"] }
    ]
  }
}
```

パターンを本番に置く前に、`aws events test-event-pattern` か `TestEventPattern` API で試せる。S3 の ACL 変更で起動する関数が ACL を変えるような再帰のルールは、無限ループと料金の増加を招く。パターンをなるべく細かく書く。

### 入力トランスフォーマー {#input-transformer}

ターゲットに渡す内容を、イベント全体ではなく必要な形に整える。ターゲットには次のどれかを指定する。

| 設定 | 渡す内容 |
| --- | --- |
| なし | イベント全体 |
| `Input` | 固定の JSON |
| `InputPath` | イベントの一部（JSON パス） |
| `InputTransformer` | `InputPathsMap` で取り出し、`InputTemplate` で組み立てる |

```json
{
  "InputPathsMap": {
    "instance": "$.detail.instance-id",
    "state": "$.detail.state"
  },
  "InputTemplate": "{\"id\": <instance>, \"message\": \"<instance> is <state>\", \"rule\": <aws.events.rule-name>}"
}
```

`{"detail":{"instance-id":"i-1","state":"running"}}` に対し、ターゲットは `{"id": "i-1", "message": "i-1 is running", "rule": "..."}` を受け取る。

| 予約済みの変数 | 内容 |
| --- | --- |
| `aws.events.rule-arn` | ルールの ARN |
| `aws.events.rule-name` | ルールの名前 |
| `aws.events.event.ingestion-time` | 受信時刻 |
| `aws.events.event.json` | 元のイベント全体（JSON の値の位置でのみ使える） |

**クォートの扱いが落とし穴**。文字列の値を指す変数は、そのままでも `"<state>"` のように囲んでもよく、実行時に正しい JSON に置き換えられる。一方、**オブジェクトや配列を指す変数はクォートしない**。文章の中に埋め込むときは、文章全体を `"` で囲む。

`aws.events.event.json` も JSON の値の位置でだけ使える。文字列の中には入れられない。DLQ の `ERROR_CODE` の一例に `INVALID_JSON` がある。

### ターゲットの再試行と DLQ {#target-retry-dlq}

ターゲットごとに `RetryPolicy` と `DeadLetterConfig` を設定する。

| 項目 | 既定 | 範囲 |
| --- | --- | --- |
| `MaximumRetryAttempts` | 185 | 0〜185 |
| `MaximumEventAgeInSeconds` | 86,400（24 時間） | 60〜86,400 |

どちらかに達すると再試行をやめる。DLQ がなければイベントは捨てられる。

```bash
aws events put-targets --rule orders-created --targets '[{
  "Id": "notify",
  "Arn": "arn:aws:lambda:ap-northeast-1:111122223333:function:notify",
  "RetryPolicy": { "MaximumRetryAttempts": 10, "MaximumEventAgeInSeconds": 3600 },
  "DeadLetterConfig": { "Arn": "arn:aws:sqs:ap-northeast-1:111122223333:eb-dlq" }
}]'
```

1 時間を過ぎた通知に価値がないなら、上のように縮める。既定のままだと、宛先の障害中に 24 時間前のイベントが届くことがある。

- DLQ は SQS の **標準キュー**。FIFO は使えない。
- DLQ のキューポリシーで EventBridge に `sqs:SendMessage` を許可する。
- 権限不足、リソースなし、DNS の失敗のように再試行しても無駄なエラーは、すぐ DLQ に送られる。DLQ がなければ捨てられる。
- DLQ のメッセージには `RULE_ARN`、`TARGET_ARN`、`ERROR_CODE`、`ERROR_MESSAGE`、`EXHAUSTED_RETRY_CONDITION`、`RETRY_ATTEMPTS` の属性が付く。
- メトリクスは `InvocationsSentToDLQ` と `InvocationsFailedToBeSentToDLQ`。

!!! note "SQS の FIFO や他のターゲット"
    SQS の FIFO キューやフェアキューをターゲットにするなら、`SqsParameters` でメッセージグループを指定する。ルールに書けるターゲットは 5 個で引き上げ不可。もっと広げるなら SNS トピックをターゲットにする。

### スケジュール {#eventbridge-schedule}

定期実行には **EventBridge Scheduler** を使う。従来の「スケジュールされたルール」はレガシーの扱いで、AWS は Scheduler を勧めている。

| 種類 | 書き方 |
| --- | --- |
| 繰り返し（rate） | `rate(5 minutes)` |
| 繰り返し（cron） | `cron(0 9 * * ? *)` |
| 1回のみ | `at(2026-12-01T09:00:00)` |

Scheduler はタイムゾーンを指定でき、柔軟な時間枠を設定できる。

```bash
aws scheduler create-schedule \
  --name daily-report \
  --schedule-expression "cron(0 9 * * ? *)" \
  --schedule-expression-timezone "Asia/Tokyo" \
  --flexible-time-window '{"Mode": "FLEXIBLE", "MaximumWindowInMinutes": 15}' \
  --target '{
    "Arn": "arn:aws:lambda:ap-northeast-1:111122223333:function:report",
    "RoleArn": "arn:aws:iam::111122223333:role/scheduler-invoke",
    "RetryPolicy": {"MaximumRetryAttempts": 3, "MaximumEventAgeInSeconds": 3600},
    "DeadLetterConfig": {"Arn": "arn:aws:sqs:ap-northeast-1:111122223333:sched-dlq"}
  }'
```

| 設定 | 内容 |
| --- | --- |
| `ScheduleExpressionTimezone` | 既定は UTC。`Asia/Tokyo` を付けないと 9 時は日本の 18 時になる |
| `FlexibleTimeWindow` | 必須。`OFF` か `FLEXIBLE`。`FLEXIBLE` には `MaximumWindowInMinutes`（1〜1,440）が要る |
| `StartDate`、`EndDate` | 繰り返しの期間。1回のみのスケジュールでは `EndDate` は無視される |
| `ActionAfterCompletion` | `NONE` か `DELETE`。`DELETE` なら完了後に自動で消える |
| `GroupName` | スケジュールグループ。リージョンに 500 まで |
| `ClientToken` | 作成の冪等性トークン |
| `Target.RoleArn` | 必須。スケジュールがターゲットを呼ぶための実行ロール |
| `RetryPolicy` | 再試行 0〜185 回、60〜86,400 秒 |
| `DeadLetterConfig` | SQS 標準キュー |

cron は 6 項目で、日と曜日の両方に `*` は書けない。片方を `?` にする。`cron(0 9 * * * *)` はエラーになる。

`FLEXIBLE` で 15 分にすると、9:00〜9:15 のどこかで動く。正確な時刻が要らず、呼び出しを分散させたい処理に向く。

ターゲットは2種類ある。**テンプレート化ターゲット** は SQS、Lambda、Step Functions などの一般的な API を簡単に呼ぶもの。**ユニバーサルターゲット** はより広い AWS サービスの API を呼ぶもの。どちらも実行ロールに権限が要る。

スケジュールの数は、既定でリージョンごとに 10,000,000 個。注文ごとの 1 回限りのリマインドのように、多数の個別予約に向く。

### Pipes {#eventbridge-pipes}

1つのソースと1つのターゲットをつなぐ、ポイントツーポイントの統合。バスが多対多のルーティングなのに対し、Pipes は1本の連携を少ないコードで作る。

```mermaid
flowchart TD
    A["ソース: SQS、Kinesis、DynamoDB Streams、MQ、Kafka"] --> B[フィルター: 任意]
    B --> C["エンリッチメント: 任意（Lambda など）"]
    C --> D[ターゲット]
```

ポーリングや変換のための Lambda を書かずに済むのが利点。

| 段階 | 設定と動き |
| --- | --- |
| フィルター | イベントパターンと同じ構文。課金は一致したイベントだけ |
| 入力トランスフォーマー | エンリッチメントとターゲットのそれぞれに指定できる。バッチでは各レコードに適用される |
| バッチ | ソースとターゲットが対応する範囲で。SQS がターゲットなら 10 件まで |
| 部分失敗 | SQS とストリームのソースでは、ターゲットの部分失敗を処理する。エンリッチメントの部分失敗には対応しない |

エンリッチメントやターゲットがバッチに対応しないと、ソースでバッチを有効にできない。

使い分けの例を示す。SQS のメッセージの一部だけを絞り、顧客情報を足してから Step Functions を起動するなら Pipes。1 つのイベントを 3 つのサービスに送るならバスとルールを使う。

### アーカイブとリプレイ {#archive-replay}

バスのイベントをアーカイブに保存し、後で再送できる。障害からの復旧や、新機能の検証に使う。

- パターンで保存するイベントを絞れる。保持期間を設定できる。
- リプレイの送信先は、元のイベントバスのみ。
- 順序は保証されない。発生時刻を基準に 1 分間隔で処理する。
- 受信からアーカイブまで遅延がある。AWS は 10 分待ってからのリプレイを勧めている。
- 再送イベントには `replay-name` が付くので、ルールで区別できる。

| 項目 | 内容 |
| --- | --- |
| 保持期間 | 日数で指定。既定は無期限 |
| 元のバス | 1つ。作成後は変更不可。1つのバスに複数のアーカイブを作れる |
| リプレイの範囲 | 開始時刻と終了時刻で指定 |
| リプレイの宛先 | 全ルールか、選んだルール |
| 件数の表示 | `DescribeArchive` の `EventCount` は最大 24 時間遅れる |
| 暗号化 | 既定は AWS 所有キーで AES-256 |

再送がアーカイブに戻らないよう、EventBridge は `replay-name` を持つイベントを除くマネージドルールを作る。

新しいルールだけに過去の 1 日分を流すなら、リプレイで **そのルールだけ** を選ぶ。全ルールにすると、既存の処理にも同じイベントが再び届き、二重に実行される。

### スキーマレジストリ {#schema-registry}

イベントの構造（スキーマ）を管理する。AWS サービスのイベントのスキーマは最初から用意されている。

- **スキーマ検出** でバス上のイベントから自動生成できる。
- OpenAPI 3 と JSONSchema Draft4 に対応する。
- 各言語の **コードバインディング** をダウンロードし、型付きで扱える。
- 入力トランスフォーマーを使っていても、検出の対象は変換前の元のイベントになる。
- IDE では AWS Toolkit から検索とダウンロードができる。

## S3 イベント通知 {#s3-events}

オブジェクトの作成や削除で処理を起動する。

| 送信先 | 備考 |
| --- | --- |
| Lambda | 非同期で呼ばれる。S3 に呼び出しを許可するリソースベースポリシーが要る |
| SQS | 標準キューのみ。FIFO は直接送れない |
| SNS | 複数の宛先へ広げたいとき |
| EventBridge | バケットで有効にすると全イベントが届く。ルールで絞る |

```python
import urllib.parse


def handler(event, context):
    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        # キーは URL エンコードされている。red flower.jpg は red+flower.jpg になる
        key = urllib.parse.unquote_plus(record["s3"]["object"]["key"])
        print(bucket, key)
```

- 配信は少なくとも1回。通常は数秒で届くが、1 分以上かかることもある。
- プレフィックスとサフィックスでフィルターできる。ワイルドカードは使えない。
- 順序の判断には `sequencer` を使う。
- トリガーのバケットに書き込むと無限ループになる。別のバケットかプレフィックスに書く。
- SQS FIFO に送りたいときは EventBridge を経由する。

S3 自体の機能は [S3](s3.md) を参照する。

## 選び方 {#how-to-choose}

| | SQS | SNS | EventBridge |
| --- | --- | --- | --- |
| モデル | キュー（プル） | パブリッシュ/サブスクライブ（プッシュ） | イベントルーター（プッシュ） |
| 主な目的 | バッファ、負荷の平準化 | 高速な1対多の配信 | 内容ベースのルーティング |
| 保持 | 最大 14 日 | なし | アーカイブ機能あり |
| フィルター | なし | フィルターポリシー | イベントパターン |
| 消費者 | 通常1種類 | 多数 | ルールごとに最大 5 ターゲット |
| 順序 | FIFO | FIFO | Classic のルールでは保証なし |
| 連携 | AWS SDK | SMS、メール、モバイル、HTTP | SaaS、AWS のサービスイベント、スケジュール |

```mermaid
flowchart TD
    A[何をしたいか] --> B{消費者は複数か}
    B -- いいえ --> C{負荷の平準化や再試行が必要か}
    C -- はい --> D[SQS]
    C -- いいえ --> E[直接呼び出しで十分か検討]
    B -- はい --> F{内容によるルーティングや SaaS 連携が必要か}
    F -- はい --> G[EventBridge]
    F -- いいえ --> H{消費者ごとにバッファが必要か}
    H -- はい --> I[SNS + SQS のファンアウト]
    H -- いいえ --> J[SNS]
```

## メッセージングの最適化 {#optimization}

| 目的 | 方法 |
| --- | --- |
| API コールと料金を減らす | ロングポーリング、バッチ API |
| 無駄な処理を減らす | SNS フィルターポリシー、EventBridge パターン |
| 負荷の差を吸収 | SNS + SQS のファンアウト。消費者ごとに速度を変えられる |
| 処理の重複を防ぐ | 可視性タイムアウトの調整、[冪等な処理](sdk-resilience.md) |
| 失敗で詰まらないようにする | DLQ と `maxReceiveCount` |
| 消費者を自動で増やす | SQS の滞留をメトリクスにして EC2 や ECS をスケール |
| Lambda の処理量を調整 | `BatchSize`、バッチウィンドウ、[部分バッチレスポンス](lambda.md) |

## 既定値と上限のまとめ {#numbers}

| サービス | 項目 | 値 |
| --- | --- | --- |
| SQS | 可視性タイムアウト | 既定 30 秒、0 秒〜12 時間 |
| SQS | 保持期間 | 既定 4 日、60 秒〜14 日 |
| SQS | 遅延（キュー、メッセージ） | 既定 0、最大 15 分 |
| SQS | `WaitTimeSeconds` | 既定 0、最大 20 秒 |
| SQS | `MaxNumberOfMessages` | 既定 1、最大 10 |
| SQS | メッセージサイズ | 既定かつ最大 1 MiB。Extended Client で 2 GB |
| SQS | バッチ | 10 件、合計 1 MiB |
| SQS | メッセージ属性 | 10 個 |
| SQS | 処理中メッセージ | 標準は約 120,000、FIFO は 120,000 |
| SQS | FIFO の重複排除 | 5 分 |
| SQS | FIFO のスループット | 300 回/秒、バッチで 3,000 件/秒（パーティションあたり） |
| SQS | `maxReceiveCount` | API の既定 10。Lambda は 5 以上を推奨 |
| SQS | `sourceQueueArns` | 10 個 |
| SQS | データキーの再利用 | 既定 300 秒、60〜86,400 秒 |
| Lambda と SQS | 可視性タイムアウト | 関数のタイムアウトの 6 倍 + バッチウィンドウ |
| Lambda と SQS | `BatchSize` | 既定 10、標準は最大 10,000、FIFO は最大 10 |
| Lambda と SQS | `MaximumConcurrency` | 2〜1,000 |
| SNS | メッセージサイズ | 既定 256 KiB、最大 1 MiB |
| SNS | `PublishBatch` | 10 件 |
| SNS | フィルターポリシー | キー 5 個、組み合わせ 150、256 KB |
| SNS | ポリシーの数 | トピックごとに 200、アカウントごとに 10,000 |
| SNS | ポリシーの反映 | 最大 15 分 |
| SNS | 再試行（AWS 管理の宛先） | 100,015 回、23 日 |
| SNS | 再試行（SMTP、SMS、プッシュ） | 50 回、6 時間 |
| SNS | HTTP/S の再試行 | 既定 3 回、`numRetries` 最大 100、合計 3,600 秒 |
| SNS | 購読者数 | 標準 12,500,000、FIFO 100 |
| SNS | FIFO のスループット | 既定 3,000 件/秒または 20 MB/秒 |
| EventBridge | `PutEvents` | 10 エントリ、合計 1 MB 未満 |
| EventBridge | イベントパターン | 2,048 文字（引き上げ可） |
| EventBridge | ルールあたりのターゲット | 5 個（引き上げ不可） |
| EventBridge | ルール数 | バスごとに 300（一部のリージョンは 100） |
| EventBridge | Classic のカスタムバス | 100 個（引き上げ可） |
| EventBridge | ターゲットの再試行 | 既定 185 回、24 時間。0〜185 回、60〜86,400 秒 |
| EventBridge | アーカイブの保持 | 既定は無期限 |
| EventBridge | リプレイ前の待ち時間 | 10 分を推奨 |
| Scheduler | 再試行 | 0〜185 回、60〜86,400 秒 |
| Scheduler | 柔軟な時間枠 | 1〜1,440 分 |
| Scheduler | スケジュール数 | リージョンごとに 10,000,000 |
| Scheduler | スケジュールグループ | 500 |

## 試験のポイント {#exam-points}

| こう問われたら | 答え |
| --- | --- |
| 関数のタイムアウトが 60 秒のときの可視性タイムアウト | 6 倍の 360 秒以上 |
| キューにメッセージがあるのに受信が空で返る | ショートポーリング。ロングポーリングにする |
| 受信で `OverLimit` | 処理中が上限。削除を確認する |
| 内容ベース重複排除で別のメッセージが消える | 属性はハッシュに含まれない。ID を明示する |
| DLQ のメッセージが予定より早く消える | 標準キューは元の送信時刻のまま。DLQ の保持期間を長くする |
| この DLQ を特定のキューだけに使わせたい | `RedriveAllowPolicy` の `byQueue` |
| SNS の配信先がすべて失敗すると消える | サブスクリプションの DLQ |
| HTTP エンドポイントが過負荷になる | 配信ポリシーの `maxReceivesPerSecond` |
| 本文の内容で SNS をフィルター | `FilterPolicyScope` を `MessageBody` に |
| フィルターの変更がすぐ効かない | 反映に最大 15 分 |
| EventBridge の再試行を短くしたい | ターゲットの `RetryPolicy` |
| 配信できなかったイベントの原因を調べる | ターゲットの DLQ と `ERROR_CODE` 属性 |
| ターゲットに必要な項目だけ渡す | 入力トランスフォーマー |
| 日本時間の 9 時に実行 | Scheduler の `ScheduleExpressionTimezone` |
| 1 回限りの予約を完了後に消す | Scheduler の `ActionAfterCompletion` を `DELETE` |
| サービスを疎結合にして障害の影響を分ける | SQS を間に挟む |
| 同じメッセージが2回処理される | 可視性タイムアウトを延ばす、処理を冪等に |
| 処理が長引くメッセージ | `ChangeMessageVisibility` で延長 |
| 空の応答とコストを減らす | ロングポーリング（`WaitTimeSeconds` 最大 20） |
| 順序と重複防止が必須 | FIFO キュー、`MessageGroupId`、`MessageDeduplicationId` |
| FIFO のスループットを上げたい | グループ ID を増やす、バッチ、高スループットモード |
| 何度も失敗するメッセージを分離 | DLQ と `maxReceiveCount` |
| 15 分以内の配信遅延 | 遅延キューまたはメッセージタイマー |
| 15 分を超える予約 | EventBridge Scheduler |
| 1 MiB を超えるメッセージ | S3 に保存して参照を送る（Extended Client） |
| 1 つのイベントを複数の処理へ | SNS + SQS のファンアウト |
| 購読者ごとに一部のメッセージだけ受信 | SNS のフィルターポリシー |
| キューに SNS が配信できない | キューのアクセスポリシーで `sqs:SendMessage` を許可 |
| SNS の JSON で包まれずに受け取りたい | raw メッセージ配信 |
| SaaS のイベントや AWS の状態変化で起動 | EventBridge |
| イベントを再処理したい | EventBridge のアーカイブとリプレイ |
| SQS から加工して別サービスへ、コードは書きたくない | EventBridge Pipes |
| イベントの型をコードで使いたい | スキーマレジストリとコードバインディング |
| S3 のイベントを SQS FIFO へ | EventBridge を経由 |
| S3 トリガーで関数が止まらない | 同じバケットへの書き込みによるループ |

## 関連ページ {#related}

- [Lambda](lambda.md)
- [Step Functions](step-functions.md)
- [ストリーミング](streaming.md)
- [SDK と耐障害性](sdk-resilience.md)
- [S3](s3.md)
- [オブザーバビリティ](observability.md)

## 参考 {#references}

- [SQS SetQueueAttributes](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_SetQueueAttributes.html)
- [SQS ChangeMessageVisibility](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_ChangeMessageVisibility.html)
- [SQS DLQ redrive](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-configure-dead-letter-queue-redrive.html)
- [SQS encryption at rest](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-server-side-encryption.html)
- [SQS key management](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-key-management.html)
- [SQS Extended Client for Python](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/extended-client-library-python.html)
- [Configuring an SQS event source for Lambda](https://docs.aws.amazon.com/lambda/latest/dg/services-sqs-configure.html)
- [SNS large message payloads](https://docs.aws.amazon.com/sns/latest/dg/large-message-payloads.html)
- [SNS message attributes](https://docs.aws.amazon.com/sns/latest/dg/sns-message-attributes.html)
- [SNS filter policy constraints](https://docs.aws.amazon.com/sns/latest/dg/subscription-filter-policy-constraints.html)
- [SNS FIFO deduplication](https://docs.aws.amazon.com/sns/latest/dg/fifo-message-dedup.html)
- [SNS SetTopicAttributes](https://docs.aws.amazon.com/sns/latest/api/API_SetTopicAttributes.html)
- [EventBridge comparison operators](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-create-pattern-operators.html)
- [EventBridge input transformation](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-transform-target-input.html)
- [EventBridge RetryPolicy](https://docs.aws.amazon.com/eventbridge/latest/APIReference/API_RetryPolicy.html)
- [EventBridge Scheduler schedule types](https://docs.aws.amazon.com/scheduler/latest/UserGuide/schedule-types.html)
- [EventBridge Scheduler CreateSchedule](https://docs.aws.amazon.com/scheduler/latest/APIReference/API_CreateSchedule.html)
- [EventBridge Pipes batching](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-batching-concurrency.html)
- [SQS message quotas](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/quotas-messages.html)
- [SQS queue types](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-queue-types.html)
- [SQS FIFO exactly-once processing](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues-exactly-once-processing.html)
- [High throughput for FIFO queues](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/high-throughput-fifo.html)
- [SQS fair queues](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-fair-queues.html)
- [SQS visibility timeout](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html)
- [SQS short and long polling](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-short-and-long-polling.html)
- [SQS dead-letter queues](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html)
- [SQS delay queues](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-delay-queues.html)
- [SQS message timers](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-message-timers.html)
- [SQS batch actions](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-batch-api-actions.html)
- [SNS endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/sns.html)
- [SNS message filtering](https://docs.aws.amazon.com/sns/latest/dg/sns-message-filtering.html)
- [SNS subscription filter policies](https://docs.aws.amazon.com/sns/latest/dg/sns-subscription-filter-policies.html)
- [SNS FIFO message delivery](https://docs.aws.amazon.com/sns/latest/dg/fifo-message-delivery.html)
- [SNS message delivery retries](https://docs.aws.amazon.com/sns/latest/dg/sns-message-delivery-retries.html)
- [SNS dead-letter queues](https://docs.aws.amazon.com/sns/latest/dg/sns-dead-letter-queues.html)
- [SNS raw message delivery](https://docs.aws.amazon.com/sns/latest/dg/sns-large-payload-raw-message-delivery.html)
- [EventBridge rules](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-rules.html)
- [EventBridge event patterns](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-event-patterns.html)
- [EventBridge retries](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-rule-retry-policy.html)
- [EventBridge dead-letter queues](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-rule-dlq.html)
- [EventBridge PutEvents](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-putevents.html)
- [EventBridge Scheduler](https://docs.aws.amazon.com/eventbridge/latest/userguide/using-eventbridge-scheduler.html)
- [EventBridge Pipes](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes.html)
- [EventBridge archive and replay](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-archive.html)
- [EventBridge schema registry](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-schema.html)
- [EventBridge quotas](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-quota.html)
- [EventBridge Custom Event Bus](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-custom-bus.html)
- [S3 Event Notifications](https://docs.aws.amazon.com/AmazonS3/latest/userguide/EventNotifications.html)
- [S3 events with EventBridge](https://docs.aws.amazon.com/AmazonS3/latest/userguide/EventBridge.html)
- [S3 event message structure](https://docs.aws.amazon.com/AmazonS3/latest/userguide/notification-content-structure.html)
