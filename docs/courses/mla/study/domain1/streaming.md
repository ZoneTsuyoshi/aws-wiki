# 分野1: ストリーミング

取り込みのサービスを要件で選び、Kinesis の症状と、ストリームの変換の手段を区別します。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.1.3](../../domain1.md#skill-1-1-3) | 取り込みと保存の問題の解決 |
| [1.1.4](../../domain1.md#skill-1-1-4) | ストリーミングでの取り込み |
| [1.2.3](../../domain1.md#skill-1-2-3) | ストリーミングデータの変換 |

## 学習の順番 {#study-order}

1. [選び方](../../../../services/streaming.md#choosing): Kinesis Data Streams、Firehose、Flink の違いをつかみます。
2. [シャード数の計算](../../../../services/streaming.md#shard-calculation)と [Kinesis のエラー](../../../../services/streaming.md#kinesis-errors): 書き込みの上限と症状を覚えます。
3. [Firehose の変換](../../../../services/streaming.md#firehose-transform): `recordId` と `result` の決まりを確認します。
4. [Lambda とストリーム](../../../../services/streaming.md#lambda-streams)と[タンブリングウィンドウ](../../../../services/lambda.md#esm-tumbling-window): 短い集計の方法を押さえます。
5. [Flink](../../../../services/data-engineering.md#flink)と [MSK との違い](../../../../services/data-engineering.md#msk-vs-kinesis): 複雑な処理と既存の Kafka の場面を区別します。
6. [Kinesis Video Streams](../../../../services/other-services.md#kinesis-video): 動画と音声の取り込みを確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| シャードの書き込み | 1 MB/秒、1,000 レコード/秒 | 2 KB を毎秒 2,500 件なら 5 シャード |
| シャードの読み取り | 2 MB/秒 | 消費者が多いなら拡張ファンアウト |
| タンブリングウィンドウ | 0〜900 秒 | シャードごとの集計 |
| Firehose の変換の `result` | `Ok`、`Dropped`、`ProcessingFailed` | `recordId` は入力と同じ |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| S3 や OpenSearch へ届けるだけ | Firehose |
| 独自のコードで順序どおりに読む | Kinesis Data Streams |
| 複雑なウィンドウ、ストリームの結合 | Flink |
| 既存の Kafka のコード | Amazon MSK |
| `ProvisionedThroughputExceededException` で一部のシャードだけ | 高カーディナリティのキーに変える |
| `IteratorAgeMilliseconds` が増え続ける | 消費者の強化、拡張ファンアウト |

## 引っかかりやすい点 {#traps}

- Firehose はバッファの分だけ遅れます。秒単位の特徴量計算には向きません。
- 拡張ファンアウトは読み取りの機能で、書き込みの偏りを解決しません。
- Firehose の変換で `recordId` を変えると、配信に失敗します。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [streaming 問1](../../exercises/streaming.md#q1) | 1.1.4 | クリックのイベントを S3 に Parquet で届けるだけで、独自の消費者コードは書きたくありませ… |
| [streaming 問2](../../exercises/streaming.md#q2) | 1.1.4 | 不正検知の特徴量を計算する 2 つのチームが、同じ取引イベントをそれぞれのコードで順序どおりに読みま… |
| [streaming 問3](../../exercises/streaming.md#q3) | 1.1.4 | 工場のカメラ映像を取り込み、後から ML の推論に使います。取り込みに適したサービスはどれですか。 |
| [streaming 問4](../../exercises/streaming.md#q4) | 1.1.4 | 既に Kafka のプロデューサーとコンシューマーのコードがあり、変更を抑えて AWS へ移します。… |
| [streaming 問5](../../exercises/streaming.md#q5) | 1.1.3 | 同じパーティションキーに書き込みが集中し、Kinesis の一部のシャードで Provisioned… |
| [streaming 問6](../../exercises/streaming.md#q6) | 1.1.3 | Lambda で Kinesis を読んで特徴量を計算しています。IteratorAgeMillis… |
| [streaming 問7](../../exercises/streaming.md#q7) | 1.2.3 | Firehose の Lambda 変換で、不要なレコードを捨て、それ以外を整形します。関数の戻り値… |
| [streaming 問8](../../exercises/streaming.md#q8) | 1.2.3 | Kinesis のイベントから、シャードごとに 5 分間の合計を計算します。別の DB は増やさず、… |
| [streaming 問9](../../exercises/streaming.md#q9) | 1.2.3 | 取引のストリームと顧客のストリームを結合し、スライディングウィンドウで複雑に集計します。状態を保持し… |
| [streaming 問10](../../exercises/streaming.md#q10) | 1.2.3 | 既存の Spark のストリーミング処理のコードを、サーバーを管理せずに動かします。マイクロバッチで… |
| [streaming 問11](../../exercises/streaming.md#q11) | 1.1.4, 1.2.3 | センサーデータの取り込みです。要件は次のとおりです。すべてのレコードを S3 に保存し、さらに 1 … |

<!-- questions:end -->
