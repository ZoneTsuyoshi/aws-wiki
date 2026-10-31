# 分野1: カスタムモデルのデプロイ

モデルの学習は範囲外です。調整済みのモデルをどう載せ、更新し、戻すかを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.2.4](../../domain1.md#skill-1-2-4) | カスタマイズしたモデルのデプロイとライフサイクル |

## 学習の順番 {#study-order}

1. [推論コンポーネントと LoRA](../../../../services/sagemaker.md#multi-model): アダプター推論コンポーネントで GPU を共有する構成を理解します。
2. [Model Registry](../../../../services/sagemaker.md#model-registry): `ModelApprovalStatus` と EventBridge の連携を押さえます。
3. [デプロイ戦略](../../../../services/sagemaker.md#deployment-strategies): Canary、Linear、シャドウの違いを確認します。
4. [Custom Model Import](../../../../services/genai-apps.md#custom-model-import): 対応する呼び出しと、対応しないものを覚えます。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 同じ基盤モデルの調整を多数、少ない GPU で提供する | LoRA のアダプター推論コンポーネント |
| 承認で自動デプロイする | Model Registry と EventBridge |
| 外部の重みを Bedrock で使う | Custom Model Import |

## 引っかかりやすい点 {#traps}

- Custom Model Import はバッチ推論と CloudFormation に対応しません。
- Legacy の基盤モデルでは、新しいファインチューニングと Provisioned Throughput を作れません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [custom-models 問1](../../exercises/custom-models.md#q1) | 1.2.4 | 同じ基盤モデルから LoRA で調整した用途別のモデルが 20 個あり、SageMaker AI で… |
| [custom-models 問2](../../exercises/custom-models.md#q2) | 1.2.4 | 調整済みモデルの新しい版を、審査役が承認した時点で本番へ自動でデプロイしたいと考えています。承認の記… |
| [custom-models 問3](../../exercises/custom-models.md#q3) | 1.2.4 | SageMaker AI のエンドポイントで動く調整済みモデルを更新します。新しい版に問題があれば利… |
| [custom-models 問4](../../exercises/custom-models.md#q4) | 1.2.4 | 外部で調整した Hugging Face 形式の Llama の重みを、Bedrock の API … |

<!-- questions:end -->
