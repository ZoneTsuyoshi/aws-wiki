# データ品質とデータ準備の問題集

対象の解説: [Data Quality](../../../services/data-engineering.md#glue-data-quality)、[DataBrew](../../../services/data-engineering.md#databrew)

### 問1 {#q1}

アナリストが、列の分割や欠損の補完を画面で試し、確定した手順を全データへ適用します。DataBrew の順序はどれですか。

- A. プロファイルジョブで試し、クローラーを保存し、ワークフローで適用する
- B. ルールセットで試し、データセットを削除し、プロジェクトで適用する
- C. レシピジョブで試し、プロジェクトを公開し、ルールセットで適用する
- D. プロジェクトで試し、レシピを保存し、レシピジョブで適用する

??? success "答えと解説"
    **正解: D**

    レシピは別のデータにも再利用できます。

    - A: 誤り。統計の取得で、整形の手順ではありません。
    - B: 誤り。ルールセットは品質の検証です。
    - C: 誤り。順序が逆です。
    - D: 正しい。

    **スキル:** [3.1.6](../domain3.md#skill-3-1-6) / **参照:** [DataBrew](../../../services/data-engineering.md#databrew)

### 問2 {#q2}

データの準備から分析、ML までを、チームで 1 つのプロジェクトの中で進めます。何を選びますか。

- A. DataBrew
- B. SageMaker Unified Studio
- C. Glue Studio のビジュアルエディタの ETL ジョブ
- D. Amazon Quick Sight

??? success "答えと解説"
    **正解: B**

    データ、分析、ML の統合環境です。

    - A: 誤り。単独の整形ツールです。
    - B: 正しい。
    - C: 誤り。ETL の作成の画面で、ML までは扱いません。
    - D: 誤り。BI のサービスです。

    **スキル:** [3.1.6](../domain3.md#skill-3-1-6) / **参照:** [SageMaker Unified Studio の位置づけ](../../../services/sagemaker.md#unified-studio)、[DataZone と SageMaker Unified Studio](../../../services/data-engineering.md#datazone-unified-studio)

### 問3 {#q3}

データ準備の担当とツールの組み合わせで正しいものはどれですか。

- A. アナリストのコード不要の整形は Glue の Spark スクリプト
- B. アナリストのコード不要の整形は EMR の Spark ジョブ
- C. データエンジニアの大規模な本番の変換は Glue の ETL ジョブ
- D. データエンジニアの大規模な本番の変換は DataBrew のプロジェクトの画面

??? success "答えと解説"
    **正解: C**

    利用者と規模で選びます。

    - A: 誤り。コードが必要です。
    - B: 誤り。コードとクラスターの準備が必要です。
    - C: 正しい。
    - D: 誤り。プロジェクトはサンプルを画面で整形する場所です。

    **スキル:** [3.1.6](../domain3.md#skill-3-1-6) / **参照:** [変換エンジン](../../../services/data-engineering.md#choosing-transform)、[DataBrew](../../../services/data-engineering.md#databrew)

### 問4 {#q4}

Quick Sight のダッシュボードを速くし、Athena のスキャン費用を抑えます。データは日次の更新で足ります。どの方式ですか。

- A. SPICE に取り込み、日次で更新する
- B. SPICE に取り込み、更新のスケジュールは設定しない
- C. 直接クエリにし、ダッシュボードの閲覧者数を制限する
- D. 直接クエリにし、表示のたびに Athena へ問い合わせる

??? success "答えと解説"
    **正解: A**

    SPICE はインメモリで、再利用に追加のクエリ料金がかかりません。

    - A: 正しい。
    - B: 誤り。データが古いままになります。
    - C: 誤り。費用の根本は変わりません。
    - D: 誤り。表示のたびに費用がかかります。

    **スキル:** [3.2.1](../domain3.md#skill-3-2-1) / **参照:** [Amazon Quick Sight](../../../services/data-engineering.md#quick-sight)

### 問5 {#q5}

見るものとツールの組み合わせで正しいものはどれですか。（2つ選択）

- A. 業務の利用者向けの売上の表は CloudWatch ダッシュボード
- B. 変換の前の列の分布や欠損は Managed Grafana
- C. 業務の利用者向けの売上のダッシュボードは Quick Sight
- D. 運用のメトリクスとログのダッシュボードは Managed Grafana
- E. 運用のメトリクスの監視は DataBrew のプロファイル

??? success "答えと解説"
    **正解: C, D**

    見るものと利用者でツールを選びます。

    - A: 誤り。運用のメトリクスを見るものです。
    - B: 誤り。DataBrew のプロファイルが向きます。
    - C: 正しい。BI のサービスです。
    - D: 正しい。運用の監視に向きます。
    - E: 誤り。データの統計の取得です。

    **スキル:** [3.2.1](../domain3.md#skill-3-2-1) / **参照:** [Amazon Quick Sight](../../../services/data-engineering.md#quick-sight)、[Amazon Managed Grafana](../../../services/operations.md#managed-grafana)

### 問6 {#q6}

Quick Sight で更新したのにダッシュボードが古いままです。取り込みの失敗も出ています。何を確認しますか。

- A. ダッシュボードのテーマとビジュアルの設定
- B. データセットの行レベルセキュリティの設定
- C. SPICE の更新スケジュールと容量の残り
- D. 閲覧者のユーザーの種類とセッションの料金

??? success "答えと解説"
    **正解: C**

    容量が足りないと取り込みが失敗します。

    - A: 誤り。見た目の設定です。
    - B: 誤り。見える行の制御で、取り込みの失敗とは別です。
    - C: 正しい。
    - D: 誤り。料金の話です。

    **スキル:** [3.2.1](../domain3.md#skill-3-2-1) / **参照:** [Amazon Quick Sight](../../../services/data-engineering.md#quick-sight)

### 問7 {#q7}

S3 のテーブルで、`email` 列の欠損の数を SQL で調べます。正しいものはどれですか。

- A. `SELECT COUNT(DISTINCT email) FROM users`
- B. `SELECT SUM(email) FROM users`
- C. `SELECT COUNT(email) - COUNT(*) FROM users`
- D. `SELECT COUNT(*) - COUNT(email) FROM users`

??? success "答えと解説"
    **正解: D**

    `COUNT(col)` は NULL を数えません。

    - A: 誤り。異なる値の数です。
    - B: 誤り。文字列の合計は求められません。
    - C: 誤り。負の値になります。
    - D: 正しい。

    **スキル:** [3.2.2](../domain3.md#skill-3-2-2) / **参照:** [Amazon Athena](../../../services/streaming.md#athena)

### 問8 {#q8}

ML の前処理のデータを、画面で検証して整え、自然言語でも変換します。どれを使いますか。

- A. Glue Data Quality の DQDL のルールを ETL で評価する方法
- B. SageMaker Canvas に統合された Data Wrangler
- C. DataBrew のレシピジョブ
- D. Athena の SQL のクエリ

??? success "答えと解説"
    **正解: B**

    Data Wrangler は Canvas に統合されました。

    - A: 誤り。検証のルールで、整形や自然言語の変換はしません。
    - B: 正しい。
    - C: 誤り。画面で整形できますが、ML の前処理と自然言語の変換の統合先は Canvas です。
    - D: 誤り。画面と自然言語の変換の機能ではありません。

    **スキル:** [3.2.2](../domain3.md#skill-3-2-2) / **参照:** [Data Wrangler](../../../services/sagemaker.md#data-wrangler)、[DataBrew](../../../services/data-engineering.md#databrew)

### 問9 {#q9}

届いたファイルの列数が正しいかを、到着時に検証して、不正なら別のプレフィックスへ移します。処理は数秒です。最も適切なものはどれですか。

- A. S3 イベントで起動する Lambda 関数
- B. 常時起動の EMR クラスターの Spark のジョブ
- C. Glue のクローラーを毎時実行して列数の変化を調べる運用
- D. Athena のクエリを人が毎朝実行して列数を確かめる運用

??? success "答えと解説"
    **正解: A**

    簡単な検証は Lambda で足ります。

    - A: 正しい。
    - B: 誤り。過剰です。
    - C: 誤り。到着時の検証にならず、ファイルも移せません。
    - D: 誤り。到着時の自動の検証になりません。

    **スキル:** [3.2.2](../domain3.md#skill-3-2-2) / **参照:** [呼び出しの種類](../../../services/lambda.md#invocation-types)、[S3 イベント通知](../../../services/messaging.md#s3-events)

### 問10 {#q10}

Glue の ETL の途中で不良レコードを隔離し、正常なデータだけを Redshift へ書き込みます。何を使いますか。

- A. ETL ジョブの中で Glue Data Quality を評価する
- B. Redshift へロードした後に `VACUUM` と `ANALYZE` を実行する
- C. CloudWatch のアラームで不良レコードを隔離する
- D. Data Catalog のテーブルを週次で評価する

??? success "答えと解説"
    **正解: A**

    ロードの前に悪いデータを止めます。

    - A: 正しい。
    - B: 誤り。領域の回収です。
    - C: 誤り。レコードの隔離はできません。
    - D: 誤り。保存済みのデータの評価で、ロードの前に止められません。

    **スキル:** [3.4.1](../domain3.md#skill-3-4-1) / **参照:** [Data Quality](../../../services/data-engineering.md#glue-data-quality)

### 問11 {#q11}

注文 ID が空でないことを確かめる DQDL のルールはどれですか。

- A. `RowCount > 0`
- B. `ColumnExists "order_id"`
- C. `IsUnique "order_id"`
- D. `IsComplete "order_id"`

??? success "答えと解説"
    **正解: D**

    `IsComplete` は空のフィールドがないことを確認します。

    - A: 誤り。行数の確認です。
    - B: 誤り。列の存在の確認です。
    - C: 誤り。一意性の確認です。
    - D: 正しい。

    **スキル:** [3.4.1](../domain3.md#skill-3-4-1) / **参照:** [Data Quality](../../../services/data-engineering.md#glue-data-quality)

### 問12 {#q12}

Data Quality の 2 つの入口の説明で正しいものはどれですか。（2つ選択）

- A. どちらの入口も評価するとスコアは出ない
- B. Data Catalog の入口は Kinesis の各レコードを受信の前に評価する
- C. ETL ジョブの入口はパイプラインの途中で評価する
- D. ETL ジョブの入口は DQDL を使えず、Python のみで書く
- E. Data Catalog の入口は保存済みのデータを評価する

??? success "答えと解説"
    **正解: C, E**

    目的で入口を選びます。

    - A: 誤り。スコアが出ます。
    - B: 誤り。ストリームの受信の機能ではありません。
    - C: 正しい。ロードの前に止められます。
    - D: 誤り。DQDL で書きます。
    - E: 正しい。スチュワードやアナリストに向きます。

    **スキル:** [3.4.1](../domain3.md#skill-3-4-1) / **参照:** [Data Quality](../../../services/data-engineering.md#glue-data-quality)

### 問13 {#q13}

アナリストが画面で「列 `APY` は 0〜100」「欠損は 5% 以下」のルールを作り、検証レポートを見ます。何を使いますか。

- A. CloudWatch のメトリクスフィルターに条件を書く
- B. DataBrew のルールセットとプロファイルジョブ
- C. Macie のカスタム識別子に範囲を書く
- D. Glue Data Quality の DQDL を ETL スクリプトに書く

??? success "答えと解説"
    **正解: B**

    DataBrew のルールセットで検証します。

    - A: 誤り。ログの機能です。
    - B: 正しい。
    - C: 誤り。機密データの検出です。
    - D: 誤り。アナリストの画面の操作ではありません。

    **スキル:** [3.4.2](../domain3.md#skill-3-4-2) / **参照:** [DataBrew](../../../services/data-engineering.md#databrew)、[Data Quality](../../../services/data-engineering.md#glue-data-quality)

### 問14 {#q14}

ステータスの列の値を許可された値に限定するルールはどれですか。

- A. `RowCount > 1000`
- B. `Completeness "status" > 0.95`
- C. `ColumnValues "status" in ["NEW", "PAID"]`
- D. `Uniqueness "status" > 0.99`

??? success "答えと解説"
    **正解: C**

    値の集合は `ColumnValues` で検査します。

    - A: 誤り。行数の確認です。
    - B: 誤り。欠損の割合の確認です。
    - C: 正しい。
    - D: 誤り。一意性の確認です。

    **スキル:** [3.4.2](../domain3.md#skill-3-4-2) / **参照:** [Data Quality](../../../services/data-engineering.md#glue-data-quality)

### 問15 {#q15}

DataBrew でルールを定義できない列はどれですか。

- A. 配列や構造体などの複合型の列
- B. 整数の値だけが入った列
- C. 欠損が多い小数の列
- D. 文字列の値だけが入り、長さが揃っていない列

??? success "答えと解説"
    **正解: A**

    複合型の列には列レベルのルールを定義できません。

    - A: 正しい。
    - B: 誤り。定義できます。
    - C: 誤り。定義でき、欠損の検査にも使えます。
    - D: 誤り。定義できます。

    **スキル:** [3.4.2](../domain3.md#skill-3-4-2) / **参照:** [DataBrew](../../../services/data-engineering.md#databrew)

### 問16 {#q16}

データの分布の変化を週次で確かめ、列の間の関係も確認します。どの機能ですか。

- A. Glue のクローラーのスキーマの変更ログ
- B. DataBrew のレシピジョブと S3 のレプリケーション
- C. DataBrew のプロファイルジョブと相関行列
- D. Athena の `TABLESAMPLE` で 1 回だけ目視で確認する

??? success "答えと解説"
    **正解: C**

    プロファイルの結果を定期的に比べます。

    - A: 誤り。スキーマの変更で、値の分布は見ません。
    - B: 誤り。整形と複製です。
    - C: 正しい。
    - D: 誤り。定期的な比較にならず、相関も見られません。

    **スキル:** [3.4.3](../domain3.md#skill-3-4-3) / **参照:** [DataBrew](../../../services/data-engineering.md#databrew)

### 問17 {#q17}

ETL の後に、ソースの S3 とターゲットの Redshift の件数が一致するかを確かめ、長期の異常も検知します。組み合わせはどれですか。

- A. S3 のオブジェクト数と Redshift の行数を比べ、WLM で監視する
- B. `COUNT(*)` を両方で比べ、Glue Data Quality の異常検出で監視する
- C. Glue のブックマークの値を比べ、Macie の結果で監視する
- D. `COUNT(*)` をソース側で 1 回だけ実行し、`VACUUM` の結果で一致を判断する

??? success "答えと解説"
    **正解: B**

    件数の一致と分布の監視を組み合わせます。

    - A: 誤り。オブジェクト数と行数は対応しません。
    - B: 正しい。
    - C: 誤り。件数の比較ではありません。
    - D: 誤り。両方を比べないと判断できません。

    **スキル:** [3.4.3](../domain3.md#skill-3-4-3) / **参照:** [Data Quality](../../../services/data-engineering.md#glue-data-quality)、[Amazon Athena](../../../services/streaming.md#athena)

### 問18 {#q18}

DynamoDB の GSI を読むと、書いた直後の値が古いことがあります。正しい説明はどれですか。

- A. 書き込みが古い値を上書きしているので、TTL を設定する必要がある
- B. DAX を使えば、GSI でも必ず最新の値を読める
- C. GSI の読み取りを `ConsistentRead=true` にすれば、必ず最新の値が読める
- D. GSI の読み取りは結果整合性で、強い整合性に対応しない

??? success "答えと解説"
    **正解: D**

    データの読み方にも一貫性の注意が必要です。

    - A: 誤り。TTL は削除の機能です。
    - B: 誤り。キャッシュで、整合性は上がりません。
    - C: 誤り。GSI は対応していません。
    - D: 正しい。

    **スキル:** [3.4.3](../domain3.md#skill-3-4-3) / **参照:** [読み取りの整合性](../../../services/dynamodb.md#read-consistency)

### 問19 {#q19}

Athena の TABLESAMPLE で、行単位の独立した抽出を行います。全ブロックのスキャンは許容します。どの指定ですか。

- A. `LIMIT 10`
- B. `ORDER BY 1 LIMIT 10`
- C. `TABLESAMPLE BERNOULLI (10)`
- D. `TABLESAMPLE SYSTEM (10)`

??? success "答えと解説"
    **正解: C**

    `BERNOULLI` は全ブロックをスキャンします。

    - A: 誤り。先頭の行を取り、偏ります。
    - B: 誤り。並び順で偏ります。
    - C: 正しい。
    - D: 誤り。セグメント単位で、独立性は保証されません。

    **スキル:** [3.4.4](../domain3.md#skill-3-4-4) / **参照:** [Amazon Athena](../../../services/streaming.md#athena)

### 問20 {#q20}

DataBrew のプロファイルでは問題なかった列に、本番で 0.1% の不正な値が見つかりました。既定の設定のままです。どう直しますか。

- A. プロファイルジョブのサンプルを既定の行数より減らす
- B. プロファイルジョブのサンプルを `FULL_DATASET` にする
- C. プロジェクトのサンプルを `FIRST_N` にして、先頭の行だけ確認する
- D. レシピジョブのバージョンを上げて、再度実行する

??? success "答えと解説"
    **正解: B**

    既定の 20,000 行ではまれな値を見落とします。

    - A: 誤り。見落としが増えます。
    - B: 正しい。
    - C: 誤り。整形の画面のサンプルです。
    - D: 誤り。整形の手順で、検査の範囲は変わりません。

    **スキル:** [3.4.4](../domain3.md#skill-3-4-4) / **参照:** [DataBrew](../../../services/data-engineering.md#databrew)

### 問21 {#q21}

少数の地域のデータが抜けないよう、地域ごとの比率を保ってサンプリングします。どの手法ですか。

- A. 系統サンプリング
- B. 先頭 N 行の抽出
- C. 単純ランダムサンプリング
- D. 層化サンプリング

??? success "答えと解説"
    **正解: D**

    グループごとに抽出すれば比率を保てます。

    - A: 誤り。周期的なデータでは偏ります。
    - B: 誤り。並び順で偏ります。
    - C: 誤り。少数のグループが抜けることがあります。
    - D: 正しい。

    **スキル:** [3.4.4](../domain3.md#skill-3-4-4) / **参照:** [DataBrew](../../../services/data-engineering.md#databrew)

### 問22 {#q22}

Redshift のテーブルの行の偏りを調べます。`DISTSTYLE KEY` の列の値が偏っています。確認と対処の組み合わせはどれですか。

- A. `SVV_TABLE_INFO` の `skew_rows` を確認し、値の種類が多い列を `DISTKEY` にする
- B. `STL_LOAD_ERRORS` を確認し、`MAXERROR` の値を増やす
- C. `STV_LOCKS` を確認し、`pg_terminate_backend` で該当のセッションをすべて切る
- D. `SVV_TRANSACTIONS` を確認し、Bucket Key を有効にする

??? success "答えと解説"
    **正解: A**

    `skew_rows` は最大と最小のスライスの行数の比です。

    - A: 正しい。
    - B: 誤り。ロードのエラーの設定です。
    - C: 誤り。ロックの話です。
    - D: 誤り。トランザクションの確認で、Bucket Key は S3 の機能です。

    **スキル:** [3.4.5](../domain3.md#skill-3-4-5) / **参照:** [分散スタイル](../../../services/data-engineering.md#redshift-distribution)

### 問23 {#q23}

Spark の結合で 1 つのタスクだけ長く、そのエグゼキューターが OOM になります。ワーカーを増やしても改善しません。適切な対処はどれですか。（2つ選択）

- A. 小さいテーブルをブロードキャストして結合する
- B. ジョブのブックマークを無効にして、同じ処理を繰り返す
- C. 偏ったキーに乱数を足すソルティングを行う
- D. 最大同時実行数を 2 にして、同じタスクを別の実行で動かす
- E. 同じキーの行をすべて 1 つのパーティションへ集める

??? success "答えと解説"
    **正解: A, C**

    同じキーは同じタスクに集まるので、ワーカーの追加は効きません。

    - A: 正しい。シャッフルを避けられます。
    - B: 誤り。偏りは解消しません。
    - C: 正しい。同じキーの集中を崩します。
    - D: 誤り。偏りは解消しません。
    - E: 誤り。偏りを悪化させます。

    **スキル:** [3.4.5](../domain3.md#skill-3-4-5) / **参照:** [DPU とワーカータイプ](../../../services/data-engineering.md#glue-dpu)、[分散スタイル](../../../services/data-engineering.md#redshift-distribution)

### 問24 {#q24}

データの偏りと対処の組み合わせで正しいものはどれですか。

- A. S3 のパーティションのサイズが偏るなら、パーティション列を `user_id` へ変える
- B. DynamoDB の特定のキーで制限されるなら、値の種類の少ないキーへ変える
- C. Redshift の日付の `DISTKEY` で狭い期間に偏るなら、より狭い期間で絞る
- D. Kinesis の一部のシャードだけ制限されるなら、シャードレベルのメトリクスで確認してキーを見直す

??? success "答えと解説"
    **正解: D**

    全体に余裕があるなら偏りを疑います。

    - A: 誤り。小さなファイルが大量にできます。
    - B: 誤り。偏りが悪化します。
    - C: 誤り。偏りが悪化します。
    - D: 正しい。

    **スキル:** [3.4.5](../domain3.md#skill-3-4-5) / **参照:** [パーティションキー](../../../services/streaming.md#partition-key)、[スロットリング](../../../services/dynamodb.md#throttling)
