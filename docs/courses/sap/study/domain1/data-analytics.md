# 分野1: データレイクと分析

データレイクの権限と形式、リアルタイムとバッチのエンジン、アカウントをまたぐ共有を判断します。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.5.1](../../domain1.md#skill-1-5-1) | データレイクとレイクハウス |
| [1.5.2](../../domain1.md#skill-1-5-2) | リアルタイムとバッチの分析パイプライン |
| [1.5.7](../../domain1.md#skill-1-5-7) | データカタログとアカウント間のデータ共有 |

## 学習の順番 {#study-order}

1. [Lake Formation](../../../../services/data-engineering.md#lake-formation)と[権限](../../../../services/data-engineering.md#lake-formation-permissions): S3 と IAM より細かく制御できることを確認します。
2. [Apache Iceberg](../../../../services/data-engineering.md#iceberg)と [S3 Tables](../../../../services/data-engineering.md#s3-tables): 行の更新とメンテナンスの任せ方を押さえます。
3. [Spectrum](../../../../services/data-engineering.md#redshift-spectrum): DWH から S3 を参照する方法を確認します。
4. [Kinesis Data Streams と MSK の違い](../../../../services/data-engineering.md#msk-vs-kinesis)、[EMR](../../../../services/data-engineering.md#emr)、[Redshift](../../../../services/data-engineering.md#redshift): 既存のコードと負荷の形で選びます。
5. [クロスアカウント共有](../../../../services/data-engineering.md#lake-formation-cross-account)、[LF タグ](../../../../services/data-engineering.md#lake-formation-lf-tags)、[データの共有](../../../../services/data-engineering.md#choosing-sharing)、[Clean Rooms](../../../../services/data-engineering.md#clean-rooms): 共有の相手と範囲で選びます。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 列や行の単位でデータレイクを制御 | Lake Formation |
| データレイクで行の削除、ACID、タイムトラベル | Apache Iceberg |
| Iceberg のメンテナンスを任せたい | S3 Tables |
| DWH の SQL で S3 の古いデータと結合 | Redshift Spectrum |
| 既存の Kafka のコードをそのまま | MSK |
| クラスターの停止を避けて Spark の費用を下げる | タスクノードをスポットに |
| 月末に集中する DWH | Redshift Serverless |
| 別のアカウントのデータレイクを、コピーなしで | Lake Formation の共有とリソースリンク |
| テーブルが増えても権限の作業を増やさない | LF タグ |
| Redshift のライブデータを別のアカウントへ | Redshift データ共有 |
| 他社と生データを見せずに共同で分析 | Clean Rooms と分析ルール |

## 引っかかりやすい点 {#traps}

- Athena や Spectrum で共有されたテーブルを参照するには、共有先でリソースリンクを作ります。
- Lake Formation の共有は内部で RAM を使います。
- コアノードをスポットにして HDFS を使うと、中断でデータを失います。やり直しを許容でき、費用を最優先する一時的なクラスターに限り、全ノードをスポットにできます。
- Lake Formation の共有では、共有先も共有された列を読めます。生データを見せないなら Clean Rooms です。
- S3 のバージョニングは、行の削除や同時の読み書きの整合性を解決しません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [data-analytics 問1](../../exercises/data-analytics.md#q1) | 1.5.1 | 保険会社の S3 データレイクを、複数のチームが Athena と Redshift Spectru… |
| [data-analytics 問2](../../exercises/data-analytics.md#q2) | 1.5.1 | 小売のデータレイクは、Hive 形式の Parquet を日次で差し替えています。顧客からの削除の依… |
| [data-analytics 問3](../../exercises/data-analytics.md#q3) | 1.5.1 | 分析チームは Iceberg を使い始めましたが、小さなファイルが増えてクエリが遅くなりました。ファ… |
| [data-analytics 問4](../../exercises/data-analytics.md#q4) | 1.5.1 | Redshift の DWH には直近 1 年のデータがあり、古い 8 年分は S3 に Parqu… |
| [data-analytics 問5](../../exercises/data-analytics.md#q5) | 1.5.2 | 広告配信の会社は、自社のデータセンターで Kafka のプロデューサー、コンシューマー、Kafka … |
| [data-analytics 問6](../../exercises/data-analytics.md#q6) | 1.5.2 | ゲーム会社は、EMR の Spark クラスターで、毎日大規模なログの集計をしています。個々のタスク… |
| [data-analytics 問7](../../exercises/data-analytics.md#q7) | 1.5.2 | 新しい BI の基盤は、複雑な結合を含む定型のレポートを SQL で実行します。利用は月末の数日に集… |
| [data-analytics 問8](../../exercises/data-analytics.md#q8) | 1.5.7 | 組織のデータレイクアカウントの Glue Data Catalog のテーブルを、分析アカウントの … |
| [data-analytics 問9](../../exercises/data-analytics.md#q9) | 1.5.7 | データレイクには数千のテーブルがあり、毎週増えています。「機密度」「部門」の分類に応じて、どのチーム… |
| [data-analytics 問10](../../exercises/data-analytics.md#q10) | 1.5.7 | 本社の Redshift の売上テーブルを、別のアカウントの事業部の Redshift Server… |
| [data-analytics 問11](../../exercises/data-analytics.md#q11) | 1.5.7 | 小売業と食品メーカーは、顧客の重なりと広告の効果を共同で分析します。どちらも相手に生データを見せられ… |

<!-- questions:end -->
