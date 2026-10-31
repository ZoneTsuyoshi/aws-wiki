# 分野3: デプロイ、プロビジョニング、自動化

配点は **22%** です。旧版の 18% から増えました。

リソースを作る、配る、失敗を直す、既存のリソースを自動で管理する、の 4 つです。パイプラインの設計は範囲外で、失敗の切り分けと運用が中心です。

## タスク 3.1: クラウドリソースをプロビジョニングし、保守する {#task-3-1}

### 3.1.1 AMI とコンテナイメージ {#skill-3-1-1}

**AMI の操作:**

| 操作 | 注意 |
|---|---|
| 別リージョンで使う | AMI はリージョンごと。`copy-image` でコピーする |
| コピー | 起動許可は引き継がれない |
| 別アカウントへ共有 | 起動許可を付与する |
| 暗号化した AMI の共有 | カスタマー管理キーを使い、共有先にキーの利用を許可する。AWS 管理キーの AMI は共有できない |
| 登録解除 | 起動済みのインスタンスに影響しない。スナップショットは既定で残る |
| 最新の AMI ID の参照 | Parameter Store の公開パラメータ |

**EC2 Image Builder:** AMI とコンテナイメージの作成、テスト、配布を自動化します。

| 構成要素 | 役割 |
|---|---|
| レシピ | ベースイメージとコンポーネントの組み合わせ |
| コンポーネント | 構築とテストの手順 |
| インフラストラクチャ設定 | ビルド用のインスタンスの条件、サブネット、IAM ロール |
| 配布設定 | 別リージョンへのコピー、別アカウントの起動許可、起動テンプレートの更新 |
| パイプライン | スケジュールと実行 |

**ビルドがタイムアウトするとき:** インスタンスのロールに `EC2InstanceProfileForImageBuilder` と `AmazonSSMManagedInstanceCore` があるか確認します。SSM に接続できるネットワークも必要です。

**コンテナイメージ（ECR）:**

| 課題 | 機能 |
|---|---|
| 古いイメージの費用を減らす | ライフサイクルポリシー |
| 同じタグの上書きを防ぐ | 不変タグ |
| 脆弱性の検査 | 基本スキャン、または Inspector の拡張スキャン |
| 別リージョンに置く | レプリケーション |
| `no basic auth credentials` などの認証エラー | `aws ecr get-login-password` でログインする |

詳細: [AMI の管理](../../services/operations.md#amis)、[EC2 Image Builder](../../services/operations.md#image-builder)、[ECR](../../services/containers.md#ecr)、[タグと不変タグ](../../services/containers.md#image-tags)、[ライフサイクルポリシー](../../services/containers.md#ecr-lifecycle)、[イメージスキャン](../../services/containers.md#ecr-scanning)、[レプリケーション](../../services/containers.md#ecr-replication)

### 3.1.2 CloudFormation と CDK {#skill-3-1-2}

**CloudFormation の運用機能:**

| 課題 | 機能 |
|---|---|
| 更新の影響を事前に確認する | 変更セット |
| 手動の変更を見つける | ドリフト検出 |
| 重要なリソースの更新を防ぐ | スタックポリシー |
| スタックの削除でデータを残す | `DeletionPolicy: Retain` または `Snapshot` |
| アラームが鳴ったら戻す | ロールバックトリガー |
| 共通の部品を再利用する | ネストされたスタック |
| 別のチームのスタックの値を使う | `Export` と `ImportValue` |
| EC2 の起動完了を待つ | `cfn-signal` と `CreationPolicy` |

**CDK の流れ:** コードを書き、`cdk synth` で CloudFormation テンプレートを作り、`cdk diff` で差分を確認し、`cdk deploy` で適用します。

| コマンド | 用途 |
|---|---|
| `cdk bootstrap` | デプロイ先のアカウントとリージョンに、必要なリソースを準備する |
| `cdk synth` | テンプレートを生成する |
| `cdk diff` | 現在との差分を見る |
| `cdk deploy` | スタックをデプロイする |

**例:** `cdk deploy` が、ブートストラップのスタックがないという理由で失敗します。リージョンごとに `cdk bootstrap` を実行します。

詳細: [どれを使うか](../../services/iac.md#choosing)、[テンプレート](../../services/iac.md#cloudformation-template)、[変更セット](../../services/iac.md#change-sets)、[スタックポリシー](../../services/iac.md#stack-policy)、[ドリフト検出](../../services/iac.md#drift)、[DeletionPolicy](../../services/iac.md#deletion-policy)、[ロールバックトリガー](../../services/iac.md#rollback-triggers)、[ヘルパースクリプト](../../services/iac.md#cfn-helpers)、[CDK](../../services/iac.md#cdk)、[CDK のコマンド](../../services/iac.md#cdk-cli)、[ブートストラップ](../../services/iac.md#cdk-bootstrap)

### 3.1.3 デプロイの問題の特定と修復 {#skill-3-1-3}

スタックイベントで、**最初に**失敗したリソースの理由を読みます。後の失敗はその連鎖であることが多いためです。

**CloudFormation のエラー:**

| 症状 | 対処 |
|---|---|
| `UPDATE_ROLLBACK_FAILED` | 原因を直して `continue-update-rollback`。難しければ `--resources-to-skip` |
| `ROLLBACK_COMPLETE` で更新できない | 初回の作成の失敗。スタックを削除して作り直す |
| `InsufficientCapabilities` | `CAPABILITY_IAM` などを指定する |
| `DELETE_FAILED` | S3 バケットが空でない、依存が残っている。`--retain-resources` も使える |
| エクスポートを消せない | 参照側のスタックを先に更新する |
| `already exists` | 固定の名前が衝突。自動生成に任せる |

**サブネットのサイズ:**

サブネットごとに 5 個の IP は使えません。先頭 4 個と最後の 1 個です。`/28` なら、使えるのは 11 個です。

| 対象 | 必要なもの |
|---|---|
| ALB | サブネットは `/27` 以上で、空き IP が 8 個以上 |
| Auto Scaling、ECS、VPC 接続の Lambda | 台数やタスクの数に応じた空き IP |
| 空きが足りない VPC | セカンダリ CIDR を追加して、新しいサブネットを作る |

サブネットのサイズは作成後に変えられません。

**権限の問題:**

| 症状 | 確認すること |
|---|---|
| ロールを渡せない | `iam:PassRole` |
| CloudFormation の操作が拒否される | サービスロールか実行者の権限。SCP の拒否 |
| EC2 が `pending` から `terminated` へ | EBS の暗号化キーの権限 |
| StackSets がアカウントで失敗する | 実行ロールの有無 |

**その他の容量と上限:** `InstanceLimitExceeded` はクォータの問題で、Service Quotas で引き上げます。`InsufficientInstanceCapacity` は AZ の容量の問題で、別のタイプや AZ を試します。

ALB のサブネットの条件は公式ドキュメントで確認して書いています。

詳細: [ロールバックの既定動作](../../services/iac.md#stack-rollback)、[よくある失敗と対処](../../services/iac.md#common-failures)、[機能の承認](../../services/iac.md#capabilities)、[VPC の CIDR](../../services/network-connectivity.md#vpc-cidr)、[iam:PassRole](../../services/iam.md#passrole)、[インスタンスのトラブルシューティング](../../services/operations.md#instance-troubleshooting)、[デプロイ失敗の診断](../../services/cicd.md#troubleshooting-deployments)。公式: [ALB のサブネット](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/application-load-balancers.html)

### 3.1.4 複数リージョンと複数アカウントへの展開 {#skill-3-1-4}

| 課題 | 手段 |
|---|---|
| 同じテンプレートを全アカウントに展開する | CloudFormation StackSets |
| リソースをコピーせず共有する | AWS RAM |
| 承認済みの構成を利用者に選ばせる | Service Catalog |
| アカウントの発行と統制 | Control Tower |
| IP アドレスの一元管理 | IPAM（プールを RAM で共有） |

**StackSets の権限:**

| 方式 | 内容 |
|---|---|
| セルフマネージド | `AWSCloudFormationStackSetAdministrationRole` と `AWSCloudFormationStackSetExecutionRole` を自分で作る |
| サービスマネージド | Organizations と連携。ロールは自動。新しいアカウントへの自動デプロイが可能 |

| 設定 | 内容 |
|---|---|
| `MaxConcurrentCount`、`MaxConcurrentPercentage` | 同時に処理するアカウントの数 |
| `FailureToleranceCount`、`FailureTolerancePercentage` | 許容する失敗の数 |
| `RegionConcurrencyType` | リージョンを順に、または並列に処理 |

**AWS RAM:** VPC サブネット、Transit Gateway、Route 53 Resolver ルール、プレフィックスリスト、IPAM プールなどを共有できます。

| 共有先 | 招待 |
|---|---|
| 組織、OU、組織内のアカウント | 組織の共有を有効にしていれば不要 |
| 組織外のアカウント | 必要 |

**VPC サブネットの共有:** オーナーがサブネットとルートテーブルを管理し、参加者は自分のリソースを管理して費用を負担します。

詳細: [StackSets の設定](../../services/iac.md#stacksets-settings)、[StackSets の運用](../../services/operations.md#stacksets-operations)、[ドリフトの運用](../../services/operations.md#drift-operations)、[AWS RAM](../../services/governance.md#ram)、[VPC サブネットの共有](../../services/governance.md#ram-vpc-sharing)、[Service Catalog](../../services/governance.md#service-catalog)、[Control Tower](../../services/governance.md#control-tower)、[IPAM](../../services/network-connectivity.md#ipam)

### 3.1.5 デプロイ戦略とサービス {#skill-3-1-5}

| 戦略 | 動き | ダウンタイム | 戻しやすさ | 追加コスト |
|---|---|---|---|---|
| 一括 | すべてを同時に更新 | ありうる | 再デプロイが必要 | なし |
| ローリング | 少しずつ順に更新 | なし（容量は一時的に減る） | 再度ローリング | なし、または少し |
| Blue/Green | 別環境を用意して切り替え | ほぼなし | 切り戻すだけ | 2 環境分の期間がある |
| カナリア | 一部へ流して確認後に残りを移す | なし | トラフィックを戻すだけ | 新旧の同時稼働 |

**運用で使う実現方法:**

| 対象 | 手段 |
|---|---|
| EC2 の Auto Scaling グループ | インスタンスの更新（ローリング、最小正常割合の既定は 90%） |
| ECS | ローリング、Blue/Green、カナリア、線形 |
| EC2、Lambda、ECS | CodeDeploy |
| Elastic Beanstalk | 一括、ローリング、追加バッチ、イミュータブル、トラフィック分割 |
| Route 53 | 加重ルーティングで割合を変える |
| Global Accelerator | トラフィックダイヤル |

**インスタンスの更新の落とし穴:** 自動ロールバックを使うときは、起動テンプレートに `$Latest` や `$Default` を指定しません。バージョンを明示します。

詳細: [デプロイ戦略の比較](../../services/cicd.md#deployment-strategies)、[ロールバックの方法](../../services/cicd.md#rollback)、[インスタンスの更新](../../services/operations.md#instance-refresh)、[ECS のデプロイ](../../services/containers.md#ecs-deployments)、[CodeDeploy](../../services/cicd.md#codedeploy)、[Beanstalk のデプロイポリシー](../../services/ec2-beanstalk.md#deployment-policies)

### 3.1.6 サードパーティのツール {#skill-3-1-6}

**Terraform:** HashiCorp の IaC ツールです。AWS Provider で AWS のリソースを管理します。

| コマンド | 用途 |
|---|---|
| `terraform init` | プロバイダーとバックエンドを準備する |
| `terraform plan` | 変更内容を確認する |
| `terraform apply` | 変更を適用する |
| `terraform import` | 既存のリソースを管理下に入れる |

**状態ファイルの管理:**

| 項目 | 推奨 |
|---|---|
| 置き場所 | S3 のリモートバックエンド。ローカルに置かない |
| 同時実行の防止 | S3 のネイティブロック（`use_lockfile = true`）。Terraform 1.11 以降で一般提供 |
| 保護 | バケットのバージョニング、SSE-KMS の暗号化 |
| 機密情報 | 状態ファイルに平文で入らないようにする |

ロック中に別の実行を始めると、`Error acquiring the state lock` で失敗します。

**CloudFormation との違い:** CloudFormation は状態を AWS が管理します。Terraform は状態ファイルを自分で管理します。

**Git:** テンプレートやコードをリポジトリで管理し、ブランチとプルリクエストで変更を確認します。タグでリリースを記録します。CodePipeline などをコミットで起動できます。

**Service Catalog:** Terraform で定義した構成も製品にできます。ただしテンプレート制約と TagOption は使えません。

!!! note "CodeCommit の状況"
    CodeCommit は 2024 年に新規受付を止めましたが、2025 年 11 月に一般提供へ戻りました。古い教材の「新規利用できない」という説明は古くなっています。

Terraform の項目は AWS の規範ガイダンスで確認して書いています。

詳細: [リポジトリ](../../services/cicd.md#repositories)、[CodeCommit の現状](../../services/cicd.md#codecommit-status)、[ブランチとタグ](../../services/cicd.md#branches-tags)、[リポジトリからの起動](../../services/cicd.md#pipeline-triggers)、[Service Catalog](../../services/governance.md#service-catalog)。公式: [Terraform AWS Provider のベストプラクティス](https://docs.aws.amazon.com/prescriptive-guidance/latest/terraform-aws-provider-best-practices/introduction.html)、[バックエンド](https://docs.aws.amazon.com/prescriptive-guidance/latest/terraform-aws-provider-best-practices/backend.html)

## タスク 3.2: 既存のリソースの管理を自動化する {#task-3-2}

### 3.2.1 Systems Manager による運用の自動化 {#skill-3-2-1}

| やりたいこと | 機能 |
|---|---|
| 全ノードで一度コマンドを実行 | Run Command |
| SSH や踏み台なしでログインし、記録を残す | Session Manager |
| OS のパッチを当て、準拠状況を見る | Patch Manager |
| API を含む複数の手順を自動化 | Automation |
| 望ましい状態を保ち続ける | State Manager |
| 業務時間外に限って実行 | Maintenance Windows |
| ソフトウェアの一覧を集める | Inventory |
| 運用の課題を一か所で追う | OpsCenter |

**マネージドノードの条件:** 次の 3 つが揃わないと、ノードが一覧に出ません。

1. SSM Agent が動いています。
2. ロールに `AmazonSSMManagedInstanceCore` があります。
3. SSM のエンドポイントへ経路があります（NAT、または VPC エンドポイント）。

**State Manager と Maintenance Windows:** 新しいノードにも自動で構成を当てるなら State Manager です。土曜の深夜だけパッチを当てるなら Maintenance Windows です。

**Patch Manager の落とし穴:** 定義済みのベースラインは、多くの OS でリリースから 7 日待ちます。7 日以内に当てるなら、カスタムのベースラインを作ります。組織全体を 1 か所で設定するなら、Quick Setup のパッチポリシーです。

**Session Manager の落とし穴:** ポート転送のセッションの内容は、ログに残せません。

!!! note "Systems Manager の機能の状況"
    Change Manager と Incident Manager は 2025年11月7日に新規受付を終了しました。Application Manager はメンテナンスに移行しています。

詳細: [Systems Manager](../../services/operations.md#systems-manager)、[マネージドノード](../../services/operations.md#managed-nodes)、[Run Command](../../services/operations.md#run-command)、[Session Manager](../../services/operations.md#session-manager)、[Patch Manager](../../services/operations.md#patch-manager)、[State Manager](../../services/operations.md#state-manager)、[Maintenance Windows](../../services/operations.md#maintenance-windows)、[両者の違い](../../services/operations.md#state-vs-maintenance)、[Inventory](../../services/operations.md#inventory)、[OpsCenter](../../services/operations.md#opscenter)、[Incident Manager と Change Manager の状況](../../services/operations.md#incident-manager)

### 3.2.2 イベント駆動の自動化 {#skill-3-2-2}

| きっかけ | 仕組み | 例 |
|---|---|---|
| オブジェクトの作成 | S3 Event Notifications から Lambda | アップロードした画像を処理する |
| AWS API の呼び出し | CloudTrail 経由で EventBridge | SG の変更を元に戻す |
| 状態の変化 | EventBridge | インスタンスの停止を通知する |
| 定期実行 | EventBridge のスケジュール | 夜間に開発環境を止める |
| 複数手順の処理 | Step Functions | 修復の手順を順に実行する |
| インシデントの発生 | AWS DevOps Agent | アラートから調査を始める |

**S3 Event Notifications と EventBridge:**

| 観点 | Event Notifications | EventBridge 経由 |
|---|---|---|
| 送信先 | Lambda、SNS、SQS（FIFO は不可） | ルールの多くのターゲット、FIFO も可 |
| 絞り込み | プレフィックスとサフィックス | イベントパターンで細かく |
| 有効化 | 宛先ごとに設定 | バケットで有効にすると全イベントが送られる |

**Lambda を動かす権限:** S3 と EventBridge は、Lambda のリソースベースポリシーで許可します。実行ロールではありません。実行ロールは、関数が他のサービスを呼ぶための権限です。

**例:** 開発環境の EC2 を毎晩止めます。EventBridge のスケジュールで、Automation の `AWS-StopEC2Instance` を対象のタグに対して実行します。

詳細: [S3 イベント通知](../../services/messaging.md#s3-events)、[Event Notifications](../../services/s3.md#event-notifications)、[EventBridge](../../services/messaging.md#eventbridge)、[スケジュール](../../services/messaging.md#eventbridge-schedule)、[EventBridge による修復](../../services/operations.md#eventbridge-remediation)、[DevOps Agent](../../services/operations.md#devops-agent)、[Lambda の実行ロール](../../services/iam.md#lambda-execution-role)

## 確認問題 {#self-check}

??? question "問1: 初めて作るスタックが失敗し、`ROLLBACK_COMPLETE` になりました。テンプレートを直して更新しようとしても、できません。どうしますか？"
    スタックを削除し、直したテンプレートで作り直します。初回の作成に失敗したスタックは更新できません。原因は、スタックイベントで最初に失敗したリソースの理由を確認します。

??? question "問2: 組織の全アカウントに、監査用のロールを展開します。新しく作るアカウントにも自動で入れたいです。何をどう設定しますか？"
    CloudFormation StackSets をサービスマネージド権限で作り、自動デプロイを有効にして対象の OU を指定します。セルフマネージド権限では、各アカウントにロールを用意する手間があり、自動デプロイも使えません。

??? question "問3: `/28` のサブネット 2 つに ALB を作ったところ、スケールの途中で IP が足りないというエラーが増えました。どう直しますか？"
    ALB のサブネットは `/27` 以上で、空き IP が 8 個以上必要です。`/28` で使える IP は 11 個しかありません。サブネットのサイズは変えられないので、セカンダリ CIDR などで大きなサブネットを作り、ALB をそちらに移します。

??? question "問4: 新しく作ったプライベートサブネットの EC2 が、Systems Manager のフリートに表示されません。ロールは正しく付いています。何を確認しますか？"
    SSM のエンドポイントへの経路を確認します。NAT ゲートウェイか、`ssm`、`ssmmessages`、`ec2messages` のインターフェイス型 VPC エンドポイントが必要です。あわせて SSM Agent が動いていることも確認します。

??? question "問5: EC2 Image Builder のパイプラインが、ビルドのステップでタイムアウトして失敗します。コンポーネントの内容は正しいです。最初に何を確認しますか？"
    インフラストラクチャ設定の IAM ロールに `EC2InstanceProfileForImageBuilder` と `AmazonSSMManagedInstanceCore` があるか、ビルド用インスタンスが SSM に接続できるネットワークかを確認します。

??? question "問6: チームが Terraform を使い始め、2 人が同時に `apply` して状態ファイルが壊れそうになりました。状態ファイルはそれぞれのローカルにあります。どう直しますか？"
    状態ファイルを S3 のリモートバックエンドに移し、`use_lockfile = true` で S3 のネイティブロックを有効にします。バケットのバージョニングと暗号化も有効にします。同時に実行すると、片方はロックのエラーで止まります。
