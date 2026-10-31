# 分野2: セキュリティのサービスと情報源

防御、展開、点検のサービスの役割と、情報の探し先を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [AWS のセキュリティ機能とサービス](../../domain2.md#t2-4-capabilities) | WAF、Shield、Firewall Manager、GuardDuty |
| [Marketplace のセキュリティ製品](../../domain2.md#t2-4-marketplace) | サードパーティの製品 |
| [セキュリティの情報源](../../domain2.md#t2-4-docs) | Security Center、Security Blog、Knowledge Center |
| [問題を見つけるサービス](../../domain2.md#t2-4-trusted-advisor) | Trusted Advisor の点検 |

## 学習の順番 {#study-order}

1. [AWS WAF](../../../../services/certificates.md#waf)と[Shield](../../../../services/threat-detection.md#shield): 守る層の違いを確認します。
2. [Firewall Manager](../../../../services/threat-detection.md#firewall-manager): 展開のサービスで、検査は行わないことを確認します。
3. [Trusted Advisor](../../../../services/cloud-foundations.md#trusted-advisor): 助言のサービスで、自動では修正しないことを確認します。
4. [AWS Marketplace](../../../../services/cloud-foundations.md#marketplace)と[サポートの情報源](../../../../services/cloud-foundations.md#support-resources): 製品と情報の探し先を覚えます。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| SQL インジェクションや特定の IP を止める | AWS WAF |
| DDoS から守る | AWS Shield |
| 全アカウントに同じ WAF ルールを強制する | AWS Firewall Manager |
| 設定の弱点を見つける | Trusted Advisor |
| 実際の不審な動きを見つける | GuardDuty |
| AWS にない機能の製品を買う | AWS Marketplace |
| よくある質問と解決方法を調べる | AWS Knowledge Center |

## 引っかかりやすい点 {#traps}

- Shield Standard は全利用者に追加料金なしで適用されます。Advanced は有料です。
- Trusted Advisor の使えるチェックは、サポートプランで変わります。
- Marketplace の料金は AWS の請求書にまとまります。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [security-services 問1](../../exercises/security-services.md#q1) | AWS のセキュリティ機能とサービス | Web アプリへの SQL インジェクションや、特定の IP からのリクエストを止めたいと考えていま… |
| [security-services 問2](../../exercises/security-services.md#q2) | AWS のセキュリティ機能とサービス | AWS Shield の説明として正しいものはどれですか。 |
| [security-services 問3](../../exercises/security-services.md#q3) | AWS のセキュリティ機能とサービス | 50 個のアカウントがある組織で、すべての ALB に同じ WAF ルールを適用し、新しいアカウント… |
| [security-services 問4](../../exercises/security-services.md#q4) | AWS のセキュリティ機能とサービス | 要件とサービスの組み合わせとして正しいものはどれですか。（2つ選択） |
| [security-services 問5](../../exercises/security-services.md#q5) | Marketplace のセキュリティ製品 | 社内で使っている他社のファイアウォール製品を、AWS でも使いたいと考えています。探して購入できる場… |
| [security-services 問6](../../exercises/security-services.md#q6) | Marketplace のセキュリティ製品 | AWS Marketplace でサードパーティのセキュリティ製品を購入したときの請求の説明として正… |
| [security-services 問7](../../exercises/security-services.md#q7) | Marketplace のセキュリティ製品 | AWS Marketplace のセキュリティ製品を検討する場面として最も適切なものはどれですか。 |
| [security-services 問8](../../exercises/security-services.md#q8) | セキュリティの情報源 | AWS のセキュリティの新機能や手法の解説記事を読みたいと考えています。最も適切な情報源はどれですか… |
| [security-services 問9](../../exercises/security-services.md#q9) | セキュリティの情報源 | セキュリティに関するよくある質問と解決方法を調べたいと考えています。最も適切な情報源はどれですか。 |
| [security-services 問10](../../exercises/security-services.md#q10) | セキュリティの情報源 | 情報の種類と情報源の組み合わせとして正しいものはどれですか。（2つ選択） |
| [security-services 問11](../../exercises/security-services.md#q11) | 問題を見つけるサービス | 環境を点検して、ルートの MFA の未設定や、公開スナップショットを指摘してほしいと考えています。最… |
| [security-services 問12](../../exercises/security-services.md#q12) | 問題を見つけるサービス | AWS Trusted Advisor の説明として正しいものはどれですか。 |
| [security-services 問13](../../exercises/security-services.md#q13) | 問題を見つけるサービス | 見つけたいものとサービスの組み合わせとして正しいものはどれですか。 |

<!-- questions:end -->
