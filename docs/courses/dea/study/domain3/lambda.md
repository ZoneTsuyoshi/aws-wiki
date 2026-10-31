# 分野3: Lambda による自動化

Lambda をパイプラインのどこで使い、どこで使わないかを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.1.8](../../domain3.md#skill-3-1-8) | Lambda によるデータ処理の自動化 |

## 学習の順番 {#study-order}

1. [呼び出しの種類](../../../../services/lambda.md#invocation-types): 同期、非同期、ポーリングを確認します。
2. [Firehose の変換](../../../../services/streaming.md#firehose-transform): 戻り値の形を覚えます。
3. [ほぼリアルタイムの処理](../../../../services/lambda.md#near-real-time): 使える場面を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| 実行時間 | 最大 15 分 | 大きな変換は Glue か EMR |
| `/tmp`、メモリ | 最大 10,240 MB | 大きなデータには向かない |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 到着したファイルの検証と Glue の起動 | S3 イベントと Lambda |
| 配信前のレコードの変換 | Firehose の Lambda 変換 |
| 定期的なパーティションの追加 | EventBridge Scheduler と Lambda |
| 数百 GB の結合 | Glue か EMR |

## 引っかかりやすい点 {#traps}

- Firehose の変換は `recordId` を入力と同じ値で返します。
- Lambda は起動と小さな変換に使います。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [lambda 問10](../../exercises/lambda.md#q10) | 3.1.8 | S3 に CSV が届いたら形式を検証し、問題なければ Glue ジョブを起動します。検証は数秒です… |
| [lambda 問11](../../exercises/lambda.md#q11) | 3.1.8 | Firehose が S3 へ配信する前に、各レコードの個人情報の列を消します。Lambda の変換… |
| [lambda 問12](../../exercises/lambda.md#q12) | 3.1.8 | Lambda によるデータ処理の自動化で、適切でないものはどれですか。 |

<!-- questions:end -->
