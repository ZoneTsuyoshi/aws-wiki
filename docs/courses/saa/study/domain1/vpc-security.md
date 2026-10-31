# 分野1: VPC のセキュリティ

どの通信をどの部品で止めるかを、適用先とステートの違いで判断します。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [VPC のセキュリティ部品と通信の制御](../../domain1.md#t1-2-vpc-security) | ポート、プロトコル、ネットワークトラフィックの制御、セキュリティ部品を含む VPC の設計 |
| [ネットワークの分割](../../domain1.md#t1-2-segmentation) | ネットワーク分割の戦略 |
| [サービスエンドポイント](../../domain1.md#t1-2-endpoints) | AWS サービスのエンドポイント |
| [外部ネットワークとの安全な接続](../../domain1.md#t1-2-external) | AWS との外部接続の保護 |

## 学習の順番 {#study-order}

1. [セキュリティグループとネットワーク ACL](../../../../services/networking.md#security-groups-nacls)と[セキュリティグループのルール](../../../../services/networking.md#security-group-rules): SG と NACL の違いと、SG の送信元に SG を指定する方法を覚えます。
2. [ネットワーク ACL のルール](../../../../services/networking.md#nacl-rules)と[NAT ゲートウェイ](../../../../services/network-connectivity.md#nat-gateway): 戻り通信のポートと、NAT ゲートウェイの制約を確認します。
3. [サブネットとルートテーブル](../../../../services/networking.md#subnets-route-tables)と[Session Manager](../../../../services/operations.md#session-manager): サブネットの種類を決めるものと、ポートを開けない管理接続を押さえます。
4. [VPC エンドポイントと PrivateLink](../../../../services/networking.md#vpc-endpoints)と[エンドポイントの選び方と制約](../../../../services/networking.md#endpoint-settings): ゲートウェイとインターフェイスの違いを表で比べます。
5. [エンドポイントポリシー](../../../../services/networking.md#endpoint-policies): エンドポイント側の制限と、バケット側の `aws:SourceVpce` を区別します。
6. [Site-to-Site VPN](../../../../services/network-connectivity.md#site-to-site-vpn)と[MACsec](../../../../services/network-connectivity.md#dx-macsec): 拠点間の暗号化の方法を比べます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| NACL の戻りポート | 1024〜65535（NAT ゲートウェイ） | ステートレスなので明示的に許可する |
| MACsec | 10、100、400 Gbps の専用接続 | ルーターまでの暗号化 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| ALB からの通信だけをアプリで受ける | アプリの SG の送信元に ALB の SG を指定する |
| 特定の IP を拒否する | NACL、または WAF |
| オンプレミスから S3 にプライベートに接続する | S3 のインターフェイスエンドポイント |
| 追加料金なしで VPC から S3 へ | S3 のゲートウェイエンドポイント |
| 専用線で VPC まで暗号化する | Direct Connect の上のプライベート IP VPN |
| 従業員の端末から VPC へ | Client VPN |

## 引っかかりやすい点 {#traps}

- SG に拒否ルールはありません。
- NAT ゲートウェイには SG を付けられず、外からの接続も受けません。
- Direct Connect は既定では暗号化されません。
- ゲートウェイエンドポイントはオンプレミスから使えません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [vpc-security 問1](../../exercises/vpc-security.md#q1) | VPC のセキュリティ部品 | ALB の後ろのアプリのインスタンスは、ALB からの 443 だけを受けます。ALB の IP は… |
| [vpc-security 問2](../../exercises/vpc-security.md#q2) | VPC のセキュリティ部品 | 特定の IP アドレスからの攻撃を、サブネットの単位で止めます。どれを使いますか。 |
| [vpc-security 問3](../../exercises/vpc-security.md#q3) | VPC のセキュリティ部品 | 自作の NACL をプライベートサブネットに付けたところ、NAT ゲートウェイ経由でインターネットの… |
| [vpc-security 問4](../../exercises/vpc-security.md#q4) | VPC のセキュリティ部品 | NAT ゲートウェイの説明として正しいものを選んでください。（2つ選択） |
| [vpc-security 問5](../../exercises/vpc-security.md#q5) | VPC のセキュリティ部品 | SG と NACL の違いとして正しいものを選んでください。（2つ選択） |
| [vpc-security 問6](../../exercises/vpc-security.md#q6) | ネットワークの分割 | あるサブネットがパブリックであるかを決めるものはどれですか。 |
| [vpc-security 問7](../../exercises/vpc-security.md#q7) | ネットワークの分割 | 3 層の Web アプリをネットワークで分けます。DB にインターネットへの経路を持たせない配置はど… |
| [vpc-security 問8](../../exercises/vpc-security.md#q8) | ネットワークの分割 | プライベートサブネットのインスタンスに管理の接続をします。インバウンドのポートを開けず、踏み台も置き… |
| [vpc-security 問9](../../exercises/vpc-security.md#q9) | サービスエンドポイント | プライベートサブネットの EC2 が S3 に大量のデータを送っています。通信をインターネットに出さ… |
| [vpc-security 問10](../../exercises/vpc-security.md#q10) | サービスエンドポイント | オンプレミスから Direct Connect 経由で、S3 にプライベートに接続します。適切なもの… |
| [vpc-security 問11](../../exercises/vpc-security.md#q11) | サービスエンドポイント | バケットへのアクセスを、特定の VPC エンドポイントからだけに限定します。どう設定しますか。 |
| [vpc-security 問12](../../exercises/vpc-security.md#q12) | サービスエンドポイント | VPC エンドポイントの比較で正しいものを選んでください。（2つ選択） |
| [vpc-security 問13](../../exercises/vpc-security.md#q13) | 外部との接続 | 本社と VPC を暗号化された回線で今週中につなぎます。専用線の開通を待てません。何を選びますか。 |
| [vpc-security 問14](../../exercises/vpc-security.md#q14) | 外部との接続 | Direct Connect の通信を、ルーターから AWS のデバイスまでの区間で暗号化します。1… |
| [vpc-security 問15](../../exercises/vpc-security.md#q15) | 外部との接続 | Direct Connect の専用線を使い、オンプレミスから VPC まで IPsec で暗号化し… |
| [vpc-security 問16](../../exercises/vpc-security.md#q16) | 外部との接続 | 在宅の従業員 300 人が、各自の端末から VPC の内部アプリへ接続します。OpenVPN ベース… |

<!-- questions:end -->
