# SOA のサービス一覧

この試験の公式の対象サービスと、wiki の解説ページの対応です。サービス名を選ぶと、該当する解説に移動します。

[コースの概要に戻る](index.md)

## アプリケーション開発 {#group-lambda}

| 解説ページ | この試験の対象サービス |
|---|---|
| [Lambda](../../services/lambda.md) | [AWS Lambda](../../services/lambda.md) |
| [メッセージング](../../services/messaging.md) | [Amazon EventBridge](../../services/messaging.md#eventbridge)、[Amazon SNS](../../services/messaging.md#sns)、[Amazon SQS](../../services/messaging.md#sqs) |
| [Step Functions](../../services/step-functions.md) | [AWS Step Functions](../../services/step-functions.md) |
| [ストリーミングと分析](../../services/streaming.md) | [Amazon Athena](../../services/streaming.md#athena)、[Amazon Data Firehose](../../services/streaming.md#firehose) |

## データとコンピューティング {#group-dynamodb}

| 解説ページ | この試験の対象サービス |
|---|---|
| [DynamoDB](../../services/dynamodb.md) | [Amazon DynamoDB](../../services/dynamodb.md)、[Amazon DynamoDB Accelerator](../../services/dynamodb.md#dax) |
| [データベースとキャッシュ](../../services/databases.md) | [Amazon Aurora](../../services/databases.md#aurora)、[Amazon Aurora Serverless v2](../../services/databases.md#aurora-serverless-v2)、[Amazon ElastiCache](../../services/databases.md#elasticache)、[Amazon RDS](../../services/databases.md#rds)、[Amazon RDS Proxy](../../services/databases.md#rds-proxy) |
| [S3](../../services/s3.md) | [Amazon S3](../../services/s3.md) |
| [ストレージ](../../services/storage.md) | [Amazon EBS](../../services/storage.md#ebs-encryption)、[Amazon EFS](../../services/storage.md#efs-settings) |
| [EC2 と Elastic Beanstalk](../../services/ec2-beanstalk.md) | [Amazon EC2](../../services/ec2-beanstalk.md) |
| [コンテナ](../../services/containers.md) | [Amazon ECR](../../services/containers.md#ecr)、[Amazon ECS](../../services/containers.md#ecs)、[Amazon EKS](../../services/containers.md#eks) |

## セキュリティ {#group-iam}

| 解説ページ | この試験の対象サービス |
|---|---|
| [IAM と STS](../../services/iam.md) | [IAM](../../services/iam.md) |
| [KMS と暗号化](../../services/kms.md) | [AWS KMS](../../services/kms.md) |
| [シークレットと設定](../../services/secrets.md) | [AWS Secrets Manager](../../services/secrets.md#secrets-manager) |
| [証明書と WAF](../../services/certificates.md) | [AWS Certificate Manager](../../services/certificates.md#acm)、[AWS WAF](../../services/certificates.md#waf) |

## デプロイと運用 {#group-cicd}

| 解説ページ | この試験の対象サービス |
|---|---|
| [IaC と CLI](../../services/iac.md) | [AWS CDK](../../services/iac.md#cdk)、[AWS CloudFormation](../../services/iac.md#cloudformation-template) |
| [オブザーバビリティ](../../services/observability.md) | [Amazon CloudWatch](../../services/observability.md)、[AWS CloudTrail](../../services/observability.md#cloudtrail)、[AWS X-Ray](../../services/observability.md#xray) |
| [ネットワークと配信](../../services/networking.md) | [Amazon CloudFront](../../services/networking.md#cloudfront)、[Amazon EC2 security groups](../../services/networking.md#security-group-rules)、[Amazon Route 53](../../services/networking.md#route53)、[Amazon VPC](../../services/networking.md#vpc)、[AWS PrivateLink](../../services/networking.md#vpc-endpoints)、[Elastic Load Balancing](../../services/networking.md#elb)、[Network ACLs](../../services/networking.md#nacl-rules) |

## クラウドの基礎とガバナンス {#group-cloud-foundations}

| 解説ページ | この試験の対象サービス |
|---|---|
| [クラウドの基礎](../../services/cloud-foundations.md) | [AWS Health Dashboard](../../services/cloud-foundations.md#health)、[AWS Trusted Advisor](../../services/cloud-foundations.md#trusted-advisor) |
| [ガバナンス](../../services/governance.md) | [AWS Config](../../services/governance.md#config)、[AWS Control Tower](../../services/governance.md#control-tower)、[AWS Organizations](../../services/governance.md#organizations)、[AWS Resource Access Manager](../../services/governance.md#ram)、[AWS Service Catalog](../../services/governance.md#service-catalog)、[Service control policies](../../services/governance.md#scp) |
| [コスト管理](../../services/cost-management.md) | [AWS Compute Optimizer](../../services/cost-management.md#compute-optimizer)、[AWS Cost and Usage Reports](../../services/cost-management.md#data-exports)、[AWS Cost Explorer](../../services/cost-management.md#cost-explorer)、[Savings Plans](../../services/cost-management.md#savings-plans) |
| [運用](../../services/operations.md) | [Amazon EC2](../../services/operations.md#ec2-operations)、[Amazon EC2 Image Builder](../../services/operations.md#image-builder)、[Amazon Managed Grafana](../../services/operations.md#managed-grafana)、[AWS Auto Scaling](../../services/operations.md#auto-scaling)、[AWS DevOps Agent](../../services/operations.md#devops-agent)、[AWS Managed Service for Prometheus](../../services/operations.md#managed-prometheus)、[AWS Systems Manager](../../services/operations.md#systems-manager) |

## 高度なネットワークとセキュリティ {#group-network-connectivity}

| 解説ページ | この試験の対象サービス |
|---|---|
| [ネットワーク接続](../../services/network-connectivity.md) | [Amazon Route 53 Resolver DNS Firewall](../../services/network-connectivity.md#dns-firewall)、[Amazon VPC IP Address Manager](../../services/network-connectivity.md#ipam)、[AWS Client VPN](../../services/network-connectivity.md#client-vpn)、[AWS Global Accelerator](../../services/network-connectivity.md#global-accelerator)、[AWS Network Firewall](../../services/network-connectivity.md#network-firewall)、[AWS Site-to-Site VPN](../../services/network-connectivity.md#site-to-site-vpn)、[AWS Transit Gateway](../../services/network-connectivity.md#transit-gateway)、[Egress-only internet gateways](../../services/network-connectivity.md#ipv6)、[Elastic IP addresses](../../services/network-connectivity.md#elastic-ip)、[NAT gateways](../../services/network-connectivity.md#nat-gateway)、[VPC Flow Logs](../../services/network-connectivity.md#flow-log-analysis)、[VPC peering](../../services/network-connectivity.md#vpc-peering)、[VPC Reachability Analyzer](../../services/network-connectivity.md#reachability-analyzer) |
| [脅威検出とインシデント対応](../../services/threat-detection.md) | [Amazon GuardDuty](../../services/threat-detection.md#guardduty)、[Amazon Inspector](../../services/threat-detection.md#inspector)、[Amazon Macie](../../services/threat-detection.md#macie)、[AWS Network Firewall](../../services/threat-detection.md#network-firewall)、[AWS Security Hub](../../services/threat-detection.md#security-hub)、[AWS Shield](../../services/threat-detection.md#shield) |
| [ID とディレクトリ](../../services/identity-directory.md) | [AWS IAM Access Analyzer](../../services/identity-directory.md#access-analyzer)、[AWS IAM Identity Center](../../services/identity-directory.md#identity-center) |

## データと分析 {#group-data-engineering}

| 解説ページ | この試験の対象サービス |
|---|---|
| [高度なストレージ](../../services/storage-advanced.md) | [Amazon FSx](../../services/storage-advanced.md#fsx-selection) |

## 移行と事業継続 {#group-migration}

| 解説ページ | この試験の対象サービス |
|---|---|
| [移行](../../services/migration.md) | [AWS DataSync](../../services/migration.md#datasync)、[AWS Storage Gateway](../../services/migration.md#storage-gateway) |
| [レジリエンスと災害対策](../../services/resilience.md) | [Amazon Application Recovery Controller](../../services/resilience.md#arc)、[AWS Backup](../../services/resilience.md#backup) |

## AI {#group-ai}

| 解説ページ | この試験の対象サービス |
|---|---|
| [AI サービス](../../services/ai.md) | [Amazon Bedrock](../../services/ai.md)、[Kiro](../../services/ai.md#kiro) |
| [生成 AI アプリケーション](../../services/genai-apps.md) | [Amazon Bedrock](../../services/genai-apps.md) |

## その他 {#group-other-services}

| 解説ページ | この試験の対象サービス |
|---|---|
| [その他のサービス](../../services/other-services.md) | [Amazon SES](../../services/other-services.md#ses) |

## 解説で参照しているページ {#related}

公式の対象サービスの一覧には載っていませんが、このコースの解説で参照しているページです。

- [CI/CD（CodeBuild / CodeDeploy / CodePipeline）](../../services/cicd.md)

## 専用の解説がないサービス {#not-covered}

公式の対象ですが、サービス解説に専用の説明がありません。コースの分野ページで必要な範囲を説明しています。

- AWS Security Agent
