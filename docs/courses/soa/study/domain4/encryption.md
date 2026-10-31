# 分野4: 暗号化とシークレット

キーの選択、エラーの切り分け、証明書、シークレットの運用を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.2.2](../../domain4.md#skill-4-2-2) | 保存時の暗号化 |
| [4.2.3](../../domain4.md#skill-4-2-3) | 転送時の暗号化 |
| [4.2.4](../../domain4.md#skill-4-2-4) | シークレットの保存 |

## 学習の順番 {#study-order}

1. [KMS キーの種類](../../../../services/kms.md#key-types)と[主なエラー](../../../../services/kms.md#kms-errors): キーの種類とエラーを確認します。
2. [EBS の暗号化](../../../../services/storage.md#ebs-encryption)、[暗号化とアクセス制御](../../../../services/storage.md#efs-encryption)と[暗号化](../../../../services/s3.md#encryption): サービスごとの手順を確認します。
3. [リージョンのルール](../../../../services/certificates.md#region-rules)、[自動更新](../../../../services/certificates.md#auto-renewal)と[更新の監視](../../../../services/certificates.md#renewal-monitoring): 証明書の運用を確認します。
4. [3 つのサービスの比較](../../../../services/secrets.md#comparison)と[ローテーション](../../../../services/secrets.md#rotation): Secrets Manager と Parameter Store を比較します。
5. [クロスアカウントでの利用](../../../../services/secrets.md#secrets-cross-account)と[CloudFormation の動的参照](../../../../services/secrets.md#dynamic-references): 共有と参照を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| キーの削除の待機 | 7〜30 日 | `cancel-key-deletion` で取り消す |
| シークレットの復旧期間 | 7〜30 日 | この間は戻せる |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 別アカウントと共有する | カスタマー管理キー |
| 既存の EBS を暗号化する | スナップショットをコピーして暗号化 |
| 既存の EFS を暗号化する | 暗号化した別のファイルシステムへ |
| KMS の呼び出しを減らす | S3 Bucket Key |
| CloudFront の証明書 | `us-east-1` で発行 |
| S3 で HTTPS を強制する | `aws:SecureTransport` が `false` を拒否 |
| 古い TLS を止める（ALB） | リスナーのセキュリティポリシー |
| パスワードの自動の変更 | Secrets Manager のローテーション |

## 引っかかりやすい点 {#traps}

- Parameter Store に自動ローテーションはありません。
- ACM はインポートした証明書を更新しません。
- AWS 管理キーのポリシーは変更できず、そのシークレットは共有できません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [encryption 問1](../../exercises/encryption.md#q1) | 4.2.2 | RDS のスナップショットを別のアカウントと共有する予定です。どのキーで暗号化しますか。 |
| [encryption 問2](../../exercises/encryption.md#q2) | 4.2.2 | 既存の暗号化されていない EBS ボリュームを暗号化します。正しい手順はどれですか。 |
| [encryption 問3](../../exercises/encryption.md#q3) | 4.2.2 | カスタマー管理キーを削除予定にしたところ、関連の EBS を使うインスタンスが起動しなくなりました。… |
| [encryption 問4](../../exercises/encryption.md#q4) | 4.2.2 | 次の KMS のエラーと対処の組み合わせとして正しいものを選んでください。（2つ選択） |
| [encryption 問5](../../exercises/encryption.md#q5) | 4.2.2 | 既存の暗号化されていない EFS を、規制の要件で保存時に暗号化する必要があります。正しい方法はどれ… |
| [encryption 問6](../../exercises/encryption.md#q6) | 4.2.2 | SSE-KMS のバケットへのアクセスが多く、KMS の ThrottlingException と… |
| [encryption 問7](../../exercises/encryption.md#q7) | 4.2.3 | 東京で作った ACM の証明書が CloudFront の画面に出てきません。ALB にも同じドメイ… |
| [encryption 問8](../../exercises/encryption.md#q8) | 4.2.3 | HTTP の通信を止めるため、バケットポリシーの Allow の文に aws:SecureTrans… |
| [encryption 問9](../../exercises/encryption.md#q9) | 4.2.3 | ACM のインポートした証明書の期限が切れて障害になりました。再発を防ぐためにどの対策を取りますか。… |
| [encryption 問10](../../exercises/encryption.md#q10) | 4.2.3 | DNS 検証の ACM の証明書が自動で更新されません。統合サービスで使用中です。最初に確認すること… |
| [encryption 問11](../../exercises/encryption.md#q11) | 4.2.3 | ALB で TLS 1.0 と 1.1 の接続を止めるよう求められました。どこを変更しますか。 |
| [encryption 問12](../../exercises/encryption.md#q12) | 4.2.3 | 転送時の暗号化を有効にする方法として正しいものを選んでください。（2つ選択） |
| [encryption 問13](../../exercises/encryption.md#q13) | 4.2.4 | RDS のパスワードを 30 日ごとに自動で変更し、アプリには常に最新の値を使わせたいです。現在は … |
| [encryption 問14](../../exercises/encryption.md#q14) | 4.2.4 | ローテーションの方式の説明として正しいものはどれですか。 |
| [encryption 問15](../../exercises/encryption.md#q15) | 4.2.4 | Lambda によるローテーションが失敗します。プライベートサブネットの RDS を更新する関数です… |
| [encryption 問16](../../exercises/encryption.md#q16) | 4.2.4 | 別のアカウントからシークレットを読みます。拒否されます。必要な設定を選んでください。（2つ選択） |
| [encryption 問17](../../exercises/encryption.md#q17) | 4.2.4 | CloudFormation のテンプレートとスタックの情報に、DB のパスワードの平文を残したくあ… |
| [encryption 問18](../../exercises/encryption.md#q18) | 4.2.4 | 本番のシークレットを既定の設定で誤って削除しました。10 分後に気づきました。アプリケーションは値を… |

<!-- questions:end -->
