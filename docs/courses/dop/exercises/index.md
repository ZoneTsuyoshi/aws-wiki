# 問題集

話題ごとの本番形式の問題です。**DOP-C02** を基準にしています。すべてオリジナルの問題で、実際の試験問題ではありません。答えは問題の下を開くと確認でき、選択肢ごとの解説と解説ページへのリンクがあります。

1. まず[分野のページ](../index.md#study-path)で範囲を確認します。
2. サービスの解説を読み、問題を解きます。
3. 間違えた問題は、解説のリンク先に戻って確認します。

同じ問題集が複数の分野にまたがるときは、それぞれの表に載せています。分野ごとの問題の一覧は、各分野の[サービス別の学習](../study/domain1/index.md)にあります。

## 分野1: SDLC の自動化 {#domain1}

| 問題集 | 主な内容 |
|---|---|
| [CodePipeline と複数アカウント](pipelines.md) | SDLC、複数アカウントの構成、トリガー、パイプラインからの呼び出し |
| [CodeBuild とテスト](codebuild.md) | buildspec、シークレット、PR のビルド、テストの配置、終了コード、カバレッジ |
| [成果物とリポジトリ](artifacts.md) | ECR、CodeArtifact、S3、Image Builder、権限、ライフサイクル |
| [デプロイ方式](deployments.md) | CodeDeploy、Beanstalk、ECS、Lambda、エージェント、失敗の解決 |
| [コンテナ](containers.md) | ECS、EKS、Fargate、プラットフォームの選択 |

## 分野2: 構成管理と IaC {#domain2}

| 問題集 | 主な内容 |
|---|---|
| [IaC と StackSets](iac.md) | CloudFormation、SAM、CDK、変更管理、StackSets、モジュール |
| [Organizations と統制](organizations.md) | OU、Control Tower、Account Factory、SCP、Service Catalog |
| [Systems Manager と自動化](systems-manager.md) | Automation、State Manager、Patch Manager、Inventory、AppConfig |
| [サーバーレス](serverless.md) | Lambda、API Gateway、Step Functions の構成と自動化 |

## 分野3: 回復力のあるクラウドソリューション {#domain3}

| 問題集 | 主な内容 |
|---|---|
| [高可用性](high-availability.md) | Multi-AZ、SLA、単一障害点、ダウンタイムの抑制 |
| [複数リージョン](multi-region.md) | 複製と切り替え、リージョンをまたぐ機能、グローバルな配置 |
| [負荷分散とヘルスチェック](load-balancing.md) | ALB、NLB、クロスゾーン、ヘルスチェック、バックエンド障害 |
| [スケーリング](scaling.md) | 指標、ポリシー、キャッシュ、スケーリングの問題、各サービスの Auto Scaling |
| [サーバーレス](serverless.md) | Lambda、API Gateway、Step Functions の構成と自動化 |
| [コンテナ](containers.md) | ECS、EKS、Fargate、プラットフォームの選択 |
| [災害対策](disaster-recovery.md) | RTO、RPO、DR 戦略、復旧手順、フェイルオーバーのテスト、AWS Backup |

## 分野4: 監視とログ {#domain4}

| 問題集 | 主な内容 |
|---|---|
| [負荷分散とヘルスチェック](load-balancing.md) | ALB、NLB、クロスゾーン、ヘルスチェック、バックエンド障害 |
| [スケーリング](scaling.md) | 指標、ポリシー、キャッシュ、スケーリングの問題、各サービスの Auto Scaling |
| [CloudWatch Logs](cloudwatch-logs.md) | メトリクスフィルター、サブスクリプション、検索、保持、暗号化、権限 |
| [CloudWatch メトリクスとアラーム](cloudwatch-metrics.md) | 標準とカスタムのメトリクス、ストリーム、異常検知、アラーム、エージェント |
| [ログのストリーミングと分析](log-streaming.md) | Kinesis、Firehose、Athena、S3 イベントによる処理 |
| [イベントとメッセージング](messaging.md) | EventBridge、SNS、SQS、イベント駆動のワークフロー |
| [AWS Config](config.md) | ルール、修復、アグリゲーター、望ましくない状態の修復 |
| [X-Ray と障害の調査](troubleshooting.md) | トレース、サービスの状態、根本原因、失敗したデプロイとプロセス |
| [脅威の検出](threat-detection.md) | GuardDuty、Inspector、Security Hub、Detective、通知と分析 |
| [監査とログ](security-audit.md) | CloudTrail、ログの安全な保管、フローログ、サービスのログ設定 |

## 分野5: インシデントとイベントへの対応 {#domain5}

| 問題集 | 主な内容 |
|---|---|
| [Systems Manager と自動化](systems-manager.md) | Automation、State Manager、Patch Manager、Inventory、AppConfig |
| [コンテナ](containers.md) | ECS、EKS、Fargate、プラットフォームの選択 |
| [イベントとメッセージング](messaging.md) | EventBridge、SNS、SQS、イベント駆動のワークフロー |
| [AWS Config](config.md) | ルール、修復、アグリゲーター、望ましくない状態の修復 |
| [X-Ray と障害の調査](troubleshooting.md) | トレース、サービスの状態、根本原因、失敗したデプロイとプロセス |

## 分野6: セキュリティとコンプライアンス {#domain6}

| 問題集 | 主な内容 |
|---|---|
| [IAM とアクセス管理](iam.md) | 要素、フェデレーション、権限境界、SCP、最小権限、ABAC、MFA |
| [ネットワークセキュリティと証明書](network-security.md) | セキュリティグループ、ネットワーク ACL、WAF、Shield、ACM、多層防御 |
| [データ保護](data-protection.md) | データ管理、暗号化、Macie、認証情報のローテーション |
| [脅威の検出](threat-detection.md) | GuardDuty、Inspector、Security Hub、Detective、通知と分析 |
| [監査とログ](security-audit.md) | CloudTrail、ログの安全な保管、フローログ、サービスのログ設定 |
