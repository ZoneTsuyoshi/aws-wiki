# AIP のサービス一覧

この試験の公式の対象サービスと、wiki の解説ページの対応です。サービス名を選ぶと、該当する解説に移動します。

[コースの概要に戻る](index.md)

## アプリケーション開発 {#group-lambda}

| 解説ページ | この試験の対象サービス |
|---|---|
| [Lambda](../../services/lambda.md) | [AWS Lambda](../../services/lambda.md) |
| [API Gateway](../../services/api-gateway.md) | [Amazon API Gateway](../../services/api-gateway.md) |
| [メッセージング](../../services/messaging.md) | [Amazon EventBridge](../../services/messaging.md#eventbridge)、[Amazon SNS](../../services/messaging.md#sns)、[Amazon SQS](../../services/messaging.md#sqs) |
| [Step Functions](../../services/step-functions.md) | [AWS Step Functions](../../services/step-functions.md) |
| [ストリーミングと分析](../../services/streaming.md) | [Amazon Athena](../../services/streaming.md#athena)、[Amazon Kinesis](../../services/streaming.md#kinesis-data-streams)、[Amazon OpenSearch Service](../../services/streaming.md#opensearch) |
| [SDK と耐障害性](../../services/sdk-resilience.md) | [AWS Tools and SDKs](../../services/sdk-resilience.md) |

## データとコンピューティング {#group-dynamodb}

| 解説ページ | この試験の対象サービス |
|---|---|
| [DynamoDB](../../services/dynamodb.md) | [Amazon DynamoDB](../../services/dynamodb.md)、[Amazon DynamoDB Streams](../../services/dynamodb.md#streams) |
| [データベースとキャッシュ](../../services/databases.md) | [Amazon Aurora](../../services/databases.md#aurora)、[Amazon ElastiCache](../../services/databases.md#elasticache)、[Amazon RDS](../../services/databases.md#rds) |
| [S3](../../services/s3.md) | [Amazon S3](../../services/s3.md)、[Amazon S3 Cross-Region Replication](../../services/s3.md#replication)、[Amazon S3 Intelligent-Tiering](../../services/s3.md#storage-classes)、[Amazon S3 Lifecycle policies](../../services/s3.md#lifecycle) |
| [ストレージ](../../services/storage.md) | [Amazon EBS](../../services/storage.md#ebs-encryption)、[Amazon EFS](../../services/storage.md#efs-settings) |
| [EC2 と Elastic Beanstalk](../../services/ec2-beanstalk.md) | [Amazon EC2](../../services/ec2-beanstalk.md) |
| [コンテナ](../../services/containers.md) | [Amazon ECR](../../services/containers.md#ecr)、[Amazon ECS](../../services/containers.md#ecs)、[Amazon EKS](../../services/containers.md#eks)、[AWS Fargate](../../services/containers.md#fargate-vs-ec2) |

## セキュリティ {#group-iam}

| 解説ページ | この試験の対象サービス |
|---|---|
| [IAM と STS](../../services/iam.md) | [IAM](../../services/iam.md) |
| [Cognito](../../services/cognito.md) | [Amazon Cognito](../../services/cognito.md) |
| [KMS と暗号化](../../services/kms.md) | [AWS Encryption SDK](../../services/kms.md#encryption-sdk)、[AWS KMS](../../services/kms.md) |
| [シークレットと設定](../../services/secrets.md) | [AWS AppConfig](../../services/secrets.md#appconfig)、[AWS Secrets Manager](../../services/secrets.md#secrets-manager) |
| [証明書と WAF](../../services/certificates.md) | [AWS WAF](../../services/certificates.md#waf) |

## デプロイと運用 {#group-cicd}

| 解説ページ | この試験の対象サービス |
|---|---|
| [CI/CD](../../services/cicd.md) | [AWS Amplify](../../services/cicd.md#amplify)、[AWS CodeArtifact](../../services/cicd.md#codeartifact)、[AWS CodeBuild](../../services/cicd.md#codebuild)、[AWS CodeDeploy](../../services/cicd.md#codedeploy)、[AWS CodePipeline](../../services/cicd.md#codepipeline) |
| [IaC と CLI](../../services/iac.md) | [AWS CDK](../../services/iac.md#cdk)、[AWS CLI](../../services/iac.md#aws-cli)、[AWS CloudFormation](../../services/iac.md#cloudformation-template) |
| [オブザーバビリティ](../../services/observability.md) | [Amazon CloudWatch](../../services/observability.md)、[Amazon CloudWatch Logs](../../services/observability.md#cloudwatch-logs)、[AWS CloudTrail](../../services/observability.md#cloudtrail)、[AWS X-Ray](../../services/observability.md#xray) |
| [ネットワークと配信](../../services/networking.md) | [Amazon CloudFront](../../services/networking.md#cloudfront)、[Amazon Route 53](../../services/networking.md#route53)、[Amazon VPC](../../services/networking.md#vpc)、[AWS Lambda@Edge](../../services/networking.md#edge-functions)、[AWS PrivateLink](../../services/networking.md#vpc-endpoints)、[Elastic Load Balancing](../../services/networking.md#elb) |

## クラウドの基礎とガバナンス {#group-cloud-foundations}

| 解説ページ | この試験の対象サービス |
|---|---|
| [クラウドの基礎](../../services/cloud-foundations.md) | [AWS Outposts](../../services/cloud-foundations.md#outposts)、[AWS Wavelength](../../services/cloud-foundations.md#wavelength)、[AWS Well-Architected Tool](../../services/cloud-foundations.md#wa-tool) |
| [ガバナンス](../../services/governance.md) | [AWS Service Catalog](../../services/governance.md#service-catalog) |
| [コスト管理](../../services/cost-management.md) | [AWS Cost Anomaly Detection](../../services/cost-management.md#cost-anomaly-detection)、[AWS Cost Explorer](../../services/cost-management.md#cost-explorer) |
| [運用](../../services/operations.md) | [Amazon CloudWatch Synthetics](../../services/operations.md#synthetics)、[Amazon EC2](../../services/operations.md#ec2-operations)、[Amazon Managed Grafana](../../services/operations.md#managed-grafana)、[AWS Auto Scaling](../../services/operations.md#auto-scaling)、[AWS Chatbot](../../services/operations.md#q-chat)、[AWS Systems Manager](../../services/operations.md#systems-manager) |

## 高度なネットワークとセキュリティ {#group-network-connectivity}

| 解説ページ | この試験の対象サービス |
|---|---|
| [ネットワーク接続](../../services/network-connectivity.md) | [AWS Global Accelerator](../../services/network-connectivity.md#global-accelerator) |
| [脅威検出とインシデント対応](../../services/threat-detection.md) | [Amazon Macie](../../services/threat-detection.md#macie) |
| [ID とディレクトリ](../../services/identity-directory.md) | [IAM Access Analyzer](../../services/identity-directory.md#access-analyzer)、[IAM Identity Center](../../services/identity-directory.md#identity-center) |

## データと分析 {#group-data-engineering}

| 解説ページ | この試験の対象サービス |
|---|---|
| [データエンジニアリング](../../services/data-engineering.md) | [Amazon AppFlow](../../services/data-engineering.md#appflow)、[Amazon EMR](../../services/data-engineering.md#emr)、[Amazon Managed Streaming for Apache Kafka](../../services/data-engineering.md#msk)、[Amazon Quick Sight](../../services/data-engineering.md#quick-sight)、[AWS Glue](../../services/data-engineering.md#glue) |
| [専用データベース](../../services/databases-specialized.md) | [Amazon DocumentDB](../../services/databases-specialized.md#documentdb)、[Amazon Neptune](../../services/databases-specialized.md#neptune) |

## 移行と事業継続 {#group-migration}

| 解説ページ | この試験の対象サービス |
|---|---|
| [移行](../../services/migration.md) | [AWS DataSync](../../services/migration.md#datasync)、[AWS Transfer Family](../../services/migration.md#transfer-family) |

## AI {#group-ai}

| 解説ページ | この試験の対象サービス |
|---|---|
| [AI サービス](../../services/ai.md) | [Amazon Bedrock](../../services/ai.md)、[Amazon Q Developer](../../services/ai.md#q-developer)、[Amazon Quick](../../services/ai.md#quick)、[Kiro](../../services/ai.md#kiro) |
| [SageMaker](../../services/sagemaker.md) | [Amazon SageMaker AI](../../services/sagemaker.md)、[Amazon SageMaker Clarify](../../services/sagemaker.md#clarify)、[Amazon SageMaker Data Wrangler](../../services/sagemaker.md#data-wrangler)、[Amazon SageMaker Ground Truth](../../services/sagemaker.md#ground-truth)、[Amazon SageMaker JumpStart](../../services/sagemaker.md#jumpstart)、[Amazon SageMaker Model Monitor](../../services/sagemaker.md#model-monitor)、[Amazon SageMaker Model Registry](../../services/sagemaker.md#model-registry)、[Amazon SageMaker Neo](../../services/sagemaker.md#neo)、[Amazon SageMaker Processing](../../services/sagemaker.md#processing)、[Amazon SageMaker Unified Studio](../../services/sagemaker.md#unified-studio) |
| [マネージド AI サービス](../../services/ai-managed-services.md) | [Amazon Augmented AI](../../services/ai-managed-services.md#a2i)、[Amazon Comprehend](../../services/ai-managed-services.md#comprehend)、[Amazon Kendra](../../services/ai-managed-services.md#kendra)、[Amazon Lex](../../services/ai-managed-services.md#lex)、[Amazon Q Business](../../services/ai-managed-services.md#q-business)、[Amazon Rekognition](../../services/ai-managed-services.md#rekognition)、[Amazon Textract](../../services/ai-managed-services.md#textract)、[Amazon Transcribe](../../services/ai-managed-services.md#transcribe) |
| [生成 AI アプリケーション](../../services/genai-apps.md) | [Amazon Bedrock](../../services/genai-apps.md)、[Amazon Bedrock AgentCore](../../services/genai-apps.md#agentcore)、[Amazon Bedrock Knowledge Bases](../../services/genai-apps.md#knowledge-bases)、[Amazon Bedrock Prompt Flows](../../services/genai-apps.md#flows)、[Amazon Bedrock Prompt Management](../../services/genai-apps.md#prompt-management)、[Amazon Titan](../../services/genai-apps.md#nova-titan) |

## その他 {#group-other-services}

| 解説ページ | この試験の対象サービス |
|---|---|
| [その他のサービス](../../services/other-services.md) | [Amazon Connect](../../services/other-services.md#connect)、[AWS App Runner](../../services/other-services.md#app-runner)、[AWS AppSync](../../services/other-services.md#appsync) |

## 解説で参照しているページ {#related}

公式の対象サービスの一覧には載っていませんが、このコースの解説で参照しているページです。

- [AI の基礎、責任ある AI、AI 戦略](../../services/ai-fundamentals.md)
