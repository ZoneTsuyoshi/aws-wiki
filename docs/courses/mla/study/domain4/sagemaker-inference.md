# 分野4: インスタンスの選択

モデルに合う推論のインスタンスファミリーを選びます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.2.1](../../domain4.md#skill-4-2-1) | 推論のインスタンスファミリーの選択 |

## 学習の順番 {#study-order}

1. [インスタンスの選び方](../../../../services/sagemaker.md#instance-selection): ファミリーの用途を覚えます。
2. [Inference Recommender](../../../../services/sagemaker.md#inference-optimization): 負荷試験の役割を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 表データの推論 | `ml.m5`、`ml.c5` |
| 深層学習、LLM | `ml.g5`、`ml.p4d`、`ml.p5` |
| 推論のコストと性能 | `ml.inf1`、`ml.inf2` |
| サイズを負荷試験で決める | Inference Recommender |

## 引っかかりやすい点 {#traps}

- Inferentia は CUDA 向けのコードがそのまま動きません。AWS Neuron でコンパイルします。
- `ml.trn1` の Trainium は学習のコストを下げる専用チップです。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [sagemaker-inference 問22](../../exercises/sagemaker-inference.md#q22) | 4.2.1 | 表データの XGBoost の推論です。GPU は不要で、コストを抑えます。どのファミリーを選びます… |
| [sagemaker-inference 問23](../../exercises/sagemaker-inference.md#q23) | 4.2.1 | 深層学習の推論のコストを Inferentia で下げます。CUDA 向けのコードを使っています。ど… |
| [sagemaker-inference 問24](../../exercises/sagemaker-inference.md#q24) | 4.2.1 | 候補のインスタンスで負荷試験をして、推論に適切なサイズを決めます。どの機能ですか。 |

<!-- questions:end -->
