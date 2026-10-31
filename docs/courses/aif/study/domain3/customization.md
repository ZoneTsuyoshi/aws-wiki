# 分野3: モデルのカスタマイズ

方法ごとの費用のトレードオフと、ファインチューニングのデータの準備を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.1.5](../../domain3.md#obj-3-1-5) | FM のカスタマイズのコストのトレードオフ |
| [3.3.1](../../domain3.md#obj-3-3-1) | FM の学習の主な要素 |
| [3.3.2](../../domain3.md#obj-3-3-2) | ファインチューニングの方法 |
| [3.3.3](../../domain3.md#obj-3-3-3) | ファインチューニングのデータの準備 |

## 学習の順番 {#study-order}

1. [モデルを業務に合わせる方法](../../../../services/ai-fundamentals.md#customization-options): 費用の小さい順の表を覚えます。
2. [モデルカスタマイズ](../../../../services/genai-apps.md#customization): 現在の Bedrock の一覧にある 3 つを確認します。
3. [データの準備](../../../../services/genai-apps.md#fine-tuning-data): データの確認項目を押さえます。
4. [カスタムモデルの実行](../../../../services/genai-apps.md#custom-model-deploy): カスタムモデルの実行方法を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| まず費用をかけずに試す | プロンプトに例を入れる（文脈内の学習） |
| 精度を保ち推論を安くする | 蒸留 |
| 文体や形式を学ばせる | ファインチューニング |
| 指示と模範の応答の組で調整する | インストラクションチューニング |
| 分野の用語に合わせる | ドメインへの適応 |
| 別のタスクの学習済みモデルを調整する | 転移学習 |
| ラベルのないデータで学習を続ける | 継続的な事前学習 |
| 報酬関数のスコアから学ぶ | 強化ファインチューニング |
| 本番の利用者とデータが違う | 代表性の不足 |

## 引っかかりやすい点 {#traps}

- 継続的な事前学習は試験ガイドに載りますが、現在の Bedrock の一覧にはありません。
- モデルは誤ったデータも学習します。キュレーションが必要です。
- カスタムモデルの実行には Provisioned Throughput かカスタムモデルのデプロイが必要です。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [customization 問1](../../exercises/customization.md#q1) | 3.1.5 | FM を業務に合わせる方法を、費用が小さい順に並べたものはどれですか。 |
| [customization 問2](../../exercises/customization.md#q2) | 3.1.5 | まず費用をかけずに FM の出力を業務に合わせたいと考えています。最初に試す方法はどれですか。 |
| [customization 問3](../../exercises/customization.md#q3) | 3.1.5 | 大きなモデルと同等の精度を保ちながら、推論の費用を下げたいと考えています。適切な方法はどれですか。 |
| [customization 問4](../../exercises/customization.md#q4) | 3.1.5 | 自社の独特の文体でモデルに文章を書かせたいと考えています。プロンプトの工夫では足りませんでした。次に… |
| [customization 問5](../../exercises/customization.md#q5) | 3.3.1 | 現在の Bedrock のカスタマイズの一覧にある方法を選んでください。（2つ選択） |
| [customization 問6](../../exercises/customization.md#q6) | 3.3.1 | FM の学習の要素のうち、通常はモデルの提供者が行うものはどれですか。 |
| [customization 問7](../../exercises/customization.md#q7) | 3.3.1, 3.3.2 | ラベルのない大量の社内文書を与えて、既存のモデルの学習を続ける手法はどれですか。 |
| [customization 問8](../../exercises/customization.md#q8) | 3.3.1 | 教師モデルと生徒モデルが登場する手法はどれですか。 |
| [customization 問9](../../exercises/customization.md#q9) | 3.3.2 | 「要約して」という指示と模範の要約の組を多数用意して、モデルを調整します。この方法はどれですか。 |
| [customization 問10](../../exercises/customization.md#q10) | 3.3.2 | 一般的な言語モデルを、医療の語彙と文脈に強くしたいと考えています。この調整の呼び名はどれですか。 |
| [customization 問11](../../exercises/customization.md#q11) | 3.3.2 | 少ないデータで専用のモデルを作るために、別のタスクで学習済みのモデルを調整します。この手法の利点はど… |
| [customization 問12](../../exercises/customization.md#q12) | 3.3.2 | Bedrock の強化ファインチューニングで、モデルが学ぶ材料はどれですか。 |
| [customization 問13](../../exercises/customization.md#q13) | 3.3.3 | ファインチューニングのデータに、誤った回答が多く混ざっています。起きやすい結果はどれですか。 |
| [customization 問14](../../exercises/customization.md#q14) | 3.3.3 | 顧客の問い合わせ履歴でファインチューニングします。学習の前にすべきことはどれですか。 |
| [customization 問15](../../exercises/customization.md#q15) | 3.3.3 | 学習データが首都圏の問い合わせばかりですが、本番は全国の利用者が使います。問題となっている観点はどれ… |
| [customization 問16](../../exercises/customization.md#q16) | 3.3.3 | RLHF の説明として正しいものはどれですか。 |
| [customization 問17](../../exercises/customization.md#q17) | 3.3.3 | ファインチューニングのデータの準備として適切なものを選んでください。（2つ選択） |

<!-- questions:end -->
