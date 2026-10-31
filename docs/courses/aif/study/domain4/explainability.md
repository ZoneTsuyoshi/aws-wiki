# 分野4: 透明性と説明可能性

透明性と説明可能性の違い、見分けるツール、トレードオフを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.2.1](../../domain4.md#obj-4-2-1) | 透明で説明可能なモデルとそうでないモデルの違い |
| [4.2.2](../../domain4.md#obj-4-2-2) | 透明で説明可能なモデルを見分けるツール |
| [4.2.3](../../domain4.md#obj-4-2-3) | 安全性と透明性のトレードオフ |
| [4.2.4](../../domain4.md#obj-4-2-4) | 説明可能な AI の人間中心の設計 |

## 学習の順番 {#study-order}

1. [説明可能性と透明性](../../../../services/ai-fundamentals.md#explainability): 区分、ツール、トレードオフ、人間中心の設計を順に読みます。
2. [Model Cards](../../../../services/sagemaker.md#model-cards): 何を記録する機能かを押さえます。
3. [人による監督](../../../../services/ai-fundamentals.md#human-oversight): 人が判断すべき場面を確認します。
4. [利用者からの評価](../../../../services/genai-apps.md#user-feedback)と[透明性と公平性](../../../../services/genai-apps.md#transparency-fairness): 評価の仕組みと AI の使用の表示を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 判断を追いたい | 線形回帰、決定木 |
| 用途、学習データ、評価、リスクの記録 | SageMaker Model Cards |
| AWS の AI サービスの用途と制約 | AI サービスカード |
| 特徴量と予測の関係 | SHAP、部分依存プロット |
| 説明が必須で精度の差が少ない | 解釈しやすいモデル |
| 安全策の詳細を公開するか | 公開しすぎると回避方法を教える |
| 誤りを報告させる | 評価ボタンなどのフィードバックの仕組み |

## 引っかかりやすい点 {#traps}

- オープンソースでも、学習データまで公開されているとは限りません。
- 透明性は仕組みや限界の開示で、説明可能性は個々の出力の理由の理解です。
- CloudTrail は API の記録です。モデルの用途やリスクの説明にはなりません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [explainability 問1](../../exercises/explainability.md#q1) | 4.2.1 | 判断の過程を追いやすいモデルの例はどれですか。 |
| [explainability 問2](../../exercises/explainability.md#q2) | 4.2.1 | 透明性と説明可能性の違いとして正しいものはどれですか。 |
| [explainability 問3](../../exercises/explainability.md#q3) | 4.2.1 | 深層学習のようなブラックボックスのモデルと、解釈しやすいモデルを比べた説明として正しいものはどれです… |
| [explainability 問4](../../exercises/explainability.md#q4) | 4.2.1 | 判断の理由を説明できないモデルを使う場合に、高まるリスクを選んでください。（2つ選択） |
| [explainability 問5](../../exercises/explainability.md#q5) | 4.2.2 | 監査に備えて、社内のモデルの用途、学習データ、評価結果、リスクを 1 か所に記録します。適切な機能は… |
| [explainability 問6](../../exercises/explainability.md#q6) | 4.2.2 | AWS の AI サービスの用途と制約を説明する資料はどれですか。 |
| [explainability 問7](../../exercises/explainability.md#q7) | 4.2.2 | オープンソースのモデルを透明性の観点で確認するときの説明として正しいものはどれですか。 |
| [explainability 問8](../../exercises/explainability.md#q8) | 4.2.2 | 特徴量と予測の関係を調べるための手法を選んでください。（2つ選択） |
| [explainability 問9](../../exercises/explainability.md#q9) | 4.2.3 | 病院が診断の補助モデルを選びます。候補 A は精度が少し高いものの理由が分かりません。候補 B は精… |
| [explainability 問10](../../exercises/explainability.md#q10) | 4.2.3 | 自社のチャットボットの安全策の詳細を公開すべきかを検討しています。トレードオフの説明として正しいもの… |
| [explainability 問11](../../exercises/explainability.md#q11) | 4.2.3 | 解釈しやすさと性能のどちらを優先するかを決める基準として適切なものはどれですか。 |
| [explainability 問12](../../exercises/explainability.md#q12) | 4.2.4 | 回答ごとに評価ボタンを付け、誤りを報告できるようにしました。この設計の原則はどれですか。 |
| [explainability 問13](../../exercises/explainability.md#q13) | 4.2.4 | 画面に「AI の回答です」と表示し、回答の根拠となる文書へのリンクも示しました。この設計の原則はどれ… |
| [explainability 問14](../../exercises/explainability.md#q14) | 4.2.4 | 融資の否決を AI が提案します。人間中心の設計として適切なものはどれですか。 |

<!-- questions:end -->
