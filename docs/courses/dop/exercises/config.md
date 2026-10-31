# AWS Configの問題集

対象の解説: [AWS Config](../../../services/governance.md#config)

### 問1 {#q1}

新しい EBS ボリュームの暗号化の有無を AWS Config のマネージドルールで評価しています。担当者は、暗号化されていないボリュームの作成がなぜ止まらないのかと質問しました。正しい説明と対応はどれですか。

- A. 評価モードが検出的なので止まらない。Lambda のカスタムルールにすれば作成を止められる
- B. ルールのトリガーが定期なので止まらない。設定変更のトリガーへ変えれば止まる
- C. ルールは判定するだけで止めない。止めるには SCP やプロアクティブなコントロールを使う
- D. レコーダーが停止しているので止まらない。レコーダーを起動すれば止まる

??? success "答えと解説"
    **正解: C**

    Config のルールは判定するだけです。止めるには SCP などを使います。

    - A: 誤り。カスタムルールでも操作は止めない。
    - B: 誤り。どのトリガーでも操作を止めない。
    - C: 正しい。
    - D: 誤り。記録が動いても操作は止まらない。

    **スキル:** [Config ルール](../domain4.md#t4-2-config-rules) / **参照:** [Config ルール](../../../services/governance.md#config-rules)、[Config と CloudTrail の違い](../../../services/governance.md#config-vs-cloudtrail)

### 問2 {#q2}

次の要件に合うルールの設定を選びます。(1) タグの付け忘れを、リソースの変更のたびに評価する。(2) ルートの MFA の状態を毎日確認する。(3) 社内独自の命名規則を評価する。適切な組み合わせはどれですか。

- A. (1) 設定変更のトリガー、(2) 定期のトリガー、(3) カスタムルール
- B. (1) 定期、(2) 設定変更、(3) プロアクティブ
- C. (1) 設定変更、(2) 定期、(3) SCP
- D. (1) カスタムルール、(2) 設定変更のトリガー、(3) マネージドルールのパラメータ

??? success "答えと解説"
    **正解: A**

    トリガーは設定変更と定期、独自の条件はカスタムルールで評価します。

    - A: 正しい。
    - B: 誤り。(1) と (2) のトリガーが逆で、(3) は評価モードの話。
    - C: 誤り。SCP は Config のルールの種類ではない。
    - D: 誤り。マネージドルールに社内の規則はない。

    **スキル:** [Config ルール](../domain4.md#t4-2-config-rules) / **参照:** [Config ルール](../../../services/governance.md#config-rules)、[設定レコーダー](../../../services/governance.md#config-recorder)

### 問3 {#q3}

Config のルールを有効にしたのに、すべて「評価なし」のままです。リージョンの他のアカウントでは評価されています。最初に確認するものはどれですか。また、CloudFormation のデプロイの前に評価できるかも確認します。

- A. Security Hub CSPM の標準の有効化の状況。デプロイの前の評価はできない
- B. CloudTrail の証跡の有無。デプロイの前の評価は変更セットで行う
- C. 設定レコーダーが対象のリソースを記録しているか。デプロイの前の評価はプロアクティブな評価モードで行う
- D. ルールのスコープのタグと評価の頻度。デプロイの前の評価は CloudFormation Hooks だけで行う

??? success "答えと解説"
    **正解: C**

    設定レコーダーが動いていないと評価できません。プロアクティブの評価モードは、作成前のリソースの設定を評価します。

    - A: 誤り。Config のルールの前提ではなく、プロアクティブな評価モードもある。
    - B: 誤り。証跡はルールの前提ではなく、変更セットは Config の評価ではない。
    - C: 正しい。
    - D: 誤り。すべてのルールが評価なしになる説明にならず、プロアクティブな評価モードもある。

    **スキル:** [Config ルール](../domain4.md#t4-2-config-rules) / **参照:** [Config ルール](../../../services/governance.md#config-rules)、[設定レコーダー](../../../services/governance.md#config-recorder)

### 問4 {#q4}

公開された S3 バケットを自動で修復します。Config のルールで検出し、Automation ドキュメントを関連付けました。非準拠の判定は出ていますが、修復の実行はログの権限エラーで失敗します。確認するものはどれですか。

- A. ルールの評価モードとトリガーの種類
- B. SSM Agent の状態とインスタンスプロファイル
- C. 修復のランブックが使うロールの権限と信頼ポリシー
- D. 修復のアクションの再試行の回数と間隔

??? success "答えと解説"
    **正解: C**

    修復はランブックのロールで実行します。必要最小限の権限と信頼関係を確認します。

    - A: 誤り。検出は動いており、修復の権限と関係がない。
    - B: 誤り。バケットの設定の変更は API の操作で、インスタンスを介さない。
    - C: 正しい。
    - D: 誤り。権限のエラーは再試行では直らない。

    **スキル:** [Config の修復](../domain4.md#t4-3-config-remediation) / **参照:** [修復](../../../services/governance.md#config-remediation)

### 問5 {#q5}

公開の S3 バケットを自動で修復すると、別の仕組みが元に戻して、修復が延々と繰り返されました。適切な対応の組み合わせはどれですか。（2つ選択）

- A. 修復の再試行の回数を制限し、結果を SNS か OpsCenter で人に伝える
- B. Config のレコーダーを止めて、ループの検知をやめる
- C. S3 バケットのスタックポリシーで更新を拒否して、パイプラインが設定を戻せないようにする
- D. 元に戻している IaC のパイプラインを特定し、正しい設定をコードに反映する
- E. 修復の再試行の間隔をなくし、より早く修復を繰り返す

??? success "答えと解説"
    **正解: A, D**

    修復の連鎖によるループは、原因の仕組みを直します。

    - A: 正しい。
    - B: 誤り。監視を失う。
    - C: 誤り。パイプラインの更新が失敗するだけで、コードの誤りが残る。
    - D: 正しい。
    - E: 誤り。連鎖が速くなるだけ。

    **スキル:** [Config の修復](../domain4.md#t4-3-config-remediation) / **参照:** [修復](../../../services/governance.md#config-remediation)、[EventBridge による修復パターン](../../../services/operations.md#eventbridge-remediation)

### 問6 {#q6}

90 日より古いアクセスキーを持つユーザーの検出は `access-keys-rotated` で行っています。自動修復でキーを無効にしますが、担当者の確認の時間を 3 日設けたいと考えています。また、誤って無効にしたときは人が判断して戻します。適切な設計はどれですか。

- A. ルールを手動の修復にして、担当者がいつでも好きなときに実行できるようにする
- B. 修復を自動にして、すぐにキーを削除する
- C. EventBridge の非準拠のイベントで通知し、Step Functions の待機の後に Automation で無効にする
- D. SCP でアクセスキーの全 API を拒否する

??? success "答えと解説"
    **正解: C**

    定型の修復を人の判断と組み合わせるときは、待機を挟めるワークフローで構成します。

    - A: 誤り。3 日の期限が守られない。
    - B: 誤り。確認の時間がなく、戻せない。
    - C: 正しい。
    - D: 誤り。全員に影響し、検出の後の個別の対応にならない。

    **スキル:** [Config の修復](../domain4.md#t4-3-config-remediation) / **参照:** [修復](../../../services/governance.md#config-remediation)、[アクセスキーの扱い](../../../services/iam.md#access-key-handling)

### 問7 {#q7}

Config のルールが非準拠になったら、当番へ通知します。全リソースの全変更を通知するのではなく、準拠の状態の変化だけを受けます。どのイベントを使いますか。

- A. `AWS API Call via CloudTrail`
- B. `Config Configuration Item Change`
- C. `Security Hub Findings - Imported`
- D. `Config Rules Compliance Change`

??? success "答えと解説"
    **正解: D**

    準拠の状態が変わると `Config Rules Compliance Change` のイベントが発生します。

    - A: 誤り。API の呼び出しのイベントで、準拠の状態の変化ではない。
    - B: 誤り。全変更が通知される。
    - C: 誤り。Security Hub CSPM のイベントで、条件に合わない。
    - D: 正しい。

    **スキル:** [構成管理](../domain5.md#t5-2-config) / **参照:** [Config ルール](../../../services/governance.md#config-rules)、[ルールとイベントパターン](../../../services/messaging.md#eventbridge-rules)

### 問8 {#q8}

組織の全アカウントの Config の評価を、1 か所のアカウントから見ます。また、同じ一連のルールをまとめて全アカウントへ配ります。適切な組み合わせはどれですか。

- A. アグリゲーターと、組織の適合パックのデプロイ
- B. 組織の適合パックと、各アカウントのコンソールの確認
- C. CloudTrail の組織の証跡と、組織の Config ルール
- D. アグリゲーターと、SCP によるルールの強制

??? success "答えと解説"
    **正解: A**

    全社の状況はアグリゲーターで見ます。ルールのまとめての配布は組織の適合パックです。

    - A: 正しい。
    - B: 誤り。配布はできるが、1 か所から評価を見られない。
    - C: 誤り。証跡は API の記録で、評価の集約にならない。
    - D: 誤り。SCP は権限の上限で、Config のルールを配らない。

    **スキル:** [構成管理](../domain5.md#t5-2-config) / **参照:** [アグリゲーター](../../../services/governance.md#config-aggregators)、[適合パック](../../../services/governance.md#config-conformance-packs)

### 問9 {#q9}

障害の調査で、3 日前の時点のセキュリティグループの規則と、関連する ENI の関係を確認します。対象のリージョンで Config のレコーダーは有効です。どの機能で確認しますか。

- A. VPC Reachability Analyzer で現在の経路を分析する
- B. VPC フローログの 3 日前の記録
- C. AWS Config の設定履歴（設定項目のタイムライン）
- D. CloudTrail のイベント履歴を読み、規則を手で再計算する

??? success "答えと解説"
    **正解: C**

    Config は設定項目の履歴と関係を記録します。

    - A: 誤り。現在の構成の分析で、3 日前の時点を示さない。
    - B: 誤り。通信の記録で、設定の状態ではない。
    - C: 正しい。
    - D: 誤り。可能でも手間がかかり、設定の状態の確認の手段として適切でない。

    **スキル:** [構成管理](../domain5.md#t5-2-config) / **参照:** [設定レコーダー](../../../services/governance.md#config-recorder)、[Config と CloudTrail の違い](../../../services/governance.md#config-vs-cloudtrail)

### 問10 {#q10}

本番のアカウントで、暗号化が無効の EBS のデフォルトの設定を検出して自動で直します。結果も人に伝えます。カスタムの Lambda は書きません。適切な構成はどれですか。

- A. Config のカスタムルールを Lambda で書き、非準拠を SNS へ通知して担当者が直す
- B. GuardDuty の検出結果を Security Hub CSPM へ送り、自動化ルールで重要度を更新するだけにする
- C. Config のルールと、Automation のランブックによる自動の修復、SNS の通知
- D. Security Hub CSPM の標準で検出して、検出結果を週次で確認する

??? success "答えと解説"
    **正解: C**

    AWS リソースの設定の修復は Config の自動修復です。

    - A: 誤り。カスタムの Lambda を書かない条件に反し、自動で直らない。
    - B: 誤り。設定の修復にならない。
    - C: 正しい。
    - D: 誤り。検出だけで、自動で直らない。

    **スキル:** [状態の修復](../domain5.md#t5-2-remediate) / **参照:** [修復](../../../services/governance.md#config-remediation)

### 問11 {#q11}

次の望ましくない状態を修復します。(1) サーバーの中で必須のセキュリティエージェントのサービスが止まった。(2) CloudFormation のスタックのセキュリティグループが手で変更された。適切な組み合わせはどれですか。

- A. (1) Config のカスタムルールから Lambda が SSH で入って起動する、(2) スタックの削除と再作成
- B. (1) Inventory の再収集、(2) ドリフト検出で自動で修復する
- C. (1) State Manager の関連付け、(2) ドリフトの内容をテンプレートへ反映するか再デプロイする
- D. (1) AppConfig で再デプロイ、(2) スタックポリシーで元へ戻す

??? success "答えと解説"
    **正解: C**

    サーバーの中は State Manager で、スタックのドリフトはテンプレートへの反映か再デプロイで直します。

    - A: 誤り。SSH の依存が増え、再作成は過剰。
    - B: 誤り。どちらも収集と検出で、修復をしない。
    - C: 正しい。
    - D: 誤り。AppConfig はサービスの状態を保たず、スタックポリシーは変更を戻さない。

    **スキル:** [状態の修復](../domain5.md#t5-2-remediate) / **参照:** [State Manager](../../../services/operations.md#state-manager)、[ドリフト検出](../../../services/iac.md#drift)

### 問12 {#q12}

Auto Scaling の起動の失敗のイベントに対応します。定型の修復が決まっているものは自動で直し、原因が分からないものは人の調査の記録を残して、関連する情報も一緒に見ます。適切な組み合わせはどれですか。（2つ選択）

- A. すべてのイベントを OpsItem にして、担当者が順に修復する
- B. 人の判断が要るものは OpsCenter に OpsItem を作る
- C. 定型の修復にも Step Functions で人の承認を必須にする
- D. Trusted Advisor のチェックの更新を EventBridge で受けて修復する
- E. 定型の修復は EventBridge から Automation を直接呼ぶ

??? success "答えと解説"
    **正解: B, E**

    定型は Automation、人の判断は OpsItem に分けます。

    - A: 誤り。定型のものまで人の作業になる。
    - B: 正しい。
    - C: 誤り。定型のものを自動で直すという条件に反する。
    - D: 誤り。起動の失敗のイベントを受ける経路にならない。
    - E: 正しい。

    **スキル:** [状態の修復](../domain5.md#t5-2-remediate) / **参照:** [OpsCenter](../../../services/operations.md#opscenter)、[Automation](../../../services/operations.md#automation)
