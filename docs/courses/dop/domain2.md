# 分野2: 構成管理と IaC

配点は **17%** です。IaC による部品化、複数アカウントの統制、大規模な運用の自動化を扱います。

プロフェッショナルでは、どのサービスが「定義」「配布」「検出」「修復」を担うかを切り分ける問題が多く出ます。

この分野に限らず、コース全体で使うサービスは[サービス一覧](services.md)から確認できます。

## タスク 2.1: インフラと再利用できる部品を定義し、ライフサイクルを通じて管理する {#task-2-1}

### IaC の選択肢 {#t2-1-iac-options}

**ガイドの項目:** 知識「AWS の IaC の選択肢とツール」、スキル「IaC テンプレートの作成とデプロイ（SAM、CloudFormation、CDK など）」

| ツール | 書き方 | 向く場面 |
|---|---|---|
| CloudFormation | YAML、JSON | 基本の形。StackSets や Service Catalog と組み合わせる |
| SAM | CloudFormation の拡張 | サーバーレス。`DeploymentPreference` でカナリア |
| CDK | プログラミング言語 | ループや抽象化が欲しい、テストを書きたい |
| AWS CLI、SDK | コマンド、コード | 単発の操作、IaC で表せない処理 |

SAM と CDK は、どちらも最終的に CloudFormation のテンプレートになります。CDK は `cdk bootstrap` で事前の準備が必要です。

テンプレートの機能は次の場面で選びます。

| 要件 | 機能 |
|---|---|
| EC2 の起動完了を待つ | `CreationPolicy` と `cfn-signal` |
| Auto Scaling の更新方法を決める | `UpdatePolicy` |
| CloudFormation が扱えない処理を挟む | カスタムリソース |
| スタック削除でデータを残す | `DeletionPolicy: Retain` または `Snapshot` |

詳細: [どれを使うか](../../services/iac.md#choosing)、[CreationPolicy](../../services/iac.md#creation-policy)、[UpdatePolicy](../../services/iac.md#update-policy)、[カスタムリソース](../../services/iac.md#custom-resources)、[SAM](../../services/iac.md#sam)、[CDK](../../services/iac.md#cdk)

### IaC の変更管理 {#t2-1-change-management}

**ガイドの項目:** 知識「IaC ベースのプラットフォームの変更管理プロセス」

コードレビューの後、影響を確認してから適用します。

| 要件 | 機能 |
|---|---|
| 適用前に差分を確認する | 変更セット、`cdk diff` |
| 重要なリソースの更新を禁止する | スタックポリシー |
| 誤ったスタック削除を防ぐ | 削除保護 |
| 更新後にアラームが鳴れば戻す | ロールバックトリガー |
| 手作業の変更を見つける | ドリフト検出 |

変更セットの確認と承認をパイプラインに組み込む形が定番です。作成のアクション、手動承認、実行のアクションの順に置きます。

**落とし穴:** ドリフト検出は見つけるだけで、直しません。自動で見つけるなら、Config のマネージドルールと組み合わせます。

詳細: [変更セット](../../services/iac.md#change-sets)、[スタックポリシー](../../services/iac.md#stack-policy)、[ロールバックトリガー](../../services/iac.md#rollback-triggers)、[ドリフト検出](../../services/iac.md#drift)、[ドリフトの運用](../../services/operations.md#drift-operations)

### 構成管理のサービスと戦略 {#t2-1-config-management}

**ガイドの項目:** 知識「構成管理のサービスと戦略」、スキル「最適な構成管理サービスの判断（OpsWorks、Systems Manager、AWS Config、AppConfig など）」

名前が似ていても、対象が違います。

| サービス | 対象 | 動き |
|---|---|---|
| Systems Manager | サーバーの中の OS、パッケージ | コマンド、望ましい状態の適用 |
| AWS Config | AWS リソースの設定 | 記録、評価、修復 |
| AppConfig | アプリの設定、機能フラグ | 段階的な配布、アラームでのロールバック |
| OpsWorks | Chef、Puppet で管理するサーバー | レシピの適用 |

**例:** 「設定変更を全サーバーへ段階的に反映し、エラーが増えたら自動で戻す。コードのデプロイはしない」なら AppConfig です。

!!! note "OpsWorks の状況"
    OpsWorks Stacks、Chef Automate、Puppet Enterprise は 2024 年 5 月 1 日に完全に終了しました。ガイドには名前が残っているので、Chef や Puppet による構成管理という役割を押さえます。実際の環境では State Manager や Automation に置き換えます。

詳細: [AppConfig](../../services/secrets.md#appconfig)、[Systems Manager](../../services/operations.md#systems-manager)、[AWS Config](../../services/governance.md#config)、[OpsWorks の状況](../../services/operations.md#opsworks)

### StackSets {#t2-1-stacksets}

**ガイドの項目:** スキル「複数のアカウントとリージョンへの StackSets の適用」

| 権限のモデル | 使う場面 | 特徴 |
|---|---|---|
| サービスマネージド | Organizations を使う | ロールが自動。OU の新しいアカウントへ自動デプロイできる |
| セルフマネージド | 組織外のアカウントがある | 管理ロールと実行ロールを自分で作る |

失敗の扱いは、次の設定で調整します。

| 設定 | 効果 |
|---|---|
| 同時実行の数 | 速さを決める |
| 失敗の許容数 | 超えると操作を止める |
| リージョンの処理順 | 順番、または並列 |

`Failure tolerance` を 0、同時実行を 1 にすると、1 アカウントずつ進んで最初の失敗で止まります。カナリアに近い展開です。

スタックインスタンスが `OUTDATED` なら、対象アカウントの実行ロール、固定名のリソースの衝突、クォータを確認します。

詳細: [StackSets の設定](../../services/iac.md#stacksets-settings)、[StackSets の運用](../../services/operations.md#stacksets-operations)

### 統制を組み込んだ再利用できる部品 {#t2-1-reusable}

**ガイドの項目:** スキル「インフラのパターン、統制、セキュリティ基準を再利用できる IaC テンプレートに組み込む（Service Catalog、CloudFormation モジュール、CDK など）」

| 手段 | 再利用の形 | 向く場面 |
|---|---|---|
| CloudFormation モジュール | テンプレートに部品として入れる | 同じリソース構成を、テンプレートの作者が取り込む |
| ネストされたスタック | 親から別スタックを呼ぶ | 部品を別スタックとして管理する |
| CDK のコンストラクト | ライブラリとして配布 | 開発者がコードから使う。L3 に基準を組み込む |
| Service Catalog | 承認済みの製品をセルフサービスで提供 | 利用者に広い権限を与えない |

**CloudFormation モジュール**は、ベストプラクティスに沿ったリソース構成を部品にする機能です。

- CloudFormation レジストリに登録し、バージョンで管理します。
- 複数のテンプレートとアカウントで使えます。
- 追加料金はなく、解決されたリソースの分だけ費用がかかります。
- スタックのクォータは、モジュールを展開した後のテンプレートに適用されます。
- どのリソースがモジュールから作られたかを追跡できます。

**Service Catalog** では、起動制約が最も重要です。製品を作るときに Service Catalog が引き受けるロールを指定すれば、利用者に EC2 などの権限を与えなくて済みます。テンプレート制約で `InstanceType` の値を限定することもできます。

詳細: [Service Catalog](../../services/governance.md#service-catalog)、[ネストとエクスポートの比較](../../services/iac.md#nested-vs-exports)、[コンストラクト](../../services/iac.md#cdk-constructs)、[CDK のテスト](../../services/iac.md#cdk-testing)

## タスク 2.2: 複数アカウント、複数リージョン環境のアカウントを作成、オンボード、保護する自動化を導入する {#task-2-2}

### アカウント構成とベストプラクティス {#t2-2-structure}

**ガイドの項目:** 知識「AWS アカウントの構成、ベストプラクティス、関連サービス」

アカウントを分けると、影響範囲、権限、費用、クォータを分離できます。

| OU の例 | 用途 |
|---|---|
| Security | ログ保管、セキュリティツール |
| Infrastructure | ネットワークなどの共有基盤 |
| Workloads | アプリの本番と開発 |
| Deployments | パイプライン |
| Sandbox | 個人の実験 |
| Policy Staging | 新しいポリシーの検証 |

管理アカウントでは作業せず、ワークロードも置きません。各サービスの管理は委任管理者に任せます。

詳細: [マルチアカウントのパターン](../../services/governance.md#multi-account-patterns)、[OU の設計](../../services/governance.md#org-ous)、[委任管理者](../../services/governance.md#delegated-admin)

### アカウント発行の標準化と自動化 {#t2-2-provisioning}

**ガイドの項目:** スキル「アカウントのプロビジョニングと設定の標準化、自動化」

| 手段 | 内容 | 向く場面 |
|---|---|---|
| Account Factory | Control Tower の標準の発行 | 基本の形 |
| Account Factory for Terraform | Terraform と Git で発行、カスタマイズ | Terraform を標準にしている |
| Customizations for Control Tower | テンプレートとポリシーを追加で展開 | CloudFormation で標準の設定を足す |
| StackSets の自動デプロイ | OU に入ると自動でスタックを作る | 全アカウントに共通のロールなど |

詳細: [Control Tower](../../services/governance.md#control-tower)、[ドリフトと拡張](../../services/governance.md#ct-drift)

### Organizations と Control Tower {#t2-2-org-ct}

**ガイドの項目:** スキル「アカウントの作成、統合、一元管理（Organizations、Control Tower など）」

| 比較 | Organizations | Control Tower |
|---|---|---|
| 役割 | 組織の仕組み、ポリシー | ランディングゾーンの構築と統制の自動化 |
| 作るもの | OU、アカウント、ポリシー | ログ保管と監査のアカウント、OU、コントロール |
| 向く場面 | 独自の構成を組む | 速く標準の形にしたい |

既存の組織には、Control Tower を後から導入できます。OU を登録すると統制の下に入ります。Control Tower の外で OU や SCP を変更すると、ドリフトになります。

SCP を使うポリシーには、Organizations のすべての機能の有効化が必要です。

詳細: [Organizations](../../services/governance.md#organizations)、[機能セット](../../services/governance.md#org-feature-sets)、[ランディングゾーン](../../services/governance.md#ct-landing-zone)

### 複数アカウントの IAM {#t2-2-iam}

**ガイドの項目:** スキル「複数アカウント、複雑な組織構造の IAM ソリューション適用（SCP、ロールの引き受けなど）」

| 手段 | 効果 |
|---|---|
| SCP | アカウント内の主体の権限の上限を決める。権限は与えない |
| RCP | リソース側の権限の上限を決める |
| ロールの引き受け | 別のアカウントで作業する。外部には `ExternalId` |
| `aws:PrincipalOrgID` | リソースポリシーで自組織に限定 |

- SCP は管理アカウントには効きません。
- サービスリンクロールにも SCP は効きません。
- 別のアカウントのロールを引き受けるには、呼び出し側の許可と、信頼ポリシーの両方が必要です。

詳細: [SCP](../../services/governance.md#scp)、[RCP](../../services/governance.md#rcp)、[クロスアカウントアクセス](../../services/iam.md#cross-account)、[SCP と権限境界の組み合わせ](../../services/identity-directory.md#multi-account-access)、[クロスアカウントの評価](../../services/identity-directory.md#cross-account-evaluation)

### 統制とセキュリティの大規模な導入 {#t2-2-governance}

**ガイドの項目:** スキル「統制とセキュリティコントロールの大規模な実装（AWS Config、Control Tower、Security Hub、Detective、GuardDuty、Service Catalog、SCP）」

それぞれが担う段階を区別します。

| 段階 | サービス | 例 |
|---|---|---|
| 操作を止める | SCP、Control Tower の予防的コントロール | リージョンの制限 |
| 作成前に止める | Control Tower のプロアクティブコントロール（CloudFormation Hooks） | 暗号化なしの作成を拒否 |
| 準拠を検出する | AWS Config、Security Hub CSPM | 公開された S3 の検出 |
| 脅威を検出する | GuardDuty | 認証情報の不正利用 |
| 原因を調べる | Detective | 検出結果の影響範囲 |
| 承認済みの構成を配る | Service Catalog | 標準の VPC |

複数アカウントでは、組織の委任管理者を指定して有効化を自動にします。

| サービス | 組織での展開 |
|---|---|
| Security Hub CSPM | 中央設定で、アカウント、OU、リージョンをまたいで管理 |
| GuardDuty | 委任管理者が組織のアカウントを自動で有効化 |
| Config | 組織ルール、組織の適合パック、アグリゲーター |
| Detective | 行動グラフの管理者が Organizations でメンバーを追加 |

!!! note "Security Hub の名前"
    2025 年 12 月に新しい統合製品の Security Hub が一般提供になり、従来のサービスは Security Hub CSPM という名前になりました。ガイドの「Security Hub」の記述は、主に CSPM の機能に当たります。

詳細: [コントロール](../../services/governance.md#ct-controls)、[Security Hub の組織と集約](../../services/threat-detection.md#security-hub-org)、[GuardDuty の複数アカウント](../../services/threat-detection.md#guardduty-multi-account)、[アグリゲーター](../../services/governance.md#config-aggregators)、[適合パック](../../services/governance.md#config-conformance-packs)、[Detective](../../services/threat-detection.md#detective)、[製品の現在の形](../../services/threat-detection.md#security-hub-products)

## タスク 2.3: 複雑な作業と大規模環境向けの自動化を設計し構築する {#task-2-3}

### 自動化に使うサービス {#t2-3-automation-services}

**ガイドの項目:** 知識「作業とプロセスを自動化する AWS のサービスとソリューション」

| 要件 | サービス |
|---|---|
| AWS API と手順を組み合わせる定型作業 | Systems Manager Automation |
| 分岐、並列、人の承認を含む長い処理 | Step Functions |
| イベントで短い処理を動かす | EventBridge と Lambda |
| 定期実行 | EventBridge のスケジュール |
| サーバー上で一斉に実行 | Run Command |
| 決まった時間帯にだけ実行 | Maintenance Windows |

Automation の複数アカウント、複数リージョンの実行では、レート制御（同時実行数とエラーのしきい値）で影響を抑えます。

詳細: [Automation](../../services/operations.md#automation)、[複数アカウント、複数リージョンの実行](../../services/operations.md#automation-multi-account)、[Maintenance Windows](../../services/operations.md#maintenance-windows)、[EventBridge のスケジュール](../../services/messaging.md#eventbridge-schedule)

### AWS を操作する方法 {#t2-3-interfaces}

**ガイドの項目:** 知識「AWS のソフトウェア定義インフラを操作する方法と戦略」

| 方法 | 向く場面 |
|---|---|
| IaC | 継続して管理する構成 |
| AWS CLI | スクリプトと単発の作業。`--query` と `--dry-run` |
| CloudShell | 手元に環境を作らず、ブラウザから CLI を使う |
| SDK | Lambda などのコードから。ページネーションと再試行を意識 |
| Session Manager | SSH と踏み台なしでサーバーに入る |

詳細: [AWS CLI](../../services/iac.md#aws-cli)、[CloudShell](../../services/iac.md#cloudshell)、[SDK の基本](../../services/sdk-resilience.md#sdk-basics)、[Session Manager](../../services/operations.md#session-manager)

### インベントリ、構成、パッチの自動化 {#t2-3-inventory-patch}

**ガイドの項目:** スキル「システムのインベントリ、構成、パッチ管理の自動化（Systems Manager、AWS Config など）」

| 目的 | サービス | 要点 |
|---|---|---|
| ノードに何が入っているか | Inventory | リソースデータ同期で S3 に集約し、Athena で検索 |
| AWS リソースの設定履歴 | AWS Config | 設定レコーダーとアグリゲーター |
| パッチの適用 | Patch Manager | ベースラインで承認を決める |

組織全体のパッチには、Quick Setup の**パッチポリシー**が推奨です。スキャンと適用を別の日程にでき、パッチグループが要りません。Maintenance Windows のタスクや State Manager は、1 アカウント、1 リージョンが範囲です。

`AWS-RunPatchBaseline` の `Operation` は、`Scan` なら報告だけ、`Install` なら適用です。

前提として、ノードがマネージドノードである必要があります。SSM Agent、インスタンスのロール、Systems Manager への経路の 3 つです。

詳細: [Inventory](../../services/operations.md#inventory)、[Patch Manager](../../services/operations.md#patch-manager)、[実行の設定方法](../../services/operations.md#patch-methods)、[マネージドノードの条件](../../services/operations.md#managed-nodes)

### Lambda と Step Functions の自動化 {#t2-3-lambda}

**ガイドの項目:** スキル「複雑なシナリオの Lambda の自動化（AWS SDK、Lambda、Step Functions など）」

Lambda の上限は 15 分です。長い処理や工程の多い処理は、Step Functions に分けます。

| 要件 | 設計 |
|---|---|
| 全アカウントに同じ操作をする | `Map` 状態で分散し、各アカウントのロールを引き受ける |
| 一時的な失敗に備える | `Retry` と `Catch` |
| 人の承認を待つ | `waitForTaskToken` |
| 再実行で壊れないようにする | 処理を冪等にする |
| API のスロットリングに備える | SDK の再試行、同時実行の制限 |

| 比較 | Standard | Express |
|---|---|---|
| 実行時間 | 最大 1 年 | 最大 5 分 |
| 向く処理 | 長い運用の工程 | 大量の短い処理 |

詳細: [Standard と Express](../../services/step-functions.md#standard-express)、[エラー処理](../../services/step-functions.md#error-handling)、[人の承認](../../services/step-functions.md#human-approval)、[冪等性](../../services/sdk-resilience.md#idempotency)、[再試行](../../services/sdk-resilience.md#retries)

### ソフトウェアの望ましい状態 {#t2-3-desired-state}

**ガイドの項目:** スキル「ソフトウェアの構成を望ましい状態に自動で保つ（OpsWorks、State Manager など）」

State Manager の関連付けで、タグが一致するノードに同じ状態を保ちます。新しいノードが現れると適用されます。別の手順で変更されても、次の実行で元に戻せます。

Ansible プレイブックや Chef レシピも実行できるので、既存の資産を生かして OpsWorks の役割を置き換えられます。

| 比較 | State Manager | Maintenance Windows | Run Command |
|---|---|---|---|
| 目的 | 状態を保ち続ける | 時間帯を決めて実行 | 一度だけ実行 |
| 繰り返し | 定期的 | 定期的 | しない |

詳細: [State Manager](../../services/operations.md#state-manager)、[State Manager と Maintenance Windows の違い](../../services/operations.md#state-vs-maintenance)

### ソフトウェアの準拠の維持 {#t2-3-compliance}

**ガイドの項目:** スキル「ソフトウェアの準拠の維持（Systems Manager など）」

Systems Manager の Compliance は、パッチと関連付けの準拠状況を集めます。

| 要件 | 方法 |
|---|---|
| パッチの不足を報告する | Patch Manager の `Scan` |
| 必須のソフトウェアが動いているか確認する | State Manager の関連付けの準拠 |
| 禁止のソフトウェアを見つける | Inventory と AWS Config の組み合わせ |
| ライセンスの超過を防ぐ | License Manager |
| 全社で確認する | リソースデータ同期、Config のアグリゲーター |

詳細: [パッチベースライン](../../services/operations.md#patch-baselines)、[Inventory](../../services/operations.md#inventory)、[License Manager](../../services/governance.md#license-manager)

## 確認問題 {#self-check}

??? question "問1: セキュリティ担当が、暗号化とログ設定を組み込んだ S3 バケットの定義を作りました。各チームのテンプレートから部品として使わせ、版も管理したいです。別スタックには分けず、アプリのスタックの中に作らせます。何を使いますか？"
    CloudFormation モジュールです。レジストリに登録して版を管理し、テンプレートに部品として入れます。ネストされたスタックは別のスタックになるので、条件に合いません。

??? question "問2: 開発者に EC2 や IAM の権限を与えず、承認済みの構成だけを自分で作らせたいです。インスタンスタイプも限定します。どう構成しますか？"
    Service Catalog の製品として登録し、起動制約で専用のロールを指定します。テンプレート制約で `InstanceType` の値を限定します。利用者は製品を起動する権限だけを持ちます。

??? question "問3: 組織に新しいアカウントが増えるたびに、監査用ロールを自動で作りたいです。最小の運用負荷にするには？"
    サービスマネージド権限の StackSets で、対象の OU に自動デプロイを有効にします。ロールの作成も、新しいアカウントへの展開も自動で行われます。

??? question "問4: Control Tower の環境で、管理者がコンソールから SCP を直接変更した後、警告が出るようになりました。原因と対処は？"
    Control Tower の外での変更によるドリフトです。コンソールで検出した内容に従い、ランディングゾーンの更新や OU の再登録で解消します。

??? question "問5: 10 個のリージョンと 200 アカウントのインスタンスに、スキャンと適用を別の日程でパッチを当てたいです。何を使いますか？"
    Quick Setup のパッチポリシーです。Organizations の複数アカウント、複数リージョンを対象にでき、スキャンと適用の日程も分けられます。Maintenance Windows は 1 アカウント、1 リージョンが範囲なので、展開の手間が増えます。

??? question "問6: 機能フラグの値を変更して全サーバーへ段階的に反映し、エラー率が上がったら自動で戻したいです。コードはデプロイしません。何を使いますか？"
    AppConfig です。デプロイ戦略で段階的に配布し、CloudWatch アラームと連動してロールバックします。Parameter Store には段階的な配布と自動ロールバックがありません。
