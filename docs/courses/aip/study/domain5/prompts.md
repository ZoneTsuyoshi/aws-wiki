# 分野5: プロンプトの問題と保守

悪化したときの戻し方と、体系的な改善、再発の防止を扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [5.2.3](../../domain5.md#skill-5-2-3) | プロンプトの問題 |
| [5.2.5](../../domain5.md#skill-5-2-5) | プロンプトの保守の問題 |

## 学習の順番 {#study-order}

1. [プロンプトの管理](../../../../services/genai-apps.md#prompt-management): バージョンと比較を確認します。
2. [トラブルシューティング](../../../../services/genai-apps.md#troubleshooting): 症状と対応の表を押さえます。
3. [モデル呼び出しログ](../../../../services/ai.md#invocation-logging)と [X-Ray](../../../../services/observability.md#xray): 実際のプロンプトと流れの見方を理解します。
4. [構造化出力](../../../../services/genai-apps.md#structured-output): 形式の不一致の対策を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 公開直後に悪化 | まず前のバージョンに戻す |
| どの変更が効いたか | 1 回に 1 つだけ変えて測る |
| 指示の取り違え | 呼び出しログで実際のプロンプトを確認 |
| 同じ不具合が繰り返す | 失敗の例を評価データに加える |

## 引っかかりやすい点 {#traps}

- CloudTrail にプロンプトの本文は残りません。
- 複数を同時に変えると、何が効いたか分かりません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [prompts 問19](../../exercises/prompts.md#q19) | 5.2.3 | プロンプトの新しいバージョンを公開した直後から回答の品質が下がりました。利用者への影響が続いています… |
| [prompts 問20](../../exercises/prompts.md#q20) | 5.2.3 | プロンプトで「指示の順序」「出力の形式」「例の数」を同時に変えたところ、品質が上がりました。ところが… |
| [prompts 問21](../../exercises/prompts.md#q21) | 5.2.3 | プロンプトの案 A と案 B で、回答の正確さに差があるかを本番の前に確かめたいと考えています。利用… |
| [prompts 問22](../../exercises/prompts.md#q22) | 5.2.5 | テンプレートの変更後、モデルが利用者の入力の一部を指示として扱うようになりました。テンプレートの差分… |
| [prompts 問23](../../exercises/prompts.md#q23) | 5.2.5 | API Gateway、Lambda、Bedrock、Knowledge Bases をつないだアプ… |
| [prompts 問24](../../exercises/prompts.md#q24) | 5.2.5 | 同じ種類の形式の誤りが、プロンプトを直すたびに別の形でまた現れます。担当者は、見つけるたびに直すだけ… |

<!-- questions:end -->
