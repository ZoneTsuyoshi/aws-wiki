# 分野2: AgentCore とエージェント

エージェントの実行基盤、記憶、ツール連携、安全な制御を扱います。モデルの判断に頼らない部分をどこに置くかが問われます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.1.1](../../domain2.md#skill-2-1-1) | 記憶と状態を持つ自律システム |
| [2.1.3](../../domain2.md#skill-2-1-3) | 安全に制御されたワークフロー |
| [2.1.6](../../domain2.md#skill-2-1-6) | 信頼できるツール連携 |
| [2.1.7](../../domain2.md#skill-2-1-7) | モデルの拡張の枠組み |

## 学習の順番 {#study-order}

1. [AgentCore のアーキテクチャ](../../../../services/genai-apps.md#agentcore)と [Runtime の選び方](../../../../services/genai-apps.md#agentcore-runtime): 層の役割と Harness、Runtime の違いを確認します。
2. [セッションの分離](../../../../services/ai.md#session-isolation)と [Memory の設計](../../../../services/genai-apps.md#agentcore-memory): 揮発するものと残すものを分けます。
3. [マルチエージェント](../../../../services/genai-apps.md#multi-agent): 手法の違いと Strands の Hooks を押さえます。
4. [Policy](../../../../services/genai-apps.md#agentcore-policy)と[ツール利用の認可](../../../../services/ai.md#tool-authorization): 実行の時点で止める方法と迂回の防止を理解します。
5. [MCP](../../../../services/genai-apps.md#mcp)と [Gateway](../../../../services/genai-apps.md#agentcore-gateway): サーバーの置き場所を選べるようにします。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| Runtime の microVM | 最大 8 時間、アイドル既定 15 分 | データは既定で揮発 |
| セッション ID | 33 文字以上 | 利用者との対応はバックエンドで |
| 待ち受け | HTTP 8080、MCP 8000、A2A 9000 | MCP のパスは `/mcp` |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 確実に金額で止める | AgentCore Policy。Gateway の迂回を禁止する |
| 好みをセッションをまたいで残す | 長期記憶。`actorId` を利用者ごとに |
| 上位が全体を統制する | Agents as Tools |
| 別の基盤のエージェントをつなぐ | A2A |
| 軽いステートレスのツール | Lambda の MCP サーバー |
| 長い処理や状態を持つツール | ECS / Fargate |
| 既存の API を束ねる | AgentCore Gateway |

## 引っかかりやすい点 {#traps}

- Policy は Gateway を通らない呼び出しに効きません。
- `guardrailConfig` は `toolUse.input` と `toolResult` を評価しません。
- 利用者が送った `toolUse` ブロックは取り除きます。
- CLI が作るロールは既定で全モデルの呼び出しを許します。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [agents 問1](../../exercises/agents.md#q1) | 2.1.1 | AgentCore Runtime で動く旅行手配のエージェントが、次回の来訪時に利用者の好みを忘れ… |
| [agents 問2](../../exercises/agents.md#q2) | 2.1.1 | 独自のフレームワークで書いた調査エージェントを動かします。セッションは利用者ごとに分離し、処理は長く… |
| [agents 問3](../../exercises/agents.md#q3) | 2.1.1 | 請求、技術、解約の 3 つの専門エージェントがあります。問い合わせの内容に応じて担当を振り分け、会話… |
| [agents 問4](../../exercises/agents.md#q4) | 2.1.1 | ある調査システムで、全体の計画役のエージェントが、検索担当と分析担当を呼び分け、全体の統制を 1 か… |
| [agents 問5](../../exercises/agents.md#q5) | 2.1.3 | 返金エージェントで、プロンプトに「1 万円を超える返金をしない」と書きましたが、攻撃的な入力で超える… |
| [agents 問6](../../exercises/agents.md#q6) | 2.1.3 | Step Functions で組んだエージェントが、ツールの結果が不足するとモデルが同じツールを呼… |
| [agents 問7](../../exercises/agents.md#q7) | 2.1.3 | 本番前のレビューで、Runtime のエージェントについて次の指摘がありました。CLI が作ったロー… |
| [agents 問8](../../exercises/agents.md#q8) | 2.1.6 | エージェントが注文の取り消しツールを呼びます。モデルの生成した引数に、他の利用者の注文番号が入ってい… |
| [agents 問9](../../exercises/agents.md#q9) | 2.1.6 | ツールが一時的なエラーのときに Lambda が例外を投げ、会話全体が失敗しています。また、似た名前… |
| [agents 問10](../../exercises/agents.md#q10) | 2.1.6 | Strands のエージェントで、ツールを実行する直前に引数を確認して危険な値を差し替え、実行後の結… |
| [agents 問11](../../exercises/agents.md#q11) | 2.1.7 | 社内で 2 種類の MCP サーバーを作ります。在庫照会は状態を持たない軽い処理で、呼び出しは不定期… |
| [agents 問12](../../exercises/agents.md#q12) | 2.1.7 | ある企業には、既存の社内 API と Lambda が数百あります。これらをエージェントから使えるよ… |
| [agents 問13](../../exercises/agents.md#q13) | 2.1.7 | 自作の MCP サーバーを AgentCore Runtime にデプロイしたところ、クライアントか… |

<!-- questions:end -->
