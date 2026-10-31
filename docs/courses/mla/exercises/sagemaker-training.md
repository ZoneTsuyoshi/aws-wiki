# SageMaker AI の学習の問題集

対象の解説: [学習ジョブの設定](../../../services/sagemaker.md#training-job)、[自動モデルチューニング](../../../services/sagemaker.md#amt)、[収束の問題](../../../services/sagemaker.md#convergence)

### 問1 {#q1}

学習ジョブの結果を見ると、`TrainingTimeInSeconds` は 500、`BillableTimeInSeconds` は 100 でした。マネージドスポットでの節約率はどれですか。

- A. 50%
- B. 500%
- C. 20%
- D. 80%

??? success "答えと解説"
    **正解: D**

    (1 − 100 / 500) × 100 = 80% です。

    - A: 誤り。計算が合いません。
    - B: 誤り。学習時間を課金時間で割った値です。
    - C: 誤り。課金時間の割合です。
    - D: 正しい。

    **スキル:** [2.1.6](../domain2.md#skill-2-1-6) / **参照:** [マネージドスポット学習](../../../services/sagemaker.md#spot-training)

### 問2 {#q2}

GPU の学習を Managed Spot で行います。中断に備え、安く済ませます。必要な設定の組み合わせを選んでください。（2つ選択）

- A. `MaxWaitTimeInSeconds` を 0 にする
- B. チェックポイントを S3 に保存する
- C. `MaxWaitTimeInSeconds` を `MaxRuntimeInSeconds` より大きくする
- D. インスタンスを 1 台のストレージなしの構成にする
- E. 容量がなければオンデマンドに切り替わるので、上限を設定しない

??? success "答えと解説"
    **正解: B, C**

    `EnableManagedSpotTraining` を有効にし、待機の上限を実行の上限より大きくします。チェックポイントで再開できます。

    - A: 誤り。`MaxRuntimeInSeconds` より大きくする必要があります。
    - B: 正しい。中断後に途中から再開できます。
    - C: 正しい。
    - D: 誤り。中断への備えになりません。
    - E: 誤り。オンデマンドには切り替わりません。

    **スキル:** [2.1.6](../domain2.md#skill-2-1-6) / **参照:** [マネージドスポット学習](../../../services/sagemaker.md#spot-training)

### 問3 {#q3}

複雑な深層学習モデルが精度で少し勝ちますが、学習は 10 倍、コストも 10 倍です。週次の再学習で、業務上の精度の要件は単純なモデルも満たします。どう判断しますか。

- A. 単純なモデルを選ぶ
- B. 複雑なモデルをさらにインスタンスを増やして動かす
- C. AMT の試行を増やして、両方のモデルを調整し続ける
- D. 精度が高いので必ず複雑なモデルを選ぶ

??? success "答えと解説"
    **正解: A**

    要件を満たすなら、学習時間、コスト、解釈のしやすさでよい方を選びます。

    - A: 正しい。
    - B: 誤り。コストが増えます。通信のために時間は比例して減りません。
    - C: 誤り。ジョブの数だけコストが増え、要件はすでに満たしています。
    - D: 誤り。コストと時間、解釈のしやすさの代償を考えていません。

    **スキル:** [2.1.6](../domain2.md#skill-2-1-6) / **参照:** [インスタンスの選び方](../../../services/sagemaker.md#instance-selection)、[分散学習と時間短縮](../../../services/sagemaker.md#distributed-training)

### 問4 {#q4}

スクリプトモードで学習します。モデルを保存すると S3 に `model.tar.gz` で出力される場所はどこですか。

- A. `/tmp/model`
- B. `/opt/ml/model`
- C. `/opt/ml/output/data`
- D. `/opt/ml/input/data/train`

??? success "答えと解説"
    **正解: B**

    `SM_MODEL_DIR` が指す `/opt/ml/model` に保存します。

    - A: 誤り。`/opt/ml/model` の外に保存したモデルは失われます。
    - B: 正しい。
    - C: 誤り。その他の成果物の場所です。
    - D: 誤り。入力データの場所です。

    **スキル:** [2.2.2](../domain2.md#skill-2-2-2) / **参照:** [スクリプトモード](../../../services/sagemaker.md#script-mode)

### 問5 {#q5}

スクリプトモードで Python の追加パッケージを使います。OS のライブラリは不要です。最も手間の小さい方法はどれですか。

- A. スクリプトの中で毎回 EC2 に SSH して入れる
- B. ビルド済みのイメージを拡張して ECR に置き、ジョブごとに指定する
- C. `source_dir` の `requirements.txt` に書く
- D. 独自のコンテナをゼロから作る

??? success "答えと解説"
    **正解: C**

    追加のパッケージは `source_dir` の `requirements.txt` に書きます。

    - A: 誤り。SageMaker AI の学習ジョブの動作ではありません。
    - B: 誤り。OS のライブラリなどを足すときの方法で、より手間がかかります。
    - C: 正しい。
    - D: 誤り。対応しないフレームワークのときの方法です。

    **スキル:** [2.2.2](../domain2.md#skill-2-2-2) / **参照:** [スクリプトモード](../../../services/sagemaker.md#script-mode)

### 問6 {#q6}

`train` チャネルでデータを渡しました。スクリプトの中でデータのパスを取得する方法はどれですか。

- A. `S3_BUCKET` を読み、自分でダウンロードする
- B. `SM_CHANNEL_TRAIN` を読む
- C. `SM_OUTPUT_DATA_DIR` を読む
- D. `SM_MODEL_DIR` を読む

??? success "答えと解説"
    **正解: B**

    環境変数 `SM_CHANNEL_<チャネル名>` が `/opt/ml/input/data/<チャネル名>` を指します。

    - A: 誤り。チャネルのデータは `/opt/ml/input/data/train` に置かれます。
    - B: 正しい。
    - C: 誤り。その他の成果物の出力先です。
    - D: 誤り。モデルの保存先です。

    **スキル:** [2.2.2](../domain2.md#skill-2-2-2) / **参照:** [スクリプトモード](../../../services/sagemaker.md#script-mode)

### 問7 {#q7}

ニューラルネットの調整で、エポックごとに指標を出せます。少ない計算資源で多くの候補を試し、見込みのないものへの割り当てを減らします。戦略と設定の組み合わせはどれですか。

- A. Hyperband と `TrainingJobEarlyStoppingType` の `Off`
- B. Bayesian と `MaxWaitTimeInSeconds` の 0、チェックポイントの無効化
- C. Grid と `Auto`
- D. Random と `Auto`

??? success "答えと解説"
    **正解: A**

    Hyperband は途中の結果で資源を配分し直します。独自の早期停止を持つので、`TrainingJobEarlyStoppingType` は `Off` にします。

    - A: 正しい。
    - B: 誤り。`MaxWaitTimeInSeconds` はスポットの設定です。
    - C: 誤り。Grid はカテゴリのパラメータだけです。
    - D: 誤り。途中の結果を使いません。

    **スキル:** [2.2.3](../domain2.md#skill-2-2-3) / **参照:** [自動モデルチューニング](../../../services/sagemaker.md#amt)

### 問8 {#q8}

学習率の探索範囲は 0.0001〜0.1 です。桁で広く探したいです。`ScalingType` はどれですか。

- A. `Linear`
- B. `Categorical`
- C. `Logarithmic`
- D. `ReverseLogarithmic`

??? success "答えと解説"
    **正解: C**

    学習率のように桁が変わる範囲は `Logarithmic` にします。

    - A: 誤り。大きい値の側に試行が偏ります。
    - B: 誤り。`ScalingType` の値ではありません。
    - C: 正しい。
    - D: 誤り。1 に近い範囲で細かく探すときに使います。

    **スキル:** [2.2.3](../domain2.md#skill-2-2-3) / **参照:** [自動モデルチューニング](../../../services/sagemaker.md#amt)

### 問9 {#q9}

前回のチューニングの結果を活かして、データは同じまま探索範囲だけ広げます。ウォームスタートの設定として正しいものはどれですか。

- A. `TRANSFER_LEARNING`、親は 1 つだけ
- B. `TRANSFER_LEARNING`、親は最大 10
- C. `IDENTICAL_DATA_AND_ALGORITHM`、親は最大 100
- D. `IDENTICAL_DATA_AND_ALGORITHM`、親は最大 5

??? success "答えと解説"
    **正解: D**

    同じデータなら `IDENTICAL_DATA_AND_ALGORITHM` で、親は最大 5 個です。

    - A: 誤り。データを変えるときの種類で、親は 1 つに限りません。
    - B: 誤り。データを変えるときの種類で、親の数も違います。
    - C: 誤り。親は最大 5 です。
    - D: 正しい。

    **スキル:** [2.2.3](../domain2.md#skill-2-2-3) / **参照:** [自動モデルチューニング](../../../services/sagemaker.md#amt)

### 問10 {#q10}

データが大きすぎて 1 台では学習が間に合いません。モデルは 1 枚の GPU に載ります。どの手法ですか。

- A. 早期停止だけを使う
- B. Provisioned Concurrency
- C. モデル並列（SMP）
- D. データ並列（SMDDP）

??? success "答えと解説"
    **正解: D**

    データが大きいならデータ並列、モデルが大きいならモデル並列です。

    - A: 誤り。改善しないジョブを止める手法で、データの量の問題は解決しません。
    - B: 誤り。サーバーレス推論の機能です。
    - C: 誤り。モデルが 1 枚の GPU に載らないときの手法です。
    - D: 正しい。

    **スキル:** [2.2.4](../domain2.md#skill-2-2-4) / **参照:** [分散学習と時間短縮](../../../services/sagemaker.md#distributed-training)

### 問11 {#q11}

数週間かかる大規模な FM の学習で、ノードの障害が起きても自動で回復して続けたいです。どの選択が適切ですか。

- A. サーバーレス推論
- B. HyperPod
- C. Bedrock のオンデマンド推論
- D. Lambda の関数で学習を分割して実行する

??? success "答えと解説"
    **正解: B**

    HyperPod は長時間の大規模な FM の学習に向き、ノード障害から回復します。

    - A: 誤り。推論の方式で、学習には使えません。
    - B: 正しい。
    - C: 誤り。推論の方式で、学習の基盤ではありません。
    - D: 誤り。実行時間の上限があり、大規模な学習には向きません。

    **スキル:** [2.2.4](../domain2.md#skill-2-2-4) / **参照:** [分散学習と時間短縮](../../../services/sagemaker.md#distributed-training)

### 問12 {#q12}

学習ジョブの開始までが長く、CloudWatch を見るとデータのダウンロードに時間がかかっています。モデルやインスタンスは変えません。適切な対応はどれですか。

- A. 入力モードを FastFile に変える
- B. エポックを減らす
- C. 正則化を強くする
- D. `MaxRuntimeInSeconds` を延ばす

??? success "答えと解説"
    **正解: A**

    全データのダウンロードが原因なら、FastFile に変えて読むときに取得します。

    - A: 正しい。
    - B: 誤り。ダウンロードの時間は変わりません。
    - C: 誤り。過学習の対策です。
    - D: 誤り。上限を延ばすだけで、時間は減りません。

    **スキル:** [2.2.4](../domain2.md#skill-2-2-4) / **参照:** [入力モード](../../../services/sagemaker.md#input-modes)

### 問13 {#q13}

学習の開始直後から損失が `NaN` になります。原因の候補と対応の組み合わせを選んでください。（2つ選択）

- A. 過学習。データを増やす
- B. エポックが少ない。増やす
- C. 勾配爆発。勾配クリッピングを使う
- D. 学習率が高い。下げる
- E. GPU の使用率が低い。ローダーを並列化する

??? success "答えと解説"
    **正解: C, D**

    損失の発散や `NaN` は、学習率の高さ、勾配爆発、欠損が原因の候補です。

    - A: 誤り。`NaN` の直接の原因ではありません。
    - B: 誤り。開始直後の発散は直りません。
    - C: 正しい。
    - D: 正しい。
    - E: 誤り。読み込みの問題で、`NaN` の原因ではありません。

    **スキル:** [2.3.5](../domain2.md#skill-2-3-5) / **参照:** [収束の問題](../../../services/sagemaker.md#convergence)

### 問14 {#q14}

深いネットワークで、入力に近い層の勾配がほぼ 0 になり、学習が進みません。適切な対応はどれですか。

- A. 層をさらに深くする
- B. データの入力モードを Pipe に変える
- C. ReLU と残差接続、正規化を使う
- D. 学習率をさらに下げる

??? success "答えと解説"
    **正解: C**

    勾配消失には、ReLU、残差接続、正規化で対応します。

    - A: 誤り。勾配消失が悪化します。
    - B: 誤り。読み込みの設定で、勾配の問題に関係しません。
    - C: 正しい。
    - D: 誤り。学習がさらに進まなくなります。

    **スキル:** [2.3.5](../domain2.md#skill-2-3-5) / **参照:** [収束の問題](../../../services/sagemaker.md#convergence)

### 問15 {#q15}

新規に作るプロジェクトで、学習の指標とプロファイルを監視します。SageMaker Debugger の新規受付は終了しています。公式の移行先の組み合わせはどれですか。

- A. Bedrock Evaluations と Inspector
- B. 指標は X-Ray のトレース、プロファイルは Config のルールとタイムライン
- C. Augmented AI と Macie
- D. 指標は MLflow と TensorBoard、プロファイルは CloudWatch

??? success "答えと解説"
    **正解: D**

    Debugger の移行先は、学習の指標に MLflow と TensorBoard、プロファイルに CloudWatch です。

    - A: 誤り。FM の評価と脆弱性の検査で、学習の監視ではありません。
    - B: 誤り。分散トレースと設定の記録で、学習の指標の移行先ではありません。
    - C: 誤り。人のレビューと機密データの検出です。
    - D: 正しい。

    **スキル:** [2.3.5](../domain2.md#skill-2-3-5) / **参照:** [Debugger](../../../services/sagemaker.md#debugger)

### 問16 {#q16}

学習ジョブが終盤に、S3 への出力の権限不足で失敗しました。原因の設定はどれですか。

- A. `StoppingCondition` の `MaxRuntimeInSeconds`
- B. `OutputDataConfig` の出力先と実行ロールの権限
- C. `ResourceConfig` のボリュームサイズ
- D. `InputDataConfig` のチャネル名

??? success "答えと解説"
    **正解: B**

    `OutputDataConfig` の権限不足は最後に失敗します。実行ロールの S3 と KMS の権限を確認します。

    - A: 誤り。時間の上限で止まる設定です。
    - B: 正しい。
    - C: 誤り。`No space left` の原因です。
    - D: 誤り。チャネル名の誤りは開始時の実行時エラーです。

    **スキル:** [3.3.3](../domain3.md#skill-3-3-3) / **参照:** [学習ジョブの設定](../../../services/sagemaker.md#training-job)

### 問17 {#q17}

バッチ変換で 1 ファイル 50 GB の CSV を処理します。インスタンスを 4 台にしましたが 1 台しか働きません。適切な対応はどれですか。

- A. 入力を複数のファイルに分割して S3 に置く
- B. `SplitType` を `Line` にする
- C. `MaxConcurrentTransforms` を 100 にする
- D. インスタンスをさらに増やす

??? success "答えと解説"
    **正解: A**

    バッチ変換はファイル単位でインスタンスに割り当てます。1 ファイルなら 1 台しか働かないので、入力を複数のファイルに分割します。`SplitType` はファイルをミニバッチに分ける設定で、台数への分散にはなりません。

    - A: 正しい。
    - B: 誤り。1 ファイルがミニバッチに分かれるだけで、そのファイルは 1 台に割り当てられたままです。
    - C: 誤り。1 ファイルが 1 台に割り当てられる問題は解決しません。積の上限にも注意が必要です。
    - D: 誤り。ファイルの単位で割り当てるので、増やしても働きません。

    **スキル:** [3.3.3](../domain3.md#skill-3-3-3) / **参照:** [バッチ変換](../../../services/sagemaker.md#batch-transform)

### 問18 {#q18}

バッチ変換で、入力の ID の列を除いて推論し、結果を ID と結合して出力します。正しい設定はどれですか。

- A. `InitialVariantWeight` と `TargetVariant`
- B. `EnableNetworkIsolation`、`VpcConfig`、`KmsKeyId`
- C. `InputFilter`、`JoinSource`、`OutputFilter`
- D. `MaxPayloadInMB` と `SplitType`

??? success "答えと解説"
    **正解: C**

    `InputFilter`、`JoinSource`、`OutputFilter` で、ID を除いて推論し、結果と結合します。

    - A: 誤り。A/B テストの設定です。
    - B: 誤り。ネットワークと暗号化の設定です。
    - C: 正しい。
    - D: 誤り。サイズと分割の設定で、列の選択と結合はできません。

    **スキル:** [3.3.3](../domain3.md#skill-3-3-3) / **参照:** [バッチ変換](../../../services/sagemaker.md#batch-transform)
