# リソースの提供単位と EC サイトの構成例

AWS のリソースは、どの単位で作られ、どこに置かれるかが決まっています。ここが分かると、障害の影響範囲、冗長化の要否、VPC エンドポイントの要否を判断できます。

## 2 つの軸で考える {#two-axes}

提供単位と VPC の内外は、別の軸です。「VPC サービス」という公式の区分はありません。

| 軸 | 問い | 値 |
|---|---|---|
| 提供単位 | どの範囲で作られ、どこまで障害が広がるか | グローバル、リージョン、AZ |
| VPC の内外 | 自分のネットワークの中に置くか | VPC 内、VPC 外、接続を選べる |

AWS の公式の資料は、サービスをグローバル、リージョン、ゾーン（AZ）の3つに分けて説明しています。

[![リソースの提供単位](../assets/diagrams/resource-scope-layers.png)](../assets/diagrams/resource-scope-layers.png)

| 単位 | 意味 | 障害の考え方 |
|---|---|---|
| グローバル | リソースがリージョンに属さない | 多くはコントロールプレーンが 1 つのリージョンにある。作成や変更が止まっても、データプレーンは動き続ける設計 |
| リージョン | AWS が複数の AZ にまたがって動かす | 1 つの AZ の障害は AWS が吸収する。S3 のように AZ を選ばないものが多いが、ALB のようにサブネットで AZ を指定するものもある |
| AZ | 自分で AZ を選んで作る | AZ の障害の影響を受ける。自分で複数の AZ に置く |

**例**: S3 はリージョンのサービスなので、AZ を選びません。データは既定で複数の AZ に分散します。EC2 は AZ のサービスなので、1 台だけなら、その AZ の障害で止まります。

## リソースごとの提供単位 {#scope-table}

「VPC」の列は、リソースを置く場所です。

### グローバル {#scope-global}

| リソース | VPC | 補足 |
|---|---|---|
| IAM（ユーザー、ロール、ポリシー） | 外 | 変更は `us-east-1` のコントロールプレーンで行う |
| AWS Organizations | 外 | 同じく `us-east-1` |
| Route 53 のホストゾーン | 外 | プライベートホストゾーンは VPC に関連付ける |
| CloudFront | 外 | 配信は世界のエッジで行う。ACM の証明書は `us-east-1` のものを使う |
| WAF（CloudFront 用） | 外 | `us-east-1` で作る。ALB 用はリージョンごとに別に作る |
| Global Accelerator | 外 | 接続先にはリージョンの ALB などを指定する |

### リージョン: VPC の外 {#scope-regional-outside}

| リソース | 補足 |
|---|---|
| S3 バケット | 名前は既定で全アカウント共通の空間にあるが、データはリージョンに置かれる |
| DynamoDB テーブル | グローバルテーブルは、複数のリージョンのテーブルを同期する機能 |
| SQS、SNS、EventBridge | VPC からはエンドポイントか NAT 経由で呼ぶ |
| Step Functions | 同上 |
| KMS キー | マルチリージョンキーも、各リージョンのキーとして存在する |
| Secrets Manager、Parameter Store | シークレットはリージョンごと |
| CloudWatch、CloudTrail の証跡 | メトリクスとログはリージョンごと。CloudTrail の証跡は単一リージョンと複数リージョンを選べる |
| ECR リポジトリ | 別のリージョンへ複製できる |
| Cognito ユーザープール | リージョンごと |
| ACM の証明書 | 使うリソースと同じリージョンに作る |
| Bedrock | リージョンごとに使えるモデルが異なる |

### リージョン: VPC の中か、接続を選べる {#scope-regional-vpc}

| リソース | 配置 | 補足 |
|---|---|---|
| VPC | リージョンに 1 つ | そのリージョンの全 AZ にまたがる |
| セキュリティグループ | VPC に属する | ENI に付ける。サブネットとは独立 |
| ネットワーク ACL | VPC に属する | サブネットに関連付ける |
| ルートテーブル | VPC に属する | サブネットに関連付ける |
| インターネットゲートウェイ | VPC に 1 つ | AZ を選ばない |
| ゲートウェイエンドポイント | VPC に属する | ルートテーブルに経路を足す。S3 と DynamoDB 用 |
| リージョナル NAT ゲートウェイ | VPC に属する | ワークロードのある AZ へ自動で広がる（最大 60 分かかる場合がある）。パブリックサブネットが不要。プライベート接続には使えない |
| ALB、NLB | サブネットを指定する | ALB は 2 つ以上の AZ のサブネットを指定する |
| Auto Scaling グループ | サブネットを指定する | 複数の AZ に EC2 を配置する |
| Lambda | 既定は VPC の外 | VPC に接続すると、指定したサブネットに ENI を置く |
| ECS クラスター、EKS クラスター | クラスター自体はリージョン | タスクや Pod、ノードはサブネットに置く |
| EFS（リージョン） | サブネットごとにマウントターゲット | 複数の AZ にデータを保存する |
| Aurora クラスター | DB サブネットグループ | ストレージは複数の AZ にまたがり、インスタンスは AZ に置く |
| Transit Gateway | VPC の外 | VPC をアタッチする |
| API Gateway | VPC の外 | プライベート API は VPC エンドポイントから呼ぶ |

### AZ {#scope-zonal}

| リソース | 配置 | 補足 |
|---|---|---|
| サブネット | VPC の中 | 1 つの AZ に収まり、AZ をまたげない |
| EC2 インスタンス | サブネット | AMI はリージョン単位だが、インスタンスは AZ 単位 |
| ENI | サブネット | 同じ AZ のインスタンスにだけ付けられる |
| EBS ボリューム | VPC の外 | 同じ AZ のインスタンスに付ける。スナップショットはリージョン単位 |
| ゾーン NAT ゲートウェイ | パブリックサブネット | 高可用にするなら AZ ごとに作る |
| インターフェイスエンドポイントの ENI | サブネット | AZ ごとに置く |
| RDS の DB インスタンス | DB サブネットグループ | Multi-AZ はスタンバイを別の AZ に置く |
| ElastiCache のノード | サブネットグループ | レプリカを別の AZ に置く |
| EFS One Zone | サブネット | 1 つの AZ にだけデータを保存する |
| S3 Express One Zone | VPC の外 | 1 つの AZ にデータを置くディレクトリバケット |

## 間違えやすい点 {#traps}

| 思い込み | 実際 |
|---|---|
| S3 はグローバルのサービス | バケットはリージョンに作る。名前の空間が既定で共通なだけ |
| ARN にリージョンがなければグローバル | S3 の ARN `arn:aws:s3:::my-bucket` にはリージョンがないが、S3 はリージョンのサービス |
| ARN にリージョンがあれば AZ を問わない | `arn:aws:ec2:ap-northeast-1:111122223333:instance/i-0abc` は AZ のリソース |
| VPC は AZ ごとに作る | VPC はリージョン単位で、AZ ごとに分かれるのはサブネット |
| ALB は 1 つの AZ のリソース | ALB は 2 つ以上の AZ のサブネットに置く |
| Lambda は VPC の中で動く | 既定では自分の VPC の外。VPC のリソースを呼ぶときだけ接続する |
| VPC に接続した Lambda はインターネットに出られる | パブリックサブネットに接続しても出られない。NAT が必要 |
| IAM の変更はどのリージョンでも独立している | 認証と認可は各リージョンで動くが、変更は `us-east-1` のコントロールプレーンで行う |

## EC サイトの構成例 {#ec-site}

東京リージョンの EC サイト `shop.example.com` を例にします。公開、注文後の処理、プライベートな通信の3枚に分けます。

### 商品ページと購入のリクエスト {#ec-site-web}

[![EC サイトのリクエストの流れ](../assets/diagrams/ec-site-web.png)](../assets/diagrams/ec-site-web.png)

| リソース | 単位 | VPC | この構成での設定の例 |
|---|---|---|---|
| Route 53 | グローバル | 外 | `shop.example.com` を CloudFront へのエイリアスにする |
| CloudFront | グローバル | 外 | `/images/*` は S3、それ以外は ALB へ送る |
| WAF | グローバル | 外 | CloudFront 用の Web ACL を `us-east-1` に作る |
| S3 | リージョン | 外 | 商品画像を置き、OAC で CloudFront からだけ読ませる |
| VPC | リージョン | 内 | `10.0.0.0/16` |
| ALB | リージョン | 内 | `10.0.0.0/24`（1a）と `10.0.1.0/24`（1c）に置く |
| Fargate タスク | AZ | 内 | `10.0.10.0/24`（1a）と `10.0.11.0/24`（1c）に置く |
| Aurora | クラスターはリージョン、インスタンスは AZ | 内 | ライターを 1a、リーダーを 1c に置く |
| ElastiCache | ノードは AZ | 内 | プライマリを 1a、レプリカを 1c に置く |

証明書は 2 枚必要です。CloudFront 用は `us-east-1` に、ALB 用は東京に ACM で作ります。

通信はセキュリティグループで順に絞ります。

| 対象 | 許可する受信 | 許可する送信元 |
|---|---|---|
| `sg-alb` | 443 | CloudFront のマネージドプレフィックスリスト |
| `sg-app` | 8080 | `sg-alb` |
| `sg-db` | 3306（Aurora MySQL） | `sg-app` |
| `sg-cache` | 6379 | `sg-app` |

**例**: 開発者が `sg-db` に `10.0.0.0/16` からの 3306 を許可すると、ALB のサブネットなど無関係な場所からも DB へ接続を試せてしまいます。送信元はセキュリティグループで指定します。

**誤ると**: `sg-alb` を `0.0.0.0/0` に開けると、CloudFront と WAF を通らずに ALB へ直接アクセスできます。WAF のルールを回避されます。プレフィックスリストは CloudFront のサーバー全体を許すので、自分のディストリビューションに絞るなら、秘密のカスタムヘッダーも ALB で確認します。

### AZ が止まったときの動き {#ec-site-az-failure}

AZ 1a が止まった場合を、単位ごとに追います。

| リソース | 動き |
|---|---|
| Route 53、CloudFront、S3、DynamoDB | AZ 1 つの障害は AWS が吸収するので、自分の作業はない |
| ALB | 1c の正常なターゲットへ送る。1a の一部だけが不調で判定されにくいときは、ゾーンシフトで 1a を切り離す |
| Fargate タスク | 1c のタスクが処理を続ける。ECS は 1c に新しいタスクを起動する |
| Aurora | 1c のリーダーをライターへ昇格する。接続はクラスターエンドポイントを使う |
| ElastiCache | Multi-AZ を有効にしていれば、1c のレプリカを昇格する |

**台数の例**: ピーク時に 4 タスクが必要なら、各 AZ に 2 タスクでは足りません。1a が止まると 2 タスクになり、新しいタスクが起動するまで処理能力が半分になります。障害時も余裕を持つなら、各 AZ に 4 タスク、計 8 タスクにします。公式の資料はこのように、障害時に増やさず済む容量を先に持つ設計を勧めています。費用とのトレードオフです。

### 注文後の非同期処理 {#ec-site-order}

注文の確定後の処理を分離すると、メールの遅延が購入を止めません。

[![EC サイトの注文後の処理](../assets/diagrams/ec-site-order.png)](../assets/diagrams/ec-site-order.png)

| リソース | 単位 | VPC | この構成での設定の例 |
|---|---|---|---|
| DynamoDB | リージョン | 外 | 注文履歴。パーティションキーは `customerId`、ソートキーは `orderedAt` |
| EventBridge | リージョン | 外 | `OrderPlaced` を 2 つのキューへ送るルール |
| SQS | リージョン | 外 | メール用と出荷用に分ける。失敗に備えて DLQ を付ける |
| Lambda | リージョン | 外 | キューを読む。VPC のリソースを呼ばないので接続しない |
| SES | リージョン | 外 | 注文確認のメールを送る |

図の中で VPC の中で動くアプリは注文 API だけです。VPC の外のサービスを呼ぶ経路を、エンドポイントが作ります。

| 呼び先 | エンドポイント | 配置 |
|---|---|---|
| DynamoDB | ゲートウェイ | ルートテーブルに経路を足す |
| EventBridge | インターフェイス | サブネットに ENI を置く。カスタムイベントバスは `eventsv2`、Classic のカスタムバスは `events` |

**例**: メールの Lambda がタイムアウト 30 秒なら、SQS の可視性タイムアウトは 180 秒以上にします（AWS は関数のタイムアウトの 6 倍を推奨）。短いと、処理中のメッセージが再配信されて、確認メールが二重に届きます。

### プライベートサブネットからの通信 {#ec-site-private}

Fargate タスクはプライベートサブネットにあるので、VPC の外へ出る経路が必要です。

[![EC サイトのプライベートな通信](../assets/diagrams/ec-site-private.png)](../assets/diagrams/ec-site-private.png)

| 通信先 | 経路 | 理由 |
|---|---|---|
| 外部の決済 API | NAT ゲートウェイ → インターネットゲートウェイ | AWS の外なので、インターネットに出る |
| ECR | インターフェイスエンドポイント（`ecr.api`、`ecr.dkr`） | イメージの取得 |
| イメージのレイヤー | S3 ゲートウェイエンドポイント | ECR のレイヤーは S3 に保存されている |
| Secrets Manager | インターフェイスエンドポイント | DB のパスワードの取得 |
| CloudWatch Logs | インターフェイスエンドポイント（`logs`） | タスクのログの送信 |

**誤ると**: NAT もエンドポイントもないと、タスクはイメージを取得できず、起動に失敗します。`ecr.dkr` だけ作って S3 ゲートウェイエンドポイントを忘れた場合も、レイヤーを取得できません。

NAT ゲートウェイは 2 つの方式があります。

| 方式 | 単位 | 作り方 | 例 |
|---|---|---|---|
| ゾーン | AZ | AZ ごとにパブリックサブネットに作り、経路も AZ ごとに書く | 1a と 1c に 1 つずつ |
| リージョナル | VPC | モードを選んで VPC に作る。パブリックサブネットは不要 | VPC に 1 つ |

**例**: ゾーン NAT を 1a にだけ作り、1c のルートも 1a へ向けると、1a の障害で 1c のタスクも外部の決済 API を呼べなくなります。

## 参考 {#references}

- [AWS Fault Isolation Boundaries: Zonal services](https://docs.aws.amazon.com/whitepapers/latest/aws-fault-isolation-boundaries/zonal-services.html)
- [AWS Fault Isolation Boundaries: Regional services](https://docs.aws.amazon.com/whitepapers/latest/aws-fault-isolation-boundaries/regional-services.html)
- [AWS Fault Isolation Boundaries: Global services](https://docs.aws.amazon.com/whitepapers/latest/aws-fault-isolation-boundaries/global-services.html)
- [How Amazon VPC works](https://docs.aws.amazon.com/vpc/latest/userguide/how-it-works.html)
- [Regional NAT gateways](https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateways-regional.html)
- [Giving Lambda functions access to resources in a VPC](https://docs.aws.amazon.com/lambda/latest/dg/configuration-vpc.html)
- [Manage your Amazon EC2 resources](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/resources.html)
