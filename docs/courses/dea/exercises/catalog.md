# データカタログとスキーマの問題集

対象の解説: [Data Catalog](../../../services/data-engineering.md#glue-data-catalog)、[パーティションの同期](../../../services/data-engineering.md#partition-sync)

### 問1 {#q1}

Glue Data Catalog の `sales.orders` を削除しました。S3 の Parquet ファイルはどうなりますか。

- A. 消える。テーブルの削除は S3 のオブジェクトも同時に削除する
- B. 残る。カタログはメタデータだけを持つ
- C. 暗号化される。テーブルの削除で KMS の鍵が変更される
- D. Glacier へ移る。テーブルの削除でライフサイクルが起動する

??? success "答えと解説"
    **正解: B**

    テーブルの定義を消しても S3 のファイルは消えません。

    - A: 誤り。データ本体は S3 に残ります。
    - B: 正しい。
    - C: 誤り。関係しません。
    - D: 誤り。削除で移行は起きません。

    **スキル:** [2.2.1](../domain2.md#skill-2-2-1) / **参照:** [Data Catalog](../../../services/data-engineering.md#glue-data-catalog)

### 問2 {#q2}

Glue Data Catalog の定義を Redshift から使います。コピーせずに参照する文はどれですか。

- A. `CREATE EXTERNAL SCHEMA lake FROM DATA CATALOG DATABASE 'lake' IAM_ROLE default;`
- B. `CREATE DATASHARE lake; ALTER DATASHARE lake ADD SCHEMA public;`
- C. `COPY lake FROM 's3://lake/' IAM_ROLE default;`
- D. `MSCK REPAIR TABLE lake;`

??? success "答えと解説"
    **正解: A**

    外部スキーマでカタログを参照します。

    - A: 正しい。
    - B: 誤り。Redshift のデータ共有です。
    - C: 誤り。データをロードします。
    - D: 誤り。Hive 形式のパーティションの同期です。

    **スキル:** [2.2.1](../domain2.md#skill-2-2-1) / **参照:** [Spectrum とデータレイクのクエリ](../../../services/data-engineering.md#redshift-spectrum)、[Data Catalog](../../../services/data-engineering.md#glue-data-catalog)

### 問3 {#q3}

別のアカウントの Athena から、共有されたカタログのテーブルを自分のカタログのように参照します。何を作りますか。

- A. Redshift のデータ共有で Glue のテーブルを共有する
- B. 自分のアカウントのクローラーで相手の S3 を読み、テーブルを複製する
- C. Lake Formation で共有を受け、リソースリンクを作る
- D. 自分のアカウントの Hive メタストアへカタログをエクスポートする

??? success "答えと解説"
    **正解: C**

    共有先でリソースリンクを作ります。

    - A: 誤り。Redshift の機能です。
    - B: 誤り。定義を複製し、権限も別管理になります。
    - C: 正しい。
    - D: 誤り。複製で、運用も増えます。

    **スキル:** [2.2.1](../domain2.md#skill-2-2-1) / **参照:** [クロスアカウント共有](../../../services/data-engineering.md#lake-formation-cross-account)、[Data Catalog](../../../services/data-engineering.md#glue-data-catalog)

### 問4 {#q4}

新規のデータレイクで Athena、EMR、Spectrum のメタデータを共有します。サーバーの運用はしません。何を選びますか。

- A. DynamoDB に自作したメタデータのテーブル
- B. EC2 上に自分で構築した Apache Hive メタストア
- C. EMR のプライマリノードの中のローカルメタストア
- D. Glue Data Catalog

??? success "答えと解説"
    **正解: D**

    Glue Data Catalog はサーバーレスです。

    - A: 誤り。エンジンから直接参照できません。
    - B: 誤り。サーバーの運用が必要です。
    - C: 誤り。クラスターの終了で失われます。
    - D: 正しい。

    **スキル:** [2.2.2](../domain2.md#skill-2-2-2) / **参照:** [Data Catalog](../../../services/data-engineering.md#glue-data-catalog)

### 問5 {#q5}

技術カタログとビジネスカタログの説明で正しいものはどれですか。

- A. ビジネスカタログは S3 のファイル本体を保存する場所である
- B. 技術カタログは人だけが使い、エンジンからは参照できない
- C. 技術カタログは型や場所を持ち、ビジネスカタログは意味、所有者、申請の流れを持つ
- D. 技術カタログは申請の流れと所有者を持ち、ビジネスカタログはテーブルの型と場所を持つ

??? success "答えと解説"
    **正解: C**

    使う相手の違いで考えます。

    - A: 誤り。データ本体は保存しません。
    - B: 誤り。エンジン向けです。
    - C: 正しい。
    - D: 誤り。逆です。

    **スキル:** [2.2.2](../domain2.md#skill-2-2-2) / **参照:** [Data Catalog](../../../services/data-engineering.md#glue-data-catalog)、[DataZone と SageMaker Unified Studio](../../../services/data-engineering.md#datazone-unified-studio)

### 問6 {#q6}

既存の Hadoop 環境で Apache Hive メタストアを運用しています。EMR を増やすにあたり、メタストアの運用をやめたいです。どうしますか。

- A. EMR で Hive メタストアの代わりに Glue Data Catalog を参照する
- B. メタストアをやめて、テーブルの定義をすべて SQL ファイルで管理する
- C. Hive のテーブルをすべて DynamoDB に移し、Athena や Spectrum からは使わない
- D. EMR の各クラスターに同じメタストアのコピーを持たせて手で同期する

??? success "答えと解説"
    **正解: A**

    EMR は Hive メタストアの代わりにカタログを使えます。

    - A: 正しい。
    - B: 誤り。エンジンが参照できません。
    - C: 誤り。分析の要件に合いません。
    - D: 誤り。運用が増えます。

    **スキル:** [2.2.2](../domain2.md#skill-2-2-2) / **参照:** [Data Catalog](../../../services/data-engineering.md#glue-data-catalog)、[クラスターのノード](../../../services/data-engineering.md#emr-nodes)

### 問7 {#q7}

日付のフォルダが毎日増えます。新しいフォルダだけ読み、既存のテーブルは変更しません。どの設定ですか。

- A. `AddOrUpdateBehavior` を `InheritFromTable` にする
- B. `TableGroupingPolicy` を `CombineCompatibleSchemas` にする
- C. テーブル数のしきい値を 1 にする
- D. 再クロールポリシーを `CRAWL_NEW_FOLDERS_ONLY` にする

??? success "答えと解説"
    **正解: D**

    更新と削除の動作は `LOG` に固定されます。

    - A: 誤り。パーティションのスキーマの設定です。
    - B: 誤り。テーブルをまとめる設定です。
    - C: 誤り。テーブルの作成数の上限です。
    - D: 正しい。

    **スキル:** [2.2.3](../domain2.md#skill-2-2-3) / **参照:** [クローラー](../../../services/data-engineering.md#glue-crawlers)

### 問8 {#q8}

データエンジニアがカタログの列の型を手で直しましたが、クローラーの実行で元に戻ります。手の修正を残す設定はどれですか。

- A. S3 イベント通知を有効にして、変更のあるフォルダだけ読む
- B. スキーマ変更ポリシーの `UpdateBehavior` を `LOG` にする
- C. `DeleteBehavior` を `DEPRECATE_IN_DATABASE` にする
- D. テーブルレベルを 1 つ深くして、パスの階層を変更する

??? success "答えと解説"
    **正解: B**

    `LOG` なら定義を更新しません。

    - A: 誤り。一覧の範囲の設定です。
    - B: 正しい。
    - C: 誤り。削除の検出時の動作です。
    - D: 誤り。テーブルを作る深さの設定です。

    **スキル:** [2.2.3](../domain2.md#skill-2-2-3) / **参照:** [クローラー](../../../services/data-engineering.md#glue-crawlers)

### 問9 {#q9}

1 つのプレフィックスの下のフォルダごとに、別々のテーブルが大量に作られました。スキーマは互換性があります。どう直しますか。

- A. `MergeNewColumns` を設定する
- B. 再クロールポリシーを `CRAWL_NEW_FOLDERS_ONLY` にして、新しいフォルダだけ読む
- C. `UpdateBehavior` を `LOG` にする
- D. `TableGroupingPolicy` を `CombineCompatibleSchemas` にする

??? success "答えと解説"
    **正解: D**

    互換性のあるデータを 1 つのテーブルにまとめます。

    - A: 誤り。列の追加の設定です。
    - B: 誤り。既に別々になる動作は直りません。
    - C: 誤り。定義の更新の設定です。
    - D: 正しい。

    **スキル:** [2.2.3](../domain2.md#skill-2-2-3) / **参照:** [クローラー](../../../services/data-engineering.md#glue-crawlers)

### 問10 {#q10}

クローラーの説明で正しいものはどれですか。（2つ選択）

- A. パーティションは追加できず、テーブルしか作らない
- B. S3 イベント通知を使うと、変更のあったフォルダだけを一覧できる
- C. 実行のたびに S3 のデータを Parquet へ変換する
- D. `MergeNewColumns` は既存の列の型も変更する
- E. ストリーミングのソースには使えないので、テーブルは手動で定義する

??? success "答えと解説"
    **正解: B, E**

    クローラーの役割はスキーマの推定です。

    - A: 誤り。パーティションも作ります。
    - B: 正しい。全件の一覧を避けられます。
    - C: 誤り。変換はしません。
    - D: 誤り。既存の列は変えません。
    - E: 正しい。Kinesis や Kafka のテーブルは手動です。

    **スキル:** [2.2.3](../domain2.md#skill-2-2-3) / **参照:** [クローラー](../../../services/data-engineering.md#glue-crawlers)、[Kinesis Data Streams](../../../services/streaming.md#kinesis-data-streams)

### 問11 {#q11}

Athena で、新しい `dt=` のフォルダのデータが結果に出ません。Hive 形式で、件数は少なく、手動で十分です。どの文ですか。

- A. `MSCK REPAIR TABLE orders;`
- B. `REFRESH MATERIALIZED VIEW orders;`
- C. `CREATE VIEW orders AS SELECT * FROM orders;`
- D. `VACUUM orders;`

??? success "答えと解説"
    **正解: A**

    S3 に作ってもカタログには自動で載りません。

    - A: 正しい。
    - B: 誤り。マテリアライズドビューの更新です。
    - C: 誤り。パーティションは同期されません。
    - D: 誤り。Redshift の領域の回収です。

    **スキル:** [2.2.4](../domain2.md#skill-2-2-4) / **参照:** [パーティションの同期](../../../services/data-engineering.md#partition-sync)

### 問12 {#q12}

パスが `s3://lake/2026/10/31/` で、Hive 形式（`key=value`）ではありません。新しい日のパーティションを 1 つ手動で追加します。どの方法ですか。

- A. `REFRESH MATERIALIZED VIEW` を実行して、新しいパスを読ませる
- B. `MSCK REPAIR TABLE` を実行する
- C. `ALTER TABLE ADD PARTITION` で場所を指定する
- D. クエリの `WHERE` に `dt` の値を書く

??? success "答えと解説"
    **正解: C**

    Hive 形式以外は明示的に追加します。

    - A: 誤り。別の機能です。
    - B: 誤り。Hive 形式のフォルダを走査します。
    - C: 正しい。
    - D: 誤り。登録されていないパーティションは読めません。

    **スキル:** [2.2.4](../domain2.md#skill-2-2-4) / **参照:** [パーティションの同期](../../../services/data-engineering.md#partition-sync)

### 問13 {#q13}

数年分の時間単位のパーティションがあり、Athena の計画に時間がかかります。値の形は規則的で、追加の作業はなくします。どれが適切ですか。

- A. パーティションを廃止して、全データを 1 つのフォルダへ移動する
- B. パーティション射影を有効にし、値の範囲と形をテーブルに書く
- C. クローラーを毎分実行するようにスケジュールを設定する
- D. 毎時 `MSCK REPAIR TABLE` を実行するスケジュールを作成する

??? success "答えと解説"
    **正解: B**

    値をテーブルのプロパティから計算します。

    - A: 誤り。スキャン量が増えます。
    - B: 正しい。
    - C: 誤り。費用がかかり、計画の遅さも解決しません。
    - D: 誤り。件数が多いと遅く、作業が残ります。

    **スキル:** [2.2.4](../domain2.md#skill-2-2-4) / **参照:** [パーティションの設定](../../../services/streaming.md#athena-partitions)、[パーティションの同期](../../../services/data-engineering.md#partition-sync)

### 問14 {#q14}

Glue ジョブの書き込みの最後に、新しいパーティションを確実にカタログへ反映します。クローラーは使いません。どの設定ですか。

- A. `groupFiles` を `inPartition` にして、書き込みの最後にカタログを更新するようにする
- B. `push_down_predicate` を指定する
- C. `transformation_ctx` を削除する
- D. `enableUpdateCatalog` を `True` にし、`partitionKeys` を指定する

??? success "答えと解説"
    **正解: D**

    書き込みと同時に追加できます。

    - A: 誤り。読み取りのグループ化です。
    - B: 誤り。読み取りの絞り込みです。
    - C: 誤り。ブックマークの設定で、削除すると悪影響があります。
    - D: 正しい。

    **スキル:** [2.2.4](../domain2.md#skill-2-2-4) / **参照:** [パーティションの同期](../../../services/data-engineering.md#partition-sync)

### 問15 {#q15}

同じ RDS を読むクローラーと 3 つのジョブがあります。接続情報を 1 か所で管理します。何を使いますか。

- A. S3 のバケットポリシーに JDBC の URL を保存する
- B. Glue 接続を作り、クローラーとジョブで再利用する
- C. ジョブごとに別の Glue 接続を作り、それぞれにパスワードを書く
- D. 各スクリプトに JDBC の URL とパスワードを直接書く

??? success "答えと解説"
    **正解: B**

    接続は Data Catalog のオブジェクトで、再利用できます。

    - A: 誤り。バケットポリシーに接続情報は保存しません。
    - B: 正しい。
    - C: 誤り。再利用になりません。
    - D: 誤り。管理が分散し、認証情報の扱いも不適切です。

    **スキル:** [2.2.5](../domain2.md#skill-2-2-5) / **参照:** [AWS Glue](../../../services/data-engineering.md#glue)、[クローラー](../../../services/data-engineering.md#glue-crawlers)

### 問16 {#q16}

Glue がネイティブに対応していないデータストアへ接続します。どの方法ですか。

- A. AWS Marketplace のコネクターか、自作のコネクターを使う
- B. データストアの種類を問わず JDBC 接続で必ず接続できるので、そのまま設定する
- C. Lake Formation に S3 パスとして登録する
- D. `AWS::Glue::Crawler` を作成して、未対応のデータストアでも自動で読む

??? success "答えと解説"
    **正解: A**

    未対応ならコネクターを使います。

    - A: 正しい。
    - B: 誤り。JDBC に対応していないこともあります。
    - C: 誤り。登録の対象は S3 です。
    - D: 誤り。未対応のストアには接続できません。

    **スキル:** [2.2.5](../domain2.md#skill-2-2-5) / **参照:** [AWS Glue](../../../services/data-engineering.md#glue)

### 問17 {#q17}

Glue のカタログ用の接続を初めて作り、クローラーで使います。正しい手順の順序はどれですか。

- A. 接続を作る、コネクターを選ぶ、クローラーで指定する、IAM ロールを作る
- B. クローラーを実行する、接続を作る、コネクターを選ぶ、IAM ロールを作る
- C. コネクターを選ぶ、接続を作る、IAM ロールを作る、クローラーで指定する
- D. IAM ロールを作る、クローラーで指定する、接続を作る、コネクターを選ぶ

??? success "答えと解説"
    **正解: C**

    接続とロールの準備の後に指定します。

    - A: 誤り。接続はコネクターを選んでから作り、ロールはクローラーの前に要ります。
    - B: 誤り。クローラーの実行が先です。
    - C: 正しい。
    - D: 誤り。クローラーで指定する接続が先に要ります。

    **スキル:** [2.2.5](../domain2.md#skill-2-2-5) / **参照:** [AWS Glue](../../../services/data-engineering.md#glue)、[信頼ポリシー](../../../services/iam.md#trust-policy)

### 問18 {#q18}

Kafka のストリームで、プロデューサーが互換性のないスキーマの変更を出さないようにします。何を使いますか。

- A. クローラーの `MergeNewColumns` を設定し、ストリームを定期的に読む
- B. `DeleteBehavior` を `LOG` に設定して、互換性のないスキーマの変更を拒否する
- C. Glue Schema Registry で互換性モードを `BACKWARD` にする
- D. 互換性モードを `NONE` にして、すべての変更を検査する

??? success "答えと解説"
    **正解: C**

    互換性のない変更は登録の時点で拒否されます。

    - A: 誤り。クローラーはストリーミングのソースに使えません。
    - B: 誤り。拒否の機能ではありません。
    - C: 正しい。
    - D: 誤り。`NONE` は検査しません。

    **スキル:** [2.4.2](../domain2.md#skill-2-4-2) / **参照:** [Schema Registry](../../../services/data-engineering.md#glue-schema-registry)

### 問19 {#q19}

`BACKWARD` の Avro スキーマの変更で、登録が拒否されるものはどれですか。

- A. 既定値のない必須列 `zip_code` の追加
- B. 既定値のある任意の列の追加
- C. 説明の文の変更だけで、列を変えない更新
- D. 必須列 `email` の削除

??? success "答えと解説"
    **正解: A**

    必須列の追加は、古いメッセージを読めなくなります。

    - A: 正しい。
    - B: 誤り。古いメッセージも読めるので登録できます。
    - C: 誤り。互換性に影響しません。
    - D: 誤り。登録できます。

    **スキル:** [2.4.2](../domain2.md#skill-2-4-2) / **参照:** [Schema Registry](../../../services/data-engineering.md#glue-schema-registry)

### 問20 {#q20}

S3 のテーブルに列を足し、パーティションを月から日へ変えます。既存のファイルは書き直しません。何を選びますか。

- A. Firehose のバッファの間隔を日単位へ変更する
- B. Iceberg のスキーマの進化とパーティションの進化
- C. Redshift の `VACUUM` でファイルを再配置する
- D. Hive 形式のテーブルで、フォルダの構造を作り直す

??? success "答えと解説"
    **正解: B**

    Iceberg は書き直しなしで変更できます。

    - A: 誤り。配信の設定です。
    - B: 正しい。
    - C: 誤り。S3 のテーブルの機能ではありません。
    - D: 誤り。パーティションの変更でフォルダの作り直しが必要です。

    **スキル:** [2.4.2](../domain2.md#skill-2-4-2) / **参照:** [Apache Iceberg](../../../services/data-engineering.md#iceberg)
