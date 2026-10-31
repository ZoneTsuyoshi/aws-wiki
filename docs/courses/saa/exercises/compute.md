# コンピューティングとスケーリングの問題集

対象の解説: [EC2 と Elastic Beanstalk](../../../services/ec2-beanstalk.md)、[運用](../../../services/operations.md)

### 問1 {#q1}

数千の独立した計算ジョブを、キューとスケジューラーの管理なしで実行します。1 つのジョブは 2 時間です。どれを選びますか。

- A. API Gateway の同期の統合
- B. ALB と EC2 の Auto Scaling で HTTP として処理する構成
- C. AWS Batch の配列ジョブでキューに投入する
- D. Lambda の同時実行を上げて 2 時間のジョブを実行する構成

??? success "答えと解説"
    **正解: C**

    Batch はスケジューラーとインフラの管理を任せられます。配列ジョブは 2〜10,000 の子ジョブに分割できます。

    - A: 誤り。長いジョブに合わない。
    - B: 誤り。スケジューラーを自作することになる。
    - C: 正しい。
    - D: 誤り。上限は 15 分。

    **スキル:** [コンピューティングの選択](../domain3.md#t3-2-compute-services) / **参照:** [AWS Batch](../../../services/other-services.md#batch)

### 問2 {#q2}

既存の Spark のジョブを、クラスターの設定を細かく調整しながら移行します。どれを選びますか。

- A. Elastic Beanstalk のワーカー環境を複数作って動かす構成
- B. Lambda で Spark のライブラリを各関数に含めて実行する構成
- C. Fargate の NGINX
- D. EMR の Spark クラスター

??? success "答えと解説"
    **正解: D**

    EMR は Spark や Hadoop の大規模なデータ処理のサービスです。

    - A: 誤り。Spark のクラスターの管理機能がない。
    - B: 誤り。15 分の上限があり、Spark のクラスターに合わない。
    - C: 誤り。用途が違う。
    - D: 正しい。

    **スキル:** [コンピューティングの選択](../domain3.md#t3-2-compute-services) / **参照:** [Amazon EMR](../../../services/data-engineering.md#emr)

### 問3 {#q3}

アプリのコードだけを用意し、キャパシティの設定やデプロイは簡単に任せます。OS には触れますが、環境の構築は最小にしたいと考えています。どれを選びますか。

- A. AWS Batch のマネージドコンピューティング環境
- B. Elastic Beanstalk の Web サーバー環境
- C. EKS のマネージドノードと Helm チャート
- D. 素の EC2 と自作の起動スクリプト

??? success "答えと解説"
    **正解: B**

    コードをアップロードすれば環境を構築します。

    - A: 誤り。ジョブの実行向けで、Web アプリの配置に向かない。
    - B: 正しい。
    - C: 誤り。Kubernetes の知識と運用が必要。
    - D: 誤り。構築を自分で行うことになる。

    **スキル:** [コンピューティングの選択](../domain3.md#t3-2-compute-services) / **参照:** [Elastic Beanstalk の環境](../../../services/ec2-beanstalk.md#beanstalk-environments)

### 問4 {#q4}

コンピューティングの選択として正しい組み合わせを選んでください。（2つ選択）

- A. 1 時間かかる同期の処理を Lambda で実行
- B. OS まで制御する必要があるので EC2
- C. 短いイベント処理のために常時稼働の EMR クラスター
- D. Kubernetes の資産を持つので ECS に書き直す
- E. サーバーの管理をせずコンテナを動かすので Fargate

??? success "答えと解説"
    **正解: B, E**

    要件の「管理の範囲」と「実行時間」で絞ります。

    - A: 誤り。上限は 15 分。
    - B: 正しい。
    - C: 誤り。過剰。
    - D: 誤り。資産を使えるのは EKS。
    - E: 正しい。

    **スキル:** [コンピューティングの選択](../domain3.md#t3-2-compute-services) / **参照:** [Fargate と EC2](../../../services/containers.md#fargate-vs-ec2)、[実行モデル](../../../services/lambda.md#execution-model)

### 問5 {#q5}

CloudFront でヘッダーを書き換える軽い処理を、1 ミリ秒未満で大量に実行します。どれを選びますか。

- A. CloudFront Functions
- B. ALB の固定レスポンス
- C. Lambda@Edge のオリジンリクエストのイベント
- D. リージョンの Lambda を API Gateway で呼ぶ構成

??? success "答えと解説"
    **正解: A**

    CloudFront Functions はビューワーのイベントの軽い処理に向きます。

    - A: 正しい。
    - B: 誤り。エッジの処理ではない。
    - C: 誤り。軽い処理には過剰で、費用も高い。
    - D: 誤り。エッジで実行されない。

    **スキル:** [エッジでの分散処理](../domain3.md#t3-2-edge) / **参照:** [Lambda@Edge と CloudFront Functions](../../../services/networking.md#edge-functions)

### 問6 {#q6}

CloudFront のオリジンリクエストのイベントで、外部サービスへのネットワーク呼び出しを含む処理を実行します。どれを選びますか。

- A. CloudFront Functions のビューワーリクエストのイベント
- B. Lambda@Edge のオリジンリクエストの関数
- C. Wavelength Zone の EC2 に転送して処理させる構成
- D. S3 のリダイレクトルール

??? success "答えと解説"
    **正解: B**

    Lambda@Edge はネットワーク接続ができ、オリジン側のイベントも扱えます。

    - A: 誤り。ネットワーク接続ができず、オリジン側のイベントでも動かない。
    - B: 正しい。
    - C: 誤り。5G 端末向けの配置で、CloudFront のイベント処理ではない。
    - D: 誤り。処理の実行はできない。

    **スキル:** [エッジでの分散処理](../domain3.md#t3-2-edge) / **参照:** [Lambda@Edge と CloudFront Functions](../../../services/networking.md#edge-functions)

### 問7 {#q7}

配置の要件に合う組み合わせはどれですか。5G 端末向けの超低遅延のアプリ、自社の施設に置くデータ、特定の大都市の利用者への低遅延の順です。

- A. Wavelength、Outposts、Local Zones の順
- B. Outposts、Local Zones、Wavelength の順
- C. CloudFront、Outposts、Wavelength の順
- D. Local Zones、Wavelength、Outposts の順

??? success "答えと解説"
    **正解: A**

    通信事業者のエッジは Wavelength、施設は Outposts、大都市は Local Zones です。

    - A: 正しい。
    - B: 誤り。順序が違う。
    - C: 誤り。最初と最後が要件に合わない。
    - D: 誤り。順序が違う。

    **スキル:** [エッジでの分散処理](../domain3.md#t3-2-edge) / **参照:** [Wavelength](../../../services/cloud-foundations.md#wavelength)、[Outposts](../../../services/cloud-foundations.md#outposts)、[Local Zones](../../../services/cloud-foundations.md#local-zones)

### 問8 {#q8}

毎朝 9 時の決まった急増に備え、事前に台数を増やします。周期は読めています。どのポリシーが最も直接ですか。

- A. ステップスケーリングのアラームのしきい値を高くする
- B. 最大台数だけを増やして何もしない
- C. CPU のターゲット追跡
- D. スケジュールされたアクション

??? success "答えと解説"
    **正解: D**

    決まった時刻の変動にはスケジュールです。周期から先回りするなら予測スケーリングも使えます。

    - A: 誤り。負荷を見てから動く。
    - B: 誤り。台数は増えない。
    - C: 誤り。負荷を見てから動く。
    - D: 正しい。

    **スキル:** [スケーリングの機能](../domain3.md#t3-2-auto-scaling) / **参照:** [EC2 Auto Scaling](../../../services/ec2-beanstalk.md#auto-scaling)、[予測スケーリング](../../../services/operations.md#predictive-scaling)

### 問9 {#q9}

起動に 10 分かかるアプリで、急増への反応を速くします。既に初期化を済ませたインスタンスをすぐに使えるようにします。何を使いますか。

- A. インスタンスのウォームアップの時間を短く設定する
- B. スポットの割合を増やす設定
- C. Auto Scaling グループのウォームプール
- D. インスタンスサイズの増加と最大数の削減

??? success "答えと解説"
    **正解: C**

    ウォームプールは初期化を済ませて待機させます。

    - A: 誤り。メトリクスの扱いの設定で、起動を速くしない。
    - B: 誤り。起動時間は変わらない。
    - C: 正しい。
    - D: 誤り。起動時間は変わらない。

    **スキル:** [スケーリングの機能](../domain3.md#t3-2-auto-scaling) / **参照:** [ウォームプール](../../../services/operations.md#warm-pools)

### 問10 {#q10}

Aurora のレプリカ、ECS のタスク、DynamoDB の容量のスケーリングを 1 か所で計画します。性能重視か費用重視の戦略も選びます。どれを使いますか。

- A. Compute Optimizer
- B. Trusted Advisor のコスト最適化チェック
- C. EC2 Auto Scaling のライフサイクルフック
- D. AWS Auto Scaling のスケーリングプラン

??? success "答えと解説"
    **正解: D**

    複数のサービスのスケーリングをまとめられます。

    - A: 誤り。推奨の機能で、スケーリングの設定はしない。
    - B: 誤り。点検の機能。
    - C: 誤り。起動と終了のときの処理を挟む機能で、EC2 が対象。
    - D: 正しい。

    **スキル:** [スケーリングの機能](../domain3.md#t3-2-auto-scaling) / **参照:** [EC2 Auto Scaling](../../../services/ec2-beanstalk.md#auto-scaling)

### 問11 {#q11}

SQS のワーカーの EC2 をスケールします。処理時間は一定で、目標の遅れの範囲があります。どの指標でターゲット追跡しますか。

- A. ワーカーの平均 CPU 使用率
- B. インスタンスあたりのバックログのカスタムメトリクス
- C. `NumberOfMessagesSent` の合計
- D. ALB の `RequestCountPerTarget`

??? success "答えと解説"
    **正解: B**

    良い指標は、台数を 2 倍にすると半分になるものです。

    - A: 誤り。I/O 待ちの処理ではキューの長さを反映しない。
    - B: 正しい。
    - C: 誤り。台数で変わらず、ターゲット追跡に向かない。
    - D: 誤り。ワーカーは ALB を通らない。

    **スキル:** [スケーリングの指標と条件](../domain3.md#t3-2-metrics) / **参照:** [可視性タイムアウト](../../../services/messaging.md#visibility-timeout)、[EC2 Auto Scaling](../../../services/ec2-beanstalk.md#auto-scaling)

### 問12 {#q12}

メモリが足りなくなるアプリで、メモリの使用率でスケールします。EC2 の標準メトリクスに見当たりません。どうしますか。

- A. `CPUUtilization` の目標を下げて代用する
- B. 詳細モニタリングを有効にしてメモリのメトリクスを得る
- C. CloudWatch エージェントでメモリを収集し、カスタムメトリクスで追跡する
- D. ELB のアクセスログからメモリの使用量を計算する

??? success "答えと解説"
    **正解: C**

    メモリは OS の中の値なので、エージェントが必要です。

    - A: 誤り。メモリの使用とは別の指標。
    - B: 誤り。詳細モニタリングは周期を短くするだけ。
    - C: 正しい。
    - D: 誤り。含まれていない。

    **スキル:** [スケーリングの指標と条件](../domain3.md#t3-2-metrics) / **参照:** [EC2 の既定メトリクスとエージェント](../../../services/observability.md#ec2-metrics)

### 問13 {#q13}

ターゲット追跡で、台数が増えすぎる症状があります。インスタンスの起動に 5 分かかり、メトリクスに反映されるまで時間がかかります。どの設定を確認しますか。

- A. インスタンスのウォームアップの時間
- B. 最小台数と最大台数を同じ値にする
- C. ターゲットグループのスティッキー期間
- D. EBS のルートボリュームのサイズ

??? success "答えと解説"
    **正解: A**

    ウォームアップが起動の所要時間より短いと、増えすぎることがあります。

    - A: 正しい。
    - B: 誤り。スケールしなくなる。
    - C: 誤り。スケーリングと関係しない。
    - D: 誤り。スケーリングの判断に関係しない。

    **スキル:** [スケーリングの指標と条件](../domain3.md#t3-2-metrics) / **参照:** [インスタンスのウォームアップ](../../../services/ec2-beanstalk.md#instance-warmup)、[スケーリングの失敗の調査](../../../services/operations.md#asg-troubleshooting)

### 問14 {#q14}

インメモリのキャッシュや大きなヒープの Java アプリに合うファミリーはどれですか。

- A. I ファミリーのストレージ最適化
- B. C ファミリーのコンピューティング最適化
- C. T 系のバースト可能
- D. R ファミリーのメモリ最適化

??? success "答えと解説"
    **正解: D**

    R や X はメモリ重視です。

    - A: 誤り。ローカルストレージ重視。
    - B: 誤り。CPU 重視。
    - C: 誤り。低負荷向け。
    - D: 正しい。

    **スキル:** [インスタンスタイプ](../domain3.md#t3-2-instance) / **参照:** [インスタンスタイプとメモリ、CPU の要件](../../../services/ec2-beanstalk.md#instance-types)

### 問15 {#q15}

HPC のノード間の通信を低遅延にします。同じ AZ に配置し、MPI を OS をバイパスして使います。どの組み合わせですか。（2つ選択）

- A. パーティションプレイスメントグループと NAT ゲートウェイ
- B. EFA
- C. クラスタープレイスメントグループ
- D. 複数のリージョンの EC2 と Global Accelerator
- E. スプレッドプレイスメントグループと通常の ENI

??? success "答えと解説"
    **正解: B, C**

    クラスターは 1 AZ に寄せます。EFA は MPI などのノード間通信に使います。

    - A: 誤り。目的が違う。
    - B: 正しい。
    - C: 正しい。
    - D: 誤り。EFA は AZ や VPC をまたげない。
    - E: 誤り。離して配置するので低遅延にならない。

    **スキル:** [インスタンスタイプ](../domain3.md#t3-2-instance) / **参照:** [プレイスメントグループ](../../../services/operations.md#placement-groups)

### 問16 {#q16}

少数の重要なインスタンスを物理的に分離し、ハードウェアの障害を同時に受けないようにします。どのプレイスメントグループですか。

- A. パーティションの 1 パーティションだけ
- B. 専有ホストの 1 台
- C. スプレッドプレイスメントグループ
- D. クラスタープレイスメントグループ

??? success "答えと解説"
    **正解: C**

    スプレッドは AZ ごとに 7 台までです。

    - A: 誤り。同じパーティションは機器を共有する。
    - B: 誤り。同じ機器に載る。
    - C: 正しい。
    - D: 誤り。寄せるので障害を共有しやすい。

    **スキル:** [インスタンスタイプ](../domain3.md#t3-2-instance) / **参照:** [プレイスメントグループ](../../../services/operations.md#placement-groups)

### 問17 {#q17}

HDFS や Cassandra のような大規模な分散ワークロードで、ラック障害の影響を区切ります。どのプレイスメントグループが適切ですか。

- A. パーティション
- B. クラスター
- C. スプレッドの AZ あたり 7 台の配置
- D. 同じインスタンスタイプのオンデマンド予約

??? success "答えと解説"
    **正解: A**

    パーティションは AZ ごとに 7 パーティションまでで、機器を分けます。

    - A: 正しい。
    - B: 誤り。同じラックの障害を受けやすい。
    - C: 誤り。台数の制約が大きい。
    - D: 誤り。配置の分離の機能ではない。

    **スキル:** [インスタンスタイプ](../domain3.md#t3-2-instance) / **参照:** [プレイスメントグループ](../../../services/operations.md#placement-groups)

### 問18 {#q18}

CPU を多く使う Lambda 関数が遅くなっています。CPU だけを増やす設定はありますか。正しい対応はどれですか。

- A. 予約済み同時実行を増やすと 1 実行の CPU も増える
- B. メモリを増やす。CPU も比例して増える
- C. タイムアウトを伸ばせば CPU の割り当ても増える
- D. CPU のコア数を指定する設定で 4 に上げる

??? success "答えと解説"
    **正解: B**

    1,769 MB で 1 vCPU 相当です。実行時間が縮めば費用が下がることもあります。

    - A: 誤り。同時実行は関係ない。
    - B: 正しい。
    - C: 誤り。関係ない。
    - D: 誤り。CPU を直接指定する設定はない。

    **スキル:** [リソースのタイプとサイズ](../domain3.md#t3-2-sizing) / **参照:** [メモリ](../../../services/lambda.md#memory)、[メモリと CPU の最適化](../../../services/lambda.md#memory-tuning)

### 問19 {#q19}

`t3` インスタンスの CPU が突然遅くなりました。`CPUCreditBalance` が 0 です。負荷は常に高いままです。どうしますか。

- A. M や C のファミリーに変更する
- B. ルートボリュームを `gp3` に変更する
- C. 詳細モニタリングを有効にしてクレジットを増やす
- D. 同じ T 系の台数を減らして負荷を集中させる

??? success "答えと解説"
    **正解: A**

    常に高負荷なら、バースト可能なタイプは向きません。

    - A: 正しい。
    - B: 誤り。CPU の問題と関係ない。
    - C: 誤り。クレジットは増えない。
    - D: 誤り。悪化する。

    **スキル:** [リソースのタイプとサイズ](../domain3.md#t3-2-sizing) / **参照:** [最小のメモリとコンピューティングを決める](../../../services/ec2-beanstalk.md#sizing)

### 問20 {#q20}

Lambda 関数の設定の範囲と、Fargate のタスクのサイズについて正しいものはどれですか。

- A. Lambda のメモリは 128 MB から 3,008 MB まで
- B. Fargate のタスクのメモリは常に CPU の 2 倍に固定される
- C. Lambda のメモリは 128〜10,240 MB、Fargate は CPU とメモリの有効な組み合わせから選ぶ
- D. Fargate の CPU とメモリは任意の数値を自由に組み合わせられる

??? success "答えと解説"
    **正解: C**

    Fargate は 1 vCPU なら 2〜8 GB のように、範囲から選びます。

    - A: 誤り。上限は 10,240 MB。
    - B: 誤り。固定ではない。
    - C: 正しい。
    - D: 誤り。有効な組み合わせが決まっている。

    **スキル:** [リソースのタイプとサイズ](../domain3.md#t3-2-sizing) / **参照:** [メモリ](../../../services/lambda.md#memory)、[Fargate と EC2](../../../services/containers.md#fargate-vs-ec2)
