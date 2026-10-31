# Athena と SQLの問題集

対象の解説: [Amazon Athena](../../../services/streaming.md#athena)

### 問1 {#q1}

Athena の費用と時間を減らす効果が最も大きいものはどれですか。

- A. ワークグループを増やして、同じクエリを分けて実行する運用
- B. Parquet にし、パーティション列で絞り、必要な列だけ選ぶ
- C. クエリの結果の保存先を別のバケットに変更する運用
- D. CSV のまま `SELECT *` にして、結果を毎回ダウンロードする運用

??? success "答えと解説"
    **正解: B**

    料金はスキャン量で決まります。

    - A: 誤り。スキャン量は増えます。
    - B: 正しい。
    - C: 誤り。スキャン量は変わりません。
    - D: 誤り。スキャン量が減りません。

    **スキル:** [3.1.7](../domain3.md#skill-3-1-7) / **参照:** [速く、安くするコツ](../../../services/streaming.md#athena-performance)、[形式と料金](../../../services/streaming.md#athena-formats-cost)

### 問2 {#q2}

チームのアナリストが巨大なクエリを誤って実行します。1 クエリが 1 TB を超えたら止めます。何を設定しますか。

- A. ワークグループ全体のデータ使用量の制限で、SNS へ通知する設定
- B. Budgets の月額の予算で通知する設定
- C. ワークグループのクエリごとのデータ使用量の制限
- D. S3 のライフサイクルでクエリ結果を失効させる設定

??? success "答えと解説"
    **正解: C**

    超えたクエリはキャンセルされます。

    - A: 誤り。通知の機能で、個別のクエリは止めません。
    - B: 誤り。費用の通知で、クエリは止めません。
    - C: 正しい。
    - D: 誤り。結果の片付けです。

    **スキル:** [3.1.7](../domain3.md#skill-3-1-7) / **参照:** [ワークグループ](../../../services/streaming.md#athena-workgroups)

### 問3 {#q3}

全アナリストのクエリ結果を、決められた暗号化済みのバケットへ強制します。どの設定ですか。

- A. ワークグループの「クライアント側の設定を上書き」を有効にする
- B. バケットのライフサイクルで結果を別の場所へ移す
- C. 各アナリストのコンソールで結果の場所を手で設定してもらう
- D. Lake Formation の LF タグを結果のバケットに付ける

??? success "答えと解説"
    **正解: A**

    ワークグループの設定を優先させます。

    - A: 正しい。
    - B: 誤り。結果の場所を決める設定ではありません。
    - C: 誤り。強制になりません。
    - D: 誤り。Data Catalog のリソースの機能です。

    **スキル:** [3.1.7](../domain3.md#skill-3-1-7) / **参照:** [ワークグループ](../../../services/streaming.md#athena-workgroups)

### 問4 {#q4}

同じダッシュボードのクエリが 10 分おきに実行されます。データの更新は 1 時間に 1 回です。スキャン量を減らす機能はどれですか。

- A. CTAS で毎回テーブルを作り直して読む
- B. `TABLESAMPLE` で一部の行だけを読む書き方に変更する
- C. パーティション射影を有効にして結果をキャッシュする
- D. クエリ結果の再利用で最大の経過時間を指定する

??? success "答えと解説"
    **正解: D**

    指定した期間は前回の結果を使い、変更の確認はしません。

    - A: 誤り。毎回スキャンします。
    - B: 誤り。集計の値が変わります。
    - C: 誤り。パーティションの計算の機能で、結果は保存しません。
    - D: 正しい。

    **スキル:** [3.1.7](../domain3.md#skill-3-1-7) / **参照:** [速く、安くするコツ](../../../services/streaming.md#athena-performance)

### 問5 {#q5}

Athena の `CREATE VIEW` で複雑な SQL をまとめました。クエリが速くなりません。説明として正しいものはどれですか。

- A. ビューの結果は S3 に保存されるが、読み取りの権限が足りない
- B. ビューは Redshift だけの機能で、Athena では何も作られない
- C. ビューはパーティションの情報を消すので、必ず全件を読む
- D. ビューは毎回元のデータを読むので、結果を保存しない

??? success "答えと解説"
    **正解: D**

    速さが要るなら CTAS で保存します。

    - A: 誤り。結果は保存されません。
    - B: 誤り。Athena でも作れます。
    - C: 誤り。条件は元のテーブルにも適用されます。
    - D: 正しい。

    **スキル:** [3.2.3](../domain3.md#skill-3-2-3) / **参照:** [マテリアライズドビュー](../../../services/data-engineering.md#redshift-materialized-views)

### 問6 {#q6}

Athena の集計の結果を、S3 に Parquet で保存し、後のクエリで読みます。どの文ですか。

- A. `CREATE TABLE daily WITH (format = 'PARQUET') AS SELECT ...`
- B. `CREATE MATERIALIZED VIEW daily AUTO REFRESH YES AS SELECT ...`
- C. `UNLOAD ('SELECT ...') TO 's3://lake/' IAM_ROLE default`
- D. `CREATE VIEW daily WITH (format = 'PARQUET') AS SELECT ...`

??? success "答えと解説"
    **正解: A**

    CTAS は結果を S3 に書きます。

    - A: 正しい。
    - B: 誤り。Redshift の文です。
    - C: 誤り。`IAM_ROLE` を付けるのは Redshift の書き方です。
    - D: 誤り。ビューは書き込みません。

    **スキル:** [3.2.3](../domain3.md#skill-3-2-3) / **参照:** [S3 上のログを問い合わせる](../../../services/streaming.md#athena-logs)、[データ形式](../../../services/data-engineering.md#data-formats)

### 問7 {#q7}

Redshift で、集計の結果を保存して速くし、S3 のテーブルとも結合します。正しい組み合わせはどれですか。（2つ選択）

- A. Athena の CTAS を Redshift の中で実行する
- B. `MSCK REPAIR TABLE` で集計の結果を保存する
- C. Spectrum の外部スキーマで S3 のテーブルを結合する
- D. 通常のビューで結果を保存する
- E. マテリアライズドビューで結果を保存する

??? success "答えと解説"
    **正解: C, E**

    目的に合う機能を選びます。

    - A: 誤り。Athena の機能です。
    - B: 誤り。パーティションの同期です。
    - C: 正しい。ローカルのテーブルと結合できます。
    - D: 誤り。結果は保存されません。
    - E: 正しい。事前計算して保存します。

    **スキル:** [3.2.3](../domain3.md#skill-3-2-3) / **参照:** [マテリアライズドビュー](../../../services/data-engineering.md#redshift-materialized-views)、[Spectrum とデータレイクのクエリ](../../../services/data-engineering.md#redshift-spectrum)

### 問8 {#q8}

データサイエンティストが、クラスターを作らずに Python で対話的に S3 のデータを探索します。SQL だけでは書きにくい処理です。何を使いますか。

- A. EMR on EC2 の長期クラスター
- B. Athena の Apache Spark
- C. Glue のスケジュールトリガーの本番ジョブ
- D. Athena の SQL の `CREATE VIEW`

??? success "答えと解説"
    **正解: B**

    Spark をサーバーレスで実行できます。

    - A: 誤り。クラスターの管理が必要です。
    - B: 正しい。
    - C: 誤り。対話的な探索に向きません。
    - D: 誤り。Python を実行できません。

    **スキル:** [3.2.4](../domain3.md#skill-3-2-4) / **参照:** [Amazon Athena](../../../services/streaming.md#athena)

### 問9 {#q9}

Athena の Spark のエンジンと実行の場所の組み合わせで正しいものはどれですか。

- A. Apache Spark バージョン 3.5 は、Glue のトリガーからだけ実行する
- B. PySpark エンジン バージョン 3 は、Spark Connect のクライアントからだけ実行する
- C. PySpark エンジン バージョン 3 は、Athena コンソールのノートブックで実行する
- D. Apache Spark バージョン 3.5 は、Athena コンソールからだけアプリケーションを送れる

??? success "答えと解説"
    **正解: C**

    エンジンごとに実行の場所が違います。

    - A: 誤り。Unified Studio のノートブックや Spark Connect のクライアントで動きます。
    - B: 誤り。コンソールのノートブックで動きます。
    - C: 正しい。
    - D: 誤り。コンソールから送れるのは PySpark エンジン バージョン 3 だけです。

    **スキル:** [3.2.4](../domain3.md#skill-3-2-4) / **参照:** [Amazon Athena](../../../services/streaming.md#athena)、[DataZone と SageMaker Unified Studio](../../../services/data-engineering.md#datazone-unified-studio)

### 問10 {#q10}

要件と選択の組み合わせで正しいものはどれですか。

- A. Python の対話的な探索は、Athena の `MSCK REPAIR TABLE` で実行する
- B. SQL で書ける単発の分析は、必ず Athena の Spark で実行する
- C. 本番で毎日実行する定期的な ETL は Athena の Spark のノートブックで手で実行する
- D. 本番で毎日実行する定期的な ETL は Glue か EMR を選ぶ

??? success "答えと解説"
    **正解: D**

    探索と本番で使い分けます。

    - A: 誤り。パーティションの同期です。
    - B: 誤り。Athena の SQL で足ります。
    - C: 誤り。対話的な探索に向きます。
    - D: 正しい。

    **スキル:** [3.2.4](../domain3.md#skill-3-2-4) / **参照:** [Amazon Athena](../../../services/streaming.md#athena)、[変換エンジン](../../../services/data-engineering.md#choosing-transform)

### 問11 {#q11}

日次の売上から、直近 7 日の移動平均を求めます。正しいウィンドウの指定はどれですか。

- A. `AVG(total) OVER (ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)`
- B. `SUM(total) OVER (ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)`
- C. `AVG(total) OVER (ORDER BY day ROWS BETWEEN 7 PRECEDING AND CURRENT ROW)`
- D. `AVG(total) OVER (PARTITION BY day ORDER BY day)`

??? success "答えと解説"
    **正解: A**

    当日を含めて 7 行です。

    - A: 正しい。
    - B: 誤り。合計で、平均ではありません。
    - C: 誤り。当日を含めて 8 日分になります。
    - D: 誤り。日ごとに区切るので、移動平均になりません。

    **スキル:** [3.2.6](../domain3.md#skill-3-2-6) / **参照:** [S3 上のログを問い合わせる](../../../services/streaming.md#athena-logs)、[Amazon Redshift](../../../services/data-engineering.md#redshift)

### 問12 {#q12}

地域ごとの売上の合計が 100 万を超える地域だけを求めます。正しい SQL はどれですか。

- A. `SELECT region, SUM(amount) FROM sales WHERE SUM(amount) > 1000000 GROUP BY region`
- B. `SELECT region, amount FROM sales HAVING amount > 1000000 GROUP BY amount, region`
- C. `SELECT region, SUM(amount) FROM sales GROUP BY region HAVING SUM(amount) > 1000000`
- D. `SELECT region, COUNT(*) FROM sales GROUP BY region WHERE COUNT(*) > 1000000`

??? success "答えと解説"
    **正解: C**

    集計後の絞り込みは `HAVING` です。

    - A: 誤り。`WHERE` に集計は書けません。
    - B: 誤り。地域の合計になりません。
    - C: 正しい。
    - D: 誤り。順序が誤りで、件数の条件になっています。

    **スキル:** [3.2.6](../domain3.md#skill-3-2-6) / **参照:** [S3 上のログを問い合わせる](../../../services/streaming.md#athena-logs)

### 問13 {#q13}

Redshift で四半期の行を列にします。方法として正しいものはどれですか。（2つ選択）

- A. `SUM(CASE WHEN quarter = 'Q1' THEN amount END)` のように `CASE` で集計する
- B. `HAVING` を使う
- C. `PIVOT` を使う
- D. `TABLESAMPLE` を使う
- E. `UNPIVOT` を使う

??? success "答えと解説"
    **正解: A, C**

    ピボットは行の値を列に変えます。

    - A: 正しい。同じ結果を得られます。
    - B: 誤り。集計の後の絞り込みです。
    - C: 正しい。行の値を列に変えます。
    - D: 誤り。サンプリングです。
    - E: 誤り。列を行に戻します。

    **スキル:** [3.2.6](../domain3.md#skill-3-2-6) / **参照:** [Amazon Redshift](../../../services/data-engineering.md#redshift)
