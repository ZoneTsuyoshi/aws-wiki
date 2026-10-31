# 分野2: ワークフローとオーケストレーション

ReAct、複数のモデルの協調、人の承認を、どの実装で組むかを判断します。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.1.2](../../domain2.md#skill-2-1-2) | 構造化された推論で問題を解く |
| [2.1.4](../../domain2.md#skill-2-1-4) | 複数のモデルの協調 |
| [2.1.5](../../domain2.md#skill-2-1-5) | 人の専門知識を組み込む |
| [2.5.5](../../domain2.md#skill-2-5-5) | 高度な生成 AI アプリ |

## 学習の順番 {#study-order}

1. [構造のパターン](../../../../services/genai-apps.md#workflow-patterns): 6 つのパターンの違いを確認します。
2. [ツール利用の流れ](../../../../services/ai.md#tool-use-flow): `stopReason` での分岐を理解します。
3. [Standard と Express](../../../../services/step-functions.md#standard-express)、[人の承認](../../../../services/step-functions.md#human-approval)、[タイムアウト](../../../../services/step-functions.md#timeouts): 待機の条件を押さえます。
4. [人による確認](../../../../services/genai-apps.md#human-in-the-loop)と [A2I](../../../../services/ai-managed-services.md#a2i): しきい値で回す設計と A2I の状況を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| Express の実行 | 最大 5 分 | `.waitForTaskToken` は不可 |
| Standard の実行 | 最大 1 年 | タイムアウトを必ず設定する |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 監査が厳しい ReAct | Step Functions の Standard |
| 手元の情報で計算 | Chain-of-thought |
| 外部の情報を調べながら答える | ReAct |
| 誤りのコストが高い | アンサンブル。費用と遅延は増える |
| 単純な処理と難しい推論が混ざる | モデルの分担 |
| 決まった手順でプロンプトの担当者が調整 | Flows |
| 手順を事前に決められない | Strands Agents |

## 引っかかりやすい点 {#traps}

- アンサンブルの遅延は最も遅いモデルに引きずられます。
- タイムアウトがないと、承認者が応答しないまま止まり続けます。
- A2I は新規顧客を受け付けていません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [workflows 問1](../../exercises/workflows.md#q1) | 2.1.2 | 監査の要件が厳しいエージェントを ReAct で作ります。各手順の入出力が実行履歴に残り、ツールの呼… |
| [workflows 問2](../../exercises/workflows.md#q2) | 2.1.2 | Step Functions で ReAct のループを組みます。Bedrock の応答を受けたあと… |
| [workflows 問3](../../exercises/workflows.md#q3) | 2.1.2 | 2 つの問題があります。(a) 手元のデータだけで答えられる複雑な料金の計算で、途中の式が崩れる。(… |
| [workflows 問4](../../exercises/workflows.md#q4) | 2.1.4 | 与信の判断の説明文を生成します。誤りのコストが非常に高く、処理は 1 日に数百件で、数分の遅延と費用… |
| [workflows 問5](../../exercises/workflows.md#q5) | 2.1.4 | 文書処理で、言語の判定、項目の抽出、法的なリスクの推論を行います。判定と抽出は単純で、件数も多いです… |
| [workflows 問6](../../exercises/workflows.md#q6) | 2.1.4 | 3 つの FM に同じ質問を並列で投げ、結果を統合するワークフローを作りました。ピーク時に応答が遅い… |
| [workflows 問7](../../exercises/workflows.md#q7) | 2.1.5 | エージェントが 100 万円を超える支払いを行う前に、経理担当の承認を得ます。承認者が休みの場合は最… |
| [workflows 問8](../../exercises/workflows.md#q8) | 2.1.5 | 承認の画面を社内ポータルに作ります。承認者がボタンを押した結果を、待機中のワークフローに返す必要があ… |
| [workflows 問9](../../exercises/workflows.md#q9) | 2.1.5 | 契約書の要約で、グラウンディングのスコアが低い回答だけを専門家が確認します。全件の確認は費用が合いま… |
| [workflows 問10](../../exercises/workflows.md#q10) | 2.5.5 | 次の 3 つのアプリの実装方式を選びます。(a) 抽出、要約、翻訳の決まった 3 手順で、プロンプト… |
| [workflows 問11](../../exercises/workflows.md#q11) | 2.5.5 | 請求、技術、解約の専門エージェントがすでにあり、利用者の問い合わせの窓口を 1 つにしたいと考えてい… |
| [workflows 問12](../../exercises/workflows.md#q12) | 2.5.5 | 自律的なエージェントで問い合わせの全手順を処理したところ、費用が読めず、同じ問い合わせでも手順が毎回… |

<!-- questions:end -->
