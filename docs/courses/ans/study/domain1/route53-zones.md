# 分野1: Route 53 のゾーンとレコード

DNS の基本、ドメイン登録、公開ゾーンとプライベートゾーンの動作を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [DNS プロトコルの基礎](../../domain1.md#t1-2-dns-protocol) | DNS プロトコル（レコード、TTL、DNSSEC、委任、ゾーン） |
| [ドメイン登録](../../domain1.md#t1-2-domains) | ドメイン登録、ドメイン登録の作成と管理 |
| [公開とプライベート、VPC との統合](../../domain1.md#t1-2-public-private) | Route 53 と VPC などの統合、公開ホストゾーンの利用、プライベートホストゾーンの利用 |

## 学習の順番 {#study-order}

1. [レコード](../../../../services/networking.md#route53-records): レコードの種類を確認します。
2. [TTL とエイリアスの違い](../../../../services/networking.md#route53-ttl): TTL とエイリアスの違いを押さえます。
3. [プライベートホストゾーン](../../../../services/network-connectivity.md#private-hosted-zones): PHZ の解決の順序と NXDOMAIN の動作を理解します。
4. [VPC の DNS 属性](../../../../services/networking.md#vpc-dns-attributes): PHZ に必要な 2 つの属性を覚えます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| 他社からの移管 | 登録または前回の移管から 60 日 | この間は移管できない |
| 別アカウントへの移転 | 受け取りの承認は 3 日以内 | ホストゾーンは移らない |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 切り替えを短時間で | 先に TTL を下げ、古いキャッシュが切れるのを待つ |
| 同じ名前で内外に別の答え | 公開ゾーンと PHZ のスプリットビュー |
| PHZ のプライベートな宛先のヘルスチェック | CloudWatch アラーム型 |

## 引っかかりやすい点 {#traps}

- 一致する PHZ にレコードがないと、公開 DNS へは流れず NXDOMAIN です。
- 登録の移管でレコードやホストゾーンは移りません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [route53-zones 問1](../../exercises/route53-zones.md#q1) | DNS プロトコルの基礎 | ある企業は www.example.com（TTL は 86400 秒）の宛先を、明日の夜に新しい環… |
| [route53-zones 問2](../../exercises/route53-zones.md#q2) | DNS プロトコルの基礎 | 社内の担当者が「api.example.com を別のチームのゾーンに任せたい」と言っています。ex… |
| [route53-zones 問3](../../exercises/route53-zones.md#q3) | DNS プロトコルの基礎 | Web サイトの障害時に Route 53 のフェイルオーバーで切り替える構成で、TTL を 360… |
| [route53-zones 問4](../../exercises/route53-zones.md#q4) | ドメイン登録 | 企業は他社のレジストラで管理するドメインを Route 53 へ移管します。現在の DNS サービス… |
| [route53-zones 問5](../../exercises/route53-zones.md#q5) | ドメイン登録 | 他社のレジストラから Route 53 へ .com のドメインを移管しようとしたところ、移管を開始… |
| [route53-zones 問6](../../exercises/route53-zones.md#q6) | ドメイン登録 | グループ会社の再編で、Route 53 に登録したドメインとそのホストゾーンを、別の AWS アカウ… |
| [route53-zones 問7](../../exercises/route53-zones.md#q7) | 公開とプライベート、VPC との統合 | VPC に PHZ corp.example.com を関連付け、レコードも登録しました。しかし E… |
| [route53-zones 問8](../../exercises/route53-zones.md#q8) | 公開とプライベート、VPC との統合 | 公開ゾーン example.com に www があり、社内向けに同名の PHZ example.c… |
| [route53-zones 問9](../../exercises/route53-zones.md#q9) | 公開とプライベート、VPC との統合 | PHZ のレコードにフェイルオーバーを設定します。プライマリは VPC 内の内部 ALB の背後では… |

<!-- questions:end -->
