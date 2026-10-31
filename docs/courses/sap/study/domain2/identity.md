# 分野2: ID のセキュリティ

従業員、アプリの利用者、ワークロードのそれぞれに、長期の認証情報を持たせない設計を問います。組織全体の上限と、例外の扱いが決め手になります。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.1.1](../../domain2.md#skill-2-1-1) | 標準プロトコルによる ID フェデレーション |
| [2.1.2](../../domain2.md#skill-2-1-2) | アプリケーションの認証と認可 |
| [2.1.3](../../domain2.md#skill-2-1-3) | 最小権限と一時認証情報 |
| [2.1.4](../../domain2.md#skill-2-1-4) | データ境界と外部アクセスの検証 |
| [2.1.5](../../domain2.md#skill-2-1-5) | ハイブリッドとマルチクラウドのワークロード ID |

## 学習の順番 {#study-order}

1. [ID ソース](../../../../services/identity-directory.md#idc-identity-sources)と[権限セット](../../../../services/identity-directory.md#idc-permission-sets): 外部 IdP、AD、既定のディレクトリの選び方と、SCIM の注意点を確認します。
2. [Managed Microsoft AD](../../../../services/identity-directory.md#managed-ad)と [AD Connector](../../../../services/identity-directory.md#ad-connector): 本体を AWS に置くか、中継するだけかの違いを押さえます。
3. [ユーザープールと ID プール](../../../../services/cognito.md#user-vs-identity-pools)と [OAuth フロー](../../../../services/cognito.md#oauth-flows): 役割の違いと、人とサーバーのフローの使い分けを理解します。
4. [Verified Permissions](../../../../services/identity-directory.md#verified-permissions)と [Pod に IAM 権限を与える](../../../../services/containers.md#pod-identity): 認可を外に出す方法と、Pod ごとの権限を確認します。
5. [権限境界の設定](../../../../services/iam.md#permissions-boundary)、[ExternalId](../../../../services/iam.md#external-id)、[セッションポリシー](../../../../services/iam.md#session-policies)、[セッションタグ](../../../../services/iam.md#session-tags): 権限を絞る手段を場面で区別します。
6. [クロスアカウントの評価](../../../../services/identity-directory.md#cross-account-evaluation): 両側の許可が要る理由を確認します。
7. [データ境界](../../../../services/identity-directory.md#data-perimeter)と [IAM Access Analyzer](../../../../services/identity-directory.md#access-analyzer): 3 つの境界と条件キー、検証の道具を覚えます。
8. [Verified Access](../../../../services/identity-directory.md#verified-access): VPN との違いと、ポリシーの評価を押さえます。
9. [プログラムからのアクセス](../../../../services/iam.md#programmatic-access)、[STS の API の比較](../../../../services/iam.md#sts-api-compare)、[オンプレミスと他クラウド](../../../../services/operations.md#hybrid-nodes): AWS の外のワークロードの選択肢を比べます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| SCIM のアクセストークン | 有効期間 1 年。残り 90 日以下で通知 | 切れると同期だけが止まる |
| Identity Center の ID ソース | 組織に 1 つ | 複数のフォレストは Managed AD の信頼で |
| RCP の Effect | Deny のみ | Allow は `RCPFullAWSAccess` だけ |
| Pod Identity の対象 | Linux の EC2 上の Pod | Fargate と Windows は対象外 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 既存の IdP があり、退職者を自動で無効にする | Identity Center の外部 IdP（SAML と SCIM） |
| 複数のアカウントでドメインに参加し、回線断でも AWS 側で認証する | Managed Microsoft AD を共有。AD Connector は共有できない |
| CI/CD サービスが OIDC トークンを持つ | IAM の OIDC プロバイダーと `AssumeRoleWithWebIdentity`。`sub` を検証する |
| 利用者が S3 へ直接アップロードする | ユーザープールで認証し、ID プールで一時認証情報を得る |
| サーバー同士の API 呼び出し | OAuth のクライアントクレデンシャル |
| 認可の規則を全サービスから切り離す | Verified Permissions（Cedar） |
| 開発者にロールの作成を任せる | 権限境界の指定を作成の条件にする |
| プロジェクトごとのロールが増え続ける | ABAC。タグの変更も拒否する |
| 第三者が顧客のロールを引き受ける | 提供者が発行する外部 ID |
| 1 つのロールで処理ごとに権限を狭める | セッションポリシー |
| 組織の外の主体を自社のリソースから締め出す | RCP と `aws:PrincipalOrgID` |
| 自社の主体が外部のリソースへ書き出すのを防ぐ | SCP と `aws:ResourceOrgID` |
| VPN をやめ、端末の状態もリクエストごとに評価する | Verified Access |
| 社内 PKI で証明書を発行している | IAM Roles Anywhere |
| 他社のクラウドのワークロードに OIDC トークンがある | `AssumeRoleWithWebIdentity` |

## 引っかかりやすい点 {#traps}

- AD Connector は他のアカウントと共有できず、キャッシュも持ちません。回線が切れると認証できません。
- ユーザープールのトークンは SigV4 の署名に使えません。AWS の権限が必要なら ID プールを通します。
- RCP を入れると、AWS サービスのプリンシパルも対象になります。`aws:PrincipalIsAWSService` の例外がないと、CloudTrail のログ配信が止まります。
- Roles Anywhere の信頼の境界はアカウントです。`aws:SourceArn` がないと、同じアカウントの別のアンカーの証明書でロールを引き受けられます。
- OIDC の信頼ポリシーで `aud` だけを検証すると、同じサービスの他のリポジトリから引き受けられます。
- Access Analyzer の外部アクセスは組織の外の共有を見つけます。組織の中の誰が届くかは内部アクセスです。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [identity 問1](../../exercises/identity.md#q1) | 2.1.1 | ある製造業の会社は 40 の AWS アカウントを Organizations で運用し、各アカウン… |
| [identity 問2](../../exercises/identity.md#q2) | 2.1.1 | ある会社はオンプレミスの Active Directory を今後も残します。AWS 側では 8 つ… |
| [identity 問3](../../exercises/identity.md#q3) | 2.1.1 | ある開発組織は SaaS の CI/CD サービスを使っています。このサービスは実行ごとに OIDC… |
| [identity 問4](../../exercises/identity.md#q4) | 2.1.1 | ある会社は Okta を IAM Identity Center の ID ソースにして、SCIM … |
| [identity 問5](../../exercises/identity.md#q5) | 2.1.2 | ある動画共有アプリでは、モバイルの利用者が大きなファイルをアプリから S3 へ直接アップロードします… |
| [identity 問6](../../exercises/identity.md#q6) | 2.1.2 | ある B2B の SaaS は、20 のマイクロサービスがそれぞれのコードで認可を判定しています。「… |
| [identity 問7](../../exercises/identity.md#q7) | 2.1.2 | ある会社は、Cognito のオーソライザーで保護した REST API を公開しています。新しく、… |
| [identity 問8](../../exercises/identity.md#q8) | 2.1.2 | ある EKS クラスターでは、Linux の EC2 ノードグループの上で 15 のチームの Pod… |
| [identity 問9](../../exercises/identity.md#q9) | 2.1.2 | ある会社の EKS では、API の Pod を AWS Fargate で動かしています。設計者は… |
| [identity 問10](../../exercises/identity.md#q10) | 2.1.3 | ある組織は、開発チームに Lambda の実行ロールを自分で作らせたいと考えています。ただし、開発者… |
| [identity 問11](../../exercises/identity.md#q11) | 2.1.3 | ある研究機関では 200 のプロジェクトが同じアカウントで S3 と DynamoDB を使い、プロ… |
| [identity 問12](../../exercises/identity.md#q12) | 2.1.3 | ある SaaS の提供者は、多数の顧客の AWS アカウントのロールを引き受けて、設定の監査を行いま… |
| [identity 問13](../../exercises/identity.md#q13) | 2.1.3 | 分析アカウントのロールが、データアカウントの S3 バケットのオブジェクトを読みます。オブジェクトは… |
| [identity 問14](../../exercises/identity.md#q14) | 2.1.3 | あるデータ処理の基盤では、1 つの共通ロールでテナントごとのジョブを実行します。ジョブごとに、そのテ… |
| [identity 問15](../../exercises/identity.md#q15) | 2.1.4 | あるセキュリティチームは、組織の外の主体による S3 へのアクセスを拒否する RCP を、aws:P… |
| [identity 問16](../../exercises/identity.md#q16) | 2.1.4 | ある金融機関は、社員や社内のワークロードが、自社のデータを個人や他社の S3 バケットへ書き出せない… |
| [identity 問17](../../exercises/identity.md#q17) | 2.1.4 | ある組織は次の 2 つを実現したいと考えています。1 つ目は、重要な DynamoDB テーブルに組… |
| [identity 問18](../../exercises/identity.md#q18) | 2.1.4 | ある会社は、委託先の担当者に社内の HTTP アプリを使わせています。今は Client VPN で… |
| [identity 問19](../../exercises/identity.md#q19) | 2.1.5 | ある会社は 1 つのアカウントで IAM Roles Anywhere を使っています。A 事業部と… |
| [identity 問20](../../exercises/identity.md#q20) | 2.1.5 | ある会社のワークロードは他社のクラウドの Kubernetes で動いています。AWS の Dyna… |
| [identity 問21](../../exercises/identity.md#q21) | 2.1.5 | ある会社のデータセンターには 300 台の Linux サーバーがあります。社内 PKI も OID… |

<!-- questions:end -->
