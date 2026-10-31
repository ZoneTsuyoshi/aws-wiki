# 専門データベース（Neptune、DocumentDB、Keyspaces、MemoryDB、Timestream ほか）

[:material-sprout: CLF](../courses/clf/services.md){ .exam-badge .exam-foundational } [:material-sprout: AIF](../courses/aif/services.md){ .exam-badge .exam-foundational } [:material-certificate: SAA](../courses/saa/services.md){ .exam-badge .exam-associate } [:material-certificate: DEA](../courses/dea/services.md){ .exam-badge .exam-associate } [:material-certificate: MLA](../courses/mla/services.md){ .exam-badge .exam-associate } [:material-star-circle: SAP](../courses/sap/services.md){ .exam-badge .exam-professional } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional } [:material-star-circle: AIP](../courses/aip/services.md){ .exam-badge .exam-professional }

グラフ、ドキュメント、ワイドカラム、インメモリ、時系列といった用途別のデータベースと、RDS Custom、Aurora の応用機能をまとめます。最後に、AWS のデータベース全体の選び方を表にします。RDS、Aurora の基本と ElastiCache は [データベースとキャッシュ](databases.md)、DynamoDB は [DynamoDB](dynamodb.md) を参照してください。

[![データモデル別のデータベース](../assets/diagrams/databases-specialized-models.png)](../assets/diagrams/databases-specialized-models.png)

| サービス | モデル | 互換性 | 一言で | 現在の状況 |
| --- | --- | --- | --- | --- |
| [Neptune](#neptune) | グラフ | Gremlin、openCypher、SPARQL | 関係をたどる | 提供中 |
| [DocumentDB](#documentdb) | ドキュメント（JSON） | MongoDB API | 柔軟なスキーマ | 提供中 |
| [Keyspaces](#keyspaces) | ワイドカラム | Apache Cassandra（CQL） | サーバーレスの Cassandra | 提供中 |
| [MemoryDB](#memorydb) | インメモリ | Valkey、Redis OSS | 耐久性のある主データベース | 提供中 |
| [Timestream for InfluxDB](#timestream-influxdb) | 時系列 | InfluxDB | マネージドの InfluxDB | 提供中 |
| [Timestream for LiveAnalytics](#timestream-liveanalytics) | 時系列 | 独自 | サーバーレスの時系列 | **新規受付を終了** |
| [RDS Custom](#rds-custom) | リレーショナル | Oracle、SQL Server | OS に入れる RDS | **Oracle は 2027 年 3 月に終了** |

## Amazon Neptune {#neptune}

[:material-sprout: CLF](../courses/clf/services.md){ .exam-badge .exam-foundational } [:material-sprout: AIF](../courses/aif/services.md){ .exam-badge .exam-foundational } [:material-certificate: SAA](../courses/saa/services.md){ .exam-badge .exam-associate } [:material-certificate: DEA](../courses/dea/services.md){ .exam-badge .exam-associate } [:material-certificate: MLA](../courses/mla/services.md){ .exam-badge .exam-associate } [:material-star-circle: SAP](../courses/sap/services.md){ .exam-badge .exam-professional } [:material-star-circle: AIP](../courses/aip/services.md){ .exam-badge .exam-professional }

高度に接続されたデータのための、フルマネージドのグラフデータベースです。数十億の関係をミリ秒で問い合わせます。SQL の多段の結合を繰り返す問題に向きます。

| グラフモデル | クエリ言語 | 向く場面 |
| --- | --- | --- |
| プロパティグラフ | Gremlin、openCypher | 不正検知、レコメンド、ネットワーク |
| RDF | SPARQL | ナレッジグラフ、Web 標準のデータ統合 |

プロパティグラフのデータには Gremlin と openCypher の両方で問い合わせできます。

**例**: 「口座 A と同じ端末や電話番号でつながる、3 ホップ以内の口座」を探します。リレーショナルでは自己結合が増えて遅くなる問いです。

### 構成とエンドポイント {#neptune-endpoints}

Aurora に似た、インスタンスとストレージを分けた構成です。

| 要素 | 内容 |
| --- | --- |
| プライマリ | 読み書き。クラスターに 1 台 |
| Neptune レプリカ | 読み取り専用。最大 15 台。同じストレージを共有する |
| クラスターボリューム | 3 AZ に複製。最大 128 TiB まで自動拡張 |

| エンドポイント | 接続先 | 用途 |
| --- | --- | --- |
| クラスター | 現在のプライマリ | 書き込みと更新 |
| リーダー | レプリカ | 読み取り |
| インスタンス | 特定のインスタンス | 診断 |
| カスタム | 選んだインスタンスのグループ | 分析とオンラインの分離 |

既定のポートは 8182 です。

**症状**: クライアントが DNS の結果をキャッシュすると、フェイルオーバー後も古いインスタンスへ接続し、リーダーの分散も効きません。接続を切って再接続します。

### 取り込みと変更の取得 {#neptune-data}

| 機能 | 内容 |
| --- | --- |
| バルクローダー | S3 のファイルから一括ロードする。`INSERT` を大量に実行するより速い |
| 形式 | `csv`（Gremlin）、`opencypher`、`ntriples`、`nquads`、RDF/XML、Turtle など |
| Neptune Streams | 変更をログに記録する。既定で 1 週間保持する。OpenSearch などへの同期に使う |

```bash
curl -X POST https://<cluster-endpoint>:8182/loader \
  -H 'Content-Type: application/json' \
  -d '{
    "source": "s3://graph-data/vertices/",
    "format": "csv",
    "iamRoleArn": "arn:aws:iam::111122223333:role/NeptuneLoadRole",
    "region": "ap-northeast-1"
  }'
```

### スケールと保護 {#neptune-scaling}

| 機能 | 内容 |
| --- | --- |
| Neptune Serverless | `db.serverless` と NCU で自動調整する。`MaxCapacity` は最大 128 NCU（256 GB）。コンピュートのみが対象 |
| グローバルデータベース | プライマリと最大 5 のセカンダリリージョン。各リージョン最大 16 読み取りインスタンス。書き込みはプライマリのみ |
| 認証 | VPC 内に配置。IAM データベース認証を有効にすると、SigV4 の署名が必須 |
| 暗号化 | KMS で保存時を暗号化。転送時は TLS |

リージョン障害の復旧は、セカンダリの切り離しと昇格で行います。計画的な移動には、データの損失がないマネージドプランドフェイルオーバーを使います。

### Neptune Analytics {#neptune-analytics}

大きなグラフをメモリに載せて分析するエンジンです。グラフアルゴリズムとベクトル検索を使えます。

| 比較 | Neptune Database | Neptune Analytics |
| --- | --- | --- |
| 用途 | アプリの読み書き | 探索、分析、データサイエンス |
| データの入力 | アプリ、バルクロード | Neptune のグラフ、スナップショット、S3 |
| ベクトル検索 | Analytics を使う | グラフ作成時に 1 つのインデックスを作成 |

## Amazon DocumentDB {#documentdb}

[:material-sprout: CLF](../courses/clf/services.md){ .exam-badge .exam-foundational } [:material-sprout: AIF](../courses/aif/services.md){ .exam-badge .exam-foundational } [:material-certificate: SAA](../courses/saa/services.md){ .exam-badge .exam-associate } [:material-certificate: DEA](../courses/dea/services.md){ .exam-badge .exam-associate } [:material-certificate: MLA](../courses/mla/services.md){ .exam-badge .exam-associate } [:material-star-circle: SAP](../courses/sap/services.md){ .exam-badge .exam-professional } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional } [:material-star-circle: AIP](../courses/aip/services.md){ .exam-badge .exam-professional }

MongoDB 互換の、フルマネージドのドキュメントデータベースです。JSON をそのまま保存し、スキーマが揃わないデータに向きます。

| クラスターの種類 | 特徴 | 向く場面 |
| --- | --- | --- |
| インスタンスベース | プライマリと最大 15 のレプリカ。ストレージを共有 | 標準 |
| サーバーレス | DCU で自動調整。0.5〜256 DCU。1 DCU は約 2 GiB | 変動の大きな負荷、開発 |
| エラスティック | ハッシュでシャード化。最大 32 シャード。毎秒数百万の読み書き | 非常に大きな規模 |

| 項目 | 内容 | 誤ったときの症状 |
| --- | --- | --- |
| ストレージ | 10 GB 単位で自動拡張。エンジン 8.0 以降は最大 256 TiB、以前は 128 TiB | 通常は設定不要 |
| TLS | 新規クラスターで既定で有効 | CA 証明書のないクライアントは接続できない |
| ネットワーク | VPC のみ | VPC の外から直接接続できない |
| リトライ可能な書き込み | エンジン 8.0.2 以降で対応 | 古いエンジンで有効のドライバーはエラー。`retryWrites=false` にする |
| 変更ストリーム | 既定 3 時間保持。1 時間〜7 日 | 消費が遅れると変更を失う |
| ポイントインタイムリカバリ | 保持期間の任意の秒へ。直近 5 分は対象外 | 復元は新しいクラスターになる |
| シャードキー（エラスティック） | ハッシュ分割に使う。値の種類が多い列を選ぶ | 偏ると性能が出ない |

```text
mongodb://user:password@my-cluster.cluster-xxxx.ap-northeast-1.docdb.amazonaws.com:27017/
  ?tls=true&tlsCAFile=global-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false
```

エラスティッククラスターは MongoDB 5.0 互換のプロトコルで動き、エンジン 8.0 には対応しません。

グローバルクラスターは 1 つのプライマリと最大 10 のセカンダリリージョンで構成します。書き込みはプライマリのみです。

**ベクトル検索**: HNSW と IVFFlat のインデックスに対応します。インデックスがなければ完全な最近傍検索になります。詳しくは [ベクトルインデックス](#vector-indexes) を見てください。

**DynamoDB との違い**: 入れ子の条件での柔軟な検索や集計を使うなら DocumentDB です。キーでの一定の遅延と運用の少なさを優先するなら DynamoDB です。既存の MongoDB からの移行は DocumentDB を選びます。

## Amazon Keyspaces {#keyspaces}

[:material-certificate: SAA](../courses/saa/services.md){ .exam-badge .exam-associate } [:material-certificate: DEA](../courses/dea/services.md){ .exam-badge .exam-associate } [:material-star-circle: SAP](../courses/sap/services.md){ .exam-badge .exam-professional }

Apache Cassandra 互換のサーバーレスなデータベースです。既存の CQL、ドライバーのコードをそのまま使えます。

| 項目 | 内容 |
| --- | --- |
| API | CQL 3.11（2.x と後方互換） |
| 接続 | ポート 9142、TLS 必須 |
| 複製 | 3 AZ に 3 重に書き込む |
| 容量モード | オンデマンドまたはプロビジョンド |
| 認証 | SigV4 またはサービス固有の認証情報 |

### 整合性と料金の単位 {#keyspaces-capacity}

書き込みは常に `LOCAL_QUORUM` です。

| 読み取りの整合性 | 4 KB あたりの消費 | 動作 |
| --- | --- | --- |
| `LOCAL_QUORUM` | 1 RRU または 1 RCU | 直前の成功した書き込みを反映する |
| `LOCAL_ONE`、`ONE` | 0.5 RRU または 0.5 RCU | 古い値を返すことがある |

`QUORUM`、`ALL`、`EACH_QUORUM`、`ANY`、`SERIAL` などは使えず、例外になります。

書き込みは 1 KB あたり 1 WRU または 1 WCU です。オンデマンドモードは、過去に到達したトラフィックまではすぐに対応します。

**症状**: 既存の Cassandra アプリが `QUORUM` を指定したままだと、例外で失敗します。`LOCAL_QUORUM` に変えます。

### Keyspaces の機能と上限 {#keyspaces-features}

| 機能 | 内容 |
| --- | --- |
| マルチリージョン複製 | アクティブアクティブ。通常 1 秒未満で複製 |
| PITR | 最大 35 日。無効にして再度有効にすると、履歴は消える |
| TTL | テーブル、行、列で指定する。期限切れのデータはクエリに出ず、通常 10 日以内に削除される |
| 軽量トランザクション | `INSERT`、`UPDATE`、`DELETE` の条件付き実行。追加料金なし |
| バッチ | ログ付き 100 コマンド、ログなし 30 コマンド |
| 行サイズ | 最大 1 MB |
| パーティションキー | 最大 2,048 バイト |
| クラスタリングキー | 最大 850 バイト |
| 接続あたりのクエリ | 最大 3,000/秒。推奨は 500/秒で、接続を増やす |

**例**: IoT の機器ごとの時系列を、機器 ID をパーティションキー、時刻をクラスタリングキーにして保存します。

**DynamoDB との違い**: 既存の Cassandra の資産を使うなら Keyspaces です。新規で AWS に寄せるなら DynamoDB が統合の面で有利です。

## Amazon MemoryDB {#memorydb}

[:material-certificate: DEA](../courses/dea/services.md){ .exam-badge .exam-associate } [:material-star-circle: SAP](../courses/sap/services.md){ .exam-badge .exam-professional } [:material-star-circle: DOP](../courses/dop/services.md){ .exam-badge .exam-professional }

耐久性のあるインメモリデータベースです。Valkey と Redis OSS に互換です。キャッシュではなく**主データベース**として使えます。

読み取りはマイクロ秒、書き込みは 1 桁ミリ秒です。書き込みは Multi-AZ のトランザクションログに永続化してから応答します。

| 項目 | 内容 |
| --- | --- |
| シャード | 1 つのプライマリと最大 5 つのレプリカ |
| プライマリの読み取り | 強い整合性。フェイルオーバー後も保たれる |
| レプリカの読み取り | 結果整合性。`READONLY` コマンドで読む |
| データ階層化 | `r6gd` でメモリと SSD を使い分ける。キーはメモリに残り、あまり使わない値を LRU で SSD へ移す |
| スナップショット | 保存して復元に使う |
| マルチリージョン | アクティブアクティブ。通常 1 秒未満で複製する。競合は CRDT と Last Writer Wins で解決する |
| ベクトル検索 | Flat と HNSW |

### ElastiCache との違い {#memorydb-vs-elasticache}

| 観点 | [ElastiCache](databases.md#elasticache) | MemoryDB |
| --- | --- | --- |
| 主な位置づけ | データベースの前のキャッシュ | 主データベース |
| 耐久性 | ノードの障害でデータを失うことがある | Multi-AZ トランザクションログ |
| 書き込みの遅延 | マイクロ秒 | 1 桁ミリ秒（ログへの永続化を待つ） |
| 向く場面 | 再生成できるデータ | キャッシュと DB を一本化したいマイクロサービス |

**例**: セッション、ランキング、在庫カウンターの正本を Redis のデータ構造で持ちたい場合に、MemoryDB を選びます。RDS の前に置く読み取りキャッシュなら ElastiCache です。

## Amazon Timestream {#timestream}

[:material-star-circle: SAP](../courses/sap/services.md){ .exam-badge .exam-professional }

時系列データ用のサービスで、2 つの異なるエンジンがあります。**試験の古い資料は LiveAnalytics を前提にしていることがあるので注意します。**

### Timestream for LiveAnalytics {#timestream-liveanalytics}

!!! warning "新規受付を終了"
    **2025 年 6 月 20 日に新規顧客の受付を終了しました。** 既存の顧客は使い続けられます。新規の時系列ワークロードは Timestream for InfluxDB を検討します。

サーバーレスで、メモリストアに直近のデータを、マグネティックストアに履歴を置きます。SQL で問い合わせ、ストア間の移動はポリシーで自動的に行われます。

### Timestream for InfluxDB {#timestream-influxdb}

マネージドの InfluxDB です。既存の InfluxDB のコード、ツールをそのまま使えます。

| 項目 | 内容 |
| --- | --- |
| 構成 | DB インスタンス単位。`db.influx` クラス |
| 高可用性 | Multi-AZ（別 AZ のスタンバイへフェイルオーバー） |
| ストレージ | Influx IOPS Included、最大 16 TiB |
| アクセス | Influx API と UI。ホストへの直接アクセスは不可 |
| ポート | 既定 8086 |
| 収集 | Telegraf など |

**選び方**:

| 要件 | 選択 |
| --- | --- |
| IoT、メトリクスを時間で集計する | Timestream for InfluxDB |
| 単純なキーと時刻で引くだけ | [DynamoDB](dynamodb.md) でも可能 |
| AWS リソースの運用メトリクス | [CloudWatch](observability.md) |
| 大量の履歴を SQL で分析する | S3 と [Athena](streaming.md#athena)、または Redshift |

## Amazon RDS Custom {#rds-custom}

[:material-star-circle: SAP](../courses/sap/services.md){ .exam-badge .exam-professional }

OS とデータベースに管理者権限でアクセスできる RDS です。パッケージアプリの要件で、独自のパッチや設定が必要なときに使います。対応エンジンは Oracle と SQL Server だけです。

!!! danger "RDS Custom for Oracle はサポート終了"
    **2027 年 3 月 31 日で RDS Custom for Oracle のサポートが終了します。** 以後は利用できません。AWS は 2026 年 3 月 31 日から 2027 年 3 月 31 日の間に、EC2 上の Oracle へ移行するよう案内しています。新規の設計では選びません。RDS Custom for SQL Server は、この通知の対象ではありません。

| 責任 | EC2 | RDS | RDS Custom for Oracle | RDS Custom for SQL Server |
| --- | --- | --- | --- | --- |
| スケーリング | 顧客 | AWS | 共有 | 共有 |
| 高可用性 | 顧客 | AWS | AWS | AWS |
| バックアップ | 顧客 | AWS | 共有 | AWS |
| DB パッチ | 顧客 | AWS | 共有 | AWS（CEV は顧客） |
| OS パッチ | 顧客 | AWS | 顧客 | AWS（CEV は顧客） |
| サーバーの保守 | AWS | AWS | AWS | AWS |

| 概念 | 内容 |
| --- | --- |
| カスタムエンジンバージョン（CEV） | DB バージョンと AMI のボリュームスナップショット |
| サポート境界 | サポートされない構成を検知する監視 |
| 自動化 | 既定はフル自動化。作業中は自動化を止められる |
| ホストの置き換え | 障害時に再起動または置き換え。公開 IP が変わる |

**制限**（RDS Custom for Oracle）: インスタンスの停止はできません。EC2 ホストを手動で停止、終了するとサポート境界の外になります。EBS は最大 64 TiB です。

**選び方**: OS への権限が不要なら RDS、自由に管理したいなら EC2、中間の RDS Custom は SQL Server など要件が明確な場合に限ります。

## Aurora の応用 {#aurora-advanced}

基本は [Aurora](databases.md#aurora)、[Serverless v2](databases.md#aurora-serverless-v2)、[グローバルデータベース](databases.md#aurora-global-database) を参照してください。ここでは、そこで扱っていない機能を比べます。

| 機能 | 内容 | 向く場面 | 注意 |
| --- | --- | --- | --- |
| クローン | コピーオンライトで高速に複製する | 本番データでのテスト | 15 個まで。以降はフルコピー。別リージョンには作れない |
| バックトラック | クラスターを過去の時点へ巻き戻す（MySQL のみ） | `WHERE` のない `DELETE` の取り消し | 作成時に有効化する。バックアップの代わりではない |
| パラレルクエリ | 一部の処理をストレージ層へ押し下げる（MySQL） | 重い分析クエリ | PostgreSQL の同名の機能とは別物 |
| Limitless Database | ルーターとシャードで書き込みを水平に分散する（PostgreSQL） | 毎秒数百万の書き込み | I/O-Optimized のみ。専用エンジンのバージョン |
| ゼロ ETL 統合 | Redshift や SageMaker のレイクハウスへほぼリアルタイムで複製する | パイプラインなしの分析 | 対応エンジンを確認する |
| pgvector | PostgreSQL のベクトル検索 | RAG、類似検索 | [ベクトルインデックス](#vector-indexes) |

### グローバルデータベースの切り替え {#aurora-global-switchover}

| 操作 | 用途 | RPO |
| --- | --- | --- |
| スイッチオーバー（旧称 managed planned failover） | リージョンのローテーションなど計画的な移動 | データ損失なし |
| フェイルオーバー | リージョン障害からの復旧 | 通常は秒単位で 0 ではない |

Aurora PostgreSQL は `rds.global_db_rpo` で RPO の上限を設定、追跡できます。

### Aurora DSQL {#aurora-dsql}

サーバーレスで分散型の、PostgreSQL 互換のリレーショナルデータベースです。アクティブアクティブ構成で、インフラの管理やフェイルオーバーの処理が不要です。

| 比較 | Aurora グローバルデータベース | Aurora DSQL |
| --- | --- | --- |
| 書き込み | プライマリリージョンのみ | マルチリージョンのクラスターでアクティブアクティブ |
| 管理 | インスタンスまたは ACU | サーバーレス |
| 互換性 | MySQL、PostgreSQL | PostgreSQL 互換（一部の機能に制限） |

## ベクトルインデックス {#vector-indexes}

ベクトルをそのまま全件比較すると正確ですが遅くなります。インデックスは、少しの精度と引き換えに速くします。

| 方式 | 仕組み | 速度 | 精度 | メモリ | 構築 |
| --- | --- | --- | --- | --- | --- |
| Flat（総当たり） | 全件と比較する | 遅い | 完全 | 少ない | 不要 |
| HNSW | 階層化したグラフをたどる | 速い | 高い | 多い | 遅い |
| IVF（IVFFlat） | クラスターに分け、近いものだけ探す | 中間 | パラメータ次第 | 少なめ | 速い。データ投入後に作る |

| サービス | 対応する方式 |
| --- | --- |
| Aurora PostgreSQL、RDS for PostgreSQL | pgvector の HNSW、IVFFlat |
| DocumentDB | HNSW、IVFFlat |
| MemoryDB | Flat、HNSW |
| Neptune Analytics | グラフごとに 1 つのベクトルインデックス |
| [OpenSearch Service](streaming.md#opensearch) | k-NN |

```sql
-- Aurora PostgreSQL。pgvector 0.5.0 以降で HNSW を使える
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE docs (id bigserial PRIMARY KEY, embedding vector(1024));

CREATE INDEX ON docs USING hnsw (embedding vector_cosine_ops)
  WITH (m = 16, ef_construction = 64);

SET hnsw.ef_search = 100;
SELECT id FROM docs ORDER BY embedding <=> $1 LIMIT 5;
```

| パラメータ | 効果 |
| --- | --- |
| `m`、`ef_construction`（HNSW） | 上げると精度が上がる。構築が遅くなる |
| `ef_search`（HNSW） | 上げると検索の精度が上がる。遅くなる |
| `lists`（IVFFlat） | クラスターの数 |
| `probes`（IVFFlat） | 検索で調べるクラスターの数。上げると精度が上がる |

**症状**: HNSW は削除や上書きが多いと、メモリの増加や精度の低下が起きることがあります。Aurora PostgreSQL は [Amazon Bedrock のナレッジベース](genai-apps.md)の保存先にも使えます。

## データベースの選び方 {#choosing}

### まず何を保存するか {#choosing-flow}

```mermaid
flowchart TD
    A["データベースを選ぶ"] --> B{"分析か、アプリの処理か"}
    B -- "分析" --> C{"データは S3 にある?"}
    C -- "はい、単発" --> ATH["Athena"]
    C -- "定常的な BI" --> RS["Redshift"]
    B -- "アプリの処理" --> D{"関係をたどるのが主?"}
    D -- "はい" --> NEP["Neptune"]
    D -- "いいえ" --> E{"結合とトランザクション?"}
    E -- "はい" --> REL["RDS / Aurora"]
    E -- "いいえ" --> F{"マイクロ秒が必要?"}
    F -- "はい" --> MEM["MemoryDB / ElastiCache"]
    F -- "いいえ" --> G{"既存の資産は?"}
    G -- "MongoDB" --> DOC["DocumentDB"]
    G -- "Cassandra" --> KS["Keyspaces"]
    G -- "なし" --> DDB["DynamoDB"]
```

### 全エンジンの比較表 {#decision-table}

| サービス | モデル | 代表的な用途 | スケール | サーバーレス | マルチリージョン | 選ぶ決め手 |
| --- | --- | --- | --- | --- | --- | --- |
| [RDS](databases.md#rds) | リレーショナル | 一般の業務アプリ | 垂直、リードレプリカ | なし | リードレプリカ | 標準エンジンをそのまま使う |
| [Aurora](databases.md#aurora) | リレーショナル | 高可用な OLTP | 最大 15 レプリカ、共有ストレージ | Serverless v2 | グローバルデータベース | MySQL、PostgreSQL の性能と高可用 |
| [Aurora DSQL](#aurora-dsql) | リレーショナル | 分散の OLTP | 自動 | はい | アクティブアクティブ | 複数リージョンで書き込みたい SQL |
| [RDS Custom](#rds-custom) | リレーショナル | OS 権限が必要なパッケージ | 垂直 | なし | － | OS と DB の管理権限が必須 |
| [DynamoDB](dynamodb.md) | キーバリュー、ドキュメント | 規模が読めないアプリ | 自動で水平 | はい | グローバルテーブル | キーで引く、規模で遅延を一定に |
| [DocumentDB](#documentdb) | ドキュメント | MongoDB の移行、カタログ | レプリカ、エラスティック | サーバーレス | グローバルクラスター | MongoDB API と柔軟な検索 |
| [Keyspaces](#keyspaces) | ワイドカラム | Cassandra の移行、IoT | 自動で水平 | はい | アクティブアクティブ | CQL の資産 |
| [ElastiCache](databases.md#elasticache) | インメモリ | キャッシュ、セッション | シャード、レプリカ | サーバーレス | Global Datastore | 再生成できる高速データ |
| [MemoryDB](#memorydb) | インメモリ | 高速な主データベース | シャード、レプリカ | なし | アクティブアクティブ | Redis 互換で耐久性が必須 |
| [Neptune](#neptune) | グラフ | 不正検知、ナレッジグラフ | 最大 15 レプリカ | Neptune Serverless | グローバルデータベース | 多段の関係をたどる |
| [Timestream for InfluxDB](#timestream-influxdb) | 時系列 | IoT、メトリクス | インスタンス | なし | － | InfluxDB の資産、時系列の集計 |
| [Redshift](data-engineering.md#redshift) | 列指向 DWH | BI、大規模集計 | ノード、RPU | Redshift Serverless | データ共有 | 複雑な SQL の分析 |
| [Athena](streaming.md#athena) | S3 への SQL | ログ分析、探索 | サーバーレス | はい | 該当なし | 単発のクエリ、S3 のまま |
| [OpenSearch Service](streaming.md#opensearch) | 検索エンジン | 全文検索、ログ | ノード | Serverless | クロスクラスター | 全文検索とあいまい検索 |

### 紛らわしい組み合わせ {#confusable}

| 迷うところ | 判断 |
| --- | --- |
| DynamoDB と DocumentDB | キーで引く、運用を最小に → DynamoDB。入れ子の検索、MongoDB API → DocumentDB |
| DynamoDB と Keyspaces | 新規 → DynamoDB。Cassandra の移行 → Keyspaces |
| ElastiCache と MemoryDB | キャッシュ → ElastiCache。正本 → MemoryDB |
| DAX と MemoryDB | DynamoDB の読み取りを速く → DAX。独立した DB → MemoryDB |
| RDS と Aurora | 標準エンジンと低コスト → RDS。可用性とレプリカ数 → Aurora |
| RDS と RDS Custom と EC2 | 権限不要 → RDS。一部の権限 → RDS Custom。完全な管理 → EC2 |
| Aurora グローバルと DSQL | プライマリ書き込みで十分 → Aurora グローバル。多リージョン書き込み → DSQL |
| Redshift と Athena | 定常の BI → Redshift。単発 → Athena |
| Redshift と Aurora | 分析 → Redshift。トランザクション → Aurora |
| Neptune とリレーショナル | 関係の深さが可変 → Neptune。固定の結合 → リレーショナル |
| Timestream と CloudWatch | 自分のアプリの時系列 → Timestream。AWS の運用メトリクス → CloudWatch |

## 既定値と上限のまとめ {#numbers}

| 項目 | 値 |
| --- | --- |
| Neptune のレプリカ | 最大 15 |
| Neptune のクラスターボリューム | 最大 128 TiB |
| Neptune Serverless | 最大 128 NCU（256 GB） |
| Neptune のグローバルデータベース | 最大 5 セカンダリ、各 16 リーダー |
| Neptune Streams | 既定 1 週間 |
| Neptune のポート | 8182 |
| DocumentDB のレプリカ | 最大 15 |
| DocumentDB のストレージ | 最大 256 TiB（8.0 以降）、128 TiB（以前） |
| DocumentDB Serverless | 0.5〜256 DCU |
| DocumentDB のエラスティッククラスター | 最大 32 シャード |
| DocumentDB のグローバルクラスター | 最大 10 セカンダリ |
| DocumentDB の変更ストリーム | 既定 3 時間、1 時間〜7 日 |
| Keyspaces のポート | 9142（TLS） |
| Keyspaces の行サイズ | 最大 1 MB |
| Keyspaces の PITR | 最大 35 日 |
| Keyspaces のバッチ | ログ付き 100、ログなし 30 |
| MemoryDB のレプリカ | シャードあたり最大 5 |
| Timestream for InfluxDB のストレージ | 最大 16 TiB |
| Timestream for InfluxDB のポート | 8086 |
| RDS Custom for Oracle の EBS | 最大 64 TiB |
| Aurora のクローン | コピーオンライトは 15 個まで |
| pgvector の HNSW | 0.5.0 以降 |

## 試験のポイント {#exam-points}

| こう問われたら | 答え |
| --- | --- |
| 不正の検出で、つながりを数ホップたどる | Neptune |
| ソーシャルグラフ、レコメンド | Neptune |
| RDF と SPARQL | Neptune |
| Gremlin や openCypher | Neptune |
| グラフのデータをメモリで分析したい | Neptune Analytics |
| MongoDB からマネージドへ移行 | DocumentDB |
| JSON で柔軟なスキーマ、入れ子の検索 | DocumentDB |
| DocumentDB で書き込みがエラーになる | `retryWrites=false`、またはエンジン 8.0.2 以降 |
| Cassandra のアプリをサーバーレスへ移す | Keyspaces |
| Keyspaces で `QUORUM` が失敗する | `LOCAL_QUORUM` を使う |
| Redis 互換で耐久性のある主データベース | MemoryDB |
| マイクロ秒の読み取りとデータ永続性の両立 | MemoryDB |
| 再生成できるデータのキャッシュ | ElastiCache |
| ベクトル検索を低遅延で | MemoryDB、または Aurora PostgreSQL の pgvector |
| 精度が高く高速なベクトルインデックス | HNSW |
| 構築が速く、メモリの少ないベクトルインデックス | IVF（IVFFlat） |
| IoT の時系列データ（新規） | Timestream for InfluxDB |
| Timestream for LiveAnalytics の新規利用 | 不可。2025 年 6 月 20 日に受付を終了 |
| OS に入って DB の設定を変えたい | RDS Custom（Oracle は 2027 年 3 月に終了） |
| 本番のデータで安く素早くテスト環境を作る | Aurora のクローン |
| 誤った `DELETE` をすぐに戻す（MySQL） | Aurora のバックトラック |
| リージョン障害に備えた低 RPO の読み取り | Aurora グローバルデータベース |
| リージョンの計画的な切り替えでデータ損失なし | Aurora グローバルのスイッチオーバー |
| 多リージョンで書き込むサーバーレスの SQL | Aurora DSQL |
| 1 つの Aurora で書き込みを水平に拡張 | Aurora PostgreSQL Limitless Database |
| Aurora のデータを Redshift で分析、ETL なし | ゼロ ETL 統合 |

## 関連ページ {#related}

- [データベースとキャッシュ](databases.md): RDS、Aurora、ElastiCache の基本
- [DynamoDB](dynamodb.md): キー設計、容量
- [データエンジニアリング](data-engineering.md): Redshift、Glue、EMR
- [ストリーミングと分析](streaming.md): Athena、OpenSearch
- [移行](migration.md): DMS、SCT
- [生成 AI アプリ](genai-apps.md): ナレッジベース、RAG
- [オブザーバビリティ](observability.md): CloudWatch

## 参考 {#references}

- [What is Amazon Neptune?](https://docs.aws.amazon.com/neptune/latest/userguide/intro.html)
- [Connecting to Neptune endpoints](https://docs.aws.amazon.com/neptune/latest/userguide/feature-overview-endpoints.html)
- [Neptune storage, reliability and availability](https://docs.aws.amazon.com/neptune/latest/userguide/feature-overview-storage.html)
- [Neptune Serverless](https://docs.aws.amazon.com/neptune/latest/userguide/neptune-serverless.html)
- [Capacity scaling in Neptune Serverless](https://docs.aws.amazon.com/neptune/latest/userguide/neptune-serverless-capacity-scaling.html)
- [Neptune global database](https://docs.aws.amazon.com/neptune/latest/userguide/neptune-global-database.html)
- [Neptune bulk loader](https://docs.aws.amazon.com/neptune/latest/userguide/bulk-load.html)
- [Neptune load data formats](https://docs.aws.amazon.com/neptune/latest/userguide/bulk-load-tutorial-format.html)
- [Neptune Streams](https://docs.aws.amazon.com/neptune/latest/userguide/streams.html)
- [Neptune IAM authentication](https://docs.aws.amazon.com/neptune/latest/userguide/iam-auth.html)
- [What is Neptune Analytics?](https://docs.aws.amazon.com/neptune-analytics/latest/userguide/what-is-neptune-analytics.html)
- [Vector indexing in Neptune Analytics](https://docs.aws.amazon.com/neptune-analytics/latest/userguide/vector-index.html)
- [What is Amazon DocumentDB?](https://docs.aws.amazon.com/documentdb/latest/developerguide/what-is.html)
- [DocumentDB elastic clusters](https://docs.aws.amazon.com/documentdb/latest/developerguide/docdb-using-elastic-clusters.html)
- [Elastic clusters: how it works](https://docs.aws.amazon.com/documentdb/latest/developerguide/elastic-how-it-works.html)
- [DocumentDB serverless](https://docs.aws.amazon.com/documentdb/latest/developerguide/docdb-serverless.html)
- [DocumentDB global clusters](https://docs.aws.amazon.com/documentdb/latest/developerguide/global-clusters.html)
- [DocumentDB functional differences](https://docs.aws.amazon.com/documentdb/latest/developerguide/functional-differences.html)
- [DocumentDB change streams](https://docs.aws.amazon.com/documentdb/latest/developerguide/change_streams.html)
- [DocumentDB vector search](https://docs.aws.amazon.com/documentdb/latest/developerguide/vector-search.html)
- [Encrypting DocumentDB data in transit](https://docs.aws.amazon.com/documentdb/latest/developerguide/security.encryption.ssl.html)
- [What is Amazon Keyspaces?](https://docs.aws.amazon.com/keyspaces/latest/devguide/what-is-keyspaces.html)
- [How Keyspaces compares to Apache Cassandra](https://docs.aws.amazon.com/keyspaces/latest/devguide/keyspaces-vs-cassandra.html)
- [Keyspaces consistency levels](https://docs.aws.amazon.com/keyspaces/latest/devguide/consistency.html)
- [Keyspaces on-demand capacity mode](https://docs.aws.amazon.com/keyspaces/latest/devguide/ReadWriteCapacityMode.OnDemand.html)
- [Keyspaces quotas](https://docs.aws.amazon.com/keyspaces/latest/devguide/quotas.html)
- [Keyspaces functional differences](https://docs.aws.amazon.com/keyspaces/latest/devguide/functional-differences.html)
- [Keyspaces multi-Region replication](https://docs.aws.amazon.com/keyspaces/latest/devguide/multiRegion-replication.html)
- [Keyspaces point-in-time recovery](https://docs.aws.amazon.com/keyspaces/latest/devguide/PointInTimeRecovery_HowItWorks.html)
- [Keyspaces TTL](https://docs.aws.amazon.com/keyspaces/latest/devguide/TTL.html)
- [What is MemoryDB](https://docs.aws.amazon.com/memorydb/latest/devguide/what-is-memorydb.html)
- [MemoryDB core components](https://docs.aws.amazon.com/memorydb/latest/devguide/components.html)
- [MemoryDB consistency](https://docs.aws.amazon.com/memorydb/latest/devguide/consistency.html)
- [MemoryDB data tiering](https://docs.aws.amazon.com/memorydb/latest/devguide/data-tiering.html)
- [MemoryDB Multi-Region](https://docs.aws.amazon.com/memorydb/latest/devguide/multi-region.html)
- [MemoryDB vector search overview](https://docs.aws.amazon.com/memorydb/latest/devguide/vector-search-overview.html)
- [Timestream for LiveAnalytics availability change](https://docs.aws.amazon.com/timestream/latest/developerguide/AmazonTimestreamForLiveAnalytics-availability-change.html)
- [What is Timestream for LiveAnalytics?](https://docs.aws.amazon.com/timestream/latest/developerguide/what-is-timestream.html)
- [What is Timestream for InfluxDB?](https://docs.aws.amazon.com/timestream/latest/developerguide/timestream-for-influxdb.html)
- [Amazon RDS Custom](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-custom.html)
- [RDS Custom architecture](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/custom-concept.html)
- [RDS Custom for Oracle requirements and limitations](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/custom-reqs-limits.html)
- [RDS Custom for Oracle end of support](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/RDS-Custom-for-Oracle-end-of-support.html)
- [Using Amazon Aurora Global Database](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-global-database.html)
- [Aurora Global Database switchover and failover](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-global-database-disaster-recovery.html)
- [Aurora cloning](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Managing.Clone.html)
- [Backtracking an Aurora DB cluster](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraMySQL.Managing.Backtrack.html)
- [Parallel query for Aurora MySQL](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-mysql-parallel-query.html)
- [Aurora PostgreSQL Limitless Database](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/limitless.html)
- [Limitless Database requirements](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/limitless-reqs-limits.html)
- [Aurora zero-ETL integrations](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/zero-etl.html)
- [Aurora PostgreSQL as a Knowledge Base for Amazon Bedrock](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.VectorDB.html)
- [What is Amazon Aurora DSQL?](https://docs.aws.amazon.com/aurora-dsql/latest/userguide/what-is-aurora-dsql.html)
