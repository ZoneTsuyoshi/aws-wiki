# 分野2: VPC の構成とエンドポイント

PrivateLink の実装と、VPC のネットワークサービスの構成を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [PrivateLink](../../domain2.md#t2-2-privatelink) | アプリのプライベート接続（PrivateLink） |
| [VPC のサービス](../../domain2.md#t2-1-vpc-services) | VPC のネットワークサービス |
| [単一と複数の VPC](../../domain2.md#t2-2-single-multi-vpc) | 単一、複数の VPC の構成（DHCP、ルーティング、SG） |

## 学習の順番 {#study-order}

1. [VPC エンドポイントと PrivateLink](../../../../services/networking.md#vpc-endpoints): 提供側と利用側の手順を確認します。
2. [エンドポイントの選び方と制約](../../../../services/networking.md#endpoint-settings): インターフェイスとゲートウェイの違いを覚えます。
3. [NAT ゲートウェイ](../../../../services/network-connectivity.md#nat-gateway): NAT の経路の制約を押さえます。
4. [サブネットとルートテーブル](../../../../services/networking.md#subnets-route-tables): VPC の構成の順序を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| NAT の接続 | 同じ宛先へ IP あたり 55,000 | `ErrorPortAllocation` |
| DHCP オプションセット | VPC に 1 つ | 1 つのセットは複数の VPC へ |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| オンプレミスから VGW 経由で NAT へ | 出られない。Transit Gateway の集中型 |
| 接続が `pendingAcceptance` | 提供者が承認する |

## 引っかかりやすい点 {#traps}

- 両側の AZ が重ならないと接続できません。
- 独自の DNS を指定すると、DNS64 や DNS Firewall は VPC Resolver を通るときだけ効きます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [vpc-endpoints 問1](../../exercises/vpc-endpoints.md#q1) | PrivateLink | アカウント A の API を、NLB の背後からアカウント B の VPC へ PrivateLi… |
| [vpc-endpoints 問2](../../exercises/vpc-endpoints.md#q2) | PrivateLink | PrivateLink のエンドポイントサービスを ap-northeast-1a と 1c の N… |
| [vpc-endpoints 問3](../../exercises/vpc-endpoints.md#q3) | PrivateLink | オンプレミスから DX 経由で、VPC のインターフェイスエンドポイントを使って AWS サービスの… |
| [vpc-endpoints 問10](../../exercises/vpc-endpoints.md#q10) | VPC のサービス | オンプレミスから VPC の NAT ゲートウェイを通ってインターネットへ出す構成を検討しています。… |
| [vpc-endpoints 問11](../../exercises/vpc-endpoints.md#q11) | VPC のサービス | IPv6 のみのプライベートサブネットの EC2 からインターネットへ接続します。インターネットから… |
| [vpc-endpoints 問12](../../exercises/vpc-endpoints.md#q12) | VPC のサービス | プライベートサブネットのバッチが、同じ外部 API へ多数の接続を開いています。接続のエラーが増え、… |
| [vpc-endpoints 問13](../../exercises/vpc-endpoints.md#q13) | 単一と複数の VPC | 新しい VPC を DHCP オプションセットと一緒に設計します。VPC には既定の DHCP オプ… |
| [vpc-endpoints 問14](../../exercises/vpc-endpoints.md#q14) | 単一と複数の VPC | 同じリージョンの VPC ピアリングで、Web 層の VPC の SG から App 層の VPC … |
| [vpc-endpoints 問15](../../exercises/vpc-endpoints.md#q15) | 単一と複数の VPC | Windows のサーバーが多い VPC で、DHCP オプションセットを変更します。IPv6 のみ… |

<!-- questions:end -->
