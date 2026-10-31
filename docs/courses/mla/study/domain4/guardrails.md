# 分野4: 安全策

生成 AI のリスクと対策を組み合わせて答えます。Guardrails の機能と層の選択、ストリーミングの動作を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.3.7](../../domain4.md#skill-4-3-7) | セキュリティリスクと脆弱性の特定と緩和 |
| [4.3.9](../../domain4.md#skill-4-3-9) | 安全策と機密データの保護 |

## 学習の順番 {#study-order}

1. [多層防御](../../../../services/genai-apps.md#defense-in-depth)と[プロンプトのリスク](../../../../services/ai-fundamentals.md#prompt-engineering): 攻撃の種類と対策を整理します。
2. [エージェントの保護](../../../../services/ai.md#agent-security): ツールの悪用への対策を確認します。
3. [Guardrails のフィルター](../../../../services/ai.md#guardrail-filters): 機能と要件を対応させます。
4. [層の選び方](../../../../services/genai-apps.md#guardrail-tiers)と[ストリーミングでの動作](../../../../services/genai-apps.md#guardrail-streaming): 日本語とマスクの条件を覚えます。
5. [コンテキストグラウンディング](../../../../services/genai-apps.md#contextual-grounding)と[組織での強制](../../../../services/genai-apps.md#guardrail-org-enforcement): 残りの機能を確認します。

## こう問われたらこう考える {#decisions}

| 要件 | Guardrails の機能 |
|---|---|
| 有害な内容を止める | コンテンツフィルター |
| 話題を禁止する | 拒否トピック |
| PII をマスクする | 機密情報フィルターの `ANONYMIZE` |
| 攻撃を防ぐ | プロンプト攻撃フィルター |
| 参照元に基づかない応答を止める | コンテキストグラウンディング |
| 規定と論理的に矛盾しないか検証する | Automated Reasoning |
| モデルを呼ばずに検査する | `ApplyGuardrail` |

## 引っかかりやすい点 {#traps}

- 日本語を扱うなら Standard 層です。Classic は英語、フランス語、スペイン語です。
- PII のマスクが必要なら、ストリーミングの非同期モードは避けます。
- プロンプトの注意書きだけでは、ツールの悪用を確実には防げません。AgentCore Policy や人の承認を使います。
- 本番では番号付きのバージョンを指定します。全アカウントに強制するなら Organizations の Bedrock ポリシーです。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [guardrails 問8](../../exercises/guardrails.md#q8) | 4.3.7 | RAG が読み込む外部の Web ページに、「以前の指示を無視せよ」という文が仕込まれていました。こ… |
| [guardrails 問9](../../exercises/guardrails.md#q9) | 4.3.7 | 既知の攻撃プロンプトに対する防御の効果を、継続して確認します。適切な方法はどれですか。 |
| [guardrails 問10](../../exercises/guardrails.md#q10) | 4.3.7 | エージェントが社内 API を呼びます。プロンプトインジェクションで高額な返金の API が呼ばれる… |
| [guardrails 問11](../../exercises/guardrails.md#q11) | 4.3.9 | 日本語の入出力を扱うガードレールを作ります。層の選択として正しいものはどれですか。 |
| [guardrails 問12](../../exercises/guardrails.md#q12) | 4.3.9 | 顧客対応の応答から PII をマスクし、ストリーミングで返します。ストリーミングの処理モードはどちら… |
| [guardrails 問13](../../exercises/guardrails.md#q13) | 4.3.9 | 投資の助言を禁止する生成 AI アプリです。さらに、参照文書に基づかない応答を止めます。Guardr… |

<!-- questions:end -->
