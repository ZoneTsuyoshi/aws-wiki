# コンピューティング の問題集

対象の解説: [EC2 と Elastic Beanstalk](../../../services/ec2-beanstalk.md)、[コンテナ](../../../services/containers.md)、[Lambda](../../../services/lambda.md)、[ネットワーク](../../../services/networking.md)

### 問1 {#q1}

OS から細かく制御できる仮想サーバーが必要です。最も適切なサービスはどれですか。

- A. Amazon EC2
- B. AWS Lambda
- C. Amazon Lightsail
- D. AWS Elastic Beanstalk

??? success "答えと解説"
    **正解: A**

    EC2 は仮想サーバーです。

    - A: 正しい。
    - B: 誤り。サーバーを管理せずコードを実行するサービスで、OS は制御できない。
    - C: 誤り。セットのプランで簡単に始めるサービス。
    - D: 誤り。基盤を自動で用意するサービスで、OS の細かい制御が中心ではない。

    **スキル:** [コンピューティングの全体像](../domain3.md#t3-3-overview) / **参照:** [インスタンスタイプとメモリ、CPU の要件](../../../services/ec2-beanstalk.md#instance-types)

### 問2 {#q2}

数千のジョブを並べて、順に実行する処理を任せたいと考えています。最も適切なサービスはどれですか。

- A. AWS Elastic Beanstalk
- B. AWS Outposts
- C. AWS Batch
- D. Amazon Lightsail

??? success "答えと解説"
    **正解: C**

    Batch はバッチジョブの実行のサービスです。

    - A: 誤り。Web アプリの基盤を用意するサービス。
    - B: 誤り。自社施設に置く AWS の機器。
    - C: 正しい。
    - D: 誤り。小さなサイトを簡単に始めるサービス。

    **スキル:** [コンピューティングの全体像](../domain3.md#t3-3-overview) / **参照:** [AWS Batch](../../../services/other-services.md#batch)

### 問3 {#q3}

要件とサービスの組み合わせとして正しいものはどれですか。（2つ選択）

- A. 数千のジョブを順に処理する: AWS Outposts
- B. 最小限の知識でサイトをすぐ公開する: Amazon Lightsail
- C. コードのアップロードで Web アプリを動かす: AWS Elastic Beanstalk
- D. OS から細かく制御する: AWS Lambda
- E. 自社施設で AWS と同じ API を使う: AWS Batch

??? success "答えと解説"
    **正解: B, C**

    問題文の要件からサービスを選びます。

    - A: 誤り。バッチジョブなら AWS Batch。
    - B: 正しい。
    - C: 正しい。
    - D: 誤り。OS の制御が必要なら Amazon EC2。
    - E: 誤り。自社施設なら AWS Outposts。

    **スキル:** [コンピューティングの全体像](../domain3.md#t3-3-overview) / **参照:** [Amazon Lightsail](../../../services/cloud-foundations.md#lightsail)、[Elastic Beanstalk の環境](../../../services/ec2-beanstalk.md#beanstalk-environments)

### 問4 {#q4}

動画のエンコードで CPU を長時間多く使います。適切なインスタンスのカテゴリはどれですか。

- A. 高速コンピューティング
- B. メモリ最適化
- C. ストレージ最適化
- D. コンピューティング最適化

??? success "答えと解説"
    **正解: D**

    CPU を多く使う処理は C 系などのコンピューティング最適化です。

    - A: 誤り。GPU を使う処理に向く。
    - B: 誤り。大きなメモリを使う処理に向く。
    - C: 誤り。高 IOPS のローカルストレージを使う処理に向く。
    - D: 正しい。

    **スキル:** [EC2 のインスタンスタイプ](../domain3.md#t3-3-instance-types) / **参照:** [インスタンスタイプとメモリ、CPU の要件](../../../services/ec2-beanstalk.md#instance-types)

### 問5 {#q5}

大きなインメモリキャッシュを動かすサーバーに向くインスタンスのカテゴリはどれですか。

- A. 汎用
- B. メモリ最適化
- C. コンピューティング最適化
- D. ストレージ最適化

??? success "答えと解説"
    **正解: B**

    大きなメモリを使う処理は R 系、X 系などのメモリ最適化です。

    - A: 誤り。一般的なアプリに向く。特にメモリを多く使う処理には向かない。
    - B: 正しい。
    - C: 誤り。CPU を多く使う処理に向く。
    - D: 誤り。ローカルストレージの高 IOPS に向く。

    **スキル:** [EC2 のインスタンスタイプ](../domain3.md#t3-3-instance-types) / **参照:** [インスタンスタイプとメモリ、CPU の要件](../../../services/ec2-beanstalk.md#instance-types)

### 問6 {#q6}

GPU を使う機械学習の学習に向くインスタンスのカテゴリはどれですか。

- A. 汎用
- B. ストレージ最適化
- C. 高速コンピューティング
- D. メモリ最適化

??? success "答えと解説"
    **正解: C**

    GPU を使う処理は P 系、G 系などの高速コンピューティングです。

    - A: 誤り。Web サーバーや一般的なアプリに向く。
    - B: 誤り。高 IOPS のローカルストレージに向く。
    - C: 正しい。
    - D: 誤り。メモリを多く使う処理に向く。

    **スキル:** [EC2 のインスタンスタイプ](../domain3.md#t3-3-instance-types) / **参照:** [インスタンスタイプとメモリ、CPU の要件](../../../services/ec2-beanstalk.md#instance-types)

### 問7 {#q7}

処理とインスタンスのカテゴリの組み合わせとして正しいものはどれですか。（2つ選択）

- A. CPU を多く使うバッチ: メモリ最適化
- B. 一般的な Web サーバー: 汎用
- C. インメモリキャッシュ: ストレージ最適化
- D. 高 IOPS のローカルストレージを使う処理: ストレージ最適化
- E. GPU を使う機械学習: 汎用

??? success "答えと解説"
    **正解: B, D**

    処理が何を多く使うかでカテゴリを選びます。

    - A: 誤り。コンピューティング最適化が向く。
    - B: 正しい。
    - C: 誤り。メモリ最適化が向く。
    - D: 正しい。
    - E: 誤り。高速コンピューティングが向く。

    **スキル:** [EC2 のインスタンスタイプ](../domain3.md#t3-3-instance-types) / **参照:** [インスタンスタイプとメモリ、CPU の要件](../../../services/ec2-beanstalk.md#instance-types)

### 問8 {#q8}

既存の Kubernetes の知識と資産を AWS で使いたいと考えています。最も適切なサービスはどれですか。

- A. Amazon EKS
- B. AWS Lambda
- C. Amazon ECS
- D. Amazon ECR

??? success "答えと解説"
    **正解: A**

    EKS はマネージドの Kubernetes です。

    - A: 正しい。
    - B: 誤り。関数を実行するサービス。
    - C: 誤り。AWS 独自のコンテナ管理で、Kubernetes ではない。
    - D: 誤り。コンテナイメージの保管先。

    **スキル:** [コンテナの選択肢](../domain3.md#t3-3-containers) / **参照:** [EKS](../../../services/containers.md#eks)

### 問9 {#q9}

コンテナイメージを AWS で保管したいと考えています。最も適切なサービスはどれですか。

- A. Amazon S3
- B. AWS Fargate
- C. Amazon ECS
- D. Amazon ECR

??? success "答えと解説"
    **正解: D**

    ECR はコンテナイメージの置き場です。

    - A: 誤り。オブジェクトストレージで、コンテナイメージのレジストリではない。
    - B: 誤り。コンテナの実行場所。
    - C: 誤り。コンテナを動かす管理サービスで、イメージの保管先ではない。
    - D: 正しい。

    **スキル:** [コンテナの選択肢](../domain3.md#t3-3-containers) / **参照:** [ECR](../../../services/containers.md#ecr)

### 問10 {#q10}

シンプルに AWS でコンテナを動かしたいと考えています。Kubernetes を使う要件はありません。最も適切なサービスはどれですか。

- A. Amazon ECR
- B. Amazon ECS
- C. Amazon Lightsail のインスタンスのプラン
- D. Amazon EKS

??? success "答えと解説"
    **正解: B**

    ECS は AWS 独自のコンテナ管理です。

    - A: 誤り。イメージの保管先で、コンテナを動かすサービスではない。
    - B: 正しい。
    - C: 誤り。コンテナの管理サービスではない。
    - D: 誤り。Kubernetes を使うときの選択肢。

    **スキル:** [コンテナの選択肢](../domain3.md#t3-3-containers) / **参照:** [ECS](../../../services/containers.md#ecs)

### 問11 {#q11}

ECS と EKS の実行場所の説明として正しいものはどれですか。

- A. どちらも Lambda の上でだけ動く
- B. どちらも EC2 と Fargate を選べる
- C. ECS は Fargate だけ、EKS は EC2 だけを選べる
- D. どちらもオンプレミスのサーバーでしか動かない

??? success "答えと解説"
    **正解: B**

    ECS も EKS も、実行場所として EC2 や Fargate を選べます。

    - A: 誤り。実行場所は EC2 や Fargate。
    - B: 正しい。
    - C: 誤り。どちらも両方を選べる。
    - D: 誤り。AWS 上の EC2 や Fargate で動く。

    **スキル:** [コンテナの選択肢](../domain3.md#t3-3-containers) / **参照:** [ECS](../../../services/containers.md#ecs)、[EKS](../../../services/containers.md#eks)、[Fargate と EC2](../../../services/containers.md#fargate-vs-ec2)

### 問12 {#q12}

S3 にファイルが置かれたら、短い処理を自動で実行したいと考えています。サーバーを管理したくありません。最も適切なサービスはどれですか。

- A. Amazon ECR
- B. AWS Outposts
- C. AWS Lambda
- D. Amazon S3

??? success "答えと解説"
    **正解: C**

    Lambda はイベントでコードを実行します。

    - A: 誤り。イメージの保管先。
    - B: 誤り。自社施設に置く機器。
    - C: 正しい。
    - D: 誤り。ファイルの保管先で、処理を実行するサービスではない。

    **スキル:** [サーバーレスの選択肢](../domain3.md#t3-3-serverless) / **参照:** [実行モデル](../../../services/lambda.md#execution-model)

### 問13 {#q13}

コンテナのアプリを長時間動かし続けます。サーバーを管理せずに実行したいと考えています。最も適切なものはどれですか。

- A. AWS Lambda
- B. EC2 の起動タイプ
- C. Amazon ECR
- D. AWS Fargate

??? success "答えと解説"
    **正解: D**

    Fargate は、サーバー管理なしでコンテナを動かします。

    - A: 誤り。実行時間は最大 15 分で、動かし続ける用途に向かない。
    - B: 誤り。サーバーの管理が必要。
    - C: 誤り。イメージの保管先で、実行はしない。
    - D: 正しい。

    **スキル:** [サーバーレスの選択肢](../domain3.md#t3-3-serverless) / **参照:** [Fargate と EC2](../../../services/containers.md#fargate-vs-ec2)

### 問14 {#q14}

AWS Lambda の 1 回の実行時間の上限はどれですか。

- A. 15 分
- B. 1 時間
- C. 24 時間
- D. 1 分

??? success "答えと解説"
    **正解: A**

    関数のタイムアウトは最大 900 秒（15 分）です。

    - A: 正しい。
    - B: 誤り。上限は 15 分。
    - C: 誤り。上限は 15 分。
    - D: 誤り。上限は 15 分。

    **スキル:** [サーバーレスの選択肢](../domain3.md#t3-3-serverless) / **参照:** [実行モデル](../../../services/lambda.md#execution-model)

### 問15 {#q15}

Lambda と Fargate に共通する説明はどれですか。

- A. 動かす単位はどちらも関数である
- B. 利用者がサーバーを管理する必要がない
- C. 実行時間が 15 分までに制限される
- D. 利用者がゲスト OS のパッチを適用する

??? success "答えと解説"
    **正解: B**

    どちらもサーバーレスの選択肢です。

    - A: 誤り。Fargate が動かすのはコンテナ。
    - B: 正しい。
    - C: 誤り。この上限は Lambda の関数のもの。
    - D: 誤り。どちらも基盤の OS は AWS の担当。

    **スキル:** [サーバーレスの選択肢](../domain3.md#t3-3-serverless) / **参照:** [実行モデル](../../../services/lambda.md#execution-model)、[Fargate と EC2](../../../services/containers.md#fargate-vs-ec2)

### 問16 {#q16}

EC2 Auto Scaling の説明として正しいものはどれですか。（2つ選択）

- A. 障害が起きたインスタンスを置き換えられる
- B. 別のアカウントの請求をまとめる
- C. インスタンスのタイプを別のカテゴリに自動で変える
- D. 負荷に応じて、インスタンス数を増減する
- E. リージョンをまたいでデータを複製する

??? success "答えと解説"
    **正解: A, D**

    台数の増減が弾力性を実現し、置き換えが可用性に役立ちます。

    - A: 正しい。
    - B: 誤り。それは一括請求の機能。
    - C: 誤り。増減するのは台数。
    - D: 正しい。
    - E: 誤り。データの複製の機能ではない。

    **スキル:** [Auto Scaling と弾力性](../domain3.md#t3-3-auto-scaling) / **参照:** [EC2 Auto Scaling](../../../services/ec2-beanstalk.md#auto-scaling)

### 問17 {#q17}

夜間は負荷が下がるのに、昼のピークに合わせた台数を動かし続けています。費用を減らす方法として最も適切なものはどれですか。

- A. Auto Scaling で負荷に応じて台数を増減する
- B. 全インスタンスを、より大きなタイプに変える
- C. 全インスタンスを、Dedicated Hosts に移す
- D. 全インスタンスを、別のリージョンに移す

??? success "答えと解説"
    **正解: A**

    負荷が下がれば減らして費用を抑えられます。

    - A: 正しい。
    - B: 誤り。費用が増え、余剰も増える。
    - C: 誤り。費用が増える可能性が高く、増減にならない。
    - D: 誤り。負荷に応じた増減にならない。

    **スキル:** [Auto Scaling と弾力性](../domain3.md#t3-3-auto-scaling) / **参照:** [EC2 Auto Scaling](../../../services/ec2-beanstalk.md#auto-scaling)

### 問18 {#q18}

EC2 Auto Scaling が直接実現する性質として最も適切なものはどれですか。

- A. 責任共有
- B. データ主権
- C. 弾力性
- D. 最小権限

??? success "答えと解説"
    **正解: C**

    Auto Scaling は弾力性を実現する仕組みです。

    - A: 誤り。AWS と利用者の分担の話。
    - B: 誤り。データの所在地の話。
    - C: 正しい。
    - D: 誤り。権限の話。

    **スキル:** [Auto Scaling と弾力性](../domain3.md#t3-3-auto-scaling) / **参照:** [EC2 Auto Scaling](../../../services/ec2-beanstalk.md#auto-scaling)、[高可用性、弾力性、俊敏性](../../../services/cloud-foundations.md#ha-elasticity-agility)

### 問19 {#q19}

Web アプリで、URL のパスによって振り分け先を変えたいと考えています。最も適切なものはどれですか。

- A. インターネットゲートウェイ
- B. Network Load Balancer
- C. NAT ゲートウェイ
- D. Application Load Balancer

??? success "答えと解説"
    **正解: D**

    ALB はレイヤー 7 で、パスやホストで振り分けます。

    - A: 誤り。VPC とインターネットをつなぐもの。
    - B: 誤り。レイヤー 4 で動き、パスは見ない。
    - C: 誤り。プライベートサブネットから外へ出るためのもの。
    - D: 正しい。

    **スキル:** [ロードバランサーの目的](../domain3.md#t3-3-load-balancers) / **参照:** [ALB と NLB の違い](../../../services/networking.md#alb-vs-nlb)

### 問20 {#q20}

固定の IP アドレスが必要で、HTTP ではない TCP の通信を高い負荷で受けます。最も適切なものはどれですか。

- A. Amazon CloudFront
- B. Application Load Balancer
- C. Amazon Route 53
- D. Network Load Balancer

??? success "答えと解説"
    **正解: D**

    NLB はレイヤー 4 で、固定 IP や非 HTTP に向きます。

    - A: 誤り。コンテンツの配信のサービス。
    - B: 誤り。HTTP/HTTPS のレイヤー 7 のロードバランサー。
    - C: 誤り。DNS のサービス。
    - D: 正しい。

    **スキル:** [ロードバランサーの目的](../domain3.md#t3-3-load-balancers) / **参照:** [ALB と NLB の違い](../../../services/networking.md#alb-vs-nlb)

### 問21 {#q21}

ロードバランサーの目的として正しいものはどれですか。（2つ選択）

- A. 費用の予算を超えたら通知する
- B. 正常なターゲットだけに送る
- C. 複数のターゲットにリクエストを振り分ける
- D. 利用者の ID を作成して管理する
- E. データベースのスキーマを変換する

??? success "答えと解説"
    **正解: B, C**

    複数の AZ に振り分ければ、高可用性にも役立ちます。

    - A: 誤り。それは AWS Budgets の役割。
    - B: 正しい。
    - C: 正しい。
    - D: 誤り。それは Cognito などの役割。
    - E: 誤り。それは AWS SCT の役割。

    **スキル:** [ロードバランサーの目的](../domain3.md#t3-3-load-balancers) / **参照:** [ALB と NLB の違い](../../../services/networking.md#alb-vs-nlb)
