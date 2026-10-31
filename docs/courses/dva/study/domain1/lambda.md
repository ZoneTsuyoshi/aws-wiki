# 分野1: Lambda

分野1では、関数の設定、VPC 内のリソースへの接続、再試行と失敗の扱い、他のサービスとのつなぎ方を問われます。デプロイとバージョンは[分野3](../domain3/lambda.md)、性能の調整と障害の調査は[分野4](../domain4/lambda.md)で扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.2.1](../../domain1.md#skill-1-2-1) | VPC 内のプライベートリソースへのアクセス |
| [1.2.2](../../domain1.md#skill-1-2-2) | メモリ、同時実行、タイムアウト、レイヤーなどの設定 |
| [1.2.3](../../domain1.md#skill-1-2-3) | イベントのライフサイクルとエラー処理 |
| [1.2.4](../../domain1.md#skill-1-2-4) | イベントソースマッピングや送信先による統合 |

## 学習の順番 {#study-order}

1. [呼び出しの種類](../../../../services/lambda.md#invocation-types): 同期、非同期、イベントソースマッピングの動きと、エラーを誰が扱うかを区別します。
2. [呼び出し権限の向き](../../../../services/lambda.md#invocation-permissions): リソースベースポリシーと実行ロールのどちらに権限を与えるかを覚えます。
3. [設定項目](../../../../services/lambda.md#configuration): メモリ、タイムアウト、`/tmp`、ペイロードの値をつかみます。
4. [レイヤー](../../../../services/lambda.md#layers)、[拡張機能](../../../../services/lambda.md#extensions)、[環境変数](../../../../services/lambda.md#environment-variables): それぞれの役割と上限を区別します。
5. [予約済みと Provisioned の違い](../../../../services/lambda.md#reserved-provisioned): 目的と、上限を超えたときの動きを比べます。
6. [VPC 内のリソースへのアクセス](../../../../services/lambda.md#vpc-access): 必要な設定と、接続先ごとの経路を覚えます。
7. [再試行の動き](../../../../services/lambda.md#retries)、[デスティネーションと DLQ](../../../../services/lambda.md#destinations-dlq): 呼び出し方ごとの再試行と、失敗の退避先を整理します。
8. [イベントソースマッピング](../../../../services/lambda.md#event-source-mapping)、[部分バッチレスポンス](../../../../services/lambda.md#partial-batch-response): SQS とストリームの設定の違いと、失敗分だけ戻す方法を学びます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| メモリ | 既定 128 MB、128〜10,240 MB | CPU も比例して増えます。1,769 MB で 1 vCPU 相当です |
| タイムアウト | 既定 3 秒、最大 900 秒 | 15 分を超える処理は Lambda の外に分けます |
| `/tmp` | 既定 512 MB、最大 10,240 MB | 実行環境ごとに分かれ、共有できません |
| 環境変数 | 合計 4 KB | 大きな設定は Parameter Store などに置きます |
| レイヤー | 5 個 | .zip の関数でのみ使えます |
| ペイロード | 同期 6 MB、非同期 1 MB | 非同期のほうが小さい点に注意します |
| アカウントの同時実行数 | 既定 1,000 | 100 は予約できません |
| RPS の上限 | 同時実行数の 10 倍 | 短い関数は同時実行に余裕があっても 429 になります |
| 非同期の再試行 | 既定 2 回、0〜2 | スロットリングはこの回数に含みません |
| イベントの最大経過時間 | 既定 6 時間、60〜21,600 秒 | 古いイベントに意味がないなら短くします |
| `BatchSize` | SQS は既定 10、ストリームは既定 100 | SQS で 10 を超えるならバッチウィンドウを 1 秒以上にします |
| 可視性タイムアウト | 関数のタイムアウト × 6 + バッチウィンドウ | SQS トリガーの推奨値です |
| `maxReceiveCount` | 5 以上を推奨 | 少ないとスロットリングだけで DLQ に移ります |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| プライベートサブネットの RDS につなぎたい | 関数に VPC 設定を追加し、`AWSLambdaVPCAccessExecutionRole` を付け、DB のセキュリティグループで関数のグループからの通信を許可します |
| VPC に接続した関数から外部 API を呼ぶ | プライベートサブネットから NAT ゲートウェイを通します |
| VPC に接続した関数から S3 や DynamoDB を使う | ゲートウェイ型の VPC エンドポイントを使います |
| 接続数 50 の DB を関数の急増から守りたい | 予約済み同時実行を 50 にします。超えた分は、同期呼び出しなら 429 になります |
| 関数を緊急停止したい | 予約済み同時実行を 0 にします |
| 非同期の成功時と失敗時に次の処理へつなぎたい | デスティネーションを成功と失敗で別々に指定します |
| 二重実行を避けたい非同期の関数 | `MaximumRetryAttempts` を 0 にします。同じイベントが複数回届くことはあるので、処理は冪等にします |
| 5 分たった通知には意味がない | `MaximumEventAgeInSeconds` を 300 にします |
| SQS のバッチで失敗した分だけ再処理したい | `FunctionResponseTypes` に `ReportBatchItemFailures` を設定し、`batchItemFailures` を返します |
| Kinesis のシャードが毒レコードで止まる | `BisectBatchOnFunctionError`、`MaximumRetryAttempts`、オンフェイラーデスティネーションを組み合わせます |

## 引っかかりやすい点 {#traps}

- 関数をパブリックサブネットに接続しても外部へ出られません。パブリック IP が付かないからです。NAT ゲートウェイが必要です。
- SQS の可視性タイムアウトが関数のタイムアウトより短いと、マッピングの作成や更新がエラーになります。
- `ReportBatchItemFailures` はコードで返すだけでは動きません。マッピングの `FunctionResponseTypes` にも設定します。
- 関数の DLQ は非同期呼び出しの仕組みです。デスティネーションは非同期呼び出しと、ストリームや Kafka のマッピングで使えます。SQS トリガーの失敗はキュー側のリドライブポリシーで DLQ に送ります。
- `put-function-event-invoke-config` は、指定しなかった項目を消します。一部だけ変えるなら `update-function-event-invoke-config` を使います。
- FIFO のキューやトピックはデスティネーションにできません。失敗すると `DestinationDeliveryFailures` が増えます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [lambda 問1](../../exercises/lambda.md#q1) | 1.2.4 | ある開発者は、標準 SQS キューをイベントソースとする Lambda 関数を作成しました。関数のタ… |
| [lambda 問2](../../exercises/lambda.md#q2) | 1.2.4 | 開発者が標準 SQS キューのイベントソースマッピングで、BatchSize を 100 に変更しよ… |
| [lambda 問3](../../exercises/lambda.md#q3) | 1.2.3 | 非同期で呼び出す関数に、オンフェイラーデスティネーションと MaximumEventAgeInSec… |
| [lambda 問4](../../exercises/lambda.md#q4) | 1.2.3 | Kinesis Data Streams を読む関数で、壊れたレコードがあるとシャードの処理が止まり… |
| [lambda 問6](../../exercises/lambda.md#q6) | 1.2.4 | DynamoDB Streams から Lambda を呼ぶマッピングを作成します。作成直後の数分間… |
| [lambda 問7](../../exercises/lambda.md#q7) | 1.2.4 | SQS から呼ばれる関数が、失敗したメッセージの ID を batchItemFailures とし… |
| [lambda 問8](../../exercises/lambda.md#q8) | 1.2.4 | SQS キューのマッピングに FilterCriteria を設定し、type が order のメ… |
| [lambda 問10](../../exercises/lambda.md#q10) | 1.2.2 | アカウントの同時実行数の上限は 1,000 です。関数 A に 500、関数 B に 300 の予約… |
| [lambda 問13](../../exercises/lambda.md#q13) | 1.2.1 | プライベートサブネットの RDS に接続する関数を VPC に接続しました。S3 からのファイル取得… |
| [lambda 問14](../../exercises/lambda.md#q14) | 1.2.2 | ネイティブ拡張を使う Python 関数を x86_64 から arm64 に移行します。設定変更の… |

<!-- questions:end -->
