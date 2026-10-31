# IAM とアクセスの調査の問題集

対象の解説: [ポリシー評価](../../../services/iam.md#policy-evaluation)、[アイデンティティベースとリソースベース](../../../services/iam.md#identity-vs-resource)、[IAM Access Analyzer](../../../services/identity-directory.md#access-analyzer)、[ポリシーシミュレーター](../../../services/iam.md#policy-simulator)

### 問1 {#q1}

`aws:MultiFactorAuthPresent` が `false` の要求を `BoolIfExists` で拒否するポリシーを IAM ユーザーに付けました。すると、MFA デバイスを登録済みの開発者の CLI の操作が、アクセスキーを使うとすべて拒否されます。CLI を使い続けるにはどうしますか。

- A. アクセスキーをローテーションし、新しいキーで実行する
- B. 拒否の条件キーを `aws:SecureTransport` に変更する
- C. `AdministratorAccess` を追加し、明示的な拒否を許可で上書きさせる
- D. `sts get-session-token` に MFA のコードを渡し、一時認証情報を使う

??? success "答えと解説"
    **正解: D**

    長期のアクセスキーの要求には MFA の情報が入らないので、この条件で拒否されます。`GetSessionToken` に MFA のコードを渡して、一時的な認証情報を使います。

    - A: 誤り。新しいキーも長期の認証情報で、MFA の情報は入らない。
    - B: 誤り。HTTPS かどうかの条件で、MFA の要求ではなくなる。
    - C: 誤り。明示的な拒否は許可では覆せない。
    - D: 正しい。

    **スキル:** [4.1.1](../domain4.md#skill-4-1-1) / **参照:** [GetSessionToken と MFA](../../../services/iam.md#mfa)、[条件とアクセス制御](../../../services/iam.md#conditions)

### 問2 {#q2}

アカウント A の IAM ロールが、アカウント B の S3 バケットを読みます。A のロールに `s3:GetObject` を許可しましたが拒否されます。どう直しますか。

- A. S3 のブロックパブリックアクセスを無効にする
- B. A のロールに `AdministratorAccess` を追加する
- C. B のバケットポリシーで A のロールを許可する
- D. A のロールの信頼ポリシーに B のアカウントを追加する

??? success "答えと解説"
    **正解: C**

    別のアカウントなら、アイデンティティベースとリソースベースの両方の許可が必要です。

    - A: 誤り。公開の設定で、別アカウントの許可とは別の話である。
    - B: 誤り。相手の側の許可がない問題は解決しない。
    - C: 正しい。
    - D: 誤り。A のロールを B から引き受ける設定で、この問題の解決ではない。

    **スキル:** [4.1.1](../domain4.md#skill-4-1-1) / **参照:** [クロスアカウントアクセス](../../../services/iam.md#cross-account)、[アイデンティティベースとリソースベース](../../../services/iam.md#identity-vs-resource)

### 問3 {#q3}

同じアカウントの IAM ユーザーに `s3:*` の許可が直接付いています。ユーザーが属するグループのポリシーは `s3:DeleteObject` を拒否しています。バケットポリシーは、このユーザーに `s3:DeleteObject` を許可しています。`DeleteObject` の結果はどれですか。

- A. 許可される。同じアカウントではバケットポリシーの許可で足りる
- B. 拒否される。どのポリシーの明示的な拒否も許可より優先される
- C. 許可される。直接付けたポリシーがグループのポリシーより優先される
- D. 許可される。リソースベースのポリシーがグループのポリシーより優先される

??? success "答えと解説"
    **正解: B**

    すべてのポリシーを集めて評価し、どこかに明示的な拒否があれば拒否です。

    - A: 誤り。同じアカウントなら片方の許可で足りるが、それは明示的な拒否がないときの話である。
    - B: 正しい。
    - C: 誤り。付け方による優先順位はない。
    - D: 誤り。ポリシーの種類による優先順位はなく、拒否が優先される。

    **スキル:** [4.1.1](../domain4.md#skill-4-1-1) / **参照:** [ポリシー評価](../../../services/iam.md#policy-evaluation)

### 問4 {#q4}

EC2 のアプリケーションが S3 で `AccessDenied` になります。インスタンスプロファイルのロールには必要な許可があります。インスタンスで `aws sts get-caller-identity` を実行すると、ロールではなく古い IAM ユーザーが表示されます。どう直しますか。

- A. 環境変数や `~/.aws/credentials` に残った古いアクセスキーを削除する
- B. インスタンスプロファイルを一度外し、同じロールを付け直す
- C. ロールの信頼ポリシーで `s3.amazonaws.com` を許可する
- D. IMDSv1 を有効にして、ロールの認証情報をメタデータから取得させる

??? success "答えと解説"
    **正解: A**

    CLI と SDK は、環境変数や認証情報ファイルをインスタンスプロファイルより先に使います。残ったキーを消すとロールが使われます。

    - A: 正しい。
    - B: 誤り。ロールは付いていて、使われていないのが問題である。
    - C: 誤り。信頼ポリシーの相手は EC2 で、S3 ではない。
    - D: 誤り。IMDS の問題ではなく、先に見つかるキーが使われているのが原因である。

    **スキル:** [4.1.1](../domain4.md#skill-4-1-1) / **参照:** [プリンシパルと権限の定義](../../../services/iam.md#principals)、[ロールの引き受け](../../../services/iam.md#assume-role)

### 問5 {#q5}

IAM のパスワードポリシーの説明として正しいものを選んでください。（2つ選択）

- A. 失敗の回数によるロックアウトを設定できる
- B. 有効期限はすぐに効き、期限が切れてもアクセスキーは使える
- C. 再利用の禁止は過去 100 個まで指定できる
- D. 長さや文字の要件は、次にパスワードを変えるときに効く
- E. ルートユーザーのパスワードにも適用される

??? success "答えと解説"
    **正解: B, D**

    [パスワードポリシーの公式ドキュメント](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_passwords_account-policy.html)の項目です。

    - A: 誤り。ロックアウトは設定できない。
    - B: 正しい。
    - C: 誤り。過去 1〜24 個である。
    - D: 正しい。
    - E: 誤り。ルートユーザーは対象外である。

    **スキル:** [4.1.1](../domain4.md#skill-4-1-1) / **参照:** [GetSessionToken と MFA](../../../services/iam.md#mfa)

### 問6 {#q6}

社内の ID プロバイダーのアカウントで、1 つの AWS アカウントのコンソールへサインインさせたいです。IAM ユーザーは増やしたくありません。どれが適切ですか。

- A. Cognito ユーザープールに社員を登録し、そのままコンソールを使わせる
- B. IAM の ID プロバイダーを作り、SAML か OIDC でロールを使う
- C. 社員ごとに IAM ユーザーを作り、パスワードを社内の ID とそろえる
- D. 部署ごとに IAM グループを作り、ID プロバイダーから直接ログインさせる

??? success "答えと解説"
    **正解: B**

    社内の ID で AWS を使うのがフェデレーションです。

    - A: 誤り。ユーザープールはアプリの利用者の認証で、コンソールのサインインの仕組みではない。
    - B: 正しい。
    - C: 誤り。要件に反する。
    - D: 誤り。IAM グループはサインインの主体にならない。

    **スキル:** [4.1.1](../domain4.md#skill-4-1-1) / **参照:** [フェデレーション](../../../services/iam.md#federation)、[IAM Identity Center](../../../services/identity-directory.md#identity-center)

### 問7 {#q7}

管理者権限のロールでも EC2 の操作が拒否されます。拒否メッセージに `service control policy` とあります。どう対応しますか。

- A. アクセスキーをローテーションして再度実行する
- B. ロールの権限の境界を外す
- C. IAM ポリシーに許可を追加する
- D. 組織の管理者と SCP を確認する

??? success "答えと解説"
    **正解: D**

    拒否メッセージでポリシーの種類が分かります。SCP が原因なら IAM を足しても直りません。

    - A: 誤り。認証の話で、SCP の拒否とは関係がない。
    - B: 誤り。権限の境界を外しても、SCP の拒否は残る。
    - C: 誤り。SCP の拒否は IAM の許可では覆せない。
    - D: 正しい。

    **スキル:** [4.1.2](../domain4.md#skill-4-1-2) / **参照:** [アクセス拒否メッセージ](../../../services/iam.md#access-denied-messages)、[SCP](../../../services/governance.md#scp)

### 問8 {#q8}

EC2 の API が `Encoded authorization failure message` を返しました。拒否の理由を読みたいです。何を使いますか。

- A. `sts decode-authorization-message`
- B. `aws logs tail`
- C. `aws kms decrypt`
- D. `aws iam get-account-authorization-details`

??? success "答えと解説"
    **正解: A**

    エンコードされた拒否メッセージは STS の `DecodeAuthorizationMessage` で読みます。権限が必要です。

    - A: 正しい。
    - B: 誤り。CloudWatch Logs を表示するコマンドである。
    - C: 誤り。KMS の暗号文を復号するコマンドで、このメッセージには使えない。
    - D: 誤り。アカウントの IAM の集計を返すコマンドである。

    **スキル:** [4.1.2](../domain4.md#skill-4-1-2) / **参照:** [DecodeAuthorizationMessage](../../../services/iam.md#decode-authorization)

### 問9 {#q9}

要件と調査のツールの組み合わせとして正しいものを選んでください。（2つ選択）

- A. RCP の影響をシミュレーションする: IAM ポリシーシミュレーター
- B. 修正したポリシーで特定の操作が許可されるか試す: IAM ポリシーシミュレーター
- C. 設定がどのように変わったかを時系列で見る: IAM Access Analyzer
- D. 実際に誰がいつ操作したかを確認する: IAM ポリシーシミュレーター
- E. 外部に共有されたリソースを見つける: IAM Access Analyzer

??? success "答えと解説"
    **正解: B, E**

    ツールごとに答えられることが違います。

    - A: 誤り。RCP は未対応である。
    - B: 正しい。
    - C: 誤り。Config で確認する。
    - D: 誤り。CloudTrail で確認する。
    - E: 正しい。

    **スキル:** [4.1.2](../domain4.md#skill-4-1-2) / **参照:** [ポリシーシミュレーター](../../../services/iam.md#policy-simulator)、[IAM Access Analyzer](../../../services/identity-directory.md#access-analyzer)

### 問10 {#q10}

90 日以上使っていないロールと権限を見つけて整理したいです。どの機能が適切ですか。

- A. Trusted Advisor の S3 バケットの権限のチェック
- B. IAM ポリシーシミュレーターの一括実行
- C. IAM Access Analyzer の未使用アクセスの検出
- D. CloudWatch のメトリクスフィルター

??? success "答えと解説"
    **正解: C**

    Access Analyzer で未使用のアクセスを見つけられます。

    - A: 誤り。S3 の権限のチェックで、未使用のロールは探さない。
    - B: 誤り。許可の判定で、利用の履歴は分からない。
    - C: 正しい。
    - D: 誤り。ログの文字列を数える機能である。

    **スキル:** [4.1.2](../domain4.md#skill-4-1-2) / **参照:** [未使用アクセスの検出](../../../services/identity-directory.md#aa-unused)

### 問11 {#q11}

先週の `AccessDenied` のイベントを主体と操作で調べたいです。CloudTrail の説明で正しいものはどれですか。

- A. IAM ポリシーの全文がイベントに入るので、原因のポリシーをそのまま読める
- B. CloudTrail を見るには、Config のレコーダーを先に有効にして、設定の履歴を取り込む必要がある
- C. イベントは常に 1 秒以内に配信されるので、発生の直後から必ず検索できる
- D. `errorCode` で `AccessDenied` を探せ、イベント履歴で 90 日分を確認できる

??? success "答えと解説"
    **正解: D**

    `errorCode` が `AccessDenied` のイベントで、拒否された操作と主体が分かります。

    - A: 誤り。ポリシーの全文は記録されない。
    - B: 誤り。Config は CloudTrail の前提ではない。
    - C: 誤り。配信は平均で約 5 分遅れる。
    - D: 正しい。

    **スキル:** [4.1.2](../domain4.md#skill-4-1-2) / **参照:** [証跡とイベント履歴](../../../services/observability.md#cloudtrail-trails)、[CloudTrail の調査](../../../services/threat-detection.md#investigate-cloudtrail)

### 問12 {#q12}

セキュリティグループのルールがいつ、どう変わったかの時系列を見たいです。また、変更した人も特定します。組み合わせはどれですか。

- A. 時系列は CloudTrail、変更した人は Trusted Advisor
- B. 時系列は Config、変更した人は CloudTrail
- C. 時系列は GuardDuty、変更した人は Inspector
- D. 時系列は Compute Optimizer、変更した人は Macie

??? success "答えと解説"
    **正解: B**

    誰が操作したかは CloudTrail、設定がどう変わったかは Config です。

    - A: 誤り。Trusted Advisor は変更の履歴を持たない。
    - B: 正しい。
    - C: 誤り。脅威と脆弱性の検出で、設定の履歴ではない。
    - D: 誤り。推奨と機密データの検出で、関係がない。

    **スキル:** [4.1.2](../domain4.md#skill-4-1-2) / **参照:** [Config と CloudTrail の違い](../../../services/governance.md#config-vs-cloudtrail)
