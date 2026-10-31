# 分野1: データの収集と保存

データがどこにあるかで取り出し方を決め、要件に合う保存先と形式を選びます。症状から原因を当てる問題も出ます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.1.1](../../domain1.md#skill-1-1-1) | データソースからの抽出 |
| [1.1.2](../../domain1.md#skill-1-1-2) | ストレージの選択と設定 |
| [1.1.3](../../domain1.md#skill-1-1-3) | 取り込みと保存の問題の解決 |
| [1.1.5](../../domain1.md#skill-1-1-5) | データ形式の選択 |
| [1.1.6](../../domain1.md#skill-1-1-6) | 複数のソースの結合 |

## 学習の順番 {#study-order}

1. [入力モード](../../../../services/sagemaker.md#input-modes): File、FastFile、Pipe の違いと、EFS を File モードで読むことを押さえます。
2. [DynamoDB のバックアップ](../../../../services/dynamodb.md#backup): S3 へのエクスポートが本番に負荷をかけない理由を確認します。
3. [ストレージクラス](../../../../services/s3.md#storage-classes)と[ライフサイクル](../../../../services/s3.md#lifecycle): アクセスの頻度から保存先を決めます。
4. [ストレージの比較](../../../../services/storage-advanced.md#storage-comparison): EFS、FSx for Lustre、EBS の違いを表で覚えます。
5. [データ形式](../../../../services/data-engineering.md#data-formats)と[パーティション](../../../../services/data-engineering.md#partitioning): Parquet と日付のパーティションの効果を理解します。
6. [S3 のリクエストレート](../../../../services/s3.md#request-rate)、[EFS のスループット](../../../../services/storage.md#efs-throughput-mode)、[パーティションの同期](../../../../services/data-engineering.md#partition-sync): 症状と原因を結びつけます。
7. [Glue のジョブ](../../../../services/data-engineering.md#glue-jobs)と[変換エンジンの選び方](../../../../services/data-engineering.md#choosing-transform): 結合の手段を選びます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| S3 Express One Zone | 1 桁ミリ秒 | 単一の AZ で許容できるとき |
| Glacier Deep Archive | 読むのは年 1 回未満 | 長期保管の最小コスト |
| DynamoDB のエクスポート形式 | DynamoDB JSON か Amazon Ion | PITR が必要 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| DynamoDB の全件を本番に影響なく S3 へ | PITR とエクスポート |
| 大きな学習データで開始が遅い | FastFile モード |
| GPU へ大量のデータを高速に渡す | S3 と連携した FSx for Lustre |
| 一部の列しか読まないのにスキャン料金が高い | Parquet とパーティション |
| 新しいパーティションがクエリに出ない | `MSCK REPAIR TABLE` かクローラー |
| Glue の結合でエグゼキューターが OOM | `R` タイプか大きなワーカー |

## 引っかかりやすい点 {#traps}

- 全件の Scan はキャパシティを消費します。本番の DynamoDB には使いません。
- gzip の大きな 1 ファイルは分割して読めません。Parquet の中で Snappy などを使います。
- 時系列の結合で予測の時点より後の値が混ざると、検証の結果だけがよくなります。
- S3 の 503 はプレフィックスの分散とバックオフで解決します。ストレージクラスや暗号化は関係ありません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [data-ingestion 問1](../../exercises/data-ingestion.md#q1) | 1.1.1 | ある EC サイトの注文データは DynamoDB にあり、本番の読み書きに余裕がありません。週に … |
| [data-ingestion 問2](../../exercises/data-ingestion.md#q2) | 1.1.1 | 学習データは 2 TB で S3 にあります。データをすべて読むのではなく一部の読み取りが中心で、ジ… |
| [data-ingestion 問3](../../exercises/data-ingestion.md#q3) | 1.1.1 | 共有の EFS にある学習データを、SageMaker AI の学習ジョブで読みます。S3 にコピー… |
| [data-ingestion 問4](../../exercises/data-ingestion.md#q4) | 1.1.2 | 読み取りが頻繁で、1 桁ミリ秒の応答が必要な特徴量のファイルを S3 に置きます。単一の AZ でも… |
| [data-ingestion 問5](../../exercises/data-ingestion.md#q5) | 1.1.2 | 学習が終わった実験データを規制で 7 年保管します。読み出すのは年 1 回未満で、取り出しに時間がか… |
| [data-ingestion 問6](../../exercises/data-ingestion.md#q6) | 1.1.2 | GPU のインスタンスを多数使う学習で、S3 の大量の学習データを高いスループットで読ませたいです。… |
| [data-ingestion 問7](../../exercises/data-ingestion.md#q7) | 1.1.3 | 取り込みジョブが 1 つの S3 プレフィックスに短時間で書き込みを集中させ、HTTP 503（Sl… |
| [data-ingestion 問8](../../exercises/data-ingestion.md#q8) | 1.1.3 | EFS をデータ置き場にした学習で、数時間後からファイルの読み取りが急に遅くなりました。スループット… |
| [data-ingestion 問9](../../exercises/data-ingestion.md#q9) | 1.1.3 | Hive 形式で S3 に日付パーティションを毎日追加しています。データはあるのに、Athena で… |
| [data-ingestion 問10](../../exercises/data-ingestion.md#q10) | 1.1.5 | 列が 150 ある CSV のログを Athena で集計しています。クエリはいつも 5 列だけ読み… |
| [data-ingestion 問11](../../exercises/data-ingestion.md#q11) | 1.1.5 | 外部の取引先から入れ子の JSON ログを毎日受け取ります。学習の前に分析しやすくしたいです。データ… |
| [data-ingestion 問12](../../exercises/data-ingestion.md#q12) | 1.1.5 | Glue のジョブを Parquet で出力します。後続の Spark でファイルを並列に読みたいで… |
| [data-ingestion 問13](../../exercises/data-ingestion.md#q13) | 1.1.6 | 複数の S3 のカタログテーブルと RDS のマスターを結合します。Spark のコードは書けますが… |
| [data-ingestion 問14](../../exercises/data-ingestion.md#q14) | 1.1.6 | 大きなテーブルを結合する Glue の Spark ジョブで、エグゼキューターのメモリ不足が起きてい… |
| [data-ingestion 問15](../../exercises/data-ingestion.md#q15) | 1.1.6 | 過去の取引から翌月の解約を予測します。顧客マスターと取引履歴を結合したところ、検証の結果だけが異常に… |
| [data-ingestion 問16](../../exercises/data-ingestion.md#q16) | 1.1.1 | 本番の RDS のデータを学習用に定期的に取り出します。本番への負荷に注意しつつ、S3 に Parq… |

<!-- questions:end -->
