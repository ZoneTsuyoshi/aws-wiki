# セキュリティのサービスと情報源 の問題集

対象の解説: [脅威の検出](../../../services/threat-detection.md)、[証明書と WAF](../../../services/certificates.md)、[クラウドの基礎](../../../services/cloud-foundations.md)

### 問1 {#q1}

Web アプリへの SQL インジェクションや、特定の IP からのリクエストを止めたいと考えています。最も適切なサービスはどれですか。

- A. AWS WAF
- B. AWS Firewall Manager
- C. AWS Shield
- D. Amazon Inspector

??? success "答えと解説"
    **正解: A**

    WAF はレイヤー 7 で Web アプリを守ります。

    - A: 正しい。
    - B: 誤り。保護の設定を展開するサービスで、検査そのものは行わない。
    - C: 誤り。DDoS の防御のサービス。
    - D: 誤り。脆弱性を見つけるサービスで、リクエストは止めない。

    **スキル:** [AWS のセキュリティ機能とサービス](../domain2.md#t2-4-capabilities) / **参照:** [AWS WAF](../../../services/certificates.md#waf)

### 問2 {#q2}

AWS Shield の説明として正しいものはどれですか。

- A. SQL インジェクションを検査する Web アプリのファイアウォールである
- B. EC2 の OS の脆弱性を検出するスキャナーである
- C. Standard は有料で、Advanced は追加料金なしで適用される
- D. Standard は追加料金なしで適用され、Advanced は有料である

??? success "答えと解説"
    **正解: D**

    Shield は DDoS を防御します。

    - A: 誤り。それは AWS WAF の役割。
    - B: 誤り。それは Amazon Inspector の役割。
    - C: 誤り。料金の説明が逆。
    - D: 正しい。

    **スキル:** [AWS のセキュリティ機能とサービス](../domain2.md#t2-4-capabilities) / **参照:** [Shield](../../../services/threat-detection.md#shield)

### 問3 {#q3}

50 個のアカウントがある組織で、すべての ALB に同じ WAF ルールを適用し、新しいアカウントにも広げたいと考えています。最も適切なサービスはどれですか。

- A. Amazon GuardDuty
- B. AWS Resource Access Manager
- C. AWS Firewall Manager
- D. AWS WAF だけ

??? success "答えと解説"
    **正解: C**

    Firewall Manager は保護の設定を組織全体に展開します。

    - A: 誤り。脅威を検出するサービスで、ルールを展開しない。
    - B: 誤り。リソースをアカウント間で共有するサービスで、ルールの展開は行わない。
    - C: 正しい。
    - D: 誤り。アカウントごとの設定が必要になる。

    **スキル:** [AWS のセキュリティ機能とサービス](../domain2.md#t2-4-capabilities) / **参照:** [Firewall Manager](../../../services/threat-detection.md#firewall-manager)

### 問4 {#q4}

要件とサービスの組み合わせとして正しいものはどれですか。（2つ選択）

- A. アカウントの不審な動きを検出する: Amazon GuardDuty
- B. 組織全体に WAF ルールを展開する: AWS Shield
- C. 大規模な DDoS から守る: AWS Shield
- D. Web アプリの特定のパスへの攻撃を止める: Amazon GuardDuty
- E. 不審な動きを検出する: AWS Firewall Manager

??? success "答えと解説"
    **正解: A, C**

    防御、検出、展開の役割で区別します。

    - A: 正しい。
    - B: 誤り。展開は AWS Firewall Manager。
    - C: 正しい。
    - D: 誤り。リクエストを止めるのは AWS WAF。
    - E: 誤り。検出は GuardDuty。

    **スキル:** [AWS のセキュリティ機能とサービス](../domain2.md#t2-4-capabilities) / **参照:** [GuardDuty](../../../services/threat-detection.md#guardduty)、[Shield](../../../services/threat-detection.md#shield)、[AWS WAF](../../../services/certificates.md#waf)

### 問5 {#q5}

社内で使っている他社のファイアウォール製品を、AWS でも使いたいと考えています。探して購入できる場所として最も適切なものはどれですか。

- A. AWS Security Hub
- B. AWS Marketplace
- C. AWS Artifact
- D. AWS Trusted Advisor

??? success "答えと解説"
    **正解: B**

    サードパーティのセキュリティ製品は Marketplace で探して購入できます。

    - A: 誤り。検出結果の集約とリスクの優先付けのサービス。
    - B: 正しい。
    - C: 誤り。AWS の監査レポートと契約を扱う。
    - D: 誤り。環境を点検するサービス。

    **スキル:** [Marketplace のセキュリティ製品](../domain2.md#t2-4-marketplace) / **参照:** [AWS Marketplace](../../../services/cloud-foundations.md#marketplace)

### 問6 {#q6}

AWS Marketplace でサードパーティのセキュリティ製品を購入したときの請求の説明として正しいものはどれですか。

- A. 料金はかからず、すべて AWS が負担する
- B. 請求は AWS Support のケースでだけ確認できる
- C. 料金は AWS の請求書にまとまる
- D. 製品ごとに別の請求書が必ず出品者から届く

??? success "答えと解説"
    **正解: C**

    調達や契約を個別に行わずに、AWS の請求書にまとめられます。

    - A: 誤り。製品の料金がかかる場合がある。
    - B: 誤り。請求の情報は Billing and Cost Management で確認できる。
    - C: 正しい。
    - D: 誤り。AWS の請求書に合算される。

    **スキル:** [Marketplace のセキュリティ製品](../domain2.md#t2-4-marketplace) / **参照:** [AWS Marketplace](../../../services/cloud-foundations.md#marketplace)

### 問7 {#q7}

AWS Marketplace のセキュリティ製品を検討する場面として最も適切なものはどれですか。

- A. ルートユーザーの MFA を設定したいとき
- B. AWS のサービスにない機能が必要なとき
- C. AWS 側の障害の影響を確認したいとき
- D. AWS の SOC レポートを入手したいとき

??? success "答えと解説"
    **正解: B**

    AWS のサービスにない機能や、社内の他社製品を使い続けたいときに選びます。

    - A: 誤り。IAM の設定で行う。
    - B: 正しい。
    - C: 誤り。AWS Health Dashboard で確認する。
    - D: 誤り。AWS Artifact で入手する。

    **スキル:** [Marketplace のセキュリティ製品](../domain2.md#t2-4-marketplace) / **参照:** [AWS Marketplace](../../../services/cloud-foundations.md#marketplace)、[GuardDuty](../../../services/threat-detection.md#guardduty)

### 問8 {#q8}

AWS のセキュリティの新機能や手法の解説記事を読みたいと考えています。最も適切な情報源はどれですか。

- A. AWS Security Blog
- B. AWS Health Dashboard
- C. AWS Artifact
- D. AWS Pricing Calculator

??? success "答えと解説"
    **正解: A**

    Security Blog は新機能や手法を解説します。

    - A: 正しい。
    - B: 誤り。障害や予定の影響を示すもの。
    - C: 誤り。監査レポートと契約の入手先。
    - D: 誤り。費用を見積もるツール。

    **スキル:** [セキュリティの情報源](../domain2.md#t2-4-docs) / **参照:** [サポートの情報源](../../../services/cloud-foundations.md#support-resources)

### 問9 {#q9}

セキュリティに関するよくある質問と解決方法を調べたいと考えています。最も適切な情報源はどれですか。

- A. AWS Security Blog
- B. AWS Marketplace
- C. AWS Prescriptive Guidance
- D. AWS Knowledge Center

??? success "答えと解説"
    **正解: D**

    Knowledge Center はよくある質問と解決方法をまとめています。

    - A: 誤り。新機能や手法の解説記事で、よくある質問をまとめたものではない。
    - B: 誤り。製品を購入する場所。
    - C: 誤り。移行や実装の手順をまとめた資料で、よくある質問の記事集ではない。
    - D: 正しい。

    **スキル:** [セキュリティの情報源](../domain2.md#t2-4-docs) / **参照:** [サポートの情報源](../../../services/cloud-foundations.md#support-resources)

### 問10 {#q10}

情報の種類と情報源の組み合わせとして正しいものはどれですか。（2つ選択）

- A. よくある質問と解決方法: AWS Trust & Safety
- B. 監査レポート: AWS Security Blog
- C. 新機能の解説記事: AWS Artifact
- D. セキュリティの総合的な情報: AWS Security Center
- E. 監査レポート: AWS Artifact

??? success "答えと解説"
    **正解: D, E**

    探す情報で選びます。

    - A: 誤り。Trust & Safety は悪用の報告先で、よくある質問は Knowledge Center。
    - B: 誤り。Blog は解説記事で、監査レポートの入手先は Artifact。
    - C: 誤り。解説記事は Security Blog。
    - D: 正しい。
    - E: 正しい。

    **スキル:** [セキュリティの情報源](../domain2.md#t2-4-docs) / **参照:** [サポートの情報源](../../../services/cloud-foundations.md#support-resources)、[AWS Artifact](../../../services/cloud-foundations.md#artifact)

### 問11 {#q11}

環境を点検して、ルートの MFA の未設定や、公開スナップショットを指摘してほしいと考えています。最も適切なサービスはどれですか。

- A. Amazon GuardDuty
- B. AWS Trusted Advisor
- C. AWS Shield
- D. Amazon Inspector

??? success "答えと解説"
    **正解: B**

    Trusted Advisor は環境を点検して、設定の弱点を指摘します。

    - A: 誤り。実際の不審な動きを検出するサービスで、設定の点検ではない。
    - B: 正しい。
    - C: 誤り。DDoS を防御するサービス。
    - D: 誤り。ソフトウェアの脆弱性を見つけるサービス。

    **スキル:** [問題を見つけるサービス](../domain2.md#t2-4-trusted-advisor) / **参照:** [Trusted Advisor](../../../services/cloud-foundations.md#trusted-advisor)

### 問12 {#q12}

AWS Trusted Advisor の説明として正しいものはどれですか。

- A. 自動では修正せず、使えるチェックはプランで変わる
- B. 問題を見つけると自動で修正し、使えるチェックは全利用者で同じである
- C. API の呼び出しを記録し、90 日間保存するサービスである
- D. サードパーティの製品を点検するカタログである

??? success "答えと解説"
    **正解: A**

    助言までがサービスの役割で、修正は利用者が行います。

    - A: 正しい。
    - B: 誤り。自動では修正せず、チェックはプランで変わる。
    - C: 誤り。それは CloudTrail の説明。
    - D: 誤り。Marketplace の説明に近く、点検の説明ではない。

    **スキル:** [問題を見つけるサービス](../domain2.md#t2-4-trusted-advisor) / **参照:** [Trusted Advisor](../../../services/cloud-foundations.md#trusted-advisor)

### 問13 {#q13}

見つけたいものとサービスの組み合わせとして正しいものはどれですか。

- A. 公開されたスナップショット: Amazon Macie
- B. 実際の不審な API の呼び出し: Trusted Advisor
- C. セキュリティグループで全開放されたポート: Trusted Advisor
- D. ソフトウェアの既知の脆弱性: GuardDuty

??? success "答えと解説"
    **正解: C**

    設定の弱点は Trusted Advisor、不審な動きは GuardDuty、脆弱性は Inspector です。

    - A: 誤り。Macie は S3 の機密データを検出する。設定の点検は Trusted Advisor。
    - B: 誤り。不審な動きは GuardDuty。
    - C: 正しい。
    - D: 誤り。脆弱性は Inspector。

    **スキル:** [問題を見つけるサービス](../domain2.md#t2-4-trusted-advisor) / **参照:** [Trusted Advisor](../../../services/cloud-foundations.md#trusted-advisor)、[GuardDuty](../../../services/threat-detection.md#guardduty)、[Inspector](../../../services/threat-detection.md#inspector)
