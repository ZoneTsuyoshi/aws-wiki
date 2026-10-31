# 分野1: Kinesis とストリーミング

ストリームをどのサービスで読み、遅れと失敗にどう備えるかを問います。Lambda の設定値がよく出ます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.1.1](../../domain1.md#skill-1-1-1) | ストリーミングソースの読み取り |
| [1.1.7](../../domain1.md#skill-1-1-7) | Kinesis から Lambda を呼ぶ |
| [1.1.9](../../domain1.md#skill-1-1-9) | スロットリングとレート制限への対応 |
| [1.1.10](../../domain1.md#skill-1-1-10) | ファンインとファンアウト |
| [1.1.11](../../domain1.md#skill-1-1-11) | 取り込みの再実行性（リプレイ） |
| [1.1.12](../../domain1.md#skill-1-1-12) | ステートフルとステートレスの処理 |

## 学習の順番 {#study-order}

1. [Kinesis と MSK の違い](../../../../services/data-engineering.md#msk-vs-kinesis): 既存の Kafka の有無で選びます。
2. [シャードの容量](../../../../services/streaming.md#shards): 書き込みと読み取りの上限を覚えます。
3. [拡張ファンアウト](../../../../services/streaming.md#enhanced-fan-out): 共有スループットとの違いを確認します。
4. [ストリームのエラー処理の設定](../../../../services/lambda.md#esm-stream-errors): 既定で止まる理由と 3 つの対策を押さえます。
5. [保持期間](../../../../services/streaming.md#retention): 読み直せる範囲とサービスごとの違いを確認します。
6. [Flink](../../../../services/data-engineering.md#flink): 状態付きの処理とチェックポイントを理解します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| `ParallelizationFactor` | 既定 1、最大 10 | シャード数との積が同時実行数 |
| `BatchSize`（Kinesis） | 既定 100、最大 10,000 | 大きいほど失敗の範囲も広がる |
| `MaximumRetryAttempts` | 既定 -1（無限） | シャードの停止の原因 |
| `PutRecords` | 500 レコード、10 MiB | 部分失敗は呼び出し側で再送 |
| Kinesis の保持 | 既定 24 時間、最大 365 日 | DynamoDB Streams は 24 時間で延ばせない |
| `TumblingWindowInSeconds` | 最大 900 秒、状態は 1 MB | シャードごとの集計 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 既存の Kafka のコードを変えない | MSK と MSK Connect |
| S3 を経由せず Redshift へ入れる | ストリーミング取り込み |
| 1 件の不正なレコードで止まる | 分割、再試行の上限、失敗の送信先 |
| 全体に余裕があるのに書き込みが制限される | パーティションキーの偏りを直す |
| 複数のアプリが低遅延で読む | 拡張ファンアウト |
| 時間ウィンドウの集計とストリームの結合 | Managed Service for Apache Flink |

## 引っかかりやすい点 {#traps}

- シャードを増やしても、同じパーティションキーは同じシャードへ入ります。
- Firehose には読み直す API がありません。配信先の S3 を入力にします。
- 同じアプリケーション名の KCL はシャードを分け合います。別々に全件を読むなら別の名前にします。
- Glue のブックマークをリセットしても、出力先のファイルは消えません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [streaming 問1](../../exercises/streaming.md#q1) | 1.1.1 | オンプレミスで Kafka を運用しているチームが AWS へ移ります。自作のコネクターとプロデュー… |
| [streaming 問2](../../exercises/streaming.md#q2) | 1.1.1 | RDS for MySQL の変更を、スキーマを変えずにほぼ連続で取り出し、Kinesis Data… |
| [streaming 問3](../../exercises/streaming.md#q3) | 1.1.1 | Kinesis Data Streams のデータを Redshift で数十秒以内に分析します。S… |
| [streaming 問4](../../exercises/streaming.md#q4) | 1.1.7 | Kinesis をソースにした Lambda で、変換できないレコードが 1 件あるとシャードの処理… |
| [streaming 問5](../../exercises/streaming.md#q5) | 1.1.7 | シャードが 6 本のストリームを Lambda で読みます。ParallelizationFacto… |
| [streaming 問6](../../exercises/streaming.md#q6) | 1.1.7 | 関数の呼び出し回数が多く、費用が増えています。1 回あたりのレコードは数件です。数十秒の遅れは許され… |
| [streaming 問7](../../exercises/streaming.md#q7) | 1.1.7 | Kinesis の 100 件のバッチで 40 件目だけが失敗します。成功済みの前半を再処理せず、失… |
| [streaming 問8](../../exercises/streaming.md#q8) | 1.1.9 | ストリーム全体の書き込み量は容量の 3 割ですが、WriteProvisionedThroughpu… |
| [streaming 問9](../../exercises/streaming.md#q9) | 1.1.9 | DynamoDB のプロビジョンドのテーブルへバッチ投入すると ProvisionedThrough… |
| [streaming 問10](../../exercises/streaming.md#q10) | 1.1.9 | Lambda から RDS for PostgreSQL へ書き込むパイプラインで、イベントの急増時… |
| [streaming 問11](../../exercises/streaming.md#q11) | 1.1.10 | 1 本のストリームを 5 つのアプリがそれぞれ 200 ms 以内の遅延で読みます。共有スループット… |
| [streaming 問12](../../exercises/streaming.md#q12) | 1.1.10 | 数千台のセンサーのデータを 1 本のストリームへ集めます。API の呼び出し回数を減らし、1 回で多… |
| [streaming 問13](../../exercises/streaming.md#q13) | 1.1.10 | 注文イベントを 4 つの処理系へ配ります。処理系ごとに速度が異なり、遅い処理系が他を待たせないよう、… |
| [streaming 問14](../../exercises/streaming.md#q14) | 1.1.11 | 変換のバグを直し、3 日前の 10 時以降のレコードを Kinesis から読み直します。保持期間は… |
| [streaming 問15](../../exercises/streaming.md#q15) | 1.1.11 | 次のうち、再処理の設計として正しいものはどれですか。 |
| [streaming 問16](../../exercises/streaming.md#q16) | 1.1.11 | Glue のジョブのバグを直し、ブックマークをリセットして全件を再実行しました。出力先の件数が 2 … |
| [streaming 問17](../../exercises/streaming.md#q17) | 1.1.12 | 不正注文の検知で、同じカードの 5 分間の取引額を集計し、2 つのストリームを結合します。障害時は状… |
| [streaming 問18](../../exercises/streaming.md#q18) | 1.1.12 | Lambda でシャードごとに 1 分間の件数を集計します。追加のサービスは使いません。Tumbli… |
| [streaming 問19](../../exercises/streaming.md#q19) | 1.1.12 | Flink アプリを更新する前に、状態を確実に残して、問題があれば戻せるようにします。何を使いますか… |

<!-- questions:end -->
