# CI/CD の問題集

対象の解説: [CI/CD（CodeBuild / CodeDeploy / CodePipeline）](../../../services/cicd.md)

### 問1 {#q1}

CodeBuild のプロジェクトで、`buildspec.yml` の `APP_ENV` が `staging`、プロジェクトの環境変数が `dev`、`start-build` の `--environment-variables-override` が `prod` です。ビルド中の `APP_ENV` の値はどれですか。

- A. `staging`
- B. `dev`
- C. `prod`
- D. エラーになり、ビルドが失敗する

??? success "答えと解説"
    **正解: C**

    優先順位は、ビルド開始時の指定、プロジェクトの定義、buildspec の順です。

    - A: buildspec の値は最も低い優先度です。
    - B: プロジェクトの値はビルド開始時の指定に上書きされます。
    - C: 正しい値です。
    - D: 同じ名前の定義はエラーになりません。

    **スキル:** C03 3.1.1 / **参照:** [buildspec のセクション](../../../services/cicd.md#buildspec-sections)

### 問2 {#q2}

ビルドでデータベースのパスワードを使います。値を buildspec に残さず、ログにも出さないようにします。JSON 形式のシークレット `prod/db` の `password` キーを読みます。最も適切な記述はどれですか。

- A. `env.variables` に `DB_PASSWORD: "prod/db:password"` と書く
- B. `env.exported-variables` に `DB_PASSWORD` と書く
- C. `env.parameter-store` に `DB_PASSWORD: "prod/db"` と書く
- D. `env.secrets-manager` に `DB_PASSWORD: "prod/db:password"` と書く

??? success "答えと解説"
    **正解: D**

    `シークレットID:JSONキー` の形式で書き、サービスロールに読み取り権限を与えます。値はログでマスクされます。

    - A: 文字列がそのまま値になり、シークレットを取得しません。
    - B: 後続のアクションへ渡す設定で、取得の設定ではありません。
    - C: Parameter Store のパラメータを読む設定です。
    - D: 正しい記述です。

    **スキル:** C03 2.2.7 / **参照:** [secrets-manager の指定](../../../services/cicd.md#buildspec-secrets)

### 問3 {#q3}

開発者は、ログ出力の前に Secrets Manager の値を Base64 に変換しました。ログにはこの文字列がそのまま表示されています。原因として最も適切なものはどれですか。

- A. サービスロールに `kms:Decrypt` がない
- B. マスクは保存値との完全一致で行われる
- C. `git-credential-helper` が無効である
- D. buildspec の `version` が `0.2` である

??? success "答えと解説"
    **正解: B**

    マスクは Secrets Manager か Parameter Store に保存された値との完全一致です。変換した文字列は対象外です。

    - A: 値を取得できているので、権限の問題ではありません。
    - B: 正しい原因です。
    - C: Git 認証情報の設定で関係ありません。
    - D: `0.2` は推奨の版です。

    **スキル:** C03 2.2.7 / **参照:** [環境変数とシークレット](../../../services/cicd.md#build-env)

### 問4 {#q4}

Docker イメージをビルドする CodeBuild プロジェクトで、`Cannot connect to the Docker daemon` が出ます。プロジェクトの設定で変更すべきものはどれですか。

- A. `privilegedMode` を `true` にする
- B. `timeoutInMinutes` を 120 にする
- C. `imagePullCredentialsType` を `SERVICE_ROLE` にする
- D. `queuedTimeoutInMinutes` を 480 にする

??? success "答えと解説"
    **正解: A**

    Docker デーモンをコンテナの中で動かすには特権モードが必要です。既定は `false` です。

    - A: 正しい設定です。
    - B: タイムアウトの設定です。
    - C: ビルドイメージの取得に使う認証情報の設定です。
    - D: キューの待ち時間です。

    **スキル:** C03 3.1.2 / **参照:** [プロジェクトの設定](../../../services/cicd.md#codebuild-project)

### 問5 {#q5}

CodeBuild のプロジェクトのタイムアウトについて、正しいものはどれですか。（2つ選択）

- A. `timeoutInMinutes` の既定は 60 分である
- B. `timeoutInMinutes` の上限は 480 分である
- C. `queuedTimeoutInMinutes` の範囲は 5〜480 分である
- D. `queuedTimeoutInMinutes` の上限は 2,160 分である
- E. `timeoutInMinutes` の既定は 30 分である

??? success "答えと解説"
    **正解: A, C**

    `timeoutInMinutes` は既定 60 分で 5〜2,160 分(36 時間)です。`queuedTimeoutInMinutes` は 5〜480 分です。

    - A: 正しい説明です。
    - B: 480 はキューのタイムアウトの上限です。
    - C: 正しい説明です。
    - D: 2,160 はビルドのタイムアウトの上限です。
    - E: 既定は 60 分です。

    **スキル:** C03 3.3.5 / **参照:** [プロジェクトの設定](../../../services/cicd.md#codebuild-project)

### 問6 {#q6}

CodeBuild の Webhook を設定します。`main` へのプッシュで動かし、ただしファイルパスが `^docs/.*` に一致するイベントは除外します。最も適切なフィルターの構成はどれですか。

- A. グループ 1 に `EVENT: PUSH`、グループ 2 に `HEAD_REF: ^refs/heads/main$`、グループ 3 に `FILE_PATH: ^docs/.*`
- B. 1 つのグループに `EVENT: PULL_REQUEST_MERGED` と `BASE_REF: main` を置く
- C. 1 つのグループに `EVENT: PUSH`、`HEAD_REF: ^refs/heads/main$`、除外の `FILE_PATH: ^docs/.*` を置く
- D. 1 つのグループに `EVENT: PUSH`、`HEAD_REF: main`、`FILE_PATH: ^(?!docs/)` を置く

??? success "答えと解説"
    **正解: C**

    グループの中のフィルターは AND、グループどうしは OR です。除外は `excludeMatchedPattern: true` で指定します。

    - A: OR になるので、どのプッシュでも動きます。
    - B: PR のマージのイベントで、要件と違います。
    - C: 正しい構成です。
    - D: RE2 は先読みに対応しません。`main` だけだと他のブランチ名にも一致します。

    **スキル:** C03 3.3.5 / **参照:** [Webhook とフィルターグループ](../../../services/cicd.md#codebuild-webhook)

### 問7 {#q7}

VPC の RDS に接続する統合テストのために `vpcConfig` を設定したところ、`pip install` と外部へのアクセスが失敗するようになりました。最も適切な対応はどれですか。

- A. パブリックサブネットを指定し、ビルド環境にパブリック IP を割り当てる
- B. 特権モードを有効にする
- C. セキュリティグループのインバウンドを全開放する
- D. プライベートサブネットと NAT ゲートウェイの経路を用意する

??? success "答えと解説"
    **正解: D**

    VPC で動くビルドの外向きの通信には、NAT ゲートウェイか VPC エンドポイントが必要です。

    - A: 公式の手順は、プライベートサブネットと NAT ゲートウェイの構成です。パブリックサブネットだけでは解決しません。
    - B: Docker の設定で、ネットワークの経路は変わりません。
    - C: 問題は外向きの経路で、インバウンドではありません。
    - D: 正しい対応です。

    **スキル:** C03 4.1.4 / **参照:** [VPC の設定](../../../services/cicd.md#codebuild-vpc)

### 問8 {#q8}

Python の 3.11 と 3.12 のすべての組み合わせでテストするバッチビルドを、最も簡潔に書きたいと考えています。使うキーはどれですか。

- A. `batch.build-graph`
- B. `batch.build-matrix`
- C. `batch.fast-fail`
- D. `artifacts.secondary-artifacts`

??? success "答えと解説"
    **正解: B**

    `build-matrix` は変数の組み合わせごとにビルドを作ります。

    - A: 依存関係のあるビルドを定義します。
    - B: 正しいキーです。
    - C: 失敗時に残りを止めるかの設定です。
    - D: 成果物を複数出力する設定です。

    **スキル:** C03 3.2.1 / **参照:** [batch](../../../services/cicd.md#buildspec-batch)

### 問9 {#q9}

CodeDeploy の EC2 向けインプレースデプロイで、配置先に以前のデプロイに含まれないファイルがあり、失敗しました。そのファイルを新しいリビジョンの版で置き換えて進めたいと考えています。最も適切な設定はどれですか。

- A. `file_exists_behavior: OVERWRITE`
- B. `file_exists_behavior: RETAIN`
- C. `file_exists_behavior: DISALLOW`
- D. `permissions` に `except` を追加する

??? success "答えと解説"
    **正解: A**

    `OVERWRITE` はリビジョンの版で置き換えます。

    - A: 正しい設定です。
    - B: 既存のファイルを残し、リビジョンの版はコピーしません。
    - C: デプロイを失敗させる動作です。
    - D: 権限の設定で、ファイルの競合は解決しません。

    **スキル:** C03 3.3.4 / **参照:** [AppSpec の項目(EC2 / オンプレミス)](../../../services/cicd.md#appspec-ec2)

### 問10 {#q10}

CodeDeploy の新しいリビジョンでスクリプトを直したのに、`ApplicationStop` で同じエラーが続きます。原因として最も適切なものはどれですか。

- A. `ApplicationStop` は最後に成功したデプロイの AppSpec のスクリプトを実行する
- B. `ApplicationStop` のスクリプトは `Install` の後に実行される
- C. `ApplicationStop` のスクリプトは `runas` が必須である
- D. `timeout` の既定値が 60 秒である

??? success "答えと解説"
    **正解: A**

    `ApplicationStop` は新しいリビジョンがダウンロードされる前に動くので、前回成功したデプロイのスクリプトを使います。そのため新しい版で直しても効きません。

    - A: 正しい原因です。
    - B: `DownloadBundle` より前に動きます。
    - C: `runas` は任意です。
    - D: 既定値は 3,600 秒です。

    **スキル:** C03 4.1.4 / **参照:** [ライフサイクルイベントの順序](../../../services/cicd.md#lifecycle-hooks)

### 問11 {#q11}

CodeDeploy の EC2 / オンプレミスのインプレースデプロイで、AppSpec にスクリプトを指定できるイベントを、実行順に正しく並べたものはどれですか。

- A. `ApplicationStop`、`BeforeInstall`、`AfterInstall`、`ApplicationStart`、`ValidateService`
- B. `BeforeInstall`、`ApplicationStop`、`AfterInstall`、`ValidateService`、`ApplicationStart`
- C. `ApplicationStop`、`DownloadBundle`、`Install`、`ApplicationStart`、`ValidateService`
- D. `BeforeInstall`、`AfterInstall`、`ApplicationStop`、`ApplicationStart`、`ValidateService`

??? success "答えと解説"
    **正解: A**

    `ApplicationStop` の後に `DownloadBundle`、`BeforeInstall`、`Install`、`AfterInstall`、`ApplicationStart`、`ValidateService` と進みます。

    - A: 正しい順序です。
    - B: `ApplicationStop` は最初で、`ValidateService` は最後です。
    - C: `DownloadBundle` と `Install` はスクリプトを指定できません。
    - D: `ApplicationStop` の位置が違います。

    **スキル:** C03 3.3.4 / **参照:** [ライフサイクルイベントの順序](../../../services/cicd.md#lifecycle-hooks)

### 問12 {#q12}

CodeDeploy の ECS のデプロイで、テストリスナーが置き換えのタスクセットへトラフィックを流した直後に検証を実行するフックはどれですか。また、Lambda のデプロイでこのフックは使えますか。

- A. `BeforeAllowTraffic`。Lambda でも使える
- B. `ValidateService`。Lambda でも使える
- C. `AfterAllowTestTraffic`。Lambda では使えない
- D. `AfterInstall`。Lambda では使えない

??? success "答えと解説"
    **正解: C**

    `AfterAllowTestTraffic` は、テストリスナーへ流した後に動きます。Lambda のフックは `BeforeAllowTraffic` と `AfterAllowTraffic` の 2 つだけです。

    - A: Lambda でも使えますが、ECS では本番トラフィックの切り替えの直前に動くフックで、テストトラフィックの直後ではありません。
    - B: EC2 / オンプレミスのイベントです。
    - C: 正しい組み合わせです。
    - D: `AfterInstall` はテストトラフィックの前で、検証に使えません。

    **スキル:** C03 3.3.4 / **参照:** [ライフサイクルイベントの順序](../../../services/cicd.md#lifecycle-hooks)

### 問13 {#q13}

10 台の EC2 に CodeDeploy でデプロイします。最小正常ホストを `FLEET_PERCENT` の 85 にしました。最初に更新した 1 台のデプロイに失敗すると、どうなりますか。

- A. 残りの 9 台へのデプロイを続けて成功とする
- B. 全体が失敗する
- C. 失敗した 1 台だけを自動で再試行し続ける
- D. 全インスタンスを終了する

??? success "答えと解説"
    **正解: B**

    1 台を更新中で正常は 90% です。そこで 1 台が失敗すると、失敗の 1 台とオフラインの 1 台で 80% になり、85% を下回ります。全体が失敗です。最後の 1 台の失敗だけは例外で、全体は成功します。

    - A: 最小正常ホストを下回るので続けられません。
    - B: 正しい動作です。
    - C: 自動で再試行し続ける機能はありません。
    - D: インスタンスは終了しません。

    **スキル:** C03 3.3.4 / **参照:** [最小正常ホスト](../../../services/cicd.md#minimum-healthy-hosts)

### 問14 {#q14}

CodeDeploy のデプロイグループに CloudWatch アラームを関連付けました。アラームが発火するとデプロイは止まりますが、前の版に戻りません。最も適切な対応はどれですか。

- A. `ignorePollAlarmFailure` を `true` にする
- B. `DEPLOYMENT_STOP_ON_ALARM` の自動ロールバックを有効にする
- C. デプロイ設定を `OneAtATime` に変更する
- D. アラームの数を増やす

??? success "答えと解説"
    **正解: B**

    アラームだけでは `Stopped` になるだけです。自動ロールバックを別に有効にします。戻すときは新しいデプロイ ID が振られます。

    - A: アラームの状態を取得できなくても続ける設定です。
    - B: 正しい対応です。
    - C: 進め方の設定で、ロールバックは有効になりません。
    - D: 検知が増えるだけです。

    **スキル:** C03 3.3.7 / **参照:** [ロールバックとアラームの設定](../../../services/cicd.md#codedeploy-rollback-settings)

### 問15 {#q15}

CodeDeploy の定義済みの設定名として、実在するものはどれですか。（2つ選択）

- A. `CodeDeployDefault.LambdaLinear10PercentEvery3Minutes`
- B. `CodeDeployDefault.ECSCanary10Percent15Minutes`
- C. `CodeDeployDefault.ECSCanary10Percent30Minutes`
- D. `CodeDeployDefault.LambdaLinear10PercentEvery5Minutes`
- E. `CodeDeployDefault.ECSLinear10PercentEvery2Minutes`

??? success "答えと解説"
    **正解: A, B**

    Lambda の線形は 1、2、3、10 分です。ECS のカナリアは 5、15 分、線形は 1、3 分です。

    - A: 実在します。
    - B: 実在します。
    - C: 30 分は Lambda のカナリアにだけあります。
    - D: 5 分の線形はありません。
    - E: ECS の線形は 1 分と 3 分です。

    **スキル:** C03 3.3.6 / **参照:** [デプロイ設定](../../../services/cicd.md#deployment-configs)

### 問16 {#q16}

Git のタグ `v*` のプッシュでだけ本番パイプラインを起動し、新しい実行が古い実行を置き換えず順に処理したいと考えています。必要な設定はどれですか。（2つ選択）

- A. パイプラインタイプを V1 にする
- B. 実行モードを `SUPERSEDED` にする
- C. 実行モードを `PARALLEL` にする
- D. V2 のトリガーで Git タグのフィルターを設定する
- E. 実行モードを `QUEUED` にする

??? success "答えと解説"
    **正解: D, E**

    Git タグのフィルターと `QUEUED` モードは、どちらも V2 だけの機能です。`QUEUED` は到着順に 1 つずつ処理します。

    - A: V1 にはトリガーのフィルターも `QUEUED` もありません。
    - B: 新しい実行が古い実行を置き換えます。
    - C: 実行どうしが同時に動きます。
    - D: 必要な設定です。
    - E: 必要な設定です。

    **スキル:** C03 3.3.5 / **参照:** [パイプラインタイプ](../../../services/cicd.md#pipeline-types)

### 問17 {#q17}

CodeBuild のアクションがエクスポートした `IMAGE_TAG` を、次の Deploy アクションの設定で使います。CodeBuild のアクションの名前空間は `BuildVariables` です。正しい参照はどれですか。

- A. `${BuildVariables.IMAGE_TAG}`
- B. `#{variables.IMAGE_TAG}`
- C. `#{BuildVariables.IMAGE_TAG}`
- D. `{{resolve:BuildVariables:IMAGE_TAG}}`

??? success "答えと解説"
    **正解: C**

    アクションの変数は `#{名前空間.キー}` で参照します。buildspec の `exported-variables` に書いておきます。

    - A: 記法が違います。
    - B: パイプラインレベルの変数の書き方です。
    - C: 正しい参照です。
    - D: CloudFormation の動的参照に似た記法で、ここでは使えません。

    **スキル:** C03 3.3.5 / **参照:** [変数](../../../services/cicd.md#pipeline-variables)

### 問18 {#q18}

本番ステージのデプロイの後で 5XX のアラームが発火したら、前回成功した実行の版へ自動で戻します。V2 パイプラインを使っています。最も適切な設定はどれですか。

- A. ステージの On Success 条件に `CloudWatchAlarm` のルールを置き、結果を Rollback にする
- B. ステージの Entry 条件に `CloudWatchAlarm` のルールを置き、結果を Skip にする
- C. 実行モードを `PARALLEL` にして On Failure 条件で Rollback にする
- D. Approval アクションを置き、SNS で担当者に通知する

??? success "答えと解説"
    **正解: A**

    On Success 条件の結果は Rollback か Fail です。デプロイの成功後にアラームを確認して戻します。

    - A: 正しい設定です。
    - B: デプロイ前の判定で、問題があるステージを飛ばす動作になります。
    - C: `PARALLEL` モードではステージのロールバックを使えません。
    - D: 人の操作が必要で、自動で戻りません。

    **スキル:** C03 3.3.7 / **参照:** [ステージ条件](../../../services/cicd.md#stage-conditions)

### 問19 {#q19}

CodeArtifact で、社内パッケージと同じ名前の公開パッケージが取り込まれるのを防ぎたいと考えています。また、認証トークンの性質も確認しています。正しいものはどれですか。（2つ選択）

- A. パッケージオリジンコントロールで、アップストリームからの取り込みを `BLOCK` にする
- B. 認証トークンの既定の有効期間は 12 時間である
- C. 1 つのリポジトリには直接のアップストリームを 100 個まで設定できる
- D. アップストリームには別のドメインの公開リポジトリを直接指定する
- E. 認証トークンは最長 7 日間に延ばせる

??? success "答えと解説"
    **正解: A, B**

    パッケージごとに公開と取り込みを制御でき、依存関係かく乱を防げます。トークンの既定は 12 時間で、15 分〜12 時間です。

    - A: 正しい対策です。
    - B: 正しい値です。
    - C: 直接のアップストリームは 10 個までです。
    - D: アップストリームは同じドメインのリポジトリで、公開リポジトリには外部接続を使います。
    - E: 上限は 12 時間です。

    **スキル:** C03 3.1.1 / **参照:** [ドメインとリポジトリの設定](../../../services/cicd.md#codeartifact-settings)

### 問20 {#q20}

Amplify Hosting を使っているチームで、PR ごとの確認環境を増やしたところ、新しいブランチを作れないエラーが発生するようになりました。最も適切な対応はどれですか。

- A. クォータの引き上げを申請し、ブランチの上限を増やす
- B. `amplify.yml` の `version` を 2 に変更する
- C. 環境変数 `AWS_BRANCH` を削除する
- D. 不要な PR を閉じ、アプリあたり 50 のブランチに収める

??? success "答えと解説"
    **正解: D**

    Web プレビューの PR はブランチのクォータ(アプリあたり 50)に数えます。このクォータは引き上げできません。

    - A: `Branches per app` は引き上げできません。
    - B: ビルド設定の形式の話で、クォータとは関係ありません。
    - C: `AWS_BRANCH` は組み込みの変数で、この問題を解決しません。
    - D: 正しい対応です。

    **スキル:** C03 3.2.4 / **参照:** [Amplify Hosting とブランチ](../../../services/cicd.md#amplify)
