# ストリーミングの問題集

対象の解説: [ストリーミングと分析](../../../services/streaming.md)、[Flink](../../../services/data-engineering.md#flink)

### 問1 {#q1}

クリックのイベントを S3 に Parquet で届けるだけで、独自の消費者コードは書きたくありません。数分の遅れは問題ありません。どのサービスを選びますか。

- A. Managed Service for Apache Flink の継続的なウィンドウ集計
- B. Kinesis Data Streams と独自の消費者アプリケーション
- C. Kinesis Video Streams のアーカイブ
- D. Amazon Data Firehose で変換して配信する

??? success "答えと解説"
    **正解: D**

    宛先に届けるのが目的なら Firehose です。バッファの分だけ遅れますが、コードの管理が不要です。

    - A: 誤り。状態を持つ処理の選択で、配信だけなら過剰です。
    - B: 誤り。消費者のコードの管理が必要になります。
    - C: 誤り。動画や音声のストリーム向けです。
    - D: 正しい。

    **スキル:** [1.1.4](../domain1.md#skill-1-1-4) / **参照:** [選び方](../../../services/streaming.md#choosing)、[Firehose](../../../services/streaming.md#firehose)

### 問2 {#q2}

不正検知の特徴量を計算する 2 つのチームが、同じ取引イベントをそれぞれのコードで順序どおりに読みます。遅延は秒単位にしたいです。取り込みのサービスはどれですか。

- A. SQS 標準キューに入れ、各チームが受信する
- B. Kinesis Data Streams を 2 つの消費者で読む
- C. Firehose で S3 に配信し、各チームが S3 を読む
- D. S3 に PUT し、イベント通知で各チームの Lambda を起動する

??? success "答えと解説"
    **正解: B**

    独自のコードで順序どおりに読み、複数の消費者を持つなら Kinesis Data Streams です。

    - A: 誤り。順序が保証されず、同じメッセージを複数のチームで読む用途にも向きません。
    - B: 正しい。
    - C: 誤り。バッファの分だけ遅れ、秒単位の要件に合いません。
    - D: 誤り。イベントの順序どおりの処理や複数の消費者には向きません。

    **スキル:** [1.1.4](../domain1.md#skill-1-1-4) / **参照:** [選び方](../../../services/streaming.md#choosing)、[Kinesis Data Streams](../../../services/streaming.md#kinesis-data-streams)

### 問3 {#q3}

工場のカメラ映像を取り込み、後から ML の推論に使います。取り込みに適したサービスはどれですか。

- A. Glue のストリーミングジョブ
- B. Amazon Data Firehose
- C. Kinesis Video Streams
- D. Amazon MSK と既存の Kafka のコード

??? success "答えと解説"
    **正解: C**

    カメラなどの動画や音声のストリームは Kinesis Video Streams で取り込みます。

    - A: 誤り。表形式などのレコードの変換が目的で、映像の取り込みの選択ではありません。
    - B: 誤り。映像のストリームを扱うサービスではありません。
    - C: 正しい。
    - D: 誤り。既存の Kafka の資産がある場面の選択です。映像向けの機能はありません。

    **スキル:** [1.1.4](../domain1.md#skill-1-1-4) / **参照:** [Kinesis Video Streams](../../../services/other-services.md#kinesis-video)

### 問4 {#q4}

既に Kafka のプロデューサーとコンシューマーのコードがあり、変更を抑えて AWS へ移します。取り込みのサービスはどれですか。

- A. Amazon MSK に接続先を切り替える
- B. Firehose に置き換える
- C. Kinesis Data Streams に書き直す
- D. SQS FIFO に置き換える

??? success "答えと解説"
    **正解: A**

    既存の Kafka のコードを活かすなら Amazon MSK です。

    - A: 正しい。
    - B: 誤り。Kafka のコードはそのまま使えず、消費者の処理も置き換えになります。
    - C: 誤り。コードの変更が大きくなります。
    - D: 誤り。Kafka の API とは別のもので、コードの書き直しが必要です。

    **スキル:** [1.1.4](../domain1.md#skill-1-1-4) / **参照:** [MSK との違い](../../../services/data-engineering.md#msk-vs-kinesis)

### 問5 {#q5}

同じパーティションキーに書き込みが集中し、Kinesis の一部のシャードで `ProvisionedThroughputExceededException` が出ています。ストリーム全体の使用量には余裕があります。対応はどれですか。

- A. 高カーディナリティのパーティションキーに変える
- B. Firehose の変換を有効にする
- C. 消費者に拡張ファンアウトを設定する
- D. シャードの保持期間を延ばす

??? success "答えと解説"
    **正解: A**

    キーの偏りで特定のシャードの上限を超えています。キーを分散させ、再試行にはバックオフを入れます。

    - A: 正しい。
    - B: 誤り。Firehose の設定は Kinesis のシャードの偏りを解決しません。
    - C: 誤り。拡張ファンアウトは読み取り側の機能で、書き込みの偏りを解決しません。
    - D: 誤り。保持期間は書き込みの上限に関係しません。

    **スキル:** [1.1.3](../domain1.md#skill-1-1-3) / **参照:** [Kinesis のエラー](../../../services/streaming.md#kinesis-errors)

### 問6 {#q6}

Lambda で Kinesis を読んで特徴量を計算しています。`IteratorAgeMilliseconds` が増え続けています。意味と対応の組み合わせとして正しいものはどれですか。

- A. S3 への配信が失敗している。Firehose のバッファを増やす
- B. データの保持期間が短い。Parquet に変える
- C. 書き込みが拒否されている。キーを分散する
- D. 消費が追いついていない。消費者を強化する

??? success "答えと解説"
    **正解: D**

    `IteratorAgeMilliseconds` の増加は、書き込みに消費が追いついていないことを示します。消費者の強化や拡張ファンアウトで対応します。

    - A: 誤り。Firehose は使っておらず、S3 の配信の話でもありません。
    - B: 誤り。データ形式と読み取りの遅れは別の問題です。
    - C: 誤り。書き込みの拒否は別の例外で示されます。この指標は読み取りの遅れを示します。
    - D: 正しい。

    **スキル:** [1.1.3](../domain1.md#skill-1-1-3) / **参照:** [Kinesis のエラー](../../../services/streaming.md#kinesis-errors)

### 問7 {#q7}

Firehose の Lambda 変換で、不要なレコードを捨て、それ以外を整形します。関数の戻り値の設定として正しいものはどれですか。

- A. 捨てる行の `result` を `Failed` にし、再試行させる
- B. 新しい `recordId` を割り当て、捨てる行は応答から除く
- C. `recordId` は入力のまま、捨てる行の `result` は `Dropped` にする
- D. 全レコードの `result` を `Ok` にして、捨てる行のデータを空にする

??? success "答えと解説"
    **正解: C**

    応答の `recordId` は入力と同じにし、`result` には `Ok`、`Dropped`、`ProcessingFailed` のいずれかを返します。

    - A: 誤り。`Failed` という値はありません。
    - B: 誤り。`recordId` は入力と同じにします。
    - C: 正しい。
    - D: 誤り。捨てるには `Dropped` を返します。

    **スキル:** [1.2.3](../domain1.md#skill-1-2-3) / **参照:** [Firehose の変換](../../../services/streaming.md#firehose-transform)

### 問8 {#q8}

Kinesis のイベントから、シャードごとに 5 分間の合計を計算します。別の DB は増やさず、Lambda のコードで実現したいです。何を使いますか。

- A. S3 のイベント通知を 5 分ごとに実行する
- B. イベントソースマッピングのタンブリングウィンドウを 300 秒にする
- C. Firehose のバッファを 300 秒にして Lambda 変換で合計する
- D. Lambda の予約済み同時実行を 300 にする

??? success "答えと解説"
    **正解: B**

    タンブリングウィンドウは 0〜900 秒の枠で状態を持って集計できます。シャードごとの短い集計に向きます。

    - A: 誤り。S3 のイベントにその設定はなく、Kinesis のレコードも読みません。
    - B: 正しい。
    - C: 誤り。バッファの単位で変換するだけで、状態を引き継ぐ集計の機能ではありません。
    - D: 誤り。同時実行の設定は時間の枠と無関係です。

    **スキル:** [1.2.3](../domain1.md#skill-1-2-3) / **参照:** [タンブリングウィンドウ](../../../services/lambda.md#esm-tumbling-window)、[Lambda とストリーム](../../../services/streaming.md#lambda-streams)

### 問9 {#q9}

取引のストリームと顧客のストリームを結合し、スライディングウィンドウで複雑に集計します。状態を保持したまま継続して処理します。最も適したサービスはどれですか。

- A. Firehose の Lambda 変換
- B. Athena の定期的なクエリ
- C. Managed Service for Apache Flink
- D. Lambda のタンブリングウィンドウ

??? success "答えと解説"
    **正解: C**

    複雑なウィンドウや結合を、状態を持って継続的に処理するなら Flink です。

    - A: 誤り。軽い整形向けで、ストリーム間の結合はできません。
    - B: 誤り。S3 のデータへの分析クエリで、継続的なストリームの処理ではありません。
    - C: 正しい。
    - D: 誤り。シャードごとの短い集計向けで、複雑な結合には向きません。

    **スキル:** [1.2.3](../domain1.md#skill-1-2-3) / **参照:** [Flink](../../../services/data-engineering.md#flink)

### 問10 {#q10}

既存の Spark のストリーミング処理のコードを、サーバーを管理せずに動かします。マイクロバッチで構いません。どれを選びますか。

- A. Firehose の Lambda 変換に移植する
- B. EMR のクラスターで Spark Structured Streaming を動かす
- C. Lambda のイベントソースマッピングに移植する
- D. Glue の Spark Streaming ジョブ

??? success "答えと解説"
    **正解: D**

    Glue の Spark Streaming はサーバーレスのマイクロバッチです。

    - A: 誤り。Spark のコードをそのまま動かせません。
    - B: 誤り。コードは動きますが、クラスターの管理が必要です。
    - C: 誤り。Spark のコードを動かす仕組みではありません。
    - D: 正しい。

    **スキル:** [1.2.3](../domain1.md#skill-1-2-3) / **参照:** [Glue のジョブ](../../../services/data-engineering.md#glue-jobs)

### 問11 {#q11}

センサーデータの取り込みです。要件は次のとおりです。すべてのレコードを S3 に保存し、さらに 1 分ごとの平均を計算してダッシュボードに出します。適切な組み合わせを選んでください。（2つ選択）

- A. CloudFormation のスタックで毎分集計する
- B. Kinesis Video Streams で数値のレコードを取り込む
- C. 全レコードを Glue Data Quality に送って平均を計算する
- D. Flink か Lambda のウィンドウで 1 分ごとに集計する
- E. Kinesis Data Streams で取り込む

??? success "答えと解説"
    **正解: D, E**

    取り込みを Kinesis Data Streams にまとめると、S3 への配信と集計を別々の消費者で処理できます。S3 への配信には Firehose を消費者として使えます。

    - A: 誤り。CloudFormation はインフラを定義するサービスです。
    - B: 誤り。動画と音声のサービスです。
    - C: 誤り。Glue Data Quality はデータの品質検査の機能です。
    - D: 正しい。時間の枠で集計できます。
    - E: 正しい。複数の消費者で同じデータを読めます。

    **スキル:** [1.1.4](../domain1.md#skill-1-1-4), [1.2.3](../domain1.md#skill-1-2-3) / **参照:** [選び方](../../../services/streaming.md#choosing)、[Flink](../../../services/data-engineering.md#flink)
