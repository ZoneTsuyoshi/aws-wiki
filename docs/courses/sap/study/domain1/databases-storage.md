# 分野1: データベースとストレージ

アクセスパターンと既存のプロトコルから、データベース、ストレージ、キャッシュを選びます。グローバルな構成では、書き込みの場所と整合性が判断の軸です。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.5.3](../../domain1.md#skill-1-5-3) | ワークロードに合うデータベース |
| [1.5.4](../../domain1.md#skill-1-5-4) | データベースのスケーリングと高可用性 |
| [1.5.5](../../domain1.md#skill-1-5-5) | アクセスパターンと性能に応じたストレージ |
| [1.5.6](../../domain1.md#skill-1-5-6) | データのキャッシュ戦略 |

## 学習の順番 {#study-order}

1. [データベースの選び方](../../../../services/databases-specialized.md#choosing)、[全エンジンの比較表](../../../../services/databases-specialized.md#decision-table)、[紛らわしい組み合わせ](../../../../services/databases-specialized.md#confusable): 互換のプロトコルとデータの形で選びます。
2. [リードレプリカと Multi-AZ](../../../../services/databases.md#read-replicas)と [RDS Proxy](../../../../services/databases.md#rds-proxy): 可用性と読み取りの拡張を区別します。
3. [Aurora グローバルデータベース](../../../../services/databases.md#aurora-global-database)と[グローバルテーブル](../../../../services/dynamodb.md#global-tables): 書き込みの場所と整合性を比べます。
4. [EBS、EFS、S3、FSx の比較](../../../../services/storage-advanced.md#storage-comparison)と [FSx の選び方](../../../../services/storage-advanced.md#fsx-selection): プロトコルと用途で選びます。
5. [キャッシュ戦略](../../../../services/databases.md#caching-strategies)、[DAX、ElastiCache、CloudFront の使い分け](../../../../services/databases.md#cache-comparison)、[DAX](../../../../services/dynamodb.md#dax): どの層でキャッシュするかを判断します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| Aurora グローバルデータベース | 1 プライマリ、最大 10 セカンダリ | 書き込みはプライマリのみ |
| MRSC のグローバルテーブル | ちょうど 3 リージョン | 3 レプリカか、2 レプリカと witness。空のテーブルから作る |
| Multi-AZ DB クラスター | ライター 1、読み取り可能なリーダー 2 | 3 つの AZ で半同期 |
| Timestream for LiveAnalytics | 2025 年 6 月 20 日に新規受付を終了 | 新規は Timestream for InfluxDB |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 多段の関係をたどる | Neptune |
| MongoDB のドライバーをそのまま | DocumentDB |
| Redis の構造で耐久性のある主データベース | MemoryDB |
| 書き込みは 1 リージョン、RPO を小さく | Aurora グローバルデータベース |
| 複数のリージョンで書き込み、数秒の不整合を許容 | MREC |
| 複数のリージョンで書き込み、常に最新を読む | MRSC |
| Lambda からの接続の急増 | RDS Proxy |
| HPC の並列処理と S3 の連携 | FSx for Lustre |
| NetApp の機能とマルチプロトコル | FSx for NetApp ONTAP |
| Linux の複数の AZ で共有、容量の管理なし | EFS |
| DynamoDB の読み取りをマイクロ秒に、変更は少なく | DAX |
| 更新の直後から新しい値を返す | 書き込みスルーと TTL |
| 世界の利用者への API の応答をキャッシュ | CloudFront |

## 引っかかりやすい点 {#traps}

- インスタンス形式の RDS Multi-AZ のスタンバイは読み取りに使えません。DB クラスター形式のリーダーは読めます。
- MRSC のモードは作成時に決まります。2 リージョンだけでは作れません。
- DAX は強い整合性の読み取りをキャッシュしません。DynamoDB に素通しします。
- EBS は 1 つの AZ に閉じます。別の AZ ではスナップショットから作ります。Multi-Attach も同じ AZ の中です。
- 遅延読み込みだけでは古い値が残ります。TTL を延ばすと悪化します。
- DynamoDB の GSI は結果整合性のみです。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [databases-storage 問1](../../exercises/databases-storage.md#q1) | 1.5.3 | カード会社は、口座、端末、加盟店のつながりから不正の連鎖を検出します。「3 段階以内につながる不審な… |
| [databases-storage 問2](../../exercises/databases-storage.md#q2) | 1.5.3 | 既存のアプリは、MongoDB のドライバーとクエリで JSON の文書を扱います。AWS へ移すと… |
| [databases-storage 問3](../../exercises/databases-storage.md#q3) | 1.5.3 | ゲームのランキングと在庫のカウンターには Redis のデータ構造を使っています。応答はマイクロ秒の… |
| [databases-storage 問4](../../exercises/databases-storage.md#q4) | 1.5.3 | 工場の新しいシステムは、機器ごとの温度を毎秒記録し、時間窓での集計を行います。チームは Influx… |
| [databases-storage 問5](../../exercises/databases-storage.md#q5) | 1.5.4 | 銀行の勘定系は Aurora MySQL にあります。書き込みは東京だけで構いませんが、大阪からも低… |
| [databases-storage 問6](../../exercises/databases-storage.md#q6) | 1.5.4 | 新しい決済システムは、東京と大阪の DynamoDB に書き込み、どちらのリージョンから読んでも常に… |
| [databases-storage 問7](../../exercises/databases-storage.md#q7) | 1.5.4 | Lambda の関数が RDS for PostgreSQL へ接続します。アクセスの急増時に to… |
| [databases-storage 問8](../../exercises/databases-storage.md#q8) | 1.5.4 | RDS for MySQL の Multi-AZ（1 つのスタンバイ）を運用しています。可用性は高い… |
| [databases-storage 問9](../../exercises/databases-storage.md#q9) | 1.5.5 | ゲノム解析の HPC は、数百の計算ノードから同じファイルを並列に読み、1 ミリ秒未満の遅延で大きな… |
| [databases-storage 問10](../../exercises/databases-storage.md#q10) | 1.5.5 | デザイン会社はオンプレミスの NetApp のストレージを使い、NFS と SMB で同じデータにア… |
| [databases-storage 問11](../../exercises/databases-storage.md#q11) | 1.5.5 | Web サーバー群は Linux で、複数の AZ のインスタンスから同じファイルを読み書きします。… |
| [databases-storage 問12](../../exercises/databases-storage.md#q12) | 1.5.5 | ap-northeast-1a の EC2 で使っている EBS ボリュームを、AZ 障害に備えて … |
| [databases-storage 問13](../../exercises/databases-storage.md#q13) | 1.5.6 | EC サイトの商品ページは DynamoDB を読みます。読み取りの大半は結果整合性で構わず、ピーク… |
| [databases-storage 問14](../../exercises/databases-storage.md#q14) | 1.5.6 | ElastiCache の前で遅延読み込みを使っています。商品の価格を更新しても、古い値がしばらく表… |
| [databases-storage 問15](../../exercises/databases-storage.md#q15) | 1.5.6 | 天気の API は REST API の API Gateway で提供しています。応答は地域ごとに… |

<!-- questions:end -->
