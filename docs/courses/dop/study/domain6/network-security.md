# 分野6: ネットワークセキュリティと証明書

層ごとの役割の違いと、組み合わせを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [ネットワーク](../../domain6.md#t6-2-network) | ネットワークセキュリティの要素 |
| [証明書](../../domain6.md#t6-2-certificates) | 証明書と PKI |
| [多層防御](../../domain6.md#t6-2-defense-in-depth) | 多層防御 |

## 学習の順番 {#study-order}

1. [セキュリティグループとネットワーク ACL](../../../../services/networking.md#security-groups-nacls): ステートフルとステートレスの違いを覚えます。
2. [Network Firewall](../../../../services/threat-detection.md#network-firewall): 境界の検査を確認します。
3. [リージョンのルール](../../../../services/certificates.md#region-rules): リージョンのルールを覚えます。
4. [更新の監視](../../../../services/certificates.md#renewal-monitoring): 期限の監視を確認します。
5. [AWS Private CA](../../../../services/certificates.md#private-ca): 社内の証明書を確認します。
6. [選び方の比較](../../../../services/threat-detection.md#choosing): サービスごとの問いを整理します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 特定の IP を遮断する | ネットワーク ACL |
| 特定のドメインだけを許可する | Network Firewall |
| SQL インジェクションを止める | WAF |
| CloudFront の証明書 | 米国東部（バージニア北部） |
| インポートした証明書の期限 | `DaysToExpiry` か Config のルール |

## 引っかかりやすい点 {#traps}

- ネットワーク ACL では戻りのエフェメラルポートも許可します。
- インポートした証明書は自動更新されません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [network-security 問1](../../exercises/network-security.md#q1) | ネットワーク | 攻撃の IP を遮断するため、サブネットのネットワーク ACL に拒否のルールを追加しました。同時に… |
| [network-security 問2](../../exercises/network-security.md#q2) | ネットワーク | 次の脅威の対策を選びます。(1) VPC から特定のドメインへの通信だけを許可する。(2) API … |
| [network-security 問3](../../exercises/network-security.md#q3) | ネットワーク | プライベートなデータ処理のサブネットで、インターネットへの経路を完全になくしつつ S3 と Dyna… |
| [network-security 問4](../../exercises/network-security.md#q4) | 証明書 | 東京の ALB の前に CloudFront を置き、利用者から CloudFront、CloudF… |
| [network-security 問5](../../exercises/network-security.md#q5) | 証明書 | ACM にインポートした証明書の期限切れで障害が起きました。パブリック証明書には切り替えられません。… |
| [network-security 問6](../../exercises/network-security.md#q6) | 証明書 | 社内のマイクロサービスの間の mTLS の証明書を発行します。公開の CA からの証明書は使いません… |
| [network-security 問7](../../exercises/network-security.md#q7) | 多層防御 | 次の問いに答えるサービスを選びます。(1) 怪しい動きがあるか。(2) ソフトウェアの脆弱性があるか… |
| [network-security 問8](../../exercises/network-security.md#q8) | 多層防御 | 公開の Web アプリに多層防御を入れます。すでに ALB の HTTPS とセキュリティグループが… |
| [network-security 問9](../../exercises/network-security.md#q9) | 多層防御 | GuardDuty、Inspector、Config、Macie の結果を一か所で優先付けし、1 つ… |
| [network-security 問10](../../exercises/network-security.md#q10) | ネットワーク | 3 層の Web アプリの通信を見直します。DB のセキュリティグループで、アプリ層の IP 範囲を… |

<!-- questions:end -->
