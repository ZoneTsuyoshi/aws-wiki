# CLF のサービス一覧

この試験の公式の対象サービスと、wiki の解説ページの対応です。サービス名を選ぶと、該当する解説に移動します。

[コースの概要に戻る](index.md)

## アプリケーション開発 {#group-lambda}

| 解説ページ | この試験の対象サービス |
|---|---|
| [Lambda](../../services/lambda.md) | [AWS Lambda](../../services/lambda.md) |
| [API Gateway](../../services/api-gateway.md) | [Amazon API Gateway](../../services/api-gateway.md) |
| [メッセージング](../../services/messaging.md) | [Amazon EventBridge](../../services/messaging.md#eventbridge)、[Amazon Simple Notification Service](../../services/messaging.md#sns)、[Amazon Simple Queue Service](../../services/messaging.md#sqs) |
| [Step Functions](../../services/step-functions.md) | [AWS Step Functions](../../services/step-functions.md) |
| [ストリーミングと分析](../../services/streaming.md) | [Amazon Athena](../../services/streaming.md#athena)、[Amazon Kinesis](../../services/streaming.md#kinesis-data-streams)、[Amazon OpenSearch Service](../../services/streaming.md#opensearch) |

## データとコンピューティング {#group-dynamodb}

| 解説ページ | この試験の対象サービス |
|---|---|
| [DynamoDB](../../services/dynamodb.md) | [Amazon DynamoDB](../../services/dynamodb.md) |
| [データベースとキャッシュ](../../services/databases.md) | [Amazon Aurora](../../services/databases.md#aurora)、[Amazon ElastiCache](../../services/databases.md#elasticache)、[Amazon RDS](../../services/databases.md#rds) |
| [S3](../../services/s3.md) | [Amazon S3](../../services/s3.md)、[Amazon S3 Glacier](../../services/s3.md#glacier-retrieval) |
| [ストレージ](../../services/storage.md) | [Amazon Elastic Block Store](../../services/storage.md#ebs-encryption)、[Amazon Elastic File System](../../services/storage.md#efs-settings) |
| [EC2 と Elastic Beanstalk](../../services/ec2-beanstalk.md) | [AWS Elastic Beanstalk](../../services/ec2-beanstalk.md) |
| [コンテナ](../../services/containers.md) | [Amazon Elastic Container Registry](../../services/containers.md#ecr)、[Amazon Elastic Container Service](../../services/containers.md#ecs)、[Amazon Elastic Kubernetes Service](../../services/containers.md#eks)、[AWS Fargate](../../services/containers.md#fargate-vs-ec2) |

## セキュリティ {#group-iam}

| 解説ページ | この試験の対象サービス |
|---|---|
| [IAM と STS](../../services/iam.md) | [AWS Identity and Access Management](../../services/iam.md) |
| [Cognito](../../services/cognito.md) | [Amazon Cognito](../../services/cognito.md) |
| [KMS と暗号化](../../services/kms.md) | [AWS Key Management Service](../../services/kms.md) |
| [シークレットと設定](../../services/secrets.md) | [AWS Secrets Manager](../../services/secrets.md#secrets-manager) |
| [証明書と WAF](../../services/certificates.md) | [AWS Certificate Manager](../../services/certificates.md#acm)、[AWS WAF](../../services/certificates.md#waf) |

## デプロイと運用 {#group-cicd}

| 解説ページ | この試験の対象サービス |
|---|---|
| [CI/CD](../../services/cicd.md) | [AWS Amplify](../../services/cicd.md#amplify)、[AWS CodeBuild](../../services/cicd.md#codebuild)、[AWS CodePipeline](../../services/cicd.md#codepipeline) |
| [IaC と CLI](../../services/iac.md) | [AWS CLI](../../services/iac.md#aws-cli)、[AWS CloudFormation](../../services/iac.md#cloudformation-template) |
| [オブザーバビリティ](../../services/observability.md) | [Amazon CloudWatch](../../services/observability.md)、[AWS CloudTrail](../../services/observability.md#cloudtrail)、[AWS X-Ray](../../services/observability.md#xray)、[Service Quotas](../../services/observability.md#quota-alerts) |
| [ネットワークと配信](../../services/networking.md) | [Amazon CloudFront](../../services/networking.md#cloudfront)、[Amazon Route 53](../../services/networking.md#route53)、[Amazon VPC](../../services/networking.md#vpc)、[AWS PrivateLink](../../services/networking.md#vpc-endpoints) |

## クラウドの基礎とガバナンス {#group-cloud-foundations}

| 解説ページ | この試験の対象サービス |
|---|---|
| [クラウドの基礎](../../services/cloud-foundations.md) | [Amazon Lightsail](../../services/cloud-foundations.md#lightsail)、[AWS Artifact](../../services/cloud-foundations.md#artifact)、[AWS Health Dashboard](../../services/cloud-foundations.md#health)、[AWS Management Console](../../services/cloud-foundations.md#access-methods)、[AWS Marketplace](../../services/cloud-foundations.md#marketplace)、[AWS Outposts](../../services/cloud-foundations.md#outposts)、[AWS Support](../../services/cloud-foundations.md#support-plans)、[AWS Trusted Advisor](../../services/cloud-foundations.md#trusted-advisor)、[AWS Well-Architected Tool](../../services/cloud-foundations.md#wa-tool) |
| [ガバナンス](../../services/governance.md) | [AWS Config](../../services/governance.md#config)、[AWS Control Tower](../../services/governance.md#control-tower)、[AWS License Manager](../../services/governance.md#license-manager)、[AWS Organizations](../../services/governance.md#organizations)、[AWS Resource Access Manager](../../services/governance.md#ram)、[AWS Service Catalog](../../services/governance.md#service-catalog) |
| [コスト管理](../../services/cost-management.md) | [AWS Budgets](../../services/cost-management.md#budgets)、[AWS Compute Optimizer](../../services/cost-management.md#compute-optimizer)、[AWS Cost and Usage Reports](../../services/cost-management.md#data-exports)、[AWS Cost Explorer](../../services/cost-management.md#cost-explorer) |
| [運用](../../services/operations.md) | [Amazon EC2](../../services/operations.md#ec2-operations)、[AWS Auto Scaling](../../services/operations.md#auto-scaling)、[AWS Systems Manager](../../services/operations.md#systems-manager) |

## 高度なネットワークとセキュリティ {#group-network-connectivity}

| 解説ページ | この試験の対象サービス |
|---|---|
| [ネットワーク接続](../../services/network-connectivity.md) | [AWS Client VPN](../../services/network-connectivity.md#client-vpn)、[AWS Direct Connect](../../services/network-connectivity.md#direct-connect)、[AWS Global Accelerator](../../services/network-connectivity.md#global-accelerator)、[AWS Site-to-Site VPN](../../services/network-connectivity.md#site-to-site-vpn)、[AWS Transit Gateway](../../services/network-connectivity.md#transit-gateway) |
| [脅威検出とインシデント対応](../../services/threat-detection.md) | [Amazon Detective](../../services/threat-detection.md#detective)、[Amazon GuardDuty](../../services/threat-detection.md#guardduty)、[Amazon Inspector](../../services/threat-detection.md#inspector)、[Amazon Macie](../../services/threat-detection.md#macie)、[AWS Firewall Manager](../../services/threat-detection.md#firewall-manager)、[AWS Security Hub](../../services/threat-detection.md#security-hub)、[AWS Shield](../../services/threat-detection.md#shield) |
| [ID とディレクトリ](../../services/identity-directory.md) | [AWS CloudHSM](../../services/identity-directory.md#cloudhsm)、[AWS Directory Service](../../services/identity-directory.md#directory-service)、[AWS IAM Identity Center](../../services/identity-directory.md#identity-center) |

## データと分析 {#group-data-engineering}

| 解説ページ | この試験の対象サービス |
|---|---|
| [データエンジニアリング](../../services/data-engineering.md) | [Amazon EMR](../../services/data-engineering.md#emr)、[Amazon Redshift](../../services/data-engineering.md#redshift)、[AWS Glue](../../services/data-engineering.md#glue) |
| [専用データベース](../../services/databases-specialized.md) | [Amazon DocumentDB](../../services/databases-specialized.md#documentdb)、[Amazon Neptune](../../services/databases-specialized.md#neptune) |
| [高度なストレージ](../../services/storage-advanced.md) | [Amazon FSx](../../services/storage-advanced.md#fsx-selection) |

## 移行と事業継続 {#group-migration}

| 解説ページ | この試験の対象サービス |
|---|---|
| [移行](../../services/migration.md) | [AWS Application Discovery Service](../../services/migration.md#application-discovery)、[AWS Application Migration Service](../../services/migration.md#mgn)、[AWS Database Migration Service](../../services/migration.md#dms)、[AWS Migration Hub](../../services/migration.md#migration-hub)、[AWS Schema Conversion Tool](../../services/migration.md#sct)、[AWS Storage Gateway](../../services/migration.md#storage-gateway)、[Migration Evaluator](../../services/migration.md#migration-evaluator) |
| [レジリエンスと災害対策](../../services/resilience.md) | [AWS Backup](../../services/resilience.md#backup)、[AWS Elastic Disaster Recovery](../../services/resilience.md#drs) |

## AI {#group-ai}

| 解説ページ | この試験の対象サービス |
|---|---|
| [AI サービス](../../services/ai.md) | [Amazon Q](../../services/ai.md#q-developer)、[Amazon Quick](../../services/ai.md#quick) |
| [SageMaker](../../services/sagemaker.md) | [Amazon SageMaker AI](../../services/sagemaker.md) |
| [マネージド AI サービス](../../services/ai-managed-services.md) | [Amazon Comprehend](../../services/ai-managed-services.md#comprehend)、[Amazon Lex](../../services/ai-managed-services.md#lex)、[Amazon Polly](../../services/ai-managed-services.md#polly)、[Amazon Rekognition](../../services/ai-managed-services.md#rekognition)、[Amazon Textract](../../services/ai-managed-services.md#textract)、[Amazon Transcribe](../../services/ai-managed-services.md#transcribe)、[Amazon Translate](../../services/ai-managed-services.md#translate) |

## その他 {#group-other-services}

| 解説ページ | この試験の対象サービス |
|---|---|
| [その他のサービス](../../services/other-services.md) | [Amazon AppStream 2.0](../../services/other-services.md#appstream)、[Amazon Connect](../../services/other-services.md#connect)、[Amazon Simple Email Service](../../services/other-services.md#ses)、[Amazon WorkSpaces](../../services/other-services.md#workspaces)、[Amazon WorkSpaces Secure Browser](../../services/other-services.md#secure-browser)、[AWS Batch](../../services/other-services.md#batch)、[AWS IoT Core](../../services/other-services.md#iot-core) |
