# 分野6: IAM とアクセス管理

人と機械のアクセスを長期の認証情報なしで、大規模に管理する方法を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [IAM の要素](../../domain6.md#t6-1-entities) | 人と機械に使う IAM の要素 |
| [フェデレーション](../../domain6.md#t6-1-federation) | ID フェデレーション |
| [権限境界](../../domain6.md#t6-1-boundaries) | 権限境界による委任 |
| [SCP](../../domain6.md#t6-1-scp) | 組織の SCP |
| [最小権限](../../domain6.md#t6-1-least-privilege) | 最小権限のポリシー設計 |
| [RBAC と ABAC](../../domain6.md#t6-1-rbac-abac) | RBAC と ABAC |
| [MFA と STS](../../domain6.md#t6-1-mfa-sts) | MFA、STS、インスタンスプロファイル |

## 学習の順番 {#study-order}

1. [プログラムからのアクセス](../../../../services/iam.md#programmatic-access): 機械の認証の手段を確認します。
2. [IAM Identity Center](../../../../services/identity-directory.md#identity-center): 権限セットと ID ソースを押さえます。
3. [権限境界の設定](../../../../services/iam.md#permissions-boundary): 委任の手順を理解します。
4. [それぞれの効く場所](../../../../services/identity-directory.md#evaluation-layers): SCP と境界の重なりを確認します。
5. [IAM Access Analyzer](../../../../services/identity-directory.md#access-analyzer): ポリシーの生成と未使用の検出を確認します。
6. [セッションタグ](../../../../services/iam.md#session-tags): ABAC の属性の渡し方を確認します。
7. [iam:PassRole](../../../../services/iam.md#passrole): 昇格の防止を覚えます。

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| GitHub Actions からデプロイする | OIDC と `sub` の条件 |
| AWS の外のサーバー | IAM Roles Anywhere |
| ロールの作成を委任する | `iam:PermissionsBoundary` を必須にする |
| プロジェクトが増え続ける | ABAC |
| CLI で MFA を満たす | `GetSessionToken` |
| 外部の SaaS に引き受けさせる | `sts:ExternalId` |

## 引っかかりやすい点 {#traps}

- 実際の権限は ID ベースポリシーと権限境界の重なりです。
- SCP は権限を与えません。管理アカウントとサービスリンクロールに効きません。
- リージョンの制限では `NotAction` でグローバルサービスを除きます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [iam 問1](../../exercises/iam.md#q1) | IAM の要素 | 次の 3 つのアクセスを見直します。(1) データセンターのサーバーの AWS の呼び出し。(2) … |
| [iam 問2](../../exercises/iam.md#q2) | IAM の要素 | 次の要件を満たすポリシーを選びます。(1) 別のアカウントのロールに S3 バケットを読ませ、ロール… |
| [iam 問3](../../exercises/iam.md#q3) | IAM の要素 | EC2 と ECS のアプリの認証情報を見直します。担当者の提案のうち適切なものはどれですか。（2つ… |
| [iam 問4](../../exercises/iam.md#q4) | フェデレーション | 200 アカウントの開発者が、社内の Okta でサインインして、権限を 1 か所で割り当てます。ユ… |
| [iam 問5](../../exercises/iam.md#q5) | フェデレーション | GitHub Actions から AWS へデプロイします。IAM の OIDC プロバイダーは作… |
| [iam 問6](../../exercises/iam.md#q6) | フェデレーション | 次の 2 つの要件を選びます。(1) オンプレミスの Active Directory のユーザーで… |
| [iam 問7](../../exercises/iam.md#q7) | 権限境界 | 開発チームにアプリ用の IAM ロールを自分で作らせつつ、管理者のロールを作る昇格を防ぎます。適切な… |
| [iam 問8](../../exercises/iam.md#q8) | 権限境界 | ロールの ID ベースポリシーは s3:* と ec2:* を許可し、権限境界は s3:* と dy… |
| [iam 問9](../../exercises/iam.md#q9) | 権限境界 | 300 アカウントの組織で、全社の上限（利用できるサービスとリージョン）は組織の管理者が決めます。各… |
| [iam 問10](../../exercises/iam.md#q10) | SCP | 東京以外のリージョンの操作を SCP で拒否したところ、IAM や Organizations の操… |
| [iam 問11](../../exercises/iam.md#q11) | SCP | ある SCP は s3:* を許可するだけの許可リストの形です。ロールには ec2:RunInsta… |
| [iam 問12](../../exercises/iam.md#q12) | SCP | SCP の効果についての説明のうち、正しいものはどれですか。（2つ選択） |
| [iam 問13](../../exercises/iam.md#q13) | 最小権限 | 新しい Lambda の権限を AdministratorAccess から必要最小限にします。実際… |
| [iam 問14](../../exercises/iam.md#q14) | 最小権限 | 組織で 1 年使われていないロールと権限を見つけ、削除する前に、残す権限で必要な API が許可され… |
| [iam 問15](../../exercises/iam.md#q15) | 最小権限 | S3 バケットのバケットポリシーで、CloudFront の特定のディストリビューションからの読み取… |
| [iam 問16](../../exercises/iam.md#q16) | RBAC と ABAC | プロジェクトが毎月増え、そのたびにロールとポリシーを追加する作業が負担です。リソースと利用者のセッシ… |
| [iam 問17](../../exercises/iam.md#q17) | RBAC と ABAC | Identity Center の利用者の部署の属性で、S3 のオブジェクトへのアクセスを制御します… |
| [iam 問18](../../exercises/iam.md#q18) | RBAC と ABAC | 監査、運用、請求という職務が固定された 3 つの役割の権限と、四半期ごとに増えるチームごとのデータの… |
| [iam 問19](../../exercises/iam.md#q19) | MFA と STS | 本番の削除の操作には MFA を必須にします。CLI で作業する IAM ユーザーが、長期のキーのま… |
| [iam 問20](../../exercises/iam.md#q20) | MFA と STS | 開発者に Lambda の作成を許可しました。監査で、開発者が既存の管理者のロールを関数に渡して権限… |
| [iam 問21](../../exercises/iam.md#q21) | MFA と STS | EC2 のアプリが別のアカウントの S3 を読みます。また、外部の SaaS が自社のアカウントのロ… |

<!-- questions:end -->
