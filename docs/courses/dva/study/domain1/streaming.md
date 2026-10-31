# 分野1: ストリーミング

分野1では、Kinesis Data Streams と Data Firehose の選択、シャードの計算、Lambda での読み取りを問われます。処理の遅れの監視やスロットリングの調査は[分野4](../domain4/streaming.md)で扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.1.5](../../domain1.md#skill-1-1-5) | SDK でのレコードの書き込み |
| [1.1.6](../../domain1.md#skill-1-1-6) | ストリーミングデータの管理 |
| [1.1.7](../../domain1.md#skill-1-1-7) | Base64 の扱い |
| [1.2.3](../../domain1.md#skill-1-2-3) | ストリームのエラー処理 |
| [1.2.4](../../domain1.md#skill-1-2-4) | Lambda との統合 |

## 学習の順番 {#study-order}

1. [選び方](../../../../services/streaming.md#choosing): Kinesis Data Streams、Firehose、SQS の違いを比べます。
2. [シャードの容量](../../../../services/streaming.md#shards)、[シャード数の計算](../../../../services/streaming.md#shard-calculation): 書き込みのサイズと件数、読み取りの3つから計算します。
3. [パーティションキー](../../../../services/streaming.md#partition-key): 順序が保証される範囲とホットシャードの原因を理解します。
4. [保持期間](../../../../services/streaming.md#retention)、[キャパシティモード](../../../../services/streaming.md#capacity-modes): 読み直しの範囲と、シャードを管理するかどうかを決めます。
5. [シャードイテレーター](../../../../services/streaming.md#shard-iterators)、[消費者と拡張ファンアウト](../../../../services/streaming.md#enhanced-fan-out): 読み始める位置と、共有スループットとの違いを覚えます。
6. [Lambda とストリーム](../../../../services/streaming.md#lambda-streams): マッピングの設定と、SQS と違うエラーの扱いを押さえます。
7. [Amazon Data Firehose](../../../../services/streaming.md#firehose)、[バッファ](../../../../services/streaming.md#firehose-buffering): 遅延とオブジェクトの大きさの関係を理解します。
8. [Lambda による変換](../../../../services/streaming.md#firehose-transform)、[配信の失敗の扱い](../../../../services/streaming.md#firehose-failure): 変換関数の応答形式と、失敗したデータの行き先を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| シャードの書き込み | 1 MB/秒、1,000 レコード/秒 | パーティションキーも容量に含みます |
| シャードの読み取り（共有） | 2 MB/秒、5 回/秒 | 全消費者で分け合います |
| 拡張ファンアウト | 消費者ごとに 2 MB/秒、約 70 ms | 消費者が多くて遅いときに使います |
| レコードサイズ | 既定 1 MiB、最大 10 MiB | |
| `PutRecords` | 500 レコード、10 MiB | 部分的に失敗します |
| 保持期間 | 既定 24 時間、最大 8,760 時間 | 下限は 24 時間です |
| シャードイテレーターの期限 | 5 分 | 切れたら取り直します |
| `UpdateShardCount` | 24 時間に 10 回、2 倍まで、半分まで | 一度に 3 倍にはできません |
| `ParallelizationFactor` | 既定 1、最大 10 | シャードごとの同時処理数です |
| `MaximumRetryAttempts`、`MaximumRecordAgeInSeconds` | 既定 -1 | 既定は無限で、シャードが止まります |
| Firehose の S3 バッファ | 1〜128 MB（5 MB）、0〜900 秒（300 秒） | どちらかに達すると配信します |
| `PutRecordBatch` | 500 レコード、4 MiB | 部分的に失敗します |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 複数のアプリが同じデータを順序付きで読み、読み直しもする | Kinesis Data Streams を使います |
| ログを S3 に保存したいだけで、運用は最小限にしたい | Data Firehose を使います |
| 2 KB を毎秒 2,500 件書き、3 つのアプリが読む | 共有スループットなら 8 シャード、拡張ファンアウトなら 5 シャードです |
| 100 バイトを毎秒 5,000 件書く | サイズは足りても、件数の条件で 5 シャード必要です |
| 流量が読めず、シャードを管理したくない | On-demand モードにします |
| 一部のシャードだけスロットリングする | キーが偏っています。キーを変えるか、シャードを分割します |
| 毒レコードで Lambda の処理が止まる | `BisectBatchOnFunctionError`、再試行の上限、失敗の記録先を組み合わせます |
| マッピングの作成前のレコードも処理する | `StartingPosition` を `TRIM_HORIZON` にします |
| 4 シャードで `ParallelizationFactor` を 2 にしたときの同時実行 | 最大 8 です。Lambda の同時実行の枠も確認します |
| 保存前に Firehose で変換し、一部のレコードを捨てる | Lambda 変換で `result` を `Dropped` にします |

## 引っかかりやすい点 {#traps}

- キーを `"prod"` に固定すると、シャードを増やしても全レコードが 1 本に入ります。キーを変えないと解決しません。
- On-demand でも、1つのパーティションキーがシャードの上限を超えると解決できません。
- Lambda のイベントでは、Kinesis のデータが Base64 で届きます。デコードしてから解析します。
- `PutRecords` と `PutRecordBatch` は例外にならずに一部だけ失敗します。`FailedRecordCount` や `FailedPutCount` を見て失敗分を再送します。
- Firehose の変換関数で `recordId` を変えるとエラーになります。応答のデータも Base64 にします。
- Firehose はバッファの分だけ遅れます。時間を短くすると、S3 の小さなオブジェクトが増えます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [streaming 問1](../../exercises/streaming.md#q1) | 1.1.6 | ある開発者は、Provisioned モードの Kinesis データストリームを設計しています。1… |
| [streaming 問3](../../exercises/streaming.md#q3) | 1.1.6 | 自前の Kinesis 消費者を再起動した後、処理済みの次のレコードから読み直したいと考えています。… |
| [streaming 問5](../../exercises/streaming.md#q5) | 1.1.6 | Provisioned モードの 4 シャードのストリームを、一度の UpdateShardCoun… |
| [streaming 問7](../../exercises/streaming.md#q7) | 1.2.3 | Kinesis の Lambda イベントソースマッピングで、壊れたレコードのためにシャードの処理が… |
| [streaming 問8](../../exercises/streaming.md#q8) | 1.1.6 | Data Firehose で S3 に配信しています。既定のバッファ設定のまま、毎秒 1 KB し… |
| [streaming 問9](../../exercises/streaming.md#q9) | 1.1.7 | Firehose の変換用 Lambda 関数で、テスト用のレコードを宛先に届けずに捨てたいと考えて… |
| [streaming 問10](../../exercises/streaming.md#q10) | 1.1.5 | あるアプリケーションが Direct PUT の Firehose に PutRecordBatch… |
| [streaming 問11](../../exercises/streaming.md#q11) | 1.1.6 | Firehose の宛先が OpenSearch Service です。クラスターの障害でデータの配… |

<!-- questions:end -->
