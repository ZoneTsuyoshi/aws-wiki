# 分野3: Transit Gateway と SD-WAN

上限とクォータ、通信パターン、接続の選択、マルチキャストを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [上限とクォータ](../../domain3.md#t3-1-quotas) | 上限とクォータの影響 |
| [通信パターン](../../domain3.md#t3-1-patterns) | リージョン間、リージョン内の通信パターン |
| [ピアリング、プロキシ、Transit Gateway](../../domain3.md#t3-3-peer-vs-tgw) | VPC ピアリングと Transit Gateway が適する状況、ピアリング、プロキシ、Transit Gateway の選択、要件に合う接続サービスの実装 |
| [マルチキャスト](../../domain3.md#t3-3-multicast) | VPC とオンプレミスのマルチキャストの実装 |

## 学習の順番 {#study-order}

1. [既定値と上限のまとめ](../../../../services/network-connectivity.md#numbers): 上限のまとめを確認します。
2. [ピアリング](../../../../services/network-connectivity.md#tgw-peering): リージョン間の接続を確認します。
3. [Cloud WAN](../../../../services/network-connectivity.md#cloud-wan): ポリシーで統一する方法を押さえます。
4. [VPC 同士の接続](../../../../services/network-connectivity.md#choosing-multi-vpc): 接続の選択を確認します。
5. [マルチキャスト](../../../../services/network-connectivity.md#tgw-multicast): マルチキャストの制約を覚えます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| VIF の受信経路 | 各 100（プレフィックス制御で 1,000 まで）、公開は 1,000 | 超えると全経路が消える |
| VPN トンネル | 1.25 Gbps | ECMP、LBT |
| VPC アタッチメント | AZ あたり 100 Gbps | Connect のピアは 5 Gbps |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 2 つの VPC で大量の転送 | VPC ピアリング |
| 多数の VPC | Transit Gateway |
| URL の許可と認証 | プロキシのパターン |

## 引っかかりやすい点 {#traps}

- マルチキャストは新規作成時のみ有効にでき、DX と VPN には非対応です。
- ピアリングから移ると MTU が 9001 から 8500 に下がります。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [transit-gateway 問16](../../exercises/transit-gateway.md#q16) | 上限とクォータ | NAT ゲートウェイの ErrorPortAllocation が増えています。同じ宛先（IP とポ… |
| [transit-gateway 問17](../../exercises/transit-gateway.md#q17) | 上限とクォータ | オンプレミスから VIF へ広告する経路が上限を超える場合の動作と、VPC の伝播の上限について正し… |
| [transit-gateway 問18](../../exercises/transit-gateway.md#q18) | 上限とクォータ | 設計書で各接続の帯域の上限を確認しています。VPN は標準のトンネルです。VPN、Connect、V… |
| [transit-gateway 問19](../../exercises/transit-gateway.md#q19) | 通信パターン | 10 リージョンの VPC を、動的な経路と 1 つのポリシーで統一して接続します。リージョン間の経… |
| [transit-gateway 問20](../../exercises/transit-gateway.md#q20) | 通信パターン | 大きなフレームを使うアプリを、東京の VPC と大阪の VPC に分けて配置します。リージョン内とリ… |
| [transit-gateway 問21](../../exercises/transit-gateway.md#q21) | 通信パターン | 本社と支社の DX ロケーションの間の通信が、今はリージョンを経由していて遅延が大きいです。AWS … |
| [transit-gateway 問22](../../exercises/transit-gateway.md#q22) | ピアリング、プロキシ、Transit Gateway | 同じリージョンの 2 つの VPC の間で大量のデータを転送し、費用と MTU を優先します。他の … |
| [transit-gateway 問23](../../exercises/transit-gateway.md#q23) | ピアリング、プロキシ、Transit Gateway | VPC ピアリングから Transit Gateway へ移行します。移行中に大きなパケットだけが消… |
| [transit-gateway 問24](../../exercises/transit-gateway.md#q24) | ピアリング、プロキシ、Transit Gateway | 外向きの HTTP を中央で検査します。要件は「URL で許可し、利用者を認証する」ことです。EC2… |
| [transit-gateway 問25](../../exercises/transit-gateway.md#q25) | マルチキャスト | VPC 内で市場データをマルチキャストで配信します。既存の Transit Gateway はマルチ… |
| [transit-gateway 問26](../../exercises/transit-gateway.md#q26) | マルチキャスト | 金融のデータ配信で、VPC 内の送信元から複数の受信者へマルチキャストします。古い世代のインスタンス… |
| [transit-gateway 問27](../../exercises/transit-gateway.md#q27) | マルチキャスト | オンプレミスの受信者へ、VPC 内の送信元のマルチキャストのデータを届けます。Direct Conn… |

<!-- questions:end -->
