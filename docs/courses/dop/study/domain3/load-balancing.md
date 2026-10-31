# 分野3: 負荷分散

AZ をまたぐ分散と、バックエンド障害のときの動きを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [負荷分散](../../domain3.md#t3-1-load-balancing) | AZ をまたぐ負荷分散の設定 |
| [ロードバランサー](../../domain3.md#t3-3-load-balancer) | バックエンド障害から復旧するロードバランサー |

## 学習の順番 {#study-order}

1. [クロスゾーン負荷分散](../../../../services/networking.md#cross-zone): ALB と NLB の既定の違いを覚えます。
2. [ヘルスチェック](../../../../services/ec2-beanstalk.md#asg-health-checks): ELB ヘルスチェックを有効にする理由を確認します。
3. [ヘルスチェック](../../../../services/networking.md#alb-health-checks): フェイルオープンの動きを理解します。
4. [ターゲットグループの属性](../../../../services/networking.md#target-group-attributes): 登録解除の遅延を確認します。
5. [Route 53 のフェイルオーバー設計](../../../../services/resilience.md#route53-failover): `Evaluate Target Health` の役割を押さえます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| クロスゾーンの既定 | ALB は有効、NLB は無効 | NLB はターゲット数の差で偏る |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| プロセスの異常でインスタンスを置き換える | Auto Scaling の ELB ヘルスチェック |
| 処理中のリクエストを完了させる | 登録解除の遅延 |
| ALB が使えなければ別のリージョンへ | `Evaluate Target Health` |

## 引っかかりやすい点 {#traps}

- ヘルスチェックが依存先を見ると、依存先の障害で全台が置き換わります。
- 全ターゲットが異常のとき、ALB は全ターゲットへ転送します。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [load-balancing 問1](../../exercises/load-balancing.md#q1) | 負荷分散 | NLB の後ろに、AZ-a に 2 台、AZ-b に 8 台のターゲットがあります。AZ-a のター… |
| [load-balancing 問2](../../exercises/load-balancing.md#q2) | 負荷分散 | ALB を 1 つのサブネットで作成しようとして失敗しました。作成後は、Auto Scaling の… |
| [load-balancing 問3](../../exercises/load-balancing.md#q3) | 負荷分散 | ALB の後ろで、AZ ごとにターゲットの数が 3 台と 1 台に変わる時間帯があります。全ターゲッ… |
| [load-balancing 問4](../../exercises/load-balancing.md#q4) | ロードバランサー | ヘルスチェックのパスでデータベースへの接続を確認しています。データベースの短い障害で全インスタンスが… |
| [load-balancing 問5](../../exercises/load-balancing.md#q5) | ロードバランサー | 新しいバージョンのバグで、全ターゲットがヘルスチェックに失敗しました。すると ALB は 503 を… |
| [load-balancing 問6](../../exercises/load-balancing.md#q6) | ロードバランサー | リージョンの ALB の後ろの全ターゲットが異常のとき、自動で別のリージョンへ切り替えます。Rout… |

<!-- questions:end -->
