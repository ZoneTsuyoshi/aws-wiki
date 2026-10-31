# 分野4: VPN とカプセル化

DX の上の VPN と IPsec の方式を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [DX の上の VPN](../../domain4.md#t4-3-vpn-dx) | DX の上の VPN |
| [暗号化の方式](../../domain4.md#t4-3-ipsec) | 転送時の暗号化の方式（IPsec） |

## 学習の順番 {#study-order}

1. [プライベート IP VPN](../../../../services/network-connectivity.md#vpn-private-ip): 公開 VIF の上の VPN との違いを確認します。
2. [トンネルオプション](../../../../services/network-connectivity.md#vpn-tunnel-options): IKE と暗号を押さえます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| 事前共有キー | 8〜64 文字 | 自動生成も可 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 公開 IP なしで DX を暗号化 | トランジット VIF の上のプライベート IP VPN |
| 暗号化ありとなしを併用 | ルートテーブルを分ける |

## 引っかかりやすい点 {#traps}

- VPN を重ねるとトンネルの帯域が上限になります。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [vpn 問7](../../exercises/vpn.md#q7) | DX の上の VPN | 規制により DX の上の通信も暗号化します。公開 IP は使えません。AWS 側は Transit … |
| [vpn 問8](../../exercises/vpn.md#q8) | DX の上の VPN | 10 Gbps の DX の上に標準のトンネルでプライベート IP VPN を張りました。すると実効… |
| [vpn 問9](../../exercises/vpn.md#q9) | DX の上の VPN | 1 本の DX で、機密データは暗号化し、大容量のバックアップは暗号化なしで DX の全帯域を使いた… |
| [vpn 問10](../../exercises/vpn.md#q10) | 暗号化の方式 | VPN のトンネルを、新しい方式へ揃えます。AWS 側から接続を開始する要件もあります。IKE のバ… |
| [vpn 問11](../../exercises/vpn.md#q11) | 暗号化の方式 | VPN の実効 MTU を最大にする暗号方式を選びます。CGW は NAT の背後にありません。正し… |
| [vpn 問12](../../exercises/vpn.md#q12) | 暗号化の方式 | DX の区間に MACsec、インターネットの区間に Site-to-Site VPN を使う設計を… |

<!-- questions:end -->
