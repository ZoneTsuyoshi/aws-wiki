# 分野1: AWS サービスによる開発

C03 の配点は **30%** で、4分野の中で最大です。疎結合の設計、Lambda、データストアの3つが中心です。

## タスク 1.1: AWS 上のアプリケーションのコードを開発する {#task-1-1}

### 1.1.1 密結合と疎結合 {#skill-1-1-1}

呼び出し先が止まると呼び出し元も止まるのが密結合です。キューやイベントを間に置くと、片方が止まっても処理を続けられます。

- 負荷の吸収や後からの処理には SQS を使います。
- 複数の宛先への配信には SNS か EventBridge を使います。

詳細: [疎結合](../../services/messaging.md#coupling)

### 1.1.2 同期と非同期の選択 {#skill-1-1-2}

利用者がすぐ結果を必要とするなら同期、時間がかかる処理や失敗時に再試行したい処理なら非同期にします。

| パターン | 代表例 | 向いている場面 |
|---|---|---|
| 同期 | API Gateway + Lambda | 画面にすぐ結果を返す |
| 非同期（キュー） | SQS + Lambda | 重い処理、負荷の平準化 |
| イベント駆動 | EventBridge | 発生元と処理側を切り離す |

詳細: [同期と非同期](../../services/messaging.md#sync-async)

### 1.1.3 耐障害性の高いアプリケーション {#skill-1-1-3}

一時的な失敗には、指数バックオフとジッターを使って再試行します。再試行しても安全なように、処理は冪等にします。依存先が長く止まるときはサーキットブレーカーで呼び出しを止め、機能を縮小して動かし続けます。

詳細: [再試行](../../services/sdk-resilience.md#retries)、[タイムアウト](../../services/sdk-resilience.md#timeouts)、[冪等性](../../services/sdk-resilience.md#idempotency)、[サーキットブレーカー](../../services/sdk-resilience.md#circuit-breaker)、[機能の縮退](../../services/sdk-resilience.md#graceful-degradation)

### 1.1.4 API の作成、拡張、保守 {#skill-1-1-4}

API Gateway では、マッピングテンプレートでリクエストとレスポンスを変換し、リクエストの検証で不正な入力をバックエンドの手前で止めます。ステータスコードの上書きもできます。

詳細: [変換](../../services/api-gateway.md#transformations)、[リクエストの検証](../../services/api-gateway.md#request-validation)、[ステータスコードの上書き](../../services/api-gateway.md#status-override)

### 1.1.5 API と SDK を使ったコード {#skill-1-1-5}

SDK のページネーション、ウェイター、エラー処理の使い方を押さえます。認証情報はコードに書かず、ロールから取得します。

詳細: [SDK の基本](../../services/sdk-resilience.md#sdk-basics)、[認証情報](../../services/iam.md#programmatic-access)

### 1.1.6 ストリーミングデータの管理 {#skill-1-1-6}

自分のコードで順序どおりに読むなら Kinesis Data Streams、S3 などへ届けるだけなら Amazon Data Firehose を選びます。パーティションキーが偏ると、特定のシャードだけ負荷が高くなります。

詳細: [Kinesis Data Streams](../../services/streaming.md#kinesis-data-streams)、[Firehose](../../services/streaming.md#firehose)、[選び方](../../services/streaming.md#choosing)

### 1.1.7 シリアライズとデシリアライズ {#skill-1-1-7}

JSON に変換できない型や、DynamoDB の型の扱いでエラーになりやすい点を押さえます。

詳細: [シリアライズ](../../services/sdk-resilience.md#serialization)、[DynamoDB の場合](../../services/sdk-resilience.md#dynamodb-serialization)

### 1.1.8 イベント駆動パターン {#skill-1-1-8}

| サービス | 主な役割 |
|---|---|
| EventBridge | 内容に応じた振り分け、スケジュール、SaaS との連携 |
| S3 イベント通知 | オブジェクトの作成や削除を起点に処理する |
| SQS | 処理側が自分のペースで取り出す |
| SNS | 複数の宛先へ同時に配信する（ファンアウト） |

詳細: [EventBridge](../../services/messaging.md#eventbridge)、[S3 イベント通知](../../services/messaging.md#s3-events)、[SQS](../../services/messaging.md#sqs)、[SNS](../../services/messaging.md#sns)

### 1.1.9 AI による開発支援ツール {#skill-1-1-9}

Kiro の仕様駆動開発を中心に、コード生成、レビュー、補完、リファクタリング、セキュリティスキャンの支援を押さえます。Amazon Q Developer は提供の縮小が進んでいるので、状況を確認してください。

詳細: [AI 開発ツール](../../services/ai.md#ai-dev-tools)、[Kiro](../../services/ai.md#kiro)、[Q Developer](../../services/ai.md#q-developer)

### 1.1.10 マネージド AI サービスの組み込み {#skill-1-1-10}

Bedrock Runtime の Converse API とストリーミング、スロットリングの処理が中心です。モデルの選定やプロンプトの設計、RAG の設計は受験者に求められていません。

詳細: [Bedrock Runtime](../../services/ai.md#bedrock-runtime)、[エラーとスロットリング](../../services/ai.md#errors-throttling)

## タスク 1.2: Lambda のコードを開発する {#task-1-2}

[![Lambda の呼び出し方式](../../assets/diagrams/lambda-invocation.png)](../../assets/diagrams/lambda-invocation.png)

### 1.2.1 VPC 内のリソースへのアクセス {#skill-1-2-1}

Lambda を VPC のサブネットとセキュリティグループに接続します。そのままではインターネットに出られないので、インターネットへは NAT ゲートウェイを使います。AWS サービスだけに接続するなら VPC エンドポイントも使えます。

詳細: [VPC アクセス](../../services/lambda.md#vpc-access)、[VPC エンドポイント](../../services/networking.md)

### 1.2.2 環境変数とパラメータの設定 {#skill-1-2-2}

メモリを増やすと CPU も比例して増えます。タイムアウト、ランタイム、ハンドラー、レイヤー、拡張機能の役割を区別します。機密情報は環境変数に平文で置きません。

詳細: [設定](../../services/lambda.md#configuration)、[環境変数](../../services/lambda.md#environment-variables)、[同時実行](../../services/lambda.md#concurrency)

### 1.2.3 イベントのライフサイクルとエラー処理 {#skill-1-2-3}

非同期呼び出しの失敗は、送信先（Destinations）か DLQ で受け取ります。送信先は成功と失敗の両方に使え、DLQ は失敗だけを扱います。失敗だけを扱う場合でも違いがあり、送信先は宛先の種類が多く（SQS、SNS、Lambda、EventBridge、失敗時のみ S3）、記録に応答の詳細も含みます。DLQ の宛先は SQS と SNS の標準タイプだけで、届くのはイベントの本文だけです。

詳細: [再試行](../../services/lambda.md#retries)、[送信先と DLQ](../../services/lambda.md#destinations-dlq)、[バッチの部分失敗](../../services/lambda.md#partial-batch-response)

### 1.2.4 他のサービスとの統合 {#skill-1-2-4}

呼び出し方は、同期、非同期、イベントソースマッピングの3種類です。SQS、Kinesis、DynamoDB Streams はイベントソースマッピングで、Lambda 側がポーリングします。

詳細: [呼び出し方式](../../services/lambda.md#invocation-types)、[イベントソースマッピング](../../services/lambda.md#event-source-mapping)

## タスク 1.3: データストアを使う {#task-1-3}

### 1.3.1 データのライフサイクル管理 {#skill-1-3-1}

S3 はライフサイクルルール、DynamoDB は TTL、CloudWatch Logs は保持期間で管理します。

詳細: [S3 ライフサイクル](../../services/s3.md#lifecycle)、[DynamoDB の TTL](../../services/dynamodb.md#ttl)、[保持](../../services/storage.md#retention)

### 1.3.2 アクセスパターンに応じたデータストアの選択 {#skill-1-3-2}

| 要件 | 選択肢 |
|---|---|
| キーで高速に読み書き、スケール重視 | DynamoDB |
| 結合やトランザクションが必要な SQL | RDS、Aurora |
| インメモリの高速アクセス | ElastiCache |
| 大きなファイル、耐久性 | S3 |
| 全文検索 | OpenSearch Service |

詳細: [データストアの選び方](../../services/databases.md#choosing-data-store)

### 1.3.3 データストアに合うキャッシュの選択 {#skill-1-3-3}

DynamoDB には DAX、RDS などには ElastiCache、静的コンテンツや API の応答には CloudFront を合わせます。遅延読み込みと書き込みスルーの違いも問われます。

詳細: [キャッシュの比較](../../services/databases.md#cache-comparison)、[キャッシュ戦略](../../services/databases.md#caching-strategies)

### 1.3.4 DynamoDB の設定 {#skill-1-3-4}

- パーティションキーには、値の種類が多く偏りの少ない属性を選びます。
- 読み取りは結果整合性が既定で、強い整合性も指定できます。GSI は強い整合性に対応していません。
- Query はキーで絞り込み、Scan はテーブル全体を読みます。
- LSI はテーブル作成時に定義し、GSI は後からでも追加できます。

詳細: [キー](../../services/dynamodb.md#keys)、[高カーディナリティ](../../services/dynamodb.md#high-cardinality)、[整合性](../../services/dynamodb.md#read-consistency)、[Query と Scan](../../services/dynamodb.md#query-vs-scan)、[インデックス](../../services/dynamodb.md#indexes)

## 確認問題 {#self-check}

まず基本を確認する問題です。本番形式の問題は[問題集](exercises/index.md)にあります（[Lambda](exercises/lambda.md)、[メッセージング](exercises/messaging.md)、[DynamoDB](exercises/dynamodb.md) など）。

??? question "問1: API Gateway から同期で呼ぶ Lambda の処理に数分かかり、API がタイムアウトします。どう直しますか？"
    リクエストを受けたら SQS に入れてすぐ応答を返し、別の Lambda で非同期に処理します。処理の結果は、状態を確認する API などで返します。

??? question "問2: DynamoDB のパーティションキーを、値が数種類しかない status にしたところ、スロットリングが発生しました。原因と対策は？"
    特定のパーティションにアクセスが集中しています。ユーザー ID のように値の種類が多い属性をキーにします。

??? question "問3: 非同期で呼ばれる Lambda の成功時と失敗時の両方で、結果を別のサービスに渡したいです。何を使いますか？"
    Lambda の送信先（Destinations）です。DLQ は失敗したイベントの本文しか受け取れず、実行結果の詳細も含みません。

??? question "問4: SQS のメッセージが、処理中に別のコンシューマーでも処理されてしまいます。何を確認しますか？"
    可視性タイムアウトが処理時間より短くないかを確認します。標準キューは重複配信がありうるので、処理を冪等にすることも必要です。

??? question "問5: VPC に接続した Lambda から DynamoDB にアクセスできなくなりました。インターネットを経由せずに解決するには？"
    DynamoDB のゲートウェイ型 VPC エンドポイントを作り、ルートテーブルに追加します。

??? question "問6: ログを S3 に届けたいだけで、独自のコンシューマーは作りたくありません。Kinesis Data Streams と Firehose のどちらを使いますか？"
    Amazon Data Firehose です。配信先へ届ける処理を自動で行います。
