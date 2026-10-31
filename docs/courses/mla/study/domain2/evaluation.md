# 分野2: モデルと AI の評価

実験の記録、説明、指標の計算を問います。生成 AI では自動の指標、人の評価、LLM の採点を組み合わせます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.3.1](../../domain2.md#skill-2-3-1) | 再現可能な実験 |
| [2.3.4](../../domain2.md#skill-2-3-4) | モデルの出力の説明 |
| [2.3.6](../../domain2.md#skill-2-3-6) | 従来の ML と生成 AI の評価手法 |
| [2.3.7](../../domain2.md#skill-2-3-7) | 人による評価の組み込み |
| [2.3.8](../../domain2.md#skill-2-3-8) | NLP の評価指標 |
| [2.3.9](../../domain2.md#skill-2-3-9) | AI の評価 |

## 学習の順番 {#study-order}

1. [MLflow](../../../../services/sagemaker.md#mlflow): 記録するものと再現の条件を押さえます。
2. [Clarify](../../../../services/sagemaker.md#clarify)、[説明可能性と透明性](../../../../services/ai-fundamentals.md#explainability)、[Model Cards](../../../../services/sagemaker.md#model-cards): 説明の手段を区別します。
3. [評価指標](../../../../services/ai-fundamentals.md#metrics)、[AUC](../../../../services/ai-fundamentals.md#auc)、[回帰の指標](../../../../services/ai-fundamentals.md#regression-metrics): 計算できるようにします。
4. [NLP の指標](../../../../services/ai-fundamentals.md#nlp-metrics): BLEU、ROUGE、BERTScore の違いを覚えます。
5. [Bedrock Evaluations](../../../../services/genai-apps.md#bedrock-evaluations)と[エージェントの評価](../../../../services/genai-apps.md#agent-evaluation): LLM の採点と指標を確認します。
6. [人による確認](../../../../services/genai-apps.md#human-in-the-loop)と[利用者からの評価](../../../../services/genai-apps.md#user-feedback): 人を組み込む方法を押さえます。

## 覚える値 {#values}

| 項目 | 値（TP 80、FN 20、FP 30、TN 870） | 判断のポイント |
|---|---|---|
| 精度 | 0.95 | クラスが均衡しているとき |
| 適合率 | 80 / 110 = 0.727 | 誤検知の損失が大きいとき |
| 再現率 | 80 / 100 = 0.80 | 見逃しの損失が大きいとき |
| F1 | 160 / 210 = 0.762 | 両方を見る |
| コサイン類似度 | (1, 0) と (1, 1) で 0.707 | 1 に近いほど似ている |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 融資の否決の理由を申込者ごとに示す | SHAP |
| 監査のためにモデルの用途とリスクを残す | Model Cards |
| 大きな誤差を強く罰する | RMSE |
| 言い換えも正しく評価する | BERTScore |
| 大量の応答を理由つきで採点する | LLM-as-a-judge |
| 信頼度が低い予測を人に回す（新規） | Step Functions の `waitForTaskToken` |
| 応答の偏りを見る | Stereotyping と、属性だけを変えた比較 |

## 引っかかりやすい点 {#traps}

- Clarify と A2I は新規顧客の受付を終了しています。代替を区別します。
- BLEU と ROUGE は語の一致を見るので、言い換えを低く評価します。
- MAE は外れ値に強く、RMSE は大きな誤差を強く罰します。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [evaluation 問1](../../exercises/evaluation.md#q1) | 2.3.1 | 従来の ML と FM の実験で、パラメータ、指標、成果物を記録して比較します。どのツールが適切です… |
| [evaluation 問2](../../exercises/evaluation.md#q2) | 2.3.1 | 半年前の実験の結果を再現します。記録が必要なものの組み合わせを選んでください。（2つ選択） |
| [evaluation 問3](../../exercises/evaluation.md#q3) | 2.3.1 | FM とプロンプトの組み合わせを、同じ評価データで比べて結果を残します。それぞれの役割の組み合わせと… |
| [evaluation 問4](../../exercises/evaluation.md#q4) | 2.3.4 | 融資の否決の理由を、申込者ごとに示します。アカウントでは SageMaker Clarify を使え… |
| [evaluation 問5](../../exercises/evaluation.md#q5) | 2.3.4 | 監査のために、モデルの用途、学習データ、評価結果、リスクをまとめて記録します。どの機能ですか。 |
| [evaluation 問6](../../exercises/evaluation.md#q6) | 2.3.4 | 生成 AI の回答の根拠を利用者に示します。適切な手段はどれですか。 |
| [evaluation 問7](../../exercises/evaluation.md#q7) | 2.3.6 | スパム検知の結果は TP 80、FN 20、FP 30、TN 870 です。適合率に最も近い値はどれ… |
| [evaluation 問8](../../exercises/evaluation.md#q8) | 2.3.6 | 病気の検査で、見逃しの損失が誤検知よりはるかに大きいです。重視する指標はどれですか。 |
| [evaluation 問9](../../exercises/evaluation.md#q9) | 2.3.6 | 配送時間の回帰モデルで、まれな大きな誤差を強く罰して評価します。どの指標を見ますか。 |
| [evaluation 問10](../../exercises/evaluation.md#q10) | 2.3.7 | FM の要約の品質を、人の評価者に採点してもらいます。Bedrock の機能はどれですか。 |
| [evaluation 問11](../../exercises/evaluation.md#q11) | 2.3.7 | 新規のシステムで、信頼度が 80% 未満の予測だけ担当者の確認に回します。A2I は新規に使えません… |
| [evaluation 問12](../../exercises/evaluation.md#q12) | 2.3.7 | 生成 AI の回答に対する利用者の「よい、悪い」の評価を集めて、改善に使います。適切な構成はどれです… |
| [evaluation 問13](../../exercises/evaluation.md#q13) | 2.3.8 | 機械翻訳のモデルを、正解の翻訳文との n-gram の一致で評価します。どの指標ですか。 |
| [evaluation 問14](../../exercises/evaluation.md#q14) | 2.3.8 | 要約モデルの ROUGE は低いのですが、人が読むと正確な言い換えです。評価に足す指標はどれですか。 |
| [evaluation 問15](../../exercises/evaluation.md#q15) | 2.3.8 | a = (1, 0)、b = (1, 1) のコサイン類似度はどれですか。 |
| [evaluation 問16](../../exercises/evaluation.md#q16) | 2.3.9 | 問い合わせの回答の品質を、大量に自動で採点し、理由も残します。人の評価者は使いません。どの方法ですか… |
| [evaluation 問17](../../exercises/evaluation.md#q17) | 2.3.9 | FM の応答の偏りを評価します。性別だけを変えたプロンプトの比較に加えて、Bedrock Evalu… |
| [evaluation 問18](../../exercises/evaluation.md#q18) | 2.3.9 | AgentCore Runtime のエージェントの品質を、実行のトレースから採点します。どの機能で… |

<!-- questions:end -->
