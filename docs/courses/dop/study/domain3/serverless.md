# 分野3: サーバーレスと疎結合

層を切り離してスケールさせる設計と、サーバーレスの設定を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [疎結合](../../domain3.md#t3-2-loose-coupling) | 疎結合で分散したアーキテクチャ |
| [サーバーレス](../../domain3.md#t3-2-serverless) | サーバーレスアーキテクチャ、サーバーレスアプリケーションの設定 |

## 学習の順番 {#study-order}

1. [密結合と疎結合](../../../../services/messaging.md#coupling): 疎結合の効果を確認します。
2. [選び方](../../../../services/messaging.md#how-to-choose): SQS、SNS、EventBridge、Kinesis の使い分けを押さえます。
3. [コールドスタートを減らす](../../../../services/lambda.md#cold-start): SnapStart と Provisioned Concurrency を確認します。
4. [同時実行とスケーリング](../../../../services/lambda.md#concurrency): 予約済み同時実行の役割を理解します。
5. [使用量プランとスロットリング](../../../../services/api-gateway.md#usage-plans-throttling): 使用量プランとスロットリングを確認します。
6. [RDS Proxy](../../../../services/databases.md#rds-proxy): 接続数の問題の解決を押さえます。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 下流の限界を超える注文を受ける | SQS で平準化する |
| 1 件を複数の処理へ配り、独立させる | SNS と SQS のファンアウト |
| 他の関数に同時実行を奪われる | 予約済み同時実行 |
| 取引先ごとに上限を決める | 使用量プランと API キー |
| `too many connections` | RDS Proxy |

## 引っかかりやすい点 {#traps}

- API Gateway の統合のタイムアウトより長い処理は、同期で待たずに渡します。
- Fargate のタスク数は Application Auto Scaling で増やします。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [serverless 問4](../../exercises/serverless.md#q4) | 疎結合 | 注文 API は同期で在庫システムを呼んでいます。在庫システムの更新は秒間 100 件が限界で、セー… |
| [serverless 問5](../../exercises/serverless.md#q5) | 疎結合 | 注文の完了イベントを、在庫、請求、通知の 3 つで処理します。将来の処理の追加でも注文サービスを変更… |
| [serverless 問6](../../exercises/serverless.md#q6) | 疎結合 | 数千の IoT デバイスのイベントを順序を保って複数のアプリで読み、過去 24 時間分は読み直します… |
| [serverless 問7](../../exercises/serverless.md#q7) | サーバーレス | Java の Lambda の API で、コールドスタートの遅延が要件の 500 ms を超えてい… |
| [serverless 問8](../../exercises/serverless.md#q8) | サーバーレス | API Gateway の後ろの Lambda と RDS が、特定の取引先の大量のアクセスで過負荷… |
| [serverless 問9](../../exercises/serverless.md#q9) | サーバーレス | Lambda から RDS へ接続すると、ピークで too many connections になり… |
| [serverless 問10](../../exercises/serverless.md#q10) | サーバーレス | API Gateway の同期の統合で、レポートの生成に 5 分かかる処理がタイムアウトします。利用… |

<!-- questions:end -->
