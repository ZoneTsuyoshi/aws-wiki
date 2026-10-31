# 分野2: カスタマイズの戦略

手軽な方法から順に検討します。「最新の情報に答えさせる」はファインチューニングではなく RAG です。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.1.2](../../domain2.md#skill-2-1-2) | 事前学習済み FM のファインチューニング戦略 |

## 学習の順番 {#study-order}

1. [方法の比較](../../../../services/ai-fundamentals.md#customization-options): プロンプト、RAG、調整の順を確認します。
2. [モデルカスタマイズ](../../../../services/genai-apps.md#customization): 教師あり、強化、蒸留の違いを覚えます。
3. [SageMaker AI での FM](../../../../services/genai-apps.md#sagemaker-fm): LoRA のアダプターを押さえます。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 情報が頻繁に変わる、引用が必要 | RAG |
| 文体を学ばせる、正解の例がある | 教師ありファインチューニング |
| 正解は決めにくいが採点はできる | 強化ファインチューニング |
| 精度を保って推論を安くする | 蒸留 |
| 少ない GPU で用途別のモデル | LoRA のアダプター |

## 引っかかりやすい点 {#traps}

- ファインチューニングしても、新しい情報は再学習するまで反映されません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [fm-customization 問4](../../exercises/fm-customization.md#q4) | 2.1.2 | 毎週更新される社内規定に答え、根拠の文書も示します。方法の選択として適切なものはどれですか。 |
| [fm-customization 問5](../../exercises/fm-customization.md#q5) | 2.1.2 | 上位のモデルで品質に満足していますが、推論のコストが高いです。応答の品質はなるべく保ちます。どのカス… |
| [fm-customization 問6](../../exercises/fm-customization.md#q6) | 2.1.2 | 用途の違う多数の小さな調整を、少ない GPU で提供します。SageMaker AI で FM を動… |
| [fm-customization 問7](../../exercises/fm-customization.md#q7) | 2.1.2 | 特定の文体で回答させたいです。プロンプトの例示では足りません。正解の文例は 1,000 件あります。… |

<!-- questions:end -->
