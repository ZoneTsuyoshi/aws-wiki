# 分野2: トラブルシューティングの効率化

生成 AI の問題を、ログ、トレース、AI の分析で素早く調べます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.5.6](../../domain2.md#skill-2-5-6) | トラブルシューティングの効率化 |

## 学習の順番 {#study-order}

1. [モデル呼び出しログ](../../../../services/ai.md#invocation-logging)と [Logs Insights](../../../../services/observability.md#logs-insights): 本文の分析の方法を確認します。
2. [X-Ray](../../../../services/observability.md#xray)と [CloudWatch の生成 AI オブザーバビリティ](../../../../services/genai-apps.md#genai-observability): 流れの追い方を押さえます。
3. [エラー分析](../../../../services/ai.md#ai-troubleshooting): AI ツールでの調査を理解します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| プロンプトと応答を分析する | 呼び出しログと Logs Insights |
| サービス間の遅延 | X-Ray |
| 第三者のモデルも含めて追う | 生成 AI オブザーバビリティと ADOT SDK |

## 引っかかりやすい点 {#traps}

- 呼び出しログは既定で無効で、さかのぼって記録されません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [observability 問1](../../exercises/observability.md#q1) | 2.5.6 | 本番で一部の回答が崩れていると報告があり、過去 3 日のプロンプトと応答を調べようとしたところ、呼び… |
| [observability 問2](../../exercises/observability.md#q2) | 2.5.6 | Bedrock の API のエラーのログが大量にあり、開発チームは生成 AI 特有のエラーの傾向と… |
| [observability 問3](../../exercises/observability.md#q3) | 2.5.6 | エージェントの一部のリクエストが遅いと報告されました。原因が API Gateway、Lambda、… |

<!-- questions:end -->
