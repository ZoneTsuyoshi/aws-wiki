# 分野1: 変換と処理

要件に合う変換サービス、データ形式、費用の削減、失敗の調査を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.2.3](../../domain1.md#skill-1-2-3) | 複数のソースのデータの統合 |
| [1.2.4](../../domain1.md#skill-1-2-4) | 処理コストの最適化 |
| [1.2.5](../../domain1.md#skill-1-2-5) | 要件に合う変換サービスの選択 |
| [1.2.6](../../domain1.md#skill-1-2-6) | データ形式の変換 |
| [1.2.7](../../domain1.md#skill-1-2-7) | 変換の失敗と性能問題の調査 |
| [1.2.9](../../domain1.md#skill-1-2-9) | データの量、速度、種類 |

## 学習の順番 {#study-order}

1. [変換エンジン](../../../../services/data-engineering.md#choosing-transform): 要件の言葉からサービスを選びます。
2. [データ形式](../../../../services/data-engineering.md#data-formats): 列指向の利点と gzip の注意を覚えます。
3. [ETL ジョブ](../../../../services/data-engineering.md#glue-jobs): Flex、同時実行、タイムアウトを確認します。
4. [DPU とワーカータイプ](../../../../services/data-engineering.md#glue-dpu): OOM の症状と対処を対応づけます。
5. [データを取り込む他の方法](../../../../services/data-engineering.md#redshift-ingestion): コピーするかしないかで選びます。
6. [Firehose の失敗](../../../../services/streaming.md#firehose-failure): 配信と変換の失敗を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| Lambda の実行時間 | 最大 15 分 | 超えるなら Glue へ |
| Firehose の Lambda 呼び出し | 最大 5 分 | 超えるとタイムアウトのエラー |
| Firehose の課金 | 5 KB 単位に切り上げ | 小さなレコードはまとめる |
| Glue の最大同時実行数 | 既定 1 | 上げるとブックマークと両立しない |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 既存の Spark をクラスターなしで動かす | EMR Serverless |
| カタログ、ブックマーク、Data Quality を使う | Glue |
| 画面で整形する | DataBrew |
| 単発の形式変換 | Athena の CTAS |
| JSON のストリームを Parquet で S3 へ | Firehose の形式変換と Glue Data Catalog |
| ドライバーの OOM | `groupFiles` |
| エグゼキューターの OOM | `R` タイプか大きなワーカー |

## 引っかかりやすい点 {#traps}

- gzip は分割して読めません。大きな 1 ファイルは避けます。
- フェデレーテッドクエリの対象は RDS と Aurora の PostgreSQL と MySQL です。S3 は Spectrum で読みます。
- Clean Rooms はデータを見せない分析で、Data Exchange は購読です。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [transform 問1](../../exercises/transform.md#q1) | 1.2.3 | Redshift の顧客テーブルと、S3 にある 5 年分のクリックログを結合します。ログはほとんど… |
| [transform 問2](../../exercises/transform.md#q2) | 1.2.3 | Aurora MySQL の運用データを Redshift で分析します。ETL の開発と運用をせず… |
| [transform 問3](../../exercises/transform.md#q3) | 1.2.3 | 気象会社の有償のデータセットを購読し、自社の販売データと結合します。ファイル受け渡しの独自の仕組みは… |
| [transform 問4](../../exercises/transform.md#q4) | 1.2.4 | 夜間の Glue ジョブは、数時間の遅れがあってもかまいません。費用を下げるために変更するのはどれで… |
| [transform 問5](../../exercises/transform.md#q5) | 1.2.4 | 毎日 2 時間の Spark ジョブを EMR on EC2 で動かします。クラスターは常時起動で、… |
| [transform 問6](../../exercises/transform.md#q6) | 1.2.4 | Firehose の費用を調べると、1 件 300 バイトのレコードを 1 件ずつ大量に送っていまし… |
| [transform 問7](../../exercises/transform.md#q7) | 1.2.5 | 既存の Spark のコードと特定の EMR リリースをそのまま使います。クラスターの運用はしません… |
| [transform 問8](../../exercises/transform.md#q8) | 1.2.5 | アナリストが画面の操作だけで CSV の欠損を埋め、列を分割し、同じ手順を毎週適用します。コードは書… |
| [transform 問9](../../exercises/transform.md#q9) | 1.2.5 | S3 に届く 2 GB の JSON を変換します。処理は Python で 40 分かかり、毎日 … |
| [transform 問10](../../exercises/transform.md#q10) | 1.2.5 | Spark の ETL で、カタログとの連携、ジョブブックマーク、Data Quality を使い、… |
| [transform 問11](../../exercises/transform.md#q11) | 1.2.6 | S3 の CSV のログを Athena で週に数回読みます。列は 200 ありますが、毎回 5 列… |
| [transform 問12](../../exercises/transform.md#q12) | 1.2.6 | Firehose で受けた JSON を、Parquet で S3 へ保存します。コードは書きません… |
| [transform 問13](../../exercises/transform.md#q13) | 1.2.6 | 一度だけ、CSV のテーブルをパーティション付きの Parquet へ変換します。新しいジョブやクラ… |
| [transform 問14](../../exercises/transform.md#q14) | 1.2.7 | Glue ジョブのエグゼキューターが、結合と集計のステージで OOM になります。ドライバーは正常で… |
| [transform 問15](../../exercises/transform.md#q15) | 1.2.7 | 同じ Glue ジョブを別のパラメータで同時に 2 つ起動すると、2 つ目がエラーになります。ブック… |
| [transform 問16](../../exercises/transform.md#q16) | 1.2.7 | COPY が Load into table failed で失敗しました。どの行のどの列で失敗した… |
| [transform 問17](../../exercises/transform.md#q17) | 1.2.7 | Firehose の Lambda 変換で、関数が 7 分かかるレコードのバッチがあり、変換の失敗が… |
| [transform 問18](../../exercises/transform.md#q18) | 1.2.9 | 次のデータの置き場として適切な組み合わせはどれですか。売上テーブル、JSON のアプリログ、契約書の… |
| [transform 問19](../../exercises/transform.md#q19) | 1.2.9 | 1 日 1 回 1 GB を受けていたパイプラインが、新しい要件で秒間数万件のイベントを数秒以内に処… |
| [transform 問20](../../exercises/transform.md#q20) | 1.2.9 | ペタバイト級へ増えるクリックログを、S3 上で分析します。量の増加に合わせる設計として適切なものはど… |

<!-- questions:end -->
