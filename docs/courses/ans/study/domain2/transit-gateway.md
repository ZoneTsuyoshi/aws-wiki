# 分野2: Transit Gateway と SD-WAN

マルチ VPC の接続と SD-WAN の実装、ルートテーブルの分離を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [SD-WAN](../../domain2.md#t2-1-sdwan) | トラフィック管理と SD-WAN（Connect） |
| [ハブアンドスポーク](../../domain2.md#t2-2-hub-spoke) | ハブアンドスポークの構成（Transit Gateway、トランジット VPC） |
| [第三者製品](../../domain2.md#t2-2-third-party) | 既存の第三者製品とのハイブリッド接続 |
| [VPC 間の接続](../../domain2.md#t2-2-multi-vpc) | VPC 間、アカウント間の接続（ピアリング、Transit Gateway、VPN、第三者、SD-WAN、MPLS） |

## 学習の順番 {#study-order}

1. [Connect](../../../../services/network-connectivity.md#tgw-connect): 実装の手順を確認します。
2. [ルートテーブル](../../../../services/network-connectivity.md#tgw-route-tables): 関連付けと伝播で分離します。
3. [アタッチメント](../../../../services/network-connectivity.md#tgw-attachments): サブネットの設計を押さえます。
4. [VPC ピアリング](../../../../services/network-connectivity.md#vpc-peering): ピアリングの手順を確認します。
5. [ピアリング](../../../../services/network-connectivity.md#tgw-peering): 静的ルートの制約を覚えます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| Connect の内部 CIDR | `169.254.0.0/16` の `/29` | アプライアンスは最初の値 |
| eBGP | `ebgp-multihop`、TTL 2 | Connect の設定 |
| アタッチメント用サブネット | AZ ごとに `/28` | 専用にする |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 新規のハブアンドスポーク | Transit Gateway |
| 第三者の VPN 機器 | Site-to-Site VPN の CGW |
| SD-WAN の仮想アプライアンス | Connect |

## 引っかかりやすい点 {#traps}

- 既定の関連付けと伝播のままだと、全 VPC が通信できます。
- AWS の VPN はルートベースです。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [transit-gateway 問4](../../exercises/transit-gateway.md#q4) | SD-WAN | Connect の実装で、アプライアンスと Transit Gateway の GRE トンネルが上… |
| [transit-gateway 問5](../../exercises/transit-gateway.md#q5) | SD-WAN | Connect のピアの内部 CIDR を 169.254.6.0/29 にしました。アプライアンス… |
| [transit-gateway 問6](../../exercises/transit-gateway.md#q6) | SD-WAN | SD-WAN のベンダーと Connect の設計を確認しています。ベンダーは静的ルートと BFD … |
| [transit-gateway 問7](../../exercises/transit-gateway.md#q7) | ハブアンドスポーク | 新規に 100 個の VPC を接続するハブアンドスポークを設計します。ハブの運用はできるだけ減らし… |
| [transit-gateway 問8](../../exercises/transit-gateway.md#q8) | ハブアンドスポーク | トランジット VPC の既存の構成が残っており、第三者のルーターの機能に依存しています。Transi… |
| [transit-gateway 問9](../../exercises/transit-gateway.md#q9) | ハブアンドスポーク | Transit Gateway の VPC アタッチメントのサブネットを設計します。ベストプラクティ… |
| [transit-gateway 問10](../../exercises/transit-gateway.md#q10) | 第三者製品 | 第三者のファイアウォールを CGW として Site-to-Site VPN へ接続します。機器はポ… |
| [transit-gateway 問11](../../exercises/transit-gateway.md#q11) | 第三者製品 | 買収した会社の VPN 機器と仮想ファイアウォールを、AWS のネットワークへつなぎます。製品は当面… |
| [transit-gateway 問12](../../exercises/transit-gateway.md#q12) | 第三者製品 | 第三者のルーターで VPN を初めて設定します。設定の間違いを減らしたいと考えています。AWS の機… |
| [transit-gateway 問13](../../exercises/transit-gateway.md#q13) | VPC 間の接続 | Transit Gateway で本番 VPC と開発 VPC を分け、両方とも共有 VPC と D… |
| [transit-gateway 問14](../../exercises/transit-gateway.md#q14) | VPC 間の接続 | VPC A と B の間でピアリングを作成して承認しました。しかし通信できません。SG は相手の範囲… |
| [transit-gateway 問15](../../exercises/transit-gateway.md#q15) | VPC 間の接続 | 東京と大阪の Transit Gateway をピアリングで接続しました。BGP を使うつもりでした… |

<!-- questions:end -->
