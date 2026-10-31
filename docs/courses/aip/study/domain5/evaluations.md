# 分野5: 評価と Bedrock Evaluations

指標の意味、評価の方式の使い分け、取得の品質のテストを扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [5.1.1](../../domain5.md#skill-5-1-1) | FM の出力の評価の枠組み |
| [5.1.2](../../domain5.md#skill-5-1-2) | 最適な構成を見つけるモデル評価 |
| [5.1.3](../../domain5.md#skill-5-1-3) | 利用者を中心にした評価 |
| [5.1.5](../../domain5.md#skill-5-1-5) | 多面的な評価 |
| [5.1.6](../../domain5.md#skill-5-1-6) | 取得の品質のテスト |

## 学習の順番 {#study-order}

1. [Bedrock Evaluations](../../../../services/genai-apps.md#bedrock-evaluations): ジョブの種類と指標を覚えます。
2. [NLP の指標](../../../../services/ai-fundamentals.md#nlp-metrics): BLEU と ROUGE の弱点を確認します。
3. [デプロイとテストの戦略](../../../../services/sagemaker.md#deployment-strategies)と[テスト](../../../../services/genai-apps.md#testing): 本番での比較の方法を整理します。
4. [利用者からの評価](../../../../services/genai-apps.md#user-feedback): 保存と偏りの扱いを押さえます。
5. [Knowledge Bases を呼ぶ](../../../../services/ai.md#knowledge-bases): `Retrieve` の単体テストを理解します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 利用者に影響なく比べる | Bedrock Evaluations、シャドウテスト |
| 事業成果を比べる | A/B テスト |
| 意味を採点して説明も得る | 判定モデル |
| 専門家が採点する | 人による評価のジョブ |
| ContextRelevance が低い | チャンク、埋め込み、検索 |
| ContextCoverage が低い | 取得件数、文書の有無 |
| 取得はよいが Faithfulness が低い | 生成を見直す |

## 引っかかりやすい点 {#traps}

- BLEU と ROUGE は言い換えを低く評価することがあります。
- 評価する人は偏ります。自動の評価と組み合わせます。
- Ground Truth は新規顧客を受け付けていません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [evaluations 問1](../../exercises/evaluations.md#q1) | 5.1.1 | 要約のモデルを BLEU で評価したところ、参照文と言い回しが違うだけの良い要約のスコアが低くなりま… |
| [evaluations 問2](../../exercises/evaluations.md#q2) | 5.1.1 | RAG の回答の評価基準を決めます。(a) 回答が質問に答えているか。(b) 取得した文書に沿ってい… |
| [evaluations 問3](../../exercises/evaluations.md#q3) | 5.1.1 | 社外向けの文面を生成するアプリで、内容は正しいのに「読みにくい」「文体が硬い」と苦情が出ています。内… |
| [evaluations 問4](../../exercises/evaluations.md#q4) | 5.1.2 | 新しいモデルの候補を選ぶ段階で、次の順に進めたいと考えています。(1) 利用者への影響なしに複数のモ… |
| [evaluations 問5](../../exercises/evaluations.md#q5) | 5.1.2 | モデル P は品質スコアが 0.90 で 1 件 1 円、モデル Q は 0.92 で 1 件 5 … |
| [evaluations 問6](../../exercises/evaluations.md#q6) | 5.1.2 | SageMaker AI のモデルの本番バリアントで、2 つの案に 90 対 10 でトラフィックを… |
| [evaluations 問7](../../exercises/evaluations.md#q7) | 5.1.3 | チャットの画面に評価のボタンを付けます。後から低評価の応答を調べ、改善に使います。サーバーレスで構築… |
| [evaluations 問8](../../exercises/evaluations.md#q8) | 5.1.3 | 医療の回答の品質を、社内の医師が採点します。新規の仕組みで、主観と専門性が重要です。自社の従業員だけ… |
| [evaluations 問9](../../exercises/evaluations.md#q9) | 5.1.3 | 評価のボタンの結果を見ると、低評価の割合が 40% ですが、評価を押した人は利用者の 2% だけです… |
| [evaluations 問10](../../exercises/evaluations.md#q10) | 5.1.5 | 1 万件の応答を毎週評価します。人の費用は 100 件分しかありません。意味の品質を広く測りつつ、重… |
| [evaluations 問11](../../exercises/evaluations.md#q11) | 5.1.5 | RAG の品質が低いという報告を受け、取得と生成のどちらが悪いのかを分けて知りたいと考えています。評… |
| [evaluations 問12](../../exercises/evaluations.md#q12) | 5.1.5 | 評価の方式を比べています。安く大量に測りたいが意味は捉えにくい方式、意味を採点して説明も返すが判定に… |
| [evaluations 問13](../../exercises/evaluations.md#q13) | 5.1.6 | RAG の評価で ContextRelevance は高いのに Faithfulness が低いです… |
| [evaluations 問14](../../exercises/evaluations.md#q14) | 5.1.6 | 取得のみの評価で、ContextCoverage が低く、ContextRelevance は高いで… |
| [evaluations 問15](../../exercises/evaluations.md#q15) | 5.1.6 | 検索の遅延のテストを追加します。生成の時間と分けて検索だけの遅延を測り、平均ではなく遅い場合を把握し… |
| [evaluations 問16](../../exercises/evaluations.md#q16) | 5.1.5, 5.1.6 | RAG の評価の設計を見直します。正解の文を含む評価データがあります。取得が必要な情報を十分に集めて… |

<!-- questions:end -->
