# 分野4: ヘルスチェック

確認する場所と失敗時の動きの違いを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [ヘルスチェック](../../domain4.md#t4-3-health-checks) | ヘルスチェックの機能、ヘルスチェックの設定 |

## 学習の順番 {#study-order}

1. [ヘルスチェック](../../../../services/networking.md#alb-health-checks): 理由コードと確認先を覚えます。
2. [Route 53 ヘルスチェック](../../../../services/networking.md#route53-health-checks): 種類と、プライベートのリソースの扱いを確認します。
3. [ヘルスチェックの計算](../../../../services/networking.md#health-check-calc): 検知までの時間を計算します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 内部のサービスを Route 53 で監視する | CloudWatch アラームの状態を監視する |
| `Target.ResponseCodeMismatch` | パスと成功コード |
| `Target.Timeout` | セキュリティグループと応答の速さ |

## 引っかかりやすい点 {#traps}

- Route 53 のヘルスチェッカーはインターネットにあります。IP 範囲の許可も必要です。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [load-balancing 問7](../../exercises/load-balancing.md#q7) | ヘルスチェック | Route 53 のフェイルオーバーで、インターネットに公開していない内部のサービスを監視します。ヘ… |
| [load-balancing 問8](../../exercises/load-balancing.md#q8) | ヘルスチェック | ALB のターゲットが unhealthy です。ターゲットの説明の理由は次のどれかです。それぞれの… |
| [load-balancing 問9](../../exercises/load-balancing.md#q9) | ヘルスチェック | ALB のターゲットグループの設定は、間隔 30 秒、異常のしきい値 5 回です。異常の検知まで最大… |
| [load-balancing 問10](../../exercises/load-balancing.md#q10) | ヘルスチェック | 公開のエンドポイントに Route 53 のヘルスチェックを設定し、セキュリティグループでは社内の … |

<!-- questions:end -->
