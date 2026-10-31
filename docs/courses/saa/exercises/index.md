# 問題集

話題ごとの本番形式の問題です。基準は **SAA-C03** です。すべてオリジナルの問題で、実際の試験問題ではありません。答えは問題の下を開くと確認でき、選択肢ごとの解説と解説ページへのリンクがあります。

1. まず[分野のページ](../index.md#study-path)で範囲を確認します。
2. サービスの解説を読み、問題を解きます。
3. 間違えた問題は、解説のリンク先に戻って確認します。

問題は話題ごとにまとめています。ストレージ、データベース、移行のように、複数の分野にまたがる話題は最初に出てくる分野に載せています。

## 分野1: セキュアなアーキテクチャの設計 {#domain1}

| 問題集 | 主な内容 |
|---|---|
| [IAM と STS](iam.md) | ポリシーの評価、権限境界、ロール、フェデレーション、リソースポリシー |
| [ガバナンスと責任共有](governance.md) | SCP、RCP、Control Tower、リージョン、責任共有モデル、Artifact |
| [VPC のセキュリティ](vpc-security.md) | SG、NACL、サブネット、VPC エンドポイント、VPN、Direct Connect |
| [脅威の検出と防御](threat-protection.md) | GuardDuty、Macie、Inspector、WAF、Shield、Network Firewall |
| [アプリのアクセスと認証情報](app-security.md) | Secrets Manager、Parameter Store、IMDSv2、Cognito、署名付き Cookie、OAC |
| [暗号化と鍵](encryption.md) | KMS、SSE、ACM、キーポリシー、ローテーション |
| [データの保護](data-protection.md) | ブロックパブリックアクセス、Object Lock、Vault Lock、AWS Backup |

## 分野2: 回復性の高いアーキテクチャの設計 {#domain2}

| 問題集 | 主な内容 |
|---|---|
| [メッセージングと API](messaging.md) | SQS、SNS、EventBridge、Amazon MQ、Step Functions、API Gateway |
| [アーキテクチャと設計](architecture.md) | ステートレス、スケーリング、キャッシュ、専用サービス、分散設計 |
| [コンテナとサーバーレス](containers-serverless.md) | ECS、EKS、Fargate、Lambda、Amplify Hosting |
| [高可用性と DR](resilience.md) | Route 53、単一障害点、フェイルオーバー、DR 戦略、クォータ、可視性 |
| [マネージド AI サービス](ai-services.md) | Comprehend、Polly、Transcribe、Textract、Rekognition、Lex |

## 分野3: 高性能なアーキテクチャの設計 {#domain3}

| 問題集 | 主な内容 |
|---|---|
| [ストレージ](storage.md) | S3、EBS、EFS、FSx の性能、拡張、耐久性、費用 |
| [コンピューティングとスケーリング](compute.md) | Batch、EMR、エッジ、Auto Scaling、インスタンスタイプ、Lambda のメモリ |
| [データベース](databases.md) | Aurora、DynamoDB、リードレプリカ、RDS Proxy、ElastiCache、DAX |
| [ネットワーク](networking.md) | CloudFront、Global Accelerator、CIDR、Transit Gateway、ロードバランサー |
| [移行とデータ転送](migration.md) | Storage Gateway、DataSync、Transfer Family、DMS、SCT |
| [データの取り込みと分析](data-analytics.md) | Kinesis、Firehose、Glue、Lake Formation、EMR、Athena、Quick Sight |

## 分野4: コストを最適化したアーキテクチャの設計 {#domain4}

| 問題集 | 主な内容 |
|---|---|
| [コスト管理ツール](cost-management.md) | Cost Explorer、Budgets、CUR、コスト配分タグ、一括請求 |
| [S3 の費用](s3.md) | ストレージクラス、ライフサイクル、リクエスタ支払い、アップロード、アーカイブ |
| [コンピューティングの費用](compute-cost.md) | Savings Plans、スポット、ファミリー、休止、負荷分散 |
| [データベースの費用](database-cost.md) | Aurora の構成、DynamoDB のクラス、形式、キャッシュ、保持 |
| [ネットワークの費用](network-cost.md) | NAT、Direct Connect、VPN、転送料、ピアリング、CDN、スロットリング |
