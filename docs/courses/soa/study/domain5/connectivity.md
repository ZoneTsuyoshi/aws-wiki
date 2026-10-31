# 分野5: プライベート接続とハイブリッド接続

接続の選択と、通らないときの切り分けを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [5.1.2](../../domain5.md#skill-5-1-2) | プライベート接続 |
| [5.3.4](../../domain5.md#skill-5-3-4) | ハイブリッド接続とプライベート接続の問題 |

## 学習の順番 {#study-order}

1. [VPC エンドポイントと PrivateLink](../../../../services/networking.md#vpc-endpoints)と[エンドポイントの選び方と制約](../../../../services/networking.md#endpoint-settings): 2 つのエンドポイントを比較します。
2. [VPC ピアリング](../../../../services/network-connectivity.md#vpc-peering)と[VPC 同士の接続](../../../../services/network-connectivity.md#choosing-multi-vpc): VPC の接続を確認します。
3. [Site-to-Site VPN](../../../../services/network-connectivity.md#site-to-site-vpn)と[トンネルオプション](../../../../services/network-connectivity.md#vpn-tunnel-options): トンネルの設定を確認します。
4. [MTU と MSS](../../../../services/network-connectivity.md#vpn-mtu)と[VGW の経路選択](../../../../services/network-connectivity.md#vgw-route-priority): 大きな転送と経路の優先順位を確認します。
5. [Direct Connect](../../../../services/network-connectivity.md#direct-connect)と[経路数の上限に当たったとき](../../../../services/network-connectivity.md#bgp-route-limits): BGP の症状を確認します。
6. [Client VPN](../../../../services/network-connectivity.md#client-vpn): ルートと認可ルールを確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| ピアリングの要求 | 7 日で失効 | 未承認のまま放置しない |
| Client VPN のクライアント CIDR | `/22` 以上 | ルートと認可ルールも設定する |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 多数の VPC を接続する | Transit Gateway |
| CIDR が重複する相手へ公開する | PrivateLink |
| `TunnelState` が 0 | CGW、PSK、IKE |
| 大きな転送だけ止まる | MTU と MSS |
| BGP が `idle` で経路が消えた | 広告の経路を集約する |
| DX が正常なのに VPN を通る | より具体的な経路がある |

## 引っかかりやすい点 {#traps}

- ピアリングは推移しません。
- VPN は PMTUD に非対応です。
- ゲートウェイエンドポイントはオンプレミスから使えません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [connectivity 問1](../../exercises/connectivity.md#q1) | 5.1.2 | 40 個の VPC を相互に接続します。オンプレミスとの接続も共有します。どれが適切ですか。 |
| [connectivity 問2](../../exercises/connectivity.md#q2) | 5.1.2 | VPC ピアリングの A-B、B-C があります。A から C へ通信できません。CIDR の重複は… |
| [connectivity 問3](../../exercises/connectivity.md#q3) | 5.1.2 | 自社のサービスを、CIDR が重複する他の VPC へ公開します。どの構成が適切ですか。 |
| [connectivity 問4](../../exercises/connectivity.md#q4) | 5.1.2 | オンプレミスと VPC を今日から接続します。専用線の契約はありません。BGP が使える機器がありま… |
| [connectivity 問5](../../exercises/connectivity.md#q5) | 5.1.2 | リモートの社員のノート PC から VPC のサーバーへ接続します。どれを設定しますか。 |
| [connectivity 問6](../../exercises/connectivity.md#q6) | 5.1.2 | VPC エンドポイントの説明として正しいものを選んでください。（2つ選択） |
| [connectivity 問7](../../exercises/connectivity.md#q7) | 5.3.4 | Site-to-Site VPN の TunnelState が 0 です。確認するものはどれですか… |
| [connectivity 問8](../../exercises/connectivity.md#q8) | 5.3.4 | VPN のトンネルが通信なしの時間に落ちます。CGW はイニシエーターにしたくありません。どの設定と… |
| [connectivity 問9](../../exercises/connectivity.md#q9) | 5.3.4 | VPN のトンネルは上がっていますが、VPC とオンプレミスの間が通りません。確認するものを選んでく… |
| [connectivity 問10](../../exercises/connectivity.md#q10) | 5.3.4 | VPN 経由で小さな通信は通るのに、大きなファイルの転送だけが止まります。どの説明が正しいですか。 |
| [connectivity 問11](../../exercises/connectivity.md#q11) | 5.3.4 | Direct Connect の BGP が idle になり、全経路が消えました。物理の接続は正常… |
| [connectivity 問12](../../exercises/connectivity.md#q12) | 5.3.4 | Direct Connect と VPN が同じ VGW にあります。DX が正常なのに、一部の通信… |
| [connectivity 問13](../../exercises/connectivity.md#q13) | 5.3.4 | インターフェイスエンドポイントを作りましたが、サービスの通常の名前が公開 IP に解決されます。何を… |
| [connectivity 問14](../../exercises/connectivity.md#q14) | 5.3.4 | 接続の問題の説明として正しいものを選んでください。（2つ選択） |

<!-- questions:end -->
