# 分野1: CloudWatch とログの要件

ログと監視の要件を定義する問題です。要件から逆算して、どのメトリクスとログを使うかを選びます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [CloudWatch](../../domain1.md#t1-4-cloudwatch) | CloudWatch のメトリクス、エージェント、ログ、アラーム、ダッシュボード、インサイト |
| [メトリクスとベースライン](../../domain1.md#t1-4-metrics) | 状態を示すメトリクスの推奨、ベースラインの取得 |
| [要件の特定](../../domain1.md#t1-4-requirements) | ログと監視の要件の特定 |
| [アクセスログ](../../domain1.md#t1-4-access-logs) | アクセスログ（ロードバランサー、CloudFront） |

## 学習の順番 {#study-order}

1. [CloudWatch メトリクス](../../../../services/observability.md#cloudwatch-metrics): ネットワークの標準メトリクスと、OS の値を集める手段を区別します。
2. [アラーム](../../../../services/observability.md#alarms): `TunnelState` などのアラームの作り方を確認します。
3. [Logs Insights でログを検索する](../../../../services/observability.md#logs-insights): フローログの集計の書き方を押さえます。
4. [ログ](../../../../services/networking.md#cloudfront-logs): 標準ログとリアルタイムログの違いを覚えます。
5. [フローログの分析](../../../../services/network-connectivity.md#flow-log-analysis): どのログに何が残るかを表で確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| CloudFront の標準ログ | ベストエフォート | 会計には向かない |
| CloudFront のリアルタイムログ | Kinesis Data Streams | 数秒以内、サンプリング |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 誰がどこへ通信したかを 1 年保持 | フローログを S3 へ |
| 拒否された通信をすぐ知りたい | CloudWatch Logs、メトリクスフィルター、アラーム |
| IDS でパケットを検査 | Traffic Mirroring |
| 問い合わせたドメインの記録 | Resolver クエリログ |
| 正常時の遅延と損失を、エージェントなしで測る | Network Synthetic Monitor |

## 引っかかりやすい点 {#traps}

- `ethtool -S` の統計は CloudWatch の標準メトリクスには出ません。
- メトリクスフィルターは作成後のログにしか効きません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [cloudwatch 問1](../../exercises/cloudwatch.md#q1) | CloudWatch | 世界の 30 拠点の VPN と DX を 1 つのチームが監視します。拠点ごとの通信量を 1 画面… |
| [cloudwatch 問2](../../exercises/cloudwatch.md#q2) | CloudWatch | EC2 のプロキシで、同時接続数と ethtool -S の統計を時系列で見たいと考えています。ハイ… |
| [cloudwatch 問3](../../exercises/cloudwatch.md#q3) | CloudWatch | フローログを CloudWatch Logs へ送っています。障害の調査中に、過去 1 時間で拒否の… |
| [cloudwatch 問4](../../exercises/cloudwatch.md#q4) | メトリクスとベースライン | NAT ゲートウェイの背後のアプリで、外部 API への接続がときどき失敗します。CPU と帯域には… |
| [cloudwatch 問5](../../exercises/cloudwatch.md#q5) | メトリクスとベースライン | EC2 間の通信でパケットの損失が増えています。CloudWatch の NetworkIn はイン… |
| [cloudwatch 問6](../../exercises/cloudwatch.md#q6) | メトリクスとベースライン | オンプレミスと VPC の間のハイブリッド接続について、正常時の遅延と損失を測ってベースラインを持ち… |
| [cloudwatch 問7](../../exercises/cloudwatch.md#q7) | 要件の特定 | 次の 2 つの要件があります。(1) 誰がどこへ通信したかを 1 年保持し、費用を抑える。(2) 拒… |
| [cloudwatch 問8](../../exercises/cloudwatch.md#q8) | 要件の特定 | 監査チームから 3 つの要件が出ました。(A) IDS でパケットの中身を検査する。(B) VPC … |
| [cloudwatch 問9](../../exercises/cloudwatch.md#q9) | 要件の特定 | ある会社は、VPC の外向きのドメインごとの接続の傾向を把握したいと考えています。一部の通信は Ne… |
| [cloudwatch 問10](../../exercises/cloudwatch.md#q10) | アクセスログ | CloudFront のログを数秒以内に処理して、地域ごとのエラーの急増を検知したいと考えています。… |
| [cloudwatch 問11](../../exercises/cloudwatch.md#q11) | アクセスログ | 経理チームが CloudFront の標準ログから、顧客への請求額を確定しようとしています。ログの性… |
| [cloudwatch 問12](../../exercises/cloudwatch.md#q12) | アクセスログ | 監査のため、HTTP の Web の ALB と TLS の NLB の両方でアクセスログを有効にし… |

<!-- questions:end -->
