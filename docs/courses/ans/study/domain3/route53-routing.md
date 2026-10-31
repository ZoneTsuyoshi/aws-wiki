# 分野3: Route 53 のルーティングと高可用性

Route 53 の高可用性を問います。データプレーンの切り替えが中心です。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [Route 53 の高可用性](../../domain3.md#t3-3-route53-ha) | Route 53 の高可用性の機能、Route 53 の信頼性の選択肢、可用性を高めるゾーンとレコードの作成（プライベートの zonal DNS など） |

## 学習の順番 {#study-order}

1. [フェイルオーバーはデータプレーンで](../../../../services/resilience.md#failover-data-plane): コントロールプレーンに依存しないことを確認します。
2. [Amazon Application Recovery Controller(ARC)](../../../../services/resilience.md#arc): ルーティングコントロールを押さえます。
3. [VPC エンドポイントと PrivateLink](../../../../services/networking.md#vpc-endpoints): zonal DNS 名を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| API が使えなくても切り替える | ARC のルーティングコントロール |
| 同じ AZ の ENI へ | zonal DNS 名 |

## 引っかかりやすい点 {#traps}

- ヘルスチェックのないレコードは正常として扱われます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [route53-routing 問11](../../exercises/route53-routing.md#q11) | Route 53 の高可用性 | ある企業は「リージョンの障害時に、Route 53 のコンソールや API が使えなくても切り替えら… |
| [route53-routing 問12](../../exercises/route53-routing.md#q12) | Route 53 の高可用性 | 2 リージョンの構成で、リージョンはレイテンシーで選び、各リージョンの中では 2 つの ALB を … |
| [route53-routing 問13](../../exercises/route53-routing.md#q13) | Route 53 の高可用性 | S3 以外の AWS サービスへのインターフェイスエンドポイントを 3 つの AZ に持っています。… |
| [route53-routing 問14](../../exercises/route53-routing.md#q14) | Route 53 の高可用性 | Active-Passive の Route 53 フェイルオーバーで、セカンダリのヘルスチェックを… |

<!-- questions:end -->
