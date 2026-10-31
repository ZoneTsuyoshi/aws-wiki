# 分野4: Guardrails

要件を読んで、どのフィルターを使うかを選びます。マスクできるのは 1 つだけです。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.1.2](../../domain4.md#obj-4-1-2) | 責任ある AI のツール |

## 学習の順番 {#study-order}

1. [フィルターの種類](../../../../services/ai.md#guardrail-filters): フィルターの種類とアクションを表で覚えます。
2. [Guardrails の実践](../../../../services/genai-apps.md#guardrails-depth): Guardrails の実践の概要を確認します。
3. [Bedrock Evaluations](../../../../services/genai-apps.md#bedrock-evaluations): 実行時の防御と導入前の計測を区別します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 投資助言のような話題を避ける | 拒否トピック |
| 競合の社名を出さない | ワードフィルター |
| 電話番号を隠す | 機密情報フィルター（`ANONYMIZE`） |
| 暴力や差別を止める | コンテンツフィルター |
| ジェイルブレイクを防ぐ | プロンプト攻撃 |

## 引っかかりやすい点 {#traps}

- マスクは機密情報フィルターだけの機能です。
- ワードフィルターは語句の一致を見るので、話題全体を止めるには向きません。
- Guardrails は実行時の防御です。導入前の計測には Bedrock の評価を使います。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [guardrails 問1](../../exercises/guardrails.md#q1) | 4.1.2 | 銀行のチャットボットに投資の助言をさせたくありません。Guardrails の適切な機能はどれですか… |
| [guardrails 問2](../../exercises/guardrails.md#q2) | 4.1.2 | チャットボットの応答で、顧客の電話番号を隠して返したいと考えています。Guardrails の適切な… |
| [guardrails 問3](../../exercises/guardrails.md#q3) | 4.1.2 | 競合の社名を応答に出したくありません。適切な機能はどれですか。 |
| [guardrails 問4](../../exercises/guardrails.md#q4) | 4.1.2 | 架空の設定で安全策を回避しようとする入力を止めたいと考えています。適切な機能はどれですか。 |
| [guardrails 問5](../../exercises/guardrails.md#q5) | 4.1.2 | Guardrails とモデルの評価の違いとして正しいものはどれですか。 |
| [guardrails 問6](../../exercises/guardrails.md#q6) | 4.1.2 | 保険会社のチャットボットで、暴力的な内容を止め、口座番号も隠したいと考えています。適切な組み合わせを… |

<!-- questions:end -->
