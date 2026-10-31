# 分野5: エージェントの評価

最終回答だけでなく、手順とツールの使い方も測ります。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [5.1.7](../../domain5.md#skill-5-1-7) | エージェントの性能の枠組み |

## 学習の順番 {#study-order}

1. [エージェントの評価](../../../../services/genai-apps.md#agent-evaluation): 指標の一覧を確認します。
2. [Evaluations と Optimization](../../../../services/genai-apps.md#agentcore-evaluations): AgentCore Evaluations の位置づけを押さえます。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 回答はよいが費用が高い | トレースでステップ数とトークンを測る |
| バージョンごとに継続して採点する | AgentCore Evaluations |

## 引っかかりやすい点 {#traps}

- 最終回答だけを見ると、無駄な手順を見逃します。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [agents 問17](../../exercises/agents.md#q17) | 5.1.7 | カスタマーサポートのエージェントは最終回答の評価が高いものの、費用が想定の 5 倍です。チームは最終… |
| [agents 問18](../../exercises/agents.md#q18) | 5.1.7 | Strands で作ったエージェントの品質を、新しいバージョンごとに継続して確かめます。独自の評価基… |
| [agents 問19](../../exercises/agents.md#q19) | 5.1.7 | 注文処理のエージェントを評価する指標を決めます。経営層は「仕事を完了できたか」、開発チームは「正しい… |

<!-- questions:end -->
