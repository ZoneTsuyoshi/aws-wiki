# 分野4: ログのストリーミングと分析

リアルタイムかどうか、加工が必要かで手段を選ぶ力を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [リアルタイムの取り込み](../../domain4.md#t4-1-real-time) | リアルタイムのログの取り込み |
| [リアルタイムの分析](../../domain4.md#t4-2-real-time-analysis) | リアルタイムのログストリームの分析 |
| [ログ分析](../../domain4.md#t4-2-log-analysis) | AWS サービスでのログ分析 |
| [S3 イベント](../../domain4.md#t4-3-s3-logs) | S3 イベントによるログ処理と配信 |

## 学習の順番 {#study-order}

1. [Kinesis Data Streams、Firehose、SQS の選び方](../../../../services/streaming.md#choosing): Kinesis Data Streams と Firehose の選び方を確認します。
2. [バッファ](../../../../services/streaming.md#firehose-buffering): 遅れの原因を理解します。
3. [消費者と拡張ファンアウト](../../../../services/streaming.md#enhanced-fan-out): 専用の読み取り量を押さえます。
4. [Amazon Managed Service for Apache Flink](../../../../services/data-engineering.md#flink): 時間枠の集計を確認します。
5. [速く、安くするコツ](../../../../services/streaming.md#athena-performance): パーティションと列指向の形式を覚えます。
6. [S3 イベント通知](../../../../services/messaging.md#s3-events): S3 イベントの制約を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 届けるだけで最小の運用 | Firehose |
| 複数のアプリが順序どおりに読む | Kinesis Data Streams |
| 時間枠の連続した集計 | Managed Service for Apache Flink |
| 読み取りが競合する | 拡張ファンアウト |
| S3 上の長期のログを調べる | Athena |
| ログファイルが大量に届く | SQS を挟む |

## 引っかかりやすい点 {#traps}

- 同じ条件の S3 イベント通知は重複できません。複数の処理には EventBridge か SNS を使います。
- 遅れは `IteratorAgeMilliseconds` で確かめます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [log-streaming 問1](../../exercises/log-streaming.md#q1) | リアルタイムの取り込み | ログを S3 へ届けるだけの要件で、担当者は Kinesis Data Streams とコンシュー… |
| [log-streaming 問2](../../exercises/log-streaming.md#q2) | リアルタイムの取り込み | 次の要件の組み合わせを考えます。(1) 順序を保って複数のアプリがログを読み直せる。(2) デプロイ… |
| [log-streaming 問3](../../exercises/log-streaming.md#q3) | リアルタイムの取り込み | Firehose で S3 へ配信しているログが、ダッシュボードに反映されるまでの遅れを短くします。… |
| [log-streaming 問4](../../exercises/log-streaming.md#q4) | リアルタイムの分析 | Kinesis Data Streams のログを分析します。(1) レコードごとに特定の文字列で通… |
| [log-streaming 問5](../../exercises/log-streaming.md#q5) | リアルタイムの分析 | 1 つの Kinesis のストリームを 5 つのアプリが読むようになると、ReadProvisio… |
| [log-streaming 問6](../../exercises/log-streaming.md#q6) | リアルタイムの分析 | Lambda のコンシューマーの IteratorAgeMilliseconds が増え続けます。C… |
| [log-streaming 問7](../../exercises/log-streaming.md#q7) | ログ分析 | Athena で CloudTrail のログを毎週分析しています。スキャン量が多く、費用がかかりま… |
| [log-streaming 問8](../../exercises/log-streaming.md#q8) | ログ分析 | 先月、特定のアクセスキーで呼ばれた API と IP の一覧を、組織の全アカウントで調べます。ログは… |
| [log-streaming 問9](../../exercises/log-streaming.md#q9) | ログ分析 | Lambda の遅延の原因を調べます。ログの REPORT 行の Duration と Max Me… |
| [log-streaming 問10](../../exercises/log-streaming.md#q10) | S3 イベント | ALB のアクセスログは S3 に出力されます。届くたびに解析して OpenSearch Servi… |
| [log-streaming 問11](../../exercises/log-streaming.md#q11) | S3 イベント | CloudFront のログファイルが大量に届くと、S3 から直接呼ばれる Lambda の同時実行… |
| [log-streaming 問12](../../exercises/log-streaming.md#q12) | S3 イベント | S3 に届く WAF のログのうち、logs/ プレフィックスの .gz の新しいファイルだけを解析… |

<!-- questions:end -->
