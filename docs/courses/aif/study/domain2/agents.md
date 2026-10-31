# 分野2: エージェント

エージェントの基本概念と、MCP、A2A、マルチエージェントの区別を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.1.6](../../domain2.md#obj-2-1-6) | エージェント型 AI の基本概念 |
| [2.3.1](../../domain2.md#obj-2-3-1) | 生成 AI アプリのサービスと機能 |

## 学習の順番 {#study-order}

1. [エージェント](../../../../services/ai-fundamentals.md#agents): 要素とチャットとの違いを表で確認します。
2. [構造のパターン](../../../../services/genai-apps.md#workflow-patterns): ルーティングや並列化などの形を見分けます。
3. [マルチエージェント](../../../../services/genai-apps.md#multi-agent): Agents as Tools、Swarm、Graph、A2A の違いと Strands の位置づけを押さえます。
4. [MCP](../../../../services/genai-apps.md#mcp): MCP が何と何をつなぐかを理解します。
5. [Memory の設計](../../../../services/genai-apps.md#agentcore-memory): 短期と長期の記憶を区別します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 複数のアプリで同じツールを再利用する | MCP |
| 別々の基盤のエージェントが通信する | A2A |
| 上位が他のエージェントをツールとして呼ぶ | Agents as Tools |
| エージェント同士が仕事を引き継ぐ | Swarm |
| 開発者が定義した流れ図に沿って進める | Graph |
| 今の会話を保持する | 短期の記憶 |
| 好みや過去の事実を保持する | 長期の記憶 |
| コードでエージェントを書く | Strands Agents |

## 引っかかりやすい点 {#traps}

- MCP はエージェントとツールの接続で、A2A はエージェント同士の通信です。
- Strands はエージェントを書く道具で、AgentCore は動かす基盤です。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [agents 問1](../../exercises/agents.md#q1) | 2.1.6 | エージェントの基本的な動きとして正しいものはどれですか。 |
| [agents 問2](../../exercises/agents.md#q2) | 2.1.6 | 複数のエージェントから、同じ社内データベース用のツールを標準の方法で使いたいと考えています。適切な仕… |
| [agents 問3](../../exercises/agents.md#q3) | 2.1.6 | 別々の基盤で作られた 2 つのエージェントに、標準のプロトコルで通信させたいと考えています。適切なも… |
| [agents 問4](../../exercises/agents.md#q4) | 2.1.6 | 上位のエージェントが、調査担当や計算担当のエージェントをツールとして呼び出す構成はどれですか。 |
| [agents 問5](../../exercises/agents.md#q5) | 2.1.6 | 複数のエージェントが、中央の指揮役なしで互いに仕事を引き継いでいく構成はどれですか。 |
| [agents 問6](../../exercises/agents.md#q6) | 2.1.6 | エージェントの記憶の説明として正しいものを選んでください。（2つ選択） |
| [agents 問7](../../exercises/agents.md#q7) | 2.1.6 | 「問い合わせを受けて請求か技術かに分類し、専門の処理に送る」というワークフローのパターンはどれですか… |
| [agents 問12](../../exercises/agents.md#q12) | 2.3.1 | コードでエージェントの動きを書くオープンソースの SDK と、それを本番で動かす基盤の組み合わせはど… |

<!-- questions:end -->
