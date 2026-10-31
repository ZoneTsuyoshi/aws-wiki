# 分野4: 監視とオブザーバビリティ

運用、トレース、FM のやり取り、事業の指標を分けて見ます。既定の指標で分からない品質の見方が問われます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.3.1](../../domain4.md#skill-4-3-1) | 全体を見渡す観測 |
| [4.3.2](../../domain4.md#skill-4-3-2) | 生成 AI に特有の監視 |
| [4.3.3](../../domain4.md#skill-4-3-3) | 実行につながる統合的な観測 |
| [4.3.6](../../domain4.md#skill-4-3-6) | 生成 AI に特有の障害の調査 |

## 学習の順番 {#study-order}

1. [監視とオブザーバビリティ](../../../../services/genai-apps.md#observability)と[見るべき指標](../../../../services/genai-apps.md#genai-metrics): 区分と手段の表を確認します。
2. [CloudWatch のメトリクス](../../../../services/ai.md#bedrock-metrics)と[モデル呼び出しログ](../../../../services/ai.md#invocation-logging): 分かることと対象を押さえます。
3. [異常検知](../../../../services/observability.md#anomaly-detection)と [Cost Anomaly Detection](../../../../services/cost-management.md#cost-anomaly-detection): 急増の検知を理解します。
4. [Managed Grafana](../../../../services/operations.md#managed-grafana)、[Quick Sight](../../../../services/data-engineering.md#quick-sight)、[チャットアプリへの通知](../../../../services/operations.md#q-chat): 相手に合う見せ方を選べるようにします。
5. [トラブルシューティング](../../../../services/genai-apps.md#troubleshooting): ハルシネーションの調査の順序を覚えます。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 品質の低下 | 評価のカスタムメトリクス |
| 費用の急増 | Cost Anomaly Detection とタグ |
| 周期のあるトークンの急増 | CloudWatch の異常検知 |
| 長期の監査 | CloudTrail と呼び出しログを S3 に |
| テナントで絞る | `requestMetadata` |
| 一貫性の低下 | 意味的類似度で比較 |

## 引っかかりやすい点 {#traps}

- `AWS/Bedrock` で分かるのは遅延や量で、品質は分かりません。
- `bedrock-mantle` の呼び出しは呼び出しログに記録されません。
- HTTP 200 でも失敗していることがあります。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [observability 問4](../../exercises/observability.md#q4) | 4.3.1 | 生成 AI の監視を設計します。運用担当は遅延とエラーを、開発者はサービス間の呼び出しとプロンプトか… |
| [observability 問5](../../exercises/observability.md#q5) | 4.3.1 | 技術者は CloudWatch と他社の監視データを 1 つのダッシュボードで見たいと考えています。… |
| [observability 問6](../../exercises/observability.md#q6) | 4.3.1 | エラー率は 0% なのに顧客満足度が下がっています。プロンプトは先週更新しました。ダッシュボードには… |
| [observability 問7](../../exercises/observability.md#q7) | 4.3.2 | エージェントの月額が急に 3 倍になりました。呼び出しの数はほぼ同じです。今後は早く検知し、原因のア… |
| [observability 問8](../../exercises/observability.md#q8) | 4.3.2 | トークンの消費量は曜日と時間帯で大きく変わるので、固定のしきい値のアラームが誤報を繰り返しています。… |
| [observability 問9](../../exercises/observability.md#q9) | 4.3.2 | bedrock-mantle と bedrock-runtime の両方のエンドポイントを使うアプリ… |
| [observability 問10](../../exercises/observability.md#q10) | 4.3.2 | プロンプトの版ごとの効果と、ハルシネーション率を、運用のダッシュボードで追いたいと考えています。何を… |
| [observability 問11](../../exercises/observability.md#q11) | 4.3.3 | セキュリティのインシデントに備えて、フォレンジックと監査の証跡を 7 年間残します。誰が呼び出したか… |
| [observability 問12](../../exercises/observability.md#q12) | 4.3.3 | 生成 AI のアラームが発報すると、担当者がメールに気づくまで数時間かかります。Slack で受け取… |
| [observability 問13](../../exercises/observability.md#q13) | 4.3.3 | モデルの更新後、エラーはないものの、応答の長さと拒否の割合が変わりました。コンプライアンス担当は、ガ… |
| [observability 問14](../../exercises/observability.md#q14) | 4.3.6 | RAG の回答にハルシネーションが増えたと報告されました。HTTP はすべて 200 です。調査の順… |
| [observability 問15](../../exercises/observability.md#q15) | 4.3.6 | 同じ入力に対するエージェントの回答が日によって大きく変わるようになりました。モデルの設定は変えていま… |
| [observability 問16](../../exercises/observability.md#q16) | 4.3.6 | 生成 AI の回答の品質が日によって悪化しますが、検索が悪いのか、生成が悪いのか、ツールが失敗したの… |

<!-- questions:end -->
