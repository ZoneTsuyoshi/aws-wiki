# 分野2: 回復性の高いアーキテクチャの設計

配点は **26%** です。部品を疎結合にして別々にスケールさせること、そして障害が起きても動き続ける、または要件の時間内に戻せることを問います。

問題文の「急増する」「注文を失わない」「RTO 15 分」「アプリを変更できない」といった条件で、答えが変わります。

各見出しの「ガイドの項目」は、試験ガイドの Knowledge of（知識）と Skills in（スキル）を、ガイドに載っている順の番号で示したものです。

## タスク 2.1: スケーラブルで疎結合なアーキテクチャを設計する {#task-2-1}

### 多層、マイクロサービス、イベント駆動の設計 {#t2-1-architectures}

**ガイドの項目:** 知識4 マイクロサービスの設計原則（ステートレスとステートフル） / 知識10 多層アーキテクチャ / スキル1 要件に基づくイベント駆動、マイクロサービス、多層アーキテクチャの設計

| パターン | 向く要件 | AWS での形 |
|---|---|---|
| 多層 | 表示、処理、データを分けて守りたい | ALB、Auto Scaling の EC2、RDS |
| マイクロサービス | 機能ごとに独立してデプロイ、スケールしたい | API Gateway と Lambda、ECS、EKS |
| イベント駆動 | 発生元と処理側を切り離したい | EventBridge、SNS、SQS |

スケールさせる層はステートレスにします。セッションはサーバーのメモリに置かず、ElastiCache か DynamoDB に出します。ファイルは S3 か EFS に置きます。

**例**: ログインのたびに同じ EC2 へ戻らないとセッションが切れるアプリは、スケールインで利用者が切断されます。セッションを ElastiCache に移せば、どのインスタンスでも処理できます。

詳細: [アーキテクチャパターン](../../services/sdk-resilience.md#architectural-patterns)、[ステートフルとステートレス](../../services/sdk-resilience.md#stateful-stateless)

### API の作成と管理 {#t2-1-api}

**ガイドの項目:** 知識1 API の作成と管理（API Gateway、REST API）

| 要件 | 選択 |
|---|---|
| API キー、使用量プラン、キャッシュ、WAF が要る | REST API |
| Lambda や HTTP へ単純につなぎ、費用を下げたい | HTTP API |
| サーバーからクライアントへ送る、チャット | WebSocket API |
| VPC の中からだけ呼ばせる | REST API のプライベートエンドポイント |
| VPC 内の ALB や NLB へ流す | プライベート統合（VPC リンク） |

API Gateway の統合タイムアウトは既定で 29 秒です。それより長い処理は SQS に入れてすぐ応答し、非同期にします。

詳細: [API の種類](../../services/api-gateway.md#api-types)、[エンドポイントタイプ](../../services/api-gateway.md#endpoint-types)、[プライベート統合](../../services/api-gateway.md#private-integration)、[クォータ](../../services/api-gateway.md#quotas)

### メッセージングとイベント駆動 {#t2-1-messaging}

**ガイドの項目:** 知識5 イベント駆動アーキテクチャ / 知識11 キューとメッセージングの概念（パブリッシュ/サブスクライブ） / スキル3 疎結合に必要なサービスの判断

| | SQS | SNS | EventBridge |
|---|---|---|---|
| モデル | キュー（プル） | パブリッシュ/サブスクライブ（プッシュ） | イベントルーター |
| 目的 | 負荷の平準化、バッファ | 1 対多の配信 | 内容で振り分け、SaaS 連携、スケジュール |
| 保持 | 最大 14 日 | なし | アーカイブ機能あり |

| 要件 | 選択 |
|---|---|
| 急増する注文を確実に受けて順に処理 | SQS |
| 順序と重複防止が必須 | SQS FIFO |
| 1 つのイベントを複数の処理に渡す | SNS と SQS のファンアウト |
| 既存の JMS、AMQP のアプリをコード変更なしで | Amazon MQ |
| 処理できないメッセージを隔離する | SQS のデッドレターキュー |

**例**: 処理時間より可視性タイムアウトが短いと、別のワーカーが同じメッセージを受け取ります。処理時間より長くします。

詳細: [疎結合](../../services/messaging.md#coupling)、[選び方](../../services/messaging.md#how-to-choose)、[標準と FIFO](../../services/messaging.md#standard-fifo)、[可視性タイムアウト](../../services/messaging.md#visibility-timeout)、[デッドレターキュー](../../services/messaging.md#sqs-dlq)、[ファンアウト](../../services/messaging.md#fanout)、[EventBridge](../../services/messaging.md#eventbridge)、[Amazon MQ](../../services/other-services.md#mq)

### ワークフローのオーケストレーション {#t2-1-workflow}

**ガイドの項目:** 知識16 ワークフローのオーケストレーション（Step Functions）

複数のステップの順序、分岐、再試行、人の承認を、コードではなくステートマシンで管理します。

| | Standard | Express |
|---|---|---|
| 最大実行時間 | 1 年 | 5 分 |
| 実行の保証 | 正確に 1 回 | 非同期は少なくとも 1 回 |
| 向く処理 | 長時間の業務フロー、人の承認 | 大量で短いイベント処理 |

「Lambda から Lambda を呼び、再試行を自前で書いている」構成の改善は Step Functions が答えです。

詳細: [Standard と Express](../../services/step-functions.md#standard-express)、[エラー処理](../../services/step-functions.md#error-handling)、[人の承認](../../services/step-functions.md#human-approval)、[オーケストレーションとコレオグラフィー](../../services/step-functions.md#orchestration-choreography)

### 水平スケーリングと垂直スケーリング {#t2-1-scaling}

**ガイドの項目:** 知識6 水平スケーリングと垂直スケーリング / スキル2 アーキテクチャの部品ごとのスケーリング戦略の判断

| 方式 | 内容 | 注意点 |
|---|---|---|
| 水平 | 台数を増やす | ステートレスにする必要があります |
| 垂直 | サイズを大きくする | 上限があり、変更時に停止することがあります |

| 部品 | スケーリングの方法 |
|---|---|
| EC2 | Auto Scaling（ターゲット追跡が第一候補） |
| ECS | サービスの Auto Scaling |
| Lambda | 自動。上限は同時実行数 |
| RDS の読み取り | リードレプリカ |
| RDS の書き込み | インスタンスのサイズを上げる、Aurora に移す |
| DynamoDB | オンデマンド、またはプロビジョンドと Auto Scaling |

**例**: SQS のワーカーは、CPU ではなくインスタンスあたりのバックログを指標にしてターゲット追跡します。

詳細: [EC2 Auto Scaling](../../services/ec2-beanstalk.md#auto-scaling)、[ECS サービスの Auto Scaling](../../services/containers.md#service-auto-scaling)、[Lambda の同時実行](../../services/lambda.md#concurrency)、[DynamoDB のキャパシティ](../../services/dynamodb.md#capacity)

### 負荷分散の概念 {#t2-1-load-balancing}

**ガイドの項目:** 知識9 負荷分散の概念（ALB）

ロードバランサーを間に置くと、クライアントは個々のサーバーを知らなくて済みます。台数の増減や障害を隠せるので、疎結合の基本の部品です。

ALB はパス、ホスト、ヘッダーで振り分けられるので、1 つの ALB で複数のマイクロサービスを受けられます。

詳細: [Elastic Load Balancing](../../services/networking.md#elb)、[ALB と NLB の違い](../../services/networking.md#alb-vs-nlb)、[リスナーとルール](../../services/networking.md#alb-listeners)

### キャッシュとエッジ {#t2-1-caching}

**ガイドの項目:** 知識3 キャッシュの戦略 / 知識7 エッジアクセラレーターの適切な使い方（CDN）

| 戦略 | 動作 | 向く場面 |
|---|---|---|
| 遅延読み込み | ミスしたときだけ DB から読む | 読まれるデータだけ入れたい |
| ライトスルー | 書き込みと同時に更新 | 常に新しい値を読ませたい |
| TTL | 一定時間で期限切れ | 古さの上限を決めたい |

| 場所 | 使うもの |
|---|---|
| 静的コンテンツ、API の応答 | CloudFront |
| API のレスポンス | API Gateway のキャッシュ（REST API） |
| RDS の読み取り | ElastiCache |
| DynamoDB の読み取り | DAX |

CloudFront はコンテンツをキャッシュします。Global Accelerator はキャッシュせず、固定 IP と AWS ネットワークで TCP と UDP を運びます。

詳細: [キャッシュ戦略](../../services/databases.md#caching-strategies)、[キャッシュの使い分け](../../services/databases.md#cache-comparison)、[CloudFront](../../services/networking.md#cloudfront)、[API Gateway のキャッシュ](../../services/api-gateway.md#caching)、[Global Accelerator](../../services/network-connectivity.md#global-accelerator)

### コンテナ {#t2-1-containers}

**ガイドの項目:** 知識8 アプリケーションをコンテナに移行する方法 / 知識14 コンテナのオーケストレーション（ECS、EKS） / スキル4 コンテナを使うべき場面の判断

| 要件 | 選択 |
|---|---|
| AWS に統合された簡単なオーケストレーション | ECS |
| Kubernetes の資産やツールを使う | EKS |
| サーバーを管理したくない | Fargate |
| GPU や特権コンテナなどの特殊な要件 | EC2 の起動タイプ |
| オンプレミスのサーバーで ECS を動かす | ECS Anywhere |
| オンプレミスで EKS と同じ配布の Kubernetes を自分で動かす | EKS Anywhere、EKS Distro |
| イメージの保管 | ECR |

コンテナが向くのは、15 分を超える処理、既存のランタイムやライブラリに依存するアプリ、ポータブルにしたいアプリです。短いイベント処理なら Lambda のほうが運用は軽くなります。

移行の流れは、アプリを Dockerfile でイメージにし、ECR に入れ、ECS か EKS で動かします。状態はコンテナの外（S3、EFS、DB）へ出します。

!!! note "App2Container の状況"
    ソースコードなしで既存アプリをコンテナにする App2Container は、新規受付を終了しました。後継は AWS Transform です。

詳細: [Dockerfile](../../services/containers.md#dockerfile)、[ECR](../../services/containers.md#ecr)、[ECS](../../services/containers.md#ecs)、[Fargate と EC2](../../services/containers.md#fargate-vs-ec2)、[EKS](../../services/containers.md#eks)、[ECS Anywhere](../../services/operations.md#ecs-anywhere)、[EKS Anywhere](../../services/operations.md#eks-anywhere)、[EKS Distro](../../services/operations.md#eks-distro)、[App2Container](../../services/migration.md#app2container)

### サーバーレス {#t2-1-serverless}

**ガイドの項目:** 知識12 サーバーレスの技術とパターン（Fargate、Lambda） / スキル5 サーバーレスを使うべき場面の判断

| 条件 | 向いているもの |
|---|---|
| 短いイベント処理、15 分以内 | Lambda |
| 負荷の増減が大きく、アイドルの時間が長い | Lambda、DynamoDB オンデマンド |
| 長時間動くコンテナ、サーバーは管理したくない | Fargate |
| 常に一定の高負荷で、細かく調整したい | EC2 |

Lambda のタイムアウトは最大 900 秒（15 分）です。これを超える処理の答えは、Fargate、Batch、Step Functions での分割です。

SAM で作られた構成を組織や公開の場で再利用するなら、AWS Serverless Application Repository で探してデプロイできます。Lambda のコンソールと統合されていて、SAM テンプレートとコードを公開します。

静的な Web アプリをすぐ公開するなら、Amplify Hosting も候補です。

詳細: [Lambda の実行モデル](../../services/lambda.md#execution-model)、[タイムアウト](../../services/lambda.md#timeout)、[Fargate と EC2](../../services/containers.md#fargate-vs-ec2)、[SAM CLI](../../services/iac.md#sam-cli)、[Amplify Hosting](../../services/cicd.md#amplify)

### ストレージの種類 {#t2-1-storage-types}

**ガイドの項目:** 知識13 ストレージの種類と特徴（オブジェクト、ファイル、ブロック）

| 種類 | サービス | 特徴 | 選ぶ手がかり |
|---|---|---|---|
| オブジェクト | S3 | HTTPS API、容量は自動 | 多数から読む、配信、データレイク |
| ファイル | EFS、FSx | マウントして共有 | 複数のサーバーで同じファイルを使う |
| ブロック | EBS | 1 つの AZ、通常 1 台 | OS のディスク、単一インスタンスの DB |

スケールアウトするアプリで共有ファイルが要るなら、EBS ではなく EFS です。

詳細: [EBS、EFS、S3 の比較](../../services/storage.md#comparison)、[EBS、EFS、S3、FSx の比較](../../services/storage-advanced.md#storage-comparison)

### リードレプリカを使う場面 {#t2-1-read-replicas}

**ガイドの項目:** 知識15 リードレプリカを使う場面

読み取りが多く、プライマリの負荷を下げたいときに使います。

| 目的 | 選択 |
|---|---|
| 読み取りをスケールする | リードレプリカ（非同期） |
| 障害に備える | Multi-AZ（同期） |
| レポートのような重いクエリを逃がす | リードレプリカ |
| 読み取り可能なスタンバイも欲しい | Multi-AZ DB クラスター |

レプリカは非同期なので、書いた直後の読み取りには古い値が返ることがあります。接続先はアプリで指定し直します。

詳細: [リードレプリカと Multi-AZ](../../services/databases.md#read-replicas)

### マネージドサービスと専用サービス {#t2-1-managed-services}

**ガイドの項目:** 知識2 マネージドサービスの適切な用途（Transfer Family、SQS、Secrets Manager） / スキル7 ワークロードに合う専用サービスの利用

自分で EC2 に構築する選択肢より、目的に合うマネージドサービスが正解になることが多いです。「最小の運用負荷で」とあれば特にそうです。

| 自前の構成 | 専用サービス |
|---|---|
| EC2 の SFTP サーバー | Transfer Family |
| EC2 の RabbitMQ | SQS か Amazon MQ |
| 設定ファイルに書いたパスワードを手で交換 | Secrets Manager |
| cron サーバーで定期実行 | EventBridge のスケジュールと Lambda |
| SaaS からデータを取るスクリプト | AppFlow |
| ワークロードの設計の点検を表計算で | Well-Architected Tool |

詳細: [Transfer Family](../../services/migration.md#transfer-family)、[SQS](../../services/messaging.md#sqs)、[Secrets Manager](../../services/secrets.md#secrets-manager)、[EventBridge のスケジュール](../../services/messaging.md#eventbridge-schedule)、[AppFlow](../../services/data-engineering.md#appflow)、[Well-Architected Tool](../../services/cloud-foundations.md#wa-tool)

### 要件からの技術の選択 {#t2-1-recommending}

**ガイドの項目:** スキル6 要件に基づくコンピューティング、ストレージ、ネットワーク、データベース技術の推奨

問題文の条件を、次の順に確認すると絞れます。

| 分類 | 確認すること | 代表的な答え |
|---|---|---|
| コンピューティング | 実行時間、管理の範囲、負荷の形 | Lambda、Fargate、EC2 |
| ストレージ | アクセス方法、共有の有無、遅延 | S3、EFS、EBS、FSx |
| ネットワーク | プロトコル、固定 IP の要否、利用者の場所 | ALB、NLB、CloudFront、Global Accelerator |
| データベース | 結合の要否、キーでの読み書き、規模 | RDS、Aurora、DynamoDB |

詳細: [データストアの選び方](../../services/databases.md#choosing-data-store)、[全エンジンの比較表](../../services/databases-specialized.md#decision-table)、[FSx の選び方](../../services/storage-advanced.md#fsx-selection)

## タスク 2.2: 高可用性や耐障害性のあるアーキテクチャを設計する {#task-2-2}

### グローバルインフラとルーティング {#t2-2-global}

**ガイドの項目:** 知識1 グローバルインフラストラクチャ（AZ、リージョン、Route 53） / 知識3 基本的なネットワークの概念（ルートテーブル）

Route 53 のルーティングポリシーで、リージョンをまたぐ振り分けを決めます。

| 要件 | ポリシー |
|---|---|
| 主系が落ちたら副系へ | フェイルオーバー |
| 最も遅延の小さいリージョンへ | レイテンシー |
| 国ごとに別のサイトへ、規制のため | 位置情報 |
| 10% だけ新しい環境へ | 加重 |
| 複数の正常な IP を返す | 複数値回答 |

ルートテーブルも可用性に関わります。AZ ごとに NAT ゲートウェイを置くなら、プライベートのルートテーブルも AZ ごとに分けて、同じ AZ の NAT を指します。

詳細: [ルーティングポリシー](../../services/networking.md#routing-policies)、[Route 53 ヘルスチェック](../../services/networking.md#route53-health-checks)、[サブネットとルートテーブル](../../services/networking.md#subnets-route-tables)、[リージョン](../../services/cloud-foundations.md#regions)

### AZ とリージョンをまたぐ構成 {#t2-2-multi-az-region}

**ガイドの項目:** スキル2 リージョンや AZ をまたぐ高可用性、耐障害性に必要なサービスの判断

| サービス | Multi-AZ | Multi-Region |
|---|---|---|
| EC2 | Auto Scaling を複数 AZ に | AMI のコピー、別リージョンの Auto Scaling |
| RDS | Multi-AZ DB インスタンス、DB クラスター | クロスリージョンリードレプリカ |
| Aurora | 3 AZ の 6 つのストレージノード | Global Database |
| DynamoDB | 標準で複数 AZ | グローバルテーブル |
| S3 | 標準で 3 AZ 以上（One Zone を除く） | CRR、Multi-Region Access Points |
| EFS | Regional タイプ | EFS のレプリケーション |
| EBS | 1 つの AZ のみ | スナップショットのコピー |

Multi-AZ の RDS DB インスタンスのスタンバイは読めません。読み取りの負荷分散にはなりません。

詳細: [サービスごとの Multi-AZ と Multi-Region](../../services/resilience.md#patterns-by-service)、[Aurora グローバルデータベース](../../services/databases.md#aurora-global-database)、[グローバルテーブル](../../services/dynamodb.md#global-tables)、[Multi-Region Access Points](../../services/storage-advanced.md#mrap)

### 単一障害点の排除 {#t2-2-spof}

**ガイドの項目:** 知識8 負荷分散の概念（ALB） / スキル4 単一障害点を軽減する設計の実装

| 単一障害点 | 対策 |
|---|---|
| 1 台の EC2 | 複数 AZ の Auto Scaling と ALB |
| 1 つの AZ の NAT ゲートウェイ | AZ ごとに作る。リージョン型 NAT も使える |
| シングル AZ の RDS | Multi-AZ |
| EC2 上のファイル | EFS か S3 |
| 1 本の専用線 | 2 つのロケーションに Direct Connect、または VPN を予備に |
| 1 本の VPN トンネル | 2 本とも設定する |

ALB を複数 AZ のサブネットに置き、Auto Scaling のヘルスチェックに ELB を加えます。こうするとアプリが異常なインスタンスも置き換えられます。既定の EC2 ステータスチェックだけでは、アプリの異常に気づきません。

**静的安定性**: AZ の障害時に新しく起動する設計は、起動の API と容量に依存します。最初から余分に動かしておく設計なら、何もしなくても続けられます。

詳細: [高可用性のための Auto Scaling](../../services/resilience.md#auto-scaling-ha)、[Auto Scaling のヘルスチェック](../../services/ec2-beanstalk.md#asg-health-checks)、[静的安定性](../../services/resilience.md#static-stability)、[NAT ゲートウェイ](../../services/network-connectivity.md#nat-gateway)、[DX の回復性のモデル](../../services/network-connectivity.md#dx-resiliency)

### フェイルオーバーの戦略 {#t2-2-failover}

**ガイドの項目:** 知識6 フェイルオーバーの戦略

| 層 | 方法 | 切り替えの性質 |
|---|---|---|
| DNS | Route 53 のフェイルオーバーとヘルスチェック | TTL に左右されます |
| 固定 IP | Global Accelerator | DNS キャッシュの影響を受けません |
| コンテンツ | CloudFront のオリジンフェイルオーバー | 読み取りのリクエストが対象です |
| DB | RDS の Multi-AZ（通常 60〜120 秒）、Aurora のレプリカの昇格 | 接続先の DNS が変わります |

アプリはインスタンスのエンドポイントではなく、DB のクラスターエンドポイントなどの DNS 名を使います。

詳細: [Route 53 のフェイルオーバー設計](../../services/resilience.md#route53-failover)、[Global Accelerator との比較](../../services/resilience.md#global-accelerator)、[オリジンフェイルオーバー](../../services/networking.md#origin-failover)、[Aurora のエンドポイント](../../services/databases.md#aurora-endpoints)、[データプレーンでのフェイルオーバー](../../services/resilience.md#failover-data-plane)

### DR 戦略の選択 {#t2-2-dr}

**ガイドの項目:** 知識4 DR 戦略（バックアップと復元、パイロットライト、ウォームスタンバイ、アクティブ/アクティブ、RPO、RTO） / スキル6 業務要件に合う DR 戦略の選択

RPO は失ってよいデータの量、RTO は復旧にかけてよい時間です。短くするほど費用が増えます。

| 戦略 | 待機側の状態 | RTO と RPO の目安 | 費用 |
|---|---|---|---|
| バックアップと復元 | データのコピーのみ | 時間単位 | 最小 |
| パイロットライト | データは複製、アプリは停止か未作成 | 数十分 | 小 |
| ウォームスタンバイ | 縮小した完全なコピーが稼働 | 数分 | 中 |
| マルチサイトアクティブ/アクティブ | 全量が稼働 | ほぼゼロ | 最大 |

パイロットライトとウォームスタンバイの違いは、**すぐにリクエストを処理できるか**です。ウォームスタンバイは容量が足りないだけなので、増やすだけで全量になります。

**例**: 社内の日報システムで RTO 24 時間、RPO 24 時間なら、毎日のバックアップを別リージョンにコピーするだけで足ります。アクティブ/アクティブは過剰で、不正解です。

詳細: [RTO と RPO](../../services/resilience.md#rto-rpo)、[4 つの DR 戦略](../../services/resilience.md#dr-strategies)、[選び方の比較](../../services/resilience.md#choosing)

### ストレージの耐久性とデータの保護 {#t2-2-data-durability}

**ガイドの項目:** 知識11 ストレージの選択肢と特徴（耐久性、レプリケーション） / スキル5 データの耐久性と可用性を確保する戦略の実装（バックアップ）

| ストレージ | 耐久性、レプリケーション |
|---|---|
| S3 | イレブンナインの設計値。One Zone-IA と Express One Zone は AZ の喪失に耐えられない |
| EBS | 1 つの AZ の中で複製。スナップショットは全 AZ から復元できる |
| インスタンスストア | 停止や終了で消える |
| EFS | Regional タイプは複数 AZ |
| FSx | タイプにより異なる。Multi-AZ を選べるものがある |

バックアップは別リージョン、別アカウントにも持ちます。復元のテストをしないと、当てになりません。

詳細: [S3 ストレージクラス](../../services/s3.md#storage-classes)、[レプリケーション](../../services/s3.md#replication)、[EBS スナップショット](../../services/storage.md#ebs-snapshots)、[インスタンスストア](../../services/storage-advanced.md#instance-store)、[AWS Backup](../../services/resilience.md#backup)、[リージョン間コピー](../../services/resilience.md#backup-cross-region)、[復元テスト](../../services/resilience.md#backup-testing)

### 分散設計のパターン {#t2-2-distributed}

**ガイドの項目:** 知識5 分散設計のパターン

| パターン | 目的 |
|---|---|
| 指数バックオフとジッター | 再試行の集中を避ける |
| 冪等性 | 再試行しても結果を変えない |
| サーキットブレーカー | 止まった依存先への呼び出しをやめる |
| 機能の縮退 | 一部が止まっても主な機能を残す |
| キューによる負荷の平準化 | 急増を吸収する |
| ファンアウト | 1 つのイベントを並列に処理する |

詳細: [リトライ](../../services/sdk-resilience.md#retries)、[指数バックオフとジッター](../../services/sdk-resilience.md#backoff-jitter)、[冪等性](../../services/sdk-resilience.md#idempotency)、[サーキットブレーカー](../../services/sdk-resilience.md#circuit-breaker)、[機能の縮退](../../services/sdk-resilience.md#graceful-degradation)、[疎結合と耐障害性](../../services/resilience.md#loose-coupling)

### 不変インフラと自動化 {#t2-2-immutable}

**ガイドの項目:** 知識7 不変インフラストラクチャ / スキル1 インフラの整合性を確保する自動化戦略の判断

不変インフラは、動いているサーバーを直さず、新しいものに置き換える考え方です。設定のずれが生まれず、問題が起きたら古いものに戻せます。

| 目的 | 使うもの |
|---|---|
| インフラをコードで再現する | CloudFormation |
| 手作業の変更を見つける | CloudFormation のドリフト検出、Config |
| 非準拠を自動で直す | Config ルールと Systems Manager Automation |
| 新しい AMI へ順に置き換える | Auto Scaling のインスタンスの更新 |
| 全 OS にパッチを当てる | Systems Manager Patch Manager |
| 標準の AMI を作り続ける | EC2 Image Builder |
| Beanstalk で新しい環境へ置き換える | 不変デプロイ、ブルー/グリーン |

!!! note "AWS Proton の状況"
    プラットフォームチームのテンプレートから開発者がインフラを作る AWS Proton は、ガイドの範囲リストに残っていますが、2026 年 10 月 7 日にサポートが終了しました。新しい設計の選択肢にはなりません。

詳細: [CloudFormation テンプレート](../../services/iac.md#cloudformation-template)、[ドリフト検出](../../services/iac.md#drift)、[Config の修復](../../services/governance.md#config-remediation)、[Automation](../../services/operations.md#automation)、[インスタンスの更新](../../services/operations.md#instance-refresh)、[Patch Manager](../../services/operations.md#patch-manager)、[EC2 Image Builder](../../services/operations.md#image-builder)、[不変デプロイ](../../services/ec2-beanstalk.md#immutable)、[Proton](../../services/governance.md#proton)

### プロキシの概念 {#t2-2-proxy}

**ガイドの項目:** 知識9 プロキシの概念（RDS Proxy）

RDS Proxy は、アプリと DB の間で接続を共有します。

| 効果 | 内容 |
|---|---|
| 接続の多重化 | Lambda のように接続が急増しても、DB の接続数を抑える |
| フェイルオーバー | 切り替え時にアプリの接続を保持する |
| 認証 | クライアントは IAM 認証ができ、DB の認証情報は Secrets Manager に置く |

プロキシは DB と同じ VPC に置き、パブリックアクセスはできません。セッションの状態を変えるとピン留めが起きて、効果が下がります。

**例**: Lambda が増えると `too many connections` になるなら、RDS Proxy が答えです。インスタンスのサイズを上げるのは根本の解決ではありません。

詳細: [RDS Proxy](../../services/databases.md#rds-proxy)、[RDS Proxy の設定](../../services/databases.md#rds-proxy-settings)、[接続プーリング](../../services/databases.md#connection-pooling)

### サービスクォータとスロットリング {#t2-2-quotas}

**ガイドの項目:** 知識10 サービスクォータとスロットリング（スタンバイ環境のクォータの設定など）

クォータの多くはリージョンごとです。**DR リージョンのクォータも本番と同じ水準に引き上げておきます。** 既定のままだと、フェイルオーバーで必要な台数を起動できません。

| 道具 | 用途 |
|---|---|
| Service Quotas | クォータの確認と引き上げの申請。調整できるかは Adjustable の列で確認 |
| CloudWatch の `SERVICE_QUOTA` | 使用率でアラームを出す（例: 80% で通知） |
| 指数バックオフとジッター | スロットリングされた呼び出しの再試行 |
| API Gateway の使用量プラン | クライアントごとの制限 |
| Lambda の予約済み同時実行 | 他の関数の影響を受けないようにする |

**例**: EC2 の `InstanceLimitExceeded` はリージョンのクォータの超過です。Service Quotas で引き上げます。

引き上げは審査に時間がかかることがあります。障害が起きてからでは間に合いません。

詳細: [クォータの上限に近づいたとき](../../services/observability.md#quota-alerts)、[インスタンスのトラブルシューティング](../../services/operations.md#instance-troubleshooting)、[API Gateway のスロットリング](../../services/api-gateway.md#throttling)、[Lambda の予約済み同時実行](../../services/lambda.md#reserved-concurrency)

### 可視性と業務に基づくメトリクス {#t2-2-visibility}

**ガイドの項目:** 知識12 ワークロードの可視性（X-Ray） / スキル3 業務要件に基づく、高可用性のためのメトリクスの特定

| 道具 | 分かること |
|---|---|
| X-Ray | リクエストがどのサービスで遅いか、失敗したか |
| CloudWatch メトリクス、アラーム | 数値の変化と通知 |
| CloudWatch Logs | アプリのログ |
| CloudTrail | 誰が API を呼んだか |
| Health Dashboard | AWS 側の障害と保守の予定 |
| Managed Grafana、Managed Service for Prometheus | 可視化とコンテナのメトリクス |

可用性の指標は、CPU より業務に近いものを選びます。

| 業務要件 | 指標の例 |
|---|---|
| 注文の処理が遅れない | SQS の `ApproximateAgeOfOldestMessage` |
| 画面が速く返る | ALB の `TargetResponseTime`（パーセンタイル） |
| エラーを出さない | ALB の 5XX の数 |
| 外形の可用性 | Route 53 ヘルスチェック、CloudWatch Synthetics |

詳細: [X-Ray](../../services/observability.md#xray)、[統計とパーセンタイル](../../services/observability.md#statistics)、[アラーム](../../services/observability.md#alarms)、[CloudWatch と CloudTrail の違い](../../services/observability.md#cloudtrail-vs-cloudwatch)、[Health Dashboard](../../services/cloud-foundations.md#health)、[Managed Grafana](../../services/operations.md#managed-grafana)、[Managed Service for Prometheus](../../services/operations.md#managed-prometheus)、[Synthetics](../../services/operations.md#synthetics)

### レガシーアプリの信頼性の向上 {#t2-2-legacy}

**ガイドの項目:** スキル7 レガシーアプリやクラウド向けでないアプリの信頼性を高めるサービスの利用（アプリを変更できない場合など）

アプリを変更できないときは、アプリの外側で信頼性を足します。

| アプリの制約 | 外側での対策 |
|---|---|
| セッションをサーバーに持つ | ALB のスティッキーセッション |
| 1 台でしか動かない | Auto Scaling グループを最小 1、最大 1 で複数 AZ に置き、自動で置き換える |
| 共有フォルダ（NFS、SMB）に依存 | EFS、FSx をそのままマウントする |
| 接続の再確立が苦手 | RDS Proxy |
| 固定 IP を許可リストに書いている | NLB の Elastic IP、Global Accelerator |
| 商用の DB で OS の権限が必要 | RDS Custom、または EC2 上の DB と Multi-AZ の構成 |
| JMS などに依存 | Amazon MQ |

スティッキーセッションは負荷が偏りやすいので、アプリを変更できるなら外部のセッションストアが優先です。

詳細: [スティッキーセッション](../../services/networking.md#stickiness)、[NLB の設定](../../services/networking.md#nlb-settings)、[EFS の設定](../../services/storage.md#efs-settings)、[FSx の選び方](../../services/storage-advanced.md#fsx-selection)、[RDS Custom](../../services/databases-specialized.md#rds-custom)

### マネージド AI サービスの用途 {#t2-2-managed-ai}

**ガイドの項目:** 知識2 マネージドサービスの適切な用途（Comprehend、Polly） / スキル8 ワークロードに合う専用サービスの利用

機能ごとの専用サービスがあるなら、モデルを自分で学習させません。SageMaker AI を選ぶのは、独自のモデルを作る要件があるときです。

| やりたいこと | サービス |
|---|---|
| 文章の感情分析、固有表現の抽出 | Comprehend |
| テキストを音声に | Polly |
| 音声をテキストに | Transcribe |
| 文書から文字と表を抽出 | Textract |
| 画像や動画の分析 | Rekognition |
| 翻訳 | Translate |
| チャットボット | Lex |
| 独自のモデルの学習とデプロイ | SageMaker AI |

詳細: [Comprehend](../../services/ai-managed-services.md#comprehend)、[Polly](../../services/ai-managed-services.md#polly)、[Transcribe](../../services/ai-managed-services.md#transcribe)、[Textract](../../services/ai-managed-services.md#textract)、[Rekognition](../../services/ai-managed-services.md#rekognition)、[Translate](../../services/ai-managed-services.md#translate)、[Lex](../../services/ai-managed-services.md#lex)、[SageMaker AI](../../services/sagemaker.md)

## 確認問題 {#self-check}

??? question "問1: 画像を受け付ける Web アプリがあります。アクセスが増えるとサムネイル作成が追いつかず、受付まで遅くなります。受付とサムネイル作成を別々にスケールさせるには？"
    受付の層が S3 に画像を置いて SQS にメッセージを入れ、別のワーカーがキューから取り出して処理します。ワーカーはインスタンスあたりのバックログを指標に Auto Scaling します。Lambda で処理しても構いません。キューが急増を吸収するので、受付の遅さと切り離せます。

??? question "問2: 基幹システムの DR を検討しています。RTO は 10 分、RPO は 1 分で、費用はできるだけ抑えたいですが、切り替え後すぐに一部のリクエストを処理したいです。どの戦略を選びますか？"
    ウォームスタンバイです。縮小した環境を別リージョンで常に動かし、データは Aurora Global Database などで複製します。バックアップと復元では間に合いません。パイロットライトはアプリが動いていないので、すぐには処理できません。アクティブ/アクティブは要件に対して費用が過剰です。

??? question "問3: ウォームスタンバイのリージョンへ切り替えたところ、EC2 を必要な台数まで増やせず、InstanceLimitExceeded が出ました。再発を防ぐには？"
    DR リージョンの Service Quotas を本番と同じ水準に引き上げておきます。クォータはリージョンごとで、引き上げの審査に時間がかかることがあるので、事前に行います。重要なら、キャパシティ予約で容量も確保します。

??? question "問4: Lambda から RDS for MySQL に接続するアプリで、アクセスの急増時に接続エラーが増えます。アプリのロジックはほとんど変えたくありません。何を追加しますか？"
    RDS Proxy です。接続を共有して DB の接続数を抑え、フェイルオーバーの時間も短くできます。リードレプリカは読み取りの分散で、接続の急増そのものは解決しません。

??? question "問5: 3 つの AZ に EC2 を配置しましたが、AZ-a の障害で全インスタンスの外向き通信が止まりました。原因と対策は？"
    NAT ゲートウェイが AZ-a の 1 つだけで、他の AZ のルートもそこを指していたからです。AZ ごとに NAT ゲートウェイを作り、各 AZ のルートテーブルで同じ AZ の NAT を指します。リージョン型の NAT ゲートウェイを使う方法もあります。

??? question "問6: 古いアプリは、再起動すると最新のセッション情報をサーバーのメモリから失います。コードは変更できません。ALB の後ろで複数台に分けつつ、利用者のセッションが切れにくいようにするには？"
    ALB のスティッキーセッションを有効にし、同じ利用者を同じターゲットへ送ります。Auto Scaling で複数 AZ に配置します。外部のセッションストアが本来の形ですが、コードの変更が必要なので、この条件では選べません。インスタンスが落ちればそのセッションは失われることを前提にします。
