# ガバナンスとコンプライアンスの問題集

対象の解説: [AI のセキュリティとコンプライアンス](../../../services/ai-fundamentals.md#security-compliance)、[統治の仕組み](../../../services/genai-apps.md#governance-controls)、[AWS Config](../../../services/governance.md#config)

### 問1 {#q1}

監査で「この回答の根拠はどの文書か」と問われました。すぐ示せるようにする仕組みはどれですか。

- A. temperature を常に 0 に固定する設定
- B. S3 のライフサイクル
- C. モデル呼び出しログの無効化
- D. Knowledge Bases の引用

??? success "答えと解説"
    **正解: D**

    回答の根拠となる文書を示すのが出典の明示です。

    - A: 誤り。根拠の提示にはなりません。
    - B: 誤り。オブジェクトの移行と削除の機能です。
    - C: 誤り。記録がなくなり、確認できません。
    - D: 正しい。

    **スキル:** [5.1.2](../domain5.md#obj-5-1-2) / **参照:** [統治の仕組み](../../../services/genai-apps.md#governance-controls)、[Knowledge Bases を呼ぶ](../../../services/ai.md#knowledge-bases)

### 問2 {#q2}

データの出所と加工の履歴を記録する考え方はどれですか。

- A. データ系譜
- B. 正則化
- C. 蒸留
- D. 文書のチャンク化

??? success "答えと解説"
    **正解: A**

    データ系譜は、データの出所と加工の履歴を記録します。

    - A: 正しい。
    - B: 誤り。過学習を抑える手法です。
    - C: 誤り。モデルを小さくする手法です。
    - D: 誤り。文書を分割する処理です。

    **スキル:** [5.1.2](../domain5.md#obj-5-1-2) / **参照:** [AI システムを守るサービス](../../../services/ai-fundamentals.md#security-services)

### 問3 {#q3}

社内のどのデータがどこにあるかを登録して、探せるようにしたいと考えています。適切な機能はどれですか。

- A. AWS Budgets
- B. AWS Artifact
- C. AWS Glue Data Catalog
- D. SageMaker Model Cards

??? success "答えと解説"
    **正解: C**

    データカタログは、どのデータがどこにあるかを登録します。

    - A: 誤り。予算を管理するサービスです。
    - B: 誤り。AWS の監査レポートを入手するサービスです。
    - C: 正しい。
    - D: 誤り。モデルの情報を記録する機能で、データの所在の登録簿ではありません。

    **スキル:** [5.1.2](../domain5.md#obj-5-1-2) / **参照:** [Data Catalog](../../../services/data-engineering.md#glue-data-catalog)

### 問4 {#q4}

「このモデルはどのデータで学習したか」という監査の質問に答えられるようにします。適切な組み合わせを選んでください。（2つ選択）

- A. AWS Artifact
- B. Amazon Inspector
- C. S3 ライフサイクル
- D. SageMaker Model Cards
- E. データカタログ

??? success "答えと解説"
    **正解: D, E**

    カタログでデータを登録し、Model Cards に学習データを記載します。

    - A: 誤り。AWS の監査レポートのサービスで、自社のモデルの情報は持ちません。
    - B: 誤り。脆弱性を調べるサービスです。
    - C: 誤り。オブジェクトの移行と削除の機能です。
    - D: 正しい。
    - E: 正しい。

    **スキル:** [5.1.2](../domain5.md#obj-5-1-2) / **参照:** [Data Catalog](../../../services/data-engineering.md#glue-data-catalog)、[Model Cards](../../../services/sagemaker.md#model-cards)

### 問5 {#q5}

監査人から、AWS のデータセンターの SOC レポートを求められました。入手先はどれですか。

- A. Amazon Inspector
- B. AWS Artifact
- C. AWS CloudTrail
- D. AWS Config

??? success "答えと解説"
    **正解: B**

    Artifact で AWS のセキュリティとコンプライアンスの文書をダウンロードできます。

    - A: 誤り。脆弱性を調べるサービスです。
    - B: 正しい。
    - C: 誤り。API の操作を記録するサービスです。
    - D: 誤り。自社のリソースの設定を評価するサービスです。

    **スキル:** [5.2.1](../domain5.md#obj-5-2-1) / **参照:** [AWS Artifact](../../../services/cloud-foundations.md#artifact)

### 問6 {#q6}

学習データの S3 バケットが暗号化されているかを、ルールで継続的に評価します。適切なサービスはどれですか。

- A. Amazon Macie
- B. AWS Artifact
- C. AWS CloudTrail
- D. AWS Config

??? success "答えと解説"
    **正解: D**

    Config はリソースの設定を記録し、ルールで評価します。

    - A: 誤り。機密データを発見するサービスです。
    - B: 誤り。AWS の監査レポートを入手するサービスです。
    - C: 誤り。API の操作を記録するサービスで、基準に合うかを判定しません。
    - D: 正しい。

    **スキル:** [5.2.1](../domain5.md#obj-5-2-1) / **参照:** [AWS Config](../../../services/governance.md#config)

### 問7 {#q7}

誰がいつ Bedrock のカスタムモデルを削除したかを調べます。適切なサービスはどれですか。

- A. AWS CloudTrail
- B. Amazon Inspector
- C. AWS Trusted Advisor
- D. AWS Config

??? success "答えと解説"
    **正解: A**

    誰が何をしたかは CloudTrail で確認します。

    - A: 正しい。
    - B: 誤り。脆弱性を調べるサービスです。
    - C: 誤り。環境を点検して推奨を出すサービスです。
    - D: 誤り。設定の状態を記録して評価する側のサービスです。

    **スキル:** [5.2.1](../domain5.md#obj-5-2-1) / **参照:** [イベントの種類](../../../services/observability.md#cloudtrail-events)、[Config と CloudTrail の違い](../../../services/governance.md#config-vs-cloudtrail)

### 問8 {#q8}

コスト、セキュリティ、耐障害性の観点で環境を点検し、推奨を受けたいと考えています。適切なサービスはどれですか。

- A. AWS CloudTrail
- B. Amazon Macie
- C. AWS Trusted Advisor
- D. AWS Artifact

??? success "答えと解説"
    **正解: C**

    Trusted Advisor はベストプラクティスに沿った推奨を出します。

    - A: 誤り。API の操作を記録するサービスです。
    - B: 誤り。機密データを発見するサービスです。
    - C: 正しい。
    - D: 誤り。AWS の監査レポートを入手するサービスです。

    **スキル:** [5.2.1](../domain5.md#obj-5-2-1) / **参照:** [Trusted Advisor](../../../services/cloud-foundations.md#trusted-advisor)

### 問9 {#q9}

AWS Artifact の文書の説明として正しいものはどれですか。

- A. 入手すれば、自社のシステムの準拠も証明される
- B. AWS 側の文書なので、自社のシステムの準拠は利用者が別に示す
- C. 自社の Bedrock のプロンプトと応答の内容を記録した監査用の文書である
- D. 自社のリソースの設定をルールで評価している

??? success "答えと解説"
    **正解: B**

    自社システムの準拠を示す文書は、利用者が別に用意します。

    - A: 誤り。文書は AWS 側のものです。
    - B: 正しい。
    - C: 誤り。それはモデル呼び出しログです。
    - D: 誤り。それは AWS Config です。

    **スキル:** [5.2.1](../domain5.md#obj-5-2-1) / **参照:** [AWS Artifact](../../../services/cloud-foundations.md#artifact)

### 問10 {#q10}

学習データの保持の要件に合わせて、一定期間が過ぎた S3 のデータを自動で削除します。適切な機能はどれですか。

- A. Amazon Macie
- B. S3 Object Lock
- C. S3 ライフサイクル
- D. AWS Artifact

??? success "答えと解説"
    **正解: C**

    データのライフサイクルや保持の戦略は、作成から削除までを管理します。

    - A: 誤り。機密データを発見するサービスです。
    - B: 誤り。保持期間中の削除を防ぐ機能で、自動で削除するものではありません。
    - C: 正しい。
    - D: 誤り。AWS の監査レポートを入手するサービスです。

    **スキル:** [5.2.2](../domain5.md#obj-5-2-2) / **参照:** [ライフサイクル](../../../services/s3.md#lifecycle)

### 問11 {#q11}

データを日本の外で処理してはいけない規定があります。どのデータガバナンスの戦略に関わりますか。

- A. プロンプトの最適化
- B. データの所在（レジデンシー）
- C. データの匿名化
- D. ラベルの品質

??? success "答えと解説"
    **正解: B**

    データを置き、処理する場所を守る戦略です。

    - A: 誤り。プロンプトの改善の話です。
    - B: 正しい。
    - C: 誤り。個人の特定を防ぐ話です。
    - D: 誤り。学習データの話です。

    **スキル:** [5.2.2](../domain5.md#obj-5-2-2) / **参照:** [モデル ID と推論プロファイル](../../../services/ai.md#model-identifiers)

### 問12 {#q12}

生成 AI アプリの呼び出し、エージェント、ナレッジベースの利用状況と品質の傾向を見続けます。適切な機能はどれですか。

- A. AWS Artifact のコンプライアンスレポートの定期的な確認
- B. SageMaker JumpStart
- C. S3 ライフサイクル
- D. CloudWatch の生成 AI オブザーバビリティ

??? success "答えと解説"
    **正解: D**

    モデルの呼び出し、エージェント、ナレッジベース、ガードレール、ツールを追えます。

    - A: 誤り。AWS の監査レポートです。
    - B: 誤り。事前学習済みモデルのハブです。
    - C: 誤り。データの移行と削除の機能です。
    - D: 正しい。

    **スキル:** [5.2.2](../domain5.md#obj-5-2-2) / **参照:** [CloudWatch の生成 AI オブザーバビリティ](../../../services/genai-apps.md#genai-observability)

### 問13 {#q13}

データガバナンスの戦略として適切なものを選んでください。（2つ選択）

- A. 学習データは一度保存したら、永久に残すと決める
- B. データの処理先のリージョンは確認しない
- C. CloudWatch Logs の保持期間を決め、必要な期間だけ残す
- D. モデル呼び出しログの機密情報は、保護せずに全社に公開する
- E. Config でポリシー違反を検知する

??? success "答えと解説"
    **正解: C, E**

    ライフサイクル、ログ、所在、監視、観察、保持の観点で考えます。

    - A: 誤り。必要な期間だけ残し、期限後に消します。
    - B: 誤り。データの所在の要件を確認します。
    - C: 正しい。
    - D: 誤り。ログには機密情報が残るので、ログ自体を保護します。
    - E: 正しい。

    **スキル:** [5.2.2](../domain5.md#obj-5-2-2) / **参照:** [データの保持](../../../services/storage.md#retention)、[AWS Config](../../../services/governance.md#config)

### 問14 {#q14}

企業が Bedrock の FM を自社の過去の問い合わせでファインチューニングして使います。Generative AI Security Scoping Matrix のどのスコープですか。

- A. スコープ 4
- B. スコープ 1
- C. スコープ 3
- D. スコープ 5

??? success "答えと解説"
    **正解: A**

    既存の FM を自社のデータで調整しています。

    - A: 正しい。
    - B: 誤り。消費者向けの公開アプリを使う形態です。
    - C: 誤り。既存の FM を調整せずにアプリを作る形態です。
    - D: 誤り。ゼロからモデルを学習する形態です。

    **スキル:** [5.2.3](../domain5.md#obj-5-2-3) / **参照:** [Generative AI Security Scoping Matrix](../../../services/ai-fundamentals.md#scoping-matrix)

### 問15 {#q15}

第三者の業務 SaaS に組み込まれた AI 機能を使います。Scoping Matrix のどのスコープですか。

- A. スコープ 1
- B. スコープ 4
- C. スコープ 3
- D. スコープ 2

??? success "答えと解説"
    **正解: D**

    スコープ 2 は企業向けのアプリの形態で、契約とデータの扱いを確認します。

    - A: 誤り。消費者向けのアプリの形態です。
    - B: 誤り。FM を自社のデータで調整する形態です。
    - C: 誤り。自社のアプリを既存の FM で作る形態です。
    - D: 正しい。

    **スキル:** [5.2.3](../domain5.md#obj-5-2-3) / **参照:** [Generative AI Security Scoping Matrix](../../../services/ai-fundamentals.md#scoping-matrix)

### 問16 {#q16}

Scoping Matrix の番号が大きくなると、どう変わりますか。

- A. 自社の制御と責任が大きくなる
- B. AWS の責任が大きくなり、自社の責任はなくなる
- C. 暗号化が不要になる
- D. 使えるモデルの数が必ず減る

??? success "答えと解説"
    **正解: A**

    スコープ 1 が最小で、スコープ 5 は全部を自社で管理します。

    - A: 正しい。
    - B: 誤り。自社の担当範囲が広がります。
    - C: 誤り。暗号化はどのスコープでも考えます。
    - D: 誤り。モデルの数を表す枠組みではありません。

    **スキル:** [5.2.3](../domain5.md#obj-5-2-3) / **参照:** [Generative AI Security Scoping Matrix](../../../services/ai-fundamentals.md#scoping-matrix)

### 問17 {#q17}

社員が会社の把握していない AI ツールを使っています。ガバナンスの手順として適切なものはどれですか。

- A. 利用者を特定して個別に処罰し、新しいツールの情報は社内に公開しない
- B. 一律に禁止だけを通達する
- C. ツールを承認済み、評価中、禁止に分類して公開し、代替を用意する
- D. 把握しないまま自由に使わせる

??? success "答えと解説"
    **正解: C**

    これはシャドー AI の問題で、方針として分類を公開し、安全な代替手段を用意します。

    - A: 誤り。安全な代替がなければ解決しません。
    - B: 誤り。禁止だけでは隠れて使われます。
    - C: 正しい。
    - D: 誤り。機密情報の流出やライセンス違反につながります。

    **スキル:** [5.2.3](../domain5.md#obj-5-2-3) / **参照:** [シャドー AI](../../../services/ai-fundamentals.md#shadow-ai)

### 問18 {#q18}

AI の用途の見直しの頻度を決めます。適切な考え方はどれですか。

- A. 影響の小さい用途ほど頻繁に見直す
- B. 影響の大きい用途ほど頻繁に見直す
- C. 問題が起きるまでは見直さず、起きた後でだけ見直す
- D. すべての用途を一度も見直さない

??? success "答えと解説"
    **正解: B**

    影響に応じて見直しの間隔を決めます。

    - A: 誤り。影響に応じた優先順位と逆です。
    - B: 正しい。
    - C: 誤り。事前に間隔を決めます。
    - D: 誤り。変化に対応できません。

    **スキル:** [5.2.3](../domain5.md#obj-5-2-3) / **参照:** [標準と規制](../../../services/ai-fundamentals.md#standards)

### 問19 {#q19}

ガバナンスの手順として適切なものを選んでください。（2つ選択）

- A. 文書化の水準をチームごとに自由に決め、揃えない
- B. 責任者を決めず、問題が起きてから話し合う
- C. 法務、セキュリティ、事業の担当者が合同で確認する
- D. ガバナンスはリリースの後に初めて検討する
- E. 開発者と利用者に定期的な研修を行う

??? success "答えと解説"
    **正解: C, E**

    レビューの方法、研修、透明性の基準を決めます。

    - A: 誤り。透明性の基準を揃えます。
    - B: 誤り。誰が何を決めるかを明確にします。
    - C: 正しい。
    - D: 誤り。企画の段階から組み込みます。
    - E: 正しい。

    **スキル:** [5.2.3](../domain5.md#obj-5-2-3) / **参照:** [役割と責任](../../../services/ai-fundamentals.md#governance-roles)
