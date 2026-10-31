# SAP のサービス一覧

この試験の公式の対象サービスと、wiki の解説ページの対応です。サービス名を選ぶと、該当する解説に移動します。

[コースの概要に戻る](index.md)

## アプリケーション開発 {#group-lambda}

| 解説ページ | この試験の対象サービス |
|---|---|
| [Lambda](../../services/lambda.md) | [AWS Lambda](../../services/lambda.md) |
| [API Gateway](../../services/api-gateway.md) | [Amazon API Gateway](../../services/api-gateway.md) |
| [メッセージング](../../services/messaging.md) | [Amazon EventBridge](../../services/messaging.md#eventbridge)、[Amazon SNS](../../services/messaging.md#sns)、[Amazon SQS](../../services/messaging.md#sqs) |
| [Step Functions](../../services/step-functions.md) | [AWS Step Functions](../../services/step-functions.md) |
| [ストリーミングと分析](../../services/streaming.md) | [Amazon Athena](../../services/streaming.md#athena)、[Amazon Kinesis Data Streams](../../services/streaming.md#kinesis-data-streams)、[Amazon OpenSearch Service](../../services/streaming.md#opensearch) |

## データとコンピューティング {#group-dynamodb}

| 解説ページ | この試験の対象サービス |
|---|---|
| [DynamoDB](../../services/dynamodb.md) | [Amazon DynamoDB](../../services/dynamodb.md) |
| [データベースとキャッシュ](../../services/databases.md) | [Amazon Aurora](../../services/databases.md#aurora)、[Amazon ElastiCache](../../services/databases.md#elasticache)、[Amazon RDS](../../services/databases.md#rds) |
| [S3](../../services/s3.md) | [Amazon S3](../../services/s3.md) |
| [ストレージ](../../services/storage.md) | [Amazon Data Lifecycle Manager](../../services/storage.md#ebs-snapshots)、[Amazon EBS](../../services/storage.md#ebs-encryption)、[Amazon EFS](../../services/storage.md#efs-settings) |
| [EC2 と Elastic Beanstalk](../../services/ec2-beanstalk.md) | [AWS Elastic Beanstalk](../../services/ec2-beanstalk.md) |
| [コンテナ](../../services/containers.md) | [Amazon ECR](../../services/containers.md#ecr)、[Amazon ECS](../../services/containers.md#ecs)、[Amazon EKS](../../services/containers.md#eks)、[AWS Fargate](../../services/containers.md#fargate-vs-ec2) |

## セキュリティ {#group-iam}

| 解説ページ | この試験の対象サービス |
|---|---|
| [IAM と STS](../../services/iam.md) | [IAM](../../services/iam.md) |
| [Cognito](../../services/cognito.md) | [Amazon Cognito](../../services/cognito.md) |
| [KMS と暗号化](../../services/kms.md) | [AWS KMS](../../services/kms.md) |
| [シークレットと設定](../../services/secrets.md) | [AWS Secrets Manager](../../services/secrets.md#secrets-manager) |
| [証明書と WAF](../../services/certificates.md) | [AWS Certificate Manager](../../services/certificates.md#acm)、[AWS WAF](../../services/certificates.md#waf) |

## デプロイと運用 {#group-cicd}

| 解説ページ | この試験の対象サービス |
|---|---|
| [CI/CD](../../services/cicd.md) | [AWS CodeBuild](../../services/cicd.md#codebuild)、[AWS CodeCommit](../../services/cicd.md#codecommit-status)、[AWS CodeDeploy](../../services/cicd.md#codedeploy)、[AWS CodePipeline](../../services/cicd.md#codepipeline) |
| [IaC と CLI](../../services/iac.md) | [AWS CDK](../../services/iac.md#cdk)、[AWS CloudFormation](../../services/iac.md#cloudformation-template) |
| [オブザーバビリティ](../../services/observability.md) | [Amazon CloudWatch](../../services/observability.md)、[AWS CloudTrail](../../services/observability.md#cloudtrail)、[AWS Distro for OpenTelemetry](../../services/observability.md#xray-opentelemetry)、[AWS X-Ray](../../services/observability.md#xray)、[Service Quotas](../../services/observability.md#quota-alerts) |
| [ネットワークと配信](../../services/networking.md) | [Amazon CloudFront](../../services/networking.md#cloudfront)、[Amazon Route 53](../../services/networking.md#route53)、[Amazon VPC](../../services/networking.md#vpc)、[AWS PrivateLink](../../services/networking.md#vpc-endpoints)、[Elastic Load Balancing](../../services/networking.md#elb) |

## クラウドの基礎とガバナンス {#group-cloud-foundations}

| 解説ページ | この試験の対象サービス |
|---|---|
| [クラウドの基礎](../../services/cloud-foundations.md) | [Amazon Lightsail](../../services/cloud-foundations.md#lightsail)、[AWS Local Zones](../../services/cloud-foundations.md#local-zones)、[AWS Outposts](../../services/cloud-foundations.md#outposts) |
| [ガバナンス](../../services/governance.md) | [AWS Config](../../services/governance.md#config)、[AWS Control Tower](../../services/governance.md#control-tower)、[AWS Organizations](../../services/governance.md#organizations)、[AWS Resource Access Manager](../../services/governance.md#ram) |
| [コスト管理](../../services/cost-management.md) | [AWS Budgets](../../services/cost-management.md#budgets)、[AWS Compute Optimizer](../../services/cost-management.md#compute-optimizer)、[AWS Cost and Usage Report](../../services/cost-management.md#data-exports)、[AWS Cost Categories](../../services/cost-management.md#cost-categories)、[AWS Cost Explorer](../../services/cost-management.md#cost-explorer)、[Reserved Instances](../../services/cost-management.md#reserved-instances)、[Savings Plans](../../services/cost-management.md#savings-plans) |
| [運用](../../services/operations.md) | [Amazon EC2](../../services/operations.md#ec2-operations)、[AWS Application Auto Scaling](../../services/operations.md#auto-scaling)、[AWS Device Farm](../../services/operations.md#device-farm)、[AWS Systems Manager](../../services/operations.md#systems-manager) |

## 高度なネットワークとセキュリティ {#group-network-connectivity}

| 解説ページ | この試験の対象サービス |
|---|---|
| [ネットワーク接続](../../services/network-connectivity.md) | [Amazon VPC Lattice](../../services/network-connectivity.md#vpc-lattice)、[AWS Cloud WAN](../../services/network-connectivity.md#cloud-wan)、[AWS Direct Connect](../../services/network-connectivity.md#direct-connect)、[AWS Global Accelerator](../../services/network-connectivity.md#global-accelerator)、[AWS Network Firewall](../../services/network-connectivity.md#network-firewall)、[AWS Transit Gateway](../../services/network-connectivity.md#transit-gateway)、[AWS VPN](../../services/network-connectivity.md#site-to-site-vpn) |
| [脅威検出とインシデント対応](../../services/threat-detection.md) | [Amazon GuardDuty](../../services/threat-detection.md#guardduty)、[Amazon Inspector](../../services/threat-detection.md#inspector)、[Amazon Security Lake](../../services/threat-detection.md#security-lake)、[AWS Network Firewall](../../services/threat-detection.md#network-firewall)、[AWS Security Hub](../../services/threat-detection.md#security-hub)、[AWS Shield](../../services/threat-detection.md#shield) |
| [ID とディレクトリ](../../services/identity-directory.md) | [Amazon Verified Permissions](../../services/identity-directory.md#verified-permissions)、[AWS CloudHSM](../../services/identity-directory.md#cloudhsm)、[AWS Directory Service](../../services/identity-directory.md#directory-service)、[AWS Verified Access](../../services/identity-directory.md#verified-access) |

## データと分析 {#group-data-engineering}

| 解説ページ | この試験の対象サービス |
|---|---|
| [データエンジニアリング](../../services/data-engineering.md) | [Amazon AppFlow](../../services/data-engineering.md#appflow)、[Amazon EMR](../../services/data-engineering.md#emr)、[Amazon Managed Streaming for Apache Kafka](../../services/data-engineering.md#msk)、[Amazon QuickSight](../../services/data-engineering.md#quick-sight)、[Amazon Redshift](../../services/data-engineering.md#redshift)、[AWS Clean Rooms](../../services/data-engineering.md#clean-rooms)、[AWS Glue](../../services/data-engineering.md#glue)、[AWS Lake Formation](../../services/data-engineering.md#lake-formation) |
| [専用データベース](../../services/databases-specialized.md) | [Amazon DocumentDB](../../services/databases-specialized.md#documentdb)、[Amazon Keyspaces](../../services/databases-specialized.md#keyspaces)、[Amazon MemoryDB](../../services/databases-specialized.md#memorydb)、[Amazon Neptune](../../services/databases-specialized.md#neptune)、[Amazon RDS Custom for Oracle](../../services/databases-specialized.md#rds-custom)、[Amazon Timestream](../../services/databases-specialized.md#timestream) |
| [高度なストレージ](../../services/storage-advanced.md) | [Amazon FSx](../../services/storage-advanced.md#fsx-selection) |

## 移行と事業継続 {#group-migration}

| 解説ページ | この試験の対象サービス |
|---|---|
| [移行](../../services/migration.md) | [AWS Data Transfer Terminal](../../services/migration.md#data-transfer-terminal)、[AWS DataSync](../../services/migration.md#datasync)、[AWS DMS](../../services/migration.md#dms)、[AWS SCT](../../services/migration.md#sct)、[AWS Storage Gateway](../../services/migration.md#storage-gateway)、[AWS Transfer Family](../../services/migration.md#transfer-family)、[AWS Transform](../../services/migration.md#transform)、[AWS Transform MGN](../../services/migration.md#mgn) |
| [レジリエンスと災害対策](../../services/resilience.md) | [AWS Backup](../../services/resilience.md#backup)、[AWS Elastic Disaster Recovery](../../services/resilience.md#drs)、[AWS Fault Injection Service](../../services/resilience.md#fis)、[AWS Resilience Hub](../../services/resilience.md#resilience-hub) |

## AI {#group-ai}

| 解説ページ | この試験の対象サービス |
|---|---|
| [AI サービス](../../services/ai.md) | [Amazon Bedrock](../../services/ai.md) |
| [SageMaker](../../services/sagemaker.md) | [Amazon SageMaker AI](../../services/sagemaker.md) |
| [マネージド AI サービス](../../services/ai-managed-services.md) | [Amazon Comprehend Medical](../../services/ai-managed-services.md#comprehend-medical)、[Amazon Transcribe Medical](../../services/ai-managed-services.md#transcribe-medical) |
| [生成 AI アプリケーション](../../services/genai-apps.md) | [Amazon Bedrock](../../services/genai-apps.md) |

## その他 {#group-other-services}

| 解説ページ | この試験の対象サービス |
|---|---|
| [その他のサービス](../../services/other-services.md) | [Amazon Braket](../../services/other-services.md#braket)、[Amazon GameLift](../../services/other-services.md#gamelift)、[Amazon Interactive Video Service](../../services/other-services.md#ivs)、[Amazon Managed Blockchain](../../services/other-services.md#managed-blockchain)、[Amazon MQ](../../services/other-services.md#mq)、[AWS DeepComposer](../../services/other-services.md#deepcomposer)、[AWS DeepRacer](../../services/other-services.md#deepracer)、[AWS Elemental MediaConvert](../../services/other-services.md#mediaconvert)、[AWS Elemental MediaLive](../../services/other-services.md#medialive)、[AWS Ground Station](../../services/other-services.md#ground-station) |

## 解説で参照しているページ {#related}

公式の対象サービスの一覧には載っていませんが、このコースの解説で参照しているページです。

- [SDK と耐障害性](../../services/sdk-resilience.md)
