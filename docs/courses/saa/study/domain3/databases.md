# 分野3: データベースの性能

データベースの種類、容量、レプリカ、キャッシュを要件から選びます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [データベースの種類とアクセスパターン](../../domain3.md#t3-3-types) | データアクセスパターン、データベースの種類とサービス、適切なデータベースの種類の判断 |
| [キャパシティの計画](../../domain3.md#t3-3-capacity) | データベースの容量計画 |
| [レプリケーションとグローバルな配置](../../domain3.md#t3-3-replicas) | グローバルインフラストラクチャ、データベースのレプリケーション、業務要件を満たすリードレプリカの設定 |
| [エンジンの選択](../../domain3.md#t3-3-engine) | データベースエンジンの適切な用途、適切なデータベースエンジンの判断 |
| [キャッシュの統合](../../domain3.md#t3-3-caching) | キャッシュの戦略とサービス、業務要件に合うキャッシュの統合 |
| [接続とプロキシ](../../domain3.md#t3-3-proxy) | データベースの接続とプロキシ |
| [データベースアーキテクチャの設計](../../domain3.md#t3-3-design) | データベースアーキテクチャの設計 |

## 学習の順番 {#study-order}

1. [データストアの選び方](../../../../services/databases.md#choosing-data-store)と[全エンジンの比較表](../../../../services/databases-specialized.md#decision-table): アクセスパターンと種類の対応を確認します。
2. [計算方法](../../../../services/dynamodb.md#capacity-calculation)と[キャパシティモードと RCU/WCU](../../../../services/dynamodb.md#capacity): RCU と WCU の計算とモードを押さえます。
3. [リードレプリカと Multi-AZ](../../../../services/databases.md#read-replicas)と[エンドポイントの動作](../../../../services/databases.md#aurora-endpoints): レプリカの作成の条件とエンドポイントの使い分けを確認します。
4. [Aurora グローバルデータベース](../../../../services/databases.md#aurora-global-database)と[グローバルテーブル](../../../../services/dynamodb.md#global-tables): リージョンをまたぐ読み取りと書き込みを比べます。
5. [Redis OSS、Valkey と Memcached](../../../../services/databases.md#engines)と[DAX](../../../../services/dynamodb.md#dax): キャッシュのエンジンと DAX を確認します。
6. [スレッドとコネクションプール](../../../../services/lambda.md#connection-pooling)と[接続プーリングと RDS Proxy](../../../../services/databases.md#connection-pooling): 接続を減らす順序を確認します。
7. [昇格の優先度](../../../../services/databases.md#aurora-failover-priority)と[LSI と GSI](../../../../services/dynamodb.md#indexes): 設計の部品を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| 1 RCU | 4 KB の強い整合性の読み取り 1 回/秒 | 結果整合性は 2 回 |
| 1 WCU | 1 KB の書き込み 1 回/秒 | 切り上げで計算する |
| Aurora のレプリカ | 最大 15 | 読み取りが多い SQL |
| RDS のレプリカ | 同一リージョンに最大 15 個 | 保持期間 0 では作れない |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 結合と高可用性、読み取りが多い | Aurora |
| キーで引く、規模で遅延を一定に | DynamoDB |
| 多段の関係をたどる | Neptune |
| MongoDB、Cassandra の移行 | DocumentDB、Keyspaces |
| 他のリージョンの利用者に低遅延で読ませる | Aurora Global Database |
| 複数のリージョンで書き込む | DynamoDB グローバルテーブル |
| 用途でレプリカを分ける | カスタムエンドポイント |
| ランキング、Pub/Sub | Valkey か Redis OSS |

## 引っかかりやすい点 {#traps}

- リードレプリカでは書き込みは増えません。
- リーダーエンドポイントは接続の単位で分散します。
- LSI はテーブルの作成時にしか追加できません。あとから足すなら GSI です。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [databases 問7](../../exercises/databases.md#q7) | データベースの種類 | 結合と複雑なトランザクションが必要で、読み取りが多く、高可用性も必要です。どれを選びますか。 |
| [databases 問8](../../exercises/databases.md#q8) | データベースの種類 | 不正検知で、口座と端末の関係を数段たどるクエリを低遅延で行います。どれを選びますか。 |
| [databases 問9](../../exercises/databases.md#q9) | データベースの種類 | 移行の要件に合う組み合わせはどれですか。MongoDB のアプリと Cassandra のアプリをそ… |
| [databases 問10](../../exercises/databases.md#q10) | データベースの種類 | 書き込みが中心で増え続けるキーと値のアプリです。読み取りのリードレプリカを増やしても書き込みの性能が… |
| [databases 問11](../../exercises/databases.md#q11) | キャパシティの計画 | 6 KB の項目を強い整合性で毎秒 100 回読みます。必要な RCU はいくつですか。 |
| [databases 問12](../../exercises/databases.md#q12) | キャパシティの計画 | 新規サービスで負荷が予測できず、DynamoDB の容量の管理もしたくありません。どのモードですか。 |
| [databases 問13](../../exercises/databases.md#q13) | キャパシティの計画 | I/O の多い RDS の DB で、ストレージの性能が足りません。安定した高い IOPS を確保し… |
| [databases 問14](../../exercises/databases.md#q14) | レプリケーション | 東京の Aurora のデータを、欧州の利用者が低遅延で読みます。書き込みは東京だけです。どれを選び… |
| [databases 問15](../../exercises/databases.md#q15) | レプリケーション | RDS でリードレプリカを作ろうとしましたが、作れません。自動バックアップの保持期間は 0 です。ど… |
| [databases 問16](../../exercises/databases.md#q16) | レプリケーション | Aurora のレポート用に大きいレプリカ、Web 用に小さいレプリカを使います。接続先を用途で分け… |
| [databases 問17](../../exercises/databases.md#q17) | レプリケーション | 複数のリージョンでキーと値を読み書きします。どのリージョンにも書けることが要件です。どれを選びますか… |
| [databases 問18](../../exercises/databases.md#q18) | エンジンの選択 | Oracle の機能に強く依存しており、当面は変更できません。OS は管理しません。どのエンジンです… |
| [databases 問19](../../exercises/databases.md#q19) | エンジンの選択 | ベクトル検索や地理空間の拡張機能を使い、高度な SQL も必要です。どのエンジンが最も合いますか。 |
| [databases 問20](../../exercises/databases.md#q20) | エンジンの選択 | 既存の MySQL の Web アプリを、変更を最小にしてストレージの自動拡張と多数のレプリカを使え… |
| [databases 問21](../../exercises/databases.md#q21) | キャッシュの統合 | 同じ商品情報を繰り返し読む RDS の負荷を下げ、ミリ秒未満で返します。どれを選びますか。 |
| [databases 問22](../../exercises/databases.md#q22) | キャッシュの統合 | ランキング、Pub/Sub、レプリケーションと自動フェイルオーバーが必要なキャッシュです。どのエンジ… |
| [databases 問23](../../exercises/databases.md#q23) | キャッシュの統合 | DynamoDB の読み取りをマイクロ秒にします。コードの変更は最小にします。どれを選びますか。 |
| [databases 問24](../../exercises/databases.md#q24) | 接続とプロキシ | Lambda で接続を毎回作り直しています。接続の処理を減らすコードの変更はどれですか。 |
| [databases 問25](../../exercises/databases.md#q25) | 接続とプロキシ | Aurora の読み取りを複数のレプリカに分散します。アプリは 1 つの接続先だけを設定します。どれ… |
| [databases 問26](../../exercises/databases.md#q26) | 接続とプロキシ | 接続の問題への対策として正しい組み合わせはどれですか。 |
| [databases 問27](../../exercises/databases.md#q27) | DB アーキテクチャ | Aurora のアーキテクチャで、接続の急増、読み取りの性能、リージョンの障害に備えます。それぞれの… |
| [databases 問28](../../exercises/databases.md#q28) | DB アーキテクチャ | Aurora の DB クラスターで、フェイルオーバー先のレプリカを、大きいインスタンスに優先させま… |
| [databases 問29](../../exercises/databases.md#q29) | DB アーキテクチャ | DynamoDB のテーブルでユーザー ID をパーティションキーにしています。メールアドレスでも検… |

<!-- questions:end -->
