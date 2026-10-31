# 分野5: ハルシネーション対策

根拠のない応答を減らし、見つける方法を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [5.1.5](../../domain5.md#obj-5-1-5) | ハルシネーションの検出とグラウンディング |

## 学習の順番 {#study-order}

1. [ハルシネーションへの対策](../../../../services/ai-fundamentals.md#hallucinations): 対策の一覧を覚えます。
2. [コンテキストグラウンディング](../../../../services/genai-apps.md#contextual-grounding): 2 つのスコアの違いを例で確認します。
3. [Automated Reasoning](../../../../services/genai-apps.md#automated-reasoning): 形式的に検証する機能を押さえます。
4. [構造化出力](../../../../services/genai-apps.md#structured-output): 出力の形式の検証を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 文書に基づいて答えさせる | RAG |
| 本番で根拠のない応答を止める | コンテキストグラウンディング |
| 規定との論理的な矛盾を検証する | Automated Reasoning |
| 出力の形式を確かめる | 構造化出力、JSON Schema |
| 信頼度が低い | 人に回す |

## 引っかかりやすい点 {#traps}

- グラウンディングは参照元に基づくか、関連性は質問に答えているかです。
- temperature を下げても、根拠のない応答は検出できません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [guardrails 問7](../../exercises/guardrails.md#q7) | 5.1.5 | 社内規定に答える RAG アプリが、文書にない内容を答えることがあります。本番で根拠のない応答を検出… |
| [guardrails 問8](../../exercises/guardrails.md#q8) | 5.1.5 | 応答は文書の内容に沿っていますが、質問には答えていません。コンテキストグラウンディングのスコアの状態… |
| [guardrails 問9](../../exercises/guardrails.md#q9) | 5.1.5 | 人事の規定と論理的に矛盾する回答がないかを形式的に検証し、理由も返してほしいと考えています。適切な機… |
| [guardrails 問10](../../exercises/guardrails.md#q10) | 5.1.5 | モデルの出力を後続のシステムに渡す前に、形式を確かめたいと考えています。適切な手法はどれですか。 |
| [guardrails 問11](../../exercises/guardrails.md#q11) | 5.1.5 | ハルシネーションを減らす手法として適切なものを選んでください。（2つ選択） |

<!-- questions:end -->
