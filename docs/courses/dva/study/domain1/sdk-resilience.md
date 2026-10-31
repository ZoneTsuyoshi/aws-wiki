# 分野1: SDK と耐障害性

分野1では、SDK を使ったコードの書き方と、失敗しても動き続ける設計を問われます。再試行、タイムアウト、冪等性は多くのサービスの問題の前提になるので、まとめて押さえます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.1.3](../../domain1.md#skill-1-1-3) | 再試行、バックオフ、グレースフルデグラデーション |
| [1.1.5](../../domain1.md#skill-1-1-5) | API と SDK を使ったコード |
| [1.1.7](../../domain1.md#skill-1-1-7) | シリアライズとデシリアライズ |

## 学習の順番 {#study-order}

1. [認証情報](../../../../services/sdk-resilience.md#credentials)、[クライアントの設定と優先順位](../../../../services/sdk-resilience.md#client-config): SDK が認証情報と設定を探す順番を覚えます。
2. [コードでのエラー処理](../../../../services/sdk-resilience.md#error-handling)、[接続の再利用](../../../../services/sdk-resilience.md#connection-reuse): `ClientError` の見方と、Lambda でクライアントを作る場所を確認します。
3. [ページネーション](../../../../services/sdk-resilience.md#pagination)、[ウェイター](../../../../services/sdk-resilience.md#waiters)、[部分的な失敗](../../../../services/sdk-resilience.md#partial-failures): 全件取得、完了待ち、バッチ API の確認項目を覚えます。
4. [リトライ](../../../../services/sdk-resilience.md#retries)、[指数バックオフとジッター](../../../../services/sdk-resilience.md#backoff-jitter): 再試行してよいエラーと、ジッターが必要な理由を理解します。
5. [SDK の再試行モード](../../../../services/sdk-resilience.md#retry-modes): 3つのモードと、`max_attempts` の数え方の違いを押さえます。
6. [タイムアウト](../../../../services/sdk-resilience.md#timeouts)、[冪等性](../../../../services/sdk-resilience.md#idempotency): タイムアウトの順序と計算、再試行を安全にする方法を学びます。
7. [サーキットブレーカー](../../../../services/sdk-resilience.md#circuit-breaker)、[グレースフルデグラデーション](../../../../services/sdk-resilience.md#graceful-degradation)、[サードパーティ連携の耐障害性](../../../../services/sdk-resilience.md#third-party): 長引く障害への対策を整理します。
8. [JSON の落とし穴](../../../../services/sdk-resilience.md#json-pitfalls)、[サービスごとの形式](../../../../services/sdk-resilience.md#service-formats)、[DynamoDB のシリアライズ](../../../../services/sdk-resilience.md#dynamodb-serialization): 型のエラーと、サービスごとの形式を覚えます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| boto3 の既定の再試行モード | `legacy`、総数 5 回 | |
| `standard` | 総数 3 回 | ほとんどの場合はこれを使います |
| `AWS_MAX_ATTEMPTS`、設定ファイルの `max_attempts` | 総数 | 3 なら最大 3 回呼びます |
| boto3 の `Config` の `max_attempts` | 再試行の回数 | 3 なら最大 4 回呼びます |
| `connect_timeout`、`read_timeout` | それぞれ 60 秒 | 短い API には長すぎます |
| `max_pool_connections` | 10 | `Connection pool is full` なら増やします |
| `table_exists` ウェイター | 20 秒間隔で 25 回 | Lambda ではタイムアウトが先に来ます |
| DynamoDB の `ClientRequestToken` | 完了から 10 分有効 | |
| DynamoDB の数値 | 38 桁まで | |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| スロットリング（429）が出る | 指数バックオフとジッターで再試行します |
| 再試行の設定を最小のコードで済ませる | SDK の `retries` を `standard` にします |
| 同じテーブルの大量書き込みでスロットリングが続く | `adaptive` モードか、キューで流量を調整します |
| Lambda の `Task timed out` で例外処理が動かない | SDK のタイムアウトを関数より短くします。接続 1 秒、読み取り 2 秒、総数 3 回なら最悪 9 秒とバックオフです |
| 外部 API の障害が長引く | サーキットブレーカーで呼び出しを止めます |
| おすすめ API が止まっても主要機能を動かす | 固定の人気商品を表示するなどして機能を縮小します |
| 外部 API の二重課金を防ぐ | 冪等性キーをリクエストに付けます |
| `BatchWriteItem` で一部が書かれない | `UnprocessedItems` をバックオフしながら再送します |
| `float` を DynamoDB に保存できない | `Decimal(str(value))` にします |
| DynamoDB Streams のイメージを Python の値にする | `TypeDeserializer` を使います |

## 引っかかりやすい点 {#traps}

- `ClientError` が届いた時点で SDK の再試行は終わっています。ここで同じ回数を再試行すると、回数が掛け算になります。
- HTTP ステータスだけで再試行を判断しません。`ProvisionedThroughputExceededException` は 400 ですが再試行します。`ValidationException` も 400 ですが再試行しません。
- バッチ API の部分的な失敗は例外になりません。応答を確認しないと黙って失われます。
- `list_objects_v2` を 1 回だけ呼ぶと、以降のオブジェクトをエラーなしで取りこぼします。ページネーターを使います。
- `PageSize` は 1 ページの件数で、全体の件数は変わりません。全体を制限するのは `MaxItems` です。
- SNS 経由の SQS は JSON が二重になります。EventBridge の `Detail` は `json.dumps` が必要で、S3 イベントのキーは `unquote_plus` でデコードします。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [sdk-resilience 問1](../../exercises/sdk-resilience.md#q1) | 1.1.3 | ある開発者は boto3 で次の設定を書きました。一時的なエラーが続いた場合、1 回の API 呼び… |
| [sdk-resilience 問2](../../exercises/sdk-resilience.md#q2) | 1.1.5 | 開発者が Lambda の環境変数に AWS_RETRY_MODE=adaptive を設定し、~/… |
| [sdk-resilience 問3](../../exercises/sdk-resilience.md#q3) | 1.1.3 | 1 つの DynamoDB テーブルに大量に書き込むバッチ処理で、スロットリングが頻発しています。追… |
| [sdk-resilience 問4](../../exercises/sdk-resilience.md#q4) | 1.1.3 | API Gateway の背後にある Lambda 関数（タイムアウト 10 秒）が、遅い下流サービ… |
| [sdk-resilience 問5](../../exercises/sdk-resilience.md#q5) | 1.1.3 | 次のエラーのうち、AWS SDK の再試行の対象になるものはどれですか。（2つ選択） |
| [sdk-resilience 問6](../../exercises/sdk-resilience.md#q6) | 1.1.3 | 多数のクライアントが同じサービスを呼んでいます。サービスの一時的な障害の後、すべてのクライアントが同… |
| [sdk-resilience 問9](../../exercises/sdk-resilience.md#q9) | 1.1.5 | list_objects_v2 を 1 回だけ呼ぶコードで、バケットのオブジェクトを処理しています。… |
| [sdk-resilience 問10](../../exercises/sdk-resilience.md#q10) | 1.1.5 | dynamodb.get_waiter("table_exists").wait(TableName… |
| [sdk-resilience 問11](../../exercises/sdk-resilience.md#q11) | 1.1.3 | 注文の支払いを DynamoDB の TransactWriteItems で書き込みます。アプリケ… |
| [sdk-resilience 問12](../../exercises/sdk-resilience.md#q12) | 1.1.3 | Step Functions の Standard ワークフローで、同じ注文の処理を二重に始めないよ… |
| [sdk-resilience 問13](../../exercises/sdk-resilience.md#q13) | 1.1.7 | boto3 の Table.put_item で次のコードを実行するとエラーになります。原因と修正の… |
| [sdk-resilience 問14](../../exercises/sdk-resilience.md#q14) | 1.1.3 | DynamoDB の PutItem で HTTP 500 が返りました。SDK の再試行を使い切っ… |

<!-- questions:end -->
