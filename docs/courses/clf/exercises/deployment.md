# デプロイと運用の方法 の問題集

対象の解説: [クラウドの基礎](../../../services/cloud-foundations.md)、[IaC](../../../services/iac.md)、[運用](../../../services/operations.md)

### 問1 {#q1}

環境の再現と変更の管理をテンプレートで行いたいと考えています。この方法に当たるものはどれですか。

- A. AWS CloudFormation によるプロビジョニング
- B. マネジメントコンソールでの手作業
- C. Amazon Lightsail のプランの選択
- D. AWS Health Dashboard の確認

??? success "答えと解説"
    **正解: A**

    CloudFormation は IaC のサービスです。

    - A: 正しい。
    - B: 誤り。手で作る方法で、再現と変更管理に向かない。
    - C: 誤り。基盤を任せる方法で、テンプレートでの管理が中心ではない。
    - D: 誤り。障害や予定を見るもので、リソースは作らない。

    **スキル:** [プロビジョニングと運用の方法](../domain3.md#t3-1-provisioning) / **参照:** [どれを使うか](../../../services/iac.md#choosing)、[CloudFormation テンプレート](../../../services/iac.md#cloudformation-template)

### 問2 {#q2}

開発者が、基盤の設定を任せて、コードをアップロードするだけで Web アプリを動かしたいと考えています。最も適切なサービスはどれですか。

- A. Amazon EC2
- B. AWS Elastic Beanstalk
- C. Amazon VPC
- D. AWS CloudFormation

??? success "答えと解説"
    **正解: B**

    Elastic Beanstalk は基盤を自動で用意します。

    - A: 誤り。OS から自分で設定する必要がある。
    - B: 正しい。
    - C: 誤り。ネットワークのサービス。
    - D: 誤り。テンプレートを自分で書いて管理する必要がある。

    **スキル:** [プロビジョニングと運用の方法](../domain3.md#t3-1-provisioning) / **参照:** [Elastic Beanstalk の環境](../../../services/ec2-beanstalk.md#beanstalk-environments)

### 問3 {#q3}

クラウドの経験が少ない担当者が、小さな Web サイトを数クリックで公開したいと考えています。最も適切なサービスはどれですか。

- A. AWS Transit Gateway
- B. AWS Batch
- C. Amazon EKS
- D. Amazon Lightsail

??? success "答えと解説"
    **正解: D**

    Lightsail は必要なものがセットになったプランで始められます。

    - A: 誤り。VPC などを接続するサービス。
    - B: 誤り。バッチジョブを実行するサービス。
    - C: 誤り。Kubernetes のサービスで、知識が必要になる。
    - D: 正しい。

    **スキル:** [プロビジョニングと運用の方法](../domain3.md#t3-1-provisioning) / **参照:** [Amazon Lightsail](../../../services/cloud-foundations.md#lightsail)

### 問4 {#q4}

多数のサーバーへのパッチの適用やコマンドの実行を、まとめて行いたいと考えています。最も適切なサービスはどれですか。

- A. Service Quotas
- B. AWS Health Dashboard
- C. AWS Systems Manager
- D. AWS Artifact

??? success "答えと解説"
    **正解: C**

    Systems Manager はサーバーの運用をまとめて行います。

    - A: 誤り。サービスの上限の確認と申請を行うサービス。
    - B: 誤り。AWS 側の障害や予定を示すサービス。
    - C: 正しい。
    - D: 誤り。監査レポートを入手するサービス。

    **スキル:** [運用を支えるサービス](../domain3.md#t3-1-operating-tools) / **参照:** [AWS Systems Manager](../../../services/operations.md#systems-manager)

### 問5 {#q5}

EC2 インスタンスの起動数がサービスの上限に近づいています。上限を確認して引き上げを申請する場所として最も適切なものはどれですか。

- A. Service Quotas
- B. AWS Config
- C. AWS Budgets
- D. AWS Systems Manager の Patch Manager

??? success "答えと解説"
    **正解: A**

    Service Quotas で、既定の上限と調整できるかを確認し、引き上げを申請できます。

    - A: 正しい。
    - B: 誤り。設定の変化と準拠を扱う。
    - C: 誤り。費用のしきい値の通知で、サービスの上限は扱わない。
    - D: 誤り。パッチの適用の機能。

    **スキル:** [運用を支えるサービス](../domain3.md#t3-1-operating-tools) / **参照:** [AWS Support プラン](../../../services/cloud-foundations.md#support-plans)、[AWS Systems Manager](../../../services/operations.md#systems-manager)

### 問6 {#q6}

予定されたメンテナンスで、自分のどのリソースが影響を受けるかを知りたいと考えています。確認する場所として最も適切なものはどれですか。

- A. Service Quotas
- B. Amazon CloudWatch
- C. AWS Health Dashboard
- D. AWS Systems Manager

??? success "答えと解説"
    **正解: C**

    Health Dashboard は、AWS 側の障害や予定されたメンテナンスの影響を示します。

    - A: 誤り。サービスの上限を扱う。
    - B: 誤り。自分のリソースのメトリクスを見るもので、AWS 側の予定は分からない。
    - C: 正しい。
    - D: 誤り。サーバーの運用を行うサービスで、AWS 側の予定は示さない。

    **スキル:** [運用を支えるサービス](../domain3.md#t3-1-operating-tools) / **参照:** [AWS Health Dashboard](../../../services/cloud-foundations.md#health)

### 問7 {#q7}

自社のアプリの中から Python のライブラリで S3 にファイルを置きたいと考えています。最も適切なアクセス方法はどれですか。

- A. IAM のパスワードポリシー
- B. AWS SDK
- C. AWS Artifact
- D. マネジメントコンソール

??? success "答えと解説"
    **正解: B**

    アプリから AWS を呼ぶなら SDK です。

    - A: 誤り。パスワードの条件の設定。
    - B: 正しい。
    - C: 誤り。監査レポートを入手するサービス。
    - D: 誤り。ブラウザーの画面で、アプリから呼ぶものではない。

    **スキル:** [AWS へのアクセス方法](../domain3.md#t3-1-access) / **参照:** [マネジメントコンソールとアクセス方法](../../../services/cloud-foundations.md#access-methods)

### 問8 {#q8}

運用担当者が、シェルスクリプトで AWS の操作を繰り返したいと考えています。最も適切なアクセス方法はどれですか。

- A. AWS Health API
- B. マネジメントコンソール
- C. AWS Trusted Advisor
- D. AWS CLI

??? success "答えと解説"
    **正解: D**

    CLI はコマンドの操作で、スクリプトで繰り返せます。

    - A: 誤り。Health の情報を連携するためのもので、リソースの操作手段ではない。
    - B: 誤り。手作業の確認や一度きりの操作に向く。
    - C: 誤り。環境を点検するサービス。
    - D: 正しい。

    **スキル:** [AWS へのアクセス方法](../domain3.md#t3-1-access) / **参照:** [マネジメントコンソールとアクセス方法](../../../services/cloud-foundations.md#access-methods)、[AWS CLI](../../../services/iac.md#aws-cli)

### 問9 {#q9}

API、SDK、CLI の関係の説明として正しいものはどれですか。

- A. CLI はコンソールからしか実行できない
- B. SDK はコンソールの画面の操作を録画して再生している
- C. CLI と SDK は、内部で HTTPS の API を呼び出している
- D. API は CLI を内部で呼び出しており、CLI がなければ API は動かない

??? success "答えと解説"
    **正解: C**

    API が土台で、CLI と SDK はその上で動きます。

    - A: 誤り。CLI はコマンドで実行するツール。
    - B: 誤り。SDK はプログラムのライブラリで、API を呼ぶ。
    - C: 正しい。
    - D: 誤り。関係が逆。

    **スキル:** [AWS へのアクセス方法](../domain3.md#t3-1-access) / **参照:** [マネジメントコンソールとアクセス方法](../../../services/cloud-foundations.md#access-methods)、[AWS CLI](../../../services/iac.md#aws-cli)

### 問10 {#q10}

要件とアクセス方法の組み合わせとして正しいものはどれですか。（2つ選択）

- A. 同じ環境を別のリージョンに作る: 手作業のコンソール
- B. アプリの実行中に DynamoDB へ書き込む: コンソール
- C. 新しいサービスの画面を見て、一度だけ確認する: コンソール
- D. 同じ環境を何度も作る: IaC
- E. 毎晩の処理を自動で実行する: コンソール

??? success "答えと解説"
    **正解: C, D**

    手作業か、スクリプトか、アプリか、環境の再現かで選びます。

    - A: 誤り。手作業はミスが増える。IaC を使う。
    - B: 誤り。アプリからは SDK を使う。
    - C: 正しい。
    - D: 正しい。
    - E: 誤り。スクリプトなどで自動化する。

    **スキル:** [AWS へのアクセス方法](../domain3.md#t3-1-access) / **参照:** [マネジメントコンソールとアクセス方法](../../../services/cloud-foundations.md#access-methods)

### 問11 {#q11}

一度だけ、特定のリソースの状態を確認したいと考えています。最も手軽な方法はどれですか。

- A. SDK でアプリを開発して確認する
- B. マネジメントコンソールの画面で確認する
- C. AWS Control Tower で基盤を作り直す
- D. CloudFormation のテンプレートを新しく書く

??? success "答えと解説"
    **正解: B**

    一度きりの確認ならコンソールが向きます。

    - A: 誤り。一度の確認には手間がかかる。
    - B: 正しい。
    - C: 誤り。マルチアカウントの基盤のサービスで、目的に合わない。
    - D: 誤り。環境の再現の方法で、一度の確認には手間がかかる。

    **スキル:** [一度きりか、繰り返しか](../domain3.md#t3-1-one-time-repeatable) / **参照:** [マネジメントコンソールとアクセス方法](../../../services/cloud-foundations.md#access-methods)

### 問12 {#q12}

開発、検証、本番に同じ構成を作る必要があります。最も適切な方法はどれですか。

- A. IaC で同じテンプレートから作る
- B. 一度だけ作り、3 つの環境で同じリソースを共有する
- C. 担当者ごとに手順書を見てコンソールで作る
- D. 本番のインスタンスにログインしてコマンドを実行する

??? success "答えと解説"
    **正解: A**

    同じ環境の繰り返しには IaC が向きます。

    - A: 正しい。
    - B: 誤り。環境を分ける要件に合わない。
    - C: 誤り。ミスや差異が起きやすい。
    - D: 誤り。環境を再現する方法ではない。

    **スキル:** [一度きりか、繰り返しか](../domain3.md#t3-1-one-time-repeatable) / **参照:** [CloudFormation テンプレート](../../../services/iac.md#cloudformation-template)

### 問13 {#q13}

毎晩、同じ手順で不要なスナップショットを削除しています。担当者のミスが増えています。最も適切な改善はどれですか。

- A. コンソールでの手順書をさらに詳しくする
- B. 作業の間隔を毎週に減らす
- C. 担当者を 2 人に増やして、毎晩の作業を互いに確認する
- D. CLI のスクリプトなどで処理を自動化する

??? success "答えと解説"
    **正解: D**

    繰り返す作業を手で行うと、ミスと手間が増えます。

    - A: 誤り。手作業が残り、ミスと手間が残る。
    - B: 誤り。手作業が残り、要件も変わる。
    - C: 誤り。人の手間が増える。
    - D: 正しい。

    **スキル:** [一度きりか、繰り返しか](../domain3.md#t3-1-one-time-repeatable) / **参照:** [AWS CLI](../../../services/iac.md#aws-cli)、[マネジメントコンソールとアクセス方法](../../../services/cloud-foundations.md#access-methods)

### 問14 {#q14}

新しいサービスをすべて AWS 上だけで作ることにしました。この形はどれですか。

- A. クラウド
- B. マルチテナント
- C. ハイブリッド
- D. オンプレミス

??? success "答えと解説"
    **正解: A**

    すべてをクラウドで動かす形です。

    - A: 正しい。
    - B: 誤り。複数の利用者で共有する構造のことで、デプロイモデルではない。
    - C: 誤り。オンプレミスと接続して併用する形。
    - D: 誤り。自社施設で動かす形。

    **スキル:** [デプロイモデル](../domain3.md#t3-1-deployment-models) / **参照:** [デプロイモデルとサービスモデル](../../../services/cloud-foundations.md#deployment-models)

### 問15 {#q15}

工場の制御システムは自社の施設に残し、分析の処理だけ AWS に送ります。両者はネットワークで接続します。この形はどれですか。

- A. クラウド
- B. オンプレミス
- C. サーバーレス
- D. ハイブリッド

??? success "答えと解説"
    **正解: D**

    オンプレミスとクラウドの併用はハイブリッドです。

    - A: 誤り。自社施設のシステムが残るので当てはまらない。
    - B: 誤り。AWS も使うので当てはまらない。
    - C: 誤り。サーバーの管理の話で、配置の形の話ではない。
    - D: 正しい。

    **スキル:** [デプロイモデル](../domain3.md#t3-1-deployment-models) / **参照:** [デプロイモデルとサービスモデル](../../../services/cloud-foundations.md#deployment-models)

### 問16 {#q16}

サービスモデルの例の組み合わせとして正しいものはどれですか。（2つ選択）

- A. IaaS: Amazon EC2
- B. IaaS: 完成した業務ソフトウェア
- C. PaaS: AWS Elastic Beanstalk
- D. SaaS: Amazon EC2
- E. PaaS: 完成した業務ソフトウェア

??? success "答えと解説"
    **正解: A, C**

    利用者が管理する範囲でサービスモデルが分かれます。

    - A: 正しい。
    - B: 誤り。完成したソフトウェアは SaaS。
    - C: 正しい。
    - D: 誤り。EC2 は IaaS。
    - E: 誤り。完成したソフトウェアは SaaS。

    **スキル:** [デプロイモデル](../domain3.md#t3-1-deployment-models) / **参照:** [デプロイモデルとサービスモデル](../../../services/cloud-foundations.md#deployment-models)
