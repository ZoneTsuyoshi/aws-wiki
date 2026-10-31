# 分野2: GenAI ゲートウェイとモデルの振り分け

入口を集約して統制し、CI/CD で品質を守り、要件に応じてモデルへ振り分けます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.3.5](../../domain2.md#skill-2-3-5) | CI/CD と GenAI ゲートウェイ |
| [2.4.4](../../domain2.md#skill-2-4-4) | モデルの振り分け |

## 学習の順番 {#study-order}

1. [GenAI ゲートウェイと CI/CD](../../../../services/genai-apps.md#genai-gateway)と [Gateway](../../../../services/genai-apps.md#agentcore-gateway): 実装の選択肢を比べます。
2. [CodePipeline](../../../../services/cicd.md#codepipeline)と [CodeBuild](../../../../services/cicd.md#codebuild): 評価をパイプラインに入れる方法を確認します。
3. [動的なモデル切り替え](../../../../services/genai-apps.md#dynamic-model-selection): 振り分けの方式を整理します。
4. [マッピングテンプレート](../../../../services/api-gateway.md#mapping-templates)と [Choice などの状態](../../../../services/step-functions.md#state-types): 実装の手段を押さえます。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 運用を減らして入口を 1 つに | AgentCore Gateway |
| 細かく作り込む | API Gateway と Lambda |
| 呼び出し側の指定なしで安全策を | Organizations の Bedrock ポリシー |
| 内容で振り分ける | Step Functions で分類して Choice |
| パスやヘッダーで決まる | API Gateway のマッピングテンプレート |
| 同じ系統で費用と品質の均衡 | Intelligent Prompt Routing |
| 指標で切り替える | AppConfig と CloudWatch |

## 引っかかりやすい点 {#traps}

- ゲートウェイは迂回されると意味がありません。IAM で直接の呼び出しを制限します。
- Intelligent Prompt Routing は英語のプロンプトに最適化されています。
- CI/CD ではコードに加えて、プロンプト、設定、評価データも管理します。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [genai-gateway 問1](../../exercises/genai-gateway.md#q1) | 2.3.5 | 全社のアプリが FM、ツール、エージェントを呼ぶ入口を 1 つにして、認証と監視を集約したいと考えて… |
| [genai-gateway 問2](../../exercises/genai-gateway.md#q2) | 2.3.5 | 生成 AI アプリの CI/CD を作ります。コードの変更に加え、プロンプトやモデルの設定の変更でも… |
| [genai-gateway 問3](../../exercises/genai-gateway.md#q3) | 2.3.5 | GenAI ゲートウェイで Guardrails を適用していますが、一部のチームがゲートウェイを通… |
| [genai-gateway 問4](../../exercises/genai-gateway.md#q4) | 2.4.4 | 問い合わせを、法務、技術、一般に分類して、それぞれに最適なモデルと異なるプロンプトで処理します。モデ… |
| [genai-gateway 問5](../../exercises/genai-gateway.md#q5) | 2.4.4 | パートナーごとに使うモデルが契約で決まっており、API のパス（/partner-a、/partne… |
| [genai-gateway 問6](../../exercises/genai-gateway.md#q6) | 2.4.4 | 日本語中心のチャットの費用を下げるため、同じ提供者のモデルの間で Intelligent Promp… |
| [genai-gateway 問7](../../exercises/genai-gateway.md#q7) | 2.4.4 | 第一候補のモデルの遅延が悪化したときに、トラフィックの 50% を別のモデルへ自動で移します。切り替… |

<!-- questions:end -->
