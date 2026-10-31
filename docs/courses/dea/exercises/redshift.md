# Redshiftの問題集

対象の解説: [Amazon Redshift](../../../services/data-engineering.md#redshift)

### 問1 {#q1}

Redshift のダッシュボードで、RDS for PostgreSQL の在庫を最新の状態で表示します。コピーは作りません。どの方法ですか。

- A. Spectrum の外部テーブルで RDS のテーブルを定義して読む
- B. データ共有で RDS のデータベースを Redshift に共有する
- C. `COPY` に RDS の接続先を指定して毎分ロードする
- D. フェデレーテッドクエリで RDS を直接参照する

??? success "答えと解説"
    **正解: D**

    フェデレーテッドクエリは PostgreSQL と MySQL をそのまま参照します。

    - A: 誤り。Spectrum が読むのは S3 です。
    - B: 誤り。データ共有は Redshift 同士の機能です。
    - C: 誤り。`COPY` のコピーが作られ、要件に反します。
    - D: 正しい。

    **スキル:** [2.1.5](../domain2.md#skill-2-1-5) / **参照:** [データを取り込む他の方法](../../../services/data-engineering.md#redshift-ingestion)、[Spectrum とデータレイクのクエリ](../../../services/data-engineering.md#redshift-spectrum)

### 問2 {#q2}

同じ結合と集計を繰り返すダッシュボードが遅いです。結果を事前に計算して保存します。ベーステーブルは夜間に更新されます。何を作りますか。

- A. Spectrum の外部テーブルを作り、結果を毎回 S3 から読み直す
- B. マテリアライズドビューを作り、更新後に `REFRESH` する
- C. 通常のビューを作り、クエリの SQL を短くして読みやすくする
- D. ベーステーブルの `DISTSTYLE` を `ALL` に変更して、全ノードに置く

??? success "答えと解説"
    **正解: B**

    事前計算した結果を保存できます。

    - A: 誤り。事前計算の保存にはなりません。
    - B: 正しい。
    - C: 誤り。ビューは毎回元のデータを読むので、速くなりません。
    - D: 誤り。大きなテーブルではストレージが増え、事前計算にもなりません。

    **スキル:** [2.1.5](../domain2.md#skill-2-1-5) / **参照:** [マテリアライズドビュー](../../../services/data-engineering.md#redshift-materialized-views)

### 問3 {#q3}

データの扱いの説明として正しいものはどれですか。（2つ選択）

- A. フェデレーテッドクエリは S3 の Parquet だけを対象にする
- B. Spectrum の外部テーブルの行は Redshift から `UPDATE` できない
- C. `AUTO REFRESH YES` を指定すると、更新は常に即時に完了する
- D. `COPY` でロードしたデータは S3 を読み続けるので、S3 の削除で消える
- E. マテリアライズドビューが古い間は、自動書き換えが効かず遅くなる

??? success "答えと解説"
    **正解: B, E**

    方法ごとの性質を押さえます。

    - A: 誤り。RDS と Aurora が対象です。
    - B: 正しい。外部テーブルの更新や削除はできません。
    - C: 誤り。リソースに余裕のある時に動きます。
    - D: 誤り。ロード後は Redshift に保存されます。
    - E: 正しい。最新のときだけ自動で使います。

    **スキル:** [2.1.5](../domain2.md#skill-2-1-5) / **参照:** [マテリアライズドビュー](../../../services/data-engineering.md#redshift-materialized-views)、[Spectrum とデータレイクのクエリ](../../../services/data-engineering.md#redshift-spectrum)

### 問4 {#q4}

夜間のロード中も、BI のクエリは読み続けられています。ところが `TRUNCATE` を実行した時だけ BI が待たされます。説明として正しいものはどれですか。

- A. `COPY` はクラスター全体の排他ロックを取り、`TRUNCATE` はどのロックも取らない
- B. BI のクエリは常に未コミットのデータを読むので、`TRUNCATE` と競合する
- C. 読み取りはコミット済みのスナップショットを読むが、`TRUNCATE` は排他ロックを取る
- D. `TRUNCATE` は WLM のキューの優先度を自動で最高にするので、BI が待つ

??? success "答えと解説"
    **正解: C**

    `DROP TABLE` と `TRUNCATE` は読み取りも止めます。

    - A: 誤り。読み取りは `COPY` 中も動いています。
    - B: 誤り。コミット済みのスナップショットを読みます。
    - C: 正しい。
    - D: 誤り。ロックの問題です。

    **スキル:** [2.1.6](../domain2.md#skill-2-1-6) / **参照:** [ロックと同時実行](../../../services/data-engineering.md#redshift-locks)

### 問5 {#q5}

Redshift で長時間止まっているセッションがテーブルをロックしています。確認して解消する手順はどれですか。

- A. `STV_LOCKS` で確認し、`pg_terminate_backend(pid)` で切る
- B. `SVL_QLOG` で確認し、クラスターを再起動するまで待ってから `VACUUM` を実行する
- C. `STL_LOAD_ERRORS` で確認し、`ANALYZE` でロックを解放する
- D. `SVV_TABLE_INFO` で確認し、`ALTER TABLE` の `DISTSTYLE` を変更してからロックを解放する

??? success "答えと解説"
    **正解: A**

    ロックの確認とセッションの切断の手順です。

    - A: 正しい。
    - B: 誤り。全体に影響し、`VACUUM` はロックの解消手段ではありません。
    - C: 誤り。ロードのエラーと統計の更新です。
    - D: 誤り。テーブルの情報と分散の変更です。

    **スキル:** [2.1.6](../domain2.md#skill-2-1-6) / **参照:** [ロックと同時実行](../../../services/data-engineering.md#redshift-locks)

### 問6 {#q6}

RDS for MySQL 8.0 のロックを調べ、問題のスレッドを切ります。正しいものはどれですか。

- A. `pg_locks` で確認し、`pg_terminate_backend(pid)` で切る
- B. `STV_LOCKS` で確認し、`pg_terminate_backend(pid)` で切る
- C. `SVV_TRANSACTIONS` で確認し、`CALL mysql.rds_kill(スレッド ID)` で該当のスレッドを切る
- D. `performance_schema.data_locks` で確認し、`CALL mysql.rds_kill(スレッド ID)` で切る

??? success "答えと解説"
    **正解: D**

    エンジンごとの確認の方法を区別します。

    - A: 誤り。PostgreSQL の方法です。
    - B: 誤り。Redshift の方法です。
    - C: 誤り。`SVV_TRANSACTIONS` は Redshift のビューです。
    - D: 正しい。

    **スキル:** [2.1.6](../domain2.md#skill-2-1-6) / **参照:** [ロックと同時実行](../../../services/data-engineering.md#redshift-locks)

### 問7 {#q7}

S3 の Parquet を Redshift へロードします。長期の認証情報は使いません。正しい文はどれですか。

- A. `UNLOAD sales FROM 's3://lake/sales/' IAM_ROLE default FORMAT AS PARQUET;`
- B. `COPY sales FROM 's3://lake/sales/' IAM_ROLE default FORMAT AS PARQUET;`
- C. `INSERT INTO sales SELECT * FROM 's3://lake/sales/' FORMAT AS PARQUET;`
- D. `COPY sales FROM 's3://lake/sales/' ACCESS_KEY_ID 'AKIA...' FORMAT AS PARQUET;`

??? success "答えと解説"
    **正解: B**

    `IAM_ROLE` で権限を渡します。

    - A: 誤り。`UNLOAD` は S3 へ書き出す文です。
    - B: 正しい。
    - C: 誤り。`INSERT` は S3 のパスを直接読めません。
    - D: 誤り。長期の認証情報を使っています。

    **スキル:** [2.3.1](../domain2.md#skill-2-3-1) / **参照:** [COPY と UNLOAD](../../../services/data-engineering.md#redshift-copy)、[iam:PassRole](../../../services/iam.md#passrole)

### 問8 {#q8}

レポートを S3 へ出し、Athena で読みます。1 ファイルを 256 MB 以下にし、地域で区切ります。適切な `UNLOAD` のオプションはどれですか。

- A. `FORMAT AS PARQUET`、`PARTITION BY (region)`、`MAXFILESIZE 256 MB` のすべて
- B. `DELIMITER '|'`、`COMPUPDATE ON`、`STATUPDATE ON`
- C. `FORMAT AS PARQUET`、`PARTITION BY (region)`、`MANIFEST mandatory`、`MAXERROR 256`
- D. `CSV GZIP`、`IGNOREHEADER 1`、`NOLOAD`

??? success "答えと解説"
    **正解: A**

    `UNLOAD` の既定はパイプ区切りのテキストです。

    - A: 正しい。
    - B: 誤り。既定の区切り文字とロードのオプションで、要件を満たしません。
    - C: 誤り。`MAXERROR` は `COPY` のオプションです。
    - D: 誤り。いずれもロードで使うオプションです。

    **スキル:** [2.3.1](../domain2.md#skill-2-3-1) / **参照:** [COPY と UNLOAD](../../../services/data-engineering.md#redshift-copy)

### 問9 {#q9}

`COPY` と `UNLOAD` の通信を、インターネットではなく VPC の中に通し、VPC フローログで監視します。何を有効にしますか。

- A. 同時実行スケーリング
- B. AI 主導のスケーリング
- C. Enhanced VPC Routing
- D. ショートクエリアクセラレーション

??? success "答えと解説"
    **正解: C**

    `COPY` と `UNLOAD` の通信を VPC 経由にします。

    - A: 誤り。キューが詰まったときに一時クラスターを追加する機能です。
    - B: 誤り。Serverless の容量を調整する機能です。
    - C: 正しい。
    - D: 誤り。短いクエリを優先する機能です。

    **スキル:** [2.3.1](../domain2.md#skill-2-3-1) / **参照:** [暗号化とセキュリティ](../../../services/data-engineering.md#redshift-security)、[Spectrum とデータレイクのクエリ](../../../services/data-engineering.md#redshift-spectrum)

### 問10 {#q10}

新規の顧客が、`UNLOAD` の結果を S3 で暗号化します。現在の選択肢として正しいものはどれですか。

- A. 暗号化はできないので、S3 のライフサイクルで Glacier へ移して暗号化する
- B. SSE-S3 か SSE-KMS のサーバー側暗号化を使う
- C. クライアント側暗号化を `ENCRYPTED` と `MASTER_SYMMETRIC_KEY` で指定する
- D. 暗号化はできないので、ファイルを別のバケットへ移した後に Macie で暗号化する

??? success "答えと解説"
    **正解: B**

    サーバー側暗号化を使います。

    - A: 誤り。ライフサイクルはストレージクラスの移行の機能です。
    - B: 正しい。
    - C: 誤り。2025 年 4 月 30 日から新規顧客に提供されていません。
    - D: 誤り。Macie は機密データの検出のサービスです。

    **スキル:** [2.3.1](../domain2.md#skill-2-3-1) / **参照:** [COPY と UNLOAD](../../../services/data-engineering.md#redshift-copy)、[クライアント側とサーバー側の暗号化](../../../services/kms.md#client-vs-server-side)

### 問11 {#q11}

大きな売上ファクトを顧客で結合し、日付の範囲で絞ります。小さな店舗ディメンションも結合します。設計として適切なものはどれですか。

- A. 売上は `sold_at` を `DISTKEY`、`customer_id` を `SORTKEY` にし、店舗は `DISTSTYLE EVEN` にする
- B. 売上は `DISTSTYLE EVEN`、ソートキーなしにし、店舗も `DISTSTYLE EVEN` にする
- C. 売上は `customer_id` を `DISTKEY`、`sold_at` を `SORTKEY` にし、店舗は `DISTSTYLE ALL` にする
- D. 売上は `DISTSTYLE ALL`、`amount` を `SORTKEY` にし、店舗は `DISTKEY` を `store_id` にする

??? success "答えと解説"
    **正解: C**

    結合列を `DISTKEY`、範囲の列を `SORTKEY`、小さなディメンションを `ALL` にします。

    - A: 誤り。日付の `DISTKEY` は狭い期間で偏り、店舗の結合で再配布が起きます。
    - B: 誤り。結合で再配布が起き、範囲の絞り込みも効きません。
    - C: 正しい。
    - D: 誤り。大きなファクトを全ノードにコピーするのは不適切です。

    **スキル:** [2.4.1](../domain2.md#skill-2-4-1) / **参照:** [分散スタイル](../../../services/data-engineering.md#redshift-distribution)、[ソートキー](../../../services/data-engineering.md#redshift-sort-keys)

### 問12 {#q12}

次のうち、Redshift のスキーマとして不適切なものはどれですか。

- A. 1 行ずつの更新が大量に発生する注文の OLTP のテーブルを、そのまま置く
- B. 新しいテーブルに `DISTSTYLE AUTO` と `SORTKEY AUTO` を指定して置く
- C. 集計の結果をマテリアライズドビューとして置く
- D. 分析のためにファクトとディメンションに分けたスタースキーマを置く

??? success "答えと解説"
    **正解: A**

    Redshift は列指向で、大量の行単位の更新には向きません。

    - A: 正しい。
    - B: 誤り。推奨の設定です。
    - C: 誤り。繰り返す集計に向きます。
    - D: 誤り。Redshift の基本の設計です。

    **スキル:** [2.4.1](../domain2.md#skill-2-4-1) / **参照:** [Amazon Redshift](../../../services/data-engineering.md#redshift)、[単一テーブル設計の基本](../../../services/dynamodb.md#single-table)

### 問13 {#q13}

ETL の負荷が高い時間に、BI のダッシュボードが待たされます。ノードは増やしません。Redshift の機能で適切なものはどれですか。

- A. BI のテーブルをすべて `INTERLEAVED` のソートキーにして、待ちを減らす
- B. ETL と BI を同じキューに入れ、手動 WLM のスロットを 200 に増やして同時に流す
- C. ETL の処理をすべて `UNLOAD` に変更して、待ちを減らす
- D. ETL と BI のキューを分け、BI の優先度を高くして同時実行スケーリングを有効にする

??? success "答えと解説"
    **正解: D**

    ワークロードを分け、急増には同時実行スケーリングを使います。

    - A: 誤り。キューの待ちには効かず、同時実行スケーリングの対象外にもなります。
    - B: 誤り。合計 15 スロット以下が推奨で、分離にもなりません。
    - C: 誤り。`UNLOAD` は S3 への書き出しです。
    - D: 正しい。

    **スキル:** [3.1.4](../domain3.md#skill-3-1-4) / **参照:** [ワークロード管理](../../../services/data-engineering.md#redshift-wlm)

### 問14 {#q14}

短いダッシュボードのクエリが、長いレポートの後ろで待たされます。短いクエリを優先する機能はどれですか。

- A. ショートクエリアクセラレーション（SQA）
- B. クエリモニタリングルール
- C. Enhanced VPC Routing
- D. データ共有

??? success "答えと解説"
    **正解: A**

    SQA は短いクエリを予測して優先枠で実行します。

    - A: 正しい。
    - B: 誤り。実行時間などで打ち切りや記録を行う機能で、優先枠で実行はしません。
    - C: 誤り。`COPY` と `UNLOAD` の通信経路の機能です。
    - D: 誤り。別のクラスターへ共有する機能です。

    **スキル:** [3.1.4](../domain3.md#skill-3-1-4) / **参照:** [ワークロード管理](../../../services/data-engineering.md#redshift-wlm)

### 問15 {#q15}

Redshift の機能でパイプラインを減らします。正しい組み合わせはどれですか。（2つ選択）

- A. `VACUUM` で S3 の新しいファイルを検知して、自動でロードする
- B. Kinesis や MSK のストリーミング取り込みで、マテリアライズドビューへ直接入れる
- C. マテリアライズドビューの増分更新で、繰り返しの集計を Redshift の中で計算する
- D. 通常のビューに結果を保存して、夜間の集計を不要にする
- E. `ANALYZE` で RDS の変更を取り込んで、テーブルを更新する

??? success "答えと解説"
    **正解: B, C**

    DWH の中で計算する機能です。

    - A: 誤り。領域の回収と並べ替えの機能です。
    - B: 正しい。S3 を経由しません。
    - C: 正しい。可能なら増分で更新します。
    - D: 誤り。通常のビューは結果を保存しません。
    - E: 誤り。統計の更新の機能です。

    **スキル:** [3.1.4](../domain3.md#skill-3-1-4) / **参照:** [データを取り込む他の方法](../../../services/data-engineering.md#redshift-ingestion)、[マテリアライズドビュー](../../../services/data-engineering.md#redshift-materialized-views)

### 問16 {#q16}

アナリストが 50 人います。Redshift で同じ権限を、人ごとの `GRANT` なしでまとめて付与します。正しい手順はどれですか。

- A. `CREATE USER analyst` を 1 つ作り、全員で同じパスワードを共有して接続する
- B. 各テーブルに `GRANT SELECT` を 50 回実行し、新しいテーブルでも同じ操作を人数分だけ繰り返して権限を揃える
- C. `ALTER TABLE` で `DISTSTYLE ALL` に変更して、全員に読めるようにする
- D. `CREATE ROLE analyst` の後にテーブルの権限を与え、`GRANT ROLE analyst TO alice` を実行する

??? success "答えと解説"
    **正解: D**

    RBAC で権限をまとめます。

    - A: 誤り。誰の操作か追えません。
    - B: 誤り。まとめる要件に反します。
    - C: 誤り。分散スタイルは権限ではありません。
    - D: 正しい。

    **スキル:** [4.2.3](../domain4.md#skill-4-2-3) / **参照:** [暗号化とセキュリティ](../../../services/data-engineering.md#redshift-security)

### 問17 {#q17}

販売担当者には自分の地域の行だけを見せ、支払いの担当者以外にはカード番号を隠します。Redshift の機能の組み合わせはどれですか。

- A. 行レベルセキュリティと列の圧縮エンコード
- B. データ共有と列レベルの `GRANT`
- C. 行レベルセキュリティと動的データマスキング
- D. WLM のキューと行レベルセキュリティ

??? success "答えと解説"
    **正解: C**

    行は RLS、列の値はマスキングで制御します。

    - A: 誤り。圧縮エンコードは値を隠しません。
    - B: 誤り。データ共有は行を制限する機能ではありません。
    - C: 正しい。
    - D: 誤り。WLM は値を隠しません。

    **スキル:** [4.2.3](../domain4.md#skill-4-2-3) / **参照:** [暗号化とセキュリティ](../../../services/data-engineering.md#redshift-security)

### 問18 {#q18}

RDS のデータベースに、パスワードを保存せず IAM の認証でユーザーを接続させます。何を使いますか。

- A. Redshift のロールを作り、RDS のユーザーへ `GRANT ROLE` する
- B. IAM データベース認証で、短時間のトークンを取得して接続する
- C. Lake Formation のデータフィルターを、RDS のテーブルに設定して接続する
- D. データベースのユーザーのパスワードを IAM ポリシーの `Condition` に書く

??? success "答えと解説"
    **正解: B**

    IAM データベース認証を使います。

    - A: 誤り。Redshift の機能です。
    - B: 正しい。
    - C: 誤り。Data Catalog のテーブルのための機能です。
    - D: 誤り。パスワードをポリシーに書く機能はありません。

    **スキル:** [4.2.3](../domain4.md#skill-4-2-3) / **参照:** [IAM データベース認証](../../../services/databases.md#rds-iam-auth)、[Secrets Manager との統合](../../../services/databases.md#rds-secrets-manager)

### 問19 {#q19}

ETL のクラスターのデータを、BI のワークグループへコピーせずライブで渡します。プロデューサーの手順の順序として正しいものはどれですか。

- A. `GRANT USAGE ... TO NAMESPACE`、`CREATE DATABASE ... FROM DATASHARE`、`CREATE DATASHARE`
- B. `UNLOAD`、`COPY`、`GRANT SELECT ON TABLE`
- C. `CREATE DATASHARE`、`ALTER DATASHARE ... ADD`、`GRANT USAGE ... TO NAMESPACE`
- D. `CREATE EXTERNAL SCHEMA`、`ALTER TABLE ADD PARTITION`、`MSCK REPAIR TABLE`

??? success "答えと解説"
    **正解: C**

    コンシューマーは `CREATE DATABASE ... FROM DATASHARE` を実行します。

    - A: 誤り。コンシューマーの手順が混ざり、順序も逆です。
    - B: 誤り。コピーを作る手順です。
    - C: 正しい。
    - D: 誤り。Spectrum などの手順です。

    **スキル:** [4.5.1](../domain4.md#skill-4-5-1) / **参照:** [データ共有](../../../services/data-engineering.md#redshift-data-sharing)

### 問20 {#q20}

Redshift のデータ共有の説明として正しいものはどれですか。（2つ選択）

- A. データはコンシューマー側へ定期的にコピーされる
- B. Provisioned と Serverless の間では共有できない
- C. コンシューマーの計算資源で読むので、ETL と BI の計算を分けられる
- D. アカウントやリージョンをまたげる
- E. S3 のデータレイクの列と行の権限を付ける機能である

??? success "答えと解説"
    **正解: C, D**

    データをコピーせずに共有します。

    - A: 誤り。コピーせず、ライブのまま共有します。
    - B: 誤り。共有できます。
    - C: 正しい。計算資源を別々に計上できます。
    - D: 正しい。別のアカウントやリージョンのクラスターと共有できます。
    - E: 誤り。それは Lake Formation です。

    **スキル:** [4.5.1](../domain4.md#skill-4-5-1) / **参照:** [データ共有](../../../services/data-engineering.md#redshift-data-sharing)、[データの共有](../../../services/data-engineering.md#choosing-sharing)

### 問21 {#q21}

共有の要件と選択の組み合わせで正しいものはどれですか。

- A. 別のアカウントの Redshift へ共有するなら、AWS Clean Rooms で生データのまま渡す
- B. 別のアカウントの Redshift へ共有するなら、AppFlow でテーブルを転送する
- C. 別のアカウントの Redshift へ共有するなら、毎日 `UNLOAD` して S3 レプリケーションで送る
- D. 別のアカウントの Redshift ワークグループへ、テーブルをライブで共有するならデータ共有

??? success "答えと解説"
    **正解: D**

    ライブのテーブルの共有はデータ共有です。

    - A: 誤り。Clean Rooms は生データを見せない共同分析のサービスです。
    - B: 誤り。AppFlow は SaaS との転送のサービスです。
    - C: 誤り。コピーになり、ライブではありません。
    - D: 正しい。

    **スキル:** [4.5.1](../domain4.md#skill-4-5-1) / **参照:** [データ共有](../../../services/data-engineering.md#redshift-data-sharing)、[データの共有](../../../services/data-engineering.md#choosing-sharing)

### 問22 {#q22}

DynamoDB で注文を設計します。「顧客の注文を新しい順に読む」と「注文 ID で 1 件読む」が主なアクセスです。結合はしません。正しい考え方はどれですか。

- A. 第三正規形でテーブルを分け、読むたびにアプリの中で全テーブルをスキャンして結合する
- B. アクセスパターンから設計し、顧客 ID をパーティションキー、日時をソートキーにして、注文 ID の検索は GSI にする
- C. Redshift と同じスタースキーマで設計し、`DISTKEY` を顧客 ID に設定して、注文 ID とは結合で読む
- D. 注文のステータスをパーティションキーにして、値の種類を少なく保つ

??? success "答えと解説"
    **正解: B**

    DynamoDB はアクセスパターンを起点に設計します。

    - A: 誤り。スキャンは費用が高く、キー設計の考え方に反します。
    - B: 正しい。
    - C: 誤り。`DISTKEY` は Redshift の機能です。
    - D: 誤り。値の種類が少ないと書き込みが偏ります。

    **スキル:** [2.4.1](../domain2.md#skill-2-4-1) / **参照:** [単一テーブル設計の基本](../../../services/dynamodb.md#single-table)、[高カーディナリティのパーティションキー](../../../services/dynamodb.md#high-cardinality)

### 問23 {#q23}

データレイクのスキーマを設計します。部門とセンシティビティごとの権限を、後から増えるテーブルにも適用します。Lake Formation で設計するものはどれですか。

- A. LF タグの体系と、テーブルや列への割り当て
- B. 部門ごとの S3 バケットと、バケットポリシーの追記
- C. Redshift の `DISTKEY` と `SORTKEY`、および WLM のキュー
- D. DynamoDB の GSI と、カタログの `MergeNewColumns` の設定

??? success "答えと解説"
    **正解: A**

    Lake Formation では権限の単位で設計します。

    - A: 正しい。
    - B: 誤り。列や行を扱えず、テーブルが増えるたびに作業が残ります。
    - C: 誤り。Redshift の性能の設計です。
    - D: 誤り。別の機能の設定です。

    **スキル:** [2.4.1](../domain2.md#skill-2-4-1) / **参照:** [LF タグ](../../../services/data-engineering.md#lake-formation-lf-tags)、[権限](../../../services/data-engineering.md#lake-formation-permissions)
