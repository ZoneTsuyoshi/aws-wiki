# SageMaker AI の推論の問題集

対象の解説: [エンドポイントと推論](../../../services/sagemaker.md#endpoints)、[自動スケーリング](../../../services/sagemaker.md#autoscaling)、[インスタンスの選び方](../../../services/sagemaker.md#instance-selection)

### 問1 {#q1}

会社は既に EKS でアプリを運用しており、同じクラスターの運用手順でモデルも動かしたいです。デプロイ先はどれですか。

- A. 既存の EKS クラスターに Pod として配置する
- B. Lambda のコンテナイメージにモデルを入れる
- C. SageMaker AI のエンドポイントを新設する
- D. ECS on Fargate に別の手順で配置する

??? success "答えと解説"
    **正解: A**

    既存の Kubernetes に載せるなら EKS です。

    - A: 正しい。
    - B: 誤り。小さなモデルや短い処理の選択です。
    - C: 誤り。ML に特化した管理機能が要るときの選択で、既存の Kubernetes の運用を活かせません。
    - D: 誤り。既存の Kubernetes の運用手順を活かせません。

    **スキル:** [3.1.1](../domain3.md#skill-3-1-1) / **参照:** [コンテナ](../../../services/containers.md#eks)、[エンドポイントと推論](../../../services/sagemaker.md#endpoints)

### 問2 {#q2}

小さなモデルの推論が 1 日に数十回だけ発生し、処理は数秒です。コンテナは 1 つで、GPU は不要です。手間とコストが小さいデプロイ先を選んでください。（2つ選択）

- A. Lambda
- B. 大きな EC2 のインスタンスを 24 時間動かす
- C. SageMaker AI のサーバーレス推論
- D. HyperPod のクラスター
- E. 常時稼働の GPU のリアルタイムエンドポイント

??? success "答えと解説"
    **正解: A, C**

    断続的で短い処理なら、Lambda かサーバーレス推論が候補です。

    - A: 正しい。小さなモデル、短い処理、断続的な呼び出しに向きます。
    - B: 誤り。管理とアイドルのコストがかかります。
    - C: 正しい。アイドルの費用がかからず、断続的な負荷に向きます。
    - D: 誤り。大規模な FM の学習や推論のクラスターです。
    - E: 誤り。アイドルの時間にも課金されます。

    **スキル:** [3.1.1](../domain3.md#skill-3-1-1) / **参照:** [サーバーレス](../../../services/sagemaker.md#serverless)、[エンドポイントと推論](../../../services/sagemaker.md#endpoints)

### 問3 {#q3}

コンテナで動く夜間の特徴量計算と推論のジョブを、キューに入れて順に実行します。SageMaker AI の機能は使わず、計算資源の管理は任せます。どれを選びますか。

- A. Bedrock のバッチ推論
- B. AWS Batch のジョブキューに登録する
- C. ECS のサービスを 24 時間動かし続ける
- D. EventBridge から Lambda を順に起動する

??? success "答えと解説"
    **正解: B**

    コンテナのバッチジョブを順に実行するなら AWS Batch です。

    - A: 誤り。FM のトークン課金の処理で、独自のコンテナは動かせません。
    - B: 正しい。
    - C: 誤り。常時動くサービスの構成で、順次のバッチジョブの管理には向きません。
    - D: 誤り。実行時間の上限があり、長いジョブのキューの管理にも向きません。

    **スキル:** [3.1.1](../domain3.md#skill-3-1-1) / **参照:** [AWS Batch](../../../services/other-services.md#batch)

### 問4 {#q4}

顧客ごとの似たモデルが 3,000 個あり、同じフレームワークです。各モデルの利用はまれです。費用を抑えたいです。どの方式ですか。

- A. 推論コンポーネントをモデルごとに作る
- B. 推論パイプラインの 15 個のコンテナに並べる
- C. 1 つのマルチモデルエンドポイントに載せる
- D. モデルごとに専用のエンドポイントを作る

??? success "答えと解説"
    **正解: C**

    マルチモデルは同じコンテナで多数のモデルを共有します。`TargetModel` で指定し、S3 から動的に読み込みます。

    - A: 誤り。モデルごとに資源を割り当てる方式で、まれにしか使わない 3,000 個には割高です。
    - B: 誤り。コンテナを順に実行する機能で、上限も 15 個です。
    - C: 正しい。
    - D: 誤り。3,000 個分のインスタンスが必要になります。

    **スキル:** [3.1.2](../domain3.md#skill-3-1-2) / **参照:** [マルチモデル](../../../services/sagemaker.md#multi-model)

### 問5 {#q5}

多様な AWS サービスと人の承認を含む業務の流れの中で、学習を 1 ステップとして実行します。どのオーケストレーターを選びますか。

- A. CloudFormation のスタックで順に実行する
- B. Airflow の既存資産はないが MWAA を新設する
- C. SageMaker Pipelines だけで人の承認と全サービスを組む
- D. Step Functions の状態として学習を組み込む

??? success "答えと解説"
    **正解: D**

    多様な AWS サービスを含む業務の流れには Step Functions です。ML の専用機能が中心なら Pipelines、Airflow の資産があれば MWAA です。

    - A: 誤り。インフラの定義で、業務の流れの実行には向きません。
    - B: 誤り。MWAA は Airflow の資産を活かす場面に向きます。
    - C: 誤り。ML の専用機能が中心のワークフローに向きます。
    - D: 正しい。

    **スキル:** [3.1.2](../domain3.md#skill-3-1-2) / **参照:** [Step Functions](../../../services/step-functions.md#orchestration-choreography)、[SageMaker Pipelines と使い分け](../../../services/sagemaker.md#pipelines)

### 問6 {#q6}

前処理の scikit-learn と推論の XGBoost を順に実行し、呼び出し側は 1 回の呼び出しで済ませます。どの方式ですか。

- A. マルチモデルエンドポイントで 2 つを切り替える
- B. 2 つのコンテナを推論パイプラインに並べる
- C. A/B テストで 50% ずつに分ける
- D. 推論コンポーネントを 2 つ作り、呼び出し側で順に呼ぶ

??? success "答えと解説"
    **正解: B**

    推論パイプラインは 2〜15 個のコンテナを順に実行します。通常の呼び出しで済みます。

    - A: 誤り。同じコンテナでモデルを切り替える機能で、順に実行しません。
    - B: 正しい。
    - C: 誤り。順に実行せず、どちらかに分かれます。
    - D: 誤り。呼び出しが 2 回になります。

    **スキル:** [3.1.2](../domain3.md#skill-3-1-2) / **参照:** [マルチモデル](../../../services/sagemaker.md#multi-model)

### 問7 {#q7}

動画の解析です。入力は 500 MB、処理は 20 分です。利用者は結果を後で受け取ります。どの推論の方式ですか。

- A. リアルタイム推論で 1 回ごとに呼ぶ
- B. バッチ変換のジョブを依頼ごとに作る
- C. サーバーレス推論のメモリを最大にする
- D. 非同期推論で S3 の入力を渡す

??? success "答えと解説"
    **正解: D**

    非同期は入力 1 GB まで、処理 1 時間までです。

    - A: 誤り。入力の上限は API リファレンスで 6 MB（FAQ は 25 MB）、処理は 60 秒です。
    - B: 誤り。データセット全体を一括で処理する方式で、利用者ごとの依頼を受ける形に向きません。
    - C: 誤り。GPU も使えず、この規模の入力には向きません。
    - D: 正しい。

    **スキル:** [3.1.3](../domain3.md#skill-3-1-3) / **参照:** [非同期](../../../services/sagemaker.md#async)

### 問8 {#q8}

毎晩、S3 の数百万件のデータセット全体にスコアを付けます。常時稼働のエンドポイントは不要です。どの方式ですか。

- A. 非同期推論を 1 件ずつ呼び続ける
- B. サーバーレスに全件を順に送る
- C. バッチ変換のジョブを毎晩実行する
- D. リアルタイムを 24 時間動かす

??? success "答えと解説"
    **正解: C**

    データセット全体を一度に処理するならバッチ変換です。インスタンスはジョブの間だけ動きます。

    - A: 誤り。個別のリクエスト向けで、データセット全体の処理の選択ではありません。
    - B: 誤り。同時実行の上限があり、データセット全体の処理の選択ではありません。
    - C: 正しい。
    - D: 誤り。常時の課金が発生します。

    **スキル:** [3.1.3](../domain3.md#skill-3-1-3) / **参照:** [バッチ変換](../../../services/sagemaker.md#batch-transform)

### 問9 {#q9}

断続的な負荷でサーバーレス推論を検討しています。次の要件のうち、サーバーレスでは満たせないものを選んでください。（2つ選択）

- A. `OverheadLatency` によるコールドスタートの確認
- B. 予測できるバーストへの Provisioned Concurrency の利用
- C. アイドル時に料金がほぼかからないこと
- D. VPC の設定
- E. GPU の使用

??? success "答えと解説"
    **正解: D, E**

    サーバーレスで GPU か VPC が必要になったら、リアルタイムを選びます。

    - A: 誤り。確認できます。
    - B: 誤り。利用できます。
    - C: 誤り。サーバーレスの特徴です。
    - D: 正しい。サーバーレスは VPC の設定に対応しません。
    - E: 正しい。サーバーレスは GPU に対応しません。

    **スキル:** [3.1.3](../domain3.md#skill-3-1-3) / **参照:** [サーバーレス](../../../services/sagemaker.md#serverless)

### 問10 {#q10}

社外で PyTorch で学習した重みを SageMaker AI で動かします。特殊な依存関係はありません。どの手順が適切ですか。

- A. `model.tar.gz` を S3 に置き、推論コンテナで `CreateModel` する
- B. ノートブックのメモリにモデルを読み込んで、インスタンスごと外部へ公開する
- C. CodeBuild でモデルを学習し直してからデプロイする
- D. Bedrock の Custom Model Import だけを使う

??? success "答えと解説"
    **正解: A**

    `model.tar.gz` を S3 に置き、推論コンテナを指定して `CreateModel` します。

    - A: 正しい。
    - B: 誤り。エンドポイントとしてデプロイする方法ではありません。
    - C: 誤り。学習し直す必要はありません。
    - D: 誤り。Bedrock の API で使う方法で、SageMaker AI では動きません。

    **スキル:** [3.1.5](../domain3.md#skill-3-1-5) / **参照:** [JumpStart と持ち込み](../../../services/sagemaker.md#jumpstart)

### 問11 {#q11}

Hugging Face で調整した Llama 系のモデルを、サーバーを管理せず Bedrock の API で呼びます。呼び出しの形も含めて正しいものはどれですか。

- A. Custom Model Import で読み込み、`InvokeModel` で呼ぶ
- B. Custom Model Import で読み込み、バッチ推論だけで呼ぶ
- C. JumpStart のエンドポイントを `InvokeModel` で呼び、インスタンスも自分で管理する
- D. Polly のカスタムの音声として登録し、API で呼ぶ

??? success "答えと解説"
    **正解: A**

    Custom Model Import は Hugging Face の重みの形式を S3 から読み込みます。`InvokeModel` のオンデマンドで呼びます。

    - A: 正しい。
    - B: 誤り。バッチ推論には対応しません。
    - C: 誤り。JumpStart のエンドポイントは SageMaker AI のエンドポイントで、インスタンスの管理も必要です。
    - D: 誤り。音声合成のサービスで、関係がありません。

    **スキル:** [3.1.5](../domain3.md#skill-3-1-5) / **参照:** [Custom Model Import](../../../services/genai-apps.md#custom-model-import)

### 問12 {#q12}

社外で作ったモデルに、独自の C++ のライブラリが必要です。SageMaker AI で動かすときの選択と、コンテナの必須の要件はどれですか。

- A. コンテナは不要で、`requirements.txt` にライブラリを書く
- B. 独自のコンテナを GitHub に置き、ポート 22 で SSH に応答する
- C. 独自のコンテナを ECR に置き、`/ping` に応答する
- D. ビルド済みのイメージをそのまま使い、起動後に手で入れる

??? success "答えと解説"
    **正解: C**

    独自の依存関係があるなら独自のコンテナを ECR に置きます。推論コンテナは `/ping` に応答する必要があります。

    - A: 誤り。Python のパッケージを足す方法です。
    - B: 誤り。ECR に置きます。SSH は要件ではありません。
    - C: 正しい。
    - D: 誤り。OS のライブラリなどはイメージに含めます。起動後の変更は残りません。

    **スキル:** [3.1.5](../domain3.md#skill-3-1-5) / **参照:** [リアルタイム](../../../services/sagemaker.md#realtime)、[ECR](../../../services/containers.md#ecr)

### 問13 {#q13}

Boto3 でリアルタイムエンドポイントを作ります。API を呼ぶ順序はどれですか。

- A. `CreateEndpointConfig`、`CreateModel`、`CreateEndpoint`
- B. `CreateEndpoint`、`CreateModel`、`CreateEndpointConfig`
- C. `CreateTrainingJob`、`CreateEndpoint`、`InvokeEndpoint`
- D. `CreateModel`、`CreateEndpointConfig`、`CreateEndpoint`

??? success "答えと解説"
    **正解: D**

    順序はモデル、エンドポイント設定、エンドポイントです。

    - A: 誤り。設定はモデルを参照するので、モデルが先です。
    - B: 誤り。エンドポイントはモデルと設定のあとに作ります。
    - C: 誤り。モデルと設定の作成が抜けています。
    - D: 正しい。

    **スキル:** [3.2.5](../domain3.md#skill-3-2-5) / **参照:** [エンドポイントと推論](../../../services/sagemaker.md#endpoints)

### 問14 {#q14}

Boto3 で `sagemaker` クライアントの `invoke_endpoint` を呼ぶと、メソッドがないと言われます。正しい修正はどれですか。

- A. `bedrock-runtime` クライアントを使う
- B. `sagemaker-runtime` クライアントを使う
- C. エンドポイントを一度削除して作り直してから、同じ `sagemaker` クライアントで呼ぶ
- D. IAM ポリシーに `sagemaker:*` を足す

??? success "答えと解説"
    **正解: B**

    呼び出しは `sagemaker-runtime` の `InvokeEndpoint` で、学習やデプロイの `sagemaker` とはクライアントが別です。

    - A: 誤り。Bedrock のモデルを呼ぶクライアントです。
    - B: 正しい。
    - C: 誤り。エンドポイントの問題ではありません。
    - D: 誤り。メソッドがないのは権限の問題ではありません。

    **スキル:** [3.2.5](../domain3.md#skill-3-2-5) / **参照:** [エンドポイントと推論](../../../services/sagemaker.md#endpoints)

### 問15 {#q15}

リアルタイムのモデルの処理に 50〜60 秒かかります。クライアント側でタイムアウトが出ています。正しい対応はどれですか。また、モデルを新しくするときの切り替えの方法はどれですか。（2つ選択）

- A. 既存のエンドポイント設定を直接書き換える
- B. SDK のソケットタイムアウトを 70 秒にする
- C. 処理の上限を設定で 120 秒に延ばす
- D. エンドポイントを削除して別の名前で作り直す
- E. 新しいエンドポイント設定を作り、`UpdateEndpoint` で切り替える

??? success "答えと解説"
    **正解: B, E**

    50〜60 秒の処理にはソケットタイムアウトを 70 秒にします。モデルの更新は新しい設定と `UpdateEndpoint` です。

    - A: 誤り。新しい設定を作って切り替えます。
    - B: 正しい。
    - C: 誤り。モデルの応答の上限は 60 秒です。60 秒を超える処理は失敗します。
    - D: 誤り。呼び出し側の変更が必要になり、停止も発生します。
    - E: 正しい。

    **スキル:** [3.2.5](../domain3.md#skill-3-2-5) / **参照:** [リアルタイム](../../../services/sagemaker.md#realtime)

### 問16 {#q16}

1 件の処理時間が安定した XGBoost のエンドポイントです。標準のターゲット追跡の指標はどれですか。

- A. `ConcurrentRequestsPerCopy`
- B. `SageMakerVariantInvocationsPerInstance`
- C. `Invocation5XXErrors`
- D. `ApproximateBacklogSizePerInstance` のカスタム指標

??? success "答えと解説"
    **正解: B**

    処理時間が安定したモデルの標準は `SageMakerVariantInvocationsPerInstance` です。

    - A: 誤り。推論コンポーネントの指標です。
    - B: 正しい。
    - C: 誤り。サーバーのエラーの数で、負荷の指標ではありません。
    - D: 誤り。非同期のキューの指標です。

    **スキル:** [3.2.6](../domain3.md#skill-3-2-6) / **参照:** [自動スケーリング](../../../services/sagemaker.md#autoscaling)

### 問17 {#q17}

非同期のエンドポイントで夜間は 0 台にします。キューが溜まったら増やします。必要な設定を選んでください。（2つ選択）

- A. `ApproximateBacklogSizePerInstance` のターゲット追跡
- B. `SageMakerVariantInvocationsPerInstance` だけのターゲット追跡
- C. Provisioned Concurrency を設定する
- D. `MinCapacity` を 2 にする
- E. `HasBacklogWithoutCapacity` のステップスケーリング

??? success "答えと解説"
    **正解: A, E**

    非同期の指標は `ApproximateBacklogSizePerInstance` です。0 台から起動するにはステップスケーリングを追加します。

    - A: 正しい。キューの溜まり具合で増減します。
    - B: 誤り。0 台のときは起動のきっかけになりません。
    - C: 誤り。サーバーレスの機能です。
    - D: 誤り。夜間に 0 台にできません。
    - E: 正しい。0 台から起動するために必要です。

    **スキル:** [3.2.6](../domain3.md#skill-3-2-6) / **参照:** [非同期](../../../services/sagemaker.md#async)、[自動スケーリング](../../../services/sagemaker.md#autoscaling)

### 問18 {#q18}

ターゲット追跡でインスタンスの増減を短い間隔で繰り返しています。適切な調整はどれですか。

- A. `ScaleInCooldown` を長くする
- B. `ScaleInCooldown` を短くする
- C. 最大の台数を最小の台数と同じにして、増減そのものをなくす
- D. ターゲットの値をなくす

??? success "答えと解説"
    **正解: A**

    `ScaleInCooldown` が短すぎると増減を繰り返します。

    - A: 正しい。
    - B: 誤り。増減の繰り返しが悪化します。
    - C: 誤り。スケーリングそのものをやめることになります。
    - D: 誤り。ターゲット追跡が成り立ちません。

    **スキル:** [3.2.6](../domain3.md#skill-3-2-6) / **参照:** [自動スケーリング](../../../services/sagemaker.md#autoscaling)

### 問19 {#q19}

LLM のストリーミングのエンドポイントで、急増に 10 秒程度で反応してスケールさせます。どの指標ですか。

- A. CPU の使用率のカスタム指標
- B. `SageMakerVariantInvocationsPerInstance` と `Invocations` の合計
- C. `Invocation4XXErrors`
- D. `SageMakerVariantConcurrentRequestsPerModelHighResolution`

??? success "答えと解説"
    **正解: D**

    高解像度の同時リクエスト数の指標は、急増に 10 秒で反応します。

    - A: 誤り。GPU のモデルの飽和を反映しません。
    - B: 誤り。分単位の指標で、LLM の長い処理の負荷を反映しにくい指標です。
    - C: 誤り。クライアントのエラーの数で、負荷を示しません。
    - D: 正しい。

    **スキル:** [3.2.10](../domain3.md#skill-3-2-10) / **参照:** [自動スケーリング](../../../services/sagemaker.md#autoscaling)

### 問20 {#q20}

推論コンポーネントで複数の FM を共有しています。モデルごとにコピーの数を増減します。どの指標を使いますか。

- A. `SageMakerVariantInvocationsPerInstance`
- B. `ApproximateBacklogSizePerInstance`
- C. コピーあたりの `ConcurrentRequestsPerCopy`
- D. Bedrock の `InvocationThrottles`

??? success "答えと解説"
    **正解: C**

    推論コンポーネントは `ConcurrentRequestsPerCopy` で増減します。

    - A: 誤り。バリアントの単位の指標です。
    - B: 誤り。非同期のキューの指標です。
    - C: 正しい。
    - D: 誤り。Bedrock のモデルの呼び出しの指標です。

    **スキル:** [3.2.10](../domain3.md#skill-3-2-10) / **参照:** [自動スケーリング](../../../services/sagemaker.md#autoscaling)

### 問21 {#q21}

HyperPod の EKS クラスターで、推論の GPU ノードを自動で増減し、アイドル時はノードを 0 まで減らします。どの仕組みですか。

- A. Karpenter によるノードの自動スケーリング
- B. Bedrock の Priority 層
- C. CloudFormation の `UpdateStack` を毎晩実行する
- D. `MaxPayloadInMB` を調整する

??? success "答えと解説"
    **正解: A**

    HyperPod の EKS クラスターは Karpenter によるマネージドのノード自動スケーリングに対応し、0 ノードまで縮小できます。

    - A: 正しい。
    - B: 誤り。Bedrock のモデルの層で、ノードの増減の機能ではありません。
    - C: 誤り。需要に合わせた自動の増減になりません。
    - D: 誤り。バッチ変換の設定です。

    **スキル:** [3.2.10](../domain3.md#skill-3-2-10) / **参照:** [分散学習と時間短縮](../../../services/sagemaker.md#distributed-training)

### 問22 {#q22}

表データの XGBoost の推論です。GPU は不要で、コストを抑えます。どのファミリーを選びますか。

- A. `ml.g5`
- B. `ml.trn1`
- C. `ml.c5`
- D. `ml.p5`

??? success "答えと解説"
    **正解: C**

    表データの推論は汎用か CPU の `ml.m5`、`ml.c5` を選びます。

    - A: 誤り。GPU のファミリーで、この用途には過剰です。
    - B: 誤り。学習のコストを下げる専用チップです。
    - C: 正しい。
    - D: 誤り。GPU のファミリーで、深層学習や LLM 向けです。

    **スキル:** [4.2.1](../domain4.md#skill-4-2-1) / **参照:** [インスタンスの選び方](../../../services/sagemaker.md#instance-selection)

### 問23 {#q23}

深層学習の推論のコストを Inferentia で下げます。CUDA 向けのコードを使っています。どうしますか。

- A. そのまま `ml.inf2` にデプロイする
- B. AWS Neuron でコンパイルしてから配置する
- C. `ml.p4d` に変えて CUDA のまま動かす
- D. Inference Recommender の結果をそのまま適用する

??? success "答えと解説"
    **正解: B**

    Inferentia は CUDA 向けのコードがそのまま動きません。AWS Neuron でコンパイルします。

    - A: 誤り。CUDA 向けのコードはそのまま動きません。
    - B: 正しい。
    - C: 誤り。GPU のファミリーで、Inferentia でコストを下げる要件に合いません。
    - D: 誤り。サイズを決める機能で、コードは変換されません。

    **スキル:** [4.2.1](../domain4.md#skill-4-2-1) / **参照:** [インスタンスの選び方](../../../services/sagemaker.md#instance-selection)

### 問24 {#q24}

候補のインスタンスで負荷試験をして、推論に適切なサイズを決めます。どの機能ですか。

- A. 本番の `CPUUtilization` を観察する
- B. Trusted Advisor のチェック
- C. Compute Optimizer の EC2 の推奨だけを使う
- D. Inference Recommender の負荷テスト

??? success "答えと解説"
    **正解: D**

    適切なサイズを負荷試験で決めるなら Inference Recommender です。

    - A: 誤り。動かしているインスタンスの使用率しか分からず、候補を比べる負荷試験になりません。
    - B: 誤り。幅広い点検で、モデルの負荷試験はしません。
    - C: 誤り。SageMaker AI のエンドポイントの負荷試験は行いません。
    - D: 正しい。

    **スキル:** [4.2.1](../domain4.md#skill-4-2-1) / **参照:** [Inference Recommender](../../../services/sagemaker.md#inference-optimization)
