# アクセスの分析の問題集

対象の解説: [アクセス拒否の切り分け](../../../services/identity-directory.md#access-troubleshooting)、[IAM Access Analyzer](../../../services/identity-directory.md#access-analyzer)、[データ境界](../../../services/identity-directory.md#data-perimeter)

### 問1 {#q1}

開発者が `codecommit:ListRepositories` を呼ぶと、エラーに `because no permissions boundary allows` と表示されました。アイデンティティポリシーでは `codecommit:*` を許可しています。また、この開発者のアカウントには SCP として `FullAWSAccess` だけが付いています。修正すべき場所はどれですか。

- A. 開発者のアイデンティティポリシーに `ListRepositories` を明示的に追加する
- B. 開発者の権限境界のポリシーで `codecommit:ListRepositories` を許可する
- C. 組織の SCP に `codecommit:ListRepositories` を追加し、OU へ適用する
- D. CodeCommit のリポジトリのリソースポリシーで開発者を許可する

??? success "答えと解説"
    **正解: B**

    `because no permissions boundary allows` は権限境界の暗黙の拒否です。境界に許可がなければ、アイデンティティポリシーで許可しても使えません。

    - A: 誤り。すでに許可されています。
    - B: 正しい。
    - C: 誤り。SCP はメッセージの原因ではありません。
    - D: 誤り。メッセージの原因は権限境界です。

    **スキル:** [4.2.4](../domain4.md#skill-4-2-4) / **参照:** [アクセス拒否メッセージ](../../../services/iam.md#access-denied-messages)

### 問2 {#q2}

パートナー企業のロールが、自社メンバーアカウントのバケットを読むと `AccessDenied` になり、メッセージは `with an explicit deny in a resource control policy` です。バケットポリシーとパートナーの IAM ポリシーは許可しています。事前にポリシーシミュレーターで確認したときは「許可」でした。この状況の説明として正しいものはどれですか。

- A. シミュレーターは RCP に未対応なので食い違った。RCP の例外を検討する
- B. シミュレーターが正しく、エラーは伝播の遅れなので、しばらく待ってから再試行すれば解決する
- C. パートナーの組織の SCP が原因なので、パートナーに SCP の変更を依頼する
- D. RCP は管理アカウントのリソースにだけ効くので、バケットを別のアカウントへ移す

??? success "答えと解説"
    **正解: A**

    シミュレーターは SCP を評価しますが RCP は未対応です。RCP の明示的な拒否は、どの許可より優先されます。

    - A: 正しい。
    - B: 誤り。メッセージが RCP の明示的な拒否を示しており、待っても解決しません。
    - C: 誤り。原因は自社の RCP です。メッセージに種類が出ています。
    - D: 誤り。RCP は管理アカウントのリソースには効かず、メンバーのリソースに効きます。

    **スキル:** [4.2.4](../domain4.md#skill-4-2-4) / **参照:** [ポリシーシミュレーター](../../../services/iam.md#policy-simulator)

### 問3 {#q3}

VPC 内の EC2 が S3 のゲートウェイエンドポイント経由でバケットを読むようにしました。以前はバケットポリシーで NAT の公開 IP を `aws:SourceIp` で許可しており、他の通信は拒否しています。切り替えてから `AccessDenied` になりました。修正はどれですか。

- A. NAT のルートを戻し、エンドポイントのルートを削除して、公開 IP の条件のまま維持する
- B. エンドポイントポリシーを `*` にして、バケットポリシーの `aws:SourceIp` の値を VPC の CIDR に変える
- C. エンドポイントに Elastic IP を割り当て、その IP を `aws:SourceIp` に追加する
- D. バケットポリシーの条件を `aws:SourceVpce` に書き換えて、対象のエンドポイントを許可する

??? success "答えと解説"
    **正解: D**

    エンドポイント経由のリクエストにはパブリック IP がなく、公開 IP の条件は一致しません。`aws:SourceVpce` を使います。

    - A: 誤り。プライベートな経路の目的に反します。
    - B: 誤り。バケットポリシーで CIDR を `aws:SourceIp` に指定しても一致しません。
    - C: 誤り。ゲートウェイエンドポイントに Elastic IP は付けられません。
    - D: 正しい。

    **スキル:** [4.2.4](../domain4.md#skill-4-2-4) / **参照:** [エンドポイントポリシー](../../../services/networking.md#endpoint-policies)

### 問4 {#q4}

外部の企業のロールが、自社のメンバーアカウントの SSE-KMS のバケットを読みます。バケットポリシーと外部のロールの IAM ポリシーでは S3 の操作を許可していますが、`GetObject` が失敗します。自社の SCP には該当する拒否はありません。追加で確認すべきものはどれですか。

- A. S3 の Object Lock のモードがガバナンスになっており、読み取りが制限されていないか
- B. 自社の SCP に外部の主体を許可する文を追加したか
- C. キーポリシーと外部のロールの双方で `kms:Decrypt` を許可しているか
- D. バケットのバージョニングが有効かどうか

??? success "答えと解説"
    **正解: C**

    KMS で暗号化されたオブジェクトは、S3 の許可に加えて KMS の許可が必要です。別のアカウントなので、キーポリシーと IAM の両方で許可します。

    - A: 誤り。Object Lock は読み取りを制限しません。
    - B: 誤り。SCP は外部の主体に効かず、許可も与えません。
    - C: 正しい。
    - D: 誤り。バージョニングはアクセス権に関係しません。

    **スキル:** [4.2.4](../domain4.md#skill-4-2-4) / **参照:** [クロスアカウントの評価](../../../services/identity-directory.md#cross-account-evaluation)

### 問5 {#q5}

EC2 の `RunInstances` が失敗し、`Encoded authorization failure message` として長い文字列が返りました。この文字列を読み取って、どのポリシーが拒否したかの情報を得たいと考えています。呼び出す人に必要な権限と手順はどれですか。（2つ選択）

- A. `aws sts decode-authorization-message` で文字列を復号する
- B. 呼び出し元の主体に `sts:DecodeAuthorizationMessage` を許可する
- C. CloudTrail で S3 データイベントを有効にして、復号された文字列をログから読む
- D. KMS の `Decrypt` を呼び、AWS 管理キーで文字列を復号する
- E. Base64 でデコードすれば、権限なしで誰でも読める

??? success "答えと解説"
    **正解: A, B**

    エンコードされたメッセージは STS の `DecodeAuthorizationMessage` で読みます。拒否の詳細を含むので、呼び出しには権限が必要です。

    - A: 正しい。
    - B: 正しい。
    - C: 誤り。データイベントは S3 のオブジェクト操作の記録で、関係しません。
    - D: 誤り。KMS は使いません。
    - E: 誤り。Base64 の変換では読めません。

    **スキル:** [4.2.4](../domain4.md#skill-4-2-4) / **参照:** [DecodeAuthorizationMessage](../../../services/iam.md#decode-authorization)

### 問6 {#q6}

組織の管理者が、全アカウントの S3 と KMS で「組織の外に共有されているもの」の一覧が欲しいと考えています。対象はポリシーで許可されているものすべてで、実際にアクセスがあったかは問いません。使うべきものはどれですか。

- A. CloudTrail のログを Athena で検索し、外部のアカウントからのアクセスを過去 1 年分集計する
- B. Macie の機密データの検出ジョブで、全バケットの中身と共有の状態を分類する
- C. 組織を信頼ゾーンにした外部アクセスの分析ツールをリージョンごとに作る
- D. Trusted Advisor のチェックを週 1 回実行し、公開バケットの結果だけを記録する

??? success "答えと解説"
    **正解: C**

    外部アクセスの分析ツールはログではなくポリシーを論理的に分析し、信頼ゾーンの外への共有を見つけます。リージョンごとに作ります。

    - A: 誤り。実際にアクセスがあったものしか分かりません。
    - B: 誤り。Macie の主な目的は機密データの検出で、KMS も対象外です。
    - C: 正しい。
    - D: 誤り。範囲が狭く、KMS や組織外へのアカウント単位の共有を網羅しません。

    **スキル:** [4.2.5](../domain4.md#skill-4-2-5) / **参照:** [外部アクセスの検出](../../../services/identity-directory.md#aa-external)

### 問7 {#q7}

開発者がリソースポリシーを Terraform で変更します。CI で「既存のポリシーより権限が増えていないか」と「`kms:ScheduleKeyDeletion` を許可していないか」を確認し、問題があればマージを止めます。呼び出す API の組み合わせはどれですか。

- A. `CheckNoNewAccess` と `CheckAccessNotGranted`
- B. `ValidatePolicy` と `CheckNoPublicAccess`
- C. `CreateAccessPreview` と `ValidatePolicy`
- D. `CheckNoPublicAccess` と `CheckNoNewAccess`

??? success "答えと解説"
    **正解: A**

    `CheckNoNewAccess` は更新後のポリシーが既存より新しいアクセスを許すかを確認します。`CheckAccessNotGranted` は指定のアクセスを許可しないことを確認します。

    - A: 正しい。
    - B: 誤り。`ValidatePolicy` は文法とベストプラクティス、`CheckNoPublicAccess` は公開の有無を見ます。
    - C: 誤り。`CreateAccessPreview` は外部アクセスの検出結果を事前に見るためのものです。
    - D: 誤り。`CheckNoPublicAccess` では特定の操作の許可を確認できません。

    **スキル:** [4.2.5](../domain4.md#skill-4-2-5) / **参照:** [ポリシーの検証とチェック](../../../services/identity-directory.md#aa-policy-checks)

### 問8 {#q8}

全アカウントの IAM ロールとユーザーについて、長期間使っていないロール、アクセスキー、権限を一覧にします。リージョンは多数使っていますが、分析ツールの管理はなるべく減らしたいと考えています。また費用の考え方も理解しておきます。正しい説明はどれですか。

- A. 外部アクセスの分析ツールを全リージョンに作成すれば、未使用の権限も一緒に検出できるので、費用もかからず管理も最小限で済む
- B. 未使用アクセスの分析ツールを作る。リージョンごとに作る必要はなく、課金はロールとユーザーの数による
- C. 未使用アクセスの分析ツールはリージョンごとに必要で、費用は検出結果の件数に基づく
- D. 内部アクセスの分析ツールを 1 つ作れば、未使用のアクセスキーも対象になる。費用は固定である

??? success "答えと解説"
    **正解: B**

    未使用アクセスの分析は結果がリージョンに依存せず、ロールとユーザーを課金の単位とします。

    - A: 誤り。外部アクセスは信頼ゾーンの外への共有を見るだけで、未使用の権限は見ません。
    - B: 正しい。
    - C: 誤り。リージョンごとには不要です。
    - D: 誤り。内部アクセスは重要なリソースへの経路の分析で、未使用のキーとは別です。

    **スキル:** [4.2.5](../domain4.md#skill-4-2-5) / **参照:** [未使用アクセスの検出](../../../services/identity-directory.md#aa-unused)

### 問9 {#q9}

組織にデータ境界を導入します。要件は「組織外の主体が組織のバケットを読めない」「組織の主体が組織外のバケットへ持ち出せない」です。どちらも個別のバケットポリシーの正しさに頼らないようにします。適切な組み合わせはどれですか。（2つ選択）

- A. RCP で `aws:PrincipalOrgID` が自組織でない主体からの S3 へのアクセスを拒否する
- B. SCP で `aws:ResourceOrgID` が自組織でないリソースへの S3 の操作を拒否する
- C. Access Analyzer の外部アクセスの検出結果を、EventBridge で週次にメール送信する
- D. Macie で組織のすべてのバケットのオブジェクトを分類し、機密データを別のバケットへ移す
- E. 各チームのバケットポリシーに `aws:PrincipalOrgID` の条件を書くよう、社内の標準を文書で配布する

??? success "答えと解説"
    **正解: A, B**

    データ境界は SCP、RCP、エンドポイントポリシーの組み合わせです。外から中は RCP、中から外は SCP が向きます。

    - A: 正しい。
    - B: 正しい。
    - C: 誤り。検出するだけで止めません。
    - D: 誤り。機密データの発見は境界の統制ではありません。
    - E: 誤り。個別のポリシーの正しさに頼っており、要件に反します。

    **スキル:** [4.2.5](../domain4.md#skill-4-2-5) / **参照:** [データ境界](../../../services/identity-directory.md#data-perimeter)

### 問10 {#q10}

データ境界の RCP を導入した翌日、CloudTrail のログが一部のバケットに配信されなくなりました。RCP の内容は「`aws:PrincipalOrgID` が自組織でないアクセスを S3 で拒否する」です。最も適切な修正はどれですか。

- A. RCP を削除し、外部アクセスの対策はすべて Access Analyzer の検出に任せる
- B. CloudTrail の証跡を組織の証跡からアカウントの証跡に切り替えて、配信先のバケットを移す
- C. RCP の条件に `aws:PrincipalIsAWSService` が `false` を加える
- D. 証跡の配信先を CloudWatch Logs に切り替え、S3 のログの保管をやめる

??? success "答えと解説"
    **正解: C**

    サービスプリンシパルは組織に属さないので、条件がないと拒否されます。AWS のサービスのアクセスを例外にします。`aws:SourceOrgID` などと組み合わせて、自組織のためのアクセスだけに絞る方法もあります。

    - A: 誤り。予防の統制を失います。
    - B: 誤り。サービスプリンシパルが拒否される点は変わりません。
    - C: 正しい。
    - D: 誤り。長期の保管が必要なログの要件に合いません。

    **スキル:** [4.2.5](../domain4.md#skill-4-2-5) / **参照:** [データ境界](../../../services/identity-directory.md#data-perimeter)
