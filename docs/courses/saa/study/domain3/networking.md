# 分野3: ネットワークの性能と設計

エッジ、IP の設計、トポロジー、接続、配置、負荷分散を選びます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [エッジネットワーキング](../../domain3.md#t3-4-edge) | エッジネットワークサービスの適切な用途 |
| [ネットワークの設計とスケール](../../domain3.md#t3-4-design) | ネットワークアーキテクチャの設計方法、将来の需要に対応できるネットワーク設定の判断 |
| [ネットワークトポロジー](../../domain3.md#t3-4-topology) | さまざまなアーキテクチャのネットワークトポロジーの作成 |
| [ネットワーク接続の選択肢](../../domain3.md#t3-4-connections) | ネットワーク接続の選択肢 |
| [リソースの配置](../../domain3.md#t3-4-placement) | 業務要件を満たすリソースの配置の判断 |
| [負荷分散の戦略](../../domain3.md#t3-4-lb) | 負荷分散の概念、適切な負荷分散の戦略の選択 |

## 学習の順番 {#study-order}

1. [CloudFront](../../../../services/networking.md#cloudfront)と[Global Accelerator](../../../../services/network-connectivity.md#global-accelerator): 2 つのエッジのサービスを比べます。
2. [キャッシュキーとポリシー](../../../../services/networking.md#cache-keys): ヒット率に効く設定を確認します。
3. [VPC の基本](../../../../services/networking.md#vpc)と[VPC の CIDR](../../../../services/network-connectivity.md#vpc-cidr): 予約される IP と、CIDR の選び方を押さえます。
4. [Transit Gateway](../../../../services/network-connectivity.md#transit-gateway)と[ハイブリッド DNS](../../../../services/network-connectivity.md#hybrid-dns): ハブアンドスポークとハイブリッド DNS を確認します。
5. [接続の種類](../../../../services/network-connectivity.md#dx-connections)と[トンネル](../../../../services/network-connectivity.md#vpn-tunnels): 接続の速度の目安を覚えます。
6. [プレイスメントグループ](../../../../services/operations.md#placement-groups)と[Outposts、Local Zones、Wavelength のネットワーク](../../../../services/network-connectivity.md#edge-infrastructure): 配置の選択を確認します。
7. [ALB と NLB の違い](../../../../services/networking.md#alb-vs-nlb)と[GWLB](../../../../services/networking.md#gwlb): ロードバランサーの違いを比べます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| サブネットの予約 | 5 個 | `/24` で使えるのは 251 個 |
| Global Accelerator | 固定の IPv4 が 2 個 | TCP と UDP |
| VPN のトンネル | 1.25 Gbps。Large Bandwidth Tunnel は 5 Gbps | 束ねるなら Transit Gateway の ECMP |
| 専用接続 | 1、10、100、400 Gbps | 開通に時間がかかる |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| UDP のゲームを AWS のネットワークへ | Global Accelerator |
| 静的コンテンツをキャッシュで高速化 | CloudFront |
| IP が足りない | セカンダリ CIDR |
| IPv6 の外向きだけ | Egress-only インターネットゲートウェイ |
| 多数の VPC とオンプレミス | Transit Gateway |
| 1 つのサービスだけを公開、CIDR が重複 | PrivateLink |
| パスで振り分け、Lambda をターゲット | ALB |
| 第三者のファイアウォールを挟む | GWLB |

## 引っかかりやすい点 {#traps}

- ピアリングは CIDR が一部でも重複すると作れません。
- NLB のクロスゾーン負荷分散は既定で無効です。ALB はロードバランサーのレベルで常に有効です。
- DB はパブリックサブネットに置きません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [networking 問1](../../exercises/networking.md#q1) | エッジネットワーキング | ゲームの UDP の通信を、世界中の利用者から AWS のネットワークに早く乗せます。キャッシュはし… |
| [networking 問2](../../exercises/networking.md#q2) | エッジネットワーキング | 静的コンテンツと API を同じドメインで高速化します。キャッシュでオリジンの負荷も減らします。どれ… |
| [networking 問3](../../exercises/networking.md#q3) | エッジネットワーキング | キャッシュのヒット率が低いです。CloudFront のキャッシュキーに全ヘッダーと全 Cookie… |
| [networking 問4](../../exercises/networking.md#q4) | エッジネットワーキング | CloudFront と Global Accelerator の違いで正しいものを選んでください。… |
| [networking 問5](../../exercises/networking.md#q5) | ネットワークの設計 | 10.0.0.0/24 のサブネットで使える IP はいくつですか。 |
| [networking 問6](../../exercises/networking.md#q6) | ネットワークの設計 | 既存の VPC で IP が足りなくなりました。サブネットを追加するため、最小の変更で範囲を増やしま… |
| [networking 問7](../../exercises/networking.md#q7) | ネットワークの設計 | 将来、オンプレミスや他の VPC とつなぐ可能性があります。CIDR を選ぶときの注意はどれですか。 |
| [networking 問8](../../exercises/networking.md#q8) | ネットワークの設計 | IPv6 のインスタンスから外への通信だけを許可し、外からの接続は受けません。何を使いますか。 |
| [networking 問9](../../exercises/networking.md#q9) | ネットワークトポロジー | 50 の VPC とオンプレミスの Direct Connect をつなぎ、さらに増えます。どのトポ… |
| [networking 問10](../../exercises/networking.md#q10) | ネットワークトポロジー | 東京と大阪の Transit Gateway をつないで、リージョンをまたぐ通信を流します。どの機能… |
| [networking 問11](../../exercises/networking.md#q11) | ネットワークトポロジー | オンプレミスの DNS で VPC のプライベートホストゾーンの名前を解決します。VPC からもオン… |
| [networking 問12](../../exercises/networking.md#q12) | ネットワーク接続の選択肢 | 既存の Direct Connect を使い、1 Gbps を安定して確保します。パートナーの提供す… |
| [networking 問13](../../exercises/networking.md#q13) | ネットワーク接続の選択肢 | 取引先の VPC に、自社の 1 つのサービスだけを公開します。お互いの CIDR は重複しています… |
| [networking 問14](../../exercises/networking.md#q14) | ネットワーク接続の選択肢 | 標準の Site-to-Site VPN のトンネル 1 本の帯域の目安はどれですか。 |
| [networking 問15](../../exercises/networking.md#q15) | リソースの配置 | インターネットから受ける Web アプリのリソースの配置として適切なものはどれですか。 |
| [networking 問16](../../exercises/networking.md#q16) | リソースの配置 | 複数のノードで低遅延の通信を行い、AZ の障害には別の方法で備えます。配置はどれですか。 |
| [networking 問17](../../exercises/networking.md#q17) | リソースの配置 | 規制でデータを自社の施設に置きますが、AWS の API と同じ運用を使います。どこに配置しますか。 |
| [networking 問18](../../exercises/networking.md#q18) | 負荷分散の戦略 | HTTP のパスとホストで振り分け、Lambda と EC2 をターゲットにします。認証も連携します… |
| [networking 問19](../../exercises/networking.md#q19) | 負荷分散の戦略 | 第三者の次世代ファイアウォールの仮想アプライアンスを、全通信に透過的に挟みます。どれを選びますか。 |
| [networking 問20](../../exercises/networking.md#q20) | 負荷分散の戦略 | NLB でクロスゾーン負荷分散について正しいものはどれですか。 |
| [networking 問21](../../exercises/networking.md#q21) | 負荷分散の戦略 | ALB の後ろのサーバーで、利用者の送信元 IP を記録します。どこから取得しますか。 |

<!-- questions:end -->
