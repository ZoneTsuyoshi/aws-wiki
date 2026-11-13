# データベースとキャッシュ

[:material-sprout: CLF](../courses/clf/services.md){ .exam-badge .exam-foundational } [:material-sprout: AIF](../courses/aif/services.md){ .exam-badge .exam-foundational } [:material-certificate: SAA](../courses/saa/services.md){ .exam-badge .exam-associate } [:material-certificate: DVA](../courses/dva/services.md){ .exam-badge .exam-associate } [:material-certificate: SOA](../courses/soa/services.md){ .exam-badge .exam-associate } [:material-certificate: DEA](../courses/dea/services.md){ .exam-badge .exam-associate } [:material-certificate: MLA](../courses/mla/services.md){ .exam-badge .exam-associate } [:material-star-circle: SAP](../courses/sap/services.md){ .exam-badge .exam-professional } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional } [:material-star-circle: AIP](../courses/aip/services.md){ .exam-badge .exam-professional }

RDS、Aurora、ElastiCache の使い方と、アクセスパターンに合わせたデータストアとキャッシュの選び方をまとめます。DynamoDB 自体の詳細は [DynamoDB](dynamodb.md) を参照してください。

[![キャッシュの層とデータストア](../assets/diagrams/databases-cache-layers.png)](../assets/diagrams/databases-cache-layers.png)

## データストアの選び方 {#choosing-data-store}

まずアクセスパターンを確認します。どのキーで読むのか、どの程度の遅延を許すのか、結合やトランザクションが必要か、という点です。

オンプレミスでは、DB サーバーを 1 台建てるのに機器の購入、構築、運用の担当者が要ります。そのため、1 つのリレーショナル DB に何でも入れる構成になりがちでした。AWS では用途ごとのデータストアをすぐに作れるので、データの使われ方に合うものを選び、組み合わせるのが基本です。AWS はこれを「目的別（purpose-built）データベース」と呼んでいます。

| 観点 | 1 つの RDB に集める | 用途ごとに分ける |
| --- | --- | --- |
| 運用 | 管理する DB が 1 つで済む | 種類ごとに知識が要る |
| 性能 | 検索もキャッシュも同じ DB が受け、互いに影響する | それぞれ得意な処理だけを受ける |
| スケール | 全体を一緒に大きくする | 負荷の高い部分だけを大きくする |
| 整合性 | 1 つのトランザクションで守れる | ストアの間は同期の仕組みが要る（Streams など） |

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

**選び方の例**:

- 商品 500 万件を商品 ID で引き、毎秒 2 万件まで増える可能性があるなら DynamoDB です。
- 「注文、顧客、商品を結合して月次の売上を出す」なら RDS か Aurora です。
- 集計済みのランキングを毎秒 5 万回読み、消えても計算し直せるなら ElastiCache です。
- 1 件 2 GB の動画なら S3 です。DynamoDB の項目は 400 KB までなので入りません。

### OpenSearch Service {#opensearch}

OpenSearch クラスターを管理してくれるサービスです。AWS ではクラスターのことをドメインと呼びます。

**提供単位**: ドメインはリージョン単位で、ノードは 2 つか 3 つの AZ に分けられます。VPC の中に置くか、パブリックエンドポイントにするかを選べます。

- **向いている用途**: 全文検索、ログ分析、アプリケーションのリアルタイム監視、クリックストリーム分析。
- **データの投入**: S3、Kinesis、Data Firehose、DynamoDB、CloudWatch Logs などと連携できます。
- **よくある構成**: 主データは DynamoDB に置き、Streams と Lambda で OpenSearch に同期して検索だけを任せます。DynamoDB の `Scan` と `FilterExpression` で検索している構成を見たら、この形を検討します。

OpenSearch を主データストアと考えるのではなく、検索用の副データとして扱うのが基本です。

**計算の例**: 1 KB の商品 100 万件を、DynamoDB の `Scan` と `contains(name, :q)` で検索します。1,000,000 KB ÷ 4 KB × 0.5 で、検索 1 回に 125,000 RCU かかります。OpenSearch へ同期すれば、この読み取りは DynamoDB から消えます。

**誤ると**: Streams からの同期処理が失敗したまま放置すると、検索結果とテーブルの内容がずれます。Streams の保持は 24 時間なので、それを超えると再同期が必要です。

## 使いどころと具体例 {#use-cases}

このページのサービスは、「SQL で結合や集計をしたい」なら RDS と Aurora、「同じものを何度も速く読みたい」なら ElastiCache、と役割が分かれます。実際のシステムでは組み合わせて使います。

**使う場面:**

| 場面 | 具体例 | 使う機能 |
| --- | --- | --- |
| 結合と集計のある業務 | 診療予約で、患者、医師、予約枠、診療科を結合して空き枠を出す | [RDS](#rds) |
| DB が止まると業務が止まる | 予約システムで、AZ の障害でも 2 分ほどで書き込みを再開する | [リードレプリカと Multi-AZ](#read-replicas) |
| 重いレポートを本番から逃がす | 毎朝 7 時の店舗別売上レポートを、注文の処理と別の DB で回す | [リードレプリカと Multi-AZ](#read-replicas) |
| 読み取りが多く、止められない SQL | 会員 300 万人の EC の商品と注文 | [Aurora](#aurora)、[エンドポイントの動作](#aurora-endpoints) |
| 夜と休日はほぼ使わない | 社員 2,000 人の社内申請システム、開発環境 | [Aurora Serverless v2](#aurora-serverless-v2) |
| 海外拠点から読む、リージョンの障害に備える | 東京の在庫 DB を、北米の倉庫からも近くで読む | [Aurora グローバルデータベース](#aurora-global-database) |
| Lambda から RDB を使う | チケットの発売開始に Lambda の同時実行が 1,000 になる | [RDS Proxy](#rds-proxy) |
| DB のパスワードを配らない | 夜間バッチのコンテナが、IAM のロールだけで DB に入る | [IAM データベース認証](#rds-iam-auth)、[Secrets Manager との統合](#rds-secrets-manager) |
| 同じ結果を何度も読む | ニュースサイトのトップページの記事一覧 | [ElastiCache](#elasticache)、[キャッシュ戦略](#caching-strategies) |
| ランキングとセッション | スマホゲームの週間ランキング、複数の EC2 でのログイン状態の共有 | [Redis OSS、Valkey と Memcached](#engines) |
| 全文検索 | 求人サイトで「駅名 + 職種 + こだわり条件」で探す | [OpenSearch Service](#opensearch) |
| 多数の顧客を 1 つの DB に載せる | 500 社が使う会計 SaaS で、テナントの行を確実に分ける | [マルチテナントのデータアクセス](#multi-tenant) |

**使わない方がよい場面:**

| 場面 | 理由 | 代わりの選択肢 |
| --- | --- | --- |
| キーで 1 件を引くだけで、規模が読めない | インスタンスの大きさと接続数の管理が要る | [DynamoDB](dynamodb.md) |
| 失えないデータの正本を ElastiCache に置く | 複製は非同期で、ノードの障害で書き込みを失うことがある | [MemoryDB](databases-specialized.md#memorydb)、RDS |
| OS にエージェントを入れる必要がある | RDS は OS に入れない | [RDS Custom](databases-specialized.md#rds-custom)、EC2 |
| 数億行を毎日集計する BI | 業務の DB に重い集計が載り、注文の処理まで遅くなる | [Redshift](data-engineering.md#redshift) |
| 1 つのライターに収まらない書き込み | RDS と通常の Aurora は書き込みを 1 台で受ける | [DynamoDB](dynamodb.md)、[Aurora Limitless Database](databases-specialized.md#aurora-advanced) |

### 例: クリニックグループの診療予約 {#use-case-clinic}

**状況:** 20 のクリニックを持つ医療法人の予約と問診のシステムです。患者は 30 万人で、朝 8 時 30 分の予約受付の開始に毎秒 200 クエリほどになります。運用の担当は 2 人です。患者情報を扱うので、通信の暗号化とパスワードの管理を監査で問われます。

**構成:**

```mermaid
flowchart TD
    W["予約サイト<br/>（ECS）"] --> P["プライマリ<br/>AZ a"]
    P -- "同期で複製" --> S["スタンバイ<br/>AZ c"]
    W -- "パスワードを取得" --> SM["Secrets Manager"]
    SM -. "7 日ごとに変更" .-> P
```

**設定値:**

| 項目 | 値 | 理由 |
| --- | --- | --- |
| エンジンと配置 | RDS for PostgreSQL、Multi-AZ DB インスタンス | 予約の結合に SQL を使う。AZ の障害で自動で切り替える |
| `rds.force_ssl` | 1 | 暗号化しない接続を DB 側で拒否する |
| クライアントの `sslmode` | `verify-full` | 接続先が本物の DB かも確かめる |
| マスターパスワード | `--manage-master-user-password` | 人がパスワードを知らずに済み、7 日ごとに変わる |
| アプリの DNS キャッシュ | 60 秒以下 | フェイルオーバーの後に新しいプライマリへつなぎ直す |

**なぜこのサービスか:** 読み取りのレプリカを何台も並べる規模ではなく、標準の PostgreSQL で足ります。Aurora は大量のレプリカと速いフェイルオーバーが強みですが、この規模では RDS の Multi-AZ の方が構成が単純です。

**つまずきやすい点:**

- フェイルオーバーの 60〜120 秒は書き込みが失敗します。予約の確定ボタンは再試行しても二重予約にならないよう、予約番号で重複を確かめます。
- Route 53 の別名で接続すると、`verify-full` で証明書のホスト名が一致せず失敗します。
- アプリがパスワードを長くキャッシュすると、7 日ごとのローテーションの後に新しい接続が認証エラーになります。

### 例: 会員 300 万人の EC の注文 DB {#use-case-ec}

**状況:** 会員 300 万人の総合 EC です。商品と注文を Aurora MySQL に置き、読み取りが書き込みの 10 倍あります。セールの日は平常の 5 倍になります。毎朝、マーケティングの担当者が重い集計クエリを流します。

**構成:**

```mermaid
flowchart TD
    APP["EC のアプリ"] -- "書き込み" --> CE["クラスターエンドポイント"]
    APP -- "Web の読み取り" --> WEB["カスタム: web"]
    BI["朝の集計"] --> REP["カスタム: report"]
    CE --> W["ライター"]
    WEB --> R1["レプリカ 1（優先度 0）"]
    WEB --> R2["レプリカ 2（優先度 1）"]
    REP --> R3["集計用レプリカ（優先度 15）"]
```

**設定値:**

| 項目 | 値 | 理由 |
| --- | --- | --- |
| Web 用レプリカ | 2 台、ライターと同じ `db.r6g.xlarge`、優先度 0 と 1 | 昇格しても書き込みの性能が落ちない |
| 集計用レプリカ | `db.r6g.4xlarge`、優先度 15 | 重い集計だけを受け、昇格の候補の最後に回す |
| カスタムエンドポイント | `web`（レプリカ 1、2）、`report`（集計用） | リーダーエンドポイントだと、Web の読み取りが集計用に当たり、集計が Web 用に当たる |
| アプリの接続先 | クラスターと `web` のエンドポイント | インスタンスのエンドポイントを書くと、フェイルオーバーに追従できない |

**なぜこのサービスか:** 読み取りの多い SQL のワークロードで、レプリカを増やしてもデータの複製が要らず、遅延も小さいためです。RDS のリードレプリカも使えますが、レプリカの遅延とフェイルオーバーの速さで Aurora が有利です。

**つまずきやすい点:**

- セールの前にレプリカを 2 台から 4 台に増やしても、接続プールが前の 2 台に接続したままだと負荷が移りません。プールの接続に寿命を設けます。
- `web` の 2 台の性能をそろえないと、小さい方だけが重くなります。
- 集計用の大きなレプリカを優先度 0 にすると、障害時にそれが昇格し、朝の集計がライターに当たります。

### 例: 製造業の社内申請システム {#use-case-internal}

**状況:** 社員 2,000 人の製造業で、出張や購買の申請と承認のシステムを Aurora PostgreSQL で動かします。使うのは平日の 8〜20 時で、夜と休日はほぼ 0 です。月末の締めの 2 日間だけ、平常の 4 倍の負荷になります。情報システム部は 5 人です。

**設定値:**

| 環境 | `MinCapacity` | `MaxCapacity` | `SecondsUntilAutoPause` | 理由 |
| --- | --- | --- | --- | --- |
| 本番 | 1 | 16 | 使わない | 朝の最初の申請を待たせない。月末は 16 ACU（約 32 GiB）まで広がる |
| 開発 | 0 | 4 | 600 | 夜と休日は 10 分で一時停止し、ACU の課金を止める |

開発環境のアプリは、JDBC の `connectTimeout` を 20 秒にします。再開には通常約 15 秒かかるためです。

**なぜこのサービスか:** 固定の大きさのインスタンスでは、夜と休日も月末のピークに合わせた容量を払い続けます。Serverless v2 は 0.5 ACU 単位で増減するので、負荷の差が大きい社内システムでは安くなりやすいです。

**つまずきやすい点:**

- 本番も `MinCapacity=0` にすると、月曜の朝の最初のアクセスが再開を待ってタイムアウトします。
- `MinCapacity` を 0.5 まで下げると、バッファプールが小さくなり、朝の負荷が来た直後に遅くなります。
- 開発の DB に夜間のヘルスチェックや監視ツールの接続が残っていると、一時停止しません。

### 例: チケット販売の発売開始 {#use-case-ticket}

**状況:** コンサートやスポーツのチケットを売るサービスです。人気公演の発売開始の 10 時ちょうどに、API の Lambda の同時実行が 1,000 になります。在庫の確保に行ロックを使うので、データは Aurora MySQL に置きます。DB の `max_connections` は 1,000 です。

**構成:**

```mermaid
flowchart LR
    U["購入画面"] --> G["API Gateway"]
    G --> L["Lambda<br/>同時実行 1,000"]
    L -- "IAM 認証" --> P["RDS Proxy"]
    P -- "最大 800 接続" --> A["Aurora MySQL"]
```

**設定値:**

| 項目 | 値 | 理由 |
| --- | --- | --- |
| `MaxConnectionsPercent` | 80 | 1,000 × 80% で 800 接続まで。残りを管理者と夜間バッチに残す |
| `ConnectionBorrowTimeout` | 5 秒 | Lambda のタイムアウト 10 秒より短くし、待ちすぎずに「混雑中」を返す |
| クライアントの認証 | IAM（`rds-db:connect`） | 関数の環境変数にパスワードを置かない |
| 接続の作り方 | ハンドラの外で接続する | 実行環境の再利用で接続を使い回す |

**なぜこのサービスか:** Lambda の実行環境は互いに接続プールを共有できません。RDS Proxy がトランザクションの間だけ DB の接続を貸すので、同時実行の 1,000 がそのまま 1,000 の接続になりません。

**つまずきやすい点:**

- 接続ごとに `SET` やプリペアドステートメントを使うと、ピン留めで多重化が効かず、`Timed-out waiting to acquire database connection` が出ます。`DatabaseConnectionsCurrentlySessionPinned` を見ます。
- `ConnectionBorrowTimeout` を既定の 120 秒のままにすると、Lambda が先にタイムアウトし、原因が見えません。
- 在庫の行ロックを長く持つと、少ない接続をその間ずっと使います。トランザクションは在庫の確保だけに絞り、決済は外に出します。

### 例: ニュースサイトの記事キャッシュ {#use-case-news}

**状況:** 月間 3 億ページビューのニュースサイトです。記事は Aurora に置き、トップページと記事ページの読み取りは平常で毎秒 5,000 回、大きな速報で毎秒 5 万回になります。記事の修正は数分以内に反映したいものの、数十秒の古さは許されます。

**構成:**

| 層 | 置くもの | 古さの許容 |
| --- | --- | --- |
| CloudFront | 画像、記事ページの HTML | 60 秒 |
| ElastiCache（Valkey） | 記事の本文、トップの一覧 | 60 秒。修正時はライトスルーで上書き |
| Aurora | 記事の正本 | － |

**設定値:**

| 項目 | 値 | 理由 |
| --- | --- | --- |
| 構成 | プライマリ 1 台、レプリカ 2 台、Multi-AZ、クラスターモード無効 | 読み取りをレプリカに分ける。データは 1 ノードに収まる |
| `maxmemory-policy` | `allkeys-lru` | すべてのキーが Aurora から作り直せる |
| TTL | `60 + random.randint(0, 15)` 秒 | 一斉に期限が切れて Aurora に集中するのを避ける |
| 書き込み | 記事の修正時にキャッシュも更新する | TTL を待たずに修正を反映する |

**なぜこのサービスか:** 記事は何度も同じものが読まれ、少し古くても困りません。Aurora のレプリカを増やすより、メモリから返す方が速く、読み取りの多くを DB から外せます。

**つまずきやすい点:**

- 速報の記事は公開直後にキャッシュが空なので、同じ記事のミスが同時に大量に起き、Aurora に集中します。公開の時点でキャッシュに書いておきます。
- キャッシュのノードが全部落ちると、Aurora には平常の 10 倍以上の読み取りが届きます。Aurora の容量はその場合も考えて決めます。
- リーダーエンドポイントはロードバランサーではなく、接続の単位で DNS が振り分けるだけです。接続を長く持つと、レプリカの間で偏ります。

### 例: 求人サイトの検索 {#use-case-jobs}

**状況:** 掲載 50 万件の求人サイトです。求人の正本は DynamoDB に置き、企業の担当者が 1 日 3 万件を更新します。応募者は「駅名 + 職種 + こだわり条件」で検索し、毎秒 300 回の検索があります。

**構成:**

```mermaid
flowchart LR
    E["企業の管理画面"] --> D["DynamoDB<br/>求人の正本"]
    D --> S["Streams"]
    S --> L["Lambda"]
    L --> O["OpenSearch Service<br/>検索用の副データ"]
    U["応募者の検索"] --> O
    U -- "求人の詳細" --> D
```

**設定値:**

| 項目 | 値 | 理由 |
| --- | --- | --- |
| Streams | `NEW_IMAGE` | 更新後の求人をそのまま検索用に書く |
| 削除の扱い | 掲載終了は項目を消さず、状態を変える | 検索の側でも同じ更新として扱える |
| OpenSearch のノード | 3 つの AZ に分ける | 1 つの AZ の障害でも検索を止めない |
| 詳細画面 | DynamoDB を求人 ID で `GetItem` | 検索の結果より新しい正本を見せる |

**なぜこのサービスか:** DynamoDB の `Scan` と `contains` で検索すると、検索のたびに全件を読む費用がかかります。検索は OpenSearch に任せ、正本と詳細の読み取りは DynamoDB に残します。

**つまずきやすい点:**

- 同期の Lambda が失敗したまま 24 時間を過ぎると、その間の更新が検索に反映されず、テーブルから全件を同期し直すことになります。
- 更新から検索に出るまで数秒の遅れがあります。企業の担当者には「反映まで少し時間がかかる」と画面で伝えます。

## RDS {#rds}

[:material-sprout: CLF](../courses/clf/services.md){ .exam-badge .exam-foundational } [:material-sprout: AIF](../courses/aif/services.md){ .exam-badge .exam-foundational } [:material-certificate: SAA](../courses/saa/services.md){ .exam-badge .exam-associate } [:material-certificate: DVA](../courses/dva/services.md){ .exam-badge .exam-associate } [:material-certificate: SOA](../courses/soa/services.md){ .exam-badge .exam-associate } [:material-certificate: DEA](../courses/dea/services.md){ .exam-badge .exam-associate } [:material-certificate: MLA](../courses/mla/services.md){ .exam-badge .exam-associate } [:material-star-circle: SAP](../courses/sap/services.md){ .exam-badge .exam-professional } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional } [:material-star-circle: AIP](../courses/aip/services.md){ .exam-badge .exam-professional }

MySQL、PostgreSQL、MariaDB、Oracle、SQL Server、Db2 を実行するマネージドのリレーショナルデータベースです。

自前で DB サーバーを運用すると、DB の中身とは関係のない作業に多くの時間を取られます。RDS は、その作業を AWS が引き受け、利用者がデータとクエリに集中できるようにするサービスです。

| 作業 | 自前の DB サーバー（オンプレミス、EC2） | RDS |
| --- | --- | --- |
| ハードウェアの調達と故障対応 | 自分 | AWS |
| OS のインストールとパッチ | 自分 | AWS。OS にはログインできない |
| DB エンジンのインストールとパッチ | 自分 | AWS。適用の時期はメンテナンスウィンドウで選ぶ |
| バックアップ | スクリプトとテープなどで自分 | 自動バックアップとスナップショット |
| 冗長構成 | クラスターソフトを自分で組む | Multi-AZ を選ぶ |
| スキーマ、インデックス、クエリの調整 | 自分 | 自分 |
| DB ユーザーと権限 | 自分 | 自分 |

その代わり、OS のファイルや root の権限は使えません。DB エンジンの設定もパラメータグループの範囲で変えます。OS まで触る必要があるなら、EC2 に自分で入れるか、RDS Custom（Oracle、SQL Server）を検討します。

**提供単位**: DB インスタンスは AZ 単位で、DB サブネットグループを通じて VPC の中に置きます。Multi-AZ はスタンバイを別の AZ に置きます([リソースの提供単位](resource-scope.md#scope-zonal))。

**保存時の暗号化**: 未暗号化の DB インスタンスは、ブルー/グリーンデプロイの作成時に `TargetKmsKeyId` を指定して暗号化されたグリーン環境を作り、切り替えることで暗号化できます。

### リードレプリカと Multi-AZ {#read-replicas}

目的が違います。読み取りを増やすならリードレプリカ、可用性を高めるなら Multi-AZ です。

どちらも「もう 1 台の DB にデータを写す」点は同じですが、解決する困りごとが違います。

| 困りごと | 対策しないと起きること | 仕組み |
| --- | --- | --- |
| DB のサーバーや AZ が壊れる | 復旧まで書き込みも読み取りも止まる | Multi-AZ（同期で写し、自動で切り替える） |
| 読み取りのクエリが多すぎる | 書き込みまで遅くなる | リードレプリカ（非同期で写し、読み取りを任せる） |
| リージョンが使えなくなる | リージョンの中の DB がすべて止まる | 別リージョンのリードレプリカを昇格 |

オンプレミスでいえば、Multi-AZ はクラスターソフトで組むアクティブ/スタンバイの冗長構成、リードレプリカは非同期レプリケーションで作る参照用のスレーブに近いものです。違いは、どちらも設定 1 つで作れ、スタンバイは AZ という別のデータセンターに置かれることです。

同期は、スタンバイに書けたことを確かめてから応答するので、切り替えてもデータを失いません。その分だけ書き込みが遅くなります。非同期は待たないので速い代わりに、レプリカは少し遅れます。

[![RDS の Multi-AZ とリードレプリカ](../assets/diagrams/databases-rds-multi-az.png)](../assets/diagrams/databases-rds-multi-az.png)

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

```bash
aws rds create-db-instance-read-replica \
  --db-instance-identifier app-report \
  --source-db-instance-identifier app
aws rds modify-db-instance --db-instance-identifier app --multi-az --apply-immediately
```

設定ごとの値の例です。

- **`ReplicaLag`**: 30 なら、レプリカは約 30 秒前の状態です。注文の直後にレプリカを読むと、その注文がまだ見えません。
- **バックアップの保持**: `--backup-retention-period 0` のインスタンスでは、レプリカの作成に失敗します。1 以上にしてから作ります。
- **JVM の DNS キャッシュ**: `networkaddress.cache.ttl=60` にします。**誤ると**: 無期限にキャッシュすると、フェイルオーバーの後も古い IP に接続して失敗し続けます。
- **フェイルオーバー**: 60〜120 秒の間、書き込みは失敗します。アプリは再接続と再試行を入れます。**誤ると**: 接続プールが壊れた接続を持ち続け、DB は復旧したのにエラーが続きます。
- **Multi-AZ の形態**: DB クラスターならリーダー 2 台を読めるので、1 台のライターと 2 台の読み取りを同じ構成で賄えます。DB インスタンス配置では、スタンバイに接続できません。

### IAM データベース認証 {#rds-iam-auth}

パスワードの代わりに、AWS 署名バージョン 4 で作る認証トークンで接続します。MariaDB、MySQL、PostgreSQL で使えます。

DB のパスワードは、アプリの設定ファイルや環境変数に散らばりがちです。漏れたら全部の置き場所を探して替える必要があり、替えるまでは使われ続けます。IAM 認証では、DB に入れるかどうかを IAM のロールで決めます。パスワードを配らずに済み、権限を外せば次の接続から入れなくなります。トークンは 15 分で切れるので、漏れても被害は短い時間に限られます。

**使う場面:** 物流会社の夜間の配車計算バッチを ECS で動かし、タスクロールに `rds-db:connect` を付けて PostgreSQL に入ります。退職者や不要になったバッチは、ロールの権限を外すだけで入れなくなります。

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

**トークンの寿命の例**: 10 時 00 分に作ったトークンで 10 時 14 分に接続すると成功し、その接続は 10 時 15 分を過ぎても使えます。10 時 16 分に同じトークンで新しい接続を開くと失敗します。接続ごとにトークンを作り直します。

**権限と DB ユーザーの例**:

```json
{
  "Effect": "Allow",
  "Action": "rds-db:connect",
  "Resource": "arn:aws:rds-db:ap-northeast-1:111122223333:dbuser:db-ABCDEFGHIJKL01234/app_user"
}
```

```sql
-- MySQL
CREATE USER app_user IDENTIFIED WITH AWSAuthenticationPlugin AS 'RDS';
-- PostgreSQL
CREATE USER app_user;
GRANT rds_iam TO app_user;
```

**誤ると**: `Action` を `rds:Connect` と書いたり、リソースに DB 識別子の `app` を書いたりすると、接続が拒否されます。必要なのはリソース ID(`db-` で始まる値)です。

### Secrets Manager との統合 {#rds-secrets-manager}

`--manage-master-user-password` を指定すると、RDS がマスターユーザーのパスワードを生成し、Secrets Manager で管理します。

マスターユーザーのパスワードは、作成時に人が決めると、誰かが覚えていたり、手順書に残ったりします。定期的に替えるのも忘れがちです。RDS に生成とローテーションを任せれば、人がパスワードを知る必要がなくなります。

**使う場面:** 委託先の開発会社が交代するとき、旧担当者が知っていたマスターパスワードを無効にする手間をなくします。最初から RDS の管理にしておけば、誰も値を知りません。

| 項目 | 内容 |
| --- | --- |
| ローテーション | デフォルトで 7 日ごと。スケジュールは変更できる |
| 暗号化 | `aws/secretsmanager` かカスタマーマネージドキー(`MasterUserSecretKmsKeyId`)。管理を始めた後はキーを変更できない |
| DB の削除 | シークレットも削除される |
| 取得 | アプリは `GetSecretValue` で読む |

**例**: Lambda の環境変数にパスワードを書く代わりに、シークレットを読むようにします。ローテーションで値が変わるので、長時間キャッシュすると認証エラーになります。ローテーションの詳細は [Secrets Manager と Parameter Store](secrets.md) を参照してください。

```bash
aws rds modify-db-instance --db-instance-identifier app \
  --manage-master-user-password \
  --master-user-secret-kms-key-id alias/rds-secrets \
  --apply-immediately
```

**例**: 既定の 7 日ごとのローテーションで、アプリがパスワードを 30 日キャッシュすると、更新の後に新しい接続が認証エラーになります。認証エラーのときにシークレットを読み直すか、キャッシュを 1 時間程度にします。

### SSL/TLS {#rds-ssl}

VPC の中でも、通信を暗号化しないと、経路上で中身を読まれるおそれがあります。暗号化だけでなく証明書を検証すると、接続先が本物の DB かどうかも確かめられます。サーバー側で強制すれば、クライアントの設定漏れがあっても平文の接続を拒否できます。

**使う場面:** 証券会社の顧客 DB で、監査の「すべての DB 接続を暗号化している」という要件に応えます。アプリごとの設定を確かめる代わりに、パラメータグループで強制します。

| エンジン | 強制する設定 | デフォルト |
| --- | --- | --- |
| PostgreSQL | パラメータ `rds.force_ssl=1` | バージョン 15 以降は 1(有効)。それより前は 0 |
| MySQL | パラメータ `require_secure_transport=ON` | 無効 |

設定はカスタムのパラメータグループで変えます。PostgreSQL で強制を有効にすると、SSL を使わない接続は拒否されます。

クライアントは AWS の CA バンドル(`global-bundle.pem`)でサーバーを検証します。PostgreSQL の `sslmode=verify-full` はサーバー証明書とホスト名の両方を確認します。

```bash
psql "host=mydb.example.ap-northeast-1.rds.amazonaws.com dbname=app user=app_user \
  sslmode=verify-full sslrootcert=global-bundle.pem"
```

**例**: `rds.force_ssl=1` の PostgreSQL に `sslmode=disable` で接続すると拒否されます。`sslmode=require` なら暗号化はされますが、証明書を検証しないので接続先のなりすましは防げません。

**誤ると**: Route 53 の別名で接続して `verify-full` を使うと、証明書のホスト名と一致せず失敗します。

## Aurora {#aurora}

[:material-sprout: CLF](../courses/clf/services.md){ .exam-badge .exam-foundational } [:material-sprout: AIF](../courses/aif/services.md){ .exam-badge .exam-foundational } [:material-certificate: SAA](../courses/saa/services.md){ .exam-badge .exam-associate } [:material-certificate: DVA](../courses/dva/services.md){ .exam-badge .exam-associate } [:material-certificate: SOA](../courses/soa/services.md){ .exam-badge .exam-associate } [:material-certificate: DEA](../courses/dea/services.md){ .exam-badge .exam-associate } [:material-star-circle: SAP](../courses/sap/services.md){ .exam-badge .exam-professional } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional } [:material-star-circle: AIP](../courses/aip/services.md){ .exam-badge .exam-professional }

MySQL、PostgreSQL 互換のマネージドデータベースです。データは DB インスタンスから独立したクラスターボリュームに保存され、ライターとレプリカが共有します。

一般的な DB は、サーバーごとに自分のディスクを持ちます。レプリカを作るには全データを写し、その後も変更を送り続けます。Aurora はストレージを計算（インスタンス）から切り離し、全インスタンスで 1 つのクラスターボリュームを共有します。

| 観点 | 一般的な DB（RDS、自前の DB） | Aurora |
| --- | --- | --- |
| ストレージ | インスタンスごとに持つ | 共有のクラスターボリューム。3 つの AZ に 6 つのコピー |
| レプリカの追加 | データを全部写す | 同じボリュームを読むので、データの複製は要らない |
| フェイルオーバー | スタンバイに切り替える | レプリカがライターに昇格する |
| レプリカの遅延 | 書き込みの量で大きく遅れることがある | 通常 100 ミリ秒を大きく下回る |

オンプレミスでいえば、複数の DB サーバーが 1 台の共有ストレージ（SAN）を使う構成に近いものです。違うのは、そのストレージ自体が 3 つの AZ に分散していることです。AWS によると、6 つのうち 2 つのコピーを失っても書き込みを、3 つを失っても読み取りを続けられるよう設計されています。1 つの AZ が持つのは 2 つなので、AZ の障害でもストレージは止まりません（ライターがその AZ にあれば、レプリカが昇格します）。

```mermaid
flowchart TD
    W["ライター<br/>AZ a"] -- 書き込み --> V["クラスターボリューム<br/>3 AZ に 6 コピー"]
    R1["レプリカ<br/>AZ c"] -- 読み取り --> V
    R2["レプリカ<br/>AZ d"] -- 読み取り --> V
    CE["クラスターエンドポイント"] --> W
    RE["リーダーエンドポイント"] --> R1
    RE --> R2
```

**提供単位**: クラスターはリージョン単位で、ストレージは複数の AZ にまたがります。インスタンスは AZ 単位で、DB サブネットグループを通じて VPC の中に置きます([リソースの提供単位](resource-scope.md#scope-regional-vpc))。

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

**例**: アプリの書き込みは `app.cluster-xxxx.ap-northeast-1.rds.amazonaws.com`、読み取りは `app.cluster-ro-xxxx.ap-northeast-1.rds.amazonaws.com` に接続します。

**誤ると**: レプリカを 2 台から 4 台に増やしても、既存の接続プールは前の 2 台に接続したままです。新しい接続が作られるまで、増やした 2 台に負荷が移りません。

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

**例**: 次の構成でライターが落ちると、`r2` が昇格します。優先度 0 の 2 台のうち、サイズが大きいからです。

| レプリカ | 優先度 | サイズ |
| --- | --- | --- |
| `r1` | 0 | `db.r6g.large` |
| `r2` | 0 | `db.r6g.xlarge` |
| `r3` | 15 | `db.r6g.4xlarge` |

`r3` はレポート用なので、優先度を 15 にして昇格の候補の後ろへ回します。

```bash
aws rds modify-db-instance --db-instance-identifier r3 --promotion-tier 15
```

**誤ると**: ライターより小さい `db.r6g.large` だけを優先度 0 にすると、そのインスタンスが昇格して、書き込みの性能が足りなくなることがあります。レプリカがあれば復旧は通常 60 秒未満ですが、レプリカがないとインスタンスの作り直しになり、より長く止まります。

### Aurora Serverless v2 {#aurora-serverless-v2}

[:material-certificate: SAA](../courses/saa/services.md){ .exam-badge .exam-associate } [:material-certificate: SOA](../courses/soa/services.md){ .exam-badge .exam-associate } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional }

容量を ACU という単位で自動調整します。1 ACU は約 2 GiB のメモリと、対応する CPU とネットワークです。

DB サーバーは、ピークに合わせた大きさで用意すると普段は余り、小さくするとピークで足りません。インスタンスのサイズを変えるには再起動やフェイルオーバーが要ります。Serverless v2 は、負荷に合わせて容量を細かく増減させ、この見積もりの難しさを減らします。その代わり、0 まで下げると再開の待ち時間が生じます。

| 設定 | 値 | 動作 |
| --- | --- | --- |
| `MinCapacity` | 0 以上(0 は自動一時停止対応のバージョンのみ) | アイドル時の費用を決める。インスタンス数 × 最小 ACU が目安 |
| `MaxCapacity` | Aurora MySQL は最大 256、Aurora PostgreSQL は最大 384(エンジンのバージョンで異なる) | ピークの上限 |
| `SecondsUntilAutoPause` | 300〜86,400 秒、デフォルト 300 | 最小 0 のとき、接続がないまま経過すると一時停止する |
| スケーリング単位 | 0.5 ACU | インスタンスの追加なしで増減する |

```bash
aws rds modify-db-cluster --db-cluster-identifier my-cluster \
  --serverless-v2-scaling-configuration \
  MinCapacity=0,MaxCapacity=8,SecondsUntilAutoPause=600
```

**例**: 開発環境は夜間に接続がないので `MinCapacity=0` にします。朝の最初の接続は再開を待つため遅くなります。本番の Web アプリで同じ設定にすると、最初のリクエストがタイムアウトすることがあります。

**計算の例**:

- `MaxCapacity=8` は 8 × 2 GiB で約 16 GiB のメモリが上限です。
- ライターとリーダーの 2 台で `MinCapacity=2` なら、アイドルでも 2 × 2 で 4 ACU 分の課金が続きます。
- `SecondsUntilAutoPause=600` なら、接続がないまま 10 分で一時停止します。

**再開の例**: 再開は通常約 15 秒です。JDBC の `connectTimeout` が 5 秒だと、再開を待てずに接続が失敗します。15 秒より長くします。24 時間を超えて止まっていると、さらに時間がかかることがあります。

**誤ると**: `MinCapacity` を 0.5 のように小さくすると、バッファプールのキャッシュも小さくなり、負荷が来た直後の遅延が増えます。`MaxCapacity` が小さいと、ピークに CPU とメモリが張り付きます。優先度 0 と 1 のリーダーはライターと一緒に一時停止するので、リーダーに接続が残っていると全体が止まりません。

### Aurora グローバルデータベース {#aurora-global-database}

1 つのプライマリリージョンと、最大 10 の読み取り専用セカンダリリージョンで構成します。

リージョンの障害に備えることと、遠くの利用者に近くで読ませることが目的です。書き込みを 1 つのリージョンに集めるので、書き込みの競合を考えずに済みます。その代わり、遠いリージョンからの書き込みは遅くなります。DR 戦略の中での位置づけは [耐障害性と DR](resilience.md#write-patterns) を参照してください。

**提供単位**: 複数のリージョンのクラスターをまとめる機能です。各クラスターは、それぞれのリージョンの VPC の中に置きます。

| 項目 | 内容 |
| --- | --- |
| 書き込み | プライマリのクラスターのみ。グローバルデータベースのライターエンドポイントで接続する |
| セカンダリの読み取り | 最大 16 個の読み取り専用インスタンス |
| 書き込み転送 | 有効にするとセカンダリに来た書き込みをプライマリに転送する |
| 切り替え(計画) | スイッチオーバー。リージョンのローテーションなどに使う |
| 切り替え(障害) | フェイルオーバー。プライマリのリージョン障害時に使う |
| 前提 | マネージドの切り替えには、同じメジャーとマイナーのエンジンバージョンが必要 |

DynamoDB のグローバルテーブルと違い、どのリージョンにも書き込めるわけではありません。

**例**: 東京をプライマリ、バージニアをセカンダリにします。米国のユーザーの読み取りはバージニアの読み取りインスタンスへ、書き込みはグローバルデータベースのライターエンドポイントへ送ります。書き込み転送を有効にすれば、バージニアへ来た `UPDATE` は東京に転送されます。

**例**: 年 2 回のリージョン切り替えの訓練はスイッチオーバーで行い、データを失いません。東京の障害ではフェイルオーバーを使い、未複製の分を失う可能性があります。

**誤ると**: 東京とバージニアのマイナーバージョンが違うと、マネージドの切り替えを実行できません。セカンダリのバージョンを先にそろえます。

## 接続プーリングと RDS Proxy {#connection-pooling}

DB への接続の確立は CPU とメモリを消費します。接続を使い回す仕組みが接続プールです。

タクシー乗り場にたとえると、客が来るたびにタクシーを呼ぶのではなく、何台かを乗り場に待たせておく形です。台数（接続数）には DB の上限があるので、客（リクエスト）が急に増えても、タクシーを無限には増やせません。

オンプレミスでは、アプリサーバーの台数がほぼ固定なので、プールの大きさも固定で決められました。クラウドでは Auto Scaling や Lambda でクライアントの数が急に変わるので、合計の接続数が DB の上限を超えやすくなります。

| 場所 | 実装 | 向く場面 |
| --- | --- | --- |
| アプリ内 | ライブラリのプール | EC2 やコンテナのように長く動くプロセス |
| 外部 | RDS Proxy | Lambda のように同時実行が急に増える構成、多数のアプリからの接続 |

**プールサイズの考え方**: プールの最大接続数 × アプリのインスタンス数が、DB の最大接続数を超えないようにします。Auto Scaling でインスタンスが増えると合計が増える点に注意します。

**計算の例**: `max_connections` が 1,000 の DB に、プール 20 接続のコンテナが 30 台なら、20 × 30 で 600 接続です。Auto Scaling で 60 台になると 1,200 接続になり、DB の上限を超えます。プールを 15 に下げると、15 × 60 で 900 接続に収まります。

**誤ると**: ピーク時にだけ `Too many connections` が出て、新しいコンテナの起動やヘルスチェックに失敗します。

### RDS Proxy {#rds-proxy}

[:material-certificate: SOA](../courses/soa/services.md){ .exam-badge .exam-associate }

アプリと DB の間に入り、接続を共有します。

Lambda の実行環境は互いにプールを共有できないので、アプリ内のプールでは数を抑えられません。共有の乗り場をアプリの外に置くのが RDS Proxy です。

```mermaid
flowchart LR
    L1["Lambda"] --> P["RDS Proxy<br/>接続を共有"]
    L2["Lambda"] --> P
    L3["Lambda<br/>同時実行 1,000"] --> P
    P -- "トランザクションの間だけ<br/>少数の接続を使う" --> DB["RDS<br/>max_connections 500"]
```

**提供単位**: プロキシはリージョン単位で、DB と同じ VPC の中に置きます。既定のエンドポイントは 2 つの AZ に配置されます。

**例**: Lambda の同時実行が 1,000 に増えると、関数ごとに 1 接続で 1,000 接続を開こうとします。`max_connections` が 500 の DB では枯渇します。RDS Proxy を挟めば、クライアントが 1,000 でも、DB 側はトランザクションの間だけ接続を使います。

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

**例**: PostgreSQL のアプリが接続のたびに `SET TIME ZONE 'Asia/Tokyo'` を実行すると、200 のクライアント接続が 200 の DB 接続に固定され、多重化が効きません。この `SET` を `InitQuery` に移します。MySQL の `time_zone` は RDS Proxy が追跡する変数なので固定されず、同じ値の接続だけが再利用されます。20 KB の `INSERT` も 16 KB を超えるのでピン留めになります。文を分割します。

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

```bash
aws rds modify-db-proxy-target-group --target-group-name default \
  --db-proxy-name app-proxy \
  --connection-pool-config \
  MaxConnectionsPercent=40,MaxIdleConnectionsPercent=5,ConnectionBorrowTimeout=5
```

設定ごとの値の例です。

- **`MaxIdleConnectionsPercent`**: 上の設定なら、1,000 × 5% で 50 接続までをアイドルで残します。指定しなければ 40 の半分の 20% で、200 接続です。夜間に DB の接続を減らしたいなら低くします。
- **`ConnectionBorrowTimeout`**: 5 秒なら、空きがなければ 5 秒でエラーを返します。既定の 120 秒のまま Lambda のタイムアウトが 30 秒だと、関数が先にタイムアウトしてエラーの原因が見えません。
- **`IdleClientTimeout`**: 300 なら、5 分使わないクライアント接続を閉じます。アプリのプールが接続を長く持つ設計なら、切られた接続でエラーになるので、プロキシより短い時間でアプリ側が閉じるようにします。
- **`InitQuery`**: `SET time_zone = '+09:00'` です。
- **`SessionPinningFilters`**: `EXCLUDE_VARIABLE_SETS` にすると、`SET` があっても接続を固定しません。**誤ると**: クライアント A の `SET` が同じ DB 接続を使うクライアント B に影響します。
- **`RequireTLS`**: `true` なら、TLS なしのクライアントは接続できません。
- **`DefaultAuthScheme`**: `IAM_AUTH` なら Secrets Manager のシークレットなしで DB まで IAM で認証します。
- **`DebugLogging`**: 問題の調査中だけ `true` にして、終わったら `false` に戻します。

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

[:material-sprout: CLF](../courses/clf/services.md){ .exam-badge .exam-foundational } [:material-sprout: AIF](../courses/aif/services.md){ .exam-badge .exam-foundational } [:material-certificate: SAA](../courses/saa/services.md){ .exam-badge .exam-associate } [:material-certificate: DVA](../courses/dva/services.md){ .exam-badge .exam-associate } [:material-certificate: SOA](../courses/soa/services.md){ .exam-badge .exam-associate } [:material-certificate: MLA](../courses/mla/services.md){ .exam-badge .exam-associate } [:material-star-circle: SAP](../courses/sap/services.md){ .exam-badge .exam-professional } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional } [:material-star-circle: AIP](../courses/aip/services.md){ .exam-badge .exam-professional }

インメモリのキャッシュとデータストアです。運用形態は 2 つあります。

同じデータを何度も DB から読むと、DB の負荷が増え、応答も遅くなります。よく使うものを机の上のメモに書き写しておき、書庫（DB）まで取りに行く回数を減らすのがキャッシュです。メモリはディスクより速いので、DB のクエリより速く返せます。

| 観点 | 同じ点（自前の Redis、Memcached サーバー） | 違う点（ElastiCache ならでは） |
| --- | --- | --- |
| 使い方 | 同じクライアントライブラリ、同じコマンド | エンドポイントは DNS 名。フェイルオーバーで指す先が変わる |
| 冗長化 | レプリカを自分で組み、監視で切り替える | Multi-AZ を有効にすれば自動で昇格する |
| パッチ、障害対応 | 自分 | AWS。適用の時期はメンテナンスウィンドウで選ぶ |
| 容量 | サーバーを買い足す | ノードやシャードを足す。サーバーレスなら自動 |

**提供単位**: ノードベースのノードは AZ 単位で、サブネットグループを通じて VPC の中に置きます。レプリカを別の AZ に置いて冗長化します([リソースの提供単位](resource-scope.md#scope-zonal))。

| 形態 | 特徴 |
| --- | --- |
| サーバーレス | 名前を指定するだけで作成でき、容量は自動で調整 |
| ノードベース | ノードタイプ、数、配置を自分で決める。細かい制御が可能 |

**例**: 負荷の増減が読めない新しいサービスならサーバーレスで始めます。パラメータグループで `maxmemory-policy` を調整したい、ノードタイプを固定して費用を見積もりたいならノードベースです。

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

**例**: ゲームのランキングはソート済みセットで作ります。Memcached にはこの型がありません。

```text
ZADD ranking 1200 user:42
ZADD ranking 980 user:7
ZREVRANGE ranking 0 9 WITHSCORES
```

**誤ると**: セッションを Memcached のノードに置くと、そのノードが落ちたときにセッションが消え、該当するユーザーがログアウトします。

### クラスターモード {#cluster-mode}

1 台のノードのメモリと書き込みの性能には上限があります。レプリカを増やしても、全データをどのノードも持つことに変わりはなく、書き込みは 1 台のプライマリが受けます。クラスターモードは、データを複数のシャードに分けて、メモリと書き込みの両方を横に広げます。その代わり、クライアントはクラスターに対応したものが要ります。

**使う場面:** 利用者 500 万人のソーシャルメディアで、各ユーザーのタイムラインのキャッシュが 300 GiB になり、1 ノードのメモリに収まらなくなったときに有効にします。

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

**計算の例**: データが 300 GiB で、メモリ 100 GiB のノードを `reserved-memory-percent` 25 で使います。1 ノードに置けるのは 100 × 0.75 で 75 GiB です。300 ÷ 75 で 4 シャードが必要です。各シャードにレプリカを 1 台付けると、4 × 2 で 8 ノードです。

**落とし穴**: クラスターモードで使うクライアントは、クラスターに対応したものにします。クラスターモードを無効のまま読み取りをノードのエンドポイントに固定すると、ノードの増減で接続先を直す必要があります。リーダーエンドポイントはロードバランサーではなく、接続単位で DNS が振り分けるだけです。

### レプリケーションと Multi-AZ {#elasticache-replication}

複製は非同期です。プライマリが障害を起こすと、Multi-AZ が有効ならレプリカが自動で昇格し、プライマリエンドポイントの DNS が切り替わります。

| 落とし穴 | 内容 |
| --- | --- |
| レプリカ 0 でノードが故障 | データをすべて失う |
| フェイルオーバー直後 | 非同期複製のため、少量のデータを失うことがある |
| Memcached | レプリケーションがない。ノードが落ちるとそのノードのデータは消える |

Memcached のノードベースのクラスターでは、自動検出対応のクライアントが設定エンドポイントからノード一覧を取得します。

**例**: プライマリ 1 台とレプリカ 2 台を別の AZ に置き、Multi-AZ を有効にします。切り替えは `TestFailover` で試せます。

```bash
aws elasticache create-replication-group --replication-group-id app-cache \
  --replication-group-description "app" --engine valkey \
  --cache-node-type cache.r7g.large --num-cache-clusters 3 \
  --automatic-failover-enabled --multi-az-enabled
aws elasticache test-failover --replication-group-id app-cache --node-group-id 0001
```

**誤ると**: アプリがノードのエンドポイントに接続していると、昇格の後も古いノードへ書こうとして失敗します。プライマリエンドポイントを使います。

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

設定ごとの例です。

- **転送中の暗号化**: `TransitEncryptionEnabled=true` のクラスターに `redis-cli` を `--tls` なしで接続すると、応答が返らず接続が切れます。
- **保存時の暗号化**: 既存のノードベースのクラスターを暗号化するなら、バックアップを取り、`AtRestEncryptionEnabled=true` の新しいクラスターへ復元します。
- **AUTH トークン**: 15 文字は短すぎ、`@` を含むトークンは使えない記号なので、どちらも拒否されます。
- **RBAC**: アプリ用のユーザーに、`app:` で始まるキーの読み書きだけを許可します。

```bash
aws elasticache create-user --user-id app-user --user-name app-user \
  --engine valkey --access-string "on ~app:* +@read +@write" \
  --authentication-mode Type=iam
```

### 追い出しとメモリ {#eviction}

メモリが一杯になったときの動作は `maxmemory-policy` で決まります。デフォルトは `volatile-lru` です。

メモリはディスクより高く、容量も小さいので、いつかは一杯になります。そのとき「何を捨てるか」を決めておくのが追い出しです。机の上のメモが一杯になったら、しばらく見ていないメモから捨てる、というのが LRU の考え方です。

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

**例**:

- **`allkeys-lru`**: 全キーがキャッシュで、DB から作り直せるならこれにします。TTL のないキーも古い順に消えます。
- **`volatile-ttl`**: TTL 30 秒の在庫と TTL 3,600 秒の説明文が混在すると、残り時間の短い在庫から消えます。
- **`noeviction`**: カートのように消せないデータなら、メモリが一杯のときに書き込みを失敗させ、アラームで気づきます。
- **`CacheHitRate`**: 1,000 回の読み取りのうち 950 回がヒットなら 95% です。
- **`reserved-memory-percent`**: メモリ 100 GiB のノードで 25 なら、データに使えるのは 75 GiB です。0 にするとバックアップやフェイルオーバーの時にメモリが足りなくなることがあります。

```bash
aws elasticache modify-cache-parameter-group \
  --cache-parameter-group-name app-valkey \
  --parameter-name-values ParameterName=maxmemory-policy,ParameterValue=allkeys-lru
```

## キャッシュ戦略 {#caching-strategies}

キャッシュは DB の写しなので、DB を更新すると古くなります。「いつキャッシュに入れるか」「いつ消すか」の決め方で、新しさ、速さ、無駄の釣り合いが変わります。どれも一長一短なので、組み合わせて使います。

| 戦略 | 机の上のメモでたとえると |
| --- | --- |
| 遅延読み込み | 聞かれて分からなかったときだけ書庫で調べ、メモに書き写す |
| ライトスルー | 書庫の資料を直すたびに、メモも同時に書き直す |
| TTL | メモに期限を書いておき、期限が過ぎたら捨てて調べ直す |

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

**ヒット率の計算**: キャッシュの往復が 1 ミリ秒、DB が 20 ミリ秒だとします。遅延読み込みのミスは、キャッシュ確認、DB、キャッシュ書き込みで 22 ミリ秒です。ヒット率 90% の平均は、0.9 × 1 + 0.1 × 22 で 3.1 ミリ秒です。

**DB の負荷の計算**: 毎秒 10,000 回の読み取りでヒット率 90% なら、DB へは毎秒 1,000 回です。キャッシュのノードが全滅すると、DB へは 10 倍の毎秒 10,000 回が届きます。DB の容量は、この場合も考えて決めます。

**落とし穴**:

- 遅延読み込みだけだと、DB を更新しても TTL まで古い値を返します。
- ライトスルーだけだと、新しいノードやフェイルオーバーの後に、書かれるまでデータがありません。
- すべてのキーを同じ TTL にすると一斉に切れて、DB に負荷が集中します。`ex=300 + random.randint(0, 60)` のように散らします。

## DAX、ElastiCache、CloudFront の使い分け {#cache-comparison}

キャッシュは、利用者に近いほど多くの往復を省けます。一方で、近いほど中身を細かく制御しにくくなります。そこで、置く場所の違う 3 つを使い分けます。

```mermaid
flowchart LR
    U["利用者"] --> CF["CloudFront<br/>エッジで HTTP の応答"]
    CF --> APP["アプリ"]
    APP --> EC["ElastiCache<br/>アプリが決めた任意のデータ"]
    APP --> DAX["DAX<br/>DynamoDB の項目"]
    EC -. ミス .-> RDS["RDS、Aurora"]
    DAX -. ミス .-> DDB["DynamoDB"]
```

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

**例**: 商品ページの画像は CloudFront で 1 日、価格の API は ElastiCache で 30 秒、DynamoDB の商品項目は DAX で 5 分のように、層ごとに古さの許容を変えて組み合わせます。

**誤ると**: DAX を RDS の前に置こうとしても動きません。CloudFront に認証付きの API をキーの設計なしでキャッシュさせると、別のユーザーの応答を返します。

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

**例**:

- **プロセス内**: 上のコードは 60 秒ごとに読み直します。10 台のコンテナがそれぞれ別の時刻に読むので、設定を変えた後の最大 60 秒は、台によって値が違います。
- **キーの設計**: `price:123` というキーをテナント間で共有すると、テナント A の価格がテナント B に返ります。`tenant:7:price:123` にします。
- **一斉失効**: 10 万キーを同じ `ex=300` で入れると、5 分後に同時に切れます。`300 + random.randint(0, 60)` なら、切れる時刻が 60 秒に分散します。

## マルチテナントのデータアクセス {#multi-tenant}

1 つのアプリで複数の顧客(テナント)を扱う場合の分離方法です。認証と認可だけでは分離になりません。データアクセスの層でもテナントの境界を強制します。

**使う場面:** 500 社が使う会計 SaaS で、通常の会社はプールに、規制の厳しい金融機関の顧客だけはサイロに置くブリッジの構成にします。

住まいにたとえると、サイロは一戸建て、プールはシェアハウス、ブリッジは共用部と専有部のあるマンションです。一戸建ては隣の音（ノイジーネイバー）を気にせず済みますが高く、シェアハウスは安い代わりに部屋の鍵（テナント ID による制限）を確実に掛ける必要があります。

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

**DynamoDB のプールの例**: セッションタグ `tenant` が `123` のロールは、`TENANT#123` のキーだけを読み書きできます。

```json
{
  "ForAllValues:StringEquals": {
    "dynamodb:LeadingKeys": ["TENANT#${aws:PrincipalTag/tenant}"]
  }
}
```

**PostgreSQL の例**: 行レベルセキュリティで、接続ごとに設定したテナントの行だけを見せます。

```sql
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_only ON orders
  USING (tenant_id = current_setting('app.tenant_id')::bigint);
```

**ノイジーネイバーの例**: 1,000 WCU のテーブルで、テナント A が 900 WCU を使うと、他のテナントは 100 WCU を奪い合います。サイロへ移すか、API のレート制限をテナントごとに付けます。

**誤ると**: アプリの `WHERE tenant_id = ?` だけに頼ると、1 つのクエリの書き忘れで全テナントのデータが返ります。

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
