# 分野1: ネットワーク

VPC の接続方式、IP アドレスの設計、検査の配置、IPv6、グローバルなルーティングを、規模と制約から選びます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [1.4.1](../../domain1.md#skill-1-4-1) | マルチ VPC とハイブリッド、マルチアカウントの接続 |
| [1.4.2](../../domain1.md#skill-1-4-2) | サブネット戦略、IP アドレス管理、セグメンテーション |
| [1.4.3](../../domain1.md#skill-1-4-3) | ネットワークセキュリティ |
| [1.4.4](../../domain1.md#skill-1-4-4) | IPv6 とデュアルスタックへの移行 |
| [1.4.5](../../domain1.md#skill-1-4-5) | グローバルなトラフィックルーティング |

## 学習の順番 {#study-order}

1. [VPC 同士の接続](../../../../services/network-connectivity.md#choosing-multi-vpc): 接続の方式を規模で比べます。
2. [VPC ピアリング](../../../../services/network-connectivity.md#vpc-peering)、[Cloud WAN](../../../../services/network-connectivity.md#cloud-wan)、[VPC サブネットの共有](../../../../services/governance.md#ram-vpc-sharing): 各方式の制約を確認します。
3. [IP アドレス設計と IPAM](../../../../services/network-connectivity.md#ip-addressing)、[VPC の CIDR](../../../../services/network-connectivity.md#vpc-cidr)、[Transit Gateway のルートテーブル](../../../../services/network-connectivity.md#tgw-route-tables): 重複の防止と分離の方法を押さえます。
4. [検査の配置](../../../../services/network-connectivity.md#choosing-inspection)、[Network Firewall](../../../../services/network-connectivity.md#network-firewall)、[GWLB による検査](../../../../services/network-connectivity.md#gwlb-inspection)、[アプライアンスモード](../../../../services/network-connectivity.md#tgw-appliance-mode): 層ごとの手段と非対称の経路を理解します。
5. [IPv6 と EIGW](../../../../services/network-connectivity.md#ipv6): デュアルスタックの手順と落とし穴を確認します。
6. [ルーティングポリシー](../../../../services/networking.md#routing-policies)と [Global Accelerator](../../../../services/network-connectivity.md#global-accelerator): DNS で分けるか、固定 IP の裏で分けるかを判断します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| パブリック IPv4 | 1 個 0.005 USD/時 | IPv6 を採用する理由になる |
| DNS64 の接頭辞 | `64:ff9b::/96` | NAT ゲートウェイの NAT64 へ向ける |
| Global Accelerator の固定 IP | IPv4 が 2 個 | エニーキャストで提供 |
| VPC あたりのサービスネットワーク | 関連付けは 1 つ | VPC Lattice の制約 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 少数の VPC、最小の費用 | VPC ピアリング |
| 多数の VPC、1 リージョン | Transit Gateway |
| 多数のリージョン、中央のポリシーとセグメント | Cloud WAN |
| 1 つのサービスを公開、CIDR の重複あり | PrivateLink |
| ネットワークは中央、リソースは各アカウント | VPC サブネットの共有 |
| 組織全体で CIDR の重複を防ぐ | IPAM のプール |
| 本番と開発を分け、共有サービスには接続 | Transit Gateway のルートテーブルを分ける |
| AZ をまたぐときだけステートフルな検査が切れる | アプライアンスモード |
| 許可したドメインだけ外へ、IPS も | Network Firewall |
| 第三者の製品を使い続ける | Gateway Load Balancer |
| IPv6 の外向きだけ | Egress-only インターネットゲートウェイ |
| IPv6 のみから IPv4 の宛先へ | DNS64 と NAT64 |
| 国で必ず分ける | 位置情報ルーティングとデフォルトレコード |
| 固定 IP、TCP、DNS に頼らない切り替え | Global Accelerator |
| 5% ずつ段階的に移す | 加重ルーティング |

## 引っかかりやすい点 {#traps}

- VPC ピアリングは推移的にルーティングできません。
- セキュリティグループには拒否のルールがありません。拒否はネットワーク ACL か WAF で書きます。
- VPC フローログは記録で、通信を止めません。
- IPv6 のルールは IPv4 とは別に評価されます。デュアルスタックにしたら `::/0` のルールを確認します。
- VGW は IPv6 のトラフィックに対応しません。Transit Gateway か Cloud WAN を使います。
- 位置情報ルーティングでは、判定できない IP アドレスがあります。デフォルトレコードを作ります。
- 作成済みのサブネットの CIDR は変更できません。セカンダリ CIDR を追加して新しいサブネットを作ります。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [network 問1](../../exercises/network.md#q1) | 1.4.1 | グローバルな製造業は、7 つのリージョンに数百の VPC とオンプレミス拠点を持ちます。本番、開発、… |
| [network 問2](../../exercises/network.md#q2) | 1.4.1 | SaaS の事業者が、1 つの API を数百の顧客の VPC へ公開します。顧客の VPC の C… |
| [network 問3](../../exercises/network.md#q3) | 1.4.1 | 組織のネットワークチームが、VPC、サブネット、ルートテーブルを一元管理します。各アプリのチームは自… |
| [network 問4](../../exercises/network.md#q4) | 1.4.1 | 3 つの VPC（A、B、C）があり、将来も増える予定はありません。A と B、B と C はピアリ… |
| [network 問5](../../exercises/network.md#q5) | 1.4.2 | M&A により、CIDR の重複が接続の障害になっています。今後は組織全体で重複を防ぎ、OU やリー… |
| [network 問6](../../exercises/network.md#q6) | 1.4.2 | EKS のクラスターの VPC は /24 のサブネットしかなく、Pod の IP アドレスが足りな… |
| [network 問7](../../exercises/network.md#q7) | 1.4.2 | 本番と開発の VPC が同じ Transit Gateway につながっています。監査で「本番と開発… |
| [network 問8](../../exercises/network.md#q8) | 1.4.3 | Transit Gateway に検査用の VPC をつなぎ、すべての VPC 間の通信をステートフ… |
| [network 問9](../../exercises/network.md#q9) | 1.4.3 | 規制の要件で、VPC からインターネットへの通信を、許可したドメインだけに制限します。HTTPS の… |
| [network 問10](../../exercises/network.md#q10) | 1.4.3 | 銀行は長年使っている第三者のファイアウォール製品のルールと運用を、AWS でも使い続けます。複数の … |
| [network 問11](../../exercises/network.md#q11) | 1.4.3 | 公開 ALB の Web アプリで、特定の IP アドレスの範囲からの不正なアクセスが発生しています… |
| [network 問12](../../exercises/network.md#q12) | 1.4.4 | プライベートサブネットの EC2 は、IPv6 でインターネット上の API を呼びます。インターネ… |
| [network 問13](../../exercises/network.md#q13) | 1.4.4 | パブリック IPv4 の費用を減らすため、新しいサブネットを IPv6 のみで作りました。そのサブネ… |
| [network 問14](../../exercises/network.md#q14) | 1.4.4 | Web サービスをデュアルスタックにします。VPC とサブネットに IPv6 の CIDR を割り当… |
| [network 問15](../../exercises/network.md#q15) | 1.4.4 | オンプレミスと AWS の間の Site-to-Site VPN を、IPv6 にも対応させます。現… |
| [network 問16](../../exercises/network.md#q16) | 1.4.5 | ある動画サービスは、法令によりドイツの利用者に EU のリージョンのコンテンツを、その他の国の利用者… |
| [network 問17](../../exercises/network.md#q17) | 1.4.5 | 決済端末のメーカーは、世界の端末から独自の TCP で 2 つのリージョンへ接続します。端末のファー… |
| [network 問18](../../exercises/network.md#q18) | 1.4.5 | Web サービスを新しいリージョンの構成へ移行します。新しい構成には、まず 5% の利用者を送り、問… |

<!-- questions:end -->
