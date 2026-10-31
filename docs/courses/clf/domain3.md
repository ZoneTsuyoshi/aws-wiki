# 分野3: クラウドのテクノロジーとサービス

配点は **34%** で、4分野の中で最大です。インフラの構造と、主なサービスの役割を扱います。

設定値までは問われません。「この要件ならどのサービスか」を答えられるようにします。似たサービスの違いは表で覚えます。

## タスク 3.1: デプロイと運用の方法を理解する {#task-3-1}

### プロビジョニングと運用の方法 {#t3-1-provisioning}

リソースの作り方は、手で作るか、コードから作るか、任せるかで分かれます。

| 方法 | 例 | 向く場面 |
|---|---|---|
| 手で作る | マネジメントコンソール | 確認、一度きりの作業 |
| スクリプト | CLI、SDK | 繰り返しの操作 |
| IaC | CloudFormation | 環境の再現と変更管理 |
| 基盤を任せる | Elastic Beanstalk、Lightsail | コードや小さなサイトに集中する |

詳細: [マネジメントコンソールとアクセス方法](../../services/cloud-foundations.md#access-methods)、[IaC の選び方](../../services/iac.md#choosing)、[Elastic Beanstalk](../../services/ec2-beanstalk.md#beanstalk-environments)

### AWS へのアクセス方法 {#t3-1-access}

| 方法 | 内容 | 選ぶ条件 |
|---|---|---|
| マネジメントコンソール | ブラウザーの画面 | 手作業の確認や、一度きりの操作 |
| AWS CLI | コマンド | スクリプトで繰り返す |
| SDK | プログラムのライブラリ | アプリから AWS を呼ぶ |
| API | HTTPS の呼び出し | CLI と SDK が内部で使う土台 |
| IaC | テンプレートやコード | 同じ環境を何度も作る |

詳細: [マネジメントコンソールとアクセス方法](../../services/cloud-foundations.md#access-methods)、[AWS CLI](../../services/iac.md#aws-cli)

### 一度きりか、繰り返しか {#t3-1-one-time-repeatable}

要件を見て判断します。

| 要件 | 選択 |
|---|---|
| 一度だけ状態を確認する | コンソール |
| 毎晩同じ処理を実行する | CLI のスクリプトなど、自動化する |
| 開発、検証、本番に同じ構成を作る | IaC |
| 別のリージョンに同じ環境を作る | IaC |

繰り返す作業を手で行うと、ミスと手間が増えます。

詳細: [マネジメントコンソールとアクセス方法](../../services/cloud-foundations.md#access-methods)、[CloudFormation](../../services/iac.md#cloudformation-template)

### デプロイモデル {#t3-1-deployment-models}

| モデル | 内容 | 例 |
|---|---|---|
| クラウド | すべてをクラウドで動かす | 新規のサービスを AWS だけで作る |
| ハイブリッド | オンプレミスとクラウドを接続して併用する | 基幹システムを残し、Web を AWS に置く |
| オンプレミス | 自社施設で動かす | 自社のデータセンター |

サービスモデルも区別します。EC2 は IaaS、Elastic Beanstalk は PaaS、完成したソフトウェアは SaaS です。

詳細: [デプロイモデルとサービスモデル](../../services/cloud-foundations.md#deployment-models)

### 運用を支えるサービス {#t3-1-operating-tools}

| サービス | 役割 |
|---|---|
| AWS Systems Manager | サーバーのパッチ適用やコマンド実行をまとめて行う |
| AWS Health Dashboard | AWS 側の障害や予定されたメンテナンスの影響を示す |
| Service Quotas | サービスの上限を一覧で確認し、引き上げを申請する |

Service Quotas では、サービスごとの既定の上限（クォータ）と、調整できるかどうかを確認できます。上限が足りなければ、コンソールから引き上げを申請します。

詳細: [Systems Manager](../../services/operations.md#systems-manager)、[Health Dashboard](../../services/cloud-foundations.md#health)

Service Quotas の参考: [What is Service Quotas?](https://docs.aws.amazon.com/servicequotas/latest/userguide/intro.html)

## タスク 3.2: グローバルインフラストラクチャを理解する {#task-3-2}

[![AWS のグローバルインフラストラクチャ](../../assets/diagrams/cloud-foundations-global-infra.png)](../../assets/diagrams/cloud-foundations-global-infra.png)

### リージョン、AZ、エッジロケーションの関係 {#t3-2-components}

| 種類 | 内容 | 用途 |
|---|---|---|
| リージョン | 世界の地理的な地域。3 つ以上の AZ を持つ | 基本の配置先 |
| アベイラビリティーゾーン（AZ） | リージョン内の独立した区画 | 高可用性 |
| エッジロケーション | リージョンとは別の、世界の多数の拠点 | コンテンツ配信、DNS |

リージョンは、データの所在地の規制、利用者への遅延、サービスの提供状況、料金で選びます。

自社施設で AWS を使いたいなら AWS Outposts です。

詳細: [リージョン](../../services/cloud-foundations.md#regions)、[AZ](../../services/cloud-foundations.md#availability-zones)、[Outposts](../../services/cloud-foundations.md#outposts)

### 複数 AZ による高可用性 {#t3-2-ha}

同じアプリを複数の AZ に置き、ロードバランサーで振り分けます。1 つの AZ が止まっても、残りの AZ で動き続けます。

データベースは RDS の Multi-AZ で、別の AZ にスタンバイを持てます。

詳細: [AZ](../../services/cloud-foundations.md#availability-zones)、[高可用性のための Auto Scaling](../../services/resilience.md#auto-scaling-ha)、[RDS の Multi-AZ](../../services/databases.md#read-replicas)

### AZ は単一障害点を共有しない {#t3-2-az-isolation}

AZ は、互いに単一障害点を共有しないように設計されています。そのため、1 つの AZ の障害が他の AZ に広がりにくくなっています。

1 つの AZ に全部を置くと、その AZ の障害で止まります。

詳細: [AZ](../../services/cloud-foundations.md#availability-zones)

### 複数リージョンを使う場面 {#t3-2-multi-region}

複数 AZ で足りないときに使います。

| 理由 | 例 |
|---|---|
| 災害復旧 | リージョン全体の障害に備えて、別のリージョンで復旧する |
| 事業継続 | 大規模な災害でも業務を止めない |
| 利用者への低遅延 | 欧州と日本の利用者の近くに、それぞれ置く |
| データ主権 | 国ごとの規制に合わせて、その国のリージョンにデータを置く |

詳細: [リージョン](../../services/cloud-foundations.md#regions)、[DR 戦略](../../services/resilience.md#dr-strategies)

### エッジロケーションの利点 {#t3-2-edge}

利用者に近い場所で応答するので、遅延が減ります。Amazon CloudFront のキャッシュ、Route 53 の応答に使います。

利用者が個別に配置するものではなく、CloudFront などを使えば自動で使われます。

詳細: [エッジロケーション](../../services/cloud-foundations.md#edge-locations)、[CloudFront](../../services/networking.md#cloudfront)

## タスク 3.3: コンピューティングサービスを理解する {#task-3-3}

### コンピューティングの全体像 {#t3-3-overview}

| サービス | 役割 | 問題文での表れ方 |
|---|---|---|
| Amazon EC2 | 仮想サーバー | OS から細かく制御したい |
| AWS Lambda | イベントでコードを実行 | サーバーを管理せず短い処理を動かす |
| AWS Elastic Beanstalk | Web アプリの基盤を自動で用意する | コードをアップロードするだけで動かしたい |
| Amazon Lightsail | 必要なものがセットのプラン | 最小限の知識でサイトをすぐ公開したい |
| AWS Batch | バッチジョブの実行 | 数千のジョブを並べて順に処理したい |
| AWS Outposts | 自社施設に置く AWS の機器 | オンプレミスで AWS と同じ API を使いたい |

詳細: [Lightsail](../../services/cloud-foundations.md#lightsail)、[Batch](../../services/other-services.md#batch)、[Outposts](../../services/cloud-foundations.md#outposts)、[Elastic Beanstalk](../../services/ec2-beanstalk.md#beanstalk-environments)

### EC2 のインスタンスタイプ {#t3-3-instance-types}

| カテゴリ | ファミリーの例 | 向く処理 |
|---|---|---|
| 汎用 | T、M | Web サーバー、一般的なアプリ |
| コンピューティング最適化 | C | CPU を多く使うバッチ、エンコード |
| メモリ最適化 | R、X | インメモリキャッシュ、大きなメモリを使う処理 |
| ストレージ最適化 | I、D | 高 IOPS のローカルストレージを使う処理 |
| 高速コンピューティング | P、G | GPU を使う機械学習、グラフィックス |

詳細: [インスタンスタイプ](../../services/ec2-beanstalk.md#instance-types)

### コンテナの選択肢 {#t3-3-containers}

| サービス | 役割 | 選ぶ条件 |
|---|---|---|
| Amazon ECS | AWS 独自のコンテナ管理 | シンプルに AWS でコンテナを動かしたい |
| Amazon EKS | マネージドの Kubernetes | Kubernetes を使いたい、既存の知識や資産がある |
| Amazon ECR | コンテナイメージの保管 | イメージの置き場 |

ECS も EKS も、実行場所として EC2 や Fargate を選べます。

詳細: [ECS](../../services/containers.md#ecs)、[EKS](../../services/containers.md#eks)、[ECR](../../services/containers.md#ecr)

### サーバーレスの選択肢 {#t3-3-serverless}

| サービス | 動かすもの | 選ぶ条件 |
|---|---|---|
| AWS Lambda | 関数 | イベントで動く短い処理。実行時間は最大 15 分 |
| AWS Fargate | コンテナ | サーバー管理なしで、コンテナを動かし続ける |

どちらもサーバーの管理は不要です。

詳細: [Lambda の実行モデル](../../services/lambda.md#execution-model)、[Fargate と EC2](../../services/containers.md#fargate-vs-ec2)

### Auto Scaling と弾力性 {#t3-3-auto-scaling}

Auto Scaling は、負荷に応じてインスタンス数を増減します。これが弾力性を実現する仕組みです。

負荷が高いときは台数を増やし、下がれば減らして費用を抑えます。障害が起きたインスタンスを置き換えることもできます。

詳細: [EC2 Auto Scaling](../../services/ec2-beanstalk.md#auto-scaling)

### ロードバランサーの目的 {#t3-3-load-balancers}

複数のターゲットにリクエストを振り分け、正常なターゲットだけに送ります。複数の AZ に振り分ければ、高可用性にも役立ちます。

| 種類 | 層 | 選ぶ条件 |
|---|---|---|
| Application Load Balancer | レイヤー 7（HTTP/HTTPS） | パスやホストで振り分ける Web アプリ |
| Network Load Balancer | レイヤー 4（TCP、UDP など） | 固定 IP、非 HTTP、高負荷 |

詳細: [ALB と NLB の違い](../../services/networking.md#alb-vs-nlb)

## タスク 3.4: データベースサービスを理解する {#task-3-4}

### データベースの全体像 {#t3-4-overview}

| 要件 | サービス |
|---|---|
| SQL と結合、トランザクション | Amazon RDS、Amazon Aurora |
| キーで高速に読み書き、規模が読めない | Amazon DynamoDB |
| マイクロ秒で読むキャッシュ | Amazon ElastiCache |
| MongoDB 互換のドキュメントデータベース | Amazon DocumentDB |
| つながりを扱うグラフデータベース | Amazon Neptune |

詳細: [データストアの選び方](../../services/databases.md#choosing-data-store)、[DocumentDB](../../services/databases-specialized.md#documentdb)、[Neptune](../../services/databases-specialized.md#neptune)

### EC2 上の DB かマネージド DB か {#t3-4-ec2-vs-managed}

| 観点 | EC2 上のデータベース | マネージドデータベース |
|---|---|---|
| OS とエンジンのパッチ | 利用者 | AWS |
| バックアップ、冗長化 | 利用者が構成する | 設定で有効にできる |
| OS への接続、細かい設定 | できる | 基本はできない |
| 向く場面 | 対応していないエンジンや、OS レベルの制御が必要 | 運用の手間を減らしたい |

要件に特別な制約がなければ、マネージドデータベースが正解になりやすいです。

詳細: [RDS](../../services/databases.md#rds)、[サービスごとの責任の違い](../../services/cloud-foundations.md#responsibility-by-service)

### リレーショナルデータベース {#t3-4-relational}

RDS は MySQL、PostgreSQL、MariaDB、Oracle、SQL Server、Db2 を動かします。Aurora は MySQL と PostgreSQL に互換で、共有ストレージを持つ AWS のデータベースです。

可用性を高めるなら Multi-AZ、読み取りを増やすならリードレプリカです。この 2 つは目的が違います。

詳細: [RDS](../../services/databases.md#rds)、[リードレプリカと Multi-AZ](../../services/databases.md#read-replicas)、[Aurora](../../services/databases.md#aurora)

### NoSQL データベース {#t3-4-nosql}

DynamoDB はサーバーレスのキーバリューデータベースです。規模によらず低遅延で読み書きできます。

複雑な結合が必要なら、RDS や Aurora を選びます。

詳細: [データストアの選び方](../../services/databases.md#choosing-data-store)、[DynamoDB のキー](../../services/dynamodb.md#keys)

### メモリベースのデータベース {#t3-4-memory}

ElastiCache はインメモリのキャッシュです。読み取りを速くして、データベースの負荷を減らします。エンジンには Valkey、Redis OSS、Memcached があります。

詳細: [ElastiCache](../../services/databases.md#elasticache)

### データベースの移行ツール {#t3-4-migration}

| ツール | 役割 |
|---|---|
| AWS DMS | データを移す。元のデータベースを動かしたまま移行できる |
| AWS SCT | エンジンが違うときに、スキーマとコードを変換する |

Oracle から Aurora PostgreSQL に移すなら、スキーマを SCT で変換し、データを DMS で移します。MySQL から Aurora MySQL に移すような同じ系統の移行では、スキーマの変換は不要です。

詳細: [AWS DMS](../../services/migration.md#dms)、[AWS SCT](../../services/migration.md#sct)

## タスク 3.5: ネットワークサービスを理解する {#task-3-5}

### ネットワークの全体像 {#t3-5-overview}

| サービス | 役割 | 問題文での表れ方 |
|---|---|---|
| Amazon VPC | 論理的に分離された仮想ネットワーク | 自分のネットワークを作る |
| Amazon CloudFront | コンテンツ配信 | 世界中に静的コンテンツを速く配信する |
| AWS Global Accelerator | 固定 IP と AWS 網の経路 | 世界共通の固定 IP で高速に届ける |
| AWS Transit Gateway | VPC や VPN を 1 か所で接続する | 多数の VPC をまとめてつなぐ |
| AWS PrivateLink | インターネットを通らずサービスに接続する | VPC からプライベートに接続する |
| Amazon API Gateway | API の作成と公開 | サーバーレスの API の入口 |

CloudFront はキャッシュで配信し、Global Accelerator はキャッシュせずに経路を速くします。

詳細: [CloudFront](../../services/networking.md#cloudfront)、[Global Accelerator](../../services/network-connectivity.md#global-accelerator)、[Transit Gateway](../../services/network-connectivity.md#transit-gateway)、[PrivateLink](../../services/networking.md#vpc-endpoints)、[API Gateway](../../services/api-gateway.md#api-types)

### VPC の構成要素 {#t3-5-vpc}

| 要素 | 役割 |
|---|---|
| サブネット | VPC を AZ ごとに分けた IP の範囲 |
| ルートテーブル | 宛先ごとの転送先を決める |
| インターネットゲートウェイ | VPC とインターネットをつなぐ |
| NAT ゲートウェイ | プライベートサブネットから外へ出る。外からの接続は受けない |

パブリックサブネットは、インターネットゲートウェイへのルートを持つサブネットです。

詳細: [サブネットとルートテーブル](../../services/networking.md#subnets-route-tables)

### VPC のセキュリティ {#t3-5-vpc-security}

| | セキュリティグループ | ネットワーク ACL |
|---|---|---|
| 適用先 | インスタンス単位 | サブネット単位 |
| ルール | 許可のみ | 許可と拒否 |
| 戻り通信 | 自動で許可（ステートフル） | 明示的な許可が必要（ステートレス） |

特定の IP を拒否したいなら、ネットワーク ACL です。セキュリティグループには拒否のルールがありません。

Amazon Inspector は、インターネットなどから EC2 のポートに届く経路を報告します。通信を止めるのではなく、問題を見つけるサービスです。

詳細: [セキュリティグループとネットワーク ACL](../../services/networking.md#security-groups-nacls)、[Inspector のネットワーク到達性](../../services/threat-detection.md#inspector-network)

### Route 53 の目的 {#t3-5-route53}

Amazon Route 53 は DNS のサービスです。ドメイン名を IP アドレスなどに変換します。

ドメインの登録、ヘルスチェック、利用者に近いリージョンや正常なリージョンへの振り分けにも使います。

詳細: [Route 53](../../services/networking.md#route53)、[ルーティングポリシー](../../services/networking.md#routing-policies)

### AWS への接続方法 {#t3-5-connectivity}

| 方法 | 経路 | 選ぶ条件 |
|---|---|---|
| AWS Site-to-Site VPN | インターネット上の暗号化トンネル | 拠点と AWS を早く、安く接続する |
| AWS Client VPN | 利用者の端末からの VPN | 在宅勤務の人を VPC に接続する |
| AWS Direct Connect | 専用の接続 | 安定した帯域と遅延がほしい。大量のデータを送る |

「すぐ接続したい」は VPN です。Direct Connect は準備に時間がかかります。

詳細: [Site-to-Site VPN](../../services/network-connectivity.md#site-to-site-vpn)、[Client VPN](../../services/network-connectivity.md#client-vpn)、[Direct Connect](../../services/network-connectivity.md#direct-connect)

## タスク 3.6: ストレージサービスを理解する {#task-3-6}

### ストレージの全体像 {#t3-6-overview}

| 種類 | サービス | アクセス方法 |
|---|---|---|
| オブジェクト | Amazon S3 | HTTPS の API |
| ブロック | Amazon EBS、インスタンスストア | インスタンスのディスク |
| ファイル | Amazon EFS、Amazon FSx | ファイルシステムとしてマウント |

詳細: [EBS、EFS、S3 の比較](../../services/storage.md#comparison)

### オブジェクトストレージの用途 {#t3-6-object}

S3 は、ファイルをオブジェクトとして HTTPS で読み書きします。容量は自動で増減します。

ファイル配信、バックアップ、データレイク、静的ウェブサイトのホスティングに使います。OS をインストールするディスクには使えません。

詳細: [S3 の基本](../../services/s3.md#basics)、[静的ウェブサイトホスティング](../../services/s3.md#static-website)

### S3 のストレージクラス {#t3-6-s3-classes}

| クラス | 向くデータ | 取り出し |
|---|---|---|
| S3 Standard | 頻繁なアクセス | ミリ秒 |
| S3 Intelligent-Tiering | アクセスパターンが不明、変わる | ミリ秒（アーカイブ階層は復元が必要） |
| S3 Standard-IA | 月 1 回程度、失えないデータ | ミリ秒、取り出し料あり |
| S3 One Zone-IA | 月 1 回程度、再生成できるデータ | ミリ秒、取り出し料あり |
| S3 Glacier Instant Retrieval | 四半期に 1 回、すぐ読みたいアーカイブ | ミリ秒、取り出し料あり |
| S3 Glacier Flexible Retrieval | 年 1 回程度のアーカイブ | 数分から数時間 |
| S3 Glacier Deep Archive | 年 1 回未満の長期保管 | 数時間 |

見分ける点は 3 つです。頻度、取り出しの速さ、AZ の喪失に耐える必要があるかです。One Zone-IA は 1 つの AZ だけに置くので、AZ の喪失に耐えられません。

詳細: [ストレージクラス](../../services/s3.md#storage-classes)、[Glacier のデータ取得](../../services/s3.md#glacier-retrieval)

### ブロックストレージ {#t3-6-block}

| 観点 | Amazon EBS | インスタンスストア |
|---|---|---|
| 永続性 | インスタンスを止めても残る | 停止や終了で消える。再起動では残る |
| 範囲 | 1 つの AZ | そのホストのみ |
| 料金 | 容量などに応じて別途かかる | インスタンスの料金に含まれる |
| 向く用途 | ブートボリューム、データベース | 一時的なデータ、キャッシュ |

詳細: [EBS](../../services/storage.md#ebs-volume-types)、[インスタンスストア](../../services/storage-advanced.md#instance-store)

### ファイルサービス {#t3-6-file}

| サービス | 向く場面 |
|---|---|
| Amazon EFS | Linux の複数のインスタンスで共有する。容量は自動で増減 |
| FSx for Windows File Server | Windows のファイル共有。SMB、Active Directory |
| FSx for NetApp ONTAP | NetApp からの移行、複数のプロトコル |
| FSx for OpenZFS | ZFS や Linux のファイルサーバーの移行 |

FSx for Lustre は HPC 向けの高性能なファイルシステムですが、このガイドでは範囲外です。

詳細: [EFS](../../services/storage.md#efs-settings)、[FSx の選び方](../../services/storage-advanced.md#fsx-selection)

### キャッシュ付きのファイルシステム {#t3-6-cached}

AWS Storage Gateway は、オンプレミスのアプリと AWS のストレージをつなぎます。よく使うデータをローカルにキャッシュするので、オンプレミスから低遅延で読めます。

| タイプ | 使い方 |
|---|---|
| S3 File Gateway | ファイルとして書き、S3 にオブジェクトとして保存する |
| Volume Gateway | iSCSI のボリュームとして使う |
| Tape Gateway | 既存のテープのバックアップソフトを使い続ける |

!!! note "FSx File Gateway の状況（2026年10月時点）"
    もう 1 つのタイプの Amazon FSx File Gateway は、新規受付を終了しています。

詳細: [Storage Gateway](../../services/migration.md#storage-gateway)

### ライフサイクルポリシーの用途 {#t3-6-lifecycle}

S3 のライフサイクルルールは、古くなったオブジェクトを安いクラスへ移したり、削除したりします。

たとえば、ログを 30 日後に Standard-IA に移し、1 年後に Glacier Deep Archive に移して、7 年後に削除します。手作業なしで費用を抑えられます。

アクセスパターンが読めないなら、Intelligent-Tiering が候補です。

詳細: [ライフサイクル](../../services/s3.md#lifecycle)

### AWS Backup の用途 {#t3-6-backup}

複数のサービスのバックアップを、1 か所のプランで管理します。対象は EBS、EC2、RDS、Aurora、DynamoDB、EFS、FSx、S3 などです。

「サービスごとにバラバラのバックアップを一元管理したい」なら AWS Backup です。

サーバーを別の場所へ継続的に複製して、障害時に素早く復旧するなら、AWS Elastic Disaster Recovery を選びます。

詳細: [AWS Backup](../../services/resilience.md#backup)、[Elastic Disaster Recovery](../../services/resilience.md#drs)

## タスク 3.7: AI/ML と分析のサービスを理解する {#task-3-7}

### AI/ML のサービス {#t3-7-ai-ml}

目的のタスクから選びます。

| タスク | サービス |
|---|---|
| 独自のモデルを作り、学習してデプロイする | Amazon SageMaker AI |
| チャットボットや音声の対話を作る | Amazon Lex |
| テキストから感情やエンティティを抽出する | Amazon Comprehend |
| 文字を音声に変換する | Amazon Polly |
| 音声を文字に変換する | Amazon Transcribe |
| 言語を翻訳する | Amazon Translate |
| 文書から文字や表を抽出する | Amazon Textract |
| 画像や動画を分析する | Amazon Rekognition |
| 生成 AI のアシスタント | Amazon Q |

Polly と Transcribe は向きが逆なので、よく問われます。Comprehend はテキストの意味、Textract は文書からの抽出です。

!!! note "Amazon Q の状況（2026年10月時点）"
    試験ガイドは Amazon Q を対象としていますが、製品ごとに状況が変わっています。Amazon Q Business は新規顧客を受け付けておらず、Amazon Quick への移行が案内されています。Amazon Q Developer は、新規の Free Tier アカウントと新規サブスクリプションの作成が 2026年5月15日に止まり、IDE 向けの部分は Kiro へ移行中です。コンソールでの利用などは影響を受けません。

詳細: [SageMaker AI](../../services/sagemaker.md#studio)、[Lex](../../services/ai-managed-services.md#lex)、[Comprehend](../../services/ai-managed-services.md#comprehend)、[Polly](../../services/ai-managed-services.md#polly)、[Transcribe](../../services/ai-managed-services.md#transcribe)、[Translate](../../services/ai-managed-services.md#translate)、[Textract](../../services/ai-managed-services.md#textract)、[Rekognition](../../services/ai-managed-services.md#rekognition)、[Q Business](../../services/ai-managed-services.md#q-business)、[Q Developer](../../services/ai.md#q-developer)

### 分析のサービス {#t3-7-analytics}

| 要件 | サービス |
|---|---|
| S3 のデータに SQL で問い合わせる | Amazon Athena |
| ストリーミングデータをリアルタイムに受ける | Amazon Kinesis |
| データの ETL とカタログ | AWS Glue |
| ダッシュボードと BI、AI による分析 | Amazon Quick |
| データウェアハウス | Amazon Redshift |
| Spark などのビッグデータ基盤 | Amazon EMR |
| 全文検索、ログ分析 | Amazon OpenSearch Service |

!!! note "Amazon Quick の名称（2026年10月時点）"
    Amazon QuickSight は Amazon Quick に発展し、BI の機能は Quick Sight になりました。古い教材の QuickSight はこの機能を指します。

詳細: [Athena](../../services/streaming.md#athena)、[Kinesis Data Streams](../../services/streaming.md#kinesis-data-streams)、[Glue](../../services/data-engineering.md#glue)、[Amazon Quick](../../services/ai.md#quick)、[Quick Sight](../../services/data-engineering.md#quick-sight)、[Redshift](../../services/data-engineering.md#redshift)、[EMR](../../services/data-engineering.md#emr)、[OpenSearch Service](../../services/streaming.md#opensearch)

## タスク 3.8: その他の範囲のサービスを理解する {#task-3-8}

!!! note "このタスクのサービスの名称と状況（2026年10月時点）"
    試験ガイドの名前と、現在の製品名が異なるものがあります。

    - Amazon AppStream 2.0 は、現在 Amazon WorkSpaces Applications です。
    - Amazon Connect のコンタクトセンターは、現在 Amazon Connect Customer です。
    - Amazon WorkSpaces Secure Browser はメンテナンスに移行し（公表は 2026年9月29日）、新しい顧客は使えません。

### メッセージと通知のサービス {#t3-8-integration}

| サービス | 役割 | 選ぶ条件 |
|---|---|---|
| Amazon SQS | キュー | 処理側が自分のペースで取り出す。負荷を平準化する |
| Amazon SNS | Pub/Sub の通知 | 複数の宛先へ同時に送る。メールや SMS のアラートを送る |
| Amazon EventBridge | イベントの振り分け | 内容で振り分ける。スケジュールで実行する |
| AWS Step Functions | 処理の流れの制御 | 複数の手順を順番に実行する |

「アラートをメールで受け取りたい」は SNS です。「注文を溜めて順に処理する」は SQS です。

詳細: [SQS](../../services/messaging.md#sqs)、[SNS](../../services/messaging.md#sns)、[EventBridge](../../services/messaging.md#eventbridge)、[選び方](../../services/messaging.md#how-to-choose)、[Step Functions](../../services/step-functions.md#standard-express)

### 業務アプリケーション {#t3-8-business}

| サービス | 役割 | 選ぶ条件 |
|---|---|---|
| Amazon Connect | クラウドのコンタクトセンター | 自前の設備なしでコールセンターを作る |
| Amazon SES | メールの送受信 | アプリからメールを大量に送る |

SNS との違いは、SES はメール本文を作って送るサービスで、SNS は購読者への通知のサービスである点です。

詳細: [Amazon Connect](../../services/other-services.md#connect)、[Amazon SES](../../services/other-services.md#ses)

### 顧客支援のサービス {#t3-8-enablement}

AWS Support は、技術的な質問や問題の相談窓口です。必要な応答の速さや、専任の担当者が必要かで、プランを選びます。

プランの違いは[タスク 4.3](domain4.md#t4-3-support-plans) で扱います。

詳細: [AWS Support プラン](../../services/cloud-foundations.md#support-plans)

### 開発ツール {#t3-8-developer}

| 目的 | サービス |
|---|---|
| ビルドとテストの実行 | AWS CodeBuild |
| リリースの流れの自動化 | AWS CodePipeline |
| 分散アプリのトレースとボトルネックの調査 | AWS X-Ray |
| コマンドでの操作 | AWS CLI |

CodePipeline は流れ全体を管理し、CodeBuild はその中のビルドを行います。X-Ray はアプリを調べるもので、API 操作の記録の CloudTrail とは別です。

詳細: [サービスの役割](../../services/cicd.md#overview)、[CodeBuild](../../services/cicd.md#codebuild)、[CodePipeline](../../services/cicd.md#codepipeline)、[X-Ray](../../services/observability.md#xray)

### エンドユーザーコンピューティング {#t3-8-euc}

利用者の端末に、クラウドで動く仮想マシンの画面を映すサービスです。

| サービス | 何を届けるか | 選ぶ条件 |
|---|---|---|
| Amazon WorkSpaces | デスクトップ全体 | 社員に仮想デスクトップを配る |
| Amazon AppStream 2.0 | 特定のアプリ | CAD などの重いアプリをブラウザーへ配信する |
| Amazon WorkSpaces Secure Browser | 管理されたブラウザー | 社内 Web アプリや SaaS に安全に接続する |

詳細: [WorkSpaces](../../services/other-services.md#workspaces)、[WorkSpaces Applications](../../services/other-services.md#appstream)、[Secure Browser](../../services/other-services.md#secure-browser)

### フロントエンドとモバイル {#t3-8-frontend}

AWS Amplify は、Web とモバイルのフロントエンドの開発とホスティングを支援します。Git リポジトリに接続すれば、ブランチごとにビルドしてデプロイします。

「フロントエンドの開発者が、サーバーの管理なしで Web アプリを公開したい」なら Amplify です。

詳細: [Amplify](../../services/cicd.md#amplify)

### IoT {#t3-8-iot}

AWS IoT Core は、デバイスと AWS を接続するメッセージブローカーです。MQTT などを使います。ルールを使えば、データを Lambda や DynamoDB に渡せます。

「多数のセンサーを AWS に接続して管理したい」なら IoT Core です。

詳細: [AWS IoT Core](../../services/other-services.md#iot-core)

## 確認問題 {#self-check}

??? question "問1: 東京の AZ の 1 つが止まってもサービスを続けたいです。最も基本的な構成は何ですか？"
    複数の AZ にインスタンスを置き、ロードバランサーで振り分けます。AZ は単一障害点を共有しないように設計されているからです。複数リージョンは、リージョン全体の障害やデータ主権などの要件があるときに検討します。

??? question "問2: 動画のエンコードで CPU を長時間多く使います。どのカテゴリのインスタンスを選びますか？"
    コンピューティング最適化（C 系）です。メモリ最適化は大きなメモリを使う処理に、ストレージ最適化は高 IOPS のローカルディスクを使う処理に向きます。

??? question "問3: 既存の Oracle データベースを、なるべく止めずに Aurora PostgreSQL へ移したいです。どのツールを使いますか？"
    スキーマの変換に AWS SCT、データの移行に AWS DMS を使います。DMS は元のデータベースを動かしたまま、変更を流し続けられます。エンジンが異なるので、スキーマの変換が必要です。

??? question "問4: 特定の攻撃元の IP アドレスをサブネットの単位で拒否したいです。何を使いますか？"
    ネットワーク ACL です。セキュリティグループには拒否のルールがないので、この要件には使えません。

??? question "問5: 法律で 7 年保管が必要な監査ログがあり、読むのは年 1 回未満で、取り出しに半日ほどかかっても構いません。最も安い S3 のストレージクラスは何ですか？"
    S3 Glacier Deep Archive です。取り出しに時間がかかる代わりに長期保管に向きます。すぐ読む必要があるなら Glacier Instant Retrieval です。

??? question "問6: コールセンターを自前の設備なしで作り、問い合わせの音声を文字に変換して分析したいです。どのサービスを組み合わせますか？"
    Amazon Connect でコンタクトセンターを作り、Amazon Transcribe で音声を文字にします。文字にしたテキストの感情の分析には Amazon Comprehend を使います。
