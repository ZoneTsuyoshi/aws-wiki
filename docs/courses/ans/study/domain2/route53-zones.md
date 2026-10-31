# 分野2: Route 53 のゾーンとレコード

ゾーンの選択、委任、レコード、DNSSEC の実装を問います。分野2で最も設定値を問うところです。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [ゾーンの選択と転送](../../domain2.md#t2-3-zones) | プライベートと公開のホストゾーンの使い分け、DNS ゾーンと条件付き転送の構成 |
| [委任と転送](../../domain2.md#t2-3-delegation) | DNS の委任と転送、DNS ゾーンと条件付き転送の構成 |
| [レコード](../../domain2.md#t2-3-records) | レコードの種類（A、AAAA、TXT、PTR、エイリアス）、適切なレコードの構成 |
| [DNSSEC](../../domain2.md#t2-3-dnssec) | DNSSEC、Route 53 の DNSSEC の構成 |

## 学習の順番 {#study-order}

1. [レコード](../../../../services/networking.md#route53-records): レコードの用途と注意を確認します。
2. [TTL とエイリアスの違い](../../../../services/networking.md#route53-ttl): エイリアスと TTL の扱いを覚えます。
3. [プライベートホストゾーン](../../../../services/network-connectivity.md#private-hosted-zones): PHZ と DNSSEC の項目を確認します。
4. [転送ルール](../../../../services/network-connectivity.md#resolver-rules): ルールの優先と System ルールを押さえます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| KSK の元のキー | `us-east-1`、`ECC_NIST_P256` | ゾーンあたり KSK は 2 つまで |
| 署名ゾーンの TTL | 最大 1 週間 | 超えても 1 週間に制限 |
| サブドメインの委任 | 親に NS を 4 つ | `NS` レコードで委任 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 署名を有効にした後 | 親に DS レコードを登録 |
| 署名を止める | 親の DS を先に削除し、TTL を待つ |
| `example.com` のルールの例外 | System ルールで個別の名前を解決 |

## 引っかかりやすい点 {#traps}

- PHZ は署名できません。
- Resolver ルールは PHZ より優先されます。
- KMS キーの権限の変更で KSK が `ACTION_NEEDED` になります。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [route53-zones 問10](../../exercises/route53-zones.md#q10) | ゾーンの選択と転送 | VPC に PHZ example.com を関連付けています。別のチームが、オンプレミスの DNS… |
| [route53-zones 問11](../../exercises/route53-zones.md#q11) | ゾーンの選択と転送 | example.com をオンプレミスへ転送する Forward ルールを全 VPC に適用していま… |
| [route53-zones 問12](../../exercises/route53-zones.md#q12) | ゾーンの選択と転送 | 社内ポータル portal.example.com は、社外からは CloudFront へ、VPC… |
| [route53-zones 問13](../../exercises/route53-zones.md#q13) | 委任と転送 | 親ドメイン example.com は他社の DNS で運用を続けながら、aws.example.c… |
| [route53-zones 問14](../../exercises/route53-zones.md#q14) | 委任と転送 | オンプレミスの DNS は corp.example.com を管理しており、VPC からの問い合わ… |
| [route53-zones 問15](../../exercises/route53-zones.md#q15) | 委任と転送 | 企業はオンプレミスの DNS を権威としつつ、サブドメイン cloud.corp.example.c… |
| [route53-zones 問16](../../exercises/route53-zones.md#q16) | レコード | ゾーンの頂点 example.com を、ALB へ向けます。ALB の IP は変わるので値を固定… |
| [route53-zones 問17](../../exercises/route53-zones.md#q17) | レコード | Web サイトをデュアルスタックの ALB で公開します。IPv6 のクライアントが AAAA を問… |
| [route53-zones 問18](../../exercises/route53-zones.md#q18) | レコード | VPC 内のメールサーバーのログ解析で、プライベート IP からホスト名を引きたいと考えています。オ… |
| [route53-zones 問19](../../exercises/route53-zones.md#q19) | レコード | Route 53 のレコードの種類について、誤った設計を指摘するレビューをしています。問題がある案は… |
| [route53-zones 問20](../../exercises/route53-zones.md#q20) | DNSSEC | Route 53 の公開ホストゾーンで DNSSEC 署名を有効にします。監査の要件で、署名の鍵の元… |
| [route53-zones 問21](../../exercises/route53-zones.md#q21) | DNSSEC | 公開ゾーンの DNSSEC 署名を有効にし、KSK も ACTIVE です。しかし監査のテストで、信… |
| [route53-zones 問22](../../exercises/route53-zones.md#q22) | DNSSEC | 本番ゾーンで DNSSEC 署名を有効にした後、担当者が権限の整理で KMS のキーポリシーを変更し… |
| [route53-zones 問23](../../exercises/route53-zones.md#q23) | DNSSEC | 公開ゾーンと PHZ の両方を持つチームが、DNSSEC の適用範囲を検討しています。ゾーンの一部の… |
| [route53-zones 問24](../../exercises/route53-zones.md#q24) | DNSSEC | 公開ゾーンの DNSSEC 署名を運用していますが、DNS プロバイダーの移行のため署名を止めること… |

<!-- questions:end -->
