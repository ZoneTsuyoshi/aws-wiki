# データ分類と検出結果の問題集

対象の解説: [選び方の比較](../../../services/threat-detection.md#choosing)、[Macie](../../../services/threat-detection.md#macie)、[GuardDuty](../../../services/threat-detection.md#guardduty)、[Security Hub](../../../services/threat-detection.md#security-hub)、[データ分類](../../../services/secrets.md#data-classification)

### 問1 {#q1}

S3 に保存された社員番号 `EMP-` で始まる 6 桁の値を見つけたいです。どの機能を使いますか。

- A. GuardDuty の抑制ルール
- B. Config の `required-tags`
- C. Inspector の拡張スキャン
- D. Macie のカスタムデータ識別子

??? success "答えと解説"
    **正解: D**

    カスタムデータ識別子で `EMP-[0-9]{6}` のような社内の形式も検出できます。

    - A: 誤り。検出結果を隠す機能である。
    - B: 誤り。タグの有無の確認である。
    - C: 誤り。脆弱性の検査である。
    - D: 正しい。

    **スキル:** [4.2.1](../domain4.md#skill-4-2-1) / **参照:** [Macie](../../../services/threat-detection.md#macie)、[識別子と許可リスト](../../../services/threat-detection.md#macie-identifiers)

### 問2 {#q2}

Macie が一部のオブジェクトを検査できません。KMS のカスタマー管理キーで暗号化されています。何を確認しますか。

- A. Macie に Lambda のリソースベースポリシーを追加したか
- B. S3 のストレージクラスを Standard へ変更したか
- C. Macie がキーを使えるか、バケットポリシーで拒否していないか
- D. CloudTrail のデータイベントを有効にしたか

??? success "答えと解説"
    **正解: C**

    KMS で暗号化したオブジェクトは、Macie がそのキーを使えることが必要です。

    - A: 誤り。検査の権限の話ではない。
    - B: 誤り。まず確認すべきは暗号化キーの権限である。
    - C: 正しい。
    - D: 誤り。Macie の検査の条件ではない。

    **スキル:** [4.2.1](../domain4.md#skill-4-2-1) / **参照:** [検出結果](../../../services/threat-detection.md#macie-findings)、[Macie](../../../services/threat-detection.md#macie)

### 問3 {#q3}

`DataClassification` のタグの値を組織で統一し、タグのないリソースも見つけたいです。組み合わせとして正しいものはどれですか。

- A. タグポリシーと Config の `required-tags`
- B. Macie の許可リストと GuardDuty の抑制ルール
- C. SCP の `aws:RequestTag` の条件と Trusted Advisor のチェック
- D. Security Hub のカスタムアクションと SNS

??? success "答えと解説"
    **正解: A**

    タグポリシーで値を統一し、`required-tags` で確認します。

    - A: 正しい。
    - B: 誤り。タグの統一には関係がない。
    - C: 誤り。作成時の条件には使えても、既存のタグのないリソースの発見には足りない。
    - D: 誤り。タグの統一には関係がない。

    **スキル:** [4.2.1](../domain4.md#skill-4-2-1) / **参照:** [タグポリシー](../../../services/governance.md#tag-policies)、[タグ戦略](../../../services/governance.md#tagging-strategy)

### 問4 {#q4}

CloudWatch Logs のログに、メールアドレスやカード番号が混ざることがあります。ログの中の機密情報を隠したいです。どの機能を使いますか。

- A. S3 へのエクスポートと Bucket Key の組み合わせ
- B. CloudWatch Logs のデータ保護ポリシー
- C. メトリクスフィルターで機密情報を数える設定
- D. Logs の保持期間を 1 日に短くする設定

??? success "答えと解説"
    **正解: B**

    データ保護ポリシーでログの機密情報をマスクできます。

    - A: 誤り。暗号化の費用の話で、マスクはしない。
    - B: 正しい。
    - C: 誤り。数えるだけで、隠さない。
    - D: 誤り。残る間は見えてしまう。

    **スキル:** [4.2.1](../domain4.md#skill-4-2-1) / **参照:** [データ保護ポリシー](../../../services/observability.md#logs-data-protection)

### 問5 {#q5}

`DataClassification=confidential` のタグが付いたリソースは、同じタグのプリンシパルだけに使わせたいです。どの方式が適切ですか。

- A. タグの条件を使う ABAC
- B. Macie で検出するだけで、アクセス制御はしない
- C. SCP で該当のサービスを全面的に拒否する
- D. リソースごとに主体の ARN を書いたポリシーを毎回更新する

??? success "答えと解説"
    **正解: A**

    タグの条件を使う ABAC でアクセスを制限できます。

    - A: 正しい。
    - B: 誤り。検出だけでは制限できない。
    - C: 誤り。使わせる人も止まる。
    - D: 誤り。運用の負担が大きい。

    **スキル:** [4.2.1](../domain4.md#skill-4-2-1) / **参照:** [条件とアクセス制御](../../../services/iam.md#conditions)、[データ分類](../../../services/secrets.md#data-classification)

### 問6 {#q6}

次の検出のサービスと対象の組み合わせとして正しいものを選んでください。（2つ選択）

- A. Inspector: EC2、ECR、Lambda の脆弱性
- B. Macie: EC2 の OS の脆弱性
- C. GuardDuty: 不審な通信や認証情報の悪用
- D. GuardDuty: 設定の基準への準拠
- E. Inspector: S3 オブジェクトの機密データ

??? success "答えと解説"
    **正解: A, C**

    GuardDuty、Inspector、Macie の違いが最もよく問われます。

    - A: 正しい。
    - B: 誤り。Macie は S3 の機密データが対象である。
    - C: 正しい。
    - D: 誤り。それは Config や Security Hub CSPM の役割である。
    - E: 誤り。それは Macie の対象である。

    **スキル:** [4.2.5](../domain4.md#skill-4-2-5) / **参照:** [選び方の比較](../../../services/threat-detection.md#choosing)

### 問7 {#q7}

GuardDuty が `CryptoCurrency:EC2/BitcoinTool.B!DNS` を検出したら、自動で EC2 を隔離したいです。どの構成が適切ですか。

- A. GuardDuty の抑制ルールで結果を隠し、次の検査を待つ
- B. Config の適合パックに隔離の手順を書き、1 日 1 回評価する
- C. EventBridge で受け、Lambda で隔離用のセキュリティグループに付け替える
- D. Trusted Advisor のチェックで同じ内容を検知して Automation を動かす

??? success "答えと解説"
    **正解: C**

    検出結果を EventBridge で受けて修復します。証拠のためスナップショットも取ります。

    - A: 誤り。抑制は結果を隠すだけで、修復しない。
    - B: 誤り。検出を受けて動く仕組みではない。
    - C: 正しい。
    - D: 誤り。このチェックは Trusted Advisor にない。

    **スキル:** [4.2.5](../domain4.md#skill-4-2-5) / **参照:** [イベント連携とエクスポート](../../../services/threat-detection.md#guardduty-events)、[EC2 の隔離](../../../services/threat-detection.md#ir-ec2-isolation)

### 問8 {#q8}

組織の全アカウントの GuardDuty の結果を受けて自動で修復します。どのアカウントにルールを作りますか。

- A. 検出が多いアカウントだけ
- B. GuardDuty の委任管理者アカウント
- C. 全メンバーアカウントのそれぞれの CloudTrail
- D. 組織の外の監査用のアカウント

??? success "答えと解説"
    **正解: B**

    管理者にはメンバーの結果も届きます。

    - A: 誤り。他のアカウントが漏れる。
    - B: 正しい。
    - C: 誤り。検出結果の受け口ではない。
    - D: 誤り。組織の外には結果が届かない。

    **スキル:** [4.2.5](../domain4.md#skill-4-2-5) / **参照:** [イベント連携とエクスポート](../../../services/threat-detection.md#guardduty-events)、[委任管理者](../../../services/governance.md#delegated-admin)

### 問9 {#q9}

検証用のスキャナーで GuardDuty の既知の誤検知が毎日出ます。修復の対象にしたくありません。どうしますか。

- A. GuardDuty をそのアカウントで無効にする
- B. 検出の更新の頻度を 6 時間のままにする
- C. CloudTrail の証跡を止める
- D. 抑制ルールを作る

??? success "答えと解説"
    **正解: D**

    既知の誤検知は抑制ルールで隠します。

    - A: 誤り。他の脅威も検出できなくなる。
    - B: 誤り。誤検知には効かない。
    - C: 誤り。他の検知に影響し、解決にならない。
    - D: 正しい。

    **スキル:** [4.2.5](../domain4.md#skill-4-2-5) / **参照:** [抑制ルールとリスト](../../../services/threat-detection.md#guardduty-suppression)、[イベント連携とエクスポート](../../../services/threat-detection.md#guardduty-events)

### 問10 {#q10}

Security Hub CSPM の検出結果の重要度を、開発環境のアカウントだけ自動で下げたいです。EventBridge のルールより先に適用したいです。どれを使いますか。

- A. 自動化ルール
- B. GuardDuty の抑制ルール
- C. カスタムアクション
- D. サブスクリプションフィルター

??? success "答えと解説"
    **正解: A**

    自動化ルールは EventBridge より先に適用されます。

    - A: 正しい。
    - B: 誤り。GuardDuty の機能である。
    - C: 誤り。人の判断の後に動かす機能である。
    - D: 誤り。ログの機能である。

    **スキル:** [4.2.5](../domain4.md#skill-4-2-5) / **参照:** [自動化](../../../services/threat-detection.md#security-hub-automation)、[製品の現在の形](../../../services/threat-detection.md#security-hub-products)

### 問11 {#q11}

人の判断の後に修復を実行したい場面と、結果を隠したい場面の説明で正しいものを選んでください。（2つ選択）

- A. カスタムアクションは検出結果を自動で全件処理する
- B. Inspector の抑制ルールは表示を隠すだけで、結果を閉じない
- C. Security Hub のカスタムアクションで人が選んで修復を起動する
- D. Inspector の抑制ルールは、脆弱性を修正して結果を閉じる
- E. GuardDuty の抑制ルールは、脅威を自動で修復する

??? success "答えと解説"
    **正解: B, C**

    修復と表示の制御を区別します。

    - A: 誤り。人が選んで実行する。
    - B: 正しい。
    - C: 正しい。
    - D: 誤り。表示を隠すだけである。
    - E: 誤り。結果を隠すだけである。

    **スキル:** [4.2.5](../domain4.md#skill-4-2-5) / **参照:** [自動化](../../../services/threat-detection.md#security-hub-automation)、[検出結果と管理](../../../services/threat-detection.md#inspector-findings)

### 問12 {#q12}

GuardDuty の結果の更新の通知が遅いので、早く受け取りたいです。既定は 6 時間です。どう変えますか。

- A. 全メンバーアカウントで 1 秒ごとに変更する
- B. 管理者のアカウントで 15 分か 1 時間へ変更する
- C. EventBridge のルールを 6 個に分ける
- D. 検出の抑制ルールを増やす

??? success "答えと解説"
    **正解: B**

    更新の通知の頻度は、管理者が変更します。

    - A: 誤り。メンバーは変更できず、1 秒の選択肢もない。
    - B: 正しい。
    - C: 誤り。通知の頻度は変わらない。
    - D: 誤り。頻度は変わらない。

    **スキル:** [4.2.5](../domain4.md#skill-4-2-5) / **参照:** [イベント連携とエクスポート](../../../services/threat-detection.md#guardduty-events)

### 問13 {#q13}

製品の名前について正しい説明はどれですか。

- A. Security Hub CSPM は 2025 年 12 月に一般提供された新しい製品で、従来の製品は Security Hub である
- B. Security Hub は GuardDuty の新しい名前で、同じ製品である
- C. Security Hub CSPM は Macie の別名である
- D. 古い教材の Security Hub は、現在の Security Hub CSPM を指す

??? success "答えと解説"
    **正解: D**

    現在は Security Hub と、従来の製品である Security Hub CSPM の 2 つがあります。

    - A: 誤り。逆である。
    - B: 誤り。別の製品である。
    - C: 誤り。別の製品である。
    - D: 正しい。

    **スキル:** [4.2.5](../domain4.md#skill-4-2-5) / **参照:** [製品の現在の形](../../../services/threat-detection.md#security-hub-products)

### 問14 {#q14}

開発中のアプリの設計とコードのレビュー、オンデマンドの侵入テストを行いたいです。どのサービスを使いますか。

- A. Amazon GuardDuty
- B. Amazon Macie
- C. AWS Security Agent
- D. AWS Trusted Advisor

??? success "答えと解説"
    **正解: C**

    組織の要件を定義すると、設計とコードのレビューで検証します。

    - A: 誤り。稼働中の環境の脅威の検出である。
    - B: 誤り。S3 の機密データの検出である。
    - C: 正しい。
    - D: 誤り。設定の助言である。

    **スキル:** [4.2.5](../domain4.md#skill-4-2-5) / **参照:** [選び方の比較](../../../services/threat-detection.md#choosing)
