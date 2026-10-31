# 分野3: FM の評価

評価の方法、指標の用途、RAG の結果の読み方を問います。計算の方法は問われません。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.4.1](../../domain3.md#obj-3-4-1) | FM の性能の評価方法 |
| [3.4.2](../../domain3.md#obj-3-4-2) | FM の性能の指標 |
| [3.4.4](../../domain3.md#obj-3-4-4) | FM を使うアプリの評価方法 |

## 学習の順番 {#study-order}

1. [Bedrock Evaluations](../../../../services/genai-apps.md#bedrock-evaluations): ジョブの種類と指標の区分を覚えます。
2. [NLP の指標](../../../../services/ai-fundamentals.md#nlp-metrics): 指標と用途の組み合わせを覚えます。計算例は読むだけで十分です。
3. [エージェントの評価](../../../../services/genai-apps.md#agent-evaluation)と[Evaluations と Optimization](../../../../services/genai-apps.md#agentcore-evaluations): エージェントの評価の観点を確認します。
4. [テスト](../../../../services/genai-apps.md#testing): アプリ全体のテストの考え方を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 文体のような主観的な品質 | 人による評価 |
| 共通の正解で客観的に比較する | ベンチマークデータセット |
| 別の LLM に採点させる | LLM-as-a-judge |
| 機械翻訳 | BLEU |
| 要約 | ROUGE |
| 言い換えを正しく評価する | BERTScore |
| ContextRelevance が低い | チャンク、埋め込み、検索を見直す |
| 取得はよいが Faithfulness が低い | プロンプトやモデルを見直す |
| エージェントの評価 | タスク完了率、ツールの選択、効率 |

## 引っかかりやすい点 {#traps}

- BLEU と ROUGE は語の一致を見るので、言い換えを低く評価します。
- モデル単体でなく、アプリ全体を評価します。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [evaluation 問1](../../exercises/evaluation.md#q1) | 3.4.1 | 広告の文案の「文体がブランドに合うか」を評価します。適切な方法はどれですか。 |
| [evaluation 問2](../../exercises/evaluation.md#q2) | 3.4.1 | 複数の FM を、正解つきの共通のデータで客観的に比較します。この方法はどれですか。 |
| [evaluation 問3](../../exercises/evaluation.md#q3) | 3.4.1 | Bedrock の評価で、別の LLM に応答を採点させ、説明も出させたいと考えています。適切なジョ… |
| [evaluation 問4](../../exercises/evaluation.md#q4) | 3.4.1 | Bedrock の評価で選べる方法を選んでください。（2つ選択） |
| [evaluation 問5](../../exercises/evaluation.md#q5) | 3.4.2 | 英日の機械翻訳の品質を、正解の訳文との語の並びの一致で測ります。代表的な指標はどれですか。 |
| [evaluation 問6](../../exercises/evaluation.md#q6) | 3.4.2 | ニュース記事の自動要約の品質を、正解の要約の語がどれだけ含まれるかで測ります。代表的な指標はどれです… |
| [evaluation 問7](../../exercises/evaluation.md#q7) | 3.4.2 | 語が違っても意味が同じ言い換えを、正しく評価したいと考えています。適切な指標はどれですか。 |
| [evaluation 問8](../../exercises/evaluation.md#q8) | 3.4.2 | 正解の文章がなく、応答の正確性や有害性を採点したいと考えています。適切な指標の種類はどれですか。 |
| [evaluation 問9](../../exercises/evaluation.md#q9) | 3.4.4 | RAG アプリの評価で、取得した文書の関連性は高いのに、回答が文書と異なることがあります。見直す部分… |
| [evaluation 問10](../../exercises/evaluation.md#q10) | 3.4.4 | RAG の評価で ContextRelevance が低い結果が出ました。原因の候補はどれですか。 |
| [evaluation 問11](../../exercises/evaluation.md#q11) | 3.4.4 | 返品を処理するエージェントを評価します。適切な観点を選んでください。（2つ選択） |
| [evaluation 問12](../../exercises/evaluation.md#q12) | 3.4.4 | 抽出、要約、翻訳を順に実行するワークフローの最終結果が悪くなりました。評価の進め方として適切なものは… |

<!-- questions:end -->
