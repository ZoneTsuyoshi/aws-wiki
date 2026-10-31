# 分野4: Lambda

同時実行とメモリの調整、スロットリングや障害の調べ方が問われます。関数を作る側の話は[分野1](../domain1/lambda.md)、デプロイやテストは[分野3](../domain3/lambda.md)で扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.1.1](../../domain4.md#skill-4-1-1) | コードとサービス連携のデバッグ |
| [4.1.2](../../domain4.md#skill-4-1-2) | メトリクス、ログ、トレースの読み取り |
| [4.2.1](../../domain4.md#skill-4-2-1) | ログの形式とレベルの設定 |
| [4.2.4](../../domain4.md#skill-4-2-4) | アクティブトレース |
| [4.3.1](../../domain4.md#skill-4-3-1) | 同時実行、接続の管理 |
| [4.3.2](../../domain4.md#skill-4-3-2) | メモリとコンピューティング能力 |
| [4.3.5](../../domain4.md#skill-4-3-5) | ボトルネックの検出 |

## 学習の順番 {#study-order}

1. [同時実行とスケーリング](../../../../services/lambda.md#concurrency): 同時実行数の見積もりの式と、上限の値を覚えます。
2. [予約済みと Provisioned の違い](../../../../services/lambda.md#reserved-provisioned): 目的、料金、超過時の動きを比べます。
3. [スロットリング](../../../../services/lambda.md#throttling)と[リクエスト数の上限](../../../../services/lambda.md#concurrency-rps): 呼び出し方ごとの動きと、429 の原因を確認します。
4. [メモリと CPU の最適化](../../../../services/lambda.md#memory-tuning)と[コールドスタート](../../../../services/lambda.md#cold-start): 計測の手順と、起動を速くする方法を学びます。
5. [スレッドとコネクションプール](../../../../services/lambda.md#connection-pooling)と[コードの最適化](../../../../services/lambda.md#code-optimization): 接続を再利用する書き方を確認します。
6. [Lambda の既定メトリクス](../../../../services/observability.md#lambda-metrics): メトリクスと統計の組み合わせを読めるようにします。
7. [ログ設定](../../../../services/lambda.md#logging-config)と[トレーシング](../../../../services/lambda.md#tracing): ログレベルが効く条件と、トレースの有効化を押さえます。
8. [コードの欠陥を特定する](../../../../services/observability.md#debug-code)と [Logs Insights](../../../../services/observability.md#logs-insights): エラーの調べ方と `REPORT` 行の集計を学びます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| 同時実行数の見積もり | 平均リクエスト数/秒 × 平均実行時間（秒） | 100 リクエスト/秒、0.5 秒なら 50 です |
| アカウントの同時実行数 | リージョンごとに既定 1,000 | 引き上げられます。新しいアカウントはもっと低いことがあります |
| 予約できない枠 | 100 | 未予約から 100 を引いた分まで予約できます |
| スケーリング速度 | 関数ごとに 10 秒あたり 1,000 環境 | 超えた分はスロットリングされることがあります |
| リクエスト数の上限 | 同時実行数の 10 倍/秒 | 短い関数では、こちらが先に上限になります |
| メモリ | 128〜10,240 MB、既定 128 MB | 1,769 MB で 1 vCPU 相当です |
| タイムアウト | 既定 3 秒、最大 900 秒 | 超えると `Task timed out` がログに残ります |
| Provisioned のターゲット追跡 | 使用率 10〜90% | 反映には 1〜2 分かかります |
| `MaximumConcurrency` | 2〜1,000 | SQS のマッピング専用です |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| コールドスタートをなくしたい | Provisioned Concurrency をバージョンかエイリアスに設定し、呼び出し元もそこを指すようにします |
| 毎日決まった時刻にピークが来る | Provisioned Concurrency をスケジュールで調整します。時刻が読めないなら、使用率のターゲット追跡です |
| Java などの起動を低コストで速くしたい | SnapStart を `ApplyOn=PublishedVersions` で有効にし、発行済みのバージョンを呼びます |
| 接続数 50 の DB を関数の増加から守りたい | 予約済み同時実行を 50 にします。51 件目以降は、同期呼び出しなら 429 になります |
| 関数を緊急停止したい | 予約済み同時実行を 0 にします |
| 平均 20 ms の関数が 30,000 リクエスト/秒で 429 になる | 同時実行数は 600 でも、リクエスト数の上限に当たっています。上限を 3,000 以上に引き上げます |
| 低優先度のキューに同時実行を奪われたくない | そのマッピングの `MaximumConcurrency` を 10 などに制限します |
| CPU が足りず処理が遅い | メモリを増やします。実行時間が縮めば、料金が下がる場合もあります |
| メモリを余分に割り当てていないか調べたい | `REPORT` 行の `Max Memory Used` を確認し、AWS Lambda Power Tuning で料金と速度を比べます |
| 同時実行が増えると RDS の接続が枯渇する | 接続をハンドラーの外で作って再利用し、[RDS Proxy](databases.md) を間に置きます |

## 引っかかりやすい点 {#traps}

- **Provisioned を設定したのにコールドスタートが残る:** 呼び出し元やイベントソースが `$LATEST` や別のエイリアスを指しています。
- **ほかの関数がスロットリングされる:** 予約を大きく取りすぎています。使わない予約分も、他の関数には回りません。
- **`logger.info()` がログに出ない:** Python の `Text` 形式では既定のログレベルが `WARN` です。ログレベルのフィルターも JSON 形式でしか効きません。
- **上流にトレースがあるのに関数のトレースが出ない:** `PassThrough` はトレースを送りません。`TracingConfig` を `Active` にします。
- **同期呼び出しが 200 なのに失敗している:** 関数内のエラーでも HTTP ステータスは 200 です。レスポンスの `FunctionError` を確認します。
- **関数のタイムアウトを伸ばしても 504 が返る:** REST API の統合タイムアウトが 29 秒なら、クライアントには 29 秒で 504 が返ります。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [lambda 問5](../../exercises/lambda.md#q5) | 4.3.1 | 20 シャードの Kinesis ストリームを読むマッピングで、ParallelizationFac… |
| [lambda 問9](../../exercises/lambda.md#q9) | 4.3.1 | 1 つの関数に 2 つの SQS キューをつないでいます。低優先度のキューにメッセージが溜まると、重… |
| [lambda 問11](../../exercises/lambda.md#q11) | 4.3.1 | 開発者は prod エイリアスに Provisioned Concurrency を 100 設定し… |
| [lambda 問12](../../exercises/lambda.md#q12) | 4.3.1 | 平均実行時間が 20 ms の関数に、ピーク時に 30,000 リクエスト/秒が届きます。アカウント… |
| [lambda 問15](../../exercises/lambda.md#q15) | 4.3.2 | ハンドラーの外で大きなモデルを読み込む関数があります。オンデマンドの実行環境で、初期化に 12 秒か… |
| [lambda 問17](../../exercises/lambda.md#q17) | 4.3.2 | SnapStart を有効にした Python 関数で、ハンドラーの外で生成したセッション ID が… |
| [lambda 問19](../../exercises/lambda.md#q19) | 4.2.1 | Node.js の関数で ApplicationLogLevel を WARN に設定しましたが、I… |

<!-- questions:end -->
