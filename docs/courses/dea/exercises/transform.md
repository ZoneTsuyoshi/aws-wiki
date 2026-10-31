# 変換と処理の問題集

対象の解説: [変換エンジン](../../../services/data-engineering.md#choosing-transform)、[データ形式](../../../services/data-engineering.md#data-formats)、[Amazon Data Firehose](../../../services/streaming.md#firehose)

### 問1 {#q1}

Redshift の顧客テーブルと、S3 にある 5 年分のクリックログを結合します。ログはほとんど読まないので、Redshift へはロードしません。何を使いますか。

- A. Redshift Spectrum の外部テーブルと結合する
- B. データ共有で S3 のログを Redshift に共有する
- C. フェデレーテッドクエリで S3 のファイルに接続する
- D. `COPY` で全ログを Redshift へロードしてから結合する

??? success "答えと解説"
    **正解: A**

    Spectrum はロードせずに S3 を読み、ローカルのテーブルと結合できます。

    - A: 正しい。
    - B: 誤り。データ共有は Redshift のデータ同士の機能です。
    - C: 誤り。対象は RDS と Aurora の PostgreSQL と MySQL です。
    - D: 誤り。要件に反して、ストレージも増えます。

    **スキル:** [1.2.3](../domain1.md#skill-1-2-3) / **参照:** [Spectrum とデータレイクのクエリ](../../../services/data-engineering.md#redshift-spectrum)、[データを取り込む他の方法](../../../services/data-engineering.md#redshift-ingestion)

### 問2 {#q2}

Aurora MySQL の運用データを Redshift で分析します。ETL の開発と運用をせず、ほぼリアルタイムにしたいです。最も適切なものはどれですか。

- A. DMS のタスクを作成し、Aurora の binlog から定期的に読む
- B. Aurora から Redshift へのゼロ ETL 統合
- C. Glue ジョブを 1 時間ごとに動かし、JDBC で差分を読む
- D. Aurora のスナップショットを S3 へエクスポートして `COPY` する

??? success "答えと解説"
    **正解: B**

    ゼロ ETL 統合はパイプラインなしで複製します。

    - A: 誤り。動きますが、タスクの運用が残ります。
    - B: 正しい。
    - C: 誤り。ジョブの開発が必要で、ほぼリアルタイムになりません。
    - D: 誤り。定期的なバッチで、手順も増えます。

    **スキル:** [1.2.3](../domain1.md#skill-1-2-3) / **参照:** [データを取り込む他の方法](../../../services/data-engineering.md#redshift-ingestion)、[変換エンジン](../../../services/data-engineering.md#choosing-transform)

### 問3 {#q3}

気象会社の有償のデータセットを購読し、自社の販売データと結合します。ファイル受け渡しの独自の仕組みは作りません。何を使いますか。

- A. AppFlow のスケジュールで、気象会社の S3 を直接読む
- B. Lake Formation のクロスアカウント共有を、購読の契約として使う
- C. AWS Data Exchange で購読する
- D. AWS Clean Rooms で購読する

??? success "答えと解説"
    **正解: C**

    Data Exchange は第三者のデータの購読に使います。

    - A: 誤り。AppFlow は SaaS の連携で、データの購読の仕組みではありません。
    - B: 誤り。販売や購読の仕組みではありません。
    - C: 正しい。
    - D: 誤り。互いのデータを見せずに共同で分析するためのサービスです。

    **スキル:** [1.2.3](../domain1.md#skill-1-2-3) / **参照:** [AWS Data Exchange](../../../services/data-engineering.md#data-exchange)、[データの共有](../../../services/data-engineering.md#choosing-sharing)

### 問4 {#q4}

夜間の Glue ジョブは、数時間の遅れがあってもかまいません。費用を下げるために変更するのはどれですか。

- A. リトライ回数を 10 にする
- B. ワーカータイプを `R` タイプにする
- C. 実行クラスを Standard のままにし、ワーカー数を 2 倍にする
- D. 実行クラスを Flex にする

??? success "答えと解説"
    **正解: D**

    Flex は開始が遅れることがありますが、急がないジョブを安くします。

    - A: 誤り。失敗時の再実行で、費用は増える方向です。
    - B: 誤り。メモリ集約のためのタイプで、費用を下げる設定ではありません。
    - C: 誤り。DPU が増え、費用削減の目的に合いません。
    - D: 正しい。

    **スキル:** [1.2.4](../domain1.md#skill-1-2-4) / **参照:** [ETL ジョブ](../../../services/data-engineering.md#glue-jobs)

### 問5 {#q5}

毎日 2 時間の Spark ジョブを EMR on EC2 で動かします。クラスターは常時起動で、タスクノードは On-Demand です。データは S3 にあります。費用を減らす変更はどれですか。（2つ選択）

- A. タスクノードを Spot にする
- B. ジョブごとにクラスターを起動して終了する一時クラスターにする
- C. プライマリノードを 3 台にして、処理を分散する
- D. 終了保護を有効にして、不要な終了を防ぐ
- E. コアノードも含めて全ノードを Spot にし、HDFS を入出力に使う

??? success "答えと解説"
    **正解: A, B**

    入出力が S3 なら、一時クラスターと Spot の組み合わせが使えます。

    - A: 正しい。タスクノードは HDFS を持たず、Spot に向いています。
    - B: 正しい。費用はジョブの時間分だけになります。
    - C: 誤り。可用性のための構成で、処理は分散されず費用も増えます。
    - D: 誤り。終了を拒否する設定で、費用は下がりません。
    - E: 誤り。中断でブロックを失い、ジョブが失敗します。

    **スキル:** [1.2.4](../domain1.md#skill-1-2-4) / **参照:** [スケーリングと終了](../../../services/data-engineering.md#emr-scaling)、[クラスターのノード](../../../services/data-engineering.md#emr-nodes)

### 問6 {#q6}

Firehose の費用を調べると、1 件 300 バイトのレコードを 1 件ずつ大量に送っていました。費用の面で効果がある変更はどれですか。

- A. 配信先の S3 のストレージクラスを変更する
- B. レコードを 1 件ずつ別のストリームに送り、負荷を分ける
- C. 送信側で小さなレコードをまとめ、5 KB に近い単位で送る
- D. バッファのサイズを大きくして、配信の頻度を下げる

??? success "答えと解説"
    **正解: C**

    Firehose は 5 KB 単位に切り上げて課金されます。

    - A: 誤り。ストレージの費用で、取り込みの費用は変わりません。
    - B: 誤り。5 KB 単位の切り上げは変わりません。
    - C: 正しい。
    - D: 誤り。取り込みの課金単位は変わりません。

    **スキル:** [1.2.4](../domain1.md#skill-1-2-4) / **参照:** [形式と料金](../../../services/streaming.md#athena-formats-cost)、[Amazon Data Firehose](../../../services/streaming.md#firehose)

### 問7 {#q7}

既存の Spark のコードと特定の EMR リリースをそのまま使います。クラスターの運用はしません。Spot の調整も不要です。何を選びますか。

- A. Glue の Python shell ジョブ
- B. EMR on EC2
- C. EMR on EKS
- D. EMR Serverless

??? success "答えと解説"
    **正解: D**

    EMR Serverless はリリースを指定し、クラスターなしで動かせます。

    - A: 誤り。Spark ではなく、EMR のリリースも指定できません。
    - B: 誤り。クラスターとノードの運用が残ります。
    - C: 誤り。EKS クラスターの運用が必要です。
    - D: 正しい。

    **スキル:** [1.2.5](../domain1.md#skill-1-2-5) / **参照:** [変換エンジン](../../../services/data-engineering.md#choosing-transform)

### 問8 {#q8}

アナリストが画面の操作だけで CSV の欠損を埋め、列を分割し、同じ手順を毎週適用します。コードは書けません。何を選びますか。

- A. DataBrew のレシピとレシピジョブ
- B. Athena の CTAS を週次で実行する
- C. Lambda の Python 関数をスケジュールで起動する
- D. Glue の Spark ジョブのスクリプト

??? success "答えと解説"
    **正解: A**

    DataBrew は視覚的に整形し、手順をレシピとして再利用できます。

    - A: 正しい。
    - B: 誤り。SQL の記述が必要です。
    - C: 誤り。コードの作成が必要です。
    - D: 誤り。コードの作成が必要です。

    **スキル:** [1.2.5](../domain1.md#skill-1-2-5) / **参照:** [変換エンジン](../../../services/data-engineering.md#choosing-transform)、[DataBrew](../../../services/data-engineering.md#databrew)

### 問9 {#q9}

S3 に届く 2 GB の JSON を変換します。処理は Python で 40 分かかり、毎日 1 回です。運用は最小にします。適切な実行先はどれですか。

- A. Firehose の Lambda 変換
- B. Glue の Python shell か Spark のジョブ
- C. API Gateway の統合
- D. Lambda 関数

??? success "答えと解説"
    **正解: B**

    15 分を超える変換は Glue などへ任せます。

    - A: 誤り。ストリームのレコードの変換で、呼び出しの上限も 5 分です。
    - B: 正しい。
    - C: 誤り。統合のタイムアウトは既定で 29 秒で、変換の実行先ではありません。
    - D: 誤り。実行時間の上限は 15 分です。

    **スキル:** [1.2.5](../domain1.md#skill-1-2-5) / **参照:** [メモリ](../../../services/lambda.md#memory)、[変換エンジン](../../../services/data-engineering.md#choosing-transform)

### 問10 {#q10}

Spark の ETL で、カタログとの連携、ジョブブックマーク、Data Quality を使い、サーバーも持ちません。どれが最も適切ですか。

- A. Redshift の SQL によるストアドプロシージャ
- B. EMR Serverless の Spark アプリケーション
- C. Managed Service for Apache Flink のアプリケーション
- D. Glue の Spark ジョブをカタログと一緒に使う

??? success "答えと解説"
    **正解: D**

    Glue は、カタログと一体の ETL が要るときに選びます。

    - A: 誤り。Spark の ETL ではありません。
    - B: 誤り。ブックマークや Data Quality の機能はありません。
    - C: 誤り。ストリームの状態付き処理に向きます。
    - D: 正しい。

    **スキル:** [1.2.5](../domain1.md#skill-1-2-5) / **参照:** [変換エンジン](../../../services/data-engineering.md#choosing-transform)、[Data Quality](../../../services/data-engineering.md#glue-data-quality)

### 問11 {#q11}

S3 の CSV のログを Athena で週に数回読みます。列は 200 ありますが、毎回 5 列しか使いません。スキャン量を減らす形式はどれですか。

- A. 非圧縮の Avro
- B. Snappy で圧縮した Parquet
- C. gzip で圧縮した CSV
- D. 改行区切りの JSON

??? success "答えと解説"
    **正解: B**

    列指向は必要な列だけ読むので、スキャン量が減ります。

    - A: 誤り。行形式なので全列を読みます。
    - B: 正しい。
    - C: 誤り。圧縮はされますが、全列を読み、分割もできません。
    - D: 誤り。行形式なので全列を読みます。

    **スキル:** [1.2.6](../domain1.md#skill-1-2-6) / **参照:** [データ形式](../../../services/data-engineering.md#data-formats)、[形式と料金](../../../services/streaming.md#athena-formats-cost)

### 問12 {#q12}

Firehose で受けた JSON を、Parquet で S3 へ保存します。コードは書きません。必要な設定はどれですか。

- A. レコード形式の変換を有効にし、Glue Data Catalog のテーブルのスキーマを指定する
- B. 配信先のファイル拡張子を `.parquet` にし、圧縮を gzip にする
- C. Glue のクローラーを Firehose ストリームに直接向けて、形式を決めさせる
- D. `COPY` の `FORMAT AS PARQUET` を Firehose の設定に書く

??? success "答えと解説"
    **正解: A**

    形式の変換には Glue Data Catalog のスキーマが必要です。

    - A: 正しい。
    - B: 誤り。形式は変換されません。
    - C: 誤り。クローラーはストリーミングのソースに使えません。
    - D: 誤り。Redshift へのロードのオプションです。

    **スキル:** [1.2.6](../domain1.md#skill-1-2-6) / **参照:** [その他の機能](../../../services/streaming.md#firehose-features)

### 問13 {#q13}

一度だけ、CSV のテーブルをパーティション付きの Parquet へ変換します。新しいジョブやクラスターは作りません。何を使いますか。

- A. Athena の `CREATE VIEW` に `format = 'PARQUET'` を指定する
- B. EMR のクラスターを起動して Hive で `INSERT OVERWRITE` する
- C. Athena の CTAS で `format = 'PARQUET'` と `partitioned_by` を指定する
- D. `ALTER TABLE ADD PARTITION` で形式を指定する

??? success "答えと解説"
    **正解: C**

    単発の変換は Athena の CTAS が手軽です。

    - A: 誤り。ビューはデータを書きません。
    - B: 誤り。クラスターを作るので要件に合いません。
    - C: 正しい。
    - D: 誤り。パーティションの追加で、既存のファイルは変わりません。

    **スキル:** [1.2.6](../domain1.md#skill-1-2-6) / **参照:** [データ形式](../../../services/data-engineering.md#data-formats)、[パーティションの設定](../../../services/streaming.md#athena-partitions)

### 問14 {#q14}

Glue ジョブのエグゼキューターが、結合と集計のステージで OOM になります。ドライバーは正常で、ファイル数は少ないです。適切な対処はどれですか。

- A. ジョブのタイムアウトを 2,880 分に延ばす
- B. `groupFiles` を `inPartition` にする
- C. メモリの多い `R` タイプのワーカーへ変える
- D. ジョブのブックマークを有効にする

??? success "答えと解説"
    **正解: C**

    シャッフルや集計が重いときは `R` タイプか大きなワーカーにします。

    - A: 誤り。時間の上限で、メモリの不足は解消しません。
    - B: 誤り。小さなファイルが多いドライバーの OOM への対処です。
    - C: 正しい。
    - D: 誤り。処理対象の追跡で、メモリには直接効きません。

    **スキル:** [1.2.7](../domain1.md#skill-1-2-7) / **参照:** [DPU とワーカータイプ](../../../services/data-engineering.md#glue-dpu)

### 問15 {#q15}

同じ Glue ジョブを別のパラメータで同時に 2 つ起動すると、2 つ目がエラーになります。ブックマークは使っていません。どうしますか。

- A. ジョブの最大同時実行数を 2 以上に上げる
- B. ジョブのタイムアウトを短くして、1 つ目を早く終わらせる
- C. リトライ回数を 10 に上げ、2 つ目が成功するまで待つ
- D. ワーカー数を 2 倍にして、同時に処理できるようにする

??? success "答えと解説"
    **正解: A**

    最大同時実行数の既定は 1 です。

    - A: 正しい。
    - B: 誤り。同時に起動するという要件を満たしません。
    - C: 誤り。根本の制限が残ります。
    - D: 誤り。同時実行の上限はワーカー数と別です。

    **スキル:** [1.2.7](../domain1.md#skill-1-2-7) / **参照:** [ETL ジョブ](../../../services/data-engineering.md#glue-jobs)、[ジョブのブックマーク](../../../services/data-engineering.md#glue-bookmarks)

### 問16 {#q16}

`COPY` が `Load into table failed` で失敗しました。どの行のどの列で失敗したかを調べる場所はどれですか。（2つ選択）

- A. `STL_LOAD_ERRORS`
- B. `SYS_LOAD_ERROR_DETAIL`
- C. `SVV_TABLE_INFO`
- D. `STV_LOCKS`
- E. `STL_TR_CONFLICT`

??? success "答えと解説"
    **正解: A, B**

    ロードのエラーはこの 2 つで確認します。

    - A: 正しい。ロードのエラーの詳細を確認できます。
    - B: 正しい。ロードのエラーの詳細を確認できます。
    - C: 誤り。テーブルの統計や偏りを表示します。
    - D: 誤り。現在のテーブルのロックを表示します。
    - E: 誤り。トランザクションの競合の履歴です。

    **スキル:** [1.2.7](../domain1.md#skill-1-2-7) / **参照:** [COPY と UNLOAD](../../../services/data-engineering.md#redshift-copy)

### 問17 {#q17}

Firehose の Lambda 変換で、関数が 7 分かかるレコードのバッチがあり、変換の失敗が続きます。原因として正しいものはどれですか。

- A. Lambda のタイムアウトの既定が 15 分なので、Firehose が先に待ちきれなくなる
- B. Firehose のバッファのサイズが小さいと、Lambda の実行時間が自動で切り詰められる
- C. Firehose は Lambda の変換を 1 分までしか待たない
- D. Firehose が対応する Lambda の呼び出し時間は最大 5 分である

??? success "答えと解説"
    **正解: D**

    5 分を超えると Firehose はタイムアウトのエラーとして扱います。

    - A: 誤り。Lambda の既定は 3 秒で、最大が 15 分です。
    - B: 誤り。バッファのサイズで実行時間は切り詰められません。
    - C: 誤り。上限は 5 分です。
    - D: 正しい。

    **スキル:** [1.2.7](../domain1.md#skill-1-2-7) / **参照:** [配信の失敗の扱い](../../../services/streaming.md#firehose-failure)、[Lambda による変換](../../../services/streaming.md#firehose-transform)

### 問18 {#q18}

次のデータの置き場として適切な組み合わせはどれですか。売上テーブル、JSON のアプリログ、契約書の PDF。

- A. 売上は S3 のみ、ログは Redshift の行、PDF は DynamoDB の項目
- B. 売上は Redshift、ログは OpenSearch か S3、PDF は S3
- C. 売上は OpenSearch、ログは RDS、PDF は Neptune
- D. 売上は DynamoDB、ログは MemoryDB、PDF は Redshift

??? success "答えと解説"
    **正解: B**

    構造化は RDS や Redshift、半構造化は S3、DynamoDB、OpenSearch、非構造化は S3 です。

    - A: 誤り。種類に合いません。PDF は項目のサイズの上限にも当たります。
    - B: 正しい。
    - C: 誤り。Neptune はグラフで、PDF の保存には向きません。
    - D: 誤り。分析、ログ、ファイルのいずれにも合いません。

    **スキル:** [1.2.9](../domain1.md#skill-1-2-9) / **参照:** [データストアの選び方](../../../services/databases.md#choosing-data-store)、[データ形式](../../../services/data-engineering.md#data-formats)

### 問19 {#q19}

1 日 1 回 1 GB を受けていたパイプラインが、新しい要件で秒間数万件のイベントを数秒以内に処理します。データの 3V のうち主にどれが変わり、どの変更が必要ですか。

- A. 量。保存先を階層化ストレージへ移すだけで済ませる
- B. 速度。バッチからストリームの構成へ変える
- C. 種類。JSON を CSV に変えれば、バッチのままで間に合う
- D. 種類。データの形が増えるので、スキーマの管理だけを追加する

??? success "答えと解説"
    **正解: B**

    速度はバッチかストリームか、シャード数、バッファの判断に効きます。

    - A: 誤り。数秒以内の処理を満たせません。
    - B: 正しい。
    - C: 誤り。形式の変更では処理の遅延は解決しません。
    - D: 誤り。問題文で変わるのは速さで、形は変わっていません。

    **スキル:** [1.2.9](../domain1.md#skill-1-2-9) / **参照:** [キャパシティモード](../../../services/streaming.md#capacity-modes)、[変換エンジン](../../../services/data-engineering.md#choosing-transform)

### 問20 {#q20}

ペタバイト級へ増えるクリックログを、S3 上で分析します。量の増加に合わせる設計として適切なものはどれですか。（2つ選択）

- A. ユーザー ID でパーティションを切り、細かく分ける
- B. 列指向の形式で保存する
- C. 日付などのよく絞る列でパーティションを切る
- D. 分析の前に全データを 1 台の EC2 のローカルディスクへコピーする
- E. 全データを 1 つの大きな gzip ファイルにまとめる

??? success "答えと解説"
    **正解: B, C**

    量には分散処理、列指向、パーティション、階層化ストレージで対応します。

    - A: 誤り。小さなファイルと多数のパーティションで遅くなります。
    - B: 正しい。必要な列だけ読むので、量が増えてもスキャン量を抑えられます。
    - C: 正しい。読む範囲を減らせます。
    - D: 誤り。1 台に収まらない量には向きません。
    - E: 誤り。分割して読めないので、並列処理が効きません。

    **スキル:** [1.2.9](../domain1.md#skill-1-2-9) / **参照:** [パーティション](../../../services/data-engineering.md#partitioning)、[データ形式](../../../services/data-engineering.md#data-formats)
