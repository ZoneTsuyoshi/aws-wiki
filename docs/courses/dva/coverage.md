# スキル対応表

公式試験ガイドの全スキルと、このwikiのページの対応です。スキル名は日本語で要約しています。正確な文言は[試験ガイド](https://docs.aws.amazon.com/aws-certification/latest/developer-associate-03/developer-associate-03.html)で確認してください。

## DVA-C03（72スキル） {#c03}

C03 の各スキルは分野ページに見出しがあり、そこから詳しい解説へ進めます。

| 分野 | タスク | スキル |
|---|---|---|
| 1 | 1.1 アプリケーションの開発 | [1.1.1](domain1.md#skill-1-1-1) [1.1.2](domain1.md#skill-1-1-2) [1.1.3](domain1.md#skill-1-1-3) [1.1.4](domain1.md#skill-1-1-4) [1.1.5](domain1.md#skill-1-1-5) [1.1.6](domain1.md#skill-1-1-6) [1.1.7](domain1.md#skill-1-1-7) [1.1.8](domain1.md#skill-1-1-8) [1.1.9](domain1.md#skill-1-1-9) [1.1.10](domain1.md#skill-1-1-10) |
| 1 | 1.2 Lambda | [1.2.1](domain1.md#skill-1-2-1) [1.2.2](domain1.md#skill-1-2-2) [1.2.3](domain1.md#skill-1-2-3) [1.2.4](domain1.md#skill-1-2-4) |
| 1 | 1.3 データストア | [1.3.1](domain1.md#skill-1-3-1) [1.3.2](domain1.md#skill-1-3-2) [1.3.3](domain1.md#skill-1-3-3) [1.3.4](domain1.md#skill-1-3-4) |
| 2 | 2.1 認証と認可 | [2.1.1](domain2.md#skill-2-1-1) [2.1.2](domain2.md#skill-2-1-2) [2.1.3](domain2.md#skill-2-1-3) [2.1.4](domain2.md#skill-2-1-4) [2.1.5](domain2.md#skill-2-1-5) [2.1.6](domain2.md#skill-2-1-6) [2.1.7](domain2.md#skill-2-1-7) |
| 2 | 2.2 暗号化と機密データ | [2.2.1](domain2.md#skill-2-2-1) [2.2.2](domain2.md#skill-2-2-2) [2.2.3](domain2.md#skill-2-2-3) [2.2.4](domain2.md#skill-2-2-4) [2.2.5](domain2.md#skill-2-2-5) [2.2.6](domain2.md#skill-2-2-6) [2.2.7](domain2.md#skill-2-2-7) |
| 2 | 2.3 AI のリスク対策 | [2.3.1](domain2.md#skill-2-3-1) [2.3.2](domain2.md#skill-2-3-2) [2.3.3](domain2.md#skill-2-3-3) [2.3.4](domain2.md#skill-2-3-4) [2.3.5](domain2.md#skill-2-3-5) |
| 3 | 3.1 成果物の準備 | [3.1.1](domain3.md#skill-3-1-1) [3.1.2](domain3.md#skill-3-1-2) [3.1.3](domain3.md#skill-3-1-3) [3.1.4](domain3.md#skill-3-1-4) [3.1.5](domain3.md#skill-3-1-5) |
| 3 | 3.2 テスト | [3.2.1](domain3.md#skill-3-2-1) [3.2.2](domain3.md#skill-3-2-2) [3.2.3](domain3.md#skill-3-2-3) [3.2.4](domain3.md#skill-3-2-4) [3.2.5](domain3.md#skill-3-2-5) |
| 3 | 3.3 CI/CD | [3.3.1](domain3.md#skill-3-3-1) [3.3.2](domain3.md#skill-3-3-2) [3.3.3](domain3.md#skill-3-3-3) [3.3.4](domain3.md#skill-3-3-4) [3.3.5](domain3.md#skill-3-3-5) [3.3.6](domain3.md#skill-3-3-6) [3.3.7](domain3.md#skill-3-3-7) [3.3.8](domain3.md#skill-3-3-8) [3.3.9](domain3.md#skill-3-3-9) |
| 4 | 4.1 根本原因の分析 | [4.1.1](domain4.md#skill-4-1-1) [4.1.2](domain4.md#skill-4-1-2) [4.1.3](domain4.md#skill-4-1-3) [4.1.4](domain4.md#skill-4-1-4) [4.1.5](domain4.md#skill-4-1-5) |
| 4 | 4.2 オブザーバビリティ | [4.2.1](domain4.md#skill-4-2-1) [4.2.2](domain4.md#skill-4-2-2) [4.2.3](domain4.md#skill-4-2-3) [4.2.4](domain4.md#skill-4-2-4) [4.2.5](domain4.md#skill-4-2-5) |
| 4 | 4.3 最適化 | [4.3.1](domain4.md#skill-4-3-1) [4.3.2](domain4.md#skill-4-3-2) [4.3.3](domain4.md#skill-4-3-3) [4.3.4](domain4.md#skill-4-3-4) [4.3.5](domain4.md#skill-4-3-5) [4.3.6](domain4.md#skill-4-3-6) |

## DVA-C02（101スキル） {#c02}

C02 は番号の付け方が C03 と異なるので、直接解説ページにつなげています。**最終受験日は 2026年11月30日**です。

### 分野1: AWS サービスによる開発 {#c02-domain1}

| スキル | 内容 | ページ |
|---|---|---|
| 1.1.1 | アーキテクチャパターン | [パターン](../../services/sdk-resilience.md#architectural-patterns)、[オーケストレーション](../../services/step-functions.md#orchestration-choreography) |
| 1.1.2 | ステートフルとステートレス | [比較](../../services/sdk-resilience.md#stateful-stateless) |
| 1.1.3 | 密結合と疎結合 | [疎結合](../../services/messaging.md#coupling) |
| 1.1.4 | 同期と非同期 | [比較](../../services/messaging.md#sync-async) |
| 1.1.5 | 耐障害性のあるアプリ | [再試行](../../services/sdk-resilience.md#retries)、[冪等性](../../services/sdk-resilience.md#idempotency) |
| 1.1.6 | API の作成と保守 | [変換](../../services/api-gateway.md#transformations)、[検証](../../services/api-gateway.md#request-validation)、[ステータスコード](../../services/api-gateway.md#status-override) |
| 1.1.7 | 単体テスト | [単体テスト](../../services/sdk-resilience.md#unit-testing) |
| 1.1.8 | メッセージング | [SQS](../../services/messaging.md#sqs)、[SNS](../../services/messaging.md#sns) |
| 1.1.9 | API と SDK | [SDK の基本](../../services/sdk-resilience.md#sdk-basics) |
| 1.1.10 | ストリーミング | [Kinesis](../../services/streaming.md#kinesis-data-streams)、[Firehose](../../services/streaming.md#firehose) |
| 1.1.11 | Amazon Q Developer | [Q Developer](../../services/ai.md#q-developer)、[Kiro との比較](../../services/ai.md#kiro-vs-q) |
| 1.1.12 | EventBridge | [EventBridge](../../services/messaging.md#eventbridge) |
| 1.1.13 | 外部サービス連携の耐障害性 | [外部サービス](../../services/sdk-resilience.md#third-party)、[サーキットブレーカー](../../services/sdk-resilience.md#circuit-breaker) |
| 1.2.1 | VPC 内へのアクセス | [VPC アクセス](../../services/lambda.md#vpc-access) |
| 1.2.2 | Lambda の設定 | [設定](../../services/lambda.md#configuration)、[呼び出し方式](../../services/lambda.md#invocation-types) |
| 1.2.3 | イベントとエラーの処理 | [送信先と DLQ](../../services/lambda.md#destinations-dlq)、[部分失敗](../../services/lambda.md#partial-batch-response) |
| 1.2.4 | テストコード | [Lambda のテスト](../../services/lambda.md#testing)、[単体テスト](../../services/iac.md#unit-tests) |
| 1.2.5 | サービスとの統合 | [イベントソースマッピング](../../services/lambda.md#event-source-mapping) |
| 1.2.6 | 性能の調整 | [性能](../../services/lambda.md#performance) |
| 1.2.7 | ほぼリアルタイムの処理 | [リアルタイム処理](../../services/lambda.md#near-real-time)、[ストリーム](../../services/streaming.md#lambda-streams) |
| 1.3.1 | 高カーディナリティのキー | [キー設計](../../services/dynamodb.md#high-cardinality) |
| 1.3.2 | 整合性モデル | [整合性](../../services/dynamodb.md#read-consistency) |
| 1.3.3 | Query と Scan | [比較](../../services/dynamodb.md#query-vs-scan) |
| 1.3.4 | キーとインデックス | [キー](../../services/dynamodb.md#keys)、[インデックス](../../services/dynamodb.md#indexes) |
| 1.3.5 | データの永続化 | [シリアライズ](../../services/sdk-resilience.md#dynamodb-serialization) |
| 1.3.6 | データストアの利用と保守 | [DynamoDB の容量](../../services/dynamodb.md#capacity)、[RDS](../../services/databases.md#rds)、[Aurora](../../services/databases.md#aurora) |
| 1.3.7 | ライフサイクル | [S3](../../services/s3.md#lifecycle)、[保持](../../services/storage.md#retention) |
| 1.3.8 | キャッシュサービス | [戦略](../../services/databases.md#caching-strategies)、[ElastiCache](../../services/databases.md#elasticache) |
| 1.3.9 | 専用のデータストア | [OpenSearch](../../services/databases.md#opensearch)、[用途](../../services/streaming.md#specialized-store) |

### 分野2: セキュリティ {#c02-domain2}

| スキル | 内容 | ページ |
|---|---|---|
| 2.1.1 | フェデレーション | [IAM](../../services/iam.md#federation)、[Cognito](../../services/cognito.md#federation) |
| 2.1.2 | ベアラートークン | [ベアラートークン](../../services/cognito.md#bearer-tokens)、[JWT の検証](../../services/cognito.md#jwt-verification) |
| 2.1.3 | プログラムによるアクセス | [認証情報](../../services/iam.md#programmatic-access) |
| 2.1.4 | 認証された呼び出し | [SigV4](../../services/iam.md#sigv4) |
| 2.1.5 | ロールの引き受け | [AssumeRole](../../services/iam.md#assume-role) |
| 2.1.6 | プリンシパルの権限 | [プリンシパル](../../services/iam.md#principals)、[評価](../../services/iam.md#policy-evaluation) |
| 2.1.7 | アプリのきめ細かい認可 | [アプリの認可](../../services/cognito.md#app-authorization) |
| 2.1.8 | マイクロサービス間の認証 | [サービス間認証](../../services/iam.md#microservices-auth) |
| 2.2.1 | 保存時と転送時 | [暗号化](../../services/kms.md#at-rest-in-transit) |
| 2.2.2 | 証明書の管理 | [ACM](../../services/certificates.md#acm)、[Private CA](../../services/certificates.md#private-ca) |
| 2.2.3 | クライアント側とサーバー側 | [比較](../../services/kms.md#client-vs-server-side) |
| 2.2.4 | キーの利用 | [キーの使い方](../../services/kms.md#use-keys) |
| 2.2.5 | 開発用の証明書と SSH キー | [生成](../../services/certificates.md#dev-certs-ssh) |
| 2.2.6 | アカウントをまたぐ暗号化 | [クロスアカウント](../../services/kms.md#cross-account) |
| 2.2.7 | キーのローテーション | [ローテーション](../../services/kms.md#key-rotation) |
| 2.3.1 | データの分類 | [分類](../../services/secrets.md#data-classification) |
| 2.3.2 | 環境変数の暗号化 | [Lambda](../../services/lambda.md#encrypting-env-vars)、[KMS](../../services/kms.md#lambda-env-encryption) |
| 2.3.3 | シークレット管理 | [Secrets Manager](../../services/secrets.md#secrets-manager)、[Parameter Store](../../services/secrets.md#parameter-store) |
| 2.3.4 | サニタイズ | [サニタイズ](../../services/secrets.md#sanitization-masking) |
| 2.3.5 | アプリでのマスキング | [マスキング](../../services/secrets.md#app-masking) |
| 2.3.6 | マルチテナント | [シークレットと権限](../../services/secrets.md#multi-tenant)、[データベース](../../services/databases.md#multi-tenant) |

### 分野3: デプロイ {#c02-domain3}

| スキル | 内容 | ページ |
|---|---|---|
| 3.1.1 | 依存関係の管理 | [パッケージング](../../services/lambda.md#packaging)、[イメージのタグ](../../services/containers.md#image-tags) |
| 3.1.2 | ディレクトリ構成 | [SAM](../../services/iac.md#project-structure)、[Beanstalk](../../services/ec2-beanstalk.md#directory-structure) |
| 3.1.3 | コードリポジトリ | [リポジトリ](../../services/cicd.md#repositories) |
| 3.1.4 | リソース要件 | [インスタンス](../../services/ec2-beanstalk.md#instance-types)、[Fargate と EC2](../../services/containers.md#fargate-vs-ec2) |
| 3.1.5 | 環境ごとの設定 | [環境別の設定](../../services/secrets.md#environment-config)、[AppConfig](../../services/secrets.md#appconfig) |
| 3.2.1 | デプロイ済みコードのテスト | [統合テスト](../../services/iac.md#integration-tests) |
| 3.2.2 | 統合テストとモック | [Mock 統合](../../services/api-gateway.md#mock-integration) |
| 3.2.3 | 開発用エンドポイント | [テスト](../../services/api-gateway.md#test-endpoints)、[ステージ](../../services/api-gateway.md#stages) |
| 3.2.4 | 既存環境の更新 | [ステージへのデプロイ](../../services/iac.md#deploy-stages) |
| 3.2.5 | イベント駆動アプリのテスト | [テスト](../../services/iac.md#event-driven-tests) |
| 3.3.1 | テストイベント | [テストイベント](../../services/iac.md#test-events) |
| 3.3.2 | API のデプロイ | [ステージ](../../services/api-gateway.md#stages) |
| 3.3.3 | 承認済みバージョンの環境 | [Lambda エイリアス](../../services/lambda.md#alias-environments)、[イメージのタグ](../../services/containers.md#environments-image-tags)、[環境](../../services/cicd.md#app-environments)、[Copilot](../../services/containers.md#copilot) |
| 3.3.4 | IaC の実装 | [CloudFormation](../../services/iac.md#cloudformation-template)、[SAM CLI](../../services/iac.md#sam-cli) |
| 3.3.5 | 環境の管理 | [ステージ](../../services/api-gateway.md#stages)、[ステージ変数](../../services/api-gateway.md#stage-variables) |
| 3.3.6 | Q Developer によるテスト生成 | [AI によるテスト](../../services/ai.md#ai-testing) |
| 3.4.1 | Lambda のパッケージング | [パッケージング](../../services/lambda.md#packaging) |
| 3.4.2 | ステージとカスタムドメイン | [ステージ](../../services/api-gateway.md#stages)、[カスタムドメイン](../../services/api-gateway.md#custom-domains) |
| 3.4.3 | IaC の更新 | [更新](../../services/iac.md#update-templates)、[変更セット](../../services/iac.md#change-sets) |
| 3.4.4 | 環境の管理 | [環境](../../services/cicd.md#app-environments)、[Beanstalk](../../services/ec2-beanstalk.md#beanstalk-environments) |
| 3.4.5 | デプロイ戦略の利用 | [デプロイ戦略](../../services/cicd.md#deployment-strategies)、[Beanstalk](../../services/ec2-beanstalk.md#deployment-policies) |
| 3.4.6 | コミットを起点にする | [トリガー](../../services/cicd.md#commit-triggers) |
| 3.4.7 | 複数環境へのデプロイ | [複数環境](../../services/cicd.md#multi-environment) |
| 3.4.8 | ロールバック | [ロールバック](../../services/cicd.md#rollback) |
| 3.4.9 | ラベルとブランチ | [ブランチとタグ](../../services/cicd.md#branches-tags) |
| 3.4.10 | ランタイム設定 | [ステージ変数](../../services/api-gateway.md#stage-variables) |
| 3.4.11 | デプロイ戦略の設定 | [デプロイ設定](../../services/cicd.md#deployment-configs) |

### 分野4: トラブルシューティングと最適化 {#c02-domain4}

| スキル | 内容 | ページ |
|---|---|---|
| 4.1.1 | デバッグ | [コードのデバッグ](../../services/observability.md#debug-code) |
| 4.1.2 | メトリクス、ログ、トレース | [読み方](../../services/observability.md#interpret-signals) |
| 4.1.3 | ログのクエリ | [Logs Insights](../../services/observability.md#logs-insights) |
| 4.1.4 | カスタムメトリクス（EMF） | [EMF](../../services/observability.md#emf) |
| 4.1.5 | ダッシュボード | [ダッシュボード](../../services/observability.md#dashboards) |
| 4.1.6 | デプロイの失敗 | [調査](../../services/cicd.md#troubleshooting-deployments) |
| 4.1.7 | サービス連携のデバッグ | [連携のデバッグ](../../services/observability.md#debug-integration) |
| 4.2.1 | ログ、モニタリング、オブザーバビリティ | [違い](../../services/observability.md#logging-monitoring-observability) |
| 4.2.2 | ログ戦略 | [ログ戦略](../../services/observability.md#logging-strategy) |
| 4.2.3 | カスタムメトリクスの送信 | [PutMetricData](../../services/observability.md#put-metric-data) |
| 4.2.4 | トレースのアノテーション | [アノテーションとメタデータ](../../services/observability.md#annotations-metadata) |
| 4.2.5 | 通知 | [アラート](../../services/observability.md#alerts) |
| 4.2.6 | トレース | [X-Ray](../../services/observability.md#xray) |
| 4.2.7 | 構造化ログ | [構造化ログ](../../services/observability.md#structured-events) |
| 4.2.8 | ヘルスチェックとプローブ | [ヘルスチェック](../../services/observability.md#health-checks)、[プローブ](../../services/containers.md#probes) |
| 4.3.1 | 同時実行 | [Lambda](../../services/lambda.md#concurrency) |
| 4.3.2 | 性能の計測 | [プロファイリング](../../services/observability.md#profiling) |
| 4.3.3 | 最小のメモリと能力 | [Lambda](../../services/lambda.md#memory-tuning)、[EC2](../../services/ec2-beanstalk.md#sizing) |
| 4.3.4 | サブスクリプションフィルター | [フィルターポリシー](../../services/messaging.md#filter-policies) |
| 4.3.5 | ヘッダーによるキャッシュ | [CloudFront](../../services/networking.md#header-caching)、[API Gateway](../../services/api-gateway.md#cache-keys) |
| 4.3.6 | アプリでのキャッシュ | [キャッシュ](../../services/databases.md#application-caching) |
| 4.3.7 | リソース使用量の最適化 | [最適化](../../services/observability.md#resource-optimization) |
| 4.3.8 | 性能の問題の分析 | [性能](../../services/observability.md#performance) |
| 4.3.9 | ログからのボトルネック特定 | [ログ](../../services/observability.md#logs-bottlenecks) |
