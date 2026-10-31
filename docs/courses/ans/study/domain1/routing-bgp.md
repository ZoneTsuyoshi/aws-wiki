# 分野1: ルーティングと BGP

ルートの優先順位と BGP の属性で、通信を制御する問題です。方向を先に決めます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [ルーティングの基礎](../../domain1.md#t1-5-routing) | ルーティングの基礎（動的と静的、BGP） |
| [BGP 属性](../../domain1.md#t1-5-bgp) | BGP 属性による制御（負荷分散、active/passive） |

## 学習の順番 {#study-order}

1. [ルートの優先順位](../../../../services/network-connectivity.md#route-priority): 最長一致が最初であることを確認します。
2. [VGW の経路選択](../../../../services/network-connectivity.md#vgw-route-priority): VGW の順序を覚えます。
3. [Transit Gateway ルートテーブル](../../../../services/network-connectivity.md#tgw-route-priority): Transit Gateway の順序を覚えます。
4. [属性の一覧](../../../../services/network-connectivity.md#bgp-attributes): 方向ごとの手段を整理します。
5. [例 1: 2 本の DX で active/passive](../../../../services/network-connectivity.md#bgp-active-passive): active/passive の作り方を確認します。
6. [例 3: AS_PATH が効かないとき](../../../../services/network-connectivity.md#bgp-associated-region): 関連付いたリージョンと AS_PATH の問題を押さえます。
7. [公開 VIF の経路制御](../../../../services/network-connectivity.md#bgp-public-vif): 公開 VIF のコミュニティを覚えます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| 優先度のコミュニティ | `7224:7100`〜`7300` | AWS からの戻りを動かす |
| 公開 VIF の広がり | `7224:9100`、`7224:9200` | リージョン、大陸 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| AWS から戻る通信を動かす | プレフィックス長、コミュニティ、AS_PATH、MED の順 |
| オンプレミスから出る通信を動かす | ルーターの Local preference |
| 2 本で分散 | 属性をそろえて ECMP |

## 引っかかりやすい点 {#traps}

- AS_PATH の付加が効かないのは、Local preference が先に評価されるからです。
- 片方向だけの設定は非対称な経路になります。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [routing-bgp 問1](../../exercises/routing-bgp.md#q1) | ルーティングの基礎 | VGW に同じプレフィックス 10.1.0.0/16 が、DX の BGP、VPN の静的、VPN … |
| [routing-bgp 問2](../../exercises/routing-bgp.md#q2) | ルーティングの基礎 | Transit Gateway のルートテーブルで、VPN は静的ルート、DX は DX ゲートウェ… |
| [routing-bgp 問3](../../exercises/routing-bgp.md#q3) | ルーティングの基礎 | VPC のルートテーブルに 10.1.0.0/16（ピアリングの静的）と 10.1.0.0/16（V… |
| [routing-bgp 問4](../../exercises/routing-bgp.md#q4) | BGP 属性 | 東京の VPC と 2 つの DX があります。関連付いたロケーションの接続 A を従、遠いロケーシ… |
| [routing-bgp 問5](../../exercises/routing-bgp.md#q5) | BGP 属性 | 2 本の DX を active/passive にしています。AWS からオンプレミスへの戻りはコ… |
| [routing-bgp 問6](../../exercises/routing-bgp.md#q6) | BGP 属性 | 同じ速度の 2 本の DX に active/active で分散させます。AWS からオンプレミス… |
| [routing-bgp 問7](../../exercises/routing-bgp.md#q7) | BGP 属性 | 公開 VIF でオンプレミスの公開プレフィックスを広告しています。AWS 内での広がりを同じ大陸のリ… |

<!-- questions:end -->
