# Organizations と統制の問題集

対象の解説: [Organizations と統制](../../../services/governance.md#organizations)

### 問1 {#q1}

新しい組織のアカウント構成を決めます。条件は次のとおりです。監査ログを開発者が消せない、パイプラインと本番を分離する、新しい SCP は本番の前に試す。管理アカウントには何も置きません。適切な構成はどれですか。

- A. 管理アカウントにログとパイプラインを集約し、他のアカウントから参照できるようにする
- B. 本番の OU の中に新しい SCP を直接適用して、問題があればすぐに外すことにする
- C. Security、Workloads、Deployments、Policy Staging の OU を作り、ログ用アカウントは Security に置く
- D. 1 つの OU に全アカウントを置いて、IAM のポリシーでログとパイプラインへのアクセスを分ける

??? success "答えと解説"
    **正解: C**

    用途ごとに OU を分け、ログは Security、パイプラインは Deployments、ポリシーの検証は Policy Staging に置きます。

    - A: 誤り。管理アカウントにはワークロードを置かない。SCP も効かない。
    - B: 誤り。本番の前に試すという条件に合わない。
    - C: 正しい。
    - D: 誤り。影響の範囲と SCP の適用を分けられない。

    **スキル:** [アカウント構成](../domain2.md#t2-2-structure) / **参照:** [マルチアカウントのパターン](../../../services/governance.md#multi-account-patterns)、[OU の設計](../../../services/governance.md#org-ous)

### 問2 {#q2}

監査で、次の指摘を受けました。GuardDuty と Config の管理の作業を、毎回管理アカウントのルートに近い権限で行っている。担当者の権限を減らし、影響を抑えるにはどうしますか。

- A. サービスごとにメンバーアカウントで別々に有効にして、組織の連携をすべて無効にする
- B. 担当者全員に管理アカウントの `AdministratorAccess` を付けて、CloudTrail で作業を記録する
- C. 各サービスの委任管理者を Security の専用アカウントにして、管理の作業をそこで行う
- D. 管理アカウントに SCP を付けて、担当者の操作を制限する

??? success "答えと解説"
    **正解: C**

    管理アカウントでは作業しません。サービスの管理は委任管理者に任せます。

    - A: 誤り。組織全体の管理の仕組みを失う。
    - B: 誤り。権限は減らず、影響の範囲も変わらない。
    - C: 正しい。
    - D: 誤り。SCP は管理アカウントに効かない。

    **スキル:** [アカウント構成](../domain2.md#t2-2-structure) / **参照:** [委任管理者](../../../services/governance.md#delegated-admin)、[マルチアカウントのパターン](../../../services/governance.md#multi-account-patterns)

### 問3 {#q3}

ある企業は、1 つのアカウントに 20 のチームのワークロードを同居させています。Lambda の同時実行のクォータの取り合い、費用の配分の難しさ、1 つのチームの誤操作の波及が問題です。根本的な改善はどれですか。

- A. VPC をチームごとに分け、IAM のポリシーでネットワークとコンピュートの権限を制限する
- B. チームや環境ごとにアカウントを分け、Organizations の OU で管理する
- C. 全チームのリソースにタグを付けて、タグで費用を集計できるようにする
- D. サービスクォータを全リージョンで最大に引き上げて、取り合いを減らす

??? success "答えと解説"
    **正解: B**

    アカウントを分けると、影響の範囲、権限、費用、クォータを分離できます。

    - A: 誤り。アカウントのクォータと費用の境界は分離できない。
    - B: 正しい。
    - C: 誤り。費用には効くが、クォータと影響の範囲は分離できない。
    - D: 誤り。誤操作の波及と費用の配分は残る。

    **スキル:** [アカウント構成](../domain2.md#t2-2-structure) / **参照:** [マルチアカウントのパターン](../../../services/governance.md#multi-account-patterns)、[Compute Optimizer と適正サイズ](../../../services/cost-management.md#compute-optimizer)

### 問4 {#q4}

Control Tower を使う組織で、新しいアカウントの発行を Terraform と Git のレビューの流れに統合します。発行のたびに、標準の IAM ロールと VPC も Terraform のコードで追加します。何を使いますか。

- A. Organizations の `CreateAccount` を Lambda で呼ぶ処理を自作し、Terraform をあとで実行する
- B. Customizations for Control Tower に CloudFormation テンプレートを追加し、Terraform のコードは書き換える
- C. Service Catalog のポートフォリオを各アカウントへ共有して、利用者に手で発行させる
- D. Account Factory for Terraform（AFT）のパイプラインで発行する

??? success "答えと解説"
    **正解: D**

    Terraform と Git で発行とカスタマイズを行うなら、Account Factory for Terraform です。

    - A: 誤り。発行の統制を自作することになり、Control Tower の管理も外れる。
    - B: 誤り。CloudFormation が前提で、Terraform の標準に合わない。
    - C: 誤り。手作業が残り、Git のレビューの流れにならない。
    - D: 正しい。

    **スキル:** [標準化と自動化](../domain2.md#t2-2-provisioning) / **参照:** [AWS Control Tower](../../../services/governance.md#control-tower)、[ドリフトと拡張](../../../services/governance.md#ct-drift)

### 問5 {#q5}

Control Tower を使わない組織で、OU にアカウントを追加すると、ログ転送のロールと S3 のパブリックブロックが自動で入る状態にします。手順を自作せず、最小の運用負荷にします。どうしますか。

- A. 全アカウントの設定を Config のルールで検出し、問題があれば毎週手で修正する
- B. CloudTrail の `CreateAccount` を EventBridge で受け、Lambda で全部の処理を自作する
- C. サービスマネージド権限の StackSets で、対象の OU への自動デプロイを有効にする
- D. 新しいアカウントごとに CloudShell でスクリプトを実行する手順を、担当者へ配布する

??? success "答えと解説"
    **正解: C**

    OU に入ると自動でスタックを作るのが StackSets の自動デプロイです。

    - A: 誤り。自動で入らず、検出だけになる。
    - B: 誤り。標準の機能で足りるのに、コードの運用が増える。
    - C: 正しい。
    - D: 誤り。手作業が残る。

    **スキル:** [標準化と自動化](../domain2.md#t2-2-provisioning) / **参照:** [StackSets の設定](../../../services/iac.md#stacksets-settings)、[AWS Control Tower](../../../services/governance.md#control-tower)

### 問6 {#q6}

Control Tower の環境で、全新規アカウントへ CloudFormation テンプレートと SCP を追加で展開します。設定はリポジトリで管理し、発行のたびにパイプラインで適用します。Terraform は使いません。何を選びますか。

- A. 管理アカウントの CloudFormation で、各アカウントに個別のスタックを手で作って適用する
- B. Customizations for Control Tower（CfCT）のパイプラインで適用する
- C. Account Factory for Terraform に CloudFormation の内容を Terraform へ書き直して登録する
- D. Service Catalog の製品を、利用者が発行の後に毎回自分で起動するように案内する

??? success "答えと解説"
    **正解: B**

    Customizations for Control Tower は、テンプレートとポリシーをパイプラインで追加展開します。

    - A: 誤り。自動にならず、アカウントが増えるほど手間が増える。
    - B: 正しい。
    - C: 誤り。Terraform を使わないという条件に反する。
    - D: 誤り。発行のたびに自動で適用されない。

    **スキル:** [標準化と自動化](../domain2.md#t2-2-provisioning) / **参照:** [ドリフトと拡張](../../../services/governance.md#ct-drift)、[AWS Control Tower](../../../services/governance.md#control-tower)

### 問7 {#q7}

Control Tower を導入済みの環境で、管理者が Organizations のコンソールから、登録済みの OU の SCP を直接変更しました。その後、警告が出ています。正しい理解と対処はどれですか。

- A. ドリフトなので、表示された内容に従い、ランディングゾーンの更新や OU の再登録で解消する
- B. Control Tower の外での変更はそのまま正式な構成として取り込まれるので、対処は要らない
- C. 組織を削除して、新しい組織で Control Tower を構築し直す
- D. Organizations の機能セットが請求の一括のみに戻るので、すべての機能を再度有効にする

??? success "答えと解説"
    **正解: A**

    Control Tower の外で OU や SCP を変更するとドリフトになります。表示に従って解消します。

    - A: 正しい。
    - B: 誤り。外での変更はドリフトになり、取り込まれない。
    - C: 誤り。過剰で、ドリフトの解消に必要ない。
    - D: 誤り。SCP の変更で機能セットは戻らない。

    **スキル:** [Organizations と Control Tower](../domain2.md#t2-2-org-ct) / **参照:** [ドリフトと拡張](../../../services/governance.md#ct-drift)、[ランディングゾーンの構造](../../../services/governance.md#ct-landing-zone)

### 問8 {#q8}

買収した会社の組織を統合します。その会社のアカウントは現在、別の組織にあり、一括請求の機能だけを使っています。統合の後、全アカウントに SCP を適用します。必要な手順の組み合わせはどれですか。（2つ選択）

- A. アカウントを元の組織から外し、自社の組織からの招待を受けて移す
- B. 自社の組織で、すべての機能を有効にする
- C. 元の組織と自社の組織を、VPC ピアリングでつなぐ
- D. 元の組織に SCP を残したまま、自社の組織の委任管理者を追加する
- E. アカウントの ID を新しく発行して、データをコピーする

??? success "答えと解説"
    **正解: A, B**

    SCP にはすべての機能の有効化が必要です。アカウントは招待で組織へ移せます。

    - A: 正しい。
    - B: 正しい。
    - C: 誤り。ネットワークの接続で、組織の統合にならない。
    - D: 誤り。別の組織の委任管理者にはなれない。
    - E: 誤り。アカウントは招待で移せるので、作り直す必要はない。

    **スキル:** [Organizations と Control Tower](../domain2.md#t2-2-org-ct) / **参照:** [機能セット](../../../services/governance.md#org-feature-sets)、[SCP](../../../services/governance.md#scp)

### 問9 {#q9}

独自の OU と SCP を持つ既存の組織があります。ログと監査のアカウント、基本のコントロール、新規アカウントの発行の仕組みを、できるだけ早く標準の形にします。既存のアカウントは止められません。どう進めますか。

- A. 既存の組織を解散して新しい組織を作り、全アカウントを 1 つずつ招待して移す
- B. 既存の組織に Control Tower を導入し、既存の OU を順に登録する
- C. Organizations の機能だけで、ログ用のアカウントと SCP を手で作り続ける
- D. 全アカウントに Config の適合パックを配って、それをランディングゾーンの代わりにする

??? success "答えと解説"
    **正解: B**

    Control Tower は既存の組織へ後から導入でき、OU を登録すると統制の下に入ります。

    - A: 誤り。大きな作業になり、既存の組織に後から導入できるので不要。
    - B: 正しい。
    - C: 誤り。動くが、標準の形を早く作るという条件に合わない。
    - D: 誤り。検出の仕組みで、アカウントの発行もログの集約も作らない。

    **スキル:** [Organizations と Control Tower](../domain2.md#t2-2-org-ct) / **参照:** [AWS Control Tower](../../../services/governance.md#control-tower)、[ランディングゾーンの構造](../../../services/governance.md#ct-landing-zone)

### 問10 {#q10}

本番の OU で、次の SCP を適用した後も、各アカウントの管理者ロールが別のリージョンにリソースを作れました。ポリシーは `aws:RequestedRegion` が東京以外なら拒否する内容です。調べると、操作は管理アカウントからの実行でした。原因はどれですか。

- A. SCP は管理アカウントには効かない
- B. SCP は `Deny` を書けないので、`Allow` のリストに書き直す必要がある
- C. 権限境界が設定されていないロールには、SCP が効かない
- D. サービスリンクロールが操作したので、SCP が適用されなかった

??? success "答えと解説"
    **正解: A**

    SCP は管理アカウントの主体に効きません。管理アカウントにはワークロードを置かず、作業も制限します。

    - A: 正しい。
    - B: 誤り。SCP は `Deny` を書ける。
    - C: 誤り。SCP は権限境界の有無に関係なく効く。
    - D: 誤り。問題の操作は管理者ロールの実行で、説明が合わない。

    **スキル:** [複数アカウントの IAM](../domain2.md#t2-2-iam) / **参照:** [SCP](../../../services/governance.md#scp)、[クロスアカウントアクセス](../../../services/iam.md#cross-account)

### 問11 {#q11}

ツール用アカウントのロールが、本番アカウントのロールを引き受けて S3 を読もうとすると拒否されます。本番のロールの信頼ポリシーはツール用のロールを許可しています。本番のロールには S3 の読み取りがあります。ツール用アカウントの SCP は `sts:AssumeRole` を許可しています。残る原因として考えられるものはどれですか。（2つ選択）

- A. 本番のロールのセッションの時間が 12 時間より短い
- B. 本番の OU の SCP が、S3 の読み取りを拒否している
- C. 本番のロールに `aws:PrincipalOrgID` の条件が付いていない
- D. ツール用のロールの ID ベースポリシーに、`sts:AssumeRole` の許可がない
- E. ツール用アカウントのルートユーザーに MFA が設定されていない

??? success "答えと解説"
    **正解: B, D**

    別のアカウントのロールの引き受けには呼び出し側の許可が必要です。引き受けた後の操作には、そのアカウントの SCP も効きます。

    - A: 誤り。セッションの長さは拒否の原因にならない。
    - B: 正しい。
    - C: 誤り。この条件は許可を絞るもので、付いていないことは拒否の原因にならない。
    - D: 正しい。
    - E: 誤り。別の主体の設定で、この呼び出しに影響しない。

    **スキル:** [複数アカウントの IAM](../domain2.md#t2-2-iam) / **参照:** [クロスアカウントの評価](../../../services/identity-directory.md#cross-account-evaluation)、[クロスアカウントアクセス](../../../services/iam.md#cross-account)

### 問12 {#q12}

S3 のログバケットを、組織の全アカウントのロールだけが読めるようにします。アカウント ID を列挙せず、新しいアカウントでも更新を不要にします。外部の取引先を誤って許可しないようにします。適切な方法はどれですか。

- A. バケットポリシーの `Principal` に全アカウントの ID を列挙し、追加のたびに更新する
- B. バケットポリシーの条件に `aws:PrincipalOrgID` を指定する
- C. バケットの ACL で、Authenticated Users グループに読み取りを許可する
- D. 全アカウントの SCP で、S3 の読み取りを許可するように書き換える

??? success "答えと解説"
    **正解: B**

    `aws:PrincipalOrgID` で自組織に限定できます。新しいアカウントも更新なしで含まれます。

    - A: 誤り。更新を不要にするという条件に反する。
    - B: 正しい。
    - C: 誤り。AWS の全認証済みの利用者に開放される。
    - D: 誤り。SCP は権限を与えない。

    **スキル:** [複数アカウントの IAM](../domain2.md#t2-2-iam) / **参照:** [クロスアカウントアクセス](../../../services/iam.md#cross-account)、[RCP](../../../services/governance.md#rcp)

### 問13 {#q13}

次の統制を実現します。(1) 暗号化していない S3 バケットの作成を CloudFormation の実行前に止める。(2) 許可されていないリージョンの操作を全面的に止める。(3) 既に公開されているバケットを検出する。Control Tower の種類の組み合わせとして正しいものはどれですか。

- A. (1) 予防的、(2) 検出的、(3) プロアクティブ
- B. (1) 検出的、(2) プロアクティブ、(3) 予防的
- C. (1) プロアクティブ、(2) 検出的コントロール、(3) 予防的コントロール
- D. (1) プロアクティブ、(2) 予防的、(3) 検出的

??? success "答えと解説"
    **正解: D**

    プロアクティブは CloudFormation Hooks で作成前に止めます。予防的は SCP で操作を止め、検出的は Config で検出します。

    - A: 誤り。(2) を操作の後に検出しても止まらず、(3) は作成前に止める種類ではない。
    - B: 誤り。種類の役割がすべて入れ違っている。
    - C: 誤り。(2) は止める必要があり、既存の状態の検出は検出的コントロールの役割。
    - D: 正しい。

    **スキル:** [統制とセキュリティ](../domain2.md#t2-2-governance) / **参照:** [コントロール](../../../services/governance.md#ct-controls)、[SCP](../../../services/governance.md#scp)

### 問14 {#q14}

200 アカウント、10 リージョンの組織で、Security Hub CSPM の標準の有効化と GuardDuty の有効化を統一します。新しいアカウントでも自動で有効にし、各アカウントの担当者が勝手に標準を外せないようにします。適切な組み合わせはどれですか。

- A. Security Hub CSPM の中央設定と、GuardDuty の委任管理者による組織の自動有効化
- B. GuardDuty の結果を Security Hub CSPM へ送るだけで、Security Hub CSPM が GuardDuty を自動で有効にする
- C. 各アカウントで個別に有効にして、Config のルールで有効化の状況を確認する
- D. 管理アカウントで全部を有効にし、管理アカウントの設定が全メンバーへ自動で複製されるようにする

??? success "答えと解説"
    **正解: A**

    Security Hub CSPM は中央設定で標準を管理します。GuardDuty は委任管理者が組織のアカウントを自動で有効にします。

    - A: 正しい。
    - B: 誤り。連携は結果の送信で、有効化を代行しない。
    - C: 誤り。手間が増え、有効化の自動化にならない。
    - D: 誤り。そのような複製の仕組みはない。委任管理者が管理する。

    **スキル:** [統制とセキュリティ](../domain2.md#t2-2-governance) / **参照:** [組織と集約](../../../services/threat-detection.md#security-hub-org)、[複数アカウント](../../../services/threat-detection.md#guardduty-multi-account)

### 問15 {#q15}

セキュリティ担当の質問に、それぞれサービスで答えます。(1) この GuardDuty の検出結果に関係するロールが、過去 30 日で何をしたか。(2) 各チームに標準の VPC を配り、独自の VPC を作らせない。(3) 全アカウントのリソースの設定が基準に合っているか。適切な組み合わせはどれですか。

- A. (1) Detective、(2) Service Catalog と SCP、(3) AWS Config
- B. (1) Inspector、(2) CloudFormation Hooks、(3) Detective
- C. (1) Security Hub CSPM、(2) AWS Config の修復、(3) CloudTrail
- D. (1) Macie、(2) Control Tower の Account Factory、(3) GuardDuty

??? success "答えと解説"
    **正解: A**

    調査は Detective、承認済みの構成の提供は Service Catalog、設定の評価は Config です。

    - A: 正しい。
    - B: 誤り。Inspector は脆弱性のスキャンで、Detective は基準の評価をしない。
    - C: 誤り。Security Hub CSPM は影響範囲の調査の道具ではなく、CloudTrail は基準を評価しない。
    - D: 誤り。Macie は S3 の機密データの検出で、GuardDuty は設定の評価をしない。

    **スキル:** [統制とセキュリティ](../domain2.md#t2-2-governance) / **参照:** [Detective](../../../services/threat-detection.md#detective)、[GuardDuty](../../../services/threat-detection.md#guardduty)、[AWS Service Catalog](../../../services/governance.md#service-catalog)
