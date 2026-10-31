# データストアの選択の問題集

対象の解説: [データの置き場と SQL エンジン](../../../services/data-engineering.md#choosing-query)、[全エンジンの比較表](../../../services/databases-specialized.md#decision-table)、[Amazon DynamoDB](../../../services/dynamodb.md)

### 問1 {#q1}

ログを S3 に置き、月に数回だけ単発で SQL を実行します。クラスターは持たず、費用を読んだ量に比例させます。何を選びますか。

- A. EMR の HDFS にログを置いて常時起動する構成
- B. S3 に置いたまま Athena で SQL を実行する
- C. Redshift の RA3 クラスターを常時起動する構成
- D. RDS for PostgreSQL にログをすべて入れる構成

??? success "答えと解説"
    **正解: B**

    単発の分析は保存量とスキャン量で課金される Athena が向きます。

    - A: 誤り。ノードの費用が続きます。
    - B: 正しい。
    - C: 誤り。使わない時間も課金されます。
    - D: 誤り。インスタンスの費用がかかり、大量のログの分析に向きません。

    **スキル:** [2.1.1](../domain2.md#skill-2-1-1) / **参照:** [データの置き場と SQL エンジン](../../../services/data-engineering.md#choosing-query)

### 問2 {#q2}

「データレイクを作る選択肢」として Lake Formation が挙がりました。正しい理解はどれですか。

- A. データの実体は Lake Formation の専用ストレージにあり、S3 は使わない
- B. データの実体は Glue Data Catalog に保存され、S3 はそのバックアップである
- C. 実体は Redshift にあり、Lake Formation はその別名である
- D. データの実体は S3 にあり、Lake Formation は権限を管理する

??? success "答えと解説"
    **正解: D**

    Lake Formation は S3 上のデータの権限を管理します。

    - A: 誤り。ストレージのサービスではありません。
    - B: 誤り。カタログはメタデータだけを持ちます。
    - C: 誤り。別のサービスです。
    - D: 正しい。

    **スキル:** [2.1.1](../domain2.md#skill-2-1-1) / **参照:** [AWS Lake Formation](../../../services/data-engineering.md#lake-formation)、[データの置き場と SQL エンジン](../../../services/data-engineering.md#choosing-query)

### 問3 {#q3}

ストリームのデータを 30 日保持します。費用の説明として正しいものはどれですか。（2つ選択）

- A. Kinesis Data Streams は 24 時間を超える保持に追加料金がかかる
- B. MSK は古いデータを階層型ストレージへ移せる
- C. Kinesis Data Streams は保持を延ばしても料金は一切変わらない
- D. MSK はブローカーの料金がなく、保存量だけで課金される
- E. DynamoDB Streams の保持を 30 日に延ばせば、最も安く保持できる

??? success "答えと解説"
    **正解: A, B**

    保持の費用はサービスごとに異なります。

    - A: 正しい。既定の 24 時間を超えると課金されます。
    - B: 正しい。Standard ブローカーの機能です。
    - C: 誤り。追加料金がかかります。
    - D: 誤り。Provisioned はブローカーとストレージの料金がかかります。
    - E: 誤り。保持は 24 時間で延ばせません。

    **スキル:** [2.1.1](../domain2.md#skill-2-1-1) / **参照:** [キャパシティモード](../../../services/streaming.md#capacity-modes)、[Amazon MSK](../../../services/data-engineering.md#msk)

### 問4 {#q4}

EMR で 1 日 1 回ジョブを実行し、終了後にクラスターを消します。入出力とシャッフルの中間データの置き場はどれですか。

- A. 入出力は S3 に置き、シャッフルの中間データは HDFS に置く
- B. 入出力もシャッフルの中間データもすべて HDFS に置く構成
- C. 入出力は EBS のスナップショットから復元し、中間データは S3 に置く構成
- D. 入出力はプライマリノードのローカルに置き、中間データは DynamoDB に置く構成

??? success "答えと解説"
    **正解: A**

    HDFS はクラスターの終了で消えます。

    - A: 正しい。
    - B: 誤り。クラスターの終了で出力が消えます。
    - C: 誤り。EMR の EBS は一時的で、スナップショットの復元もできません。
    - D: 誤り。終了で消え、中間データの置き場にも向きません。

    **スキル:** [2.1.2](../domain2.md#skill-2-1-2) / **参照:** [HDFS と S3](../../../services/data-engineering.md#emr-hdfs-vs-s3)

### 問5 {#q5}

RDS のレポートのクエリが本番の書き込みに影響します。読み取りを逃がす構成はどれですか。

- A. Multi-AZ のインスタンス配置を有効にして、スタンバイでレポートを実行する
- B. ストレージの種類を変えて SQL を速くする
- C. リードレプリカを追加し、レポートをそちらへ向ける
- D. RDS Proxy を入れて、書き込みのトランザクションを自動で減らす

??? success "答えと解説"
    **正解: C**

    Multi-AZ は可用性、リードレプリカは読み取りの拡張です。

    - A: 誤り。この配置のスタンバイは読めず、目的は可用性です。
    - B: 誤り。読み取りの分離になりません。
    - C: 正しい。
    - D: 誤り。接続の共有の機能で、読み取りの分離はしません。

    **スキル:** [2.1.2](../domain2.md#skill-2-1-2) / **参照:** [リードレプリカと Multi-AZ](../../../services/databases.md#read-replicas)、[データストアの選び方](../../../services/databases.md#choosing-data-store)

### 問6 {#q6}

DynamoDB のテーブルを作成した後で、「メールアドレスで項目を引く」要件が増えました。どのインデックスを使いますか。

- A. メールアドレスをパーティションキーにした GSI を追加する
- B. テーブルのパーティションキーをメールアドレスに変更する
- C. メールアドレスをソートキーにした LSI を追加する
- D. 定期的にテーブルをスキャンして、結果を DAX に入れる

??? success "答えと解説"
    **正解: A**

    キー以外で引くなら GSI です。

    - A: 正しい。
    - B: 誤り。キーは後から変更できません。
    - C: 誤り。LSI は作成時だけ定義できます。
    - D: 誤り。全件を読むので費用が高くなります。

    **スキル:** [2.1.2](../domain2.md#skill-2-1-2) / **参照:** [LSI と GSI](../../../services/dynamodb.md#indexes)

### 問7 {#q7}

Redshift の `COMPOUND SORTKEY (sold_at, region)` のテーブルで、`region` だけを条件にしたクエリが遅いです。原因はどれですか。

- A. ソートキーに 2 列を指定すると、Redshift はソートキーを無視する
- B. `COMPOUND` は常に全列に等しい重みを持つので、条件の順序が重要である
- C. 先頭の列を含まない条件では、ソートキーがほとんど効かない
- D. `region` を条件に使うと、必ず `DS_BCAST_INNER` の再配布が起きる

??? success "答えと解説"
    **正解: C**

    `COMPOUND` は先頭の列からの条件に効きます。

    - A: 誤り。複数列を指定できます。
    - B: 誤り。等しい重みは `INTERLEAVED` です。
    - C: 正しい。
    - D: 誤り。再配布は結合の話です。

    **スキル:** [2.1.2](../domain2.md#skill-2-1-2) / **参照:** [ソートキー](../../../services/data-engineering.md#redshift-sort-keys)、[分散スタイル](../../../services/data-engineering.md#redshift-distribution)

### 問8 {#q8}

キーと値の検索をマイクロ秒で読み、データは再起動後も失われないようにして、主データベースとして使います。どのサービスですか。

- A. Keyspaces
- B. MemoryDB
- C. DocumentDB
- D. ElastiCache

??? success "答えと解説"
    **正解: B**

    MemoryDB は Multi-AZ のトランザクションログへ書いてから応答します。

    - A: 誤り。Cassandra 互換のワイドカラムです。
    - B: 正しい。
    - C: 誤り。MongoDB 互換のドキュメントデータベースです。
    - D: 誤り。データベースの前に置くキャッシュに向きます。

    **スキル:** [2.1.3](../domain2.md#skill-2-1-3) / **参照:** [ElastiCache との違い](../../../services/databases-specialized.md#memorydb-vs-elasticache)

### 問9 {#q9}

要件とサービスの組み合わせで正しいものはどれですか。

- A. MongoDB の既存のアプリをそのまま移すのは Keyspaces
- B. アプリログの全文検索とダッシュボードは MemoryDB
- C. Cassandra のクエリをそのまま使うのは Neptune
- D. 人と取引のつながりを何段もたどる不正検知は Neptune

??? success "答えと解説"
    **正解: D**

    グラフのつながりは Neptune です。

    - A: 誤り。DocumentDB です。
    - B: 誤り。OpenSearch Service です。
    - C: 誤り。Keyspaces です。
    - D: 正しい。

    **スキル:** [2.1.3](../domain2.md#skill-2-1-3) / **参照:** [データベースの選び方](../../../services/databases-specialized.md#choosing)、[紛らわしい組み合わせ](../../../services/databases-specialized.md#confusable)

### 問10 {#q10}

要件に合う保存先として正しい組み合わせはどれですか。（2つ選択）

- A. キーで引く低遅延の読み書きに Redshift を使う
- B. 既存の PostgreSQL の中で意味検索をするなら Aurora PostgreSQL と pgvector
- C. データベースの前のキャッシュに DocumentDB を置く
- D. 保守を任せた Iceberg のテーブルなら S3 Tables
- E. 全文検索とダッシュボードに Neptune を使う

??? success "答えと解説"
    **正解: B, D**

    要件から保存先を選びます。

    - A: 誤り。分析の DWH です。
    - B: 正しい。HNSW を使えます。
    - C: 誤り。ドキュメントデータベースです。
    - D: 正しい。圧縮などが既定で有効です。
    - E: 誤り。グラフデータベースです。

    **スキル:** [2.1.3](../domain2.md#skill-2-1-3) / **参照:** [S3 Tables](../../../services/data-engineering.md#s3-tables)、[pgvector](../../../services/genai-apps.md#pgvector)

### 問11 {#q11}

S3 のデータを `user_id` でパーティションにしたところ、Athena が遅くなりました。ユーザーは数百万人です。正しい見直しはどれですか。

- A. よく絞る日付などのカーディナリティが中程度の列でパーティションを切り直す
- B. 各パーティションのファイルを 1 KB 以下に細かく分け、並列度を上げる
- C. データを CSV に戻し、ファイルの読みやすさを優先する
- D. パーティションの階層を増やし、`user_id` の下にさらに時刻を入れて細かくする

??? success "答えと解説"
    **正解: A**

    値の種類が多すぎる列は避けます。

    - A: 正しい。
    - B: 誤り。一覧と起動の費用が増えます。
    - C: 誤り。スキャン量が増えます。
    - D: 誤り。小さなファイルがさらに増えます。

    **スキル:** [2.4.5](../domain2.md#skill-2-4-5) / **参照:** [パーティション](../../../services/data-engineering.md#partitioning)

### 問12 {#q12}

Spark で読む 200 GB の gzip の CSV 1 ファイルが遅いです。圧縮と形式の見直しとして適切なものはどれですか。

- A. 非圧縮の CSV を 1 つのファイルのまま読み、全列を読むようにする
- B. 行形式の JSON に変えて、1 つの大きなファイルにまとめる
- C. Parquet と Snappy に変換し、適切な大きさの複数のファイルに分ける
- D. gzip のまま圧縮のレベルを最大にして、1 つのファイルのまま読む

??? success "答えと解説"
    **正解: C**

    列指向と分割できる形が並列処理に効きます。

    - A: 誤り。スキャン量が増えます。
    - B: 誤り。全列を読み、遅いままです。
    - C: 正しい。
    - D: 誤り。gzip は分割して読めません。

    **スキル:** [2.4.5](../domain2.md#skill-2-4-5) / **参照:** [データ形式](../../../services/data-engineering.md#data-formats)、[速く、安くするコツ](../../../services/streaming.md#athena-performance)

### 問13 {#q13}

DynamoDB の GSI で、読む属性は 3 つだけです。ストレージと書き込みの費用を抑える設定はどれですか。

- A. GSI のパーティションキーを、値の種類が少ない列に変更する
- B. `ALL` で全属性を射影して、将来の要件に備える
- C. LSI を追加して、同じ属性をすべて複製する
- D. `INCLUDE` で必要な属性だけを射影する

??? success "答えと解説"
    **正解: D**

    必要な属性だけを射影します。

    - A: 誤り。書き込みが偏ります。
    - B: 誤り。費用が増えます。
    - C: 誤り。費用が増え、LSI は作成時だけ定義できます。
    - D: 正しい。

    **スキル:** [2.4.5](../domain2.md#skill-2-4-5) / **参照:** [射影とフェッチ](../../../services/dynamodb.md#projection)、[LSI と GSI](../../../services/dynamodb.md#indexes)
