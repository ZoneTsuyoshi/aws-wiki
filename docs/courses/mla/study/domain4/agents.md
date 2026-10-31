# 分野4: エージェントの監視

エージェントの症状から調べるものを選び、依頼あたりの資源の消費を監視します。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.1.5](../../domain4.md#skill-4-1-5) | エージェントの性能と連携の監視 |
| [4.2.8](../../domain4.md#skill-4-2-8) | エージェントのリソース消費の監視 |

## 学習の順番 {#study-order}

1. [ストリーミング](../../../../services/ai.md#streaming): イベントの順序と途中の失敗を確認します。
2. [トラブルシューティング](../../../../services/genai-apps.md#troubleshooting): 症状と調べるものを結びつけます。
3. [安全な自律動作](../../../../services/genai-apps.md#agent-safeguards): 上限と予算を押さえます。
4. [見るべき指標](../../../../services/genai-apps.md#genai-metrics)と [AgentCore の構成要素と設定](../../../../services/ai.md#agentcore-components): 消費の指標と資源の値を覚えます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| Runtime の 1 セッション | 2 vCPU、8 GB | 変更できない上限 |

## こう問われたらこう考える {#decisions}

| 症状 | 調べるもの |
|---|---|
| 応答が途中で切れる | `stopReason` が `max_tokens` |
| ストリームが途中で止まる | `modelStreamErrorException` などのイベント |
| ツールが呼ばれない | ツールの説明、`toolChoice` |
| 同じ操作を繰り返す | トレース、繰り返し回数 |
| 依頼あたりのコストが高い | トークンの累計を記録し、予算で止める |

## 引っかかりやすい点 {#traps}

- ストリーミングは HTTP 200 を受け取った後でも失敗します。
- トークン数は最後の `metadata` にしか来ないので、途中で切れると使用量を取得できません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [agents 問13](../../exercises/agents.md#q13) | 4.1.5 | エージェントの応答が文の途中で切れます。stopReason は max_tokens です。適切な… |
| [agents 問14](../../exercises/agents.md#q14) | 4.1.5 | ストリーミングのエージェントで、HTTP 200 を受け取ったあとに応答が止まることがあります。適切… |
| [agents 問15](../../exercises/agents.md#q15) | 4.1.5 | エージェントがあるツールだけ呼びません。ツールのエラーは出ていません。調べる項目はどれですか。 |
| [agents 問16](../../exercises/agents.md#q16) | 4.2.8 | エージェントは 1 依頼で何度もモデルとツールを呼びます。依頼あたりのコストの上限を守る実装はどれで… |
| [agents 問17](../../exercises/agents.md#q17) | 4.2.8 | エージェントの繰り返し回数とステップ数を依頼ごとに確認します。どの手段ですか。 |
| [agents 問18](../../exercises/agents.md#q18) | 4.2.8 | AgentCore Runtime の 1 セッションで使える資源を確認し、ツールごとの呼び出し回数… |

<!-- questions:end -->
