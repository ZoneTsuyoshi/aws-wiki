# 分野4: アクセスの分析

拒否の原因をメッセージとツールで切り分け、意図しない権限を見つけて防ぐ力を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.2.4](../../domain4.md#skill-4-2-4) | 認可の失敗の分析 |
| [4.2.5](../../domain4.md#skill-4-2-5) | 意図しない権限の調査と修正 |

## 学習の順番 {#study-order}

1. [アクセス拒否メッセージ](../../../../services/iam.md#access-denied-messages): 言い回しから、拒否したポリシーの種類を読み取ります。
2. [ポリシーシミュレーター](../../../../services/iam.md#policy-simulator)と [DecodeAuthorizationMessage](../../../../services/iam.md#decode-authorization): できることと限界を確認します。
3. [クロスアカウントの評価](../../../../services/identity-directory.md#cross-account-evaluation)と[アクセス拒否の切り分け](../../../../services/identity-directory.md#access-troubleshooting): 両側の許可と KMS の許可を確認します。
4. [エンドポイントポリシー](../../../../services/networking.md#endpoint-policies): `aws:SourceVpce` への書き換えを押さえます。
5. [IAM Access Analyzer](../../../../services/identity-directory.md#access-analyzer)、[外部アクセスの検出](../../../../services/identity-directory.md#aa-external)、[未使用アクセスの検出](../../../../services/identity-directory.md#aa-unused): 3 種類の分析ツールの違いを表で覚えます。
6. [ポリシーの検証とチェック](../../../../services/identity-directory.md#aa-policy-checks): パイプラインで使う API を選べるようにします。
7. [データ境界](../../../../services/identity-directory.md#data-perimeter): 3 つの統制と、サービスプリンシパルの例外を理解します。

## 覚える値 {#values}

| 分析ツール | リージョン | 料金 |
|---|---|---|
| 外部アクセス | リージョンごと | 無料 |
| 内部アクセス | リージョンごと | リソース数で課金 |
| 未使用アクセス | リージョンを問わない | ロールとユーザーの数で課金 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| `because no permissions boundary allows` | 権限境界の暗黙の拒否。境界を確認 |
| `with an explicit deny in a resource control policy` | RCP の拒否。シミュレーターでは再現しない |
| エンドポイント経由で公開 IP の条件が効かない | `aws:SourceVpce` に書き換える |
| 外部の主体が SSE-KMS のオブジェクトを読めない | キーポリシーと IAM の `kms:Decrypt` |
| `Encoded authorization failure message` | `sts:DecodeAuthorizationMessage` の権限と `decode-authorization-message` |
| 組織の外への共有を一覧にする | 組織を信頼ゾーンにした外部アクセスの分析ツール |
| 権限の増加を CI で止める | `CheckNoNewAccess` |
| 危険な操作の許可を CI で止める | `CheckAccessNotGranted` |
| 外から中のアクセスを組織で拒否 | RCP と `aws:PrincipalOrgID` |
| 中から外への持ち出しを組織で拒否 | SCP と `aws:ResourceOrgID` |

## 引っかかりやすい点 {#traps}

- ポリシーシミュレーターは SCP を評価しますが、RCP には対応していません。
- 外部アクセスの分析は、実際に使われたかではなく、ポリシーで許可されているかを判定します。
- Access Analyzer は検出するだけで止めません。止めるのは SCP や RCP です。
- SCP は外部の主体には効きません。
- RCP を導入してログの配信が止まったら、`aws:PrincipalIsAWSService` の例外を確認します。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [access-analysis 問1](../../exercises/access-analysis.md#q1) | 4.2.4 | 開発者が codecommit:ListRepositories を呼ぶと、エラーに because… |
| [access-analysis 問2](../../exercises/access-analysis.md#q2) | 4.2.4 | パートナー企業のロールが、自社メンバーアカウントのバケットを読むと AccessDenied になり… |
| [access-analysis 問3](../../exercises/access-analysis.md#q3) | 4.2.4 | VPC 内の EC2 が S3 のゲートウェイエンドポイント経由でバケットを読むようにしました。以前… |
| [access-analysis 問4](../../exercises/access-analysis.md#q4) | 4.2.4 | 外部の企業のロールが、自社のメンバーアカウントの SSE-KMS のバケットを読みます。バケットポリ… |
| [access-analysis 問5](../../exercises/access-analysis.md#q5) | 4.2.4 | EC2 の RunInstances が失敗し、Encoded authorization fail… |
| [access-analysis 問6](../../exercises/access-analysis.md#q6) | 4.2.5 | 組織の管理者が、全アカウントの S3 と KMS で「組織の外に共有されているもの」の一覧が欲しいと… |
| [access-analysis 問7](../../exercises/access-analysis.md#q7) | 4.2.5 | 開発者がリソースポリシーを Terraform で変更します。CI で「既存のポリシーより権限が増え… |
| [access-analysis 問8](../../exercises/access-analysis.md#q8) | 4.2.5 | 全アカウントの IAM ロールとユーザーについて、長期間使っていないロール、アクセスキー、権限を一覧… |
| [access-analysis 問9](../../exercises/access-analysis.md#q9) | 4.2.5 | 組織にデータ境界を導入します。要件は「組織外の主体が組織のバケットを読めない」「組織の主体が組織外の… |
| [access-analysis 問10](../../exercises/access-analysis.md#q10) | 4.2.5 | データ境界の RCP を導入した翌日、CloudTrail のログが一部のバケットに配信されなくなり… |

<!-- questions:end -->
