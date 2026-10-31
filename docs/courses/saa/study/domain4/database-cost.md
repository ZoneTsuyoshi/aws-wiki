# 分野4: データベースの費用

サービス、容量、キャッシュ、保持の順に費用を考えます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [費用対効果の高いデータベースサービス](../../domain4.md#t4-3-services) | データベースの種類とサービス、費用対効果の高いデータベースサービスの判断 |
| [データベースの形式](../../domain4.md#t4-3-types) | 費用対効果の高いデータベースの種類の判断 |
| [容量の計画](../../domain4.md#t4-3-capacity) | データベースの容量計画 |
| [キャッシュとレプリケーション](../../domain4.md#t4-3-caching-replica) | キャッシュの戦略、データベースのレプリケーション |
| [接続とプロキシ](../../domain4.md#t4-3-proxy) | データベースの接続とプロキシ |
| [エンジンの選択と費用](../../domain4.md#t4-3-engine) | データベースエンジンの適切な用途、適切なデータベースエンジンの判断 |
| [バックアップと保持のポリシー](../../domain4.md#t4-3-backup) | データの保持ポリシー、適切なバックアップと保持のポリシーの設計 |

## 学習の順番 {#study-order}

1. [キャパシティモードと RCU/WCU](../../../../services/dynamodb.md#capacity)と[テーブルクラス](../../../../services/dynamodb.md#table-classes): モードとテーブルクラスを確認します。
2. [Aurora Serverless v2](../../../../services/databases.md#aurora-serverless-v2)と[Savings Plans](../../../../services/cost-management.md#savings-plans): 変動する SQL と割引を確認します。
3. [Amazon Redshift](../../../../services/data-engineering.md#redshift)と[Amazon Timestream](../../../../services/databases-specialized.md#timestream): 列形式と時系列の使いどころを押さえます。
4. [読み取りの整合性](../../../../services/dynamodb.md#read-consistency)と[LSI と GSI](../../../../services/dynamodb.md#indexes): 容量を減らす方法を確認します。
5. [DAX、ElastiCache、CloudFront の使い分け](../../../../services/databases.md#cache-comparison)と[DAX](../../../../services/dynamodb.md#dax): 読み取りを減らす方法を比べます。
6. [RDS Proxy](../../../../services/databases.md#rds-proxy)と[スレッドとコネクションプール](../../../../services/lambda.md#connection-pooling): 接続の費用の考え方を確認します。
7. [移行の 7 つの R](../../../../services/migration.md#seven-rs)と[バックアップと復元](../../../../services/dynamodb.md#backup): 移行の考え方と保持の費用を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| Aurora I/O-Optimized | I/O が総額の 25% 以上 | I/O の料金がかからない |
| RDS のバックアップストレージ | プロビジョニング済み容量の 100% まで無料 | 超えた分が課金 |
| RDS の自動バックアップ | 0〜35 日 | 7 年には足りない |
| DynamoDB の PITR | 1〜35 日 | 期間で費用は変わらない |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 夜間にほぼアクセスのない SQL | Aurora Serverless v2（最小 0 ACU） |
| 古いデータの多い DynamoDB | `STANDARD_INFREQUENT_ACCESS` |
| 大規模な列の集計 | Redshift |
| 新規の時系列 | Timestream for InfluxDB |
| 接続数のためだけに大きなインスタンス | RDS Proxy |
| Oracle のライセンスをなくす | Aurora PostgreSQL へ移す |

## 引っかかりやすい点 {#traps}

- GSI は書き込みのたびに WCU を消費します。
- 手動スナップショットは DB を消しても残り、課金も続きます。
- リードレプリカにはレプリカ分の料金がかかります。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [database-cost 問1](../../exercises/database-cost.md#q1) | データベースサービス | 負荷の変動が大きい SQL のアプリで、夜間はほとんどアクセスがありません。MySQL 互換を維持し… |
| [database-cost 問2](../../exercises/database-cost.md#q2) | データベースサービス | 古いデータが多く、アクセスが少ない DynamoDB のテーブルで、費用の大部分がストレージです。ど… |
| [database-cost 問3](../../exercises/database-cost.md#q3) | データベースサービス | Aurora の I/O の費用が総額の 25% 以上を占めています。費用を抑える設定はどれですか。 |
| [database-cost 問4](../../exercises/database-cost.md#q4) | データベースの形式 | RDS の分析の集計が本番を遅くし、大きなインスタンスの費用がかかっています。大規模な列の集計を B… |
| [database-cost 問5](../../exercises/database-cost.md#q5) | データベースの形式 | IoT の測定値を時系列で保存します。新規の設計です。どれを検討しますか。 |
| [database-cost 問6](../../exercises/database-cost.md#q6) | データベースの形式 | S3 上のログに単発の SQL を実行します。費用を最小にする形式はどれですか。 |
| [database-cost 問7](../../exercises/database-cost.md#q7) | 容量の計画 | DynamoDB のプロビジョンドのテーブルで、8 KB の項目を毎秒 400 回、強い整合性で読ん… |
| [database-cost 問8](../../exercises/database-cost.md#q8) | 容量の計画 | 1 KB の項目を毎秒 100 回書くテーブルに、すべての属性を投影した GSI が 5 個あります… |
| [database-cost 問9](../../exercises/database-cost.md#q9) | 容量の計画 | 1 KB の項目を毎秒 50 回書きます。各項目は GSI 1 つにも投影されます。プロビジョンドの… |
| [database-cost 問10](../../exercises/database-cost.md#q10) | キャッシュとレプリカ | RDS を大きくする前に、同じデータの繰り返しの読み取りを減らします。費用の面で最も適切な順序はどれ… |
| [database-cost 問11](../../exercises/database-cost.md#q11) | キャッシュとレプリカ | リードレプリカの費用について正しいものはどれですか。 |
| [database-cost 問12](../../exercises/database-cost.md#q12) | キャッシュとレプリカ | 読み取りが多い DynamoDB の RCU を減らします。どれが適切ですか。 |
| [database-cost 問13](../../exercises/database-cost.md#q13) | 接続とプロキシ | 接続数のためだけに大きな RDS インスタンスを使っています。CPU とメモリは余っています。費用を… |
| [database-cost 問14](../../exercises/database-cost.md#q14) | 接続とプロキシ | アプリは数台の EC2 で動き、接続プールを持ち、接続数は上限の 1 割です。フェイルオーバーの要件… |
| [database-cost 問15](../../exercises/database-cost.md#q15) | 接続とプロキシ | Lambda が接続を毎回作っており、接続の処理で実行時間が延び、費用も増えています。最初に行う変更… |
| [database-cost 問16](../../exercises/database-cost.md#q16) | エンジンと費用 | Oracle のライセンス費用をなくします。異種間の変換の費用は受け入れます。どれを選びますか。 |
| [database-cost 問17](../../exercises/database-cost.md#q17) | エンジンと費用 | MySQL と PostgreSQL の選択について、費用の点で正しいものはどれですか。 |
| [database-cost 問18](../../exercises/database-cost.md#q18) | エンジンと費用 | MySQL から Aurora MySQL への移行の作業の費用が小さい理由はどれですか。 |
| [database-cost 問19](../../exercises/database-cost.md#q19) | 保持のポリシー | RDS のストレージを 500 GB プロビジョニングしています。同じリージョンの DB はこれだけ… |
| [database-cost 問20](../../exercises/database-cost.md#q20) | 保持のポリシー | 規制で DB のバックアップを 7 年保管します。RDS で適切な設計を選んでください。（2つ選択） |
| [database-cost 問21](../../exercises/database-cost.md#q21) | 保持のポリシー | DynamoDB の PITR の期間を 35 日から 7 日に短くしました。費用はどうなりますか。 |

<!-- questions:end -->
