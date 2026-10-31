# 分野2: IAM と STS

分野2の中心です。ポリシーがどう評価されるか、ロールをどう引き受けるか、外部の ID やプログラムからどう AWS にアクセスするかを問います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.1.1](../../domain2.md#skill-2-1-1) | SAML、OIDC、IAM Identity Center によるフェデレーション |
| [2.1.2](../../domain2.md#skill-2-1-2) | 条件キー、MFA、セッショントークン |
| [2.1.3](../../domain2.md#skill-2-1-3) | 実行環境ごとの認証情報とプロバイダーチェーン |
| [2.1.5](../../domain2.md#skill-2-1-5) | SigV4 による署名 |
| [2.1.6](../../domain2.md#skill-2-1-6) | プリンシパル、ポリシーの種類、評価の順序 |
| [2.1.7](../../domain2.md#skill-2-1-7) | AssumeRole、信頼ポリシー、クロスアカウント |

## 学習の順番 {#study-order}

1. [プリンシパル](../../../../services/iam.md#principals): 長期と一時の認証情報の違い、`iam:PassRole` と信頼ポリシーの違いをつかみます。
2. [ポリシー評価](../../../../services/iam.md#policy-evaluation): 明示的な Deny の優先と、和集合と積集合の場面を覚えます。続けて[権限境界と SCP](../../../../services/iam.md#boundaries-scp) で上限の仕組みを見ます。
3. [アイデンティティベースとリソースベース](../../../../services/iam.md#identity-vs-resource): `Principal` の有無と、別アカウントへ許可できるかの違いを整理します。
4. [条件とアクセス制御](../../../../services/iam.md#conditions): 主な条件キーと ABAC を押さえ、[条件演算子](../../../../services/iam.md#condition-operators)で `IfExists` と `ForAllValues` を確認します。
5. [ロールの引き受け](../../../../services/iam.md#assume-role): 信頼ポリシーと許可ポリシーの役割、`DurationSeconds` を理解し、[API の比較](../../../../services/iam.md#sts-api-compare)で STS の API を見分けます。
6. [クロスアカウントアクセス](../../../../services/iam.md#cross-account): リソースベースポリシーとロールの引き受けの選び方を学びます。
7. [フェデレーション](../../../../services/iam.md#federation)と [GetSessionToken と MFA](../../../../services/iam.md#mfa): 方式ごとの API と、MFA 付きの一時認証情報の取り方を覚えます。
8. [プログラムからのアクセス](../../../../services/iam.md#programmatic-access)と [SigV4](../../../../services/iam.md#sigv4): 実行環境別の渡し方、チェーンの順序、署名エラーの見分け方を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| `MaxSessionDuration` | 既定 1 時間。1〜12 時間 | 長くするだけでは足りない。`DurationSeconds` も指定する |
| `DurationSeconds`（ロール） | 既定 1 時間。最短 900 秒 | 省略すると `MaxSessionDuration` に関係なく 1 時間 |
| ロールチェーン | 最大 1 時間 | より長い値を指定すると失敗する |
| `GetSessionToken`（IAM ユーザー） | 15 分〜36 時間。既定 12 時間 | ルートユーザーは最大 1 時間 |
| セッションポリシー | 合計 2,048 文字、管理ポリシー 10 個 | 権限は増やせない |
| セッションタグ | 50 個 | 信頼ポリシーに `sts:TagSession` が必要 |
| アクセスキー | ユーザーごとに 2 つ | ローテーションのために 2 つ持てる |
| SigV4 のタイムスタンプ | 原則 5 分以内に到達 | 時計のずれで期限切れエラーになる |
| IMDS のホップ制限 | 既定 1 | EC2 上のコンテナからは 2 にする |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 別アカウントの S3 に読み書きすると 403 | 呼び出し側とバケット側の両方に Allow が必要 |
| 自分のバケットから相手のバケットへコピーする | 両方に同時にアクセスするのでリソースベースポリシー。元の権限を維持できる |
| 相手アカウントの複数サービスをまとめて操作する | ロールの引き受け。呼び出し側の `sts:AssumeRole` と信頼ポリシーの両方が必要 |
| 第三者の SaaS にアクセスを許可する | ロールと `ExternalId`。値は SaaS 側が顧客ごとに発行する |
| GitHub Actions に長期キーを置きたくない | OIDC と `AssumeRoleWithWebIdentity`。信頼ポリシーで `sub` を絞る |
| CLI から MFA 必須の API を呼ぶ | `GetSessionToken` に `SerialNumber` と `TokenCode` を渡す。他アカウントなら信頼ポリシーで MFA を要求した `AssumeRole` |
| 4 時間かかるバッチのセッションが切れる | `MaxSessionDuration` に加えて `DurationSeconds=14400` を指定する |
| 開発者が作るロールに上限を設ける | 権限境界。組織全体のガードレールなら SCP |
| チームごとに S3 のパスを分ける | `${aws:PrincipalTag/team}` のポリシー変数と ABAC |
| 拒否の原因を調べる | まず `sts:GetCallerIdentity`。エンコードされた拒否は `sts:DecodeAuthorizationMessage` |

## 引っかかりやすい点 {#traps}

- EC2 に正しいロールを付けたのに権限エラーが出ます。環境変数や `~/.aws/credentials` の古いキーがチェーンで先に使われています。
- `my-bucket/*` だけを許可すると `ListObjectsV2` が `AccessDenied` になります。`s3:ListBucket` はバケットの ARN に対する操作です。
- `ForAllValues` はキーがないときや値が空のときも真になります。`Allow` では `Null` でキーの存在も確認します。
- VPC エンドポイント経由のリクエストには `aws:SourceIp` の値が入りません。`aws:SourceVpc` や `aws:SourceVpce` を使います。
- `SignatureDoesNotMatch` は署名の問題で、`AccessDenied` は署名が通った後のポリシーの問題です。確認先が変わります。
- `Version` を省略すると `${...}` がただの文字列として扱われ、ポリシー変数が効きません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [iam 問1](../../exercises/iam.md#q1) | 2.1.6 | ある開発者は、S3 バケット reports の一覧を取得するアプリのロールに、次の文だけを付けまし… |
| [iam 問2](../../exercises/iam.md#q2) | 2.1.6 | ポリシーに {"Effect": "Allow", "NotAction": "iam:*", "R… |
| [iam 問3](../../exercises/iam.md#q3) | 2.1.2 | 条件 {"StringLikeIfExists": {"ec2:InstanceType": ["t… |
| [iam 問4](../../exercises/iam.md#q4) | 2.1.2 | Allow の文に {"ForAllValues:StringEquals": {"aws:TagK… |
| [iam 問5](../../exercises/iam.md#q5) | 2.1.6 | 開発チームはポリシーの Resource を arn:aws:s3:::data/${aws:Pri… |
| [iam 問6](../../exercises/iam.md#q6) | 2.1.6 | 3 つの主体だけで共有する権限を、主体の削除と一緒に消えず、バージョン管理してロールバックできるよう… |
| [iam 問7](../../exercises/iam.md#q7) | 2.1.7 | ロールの MaxSessionDuration を 8 時間にしました。アプリは AssumeRol… |
| [iam 問8](../../exercises/iam.md#q8) | 2.1.7 | Lambda の実行ロール A が、別のロール B を AssumeRole します。ロール B の… |
| [iam 問9](../../exercises/iam.md#q9) | 2.1.2 | STS の次の API のうち、セッションポリシーを渡せないものはどれですか。 |
| [iam 問10](../../exercises/iam.md#q10) | 2.1.3 | カスタム ID ブローカーが GetFederationToken で一時認証情報を発行しました。こ… |
| [iam 問11](../../exercises/iam.md#q11) | 2.1.7 | マルチテナントのアプリで、広い権限のロールを引き受けるときに、テナント A のパスだけに絞ったポリシ… |
| [iam 問12](../../exercises/iam.md#q12) | 2.1.7 | セッションポリシーとセッションタグをそれぞれ上限内で渡したのに、AssumeRole が Packe… |
| [iam 問13](../../exercises/iam.md#q13) | 2.1.7 | 共有の管理者ロールを複数の担当者が使っています。セッション名は書き換えられるので、ロールチェーンの先… |
| [iam 問14](../../exercises/iam.md#q14) | 2.1.6 | 開発者に Lambda の実行ロールを作らせたいが、上限より大きな権限は持たせたくありません。作成で… |
| [iam 問15](../../exercises/iam.md#q15) | 2.1.6 | ロールの許可ポリシーは dynamodb:* だけで、権限境界は s3:* だけです。別のポリシーや… |
| [iam 問16](../../exercises/iam.md#q16) | 2.1.6 | 開発者が CLI で Lambda 関数を作成すると、iam:PassRole についての Acce… |
| [iam 問17](../../exercises/iam.md#q17) | 2.1.6 | サービスリンクロールについて正しいものはどれですか。 |
| [iam 問18](../../exercises/iam.md#q18) | 2.1.5 | EC2 の API が UnauthorizedOperation とエンコードされたメッセージを返… |
| [iam 問19](../../exercises/iam.md#q19) | 2.1.3 | EC2 上のコンテナのアプリから、IMDSv2 で認証情報を取得するのに失敗します。HttpToke… |
| [iam 問20](../../exercises/iam.md#q20) | 2.1.6 | 新しいポリシーを本番に適用する前に確認したいと考えています。IAM の機能の説明として正しいものを選… |

<!-- questions:end -->
