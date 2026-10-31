# 分野3: Bedrock の FM のデプロイ

負荷の形で FM のデプロイ方式を選びます。自前でホストするときの資源の設定も問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.1.4](../../domain3.md#skill-3-1-4) | FM のデプロイ方式の評価と選択 |
| [3.1.7](../../domain3.md#skill-3-1-7) | FM のデプロイ、ホスティング、リソースの設定 |
| [3.2.1](../../domain3.md#skill-3-2-1) | オンデマンドとプロビジョンドの最適化 |

## 学習の順番 {#study-order}

1. [デプロイ戦略](../../../../services/genai-apps.md#deployment): 方式ごとの課金と場面を比べます。
2. [スループットの選択肢](../../../../services/ai.md#throughput-options)と[推論の容量](../../../../services/genai-apps.md#inference-profiles): Provisioned Throughput とモデルユニットを確認します。
3. [マルチモデルと推論コンポーネント](../../../../services/sagemaker.md#multi-model)と [SageMaker AI での FM](../../../../services/genai-apps.md#sagemaker-fm): GPU の共有を押さえます。
4. [推論の最適化](../../../../services/sagemaker.md#inference-optimization): 量子化とコンパイルの違いを覚えます。
5. [サーバーレス](../../../../services/sagemaker.md#serverless): Provisioned Concurrency を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 変動する負荷で小さく始める | Bedrock のオンデマンド |
| 固定の大きな処理量、カスタムモデル | Provisioned Throughput |
| 大量で急がない | バッチ、Flex |
| モデルと GPU を細かく制御する | SageMaker JumpStart |
| 複数の FM で GPU を共有する | 推論コンポーネント |
| GPU メモリが足りない | 量子化、大きなインスタンス |
| モデルユニットの見積もり | `InputTokenCount` と `OutputTokenCount` のピーク |

## 引っかかりやすい点 {#traps}

- Provisioned Throughput は削除するまで時間課金です。コミットメントの期間中は削除できません。
- コンパイルは精度が落ちません。量子化は少し落ちることがあります。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [bedrock-fm 問7](../../exercises/bedrock-fm.md#q7) | 3.1.4 | 利用者の増減が読めない新規の社内アプリで、FM を素早く使い始めます。どのデプロイ方式ですか。 |
| [bedrock-fm 問8](../../exercises/bedrock-fm.md#q8) | 3.1.4 | モデルの重みやサーバーの GPU を細かく制御し、VPC の中で FM をホストします。どの方式です… |
| [bedrock-fm 問9](../../exercises/bedrock-fm.md#q9) | 3.1.4 | カスタムモデルを常に一定の大きな処理量で動かします。Bedrock の中で選ぶ方式はどれですか。 |
| [bedrock-fm 問10](../../exercises/bedrock-fm.md#q10) | 3.1.7 | 複数の FM を 1 台の GPU のエンドポイントで共有し、モデルごとに資源を割り当てます。Sag… |
| [bedrock-fm 問11](../../exercises/bedrock-fm.md#q11) | 3.1.7 | LLM の GPU メモリが足りません。多少の精度の低下は許容できます。インスタンスのサイズは変えま… |
| [bedrock-fm 問12](../../exercises/bedrock-fm.md#q12) | 3.1.7 | Bedrock の Provisioned Throughput のモデルユニット数を見積もります。… |
| [bedrock-fm 問13](../../exercises/bedrock-fm.md#q13) | 3.2.1 | 需要が読めず、平均の使用率が低い Bedrock のアプリがあります。Provisioned Thr… |
| [bedrock-fm 問14](../../exercises/bedrock-fm.md#q14) | 3.2.1 | Bedrock の Provisioned Throughput で 1 か月のコミットメントを選び… |
| [bedrock-fm 問15](../../exercises/bedrock-fm.md#q15) | 3.2.1 | SageMaker AI のエンドポイントの負荷が、予測できるバーストを持ちます。サーバーレス推論で… |

<!-- questions:end -->
