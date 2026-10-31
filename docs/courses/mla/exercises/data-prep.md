# データ変換と特徴量の問題集

対象の解説: [Data Wrangler](../../../services/sagemaker.md#data-wrangler)、[Feature Store](../../../services/sagemaker.md#feature-store)、[特徴量エンジニアリング](../../../services/ai-fundamentals.md#feature-engineering)

### 問1 {#q1}

分析担当者がコードを書かずに、売上データの整形手順を画面で作り、毎月同じ手順を再利用します。ML の専用の機能は要りません。どれを選びますか。

- A. EMR の Spark
- B. SageMaker Processing
- C. Glue の Spark ジョブのスクリプトを自分で書く
- D. Glue DataBrew

??? success "答えと解説"
    **正解: D**

    分析担当が画面で整形し、レシピを再利用するなら DataBrew です。ML の前処理の文脈なら Data Wrangler を選びます。

    - A: 誤り。クラスターとコードの管理が必要です。
    - B: 誤り。コードで組み込む機能です。
    - C: 誤り。コードを書く必要があります。
    - D: 正しい。

    **スキル:** [1.2.1](../domain1.md#skill-1-2-1) / **参照:** [DataBrew](../../../services/data-engineering.md#databrew)、[Data Wrangler](../../../services/sagemaker.md#data-wrangler)

### 問2 {#q2}

データサイエンティストが画面で ML の前処理を試し、結果を Feature Store と Pipelines へ渡したいです。どれを選びますか。

- A. Glue Studio のビジュアルエディタで作るジョブ
- B. Data Wrangler のデータフロー
- C. Athena の CTAS
- D. Glue DataBrew

??? success "答えと解説"
    **正解: B**

    ML の前処理を画面で試し、Pipelines や Feature Store へ渡すなら Data Wrangler です。

    - A: 誤り。ETL の作成が中心で、Feature Store や Pipelines へ渡す ML の前処理の機能ではありません。
    - B: 正しい。
    - C: 誤り。SQL による変換で、画面で試しながら作る機能ではありません。
    - D: 誤り。分析担当向けの整形に向きます。ML のパイプラインとの連携を問う場面では第一候補になりません。

    **スキル:** [1.2.1](../domain1.md#skill-1-2-1) / **参照:** [Data Wrangler](../../../services/sagemaker.md#data-wrangler)

### 問3 {#q3}

既に Spark の独自コードがあり、クラスターの構成や Spark の設定を細かく調整します。大規模な変換です。どれが適切ですか。

- A. EMR のクラスターで Spark を実行する
- B. SageMaker の Data Wrangler で画面から再現する
- C. Lambda を多数並列に動かして変換する
- D. Glue DataBrew のレシピに書き換える

??? success "答えと解説"
    **正解: A**

    既存の Spark コードとクラスターの細かい制御が要るなら EMR です。

    - A: 正しい。
    - B: 誤り。コードを活かせず、細かな制御もできません。
    - C: 誤り。Spark のコードが動かず、長時間の大規模処理には向きません。
    - D: 誤り。既存のコードを活かせません。

    **スキル:** [1.2.1](../domain1.md#skill-1-2-1) / **参照:** [EMR](../../../services/data-engineering.md#emr)

### 問4 {#q4}

不正検知で、推論時に顧客の最新の特徴量を低遅延で読み、再学習には過去の値を使います。Feature Store のフィーチャーグループの設定として適切なものはどれですか。

- A. どちらも無効にして、S3 に直接書き込む
- B. オフラインストアだけを有効にする
- C. オンラインストアとオフラインストアの両方を有効にする
- D. オンラインストアだけを有効にする

??? success "答えと解説"
    **正解: C**

    オンラインは最新のレコードを低遅延で返し、オフラインは全履歴を S3 に保存します。

    - A: 誤り。Feature Store の機能を使わず、学習と推論のずれも防げません。
    - B: 誤り。推論時の低遅延の読み取りができません。
    - C: 正しい。
    - D: 誤り。履歴が残らないので、再学習に使えません。

    **スキル:** [1.2.2](../domain1.md#skill-1-2-2) / **参照:** [Feature Store](../../../services/sagemaker.md#feature-store)

### 問5 {#q5}

推論では最新の値を読み、学習では特徴量の履歴を検索します。それぞれの方法の組み合わせとして正しいものはどれですか。

- A. 推論も学習も `PutRecord` で読み取る
- B. 推論は `BatchTransform`、学習は `DeleteRecord` を使う
- C. 推論は `GetRecord`、学習はオフラインストアを Athena で検索する
- D. 推論はオフラインストアを Athena で検索し、学習は `GetRecord` を使う

??? success "答えと解説"
    **正解: C**

    オンラインストアの最新のレコードは `GetRecord` で読み、オフラインストアの履歴は Athena で検索します。

    - A: 誤り。`PutRecord` は書き込みの API です。
    - B: 誤り。どちらも特徴量の読み取りの方法ではありません。
    - C: 正しい。
    - D: 誤り。逆です。Athena の検索は低遅延の推論に向かず、`GetRecord` は最新の値しか返しません。

    **スキル:** [1.2.2](../domain1.md#skill-1-2-2) / **参照:** [Feature Store](../../../services/sagemaker.md#feature-store)

### 問6 {#q6}

学習のノートブックと推論のコードで計算方法が別々になり、本番の精度が検証より大きく落ちました。この問題の名前と、最も直接の対策はどれですか。

- A. 学習と推論のずれです。Feature Store で特徴量を共有します
- B. 過少適合です。エポックを増やします
- C. コンセプトドリフトです。正解ラベルを増やします
- D. 破滅的忘却です。学習率を下げます

??? success "答えと解説"
    **正解: A**

    学習と推論のずれ（training-serving skew）は、同じ特徴量を Feature Store から使うことで減らせます。

    - A: 正しい。
    - B: 誤り。検証の精度は高いので過少適合ではありません。
    - C: 誤り。入力と正解の関係の変化ではなく、計算方法の違いが原因です。
    - D: 誤り。新しいデータだけの追加学習で起きる現象で、この症状とは別です。

    **スキル:** [1.2.2](../domain1.md#skill-1-2-2) / **参照:** [Feature Store](../../../services/sagemaker.md#feature-store)

### 問7 {#q7}

フィーチャーグループを作成します。スキーマの中で定義が必須の特徴はどれですか。（2つ選択）

- A. 正解ラベル（`TargetAttributeName`）
- B. Athena のワークグループ名
- C. 期限（`TtlDuration`）
- D. レコード ID（`RecordIdentifierFeatureName`）
- E. イベント時刻（`EventTimeFeatureName`）

??? success "答えと解説"
    **正解: D, E**

    レコード ID とイベント時刻は必須です。イベント時刻でレコードの新旧を判断します。

    - A: 誤り。フィーチャーグループの必須項目ではありません。
    - B: 誤り。フィーチャーグループの定義に含まれません。
    - C: 誤り。任意の設定で、期限を過ぎたレコードを削除するときに使います。
    - D: 正しい。
    - E: 正しい。

    **スキル:** [1.1.9](../domain1.md#skill-1-1-9) / **参照:** [Feature Store](../../../services/sagemaker.md#feature-store)

### 問8 {#q8}

Kinesis のイベントを Lambda で集計し、結果を 1 件ずつ Feature Store へ書き込みます。使う操作はどれですか。

- A. `StartPipelineExecution`
- B. `BatchGetRecord`
- C. `GetRecord`
- D. `PutRecord`

??? success "答えと解説"
    **正解: D**

    ストリームやバッチから 1 件ずつ書くなら `PutRecord` です。

    - A: 誤り。Pipelines の実行を開始する操作です。
    - B: 誤り。複数のレコードをまとめて読む API です。
    - C: 誤り。読み取りの API です。
    - D: 正しい。

    **スキル:** [1.1.9](../domain1.md#skill-1-1-9) / **参照:** [Feature Store](../../../services/sagemaker.md#feature-store)

### 問9 {#q9}

数億件の過去データを、まとめてフィーチャーグループへ取り込みます。最も適した方法はどれですか。

- A. Firehose の配信先に指定して書き込む
- B. Spark コネクタで DataFrame をまとめて書き込む
- C. Lambda から `PutRecord` を 1 件ずつ順に呼ぶ
- D. Athena の `INSERT` でオフラインストアの表へ書く

??? success "答えと解説"
    **正解: B**

    大量のバッチは Spark コネクタを使います。前処理の結果なら Data Wrangler や Canvas から出力する方法もあります。

    - A: 誤り。Firehose の配信先は S3 や OpenSearch などで、Feature Store の取り込みの方法ではありません。
    - B: 正しい。
    - C: 誤り。大量のバッチでは時間がかかり、Lambda の実行時間の上限にも当たりやすくなります。
    - D: 誤り。オンラインストアに届かず、Feature Store の取り込みの方法でもありません。

    **スキル:** [1.1.9](../domain1.md#skill-1-1-9) / **参照:** [Feature Store](../../../services/sagemaker.md#feature-store)

### 問10 {#q10}

年収の列は右に長い分布で、10 万から 1 億まで広がります。線形モデルの前に行う変換として最も適切なものはどれですか。

- A. 最小最大の正規化
- B. ワンホットエンコーディング
- C. 対数変換を適用する
- D. Z スコアで標準化する

??? success "答えと解説"
    **正解: C**

    右に長い分布は対数変換で整えます。桁が大きく違う値の差を圧縮できます。

    - A: 誤り。尺度は揃いますが、分布の偏りは残ります。
    - B: 誤り。順序のないカテゴリ向けです。
    - C: 正しい。
    - D: 誤り。平均と分散は揃いますが、右に長い形はそのままです。

    **スキル:** [1.2.4](../domain1.md#skill-1-2-4) / **参照:** [特徴量エンジニアリング](../../../services/ai-fundamentals.md#feature-engineering)

### 問11 {#q11}

平均 50、標準偏差 10 の列を標準化します。値が 70 のとき、結果はどれですか。

- A. 0.7
- B. 1.0
- C. 20
- D. 2.0

??? success "答えと解説"
    **正解: D**

    標準化は (値 − 平均) / 標準偏差です。(70 − 50) / 10 = 2.0 です。

    - A: 誤り。70 を 100 で割った値で、標準化ではありません。
    - B: 誤り。1 標準偏差分の差のときの値です。
    - C: 誤り。平均との差のままで、標準偏差で割っていません。
    - D: 正しい。

    **スキル:** [1.2.4](../domain1.md#skill-1-2-4) / **参照:** [特徴量エンジニアリング](../../../services/ai-fundamentals.md#feature-engineering)

### 問12 {#q12}

全データの平均と標準偏差で標準化したあとに学習用とテスト用へ分割した結果、テストの指標が本番よりよくなりました。正しい手順はどれですか。

- A. 標準化をやめて、XGBoost 以外のモデルも尺度を揃えずに使う
- B. 先に分割し、学習データの統計値で学習、検証、テストを変換する
- C. テストデータの平均だけで標準化してから分割する
- D. 全データで計算し、テストだけもう一度標準化する

??? success "答えと解説"
    **正解: B**

    統計値は学習データだけで計算し、同じ値を検証とテストにも使います。これでデータ漏えいを防げます。

    - A: 誤り。k-means や線形モデルでは桁の大きい列が結果を支配します。
    - B: 正しい。
    - C: 誤り。テストの情報を使うので、データ漏えいのままです。
    - D: 誤り。全データを使う時点でテストの情報が混ざり、データ漏えいは解消しません。

    **スキル:** [1.2.4](../domain1.md#skill-1-2-4) / **参照:** [特徴量エンジニアリング](../../../services/ai-fundamentals.md#feature-engineering)

### 問13 {#q13}

年収の列に欠損があり、極端に高い外れ値も少数あります。分布を大きく歪めずに補完する方法はどれですか。

- A. 中央値で補完する
- B. 全ての列を削除する
- C. 平均で補完する
- D. 最大値で補完する

??? success "答えと解説"
    **正解: A**

    外れ値がある数値の列は、中央値での補完が適しています。

    - A: 正しい。
    - B: 誤り。情報を失い、補完にもなりません。
    - C: 誤り。平均は外れ値に引っ張られます。
    - D: 誤り。分布を大きく歪めます。

    **スキル:** [1.3.7](../domain1.md#skill-1-3-7) / **参照:** [データ品質](../../../services/ai-fundamentals.md#data-quality)

### 問14 {#q14}

2 つの顧客データベースを統合します。共通の ID がなく、氏名や住所の表記も少しずつ違います。同じ顧客のレコードを照合する機能はどれですか。

- A. Lake Formation の FindMatches
- B. Athena の `DISTINCT` で重複を削除する
- C. 重複のない ID を各行に振り直す
- D. 完全に一致する行の削除

??? success "答えと解説"
    **正解: A**

    FindMatches は、共通の ID がなく値も完全には一致しないレコードを照合する ML の変換です。Glue のジョブで作成して実行します。

    - A: 正しい。
    - B: 誤り。完全に同じ行しか除外できません。
    - C: 誤り。新しい ID を振っても、同じ顧客であることは判定できません。
    - D: 誤り。表記の違う重複は見つかりません。

    **スキル:** [1.3.7](../domain1.md#skill-1-3-7) / **参照:** [データ品質](../../../services/ai-fundamentals.md#data-quality)

### 問15 {#q15}

ラベルのないセンサーデータの中から、異常なレコードを見つけて前処理で確認したいです。SageMaker AI の組み込みアルゴリズムはどれですか。

- A. DeepAR
- B. BlazingText
- C. Factorization Machines
- D. Random Cut Forest

??? success "答えと解説"
    **正解: D**

    Random Cut Forest は、ラベルなしで異常なレコードを見つけられます。

    - A: 誤り。時系列の予測のアルゴリズムです。
    - B: 誤り。テキストのアルゴリズムです。
    - C: 誤り。高次元の疎データ向けで、異常検知のアルゴリズムではありません。
    - D: 正しい。

    **スキル:** [1.3.7](../domain1.md#skill-1-3-7) / **参照:** [組み込みアルゴリズム](../../../services/sagemaker.md#built-in-algorithms)
