# 分野1: IAM と STS

誰に何を許すかを、ユーザー、ロール、ポリシーの部品で設計します。長期の認証情報を減らす判断が中心です。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [認可モデルと最小権限](../../domain1.md#t1-1-authz-model) | セキュリティのベストプラクティス、ユーザー、グループ、ロール、ポリシーによる柔軟な認可モデル |
| [ルートユーザーと IAM ユーザーの保護](../../domain1.md#t1-1-root-mfa) | IAM ユーザーとルートユーザーへのベストプラクティスの適用 |
| [ロールベースのアクセス制御](../../domain1.md#t1-1-rbac) | ロールベースのアクセス制御戦略 |
| [フェデレーションとディレクトリ連携](../../domain1.md#t1-1-federation) | フェデレーションと ID サービス、ディレクトリサービスと IAM ロールを連携すべき場面の判断 |
| [リソースポリシーの使いどころ](../../domain1.md#t1-1-resource-policy) | AWS サービスのリソースポリシーの適切な利用の判断 |

## 学習の順番 {#study-order}

1. [プリンシパルと権限の定義](../../../../services/iam.md#principals)と[ポリシー評価](../../../../services/iam.md#policy-evaluation): プリンシパルの種類と、明示的な Deny が最優先という評価の順序を押さえます。
2. [管理ポリシーとインラインポリシー](../../../../services/iam.md#managed-vs-inline)と[権限境界の設定](../../../../services/iam.md#permissions-boundary): 再利用できるポリシーと、権限の上限を決める部品を区別します。
3. [ロールの引き受け](../../../../services/iam.md#assume-role)と[信頼ポリシー](../../../../services/iam.md#trust-policy): 信頼ポリシーと権限ポリシーの役割の違いを理解します。
4. [クロスアカウントアクセス](../../../../services/iam.md#cross-account)と[ExternalId と混乱した代理問題](../../../../services/iam.md#external-id): アカウントをまたぐときの両側の許可と、混乱した代理問題の対策を覚えます。
5. [フェデレーション](../../../../services/iam.md#federation)と[選び方の比較](../../../../services/identity-directory.md#choosing): Identity Center、SAML、OIDC、Directory Service の使い分けを表で確認します。
6. [アイデンティティベースとリソースベース](../../../../services/iam.md#identity-vs-resource): リソースポリシーが必要な場面と、別アカウントのときの許可の条件を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| アクセスキー | 1 ユーザーにつき最大 2 つ | 新旧を重ねて入れ替えられる |
| 評価の順序 | 明示的な Deny、Allow、暗黙の拒否 | Deny は Allow を常に上書きする |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| EC2 や Lambda に権限を渡す | インスタンスプロファイル、実行ロール |
| 開発者が作るロールの権限に上限を設ける | 権限境界 |
| 別アカウントの人に本番を操作させる | 本番にロールを作り、信頼ポリシーで相手を指定する |
| 第三者の SaaS に操作させる | 信頼ポリシーで `sts:ExternalId` を条件にする |
| 従業員が複数アカウントへサインオンする | Identity Center と権限セット |
| CI から長期のキーなしでデプロイする | OIDC プロバイダーと `AssumeRoleWithWebIdentity` |
| 重要な操作に MFA を求める | 条件キー `aws:MultiFactorAuthPresent` |
| AD の認証を中継するだけで、データを AWS に置かない | AD Connector |

## 引っかかりやすい点 {#traps}

- グループはプリンシパルではありません。ポリシーの `Principal` に指定できません。
- 権限境界と SCP は権限を与えません。IAM ポリシーの Allow も必要です。
- 同じアカウントならどちらかの許可で足りますが、別アカウントなら原則として両方が必要です。
- 一般の利用者は Cognito、従業員は Identity Center です。逆の選択肢は誤りです。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [iam 問1](../../exercises/iam.md#q1) | 認可モデル | EC2 上のアプリが、1 つの S3 バケットのオブジェクトだけを読みます。最小権限で、長期の認証情… |
| [iam 問2](../../exercises/iam.md#q2) | 認可モデル | 開発チームに IAM ロールの作成を任せますが、作られるロールが持てる権限には上限を設けたいと考えて… |
| [iam 問3](../../exercises/iam.md#q3) | 認可モデル | IAM ポリシーでバケットへの s3:GetObject を Allow し、同じユーザーが属するグ… |
| [iam 問4](../../exercises/iam.md#q4) | 認可モデル | 複数の IAM ロールに同じ権限のセットを付け、更新も 1 か所で済ませたいと考えています。最も適切… |
| [iam 問5](../../exercises/iam.md#q5) | 認可モデル | 正しい記述を選んでください。（2つ選択） |
| [iam 問6](../../exercises/iam.md#q6) | ルートユーザーの保護 | AWS アカウントのルートユーザーの扱いとして、ベストプラクティスに合うものはどれですか。 |
| [iam 問7](../../exercises/iam.md#q7) | ルートユーザーの保護 | 外部ツールのためにやむを得ず IAM ユーザーのアクセスキーを使っています。キーを無停止で入れ替える… |
| [iam 問8](../../exercises/iam.md#q8) | ルートユーザーの保護 | 特定の IAM ロールの削除は、MFA で認証したセッションでだけ許可したいと考えています。IAM … |
| [iam 問9](../../exercises/iam.md#q9) | ルートユーザーの保護 | 従業員 200 人が複数の AWS アカウントのコンソールを使います。IAM ユーザーを増やさず、M… |
| [iam 問10](../../exercises/iam.md#q10) | ロール | 開発アカウントのエンジニアに、本番アカウントの DynamoDB を読ませます。IAM ユーザーを増… |
| [iam 問11](../../exercises/iam.md#q11) | ロール | 第三者の監視 SaaS に自社アカウントの読み取りを許可します。SaaS 事業者が他の顧客の依頼で誤… |
| [iam 問12](../../exercises/iam.md#q12) | ロール | AssumeRole で得た認証情報の説明として正しいものを選んでください。（2つ選択） |
| [iam 問13](../../exercises/iam.md#q13) | ロール | 監査チームが 30 のアカウントを読み取ります。アカウントが増えても手間が増えにくい設計を選んでくだ… |
| [iam 問14](../../exercises/iam.md#q14) | ロール | EC2 と Lambda に AWS の権限を与える方法の組み合わせで、正しいものはどれですか。 |
| [iam 問15](../../exercises/iam.md#q15) | フェデレーション | GitHub Actions のような外部の CI から AWS にデプロイします。長期のアクセスキ… |
| [iam 問16](../../exercises/iam.md#q16) | フェデレーション | 社内の Active Directory のユーザーに複数アカウントのコンソールを使わせます。人事異… |
| [iam 問17](../../exercises/iam.md#q17) | フェデレーション | オンプレミスの AD はそのまま使い、AWS にはディレクトリのデータを保存したくありません。ドメイ… |
| [iam 問18](../../exercises/iam.md#q18) | フェデレーション | AWS 上で動く Microsoft SharePoint に、本物の AD の機能が必要です。さら… |
| [iam 問19](../../exercises/iam.md#q19) | フェデレーション | 1 つのアカウントだけで、既存の SAML 2.0 の IdP からコンソールと API にフェデレ… |
| [iam 問20](../../exercises/iam.md#q20) | リソースポリシー | 別のアカウント 111122223333 のロールに、自社の S3 バケットのオブジェクトを読ませま… |
| [iam 問21](../../exercises/iam.md#q21) | リソースポリシー | S3 のイベントで Lambda 関数を呼びます。S3 に呼び出しを許可するのはどれですか。 |
| [iam 問22](../../exercises/iam.md#q22) | リソースポリシー | REST API を特定の VPC エンドポイントからだけ呼べるようにしたいと考えています。アプリの… |
| [iam 問23](../../exercises/iam.md#q23) | リソースポリシー | 別アカウントのアプリに Secrets Manager のシークレットを読ませます。正しい組み合わせ… |

<!-- questions:end -->
