# 分野4: トラブルシューティングと最適化

C03 の配点は **22%** で、C02 の 18% から増えました。原因の調査、オブザーバビリティ、性能の最適化を扱います。

## タスク 4.1: 根本原因の分析を支援する {#task-4-1}

[![オブザーバビリティの3つのシグナル](../../assets/diagrams/observability-signals.png)](../../assets/diagrams/observability-signals.png)

### 4.1.1 コードとサービス連携のデバッグ {#skill-4-1-1}

エラーコードから、原因がアプリ側、権限、スロットリングのどれかを切り分けます。

詳細: [コードのデバッグ](../../services/observability.md#debug-code)、[サービス連携のデバッグ](../../services/observability.md#debug-integration)、[エラーコード](../../services/observability.md#error-codes)

### 4.1.2 メトリクス、ログ、トレースの読み取り {#skill-4-1-2}

メトリクスで異常に気づき、トレースで遅い箇所を特定し、ログで原因を確認します。

詳細: [シグナルの読み方](../../services/observability.md#interpret-signals)、[サービスマップ](../../services/observability.md#service-map)

### 4.1.3 ログのクエリ {#skill-4-1-3}

CloudWatch Logs Insights で検索や集計をします。S3 に保存したログは Athena でも検索できます。

詳細: [Logs Insights](../../services/observability.md#logs-insights)、[Athena](../../services/streaming.md)

### 4.1.4 デプロイの失敗の調査 {#skill-4-1-4}

CodeBuild のログ、CodeDeploy のデプロイイベント、CloudFormation のスタックイベントを確認します。

詳細: [デプロイの調査](../../services/cicd.md#troubleshooting-deployments)、[よくある失敗](../../services/iac.md#common-failures)

### 4.1.5 AI によるエラー分析 {#skill-4-1-5}

エラーの分析と対処案の作成に AI ツールを使います。

詳細: [AI によるトラブルシューティング](../../services/ai.md#ai-troubleshooting)

## タスク 4.2: ログ、モニタリング、オブザーバビリティ {#task-4-2}

### 4.2.1 ログ戦略 {#skill-4-2-1}

JSON の構造化ログにすると、Logs Insights で項目ごとに検索できます。

詳細: [構造化ログ](../../services/observability.md#structured-logging)、[ログ戦略](../../services/observability.md#logging-strategy)、[イベントの記録](../../services/observability.md#structured-events)

### 4.2.2 カスタムメトリクス {#skill-4-2-2}

`PutMetricData` で送るか、埋め込みメトリクスフォーマット（EMF）でログから生成します。Lambda では、API 呼び出しの増えない EMF が向いています。

詳細: [PutMetricData](../../services/observability.md#put-metric-data)、[EMF](../../services/observability.md#emf)

### 4.2.3 通知 {#skill-4-2-3}

CloudWatch アラームや EventBridge のルールから SNS で通知します。クォータの上限やデプロイ完了の通知も同じ考え方です。

詳細: [アラート](../../services/observability.md#alerts)、[クォータ](../../services/observability.md#quota-alerts)、[デプロイ](../../services/observability.md#deployment-alerts)

### 4.2.4 トレース {#skill-4-2-4}

X-Ray のアノテーションは検索に使え、メタデータは検索に使えません。X-Ray SDK とデーモンは保守モードに入っていて、OpenTelemetry（ADOT）が推奨されています。

詳細: [X-Ray](../../services/observability.md#xray)、[アノテーションとメタデータ](../../services/observability.md#annotations-metadata)、[OpenTelemetry](../../services/observability.md#xray-opentelemetry)、[Lambda のアクティブトレース](../../services/observability.md#lambda-active-tracing)

### 4.2.5 ワークロードの状態監視 {#skill-4-2-5}

ALB のヘルスチェック、Kubernetes の liveness プローブと readiness プローブを区別します。liveness は再起動の判断、readiness はトラフィックを流すかどうかの判断に使います。

詳細: [ヘルスチェック](../../services/observability.md#health-checks)、[ALB](../../services/networking.md#alb-health-checks)、[プローブ](../../services/containers.md#probes)

## タスク 4.3: アプリケーションを最適化する {#task-4-3}

### 4.3.1 同時実行 {#skill-4-3-1}

Lambda のコールドスタート対策にはプロビジョニング済み同時実行を、他の関数の影響を防ぐには予約済み同時実行を使います。データベース接続が多すぎるときは RDS Proxy やコネクションプーリングを使います。

詳細: [Lambda の同時実行](../../services/lambda.md#concurrency)、[Lambda の接続管理](../../services/lambda.md#connection-pooling)、[Auto Scaling](../../services/ec2-beanstalk.md#auto-scaling)、[コネクションプーリング](../../services/databases.md#connection-pooling)、[RDS Proxy](../../services/databases.md#rds-proxy)

### 4.3.2 メモリとコンピューティング能力 {#skill-4-3-2}

Lambda はメモリを増やすと CPU も増え、実行時間が短くなって費用が下がることもあります。

詳細: [Lambda のメモリ調整](../../services/lambda.md#memory-tuning)、[インスタンスタイプ](../../services/ec2-beanstalk.md#instance-types)、[サイズの決め方](../../services/ec2-beanstalk.md#sizing)

### 4.3.3 メッセージングの最適化 {#skill-4-3-3}

SNS のフィルターポリシーで不要な配信を減らし、SQS のロングポーリングとバッチ処理で API 呼び出しを減らします。

詳細: [最適化](../../services/messaging.md#optimization)、[ファンアウト](../../services/messaging.md#fanout)、[フィルターポリシー](../../services/messaging.md#filter-policies)

### 4.3.4 キャッシュ {#skill-4-3-4}

| 対象 | サービス |
|---|---|
| DynamoDB の読み取り | DAX |
| データベースのクエリ結果、セッション | ElastiCache |
| 静的コンテンツ、API の応答 | CloudFront |
| API の応答 | API Gateway のキャッシュ |

詳細: [キャッシュの比較](../../services/databases.md#cache-comparison)、[DAX](../../services/dynamodb.md#dax)、[CloudFront のキャッシュキー](../../services/networking.md#cache-keys)、[ヘッダーによるキャッシュ](../../services/networking.md#header-caching)

### 4.3.5 ボトルネックの検出 {#skill-4-3-5}

CloudWatch のメトリクスとログから遅い処理を探します。

詳細: [性能](../../services/observability.md#performance)、[メトリクス](../../services/observability.md#bottleneck-metrics)、[ログ](../../services/observability.md#logs-bottlenecks)

### 4.3.6 AI による最適化 {#skill-4-3-6}

性能のボトルネックの検出、リソース使用量やコードの改善に AI ツールを使います。

詳細: [AI による最適化](../../services/ai.md#ai-optimization)

## 確認問題 {#self-check}

??? question "問1: X-Ray で、ユーザー ID を指定してトレースを検索したいです。何に記録しますか？"
    アノテーションです。メタデータは検索に使えません。

??? question "問2: Lambda から多数のカスタムメトリクスを、遅延を増やさずに送りたいです。どうしますか？"
    埋め込みメトリクスフォーマット（EMF）でログに書き出します。

??? question "問3: Lambda の同時実行が増えると、RDS の接続数が上限に達します。どうしますか？"
    RDS Proxy を使って接続を共有します。ハンドラーの外で接続を再利用することも有効です。

??? question "問4: Lambda のコールドスタートで応答が遅くなります。必ず初期化済みの環境を用意するには？"
    プロビジョニング済み同時実行を設定します。

??? question "問5: DynamoDB の読み取りをコードの変更を抑えてマイクロ秒単位に速くしたいです。何を使いますか？"
    DAX です。

??? question "問6: 特定の種類の SNS メッセージだけを、ある SQS キューで受け取りたいです。どうしますか？"
    サブスクリプションにフィルターポリシーを設定します。
