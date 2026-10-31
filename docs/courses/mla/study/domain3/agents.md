# 分野3: エージェント

新規のエージェントは AgentCore で作ります。Harness と Runtime の選択、状態の持ち方、本番の安全な更新を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.1.6](../../domain3.md#skill-3-1-6) | エージェントのデプロイと設定 |
| [3.2.9](../../domain3.md#skill-3-2-9) | エージェントの状態管理 |
| [3.2.11](../../domain3.md#skill-3-2-11) | エージェントのワークフローの基盤 |
| [3.3.8](../../domain3.md#skill-3-3-8) | エージェントのデプロイパイプラインとバージョン管理 |

## 学習の順番 {#study-order}

1. [AgentCore](../../../../services/genai-apps.md#agentcore): 構成要素の役割をつかみます。
2. [Runtime の選び方](../../../../services/genai-apps.md#agentcore-runtime): microVM と Instances、ポートを覚えます。
3. [MCP](../../../../services/genai-apps.md#mcp)と[マルチエージェント](../../../../services/genai-apps.md#multi-agent): MCP と A2A を区別します。
4. [Memory の設計](../../../../services/genai-apps.md#agentcore-memory)と [AgentCore の構成要素と設定](../../../../services/ai.md#agentcore-components): 短期と長期、`actorId` を押さえます。
5. [安全な自律動作](../../../../services/genai-apps.md#agent-safeguards)と[構造のパターン](../../../../services/genai-apps.md#workflow-patterns): 暴走への備えを確認します。
6. [Evaluations と Optimization](../../../../services/genai-apps.md#agentcore-evaluations): パイプラインの評価の段階を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| 既定のポート | HTTP 8080、MCP 8000、A2A 9000 | 設定で変更できる |
| アイドルの既定 | 900 秒 | `idleRuntimeSessionTimeout` で延ばす |
| セッションの上限 | microVM 8 時間、Instances 14 日 | 複数日なら Instances |
| Docker イメージ | 2 GB まで | |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| モデル、プロンプト、ツールを指定するだけ | AgentCore Harness |
| 独自のフレームワークやコード | AgentCore Runtime |
| 既存の API や Lambda をツールにする | AgentCore Gateway |
| ツールの呼び出しを決定的に認可する | AgentCore Policy |
| 本番を評価の後で切り替える | 独自のエンドポイントと `UpdateAgentRuntimeEndpoint` |

## 引っかかりやすい点 {#traps}

- Bedrock Agents は Agents Classic に改称され、新規の受付を終了しました。
- `DEFAULT` は常に最新のバージョンを指します。本番には独自のエンドポイントを使います。
- `actorId` を利用者ごとに分けないと、別の利用者の記憶が混ざります。
- Runtime は VPC に接続できますが、パブリックサブネットに置いてもインターネットには出られません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [agents 問1](../../exercises/agents.md#q1) | 3.1.6 | 2026 年後半に新しいエージェントを作ります。LangGraph の独自コードをそのまま動かし、セ… |
| [agents 問2](../../exercises/agents.md#q2) | 3.1.6 | 既存の社内 REST API と Lambda を、コードを書き換えずにエージェントのツールとして公… |
| [agents 問3](../../exercises/agents.md#q3) | 3.1.6 | AgentCore Runtime で動かすサーバーの種類と、既定の提供ポートの組み合わせとして正し… |
| [agents 問4](../../exercises/agents.md#q4) | 3.2.9 | 同じ Runtime のエージェントを複数の利用者が使います。AgentCore Memory で別… |
| [agents 問5](../../exercises/agents.md#q5) | 3.2.9 | 問い合わせのエージェントで、30 分ぶりの再開時に会話の文脈が失われます。Runtime のアイドル… |
| [agents 問6](../../exercises/agents.md#q6) | 3.2.9 | 既存の基盤を使ってエージェントの状態を自前で管理します。会話履歴と長期の知識の置き場所の組み合わせは… |
| [agents 問7](../../exercises/agents.md#q7) | 3.2.11 | エージェントの処理が数日続きます。AgentCore Runtime の実行の種類はどれですか。 |
| [agents 問8](../../exercises/agents.md#q8) | 3.2.11 | エージェントのツールのうち、処理が短くステートレスなものと、長時間で複雑なものを配置します。組み合わ… |
| [agents 問9](../../exercises/agents.md#q9) | 3.2.11 | 自律動作するエージェントの暴走に備えます。適切な対策の組み合わせを選んでください。（3つ選択） |
| [agents 問10](../../exercises/agents.md#q10) | 3.3.8 | AgentCore Runtime のエージェントを更新すると、本番が検証前のコードに切り替わります… |
| [agents 問11](../../exercises/agents.md#q11) | 3.3.8 | エージェントの本番の更新に問題が見つかりました。Runtime のバージョン管理を使って素早く戻す方… |
| [agents 問12](../../exercises/agents.md#q12) | 3.3.8 | エージェントのデプロイパイプラインの順序として適切なものはどれですか。 |

<!-- questions:end -->
