# プライバシーとコンプライアンスの問題集

対象の解説: [Macie](../../../services/threat-detection.md#macie)、[ガバナンス](../../../services/governance.md)

### 問1 {#q1}

S3 のデータレイク全体で、どこに個人情報がありそうかを毎日の検査で見通します。何を使いますか。

- A. Macie の自動検出を有効にする
- B. Macie の 1 回限りのジョブで、すべてのバケットを毎日作り直す方法
- C. Glue のクローラーで列名を読む方法
- D. Glue Data Quality のルールで全列を毎日評価する方法

??? success "答えと解説"
    **正解: A**

    サンプリングで検査し、全体を見通します。

    - A: 正しい。
    - B: 誤り。特定のバケットの詳しい検査に向きます。
    - C: 誤り。中身の機密データは検出しません。
    - D: 誤り。品質のルールの評価で、個人情報の検出ではありません。

    **スキル:** [4.5.2](../domain4.md#skill-4-5-2) / **参照:** [Macie](../../../services/threat-detection.md#macie)、[検出の方法](../../../services/threat-detection.md#macie-discovery)

### 問2 {#q2}

Macie の検出結果に基づいて、自動で該当のテーブルをアナリストから隠します。どの流れですか。

- A. 検出結果を EventBridge で受け、Lambda で IAM タグを付けて Lake Formation で制限する
- B. 検出結果を Config ルールで評価し、修復アクションでオブジェクトを削除する
- C. 検出結果を EventBridge で受け、Lambda で LF タグを付け、Lake Formation で制限する
- D. Macie の許可リストに列を登録し、Lake Formation で列を隠す

??? success "答えと解説"
    **正解: C**

    サービスを組み合わせて自動化します。

    - A: 誤り。IAM タグは LF タグと別物で、Lake Formation の権限に効きません。
    - B: 誤り。Config は検出結果を受ける仕組みではなく、削除は要件に反します。
    - C: 正しい。
    - D: 誤り。許可リストは検出の対象から除く設定で、隠す機能ではありません。

    **スキル:** [4.5.2](../domain4.md#skill-4-5-2) / **参照:** [検出結果](../../../services/threat-detection.md#macie-findings)、[LF タグ](../../../services/data-engineering.md#lake-formation-lf-tags)

### 問3 {#q3}

Macie が一部のバケットを検査できません。確認すべきものはどれですか。（2つ選択）

- A. Lake Formation の LF タグが付いているか
- B. Macie がオブジェクトの KMS キーを使えるか
- C. バケットの Intelligent-Tiering が無効か
- D. バケットポリシーが Macie を許可しているか
- E. Glue のクローラーがバケットを読んだか

??? success "答えと解説"
    **正解: B, D**

    権限と鍵を確認します。

    - A: 誤り。前提ではありません。
    - B: 正しい。復号できないと検査できません。
    - C: 誤り。原因ではありません。
    - D: 正しい。拒否されていると検査できません。
    - E: 誤り。前提ではありません。

    **スキル:** [4.5.2](../domain4.md#skill-4-5-2) / **参照:** [Macie](../../../services/threat-detection.md#macie)、[識別子と許可リスト](../../../services/threat-detection.md#macie-identifiers)

### 問4 {#q4}

規制で東京リージョンの外にデータを置けません。全アカウントで他のリージョンへの作成を防ぎます。何を使いますか。

- A. 各 IAM ロールの権限境界に、使えるリージョンの条件を 1 つずつ書いて制限する
- B. Config ルールで事前に作成を拒否する
- C. Config のアグリゲーターをリージョンごとに設定する
- D. SCP で `aws:RequestedRegion` を条件に拒否する

??? success "答えと解説"
    **正解: D**

    組織全体で拒否できます。

    - A: 誤り。ロールごとの設定で、全アカウントに強制できません。
    - B: 誤り。検出の仕組みで、事前の拒否はしません。
    - C: 誤り。設定の情報の集約で、作成は防げません。
    - D: 正しい。

    **スキル:** [4.5.3](../domain4.md#skill-4-5-3) / **参照:** [SCP](../../../services/governance.md#scp)、[主なグローバル条件キー](../../../services/iam.md#condition-keys)

### 問5 {#q5}

`aws:RequestedRegion` で他のリージョンを拒否する SCP を適用すると、IAM や CloudFront の操作に支障が出ました。また管理アカウントでは効いていません。正しい理解はどれですか。

- A. サービスリンクロールの操作を SCP で制限すれば、管理アカウントも制限される
- B. グローバルサービスは `NotAction` で除き、管理アカウントは SCP の対象外である
- C. SCP を削除して IAM ポリシーで置き換えると、全組織に効く
- D. グローバルサービスは `Allow` で別途追加し、管理アカウントにも必ず効く

??? success "答えと解説"
    **正解: B**

    SCP の範囲を押さえます。

    - A: 誤り。どちらも制限できません。
    - B: 正しい。
    - C: 誤り。組織全体の制限になりません。
    - D: 誤り。`Deny` の条件の問題で、管理アカウントには効きません。

    **スキル:** [4.5.3](../domain4.md#skill-4-5-3) / **参照:** [SCP](../../../services/governance.md#scp)

### 問6 {#q6}

許可しないリージョンへのバックアップと複製を防ぐ確認で正しいものはどれですか。（2つ選択）

- A. AWS Backup のコピールールのコピー先を確認する
- B. S3 ライフサイクルのルールの移行先のストレージクラスを確認する
- C. 同じリージョンのリードレプリカの AZ を確認する
- D. S3 レプリケーションのルールの送信先を確認する
- E. KMS キーのローテーションの周期を確認する

??? success "答えと解説"
    **正解: A, D**

    複製の設定も確認します。

    - A: 正しい。コピー先のリージョンを決めます。
    - B: 誤り。同じバケットの中の移行で、リージョンは変わりません。
    - C: 誤り。リージョンをまたぎません。
    - D: 正しい。許可するリージョンだけにします。
    - E: 誤り。鍵素材の更新で、データの場所は変わりません。

    **スキル:** [4.5.3](../domain4.md#skill-4-5-3) / **参照:** [リージョン間コピー](../../../services/resilience.md#backup-cross-region)、[レプリケーション](../../../services/s3.md#replication)

### 問7 {#q7}

S3 バケットの設定がいつどう変わったかの履歴を確認し、基準に合うかを評価します。どのサービスですか。

- A. AWS Config の記録とルール
- B. CloudTrail の Insights イベント
- C. Amazon Macie
- D. AWS Trusted Advisor

??? success "答えと解説"
    **正解: A**

    設定の状態を記録し、ルールで評価します。

    - A: 正しい。
    - B: 誤り。API の呼び出し率の異常の検出です。
    - C: 誤り。機密データの検出です。
    - D: 誤り。推奨事項の確認で、設定の履歴は持ちません。

    **スキル:** [4.5.4](../domain4.md#skill-4-5-4) / **参照:** [AWS Config](../../../services/governance.md#config)

### 問8 {#q8}

S3 バケットが公開になったら検出して、自動で元に戻します。どの組み合わせですか。

- A. CloudTrail のイベント履歴と手動の確認
- B. Macie の自動検出と検出結果の確認
- C. IAM Access Analyzer の検出と手動の確認
- D. Config ルールと自動修復のアクション

??? success "答えと解説"
    **正解: D**

    検出と修復を組み合わせます。

    - A: 誤り。自動になりません。
    - B: 誤り。機密データの検出で、バケットの公開の修復はしません。
    - C: 誤り。検出はできますが、自動で元に戻しません。
    - D: 正しい。

    **スキル:** [4.5.4](../domain4.md#skill-4-5-4) / **参照:** [修復](../../../services/governance.md#config-remediation)、[Config ルール](../../../services/governance.md#config-rules)

### 問9 {#q9}

複数のアカウントの設定の変更を集約し、誰が変えたかまで調べます。正しい組み合わせはどれですか。

- A. Logs Insights で設定の履歴を集約し、メトリクスで誰が変えたかを調べる
- B. Config のアグリゲーターで集約し、タイムラインから CloudTrail のイベントへたどる
- C. Config のアグリゲーターで集約すれば、Config の記録だけで変更者が分かる
- D. Macie で設定の変更を集約し、検出結果から変更者を調べる

??? success "答えと解説"
    **正解: B**

    「何が」は Config、「誰が」は CloudTrail です。

    - A: 誤り。設定の履歴を持つのは Config です。
    - B: 正しい。
    - C: 誤り。Config は「何が」で、「誰が」は CloudTrail で確認します。
    - D: 誤り。機密データの検出のサービスです。

    **スキル:** [4.5.4](../domain4.md#skill-4-5-4) / **参照:** [アグリゲーター](../../../services/governance.md#config-aggregators)、[Config と CloudTrail の違い](../../../services/governance.md#config-vs-cloudtrail)

### 問10 {#q10}

データを日本に留める要件です。データ主権の点で、有効にする前に確認すべき機能はどれですか。（2つ選択）

- A. DynamoDB のグローバルテーブル
- B. 同じリージョンの CloudWatch のアラーム
- C. 同じリージョンの Athena のパーティション射影
- D. 同じリージョンの S3 のライフサイクルの移行
- E. S3 のクロスリージョンレプリケーション

??? success "答えと解説"
    **正解: A, E**

    複製先の確認が必要です。

    - A: 正しい。他のリージョンへ複製します。
    - B: 誤り。リージョンをまたぎません。
    - C: 誤り。リージョンをまたぎません。
    - D: 誤り。リージョンをまたぎません。
    - E: 正しい。他のリージョンへ複製します。

    **スキル:** [4.5.5](../domain4.md#skill-4-5-5) / **参照:** [リージョン](../../../services/cloud-foundations.md#regions)、[グローバルテーブル](../../../services/dynamodb.md#global-tables)

### 問11 {#q11}

Bedrock で推論プロファイルを使います。データ主権の点で注意することはどれですか。

- A. 推論プロファイルは常に呼び出し元の AZ の中で処理される
- B. 推論プロファイルは IAM の認証を使えないので、別の認証が要る
- C. 他のリージョンで処理されることがあるので、法律の要件を確認する
- D. 推論プロファイルを使うと、データは S3 に必ず保存される

??? success "答えと解説"
    **正解: C**

    保存場所だけでなく処理の場所も管理します。

    - A: 誤り。他のリージョンで処理されることがあります。
    - B: 誤り。認証の話ではありません。
    - C: 正しい。
    - D: 誤り。保存の話ではありません。

    **スキル:** [4.5.5](../domain4.md#skill-4-5-5) / **参照:** [モデル ID と推論プロファイル](../../../services/ai.md#model-identifiers)

### 問12 {#q12}

監査人に、AWS の準拠のレポートを提出します。どこで入手しますか。

- A. AWS Config のアグリゲーター
- B. AWS Artifact のダウンロード
- C. AWS Trusted Advisor のチェック
- D. Amazon Macie のレポート

??? success "答えと解説"
    **正解: B**

    監査レポートは AWS Artifact で入手します。

    - A: 誤り。自分のリソースの設定の情報です。
    - B: 正しい。
    - C: 誤り。推奨事項の確認です。
    - D: 誤り。機密データの検出の結果です。

    **スキル:** [4.5.5](../domain4.md#skill-4-5-5) / **参照:** [AWS Artifact](../../../services/threat-detection.md#artifact)
