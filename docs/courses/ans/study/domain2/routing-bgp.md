# 分野2: ルーティングと BGP

ルーティングの実装で忘れやすい設定を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [ルーティングプロトコル](../../domain2.md#t2-1-routing) | ルーティングプロトコル（静的、動的）、静的、動的ルーティングの構成 |

## 学習の順番 {#study-order}

1. [ルーティング](../../../../services/network-connectivity.md#vpn-routing): VPN の静的と動的を確認します。
2. [ルートテーブル](../../../../services/network-connectivity.md#tgw-route-tables): Transit Gateway の表を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| VGW の経路がサブネットに反映されない | ルートテーブルの伝播を有効に |
| Transit Gateway の経路があるのに通信できない | VPC に `tgw-` のルートを追加 |

## 引っかかりやすい点 {#traps}

- Transit Gateway ピアリングは静的ルートのみです。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [routing-bgp 問8](../../exercises/routing-bgp.md#q8) | ルーティングプロトコル | 複数のリージョンと拠点を結ぶ設計で、BGP に統一する案をレビューしています。接続ごとのルーティング… |
| [routing-bgp 問9](../../exercises/routing-bgp.md#q9) | ルーティングプロトコル | VGW の経路が BGP で届いているのに、サブネットの EC2 からオンプレミスへ通信できません。… |
| [routing-bgp 問10](../../exercises/routing-bgp.md#q10) | ルーティングプロトコル | VPC を Transit Gateway にアタッチし、Transit Gateway のルートテ… |

<!-- questions:end -->
