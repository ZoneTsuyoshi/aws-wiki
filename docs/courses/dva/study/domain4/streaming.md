# 分野4: ストリーミング

Kinesis のスループットエラーと処理の遅れの診断、S3 に保存したログの Athena での検索が問われます。ストリームの設計やサービスの選び方は[分野1](../domain1/streaming.md)で扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.1.1](../../domain4.md#skill-4-1-1) | Kinesis のエラーの切り分け |
| [4.1.2](../../domain4.md#skill-4-1-2) | メトリクスの読み取り |
| [4.1.3](../../domain4.md#skill-4-1-3) | Athena によるログのクエリ |
| [4.3.5](../../domain4.md#skill-4-3-5) | 処理の遅れの検出 |

## 学習の順番 {#study-order}

1. [シャードの容量](../../../../services/streaming.md#shards): 読み書きの上限を覚えます。エラーの診断の前提です。
2. [エラーと監視](../../../../services/streaming.md#kinesis-errors): 書き込みと読み取りのエラーの違い、ホットシャードの見つけ方を学びます。
3. [消費者と拡張ファンアウト](../../../../services/streaming.md#enhanced-fan-out): 読み取りの競合を解消する方法を確認します。
4. [Lambda とストリーム](../../../../services/streaming.md#lambda-streams): シャードが止まる理由と、並列度の上げ方を押さえます。
5. [S3 上のログを問い合わせる](../../../../services/streaming.md#athena-logs): Logs Insights との使い分けを理解します。
6. [パーティションの設定](../../../../services/streaming.md#athena-partitions): パーティションの読み込み方と、0 件のときの確認を学びます。
7. [形式と料金](../../../../services/streaming.md#athena-formats-cost): スキャン量の減らし方を確認します。
8. [ワークグループ](../../../../services/streaming.md#athena-workgroups): スキャン量の制限と通知を押さえます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| 書き込み | シャードあたり 1 MB/秒、1,000 レコード/秒 | 超えると `ProvisionedThroughputExceededException` です |
| 読み取り（共有） | シャードあたり 2 MB/秒、5 トランザクション/秒 | 全消費者で共有します |
| 読み取り（拡張ファンアウト） | 消費者ごとに 2 MB/秒 | 登録は 20（On-demand Advantage は 50）です |
| `GetRecords` | 1 回 10 MB または 10,000 レコード | 10 MB を返すと次の 5 秒間は例外になります |
| シャードイテレーター | 5 分で期限切れ | `ExpiredIteratorException` の原因です |
| `ParallelizationFactor` | 既定 1、最大 10 | シャードごとの同時処理数です |
| Athena の料金 | スキャン量で決まる。1 クエリの最小は 10 MB | 失敗したクエリと DDL は無料です |
| CTAS と `INSERT INTO` | 一度に 100 パーティションまで | 超えるなら分けて実行します |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 書き込みで `ProvisionedThroughputExceededException` になる | バックオフと再送、`PutRecords` の利用、シャード追加、キーの分散を検討します |
| 全体に余裕があるのに一部のシャードだけ抑制される | `EnableEnhancedMonitoring` でホットシャードを特定し、キーを変えるか分割します |
| 読み取りで同じ例外が出る、消費者が増えて遅い | 拡張ファンアウトを使います |
| `ExpiredIteratorException` が出る | イテレーターを取り直します。KCL ならリーステーブルの容量も確認します |
| `IteratorAge` が増え続ける | `ParallelizationFactor` を上げるか、シャードを増やします |
| 毒レコードでシャードの処理が止まる | `BisectBatchOnFunctionError`、`MaximumRetryAttempts`、失敗の記録先を組み合わせます |
| 長期保管した大量のログを SQL で分析したい | S3 のログに Athena を使います。直近のログなら Logs Insights です |
| データがあるのに Athena の結果が 0 件 | パーティションの読み込みを確認します。Hive 形式は `MSCK REPAIR TABLE`、それ以外は `ALTER TABLE ... ADD PARTITION` です |
| パーティションが大量でクエリが遅い | パーティション射影を使います |
| Athena の費用を下げたい、巨大なスキャンを防ぎたい | パーティションと Parquet を使います。ワークグループのクエリごとの制限でも止められます |

## 引っかかりやすい点 {#traps}

- **他のアプリの読み取りまで失敗する:** 1 シャードに複数のアプリがあると、誰かの 10 MB の読み取りの後、5 秒間は同じシャードの呼び出しが例外になります。
- **`GetShardIterator` で同じ例外が出る:** ループで毎回取り直さず、`NextShardIterator` を使います。
- **シャード別のメトリクスがない:** シャードレベルのメトリクスは既定で無効です。
- **`WHERE` を付けたのに料金が下がらない:** パーティション列を指定しないと全件を読みます。
- **`MSCK REPAIR TABLE` で追加されない:** `userId=1` のようなキャメルケースのパスは追加されません。小文字にします。
- **指定した場所に結果が出ない:** ワークグループの「クライアント側の設定を上書き」がオンだと、`OutputLocation` は無視されます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [streaming 問2](../../exercises/streaming.md#q2) | 4.1.1 | Kinesis の 1 本のシャードだけで WriteProvisionedThroughputEx… |
| [streaming 問4](../../exercises/streaming.md#q4) | 4.1.1 | Kinesis の消費者が各バッチの処理に約 6 分かかります。1 つのイテレーターを取得してからま… |
| [streaming 問6](../../exercises/streaming.md#q6) | 4.1.1 | KCL を使う 2 つの別々の消費者アプリケーションを同じアプリケーション名でデプロイしました。各ア… |
| [streaming 問12](../../exercises/streaming.md#q12) | 4.1.3 | Athena の Hive 形式のテーブルがあり、S3 の dt=2026-10-30/ に新しいデ… |
| [streaming 問13](../../exercises/streaming.md#q13) | 4.3.5 | Athena で S3 の CSV のテーブルを毎日集計しています。1 回のクエリが読むデータ量が大… |
| [streaming 問14](../../exercises/streaming.md#q14) | 4.3.5 | 分析チームのメンバーが誤って巨大なテーブルを全件スキャンし、料金が高くなることがあります。**個々の… |

<!-- questions:end -->
