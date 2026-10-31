# 分野3: ルーティングと BGP

BGP の管理、ルートテーブルの制御、経路の最適化を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [BGP の管理](../../domain3.md#t3-1-bgp) | 業界標準のルーティングプロトコル（DX の BGP）、ルーティングプロトコルの管理（DX、VPN） |
| [ルートテーブル](../../domain3.md#t3-1-route-tables) | ルートテーブルによる制御（伝播、BGP） |
| [経路の最適化](../../domain3.md#t3-1-route-optimization) | 動的、静的ルーティングの最適化（集約、CIDR の重複） |

## 学習の順番 {#study-order}

1. [VPN の 2 本のトンネル](../../../../services/network-connectivity.md#bgp-vpn-tunnels): トンネルの MED の動きを確認します。
2. [VIF の種類](../../../../services/network-connectivity.md#dx-vif-types): BFD の扱いを覚えます。
3. [Transit Gateway ルートテーブル](../../../../services/network-connectivity.md#tgw-route-priority): ブラックホールを含む制御を確認します。
4. [計算例](../../../../services/network-connectivity.md#route-priority-examples): 計算の例を確認します。
5. [経路数の上限に当たったとき](../../../../services/network-connectivity.md#bgp-route-limits): 上限と集約を押さえます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| Connect の BGP タイマー | キープアライブ 10 秒、ホールド 30 秒 | BFD は使えない |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 特定の宛先だけ止める | ブラックホールルート |
| VPC の中の機器の経路を反映 | VPC Route Server |

## 引っかかりやすい点 {#traps}

- 表に出るのは優先経路だけです。VPN の経路がなくても異常ではありません。
- Weight や Local preference をトンネルで変えると AWS の MED が無視されます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [routing-bgp 問11](../../exercises/routing-bgp.md#q11) | BGP の管理 | VPN の 2 本のトンネルのうち、AWS の保守のときに片方へ切り替わるようにしています。CGW … |
| [routing-bgp 問12](../../exercises/routing-bgp.md#q12) | BGP の管理 | DX の BGP の障害検出が遅く、切り替えまで 90 秒かかっています。プライベート VIF です… |
| [routing-bgp 問13](../../exercises/routing-bgp.md#q13) | BGP の管理 | SD-WAN のアプライアンスが Transit Gateway Connect の BGP を使っ… |
| [routing-bgp 問14](../../exercises/routing-bgp.md#q14) | ルートテーブル | Transit Gateway で開発 VPC の通信を、特定の宛先 10.9.0.0/16 だけ止… |
| [routing-bgp 問15](../../exercises/routing-bgp.md#q15) | ルートテーブル | VPC のルートテーブルで DX と VPN が同じ経路を広告しています。表には DX の経路しか表… |
| [routing-bgp 問16](../../exercises/routing-bgp.md#q16) | ルートテーブル | VPC の中のアプライアンス（BGP に対応）の経路を、サブネットのルートテーブルへ動的に反映したい… |
| [routing-bgp 問17](../../exercises/routing-bgp.md#q17) | 経路の最適化 | VPC に新しい CIDR 10.2.0.0/16 を追加しようとしましたが、失敗しました。ルートテ… |
| [routing-bgp 問18](../../exercises/routing-bgp.md#q18) | 経路の最適化 | DX を主の経路として広告する 10.0.0.0/8 と、VPN で従の経路として広告する 10.1… |
| [routing-bgp 問19](../../exercises/routing-bgp.md#q19) | 経路の最適化 | プライベート VIF へ 90 経路を広告していますが、新しい拠点で 15 経路増えます。経路が増え… |
| [routing-bgp 問20](../../exercises/routing-bgp.md#q20) | 経路の最適化 | Transit Gateway に接続した VPC のプレフィックスを、トランジット VIF でオン… |

<!-- questions:end -->
