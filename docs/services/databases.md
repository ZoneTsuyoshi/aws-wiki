# データベースとキャッシュ

RDS、Aurora、ElastiCache の使い方と、アクセスパターンに合わせたデータストアとキャッシュの選び方をまとめます。DynamoDB 自体の詳細は [DynamoDB](dynamodb.md) を参照してください。

[![キャッシュの層とデータストア](../assets/diagrams/databases-cache-layers.png)](../assets/diagrams/databases-cache-layers.png)

## データストアの選び方 {#choosing-data-store}

まずアクセスパターンを確認します。どのキーで読むのか、どの程度の遅延を許すのか、結合やトランザクションが必要か、という点です。

| アクセスパターン | 候補 | 理由 |
| --- | --- | --- |
| キーで引く、遅延を一定にしたい、規模が読めない | [DynamoDB](dynamodb.md) | 規模によらず低レイテンシ。スキーマレス |
| 結合、複雑なクエリ、複数テーブルのトランザクション | RDS、Aurora | リレーショナルモデルと SQL |
| 読み取りが多い SQL ワークロードを高可用で | Aurora | 共有ストレージと最大 15 個のレプリカ |
| マイクロ秒で読みたい、データは再生成できる | ElastiCache | インメモリ |
| DynamoDB の読み取りだけを速くしたい | DAX | DynamoDB 専用でコード変更が少ない |
| 全文検索、ログ分析、柔軟な検索条件 | OpenSearch Service | 検索と分析のエンジン |
| 大きなファイル、静的コンテンツ、アーカイブ | [S3](s3.md) | オブジェクトストレージ |
| ファイルシステムとして共有したい | [EFS](storage.md) | NFS |

```mermaid
flowchart TD
    A["保存したいデータ"] --> B{"ファイルや大きなバイナリ?"}
    B -- "はい" --> S3["S3"]
    B -- "いいえ" --> C{"全文検索やログ分析が主?"}
    C -- "はい" --> OS["OpenSearch Service"]
    C -- "いいえ" --> D{"失っても再生成できる一時データ?"}
    D -- "はい" --> EC["ElastiCache"]
    D -- "いいえ" --> E{"結合や複雑な SQL が必要?"}
    E -- "はい" --> RDS["RDS / Aurora"]
    E -- "いいえ" --> DDB["DynamoDB"]
```

### OpenSearch Service {#opensearch}

OpenSearch クラスターを管理してくれるサービスです。AWS ではクラスターのことをドメインと呼びます。

- **向いている用途**: 全文検索、ログ分析、アプリケーションのリアルタイム監視、クリックストリーム分析。
- **データの投入**: S3、Kinesis、Data Firehose、DynamoDB、CloudWatch Logs などと連携できます。
- **よくある構成**: 主データは DynamoDB に置き、Streams と Lambda で OpenSearch に同期して検索だけを任せます。DynamoDB の `Scan` と `FilterExpression` で検索している構成を見たら、この形を検討します。

OpenSearch を主データストアと考えるのではなく、検索用の副データとして扱うのが基本です。

## RDS {#rds}

MySQL、PostgreSQL、MariaDB、Oracle、SQL Server、Db2 を実行するマネージドのリレーショナルデータベースです。

### リードレプリカと Multi-AZ {#read-replicas}

目的が違います。読み取りを増やすならリードレプリカ、可用性を高めるなら Multi-AZ です。

| 観点 | リードレプリカ | Multi-AZ のスタンバイ |
| --- | --- | --- |
| 目的 | 読み取りのスケール | 高可用性 |
| 複製 | 非同期 | 同期 |
| 読み取りに使えるか | 使える | 使えない |
| 接続先 | レプリカのエンドポイントをアプリで指定 | プライマリと同じエンドポイント |
| 自動スケール | なし。手動で作成と削除 | 該当なし |
| 別リージョン | 可能 | 同一リージョン内 |
| 昇格 | スタンドアロンの DB に昇格できる | 障害時に自動フェイルオーバー |

- レプリカは非同期なので、書いた直後の読み取りには古い値が返る可能性があります。整合性が必要な読み取りはプライマリに送ります。
- レポートのような重いクエリをレプリカに逃がすと、本番の負荷を下げられます。
- 両者は併用できます。

Multi-AZ には 2 つの形態があります。「スタンバイは読めない」のは DB インスタンス配置のほうだけです。

| 観点 | Multi-AZ DB インスタンス | Multi-AZ DB クラスター |
| --- | --- | --- |
| 構成 | プライマリ 1 + スタンバイ 1 | ライター 1 + 読み取り可能なリーダー 2(3 つの AZ) |
| 複製 | 同期 | 準同期 |
| スタンバイ、リーダーの読み取り | 不可 | 可 |

| 設定 | 値 | 動作と落とし穴 |
| --- | --- | --- |
| フェイルオーバーの時間 | 通常 60〜120 秒 | DNS がスタンバイに切り替わる。接続は作り直す |
| JVM の DNS キャッシュ | TTL を 60 秒以下に推奨 | 長いと古い IP に接続し続ける |
| レプリカの数 | 1 つのインスタンスから同一リージョンに最大 15 個 | Auto Scaling はない |
| レプリカの前提 | 自動バックアップの有効化 | バックアップ保持期間が 0 だと作成できない |
| 遅延の監視 | `ReplicaLag` | 古い値が返る原因を確認する |
| 書き込みの遅延 | Multi-AZ は同期複製のぶん増えることがある | シングル AZ より遅いことがある |

**例**: 毎朝のレポートで本番が重いなら、リードレプリカを作りレポートをそちらに向けます。アプリの接続先を指定し直す必要があります。Multi-AZ に変更しても、読み取りの負荷は減りません。

### IAM データベース認証 {#rds-iam-auth}

パスワードの代わりに、AWS 署名バージョン 4 で作る認証トークンで接続します。MariaDB、MySQL、PostgreSQL で使えます。

| 項目 | 内容 |
| --- | --- |
| 有効化 | DB の設定で有効にする(`--enable-iam-database-authentication`) |
| トークンの寿命 | 15 分。接続の確立にだけ使い、既存の接続は切れない |
| 必要な権限 | `rds-db:connect`。`rds:` ではない |
| リソース | `arn:aws:rds-db:リージョン:アカウント:dbuser:リソース ID/DB ユーザー名` |
| DB 側のユーザー | MySQL は `AWSAuthenticationPlugin`、PostgreSQL は `rds_iam` ロール |
| 通信 | SSL/TLS を使う |

```bash
TOKEN=$(aws rds generate-db-auth-token \
  --hostname mydb.example.ap-northeast-1.rds.amazonaws.com \
  --port 3306 --username app_user --region ap-northeast-1)
mysql -h mydb.example.ap-northeast-1.rds.amazonaws.com -u app_user \
  --enable-cleartext-plugin --ssl-ca=global-bundle.pem --password="$TOKEN"
```

**落とし穴**:

- Route 53 のカスタム DNS 名でトークンを作ることはできません。DB のエンドポイントを使います。
- PostgreSQL では `rds_iam` を付けたユーザーは、パスワードで入れなくなります。
- CloudWatch と CloudTrail は IAM 認証を記録しません。

### Secrets Manager との統合 {#rds-secrets-manager}

`--manage-master-user-password` を指定すると、RDS がマスターユーザーのパスワードを生成し、Secrets Manager で管理します。

| 項目 | 内容 |
| --- | --- |
| ローテーション | デフォルトで 7 日ごと。スケジュールは変更できる |
| 暗号化 | `aws/secretsmanager` かカスタマーマネージドキー(`MasterUserSecretKmsKeyId`)。管理を始めた後はキーを変更できない |
| DB の削除 | シークレットも削除される |
| 取得 | アプリは `GetSecretValue` で読む |

**例**: Lambda の環境変数にパスワードを書く代わりに、シークレットを読むようにします。ローテーションで値が変わるので、長時間キャッシュすると認証エラーになります。ローテーションの詳細は [Secrets Manager と Parameter Store](secrets.md) を参照してください。

### SSL/TLS {#rds-ssl}

| エンジン | 強制する設定 | デフォルト |
| --- | --- | --- |
| PostgreSQL | パラメータ `rds.force_ssl=1` | バージョン 15 以降は 1(有効)。それより前は 0 |
| MySQL | パラメータ `require_secure_transport=ON` | 無効 |

設定はカスタムのパラメータグループで変えます。PostgreSQL で強制を有効にすると、SSL を使わない接続は拒否されます。

クライアントは AWS の CA バンドル(`global-bundle.pem`)でサーバーを検証します。PostgreSQL の `sslmode=verify-full` はサーバー証明書とホスト名の両方を確認します。

## Aurora {#aurora}

MySQL、PostgreSQL 互換のマネージドデータベースです。データは DB インスタンスから独立したクラスターボリュームに保存され、ライターとレプリカが共有します。

| エンドポイント | 接続先 | 用途 |
| --- | --- | --- |
| クラスター(ライター) | 現在のプライマリ | 書き込みと一般的な接続 |
| リーダー | Aurora レプリカ間で接続を分散 | 読み取り |
| カスタム | 指定したインスタンスのグループ | 性能の違うインスタンスの使い分け |
| インスタンス | 特定のインスタンス | 診断、チューニング |
| グローバルデータベースのライター | プライマリリージョンのクラスター | リージョンをまたぐ切り替え |

- レプリカは最大 15 個で、フェイルオーバー先にもなります。
- レプリカの遅延は通常 100 ミリ秒を大きく下回りますが、書き込みが多いと増えます。
- アプリはクラスターとリーダーのエンドポイントを使います。インスタンスのエンドポイントをコードに書くとフェイルオーバーに追従できません。

!!! tip "リーダーエンドポイントの分散"
    リーダーエンドポイントは接続を分散します。分散の単位はクエリではなく接続です。接続プールを使う場合は接続を作り直すタイミングも考慮します。

### エンドポイントの動作 {#aurora-endpoints}

| エンドポイント | 細かい動作 |
| --- | --- |
| クラスター | 書き込みができる唯一のエンドポイント。フェイルオーバーで指す先が変わる |
| リーダー | レプリカがなければプライマリに接続する。この場合は書き込みも通る |
| カスタム | 1 クラスターに最大 5 個。最初は 1 つもない。自分でインスタンスを選ぶ |

**例**: レポート用に大きなインスタンス 2 台、Web 用に小さなインスタンス 3 台がある場合、カスタムエンドポイントを 2 つ作ります。リーダーエンドポイントでは、レポートが小さなインスタンスに当たることがあります。

**落とし穴**: カスタムエンドポイントの中のインスタンスは性能をそろえます。接続がどれに行くか選べないからです。

### 昇格の優先度 {#aurora-failover-priority}

レプリカには 0(最優先)から 15(最低)の優先度を付けます。同じ優先度なら、サイズの大きいレプリカが昇格します。レプリカがないとインスタンスを作り直すので、復旧に時間がかかります。

データは 3 つの AZ にまたがる 6 つのストレージノードに同期して書き込まれます。

### Aurora Serverless v2 {#aurora-serverless-v2}

容量を ACU という単位で自動調整します。1 ACU は約 2 GiB のメモリと、対応する CPU とネットワークです。

| 設定 | 値 | 動作 |
| --- | --- | --- |
| `MinCapacity` | 0 以上(0 は自動一時停止対応のバージョンのみ) | アイドル時の費用を決める。インスタンス数 × 最小 ACU が目安 |
| `MaxCapacity` | 最大 256(プラットフォームのバージョンで異なる) | ピークの上限 |
| `SecondsUntilAutoPause` | 300〜86,400 秒、デフォルト 300 | 最小 0 のとき、接続がないまま経過すると一時停止する |
| スケーリング単位 | 0.5 ACU | インスタンスの追加なしで増減する |

```bash
aws rds modify-db-cluster --db-cluster-identifier my-cluster \
  --serverless-v2-scaling-configuration \
  MinCapacity=0,MaxCapacity=8,SecondsUntilAutoPause=600
```

**例**: 開発環境は夜間に接続がないので `MinCapacity=0` にします。朝の最初の接続は再開を待つため遅くなります。本番の Web アプリで同じ設定にすると、最初のリクエストがタイムアウトすることがあります。

### Aurora グローバルデータベース {#aurora-global-database}

1 つのプライマリリージョンと、最大 10 の読み取り専用セカンダリリージョンで構成します。

| 項目 | 内容 |
| --- | --- |
| 書き込み | プライマリのクラスターのみ。グローバルデータベースのライターエンドポイントで接続する |
| セカンダリの読み取り | 最大 16 個の読み取り専用インスタンス |
| 書き込み転送 | 有効にするとセカンダリに来た書き込みをプライマリに転送する |
| 切り替え(計画) | スイッチオーバー。リージョンのローテーションなどに使う |
| 切り替え(障害) | フェイルオーバー。プライマリのリージョン障害時に使う |
| 前提 | マネージドの切り替えには、同じメジャーとマイナーのエンジンバージョンが必要 |

DynamoDB のグローバルテーブルと違い、どのリージョンにも書き込めるわけではありません。

## 接続プーリングと RDS Proxy {#connection-pooling}

DB への接続の確立は CPU とメモリを消費します。接続を使い回す仕組みが接続プールです。

| 場所 | 実装 | 向く場面 |
| --- | --- | --- |
| アプリ内 | ライブラリのプール | EC2 やコンテナのように長く動くプロセス |
| 外部 | RDS Proxy | Lambda のように同時実行が急に増える構成、多数のアプリからの接続 |

**プールサイズの考え方**: プールの最大接続数 × アプリのインスタンス数が、DB の最大接続数を超えないようにします。Auto Scaling でインスタンスが増えると合計が増える点に注意します。

### RDS Proxy {#rds-proxy}

アプリと DB の間に入り、接続を共有します。

| 機能 | 内容 |
| --- | --- |
| 多重化 | トランザクションが終わるごとに DB 接続を他のクライアントが再利用 |
| 負荷保護 | 接続数を制御し、すぐに処理できない接続は待たせる。上限を超えると拒否 |
| フェイルオーバー | スタンバイへの切り替え時にアプリの接続を保持 |
| 認証 | クライアントは IAM 認証が可能。プロキシから DB へは IAM か Secrets Manager の認証情報 |

制約も押さえます。

- プロキシは DB と同じ VPC に置きます。パブリックアクセスはできません。
- レプリケーション構成の RDS では、関連付けられるのはライターだけです。リードレプリカには付けられません。
- デフォルトエンドポイントは 2 つの AZ に配置されます。

**ピン留め(pinning)**: セッションの状態が変わると、そのクライアント接続は特定の DB 接続に固定され、再利用の効果が下がります。

| エンジン | ピン留めの主な原因 |
| --- | --- |
| 共通 | 16 KB を超えるステートメント |
| MySQL、MariaDB | テーブルロック、`GET_LOCK`、一時テーブル、プリペアドステートメント、一部の変数設定 |
| PostgreSQL | `SET`、`PREPARE`、一時テーブル、カーソル、`LISTEN`、シーケンス操作、セッションレベルのアドバイザリロック |

CloudWatch の `DatabaseConnectionsCurrentlySessionPinned` で発生頻度を確認します。接続ごとに同じ `SET` を実行しているなら、プロキシの初期化クエリに移します。

### RDS Proxy の設定 {#rds-proxy-settings}

| 設定 | デフォルト | 範囲 | 動作 |
| --- | --- | --- | --- |
| `MaxConnectionsPercent` | 100(SQL Server は 10) | 1〜100 | DB の `max_connections` に対する、プールの上限の割合 |
| `MaxIdleConnectionsPercent` | `MaxConnectionsPercent` の半分 | 0〜`MaxConnectionsPercent` | アイドル接続を残す割合。低いほど早く閉じる |
| `ConnectionBorrowTimeout` | 120 秒 | 0〜300 秒 | 空き接続を待つ時間。超えるとタイムアウトエラー |
| `IdleClientTimeout` | 1,800 秒(30 分) | - | アイドルのクライアント接続を閉じるまでの時間 |
| `InitQuery` | なし | - | 新しい DB 接続を開くときに実行する SQL。パスワードなどは書かない |
| `SessionPinningFilters` | なし | `EXCLUDE_VARIABLE_SETS` | 変数の `SET` によるピン留めを除外する。別の接続に変数が影響するおそれがある。PostgreSQL は非対応 |
| `RequireTLS` | - | true / false | クライアント接続に TLS を強制する |
| `DefaultAuthScheme` | `NONE` | `NONE`、`IAM_AUTH` | `IAM_AUTH` はプロキシから DB まで IAM で認証する |
| `DebugLogging` | - | true / false | 詳細ログ。費用と性能に影響するので常用しない |

**例**: `max_connections` が 1,000 の DB に、同じ DB を使うプロキシを 2 つ付けるなら、`MaxConnectionsPercent` をそれぞれ 40 にして、合計 800 接続にします。残りを管理者とほかの接続に残します。

**症状と対処**:

| 症状 | 原因と対処 |
| --- | --- |
| `Timed-out waiting to acquire database connection` | `ConnectionBorrowTimeout` 内に接続を取れない。ピン留めや長いトランザクションを確認し、`MaxConnectionsPercent` や DB の容量を増やす |
| `MaxDatabaseConnectionsAllowed` に張り付く | プールの上限に達している |
| 効果が出ない | ピン留めを確認する |

CloudFormation や CLI では、接続設定はターゲットグループ `default` に付きます。プロキシを作ると自動で作られます。

Secrets Manager で認証する場合は、プロキシの IAM ロールにシークレットの読み取りを許可します。ロールがシークレットを読めないと、プロキシは DB に接続できません。

IAM 認証については、プロキシに接続するアプリの権限は `rds-db:connect` です。

Lambda では、接続をハンドラの外で作り、実行環境の再利用時に使い回します。

```python
import os
import pymysql

# 実行環境ごとに 1 回だけ実行される
conn = pymysql.connect(
    host=os.environ["PROXY_ENDPOINT"],
    user=os.environ["DB_USER"],
    password=get_password(),
    database="app",
    ssl={"ca": "/opt/global-bundle.pem"},
)

def handler(event, context):
    with conn.cursor() as cur:
        cur.execute("SELECT name FROM users WHERE id = %s", (event["id"],))
        return cur.fetchone()
```

## ElastiCache {#elasticache}

インメモリのキャッシュとデータストアです。運用形態は 2 つあります。

| 形態 | 特徴 |
| --- | --- |
| サーバーレス | 名前を指定するだけで作成でき、容量は自動で調整 |
| ノードベース | ノードタイプ、数、配置を自分で決める。細かい制御が可能 |

### Redis OSS、Valkey と Memcached {#engines}

| 機能 | Valkey / Redis OSS | Memcached |
| --- | --- | --- |
| データ型 | 文字列、ハッシュ、リスト、セット、ソート済みセットなど | シンプルな文字列とオブジェクト |
| レプリケーション、高可用性 | あり | なし |
| 自動フェイルオーバー | あり | なし |
| バックアップと復元 | あり | ノードベースではなし |
| Pub/Sub | あり | なし |
| ソート済みセット(ランキング) | あり | なし |
| 地理空間インデックス | あり | なし |
| マルチスレッド | なし(Valkey 8.0 以降は非同期 I/O スレッドに対応) | あり |
| 向く用途 | ランキング、セッション、高可用性が必要なキャッシュ | シンプルなオブジェクトキャッシュ、大きなマルチコアノード |

クラスターモードを有効にすると、Valkey と Redis OSS はデータをシャードに分割して水平にスケールできます。

!!! tip "選択の目安"
    データ構造、永続性、フェイルオーバーのいずれかが要件にあれば Valkey または Redis OSS。とにかく単純でマルチスレッドの性能が欲しければ Memcached です。

一度作ったキャッシュのエンジンバージョンは、上げることはできますが、下げることはできません。

### クラスターモード {#cluster-mode}

| 観点 | 無効 | 有効 |
| --- | --- | --- |
| シャード | 1 | 1〜500 |
| 読み取りレプリカ | 0〜5 | シャードごとに 0〜5 |
| データの分割 | しない | シャードに分割 |
| 自動フェイルオーバー | 任意 | 必須 |
| オンラインのリシャード | なし | あり |
| バックアップ | 1 つの .rdb | シャードごとの .rdb |
| 接続先 | プライマリエンドポイント、リーダーエンドポイント | 設定エンドポイント |

**例**: データが 1 ノードのメモリに収まらない、または書き込みが 1 ノードの限界を超えるならクラスターモードを有効にします。読み取りだけが足りないなら、無効のままレプリカを増やします。

**落とし穴**: クラスターモードで使うクライアントは、クラスターに対応したものにします。クラスターモードを無効のまま読み取りをノードのエンドポイントに固定すると、ノードの増減で接続先を直す必要があります。リーダーエンドポイントはロードバランサーではなく、接続単位で DNS が振り分けるだけです。

### レプリケーションと Multi-AZ {#elasticache-replication}

複製は非同期です。プライマリが障害を起こすと、Multi-AZ が有効ならレプリカが自動で昇格し、プライマリエンドポイントの DNS が切り替わります。

| 落とし穴 | 内容 |
| --- | --- |
| レプリカ 0 でノードが故障 | データをすべて失う |
| フェイルオーバー直後 | 非同期複製のため、少量のデータを失うことがある |
| Memcached | レプリケーションがない。ノードが落ちるとそのノードのデータは消える |

Memcached のノードベースのクラスターでは、自動検出対応のクライアントが設定エンドポイントからノード一覧を取得します。

### 認証と暗号化 {#elasticache-security}

| 項目 | 内容 | 落とし穴 |
| --- | --- | --- |
| 転送中の暗号化 | `TransitEncryptionEnabled=true`。サーバーレスは常に有効 | クライアントでも TLS を有効にする。既存クラスターの変更は Valkey 7.2 以降、Redis OSS 7 以降 |
| 保存時の暗号化 | `AtRestEncryptionEnabled=true`。Valkey ではデフォルト `true`。サーバーレスは常に有効 | ノードベースの Valkey と Redis OSS は作成時のみ。後から有効にするならバックアップから作り直す |
| キー | サービス管理か、対称のカスタマーマネージドキー | - |
| AUTH トークン | `--auth-token` で指定。16〜128 文字の印字可能文字 | 転送中の暗号化が必須。ノードベース専用 |
| RBAC | ユーザーとユーザーグループで ACL を割り当てる | サーバーレスでは RBAC が必須。AUTH より優先して検討する |
| IAM 認証 | 一時的な認証情報で接続する | パブリックエンドポイントのサーバーレスでは必須 |
| mTLS | 非対応 | - |

使えるのは、AUTH トークンでは次の記号だけです: `!`、`&`、`#`、`$`、`^`、`<`、`>`、`-`。

トークンを無停止で変えるには、`ModifyReplicationGroup` を 2 段階で呼びます。

```bash
# 1. ROTATE: 新旧両方のトークンで接続できる
aws elasticache modify-replication-group --replication-group-id app-cache \
  --auth-token "$NEW_TOKEN" --auth-token-update-strategy ROTATE --apply-immediately
# 2. アプリを新しいトークンに切り替えた後、SET: 新しいトークンだけにする
aws elasticache modify-replication-group --replication-group-id app-cache \
  --auth-token "$NEW_TOKEN" --auth-token-update-strategy SET --apply-immediately
```

### 追い出しとメモリ {#eviction}

メモリが一杯になったときの動作は `maxmemory-policy` で決まります。デフォルトは `volatile-lru` です。

| 値 | 動作 | 使いどころ |
| --- | --- | --- |
| `volatile-lru` | TTL 付きのキーから、最近使っていないものを消す | TTL を付けるキャッシュとデータの混在 |
| `allkeys-lru` | すべてのキーから、最近使っていないものを消す | 純粋なキャッシュ |
| `volatile-lfu`、`allkeys-lfu` | 使う頻度の低いものを消す | 頻度の偏りが大きい |
| `volatile-random`、`allkeys-random` | ランダムに消す | - |
| `volatile-ttl` | TTL が短いものから消す | - |
| `noeviction` | 消さず、書き込みをエラーにする | データを失いたくない |

**落とし穴**: デフォルトの `volatile-lru` で TTL を付けていないと、追い出せるキーがなくなり書き込みが失敗することがあります。TTL を付けるか、`allkeys-lru` にします。

| メトリクスと設定 | 見方 |
| --- | --- |
| `Evictions` | 増え続けるならメモリ不足。スケールアップやシャードの追加を考える |
| `CacheHitRate` | 低いなら TTL やキーの設計を見直す |
| `DatabaseMemoryUsagePercentage` | 使用メモリの割合 |
| `reserved-memory-percent` | データ以外に確保するメモリの割合。デフォルト 25 |

## キャッシュ戦略 {#caching-strategies}

```mermaid
sequenceDiagram
    participant App as アプリ
    participant Cache as ElastiCache
    participant DB as データベース
    App->>Cache: 読み取り
    Cache-->>App: ミス
    App->>DB: 読み取り
    DB-->>App: データ
    App->>Cache: 書き込み (TTL 付き)
```

| 戦略 | 動作 | 長所 | 短所 |
| --- | --- | --- | --- |
| 遅延読み込み(レイジーローディング) | ミスしたときだけ DB から読み、キャッシュに入れる | 使うデータだけ入る。ノード障害でも動き続ける | ミス時に 3 回の往復。データが古くなる |
| ライトスルー | DB への書き込みと同時にキャッシュも更新 | 常に最新 | 書き込みが遅くなる。読まれないデータも入る。新しいノードにはデータがない |
| TTL | 一定時間で期限切れにする | 古さの上限を決められる。不要なデータが消える | 期限切れのたびに DB にアクセスが発生 |

実際には組み合わせます。**遅延読み込みとライトスルーの両方を使い、すべての書き込みに TTL を付ける**形が基本です。

```python
import json
import redis

cache = redis.Redis(host=CACHE_ENDPOINT, port=6379, ssl=True)
TTL = 300

def get_user(user_id):
    key = f"user:{user_id}"
    cached = cache.get(key)
    if cached is not None:
        return json.loads(cached)
    user = db_select_user(user_id)
    cache.set(key, json.dumps(user), ex=TTL)
    return user

def save_user(user_id, values):
    user = db_update_user(user_id, values)
    cache.set(f"user:{user_id}", json.dumps(user), ex=TTL)
    return user
```

TTL は秒数です。Valkey と Redis OSS はミリ秒でも指定できます。`ex=300` のキーは 5 分後に期限切れになり、次の読み取りはキャッシュミスになります。

**値の決め方の例**:

| データ | TTL の例 | 理由 |
| --- | --- | --- |
| 商品の説明 | 3,600 秒 | ほとんど変わらない。更新時はライトスルーで上書きする |
| 在庫数 | 30 秒 | 古いと困るが、毎回 DB を読むと重い |
| 価格の決済時の確認 | キャッシュしない | 古い値を使えない |

ここでの秒数は説明のための例です。どこまで古くても許せるかで決めます。

**落とし穴**:

- 遅延読み込みだけだと、DB を更新しても TTL まで古い値を返します。
- ライトスルーだけだと、新しいノードやフェイルオーバーの後に、書かれるまでデータがありません。
- すべてのキーを同じ TTL にすると一斉に切れて、DB に負荷が集中します。`ex=300 + random.randint(0, 60)` のように散らします。

## DAX、ElastiCache、CloudFront の使い分け {#cache-comparison}

| 観点 | DAX | ElastiCache | CloudFront |
| --- | --- | --- | --- |
| キャッシュする場所 | VPC 内、DynamoDB の前 | VPC 内、アプリの横 | エッジロケーション |
| 対象 | DynamoDB の項目と Query、Scan の結果 | アプリが入れる任意のデータ | HTTP レスポンス |
| アプリの変更 | DAX クライアントへの差し替え | キャッシュのロジックを自分で実装 | 不要(ヘッダーやポリシーの設定) |
| データストア | DynamoDB のみ | RDS、DynamoDB、計算結果など | S3、ALB、API Gateway など |
| 無効化 | TTL、書き込み、LRU | TTL か明示的な削除 | TTL か invalidation |
| 代表的な用途 | DynamoDB の読み取り負荷と遅延の削減 | DB クエリ結果、セッション、ランキング | 静的ファイル、世界中のユーザーへの配信 |

選び方の例を示します。

| 要件 | 選択 |
| --- | --- |
| DynamoDB の読み取りを最小のコード変更で速くしたい | DAX |
| RDS のクエリ結果をキャッシュしたい | ElastiCache |
| 複数の EC2 でセッションを共有したい | ElastiCache |
| ランキングを実装したい | ElastiCache の Valkey / Redis OSS(ソート済みセット) |
| 世界中のユーザーに画像を速く配信したい | CloudFront |
| API の GET レスポンスをエッジでキャッシュしたい | CloudFront |

## アプリケーションレベルのキャッシュ {#application-caching}

キャッシュはアプリの外だけではありません。層ごとに特徴があります。

| 層 | 例 | 適した用途 | 注意点 |
| --- | --- | --- | --- |
| プロセス内 | 変数、LRU キャッシュ、Lambda のハンドラ外の変数 | 設定値、参照データ | インスタンス間で共有されない |
| 共有 | ElastiCache | セッション、クエリ結果 | ネットワーク往復が発生 |
| HTTP | CloudFront、API Gateway | GET レスポンス | キーと無効化の設計が必要 |

```python
import time

_config = None
_loaded_at = 0.0

def get_config():
    global _config, _loaded_at
    if _config is None or time.time() - _loaded_at > 60:
        _config = load_config_from_ssm()
        _loaded_at = time.time()
    return _config
```

設計で考えることは次のとおりです。

- **キーの設計**: テナント ID やユーザー ID など、結果に影響するものをすべてキーに含めます。漏れると他人のデータが返ります。
- **TTL**: データが古くても許される時間から決めます。
- **一斉失効**: 同じ TTL のキーが同時に切れると DB に負荷が集中します。TTL にばらつきを持たせます。
- **障害時**: キャッシュが落ちても DB を読んで動くようにします。ただし DB が受けられる負荷かどうかも確認します。

## マルチテナントのデータアクセス {#multi-tenant}

1 つのアプリで複数の顧客(テナント)を扱う場合の分離方法です。認証と認可だけでは分離になりません。データアクセスの層でもテナントの境界を強制します。

| モデル | 構成 | 長所 | 短所 |
| --- | --- | --- | --- |
| サイロ | テナントごとに専用のリソース | 分離が明確。規制に対応しやすい。ノイジーネイバーがない。障害範囲が狭い | 費用が高い。テナントが増えると運用が複雑 |
| プール | 全テナントでリソースを共有し、テナント ID で区別 | 費用効率と運用効率が高い | ノイジーネイバー、障害範囲の広さ、テナントごとの費用把握が難しい |
| ブリッジ | 一部を共有、一部を専用 | 要件に合わせて配分できる | 構成が複雑になる |

データストアごとの実装例は次のとおりです。

| データストア | サイロ | プール |
| --- | --- | --- |
| DynamoDB | テナントごとのテーブル | パーティションキーに `TENANT#123` を含める。`dynamodb:LeadingKeys` で強制 |
| RDS、Aurora | テナントごとのインスタンスやデータベース | 全テーブルに `tenant_id` 列を持つ。PostgreSQL の行レベルセキュリティ |
| S3 | テナントごとのバケット | プレフィックスで分離し、IAM の条件で制限 |
| ElastiCache | テナントごとのクラスター | キーの先頭にテナント ID |

分離の強制は、個々の開発者の注意に任せず、共通の仕組みにします。よく使われるのは次の方法です。

1. リクエストの JWT からテナント ID を取得します([Cognito](cognito.md) のカスタム属性など)。
2. テナント ID をセッションタグなどに入れて、STS で権限を絞った一時認証情報を取得します([IAM](iam.md))。
3. その認証情報でデータにアクセスします。IAM の条件で他のテナントのキーへのアクセスを拒否できます。

DynamoDB のプールモデルでは、テナント ID をパーティションキーの先頭に置きます。テナントごとのアクセスが自然に分散しますが、大きなテナントがホットキーになる場合はシャーディングを検討します。

## 既定値と上限のまとめ {#numbers}

| 項目 | 値 |
| --- | --- |
| RDS のリードレプリカ(同一リージョン) | 1 つのインスタンスから最大 15 個 |
| Multi-AZ のフェイルオーバー | 通常 60〜120 秒 |
| IAM 認証トークンの寿命 | 15 分 |
| マスターユーザーのシークレットのローテーション | デフォルト 7 日 |
| `rds.force_ssl` | PostgreSQL 15 以降は 1 がデフォルト |
| Aurora レプリカ | 最大 15 個 |
| Aurora の昇格優先度 | 0〜15 |
| Aurora のカスタムエンドポイント | 1 クラスターに最大 5 個 |
| Serverless v2 の容量 | 1 ACU は約 2 GiB。最小 0、0.5 単位 |
| `SecondsUntilAutoPause` | 300〜86,400 秒 |
| グローバルデータベースのセカンダリ | 最大 10 リージョン |
| RDS Proxy の `ConnectionBorrowTimeout` | デフォルト 120 秒、最大 300 秒 |
| RDS Proxy の `IdleClientTimeout` | デフォルト 1,800 秒 |
| RDS Proxy の `MaxConnectionsPercent` | デフォルト 100(SQL Server は 10) |
| RDS Proxy のピン留め | 16 KB を超えるステートメント |
| ElastiCache のシャード | クラスターモード有効で最大 500 |
| ElastiCache のレプリカ | シャードごとに最大 5 |
| AUTH トークン | 16〜128 文字 |
| `maxmemory-policy` | デフォルト `volatile-lru` |
| `reserved-memory-percent` | デフォルト 25 |

## 試験のポイント {#exam-points}

| こう問われたら | 答え |
| --- | --- |
| RDS の読み取り負荷を減らしたい | リードレプリカ、または ElastiCache |
| RDS の可用性を高めたい | Multi-AZ |
| Multi-AZ のスタンバイで読み取れるか | 読めない(インスタンス配置の場合) |
| レプリカから古い値が返る | 非同期複製のため。最新が必須ならプライマリを読む |
| Aurora で読み取りを分散したい | リーダーエンドポイント |
| Lambda から RDS への接続が枯渇する | RDS Proxy |
| RDS Proxy の効果が出ない | ピン留めを確認。`DatabaseConnectionsCurrentlySessionPinned` |
| 全文検索を追加したい | OpenSearch Service |
| キャッシュに古いデータが残る | TTL、またはライトスルー |
| キャッシュが読まれないデータで埋まる | 遅延読み込みと TTL |
| 新しいノードのキャッシュが空でミスが多い | 遅延読み込みとライトスルーを併用 |
| ランキングを作りたい | ソート済みセット(Valkey / Redis OSS) |
| キャッシュに高可用性が必要 | Valkey / Redis OSS の Multi-AZ と自動フェイルオーバー |
| シンプルでマルチスレッドのキャッシュ | Memcached |
| マルチテナントで強い分離が必要、規制がある | サイロモデル |
| マルチテナントで費用効率を優先 | プールモデルと、テナント ID によるアクセス制御 |
| DB のパスワードをアプリに持たせたくない | IAM データベース認証、または Secrets Manager |
| IAM 認証で必要な権限 | `rds-db:connect` |
| Aurora で用途別にインスタンスを分けたい | カスタムエンドポイント |
| 夜間に Aurora の費用を下げたい | Serverless v2 の最小 0 ACU と自動一時停止 |
| RDS Proxy で接続待ちのタイムアウト | `ConnectionBorrowTimeout`、ピン留め、`MaxConnectionsPercent` |
| キャッシュのデータが 1 ノードに収まらない | クラスターモード有効 |
| AUTH を有効にできない | 転送中の暗号化が必須 |
| AUTH トークンを無停止で変えたい | `ROTATE` の後に `SET` |
| `Evictions` が増える | メモリ不足。スケールするか TTL を見直す |

## 関連ページ {#related}

- [DynamoDB](dynamodb.md)
- [S3](s3.md)
- [ストレージの選び方](storage.md)
- [Lambda](lambda.md)
- [Secrets Manager と Parameter Store](secrets.md)
- [IAM](iam.md)
- [Cognito](cognito.md)
- [監視](observability.md)

## 参考 {#references}

- [Working with DB instance read replicas](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ReadRepl.html)
- [Amazon Aurora endpoint connections](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Overview.Endpoints.html)
- [Replication with Amazon Aurora](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Replication.html)
- [Amazon RDS Proxy](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-proxy.html)
- [Avoiding pinning an RDS Proxy](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-proxy-pinning.html)
- [What is Amazon ElastiCache?](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/WhatIs.html)
- [Comparing node-based Valkey, Memcached, and Redis OSS clusters](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/SelectEngine.html)
- [Caching strategies](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/Strategies.html)
- [Multi-AZ DB instance deployments](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZSingleStandby.html)
- [Multi-AZ DB cluster deployments](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/multi-az-db-clusters-concepts.html)
- [IAM database authentication](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.html)
- [Password management with Secrets Manager](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-secrets-manager.html)
- [ConnectionPoolConfiguration](https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_ConnectionPoolConfiguration.html)
- [Aurora Serverless v2: how it works](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless-v2.how-it-works.html)
- [Scaling to zero ACUs](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless-v2-auto-pause.html)
- [Aurora Global Database](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-global-database.html)
- [Cluster mode disabled vs enabled](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/Replication.Redis-RedisCluster.html)
- [AUTH command](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/auth.html)
- [In-transit encryption](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/in-transit-encryption.html)
- [At-rest encryption](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/at-rest-encryption.html)
- [Engine-specific parameters](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/ParameterGroups.Engine.html)
- [What is Amazon OpenSearch Service?](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html)
- [DAX: How it works](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DAX.concepts.html)
- [SaaS Tenant Isolation Strategies: The isolation mindset](https://docs.aws.amazon.com/whitepapers/latest/saas-tenant-isolation-strategies/the-isolation-mindset.html)
- [SaaS Tenant Isolation Strategies: Silo isolation](https://docs.aws.amazon.com/whitepapers/latest/saas-tenant-isolation-strategies/silo-isolation.html)
- [SaaS Tenant Isolation Strategies: Pool isolation](https://docs.aws.amazon.com/whitepapers/latest/saas-tenant-isolation-strategies/pool-isolation.html)
