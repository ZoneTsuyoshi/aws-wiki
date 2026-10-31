# 分野3: エージェントの業務利用

通常のチャットとの違いと、業務で使うときの注意点を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.1.6](../../domain3.md#obj-3-1-6) | AI エージェントの役割と業務での使い方 |

## 学習の順番 {#study-order}

1. [エージェント](../../../../services/ai-fundamentals.md#agents): チャットとの違いの表を確認します。
2. [安全な自律動作](../../../../services/genai-apps.md#agent-safeguards): 自律動作のリスクと対策を押さえます。
3. [AgentCore のアーキテクチャ](../../../../services/genai-apps.md#agentcore)と[Bedrock Agents（Classic）](../../../../services/genai-apps.md#agents-classic): 新規のエージェントの基盤を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 複数の手順とツールの実行が必要 | エージェント |
| 手順の判断が不要な定型処理 | マネージド AI サービスや通常のプログラム |
| 送金や削除 | 実行前に人が承認する |
| 新規のエージェントの基盤 | AgentCore |

## 引っかかりやすい点 {#traps}

- Bedrock Agents は Agents Classic に改称され、新規顧客を受け付けていません。
- プロンプトでの禁止は確実な防御ではありません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [agents 問8](../../exercises/agents.md#q8) | 3.1.6 | 通常のチャットとエージェントの違いとして正しいものはどれですか。 |
| [agents 問9](../../exercises/agents.md#q9) | 3.1.6 | 業務での使い方として、エージェントが最も適しているものはどれですか。 |
| [agents 問10](../../exercises/agents.md#q10) | 3.1.6 | エージェントが送金を実行できるようにします。安全のための対策として適切なものはどれですか。 |
| [agents 問11](../../exercises/agents.md#q11) | 3.1.6 | 新規にエージェントを本番で動かします。2026 年 10 月時点の公式の案内に沿った基盤はどれですか… |

<!-- questions:end -->
