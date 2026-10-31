# 分野1: VPN とカプセル化

カプセル化と暗号化の違い、MTU への影響を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [カプセル化と暗号化](../../domain1.md#t1-5-encapsulation) | カプセル化と暗号化（GRE、IPsec） |

## 学習の順番 {#study-order}

1. [MTU と MSS](../../../../services/network-connectivity.md#vpn-mtu): VPN の実効 MTU を確認します。
2. [Connect](../../../../services/network-connectivity.md#tgw-connect): GRE の MTU を確認します。
3. [MTU とジャンボフレーム](../../../../services/network-connectivity.md#mtu): 経路ごとの MTU を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| GRE の内側 | 外部 1500 なら 1476 | 24 バイトを引く |
| VPN の実効 MTU | 最大 1446 | AES-GCM、NAT-T なし |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| DX から VPN への切り替えで大きなパケットだけ消える | MTU を確認して MSS を調整 |

## 引っかかりやすい点 {#traps}

- MACsec は区間の暗号化で、VPC までは守りません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [vpn 問4](../../exercises/vpn.md#q4) | カプセル化と暗号化 | 新しい担当者が、AWS のカプセル化の技術を整理しています。規制で暗号化の有無を報告します。カプセル… |
| [vpn 問5](../../exercises/vpn.md#q5) | カプセル化と暗号化 | Connect の GRE のアプライアンスで、外部の MTU が 1500 です。内側のインターフ… |
| [vpn 問6](../../exercises/vpn.md#q6) | カプセル化と暗号化 | 平常時は DX のトランジット VIF（MTU 8500）を使い、障害時は VPN へ切り替わります… |

<!-- questions:end -->
