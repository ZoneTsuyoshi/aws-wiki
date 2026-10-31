# Cognito の問題集

対象の解説: [Amazon Cognito](../../../services/cognito.md)

### 問1 {#q1}

運用中のユーザープールで、ユーザー名に加えてメールでもサインインできるようにしたいと考えています。プールは作成時にエイリアス属性もユーザー名属性も指定していません。最も適切な対応はどれですか。

- A. 既存のプールの設定でエイリアス属性を追加する
- B. アプリクライアントの `ReadAttributes` に `email` を追加する
- C. Pre sign-up トリガーで `email` を別名に設定する
- D. 新しいプールを作り、利用者を移行する

??? success "答えと解説"
    **正解: D**

    サインイン属性の方式は作成後に変更できません。User migration トリガーなどで移行します。

    - A: 誤り。作成後は変更できない。
    - B: 誤り。属性の読み取り権限で、サインインとは関係がない。
    - C: 誤り。トリガーで方式は変えられない。
    - D: 正しい。

    **スキル:** C03 2.1.1 / **参照:** [サインイン属性](../../../services/cognito.md#sign-in-attributes)

### 問2 {#q2}

`AdminCreateUser` で作った利用者が、10 日後に初めてサインインしようとすると失敗します。パスワードポリシーの `TemporaryPasswordValidityDays` は設定していません。原因として最も適切なものはどれですか。

- A. 一時パスワードの既定の有効期間 7 日を過ぎている
- B. 確認コードの有効期間 24 時間を過ぎている
- C. リフレッシュトークンの有効期間を過ぎている
- D. パスワードの最小長が 6 文字より短い

??? success "答えと解説"
    **正解: A**

    既定は 7 日で、最大 365 日です。過ぎたら、管理者が `MessageAction=RESEND` で送り直すなどの対応をします。

    - A: 正しい。
    - B: 誤り。これは自分でサインアップしたときの確認コード。
    - C: 誤り。まだサインインしていないのでトークンがない。
    - D: 誤り。最小長の範囲は 6〜99 で、期間とは関係ない。

    **スキル:** C03 2.1.1 / **参照:** [パスワードポリシー](../../../services/cognito.md#password-policy)

### 問3 {#q3}

SPA のアプリクライアントを作成するとき、ブラウザに秘密を置きたくありません。最も適切な設定はどれですか。

- A. `GenerateSecret=true` と暗黙的グラント
- B. `GenerateSecret=false` と認可コードグラント、PKCE
- C. `GenerateSecret=true` とクライアント認証情報グラント
- D. `GenerateSecret=false` とクライアント認証情報グラント

??? success "答えと解説"
    **正解: B**

    公開クライアントにはシークレットを付けず、認可コードと PKCE を使います。

    - A: 誤り。シークレットがブラウザに必要になり、暗黙的グラントはレガシー。
    - B: 正しい。
    - C: 誤り。クライアント認証情報はマシン間の認証向け。
    - D: 誤り。クライアント認証情報にはシークレットが必須。

    **スキル:** C03 2.1.1 / **参照:** [アプリクライアント](../../../services/cognito.md#app-client-settings)

### 問4 {#q4}

アプリクライアントでアクセストークンと ID トークンの有効期間を指定しなかった場合の既定値はどれですか。

- A. 5 分
- B. 1 時間
- C. 1 日
- D. 30 日

??? success "答えと解説"
    **正解: B**

    既定は 1 時間で、5 分〜1 日で設定できます。

    - A: 誤り。5 分は最短の値。
    - B: 正しい。
    - C: 誤り。1 日は最長の値。
    - D: 誤り。30 日はリフレッシュトークンの既定。

    **スキル:** C03 2.1.2 / **参照:** [アプリクライアント](../../../services/cognito.md#app-client-settings)

### 問5 {#q5}

リフレッシュトークンのローテーションを有効にしたところ、既存のアプリの更新処理が失敗するようになりました。アプリは `InitiateAuth` の `REFRESH_TOKEN_AUTH` を使っています。また有効期間は 30 日です。正しいものを選んでください。（2つ選択）

- A. `GetTokensFromRefreshToken` で更新する必要がある
- B. `ALLOW_USER_SRP_AUTH` を無効にする必要がある
- C. 毎日更新しても、最初のサインインから 30 日で再認証が必要である
- D. 更新のたびに、有効期限が 30 日延びる
- E. ローテーションを有効にすると ID トークンは発行されなくなる

??? success "答えと解説"
    **正解: A, C**

    ローテーションは `REFRESH_TOKEN_AUTH` と両立しません。ローテーションしても期間は延びません。

    - A: 正しい。
    - B: 誤り。SRP は更新と関係がない。
    - C: 正しい。
    - D: 誤り。期間は最初のトークンの残りのまま。
    - E: 誤り。ID、アクセス、リフレッシュの 3 つが返る。

    **スキル:** C03 2.1.2 / **参照:** [アプリクライアント](../../../services/cognito.md#app-client-settings)

### 問6 {#q6}

東京リージョンのユーザープールに `auth.example.com` のカスタムドメインを設定します。ACM の証明書の置き場所として正しいものはどれですか。

- A. `ap-northeast-1`
- B. `us-east-1`
- C. 任意のリージョン
- D. 証明書は不要である

??? success "答えと解説"
    **正解: B**

    カスタムドメインは CloudFront を使うので、証明書は `us-east-1` に用意します。親ドメインには有効な DNS の A レコードも必要です。

    - A: 誤り。プールのリージョンは関係がない。
    - B: 正しい。
    - C: 誤り。`us-east-1` だけが選べる。
    - D: 誤り。不要なのはプレフィックスドメインである。

    **スキル:** C03 2.2.2 / **参照:** [ドメイン](../../../services/cognito.md#domain-settings)

### 問7 {#q7}

REST API のメソッドに `orders-api/read` のスコープを要求する設定にしました。クライアントが有効な ID トークンを送ると拒否されます。最も適切な修正はどれですか。

- A. トークンを、スコープを含むアクセストークンに変更する
- B. オーソライザーの種類を `TOKEN` に変更する
- C. `aud` の正規表現を `identityValidationExpression` に設定する
- D. 同じ名前のカスタム属性を追加する

??? success "答えと解説"
    **正解: A**

    スコープを設定すると、API Gateway はトークンをアクセストークンとして扱います。スコープが一致しないと `401 Unauthorized` です。

    - A: 正しい。
    - B: 誤り。`TOKEN` は Lambda オーソライザーの種類。
    - C: 誤り。ID トークンの `aud` を調べる設定で、スコープの問題を解決しない。
    - D: 誤り。スコープは属性ではない。

    **スキル:** C03 2.1.2 / **参照:** [REST API のオーソライザー](../../../services/cognito.md#rest-authorizer-settings)

### 問8 {#q8}

ある利用者が `admin`（Precedence 5、ロール R1）と `staff`（Precedence 5、ロール R2）に属しています。ID プールはトークンからロールを選択し、`AmbiguousRoleResolution` は `Deny` です。`CustomRoleArn` は指定していません。結果はどれですか。

- A. R1 が使われる
- B. R2 が使われる
- C. 認証済みの既定のロールが使われる
- D. 拒否される

??? success "答えと解説"
    **正解: D**

    同じ Precedence で異なるロールだと `cognito:preferred_role` が設定されず、`AmbiguousRoleResolution` に従います。

    - A: 誤り。優先するグループがない。
    - B: 誤り。同上。
    - C: 誤り。`AuthenticatedRole` ならこの動作になる。
    - D: 正しい。

    **スキル:** C03 2.1.1 / **参照:** [ロールマッピング](../../../services/cognito.md#role-mapping)

### 問9 {#q9}

アダプティブ認証を導入します。AWS の推奨に沿う進め方として最も適切なものはどれですか。

- A. Essentials プランのまま全機能モードにする
- B. Plus プランで監査のみモードにして、2 週間以上ログを確認してから全機能モードにする
- C. Plus プランで最初から全リスクレベルをブロックする
- D. Lite プランで Pre authentication トリガーから有効にする

??? success "答えと解説"
    **正解: B**

    脅威保護は Plus プランの機能です。監査のみで傾向を見てから、全機能モードにするのが推奨です。

    - A: 誤り。Essentials には含まれない。
    - B: 正しい。
    - C: 誤り。正常な利用者を止めるおそれがある。
    - D: 誤り。Lite には含まれない。

    **スキル:** C03 2.1.1 / **参照:** [脅威保護](../../../services/cognito.md#threat-protection)

### 問10 {#q10}

Lambda トリガーの説明として正しいものを選んでください。（2つ選択）

- A. Pre sign-up の応答の `autoConfirmUser` は、`AdminCreateUser` では無視される
- B. トリガーの関数の応答期限は 5 秒で、変更できない
- C. 関数の設定でタイムアウトを 60 秒にすれば、Cognito も 60 秒待つ
- D. カスタム送信者トリガーも同期呼び出しである
- E. Pre token generation で `sub` を上書きできる

??? success "答えと解説"
    **正解: A, B**

    カスタム送信者以外は同期呼び出しで、5 秒が固定です。

    - A: 正しい。
    - B: 正しい。
    - C: 誤り。Cognito の待ち時間は変わらない。
    - D: 誤り。カスタム送信者は例外である。
    - E: 誤り。`sub` は変更できない。

    **スキル:** C03 2.1.1 / **参照:** [Lambda トリガーの詳細](../../../services/cognito.md#trigger-details)

### 問11 {#q11}

既存のユーザー DB から、パスワードを再設定させずに Cognito へ順次移行します。User migration トリガーを使うときの設定として最も適切なものはどれですか。

- A. クライアントは `ALLOW_USER_PASSWORD_AUTH` を使い、`finalUserStatus` を `CONFIRMED` にする
- B. クライアントは `ALLOW_USER_SRP_AUTH` だけを使い、`finalUserStatus` を `CONFIRMED` にする
- C. クライアントは `ALLOW_CUSTOM_AUTH` を使い、`finalUserStatus` を `RESET_REQUIRED` にする
- D. クライアントは `ALLOW_USER_PASSWORD_AUTH` を使い、`finalUserStatus` を `RESET_REQUIRED` にする

??? success "答えと解説"
    **正解: A**

    トリガーで既存の DB を確認するには、パスワードが Cognito に届くフローが必要です。`CONFIRMED` なら追加の操作なしでサインインできます。

    - A: 正しい。全員の移行後は SRP に切り替える。
    - B: 誤り。SRP はパスワードを Cognito に渡さない。
    - C: 誤り。カスタム認証では呼ばれない。
    - D: 誤り。`RESET_REQUIRED` はパスワードの変更を求める。

    **スキル:** C03 2.1.1 / **参照:** [Lambda トリガーの詳細](../../../services/cognito.md#trigger-details)

### 問12 {#q12}

Pre token generation でアクセストークンにスコープを追加する関数を作りましたが、反映されません。ID トークンのクレームの変更は反映されています。プランは Essentials です。最も適切な修正はどれですか。

- A. 関数のタイムアウトを延ばす
- B. `claimsToAddOrOverride` に `scope` を入れる
- C. トリガーのイベント版を `V2_0` にする
- D. アプリクライアントのトークンの有効期間を短くする

??? success "答えと解説"
    **正解: C**

    既定の `V1_0` は ID トークンだけを変更します。`scopesToAdd` は `V2_0` と `V3_0` で使えます。M2M のトークンを変えるなら `V3_0` です。

    - A: 誤り。呼ばれているので時間の問題ではない。
    - B: 誤り。スコープは `scopesToAdd` で変える。
    - C: 正しい。
    - D: 誤り。発行の内容は変わらない。

    **スキル:** C03 2.1.1 / **参照:** [Lambda トリガーの詳細](../../../services/cognito.md#trigger-details)

### 問13 {#q13}

ルールでロールを選択する ID プールで、基本フローの `GetOpenIdToken` を呼ぶとエラーになります。最も適切な対応はどれですか。

- A. `GetId` の代わりに `AssumeRole` を呼ぶ
- B. `AmbiguousRoleResolution` を `Deny` にする
- C. 未認証のアクセスを有効にする
- D. `GetCredentialsForIdentity` の拡張フローに変更する

??? success "答えと解説"
    **正解: D**

    ロールマッピングがあるプールは基本フローに対応しません。

    - A: 誤り。ID プールのトークンは `AssumeRoleWithWebIdentity` で使う。
    - B: 誤り。ロールが決まらないときの動作で、フローは変わらない。
    - C: 誤り。ゲストの設定は別の問題。
    - D: 正しい。

    **スキル:** C03 2.1.1 / **参照:** [拡張フローと基本フロー](../../../services/cognito.md#enhanced-basic-flow)

### 問14 {#q14}

自社の認証基盤で認証した利用者に、ID プールの認証情報を発行します。`GetCredentialsForIdentity` が `NotAuthorizedException: Invalid login token. Issuer doesn't match providerName` になりました。原因として最も適切なものはどれですか。

- A. `Logins` のキーがトークンの `iss` と一致していない
- B. 開発者プロバイダー名が空である
- C. `TokenDuration` が 15 分より短い
- D. 認証情報の呼び出しに SigV4 の署名がない

??? success "答えと解説"
    **正解: A**

    `GetOpenIdTokenForDeveloperIdentity` のトークンで呼ぶときは、`Logins` のキーを `iss` に完全に一致させます。

    - A: 正しい。
    - B: 誤り。プロバイダー名は作成時に必要で、エラーの内容と合わない。
    - C: 誤り。`TokenDuration` は短くても一致の問題にはならない。
    - D: 誤り。このエラーの原因ではない。

    **スキル:** C03 2.1.1 / **参照:** [開発者認証](../../../services/cognito.md#developer-authenticated)

### 問15 {#q15}

自作の API で JWT を自分で検証します。次のうち、検証に含めるべきものを選んでください。（2つ選択）

- A. `kid` に対応する公開鍵を、ユーザープールの JWKS から取得して署名を検証する
- B. アクセストークンの `aud` がアプリクライアント ID と一致することを確認する
- C. `token_use` が想定のトークンの種類と一致することを確認する
- D. 公開鍵を自分のカスタムドメインの `/.well-known/jwks.json` から取得する
- E. 署名が正しければ他の確認は省略する

??? success "答えと解説"
    **正解: A, C**

    JWKS は `cognito-idp.<region>.amazonaws.com/<userPoolId>/` にあります。`iss`、`exp`、アクセストークンの `client_id` も確認します。

    - A: 正しい。
    - B: 誤り。アクセストークンで確認するのは `client_id`。`aud` は ID トークン。
    - C: 正しい。
    - D: 誤り。JWKS はカスタムドメインには置かれない。
    - E: 誤り。別のプールやアプリ向けのトークンの可能性がある。

    **スキル:** C03 2.1.2 / **参照:** [JWT の検証](../../../services/cognito.md#jwt-verification)
