# 分野4: 暗号化とシークレット

認証情報の保存とローテーション、マスキング、鍵の選択、アカウントをまたぐ暗号化、転送時の暗号化を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.1.3](../../domain4.md#skill-4-1-3) | 認証情報の作成とローテーション |
| [4.2.2](../../domain4.md#skill-4-2-2) | 認証情報の保存 |
| [4.3.1](../../domain4.md#skill-4-3-1) | データマスキングと匿名化 |
| [4.3.2](../../domain4.md#skill-4-3-2) | 暗号鍵による暗号化と復号 |
| [4.3.3](../../domain4.md#skill-4-3-3) | アカウントをまたぐ暗号化 |
| [4.3.4](../../domain4.md#skill-4-3-4) | 転送時と転送前の暗号化 |

## 学習の順番 {#study-order}

1. [3 つのサービスの比較](../../../../services/secrets.md#comparison): Secrets Manager と Parameter Store を比べます。
2. [ローテーション](../../../../services/secrets.md#rotation): 自動の更新を確認します。
3. [KMS キーの種類](../../../../services/kms.md#key-types): 制御の範囲で選びます。
4. [アカウントをまたぐ手順](../../../../services/kms.md#cross-account-steps): 両側の許可を覚えます。
5. [暗号化の強制](../../../../services/s3.md#enforcing-encryption): `aws:SecureTransport` を確認します。
6. [クライアント側とサーバー側](../../../../services/kms.md#client-vs-server-side): 要件で選びます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| Secrets Manager の値 | 65,536 バイト | 自動ローテーションあり |
| Parameter Store の値 | 4 KB または 8 KB | スタンダードは無料 |
| Redshift のキー無効 | `inaccessible-kms-key`、14 日 | 14 日以内に戻せば復旧 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| パスワードを自動で変更する | Secrets Manager |
| 費用を抑えて設定値を置く | Parameter Store |
| 鍵のポリシーを制御する | カスタマー管理キー |
| KMS の呼び出しを減らす | S3 バケットキー |
| AWS に平文を見せない | クライアント側暗号化 |
| HTTP を拒否する | `aws:SecureTransport` が `false` で `Deny` |

## 引っかかりやすい点 {#traps}

- AWS 管理キーは共有できません。
- 別のアカウントのキーは ARN で指定します。
- MSK の SCRAM のシークレットにはカスタマー管理キーが必要です。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [encryption-secrets 問1](../../exercises/encryption-secrets.md#q1) | 4.1.3 | RDS のパスワードを 30 日ごとに自動で変更します。アプリはコードに値を持ちません。どれを選びま… |
| [encryption-secrets 問2](../../exercises/encryption-secrets.md#q2) | 4.1.3 | ローテーションの後に、Glue 以外の長時間動くアプリで接続エラーが出ます。原因として考えられるもの… |
| [encryption-secrets 問3](../../exercises/encryption-secrets.md#q3) | 4.1.3 | MSK の SASL/SCRAM のシークレットを関連付けられません。確認するものはどれですか。（2… |
| [encryption-secrets 問4](../../exercises/encryption-secrets.md#q4) | 4.2.2 | 環境ごとの設定値（S3 のパス）を、費用を抑えて保存します。自動のローテーションは不要です。どれを選… |
| [encryption-secrets 問5](../../exercises/encryption-secrets.md#q5) | 4.2.2 | Secrets Manager と Parameter Store の値のサイズ上限の組み合わせで正… |
| [encryption-secrets 問6](../../exercises/encryption-secrets.md#q6) | 4.2.2 | CloudFormation テンプレートに、データベースのパスワードを平文で書かずに渡します。どの… |
| [encryption-secrets 問7](../../exercises/encryption-secrets.md#q7) | 4.3.1 | 顧客のメールを、値を見せずに複数のデータセットで突合します。元に戻す必要はありません。どの手法ですか… |
| [encryption-secrets 問8](../../exercises/encryption-secrets.md#q8) | 4.3.1 | Redshift で、データはそのままに、支払い担当者以外にはカード番号の列の値を **** に置き… |
| [encryption-secrets 問9](../../exercises/encryption-secrets.md#q9) | 4.3.1 | マスキングや匿名化をコード不要で行う組み合わせで正しいものはどれですか。（2つ選択） |
| [encryption-secrets 問10](../../exercises/encryption-secrets.md#q10) | 4.3.2 | 鍵のポリシーを自分で管理し、削除やローテーションも制御します。どの KMS キーですか。 |
| [encryption-secrets 問11](../../exercises/encryption-secrets.md#q11) | 4.3.2 | SSE-KMS のバケットで大量のオブジェクトを書き、KMS の費用が高く、ThrottlingEx… |
| [encryption-secrets 問12](../../exercises/encryption-secrets.md#q12) | 4.3.2 | Redshift のカスタマー管理キーを無効にしました。クラスターはどうなりますか。 |
| [encryption-secrets 問13](../../exercises/encryption-secrets.md#q13) | 4.3.2 | 暗号化の設定の組み合わせで正しいものはどれですか。 |
| [encryption-secrets 問14](../../exercises/encryption-secrets.md#q14) | 4.3.3 | アカウント B のロールが、アカウント A のカスタマー管理キーで暗号化された S3 のデータを読む… |
| [encryption-secrets 問15](../../exercises/encryption-secrets.md#q15) | 4.3.3 | 別のアカウントへ渡す S3 のデータの暗号化で、aws/s3 の AWS 管理キーを使っています。読… |
| [encryption-secrets 問16](../../exercises/encryption-secrets.md#q16) | 4.3.3 | 別のアカウントのキーを SDK で使います。KeyId の指定として正しいものはどれですか。 |
| [encryption-secrets 問17](../../exercises/encryption-secrets.md#q17) | 4.3.4 | データを S3 へ送る前に手元で暗号化し、AWS には平文を見せません。どの方法ですか。 |
| [encryption-secrets 問18](../../exercises/encryption-secrets.md#q18) | 4.3.4 | 分析バケットへの HTTP のアクセスを拒否します。バケットポリシーの条件はどれですか。 |
| [encryption-secrets 問19](../../exercises/encryption-secrets.md#q19) | 4.3.4 | 転送時の暗号化を強制する設定の組み合わせで正しいものはどれですか。（2つ選択） |

<!-- questions:end -->
