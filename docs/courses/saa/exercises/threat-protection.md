# 脅威の検出と防御の問題集

対象の解説: [脅威の検出](../../../services/threat-detection.md)、[証明書と WAF](../../../services/certificates.md)

### 問1 {#q1}

多数のバケットのうち、個人情報がどのバケットに入っているかを調べます。どれを使いますか。

- A. Inspector の脆弱性スキャンを全バケットに実行する
- B. GuardDuty の脅威検出を S3 保護つきで有効にする
- C. Detective のグラフ
- D. Macie の機密データ検出ジョブ

??? success "答えと解説"
    **正解: D**

    Macie は S3 の機密データを発見して分類します。

    - A: 誤り。EC2、ECR、Lambda の脆弱性が対象。
    - B: 誤り。脅威の検出で、中身の機密データは分類しない。
    - C: 誤り。検出結果の原因の調査に使う。
    - D: 正しい。

    **スキル:** [セキュリティサービス](../domain1.md#t1-2-security-services) / **参照:** [Macie](../../../services/threat-detection.md#macie)

### 問2 {#q2}

EC2 インスタンスが暗号通貨のマイニングに使われている疑いや、不審な API 呼び出しを、エージェントの導入なしで継続して検出します。どれを使いますか。

- A. Macie の機密データ検出ジョブをスケジュールで実行する
- B. GuardDuty の脅威検出の有効化
- C. Inspector の CVE スキャンをインスタンスごとに実行する
- D. Config のマネージドルール

??? success "答えと解説"
    **正解: B**

    GuardDuty は CloudTrail、VPC フローログ、DNS ログなどから脅威を検出します。

    - A: 誤り。S3 の機密データが対象。
    - B: 正しい。
    - C: 誤り。脆弱性の評価で、活動の検出はしない。
    - D: 誤り。設定の評価で、脅威は検出しない。

    **スキル:** [セキュリティサービス](../domain1.md#t1-2-security-services) / **参照:** [GuardDuty](../../../services/threat-detection.md#guardduty)

### 問3 {#q3}

ECR のコンテナイメージと EC2 のパッケージに、既知の CVE がないかを継続して評価します。どれを使いますか。

- A. Macie の自動検出
- B. GuardDuty の Runtime Monitoring をコンテナに有効にする
- C. Inspector の継続スキャン
- D. Firewall Manager のポリシーを組織に展開する

??? success "答えと解説"
    **正解: C**

    Inspector は EC2、ECR、Lambda の脆弱性を評価します。

    - A: 誤り。対象は S3 の機密データ。
    - B: 誤り。実行時の脅威の検出で、CVE の評価ではない。
    - C: 正しい。
    - D: 誤り。ルールの展開のサービス。

    **スキル:** [セキュリティサービス](../domain1.md#t1-2-security-services) / **参照:** [Inspector](../../../services/threat-detection.md#inspector)

### 問4 {#q4}

GuardDuty の検出結果について、関連するリソースと時系列をたどって根本原因を調べます。どれが適切ですか。

- A. Detective の行動グラフ
- B. Inspector の一覧
- C. Trusted Advisor のセキュリティのチェックを確認する
- D. Security Hub の基準のスコアを確認して、低いものから修正する

??? success "答えと解説"
    **正解: A**

    Detective はログからグラフを作り、検出の後の調査を助けます。

    - A: 正しい。
    - B: 誤り。脆弱性の評価で、調査の機能ではない。
    - C: 誤り。点検で、インシデントの調査ではない。
    - D: 誤り。集約と基準の評価で、原因の分析ではない。

    **スキル:** [セキュリティサービス](../domain1.md#t1-2-security-services) / **参照:** [Detective](../../../services/threat-detection.md#detective)

### 問5 {#q5}

組織の全アカウントの GuardDuty、Inspector、Macie の検出結果を 1 か所に集め、優先度を付けます。また、複数アカウントの ALB に同じ WAF のルールを一括で適用します。組み合わせとして正しいものはどれですか。

- A. Security Hub と Firewall Manager
- B. CloudTrail Lake と AWS Config の組み合わせで集約する
- C. Detective と Service Catalog を組み合わせて配布する
- D. Control Tower と RAM

??? success "答えと解説"
    **正解: A**

    Security Hub は検出結果の集約、Firewall Manager は WAF や SG などのルールの組織への展開です。

    - A: 正しい。
    - B: 誤り。検出結果の集約と WAF の展開の役割ではない。
    - C: 誤り。Detective は調査、Service Catalog は製品の配布。
    - D: 誤り。環境の構築とリソースの共有で、役割が違う。

    **スキル:** [セキュリティサービス](../domain1.md#t1-2-security-services) / **参照:** [Security Hub](../../../services/threat-detection.md#security-hub)、[Firewall Manager](../../../services/threat-detection.md#firewall-manager)

### 問6 {#q6}

ALB の後ろの Web アプリに SQL インジェクションの試行が続いています。アプリの改修まで、最小の手間で防ぎます。どれが適切ですか。

- A. NACL で HTTP のボディにある SQL の文字列を拒否する
- B. ALB に WAF を関連付け、SQL 用のマネージドルールを使う
- C. SG でアプリのポートを攻撃元の国の IP について拒否する
- D. Shield Advanced のサブスクリプションを追加する

??? success "答えと解説"
    **正解: B**

    WAF はリクエストの中身を検査します。マネージドルールならルールを自分で書かずに済みます。

    - A: 誤り。NACL は L3、L4 で、中身を見られない。
    - B: 正しい。
    - C: 誤り。SG に拒否ルールはなく、中身も見ない。
    - D: 誤り。主に量の攻撃への対策で、リクエストの中身は見ない。

    **スキル:** [外部の脅威](../domain1.md#t1-2-threats) / **参照:** [AWS WAF](../../../services/certificates.md#waf)

### 問7 {#q7}

特定の IP から短時間に大量のリクエストが来る、ログイン画面への攻撃を自動で抑えます。CloudFront の前段で対応します。何を使いますか。

- A. CloudFront の署名付き URL を全利用者に事前に配布する
- B. Shield Standard の既定の保護に任せ、追加の設定はしない
- C. Route 53 のヘルスチェックで攻撃元の IP を切り離す
- D. WAF のレートベースルール

??? success "答えと解説"
    **正解: D**

    レートベースルールは、一定時間のリクエスト数がしきい値を超えた送信元を制限します。

    - A: 誤り。コンテンツの限定配信で、レートの制御ではない。
    - B: 誤り。L3、L4 の保護で、HTTP のログイン試行は判定しない。
    - C: 誤り。DNS の振り分けで、攻撃元を制限しない。
    - D: 正しい。

    **スキル:** [外部の脅威](../domain1.md#t1-2-threats) / **参照:** [レートベースルール](../../../services/certificates.md#rate-based-rules)

### 問8 {#q8}

重要な公開サイトで、大規模な DDoS に備えます。専門チームの支援と、攻撃によるスケーリング費用の保護が要件です。どれを選びますか。

- A. GuardDuty の拡張保護プランを追加で有効にする
- B. Shield Standard をコンソールで有効にして保護対象を登録する
- C. Shield Advanced
- D. Network Firewall を ALB の前段のサブネットに配置する

??? success "答えと解説"
    **正解: C**

    Shield Advanced は専門チームの支援と費用の保護を提供します。

    - A: 誤り。脅威の検出で、DDoS の防御ではない。
    - B: 誤り。追加料金なしで自動適用されるが、支援や費用の保護はない。
    - C: 正しい。
    - D: 誤り。VPC の通信の検査で、この支援はない。

    **スキル:** [外部の脅威](../domain1.md#t1-2-threats) / **参照:** [Shield](../../../services/threat-detection.md#shield)

### 問9 {#q9}

Shield Advanced で保護できる対象の組み合わせとして正しいものはどれですか。

- A. S3 バケットと DynamoDB テーブルと Lambda 関数
- B. VPC エンドポイント、NAT ゲートウェイ、RDS インスタンス、EFS
- C. CloudFront、Route 53、Global Accelerator、ALB、Elastic IP
- D. IAM ロールと KMS キーと Secrets Manager のシークレット

??? success "答えと解説"
    **正解: C**

    EC2 と NLB は Elastic IP を関連付けて保護します。

    - A: 誤り。いずれも直接の保護対象ではない。
    - B: 誤り。保護対象のリストにない。
    - C: 正しい。
    - D: 誤り。ネットワークの資源ではない。

    **スキル:** [外部の脅威](../domain1.md#t1-2-threats) / **参照:** [Shield](../../../services/threat-detection.md#shield)

### 問10 {#q10}

VPC の全通信を、ステートフルなルールと侵入防止のシグネチャで検査します。ファイアウォールの機器は管理したくありません。どれを選びますか。

- A. Network Firewall
- B. WAF を各インスタンスの ENI に関連付けて全ポートを検査する
- C. GuardDuty の検出結果を受けて手動で NACL を更新する
- D. SG のアウトバウンドに拒否ルールを追加して検査する

??? success "答えと解説"
    **正解: A**

    Network Firewall は VPC の専用サブネットに置くマネージドファイアウォールです。

    - A: 正しい。
    - B: 誤り。WAF は HTTP の保護で、ENI には付けられない。
    - C: 誤り。検出で、インラインの検査ではない。
    - D: 誤り。SG に拒否と検査の機能はない。

    **スキル:** [外部の脅威](../domain1.md#t1-2-threats) / **参照:** [Network Firewall](../../../services/threat-detection.md#network-firewall)

### 問11 {#q11}

VPC のワークロードが悪意のあるドメインを名前解決することを止めます。どれを使いますか。

- A. CloudFront の地理的制限を有効にして拒否する
- B. Route 53 Resolver の DNS Firewall
- C. プライベートホストゾーンに全ドメインを手で登録して管理する
- D. Route 53 のレイテンシールーティングで別のレコードを返す

??? success "答えと解説"
    **正解: B**

    DNS Firewall は VPC からの DNS クエリを、ドメインのリストで許可または遮断します。

    - A: 誤り。配信の国の制限で、VPC の DNS とは関係ない。
    - B: 正しい。
    - C: 誤り。管理できず、遮断の機能でもない。
    - D: 誤り。振り分けの設定で、ドメインの遮断ではない。

    **スキル:** [外部の脅威](../domain1.md#t1-2-threats) / **参照:** [DNS Firewall](../../../services/network-connectivity.md#dns-firewall)
