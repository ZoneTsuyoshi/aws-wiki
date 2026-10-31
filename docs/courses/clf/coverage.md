# スキル対応表

公式試験ガイドの全項目と、このコースの見出しの対応です。項目名は日本語で要約しています。正確な文言は[試験ガイド](https://docs.aws.amazon.com/aws-certification/latest/cloud-practitioner-02/cloud-practitioner-02.html)で確認してください。

ガイドの項目には番号がありません。各タスクの「知識（Knowledge of）」と「スキル（Skills in）」を、ガイドの順に並べています。全19タスク、135項目です。

## 分野1: クラウドの概念（18項目） {#domain1}

| タスク | 区分 | 項目 | 見出し |
|---|---|---|---|
| [1.1](domain1.md#task-1-1) | 知識 | AWS クラウドの価値 | [AWS クラウドの価値](domain1.md#t1-1-value) |
| 1.1 | スキル | グローバルインフラの利点（展開の速さ、世界展開） | [グローバルインフラの利点](domain1.md#t1-1-global) |
| 1.1 | スキル | 高可用性、弾力性、俊敏性の利点 | [高可用性、弾力性、俊敏性](domain1.md#t1-1-ha-elastic-agile) |
| [1.2](domain1.md#task-1-2) | 知識 | Well-Architected Framework | [Well-Architected Framework](domain1.md#t1-2-wa-framework) |
| 1.2 | スキル | 6 つの柱の理解 | [6 つの柱](domain1.md#t1-2-pillars) |
| 1.2 | スキル | 柱の違いの判別 | [柱の違いの見分け方](domain1.md#t1-2-pillar-differences) |
| [1.3](domain1.md#task-1-3) | 知識 | クラウド導入の戦略 | [クラウド導入の戦略](domain1.md#t1-3-adoption-strategies) |
| 1.3 | 知識 | 移行を支える情報源 | [移行を支える情報源とプログラム](domain1.md#t1-3-resources) |
| 1.3 | スキル | AWS CAF の構成要素（リスク低減、ESG、収益、運用効率） | [AWS CAF の成果とパースペクティブ](domain1.md#t1-3-caf) |
| 1.3 | スキル | 適切な移行戦略の判別（データベースのレプリケーションなど） | [移行の戦略](domain1.md#t1-3-migration-strategies) |
| [1.4](domain1.md#task-1-4) | 知識 | クラウドの経済性の要素 | [経済性の見方と節約の要素](domain1.md#t1-4-economics) |
| 1.4 | 知識 | 移行による費用の節約 | [経済性の見方と節約の要素](domain1.md#t1-4-economics) |
| 1.4 | スキル | 固定費と変動費 | [固定費と変動費](domain1.md#t1-4-fixed-variable) |
| 1.4 | スキル | オンプレミスにかかる費用 | [オンプレミスにかかる費用](domain1.md#t1-4-onprem-costs) |
| 1.4 | スキル | ライセンスの方式（BYOL とライセンス込み） | [ライセンスの持ち込みとライセンス込み](domain1.md#t1-4-licensing) |
| 1.4 | スキル | 適正サイズ | [適正サイズ](domain1.md#t1-4-rightsizing) |
| 1.4 | スキル | 自動化の利点 | [自動化の利点](domain1.md#t1-4-automation) |
| 1.4 | スキル | 規模の経済 | [規模の経済](domain1.md#t1-4-scale) |

## 分野2: セキュリティとコンプライアンス（31項目） {#domain2}

| タスク | 区分 | 項目 | 見出し |
|---|---|---|---|
| [2.1](domain2.md#task-2-1) | 知識 | 責任共有モデル | [モデルの全体像](domain2.md#t2-1-model) |
| 2.1 | スキル | モデルの構成要素の理解 | [モデルの全体像](domain2.md#t2-1-model) |
| 2.1 | スキル | 利用者の責任 | [利用者の責任](domain2.md#t2-1-customer) |
| 2.1 | スキル | AWS の責任 | [AWS の責任](domain2.md#t2-1-aws) |
| 2.1 | スキル | 共有する責任 | [共有する責任](domain2.md#t2-1-shared) |
| 2.1 | スキル | サービスによる責任の変化（RDS、Lambda、EC2） | [サービスによる責任の変化](domain2.md#t2-1-by-service) |
| [2.2](domain2.md#task-2-2) | 知識 | コンプライアンスとガバナンスの概念 | [コンプライアンスとガバナンスの考え方](domain2.md#t2-2-concepts) |
| 2.2 | 知識 | クラウドセキュリティの利点（暗号化など） | [暗号化の利点と選択肢](domain2.md#t2-2-encryption) |
| 2.2 | 知識 | セキュリティのログを取得する場所 | [セキュリティのログを取る場所](domain2.md#t2-2-logs) |
| 2.2 | スキル | コンプライアンス情報の入手先（Artifact） | [コンプライアンス情報の入手先](domain2.md#t2-2-compliance-info) |
| 2.2 | スキル | 地域や業界で異なる要件 | [地域や業界で異なる要件](domain2.md#t2-2-regions-industries) |
| 2.2 | スキル | リソースの保護（Inspector、Security Hub、GuardDuty、Shield） | [リソースを守るサービス](domain2.md#t2-2-securing) |
| 2.2 | スキル | 暗号化の選択肢（転送時、保存時） | [暗号化の利点と選択肢](domain2.md#t2-2-encryption) |
| 2.2 | スキル | ガバナンスを助けるサービス（CloudWatch、CloudTrail、Config、アクセスレポート） | [ガバナンスとコンプライアンスを助けるサービス](domain2.md#t2-2-governance-services) |
| 2.2 | スキル | サービスで異なる準拠の要件 | [サービスで異なる準拠の範囲](domain2.md#t2-2-service-variance) |
| [2.3](domain2.md#task-2-3) | 知識 | ID とアクセスの管理（IAM） | [IAM の要素](domain2.md#t2-3-iam) |
| 2.3 | 知識 | ルートユーザーの保護の重要性 | [ルートユーザーの保護](domain2.md#t2-3-root) |
| 2.3 | 知識 | 最小権限の原則 | [最小権限とポリシーの種類](domain2.md#t2-3-least-privilege) |
| 2.3 | 知識 | IAM Identity Center | [IAM Identity Center](domain2.md#t2-3-identity-center) |
| 2.3 | スキル | アクセスキー、パスワードポリシー、認証情報の保管 | [アクセスキー、パスワードポリシー、認証情報の保管](domain2.md#t2-3-credentials) |
| 2.3 | スキル | 認証の方法（MFA、Identity Center、クロスアカウントロール） | [認証の方法](domain2.md#t2-3-authentication) |
| 2.3 | スキル | 最小権限に沿ったグループ、ユーザー、カスタムポリシー、管理ポリシー | [IAM の要素](domain2.md#t2-3-iam)、[最小権限とポリシーの種類](domain2.md#t2-3-least-privilege) |
| 2.3 | スキル | ルートユーザーだけができる作業 | [ルートユーザーだけができる作業](domain2.md#t2-3-root-tasks) |
| 2.3 | スキル | ルートユーザーを保護する方法 | [ルートユーザーの保護](domain2.md#t2-3-root) |
| 2.3 | スキル | ID 管理の種類（フェデレーションなど） | [ID 管理の種類](domain2.md#t2-3-federation) |
| [2.4](domain2.md#task-2-4) | 知識 | AWS のセキュリティ機能 | [AWS のセキュリティ機能とサービス](domain2.md#t2-4-capabilities) |
| 2.4 | 知識 | AWS のセキュリティ文書 | [セキュリティの情報源](domain2.md#t2-4-docs) |
| 2.4 | スキル | セキュリティ機能とサービス（WAF、Firewall Manager、Shield、GuardDuty） | [AWS のセキュリティ機能とサービス](domain2.md#t2-4-capabilities) |
| 2.4 | スキル | Marketplace のサードパーティのセキュリティ製品 | [Marketplace のセキュリティ製品](domain2.md#t2-4-marketplace) |
| 2.4 | スキル | セキュリティ情報の入手先（Knowledge Center、Security Center、Security Blog） | [セキュリティの情報源](domain2.md#t2-4-docs) |
| 2.4 | スキル | 問題を見つけるサービス（Trusted Advisor） | [問題を見つけるサービス](domain2.md#t2-4-trusted-advisor) |

## 分野3: クラウドのテクノロジーとサービス（58項目） {#domain3}

| タスク | 区分 | 項目 | 見出し |
|---|---|---|---|
| [3.1](domain3.md#task-3-1) | 知識 | プロビジョニングと運用の方法 | [プロビジョニングと運用の方法](domain3.md#t3-1-provisioning)、[運用を支えるサービス](domain3.md#t3-1-operating-tools) |
| 3.1 | 知識 | AWS へのアクセス方法 | [AWS へのアクセス方法](domain3.md#t3-1-access) |
| 3.1 | 知識 | デプロイモデルの種類 | [デプロイモデル](domain3.md#t3-1-deployment-models) |
| 3.1 | スキル | API、SDK、CLI、コンソール、IaC の選択 | [AWS へのアクセス方法](domain3.md#t3-1-access) |
| 3.1 | スキル | 一度きりか繰り返しかの判断 | [一度きりか、繰り返しか](domain3.md#t3-1-one-time-repeatable) |
| 3.1 | スキル | デプロイモデルの判別（クラウド、ハイブリッド、オンプレミス） | [デプロイモデル](domain3.md#t3-1-deployment-models) |
| [3.2](domain3.md#task-3-2) | 知識 | リージョン、AZ、エッジロケーション | [リージョン、AZ、エッジロケーションの関係](domain3.md#t3-2-components) |
| 3.2 | 知識 | 高可用性 | [複数 AZ による高可用性](domain3.md#t3-2-ha) |
| 3.2 | 知識 | 複数リージョンの利用 | [複数リージョンを使う場面](domain3.md#t3-2-multi-region) |
| 3.2 | 知識 | エッジロケーションの利点 | [エッジロケーションの利点](domain3.md#t3-2-edge) |
| 3.2 | スキル | リージョン、AZ、エッジロケーションの関係 | [リージョン、AZ、エッジロケーションの関係](domain3.md#t3-2-components) |
| 3.2 | スキル | 複数 AZ で高可用性を実現する方法 | [複数 AZ による高可用性](domain3.md#t3-2-ha) |
| 3.2 | スキル | AZ は単一障害点を共有しない | [AZ は単一障害点を共有しない](domain3.md#t3-2-az-isolation) |
| 3.2 | スキル | 複数リージョンを使う場面（災害復旧、事業継続、低遅延、データ主権） | [複数リージョンを使う場面](domain3.md#t3-2-multi-region) |
| [3.3](domain3.md#task-3-3) | 知識 | コンピューティングサービス | [コンピューティングの全体像](domain3.md#t3-3-overview) |
| 3.3 | スキル | EC2 インスタンスタイプの使い分け | [EC2 のインスタンスタイプ](domain3.md#t3-3-instance-types) |
| 3.3 | スキル | コンテナの選択肢（ECS、EKS） | [コンテナの選択肢](domain3.md#t3-3-containers) |
| 3.3 | スキル | サーバーレスの選択肢（Fargate、Lambda） | [サーバーレスの選択肢](domain3.md#t3-3-serverless) |
| 3.3 | スキル | Auto Scaling と弾力性 | [Auto Scaling と弾力性](domain3.md#t3-3-auto-scaling) |
| 3.3 | スキル | ロードバランサーの目的 | [ロードバランサーの目的](domain3.md#t3-3-load-balancers) |
| [3.4](domain3.md#task-3-4) | 知識 | データベースサービス | [データベースの全体像](domain3.md#t3-4-overview) |
| 3.4 | 知識 | データベースの移行 | [データベースの移行ツール](domain3.md#t3-4-migration) |
| 3.4 | スキル | EC2 上の DB かマネージド DB か | [EC2 上の DB かマネージド DB か](domain3.md#t3-4-ec2-vs-managed) |
| 3.4 | スキル | リレーショナルデータベース（RDS、Aurora） | [リレーショナルデータベース](domain3.md#t3-4-relational) |
| 3.4 | スキル | NoSQL データベース（DynamoDB） | [NoSQL データベース](domain3.md#t3-4-nosql) |
| 3.4 | スキル | メモリベースのデータベース（ElastiCache） | [メモリベースのデータベース](domain3.md#t3-4-memory) |
| 3.4 | スキル | データベースの移行ツール（DMS、SCT） | [データベースの移行ツール](domain3.md#t3-4-migration) |
| [3.5](domain3.md#task-3-5) | 知識 | ネットワークサービス | [ネットワークの全体像](domain3.md#t3-5-overview) |
| 3.5 | スキル | VPC の構成要素（サブネット、ゲートウェイ） | [VPC の構成要素](domain3.md#t3-5-vpc) |
| 3.5 | スキル | VPC のセキュリティ（ネットワーク ACL、セキュリティグループ、Inspector） | [VPC のセキュリティ](domain3.md#t3-5-vpc-security) |
| 3.5 | スキル | Route 53 の目的 | [Route 53 の目的](domain3.md#t3-5-route53) |
| 3.5 | スキル | AWS への接続方法（VPN、Direct Connect） | [AWS への接続方法](domain3.md#t3-5-connectivity) |
| [3.6](domain3.md#task-3-6) | 知識 | ストレージサービス | [ストレージの全体像](domain3.md#t3-6-overview) |
| 3.6 | スキル | オブジェクトストレージの用途 | [オブジェクトストレージの用途](domain3.md#t3-6-object) |
| 3.6 | スキル | S3 ストレージクラスの違い | [S3 のストレージクラス](domain3.md#t3-6-s3-classes) |
| 3.6 | スキル | ブロックストレージ（EBS、インスタンスストア） | [ブロックストレージ](domain3.md#t3-6-block) |
| 3.6 | スキル | ファイルサービス（EFS、FSx） | [ファイルサービス](domain3.md#t3-6-file) |
| 3.6 | スキル | キャッシュ付きのファイルシステム（Storage Gateway） | [キャッシュ付きのファイルシステム](domain3.md#t3-6-cached) |
| 3.6 | スキル | ライフサイクルポリシーの用途 | [ライフサイクルポリシーの用途](domain3.md#t3-6-lifecycle) |
| 3.6 | スキル | AWS Backup の用途 | [AWS Backup の用途](domain3.md#t3-6-backup) |
| [3.7](domain3.md#task-3-7) | 知識 | AI/ML のサービス | [AI/ML のサービス](domain3.md#t3-7-ai-ml) |
| 3.7 | 知識 | 分析のサービス | [分析のサービス](domain3.md#t3-7-analytics) |
| 3.7 | スキル | AI/ML のサービスとタスク（SageMaker AI、Lex） | [AI/ML のサービス](domain3.md#t3-7-ai-ml) |
| 3.7 | スキル | データ分析のサービス（Athena、Kinesis、Glue、Quick） | [分析のサービス](domain3.md#t3-7-analytics) |
| [3.8](domain3.md#task-3-8) | 知識 | アプリケーション統合（EventBridge、SNS、SQS） | [メッセージと通知のサービス](domain3.md#t3-8-integration) |
| 3.8 | 知識 | 業務アプリケーション（Connect、SES） | [業務アプリケーション](domain3.md#t3-8-business) |
| 3.8 | 知識 | 顧客支援（AWS Support） | [顧客支援のサービス](domain3.md#t3-8-enablement) |
| 3.8 | 知識 | 開発ツール（CodeBuild、CodePipeline、X-Ray） | [開発ツール](domain3.md#t3-8-developer) |
| 3.8 | 知識 | エンドユーザーコンピューティング（AppStream 2.0、WorkSpaces、Secure Browser） | [エンドユーザーコンピューティング](domain3.md#t3-8-euc) |
| 3.8 | 知識 | フロントエンドとモバイル（Amplify） | [フロントエンドとモバイル](domain3.md#t3-8-frontend) |
| 3.8 | 知識 | IoT（IoT Core） | [IoT](domain3.md#t3-8-iot) |
| 3.8 | スキル | メッセージ、アラート、通知のサービスの選択 | [メッセージと通知のサービス](domain3.md#t3-8-integration) |
| 3.8 | スキル | 業務に合うサービスの選択 | [業務アプリケーション](domain3.md#t3-8-business) |
| 3.8 | スキル | 事業の支援の選択 | [顧客支援のサービス](domain3.md#t3-8-enablement)、[サポートプラン](domain4.md#t4-3-support-plans) |
| 3.8 | スキル | 開発、デプロイ、トラブルシュートのツール | [開発ツール](domain3.md#t3-8-developer) |
| 3.8 | スキル | VM の画面を端末に表示するサービス | [エンドユーザーコンピューティング](domain3.md#t3-8-euc) |
| 3.8 | スキル | フロントエンドとモバイルのサービス | [フロントエンドとモバイル](domain3.md#t3-8-frontend) |
| 3.8 | スキル | IoT デバイスを管理するサービス | [IoT](domain3.md#t3-8-iot) |

## 分野4: 請求、料金、サポート（28項目） {#domain4}

| タスク | 区分 | 項目 | 見出し |
|---|---|---|---|
| [4.1](domain4.md#task-4-1) | 知識 | コンピューティングの購入オプション | [コンピューティングの購入オプション](domain4.md#t4-1-compute-options) |
| 4.1 | 知識 | ストレージの選択肢と階層 | [ストレージの料金](domain4.md#t4-1-storage) |
| 4.1 | スキル | 購入オプションの使い分け | [コンピューティングの購入オプション](domain4.md#t4-1-compute-options) |
| 4.1 | スキル | RI の柔軟性 | [リザーブドインスタンスの柔軟性](domain4.md#t4-1-ri-flexibility) |
| 4.1 | スキル | Organizations での RI の動き | [Organizations での RI の動き](domain4.md#t4-1-ri-organizations) |
| 4.1 | スキル | データ転送の受信と送信の費用 | [データ転送の費用](domain4.md#t4-1-data-transfer) |
| 4.1 | スキル | ストレージの料金 | [ストレージの料金](domain4.md#t4-1-storage) |
| [4.2](domain4.md#task-4-2) | 知識 | 請求のサポートと情報 | [請求の情報](domain4.md#t4-2-billing-info) |
| 4.2 | 知識 | サービスの料金情報 | [サービスの料金情報](domain4.md#t4-2-pricing-info) |
| 4.2 | 知識 | AWS Organizations | [Organizations の一括請求](domain4.md#t4-2-organizations) |
| 4.2 | 知識 | コスト配分タグ | [コスト配分タグとレポート](domain4.md#t4-2-tags) |
| 4.2 | スキル | Budgets と Cost Explorer の用途 | [Budgets と Cost Explorer](domain4.md#t4-2-budgets-explorer) |
| 4.2 | スキル | Pricing Calculator の用途 | [Pricing Calculator](domain4.md#t4-2-pricing-calculator) |
| 4.2 | スキル | 一括請求と費用の配分 | [Organizations の一括請求](domain4.md#t4-2-organizations) |
| 4.2 | スキル | コスト配分タグの種類と請求レポート（CUR） | [コスト配分タグとレポート](domain4.md#t4-2-tags) |
| [4.3](domain4.md#task-4-3) | 知識 | 公式サイトの情報とドキュメント | [AWS の公式サイトの情報](domain4.md#t4-3-official-sites) |
| 4.3 | 知識 | サポートプラン | [サポートプラン](domain4.md#t4-3-support-plans) |
| 4.3 | 知識 | Partner Network の役割（ISV、システムインテグレーター） | [AWS Partner Network](domain4.md#t4-3-apn) |
| 4.3 | 知識 | AWS Support Center | [AWS Support Center](domain4.md#t4-3-support-center) |
| 4.3 | スキル | ホワイトペーパー、ブログ、ドキュメントの場所 | [AWS の公式サイトの情報](domain4.md#t4-3-official-sites) |
| 4.3 | スキル | 技術リソース（Prescriptive Guidance、Knowledge Center、re:Post） | [技術リソースの探し方](domain4.md#t4-3-technical-resources) |
| 4.3 | スキル | サポートの選択肢（Basic、Business Support+、Enterprise、Unified Operations） | [サポートプラン](domain4.md#t4-3-support-plans) |
| 4.3 | スキル | Trusted Advisor、Health Dashboard、Health API の役割 | [Trusted Advisor と Health による管理](domain4.md#t4-3-monitoring-role) |
| 4.3 | スキル | Trust and Safety チームの役割 | [AWS Trust & Safety](domain4.md#t4-3-trust-safety) |
| 4.3 | スキル | パートナーの役割（Marketplace、ISV、システムインテグレーター） | [AWS Partner Network](domain4.md#t4-3-apn) |
| 4.3 | スキル | パートナーになる利点（研修と認定、イベント、ボリューム割引） | [AWS Partner になる利点](domain4.md#t4-3-partner-benefits) |
| 4.3 | スキル | Marketplace の主な機能（費用管理、ガバナンス、権利） | [AWS Marketplace の主な機能](domain4.md#t4-3-marketplace) |
| 4.3 | スキル | 技術支援の選択肢（Professional Services、ソリューションアーキテクト） | [技術支援の選択肢](domain4.md#t4-3-technical-assistance) |

## 技術と概念 {#technologies}

試験ガイドの「Technologies and Concepts」の一覧です。出題の可能性があるものとして挙げられています。

| 項目 | 見出し |
|---|---|
| API | [AWS へのアクセス方法](domain3.md#t3-1-access) |
| AWS クラウドへの移行の利点 | [経済性の見方と節約の要素](domain1.md#t1-4-economics) |
| AWS CAF | [AWS CAF の成果とパースペクティブ](domain1.md#t1-3-caf) |
| AWS コンプライアンス | [コンプライアンスとガバナンスの考え方](domain2.md#t2-2-concepts) |
| コンピューティング | [コンピューティングの全体像](domain3.md#t3-3-overview) |
| コスト管理 | [Budgets と Cost Explorer](domain4.md#t4-2-budgets-explorer) |
| データベース | [データベースの全体像](domain3.md#t3-4-overview) |
| EC2 の購入オプション（RI、オンデマンド、スポット） | [コンピューティングの購入オプション](domain4.md#t4-1-compute-options) |
| グローバルインフラ（リージョン、AZ） | [リージョン、AZ、エッジロケーションの関係](domain3.md#t3-2-components) |
| IaC | [プロビジョニングと運用の方法](domain3.md#t3-1-provisioning) |
| AWS Knowledge Center | [技術リソースの探し方](domain4.md#t4-3-technical-resources) |
| 機械学習 | [AI/ML のサービス](domain3.md#t3-7-ai-ml) |
| 管理とガバナンス | [ガバナンスとコンプライアンスを助けるサービス](domain2.md#t2-2-governance-services)、[運用を支えるサービス](domain3.md#t3-1-operating-tools) |
| 移行とデータ転送 | [移行を支える情報源とプログラム](domain1.md#t1-3-resources)、[データベースの移行ツール](domain3.md#t3-4-migration) |
| ネットワークサービス | [ネットワークの全体像](domain3.md#t3-5-overview) |
| AWS Partner Network | [AWS Partner Network](domain4.md#t4-3-apn) |
| AWS Prescriptive Guidance | [技術リソースの探し方](domain4.md#t4-3-technical-resources) |
| AWS Pricing Calculator | [Pricing Calculator](domain4.md#t4-2-pricing-calculator) |
| AWS Professional Services | [技術支援の選択肢](domain4.md#t4-3-technical-assistance) |
| AWS re:Post | [技術リソースの探し方](domain4.md#t4-3-technical-resources) |
| AWS SDK | [AWS へのアクセス方法](domain3.md#t3-1-access) |
| セキュリティ | [リソースを守るサービス](domain2.md#t2-2-securing) |
| AWS Security Blog | [セキュリティの情報源](domain2.md#t2-4-docs) |
| 責任共有モデル | [モデルの全体像](domain2.md#t2-1-model) |
| AWS ソリューションアーキテクト | [技術支援の選択肢](domain4.md#t4-3-technical-assistance) |
| ストレージ | [ストレージの全体像](domain3.md#t3-6-overview) |
| AWS Support Center | [AWS Support Center](domain4.md#t4-3-support-center) |
| サポートプラン | [サポートプラン](domain4.md#t4-3-support-plans) |
| Well-Architected Framework | [Well-Architected Framework](domain1.md#t1-2-wa-framework) |
