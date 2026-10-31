# 分野2: モデルの監視とテスト

学習時をベースラインにして本番と比べる流れと、シャドウテストと本番バリアントの違いを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.3.2](../../domain2.md#skill-2-3-2) | ベースラインの作成とドリフト検知 |
| [2.3.3](../../domain2.md#skill-2-3-3) | シャドウバリアントと本番バリアントの比較 |

## 学習の順番 {#study-order}

1. [ドリフトの種類](../../../../services/sagemaker.md#drift): データ、コンセプト、予測、バイアスを区別します。
2. [Model Monitor](../../../../services/sagemaker.md#model-monitor): 流れと新規の場合の移行先を覚えます。
3. [デプロイとテストの戦略](../../../../services/sagemaker.md#deployment-strategies): シャドウと A/B の違いを確認します。
4. [CloudWatch のメトリクス](../../../../services/sagemaker.md#cloudwatch-metrics): 比べる指標を押さえます。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 入力の分布は同じで精度が落ちた | コンセプトドリフト |
| 新規に監視を作る | Processing の Evidently AI と EventBridge Scheduler |
| 利用者に影響させずに遅延を確かめる | シャドウテスト |
| 業務指標を比べる | A/B（本番バリアント） |
| シャドウで精度を見る | ログを保存して、届いた正解と結合する |

## 引っかかりやすい点 {#traps}

- Model Monitor は新規顧客の受付を終了しています。
- シャドウの応答は利用者に返らないので、業務指標は測れません。
- モデル品質の監視には正解ラベルが必要です。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [model-monitoring 問1](../../exercises/model-monitoring.md#q1) | 2.3.2 | 半年で精度が落ちましたが、入力の分布はほとんど変わっていません。どのドリフトですか。 |
| [model-monitoring 問2](../../exercises/model-monitoring.md#q2) | 2.3.2 | 既に SageMaker Model Monitor を使っているチームが、データ品質を監視します。… |
| [model-monitoring 問3](../../exercises/model-monitoring.md#q3) | 2.3.2 | 新規の顧客がドリフトの監視を作ります。Model Monitor は新規の受付を終了しています。公式… |
| [model-monitoring 問4](../../exercises/model-monitoring.md#q4) | 2.3.3 | 新しいモデルの遅延と安定性を、利用者に影響を与えずに本番のトラフィックで確かめます。どの方式ですか。 |
| [model-monitoring 問5](../../exercises/model-monitoring.md#q5) | 2.3.3 | シャドウテストで比べる項目の組み合わせとして適切なものはどれですか。 |
| [model-monitoring 問6](../../exercises/model-monitoring.md#q6) | 2.3.3 | シャドウテストで新しいモデルの精度も確かめます。正解のラベルは数日後に届きます。どうしますか。 |

<!-- questions:end -->
