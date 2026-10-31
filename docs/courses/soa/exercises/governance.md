# Organizations、Trusted Advisor、Config の問題集

対象の解説: [AWS Organizations](../../../services/governance.md#organizations)、[SCP](../../../services/governance.md#scp)、[AWS Control Tower](../../../services/governance.md#control-tower)、[AWS Config](../../../services/governance.md#config)、[Trusted Advisor](../../../services/cloud-foundations.md#trusted-advisor)

### 問1 {#q1}

SCP の説明として正しいものを選んでください。（2つ選択）

- A. SCP で許可しても、IAM の許可は別に必要である
- B. SCP はサービスリンクロールも制限する
- C. SCP は権限を与えるので、IAM ポリシーは不要である
- D. 委任管理者のアカウントは SCP の影響を受けない
- E. 管理アカウントは SCP の影響を受けない

??? success "答えと解説"
    **正解: A, E**

    SCP は権限の上限を決めます。

    - A: 正しい。
    - B: 誤り。サービスリンクロールは制限できない。
    - C: 誤り。SCP は上限を決めるだけで、権限を与えない。
    - D: 誤り。メンバーアカウントなので影響を受ける。
    - E: 正しい。

    **スキル:** [4.1.3](../domain4.md#skill-4-1-3) / **参照:** [SCP](../../../services/governance.md#scp)

### 問2 {#q2}

本番の全アカウントに新しい拒否の SCP を付けたいですが、影響が読めません。どの進め方が適切ですか。

- A. ポリシーシミュレーターで確かめて、全アカウントへ一度に適用する
- B. テスト用の OU にアカウントを少しずつ移す
- C. ルートに直接付けて、問題があれば外す
- D. 管理アカウントで動作を試す

??? success "答えと解説"
    **正解: B**

    適用の前に、テスト用の OU で確認します。

    - A: 誤り。シミュレーターの結果は実際と異なることがあり、段階的な適用の代わりにならない。
    - B: 正しい。
    - C: 誤り。影響が全アカウントに及ぶ。
    - D: 誤り。管理アカウントは SCP の影響を受けないので、試験にならない。

    **スキル:** [4.1.3](../domain4.md#skill-4-1-3) / **参照:** [SCP](../../../services/governance.md#scp)、[OU の設計](../../../services/governance.md#org-ous)

### 問3 {#q3}

複数のアカウントへ、1 か所のサインインでアクセスさせたいです。権限は職務ごとにまとめます。どれが適切ですか。

- A. アカウントごとに IAM ユーザーを作成する
- B. SCP で権限を付与する
- C. IAM Identity Center の権限セットを割り当てる
- D. IAM Access Analyzer でアカウント間のアクセスをまとめる

??? success "答えと解説"
    **正解: C**

    権限セットをアカウントに割り当てると、各アカウントに IAM ロールが作られます。

    - A: 誤り。1 か所のサインインにならない。
    - B: 誤り。SCP は権限を与えない。
    - C: 正しい。
    - D: 誤り。アクセスを分析する機能で、サインインの仕組みではない。

    **スキル:** [4.1.3](../domain4.md#skill-4-1-3) / **参照:** [権限セット](../../../services/identity-directory.md#idc-permission-sets)、[IAM Identity Center](../../../services/identity-directory.md#identity-center)

### 問4 {#q4}

Control Tower のコントロールの動作と実装の組み合わせとして正しいものはどれですか。

- A. プロアクティブ: CloudFormation Hooks
- B. プロアクティブ: Config ルール
- C. 予防的: Config ルール
- D. 検出的: SCP

??? success "答えと解説"
    **正解: A**

    プロアクティブは作成の前に確認し、不適合なら作りません。

    - A: 正しい。
    - B: 誤り。プロアクティブは CloudFormation Hooks で実装する。
    - C: 誤り。予防的は SCP や RCP で実装する。
    - D: 誤り。検出的は Config ルールで実装する。

    **スキル:** [4.1.3](../domain4.md#skill-4-1-3) / **参照:** [コントロール](../../../services/governance.md#ct-controls)

### 問5 {#q5}

組織の外のプリンシパルが、組織の S3 バケットへアクセスできないよう、リソース側の上限を一律に決めたいです。どれを使いますか。

- A. SCP
- B. タグポリシー
- C. バックアップポリシー
- D. RCP

??? success "答えと解説"
    **正解: D**

    RCP はリソース側の上限を決めます。

    - A: 誤り。SCP はメンバーアカウントのプリンシパルに適用される。
    - B: 誤り。タグの標準化の機能である。
    - C: 誤り。バックアップの機能である。
    - D: 正しい。

    **スキル:** [4.1.3](../domain4.md#skill-4-1-3) / **参照:** [RCP](../../../services/governance.md#rcp)、[SCP](../../../services/governance.md#scp)

### 問6 {#q6}

Trusted Advisor のセキュリティチェックの指摘について正しいものはどれですか。

- A. イベントは各リージョンの EventBridge に同じものが届くので、リージョンごとにルールを作って受ける
- B. 自動で修復するなら、結果の変化を EventBridge で受けて Lambda か Automation を動かす
- C. 全チェックと API は Basic のプランでも使える
- D. 指摘されたものは Trusted Advisor が自動で直す

??? success "答えと解説"
    **正解: B**

    Trusted Advisor は助言するだけです。

    - A: 誤り。`us-east-1` に届き、配信はベストエフォートである。
    - B: 正しい。
    - C: 誤り。Business Support+ 以上である。
    - D: 誤り。助言するだけで、自動では直さない。

    **スキル:** [4.1.4](../domain4.md#skill-4-1-4) / **参照:** [Trusted Advisor](../../../services/cloud-foundations.md#trusted-advisor)

### 問7 {#q7}

Trusted Advisor で S3 バケットの権限の指摘が出ました。公開の必要はありません。修復として適切なものはどれですか。

- A. ブロックパブリックアクセスを有効にし、ポリシーを直す
- B. CloudFront の地理的制限で国を絞る設定を加える
- C. バケットのバージョニングを有効にして、前のバージョンを残す
- D. バケットのストレージクラスを Standard-IA へ変更する

??? success "答えと解説"
    **正解: A**

    公開が不要なら、ブロックパブリックアクセスを有効にします。

    - A: 正しい。
    - B: 誤り。オリジンのバケットの公開の設定は直らない。
    - C: 誤り。公開の設定は直らない。
    - D: 誤り。アクセスの制御とは関係がない。

    **スキル:** [4.1.4](../domain4.md#skill-4-1-4) / **参照:** [Trusted Advisor](../../../services/cloud-foundations.md#trusted-advisor)、[ブロックパブリックアクセス](../../../services/s3.md#block-public-access)

### 問8 {#q8}

Trusted Advisor でセキュリティグループの指摘が出ました。SSH が `0.0.0.0/0` に開いています。修復として適切なものを選んでください。（2つ選択）

- A. インスタンスに Elastic IP を割り当てる
- B. 必要な範囲だけにルールを絞る
- C. Session Manager へ移し、ポート 22 のルールを削除する
- D. CloudTrail の証跡でデータイベントを有効にする
- E. ネットワーク ACL で番号の大きいルールに許可を追加する

??? success "答えと解説"
    **正解: B, C**

    特定のポートを必要な範囲へ絞ります。

    - A: 誤り。開放のルールは直らない。
    - B: 正しい。
    - C: 正しい。
    - D: 誤り。記録の設定で、開放のルールは直らない。
    - E: 誤り。開放のルールは直らない。

    **スキル:** [4.1.4](../domain4.md#skill-4-1-4) / **参照:** [Trusted Advisor](../../../services/cloud-foundations.md#trusted-advisor)、[セキュリティグループのルール](../../../services/networking.md#security-group-rules)

### 問9 {#q9}

次の見分け方として正しいものはどれですか。

- A. 自分の設定の改善は AWS Health Dashboard、AWS 側の障害の影響は Trusted Advisor で確認する
- B. 幅広い助言は Security Hub CSPM、基準の準拠チェックは Trusted Advisor
- C. 自分の設定の改善は Trusted Advisor、AWS 側の障害の影響は Health Dashboard
- D. 公開スナップショットのチェックは Compute Optimizer、MFA のチェックは Macie

??? success "答えと解説"
    **正解: C**

    それぞれの役割を区別します。

    - A: 誤り。逆である。
    - B: 誤り。逆である。
    - C: 正しい。
    - D: 誤り。どちらも Trusted Advisor のチェックである。

    **スキル:** [4.1.4](../domain4.md#skill-4-1-4) / **参照:** [Trusted Advisor](../../../services/cloud-foundations.md#trusted-advisor)、[AWS Health Dashboard](../../../services/cloud-foundations.md#health)

### 問10 {#q10}

`ap-northeast-1` 以外の操作を止める SCP を作りました。すると、IAM の操作まで止まりました。どう直しますか。

- A. IAM ユーザーに `AdministratorAccess` を付ける
- B. 条件キーを `aws:SourceIp` に変更する
- C. 付ける先を管理アカウントに変更する
- D. `NotAction` でグローバルサービスを除く

??? success "答えと解説"
    **正解: D**

    `aws:RequestedRegion` の制限では、IAM などのグローバルサービスを除きます。

    - A: 誤り。SCP の拒否は IAM の許可では覆せない。
    - B: 誤り。リージョンの制限にならない。
    - C: 誤り。管理アカウントには効かない。
    - D: 正しい。

    **スキル:** [4.1.5](../domain4.md#skill-4-1-5) / **参照:** [SCP](../../../services/governance.md#scp)、[NotAction](../../../services/iam.md#notaction)、[主なグローバル条件キー](../../../services/iam.md#condition-keys)

### 問11 {#q11}

AWS Config で非準拠のリソースを、人の操作なしに直したいです。正しい設定はどれですか。

- A. アグリゲーターを作り、非準拠のリソースを集める
- B. ルールに Automation の自動修復を関連付ける
- C. 適合パックの上限を引き上げて、ルールの数を増やす
- D. Config のプロアクティブ評価を有効にして、作成を止める

??? success "答えと解説"
    **正解: B**

    修復には Automation のドキュメントを使います。

    - A: 誤り。閲覧の機能で、修復はしない。
    - B: 正しい。
    - C: 誤り。修復の設定ではない。
    - D: 誤り。判定するだけで、止めない。

    **スキル:** [4.1.5](../domain4.md#skill-4-1-5) / **参照:** [修復](../../../services/governance.md#config-remediation)、[AWS Config](../../../services/governance.md#config)

### 問12 {#q12}

Config のルールと修復をまとめて各アカウントへ展開します。また、結果を中央で見ます。組み合わせとして正しいものはどれですか。

- A. 展開は Trusted Advisor、閲覧は Compute Optimizer
- B. 展開はアグリゲーター、閲覧は適合パック
- C. 展開は適合パック、閲覧はアグリゲーター
- D. 展開はサブスクリプションフィルター、閲覧は Athena

??? success "答えと解説"
    **正解: C**

    パックは展開、アグリゲーターは閲覧です。

    - A: 誤り。Config の機能ではない。
    - B: 誤り。逆である。
    - C: 正しい。
    - D: 誤り。Config の機能ではない。

    **スキル:** [4.1.5](../domain4.md#skill-4-1-5) / **参照:** [適合パック](../../../services/governance.md#config-conformance-packs)、[アグリゲーター](../../../services/governance.md#config-aggregators)

### 問13 {#q13}

Config の自動修復が途中で止まりました。修復の失敗が続いています。確認すべきものを選んでください。（2つ選択）

- A. アグリゲーターが同じアカウントに作られているか
- B. ルールの評価を定期から変更時に変えたか
- C. 適合パックの数がアカウントの上限の 50 個以下か
- D. `MaximumAutomaticAttempts` を超えていないか
- E. 実行ロールの権限が足りているか

??? success "答えと解説"
    **正解: D, E**

    試行の上限を超えると止まります。実行ロールの権限不足もよくある失敗です。

    - A: 誤り。閲覧の機能で、修復の失敗の原因にならない。
    - B: 誤り。評価のきっかけの話で、修復の失敗の理由にならない。
    - C: 誤り。パックの上限は修復の試行と関係がない。
    - D: 正しい。
    - E: 正しい。

    **スキル:** [4.1.5](../domain4.md#skill-4-1-5) / **参照:** [修復](../../../services/governance.md#config-remediation)

### 問14 {#q14}

「暗号化なしの EBS ボリュームの作成を禁止する」という要件を、作成の時点で止めたいです。正しい判断はどれですか。

- A. SCP か Control Tower のプロアクティブコントロールで止める
- B. Config のルールだけで止められる。検知すると作成が取り消される
- C. Trusted Advisor のチェックで止められる。指摘すると作成が取り消される
- D. GuardDuty の抑制ルールで止められる。脅威として判定される

??? success "答えと解説"
    **正解: A**

    Config は止めません。操作を止めるなら SCP か、プロアクティブコントロールです。

    - A: 正しい。
    - B: 誤り。Config は判定するだけで、止めない。
    - C: 誤り。助言するだけである。
    - D: 誤り。検出の結果を隠す機能である。

    **スキル:** [4.1.5](../domain4.md#skill-4-1-5) / **参照:** [AWS Config](../../../services/governance.md#config)、[SCP](../../../services/governance.md#scp)
