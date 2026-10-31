# 分野4: 認可

要件に合う認可の仕組みを選び、属性で権限を決め、権限の上限を設計する力を問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [4.2.1](../../domain4.md#skill-4-2-1) | 認可の統制の設計 |
| [4.2.2](../../domain4.md#skill-4-2-2) | ABAC と RBAC |
| [4.2.3](../../domain4.md#skill-4-2-3) | 最小権限のポリシーの設計 |

## 学習の順番 {#study-order}

1. [Verified Permissions](../../../../services/identity-directory.md#verified-permissions): アプリの中の認可を切り出す役割と、Cedar の既定の拒否を押さえます。
2. [クロスアカウントアクセス](../../../../services/iam.md#cross-account)と[信頼ポリシー](../../../../services/iam.md#trust-policy): ロールの引き受けとリソースポリシーの違いを理解します。
3. [ExternalId](../../../../services/iam.md#external-id): 混乱した代理の防ぎ方を確認します。
4. [認証情報プロバイダーチェーン](../../../../services/iam.md#credential-chain): AWS の外のワークロードの認証情報の流れを確認します。
5. [条件とアクセス制御](../../../../services/iam.md#conditions)と[セッションタグ](../../../../services/iam.md#session-tags): ABAC の基本形と `TransitiveTagKeys` を覚えます。
6. [権限境界と SCP](../../../../services/iam.md#boundaries-scp)、[権限境界の設定](../../../../services/iam.md#permissions-boundary)、[セッションポリシー](../../../../services/iam.md#session-policies): 上限の仕組みは権限を与えないことを押さえます。
7. [PassRole](../../../../services/iam.md#passrole)と[最小権限](../../../../services/iam.md#least-privilege): 権限の昇格の防止と、ポリシーの生成を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| セッションポリシー | 合計 2,048 文字。管理ポリシーは最大 10 個 | ロールを増やさずに絞る |
| Cedar の判定 | 既定は拒否。`forbid` が優先 | 明示の許可が必要 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 自作アプリの細かい認可 | Verified Permissions。JWT なら `IsAuthorizedWithToken` |
| AWS の外のサーバーに長期のキーを渡したくない | IAM Roles Anywhere。`aws:SourceArn` でトラストアンカーを絞る |
| 第三者の SaaS にロールを引き受けさせる | `sts:ExternalId` |
| 元の権限のまま別アカウントのリソースも使う | リソースポリシー |
| プロジェクトの増減が多い | ABAC |
| 役割が固定で、ポリシーの一覧で説明する | RBAC |
| 開発者に作らせるロールの上限 | 権限境界と `iam:PermissionsBoundary` |
| 共通のロールをテナントごとに絞る | セッションポリシー |
| 実際の活動から最小権限を作る | Access Analyzer のポリシーの生成 |

## 引っかかりやすい点 {#traps}

- IAM パスは `Resource` の指定に便利ですが、パス自体は権限を与えも制限もしません。
- 権限境界を使うときは、境界を外す操作と境界のポリシーの変更も拒否します。
- ABAC では、タグを変更する権限がそのまま権限の昇格の経路になります。
- セッションタグは既定でロールチェーンに引き継がれません。
- 使える権限はアイデンティティポリシー、権限境界、セッションポリシーの共通部分です。
- トラストアンカーの信頼はアカウント単位です。条件を書かないと、他のトラストアンカーの証明書でもロールを引き受けられます。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [authorization 問1](../../exercises/authorization.md#q1) | 4.2.1 | SaaS の開発チームが、自社アプリの中で「文書の所有者と同じ部署のマネージャーだけが承認できる」と… |
| [authorization 問2](../../exercises/authorization.md#q2) | 4.2.1 | オンプレミスのサーバーのアプリが S3 を読みます。アクセスキーの配布をやめたいと考えています。社内… |
| [authorization 問3](../../exercises/authorization.md#q3) | 4.2.1 | 監視の SaaS を提供する第三者に、自社アカウントのロールを引き受けさせます。その第三者は多数の顧… |
| [authorization 問4](../../exercises/authorization.md#q4) | 4.2.1 | チームごとに作るロールを整理します。iam:PassRole を「チーム A のロールだけ」に絞りた… |
| [authorization 問5](../../exercises/authorization.md#q5) | 4.2.1 | 別アカウントのチームが 200 個の S3 オブジェクトを自分のアカウントへコピーします。コピーを実… |
| [authorization 問6](../../exercises/authorization.md#q6) | 4.2.2 | 新しいプロジェクトが月に 10 件増えます。現在はプロジェクトごとに IAM ポリシーとロールを作っ… |
| [authorization 問7](../../exercises/authorization.md#q7) | 4.2.2 | ABAC を導入した後の監査で、開発者が自分の EC2 インスタンスの Project タグを他のプ… |
| [authorization 問8](../../exercises/authorization.md#q8) | 4.2.2 | ロール A でセッションタグ Department=finance を付けて AssumeRole … |
| [authorization 問9](../../exercises/authorization.md#q9) | 4.2.2 | 10 人の役割が明確で、3 年間ほぼ変わらない経理チームがあります。監査では「誰がどの権限を持つか」… |
| [authorization 問10](../../exercises/authorization.md#q10) | 4.2.3 | 開発チームに Lambda の実行ロールを自分で作らせます。ただし、作るロールの権限が決められた範囲… |
| [authorization 問11](../../exercises/authorization.md#q11) | 4.2.3 | マルチテナントの SaaS です。バックエンドは共通のロールを引き受け、S3 の data/<テナン… |
| [authorization 問12](../../exercises/authorization.md#q12) | 4.2.3 | 共通のロールに s3:* を許可し、セッションポリシーで s3:GetObject だけを許可しまし… |
| [authorization 問13](../../exercises/authorization.md#q13) | 4.2.3 | 新しいバッチのロールは最初に広めの権限で動かしました。本番の前に、実際に使った操作に基づいて最小権限… |

<!-- questions:end -->
