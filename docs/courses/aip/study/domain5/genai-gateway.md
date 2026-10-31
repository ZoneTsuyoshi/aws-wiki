# 分野5: 品質保証とデプロイの検証

CI/CD の品質ゲートと、本番に出したあとの検証を扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [5.1.4](../../domain5.md#skill-5-1-4) | 品質保証のプロセス |
| [5.1.9](../../domain5.md#skill-5-1-9) | デプロイの検証 |

## 学習の順番 {#study-order}

1. [テスト](../../../../services/genai-apps.md#testing): テストの種類を整理します。
2. [CodeBuild](../../../../services/cicd.md#codebuild)と[ステージ条件](../../../../services/cicd.md#stage-conditions): パイプラインを止める方法を確認します。
3. [CloudWatch Synthetics](../../../../services/operations.md#synthetics): 内容の検証を押さえます。
4. [AppConfig のロールバック](../../../../services/secrets.md#appconfig-rollback)と[デプロイとテストの戦略](../../../../services/sagemaker.md#deployment-strategies): 自動で戻す方法を理解します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 本番の前に悪化を止める | CodeBuild でゴールデンデータセットを評価 |
| 変更がなくても品質を見る | EventBridge で定期の評価 |
| 応答の内容を定期的に確かめる | Synthetics のカナリア |
| 意味のドリフト | 応答の埋め込みを前の版と比べる |
| 応答を見せずに本番に近い検証 | シャドウテスト |

## 引っかかりやすい点 {#traps}

- モデルを変えなくても、文書や質問の変化で品質は変わります。
- HTTP の死活監視だけでは品質の低下は分かりません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [genai-gateway 問8](../../exercises/genai-gateway.md#q8) | 5.1.4 | 新しいプロンプトを本番へ出す前に、品質の悪化を自動で止めたいと考えています。本番の利用者には影響させ… |
| [genai-gateway 問9](../../exercises/genai-gateway.md#q9) | 5.1.4 | プロンプトとモデルは半年間変えていないのに、回答の品質が下がったと報告がありました。パイプラインの回… |
| [genai-gateway 問10](../../exercises/genai-gateway.md#q10) | 5.1.4 | チームがゴールデンデータセットを作ります。CI の回帰テストに使い、本番の変化も検出したいと考えてい… |
| [genai-gateway 問11](../../exercises/genai-gateway.md#q11) | 5.1.9 | チャットのデプロイのあと、5xx は増えていませんが、回答の傾向が変わったと報告がありました。今後は… |
| [genai-gateway 問12](../../exercises/genai-gateway.md#q12) | 5.1.9 | AppConfig で新しいモデルに段階的に切り替えます。切り替えの途中で品質が落ちたら自動で戻した… |
| [genai-gateway 問13](../../exercises/genai-gateway.md#q13) | 5.1.9 | SageMaker AI の新しいモデルのハルシネーション率と一貫性を、本番のリクエストに近い形で確… |

<!-- questions:end -->
