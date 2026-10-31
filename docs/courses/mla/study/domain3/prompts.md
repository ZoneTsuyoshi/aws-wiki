# 分野3: プロンプトとテスト

プロンプトをコードから分けて版を管理し、CI/CD で品質を確かめます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [3.3.7](../../domain3.md#skill-3-3-7) | プロンプトの管理 |
| [3.3.9](../../domain3.md#skill-3-3-9) | AI モデルのテストの枠組み |

## 学習の順番 {#study-order}

1. [プロンプトの管理](../../../../services/genai-apps.md#prompt-management): バリアント、バージョン、呼び出しの方法を覚えます。
2. [テスト](../../../../services/genai-apps.md#testing): テストの種類と品質ゲートを確認します。
3. [多層防御](../../../../services/genai-apps.md#defense-in-depth): 敵対的テストの位置づけを押さえます。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| デプロイなしでプロンプトを更新する | Prompt Management |
| 変更できない版を作る | バージョン |
| 別案と比べる | バリアント |
| 変更で悪化しないか調べる | ゴールデンデータセットの回帰テスト |
| 応答の意味の変化を調べる | 意味的類似度 |
| 攻撃への耐性を調べる | 敵対的テスト |

## 引っかかりやすい点 {#traps}

- `Converse` の `modelId` にプロンプトの ARN を、`promptVariables` に値を渡します。
- 品質ゲートの例は「`Faithfulness` が 0.8 未満なら昇格しない」です。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [prompts 問4](../../exercises/prompts.md#q4) | 3.3.7 | プロンプトの文言をコードから分け、デプロイなしで更新します。Prompt Management のプ… |
| [prompts 問5](../../exercises/prompts.md#q5) | 3.3.7 | 本番で使うプロンプトを変更できない形で固定し、CI/CD で昇格させます。正しい方法を選んでください… |
| [prompts 問6](../../exercises/prompts.md#q6) | 3.3.7 | 同じプロンプトの 2 つの案を、同じテスト値で比べて出力のよいほうを選びます。どの機能を使いますか。 |
| [prompts 問7](../../exercises/prompts.md#q7) | 3.3.9 | プロンプトやモデルの変更で品質が悪化しないよう、CI/CD で自動で確認します。適切なテストの組み合… |
| [prompts 問8](../../exercises/prompts.md#q8) | 3.3.9 | 新しいプロンプトの昇格の品質ゲートとして適切なものはどれですか。 |
| [prompts 問9](../../exercises/prompts.md#q9) | 3.3.9 | 同じ入力に対する新旧のモデルの応答を比べます。表現の違いは許容し、意味が大きく変わっていないかを調べ… |
| [prompts 問10](../../exercises/prompts.md#q10) | 3.3.9 | Guardrails の設定を変えたので、攻撃への耐性が下がっていないか確かめます。どのテストですか… |

<!-- questions:end -->
