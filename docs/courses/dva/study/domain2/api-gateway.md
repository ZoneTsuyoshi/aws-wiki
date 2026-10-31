# 分野2: API Gateway

API の呼び出しをどう認証、認可するかを問います。統合やマッピングは[分野1](../domain1/api-gateway.md)、ステージとデプロイは[分野3](../domain3/api-gateway.md)、エラーの調査やキャッシュは[分野4](../domain4/api-gateway.md)で扱います。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.1.2](../../domain2.md#skill-2-1-2) | オーソライザー、スコープ、リソースポリシー |
| [2.1.5](../../domain2.md#skill-2-1-5) | IAM 認証と SigV4 での呼び出し |

## 学習の順番 {#study-order}

1. [認可](../../../../services/api-gateway.md#authorizers): 5 つの方式と向いている場面を比べます。
2. [Cognito オーソライザー](../../../../services/api-gateway.md#cognito-authorizer)と[その設定](../../../../services/api-gateway.md#cognito-authorizer-settings): ID トークンとアクセストークンの違いを確認します。
3. [Lambda オーソライザー](../../../../services/api-gateway.md#lambda-authorizer): `TOKEN` と `REQUEST`、キャッシュの動き、ステータスコードを覚えます。
4. [HTTP API のオーソライザー](../../../../services/api-gateway.md#http-api-authorizers): JWT オーソライザーとシンプルレスポンスを押さえます。
5. [IAM 認証](../../../../services/api-gateway.md#iam-auth)と[リソースポリシー](../../../../services/api-gateway.md#resource-policy): `execute-api:Invoke` と、同じアカウントと別アカウントでの許可の違いを理解します。
6. [使用量プランと API キー](../../../../services/api-gateway.md#usage-plans): API キーが認証ではないことと、キーソース `AUTHORIZER` を確認します。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| `authorizerResultTtlInSeconds` | 既定 300。0〜3,600 | 0 でキャッシュなし |
| `Deny` を返す | 403（`ACCESS_DENIED`） | 未認証は 401（`UNAUTHORIZED`） |
| 関数の失敗、不正な応答 | 500（`AUTHORIZER_FAILURE` など） | 認可の結果ではない |
| HTTP API の Lambda オーソライザー | 応答待ちは 10 秒まで | |
| リソースポリシー | 8,192 文字 | REST API の機能 |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| AWS の認証情報を持つクライアントに呼ばせる | IAM 認証（SigV4）と `execute-api:Invoke` |
| アプリのユーザーのログインで認可する | `COGNITO_USER_POOLS` オーソライザー |
| カスタムスコープで認可する | メソッドに `authorizationScopes` を設定し、アクセストークンを送る |
| 独自のトークンや外部の IdP を使う | Lambda オーソライザー。AWS は `REQUEST` を勧めている |
| テナント別に判定し、キャッシュも分ける | `REQUEST` で `Authorization` とクエリ `tenant` をアイデンティティソースにする |
| 別アカウントから IAM 認証で呼ばせる | 呼び出し元の IAM ポリシーと API のリソースポリシーの両方で許可する |
| 特定の IP や VPC エンドポイントだけに制限する | リソースポリシー |
| クライアントが `X-API-Key` を送れない | キーソース `AUTHORIZER` と `usageIdentifierKey` |
| クライアントも証明書で認証する | カスタムドメインの [mutual TLS](../../../../services/certificates.md#mtls) |
| 権限のない相手にキャッシュを消させない | [Require authorization](../../../../services/api-gateway.md#cache-invalidation) と `execute-api:InvalidateCache` |

## 引っかかりやすい点 {#traps}

- `event["methodArn"]` だけを許可するポリシーをキャッシュすると、同じトークンの別のメソッドが 403 になります。全メソッドに使えるポリシーを返すか、キャッシュキーを分けます。
- `REQUEST` でキャッシュを有効にすると、アイデンティティソースが欠けたリクエストは関数を呼ばずに 401 で拒否されます。
- API キーは認証の手段ではありません。IAM、Cognito、Lambda オーソライザーを使います。
- リソースポリシーの変更も、再デプロイしないと反映されません。
- HTTP API の JWT オーソライザーは、ID トークンとアクセストークンを標準では区別できません。ID トークンを受け入れないならスコープを必須にします。
- ステージ変数に機密情報を入れません。`dataTraceEnabled` は本文までログに残すので、本番では使いません。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [api-gateway 問10](../../exercises/api-gateway.md#q10) | 2.1.2 | 顧客の端末は X-API-Key ヘッダーを送れません。そこで Lambda オーソライザーがトーク… |
| [api-gateway 問15](../../exercises/api-gateway.md#q15) | 2.1.2 | TOKEN タイプの Lambda オーソライザーで TTL を 300 秒にしています。関数は e… |
| [api-gateway 問16](../../exercises/api-gateway.md#q16) | 2.1.2 | REQUEST タイプの Lambda オーソライザーで、キャッシュを有効にし、アイデンティティソー… |

<!-- questions:end -->
