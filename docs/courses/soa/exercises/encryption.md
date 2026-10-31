# 暗号化とシークレットの問題集

対象の解説: [KMS キーの種類](../../../services/kms.md#key-types)、[サービスでの KMS の利用](../../../services/kms.md#service-integration)、[AWS Certificate Manager](../../../services/certificates.md#acm)、[3 つのサービスの比較](../../../services/secrets.md#comparison)

### 問1 {#q1}

RDS のスナップショットを別のアカウントと共有する予定です。どのキーで暗号化しますか。

- A. AWS 管理キー `aws/rds`
- B. カスタマー管理キー
- C. AWS 所有キー
- D. SSE-S3 のキー

??? success "答えと解説"
    **正解: B**

    ポリシーを変更できるのはカスタマー管理キーです。

    - A: 誤り。AWS 管理キーのポリシーは変更できず、共有できない。
    - B: 正しい。
    - C: 誤り。自分で管理できず、共有にも使えない。
    - D: 誤り。S3 の暗号化の方式で、RDS では選べない。

    **スキル:** [4.2.2](../domain4.md#skill-4-2-2) / **参照:** [KMS キーの種類](../../../services/kms.md#key-types)、[キーポリシー、IAM、グラント](../../../services/kms.md#access-control)

### 問2 {#q2}

既存の暗号化されていない EBS ボリュームを暗号化します。正しい手順はどれですか。

- A. インスタンスを再起動すると、デフォルトでの暗号化が既存にも適用される
- B. ボリュームの属性を `ModifyVolume` で暗号化ありに変更する
- C. ボリュームを `gp3` へ変更する
- D. スナップショットを暗号化してコピーし、そこから作り直す

??? success "答えと解説"
    **正解: D**

    既存はスナップショットをコピーして暗号化します。今後の分はリージョンの「デフォルトでの暗号化」で対応します。

    - A: 誤り。新しいボリュームだけに効く。
    - B: 誤り。既存のボリュームの属性は変えられない。
    - C: 誤り。ボリュームタイプの変更で、暗号化はされない。
    - D: 正しい。

    **スキル:** [4.2.2](../domain4.md#skill-4-2-2) / **参照:** [EBS の暗号化](../../../services/storage.md#ebs-encryption)

### 問3 {#q3}

カスタマー管理キーを削除予定にしたところ、関連の EBS を使うインスタンスが起動しなくなりました。待機期間中です。どうしますか。

- A. `cancel-key-deletion` で取り消し、キーを有効にする
- B. `ScheduleKeyDeletion` の待機期間を 30 日へ延ばす
- C. EBS をスナップショットからコピーして別のキーで暗号化する
- D. キーの別名を新しいキーへ付け替える

??? success "答えと解説"
    **正解: A**

    待機期間（7〜30 日）の間なら取り消せます。

    - A: 正しい。
    - B: 誤り。期間を延ばしても使えるようにならない。
    - C: 誤り。元のキーが使えないと、コピーもできない。
    - D: 誤り。暗号文は元のキーでしか復号できない。

    **スキル:** [4.2.2](../domain4.md#skill-4-2-2) / **参照:** [主なエラー](../../../services/kms.md#kms-errors)、[キーの無効化と削除](../../../services/kms.md#disable-delete)

### 問4 {#q4}

次の KMS のエラーと対処の組み合わせとして正しいものを選んでください。（2つ選択）

- A. `ThrottlingException`: キーポリシーに主体を追加する
- B. `DisabledException`: キーを有効にする
- C. `AccessDeniedException`: キーをローテーションする
- D. `KMSInvalidStateException`: IAM ポリシーに `kms:Decrypt` を追加する
- E. `ThrottlingException`: S3 Bucket Key やキャッシュを使う

??? success "答えと解説"
    **正解: B, E**

    エラーからキーの状態、権限、上限のどれが原因かを見分けます。

    - A: 誤り。リクエストの上限の問題である。
    - B: 正しい。
    - C: 誤り。許可の問題で、ローテーションでは直らない。
    - D: 誤り。キーの状態の問題である。
    - E: 正しい。

    **スキル:** [4.2.2](../domain4.md#skill-4-2-2) / **参照:** [主なエラー](../../../services/kms.md#kms-errors)

### 問5 {#q5}

既存の暗号化されていない EFS を、規制の要件で保存時に暗号化する必要があります。正しい方法はどれですか。

- A. `tls` でマウントする
- B. バケットのデフォルト暗号化を SSE-KMS に変更する
- C. 暗号化した新しいファイルシステムへ移す
- D. ファイルシステムの設定を編集して、保存時の暗号化を有効にする

??? success "答えと解説"
    **正解: C**

    EFS の保存時の暗号化は作成時のみです。

    - A: 誤り。転送時の暗号化の設定である。
    - B: 誤り。S3 の設定である。
    - C: 正しい。
    - D: 誤り。作成時にしか指定できない。

    **スキル:** [4.2.2](../domain4.md#skill-4-2-2) / **参照:** [暗号化とアクセス制御](../../../services/storage.md#efs-encryption)、[サービスでの KMS の利用](../../../services/kms.md#service-integration)

### 問6 {#q6}

SSE-KMS のバケットへのアクセスが多く、KMS の `ThrottlingException` と費用が増えています。暗号化は KMS のままにします。どの設定を使いますか。

- A. S3 Bucket Key を有効にする
- B. SSE-C へ切り替える
- C. S3 Object Lock を有効にする
- D. Multi-Region Access Point を使う

??? success "答えと解説"
    **正解: A**

    Bucket Key で KMS の呼び出しを減らせます。

    - A: 正しい。
    - B: 誤り。KMS を使わなくなり、要件に合わない。鍵の管理の負担も増える。
    - C: 誤り。KMS の呼び出しは減らない。
    - D: 誤り。KMS の呼び出しは減らない。

    **スキル:** [4.2.2](../domain4.md#skill-4-2-2) / **参照:** [暗号化](../../../services/s3.md#encryption)、[主なエラー](../../../services/kms.md#kms-errors)

### 問7 {#q7}

東京で作った ACM の証明書が CloudFront の画面に出てきません。ALB にも同じドメインの証明書が要ります。どうしますか。

- A. 東京の証明書を CloudFront へコピーする API を実行して関連付ける
- B. CloudFront 用は `us-east-1` で、ALB 用は東京で発行する
- C. CloudFront の代わりに ALB を削除し、東京の証明書をエッジへ移す
- D. 証明書の秘密鍵をエクスポートして、CloudFront にインポートする

??? success "答えと解説"
    **正解: B**

    CloudFront の証明書は `us-east-1` に作ります。証明書はリージョンごとです。

    - A: 誤り。ACM の証明書はコピーできない。
    - B: 正しい。
    - C: 誤り。別の問題を生むだけである。
    - D: 誤り。必要な手順ではない。

    **スキル:** [4.2.3](../domain4.md#skill-4-2-3) / **参照:** [リージョンのルール](../../../services/certificates.md#region-rules)、[HTTPS](../../../services/networking.md#cloudfront-https)

### 問8 {#q8}

HTTP の通信を止めるため、バケットポリシーの `Allow` の文に `aws:SecureTransport` が `true` の条件を付けました。ところが、同じアカウントで IAM ポリシーの許可を持つ利用者は HTTP でも読めます。どう直しますか。

- A. `Allow` の文のまま、`aws:SecureTransport` の値を `false` に変える
- B. ブロックパブリックアクセスを有効にする
- C. デフォルト暗号化を SSE-KMS に変える
- D. `aws:SecureTransport` が `false` の要求を `Deny` する文を加える

??? success "答えと解説"
    **正解: D**

    同じアカウントでは IAM の許可だけで読めるので、`Allow` に条件を付けても止まりません。明示的な拒否を使います。

    - A: 誤り。HTTP の要求を許可する文になってしまう。
    - B: 誤り。公開の制限で、HTTP の拒否ではない。
    - C: 誤り。保存時の暗号化の設定である。
    - D: 正しい。

    **スキル:** [4.2.3](../domain4.md#skill-4-2-3) / **参照:** [暗号化](../../../services/s3.md#encryption)、[主なグローバル条件キー](../../../services/iam.md#condition-keys)

### 問9 {#q9}

ACM のインポートした証明書の期限が切れて障害になりました。再発を防ぐためにどの対策を取りますか。（2つ選択）

- A. DNS の CNAME を消して検証をやり直す
- B. 証明書を S3 に保存しておくと自動で更新される
- C. `DaysToExpiry` のアラームで監視する
- D. 可能なら ACM が発行した証明書に置き換える
- E. ACM の自動更新を、インポートした証明書でも有効にする

??? success "答えと解説"
    **正解: C, D**

    ACM はインポートした証明書を更新しません。

    - A: 誤り。インポートした証明書は ACM の検証と更新の対象ではないので、CNAME は関係がない。
    - B: 誤り。更新は行われない。
    - C: 正しい。
    - D: 正しい。
    - E: 誤り。インポートした証明書は ACM が更新しない。

    **スキル:** [4.2.3](../domain4.md#skill-4-2-3) / **参照:** [自動更新](../../../services/certificates.md#auto-renewal)、[更新の監視](../../../services/certificates.md#renewal-monitoring)

### 問10 {#q10}

DNS 検証の ACM の証明書が自動で更新されません。統合サービスで使用中です。最初に確認することはどれですか。

- A. 証明書の暗号化に使う KMS キーのローテーションの期間
- B. ALB のヘルスチェックのパス
- C. DNS の CNAME が残っているか
- D. 証明書の `DaysToExpiry` のアラームの統計

??? success "答えと解説"
    **正解: C**

    CNAME が消えると、検証ができないので更新されません。

    - A: 誤り。ACM の更新の条件ではない。
    - B: 誤り。証明書の更新に関係がない。
    - C: 正しい。
    - D: 誤り。監視の設定で、更新の条件ではない。

    **スキル:** [4.2.3](../domain4.md#skill-4-2-3) / **参照:** [自動更新](../../../services/certificates.md#auto-renewal)、[ドメイン検証](../../../services/certificates.md#domain-validation)

### 問11 {#q11}

ALB で TLS 1.0 と 1.1 の接続を止めるよう求められました。どこを変更しますか。

- A. ACM の証明書の鍵の長さ
- B. ターゲットグループのヘルスチェックのプロトコル
- C. セキュリティグループのルール
- D. リスナーのセキュリティポリシー

??? success "答えと解説"
    **正解: D**

    古い TLS を止めるには、リスナーのセキュリティポリシーを変えます。

    - A: 誤り。TLS のバージョンは証明書では決まらない。
    - B: 誤り。ターゲットへの確認の設定である。
    - C: 誤り。ポートの制御で、TLS のバージョンは見ない。
    - D: 正しい。

    **スキル:** [4.2.3](../domain4.md#skill-4-2-3) / **参照:** [リスナーとルール](../../../services/networking.md#alb-listeners)、[転送時の TLS](../../../services/certificates.md#tls-in-transit)

### 問12 {#q12}

転送時の暗号化を有効にする方法として正しいものを選んでください。（2つ選択）

- A. CloudFront の地理的制限を有効にする
- B. EBS のデフォルト暗号化を有効にすれば、EFS の通信も暗号化される
- C. RDS のパラメータグループとクライアントの設定で TLS を強制する
- D. S3 Bucket Key を有効にすれば、S3 への通信が HTTPS になる
- E. EFS のマウントオプションに `tls` を指定する

??? success "答えと解説"
    **正解: C, E**

    サービスごとに転送時の暗号化の手段が違います。

    - A: 誤り。国の制限で、暗号化とは関係がない。
    - B: 誤り。保存時の EBS の暗号化の設定である。
    - C: 正しい。
    - D: 誤り。KMS の呼び出しを減らす機能である。
    - E: 正しい。

    **スキル:** [4.2.3](../domain4.md#skill-4-2-3) / **参照:** [SSL/TLS](../../../services/databases.md#rds-ssl)、[暗号化とアクセス制御](../../../services/storage.md#efs-encryption)

### 問13 {#q13}

RDS のパスワードを 30 日ごとに自動で変更し、アプリには常に最新の値を使わせたいです。現在は Parameter Store の `SecureString` です。どう変えますか。

- A. Secrets Manager に移し、ローテーションを有効にする
- B. KMS キーの自動ローテーションを 30 日に設定して、パスワードも変える
- C. `SecureString` のままで Parameter Store の自動ローテーションを有効に設定する
- D. パスワードを S3 に保存し、ライフサイクルで 30 日ごとに削除する

??? success "答えと解説"
    **正解: A**

    Parameter Store には自動ローテーションがありません。

    - A: 正しい。
    - B: 誤り。KMS のローテーションは鍵素材の更新で、パスワードは変わらない。
    - C: 誤り。Parameter Store に自動ローテーションはない。
    - D: 誤り。パスワードは変わらず、DB の側とも同期しない。

    **スキル:** [4.2.4](../domain4.md#skill-4-2-4) / **参照:** [3 つのサービスの比較](../../../services/secrets.md#comparison)、[ローテーション](../../../services/secrets.md#rotation)

### 問14 {#q14}

ローテーションの方式の説明として正しいものはどれですか。

- A. Lambda 関数によるローテーションには VPC の接続を設定できない
- B. RDS が管理するシークレットでは Lambda が不要である
- C. どのシークレットでも、Lambda 関数の作成が必ず必要である
- D. マネージドローテーションは Parameter Store の機能である

??? success "答えと解説"
    **正解: B**

    他のサービスが管理するシークレットはマネージドローテーションです。

    - A: 誤り。DB に接続するなら VPC に接続する。
    - B: 正しい。
    - C: 誤り。マネージドローテーションなら不要である。
    - D: 誤り。Secrets Manager の機能である。

    **スキル:** [4.2.4](../domain4.md#skill-4-2-4) / **参照:** [ローテーション](../../../services/secrets.md#rotation)、[Secrets Manager との統合](../../../services/databases.md#rds-secrets-manager)

### 問15 {#q15}

Lambda によるローテーションが失敗します。プライベートサブネットの RDS を更新する関数です。確認すべきものを選んでください。（2つ選択）

- A. Lambda から Secrets Manager への経路（VPC エンドポイントや NAT）
- B. シークレットの復旧期間の日数
- C. Lambda から DB への経路とセキュリティグループ
- D. KMS キーの自動ローテーションの期間
- E. シークレットのレプリカのリージョン

??? success "答えと解説"
    **正解: A, C**

    関数は DB と Secrets Manager の両方に届く必要があります。

    - A: 正しい。
    - B: 誤り。削除の設定で、ローテーションの経路と関係がない。
    - C: 正しい。
    - D: 誤り。鍵素材の更新の周期で、シークレットのローテーションの失敗の原因にならない。
    - E: 誤り。複製先は、この経路の問題と関係がない。

    **スキル:** [4.2.4](../domain4.md#skill-4-2-4) / **参照:** [ローテーション](../../../services/secrets.md#rotation)

### 問16 {#q16}

別のアカウントからシークレットを読みます。拒否されます。必要な設定を選んでください。（2つ選択）

- A. シークレットを相手のリージョンへ複製する
- B. シークレットのリソースポリシーで相手を許可する
- C. AWS 管理キー `aws/secretsmanager` のポリシーを編集する
- D. 相手のロールの信頼ポリシーにシークレットの ARN を書く
- E. カスタマー管理キーのキーポリシーで相手に復号を許可する

??? success "答えと解説"
    **正解: B, E**

    AWS 管理キーのシークレットは共有できません。

    - A: 誤り。リージョンの複製で、別のアカウントへの許可にはならない。
    - B: 正しい。
    - C: 誤り。AWS 管理キーのポリシーは変更できない。
    - D: 誤り。信頼ポリシーはロールを引き受ける相手の設定である。
    - E: 正しい。

    **スキル:** [4.2.4](../domain4.md#skill-4-2-4) / **参照:** [クロスアカウントでの利用](../../../services/secrets.md#secrets-cross-account)

### 問17 {#q17}

CloudFormation のテンプレートとスタックの情報に、DB のパスワードの平文を残したくありません。パスワードは Secrets Manager にあります。どれを使いますか。

- A. `NoEcho` のパラメータの `Default` に値を書く
- B. `Metadata` に値を書き、`NoEcho` を付けたパラメータから参照する
- C. `{{resolve:secretsmanager:...}}` の動的参照を使う
- D. パスワードを `Outputs` に出して、他のスタックから参照する

??? success "答えと解説"
    **正解: C**

    動的参照でシークレットの値を参照します。

    - A: 誤り。`NoEcho` は `Default` の値を隠さず、平文がテンプレートに残る。
    - B: 誤り。`NoEcho` は `Metadata` を隠さない。
    - C: 正しい。
    - D: 誤り。平文が出力される。

    **スキル:** [4.2.4](../domain4.md#skill-4-2-4) / **参照:** [CloudFormation の動的参照](../../../services/secrets.md#dynamic-references)

### 問18 {#q18}

本番のシークレットを既定の設定で誤って削除しました。10 分後に気づきました。アプリケーションは値を読めなくなっています。どう戻しますか。

- A. `put-secret-value` で同じ値を入れ直す
- B. 同じ名前で新しいシークレットを作成し、値を入れ直す
- C. AWS Backup のボールトから復元する
- D. `restore-secret` で削除の予定を取り消す

??? success "答えと解説"
    **正解: D**

    削除の後の復旧期間は 7〜30 日で、既定は 30 日です。この間は削除の予定になっているだけで、`restore-secret` で戻せます。

    - A: 誤り。削除の予定のシークレットには直接アクセスできず、値を入れ直せない。
    - B: 誤り。元のシークレットが残っているので、同じ名前は使えない。
    - C: 誤り。削除の予定の取り消しは Secrets Manager の操作で行う。
    - D: 正しい。

    **スキル:** [4.2.4](../domain4.md#skill-4-2-4) / **参照:** [削除と復旧](../../../services/secrets.md#recovery-window)、[他リージョンへの複製](../../../services/secrets.md#secret-replication)
