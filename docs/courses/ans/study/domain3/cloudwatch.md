# 分野3: CloudWatch とログの要件

性能の指標の解釈と、調べるログとメトリクスを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [指標と制約](../../domain3.md#t3-2-metrics) | 性能の指標と到達性の制約（ルーティング、パケットサイズ） |
| [ログとメトリクス](../../domain3.md#t3-2-logs) | 性能と到達性を調べるログとメトリクス |

## 学習の順番 {#study-order}

1. [MTU とジャンボフレーム](../../../../services/network-connectivity.md#mtu): パケットサイズの制約を確認します。
2. [ルートテーブル](../../../../services/network-connectivity.md#tgw-route-tables): Transit Gateway の破棄を確認します。
3. [ALB のエラーコード](../../../../services/networking.md#alb-errors): 5xx の区別を押さえます。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 1 フローだけ 5 Gbps | シングルフローの上限 |
| Transit Gateway の破棄 | `PacketDropCountNoRoute`、`PacketDropCountBlackhole` |
| DX の損失 | `ConnectionErrorCount` |

## 引っかかりやすい点 {#traps}

- 小さな通信が通るなら、まずパケットサイズを疑います。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [cloudwatch 問19](../../exercises/cloudwatch.md#q19) | 指標と制約 | 同じ VPC の 2 台の間で iperf を実行すると、1 フローでは 5 Gbps で止まり、1… |
| [cloudwatch 問20](../../exercises/cloudwatch.md#q20) | 指標と制約 | ある経路で、小さな ping は通りますが、ファイル転送だけタイムアウトします。ルート、SG、NAC… |
| [cloudwatch 問21](../../exercises/cloudwatch.md#q21) | 指標と制約 | VPN の経路で帯域が 1 Gbps を少し超えると損失が増えます。トンネルの状態は UP で、BG… |
| [cloudwatch 問22](../../exercises/cloudwatch.md#q22) | ログとメトリクス | Transit Gateway を通る通信が一部失敗します。アタッチメントの宛先によって動きが違いま… |
| [cloudwatch 問23](../../exercises/cloudwatch.md#q23) | ログとメトリクス | DX の接続でパケットの損失があります。トンネルや BGP に異常はなく、物理の問題を疑っています。… |
| [cloudwatch 問24](../../exercises/cloudwatch.md#q24) | ログとメトリクス | ALB の 5xx が増えています。ALB 自身の 5xx か、ターゲットの 5xx かを区別したう… |

<!-- questions:end -->
