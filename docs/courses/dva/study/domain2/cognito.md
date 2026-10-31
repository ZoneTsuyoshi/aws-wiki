# 分野2: Cognito

利用者をどう認証し、その結果を API や AWS サービスの認可にどうつなぐかを問います。2つのプールの使い分けとトークンの扱いが中心です。

## 問われるスキル {#skills}

| スキル | 内容 |
|---|---|
| [2.1.1](../../domain2.md#skill-2-1-1) | ユーザープールと ID プールによるフェデレーション |
| [2.1.2](../../domain2.md#skill-2-1-2) | トークン、スコープ、グループ、MFA |
| [2.2.2](../../domain2.md#skill-2-2-2) | カスタムドメインの ACM 証明書 |

## 学習の順番 {#study-order}

1. [ユーザープールと ID プール](../../../../services/cognito.md#user-vs-identity-pools): 出力が JWT か AWS の認証情報かで見分けます。
2. [フェデレーション](../../../../services/cognito.md#federation)と [OAuth フロー](../../../../services/cognito.md#oauth-flows): IdP との連携と、グラントの選び方を覚えます。
3. [トークン](../../../../services/cognito.md#tokens): 3種類の用途と有効期間を押さえ、[JWT の検証](../../../../services/cognito.md#jwt-verification)の項目を確認します。
4. [API Gateway との統合](../../../../services/cognito.md#api-gateway): どのトークンで通るかを理解し、[オーソライザーの設定](../../../../services/cognito.md#authorizer-settings)で値を見ます。
5. [ID プールとロールマッピング](../../../../services/cognito.md#identity-pools): ロールの決まり方と、`dynamodb:LeadingKeys` の例を学びます。
6. [グループとカスタム属性](../../../../services/cognito.md#groups-attributes)と[アプリケーションレベルの認可](../../../../services/cognito.md#app-authorization): 権限判定に使ってよい値と、判定の場所を整理します。
7. [MFA](../../../../services/cognito.md#mfa)と[脅威保護](../../../../services/cognito.md#threat-protection): 設定の3種類と、アダプティブ認証の進め方を確認します。
8. [ドメイン](../../../../services/cognito.md#domain-settings): カスタムドメインの証明書の置き場所を覚えます。

## 覚える値 {#values}

| 項目 | 値 | 判断のポイント |
|---|---|---|
| ID、アクセストークン | 既定 1 時間。5 分〜1 日 | 長いほど権限の変更が遅れて反映される |
| リフレッシュトークン | 既定 30 日。60 分〜10 年 | ローテーションしても期限は延びない |
| Lambda トリガーの応答 | 5 秒（変更不可） | カスタム送信者以外は同期呼び出し |
| カスタム属性 | 50 個 | 削除、改名、型の変更はできない |
| ID プールのルール | プロバイダーごとに 25 個 | 先頭から評価し、最初の一致を使う |
| カスタムドメインの証明書 | `us-east-1` | プールが東京にあっても同じ |

## こう問われたらこう考える {#decisions}

| 状況 | 判断 |
|---|---|
| 自作 API を呼ぶアプリのログイン | ユーザープール |
| モバイルアプリから S3 に直接アップロードする | ユーザープールのトークンを ID プールで一時認証情報に交換する |
| ログイン前のゲストに限定的な権限を与える | ID プールの未認証ロール |
| SPA やモバイルでトークンを取得する | 認可コードグラントと PKCE |
| サービス間の認証 | クライアント認証情報グラント。発行はアクセストークンのみ |
| ユーザーが自分の DynamoDB 項目だけを操作する | `dynamodb:LeadingKeys` と `${cognito-identity.amazonaws.com:sub}` |
| グループごとに AWS の権限を変える | グループに IAM ロールを割り当て、ID プールで「トークンから選択」 |
| 別の API や別のアプリ向けのトークンを防ぐ | アクセストークンは `client_id`、ID トークンは `aud` と `token_use` を確認する |
| トークンに独自のクレームを追加する | Pre token generation トリガー。アクセストークンを変えるなら `V2_0` 以上（Essentials か Plus プラン） |
| リスクが高いサインインにだけ MFA を要求する | Plus プランの脅威保護。監査のみで 2 週間以上見てから全機能にする |

## 引っかかりやすい点 {#traps}

- 連携ユーザーには Cognito の MFA が適用されません。MFA は IdP 側で設定します。
- トークンは暗号化ではなく base64url エンコードなので、誰でも読めます。秘密情報を入れません。
- 署名と期限の確認だけでは、失効したトークンを検出できません。アクセストークンの有効期間を短くするか、Cognito に問い合わせます。
- REST API でスコープを設定していないのにアクセストークンを送ると拒否されます。スコープ未設定なら ID トークンです。
- 同じ `Precedence` で異なるロールのグループに属すと、`cognito:preferred_role` が設定されません。`AmbiguousRoleResolution` に従います。
- ロールマッピングがある ID プールで基本フローを呼ぶとエラーになります。拡張フローを使います。

## 問題 {#questions}

<!-- questions:start -->

| 問題 | スキル | 内容 |
|---|---|---|
| [cognito 問1](../../exercises/cognito.md#q1) | 2.1.1 | 運用中のユーザープールで、ユーザー名に加えてメールでもサインインできるようにしたいと考えています。プ… |
| [cognito 問2](../../exercises/cognito.md#q2) | 2.1.1 | AdminCreateUser で作った利用者が、10 日後に初めてサインインしようとすると失敗しま… |
| [cognito 問3](../../exercises/cognito.md#q3) | 2.1.1 | SPA のアプリクライアントを作成するとき、ブラウザに秘密を置きたくありません。最も適切な設定はどれ… |
| [cognito 問4](../../exercises/cognito.md#q4) | 2.1.2 | アプリクライアントでアクセストークンと ID トークンの有効期間を指定しなかった場合の既定値はどれで… |
| [cognito 問5](../../exercises/cognito.md#q5) | 2.1.2 | リフレッシュトークンのローテーションを有効にしたところ、既存のアプリの更新処理が失敗するようになりま… |
| [cognito 問6](../../exercises/cognito.md#q6) | 2.2.2 | 東京リージョンのユーザープールに auth.example.com のカスタムドメインを設定します。… |
| [cognito 問7](../../exercises/cognito.md#q7) | 2.1.2 | REST API のメソッドに orders-api/read のスコープを要求する設定にしました。… |
| [cognito 問8](../../exercises/cognito.md#q8) | 2.1.1 | ある利用者が admin（Precedence 5、ロール R1）と staff（Precedenc… |
| [cognito 問9](../../exercises/cognito.md#q9) | 2.1.1 | アダプティブ認証を導入します。AWS の推奨に沿う進め方として最も適切なものはどれですか。 |
| [cognito 問10](../../exercises/cognito.md#q10) | 2.1.1 | Lambda トリガーの説明として正しいものを選んでください。（2つ選択） |
| [cognito 問11](../../exercises/cognito.md#q11) | 2.1.1 | 既存のユーザー DB から、パスワードを再設定させずに Cognito へ順次移行します。User … |
| [cognito 問12](../../exercises/cognito.md#q12) | 2.1.1 | Pre token generation でアクセストークンにスコープを追加する関数を作りましたが、… |
| [cognito 問13](../../exercises/cognito.md#q13) | 2.1.1 | ルールでロールを選択する ID プールで、基本フローの GetOpenIdToken を呼ぶとエラー… |
| [cognito 問14](../../exercises/cognito.md#q14) | 2.1.1 | 自社の認証基盤で認証した利用者に、ID プールの認証情報を発行します。GetCredentialsF… |
| [cognito 問15](../../exercises/cognito.md#q15) | 2.1.2 | 自作の API で JWT を自分で検証します。次のうち、検証に含めるべきものを選んでください。（2… |

<!-- questions:end -->
