# 分野1: Direct Connect

物理接続、冗長構成、接続の要件の特定を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [物理接続](../../domain1.md#t1-5-physical) | 物理接続の L1、L2（VLAN、LAG、光、ジャンボフレーム） |
| [冗長な接続](../../domain1.md#t1-5-redundancy) | 冗長な接続の設計（DX、VPN） |
| [要件の特定](../../domain1.md#t1-5-requirements) | ハイブリッド接続の要件の特定 |

## 学習の順番 {#study-order}

1. [接続の種類](../../../../services/network-connectivity.md#dx-connections): 専用接続とホスト接続、光の規格を確認します。
2. [LAG](../../../../services/network-connectivity.md#dx-lag): LAG の用途と `minimumLinks` を理解します。
3. [回復性のモデル](../../../../services/network-connectivity.md#dx-resiliency): 回復性のモデルと可用性を覚えます。
4. [例 4: DX を主、VPN を従にする](../../../../services/network-connectivity.md#bgp-dx-vpn): VPN を従にするときの注意を確認します。
5. [オンプレミスとの接続](../../../../services/network-connectivity.md#choosing-hybrid): 要件から接続を選びます。
6. [DX の VIF](../../../../services/network-connectivity.md#choosing-vif): VIF の種類を選びます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| LAG の本数 | 100 Gbps 未満は 4 本、以上は 2 本 | 同じ速度 |
| Maximum のモデル | 2 ロケーションに各 2 接続 | 99.99% |
| High のモデル | 2 ロケーションに各 1 接続 | 99.9% |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 多数の VPC を DX で | トランジット VIF と Transit Gateway |
| S3 の公開エンドポイント | 公開 VIF |
| 25 拠点以上、各 100 Mbps 未満 | VPN Concentrator |
| 拠点の間を AWS で | SiteLink |

## 引っかかりやすい点 {#traps}

- LAG は冗長化の手段ではありません。同じエンドポイントで終端します。
- Transit Gateway で VPN を静的にすると DX に勝ちます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [direct-connect 問1](../../exercises/direct-connect.md#q1) | 物理接続 | 10 Gbps の専用接続を 4 本束ねた LAG で、通常は 25 Gbps を流しています。2 … |
| [direct-connect 問2](../../exercises/direct-connect.md#q2) | 物理接続 | 10 Gbps の DX を同じロケーションで 2 本束ねた LAG があります。監査で「ロケーショ… |
| [direct-connect 問3](../../exercises/direct-connect.md#q3) | 物理接続 | 新しく 100 Gbps の DX の専用接続を発注します。ルーターの光モジュールの選定と、VIF … |
| [direct-connect 問7](../../exercises/direct-connect.md#q7) | 冗長な接続 | 重要な業務で 99.99% の可用性が必要です。コストより可用性を優先します。DX の接続の構成とし… |
| [direct-connect 問8](../../exercises/direct-connect.md#q8) | 冗長な接続 | 10 Gbps の DX の従の経路として VPN を入れます。切り替えたあと、大きなファイルの転送… |
| [direct-connect 問9](../../exercises/direct-connect.md#q9) | 冗長な接続 | 監査のため、VIF の BGP を止めたときの切り替えを確かめます。本番のルーターの設定は変更せず、… |
| [direct-connect 問13](../../exercises/direct-connect.md#q13) | 要件の特定 | 小規模な拠点が 40 か所あり、各拠点の帯域は 50 Mbps 程度です。VPN の接続の費用を抑え… |
| [direct-connect 問14](../../exercises/direct-connect.md#q14) | 要件の特定 | 日本と米国の DX ロケーションにそれぞれ拠点があり、拠点間の通信もリージョンを経由せず AWS の… |
| [direct-connect 問15](../../exercises/direct-connect.md#q15) | 要件の特定 | 1 つの DX で次の要件があります。(1) 東京の 150 個の VPC へ接続する。(2) S3… |

<!-- questions:end -->
