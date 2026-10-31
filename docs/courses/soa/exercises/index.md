# 問題集

本番形式の問題です。**SOA-C03** を基準にしています。すべてオリジナルの問題で、実際の試験問題ではありません。答えは問題の下を開くと確認でき、選択肢ごとの解説と解説ページへのリンクがあります。

1. まず[分野のページ](../index.md#study-path)で範囲を確認します。
2. サービスの解説を読み、問題を解きます。
3. 間違えた問題は、解説のリンク先に戻って確認します。

## 分野1: 監視、ログ、分析、修復、性能の最適化 {#domain1}

| 問題集 | 主な内容 |
|---|---|
| [CloudWatch](cloudwatch.md) | ログ、エージェント、アラーム、ダッシュボード |
| [EventBridge と通知](eventbridge.md) | SNS、ルールの切り分け、DLQ、イベント駆動 |
| [Systems Manager と修復](systems-manager.md) | Automation、修復の手段、Patch Manager |
| [EC2 と性能の最適化](ec2-performance.md) | Compute Optimizer、プレイスメントグループ、ネットワーク |
| [EBS、EFS、FSx](storage.md) | ボリュームタイプ、メトリクス、共有ストレージ |
| [S3](s3.md) | アップロードの性能、DataSync、バージョニング |

## 分野2: 信頼性と事業継続性 {#domain2}

| 問題集 | 主な内容 |
|---|---|
| [Auto Scaling](auto-scaling.md) | ポリシー、起動の失敗、ECS と Lambda |
| [キャッシュ](caching.md) | ElastiCache、DAX、CloudFront の使い分け |
| [RDS、Aurora、DynamoDB](databases.md) | 監視、スケーリング、復元 |
| [ヘルスチェックと高可用性](high-availability.md) | ALB、Route 53、Multi-AZ、ARC |
| [バックアップと災害復旧](backup-dr.md) | AWS Backup、DLM、DR 戦略 |

## 分野3: デプロイ、プロビジョニング、自動化 {#domain3}

| 問題集 | 主な内容 |
|---|---|
| [CloudFormation、CDK、Terraform](iac.md) | 運用の機能、失敗の対処、StackSets、AWS RAM |
| [イメージとデプロイ戦略](deployment.md) | AMI、Image Builder、ECR、更新の方法 |

## 分野4: セキュリティとコンプライアンス {#domain4}

| 問題集 | 主な内容 |
|---|---|
| [IAM とアクセスの調査](iam.md) | ポリシーの評価、拒否の調査、Access Analyzer |
| [Organizations、Trusted Advisor、Config](governance.md) | SCP、Control Tower、修復、適合パック |
| [暗号化とシークレット](encryption.md) | KMS、ACM、Secrets Manager |
| [データ分類と検出結果](threat-detection.md) | Macie、GuardDuty、Security Hub |

## 分野5: ネットワークとコンテンツ配信 {#domain5}

| 問題集 | 主な内容 |
|---|---|
| [VPC の設定と調査](vpc.md) | 経路、NACL、費用、Reachability Analyzer |
| [プライベート接続とハイブリッド接続](connectivity.md) | エンドポイント、VPN、Direct Connect |
| [ネットワークの保護、ログ、監視](network-ops.md) | WAF、フローログ、Network Monitor |
| [DNS と配信](dns-cdn.md) | Route 53、CloudFront、Global Accelerator |
