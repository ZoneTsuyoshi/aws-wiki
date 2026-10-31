# IAM とアクセス管理の問題集

対象の解説: [IAM とアクセス管理](../../../services/iam.md)

### 問1 {#q1}

次の 3 つのアクセスを見直します。(1) データセンターのサーバーの AWS の呼び出し。(2) GitHub Actions のデプロイ。(3) 開発者の複数アカウントへの作業。長期の認証情報をなくします。適切な組み合わせはどれですか。

- A. (1) インスタンスプロファイル、(2) Roles Anywhere、(3) Cognito
- B. (1) Identity Center、(2) IAM ユーザー、(3) OIDC のフェデレーション
- C. (1) IAM Roles Anywhere、(2) OIDC のフェデレーション、(3) Identity Center
- D. (1) IAM ユーザーのキーの定期的なローテーション、(2) GitHub のシークレットに置くキー、(3) 開発者ごとの IAM ユーザー

??? success "答えと解説"
    **正解: C**

    AWS の外のサーバーは Roles Anywhere、パイプラインは OIDC、人は Identity Center です。

    - A: 誤り。インスタンスプロファイルは EC2 用で、Cognito はアプリの利用者向け。
    - B: 誤り。(1) は人のアクセス用で、(2) はキーが残る。
    - C: 正しい。
    - D: 誤り。すべて長期の認証情報が残る。

    **スキル:** [IAM の要素](../domain6.md#t6-1-entities) / **参照:** [プログラムからのアクセス](../../../services/iam.md#programmatic-access)、[プリンシパルと権限の定義](../../../services/iam.md#principals)

### 問2 {#q2}

次の要件を満たすポリシーを選びます。(1) 別のアカウントのロールに S3 バケットを読ませ、ロールの引き受けはさせない。(2) CI のジョブが引き受けたセッションだけ、書き込みの権限を除く。適切な組み合わせはどれですか。

- A. (1) 権限境界、(2) ID ベースポリシーの更新
- B. (1) 引き受けのセッションポリシー、(2) バケットのリソースベースポリシー
- C. (1) リソースベースポリシー、(2) セッションポリシー
- D. (1) SCP、(2) 権限境界

??? success "答えと解説"
    **正解: C**

    別のアカウントからのアクセスにはリソースベースポリシー、そのセッションだけの制限にはセッションポリシーを使います。

    - A: 誤り。権限境界は許可を与えず、ポリシーの更新は全セッションに影響する。
    - B: 誤り。用途が逆。
    - C: 正しい。
    - D: 誤り。どちらも権限の上限で、(1) の許可は与えない。

    **スキル:** [IAM の要素](../domain6.md#t6-1-entities) / **参照:** [アイデンティティベースとリソースベース](../../../services/iam.md#identity-vs-resource)、[セッションポリシー](../../../services/iam.md#session-policies)

### 問3 {#q3}

EC2 と ECS のアプリの認証情報を見直します。担当者の提案のうち適切なものはどれですか。（2つ選択）

- A. ECS のアプリの権限をタスク実行ロールにまとめる
- B. アプリのコンテナの環境変数に IAM ユーザーのキーを入れる
- C. EC2 のアプリはインスタンスプロファイルのロールを使う
- D. 全アプリで 1 つの IAM ユーザーのキーを共有する
- E. ECS のアプリの権限はタスクロールに与える

??? success "答えと解説"
    **正解: C, E**

    AWS 上のアプリはロールを使います。ECS のアプリの権限はタスクロールです。

    - A: 誤り。実行ロールはイメージの取得とログの送信用で、アプリの権限は分ける。
    - B: 誤り。長期のキーが残る。
    - C: 正しい。
    - D: 誤り。権限の分離ができず、漏えいの影響も大きい。
    - E: 正しい。

    **スキル:** [IAM の要素](../domain6.md#t6-1-entities) / **参照:** [インスタンスプロファイル](../../../services/iam.md#instance-profile)、[タスクロールと実行ロール](../../../services/containers.md#task-role-vs-execution-role)

### 問4 {#q4}

200 アカウントの開発者が、社内の Okta でサインインして、権限を 1 か所で割り当てます。ユーザーの追加と削除も自動で同期します。適切な構成はどれですか。

- A. 各アカウントの IAM に SAML プロバイダーを作り、ロールと信頼ポリシーを 200 アカウント分それぞれ設定する
- B. Cognito のユーザープールに Okta を連携して、AWS コンソールへ入る
- C. Identity Center の ID ソースに Okta を指定し、SCIM で同期して権限セットを割り当てる
- D. Directory Service の Simple AD を各アカウントに作る

??? success "答えと解説"
    **正解: C**

    複数アカウントへの人のアクセスは Identity Center です。権限セットを割り当てます。

    - A: 誤り。管理が分散し、手間が増える。
    - B: 誤り。アプリの利用者向けで、AWS の管理者向けではない。
    - C: 正しい。
    - D: 誤り。外部の IdP との連携にならない。

    **スキル:** [フェデレーション](../domain6.md#t6-1-federation) / **参照:** [IAM Identity Center](../../../services/identity-directory.md#identity-center)、[ID ソース](../../../services/identity-directory.md#idc-identity-sources)

### 問5 {#q5}

GitHub Actions から AWS へデプロイします。IAM の OIDC プロバイダーは作成済みです。信頼ポリシーで、特定のリポジトリの `main` ブランチからの引き受けだけを許可します。最も適切な条件はどれですか。

- A. `sts:ExternalId` にリポジトリ名を指定する
- B. `token.actions.githubusercontent.com:sub` で `repo:example-org/app:ref:refs/heads/main` を指定する
- C. `aws:SourceIp` に GitHub の全 IP 範囲を列挙する
- D. `token.actions.githubusercontent.com:aud` だけを確認する

??? success "答えと解説"
    **正解: B**

    `sub` にリポジトリとブランチが入るので、ここで絞ります。

    - A: 誤り。OIDC の信頼の条件にならない。
    - B: 正しい。
    - C: 誤り。リポジトリやブランチを絞れない。
    - D: 誤り。リポジトリとブランチを絞れない。IAM は `sub` か `job_workflow_ref` のない GitHub の信頼ポリシーの作成と更新を `MalformedPolicyDocument` で拒否する（この検査より前からあるロールは評価されず、他のリポジトリからも引き受けられる）。

    **スキル:** [フェデレーション](../domain6.md#t6-1-federation) / **参照:** [フェデレーション](../../../services/iam.md#federation)、[信頼ポリシー](../../../services/iam.md#trust-policy)

### 問6 {#q6}

次の 2 つの要件を選びます。(1) オンプレミスの Active Directory のユーザーで Identity Center へサインインする。ディレクトリは AWS へ移さない。(2) 自社の EC サイトの利用者のサインイン。適切な組み合わせはどれですか。

- A. (1) Simple AD、(2) IAM ユーザー
- B. (1) Cognito、(2) Identity Center
- C. (1) AD Connector、(2) Cognito
- D. (1) IAM の OIDC プロバイダー、(2) AD Connector

??? success "答えと解説"
    **正解: C**

    AD Connector はオンプレミスの AD へ要求を転送します。アプリの利用者には Cognito を使います。

    - A: 誤り。Simple AD はオンプレミスの AD への接続の手段ではなく、IAM ユーザーは利用者向けではない。
    - B: 誤り。用途が逆。
    - C: 正しい。
    - D: 誤り。どちらも用途が違う。

    **スキル:** [フェデレーション](../domain6.md#t6-1-federation) / **参照:** [AD Connector](../../../services/identity-directory.md#ad-connector)、[Amazon Cognito](../../../services/cognito.md)

### 問7 {#q7}

開発チームにアプリ用の IAM ロールを自分で作らせつつ、管理者のロールを作る昇格を防ぎます。適切な構成の組み合わせはどれですか。（2つ選択）

- A. 境界のポリシー自体の変更と、ロールからの境界の削除を拒否する
- B. SCP で `iam:CreateRole` を全面的に拒否する
- C. 全ロールにセッションポリシーを付けて、ロールの作成を制限する
- D. 開発者のロールに `iam:*` を許可し、CloudTrail で作業を確認する
- E. `iam:CreateRole` を、条件 `iam:PermissionsBoundary` で指定の境界が付く場合だけ許可する

??? success "答えと解説"
    **正解: A, E**

    境界の指定を必須にし、境界自体を守ります。

    - A: 正しい。
    - B: 誤り。ロールを作らせるという要件に反する。
    - C: 誤り。セッションポリシーは作成の統制にならない。
    - D: 誤り。昇格を防げない。
    - E: 正しい。

    **スキル:** [権限境界](../domain6.md#t6-1-boundaries) / **参照:** [権限境界の設定](../../../services/iam.md#permissions-boundary)

### 問8 {#q8}

ロールの ID ベースポリシーは `s3:*` と `ec2:*` を許可し、権限境界は `s3:*` と `dynamodb:*` を許可しています。SCP はすべて許可しています。このロールで許可される操作はどれですか。

- A. `dynamodb:*` だけ
- B. `s3:*` だけ
- C. `s3:*` と `ec2:*` と `dynamodb:*` のすべて
- D. `ec2:*` だけ

??? success "答えと解説"
    **正解: B**

    実際の権限は、ID ベースポリシーと権限境界の重なりです。

    - A: 誤り。ID ベースポリシーの許可がない。
    - B: 正しい。
    - C: 誤り。境界は許可を足さない。
    - D: 誤り。境界が許可していない。

    **スキル:** [権限境界](../domain6.md#t6-1-boundaries) / **参照:** [権限境界と SCP](../../../services/iam.md#boundaries-scp)、[権限境界の設定](../../../services/iam.md#permissions-boundary)

### 問9 {#q9}

300 アカウントの組織で、全社の上限（利用できるサービスとリージョン）は組織の管理者が決めます。各アカウントの管理者は、開発者にロールの作成を委任しつつ、権限の範囲を制限します。それぞれの仕組みの組み合わせとして適切なものはどれですか。

- A. 全社は SCP、委任は権限境界
- B. どちらも SCP
- C. 全社は各ロールの権限境界、委任は OU ごとの SCP
- D. 全社は Identity Center の権限セット、委任は OU ごとの SCP

??? success "答えと解説"
    **正解: A**

    SCP は組織としての上限、権限境界は委任の上限です。

    - A: 正しい。
    - B: 誤り。SCP は OU とアカウントに適用し、ユーザーやロールの委任に向かない。
    - C: 誤り。適用先が逆。
    - D: 誤り。権限セットはアカウントへの割り当てで全社の上限にならず、SCP はロールごとの委任に向かない。

    **スキル:** [権限境界](../domain6.md#t6-1-boundaries) / **参照:** [権限境界と SCP](../../../services/iam.md#boundaries-scp)、[それぞれの効く場所](../../../services/identity-directory.md#evaluation-layers)

### 問10 {#q10}

東京以外のリージョンの操作を SCP で拒否したところ、IAM や Organizations の操作まで拒否されました。また、管理者のロールだけ例外にしたいと考えています。適切な修正はどれですか。（2つ選択）

- A. `ArnNotLike` の `aws:PrincipalArn` で管理者のロールを除く
- B. 管理アカウントへ SCP を付けて例外にする
- C. `NotAction` でグローバルサービスを除く
- D. SCP の `Effect` を `Allow` に変える
- E. 権限境界で全リージョンを許可する

??? success "答えと解説"
    **正解: A, C**

    グローバルサービスを除かないと IAM なども拒否されます。例外は条件で書きます。

    - A: 正しい。
    - B: 誤り。管理アカウントの主体は例外になるが、メンバーの管理者の例外にはならない。
    - C: 正しい。
    - D: 誤り。`Allow` は拒否の役割にならず、許可も与えない。
    - E: 誤り。SCP の拒否は上書きできない。

    **スキル:** [SCP](../domain6.md#t6-1-scp) / **参照:** [SCP](../../../services/governance.md#scp)、[SCP と RCP の例外](../../../services/identity-directory.md#guardrail-exceptions)

### 問11 {#q11}

ある SCP は `s3:*` を許可するだけの許可リストの形です。ロールには `ec2:RunInstances` の ID ベースポリシーがあり、`s3:GetObject` の許可はありません。このロールの操作の結果はどれですか。

- A. どちらも拒否される
- B. `s3:GetObject` だけが許可される
- C. `ec2:RunInstances` だけが許可される
- D. `ec2:RunInstances` も `s3:GetObject` も許可される

??? success "答えと解説"
    **正解: A**

    SCP は権限を与えず、上限を決めるだけです。両方の許可が必要です。

    - A: 正しい。
    - B: 誤り。SCP は権限を与えないので、ID ベースの許可が必要。
    - C: 誤り。SCP の許可リストに含まれない。
    - D: 誤り。SCP が EC2 を許可していない。S3 も ID ベースの許可がない。

    **スキル:** [SCP](../domain6.md#t6-1-scp) / **参照:** [SCP](../../../services/governance.md#scp)、[ポリシー評価](../../../services/iam.md#policy-evaluation)

### 問12 {#q12}

SCP の効果についての説明のうち、正しいものはどれですか。（2つ選択）

- A. リソースベースポリシーで与えた外部のアカウントの主体にも効く
- B. 組織の管理アカウントのユーザーにも効く
- C. 組織のメンバーアカウントのルートユーザーにも効く
- D. 付与した SCP は権限を自動で与える
- E. サービスリンクロールには効かない

??? success "答えと解説"
    **正解: C, E**

    SCP の効く範囲を押さえます。

    - A: 誤り。外部の主体には効かない。
    - B: 誤り。管理アカウントには効かない。
    - C: 正しい。
    - D: 誤り。権限は与えない。
    - E: 正しい。

    **スキル:** [SCP](../domain6.md#t6-1-scp) / **参照:** [SCP](../../../services/governance.md#scp)、[サービスロールとサービスリンクロール](../../../services/iam.md#service-linked-roles)

### 問13 {#q13}

新しい Lambda の権限を `AdministratorAccess` から必要最小限にします。実際の呼び出しの履歴をもとに生成します。さらに、広すぎる権限のデプロイをパイプラインで止めます。適切な組み合わせはどれですか。

- A. Trusted Advisor のセキュリティのチェックと、ポリシーシミュレーターの手動の実行を毎月の作業にする
- B. ポリシーシミュレーターで候補を試し、デプロイの前に `cfn-lint` で構文を検査する
- C. CloudTrail の証跡を Athena で集計して手で書き、Config の `iam-policy-no-statements-with-admin-access` で検出する
- D. IAM Access Analyzer のポリシー生成と、カスタムポリシーチェック

??? success "答えと解説"
    **正解: D**

    CloudTrail の履歴から必要な権限を生成できます。ポリシーの検証をパイプラインへ組み込みます。

    - A: 誤り。履歴から生成せず、パイプラインの自動の判定にならない。
    - B: 誤り。履歴から生成せず、`cfn-lint` は権限の広さを判定しない。
    - C: 誤り。生成が手作業で、Config はデプロイの後の検出で止めない。
    - D: 正しい。

    **スキル:** [最小権限](../domain6.md#t6-1-least-privilege) / **参照:** [IAM Access Analyzer](../../../services/identity-directory.md#access-analyzer)、[ポリシーの検証とチェック](../../../services/identity-directory.md#aa-policy-checks)

### 問14 {#q14}

組織で 1 年使われていないロールと権限を見つけ、削除する前に、残す権限で必要な API が許可されるかを確かめます。適切な組み合わせはどれですか。

- A. CloudTrail の 90 日のイベント履歴と `sts:GetCallerIdentity`
- B. Trusted Advisor のセキュリティのチェックと、スタックポリシー
- C. IAM の最終アクセス情報を各アカウントで手で確認し、`sts:GetCallerIdentity` で確かめる
- D. Access Analyzer の未使用アクセスの検出と、ポリシーシミュレーター

??? success "答えと解説"
    **正解: D**

    未使用アクセスを検出し、ポリシーシミュレーターで許可と拒否をテストします。

    - A: 誤り。1 年を見られず、許可の確認にならない。
    - B: 誤り。未使用の権限の検出と、許可の確認のどちらにもならない。
    - C: 誤り。組織の規模で手作業になり、`GetCallerIdentity` は許可を確かめない。
    - D: 正しい。

    **スキル:** [最小権限](../domain6.md#t6-1-least-privilege) / **参照:** [未使用アクセスの検出](../../../services/identity-directory.md#aa-unused)、[ポリシーシミュレーター](../../../services/iam.md#policy-simulator)

### 問15 {#q15}

S3 バケットのバケットポリシーで、CloudFront の特定のディストリビューションからの読み取りだけを許可し、混乱した代理の問題も避けます。KMS キーは S3 経由でだけ使わせます。適切な条件の組み合わせはどれですか。

- A. `aws:SourceArn` と `kms:ViaService`
- B. `aws:SourceArn` と `aws:PrincipalOrgID`
- C. `aws:SourceAccount` と `aws:SecureTransport`
- D. `aws:Referer` と `kms:ViaService`

??? success "答えと解説"
    **正解: A**

    サービスの呼び出し元は `aws:SourceArn` で絞り、キーの利用は `kms:ViaService` で限定します。

    - A: 正しい。
    - B: 誤り。`aws:PrincipalOrgID` は組織の主体の限定で、キーの利用を S3 経由に限定しない。
    - C: 誤り。アカウントまでしか絞れず、特定のディストリビューションやキーの利用を限定しない。
    - D: 誤り。Referer は利用者が偽装でき、ディストリビューションの限定にならない。

    **スキル:** [最小権限](../domain6.md#t6-1-least-privilege) / **参照:** [条件とアクセス制御](../../../services/iam.md#conditions)、[kms:ViaService](../../../services/kms.md#via-service)

### 問16 {#q16}

プロジェクトが毎月増え、そのたびにロールとポリシーを追加する作業が負担です。リソースと利用者のセッションのタグは `Project` で揃っています。プロジェクトが増えてもポリシーを更新しないようにします。1 つのポリシーで済ませるには、どう書きますか。

- A. プロジェクトごとのロールとポリシーの作成をパイプラインで自動化する
- B. `aws:ResourceTag/Project` が `${aws:PrincipalTag/Project}` と一致するときに許可する
- C. `aws:RequestTag/Project` だけを条件にして、利用者のタグとは比べない
- D. プロジェクトごとのリソースの ARN をすべて `Resource` に列挙し、毎月スクリプトで更新する

??? success "答えと解説"
    **正解: B**

    ABAC ならタグを付けるだけで対象になります。

    - A: 誤り。ポリシーを増やす作業が自動になるだけで、1 つのポリシーにならない。
    - B: 正しい。
    - C: 誤り。作成時に付けるタグの条件で、既存のリソースへのアクセスの判定にならない。
    - D: 誤り。毎月の更新が残る。

    **スキル:** [RBAC と ABAC](../domain6.md#t6-1-rbac-abac) / **参照:** [条件とアクセス制御](../../../services/iam.md#conditions)、[セッションタグ](../../../services/iam.md#session-tags)

### 問17 {#q17}

Identity Center の利用者の部署の属性で、S3 のオブジェクトへのアクセスを制御します。開発者が勝手にリソースのタグを変更して権限を広げる問題も防ぎます。適切な組み合わせはどれですか。（2つ選択）

- A. タグの変更の操作を条件で制限する
- B. Identity Center のアクセス制御の属性でセッションタグとして渡す
- C. 部署ごとに別の権限セットを作り、全リソースの ARN を列挙する
- D. Identity Center のグループごとに、バケットポリシーへ部署の ARN を列挙する
- E. S3 のアクセスポイントを部署ごとに作り、リソースのタグとは別に管理する

??? success "答えと解説"
    **正解: A, B**

    Identity Center から属性をセッションタグとして渡します。タグを勝手に変更されないよう制限します。

    - A: 正しい。
    - B: 正しい。
    - C: 誤り。RBAC のままで、増加に対応しにくい。
    - D: 誤り。属性を使わず、部署が増えるたびに更新が要る。
    - E: 誤り。属性による制御にならず、タグの変更の防止にもならない。

    **スキル:** [RBAC と ABAC](../domain6.md#t6-1-rbac-abac) / **参照:** [ABAC](../../../services/identity-directory.md#idc-abac)、[タグ戦略](../../../services/governance.md#tagging-strategy)

### 問18 {#q18}

監査、運用、請求という職務が固定された 3 つの役割の権限と、四半期ごとに増えるチームごとのデータのアクセスを設計します。リソースのタグは自動で付与されます。ポリシーの更新の作業を最小にします。適切な組み合わせはどれですか。

- A. どちらも RBAC で、チームが増えるたびにロールを追加する
- B. どちらも SCP で許可を与える
- C. 3 つの役割は RBAC、チームごとのデータは ABAC
- D. 3 つの役割も ABAC のみで、チームごとのデータは個別のユーザーへ付与する

??? success "答えと解説"
    **正解: C**

    職務が固定なら RBAC、チームやプロジェクトが増えるなら ABAC が向きます。

    - A: 誤り。チームの増加でロールが増える。
    - B: 誤り。SCP は権限を与えない。
    - C: 正しい。
    - D: 誤り。チームの増加で個別の付与が増える。

    **スキル:** [RBAC と ABAC](../domain6.md#t6-1-rbac-abac) / **参照:** [ポリシー変数](../../../services/iam.md#policy-variables)、[最小権限](../../../services/iam.md#least-privilege)

### 問19 {#q19}

本番の削除の操作には MFA を必須にします。CLI で作業する IAM ユーザーが、長期のキーのままでも同じ条件を満たせるようにします。適切な組み合わせはどれですか。

- A. 条件 `aws:MultiFactorAuthPresent` で拒否し、ユーザーに MFA デバイスを追加するだけにする
- B. 条件 `aws:MultiFactorAge` で拒否し、`GetFederationToken` に MFA のコードを渡す
- C. 条件 `aws:MultiFactorAuthPresent` で拒否し、`AssumeRoleWithWebIdentity` に MFA のコードを渡す
- D. 条件 `aws:MultiFactorAuthPresent` で拒否し、`GetSessionToken` に MFA のコードを渡して一時的な認証情報を得る

??? success "答えと解説"
    **正解: D**

    長期のキーの呼び出しには MFA の情報が含まれません。拒否の条件には `BoolIfExists` を使い、`GetSessionToken` で MFA 付きの一時的な認証情報を得ます。

    - A: 誤り。長期のキーのままの呼び出しに MFA の情報は含まれない。
    - B: 誤り。`GetFederationToken` は MFA のコードを受け取らない。
    - C: 誤り。`AssumeRoleWithWebIdentity` は MFA のコードを受け取らず、用途も違う。
    - D: 正しい。

    **スキル:** [MFA と STS](../domain6.md#t6-1-mfa-sts) / **参照:** [GetSessionToken と MFA](../../../services/iam.md#mfa)、[API の比較](../../../services/iam.md#sts-api-compare)

### 問20 {#q20}

開発者に Lambda の作成を許可しました。監査で、開発者が既存の管理者のロールを関数に渡して権限を昇格できることが指摘されました。開発者はアプリ用のロール `app-*` だけを関数に指定できれば十分です。何で防ぎますか。

- A. `iam:PassRole` の `Resource` は `*` のままで、`iam:PassedToService` だけを Lambda に絞る
- B. 権限境界で `lambda:CreateFunction` を許可し、実行ロールの指定は CloudTrail で事後に確認する
- C. SCP で開発者の `iam:CreateRole` を拒否する
- D. `iam:PassRole` を特定のロールと `iam:PassedToService` に絞る

??? success "答えと解説"
    **正解: D**

    サービスに渡せるロールを `iam:PassRole` で制限します。

    - A: 誤り。管理者のロールも Lambda へ渡せるままになる。
    - B: 誤り。渡すロールの制限にならず、事後の確認では防げない。
    - C: 誤り。既存のロールを渡す問題が残る。
    - D: 正しい。

    **スキル:** [MFA と STS](../domain6.md#t6-1-mfa-sts) / **参照:** [iam:PassRole](../../../services/iam.md#passrole)

### 問21 {#q21}

EC2 のアプリが別のアカウントの S3 を読みます。また、外部の SaaS が自社のアカウントのロールを引き受けます。適切な組み合わせはどれですか。（2つ選択）

- A. `aws:PrincipalOrgID` で外部の SaaS を許可する
- B. EC2 のインスタンスプロファイルのロールから、相手のアカウントのロールを `AssumeRole` する
- C. SaaS の事業者に IAM ユーザーを発行し、長期のキーを渡して定期的に更新する
- D. SaaS の信頼ポリシーの条件に `sts:ExternalId` を指定する
- E. EC2 に相手のアカウントの IAM ユーザーのキーを配置する

??? success "答えと解説"
    **正解: B, D**

    別のアカウントには `AssumeRole`、外部には `ExternalId` で混乱した代理を防ぎます。

    - A: 誤り。自組織に限定する条件で、外部の SaaS に合わない。
    - B: 正しい。
    - C: 誤り。長期のキーが社外に残る。
    - D: 正しい。
    - E: 誤り。長期のキーが残る。

    **スキル:** [MFA と STS](../domain6.md#t6-1-mfa-sts) / **参照:** [ロールの引き受け](../../../services/iam.md#assume-role)、[インスタンスプロファイル](../../../services/iam.md#instance-profile)、[ExternalId と混乱した代理問題](../../../services/iam.md#external-id)
