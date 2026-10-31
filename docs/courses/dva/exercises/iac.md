# IaC の問題集

対象の解説: [IaC（CloudFormation / SAM / CDK / CLI）](../../../services/iac.md)

### 問1 {#q1}

手作業の変更でスタックのリソースがテンプレートとずれていないか確認しました。あるリソースの `StackResourceDriftStatus` が `DELETED` でした。正しい説明はどれですか。

- A. CloudFormation がリソースをテンプレートから自動で再作成している
- B. リソースがスタックの外で削除されている
- C. このリソースの種類はドリフト検出に対応していない
- D. プロパティの既定値がテンプレートと異なっている

??? success "答えと解説"
    **正解: B**

    `DELETED` は実際のリソースが削除された状態です。ドリフト検出は確認するだけで、自動で直しません。

    - A: 自動で修復しません。
    - B: 正しい説明です。
    - C: 対応していないリソースは `NOT_CHECKED` です。
    - D: 明示的に設定した値だけが比較の対象で、状態は `MODIFIED` です。

    **スキル:** C03 3.3.3 / **参照:** [ドリフト検出](../../../services/iac.md#drift)

### 問2 {#q2}

`Stage` が `prod` のときに、`InstanceType` が大きいサイズであることをリソース作成の前に検証したいと考えています。組み合わせの検証に最も適したものはどれですか。

- A. `Parameters` の `AllowedValues`
- B. `Conditions` の `Fn::If`
- C. `Rules` の `RuleCondition` と `Assertions`
- D. `Metadata` の `AWS::CloudFormation::Interface`

??? success "答えと解説"
    **正解: C**

    `Rules` はパラメータの組み合わせを検証します。条件に合わないと、作成の前に失敗して `AssertDescription` を表示します。

    - A: 1 つのパラメータの値の制限で、他のパラメータに依存できません。
    - B: 値を切り替えるだけで、検証しません。
    - C: 正しい方法です。
    - D: コンソールの表示の設定です。

    **スキル:** C03 3.3.3 / **参照:** [セクションの詳細](../../../services/iac.md#section-details)

### 問3 {#q3}

開発者のマシンには環境変数 `AWS_REGION=us-east-1` と `AWS_DEFAULT_REGION=eu-west-1` があり、`~/.aws/config` の `[default]` は `region = ap-northeast-1` です。`aws s3 ls` を `--region` なしで実行すると、どのリージョンが使われますか。

- A. `us-east-1`
- B. `eu-west-1`
- C. `ap-northeast-1`
- D. エラーになる

??? success "答えと解説"
    **正解: A**

    環境変数は設定ファイルより優先されます。`AWS_REGION` は `AWS_DEFAULT_REGION` より優先されます。

    - A: 正しい値です。
    - B: `AWS_REGION` に上書きされます。
    - C: 環境変数より優先度が低くなります。
    - D: エラーにはなりません。

    **スキル:** C03 2.1.3 / **参照:** [設定ファイルと優先順位](../../../services/iac.md#cli-config)

### 問4 {#q4}

本番のスタック更新の後 10 分間、5XX のアラームを監視し、発火したらスタック全体を戻したいと考えています。アラームのメトリクスにデータが来ないときも戻します。最も適切な設定はどれですか。

- A. ロールバックトリガーを `MonitoringTimeInMinutes: 10` で設定し、アラームの欠落データを `breaching` にする
- B. ロールバックトリガーを `MonitoringTimeInMinutes: 10` で設定し、アラームの欠落データは既定のままにする
- C. `CreationPolicy` の `Timeout` を `PT10M` に設定し、アラームを `DependsOn` で指定する
- D. スタックポリシーで `Update:*` を拒否し、発火時に手動で許可する

??? success "答えと解説"
    **正解: A**

    `INSUFFICIENT_DATA` では戻りません。データがないときも戻すには、欠落データを `breaching` にしてアラームを `ALARM` にします。監視は 0〜180 分、トリガーは 5 個までです。

    - A: 正しい設定です。
    - B: データがないときに戻りません。
    - C: `CreationPolicy` は作成時のシグナルを待つ設定です。
    - D: 更新の保護で、自動で戻す機能ではありません。

    **スキル:** C03 3.3.7 / **参照:** [ロールバックトリガー](../../../services/iac.md#rollback-triggers)

### 問5 {#q5}

`aws s3api list-objects-v2` を大きなバケットで実行すると、タイムアウトで失敗します。全件を取得する動作は変えたくありません。最も適切なオプションはどれですか。

- A. `--max-items 100`
- B. `--no-paginate`
- C. `--query "Contents[]"`
- D. `--page-size 100`

??? success "答えと解説"
    **正解: D**

    `--page-size` は 1 回の API 呼び出しの件数を減らし、全件は取得します。S3 の既定のページサイズは 1,000 です。

    - A: 出力の総数を制限します。全件は返りません。
    - B: 最初の 1 ページだけを取得します。
    - C: クライアント側の絞り込みで、サービスへの呼び出しは軽くなりません。
    - D: 正しいオプションです。

    **スキル:** C03 1.1.5 / **参照:** [ページネーション](../../../services/iac.md#cli-pagination)

### 問6 {#q6}

DynamoDB テーブルのプロパティの変更で置き換えが起きても、古いテーブルを残したいと考えています。また、スタックの削除でも残します。設定すべき属性はどれですか。（2つ選択）

- A. `UpdateReplacePolicy: Retain`
- B. `DeletionPolicy: Retain`
- C. `CreationPolicy`
- D. `UpdatePolicy`
- E. `DependsOn`

??? success "答えと解説"
    **正解: A, B**

    置き換えのときは `UpdateReplacePolicy`、スタックの削除のときは `DeletionPolicy` が効きます。データを守るなら両方を書きます。

    - A: 置き換えで元のリソースを残します。
    - B: 削除で残します。
    - C: 作成時のシグナルを待つ属性です。
    - D: 更新の進め方を決める属性で、古いリソースの保持とは別です。
    - E: 作成の順序の属性です。

    **スキル:** C03 3.3.3 / **参照:** [UpdateReplacePolicy](../../../services/iac.md#update-replace-policy)

### 問7 {#q7}

EC2 で動くアプリの起動が終わるまで、スタックの作成を完了させたくありません。インスタンスは起動に約 12 分かかります。設定は既定値を基準にします。最も適切な構成はどれですか。

- A. `DependsOn` で次のリソースへの依存を書く
- B. `CreationPolicy` は既定のままにし、`cfn-signal` で通知する
- C. `CreationPolicy` の `Timeout` を `PT15M` にし、`cfn-signal` で通知する
- D. `UpdatePolicy` の `PauseTime` を `PT15M` にする

??? success "答えと解説"
    **正解: C**

    `Timeout` の既定は `PT5M` で、12 分の起動には短すぎます。最大は 12 時間です。

    - A: 順序を決めるだけで、アプリの起動完了は待ちません。
    - B: 5 分でタイムアウトし、ロールバックします。
    - C: 正しい構成です。
    - D: 更新のときの設定で、作成には効きません。

    **スキル:** C03 3.3.3 / **参照:** [CreationPolicy](../../../services/iac.md#creation-policy)

### 問8 {#q8}

本番スタックの更新の前に変更セットを確認すると、RDS インスタンスの `Replacement` が `Conditional` でした。最も適切な解釈と対応はどれですか。

- A. 必ず置き換えが起きるので、実行を中止する
- B. 置き換えは起きないので、そのまま実行する
- C. 実行時の値で置き換えが決まるので、変更の内容を確認してから判断する
- D. 変更セットの作成が失敗しているので、作り直す

??? success "答えと解説"
    **正解: C**

    `Replacement` の値は `True`、`False`、`Conditional` です。`Conditional` は実行時の値で決まります。

    - A: 必ず起きるのは `True` です。
    - B: 起きないのは `False` です。
    - C: 正しい対応です。
    - D: 作成は成功していて、内容を表示しています。

    **スキル:** C03 3.3.3 / **参照:** [変更セット](../../../services/iac.md#change-sets)

### 問9 {#q9}

`cfn-init` が `AWS::CloudFormation::Init` の `config` を処理する順序として正しいものはどれですか。

- A. `files`、`packages`、`users`、`commands`、`services`
- B. `commands`、`packages`、`groups`、`files`、`services`
- C. `services`、`packages`、`files`、`commands`、`users`
- D. `packages`、`users`、`files`、`commands`、`services`

??? success "答えと解説"
    **正解: D**

    順序は `packages`、`groups`、`users`、`sources`、`files`、`commands`、`services` です。順序を変えたいなら `configSets` を使います。

    - A: `packages` が最初です。
    - B: `commands` は後のほうです。
    - C: `services` は最後です。
    - D: 正しい順序です。

    **スキル:** C03 3.3.3 / **参照:** [ヘルパースクリプト](../../../services/iac.md#cfn-helpers)

### 問10 {#q10}

Lambda を使うカスタムリソースが、例外で応答を送らずに終わりました。`ServiceTimeout` は指定していません。スタックはどうなりますか。

- A. 直ちに `CREATE_FAILED` になる
- B. 5 分後にロールバックする
- C. 1 時間まで待ってから失敗する
- D. 12 時間まで待ってから失敗する

??? success "答えと解説"
    **正解: C**

    応答は署名付き S3 URL へ送ります。応答がないと `ServiceTimeout`(既定 3,600 秒)まで待ちます。

    - A: 応答がないので、すぐには失敗しません。
    - B: `CreationPolicy` の既定と混同しています。
    - C: 正しい動作です。
    - D: `CreationPolicy` の最大と混同しています。

    **スキル:** C03 4.1.4 / **参照:** [カスタムリソース](../../../services/iac.md#custom-resources)

### 問11 {#q11}

スタックポリシーで `OrdersTable` の置き換えを拒否しています。今回だけ、承認を得た上で置き換えます。ポリシーを恒久的に変えない方法として最も適切なものはどれですか。

- A. `update-stack` で `--stack-policy-during-update-body` を指定する
- B. スタックの終了保護を無効にする
- C. `--capabilities CAPABILITY_IAM` を指定する
- D. `DeletionPolicy` を `Delete` にする

??? success "答えと解説"
    **正解: A**

    `--stack-policy-during-update-body` は、その更新の間だけ一時的なポリシーで上書きします。

    - A: 正しい方法です。
    - B: スタックの削除の保護です。
    - C: IAM の承認で、スタックポリシーに関係しません。
    - D: 削除の扱いで、スタックポリシーの拒否は変わりません。

    **スキル:** C03 3.3.3 / **参照:** [スタックポリシー](../../../services/iac.md#stack-policy)

### 問12 {#q12}

`RoleName` を指定した IAM ロールを含むテンプレートを `--capabilities CAPABILITY_IAM` でデプロイしたところ、失敗しました。正しい対応はどれですか。

- A. `CAPABILITY_AUTO_EXPAND` に変更する
- B. `--capabilities` を外す
- C. `--role-arn` に管理者ロールを指定する
- D. `CAPABILITY_NAMED_IAM` に変更する

??? success "答えと解説"
    **正解: D**

    名前を指定した IAM リソースには `CAPABILITY_NAMED_IAM` が必要です。

    - A: マクロやトランスフォーム向けの承認です。
    - B: IAM リソースの承認が必要なので失敗します。
    - C: 実行する権限の問題ではなく、承認の問題です。
    - D: 正しい対応です。

    **スキル:** C03 4.1.4 / **参照:** [機能の承認(capabilities)](../../../services/iac.md#capabilities)

### 問13 {#q13}

VPC のスタックが出力をエクスポートし、チームごとの複数のスタックが参照しています。ライフサイクルは別々です。再利用の方法として最も適切なものはどれですか。また、注意点はどれですか。

- A. ネストされたスタックにする。親を更新すると子も更新される
- B. `Export` と `ImportValue` を使う。参照されている間は値を変更できない
- C. `Export` と `ImportValue` を使う。別のアカウントからも参照できる
- D. StackSets を使う。出力を自動で共有できる

??? success "答えと解説"
    **正解: B**

    独立したスタックで値を共有するならエクスポートです。参照されている間は、値の変更とスタックの削除ができません。

    - A: ライフサイクルが親に結び付くので合いません。
    - B: 正しい組み合わせです。
    - C: `ImportValue` は同じアカウントとリージョンだけです。
    - D: 複数のアカウントとリージョンへの展開の機能です。

    **スキル:** C03 3.3.3 / **参照:** [ネストとエクスポートの比較](../../../services/iac.md#nested-vs-exports)

### 問14 {#q14}

新しいスタックの作成に失敗したときに、原因を調べるためリソースを残したいと考えています。`aws cloudformation create-stack` のオプションとして最も適切なものはどれですか。

- A. `--on-failure DELETE`
- B. `--on-failure ROLLBACK`
- C. `--on-failure DO_NOTHING`
- D. `--enable-termination-protection`

??? success "答えと解説"
    **正解: C**

    `DO_NOTHING` は失敗したリソースも含めて残します。`--disable-rollback` と同時には指定できません。

    - A: スタックごと削除します。
    - B: 既定の動作で、リソースを消します。
    - C: 正しいオプションです。
    - D: 削除を防ぐ設定で、失敗時の動作を変えません。

    **スキル:** C03 4.1.4 / **参照:** [作成の失敗時の動作](../../../services/iac.md#on-failure)

### 問15 {#q15}

SAM の `Globals` に `Timeout: 10` と `Environment.Variables.STAGE: prod` があります。関数の `Timeout` は 30 で、`Environment.Variables.TABLE: orders` です。関数の設定はどうなりますか。

- A. `Timeout` は 10、変数は `STAGE` のみ
- B. `Timeout` は 30、変数は `TABLE` のみ
- C. `Timeout` は 30、変数は `STAGE` と `TABLE`
- D. デプロイのときにエラーになる

??? success "答えと解説"
    **正解: C**

    基本の型は置き換え、マップはマージ、リストは追加です。

    - A: リソース側の値が優先です。
    - B: マップはマージされます。
    - C: 正しい結果です。
    - D: 上書きはエラーになりません。

    **スキル:** C03 3.3.3 / **参照:** [Globals](../../../services/iac.md#sam-globals)

### 問16 {#q16}

SAM の関数が、DynamoDB テーブル `OrdersTable` の読み書きだけを許可されるようにします。IAM のドキュメントを書かず、最も簡潔な書き方はどれですか。

- A. `Policies: [AmazonDynamoDBFullAccess]`
- B. `Policies: [{DynamoDBCrudPolicy: {TableName: !Ref OrdersTable}}]`
- C. `Role: DynamoDBCrudPolicy`
- D. `Policies: [{DynamoDBReadPolicy: {TableName: !Ref OrdersTable}}]`

??? success "答えと解説"
    **正解: B**

    ポリシーテンプレートはプレースホルダーでリソースを絞ります。読み書きなら `DynamoDBCrudPolicy` です。

    - A: すべてのテーブルに広い権限を与えます。
    - B: 正しい書き方です。
    - C: `Role` はロールの ARN を指定するプロパティです。
    - D: 読み取りだけで、書き込みができません。

    **スキル:** C03 2.1.6 / **参照:** [Policies](../../../services/iac.md#sam-policies)

### 問17 {#q17}

SAM で Lambda の新しい版へトラフィックを段階的に移し、エラーの増加で戻したいと考えています。必要な組み合わせはどれですか。（3つ選択）

- A. `AutoPublishAlias`
- B. `DeploymentPreference` の `Type`
- C. `DeploymentPreference` の `Alarms`
- D. `sam sync --watch`
- E. `Globals` の `SimpleTable`
- F. `sam local start-api`

??? success "答えと解説"
    **正解: A, B, C**

    `AutoPublishAlias` で新しいバージョンとエイリアスを作り、`Type` で移し方を決め、`Alarms` で発火時に戻します。

    - A: 必要です。
    - B: 必要です。
    - C: 必要です。
    - D: 開発向けの同期で、本番には勧められません。
    - E: テーブルの共通設定で関係ありません。
    - F: ローカルの実行で関係ありません。

    **スキル:** C03 3.3.7 / **参照:** [DeploymentPreference によるカナリア](../../../services/iac.md#deployment-preference)

### 問18 {#q18}

AWS CLI の動作について、正しいものはどれですか。（2つ選択）

- A. `--query` は結果を受け取った後にクライアント側で絞り込む
- B. `--dry-run` で権限があるときは `DryRunOperation` が返る
- C. `--filters` はクライアント側の JMESPath の処理である
- D. `--dry-run` はすべての API で使える
- E. `--output off` は結果を JSON で標準出力へ出す

??? success "答えと解説"
    **正解: A, B**

    `--query` は JMESPath でクライアント側で動きます。EC2 などの `--dry-run` は、権限があれば `DryRunOperation`、なければ `UnauthorizedOperation` です。

    - A: 正しい説明です。
    - B: 正しい説明です。
    - C: `--filters` はサービス側の絞り込みです。
    - D: `--dry-run` がない API もあります。
    - E: `off` は標準出力を抑止します。

    **スキル:** C03 1.1.5 / **参照:** [--query で絞り込む](../../../services/iac.md#cli-query)

### 問19 {#q19}

CDK で次の要件があります。VPC の参照結果をチームで同じにし、別の AWS リージョンへ初めてデプロイする準備をします。適切な対応はどれですか。（2つ選択）

- A. `cdk.context.json` をソース管理に入れる
- B. `cdk bootstrap` を新しいリージョンで実行する
- C. `cdk.context.json` を手で編集して値を固定する
- D. `cdk deploy --hotswap` で初回をデプロイする
- E. L1 コンストラクトを L3 に書き換える

??? success "答えと解説"
    **正解: A, B**

    ルックアップの結果は `cdk.context.json` に保存されるので、コミットして共有します。ブートストラップはアカウントとリージョンごとに必要です。

    - A: 正しい対応です。
    - B: 正しい対応です。
    - C: 手で編集せず、`cdk context` で管理します。
    - D: 開発用のオプションで、ブートストラップの代わりになりません。
    - E: コンストラクトのレベルは関係ありません。

    **スキル:** C03 3.3.3 / **参照:** [コンテキスト](../../../services/iac.md#cdk-context)

### 問20 {#q20}

CloudShell で 40 分かかるスクリプトを実行し、途中で画面を操作しませんでした。セッションが途中で終わりました。正しい説明はどれですか。

- A. 動いているプロセスがあれば非アクティブと判定されないので、別の原因である
- B. VPC 環境でないと 15 分で終わる
- C. 永続ストレージの 1 GB を超えたので終了した
- D. キーボードとポインターの操作が 20〜30 分ないと終わり、プロセスは操作に数えない

??? success "答えと解説"
    **正解: D**

    非アクティブの判定は操作だけで決まります。長いジョブには EC2、CodeBuild などを使います。

    - A: 動いているプロセスは操作に数えません。
    - B: 通常の環境でも 20〜30 分です。
    - C: 容量とセッションの終了は別の話です。
    - D: 正しい説明です。

    **スキル:** C03 2.1.3 / **参照:** [CloudShell](../../../services/iac.md#cloudshell)

### 問21 {#q21}

CDK のスタックで、SQS キューの可視性タイムアウトが 360 秒であることをテストします。デプロイせず、関係のない変更ではテストが失敗しないようにしたいと考えています。最も適切な方法はどれですか。

- A. 合成したテンプレート全体を、スナップショットのテストで基準と比較する
- B. `cdk deploy` の後で `GetQueueAttributes` を呼び、キューの属性の値を確認する
- C. `cdk diff` の出力を毎回確認し、差分を人の目で判断する
- D. `Template.fromStack` の `hasResourceProperties` で検証する

??? success "答えと解説"
    **正解: D**

    きめ細かいアサーションは、合成した CloudFormation テンプレートの特定のプロパティを検証します。デプロイは不要です。

    - A: 誤り。全体を比べるので、関係のない変更でも失敗します。
    - B: 誤り。デプロイが必要です。
    - C: 誤り。自動のテストになりません。
    - D: 正しい。必要な値だけを検証できます。

    **スキル:** C03 3.2.1 / **参照:** [assertions によるテスト](../../../services/iac.md#cdk-testing)

### 問22 {#q22}

CI で SAM テンプレートを検査しています。`aws cloudformation validate-template` は成功したのに、プロパティの値の誤りでデプロイが失敗しました。このような誤りをデプロイの前に見つけたいと考えています。最も適切なものはどれですか。

- A. `aws cloudformation validate-template` を変換後のテンプレートにも実行する
- B. `sam validate --lint` で cfn-lint の検査を実行する
- C. `sam local generate-event` でイベントを作り、テンプレートと比較する
- D. `sam build` を実行し、ビルドの成功をもって検査の合格とする

??? success "答えと解説"
    **正解: B**

    `ValidateTemplate` は JSON か YAML として正しいかを確認するものなので、プロパティの値の誤りは見つけられません。`sam validate --lint` は cfn-lint でテンプレートを検査します。cfn-lint はカレントディレクトリの設定からカスタムルールを読むので、信頼できないコードには実行しません。

    - A: 誤り。対象を変えても、検査の内容は同じです。
    - B: 正しい。デプロイの前に CI で実行できます。
    - C: 誤り。テスト用のイベントを作るコマンドです。
    - D: 誤り。コードの準備であって、プロパティの値の検査ではありません。

    **スキル:** C03 3.2.1 / **参照:** [テンプレートの検証方法のまとめ](../../../services/iac.md#validate-iac)

### 問23 {#q23}

S3 の `ObjectCreated` で動く関数をローカルで試します。S3 のイベントの JSON をゼロから書かずに用意し、Docker で関数を実行したいと考えています。最も適切な手順はどれですか。

- A. `sam deploy` の後でバケットにファイルを置き、本物のイベントで関数を動かす
- B. `sam validate` の出力をファイルに保存し、`sam local start-api` に渡して実行する
- C. `sam local generate-event` の結果を `sam local invoke` に渡す
- D. `aws lambda invoke` に `{}` を渡し、関数のログからイベントの形を確認する

??? success "答えと解説"
    **正解: C**

    `sam local generate-event` はサービスごとのイベントのサンプルを生成します。`--bucket` などで値も変えられます。`sam local invoke --event` はローカルのコンテナで関数を実行します。

    - A: 誤り。動きますが、デプロイが必要でローカルの実行ではありません。
    - B: 誤り。`sam validate` はテンプレートの検査で、イベントは出力しません。
    - C: 正しい。要件のとおりです。
    - D: 誤り。デプロイ済みの関数を呼ぶもので、S3 のイベントの形にもなりません。

    **スキル:** C03 3.2.3 / **参照:** [テストイベントの作成](../../../services/iac.md#test-events)
