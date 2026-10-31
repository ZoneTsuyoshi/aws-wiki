# アクセス制御とデータの保護の問題集

対象の解説: [データプライバシー](../../../services/ai.md#data-privacy)、[データの保護](../../../services/genai-apps.md#data-protection)、[アクセスの要求と管理](../../../services/ai.md#access)

### 問1 {#q1}

あるチームのロールに、承認済みの 2 つのモデルだけを使わせ、呼び出しのたびに指定のガードレールを必須にします。IAM で制御します。アプリは `Converse` を使っています。最も適切なポリシーはどれですか。

- A. `bedrock:Converse` を 2 つのモデルの ARN に許可し、`guardrailConfig` の指定はアプリの規約で定める
- B. `bedrock:InvokeModel` を `*` に許可し、`aws:SourceVpce` の条件でガードレールを必須にする
- C. `bedrock:*` を全リソースに許可し、使えないモデルは Marketplace の `Subscribe` の拒否で止める
- D. `bedrock:InvokeModel` を 2 つのモデルの ARN に許可し、`bedrock:GuardrailIdentifier` の条件で指定がないものを拒否する

??? success "答えと解説"
    **正解: D**

    モデルの ARN に絞り、`bedrock:GuardrailIdentifier` で指定のガードレールなしの推論を拒否します。

    - A: 誤り。`bedrock:Converse` というアクションはなく、規約では必須にならない。
    - B: 誤り。`aws:SourceVpce` は経路の条件で、ガードレールを強制しない。
    - C: 誤り。広すぎて、`Subscribe` の拒否では初回の呼び出しを止められない。
    - D: 正しい。

    **スキル:** [2.3.3](../domain2.md#skill-2-3-3) / **参照:** [IAM のスコープ](../../../services/ai.md#iam-scope)、[適用の強制と限界](../../../services/ai.md#guardrail-enforcement)

### 問2 {#q2}

社内の IdP に登録された従業員が、Web アプリの生成 AI のチャットを使います。ブラウザに AWS の認証情報を渡したくありません。バックエンドの Bedrock の呼び出しの認証も決めます。最も適切な組み合わせはどれですか。

- A. 利用者は Cognito のフェデレーションで認証し、バックエンドは IAM ロールで Bedrock を呼ぶ
- B. 全従業員に IAM ユーザーを作り、アクセスキーをブラウザの設定に保存する
- C. 長期の Bedrock API キーをフロントエンドのコードに埋め込んで全従業員に配布し、従業員の認証の処理を省く
- D. 社内 IdP を使わずにアプリ専用のパスワードを平文で DynamoDB に保存する

??? success "答えと解説"
    **正解: A**

    利用者の認証はフェデレーション、Bedrock の呼び出しは IAM ロールを基本にします。

    - A: 正しい。
    - B: 誤り。長期の認証情報をブラウザに渡している。
    - C: 誤り。キーが漏えいし、利用者の認証もできない。
    - D: 誤り。社内 IdP を使わず、平文の保存も不適切。

    **スキル:** [2.3.3](../domain2.md#skill-2-3-3) / **参照:** [Cognito のフェデレーション](../../../services/cognito.md#federation)、[IAM Identity Center](../../../services/identity-directory.md#identity-center)、[Bedrock API キー](../../../services/ai.md#api-keys)

### 問3 {#q3}

エージェントが利用者の代わりに、社外の SaaS の予定表を読み書きします。利用者ごとの同意が必要です。また、社内文書の検索では、利用者の部署の文書だけを返します。最も適切な組み合わせはどれですか。

- A. SaaS の管理者のトークンを全利用者で共有し、検索はプロンプトで部署を指示する
- B. AgentCore Identity の OAuth（3LO）で委任を受け、検索はメタデータフィルターで絞る
- C. AgentCore Identity のクライアントクレデンシャル（2LO）で全利用者のデータにアクセスし、検索の結果は画面で隠す
- D. 利用者のパスワードを Memory に保存して SaaS にログインし、検索はナレッジベースを部署ごとに分ける

??? success "答えと解説"
    **正解: B**

    利用者の代わりに外部の API を呼ぶには 3LO です。文書の権限は検索の時点で絞ります。

    - A: 誤り。利用者ごとの同意にならず、プロンプトでは確実に絞れない。
    - B: 正しい。
    - C: 誤り。利用者の同意にならない。画面で隠してもデータはモデルに渡る。
    - D: 誤り。パスワードの保存は不適切。

    **スキル:** [2.3.3](../domain2.md#skill-2-3-3) / **参照:** [ツール利用の認可](../../../services/ai.md#tool-authorization)、[文書の権限](../../../services/genai-apps.md#data-protection)

### 問4 {#q4}

本番の Bedrock のロールに `bedrock:*` が付いたままになっている疑いがあります。実際に使っている権限との差を確かめ、最小権限に近づけます。ポリシーを手で読むだけでなく、未使用の権限を見つけたいと考えています。最も適切なサービスはどれですか。

- A. CloudWatch Synthetics
- B. Bedrock Evaluations
- C. IAM Access Analyzer
- D. Macie

??? success "答えと解説"
    **正解: C**

    IAM Access Analyzer は未使用の権限や過剰な権限の発見に使います。

    - A: 誤り。エンドポイントの合成監視で、権限は分析しない。
    - B: 誤り。モデルの評価で、権限は分析しない。
    - C: 正しい。
    - D: 誤り。S3 の機密データの発見のサービスで、IAM の過剰な権限は見ない。

    **スキル:** [2.3.3](../domain2.md#skill-2-3-3) / **参照:** [IAM Access Analyzer](../../../services/iam.md#access-analyzer)、[IAM のスコープ](../../../services/ai.md#iam-scope)

### 問5 {#q5}

インターネットへの経路がないプライベートサブネットの ECS から、Knowledge Bases の `Retrieve` と Bedrock の `Converse` を呼びます。プライベート DNS は有効です。必要なインターフェイスエンドポイントはどれですか。

- A. `bedrock-agent-runtime` と `bedrock-runtime`
- B. `bedrock-runtime` だけ
- C. `bedrock` だけ
- D. `bedrock-agent` と `bedrock`

??? success "答えと解説"
    **正解: A**

    API ごとに別のエンドポイントが必要です。

    - A: 正しい。
    - B: 誤り。`Retrieve` は `bedrock-agent-runtime` の API。
    - C: 誤り。コントロールプレーンのエンドポイントで、`Retrieve` と `Converse` には使えない。
    - D: 誤り。どちらも構築や管理の API のエンドポイントで、実行の API には使えない。

    **スキル:** [3.2.1](../domain3.md#skill-3-2-1) / **参照:** [VPC エンドポイント](../../../services/ai.md#privatelink)、[Knowledge Bases を呼ぶ](../../../services/ai.md#knowledge-bases)

### 問6 {#q6}

VPC エンドポイント経由で Bedrock を呼ぶように変更したところ、`aws:SourceIp` で社内の範囲を許可していた IAM ポリシーのせいで拒否されるようになりました。エンドポイント経由だけを許可する正しい修正はどれですか。

- A. `aws:SourceIp` の範囲にサブネットのプライベートの範囲を追加する
- B. 条件を削除して、エンドポイントポリシーの既定のフルアクセスに任せる
- C. エンドポイントのセキュリティグループで社内の範囲を許可すれば、`aws:SourceIp` が満たされる
- D. 条件を `aws:SourceVpce` に変え、エンドポイントの ID を指定する

??? success "答えと解説"
    **正解: D**

    エンドポイント経由では `aws:SourceIp` が使えないので、`aws:SourceVpce` を使います。

    - A: 誤り。エンドポイント経由のリクエストにこのキーは含まれない。
    - B: 誤り。経路の制限がなくなる。
    - C: 誤り。セキュリティグループはキーの値を変えない。
    - D: 正しい。

    **スキル:** [3.2.1](../domain3.md#skill-3-2-1) / **参照:** [エンドポイントポリシー](../../../services/networking.md#endpoint-policies)、[VPC エンドポイント](../../../services/ai.md#privatelink)

### 問7 {#q7}

FM の学習の外で、Athena からの分析と、要約に渡すデータの取得で、部署ごとに見える列と行を分けます。データは Data Catalog で管理された S3 上にあります。バケットポリシーの組み合わせは複雑になりすぎました。最も適切なものはどれですか。

- A. Macie で列を検出し、見せないように自動で隠す
- B. Lake Formation で列や行の権限を設定する
- C. Guardrails の機密情報フィルターで、見せない列を含む応答を止める
- D. S3 のバケットポリシーを列の名前の条件で書き直す

??? success "答えと解説"
    **正解: B**

    Lake Formation は Data Catalog と S3 上のデータに、データベースのような権限を与えます。

    - A: 誤り。Macie は発見のサービスで、アクセスの制御はしない。
    - B: 正しい。
    - C: 誤り。データの取得の権限ではなく、モデルの入出力の検査。
    - D: 誤り。バケットポリシーではオブジェクトの中の列を制御できない。

    **スキル:** [3.2.1](../domain3.md#skill-3-2-1) / **参照:** [Lake Formation](../../../services/data-engineering.md#lake-formation)、[データの保護](../../../services/genai-apps.md#data-protection)

### 問8 {#q8}

RAG に取り込む S3 の文書に個人情報が混ざっていないかを、取り込みの前に大量に調べます。さらに、モデルの入出力でも個人情報を検査します。文書は英語です。最も適切な組み合わせはどれですか。

- A. どちらも S3 のライフサイクルで行う
- B. どちらも CloudWatch Logs のデータ保護で行う
- C. 文書の発見は Macie、モデルの入出力は Guardrails の機密情報フィルター
- D. 文書の発見は Guardrails の機密情報フィルター、モデルの入出力は Macie で検査する

??? success "答えと解説"
    **正解: C**

    Macie は保存された S3 のデータの PII を見つけます。Guardrails はモデルの入出力を検査します。

    - A: 誤り。保存期間の管理で、検査にならない。
    - B: 誤り。ログの保護で、S3 の文書やモデルの入出力は検査しない。
    - C: 正しい。
    - D: 誤り。役割が逆。Macie はモデルの入出力を検査しない。

    **スキル:** [3.2.2](../domain3.md#skill-3-2-2) / **参照:** [Macie](../../../services/threat-detection.md#macie)、[機密情報フィルター](../../../services/ai.md#guardrail-policy-settings)

### 問9 {#q9}

法務部門から、Bedrock の入出力の扱いについて質問がありました。「モデルの学習に使われないなら、AWS の側に残ることもないのか」というものです。正しい回答はどれですか。

- A. 入出力はモデルの学習に使われるが、オプトアウトすれば保持されない
- B. 入出力はモデルの提供者に共有されるが、提供者が 30 日で削除する
- C. 学習に使われないので、どのモデルでも入出力は一切保持されない
- D. 学習には使われず提供者とも共有されないが、一部のモデルは不正利用検知で最大 30 日保持する

??? success "答えと解説"
    **正解: D**

    保持は `none`、`default`、`aws_review` などのモードで、アカウントのリージョンかプロジェクトの単位に設定します。最大 30 日の保持は一部のモデルに限られます。

    - A: 誤り。Bedrock は学習に使わない。
    - B: 誤り。提供者とは共有されない。
    - C: 誤り。学習に使わないことと保持しないことは別。
    - D: 正しい。

    **スキル:** [3.2.2](../domain3.md#skill-3-2-2) / **参照:** [入出力は学習に使われるか](../../../services/ai.md#training-use)

### 問10 {#q10}

監査で、Bedrock の呼び出しログに顧客のメールアドレスが残っていると指摘されました。Guardrails の `ANONYMIZE` は設定済みです。ログは CloudWatch Logs に送っています。原因と修正の組み合わせとして正しいものはどれですか。

- A. ガードレールのバージョンが古いので、新しいバージョンを作ればログもマスクされる
- B. ログが暗号化されていないので、KMS のカスタマー管理キーで暗号化すればログのアドレスが読めなくなる
- C. ログの `input` は元のリクエストのままなので、ロググループにデータ保護ポリシーを適用する
- D. CloudTrail の設定の誤りなので、データイベントを無効にする

??? success "答えと解説"
    **正解: C**

    Guardrails はログを守りません。データ保護ポリシーを適用します。適用前のログはマスクされません。

    - A: 誤り。どのバージョンでも `input` は元のリクエストのまま。
    - B: 誤り。読める権限を持つ人には見える。マスクにならない。
    - C: 正しい。
    - D: 誤り。呼び出しログと CloudTrail は別のもの。

    **スキル:** [3.2.2](../domain3.md#skill-3-2-2) / **参照:** [モデル呼び出しログ](../../../services/ai.md#invocation-logging)、[CloudWatch Logs のデータ保護](../../../services/ai.md#cloudwatch-data-protection)

### 問11 {#q11}

呼び出しログを CloudWatch Logs と S3 の両方に送っています。CloudWatch Logs のデータ保護ポリシーを適用しましたが、S3 のログにはメールアドレスが残っています。ログの保持は 90 日で十分です。適切な対応を選んでください。（2つ選択）

- A. S3 のログはバケットポリシーと SSE-KMS で保護する
- B. データ保護ポリシーを S3 のバケットにも関連付ける
- C. 適用の前に取り込んだログも、ポリシーの更新で自動的にマスクされるので待つ
- D. ガードレールの `ANONYMIZE` を追加して、S3 のログをマスクする
- E. S3 ライフサイクルで 90 日後に削除する

??? success "答えと解説"
    **正解: A, E**

    データ保護は S3 に送ったログには効きません。別に保護し、期限で削除します。

    - A: 正しい。
    - B: 誤り。このポリシーは CloudWatch Logs だけを守る。
    - C: 誤り。適用前に取り込んだログはマスクされない。
    - D: 誤り。呼び出しログの `input` は元のリクエストのまま。
    - E: 正しい。

    **スキル:** [3.2.2](../domain3.md#skill-3-2-2) / **参照:** [CloudWatch Logs のデータ保護](../../../services/ai.md#cloudwatch-data-protection)、[S3 ライフサイクル](../../../services/s3.md#lifecycle)

### 問12 {#q12}

全社の Bedrock の呼び出しに同じ安全策を適用します。アプリの多くは既存のコードで、`guardrailConfig` を指定していません。アプリの修正は待てません。最も適切なものはどれですか。

- A. Organizations の Bedrock ポリシーで、指定なしでも適用する
- B. 全社の文書に方針を書き、四半期ごとにアンケートで確認する
- C. `bedrock:GuardrailIdentifier` の条件キーで、指定のない呼び出しを全社で拒否する
- D. CloudTrail で指定のない呼び出しを見つけ、各チームに依頼のメールを送る

??? success "答えと解説"
    **正解: A**

    Organizations の Bedrock ポリシーは呼び出し側の指定なしで適用できます。

    - A: 正しい。
    - B: 誤り。文書だけで技術的な強制にならない。
    - C: 誤り。アプリの修正なしでは呼び出しが拒否され、業務が止まる。
    - D: 誤り。適用にならず、修正も待つことになる。

    **スキル:** [3.3.3](../domain3.md#skill-3-3-3) / **参照:** [組織での強制](../../../services/genai-apps.md#guardrail-org-enforcement)、[適用の強制と限界](../../../services/ai.md#guardrail-enforcement)

### 問13 {#q13}

組織のガードレールでは投資助言を `HIGH` で止めています。アプリのガードレールでは同じ項目を `LOW` にしていて、チームは「アプリの設定が優先される」と考えています。実際の動作として正しいものはどれですか。

- A. アプリの設定だけが適用され、組織のガードレールは無視される
- B. 両方が適用され、同じ項目は厳しい方が優先される
- C. 組織の設定だけが適用され、アプリのガードレールは無視される
- D. 設定の衝突で `ValidationException` になる

??? success "答えと解説"
    **正解: B**

    組織とアプリの両方が適用され、同じ項目は厳しい方が優先されます。

    - A: 誤り。組織とアプリの両方が適用される。
    - B: 正しい。
    - C: 誤り。両方が適用される。
    - D: 誤り。衝突でエラーにはならない。

    **スキル:** [3.3.3](../domain3.md#skill-3-3-3) / **参照:** [組織での強制](../../../services/genai-apps.md#guardrail-org-enforcement)、[適用の強制と限界](../../../services/ai.md#guardrail-enforcement)

### 問14 {#q14}

全社で、特定の第三者モデルの利用を止め、推論を EU の中に限定します。Marketplace の `Subscribe` を SCP で拒否しましたが、そのモデルが使えてしまいました。最も適切な修正はどれですか。

- A. IAM ユーザーのパスワードの期限を短くして、利用の機会を減らす
- B. `Subscribe` の拒否を維持し、モデルの契約を削除すれば、次の呼び出しから止まる
- C. `global` の推論プロファイルに統一して、EU の中に限定する
- D. SCP で対象モデルの ARN に `bedrock:InvokeModel` 系を拒否し、EU の宛先リージョンだけを許可する

??? success "答えと解説"
    **正解: D**

    `Subscribe` の拒否では初回の呼び出しを止められません。`InvokeModel` 系を拒否します。`Converse` も一緒に止まります。

    - A: 誤り。モデルの利用の制御にならない。
    - B: 誤り。契約を削除しても次の呼び出しで再び作られる。
    - C: 誤り。`global` は EU の外でも処理される。
    - D: 正しい。

    **スキル:** [3.3.3](../domain3.md#skill-3-3-3) / **参照:** [使わせない方法](../../../services/ai.md#block-access)、[クロスリージョン推論](../../../services/ai.md#model-identifiers)

### 問15 {#q15}

全社の生成 AI のガバナンス方針を作りました。しかし、「誰が最終責任を持つのか」「どの用途がどの統制を必要とするのか」が曖昧で、リスクの判断が止まっています。最も適切な対応はどれですか。

- A. 全用途で最も厳しい統制を一律に適用し、例外を認めない
- B. 承認者とリスクの所有者を定義し、Scoping Matrix で用途ごとの範囲を整理する
- C. 全員をリスクの所有者にして、責任を分散させる
- D. 判断を止めるリスクを避けるため、方針をいったん撤回して、各チームの判断と責任にすべて任せる

??? success "答えと解説"
    **正解: B**

    役割と責任を定義し、用途の範囲に応じて統制を決めます。

    - A: 誤り。用途の違いを無視し、低リスクの用途も止まる。
    - B: 正しい。
    - C: 誤り。誰も責任を取らない状態になる。
    - D: 誤り。ガバナンスがなくなる。

    **スキル:** [3.3.3](../domain3.md#skill-3-3-3) / **参照:** [役割と責任](../../../services/ai-fundamentals.md#governance-roles)、[Generative AI Security Scoping Matrix](../../../services/ai-fundamentals.md#scoping-matrix)
