# 分野1: 脅威の検出と防御

名前が似たサービスを「何を見るか」で見分けます。攻撃の種類と守る場所も対応させます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [セキュリティサービスの使い分け](../../domain1.md#t1-2-security-services) | セキュリティサービスの適切な用途 |
| [外部の脅威への対策](../../domain1.md#t1-2-threats) | AWS の外部からの脅威、アプリケーションを保護するサービスの統合 |

## 学習の順番 {#study-order}

1. [選び方の比較](../../../../services/threat-detection.md#choosing): 各サービスが見るものの比較を、最初に確認します。
2. [GuardDuty](../../../../services/threat-detection.md#guardduty)と[Inspector](../../../../services/threat-detection.md#inspector): 活動の検出と脆弱性の評価の違いを押さえます。
3. [Macie](../../../../services/threat-detection.md#macie)と[Detective](../../../../services/threat-detection.md#detective): 機密データの発見と、原因の調査を区別します。
4. [Security Hub](../../../../services/threat-detection.md#security-hub)と[Firewall Manager](../../../../services/threat-detection.md#firewall-manager): 集約と展開の役割を分けます。
5. [AWS WAF](../../../../services/certificates.md#waf)と[レートベースルール](../../../../services/certificates.md#rate-based-rules): マネージドルールとレートベースルールの使いどころを覚えます。
6. [Shield](../../../../services/threat-detection.md#shield)と[Network Firewall](../../../../services/threat-detection.md#network-firewall): 量の攻撃への防御と、VPC の検査を確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 不審な API 呼び出し、マイニングの疑い | GuardDuty |
| CVE、パッチの漏れ | Inspector |
| 個人情報がどのバケットにあるか | Macie |
| 検出結果の根本原因を調べる | Detective |
| 組織の検出結果を 1 か所に集める | Security Hub |
| WAF のルールを複数アカウントに展開する | Firewall Manager |
| SQL インジェクション、XSS | WAF のマネージドルール |
| 大規模な DDoS と専門チームの支援 | Shield Advanced |
| 悪意のあるドメインの名前解決を止める | DNS Firewall |

## 引っかかりやすい点 {#traps}

- Shield は量の攻撃、WAF はリクエストの中身を扱います。L7 の DDoS には両方を組み合わせます。
- SG と NACL はリクエストの中身を見られません。
- EC2 と NLB を Shield Advanced で守るときは、Elastic IP を関連付けます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [threat-protection 問1](../../exercises/threat-protection.md#q1) | セキュリティサービス | 多数のバケットのうち、個人情報がどのバケットに入っているかを調べます。どれを使いますか。 |
| [threat-protection 問2](../../exercises/threat-protection.md#q2) | セキュリティサービス | EC2 インスタンスが暗号通貨のマイニングに使われている疑いや、不審な API 呼び出しを、エージェ… |
| [threat-protection 問3](../../exercises/threat-protection.md#q3) | セキュリティサービス | ECR のコンテナイメージと EC2 のパッケージに、既知の CVE がないかを継続して評価します。… |
| [threat-protection 問4](../../exercises/threat-protection.md#q4) | セキュリティサービス | GuardDuty の検出結果について、関連するリソースと時系列をたどって根本原因を調べます。どれが… |
| [threat-protection 問5](../../exercises/threat-protection.md#q5) | セキュリティサービス | 組織の全アカウントの GuardDuty、Inspector、Macie の検出結果を 1 か所に集… |
| [threat-protection 問6](../../exercises/threat-protection.md#q6) | 外部の脅威 | ALB の後ろの Web アプリに SQL インジェクションの試行が続いています。アプリの改修まで、… |
| [threat-protection 問7](../../exercises/threat-protection.md#q7) | 外部の脅威 | 特定の IP から短時間に大量のリクエストが来る、ログイン画面への攻撃を自動で抑えます。CloudF… |
| [threat-protection 問8](../../exercises/threat-protection.md#q8) | 外部の脅威 | 重要な公開サイトで、大規模な DDoS に備えます。専門チームの支援と、攻撃によるスケーリング費用の… |
| [threat-protection 問9](../../exercises/threat-protection.md#q9) | 外部の脅威 | Shield Advanced で保護できる対象の組み合わせとして正しいものはどれですか。 |
| [threat-protection 問10](../../exercises/threat-protection.md#q10) | 外部の脅威 | VPC の全通信を、ステートフルなルールと侵入防止のシグネチャで検査します。ファイアウォールの機器は… |
| [threat-protection 問11](../../exercises/threat-protection.md#q11) | 外部の脅威 | VPC のワークロードが悪意のあるドメインを名前解決することを止めます。どれを使いますか。 |

<!-- questions:end -->
