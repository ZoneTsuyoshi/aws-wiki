# ログのストリーミングと分析の問題集

対象の解説: [ログのストリーミングと分析](../../../services/streaming.md#choosing)

### 問1 {#q1}

ログを S3 へ届けるだけの要件で、担当者は Kinesis Data Streams とコンシューマーの Lambda を自作する案を出しました。条件は、最小の運用負荷、最大で数分の遅れは許容、圧縮して保存です。何を提案しますか。

- A. Kinesis Data Streams のシャード数を増やし、Lambda の同時実行を増やす
- B. Amazon Data Firehose
- C. SQS の標準キューに入れて、EC2 のワーカーで S3 へ書く
- D. CloudWatch Logs の Live Tail を S3 へ保存する

??? success "答えと解説"
    **正解: B**

    S3 や OpenSearch へ届けるだけなら Firehose です。バッファの分は遅れます。

    - A: 誤り。届けるだけの要件に対して運用が重い。
    - B: 正しい。
    - C: 誤り。サーバーの運用が必要になる。
    - D: 誤り。Live Tail は人が見るための機能。

    **スキル:** [リアルタイムの取り込み](../domain4.md#t4-1-real-time) / **参照:** [Kinesis Data Streams、Firehose、SQS の選び方](../../../services/streaming.md#choosing)、[バッファ](../../../services/streaming.md#firehose-buffering)

### 問2 {#q2}

次の要件の組み合わせを考えます。(1) 順序を保って複数のアプリがログを読み直せる。(2) デプロイの直後の 10 分間だけ、担当者がログを流して見る。適切な手段はどれですか。

- A. (1) Kinesis Data Streams、(2) Live Tail
- B. (1) CloudWatch アラーム、(2) X-Ray
- C. (1) SQS の標準キュー、(2) Athena
- D. (1) Firehose の Lambda 変換、(2) `CreateExportTask` と S3 の閲覧

??? success "答えと解説"
    **正解: A**

    独自のコンシューマーと順序には Kinesis Data Streams です。調査の間だけ見るなら Live Tail です。

    - A: 正しい。
    - B: 誤り。ログを読む手段にならない。
    - C: 誤り。順序と読み直しができず、Athena もリアルタイムでない。
    - D: 誤り。Firehose は読み直しのコンシューマーを持たず、エクスポートはリアルタイムでない。

    **スキル:** [リアルタイムの取り込み](../domain4.md#t4-1-real-time) / **参照:** [Kinesis Data Streams、Firehose、SQS の選び方](../../../services/streaming.md#choosing)、[Live Tail](../../../services/observability.md#live-tail)

### 問3 {#q3}

Firehose で S3 へ配信しているログが、ダッシュボードに反映されるまでの遅れを短くします。形式の変換も Lambda で行います。設定の見直しとして適切なものはどれですか。

- A. 配信先を S3 から Glacier へ変える
- B. 転送の TLS を無効にして、配信を速くする
- C. Firehose のシャードの数を増やして、バッファの設定には触らずに配信の回数を増やす
- D. バッファの間隔とサイズを小さくし、変換の Lambda のタイムアウトを確認する

??? success "答えと解説"
    **正解: D**

    遅れは主にバッファで決まります。

    - A: 誤り。遅れは短くならず、読み取りが遅くなる。
    - B: 誤り。安全性を落とすだけで、遅れの原因ではない。
    - C: 誤り。Firehose のシャードの設定ではなく、バッファの問題が残る。
    - D: 正しい。

    **スキル:** [リアルタイムの取り込み](../domain4.md#t4-1-real-time) / **参照:** [バッファ](../../../services/streaming.md#firehose-buffering)、[Lambda による変換](../../../services/streaming.md#firehose-transform)

### 問4 {#q4}

Kinesis Data Streams のログを分析します。(1) レコードごとに特定の文字列で通知する。(2) 5 分の時間枠で IP ごとのアクセス数を集計し、連続して異常を判定する。適切な組み合わせはどれですか。

- A. (1) Firehose、(2) S3 のイベント通知
- B. (1) Lambda、(2) Managed Service for Apache Flink
- C. (1) Glue の ETL のバッチ、(2) Lambda の 1 回の呼び出しに 5 分間のデータをまとめる
- D. (1) Flink、(2) Athena の毎日のバッチ

??? success "答えと解説"
    **正解: B**

    イベントごとの判定は Lambda、時間枠の連続した集計は Flink です。

    - A: 誤り。どちらも分析の処理ではない。
    - B: 正しい。
    - C: 誤り。状態を持つ時間枠の集計に Lambda の単発の呼び出しは向かない。
    - D: 誤り。連続した分析にならない。

    **スキル:** [リアルタイムの分析](../domain4.md#t4-2-real-time-analysis) / **参照:** [Lambda とストリーム](../../../services/streaming.md#lambda-streams)、[Amazon Managed Service for Apache Flink](../../../services/data-engineering.md#flink)

### 問5 {#q5}

1 つの Kinesis のストリームを 5 つのアプリが読むようになると、`ReadProvisionedThroughputExceeded` が増えて遅れました。アプリごとに独立の読み取り量を確保します。どの機能を使いますか。

- A. ストリームの保持期間を 365 日に延ばす
- B. 拡張ファンアウト
- C. プロデューサーの `PutRecords` のバッチのサイズを大きくする
- D. パーティションキーを見直してシャードの偏りをなくす

??? success "答えと解説"
    **正解: B**

    標準のコンシューマーは読み取り量を共有します。拡張ファンアウトは各コンシューマーに専用の読み取り量を割り当てます。

    - A: 誤り。読み取りの速さに関係しない。
    - B: 正しい。
    - C: 誤り。書き込みの変更で、読み取りの競合を解消しない。
    - D: 誤り。偏りの問題ではなく、コンシューマーの数の問題。

    **スキル:** [リアルタイムの分析](../domain4.md#t4-2-real-time-analysis) / **参照:** [消費者と拡張ファンアウト](../../../services/streaming.md#enhanced-fan-out)、[エラーと監視](../../../services/streaming.md#kinesis-errors)

### 問6 {#q6}

Lambda のコンシューマーの `IteratorAgeMilliseconds` が増え続けます。CloudWatch で 1 つのシャードの処理だけ遅れており、書き込みのキーはサーバー名です。アクセスは 1 台に集中しています。適切な対応の組み合わせはどれですか。（2つ選択）

- A. イベントソースマッピングの `ParallelizationFactor` を増やす
- B. 関数の予約済み同時実行を 0 にする
- C. `IteratorAge` のアラームを削除する
- D. ストリームの保持期間を 1 時間に短くして、遅れたデータを捨てる
- E. パーティションキーを見直してシャードの偏りをなくす

??? success "答えと解説"
    **正解: A, E**

    偏りはキーの設計で解消します。シャードあたりの並列数も増やせます。

    - A: 正しい。
    - B: 誤り。処理が止まる。
    - C: 誤り。問題が見えなくなるだけ。
    - D: 誤り。データを失い、原因も解決しない。
    - E: 正しい。

    **スキル:** [リアルタイムの分析](../domain4.md#t4-2-real-time-analysis) / **参照:** [パーティションキー](../../../services/streaming.md#partition-key)、[Lambda とストリーム](../../../services/streaming.md#lambda-streams)

### 問7 {#q7}

Athena で CloudTrail のログを毎週分析しています。スキャン量が多く、費用がかかります。クエリの条件は日付とリージョンで、列の一部しか使いません。適切な最適化はどれですか。（2つ選択）

- A. 日付とリージョンでパーティションを切る
- B. Athena のクエリを Logs Insights へ切り替える
- C. クエリの結果を `SELECT *` にして、すべての列を表示する
- D. S3 のストレージクラスを Glacier Flexible Retrieval へ移す
- E. Parquet などの列指向の形式に変換する

??? success "答えと解説"
    **正解: A, E**

    パーティションと列指向の形式でスキャン量を減らせます。

    - A: 正しい。
    - B: 誤り。対象が S3 で、Logs Insights の対象ではない。
    - C: 誤り。スキャン量が増える。
    - D: 誤り。Athena からの読み取りができなくなる。
    - E: 正しい。

    **スキル:** [ログ分析](../domain4.md#t4-2-log-analysis) / **参照:** [速く、安くするコツ](../../../services/streaming.md#athena-performance)、[パーティションの設定](../../../services/streaming.md#athena-partitions)

### 問8 {#q8}

先月、特定のアクセスキーで呼ばれた API と IP の一覧を、組織の全アカウントで調べます。ログは 90 日以上あり、S3 の中央のバケットにあります。適切な手段はどれですか。

- A. CloudTrail のイベント履歴をアカウントごとのコンソールで検索する
- B. Config のアグリゲーターで、キーの使用の履歴を検索する
- C. Athena で CloudTrail のテーブルを作って `useridentity.accesskeyid` で絞る
- D. CloudWatch の `GetMetricData` でアクセスキーごとの API の呼び出しの数を集計して、IP を推定する

??? success "答えと解説"
    **正解: C**

    S3 の長期のログは Athena で問い合わせます。

    - A: 誤り。90 日までで、全アカウントの調査に手間がかかる。
    - B: 誤り。Config は API の呼び出しの履歴を持たない。
    - C: 正しい。
    - D: 誤り。API の履歴の項目をメトリクスで持たない。

    **スキル:** [ログ分析](../domain4.md#t4-2-log-analysis) / **参照:** [S3 上のログを問い合わせる](../../../services/streaming.md#athena-logs)、[CloudTrail の調査](../../../services/threat-detection.md#investigate-cloudtrail)

### 問9 {#q9}

Lambda の遅延の原因を調べます。ログの `REPORT` 行の `Duration` と `Max Memory Used` を関数のバージョンごとに集計し、直近 3 日の p95 を比べます。適切な手段はどれですか。

- A. Logs Insights の `stats pct(@duration, 95) by @logStream`
- B. Live Tail を開いて `REPORT` の行に絞り、3 日分の値を書き留めて集計する
- C. ログを S3 にエクスポートしてから、Athena の毎日のバッチで集計する
- D. X-Ray のアノテーションに `Max Memory Used` を手で書き込み、トレースの検索で集計する

??? success "答えと解説"
    **正解: A**

    Logs Insights はログの検出フィールドを使って集計できます。

    - A: 正しい。
    - B: 誤り。流れるログを見る機能で、過去 3 日の集計にならない。
    - C: 誤り。直近の調査には手間がかかる。
    - D: 誤り。既にログにあるものをコードの変更で残す手間がかかる。

    **スキル:** [ログ分析](../domain4.md#t4-2-log-analysis) / **参照:** [ログからボトルネックを見つける](../../../services/observability.md#logs-bottlenecks)、[Logs Insights でログを検索する](../../../services/observability.md#logs-insights)

### 問10 {#q10}

ALB のアクセスログは S3 に出力されます。届くたびに解析して OpenSearch Service へ入れます。Lambda は `AccessDenied` で失敗します。必要な権限と設定の組み合わせはどれですか。

- A. S3 のイベント通知と、関数の実行ロールに S3 の読み取りと OpenSearch への書き込み
- B. CloudTrail のデータイベントと、バケットの公開の読み取りの設定を組み合わせる
- C. ALB のアクセスログの設定に Lambda の ARN を直接書く設定
- D. サブスクリプションフィルターと、OpenSearch のドメインの公開アクセスの設定を組み合わせて入れる

??? success "答えと解説"
    **正解: A**

    S3 のイベント通知で起動します。Lambda のロールに読み取りと書き込みの権限が必要です。

    - A: 正しい。
    - B: 誤り。イベントの経路としては冗長で、公開も不適切。
    - C: 誤り。ALB のログの宛先は S3 で、Lambda を直接指定できない。
    - D: 誤り。S3 のログに使えず、公開も不適切。

    **スキル:** [S3 イベント](../domain4.md#t4-3-s3-logs) / **参照:** [Event Notifications](../../../services/s3.md#event-notifications)、[実行ロール](../../../services/lambda.md#execution-role)、[Amazon OpenSearch Service](../../../services/streaming.md#opensearch)

### 問11 {#q11}

CloudFront のログファイルが大量に届くと、S3 から直接呼ばれる Lambda の同時実行が上限に達し、失敗したファイルの処理が失われます。再試行と負荷の平準化を入れます。適切な構成はどれですか。

- A. S3 のイベント通知を SQS へ送り、Lambda のイベントソースマッピングと DLQ を使う
- B. S3 のイベント通知の宛先を SNS にして、Lambda を購読させるだけで再試行を任せる
- C. Lambda のメモリを最大にし、タイムアウトを 15 分にして 1 回の処理を速くする
- D. CloudFront のログを無効にして、代わりに WAF のログだけを見る

??? success "答えと解説"
    **正解: A**

    間に SQS を挟むと、再試行と負荷の平準化ができます。

    - A: 正しい。
    - B: 誤り。キューのバッファにならない。
    - C: 誤り。同時実行の問題の解決にならない。
    - D: 誤り。必要なログを失う。

    **スキル:** [S3 イベント](../domain4.md#t4-3-s3-logs) / **参照:** [S3 イベント通知](../../../services/messaging.md#s3-events)、[Lambda から使うときの設定](../../../services/messaging.md#sqs-lambda-settings)

### 問12 {#q12}

S3 に届く WAF のログのうち、`logs/` プレフィックスの `.gz` の新しいファイルだけを解析し、`BLOCK` の行だけを CloudWatch Logs へ書きます。同じ条件で 2 つの別の Lambda を動かす案は S3 で拒否されました。適切な設計はどれですか。（2つ選択）

- A. ログファイルを S3 Select の対象に登録し、自動で CloudWatch Logs へ配信する
- B. 同じイベント通知の条件を 2 つ作成するため、バケットを 2 つに分ける
- C. 複数の処理を動かすなら、EventBridge か SNS のファンアウトへ通知する
- D. ライフサイクルルールの実行の結果で Lambda を起動する
- E. イベント通知にプレフィックスとサフィックスを指定して絞り、関数で `PutLogEvents` を呼ぶ

??? success "答えと解説"
    **正解: C, E**

    同じ条件の重複は S3 のイベント通知では指定できません。EventBridge か SNS で複数の処理へ配ります。

    - A: 誤り。そのような配信の仕組みはない。
    - B: 誤り。別の仕組みで解決できるのに、データの置き場を分ける必要はない。
    - C: 正しい。
    - D: 誤り。新しいファイルの通知の仕組みではない。
    - E: 正しい。

    **スキル:** [S3 イベント](../domain4.md#t4-3-s3-logs) / **参照:** [Event Notifications](../../../services/s3.md#event-notifications)、[PutLogEvents の制限](../../../services/observability.md#put-log-events)
