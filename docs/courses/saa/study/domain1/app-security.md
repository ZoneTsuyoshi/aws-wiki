# 分野1: アプリケーションのアクセスと認証情報

秘密情報の置き場所と、利用者や従業員のアプリへの入口を選びます。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [設定と認証情報の保護](../../domain1.md#t1-2-credentials) | アプリケーションの設定と認証情報のセキュリティ |
| [アプリケーションへの安全なアクセス](../../domain1.md#t1-2-app-access) | アプリケーションへの安全なアクセス |

## 学習の順番 {#study-order}

1. [3 つのサービスの比較](../../../../services/secrets.md#comparison)と[ローテーション](../../../../services/secrets.md#rotation): Secrets Manager と Parameter Store の選び方を確認します。
2. [インスタンスメタデータサービス (IMDS)](../../../../services/ec2-beanstalk.md#imds)と[インスタンスプロファイル](../../../../services/iam.md#instance-profile): EC2 の認証情報の渡し方と、メタデータの保護を押さえます。
3. [IAM データベース認証](../../../../services/databases.md#rds-iam-auth): パスワードなしの接続に対応するエンジンを覚えます。
4. [ユーザープールと ID プール](../../../../services/cognito.md#user-vs-identity-pools): 認証と AWS の認証情報の交換を区別します。
5. [署名付き URL と署名付き Cookie](../../../../services/networking.md#signed-urls-cookies)と[S3 オリジンの保護: OAC](../../../../services/networking.md#oac): CloudFront の限定配信と S3 の保護を確認します。
6. [Verified Access](../../../../services/identity-directory.md#verified-access): VPN なしの従業員向けアクセスを確認します。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| DB のパスワードを自動でローテーションする | Secrets Manager |
| 設定値を安価に階層で管理する | Parameter Store |
| SSRF でメタデータを盗まれたくない | IMDSv2 を必須にする |
| 利用者のサインアップとサインイン | Cognito ユーザープール |
| 利用者に AWS の一時的な認証情報を渡す | Cognito ID プール |
| 多数のファイルを URL を変えずに限定配信する | CloudFront の署名付き Cookie |
| S3 を CloudFront 経由だけで公開する | OAC とブロックパブリックアクセス |

## 引っかかりやすい点 {#traps}

- ソースコード、環境変数の平文、AMI に認証情報を埋め込みません。
- S3 の静的ウェブサイトエンドポイントには OAC を使えません。
- ユーザープールのトークンは、それ自体は AWS の認証情報ではありません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [app-security 問1](../../exercises/app-security.md#q1) | 認証情報の保護 | アプリの RDS のパスワードを 30 日ごとに自動で入れ替えます。コードに値を書きません。最も少な… |
| [app-security 問2](../../exercises/app-security.md#q2) | 認証情報の保護 | アプリの設定値と、ローテーションの要らない低リスクのトークンを安価に階層で管理します。どれが適切です… |
| [app-security 問3](../../exercises/app-security.md#q3) | 認証情報の保護 | EC2 のアプリの SSRF の脆弱性で、インスタンスメタデータからロールの認証情報を盗まれるリスク… |
| [app-security 問4](../../exercises/app-security.md#q4) | 認証情報の保護 | RDS for PostgreSQL に、アプリからパスワードなしで接続します。インスタンスのロール… |
| [app-security 問5](../../exercises/app-security.md#q5) | 認証情報の保護 | 認証情報の置き場所として不適切なものを選んでください。（2つ選択） |
| [app-security 問6](../../exercises/app-security.md#q6) | アプリへのアクセス | モバイルアプリの利用者のサインアップとサインインを、ソーシャルログインも含めて実装します。どれを使い… |
| [app-security 問7](../../exercises/app-security.md#q7) | アプリへのアクセス | サインイン済みのモバイル利用者が、自分のフォルダの S3 オブジェクトを直接アップロードします。AW… |
| [app-security 問8](../../exercises/app-security.md#q8) | アプリへのアクセス | 有料の動画を、CloudFront で購入者だけに配信します。購入者は多数のファイルにアクセスし、U… |
| [app-security 問9](../../exercises/app-security.md#q9) | アプリへのアクセス | S3 の静的コンテンツを CloudFront 経由でだけ公開し、S3 の URL からの直接のアク… |
| [app-security 問10](../../exercises/app-security.md#q10) | アプリへのアクセス | 社内向け Web アプリを、VPN なしで従業員に公開します。リクエストごとに ID と端末の状態を… |

<!-- questions:end -->
