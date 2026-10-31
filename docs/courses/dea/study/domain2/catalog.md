# 分野2: データカタログとスキーマ

Data Catalog の使い方、クローラーの設定、パーティションの同期、接続、スキーマの変化への対応を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.2.1](../../domain2.md#skill-2-2-1) | カタログを使ったソースのデータの利用 |
| [2.2.2](../../domain2.md#skill-2-2-2) | 技術カタログの構築と参照 |
| [2.2.3](../../domain2.md#skill-2-2-3) | スキーマの検出とクローラー |
| [2.2.4](../../domain2.md#skill-2-2-4) | パーティションの同期 |
| [2.2.5](../../domain2.md#skill-2-2-5) | カタログ用の接続の作成 |
| [2.4.2](../../domain2.md#skill-2-4-2) | データの特性の変化への対応 |

## 学習の順番 {#study-order}

1. [Data Catalog](../../../../services/data-engineering.md#glue-data-catalog): メタデータだけを持つことを理解します。
2. [クローラー](../../../../services/data-engineering.md#glue-crawlers): 設定と症状を対応づけます。
3. [パーティションの同期](../../../../services/data-engineering.md#partition-sync): 方法ごとの向く場面を覚えます。
4. [Athena のパーティション](../../../../services/streaming.md#athena-partitions): 射影の動作を確認します。
5. [Schema Registry](../../../../services/data-engineering.md#glue-schema-registry): 互換性モードを確認します。
6. [Iceberg](../../../../services/data-engineering.md#iceberg): スキーマとパーティションの進化を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 手で直した定義を守る | `UpdateBehavior: LOG` |
| 新しいフォルダだけ読む | `CRAWL_NEW_FOLDERS_ONLY` |
| フォルダごとにテーブルが大量にできる | `CombineCompatibleSchemas` |
| Hive 形式で少量のパーティション | `MSCK REPAIR TABLE` |
| Hive 形式以外 | `ALTER TABLE ADD PARTITION` |
| 非常に多いパーティション | パーティション射影 |
| ストリームの互換性を強制する | Schema Registry の `BACKWARD` |

## 引っかかりやすい点 {#traps}

- テーブルを削除しても S3 のファイルは消えません。
- パーティション射影を有効にすると、登録済みのパーティションは無視されます。
- クローラーはストリーミングのソースに使えません。
- 必須列の追加は `BACKWARD` で拒否されます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [catalog 問1](../../exercises/catalog.md#q1) | 2.2.1 | Glue Data Catalog の sales.orders を削除しました。S3 の Parq… |
| [catalog 問2](../../exercises/catalog.md#q2) | 2.2.1 | Glue Data Catalog の定義を Redshift から使います。コピーせずに参照する文… |
| [catalog 問3](../../exercises/catalog.md#q3) | 2.2.1 | 別のアカウントの Athena から、共有されたカタログのテーブルを自分のカタログのように参照します… |
| [catalog 問4](../../exercises/catalog.md#q4) | 2.2.2 | 新規のデータレイクで Athena、EMR、Spectrum のメタデータを共有します。サーバーの運… |
| [catalog 問5](../../exercises/catalog.md#q5) | 2.2.2 | 技術カタログとビジネスカタログの説明で正しいものはどれですか。 |
| [catalog 問6](../../exercises/catalog.md#q6) | 2.2.2 | 既存の Hadoop 環境で Apache Hive メタストアを運用しています。EMR を増やすに… |
| [catalog 問7](../../exercises/catalog.md#q7) | 2.2.3 | 日付のフォルダが毎日増えます。新しいフォルダだけ読み、既存のテーブルは変更しません。どの設定ですか。 |
| [catalog 問8](../../exercises/catalog.md#q8) | 2.2.3 | データエンジニアがカタログの列の型を手で直しましたが、クローラーの実行で元に戻ります。手の修正を残す… |
| [catalog 問9](../../exercises/catalog.md#q9) | 2.2.3 | 1 つのプレフィックスの下のフォルダごとに、別々のテーブルが大量に作られました。スキーマは互換性があ… |
| [catalog 問10](../../exercises/catalog.md#q10) | 2.2.3 | クローラーの説明で正しいものはどれですか。（2つ選択） |
| [catalog 問11](../../exercises/catalog.md#q11) | 2.2.4 | Athena で、新しい dt= のフォルダのデータが結果に出ません。Hive 形式で、件数は少なく… |
| [catalog 問12](../../exercises/catalog.md#q12) | 2.2.4 | パスが s3://lake/2026/10/31/ で、Hive 形式（key=value）ではあり… |
| [catalog 問13](../../exercises/catalog.md#q13) | 2.2.4 | 数年分の時間単位のパーティションがあり、Athena の計画に時間がかかります。値の形は規則的で、追… |
| [catalog 問14](../../exercises/catalog.md#q14) | 2.2.4 | Glue ジョブの書き込みの最後に、新しいパーティションを確実にカタログへ反映します。クローラーは使… |
| [catalog 問15](../../exercises/catalog.md#q15) | 2.2.5 | 同じ RDS を読むクローラーと 3 つのジョブがあります。接続情報を 1 か所で管理します。何を使… |
| [catalog 問16](../../exercises/catalog.md#q16) | 2.2.5 | Glue がネイティブに対応していないデータストアへ接続します。どの方法ですか。 |
| [catalog 問17](../../exercises/catalog.md#q17) | 2.2.5 | Glue のカタログ用の接続を初めて作り、クローラーで使います。正しい手順の順序はどれですか。 |
| [catalog 問18](../../exercises/catalog.md#q18) | 2.4.2 | Kafka のストリームで、プロデューサーが互換性のないスキーマの変更を出さないようにします。何を使… |
| [catalog 問19](../../exercises/catalog.md#q19) | 2.4.2 | BACKWARD の Avro スキーマの変更で、登録が拒否されるものはどれですか。 |
| [catalog 問20](../../exercises/catalog.md#q20) | 2.4.2 | S3 のテーブルに列を足し、パーティションを月から日へ変えます。既存のファイルは書き直しません。何を… |

<!-- questions:end -->
