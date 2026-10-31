# CloudFormation、CDK、Terraform の問題集

対象の解説: [どれを使うか](../../../services/iac.md#choosing)、[CloudFormation テンプレート](../../../services/iac.md#cloudformation-template)、[CDK](../../../services/iac.md#cdk)、[StackSets とドリフトの運用](../../../services/operations.md#stacksets-drift)、[AWS Resource Access Manager](../../../services/governance.md#ram)

### 問1 {#q1}

本番のスタックを更新する前に、どのリソースが置き換えになるのかを確認したいです。どの機能を使いますか。

- A. ドリフト検出
- B. 変更セット
- C. ロールバックトリガー
- D. スタックポリシー

??? success "答えと解説"
    **正解: B**

    変更セットは、適用の前に変更の内容を確認します。

    - A: 誤り。手動の変更を見つける機能で、これからの更新の影響は確認できない。
    - B: 正しい。
    - C: 誤り。更新の後に戻す機能である。
    - D: 誤り。更新を防ぐ機能で、影響の確認はしない。

    **スキル:** [3.1.2](../domain3.md#skill-3-1-2) / **参照:** [変更セット](../../../services/iac.md#change-sets)

### 問2 {#q2}

担当者がコンソールでセキュリティグループを手で変更したようです。テンプレートとの違いを見つけたいです。どの機能を使いますか。

- A. 変更セット
- B. `cdk synth`
- C. ドリフト検出
- D. `cfn-signal`

??? success "答えと解説"
    **正解: C**

    手動の変更はドリフト検出で見つけます。

    - A: 誤り。テンプレートの更新の影響の確認で、手動の変更の検出ではない。
    - B: 誤り。テンプレートの生成のコマンドである。
    - C: 正しい。
    - D: 誤り。起動の完了を通知するスクリプトである。

    **スキル:** [3.1.2](../domain3.md#skill-3-1-2) / **参照:** [ドリフト検出](../../../services/iac.md#drift)

### 問3 {#q3}

RDS のスタックを削除しても、データを残したいです。またスタックの更新でもデータベースを置き換えさせたくありません。組み合わせとして正しいものはどれですか。

- A. `DeletionPolicy: Snapshot` とスタックポリシー
- B. `CreationPolicy` とロールバックトリガーで、削除と更新の失敗を検知して戻す構成
- C. ネストされたスタックと `Export`
- D. `cfn-signal` と変更セット

??? success "答えと解説"
    **正解: A**

    削除時は `DeletionPolicy`、更新時の保護はスタックポリシーで指定します。

    - A: 正しい。
    - B: 誤り。起動の待機と更新の後の戻しの機能である。
    - C: 誤り。再利用の仕組みで、データの保護ではない。
    - D: 誤り。起動の通知と影響の確認で、削除からの保護ではない。

    **スキル:** [3.1.2](../domain3.md#skill-3-1-2) / **参照:** [リソースの属性: DeletionPolicy](../../../services/iac.md#deletion-policy)、[スタックポリシー](../../../services/iac.md#stack-policy)

### 問4 {#q4}

EC2 のユーザーデータの処理が終わるまでスタックの作成を完了させたくありません。処理が失敗したら、スタックも失敗させたいです。どれを組み合わせますか。

- A. `Export` と `ImportValue` でスタックの間に処理の結果を渡す構成
- B. 変更セットとドリフト検出
- C. `DependsOn` とスタックポリシー
- D. `cfn-signal` と `CreationPolicy`

??? success "答えと解説"
    **正解: D**

    `CreationPolicy` がシグナルを待ち、`cfn-signal` が結果を送ります。

    - A: 誤り。スタックの間での値の受け渡しである。
    - B: 誤り。更新の確認と差分の検出である。
    - C: 誤り。作成の順序と更新の保護で、処理の完了は待たない。
    - D: 正しい。

    **スキル:** [3.1.2](../domain3.md#skill-3-1-2) / **参照:** [ヘルパースクリプト](../../../services/iac.md#cfn-helpers)、[CreationPolicy](../../../services/iac.md#creation-policy)

### 問5 {#q5}

`cdk deploy` がブートストラップのスタックがないという理由で失敗します。新しいリージョンへのデプロイは初めてです。何をしますか。

- A. `cdk diff` を実行し、差分を確認してから `cdk deploy` を再実行する
- B. `cdk synth` を実行して、テンプレートを作り直す
- C. `cdk destroy` を実行してから作り直す
- D. そのリージョンで `cdk bootstrap` を実行する

??? success "答えと解説"
    **正解: D**

    ブートストラップは、デプロイ先のアカウントとリージョンごとに必要です。

    - A: 誤り。差分の確認で、準備のリソースは作らない。
    - B: 誤り。テンプレートの生成で、準備のリソースは作らない。
    - C: 誤り。スタックの削除で、解決にならない。
    - D: 正しい。

    **スキル:** [3.1.2](../domain3.md#skill-3-1-2) / **参照:** [ブートストラップ](../../../services/iac.md#cdk-bootstrap)、[CDK のコマンド](../../../services/iac.md#cdk-cli)

### 問6 {#q6}

CDK のコマンドと用途の組み合わせとして正しいものを選んでください。（2つ選択）

- A. `cdk diff`: アカウントのブートストラップのスタックを作成する
- B. `cdk deploy`: テンプレートを生成するだけで適用はしない
- C. `cdk synth`: CloudFormation テンプレートを生成する
- D. `cdk bootstrap`: スタックを更新して本番へ反映する
- E. `cdk diff`: 現在のスタックとの差分を確認する

??? success "答えと解説"
    **正解: C, E**

    CDK の流れは synth、diff、deploy です。

    - A: 誤り。差分を見るコマンドである。
    - B: 誤り。スタックをデプロイするコマンドである。
    - C: 正しい。
    - D: 誤り。デプロイ先の準備のコマンドである。
    - E: 正しい。

    **スキル:** [3.1.2](../domain3.md#skill-3-1-2) / **参照:** [CDK のコマンド](../../../services/iac.md#cdk-cli)

### 問7 {#q7}

初めて作るスタックが失敗し、`ROLLBACK_COMPLETE` になりました。テンプレートを直して更新しようとしてもできません。どうしますか。

- A. 変更セットで更新する
- B. スタックを削除して作り直す
- C. `continue-update-rollback` を実行し、スタックの状態を戻す
- D. `--resources-to-skip` を指定して更新を再実行する

??? success "答えと解説"
    **正解: B**

    初回の作成に失敗したスタックは更新できません。

    - A: 誤り。この状態のスタックは更新できない。
    - B: 正しい。
    - C: 誤り。`UPDATE_ROLLBACK_FAILED` の対処である。
    - D: 誤り。`continue-update-rollback` の引数で、この状態には使わない。

    **スキル:** [3.1.3](../domain3.md#skill-3-1-3) / **参照:** [ロールバックの既定動作](../../../services/iac.md#stack-rollback)、[よくある失敗と対処](../../../services/iac.md#common-failures)

### 問8 {#q8}

スタックの更新が失敗し、ロールバックも失敗して `UPDATE_ROLLBACK_FAILED` になりました。外部で削除されたリソースが原因です。どう対処しますか。

- A. 原因を直して `continue-update-rollback` を実行する
- B. テンプレートをもう一度アップロードして更新する
- C. スタックの削除だけを行い、他のスタックの参照も消す
- D. ドリフト検出を実行して差分を確認し、状態が自動で `UPDATE_COMPLETE` に直るのを待つ

??? success "答えと解説"
    **正解: A**

    難しければ `--resources-to-skip` で該当のリソースを飛ばせます。

    - A: 正しい。
    - B: 誤り。この状態では更新できない。
    - C: 誤り。スタックを失うことになり、最初の対処として適切ではない。
    - D: 誤り。検出の機能で、状態は直らない。

    **スキル:** [3.1.3](../domain3.md#skill-3-1-3) / **参照:** [よくある失敗と対処](../../../services/iac.md#common-failures)

### 問9 {#q9}

IAM ロールを含むテンプレートをデプロイすると `InsufficientCapabilities` で失敗します。何をしますか。

- A. テンプレートのサイズを減らし、S3 にアップロードする
- B. テンプレートから `Description` のセクションを除く
- C. `CAPABILITY_IAM` などを指定する
- D. 実行者に `iam:PassRole` を追加する

??? success "答えと解説"
    **正解: C**

    IAM リソースを作るテンプレートは、機能の承認が必要です。

    - A: 誤り。サイズの問題ではない。
    - B: 誤り。このエラーと関係がない。
    - C: 正しい。
    - D: 誤り。ロールを渡す権限で、このエラーの対処ではない。

    **スキル:** [3.1.3](../domain3.md#skill-3-1-3) / **参照:** [機能の承認(capabilities)](../../../services/iac.md#capabilities)

### 問10 {#q10}

`/28` のサブネット 2 つに ALB を作ったところ、スケールの途中で IP が足りないというエラーが増えました。どう直しますか。

- A. ALB のアイドルタイムアウトを短くする
- B. サブネットのマスクを `/27` に変更する
- C. ALB のセキュリティグループを 2 つに分けて、ENI の IP の消費を減らす
- D. `/27` 以上のサブネットを作り、ALB をそちらへ移す

??? success "答えと解説"
    **正解: D**

    ALB のサブネットは `/27` 以上で、空き IP が 8 個以上必要です。空きが足りなければセカンダリ CIDR を追加します。

    - A: 誤り。接続の維持の設定で、IP は増えない。
    - B: 誤り。サブネットのサイズは作成後に変えられない。
    - C: 誤り。IP の数に関係がない。
    - D: 正しい。

    **スキル:** [3.1.3](../domain3.md#skill-3-1-3) / **参照:** [VPC の CIDR](../../../services/network-connectivity.md#vpc-cidr)

### 問11 {#q11}

EC2 の起動のエラーと原因の組み合わせとして正しいものを選んでください。（2つ選択）

- A. `InstanceLimitExceeded`: EBS の暗号化キーの権限の不足で、キーポリシーを直す
- B. `InsufficientInstanceCapacity`: クォータの超過で、Service Quotas で引き上げる
- C. `InsufficientInstanceCapacity`: AZ の容量の不足で、別のタイプや AZ を試す
- D. インスタンスがすぐ `terminated` へ変わる症状: 必ずクォータの超過である
- E. `InstanceLimitExceeded`: クォータの超過で、Service Quotas で引き上げる

??? success "答えと解説"
    **正解: C, E**

    クォータと容量のエラーを区別します。

    - A: 誤り。暗号化キーの問題なら `pending` から `terminated` へ変わる症状になる。
    - B: 誤り。引き上げても容量は増えない。
    - C: 正しい。
    - D: 誤り。暗号化キーの権限などが原因である。
    - E: 正しい。

    **スキル:** [3.1.3](../domain3.md#skill-3-1-3) / **参照:** [インスタンスのトラブルシューティング](../../../services/operations.md#instance-troubleshooting)

### 問12 {#q12}

CloudFormation で EC2 インスタンスプロファイルを指定するスタックが、権限のエラーで失敗します。CloudTrail の拒否のメッセージには `iam:PassRole` とあります。何を確認しますか。

- A. 実行者かサービスロールの `iam:PassRole` の許可
- B. スタックの `DeletionPolicy` とスタックポリシーの設定の組み合わせ
- C. インスタンスの詳細モニタリングの設定
- D. バケットのブロックパブリックアクセスの設定

??? success "答えと解説"
    **正解: A**

    ロールを AWS サービスへ渡すときに、`iam:PassRole` が必要です。

    - A: 正しい。
    - B: 誤り。削除の動作の設定で関係がない。
    - C: 誤り。監視の設定で関係がない。
    - D: 誤り。ロールを渡す権限とは関係がない。

    **スキル:** [3.1.3](../domain3.md#skill-3-1-3) / **参照:** [iam:PassRole](../../../services/iam.md#passrole)、[よくある失敗と対処](../../../services/iac.md#common-failures)

### 問13 {#q13}

組織の全アカウントに監査用のロールを展開します。新しいアカウントにも自動で入れたいです。何をどう設定しますか。

- A. ネストされたスタックに全アカウントの ID を記述する
- B. 1 つのスタックを作り、`Export` で全アカウントへ渡す
- C. サービスマネージドの StackSets で自動デプロイを有効にする
- D. セルフマネージドの StackSets で、各アカウントに実行ロールを手で作る

??? success "答えと解説"
    **正解: C**

    サービスマネージドは Organizations と連携し、新しいアカウントへの自動デプロイができます。

    - A: 誤り。ネストは同じアカウントの部品の再利用である。
    - B: 誤り。エクスポートはアカウントをまたげない。
    - C: 正しい。
    - D: 誤り。自動デプロイが使えない。

    **スキル:** [3.1.4](../domain3.md#skill-3-1-4) / **参照:** [StackSets の設定](../../../services/iac.md#stacksets-settings)、[StackSets の運用](../../../services/operations.md#stacksets-operations)

### 問14 {#q14}

StackSets で 100 アカウントに展開します。一度に 10 アカウントずつ処理し、失敗が 2 アカウントを超えたら止めたいです。どの設定の組み合わせですか。

- A. `RegionConcurrencyType` のみ
- B. `MaxConcurrentCount` と `FailureToleranceCount`
- C. `DeletionPolicy` と `CreationPolicy` の 2 つのリソース属性を全リソースに指定する
- D. `MaxConcurrentPercentage` のみ

??? success "答えと解説"
    **正解: B**

    同時に処理する数と、許容する失敗の数を指定します。

    - A: 誤り。リージョンの処理の順序の設定で、件数は決まらない。
    - B: 正しい。
    - C: 誤り。リソースの属性で、展開の制御ではない。
    - D: 誤り。失敗の許容の設定がない。

    **スキル:** [3.1.4](../domain3.md#skill-3-1-4) / **参照:** [StackSets の設定](../../../services/iac.md#stacksets-settings)

### 問15 {#q15}

組織の別のアカウントに、VPC のサブネットを共有します。オーナーと参加者の責任の説明として正しいものを選んでください。（2つ選択）

- A. 共有にはサブネットのコピーが作られ、参加者の VPC に入る
- B. 参加者が共有されたサブネットのルートテーブルを変更する
- C. オーナーがサブネットとルートテーブルを管理する
- D. 参加者は自分のリソースを管理し、その費用を負担する
- E. 組織の内の共有には、必ず招待の承諾が必要である

??? success "答えと解説"
    **正解: C, D**

    AWS RAM はリソースをコピーせずに共有します。

    - A: 誤り。コピーせずに共有する。
    - B: 誤り。オーナーが管理する。
    - C: 正しい。
    - D: 正しい。
    - E: 誤り。組織の共有を有効にしていれば不要である。

    **スキル:** [3.1.4](../domain3.md#skill-3-1-4) / **参照:** [AWS Resource Access Manager](../../../services/governance.md#ram)、[VPC サブネットの共有](../../../services/governance.md#ram-vpc-sharing)

### 問16 {#q16}

次の課題と手段の組み合わせとして正しいものはどれですか。

- A. アカウントの発行と統制: Service Catalog
- B. IP アドレスの一元管理: IPAM（プールを RAM で共有）
- C. 同じテンプレートの全アカウントへの展開: AWS RAM
- D. 承認済みの構成を利用者に選ばせる: Control Tower のコントロール

??? success "答えと解説"
    **正解: B**

    課題ごとにサービスを区別します。

    - A: 誤り。Service Catalog は承認済みの構成を利用者に選ばせるサービスである。
    - B: 正しい。
    - C: 誤り。RAM は共有で、展開は StackSets である。
    - D: 誤り。Control Tower はアカウントの発行と統制である。

    **スキル:** [3.1.4](../domain3.md#skill-3-1-4) / **参照:** [AWS Service Catalog](../../../services/governance.md#service-catalog)、[AWS Control Tower](../../../services/governance.md#control-tower)、[IPAM](../../../services/network-connectivity.md#ipam)

### 問17 {#q17}

チームが Terraform を使い始め、2 人が同時に `apply` して状態ファイルが壊れそうになりました。状態はそれぞれのローカルにあります。どう直しますか。

- A. CloudFormation の変更セットで Terraform の状態を管理するように連携させる
- B. 状態ファイルを Git のリポジトリにコミットし、毎回プルしてから `apply` を実行する
- C. S3 のリモートバックエンドに移し、`use_lockfile = true` にする
- D. 状態ファイルをやめて、`terraform import` を毎回実行するように手順を変更する

??? success "答えと解説"
    **正解: C**

    S3 のネイティブロックは Terraform 1.11 以降で一般提供です。[公式のガイダンス](https://docs.aws.amazon.com/prescriptive-guidance/latest/terraform-aws-provider-best-practices/backend.html)を確認してください。

    - A: 誤り。Terraform の状態の管理の機能ではない。
    - B: 誤り。状態に機密が入ることがあり、ロックもできない。
    - C: 正しい。
    - D: 誤り。既存リソースを取り込むコマンドで、ロックの代わりにならない。

    **スキル:** [3.1.6](../domain3.md#skill-3-1-6) / **参照:** [デプロイ環境でコードリポジトリを使う](../../../services/cicd.md#repositories)、[どれを使うか](../../../services/iac.md#choosing)

### 問18 {#q18}

Terraform のコマンドと用途の組み合わせとして正しいものはどれですか。

- A. `terraform import`: 既存のリソースを管理下に入れる
- B. `terraform init`: 既存のリソースを管理下に入れる
- C. `terraform plan`: 変更をすぐ適用する
- D. `terraform apply`: プロバイダーとバックエンドを準備する

??? success "答えと解説"
    **正解: A**

    順序は init、plan、apply です。

    - A: 正しい。
    - B: 誤り。プロバイダーとバックエンドを準備するコマンドである。
    - C: 誤り。変更の内容を確認するコマンドである。
    - D: 誤り。変更を適用するコマンドである。

    **スキル:** [3.1.6](../domain3.md#skill-3-1-6) / **参照:** [どれを使うか](../../../services/iac.md#choosing)

### 問19 {#q19}

Terraform の状態を保存する S3 バケットの設定として適切なものを選んでください。（2つ選択）

- A. 全員が読めるようにパブリックに公開する
- B. バケットのバージョニングを有効にする
- C. オブジェクトを別のアカウントへレプリケーションで必ず同期する
- D. SSE-KMS で暗号化する
- E. ライフサイクルで状態ファイルを 1 日で削除する

??? success "答えと解説"
    **正解: B, D**

    状態ファイルを保護します。[公式のガイダンス](https://docs.aws.amazon.com/prescriptive-guidance/latest/terraform-aws-provider-best-practices/backend.html)を確認してください。

    - A: 誤り。状態には機密情報が入ることがある。
    - B: 正しい。
    - C: 誤り。必須の設定ではなく、この問いの要点でもない。
    - D: 正しい。
    - E: 誤り。状態を失ってしまう。

    **スキル:** [3.1.6](../domain3.md#skill-3-1-6) / **参照:** [どれを使うか](../../../services/iac.md#choosing)

### 問20 {#q20}

Terraform の定義を Service Catalog の製品にしたいです。正しい説明はどれですか。

- A. Service Catalog は CloudFormation のみ対応で、Terraform の製品は作れない
- B. 製品にすると、CloudFormation のスタックポリシーが自動で適用される
- C. 製品にするには、Terraform の状態ファイルを CodeCommit に置く必要がある
- D. 製品にでき、起動制約を付けて利用者にプロビジョニングさせられる

??? success "答えと解説"
    **正解: D**

    起動制約で、利用者が直接の権限を持たなくても製品を配布できます。[公式の手順](https://docs.aws.amazon.com/servicecatalog/latest/adminguide/getstarted-Terraform.html)を確認してください。

    - A: 誤り。Terraform で定義した構成も製品にできる。
    - B: 誤り。CloudFormation のスタックの機能で、Terraform の製品には関係がない。
    - C: 誤り。製品の条件ではない。
    - D: 正しい。

    **スキル:** [3.1.6](../domain3.md#skill-3-1-6) / **参照:** [AWS Service Catalog](../../../services/governance.md#service-catalog)

### 問21 {#q21}

IaC のコードの管理の説明として正しいものを選んでください。（2つ選択）

- A. テンプレートをリポジトリで管理し、プルリクエストで変更を確認する
- B. CodeCommit は現在も新規利用ができないので、選択肢にならない
- C. テンプレートは本番の担当者のローカルだけに置くのが安全である
- D. リリースの記録にタグを使うことは、Git では想定されていない
- E. CodePipeline などをコミットで起動できる

??? success "答えと解説"
    **正解: A, E**

    テンプレートもコードと同じように管理します。

    - A: 正しい。
    - B: 誤り。2025 年 11 月に一般提供へ戻った。
    - C: 誤り。変更の確認や共有ができない。
    - D: 誤り。タグでリリースを記録する。
    - E: 正しい。

    **スキル:** [3.1.6](../domain3.md#skill-3-1-6) / **参照:** [CodeCommit の現状](../../../services/cicd.md#codecommit-status)、[ブランチとタグでバージョンとリリースを管理する](../../../services/cicd.md#branches-tags)、[リポジトリからの起動](../../../services/cicd.md#pipeline-triggers)
