# IaC、CI/CD と開発の実践の問題集

対象の解説: [IaC（CloudFormation / SAM / CDK / CLI）](../../../services/iac.md)、[CI/CD（CodeBuild / CodeDeploy / CodePipeline）](../../../services/cicd.md)

### 問1 {#q1}

使う言語とフレームワークの組み合わせとして適切なものはどれですか。

- A. Airflow の DAG を Scala で書く
- B. EMR のブートストラップを HiveQL で書く
- C. Step Functions のワークフローを Python のファイルで定義する
- D. ストリームの状態付き処理に Flink を使い、Java か SQL で書く

??? success "答えと解説"
    **正解: D**

    場面ごとに言語とフレームワークを選びます。

    - A: 誤り。DAG は Python で書きます。
    - B: 誤り。ブートストラップは Bash などのスクリプトです。
    - C: 誤り。定義は ASL です。
    - D: 正しい。

    **スキル:** [1.4.3](../domain1.md#skill-1-4-3) / **参照:** [ETL ジョブ](../../../services/data-engineering.md#glue-jobs)、[Amazon Managed Service for Apache Flink](../../../services/data-engineering.md#flink)

### 問2 {#q2}

次の作業に適した言語はどれですか。「EMR のノードの起動時に OS のパッケージを入れ、CLI で設定をコピーする」。

- A. R
- B. Bash
- C. SQL
- D. ASL

??? success "答えと解説"
    **正解: B**

    EMR のブートストラップや CLI の自動化には Bash を使います。

    - A: 誤り。統計処理に使う言語で、この作業には向きません。
    - B: 正しい。
    - C: 誤り。データの問い合わせの言語で、OS の操作はできません。
    - D: 誤り。Step Functions の定義の言語で、ノードの中では動きません。

    **スキル:** [1.4.3](../domain1.md#skill-1-4-3) / **参照:** [Amazon MWAA](../../../services/data-engineering.md#mwaa)、[AWS CLI](../../../services/iac.md#aws-cli)

### 問3 {#q3}

Spark を使う場面として最も適切なものはどれですか。

- A. 大量のデータのバッチとマイクロバッチの変換
- B. キーによる 1 件ずつの低遅延の読み書きの処理
- C. ミリ秒単位の状態付きイベント処理の実行基盤
- D. 依存関係のあるワークフローのスケジュール管理

??? success "答えと解説"
    **正解: A**

    Spark はバッチとマイクロバッチの標準です。

    - A: 正しい。
    - B: 誤り。DynamoDB などの役割です。
    - C: 誤り。状態付きのストリーム処理は Flink が向きます。
    - D: 誤り。Airflow などの役割です。

    **スキル:** [1.4.3](../domain1.md#skill-1-4-3) / **参照:** [ETL ジョブ](../../../services/data-engineering.md#glue-jobs)、[変換エンジン](../../../services/data-engineering.md#choosing-transform)

### 問4 {#q4}

PySpark の変換のコードを本番前に確かめます。費用を抑えて素早く失敗を見つけるテストの組み合わせはどれですか。

- A. 本番と同じ規模のステージングで全件の実行だけを毎回行う
- B. 本番のサンプルの結果を毎日手で確認する運用
- C. 変換関数の単体テストと、小さなサンプルデータでの結合テスト
- D. CodeDeploy のカナリアで本番に流して確かめるテスト

??? success "答えと解説"
    **正解: C**

    小さな単位でテストします。

    - A: 誤り。遅く、費用もかかります。
    - B: 誤り。本番の前に失敗を見つけられません。
    - C: 正しい。
    - D: 誤り。本番で初めて失敗を見つけます。

    **スキル:** [1.4.4](../domain1.md#skill-1-4-4) / **参照:** [単体テスト](../../../services/sdk-resilience.md#unit-testing)、[ブランチとタグでバージョンとリリースを管理する](../../../services/cicd.md#branches-tags)

### 問5 {#q5}

パイプラインのログの実践として正しいものはどれですか。（2つ選択）

- A. 処理件数と遅延をメトリクスにして、アラームを付ける
- B. ログは自由な文章にして、人が読むことだけを優先する
- C. 成功時も失敗時もログを出さず、費用をなくす
- D. JSON の構造化ログで、実行 ID と処理件数を残す
- E. デバッグのため、顧客のメールアドレスをすべてログに書く

??? success "答えと解説"
    **正解: A, D**

    ロギングと監視をセットにします。

    - A: 正しい。異常に早く気づけます。
    - B: 誤り。機械で検索しにくくなります。
    - C: 誤り。調査ができません。
    - D: 正しい。検索しやすくなります。
    - E: 誤り。機密情報はログに書きません。

    **スキル:** [1.4.4](../domain1.md#skill-1-4-4) / **参照:** [構造化ログ](../../../services/observability.md#structured-logging)、[ロギング、モニタリング、オブザーバビリティの違い](../../../services/observability.md#logging-monitoring-observability)

### 問6 {#q6}

ETL のスクリプトと DAG、SQL を管理します。正しい実践はどれですか。

- A. S3 のスクリプトを本番で直接編集し、変更履歴はファイル名の日付で管理する
- B. 本番の環境で変更を試し、問題がなければ開発環境へ戻して記録する
- C. 開発者ごとの PC に最新版を置き、共有のリポジトリは使わないで運用する
- D. IaC とともに Git で管理し、リリースはタグで識別する

??? success "答えと解説"
    **正解: D**

    バージョン管理で変更を追跡します。

    - A: 誤り。誰が何を変えたか追えません。
    - B: 誤り。順序が逆です。
    - C: 誤り。共同の作業ができません。
    - D: 正しい。

    **スキル:** [1.4.4](../domain1.md#skill-1-4-4) / **参照:** [ブランチとタグでバージョンとリリースを管理する](../../../services/cicd.md#branches-tags)、[CloudFormation テンプレート](../../../services/iac.md#cloudformation-template)

### 問7 {#q7}

開発と本番に同じ Glue のジョブ、クローラー、IAM ロールを作ります。バケット名だけが異なります。どう書きますか。

- A. 環境ごとにテンプレートをコピーして、バケット名を直接書き換えて管理する
- B. 1 つのテンプレートにパラメータでバケット名を渡し、環境ごとにスタックを作る
- C. テンプレートに全環境のバケット名をコメントで書き、手で切り替える
- D. 開発はコンソールで作り、本番だけテンプレートから作るように分ける

??? success "答えと解説"
    **正解: B**

    環境ごとの値はパラメータで分けます。

    - A: 誤り。差が生まれて、管理も増えます。
    - B: 正しい。
    - C: 誤り。コメントは動作しません。
    - D: 誤り。環境の差をなくせません。

    **スキル:** [1.4.5](../domain1.md#skill-1-4-5) / **参照:** [CloudFormation テンプレート](../../../services/iac.md#cloudformation-template)、[パラメータ](../../../services/iac.md#parameters)

### 問8 {#q8}

CloudFormation で `AWS::Glue::Job` を定義します。ETL のスクリプトはどう扱いますか。

- A. スクリプトを S3 に置き、`Command` の `ScriptLocation` で参照する
- B. スクリプトの全文を `Role` のプロパティに埋め込んで渡す
- C. スクリプトは定義に書かず、起動のたびにコンソールで貼り付ける
- D. スクリプトを `WorkerType` のプロパティに書いて実行する

??? success "答えと解説"
    **正解: A**

    スクリプトは S3 に置いて参照します。

    - A: 正しい。
    - B: 誤り。`Role` は IAM ロールの指定です。
    - C: 誤り。再現できません。
    - D: 誤り。`WorkerType` はワーカーの種類です。

    **スキル:** [1.4.5](../domain1.md#skill-1-4-5) / **参照:** [CloudFormation テンプレート](../../../services/iac.md#cloudformation-template)、[ETL ジョブ](../../../services/data-engineering.md#glue-jobs)

### 問9 {#q9}

データ基盤の構築で、手作業ではなく IaC を選ぶ理由として最も適切なものはどれですか。

- A. テンプレートにすると実行時の性能が必ず上がる
- B. テンプレートにするとクォータの上限がなくなる
- C. 環境ごとの差をなくし、同じ構成を繰り返し作れる
- D. IaC を使うと手作業の変更が AWS 側で拒否される

??? success "答えと解説"
    **正解: C**

    IaC の主な利点は再現性です。

    - A: 誤り。性能は構成で決まります。
    - B: 誤り。クォータは残ります。
    - C: 正しい。
    - D: 誤り。手作業の変更はできるので、ドリフト検出で見つけます。

    **スキル:** [1.4.5](../domain1.md#skill-1-4-5) / **参照:** [どれを使うか](../../../services/iac.md#choosing)、[SAM](../../../services/iac.md#sam)

### 問10 {#q10}

Lambda、Step Functions、DynamoDB のパイプラインを短い定義でデプロイします。SAM のリソースの組み合わせとして正しいものはどれですか。

- A. `AWS::Serverless::Function`、`AWS::Serverless::Workflow`、`AWS::Serverless::DynamoDB`
- B. `AWS::Serverless::Lambda`、`AWS::StepFunctions::Serverless`、`AWS::Serverless::Table`
- C. `AWS::Glue::Job`、`AWS::Serverless::Queue`、`AWS::Serverless::Bucket`
- D. `AWS::Serverless::Function`、`AWS::Serverless::StateMachine`、`AWS::Serverless::SimpleTable`

??? success "答えと解説"
    **正解: D**

    SAM は CloudFormation の拡張です。

    - A: 誤り。そのような種類はありません。
    - B: 誤り。正しい名前ではありません。
    - C: 誤り。SAM の種類ではないものが含まれます。
    - D: 正しい。

    **スキル:** [1.4.6](../domain1.md#skill-1-4-6) / **参照:** [SAM](../../../services/iac.md#sam)、[テンプレート](../../../services/iac.md#sam-template)

### 問11 {#q11}

SAM のアプリケーションをパッケージにしてデプロイする CLI の手順はどれですか。

- A. `sam build` の後に `sam deploy`
- B. `sam init` の後に `sam local start-api`
- C. `cdk synth` の後に `cdk deploy`
- D. `sam local invoke` の後に `aws glue start-job-run`

??? success "答えと解説"
    **正解: A**

    `sam build` が依存を解決し、`sam deploy` でデプロイします。

    - A: 正しい。
    - B: 誤り。雛形の作成と手元の実行で、デプロイではありません。
    - C: 誤り。CDK のコマンドです。
    - D: 誤り。手元の確認と Glue の起動で、デプロイではありません。

    **スキル:** [1.4.6](../domain1.md#skill-1-4-6) / **参照:** [SAM CLI のコマンド](../../../services/iac.md#sam-cli)

### 問12 {#q12}

デプロイの前に、SAM の関数を手元でサンプルのイベントで動かします。どのコマンドですか。

- A. `cdk bootstrap`
- B. `sam local invoke`
- C. `sam deploy --guided`
- D. `aws lambda invoke --dry-run-local`

??? success "答えと解説"
    **正解: B**

    手元で関数を実行できます。

    - A: 誤り。CDK の準備のコマンドです。
    - B: 正しい。
    - C: 誤り。AWS へのデプロイです。
    - D: 誤り。そのようなオプションはありません。

    **スキル:** [1.4.6](../domain1.md#skill-1-4-6) / **参照:** [SAM CLI のコマンド](../../../services/iac.md#sam-cli)、[SAM](../../../services/iac.md#sam)

### 問13 {#q13}

データレイクのバケットをスタックで作りました。スタックを消してもバケットを残します。どの設定ですか。

- A. バケットの `VersioningConfiguration` を有効にしてスタックを削除する操作
- B. スタックのドリフト検出を有効にしてから、スタックを削除する操作
- C. リソースの `DeletionPolicy: Retain`
- D. スタックの変更セットを作成してから、スタックを削除する操作

??? success "答えと解説"
    **正解: C**

    `DeletionPolicy` で削除時の動作を決めます。

    - A: 誤り。バージョニングはリソースを残す設定ではありません。
    - B: 誤り。手作業の変更の検出です。
    - C: 正しい。
    - D: 誤り。更新の影響の確認で、残す設定ではありません。

    **スキル:** [1.4.8](../domain1.md#skill-1-4-8) / **参照:** [リソースの属性: DeletionPolicy](../../../services/iac.md#deletion-policy)

### 問14 {#q14}

本番のスタックの更新で、Redshift のクラスターが置き換わらないか事前に確認します。また手作業の変更も見つけます。組み合わせはどれですか。

- A. `cdk bootstrap` で更新の影響を確認し、パラメータで手作業の変更を見つける
- B. 変更セットで更新の影響を確認し、ドリフト検出で手作業の変更を見つける
- C. ドリフト検出で更新の影響を確認し、変更セットで手作業の変更を見つける
- D. StackSets で更新の影響を確認し、`DeletionPolicy` で手作業の変更を見つける

??? success "答えと解説"
    **正解: B**

    2 つの機能の役割を分けて覚えます。

    - A: 誤り。どちらも別の役割です。
    - B: 正しい。
    - C: 誤り。役割が逆です。
    - D: 誤り。どちらも別の役割です。

    **スキル:** [1.4.8](../domain1.md#skill-1-4-8) / **参照:** [変更セット](../../../services/iac.md#change-sets)、[ドリフト検出](../../../services/iac.md#drift)

### 問15 {#q15}

CDK と CloudFormation の説明として正しいものはどれですか。（2つ選択）

- A. CDK は `cdk synth` で CloudFormation テンプレートを生成する
- B. CloudFormation の再利用の単位はコンストラクトである
- C. CDK は YAML だけで書き、Python や TypeScript は使えない
- D. 複数のアカウントとリージョンへの展開には StackSets を使える
- E. CDK を使うと `cdk bootstrap` は常に不要である

??? success "答えと解説"
    **正解: A, D**

    CDK はコードで書き、CloudFormation を生成します。

    - A: 正しい。実体は CloudFormation です。
    - B: 誤り。コンストラクトは CDK の単位です。
    - C: 誤り。プログラミング言語で書きます。
    - D: 正しい。同じテンプレートを展開します。
    - E: 誤り。最初の準備が必要です。

    **スキル:** [1.4.8](../domain1.md#skill-1-4-8) / **参照:** [CDK](../../../services/iac.md#cdk)、[StackSets の設定](../../../services/iac.md#stacksets-settings)

### 問16 {#q16}

データパイプラインの CI で、PySpark の単体テストを実行し、スクリプトをパッケージにします。実行するサービスと定義はどれですか。

- A. CodeBuild と `buildspec.yml`
- B. CloudFormation と `samconfig.toml`
- C. CodeDeploy と `appspec.yml`
- D. CodePipeline と `requirements.txt`

??? success "答えと解説"
    **正解: A**

    テストとパッケージは CodeBuild です。

    - A: 正しい。
    - B: 誤り。デプロイの設定で、テストの実行ではありません。
    - C: 誤り。デプロイのサービスで、テストの実行が主な役割ではありません。
    - D: 誤り。連結のサービスで、依存の一覧はビルドの定義ではありません。

    **スキル:** [1.4.9](../domain1.md#skill-1-4-9) / **参照:** [サービスの役割](../../../services/cicd.md#overview)、[buildspec の構成](../../../services/cicd.md#buildspec)

### 問17 {#q17}

ETL の変更を開発へ自動で出し、結合テストの後に、担当者の確認を経て本番へ出します。どの構成ですか。

- A. CodeBuild の `buildspec.yml` に `sleep` を書き、担当者の確認の時間を確保する
- B. 本番の環境へ先に出してから開発へ出し、問題があれば戻すように順番を変える
- C. CodePipeline のステージの間に手動承認のアクションを入れる
- D. CodeDeploy のカナリアの割合で担当者の確認を待つ

??? success "答えと解説"
    **正解: C**

    手動承認は CodePipeline の機能です。

    - A: 誤り。承認の仕組みではありません。
    - B: 誤り。順序が逆です。
    - C: 正しい。
    - D: 誤り。承認の機能ではありません。

    **スキル:** [1.4.9](../domain1.md#skill-1-4-9) / **参照:** [手動承認](../../../services/cicd.md#manual-approval)、[複数環境への展開](../../../services/cicd.md#multi-environment)

### 問18 {#q18}

CI/CD のサービスの役割の説明として正しいものはどれですか。

- A. CodeBuild は本番の承認を待つ専用のワークフローのサービスである
- B. CodePipeline は Spark の変換を実行するサーバーレスの基盤である
- C. CodeDeploy はデータの品質を検査するルールを実行するサービスである
- D. CodeDeploy は Lambda のトラフィックを段階的に切り替えられる

??? success "答えと解説"
    **正解: D**

    それぞれの役割を区別します。

    - A: 誤り。テストとパッケージのサービスです。
    - B: 誤り。ステージの連結のサービスです。
    - C: 誤り。デプロイのサービスです。
    - D: 正しい。

    **スキル:** [1.4.9](../domain1.md#skill-1-4-9) / **参照:** [サービスの役割](../../../services/cicd.md#overview)、[サービス統合パターン](../../../services/step-functions.md#integration-patterns)
