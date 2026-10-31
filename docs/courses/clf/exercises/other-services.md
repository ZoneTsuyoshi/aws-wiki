# アプリ統合とその他のサービス の問題集

対象の解説: [メッセージング](../../../services/messaging.md)、[その他のサービス](../../../services/other-services.md)、[CI/CD](../../../services/cicd.md)、[クラウドの基礎](../../../services/cloud-foundations.md)

### 問1 {#q1}

注文をいったん溜めて、処理側が自分のペースで順に取り出すようにしたいと考えています。最も適切なサービスはどれですか。

- A. Amazon SES
- B. Amazon Connect
- C. Amazon SQS
- D. Amazon SNS

??? success "答えと解説"
    **正解: C**

    SQS はキューで、負荷を平準化します。

    - A: 誤り。メールを送受信するサービス。
    - B: 誤り。コンタクトセンターのサービス。
    - C: 正しい。
    - D: 誤り。複数の宛先へ同時に通知するサービスで、溜めて取り出す形ではない。

    **スキル:** [メッセージと通知のサービス](../domain3.md#t3-8-integration) / **参照:** [SQS](../../../services/messaging.md#sqs)、[選び方](../../../services/messaging.md#how-to-choose)

### 問2 {#q2}

サーバーの異常のアラートを、担当者のメールや SMS に同時に送りたいと考えています。最も適切なサービスはどれですか。

- A. Amazon SQS
- B. Amazon SNS
- C. AWS Step Functions
- D. AWS X-Ray

??? success "答えと解説"
    **正解: B**

    SNS は複数の宛先へ同時に通知します。

    - A: 誤り。処理側が取り出すキューで、人へ通知するものではない。
    - B: 正しい。
    - C: 誤り。処理の流れを制御するサービス。
    - D: 誤り。トレースのサービス。

    **スキル:** [メッセージと通知のサービス](../domain3.md#t3-8-integration) / **参照:** [SNS](../../../services/messaging.md#sns)

### 問3 {#q3}

イベントの内容によって送り先を振り分け、スケジュールでの実行もしたいと考えています。最も適切なサービスはどれですか。

- A. Amazon SQS
- B. AWS CodeBuild
- C. Amazon SES
- D. Amazon EventBridge

??? success "答えと解説"
    **正解: D**

    EventBridge はイベントの内容で振り分け、スケジュールでも実行できます。

    - A: 誤り。キューのサービスで、内容で振り分けるものではない。
    - B: 誤り。ビルドとテストのサービス。
    - C: 誤り。メールの送受信のサービス。
    - D: 正しい。

    **スキル:** [メッセージと通知のサービス](../domain3.md#t3-8-integration) / **参照:** [EventBridge](../../../services/messaging.md#eventbridge)

### 問4 {#q4}

受注、在庫の確認、配送の手配の処理を順番に実行し、流れを管理したいと考えています。最も適切なサービスはどれですか。

- A. AWS Step Functions
- B. AWS Amplify
- C. Amazon Lex
- D. Amazon SNS

??? success "答えと解説"
    **正解: A**

    Step Functions は複数の手順の流れを制御します。

    - A: 正しい。
    - B: 誤り。フロントエンドの開発とホスティングのサービス。
    - C: 誤り。対話のボットを作るサービス。
    - D: 誤り。通知のサービスで、流れの管理は行わない。

    **スキル:** [メッセージと通知のサービス](../domain3.md#t3-8-integration) / **参照:** [Standard と Express](../../../services/step-functions.md#standard-express)

### 問5 {#q5}

自前の設備なしでコールセンターを作りたいと考えています。最も適切なサービスはどれですか。

- A. Amazon Connect
- B. Amazon Lex
- C. Amazon SES
- D. AWS Step Functions

??? success "答えと解説"
    **正解: A**

    Connect はクラウドのコンタクトセンターです。

    - A: 正しい。
    - B: 誤り。対話のボットを作るサービスで、コンタクトセンターそのものではない。
    - C: 誤り。メールの送受信のサービス。
    - D: 誤り。処理の流れを制御するサービス。

    **スキル:** [業務アプリケーション](../domain3.md#t3-8-business) / **参照:** [Amazon Connect](../../../services/other-services.md#connect)

### 問6 {#q6}

アプリから、案内のメールを本文付きで大量に送りたいと考えています。最も適切なサービスはどれですか。

- A. AWS Step Functions
- B. Amazon Connect
- C. Amazon SQS
- D. Amazon SES

??? success "答えと解説"
    **正解: D**

    SES はメールの送受信のサービスです。

    - A: 誤り。処理の流れを制御するサービス。
    - B: 誤り。コンタクトセンターのサービス。
    - C: 誤り。キューのサービス。
    - D: 正しい。

    **スキル:** [業務アプリケーション](../domain3.md#t3-8-business) / **参照:** [Amazon SES](../../../services/other-services.md#ses)

### 問7 {#q7}

SES と SNS の違いの説明として正しいものはどれですか。

- A. SES はコールセンターのサービス、SNS はバッチのサービス
- B. SES はキューのサービス、SNS はメールの受信だけを行う専用のサービス
- C. SES はメール本文を作って送るサービス、SNS は購読者への通知のサービス
- D. 両者は同じサービスの古い名前と新しい名前である

??? success "答えと解説"
    **正解: C**

    メール本文を作って送るなら SES、購読者に通知するなら SNS です。

    - A: 誤り。どちらも違う。
    - B: 誤り。SES はメールの送受信、SNS は通知。
    - C: 正しい。
    - D: 誤り。別のサービス。

    **スキル:** [業務アプリケーション](../domain3.md#t3-8-business) / **参照:** [Amazon SES](../../../services/other-services.md#ses)、[SNS](../../../services/messaging.md#sns)

### 問8 {#q8}

本番環境で AWS の技術的な問題が起きたときの相談先として最も適切なものはどれですか。

- A. AWS Artifact
- B. AWS Support
- C. AWS Marketplace
- D. Service Quotas

??? success "答えと解説"
    **正解: B**

    AWS Support は、技術的な質問や問題の相談窓口です。

    - A: 誤り。監査レポートと契約の入手先。
    - B: 正しい。
    - C: 誤り。製品を探して購入するカタログ。
    - D: 誤り。サービスの上限の確認と申請の場所。

    **スキル:** [顧客支援のサービス](../domain3.md#t3-8-enablement) / **参照:** [AWS Support プラン](../../../services/cloud-foundations.md#support-plans)

### 問9 {#q9}

サポートプランを選ぶときに比べるものとして適切なものはどれですか。（2つ選択）

- A. リージョンの AZ の数
- B. S3 のストレージクラス
- C. 必要な応答の速さ
- D. 専任の担当者が必要か
- E. EC2 のインスタンスタイプのカテゴリ

??? success "答えと解説"
    **正解: C, D**

    必要な応答の速さや、専任の担当者が必要かでプランを選びます。

    - A: 誤り。プランの選択の観点ではない。
    - B: 誤り。プランの選択の観点ではない。
    - C: 正しい。
    - D: 正しい。
    - E: 誤り。プランの選択の観点ではない。

    **スキル:** [顧客支援のサービス](../domain3.md#t3-8-enablement) / **参照:** [AWS Support プラン](../../../services/cloud-foundations.md#support-plans)

### 問10 {#q10}

専任の担当者（TAM）に継続して支援してほしい会社が選ぶべきプランとして適切なものはどれですか。

- A. Business Support+
- B. Basic
- C. プランに関係なく全利用者に TAM が付く
- D. Enterprise

??? success "答えと解説"
    **正解: D**

    専任の TAM が必要なら Enterprise 以上です。

    - A: 誤り。専任の TAM はいない。
    - B: 誤り。技術サポートのケースはなく、TAM もいない。
    - C: 誤り。TAM は Enterprise 以上。
    - D: 正しい。

    **スキル:** [顧客支援のサービス](../domain3.md#t3-8-enablement) / **参照:** [AWS Support プラン](../../../services/cloud-foundations.md#support-plans)

### 問11 {#q11}

コードのビルドとテストを実行するサービスはどれですか。

- A. AWS X-Ray
- B. AWS CodeBuild
- C. AWS CodePipeline
- D. AWS CLI

??? success "答えと解説"
    **正解: B**

    CodeBuild はビルドとテストを実行します。

    - A: 誤り。分散アプリのトレースのサービス。
    - B: 正しい。
    - C: 誤り。リリースの流れ全体を管理するサービス。
    - D: 誤り。コマンドでの操作のツール。

    **スキル:** [開発ツール](../domain3.md#t3-8-developer) / **参照:** [CodeBuild](../../../services/cicd.md#codebuild)、[サービスの役割](../../../services/cicd.md#overview)

### 問12 {#q12}

ソースの変更からビルド、デプロイまでの流れ全体を自動化したいと考えています。最も適切なサービスはどれですか。

- A. AWS CodeBuild
- B. Amazon Inspector
- C. AWS CodePipeline
- D. AWS X-Ray

??? success "答えと解説"
    **正解: C**

    CodePipeline は流れ全体を管理します。

    - A: 誤り。流れの中のビルドを行う部分。
    - B: 誤り。脆弱性を検出するサービス。
    - C: 正しい。
    - D: 誤り。トレースのサービス。

    **スキル:** [開発ツール](../domain3.md#t3-8-developer) / **参照:** [CodePipeline](../../../services/cicd.md#codepipeline)、[サービスの役割](../../../services/cicd.md#overview)

### 問13 {#q13}

分散アプリの遅いリクエストについて、どのサービスの間でボトルネックが起きているかを調べたいと考えています。最も適切なサービスはどれですか。

- A. AWS X-Ray
- B. AWS CodePipeline
- C. AWS CloudTrail
- D. AWS Config

??? success "答えと解説"
    **正解: A**

    X-Ray はアプリのトレースを取ります。

    - A: 正しい。
    - B: 誤り。リリースの流れのサービス。
    - C: 誤り。API の操作の記録で、アプリのトレースではない。
    - D: 誤り。設定の記録のサービス。

    **スキル:** [開発ツール](../domain3.md#t3-8-developer) / **参照:** [X-Ray によるトレース](../../../services/observability.md#xray)

### 問14 {#q14}

社員に仮想デスクトップを配り、在宅勤務でも同じ環境を使わせたいと考えています。最も適切なサービスはどれですか。

- A. Amazon Connect
- B. AWS Client VPN
- C. Amazon WorkSpaces
- D. AWS Amplify

??? success "答えと解説"
    **正解: C**

    WorkSpaces はデスクトップ全体を届けます。

    - A: 誤り。コンタクトセンターのサービス。
    - B: 誤り。端末を VPC に接続するサービスで、デスクトップの配信ではない。
    - C: 正しい。
    - D: 誤り。フロントエンドのサービス。

    **スキル:** [エンドユーザーコンピューティング](../domain3.md#t3-8-euc) / **参照:** [Amazon WorkSpaces](../../../services/other-services.md#workspaces)

### 問15 {#q15}

CAD などの重いアプリだけを、ブラウザーへ配信したいと考えています。デスクトップ全体は不要です。試験ガイドの名前で最も適切なサービスはどれですか。

- A. Amazon AppStream 2.0
- B. Amazon WorkSpaces
- C. Amazon CloudFront
- D. AWS Lambda

??? success "答えと解説"
    **正解: A**

    特定のアプリを配信します。現在の名前は Amazon WorkSpaces Applications です。

    - A: 正しい。
    - B: 誤り。デスクトップ全体を届けるサービス。
    - C: 誤り。コンテンツ配信のサービスで、アプリの画面を配信するものではない。
    - D: 誤り。イベントでコードを実行するサービス。

    **スキル:** [エンドユーザーコンピューティング](../domain3.md#t3-8-euc) / **参照:** [Amazon WorkSpaces Applications（旧 AppStream 2.0）](../../../services/other-services.md#appstream)

### 問16 {#q16}

届けるものとサービスの組み合わせとして正しいものはどれですか。（2つ選択）

- A. デスクトップ全体: Amazon AppStream 2.0
- B. 管理されたブラウザー: Amazon WorkSpaces Secure Browser
- C. 特定のアプリ: Amazon WorkSpaces Secure Browser
- D. デスクトップ全体: Amazon WorkSpaces
- E. 管理されたブラウザー: Amazon AppStream 2.0

??? success "答えと解説"
    **正解: B, D**

    何を届けるかで選びます。Secure Browser は 2026 年 10 月 29 日に新規受付を終了しましたが、試験ガイドの対象です。

    - A: 誤り。デスクトップ全体は WorkSpaces。
    - B: 正しい。
    - C: 誤り。特定のアプリは AppStream 2.0。
    - D: 正しい。
    - E: 誤り。ブラウザーは Secure Browser。

    **スキル:** [エンドユーザーコンピューティング](../domain3.md#t3-8-euc) / **参照:** [Amazon WorkSpaces Secure Browser](../../../services/other-services.md#secure-browser)、[Amazon WorkSpaces](../../../services/other-services.md#workspaces)、[Amazon WorkSpaces Applications（旧 AppStream 2.0）](../../../services/other-services.md#appstream)

### 問17 {#q17}

フロントエンドの開発者が、サーバーの管理なしで Web アプリを公開したいと考えています。最も適切なサービスはどれですか。

- A. Amazon EC2
- B. AWS CodeBuild
- C. Amazon EKS
- D. AWS Amplify

??? success "答えと解説"
    **正解: D**

    Amplify はフロントエンドの開発とホスティングを支援します。

    - A: 誤り。サーバーの管理が必要。
    - B: 誤り。ビルドのサービスで、ホスティングは行わない。
    - C: 誤り。Kubernetes のサービス。
    - D: 正しい。

    **スキル:** [フロントエンドとモバイル](../domain3.md#t3-8-frontend) / **参照:** [Amplify Hosting とブランチ](../../../services/cicd.md#amplify)

### 問18 {#q18}

Git リポジトリに接続して、ブランチごとに Web アプリをビルドしてデプロイしたいと考えています。最も適切なサービスはどれですか。

- A. Amazon Lightsail
- B. AWS Amplify
- C. AWS Batch
- D. AWS Elastic Beanstalk

??? success "答えと解説"
    **正解: B**

    Amplify は Git リポジトリに接続すれば、ブランチごとにビルドしてデプロイします。

    - A: 誤り。セットのプランで小さなサイトを始めるサービスで、ブランチごとのデプロイの機能が中心ではない。
    - B: 正しい。
    - C: 誤り。バッチジョブを実行するサービス。
    - D: 誤り。アップロードしたコードの基盤を用意するサービスで、ブランチごとのデプロイの機能が中心ではない。

    **スキル:** [フロントエンドとモバイル](../domain3.md#t3-8-frontend) / **参照:** [Amplify Hosting とブランチ](../../../services/cicd.md#amplify)

### 問19 {#q19}

AWS Amplify の説明として正しいものはどれですか。

- A. 多数のデバイスを AWS に接続するメッセージブローカーのサービスである
- B. 仮想デスクトップを配布するサービスである
- C. データウェアハウスのサービスである
- D. Web とモバイルのフロントエンドの開発とホスティングを支援する

??? success "答えと解説"
    **正解: D**

    Amplify はフロントエンドとモバイルのサービスです。

    - A: 誤り。それは AWS IoT Core の説明。
    - B: 誤り。それは Amazon WorkSpaces の説明。
    - C: 誤り。それは Amazon Redshift の説明。
    - D: 正しい。

    **スキル:** [フロントエンドとモバイル](../domain3.md#t3-8-frontend) / **参照:** [Amplify Hosting とブランチ](../../../services/cicd.md#amplify)、[AWS IoT Core](../../../services/other-services.md#iot-core)

### 問20 {#q20}

工場の多数のセンサーを AWS に接続して管理したいと考えています。最も適切なサービスはどれですか。

- A. AWS IoT Core
- B. AWS Direct Connect
- C. Amazon Kinesis
- D. Amazon Connect

??? success "答えと解説"
    **正解: A**

    IoT Core はデバイスと AWS を接続します。

    - A: 正しい。
    - B: 誤り。拠点と AWS の専用接続のサービスで、センサーの管理は行わない。
    - C: 誤り。ストリーミングデータを受けるサービスで、デバイスの管理は行わない。
    - D: 誤り。コンタクトセンターのサービス。

    **スキル:** [IoT](../domain3.md#t3-8-iot) / **参照:** [AWS IoT Core](../../../services/other-services.md#iot-core)

### 問21 {#q21}

AWS IoT Core がデバイスとの通信に使うプロトコルの例はどれですか。

- A. iSCSI
- B. SMTP
- C. MQTT
- D. SMB

??? success "答えと解説"
    **正解: C**

    IoT Core はデバイスと AWS をつなぐメッセージブローカーです。

    - A: 誤り。ブロックストレージのプロトコル。
    - B: 誤り。メールのプロトコル。
    - C: 正しい。
    - D: 誤り。Windows のファイル共有のプロトコル。

    **スキル:** [IoT](../domain3.md#t3-8-iot) / **参照:** [AWS IoT Core](../../../services/other-services.md#iot-core)

### 問22 {#q22}

センサーのデータを受けて、ルールで Lambda や DynamoDB に渡したいと考えています。受け口として最も適切なサービスはどれですか。

- A. Amazon SQS
- B. AWS IoT Core
- C. Amazon WorkSpaces
- D. Amazon Kinesis

??? success "答えと解説"
    **正解: B**

    IoT Core のルールを使えば、データを Lambda や DynamoDB に渡せます。

    - A: 誤り。キューのサービスで、デバイスの接続やルールの機能はない。
    - B: 正しい。
    - C: 誤り。仮想デスクトップのサービス。
    - D: 誤り。ストリーミングデータを受けるサービスで、デバイスの接続やルールの機能はない。

    **スキル:** [IoT](../domain3.md#t3-8-iot) / **参照:** [AWS IoT Core](../../../services/other-services.md#iot-core)
