# 分野4: 監視と調査

遅延の内訳の切り分け、Bedrock の指標の意味、調査ツールの選択、ダッシュボードの設定を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.1.2](../../domain4.md#skill-4-1-2) | ワークフローの異常とエラーの検出 |
| [4.1.6](../../domain4.md#skill-4-1-6) | FM の性能の監視 |
| [4.2.2](../../domain4.md#skill-4-2-2) | 調査と分析のツール |
| [4.2.3](../../domain4.md#skill-4-2-3) | ダッシュボードの設定 |

## 学習の順番 {#study-order}

1. [SageMaker の CloudWatch メトリクス](../../../../services/sagemaker.md#cloudwatch-metrics): `ModelLatency` と `OverheadLatency` を区別します。
2. [異常検知](../../../../services/observability.md#anomaly-detection)と [Logs Insights](../../../../services/observability.md#logs-insights): 誤報の抑え方とログの検索を押さえます。
3. [Bedrock のメトリクス](../../../../services/ai.md#bedrock-metrics)と[モデル呼び出しログ](../../../../services/ai.md#invocation-logging): 指標の定義を覚えます。
4. [X-Ray](../../../../services/observability.md#xray)と [CloudTrail と CloudWatch](../../../../services/observability.md#cloudtrail-vs-cloudwatch): ツールの使い分けを確認します。
5. [ダッシュボード](../../../../services/observability.md#dashboards)と[ダッシュボードの設定](../../../../services/observability.md#dashboard-settings): 料金の注意を押さえます。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| `ModelLatency` が大きい | モデルやインスタンス |
| `OverheadLatency` が大きい | コールドスタートなどの基盤側 |
| 季節性のある指標のアラーム | CloudWatch の異常検知 |
| 最初の応答が遅い | `TimeToFirstToken` |
| スロットリングの確認 | `InvocationThrottles`、`EstimatedTPMQuotaUsage` |
| どこで遅いか | X-Ray |
| 誰が変更したか | CloudTrail |
| 経営層に事業の指標を見せる | Amazon Quick |

## 引っかかりやすい点 {#traps}

- `Invocations` にスロットリングされた分は含まれません。
- 呼び出しログは既定で無効です。
- DevOps Guru は 2026-10-29 で新規顧客の受付を終了しました。
- Logs Insights のウィジェットは更新のたびに料金がかかります。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [observability 問1](../../exercises/observability.md#q1) | 4.1.2 | サーバーレス推論の遅延が増えました。ModelLatency は変わらず、OverheadLaten… |
| [observability 問2](../../exercises/observability.md#q2) | 4.1.2 | 曜日で変動する呼び出し数に、固定のしきい値のアラームを設定すると誤報が多く出ます。適切な機能はどれで… |
| [observability 問3](../../exercises/observability.md#q3) | 4.1.2 | ML のワークフローの異常を検知します。次の組み合わせのうち正しいものを選んでください。（2つ選択） |
| [observability 問4](../../exercises/observability.md#q4) | 4.1.6 | 対話アプリの「最初の応答が遅い」という声を調べます。どの Bedrock の指標を見ますか。 |
| [observability 問5](../../exercises/observability.md#q5) | 4.1.6 | Bedrock でスロットリングが起きています。Invocations は増えていません。正しい説明… |
| [observability 問6](../../exercises/observability.md#q6) | 4.1.6 | 大きなプロンプトを送っているアプリを特定するため、CloudWatch Logs Insights … |
| [observability 問7](../../exercises/observability.md#q7) | 4.2.2 | API Gateway、Lambda、エンドポイントをつなぐ推論のシステムで、どこで遅いかを探します… |
| [observability 問8](../../exercises/observability.md#q8) | 4.2.2 | 昨夜エンドポイントの設定を変更した人を調べます。どのサービスですか。 |
| [observability 問9](../../exercises/observability.md#q9) | 4.2.2 | AgentCore のエージェントの動作を調べます。正しい説明を選んでください。（2つ選択） |
| [observability 問10](../../exercises/observability.md#q10) | 4.2.3 | 複数のリージョンのエンドポイントの指標を、1 つの画面で見ます。追加のサービスを増やさない選択はどれ… |
| [observability 問11](../../exercises/observability.md#q11) | 4.2.3 | 複数のアカウントのエンドポイントの指標を CloudWatch でまとめ、事業の指標は経営層向けに別… |
| [observability 問12](../../exercises/observability.md#q12) | 4.2.3 | CloudWatch のダッシュボードに Logs Insights のウィジェットを多数置き、10… |

<!-- questions:end -->
