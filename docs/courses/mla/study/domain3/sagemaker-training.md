# 分野3: 学習と推論のジョブの設定

学習ジョブとバッチ変換の設定の項目を、症状と結びつけて覚えます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.3.3](../../domain3.md#skill-3-3-3) | 学習ジョブと推論ジョブの設定 |

## 学習の順番 {#study-order}

1. [学習ジョブの設定](../../../../services/sagemaker.md#training-job): 項目と誤ったときの症状を確認します。
2. [バッチ変換](../../../../services/sagemaker.md#batch-transform): サイズ、分割、結合の設定を押さえます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| `MaxPayloadInMB` | 既定 6、最大 100 | |
| `MaxConcurrentTransforms × MaxPayloadInMB` | 100 以下 | |

## こう問われたらこう考える {#decisions}

| 症状 | 確認する項目 |
|---|---|
| チャネル名の実行時エラー | `InputDataConfig` |
| 最後に権限不足で失敗する | `OutputDataConfig` と実行ロール |
| `No space left` | `ResourceConfig` のボリューム |
| 途中で止まる | `StoppingCondition` の `MaxRuntimeInSeconds` |
| 1 ファイルで 1 台しか働かない | 入力を複数のファイルに分割する（`SplitType` では分散しない） |

## 引っかかりやすい点 {#traps}

- `SplitType` が `None` だと、1 ファイルを 1 リクエストで送ります。
- ID を除いて推論し結果と結合するには、`InputFilter`、`JoinSource`、`OutputFilter` を使います。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [sagemaker-training 問16](../../exercises/sagemaker-training.md#q16) | 3.3.3 | 学習ジョブが終盤に、S3 への出力の権限不足で失敗しました。原因の設定はどれですか。 |
| [sagemaker-training 問17](../../exercises/sagemaker-training.md#q17) | 3.3.3 | バッチ変換で 1 ファイル 50 GB の CSV を処理します。インスタンスを 4 台にしましたが… |
| [sagemaker-training 問18](../../exercises/sagemaker-training.md#q18) | 3.3.3 | バッチ変換で、入力の ID の列を除いて推論し、結果を ID と結合して出力します。正しい設定はどれ… |

<!-- questions:end -->
