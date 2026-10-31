# 分野4: 暗号化と証明書

暗号化の選択肢、サービスごとの転送時の暗号化、証明書、責任の分担を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [暗号化の選択肢](../../domain4.md#t4-3-options) | AWS の暗号化の選択肢、要件を満たす暗号化の実装（IPsec、TLS） |
| [サービスごとの暗号化](../../domain4.md#t4-3-in-transit) | 転送時の暗号化の実装（CloudFront、ALB、NLB、VPN over DX、マネージド DB、S3、EC2、Transit Gateway） |
| [証明書の管理](../../domain4.md#t4-3-certificates) | 証明書管理の実装（ACM、Private CA） |
| [責任共有モデル](../../domain4.md#t4-3-shared-responsibility) | 責任共有モデルと暗号化 |

## 学習の順番 {#study-order}

1. [MACsec](../../../../services/network-connectivity.md#dx-macsec): `must_encrypt` と範囲を確認します。
2. [プライベート IP VPN](../../../../services/network-connectivity.md#vpn-private-ip): VPC までの暗号化を押さえます。
3. [転送時の TLS](../../../../services/certificates.md#tls-in-transit): サービスごとの設定を確認します。
4. [リージョンのルール](../../../../services/certificates.md#region-rules): 証明書のリージョンを覚えます。
5. [AWS Private CA](../../../../services/certificates.md#private-ca): 社内の証明書を確認します。
6. [責任共有モデル](../../../../services/cloud-foundations.md#shared-responsibility): 責任の分担を整理します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| MACsec のポート | 10、100、400 Gbps | ルーターと DX ロケーションの間 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 暗号化できないなら止める | MACsec の `must_encrypt` |
| S3 の TLS を強制 | `aws:SecureTransport` |
| 社内の mTLS | AWS Private CA |

## 引っかかりやすい点 {#traps}

- DX は既定で暗号化されません。
- Transit Gateway ピアリングの暗号化は同じリージョンの区間には当てはまりません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [encryption 問1](../../exercises/encryption.md#q1) | 暗号化の選択肢 | 金融の監査で「100 Gbps の DX で全通信を暗号化し、暗号化できないなら通信を止めること」を… |
| [encryption 問2](../../exercises/encryption.md#q2) | 暗号化の選択肢 | 追加の監査で、DX ロケーションから VPC までの暗号化と、アプリの間の相互認証が必要になりました… |
| [encryption 問3](../../exercises/encryption.md#q3) | 暗号化の選択肢 | 暗号化の方法の表をレビューしています。方法と範囲の組み合わせで正しいものはどれですか。 |
| [encryption 問4](../../exercises/encryption.md#q4) | サービスごとの暗号化 | CloudFront でビューワーとの通信を HTTPS に限定し、HTTP のアクセスは自動で誘導… |
| [encryption 問5](../../exercises/encryption.md#q5) | サービスごとの暗号化 | S3 のバケットへ HTTP でアクセスするクライアントが残っていることが監査で分かりました。今後は… |
| [encryption 問6](../../exercises/encryption.md#q6) | サービスごとの暗号化 | 東京の VPC 間は Transit Gateway、東京と大阪の間は Transit Gatewa… |
| [encryption 問7](../../exercises/encryption.md#q7) | サービスごとの暗号化 | ElastiCache（Redis）へのアプリの通信と、RDS への通信を暗号化します。アプリは接続… |
| [encryption 問8](../../exercises/encryption.md#q8) | 証明書の管理 | 東京の ALB と CloudFront で同じドメインの ACM の証明書を使います。CloudF… |
| [encryption 問9](../../exercises/encryption.md#q9) | 証明書の管理 | 社内のマイクロサービスの mTLS に使う証明書を発行します。ブラウザーの信頼は不要で、信頼のルート… |
| [encryption 問10](../../exercises/encryption.md#q10) | 証明書の管理 | ACM の DNS 検証の証明書が更新に失敗しました。担当者が検証の CNAME を消していたことが… |
| [encryption 問11](../../exercises/encryption.md#q11) | 責任共有モデル | 監査で「DX は専用線だから暗号化は不要」という社内文書が指摘されました。データは規制の対象です。責… |
| [encryption 問12](../../exercises/encryption.md#q12) | 責任共有モデル | 暗号化の責任の分担の表をレビューしています。組み合わせで正しいものを選んでください。（2つ選択） |
| [encryption 問13](../../exercises/encryption.md#q13) | 責任共有モデル | EC2 で動く独自の TCP サービスの通信を暗号化します。ACM の証明書を EC2 に置きたいと… |

<!-- questions:end -->
