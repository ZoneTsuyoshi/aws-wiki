# 分野3: ネットワーク

VPC の構成要素、通信の制御、AWS への接続方法を区別します。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [ネットワークの全体像](../../domain3.md#t3-5-overview) | CloudFront、Global Accelerator、Transit Gateway など |
| [VPC の構成要素](../../domain3.md#t3-5-vpc) | サブネットとゲートウェイ |
| [VPC のセキュリティ](../../domain3.md#t3-5-vpc-security) | セキュリティグループ、ネットワーク ACL、Inspector |
| [Route 53 の目的](../../domain3.md#t3-5-route53) | DNS と振り分け |
| [AWS への接続方法](../../domain3.md#t3-5-connectivity) | VPN と Direct Connect |

## 学習の順番 {#study-order}

1. [サブネットとルートテーブル](../../../../services/networking.md#subnets-route-tables): 構成要素の役割を確認します。
2. [セキュリティグループとネットワーク ACL](../../../../services/networking.md#security-groups-nacls): 比較の表を覚えます。
3. [Route 53](../../../../services/networking.md#route53)と[ルーティングポリシー](../../../../services/networking.md#routing-policies): DNS でできることを確認します。
4. [Site-to-Site VPN](../../../../services/network-connectivity.md#site-to-site-vpn)、[Client VPN](../../../../services/network-connectivity.md#client-vpn)、[Direct Connect](../../../../services/network-connectivity.md#direct-connect): 選ぶ条件を覚えます。
5. [CloudFront](../../../../services/networking.md#cloudfront)、[Global Accelerator](../../../../services/network-connectivity.md#global-accelerator)、[Transit Gateway](../../../../services/network-connectivity.md#transit-gateway): 全体像を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| プライベートサブネットから外へ出る | NAT ゲートウェイ |
| 特定の IP をサブネット単位で拒否する | ネットワーク ACL |
| インスタンス単位で許可する | セキュリティグループ |
| 外から届く経路を報告する | Amazon Inspector |
| 拠点と AWS をすぐ、安く接続する | Site-to-Site VPN |
| 在宅の端末を VPC に接続する | Client VPN |
| 安定した帯域と遅延 | Direct Connect |
| 多数の VPC をまとめて接続する | Transit Gateway |
| 静的コンテンツを速く配信する | CloudFront |

## 引っかかりやすい点 {#traps}

- セキュリティグループには拒否のルールがありません。
- セキュリティグループはステートフル、ネットワーク ACL はステートレスです。
- CloudFront はキャッシュで配信し、Global Accelerator はキャッシュせずに経路を速くします。
- Direct Connect は準備に時間がかかります。「すぐ」なら VPN です。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [networking 問1](../../exercises/networking.md#q1) | ネットワークの全体像 | CloudFront と Global Accelerator の違いの説明として正しいものはどれで… |
| [networking 問2](../../exercises/networking.md#q2) | ネットワークの全体像 | 多数の VPC とオンプレミスの VPN を 1 か所で接続したいと考えています。最も適切なサービス… |
| [networking 問3](../../exercises/networking.md#q3) | ネットワークの全体像 | 要件とサービスの組み合わせとして正しいものはどれですか。（2つ選択） |
| [networking 問4](../../exercises/networking.md#q4) | VPC の構成要素 | プライベートサブネットのインスタンスから外へ通信し、外からの接続は受けないようにしたいと考えています… |
| [networking 問5](../../exercises/networking.md#q5) | VPC の構成要素 | パブリックサブネットの説明として正しいものはどれですか。 |
| [networking 問6](../../exercises/networking.md#q6) | VPC の構成要素 | VPC の構成要素と役割の組み合わせとして正しいものはどれですか。（2つ選択） |
| [networking 問7](../../exercises/networking.md#q7) | VPC のセキュリティ | 特定の攻撃元の IP アドレスをサブネットの単位で拒否したいと考えています。最も適切なものはどれです… |
| [networking 問8](../../exercises/networking.md#q8) | VPC のセキュリティ | セキュリティグループの説明として正しいものはどれですか。 |
| [networking 問9](../../exercises/networking.md#q9) | VPC のセキュリティ | インターネットから EC2 のポートに届く経路があるかを報告してほしいと考えています。最も適切なサー… |
| [networking 問10](../../exercises/networking.md#q10) | VPC のセキュリティ | ネットワーク ACL の説明として正しいものはどれですか。（2つ選択） |
| [networking 問11](../../exercises/networking.md#q11) | Route 53 の目的 | ドメイン名を IP アドレスなどに変換する DNS のサービスはどれですか。 |
| [networking 問12](../../exercises/networking.md#q12) | Route 53 の目的 | Amazon Route 53 でできることはどれですか。（2つ選択） |
| [networking 問13](../../exercises/networking.md#q13) | Route 53 の目的 | 障害の起きたリージョンを避けて、正常なリージョンへ利用者を向けたいと考えています。DNS の段階で行… |
| [networking 問14](../../exercises/networking.md#q14) | AWS への接続方法 | 本社と AWS を今週中に、なるべく費用をかけずに暗号化して接続したいと考えています。最も適切なもの… |
| [networking 問15](../../exercises/networking.md#q15) | AWS への接続方法 | 大量のデータを送るので、安定した帯域と遅延がほしいと考えています。最も適切なものはどれですか。 |
| [networking 問16](../../exercises/networking.md#q16) | AWS への接続方法 | 在宅勤務の社員の端末を VPC に接続したいと考えています。最も適切なものはどれですか。 |

<!-- questions:end -->
