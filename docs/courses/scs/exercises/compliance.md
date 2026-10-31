# 準拠の評価の問題集

対象の解説: [Config](../../../services/governance.md#config)、[Audit Manager](../../../services/threat-detection.md#audit-manager)、[Well-Architected Tool](../../../services/cloud-foundations.md#wa-tool)

### 問1 {#q1}

暗号化されていない EBS ボリュームの作成を止めたいと、担当者は Config ルール `encrypted-volumes` を組織に配りました。その後も未暗号化のボリュームが作成され続けています。正しい評価と対応はどれですか。

- A. 評価するだけで作成は止めない。止めるなら SCP や EBS の既定の暗号化を使う
- B. Config ルールの評価の頻度が低いのが原因なので、1 時間ごとの評価に変更する
- C. Config ルールは新しいアカウントにしか効かないので、既存のアカウントのために組織のルートへ再度適用する
- D. Config のアグリゲーターを作ると、組織全体の作成が止まるようになる

??? success "答えと解説"
    **正解: A**

    Config のルールは評価するだけで、作成を止めません。操作を止めるのは SCP などです。

    - A: 正しい。
    - B: 誤り。頻度を上げても止まりません。
    - C: 誤り。新しいアカウントに限定されません。
    - D: 誤り。アグリゲーターは読み取り専用の集約です。

    **スキル:** [6.3.1](../domain6.md#skill-6-3-1) / **参照:** [Config ルール](../../../services/governance.md#config-rules)

### 問2 {#q2}

S3 のパブリックアクセスの設定が外れたバケットを、Config で検出したら自動で戻します。修復の実行が権限不足で失敗しています。担当者は Config のサービスリンクロールの変更を考えています。正しい対応はどれですか。

- A. Config のサービスリンクロールに `s3:*` を追加する
- B. Security Hub CSPM のサービスリンクルールに修復を追加する
- C. Automation の実行ロールに必要な権限を付けて、修復の設定で指定する
- D. 修復の操作を AWS Support のチケットで依頼する

??? success "答えと解説"
    **正解: C**

    修復は Systems Manager Automation で実行され、実行ロールが必要です。サービスリンクロールの権限は変更しません。

    - A: 誤り。サービスリンクロールの権限は変更しません。
    - B: 誤り。サービスリンクルールの修復は管理できません。
    - C: 正しい。
    - D: 誤り。手動の依頼では自動修復になりません。

    **スキル:** [6.3.1](../domain6.md#skill-6-3-1) / **参照:** [修復](../../../services/governance.md#config-remediation)

### 問3 {#q3}

全アカウントと全リージョンの未暗号化の EBS を、アドホックに一覧にします。また、今後も組織の準拠の状況を 1 か所で見たいと考えています。修復はそれぞれのアカウントで動いており、変更しません。適切なものはどれですか。

- A. 各アカウントで `DescribeVolumes` を実行するスクリプトを作り、結果を手で集計する
- B. アグリゲーターを作り、高度なクエリで横断して検索する
- C. アグリゲーターから修復を実行し、組織のルールの展開もアグリゲーターで行う
- D. Security Lake に EBS の設定の情報を入れ、Athena で検索する

??? success "答えと解説"
    **正解: B**

    アグリゲーターは複数のアカウントとリージョンの設定と準拠の状況を集約します。高度なクエリで横断して検索できます。

    - A: 誤り。動きますが手間がかかります。
    - B: 正しい。
    - C: 誤り。アグリゲーターは展開も修復もしません。
    - D: 誤り。Security Lake はセキュリティログの集約で、設定の検索には向きません。

    **スキル:** [6.3.1](../domain6.md#skill-6-3-1) / **参照:** [アグリゲーター](../../../services/governance.md#config-aggregators)

### 問4 {#q4}

新規の環境で、PCI DSS に対応する一連の Config ルールと修復を、組織全体へ一括で配ります。組織ルールを 1 つずつ作る方法と比較しています。また、適合パックのテンプレートの形式も確認しています。適切なものはどれですか。（2つ選択）

- A. 適合パックはルールと修復を 1 つのまとまりとして組織へ展開できる
- B. 適合パックは YAML のテンプレートで定義する
- C. 組織ルールはコンソールの画面からだけ作成できる
- D. 適合パックを作成すると、対象のリソースの違反の操作が自動で止まる
- E. 適合パックは Security Hub CSPM の標準でのみ定義できる

??? success "答えと解説"
    **正解: A, B**

    適合パックは YAML で定義し、ルールと修復を 1 つのまとまりとして組織に展開できます。

    - A: 正しい。
    - B: 正しい。
    - C: 誤り。逆で、組織ルールは API か CLI でのみ作成します。
    - D: 誤り。評価するだけで止めません。
    - E: 誤り。独自のテンプレートで定義できます。

    **スキル:** [6.3.1](../domain6.md#skill-6-3-1) / **参照:** [適合パック](../../../services/governance.md#config-conformance-packs)

### 問5 {#q5}

監査人から、AWS 自身の SOC 2 レポートの提出を求められました。別途、組織の全アカウントで HIPAA の BAA を受諾する必要もあります。使うサービスはどれですか。

- A. Audit Manager の評価レポートから SOC 2 のレポートをダウンロードする
- B. AWS Support に依頼して、SOC 2 のレポートと BAA の個別の PDF を受け取る
- C. Security Hub CSPM の標準で SOC 2 のレポートを生成する
- D. Artifact で SOC 2 のレポートをダウンロードし、組織の BAA を Artifact で受諾する

??? success "答えと解説"
    **正解: D**

    Artifact は AWS 自身の報告書と契約を扱います。組織全体で BAA を受諾できます。

    - A: 誤り。Audit Manager は自社のワークロードの証拠を収集するもので、AWS 自身の報告書ではありません。
    - B: 誤り。Artifact でオンデマンドに取得できます。
    - C: 誤り。CSPM は自社のリソースのチェックで、AWS の報告書を作りません。
    - D: 正しい。

    **スキル:** [6.3.2](../domain6.md#skill-6-3-2) / **参照:** [Artifact](../../../services/threat-detection.md#artifact)

### 問6 {#q6}

新しい会社が 2026 年 10 月に AWS を使い始めました。監査に向けて、自社のワークロードが基準を満たす証拠を集める仕組みを作ります。ある教材は Audit Manager を勧めています。この状況で最も適切な判断はどれですか。

- A. Audit Manager の評価を作成し、フレームワークごとに評価レポートを生成して、Artifact のレポートと一緒に監査人へ提出する
- B. 新規に設定できないので、Config の適合パックと履歴などで証拠をそろえる
- C. Artifact のレポートに自社の情報を追記し、監査人に提出する
- D. 証拠の収集は AWS の責任なので、作業は不要である

??? success "答えと解説"
    **正解: B**

    Audit Manager は 2026 年 4 月 30 日から新しいアカウントで設定できません。AWS の代替案は Config の適合パックです。

    - A: 誤り。新規の顧客は使えません。
    - B: 正しい。
    - C: 誤り。Artifact は AWS の資料で、自社の証明にはなりません。
    - D: 誤り。責任共有モデルでは自社のワークロードの証拠は自社で用意します。

    **スキル:** [6.3.2](../domain6.md#skill-6-3-2) / **参照:** [Audit Manager](../../../services/threat-detection.md#audit-manager)

### 問7 {#q7}

既存の Audit Manager の利用者が、PCI DSS のフレームワークで評価を作成しました。監査担当者は「Audit Manager の評価レポートをもって準拠の合格の証明になる」と考えています。証拠のデータソースも確認しています。正しい説明はどれですか。

- A. Audit Manager は準拠を自動で判定し、結果が公式の合格の証明になる
- B. Audit Manager の証拠は AWS が自動で第三者に提出する
- C. 証拠を自社の環境から集めるが、準拠の判定はしないので、評価は別途必要である
- D. Audit Manager の証拠は Artifact の SOC レポートだけから作成されるので、自社のリソースの情報を集める必要はない

??? success "答えと解説"
    **正解: C**

    Audit Manager は証拠を収集してレポートにまとめますが、準拠を判定するものではありません。

    - A: 誤り。合否を判定しません。
    - B: 誤り。そのような提出はありません。
    - C: 正しい。
    - D: 誤り。データソースは自社の環境のものです。

    **スキル:** [6.3.2](../domain6.md#skill-6-3-2) / **参照:** [Audit Manager](../../../services/threat-detection.md#audit-manager)

### 問8 {#q8}

責任共有モデルについて、監査の担当者に説明する資料を作ります。EC2 の OS のパッチの適用と、データセンターの物理的なセキュリティの証拠を、誰がどこで用意するかを整理します。正しい組み合わせはどれですか。

- A. OS のパッチの証拠は AWS が Artifact で提供し、物理的なセキュリティの証拠はデータセンターの入館記録などとして自社で用意する
- B. OS は Patch Manager の準拠レポートなどを自社で用意し、物理面は Artifact で確認する
- C. どちらの証拠も Audit Manager が自動で判定するので、用意は不要である
- D. どちらの証拠も AWS の責任なので、AWS Support に依頼して受け取る

??? success "答えと解説"
    **正解: B**

    EC2 の OS は利用者の責任で、証拠も自社で用意します。データセンターは AWS の責任で、Artifact の報告書で確認します。

    - A: 誤り。責任が逆です。
    - B: 正しい。
    - C: 誤り。判定はしません。
    - D: 誤り。OS は利用者の責任です。

    **スキル:** [6.3.2](../domain6.md#skill-6-3-2) / **参照:** [責任共有モデル](../../../services/cloud-foundations.md#shared-responsibility)

### 問9 {#q9}

アーキテクトが主要なワークロードのセキュリティの設計を見直します。質問に答えてリスクと改善計画を残し、半年後に改善の前後を比較します。修正の作業はチームが行います。適切なものはどれですか。

- A. Trusted Advisor のチェックを有効にして、自動で修正されるのを待つ
- B. Security Hub CSPM の FSBP を有効にして、質問への回答を CSPM の画面で残す
- C. Config の適合パックの結果を比較して、設計のレビューの代わりにする
- D. Well-Architected Tool でレビューし、マイルストーンで前後を比較する

??? success "答えと解説"
    **正解: D**

    Well-Architected Tool は質問形式のレビューで、リスクと改善計画を残し、マイルストーンで比較できます。指摘と記録だけで、リソースは修正しません。

    - A: 誤り。自動で修正するものではなく、質問形式でもありません。
    - B: 誤り。CSPM はコントロールのチェックです。
    - C: 誤り。設定の評価で、設計のレビューではありません。
    - D: 正しい。

    **スキル:** [6.3.3](../domain6.md#skill-6-3-3) / **参照:** [Well-Architected Tool](../../../services/cloud-foundations.md#wa-tool)

### 問10 {#q10}

組織の標準として、AWS のベストプラクティスのチェックを全アカウントで継続的に行い、スコアで全体を把握します。一部の結果が出ていないアカウントがあります。適切な手段と確認点はどれですか。

- A. CSPM の FSBP を使う。結果が出なければ Config の有効化を確認する
- B. Well-Architected Tool のレビューを毎週全アカウントで実施し、質問への回答から継続的なスコアを作る
- C. Trusted Advisor のコスト最適化のチェックだけを週次で確認する
- D. Inspector の検出結果を週次でエクスポートする

??? success "答えと解説"
    **正解: A**

    FSBP はコントロールを継続的にチェックします。多くのコントロールは Config のサービスリンクルールで動くので、Config の状態を確認します。

    - A: 正しい。
    - B: 誤り。質問形式のレビューで、継続的なチェックではありません。
    - C: 誤り。コストのチェックで、セキュリティの基準ではありません。
    - D: 誤り。脆弱性のスキャンです。

    **スキル:** [6.3.3](../domain6.md#skill-6-3-3) / **参照:** [CSPM の標準](../../../services/threat-detection.md#security-hub-cspm)

### 問11 {#q11}

ツールを選びます。「環境を自動で幅広く点検し、セキュリティ、費用、耐障害性の推奨を見る」「自社独自の質問でレビューの項目を足す」の 2 つの要望があります。それぞれの手段の組み合わせはどれですか。

- A. Resilience Hub と Config の適合パック
- B. Security Lake と Audit Manager のカスタムフレームワーク
- C. Trusted Advisor と Well-Architected Tool のカスタムレンズ
- D. Well-Architected Tool の Framework レンズと Trusted Advisor のカスタムチェック

??? success "答えと解説"
    **正解: C**

    Trusted Advisor は環境を自動で点検します。Well-Architected Tool はカスタムレンズで独自の質問を追加できます。

    - A: 誤り。Resilience Hub は回復性の評価で、幅広い点検ではありません。
    - B: 誤り。Security Lake はログの集約です。Audit Manager は証拠の収集です。
    - C: 正しい。
    - D: 誤り。役割が逆です。

    **スキル:** [6.3.3](../domain6.md#skill-6-3-3) / **参照:** [Trusted Advisor](../../../services/cloud-foundations.md#trusted-advisor)、[Well-Architected Tool](../../../services/cloud-foundations.md#wa-tool)
