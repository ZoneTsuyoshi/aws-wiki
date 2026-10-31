# 分野4: API Gateway

エラーコードの切り分け、ログとメトリクスの読み方、キャッシュの設定が問われます。API の作り方は[分野1](../domain1/api-gateway.md)、認可は[分野2](../domain2/api-gateway.md)、ステージやデプロイは[分野3](../domain3/api-gateway.md)で扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.1.1](../../domain4.md#skill-4-1-1) | エラーコードからの切り分け |
| [4.1.2](../../domain4.md#skill-4-1-2) | メトリクスとログの読み取り |
| [4.2.1](../../domain4.md#skill-4-2-1) | 実行ログとアクセスログ |
| [4.2.4](../../domain4.md#skill-4-2-4) | ステージでの X-Ray の有効化 |
| [4.3.4](../../domain4.md#skill-4-3-4) | ステージのキャッシュ |
| [4.3.5](../../domain4.md#skill-4-3-5) | 遅延の原因の特定 |

## 学習の順番 {#study-order}

1. [エラーコード](../../../../services/api-gateway.md#errors): 500、502、504 と、4XX の原因を分けて覚えます。
2. [スロットリングの階層](../../../../services/api-gateway.md#throttling): 429 の出どころと、トークンバケットの動きを理解します。
3. [ログとメトリクス](../../../../services/api-gateway.md#logging-metrics): ログの種類、有効化の準備、`Latency` の読み方を学びます。
4. [既定メトリクス](../../../../services/observability.md#apigw-metrics): 統計の選び方と、詳細メトリクスの条件を確認します。
5. [キャッシュ](../../../../services/api-gateway.md#caching): 有効化の 2 段階と、TTL の値を押さえます。
6. [キャッシュキー](../../../../services/api-gateway.md#cache-keys)と[無効化](../../../../services/api-gateway.md#cache-invalidation): 応答を変えるパラメーターと、無効化の権限を確認します。
7. [X-Ray の有効化](../../../../services/observability.md#xray-apigateway): ステージでの設定とサンプリングルールを確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| アカウントのスロットリング | 10,000 リクエスト/秒、バースト 5,000 | 一部のリージョンは 2,500 と 1,250 です |
| キャッシュの TTL | 既定 300 秒、最大 3,600 秒、0 で無効 | メソッドごとに上書きできます |
| キャッシュ可能な応答 | 1,048,576 バイトまで | 超える応答はキャッシュされません |
| キャッシュの既定の対象 | `GET` のみ | `POST` はメソッドの設定で上書きします |
| 統合タイムアウト | REST API は最大 29 秒、HTTP API は最大 30 秒 | リージョンとプライベートの REST API は引き上げられます |
| ペイロード | 10 MB | 超えると 413 です |
| アクセスログの形式 | 3 KB まで | `$context` 変数で書きます |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 502 が返る | 関数のエラーか応答形式の誤りです。Lambda のログを確認し、`statusCode` と文字列の `body` を返します |
| 504 が返る | 統合のタイムアウトです。処理を短くするか、受付だけして SQS や Step Functions に渡します |
| 500 が返る | 設定の問題です。オーソライザー、権限、マッピングを確認します |
| 存在するはずの URL で `Missing Authentication Token` の 403 になる | URL、ステージ、メソッドを確認します |
| 429 が返る | `THROTTLED` はバックオフと制限の見直し、`QUOTA_EXCEEDED` は使用量プランの見直しです |
| `Latency` と `IntegrationLatency` がほぼ同じ | 遅いのはバックエンドです |
| `Latency` が 2,000 ms で `IntegrationLatency` が 100 ms | API Gateway 側を調べます。オーソライザーの実行時間などです |
| CloudWatch にログが出ない | `cloudWatchRoleArn` をリージョンごとに設定し、`loggingLevel` を `ERROR` か `INFO` にします |
| ヘッダーで応答が変わるのに同じキャッシュが返る | `Accept-Language` などをキャッシュキーに追加します |
| 誰でもキャッシュを無効化できてしまう | Require authorization を有効にし、`execute-api:InvalidateCache` を許可したクライアントに限定します |

## 引っかかりやすい点 {#traps}

- **キャッシュを作ったのに効かない:** **Provision API cache** だけでは使われません。メソッドレベルの設定で対象を選びます。
- **キャッシュの確認方法を誤る:** `X-Cache` ヘッダーではなく、`CacheHitCount`、`CacheMissCount`、応答のタイムスタンプで確認します。
- **他人の応答が返る:** ユーザーごとに違う応答なのに、ユーザーを区別する値をキーに含めていません。
- **メソッド単位のメトリクスが見えない:** 詳細メトリクス（`metricsEnabled`）を有効にしないと送られません。
- **ログに機密情報が残る:** `dataTraceEnabled` は本文まで記録します。本番では使いません。
- **`Count` の見方を誤る:** リクエスト数は `SampleCount` で見ます。`4XXError` と `5XXError` は `Average` がエラー率です。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [api-gateway 問9](../../exercises/api-gateway.md#q9) | 4.1.1 | REST API に使用量プランと API キーを設定しました。次のリクエストに対するステータスコー… |
| [api-gateway 問11](../../exercises/api-gateway.md#q11) | 4.1.2 | API の Latency が 2,000 ms で、IntegrationLatency が 10… |
| [api-gateway 問12](../../exercises/api-gateway.md#q12) | 4.3.4 | REST API のステージでキャッシュを有効にしました。GET は速くなりましたが、検索用の PO… |
| [api-gateway 問13](../../exercises/api-gateway.md#q13) | 4.3.4 | REST API のキャッシュで、Cache-Control: max-age=0 を送れるのは特定… |
| [api-gateway 問18](../../exercises/api-gateway.md#q18) | 4.1.2 | 新しいリージョンの REST API で、ステージの実行ログを INFO にしましたが、CloudW… |

<!-- questions:end -->
