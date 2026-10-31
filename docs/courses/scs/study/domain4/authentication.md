# 分野4: 認証

主体の種類に合う ID の選択と、一時認証情報の発行、サインインできないときの切り分けを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.1.1](../../domain4.md#skill-4-1-1) | 人、アプリ、システムの ID |
| [4.1.2](../../domain4.md#skill-4-1-2) | 一時認証情報の発行 |
| [4.1.3](../../domain4.md#skill-4-1-3) | 認証のトラブルシューティング |

## 学習の順番 {#study-order}

1. [IAM Identity Center](../../../../services/identity-directory.md#identity-center)と [ID ソース](../../../../services/identity-directory.md#idc-identity-sources): 組織に 1 つの ID ソースと、変更時の影響を覚えます。
2. [ユーザープールと ID プール](../../../../services/cognito.md#user-vs-identity-pools): JWT と AWS 認証情報の違いを押さえます。
3. [脅威保護](../../../../services/cognito.md#threat-protection)と [Cognito の MFA](../../../../services/cognito.md#mfa-settings): Plus プランの機能と `Required` の影響を確認します。
4. [フェデレーション](../../../../services/iam.md#federation)と[信頼ポリシー](../../../../services/iam.md#trust-policy): CI/CD の OIDC と `sub` の絞り込みを押さえます。
5. [API の比較](../../../../services/iam.md#sts-api-compare)と[最大セッション時間](../../../../services/iam.md#max-session-duration): 期間と MFA の可否を表で覚えます。
6. [署名付き URL](../../../../services/s3.md#presigned-urls): 署名した認証情報と期限の関係を理解します。
7. [Identity Center のトラブルシュート](../../../../services/identity-directory.md#idc-troubleshooting)、[権限セット](../../../../services/identity-directory.md#idc-permission-sets)、[AD Connector](../../../../services/identity-directory.md#ad-connector)、[ロールマッピング](../../../../services/cognito.md#role-mapping): 症状と確認先を結びつけます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| `AssumeRole` の既定 | 1 時間 | ロールの設定で最大 12 時間 |
| ロールチェーン | 最大 1 時間 | 超える指定は失敗する |
| `GetSessionToken` | 既定 12 時間、最大 36 時間 | ルートは最大 1 時間 |
| 権限セットのセッション | 既定 1 時間、最大 12 時間 | Identity Center が作るロールも 12 時間 |
| SCIM のトークン | 1 年 | 切れると同期が止まる |
| 署名付き URL（IAM ユーザー） | 最長 7 日 | コンソールは 12 時間 |
| AD Connector のポート | TCP/UDP 53、88、389 | DNS と SRV レコードも必要 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 従業員を複数のアカウントへ | Identity Center。IdP があれば SCIM で同期 |
| 利用者のアプリが AWS を直接呼ぶ | Cognito の ID プール |
| 漏えいしたパスワードと不審なサインイン | Cognito Plus プランの脅威保護 |
| 長期のキーを CI から消す | OIDC フェデレーションと `sub` の条件 |
| CLI で MFA を証明する | `GetSessionToken` |
| 署名付き URL が期限より早く切れる | 署名した一時認証情報の失効 |
| 割り当てが特定のアカウントだけ失敗 | カスタマー管理ポリシーの有無 |
| 新入社員だけポータルに出ない | SCIM のトークンの期限 |
| 権限セットの再割り当ての後にキーを使えない | ロールの ARN の接尾辞の変化 |

## 引っかかりやすい点 {#traps}

- ID ソースを Active Directory に変えると、ユーザー、グループ、割り当てがすべて削除されます。
- Identity Center の ID ソースに Simple AD は使えません。
- `aud` だけの信頼では、他のリポジトリからの引き受けを防げません。
- `AssumeRoleWithSAML` と `AssumeRoleWithWebIdentity` に MFA のパラメータはありません。MFA は IdP 側です。
- 署名付き URL を止める専用の API はありません。署名の認証情報を無効にするか、ポリシーで拒否します。
- ID プールで同じ優先度のロールが複数あると、`cognito:preferred_role` が設定されません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [authentication 問1](../../exercises/authentication.md#q1) | 4.1.1 | ある会社は 40 のアカウントを持ち、社員 3,000 人は社外の IdP で認証しています。各アカ… |
| [authentication 問2](../../exercises/authentication.md#q2) | 4.1.1 | モバイルアプリの利用者が、サインイン後に自分専用の S3 プレフィックスへ直接ファイルをアップロード… |
| [authentication 問3](../../exercises/authentication.md#q3) | 4.1.1 | 会社は AWS Managed Microsoft AD を 1 つのアカウントで運用しています。次… |
| [authentication 問4](../../exercises/authentication.md#q4) | 4.1.1 | 一般消費者向けのサイトで Cognito ユーザープールを使っています。漏えいしたパスワードの再利用… |
| [authentication 問5](../../exercises/authentication.md#q5) | 4.1.1, 4.1.2 | GitHub Actions から AWS へデプロイしています。現在は IAM ユーザーのアクセス… |
| [authentication 問6](../../exercises/authentication.md#q6) | 4.1.2 | バッチが IAM ユーザーの認証情報で STS を呼びます。ロール A の MaxSessionDu… |
| [authentication 問7](../../exercises/authentication.md#q7) | 4.1.2 | 管理者が CLI で作業するときに MFA を必須にします。IAM ユーザーのポリシーは aws:M… |
| [authentication 問8](../../exercises/authentication.md#q8) | 4.1.2 | アプリケーションが ECS のタスクロールで S3 の署名付き URL を生成し、取引先へメールで送… |
| [authentication 問9](../../exercises/authentication.md#q9) | 4.1.2 | IAM ユーザーで署名した署名付き URL を、有効期限 3 日で取引先に渡しました。翌日、誤送信が… |
| [authentication 問10](../../exercises/authentication.md#q10) | 4.1.2 | パートナーの開発者が CLI から AssumeRoleWithSAML と AssumeRole … |
| [authentication 問11](../../exercises/authentication.md#q11) | 4.1.3 | Identity Center で、カスタマー管理ポリシーを含む権限セットをアカウント Y に割り当… |
| [authentication 問12](../../exercises/authentication.md#q12) | 4.1.3 | 外部 IdP と SCIM で同期している Identity Center で、数日前から新入社員が… |
| [authentication 問13](../../exercises/authentication.md#q13) | 4.1.3 | ある朝、運用チームが Identity Center の権限セットで KMS キーを使えなくなりまし… |
| [authentication 問14](../../exercises/authentication.md#q14) | 4.1.3 | AD Connector を作成しようとしていますが、接続に失敗します。オンプレミスの AD とは … |
| [authentication 問15](../../exercises/authentication.md#q15) | 4.1.3 | Cognito ID プールで、ID トークンの cognito:roles に複数のロールがあるユ… |

<!-- questions:end -->
