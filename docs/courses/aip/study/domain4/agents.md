# 分野4: ツールの性能の監視

エージェントのツールの呼び出しを指標にして、ループや協調の問題を捉えます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.3.4](../../domain4.md#skill-4-3-4) | ツールの性能の枠組み |

## 学習の順番 {#study-order}

1. [見るべき指標](../../../../services/genai-apps.md#genai-metrics): ツールとエージェントの指標を確認します。
2. [CloudWatch の生成 AI オブザーバビリティ](../../../../services/genai-apps.md#genai-observability): AgentCore Observability の位置づけを押さえます。
3. [EMF](../../../../services/observability.md#emf): カスタムメトリクスの送り方を理解します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| ツールごとの指標を軽く送る | Embedded Metric Format |
| 同じツールの呼び出しが急増 | ループを疑い、トレースで確認 |
| 引き継ぎの原因を探す | スパンの親子関係 |

## 引っかかりやすい点 {#traps}

- エラーが増えなくてもループは起きます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [agents 問14](../../exercises/agents.md#q14) | 4.3.4 | Lambda のツールごとの呼び出し回数、失敗率、遅延を CloudWatch の指標にします。呼び… |
| [agents 問15](../../exercises/agents.md#q15) | 4.3.4 | エージェントの同じツールの呼び出しが、ある日から平常の 10 倍に増えました。エラーは増えていません… |
| [agents 問16](../../exercises/agents.md#q16) | 4.3.4 | マルチエージェントのシステムで、処理が遅い原因がどのエージェントの引き継ぎにあるのかが分かりません。… |

<!-- questions:end -->
