# 分野4: Route 53 のゾーンとレコード

DNS の通信の保護を問います。改ざんと盗聴で手段が変わります。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [DNS の保護](../../domain4.md#t4-3-dns) | DNS の通信の保護（DNSSEC）、安全な DNS 通信の実装 |

## 学習の順番 {#study-order}

1. [プライベートホストゾーン](../../../../services/network-connectivity.md#private-hosted-zones): DNSSEC の項目を確認します。
2. [エンドポイント](../../../../services/network-connectivity.md#resolver-endpoints): DoH の設定を確認します。
3. [DNS Firewall](../../../../services/network-connectivity.md#dns-firewall): できることの範囲を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 改ざんを防ぐ | DNSSEC |
| 盗聴を防ぐ | DoH か、区間の暗号化 |

## 引っかかりやすい点 {#traps}

- DNSSEC は暗号化しません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [route53-zones 問25](../../exercises/route53-zones.md#q25) | DNS の保護 | 金融機関は「オンプレミスのリゾルバーから AWS のインバウンドエンドポイントまでの DNS の問い… |
| [route53-zones 問26](../../exercises/route53-zones.md#q26) | DNS の保護 | 公開サイトの利用者が偽の応答へ誘導されるリスク（キャッシュポイズニング）を下げるよう、監査で指摘され… |
| [route53-zones 問27](../../exercises/route53-zones.md#q27) | DNS の保護 | セキュリティの担当者が DNS の保護の手段を表にまとめています。手段と効果の組み合わせとして誤って… |

<!-- questions:end -->
