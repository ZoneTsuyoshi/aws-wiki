# 分野3: データの取り込みと分析

ストリーミング、形式の変換、データレイク、可視化を要件から選びます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [ストリーミング](../../domain3.md#t3-5-streaming) | ストリーミングデータサービスの適切な用途、データストリーミングアーキテクチャの設計 |
| [取り込みのパターンと設定](../../domain3.md#t3-5-ingestion) | データ取り込みのパターン、業務要件に必要なサイズと速度、取り込みの適切な設定の選択 |
| [取り込みポイントの保護](../../domain3.md#t3-5-secure) | 取り込みのアクセスポイントのセキュリティ |
| [データレイクの構築と保護](../../domain3.md#t3-5-lake) | データレイクの構築と保護 |
| [変換と形式](../../domain3.md#t3-5-transform) | データ変換サービスの適切な用途、形式間のデータ変換 |
| [データ処理のコンピューティング](../../domain3.md#t3-5-compute) | データ処理に適したコンピューティングの選択 |
| [分析と可視化](../../domain3.md#t3-5-analytics) | データ分析と可視化サービスの適切な用途、可視化の戦略の実装 |

## 学習の順番 {#study-order}

1. [Kinesis Data Streams、Firehose、SQS の選び方](../../../../services/streaming.md#choosing)と[シャードの容量](../../../../services/streaming.md#shards): サービスの選択とシャードの計算を確認します。
2. [消費者と拡張ファンアウト](../../../../services/streaming.md#enhanced-fan-out)と[パーティションキー](../../../../services/streaming.md#partition-key): 読み取りの帯域と書き込みの偏りを押さえます。
3. [バッファ](../../../../services/streaming.md#firehose-buffering)と[その他の機能](../../../../services/streaming.md#firehose-features): 遅れと費用、形式の変換を確認します。
4. [暗号化](../../../../services/streaming.md#kinesis-encryption)と[署名付き URL](../../../../services/s3.md#presigned-urls): 受け口の保護を確認します。
5. [クローラー](../../../../services/data-engineering.md#glue-crawlers)と[LF タグ](../../../../services/data-engineering.md#lake-formation-lf-tags): カタログと権限の流れを理解します。
6. [ETL ジョブ](../../../../services/data-engineering.md#glue-jobs)と[データ形式](../../../../services/data-engineering.md#data-formats): 変換の方法を比べます。
7. [クラスターのノード](../../../../services/data-engineering.md#emr-nodes)と[HDFS と S3](../../../../services/data-engineering.md#emr-hdfs-vs-s3): ノードの役割とデータの置き場所を確認します。
8. [Amazon Athena](../../../../services/streaming.md#athena)と[Amazon Quick Sight](../../../../services/data-engineering.md#quick-sight): 分析と可視化の選択を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| シャード 1 つの書き込み | 1 MB/秒、1,000 レコード/秒 | 総量と件数の両方で計算 |
| シャードの読み取り | 共有で 2 MB/秒 | 拡張ファンアウトはコンシューマーごと |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 順序付きで複数のアプリが読み直す | Kinesis Data Streams |
| コードなしで S3 へ配信する | Amazon Data Firehose |
| 一部のシャードだけスロットリング | パーティションキーの値を増やす |
| 列と行の権限 | Lake Formation |
| CSV を定期的に Parquet へ | Glue の ETL ジョブ |
| 単発の SQL で変換 | Athena の CTAS |
| 既存の Spark を不定期に | EMR Serverless |
| ダッシュボードを速く、Athena の費用を抑える | Quick Sight の SPICE |

## 引っかかりやすい点 {#traps}

- Firehose はバッファの分だけ遅れるので「ほぼリアルタイム」です。
- EMR のタスクノードは HDFS を持たないので Spot に向きます。
- Data Pipeline は新規のお客様は利用できません。Glue や Step Functions を選びます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [data-analytics 問1](../../exercises/data-analytics.md#q1) | ストリーミング | 順序付きのイベントを、複数のアプリが独自のコードで読み、24 時間以内なら読み直します。どれを選びま… |
| [data-analytics 問2](../../exercises/data-analytics.md#q2) | ストリーミング | ログを S3 と OpenSearch Service に、コードなしで配信します。数十秒の遅れは許… |
| [data-analytics 問3](../../exercises/data-analytics.md#q3) | ストリーミング | 毎秒 5,000 件、1 件 1 KB のイベントを Kinesis に書きます。プロビジョンドモー… |
| [data-analytics 問4](../../exercises/data-analytics.md#q4) | ストリーミング | 同じストリームを 5 つのコンシューマーが読み、読み取りの遅延が増えています。シャードの共有の 2 … |
| [data-analytics 問5](../../exercises/data-analytics.md#q5) | 取り込みの設定 | Kinesis で一部のシャードだけが ProvisionedThroughputExceededE… |
| [data-analytics 問6](../../exercises/data-analytics.md#q6) | 取り込みの設定 | 取り込みの頻度に合わせた選択として正しいものはどれですか。 |
| [data-analytics 問7](../../exercises/data-analytics.md#q7) | 取り込みの設定 | Firehose から S3 への配信で、小さなファイルが多く、Athena が遅くなっています。遅… |
| [data-analytics 問8](../../exercises/data-analytics.md#q8) | 取り込みポイントの保護 | Kinesis Data Streams への取り込みを保護します。適切な組み合わせを選んでください… |
| [data-analytics 問9](../../exercises/data-analytics.md#q9) | 取り込みポイントの保護 | モバイルアプリから S3 へ直接アップロードさせます。AWS の認証情報は渡さず、有効期限も短くしま… |
| [data-analytics 問10](../../exercises/data-analytics.md#q10) | 取り込みポイントの保護 | SFTP の受け口を VPC の内部からだけ使わせます。利用者ごとに書き込めるプレフィックスも分けま… |
| [data-analytics 問11](../../exercises/data-analytics.md#q11) | データレイク | S3 のデータレイクのスキーマを自動で検出し、Athena からテーブルとして使います。どの組み合わ… |
| [data-analytics 問12](../../exercises/data-analytics.md#q12) | データレイク | データレイクの列と行の権限を、属性で多数のテーブルにまとめて付けます。別のアカウントとも共有します。… |
| [data-analytics 問13](../../exercises/data-analytics.md#q13) | データレイク | データレイクのクエリの費用を下げ、日付で絞る処理も速くします。どの設計が適切ですか。 |
| [data-analytics 問14](../../exercises/data-analytics.md#q14) | 変換と形式 | S3 の CSV を定期的に Parquet に変換します。サーバーレスの Spark で、カタログ… |
| [data-analytics 問15](../../exercises/data-analytics.md#q15) | 変換と形式 | S3 上のテーブルを、単発の SQL で Parquet に変換します。サーバーの準備はしません。ど… |
| [data-analytics 問16](../../exercises/data-analytics.md#q16) | 変換と形式 | Firehose で受ける JSON を、配信のときに Parquet に変えます。どの機能を使いま… |
| [data-analytics 問17](../../exercises/data-analytics.md#q17) | データ処理 | 既存の Spark のジョブで、ノードの費用を下げます。一部のノードの中断は許せます。データは S3… |
| [data-analytics 問18](../../exercises/data-analytics.md#q18) | データ処理 | 不定期に実行する Spark のジョブで、クラスターを管理せず、EMR のランタイムを使います。どれ… |
| [data-analytics 問19](../../exercises/data-analytics.md#q19) | データ処理 | EMR クラスターを止めてもデータを失わず、ジョブのときだけ起動します。データはどこに置きますか。 |
| [data-analytics 問20](../../exercises/data-analytics.md#q20) | 分析と可視化 | S3 のログに単発の SQL を投げます。インフラの準備はしません。どれを選びますか。 |
| [data-analytics 問21](../../exercises/data-analytics.md#q21) | 分析と可視化 | 業務のダッシュボードで、Athena のクエリの費用を抑えつつ表示を速くします。最新性は 1 時間前… |
| [data-analytics 問22](../../exercises/data-analytics.md#q22) | 分析と可視化 | ダッシュボードで、地域の担当者には自分の地域の行だけを見せます。どの機能ですか。 |

<!-- questions:end -->
