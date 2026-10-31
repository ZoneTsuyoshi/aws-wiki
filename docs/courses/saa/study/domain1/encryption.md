# 分野1: 暗号化と鍵

保存時と転送時の方式、鍵のアクセスポリシー、ローテーションと証明書の更新を扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [保存時の暗号化と鍵の管理](../../domain1.md#t1-3-at-rest) | 暗号化と適切な鍵の管理、保存時の暗号化 |
| [転送時の暗号化](../../domain1.md#t1-3-in-transit) | 転送時の暗号化 |
| [暗号鍵のアクセスポリシー](../../domain1.md#t1-3-key-policies) | 暗号鍵のアクセスポリシーの実装 |
| [鍵のローテーションと証明書の更新](../../domain1.md#t1-3-rotation) | 暗号鍵のローテーションと証明書の更新 |

## 学習の順番 {#study-order}

1. [KMS キーの種類](../../../../services/kms.md#key-types)と[暗号化](../../../../services/s3.md#encryption): キーの種類と S3 の暗号化の方式を表で比べます。
2. [S3 Bucket Key の動作](../../../../services/s3.md#bucket-key)と[EBS の暗号化](../../../../services/storage.md#ebs-encryption): KMS の呼び出しの削減と、EBS の既定の暗号化を確認します。
3. [リージョンのルール](../../../../services/certificates.md#region-rules)と[統合サービス](../../../../services/certificates.md#integrated-services): 証明書を置くリージョンのルールを覚えます。
4. [キーポリシー、IAM、グラント](../../../../services/kms.md#access-control)と[既定のキーポリシー](../../../../services/kms.md#default-key-policy-details): IAM だけではキーを使えない理由を理解します。
5. [kms:ViaService](../../../../services/kms.md#via-service)と[アカウントをまたぐ暗号化](../../../../services/kms.md#cross-account): サービスの限定と、アカウントをまたぐ許可を確認します。
6. [キーのローテーション](../../../../services/kms.md#key-rotation)と[鍵素材のインポート](../../../../services/kms.md#imported-key-material): 自動ローテーションの範囲と例外を押さえます。
7. [自動更新](../../../../services/certificates.md#auto-renewal)と[更新の監視](../../../../services/certificates.md#renewal-monitoring): 自動更新の条件と監視を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| 自動ローテーション | 既定 365 日。90〜2,560 日 | 対称のカスタマー管理キー |
| CloudFront の証明書 | `us-east-1` | ALB は同じリージョン |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 鍵の利用を監査し、権限を分ける | SSE-KMS とカスタマー管理キー |
| SSE-KMS の KMS の呼び出しを減らす | S3 バケットキー |
| 暗号化スナップショットを別アカウントへ共有 | カスタマー管理キー |
| 未暗号化の RDS を暗号化する | スナップショットを暗号化コピーして復元する。ブルー/グリーンデプロイも使える |
| HTTP を拒否する | `aws:SecureTransport` が `false` を Deny |
| 特定のサービス経由でだけキーを使わせる | `kms:ViaService` |
| 証明書の更新を人の作業なしで続ける | ACM の DNS 検証 |

## 引っかかりやすい点 {#traps}

- ローテーションしても、キーの ID と ARN は変わらず、古い暗号文も復号できます。
- インポートした鍵素材のキーは、自動ローテーションはできず、オンデマンドローテーションはできます。
- ACM にインポートした証明書は自動更新されません。
- AWS 管理キーのポリシーは変更できず、別アカウントと共有できません。
- ACM の証明書はリージョン間でコピーできません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [encryption 問1](../../exercises/encryption.md#q1) | 保存時の暗号化 | S3 の暗号化で、鍵の利用を CloudTrail で監査し、部門ごとに使える人を分けたいと考えてい… |
| [encryption 問2](../../exercises/encryption.md#q2) | 保存時の暗号化 | 東京リージョンの SSE-KMS のバケットに大量の PUT があり、KMS の費用とスロットリング… |
| [encryption 問3](../../exercises/encryption.md#q3) | 保存時の暗号化 | 暗号化されていない RDS インスタンスを暗号化します。手順として正しいものはどれですか。 |
| [encryption 問4](../../exercises/encryption.md#q4) | 保存時の暗号化 | 暗号化スナップショットを別のアカウントに共有します。どの種類のキーで暗号化する必要がありますか。 |
| [encryption 問5](../../exercises/encryption.md#q5) | 保存時の暗号化 | 新しいアカウントで作る EBS ボリュームとスナップショットを、すべて暗号化された状態にします。最も… |
| [encryption 問6](../../exercises/encryption.md#q6) | 転送時の暗号化 | CloudFront のディストリビューションで独自ドメインの HTTPS を使います。ACM の証… |
| [encryption 問7](../../exercises/encryption.md#q7) | 転送時の暗号化 | S3 バケットへの HTTP のアクセスを拒否します。どう設定しますか。 |
| [encryption 問8](../../exercises/encryption.md#q8) | 転送時の暗号化 | 東京の ALB で HTTPS を終端します。ACM の公開証明書の扱いとして正しいものはどれですか… |
| [encryption 問9](../../exercises/encryption.md#q9) | 転送時の暗号化 | ALB の背後の EC2 まで通信を暗号化したいと考えています。EC2 のサーバーにも証明書が要りま… |
| [encryption 問10](../../exercises/encryption.md#q10) | キーポリシー | IAM ポリシーで kms:Decrypt を許可したのに、AccessDeniedExceptio… |
| [encryption 問11](../../exercises/encryption.md#q11) | キーポリシー | 鍵の管理者は暗号化されたデータを読めないようにし、アプリのロールは暗号操作だけできるようにします。ど… |
| [encryption 問12](../../exercises/encryption.md#q12) | キーポリシー | カスタマー管理キーを、S3 の暗号化のときだけ使わせ、アプリからの直接の Decrypt は拒否しま… |
| [encryption 問13](../../exercises/encryption.md#q13) | キーポリシー | 別のアカウントのアプリに KMS キーで復号させます。設定として正しいものはどれですか。（2つ選択） |
| [encryption 問14](../../exercises/encryption.md#q14) | ローテーション | カスタマー管理キーの自動ローテーションを有効にしました。正しい説明はどれですか。 |
| [encryption 問15](../../exercises/encryption.md#q15) | ローテーション | 外部の HSM で作った鍵素材を KMS にインポートしたキーがあります。定期的に入れ替えるにはどう… |
| [encryption 問16](../../exercises/encryption.md#q16) | ローテーション | ACM にインポートした外部の CA の証明書を ALB で使っています。正しいものはどれですか。 |
| [encryption 問17](../../exercises/encryption.md#q17) | ローテーション | ACM の公開証明書の更新を、人の作業なしで続けたいと考えています。発行時に選ぶ方法はどれですか。 |

<!-- questions:end -->
