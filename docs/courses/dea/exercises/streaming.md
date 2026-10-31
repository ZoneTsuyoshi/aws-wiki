# Kinesis とストリーミングの問題集

対象の解説: [ストリーミングとデータ分析（Kinesis、Firehose、Athena、OpenSearch）](../../../services/streaming.md)、[Amazon MSK](../../../services/data-engineering.md#msk)、[Amazon Managed Service for Apache Flink](../../../services/data-engineering.md#flink)

### 問1 {#q1}

オンプレミスで Kafka を運用しているチームが AWS へ移ります。自作のコネクターとプロデューサーのコードは変更したくありません。適切な取り込み先はどれですか。

- A. Amazon MSK に移し、コネクターは MSK Connect で動かす
- B. Kinesis Data Streams に移し、コネクターを KCL のアプリに書き換える
- C. SQS の FIFO キューを受け口にし、コネクターの処理をポーリングへ移す
- D. Data Firehose を受け口にし、コネクターの処理を Lambda の変換へ移す

??? success "答えと解説"
    **正解: A**

    MSK は Kafka の API とツールをそのまま使えます。

    - A: 正しい。
    - B: 誤り。API が異なるのでコードの変更が必要です。
    - C: 誤り。Kafka の互換性がなく、ログを読み直す使い方もできません。
    - D: 誤り。Kafka の API を受けないので、プロデューサーの変更が必要です。

    **スキル:** [1.1.1](../domain1.md#skill-1-1-1) / **参照:** [Amazon MSK](../../../services/data-engineering.md#msk)、[Kinesis Data Streams と MSK の違い](../../../services/data-engineering.md#msk-vs-kinesis)

### 問2 {#q2}

RDS for MySQL の変更を、スキーマを変えずにほぼ連続で取り出し、Kinesis Data Streams へ流します。アプリの改修はしません。何を使いますか。

- A. DynamoDB Streams を MySQL のテーブルで有効にし、Lambda で転送する
- B. Redshift のストリーミング取り込みで、MySQL のテーブルを直接読む
- C. Glue のジョブブックマークを有効にし、JDBC で定期的に全表を読む
- D. DMS の CDC タスクで、Kinesis Data Streams をターゲットにする

??? success "答えと解説"
    **正解: D**

    DMS の CDC は、データベースの変更を取り出してストリームへ送れます。

    - A: 誤り。DynamoDB Streams は DynamoDB のテーブルの機能です。
    - B: 誤り。ストリーミング取り込みのソースは Kinesis と MSK です。
    - C: 誤り。定期バッチであり、削除や更新の変更履歴を連続では取り出せません。
    - D: 正しい。

    **スキル:** [1.1.1](../domain1.md#skill-1-1-1) / **参照:** [CDC の前提](../../../services/migration.md#dms-cdc)、[Kinesis Data Streams](../../../services/streaming.md#kinesis-data-streams)

### 問3 {#q3}

Kinesis Data Streams のデータを Redshift で数十秒以内に分析します。S3 への中間ファイルは作らないという要件です。どの方法を選びますか。

- A. フェデレーテッドクエリで Kinesis に接続し、シャードを SQL で読む
- B. Spectrum の外部テーブルでストリームを直接定義し、毎回読みに行く
- C. ストリーミング取り込みで、ストリームを読むマテリアライズドビューを作る
- D. Firehose で S3 へ配信し、Redshift の `COPY` を定期的に実行する

??? success "答えと解説"
    **正解: C**

    ストリーミング取り込みは、S3 を経由せずマテリアライズドビューへ直接入れます。

    - A: 誤り。フェデレーテッドクエリの対象は RDS や Aurora の PostgreSQL と MySQL です。
    - B: 誤り。Spectrum が読むのは S3 のファイルです。
    - C: 正しい。
    - D: 誤り。S3 を経由するので要件に合いません。

    **スキル:** [1.1.1](../domain1.md#skill-1-1-1) / **参照:** [データを取り込む他の方法](../../../services/data-engineering.md#redshift-ingestion)、[Kinesis Data Streams](../../../services/streaming.md#kinesis-data-streams)

### 問4 {#q4}

Kinesis をソースにした Lambda で、変換できないレコードが 1 件あるとシャードの処理が止まり、`IteratorAge` が増え続けます。既定の設定のままです。処理を止めず、問題のレコードを後で調べられるようにする設定の組み合わせはどれですか。

- A. `BatchSize` を 10,000 に増やし、`MaximumBatchingWindowInSeconds` を 300 にして一度に処理する
- B. `BisectBatchOnFunctionError` を有効にし、`MaximumRetryAttempts` に上限を設定し、失敗の送信先を指定する
- C. `StartingPosition` を `LATEST` に変更し、不正なレコードより後ろから読み始める
- D. `ParallelizationFactor` を 10 に上げ、同じシャードを別のバッチでも並列に処理させる

??? success "答えと解説"
    **正解: B**

    既定では再試行が無限で、レコードが期限切れになるまで止まります。分割、上限、失敗の記録を組み合わせます。

    - A: 誤り。不正なレコードが含まれる範囲が広がるだけで、再試行は続きます。
    - B: 正しい。
    - C: 誤り。既存のマッピングの再開位置は変わらず、問題のレコードの情報も残りません。
    - D: 誤り。パーティションキー単位の順序は保たれるので、不正なレコードのあるキーの処理は止まったままです。

    **スキル:** [1.1.7](../domain1.md#skill-1-1-7) / **参照:** [ストリームのエラー処理の設定](../../../services/lambda.md#esm-stream-errors)、[Lambda とストリーム](../../../services/streaming.md#lambda-streams)

### 問5 {#q5}

シャードが 6 本のストリームを Lambda で読みます。`ParallelizationFactor` を 3 にしました。このマッピングで動く関数の同時実行数は最大でいくつですか。

- A. 18
- B. 9
- C. 3
- D. 6

??? success "答えと解説"
    **正解: A**

    シャード数と `ParallelizationFactor` の積が最大の同時実行数です。

    - A: 正しい。
    - B: 誤り。シャード数と係数は足さず、掛けます。
    - C: 誤り。シャードごとの同時バッチ数であり、全体の値ではありません。
    - D: 誤り。係数が 1 のときの値です。

    **スキル:** [1.1.7](../domain1.md#skill-1-1-7) / **参照:** [イベントソースマッピング](../../../services/lambda.md#event-source-mapping)、[Lambda とストリーム](../../../services/streaming.md#lambda-streams)

### 問6 {#q6}

関数の呼び出し回数が多く、費用が増えています。1 回あたりのレコードは数件です。数十秒の遅れは許されます。費用を抑えるために変更する設定はどれですか。

- A. `FunctionResponseTypes` に `ReportBatchItemFailures` を指定する
- B. `MaximumRetryAttempts` を 0 にし、失敗時の呼び出しをなくす
- C. `ParallelizationFactor` を増やし、シャードあたりの同時バッチを増やす
- D. `MaximumBatchingWindowInSeconds` を増やし、ためてから呼ぶ

??? success "答えと解説"
    **正解: D**

    ウィンドウを増やすと、1 回あたりのレコードが増えて呼び出しが減ります。既定は 0 秒です。

    - A: 誤り。失敗の範囲を返す設定で、通常の呼び出し回数は変わりません。
    - B: 誤り。通常の呼び出し回数は変わらず、データを失う恐れが増えます。
    - C: 誤り。呼び出しは増える方向です。
    - D: 正しい。

    **スキル:** [1.1.7](../domain1.md#skill-1-1-7) / **参照:** [イベントソースマッピング](../../../services/lambda.md#event-source-mapping)、[Lambda とストリーム](../../../services/streaming.md#lambda-streams)

### 問7 {#q7}

Kinesis の 100 件のバッチで 40 件目だけが失敗します。成功済みの前半を再処理せず、失敗した位置から再試行したいです。どう実装しますか。

- A. 関数内で例外を握りつぶして成功を返し、失敗したレコードをログに書く
- B. `BisectBatchOnFunctionError` だけを有効にし、関数はそのまま例外を投げる
- C. `ReportBatchItemFailures` を有効にし、関数が失敗したレコードのシーケンス番号を返す
- D. `TumblingWindowInSeconds` を設定し、ウィンドウごとに状態を持って位置を覚える

??? success "答えと解説"
    **正解: C**

    部分バッチレスポンスは、失敗の位置を返して、そこから再試行させます。

    - A: 誤り。失敗が再試行されません。
    - B: 誤り。分割はできますが、成功済みのレコードの一部は再処理されます。
    - C: 正しい。
    - D: 誤り。集計のための機能で、失敗の位置の報告ではありません。

    **スキル:** [1.1.7](../domain1.md#skill-1-1-7) / **参照:** [部分バッチレスポンス](../../../services/lambda.md#partial-batch-response)、[ストリームのエラー処理の設定](../../../services/lambda.md#esm-stream-errors)

### 問8 {#q8}

ストリーム全体の書き込み量は容量の 3 割ですが、`WriteProvisionedThroughputExceeded` が発生します。パーティションキーは工場 ID で、1 つの工場のデータが大半です。最初に行う対処はどれですか。

- A. 全シャードを均等に 2 倍へ増やし、同じキーのまま書き込みを続ける
- B. 値の種類が多いパーティションキーへ変え、書き込みを分散する
- C. 拡張ファンアウトの消費者を登録し、読み取りの容量を増やす
- D. データの保持期間を 7 日に延ばし、再試行の余裕を増やす

??? success "答えと解説"
    **正解: B**

    全体に余裕があるのに制限されるならホットシャードです。キーを分散します。

    - A: 誤り。同じキーは同じシャードへ入り、偏りが残ります。
    - B: 正しい。
    - C: 誤り。書き込みの制限には効きません。
    - D: 誤り。書き込みのスループットには関係しません。

    **スキル:** [1.1.9](../domain1.md#skill-1-1-9) / **参照:** [エラーと監視](../../../services/streaming.md#kinesis-errors)、[パーティションキー](../../../services/streaming.md#partition-key)

### 問9 {#q9}

DynamoDB のプロビジョンドのテーブルへバッチ投入すると `ProvisionedThroughputExceededException` が出ます。投入は 1 日 1 回で 10 分だけ急増します。テーブルの容量は普段は十分です。投入側で行うのに最も適した対処はどれですか。

- A. 再試行を即時に無制限で繰り返し、早く投入を終わらせる
- B. GSI を削除せずに WCU をベーステーブルの半分に下げ、費用を減らす
- C. 読み取りを強い整合性に変更し、書き込みの完了を確認してから次を送る
- D. SQS を挟んで流量をならし、指数バックオフとジッターで再試行する

??? success "答えと解説"
    **正解: D**

    流量の平準化とバックオフは、急増への共通の対策です。

    - A: 誤り。負荷を増やし、制限が長引きます。
    - B: 誤り。GSI の WCU が足りないと、ベーステーブルの書き込みも制限されます。
    - C: 誤り。読み取りの設定で、書き込みの容量は増えません。
    - D: 正しい。

    **スキル:** [1.1.9](../domain1.md#skill-1-1-9) / **参照:** [スロットリング](../../../services/dynamodb.md#throttling)、[指数バックオフとジッター](../../../services/sdk-resilience.md#backoff-jitter)

### 問10 {#q10}

Lambda から RDS for PostgreSQL へ書き込むパイプラインで、イベントの急増時に接続数が枯渇します。インスタンスのサイズは変えません。適切な対処はどれですか。（2つ選択）

- A. 関数のメモリを増やし、1 回の処理時間を伸ばす
- B. Multi-AZ のインスタンス配置を有効にし、スタンバイにも接続を分散する
- C. 関数に予約済み同時実行を設定し、下流へ送る量を抑える
- D. RDS Proxy を挟み、接続を共有する
- E. Provisioned Concurrency を増やし、接続をあらかじめ多く開いておく

??? success "答えと解説"
    **正解: C, D**

    接続の共有と同時実行の制限で、下流の接続を守ります。

    - A: 誤り。メモリは接続数の制限と関係せず、処理時間を伸ばす理由もありません。
    - B: 誤り。この配置のスタンバイは接続を受けないので、分散されません。
    - C: 正しい。同時実行の上限になるので、データベースへの負荷を抑えられます。
    - D: 正しい。接続を再利用して、データベース側の接続数を抑えます。
    - E: 誤り。コールドスタートを減らす機能で、接続数の枯渇は悪化する恐れがあります。

    **スキル:** [1.1.9](../domain1.md#skill-1-1-9) / **参照:** [RDS Proxy](../../../services/databases.md#rds-proxy)、[予約済みと Provisioned の違い](../../../services/lambda.md#reserved-provisioned)

### 問11 {#q11}

1 本のストリームを 5 つのアプリがそれぞれ 200 ms 以内の遅延で読みます。共有スループットでは `ReadProvisionedThroughputExceeded` が出ます。適切な変更はどれですか。

- A. 各アプリを拡張ファンアウトの消費者として登録する
- B. シャードの数はそのまま、各アプリのポーリング間隔を短くする
- C. Firehose を消費者にして S3 へ配信し、各アプリは S3 を読む
- D. 5 つのアプリを同じアプリケーション名の 1 つの KCL アプリにまとめる

??? success "答えと解説"
    **正解: A**

    拡張ファンアウトは、消費者ごとにシャードあたり 2 MB/秒をプッシュで受けられます。

    - A: 正しい。
    - B: 誤り。共有の 2 MB/秒の取り合いが悪化します。
    - C: 誤り。バッファが入るので、この遅延の要件を満たせません。
    - D: 誤り。同じ名前の KCL はシャードを分け合うので、各アプリが全データを読めません。

    **スキル:** [1.1.10](../domain1.md#skill-1-1-10) / **参照:** [消費者と拡張ファンアウト](../../../services/streaming.md#enhanced-fan-out)、[シャードの容量](../../../services/streaming.md#shards)

### 問12 {#q12}

数千台のセンサーのデータを 1 本のストリームへ集めます。API の呼び出し回数を減らし、1 回で多くのレコードを送りたいです。`PutRecords` について正しいものはどれですか。

- A. 一部のレコードが失敗すると、全レコードが自動で巻き戻される
- B. 1 リクエストで 500 レコード、合計 10 MiB まで送れる
- C. 順序を保つため、1 リクエストは同じパーティションキーだけに限られる
- D. 1 リクエストで 10,000 レコードまで送れ、サイズの上限はない

??? success "答えと解説"
    **正解: B**

    バッチ API で呼び出しを減らします。部分的な失敗の再送は呼び出し側で行います。

    - A: 誤り。部分的に失敗し、`FailedRecordCount` を見て失敗分を再送します。
    - B: 正しい。
    - C: 誤り。キーは混在できます。
    - D: 誤り。レコード数の上限は 500 で、サイズの上限もあります。

    **スキル:** [1.1.10](../domain1.md#skill-1-1-10) / **参照:** [シャードの容量](../../../services/streaming.md#shards)、[エラーと監視](../../../services/streaming.md#kinesis-errors)

### 問13 {#q13}

注文イベントを 4 つの処理系へ配ります。処理系ごとに速度が異なり、遅い処理系が他を待たせないよう、それぞれ緩衝したいです。低遅延の順序保証は不要です。どの構成が適切ですか。

- A. Lambda の非同期呼び出しを 1 つの関数に向け、関数の中で順に呼ぶ
- B. 1 つの SQS キューを 4 つの処理系が共有し、順にポーリングする
- C. SNS トピックから処理系ごとの SQS キューへ配る
- D. 1 つの Kafka のコンシューマーグループに 4 つの処理系を入れる

??? success "答えと解説"
    **正解: C**

    SNS でファンアウトし、消費者ごとのキューで緩衝します。

    - A: 誤り。遅い処理系が全体を待たせます。
    - B: 誤り。1 通は 1 つの処理系にしか渡らないので、配信になりません。
    - C: 正しい。
    - D: 誤り。同じグループではパーティションを分け合うので、全部を読めません。

    **スキル:** [1.1.10](../domain1.md#skill-1-1-10) / **参照:** [ファンアウト](../../../services/messaging.md#fanout)、[消費者と拡張ファンアウト](../../../services/streaming.md#enhanced-fan-out)

### 問14 {#q14}

変換のバグを直し、3 日前の 10 時以降のレコードを Kinesis から読み直します。保持期間は 7 日に設定済みです。どのシャードイテレーターを使いますか。

- A. `TRIM_HORIZON` を指定し、読み始めの時刻をアプリで指定する
- B. `AT_TIMESTAMP` に 3 日前の 10 時を指定する
- C. `AFTER_SEQUENCE_NUMBER` に 3 日前の 10 時の日時の文字列を指定する
- D. `LATEST` を指定し、最新の位置から読む

??? success "答えと解説"
    **正解: B**

    時刻で開始位置を決めるのは `AT_TIMESTAMP` です。

    - A: 誤り。最も古いレコードから読むので、不要な範囲まで処理します。
    - B: 正しい。
    - C: 誤り。シーケンス番号を指定するイテレーターで、日時は受け付けません。
    - D: 誤り。新しいレコードだけを読みます。

    **スキル:** [1.1.11](../domain1.md#skill-1-1-11) / **参照:** [保持期間](../../../services/streaming.md#retention)、[シャードイテレーター](../../../services/streaming.md#shard-iterators)

### 問15 {#q15}

次のうち、再処理の設計として正しいものはどれですか。

- A. DynamoDB Streams の保持期間を 365 日に延ばし、古い変更も読めるようにする
- B. Firehose は配信済みのレコードを 7 日間保持するので、`GetRecords` で読み直す
- C. DynamoDB Streams は 24 時間で消えるので、長期の再処理に備えて変更を S3 へ退避する
- D. Glue のブックマークをリセットすれば、以前の出力ファイルも自動で消える

??? success "答えと解説"
    **正解: C**

    基本は加工前のデータを不変のまま S3 に残すことです。

    - A: 誤り。保持は 24 時間で、延ばせません。
    - B: 誤り。Firehose に読み直す API はなく、配信先の S3 を入力にします。
    - C: 正しい。
    - D: 誤り。追跡するのはソース側だけで、出力先は残ります。

    **スキル:** [1.1.11](../domain1.md#skill-1-1-11) / **参照:** [DynamoDB Streams](../../../services/dynamodb.md#streams)、[Amazon Data Firehose](../../../services/streaming.md#firehose)

### 問16 {#q16}

Glue のジョブのバグを直し、ブックマークをリセットして全件を再実行しました。出力先の件数が 2 倍になりました。今後、再処理で重複させない方法はどれですか。（2つ選択）

- A. 再処理の出力先を別のプレフィックスに分ける
- B. ブックマークを `job-bookmark-pause` にしてから再実行する
- C. ジョブの最大同時実行数を 2 に上げて、再処理を早く終わらせる
- D. 処理を冪等にし、同じキーの行を上書きする形で書く
- E. `transformation_ctx` の値を変更して、別の処理として扱わせる

??? success "答えと解説"
    **正解: A, D**

    リセットしても出力先のファイルは消えません。

    - A: 正しい。古い出力と混ざりません。
    - B: 誤り。状態を更新しないだけで、出力先の重複は防げません。
    - C: 誤り。重複には効かず、ブックマークとも両立しません。
    - D: 正しい。何度実行しても結果が同じになります。
    - E: 誤り。状態のキーが変わるだけで、全件を読み直して重複します。

    **スキル:** [1.1.11](../domain1.md#skill-1-1-11) / **参照:** [ジョブのブックマーク](../../../services/data-engineering.md#glue-bookmarks)、[冪等性](../../../services/sdk-resilience.md#idempotency)

### 問17 {#q17}

不正注文の検知で、同じカードの 5 分間の取引額を集計し、2 つのストリームを結合します。障害時は状態を復元します。どのサービスが適切ですか。

- A. Firehose の Lambda 変換
- B. Glue のクローラーと Data Catalog
- C. S3 イベント通知で起動する Lambda
- D. Managed Service for Apache Flink

??? success "答えと解説"
    **正解: D**

    時間ウィンドウや結合はステートフルな処理で、Flink が向きます。

    - A: 誤り。レコードごとの変換に向き、ウィンドウの状態やストリームの結合は持ちません。
    - B: 誤り。スキーマの推定で、ストリームは対象外です。
    - C: 誤り。ファイル到着時の処理で、ストリームの状態は持ちません。
    - D: 正しい。

    **スキル:** [1.1.12](../domain1.md#skill-1-1-12) / **参照:** [ステートフルとステートレス](../../../services/sdk-resilience.md#stateful-stateless)、[Amazon Managed Service for Apache Flink](../../../services/data-engineering.md#flink)

### 問18 {#q18}

Lambda でシャードごとに 1 分間の件数を集計します。追加のサービスは使いません。`TumblingWindowInSeconds` の説明として正しいものはどれですか。

- A. 状態は関数の戻り値で次の呼び出しへ渡し、シャードあたり最大 1 MB である
- B. リシャーディングの後も、親シャードの状態を子シャードが引き継ぐ
- C. ウィンドウは最大 24 時間で、複数のシャードをまたいで集計できる
- D. 状態は Lambda が DynamoDB に自動で保存し、サイズの上限はない

??? success "答えと解説"
    **正解: A**

    短い集計なら Lambda のタンブリングウィンドウで足ります。

    - A: 正しい。
    - B: 誤り。シャードが終わるとウィンドウは閉じ、子シャードは新しい状態で始めます。
    - C: 誤り。最大は 900 秒で、シャードごとの集計です。
    - D: 誤り。状態は戻り値で引き継ぎ、外部のデータベースは使いません。

    **スキル:** [1.1.12](../domain1.md#skill-1-1-12) / **参照:** [TumblingWindowInSeconds](../../../services/lambda.md#esm-tumbling-window)、[ステートフルとステートレス](../../../services/sdk-resilience.md#stateful-stateless)

### 問19 {#q19}

Flink アプリを更新する前に、状態を確実に残して、問題があれば戻せるようにします。何を使いますか。

- A. 更新の前に手動でスナップショットを作る
- B. Firehose の Lambda 変換に処理を移し、バッファを状態として使う
- C. 自動のチェックポイントの間隔を 1 秒へ短くする
- D. `AutoScalingEnabled` を無効にして、更新中の KPU を固定する

??? success "答えと解説"
    **正解: A**

    チェックポイントは自動で障害復旧用、スナップショットは手動で更新や移行の前に取ります。

    - A: 正しい。
    - B: 誤り。バッファは配信のための一時保持で、状態の保存にはなりません。
    - C: 誤り。チェックポイントは障害復旧のためで、負荷も増えます。
    - D: 誤り。状態の保存とは関係しません。

    **スキル:** [1.1.12](../domain1.md#skill-1-1-12) / **参照:** [Amazon Managed Service for Apache Flink](../../../services/data-engineering.md#flink)、[Lambda による変換](../../../services/streaming.md#firehose-transform)
