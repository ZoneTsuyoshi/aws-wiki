# コンテナとサーバーレスの問題集

対象の解説: [コンテナ](../../../services/containers.md)、[AWS Lambda](../../../services/lambda.md)

### 問1 {#q1}

Kubernetes のマニフェストと Helm の資産を AWS で使い続けます。コントロールプレーンの管理は任せたいと考えています。どれを選びますか。

- A. Elastic Beanstalk の Docker プラットフォームで動かす
- B. Lambda のコンテナイメージ
- C. EKS のマネージドノードグループ
- D. ECS のサービスとタスク定義に書き直して移行する

??? success "答えと解説"
    **正解: C**

    EKS はマネージドの Kubernetes です。

    - A: 誤り。Kubernetes の資産を使えない。
    - B: 誤り。Kubernetes を動かす仕組みではない。
    - C: 正しい。
    - D: 誤り。既存の資産を使い続けられない。

    **スキル:** [コンテナ](../domain2.md#t2-1-containers) / **参照:** [EKS](../../../services/containers.md#eks)

### 問2 {#q2}

Kubernetes の資産はなく、AWS と統合された簡単なコンテナの運用をしたいと考えています。サーバーの管理もしたくありません。どの組み合わせですか。

- A. ECS と Fargate のサービス
- B. EKS と自己管理の EC2 ノードグループ
- C. EC2 に Docker を手で入れて起動スクリプトで動かす
- D. ECS Anywhere

??? success "答えと解説"
    **正解: A**

    ECS はシンプルなオーケストレーターで、Fargate ならサーバーの管理が要りません。

    - A: 正しい。
    - B: 誤り。運用の負担が大きい。
    - C: 誤り。管理が多く、オーケストレーションがない。
    - D: 誤り。オンプレミスの管理が残る。

    **スキル:** [コンテナ](../domain2.md#t2-1-containers) / **参照:** [ECS](../../../services/containers.md#ecs)、[Fargate と EC2](../../../services/containers.md#fargate-vs-ec2)

### 問3 {#q3}

GPU を使い、特権コンテナも必要なワークロードを ECS で動かします。適切な起動タイプはどれですか。

- A. Fargate の最大の CPU とメモリの組み合わせを指定する
- B. EC2 起動タイプと GPU インスタンス
- C. Fargate Spot
- D. Lambda の最大メモリの 10,240 MB を設定して動かす

??? success "答えと解説"
    **正解: B**

    特殊な要件には EC2 起動タイプを使います。

    - A: 誤り。特権コンテナと GPU の要件に合わない。
    - B: 正しい。
    - C: 誤り。Fargate の制約は同じ。
    - D: 誤り。GPU も特権コンテナも使えない。

    **スキル:** [コンテナ](../domain2.md#t2-1-containers) / **参照:** [Fargate と EC2](../../../services/containers.md#fargate-vs-ec2)

### 問4 {#q4}

既存のアプリをコンテナに移します。正しい流れはどれですか。

- A. EC2 のスナップショットをそのままタスク定義に指定して起動する
- B. ECR にソースコードを置くと、自動でイメージが作られて ECS に配置される
- C. コンテナのローカルファイルにセッションと DB を置いたままタスクを増やす
- D. Dockerfile でイメージを作って ECR に入れ、ECS か EKS で動かす。状態はコンテナの外に出す

??? success "答えと解説"
    **正解: D**

    状態は S3、EFS、DB などに出します。

    - A: 誤り。スナップショットはイメージではない。
    - B: 誤り。ECR はイメージを保管するレジストリ。
    - C: 誤り。状態がタスクに残り、スケールできない。
    - D: 正しい。

    **スキル:** [コンテナ](../domain2.md#t2-1-containers) / **参照:** [Dockerfile の基本](../../../services/containers.md#dockerfile)、[ECR](../../../services/containers.md#ecr)

### 問5 {#q5}

次の処理のうち、Lambda よりコンテナを選ぶべきものはどれですか。

- A. S3 のイベントで 10 秒以内に画像のサイズを変える処理
- B. DynamoDB Streams の通知の処理
- C. 2 時間かかる独自のランタイムに依存したバッチ処理
- D. API Gateway から呼ばれる数百ミリ秒の応答の処理

??? success "答えと解説"
    **正解: C**

    15 分を超える処理や、独自のランタイムに依存する処理はコンテナが向きます。

    - A: 誤り。短いイベント処理は Lambda が軽い。
    - B: 誤り。短いイベント処理で Lambda に向く。
    - C: 正しい。
    - D: 誤り。Lambda に向く。

    **スキル:** [コンテナ](../domain2.md#t2-1-containers) / **参照:** [Fargate と EC2](../../../services/containers.md#fargate-vs-ec2)、[タイムアウト](../../../services/lambda.md#timeout)

### 問6 {#q6}

Lambda で実行したい処理が最長 40 分かかります。分割はできません。サーバーの管理はしたくありません。どれが適切ですか。

- A. Lambda のメモリを最大にして 15 分に収まることを期待する
- B. Fargate のタスクで実行する
- C. Lambda のタイムアウトを 40 分に設定して実行する
- D. API Gateway の統合タイムアウトを 40 分に設定して呼ぶ

??? success "答えと解説"
    **正解: B**

    15 分を超える処理は Fargate や Batch を選びます。分割できるなら Step Functions も候補です。

    - A: 誤り。確実に収まる保証がない。
    - B: 正しい。
    - C: 誤り。上限は 900 秒（15 分）。
    - D: 誤り。Lambda の上限は変わらない。

    **スキル:** [サーバーレス](../domain2.md#t2-1-serverless) / **参照:** [タイムアウト](../../../services/lambda.md#timeout)、[Fargate と EC2](../../../services/containers.md#fargate-vs-ec2)

### 問7 {#q7}

負荷の増減が大きく、夜間はほぼアクセスがない API を作ります。インフラの管理を最小にします。適切な組み合わせはどれですか。

- A. NLB、Fargate の固定 10 タスク、Aurora の固定インスタンス
- B. ALB、EC2 の Auto Scaling、RDS のプロビジョンド IOPS
- C. CloudFront と 1 台の EC2
- D. API Gateway、Lambda、DynamoDB オンデマンド

??? success "答えと解説"
    **正解: D**

    使った分の課金で、増減にも自動で対応します。

    - A: 誤り。常に動き、アイドルの費用がかかる。
    - B: 誤り。待機中も費用がかかり、管理も多い。
    - C: 誤り。単一障害点で、負荷の増減にも対応できない。
    - D: 正しい。

    **スキル:** [サーバーレス](../domain2.md#t2-1-serverless) / **参照:** [実行モデル](../../../services/lambda.md#execution-model)、[キャパシティモードと RCU/WCU](../../../services/dynamodb.md#capacity)

### 問8 {#q8}

Fargate と Lambda の選択で、Fargate を選ぶ手がかりはどれですか。

- A. 長時間動くコンテナで、サーバーは管理したくない
- B. 実行は数秒で、発生の頻度が不規則である
- C. 実行の分だけ 1 ミリ秒単位で課金したい
- D. S3 のイベントに直接反応させたい

??? success "答えと解説"
    **正解: A**

    Fargate は長時間のコンテナに向きます。

    - A: 正しい。
    - B: 誤り。Lambda の手がかり。
    - C: 誤り。Lambda の課金の形。
    - D: 誤り。Lambda が直接統合される。

    **スキル:** [サーバーレス](../domain2.md#t2-1-serverless) / **参照:** [Fargate と EC2](../../../services/containers.md#fargate-vs-ec2)

### 問9 {#q9}

既存の React の静的な Web アプリを Git から自動でビルドして公開します。CDN の設定も最小で済ませます。どれを選びますか。

- A. EC2 の Nginx に配置して、ALB と Auto Scaling を組む
- B. Lambda の関数 URL で HTML を 1 ページずつ返す
- C. Amplify Hosting の Git 連携
- D. ECS のコンテナの Nginx

??? success "答えと解説"
    **正解: C**

    Amplify Hosting は Git と連携してビルド、公開までを行います。

    - A: 誤り。管理が多い。
    - B: 誤り。配信の用途に合わない。
    - C: 正しい。
    - D: 誤り。静的サイトには過剰。

    **スキル:** [サーバーレス](../domain2.md#t2-1-serverless) / **参照:** [Amplify Hosting とブランチ](../../../services/cicd.md#amplify)

### 問10 {#q10}

組織内で再利用するサーバーレスのアプリの部品を、SAM テンプレートとして公開し、他のチームがコンソールから探してデプロイできるようにします。どれを使いますか。

- A. Lambda のレイヤーに SAM テンプレートを入れて共有する
- B. AWS Config の適合パックにアプリとして登録する
- C. ECR のパブリックリポジトリにテンプレートを置く
- D. AWS Serverless Application Repository

??? success "答えと解説"
    **正解: D**

    SAR は SAM で書かれたアプリを公開し、Lambda のコンソールから探してデプロイできます。

    - A: 誤り。レイヤーは関数のライブラリの共有。
    - B: 誤り。設定の評価の仕組み。
    - C: 誤り。コンテナイメージのレジストリ。
    - D: 正しい。

    **スキル:** [サーバーレス](../domain2.md#t2-1-serverless) / **参照:** [SAM CLI のコマンド](../../../services/iac.md#sam-cli)
