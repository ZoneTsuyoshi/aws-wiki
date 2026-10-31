# コンプライアンスとガバナンス の問題集

対象の解説: [クラウドの基礎](../../../services/cloud-foundations.md)、[ガバナンス](../../../services/governance.md)、[AWS KMS](../../../services/kms.md)、[オブザーバビリティ](../../../services/observability.md)

### 問1 {#q1}

複数のアカウントで使える操作を組織全体で制限したいと考えています。SCP を使うサービスはどれですか。

- A. AWS Artifact
- B. AWS Config
- C. AWS Organizations
- D. AWS Resource Access Manager

??? success "答えと解説"
    **正解: C**

    Organizations はアカウントをまとめ、SCP で使える操作を制限できます。

    - A: 誤り。AWS の監査レポートを入手するサービス。
    - B: 誤り。設定の記録と評価を行うサービスで、操作を制限しない。
    - C: 正しい。
    - D: 誤り。リソースをアカウント間で共有するサービス。

    **スキル:** [コンプライアンスとガバナンスの考え方](../domain2.md#t2-2-concepts) / **参照:** [AWS Organizations](../../../services/governance.md#organizations)

### 問2 {#q2}

マルチアカウントの基盤をベストプラクティスに沿った標準の形で用意したいと考えています。最も適切なサービスはどれですか。

- A. AWS Control Tower
- B. AWS License Manager
- C. AWS Resource Access Manager
- D. AWS Service Catalog

??? success "答えと解説"
    **正解: A**

    Control Tower は、マルチアカウントの基盤を標準の形で用意します。

    - A: 正しい。
    - B: 誤り。ライセンスを管理するサービス。
    - C: 誤り。リソースを共有するサービスで、基盤は用意しない。
    - D: 誤り。承認済みの構成を利用者に提供するサービス。

    **スキル:** [コンプライアンスとガバナンスの考え方](../domain2.md#t2-2-concepts) / **参照:** [AWS Control Tower](../../../services/governance.md#control-tower)、[AWS Service Catalog](../../../services/governance.md#service-catalog)

### 問3 {#q3}

社内の利用者に、承認済みの構成だけを選んで作らせたいと考えています。最も適切なサービスはどれですか。

- A. AWS Marketplace
- B. AWS Service Catalog
- C. AWS Systems Manager
- D. AWS Control Tower

??? success "答えと解説"
    **正解: B**

    Service Catalog で、承認済みの構成を利用者に提供できます。

    - A: 誤り。サードパーティの製品を探して購入するカタログ。
    - B: 正しい。
    - C: 誤り。サーバーの運用を行うサービス。
    - D: 誤り。マルチアカウントの基盤を用意するサービス。

    **スキル:** [コンプライアンスとガバナンスの考え方](../domain2.md#t2-2-concepts) / **参照:** [AWS Service Catalog](../../../services/governance.md#service-catalog)

### 問4 {#q4}

コンプライアンスとガバナンスの説明として正しいものはどれですか。（2つ選択）

- A. コンプライアンスの資料は、利用者のシステムの分まで AWS が作る
- B. AWS の認証があれば、利用者のシステムも自動で基準を満たす
- C. ガバナンスは AWS だけが行うもので、利用者は関わらない
- D. ガバナンスは組織のルールどおりに使われるようにする仕組み
- E. コンプライアンスは法律や業界の基準を満たしていること

??? success "答えと解説"
    **正解: D, E**

    AWS は自社のインフラについて監査を受け、利用者のシステムが基準を満たすことは利用者が示します。

    - A: 誤り。AWS の資料は自社のインフラについてのもの。
    - B: 誤り。利用者のシステムの準拠は、利用者が示す。
    - C: 誤り。組織のルールを決めるのは利用者。
    - D: 正しい。
    - E: 正しい。

    **スキル:** [コンプライアンスとガバナンスの考え方](../domain2.md#t2-2-concepts) / **参照:** [責任共有モデル](../../../services/cloud-foundations.md#shared-responsibility)、[AWS Organizations](../../../services/governance.md#organizations)

### 問5 {#q5}

保存時の暗号化で防げるものはどれですか。

- A. 権限を持つユーザーによる誤った操作
- B. アプリへの大量のリクエストによる停止
- C. 通信の途中でのデータの盗聴
- D. 媒体やバックアップからの漏えい

??? success "答えと解説"
    **正解: D**

    保存時の暗号化は、ディスクやストレージ上のデータを守ります。

    - A: 誤り。暗号化では防げない。権限の設計の話。
    - B: 誤り。DDoS の話で、暗号化では防げない。
    - C: 誤り。これは転送時の暗号化で防ぐ。
    - D: 正しい。

    **スキル:** [暗号化の利点と選択肢](../domain2.md#t2-2-encryption) / **参照:** [保存時と転送時の暗号化](../../../services/kms.md#at-rest-in-transit)

### 問6 {#q6}

ブラウザーと ALB の間を流れるデータの盗聴を防ぎたいと考えています。使う仕組みとして最も適切なものはどれですか。

- A. TLS（HTTPS）
- B. S3 のサーバー側暗号化
- C. AWS CloudTrail の証跡
- D. EBS の暗号化

??? success "答えと解説"
    **正解: A**

    転送時の暗号化には TLS を使います。

    - A: 正しい。
    - B: 誤り。保存時の暗号化。
    - C: 誤り。API の呼び出しの記録で、暗号化はしない。
    - D: 誤り。保存時の暗号化で、流れるデータは守らない。

    **スキル:** [暗号化の利点と選択肢](../domain2.md#t2-2-encryption) / **参照:** [保存時と転送時の暗号化](../../../services/kms.md#at-rest-in-transit)

### 問7 {#q7}

Web サイトの TLS 証明書を発行して、更新を任せたいと考えています。最も適切なサービスはどれですか。

- A. AWS CloudHSM
- B. AWS Secrets Manager
- C. AWS KMS
- D. AWS Certificate Manager

??? success "答えと解説"
    **正解: D**

    TLS 証明書の発行と更新は ACM です。

    - A: 誤り。専用のハードウェアで鍵を保護するサービス。
    - B: 誤り。データベースの資格情報などを保管するサービス。
    - C: 誤り。暗号鍵を管理するサービスで、TLS 証明書は発行しない。
    - D: 正しい。

    **スキル:** [暗号化の利点と選択肢](../domain2.md#t2-2-encryption) / **参照:** [AWS Certificate Manager](../../../services/certificates.md#acm)

### 問8 {#q8}

規制の要件で、専用のハードウェアで暗号鍵を保護する必要があります。最も適切なサービスはどれですか。

- A. AWS Certificate Manager
- B. AWS CloudHSM
- C. Amazon Macie
- D. AWS KMS

??? success "答えと解説"
    **正解: B**

    専用のハードウェアで鍵を保護するなら CloudHSM です。

    - A: 誤り。TLS 証明書のサービス。
    - B: 正しい。
    - C: 誤り。機密データを検出するサービス。
    - D: 誤り。共有の管理サービスで、専用のハードウェアを割り当てるものではない。

    **スキル:** [暗号化の利点と選択肢](../domain2.md#t2-2-encryption) / **参照:** [KMS との比較](../../../services/identity-directory.md#cloudhsm-vs-kms)

### 問9 {#q9}

誰がいつどの API を呼んだかを調べたいと考えています。確認するものはどれですか。

- A. ALB のアクセスログ
- B. VPC フローログ
- C. AWS CloudTrail
- D. CloudWatch Logs

??? success "答えと解説"
    **正解: C**

    API の呼び出しは CloudTrail に記録されます。

    - A: 誤り。HTTP リクエストの記録で、AWS の API の呼び出しの記録ではない。
    - B: 誤り。IP 通信の有無と許可、拒否を記録するもの。
    - C: 正しい。
    - D: 誤り。アプリケーションのログなどを保管するもの。

    **スキル:** [セキュリティのログを取る場所](../domain2.md#t2-2-logs) / **参照:** [どのログを見るか](../../../services/threat-detection.md#log-sources)、[証跡とイベント履歴](../../../services/observability.md#cloudtrail-trails)

### 問10 {#q10}

ある IP アドレスから EC2 への通信が許可されたか拒否されたかを調べたいと考えています。確認するものはどれですか。

- A. AWS Config
- B. AWS Cost and Usage Report
- C. VPC フローログ
- D. AWS CloudTrail

??? success "答えと解説"
    **正解: C**

    IP 通信の有無と許可、拒否は VPC フローログで確認します。

    - A: 誤り。リソースの設定の変化の記録。
    - B: 誤り。費用と使用量のデータ。
    - C: 正しい。
    - D: 誤り。AWS の API の呼び出しの記録で、IP 通信は記録しない。

    **スキル:** [セキュリティのログを取る場所](../domain2.md#t2-2-logs) / **参照:** [どのログを見るか](../../../services/threat-detection.md#log-sources)

### 問11 {#q11}

CloudTrail のイベント履歴で管理イベントを確認できる期間と、長く残す方法の組み合わせはどれですか。

- A. 90 日間。長く残すなら証跡を作って S3 に保存する
- B. 7 日間。長く残すならサポートケースで依頼する
- C. 無期限。追加の設定はいらない
- D. 1 年間。長く残すなら AWS Backup のプランに追加する

??? success "答えと解説"
    **正解: A**

    イベント履歴は過去 90 日です。継続的な記録には証跡などを作ります。

    - A: 正しい。
    - B: 誤り。イベント履歴は 90 日間で、サポートケースは不要。
    - C: 誤り。イベント履歴は過去 90 日に限られる。
    - D: 誤り。イベント履歴は 90 日間で、保存には証跡を使う。

    **スキル:** [セキュリティのログを取る場所](../domain2.md#t2-2-logs) / **参照:** [証跡とイベント履歴](../../../services/observability.md#cloudtrail-trails)

### 問12 {#q12}

調べたい内容と、確認するログの組み合わせとして正しいものはどれですか。（2つ選択）

- A. 設定がいつ変わったか: VPC フローログ
- B. 誰が API を呼んだか: CloudWatch Logs のアプリのログ
- C. IP 通信の許可と拒否: AWS Config
- D. アプリが出力したエラーの内容: CloudWatch Logs
- E. Web アプリへの HTTP リクエストの記録: ALB のアクセスログ

??? success "答えと解説"
    **正解: D, E**

    知りたいことでログを選びます。

    - A: 誤り。設定の変化は AWS Config で確認する。
    - B: 誤り。API の呼び出しは CloudTrail で確認する。
    - C: 誤り。IP 通信は VPC フローログで確認する。
    - D: 正しい。
    - E: 正しい。リクエストの行や応答コードなどを記録する。本文は項目にない。

    **スキル:** [セキュリティのログを取る場所](../domain2.md#t2-2-logs) / **参照:** [CloudWatch Logs](../../../services/observability.md#cloudwatch-logs)、[どのログを見るか](../../../services/threat-detection.md#log-sources)

### 問13 {#q13}

監査人が、AWS の SOC レポートの提出を求めています。入手先として最も適切なものはどれですか。

- A. AWS CloudTrail
- B. AWS Config
- C. AWS Trusted Advisor
- D. AWS Artifact

??? success "答えと解説"
    **正解: D**

    Artifact で、AWS の監査レポートや認証をダウンロードできます。

    - A: 誤り。API の呼び出しの記録。
    - B: 誤り。自分のリソースの設定を監査するもので、AWS 自身のレポートは得られない。
    - C: 誤り。環境を点検するサービス。
    - D: 正しい。

    **スキル:** [コンプライアンス情報の入手先](../domain2.md#t2-2-compliance-info) / **参照:** [AWS Artifact](../../../services/cloud-foundations.md#artifact)

### 問14 {#q14}

AWS Artifact で入手や確認ができるものはどれですか。（2つ選択）

- A. ISO や PCI の AWS の認証やレポート
- B. AWS との契約
- C. 自社のアプリの脆弱性のスキャン結果
- D. サーバーの CPU 使用率のグラフ
- E. 自社のシステムが準拠していることの証明書

??? success "答えと解説"
    **正解: A, B**

    Artifact はレポートと契約を扱います。

    - A: 正しい。
    - B: 正しい。
    - C: 誤り。Inspector の役割。
    - D: 誤り。CloudWatch の役割。
    - E: 誤り。自社のシステムの証明は利用者が用意する。

    **スキル:** [コンプライアンス情報の入手先](../domain2.md#t2-2-compliance-info) / **参照:** [AWS Artifact](../../../services/cloud-foundations.md#artifact)

### 問15 {#q15}

自社のシステムが PCI DSS に準拠していることを取引先に示す必要があります。正しい考え方はどれですか。

- A. AWS を使っていれば、PCI DSS の要件はすべて自動で満たされる
- B. AWS の資料が示すのは基盤の分だけなので、自社のシステムの部分は自社で示す
- C. Artifact のレポートだけで、自社のシステムの準拠も証明される
- D. AWS Support に依頼すれば、自社のシステムの監査報告書を作ってくれる

??? success "答えと解説"
    **正解: B**

    自社のシステムの準拠を示す文書は、利用者が別に用意します。

    - A: 誤り。利用者の担当部分が残る。
    - B: 正しい。
    - C: 誤り。AWS のレポートは AWS のインフラについてのもの。
    - D: 誤り。利用者のシステムの証明は利用者が行う。

    **スキル:** [コンプライアンス情報の入手先](../domain2.md#t2-2-compliance-info) / **参照:** [AWS Artifact](../../../services/cloud-foundations.md#artifact)、[責任共有モデル](../../../services/cloud-foundations.md#shared-responsibility)

### 問16 {#q16}

ある国の規制で、個人データを国内に保管する必要があります。AWS で最初に検討することはどれですか。

- A. すべてのデータを CloudFront にキャッシュする
- B. 複数の AZ に配置するだけで要件を満たす
- C. AWS Support に対応を任せる
- D. その国にあるリージョンを選んでデータを置く

??? success "答えと解説"
    **正解: D**

    データの所在地の規制には、該当する国のリージョンを選びます。

    - A: 誤り。エッジのキャッシュは保管先の規制の解決にならない。
    - B: 誤り。AZ は 1 つのリージョンの中の話で、リージョンの選択が先。
    - C: 誤り。規制への対応は利用者の責任。
    - D: 正しい。

    **スキル:** [地域や業界で異なる要件](../domain2.md#t2-2-regions-industries) / **参照:** [リージョン](../../../services/cloud-foundations.md#regions)、[AWS Artifact](../../../services/cloud-foundations.md#artifact)

### 問17 {#q17}

クレジットカードのデータを扱う会社が、AWS で業界の基準に対応します。正しい進め方はどれですか。

- A. AWS の認証を持っていれば、自社の確認は必要ない
- B. どの業種でも基準は同じなので、確認は省いてよい
- C. 自社に必要な基準を確認して、AWS の準拠資料を Artifact で確認する
- D. クレジットカードのデータは AWS に一切保存できないと考えて、オンプレミスに残す

??? success "答えと解説"
    **正解: C**

    業界の基準の例は PCI で、自社に必要な基準から確認します。

    - A: 誤り。自社に必要な基準の確認は利用者の担当。
    - B: 誤り。基準は国や業種で異なる。
    - C: 正しい。
    - D: 誤り。保存を一律に禁じるものではない。

    **スキル:** [地域や業界で異なる要件](../domain2.md#t2-2-regions-industries) / **参照:** [AWS Artifact](../../../services/cloud-foundations.md#artifact)

### 問18 {#q18}

コンプライアンスの要件についての説明として正しいものはどれですか。

- A. 世界で共通の 1 つの基準を満たせば、どの国でも足りる
- B. 必要な基準は、事業を行う国や業種によって大きく異なる
- C. 必要な基準は、使う EC2 のインスタンスタイプで決まる
- D. 必要な基準は、AWS のサポートプランで決まる

??? success "答えと解説"
    **正解: B**

    業種や国に合わせて基準を確認します。

    - A: 誤り。国や業種で異なる。
    - B: 正しい。
    - C: 誤り。インスタンスタイプでは決まらない。
    - D: 誤り。サポートプランでは決まらない。

    **スキル:** [地域や業界で異なる要件](../domain2.md#t2-2-regions-industries) / **参照:** [AWS Artifact](../../../services/cloud-foundations.md#artifact)

### 問19 {#q19}

不審な API 呼び出しや、不審な通信を継続的に検出したいと考えています。最も適切なサービスはどれですか。

- A. Amazon GuardDuty
- B. AWS Shield
- C. Amazon Macie
- D. Amazon Inspector

??? success "答えと解説"
    **正解: A**

    GuardDuty は脅威を検出します。

    - A: 正しい。
    - B: 誤り。DDoS を防御するサービス。
    - C: 誤り。S3 の機密データを検出するサービス。
    - D: 誤り。ソフトウェアの脆弱性を検出するサービス。

    **スキル:** [リソースを守るサービス](../domain2.md#t2-2-securing) / **参照:** [GuardDuty](../../../services/threat-detection.md#guardduty)

### 問20 {#q20}

EC2 インスタンスとコンテナイメージの既知の脆弱性（CVE）を見つけたいと考えています。最も適切なサービスはどれですか。

- A. Amazon GuardDuty
- B. Amazon Detective
- C. AWS Security Hub
- D. Amazon Inspector

??? success "答えと解説"
    **正解: D**

    Inspector は脆弱性を検出します。

    - A: 誤り。不審な動きを検出するサービスで、CVE のスキャンが役割ではない。
    - B: 誤り。検出結果の根本原因を調査するサービス。
    - C: 誤り。検出結果の集約とリスクの優先付けを行うサービス。
    - D: 正しい。

    **スキル:** [リソースを守るサービス](../domain2.md#t2-2-securing) / **参照:** [Inspector](../../../services/threat-detection.md#inspector)

### 問21 {#q21}

複数のセキュリティサービスの検出結果を 1 か所にまとめて、リスクの優先付けをしたいと考えています。最も適切なサービスはどれですか。

- A. Amazon Macie
- B. Amazon Inspector
- C. AWS Security Hub
- D. AWS Shield

??? success "答えと解説"
    **正解: C**

    Security Hub は検出結果の集約とリスクの優先付けを行います。

    - A: 誤り。機密データの検出に特化している。
    - B: 誤り。脆弱性を検出する側で、全体の集約が役割ではない。
    - C: 正しい。
    - D: 誤り。DDoS の防御のサービス。

    **スキル:** [リソースを守るサービス](../domain2.md#t2-2-securing) / **参照:** [製品の現在の形](../../../services/threat-detection.md#security-hub-products)

### 問22 {#q22}

目的とサービスの組み合わせとして正しいものはどれですか。（2つ選択）

- A. DDoS から守る: Amazon GuardDuty
- B. 検出結果を集約する: AWS Shield
- C. 検出結果の根本原因を調べる: Amazon Detective
- D. S3 の個人情報を見つける: Amazon Macie
- E. 脆弱性を見つける: Amazon Macie

??? success "答えと解説"
    **正解: C, D**

    名前が似ているので、見るものと役割で区別します。

    - A: 誤り。DDoS の防御は AWS Shield。
    - B: 誤り。集約は AWS Security Hub。
    - C: 正しい。
    - D: 正しい。
    - E: 誤り。脆弱性の検出は Amazon Inspector。

    **スキル:** [リソースを守るサービス](../domain2.md#t2-2-securing) / **参照:** [Macie](../../../services/threat-detection.md#macie)、[Detective](../../../services/threat-detection.md#detective)

### 問23 {#q23}

セキュリティグループの設定がどう変わり、社内の基準に合っているかを評価したいと考えています。最も適切なサービスはどれですか。

- A. AWS Artifact
- B. AWS Config
- C. AWS CloudTrail
- D. Amazon CloudWatch

??? success "答えと解説"
    **正解: B**

    Config は設定の変化を記録し、ルールで準拠を評価します。

    - A: 誤り。AWS の監査レポートを入手するサービス。
    - B: 正しい。
    - C: 誤り。誰がいつ API を呼んだかの記録で、基準への準拠を評価しない。
    - D: 誤り。性能や動作を監視するサービス。

    **スキル:** [ガバナンスとコンプライアンスを助けるサービス](../domain2.md#t2-2-governance-services) / **参照:** [Config と CloudTrail の違い](../../../services/governance.md#config-vs-cloudtrail)

### 問24 {#q24}

目的とサービスの組み合わせとして正しいものはどれですか。

- A. CPU 使用率の監視: CloudWatch、API の操作の監査: CloudTrail
- B. CPU 使用率の監視: Config、API の操作の監査: Inspector
- C. CPU 使用率の監視: CloudTrail、API の操作の監査: CloudWatch
- D. CPU 使用率の監視: Artifact、API の操作の監査: Config

??? success "答えと解説"
    **正解: A**

    CloudWatch は性能や動作を、CloudTrail は API の呼び出しを見ます。

    - A: 正しい。
    - B: 誤り。どちらも役割が違う。
    - C: 誤り。組み合わせが逆。
    - D: 誤り。Artifact は監査レポートの入手先。API の操作の監査は CloudTrail。

    **スキル:** [ガバナンスとコンプライアンスを助けるサービス](../domain2.md#t2-2-governance-services) / **参照:** [CloudWatch と CloudTrail の違い](../../../services/observability.md#cloudtrail-vs-cloudwatch)

### 問25 {#q25}

全 IAM ユーザーのパスワード、アクセスキー、MFA の状態を CSV で一覧にしたいと考えています。何を使いますか。

- A. AWS Artifact のレポート
- B. VPC フローログ
- C. IAM の認証情報レポート
- D. CloudWatch のダッシュボード

??? success "答えと解説"
    **正解: C**

    認証情報レポートは 4 時間に 1 回まで生成できる CSV の一覧です。

    - A: 誤り。AWS の監査レポートで、自分の IAM ユーザーの状態は分からない。
    - B: 誤り。IP 通信の記録。
    - C: 正しい。
    - D: 誤り。メトリクスの可視化のためのもの。

    **スキル:** [ガバナンスとコンプライアンスを助けるサービス](../domain2.md#t2-2-governance-services) / **参照:** [最小権限](../../../services/iam.md#least-privilege)、[Config と CloudTrail の違い](../../../services/governance.md#config-vs-cloudtrail)

### 問26 {#q26}

許可したのに使われていないサービスの権限を見つけて削りたいと考えています。役立つ IAM の機能はどれですか。

- A. 最終アクセス情報
- B. AWS Budgets
- C. Amazon Inspector
- D. パスワードポリシー

??? success "答えと解説"
    **正解: A**

    最終アクセス情報は、許可されたサービスにいつアクセスしたかを示します。

    - A: 正しい。
    - B: 誤り。費用のしきい値の通知。
    - C: 誤り。ソフトウェアの脆弱性の検出。
    - D: 誤り。パスワードの条件を決める設定。

    **スキル:** [ガバナンスとコンプライアンスを助けるサービス](../domain2.md#t2-2-governance-services) / **参照:** [最小権限](../../../services/iam.md#least-privilege)

### 問27 {#q27}

ある基準について、使う予定の AWS のサービスが対象に含まれるかを確認したいと考えています。正しい方法はどれですか。

- A. CloudWatch のメトリクスで、基準の対象かを確認する
- B. 同じカテゴリの別のサービスが対象なら、同じと考える
- C. AWS が認証を持つ基準なら、全サービスが対象と考える
- D. 公式の対象サービスのページで確認する

??? success "答えと解説"
    **正解: D**

    基準の対象でも全サービスが含まれるとは限らないので、公式のページで確認します。

    - A: 誤り。メトリクスでは分からない。
    - B: 誤り。サービスごとに確認が必要。
    - C: 誤り。すべてのサービスが含まれるわけではない。
    - D: 正しい。

    **スキル:** [サービスで異なる準拠の範囲](../domain2.md#t2-2-service-variance) / **参照:** [AWS Artifact](../../../services/cloud-foundations.md#artifact)

### 問28 {#q28}

「AWS はある基準の認証を取得している」と聞いた担当者の理解として正しいものはどれですか。

- A. AWS が認証を持つので、どのサービスを使っても自動的に対象となる
- B. 対象のサービスは基準ごとに決まるので、使うサービスを確認する必要がある
- C. 認証はサポートプランで決まるので、Enterprise なら確認はいらない
- D. 認証はリージョンだけで決まるので、サービスの確認はいらない

??? success "答えと解説"
    **正解: B**

    要件はサービスごとに異なります。

    - A: 誤り。対象のサービスは基準で異なる。
    - B: 正しい。
    - C: 誤り。サポートプランでは決まらない。
    - D: 誤り。サービスの確認が必要。

    **スキル:** [サービスで異なる準拠の範囲](../domain2.md#t2-2-service-variance) / **参照:** [AWS Artifact](../../../services/cloud-foundations.md#artifact)

### 問29 {#q29}

医療データを扱う新しいアプリの設計で、候補の 3 つのサービスのうち 1 つが必要な基準の対象か不明です。最初にすべきことはどれですか。

- A. 対象サービスの公式のページで、3 つとも対象か確認する
- B. 不明なサービスも他の 2 つと同じ扱いで、そのまま本番に使う
- C. 不明なサービスの設定を強くすれば、基準の対象になると考える
- D. AWS Trust & Safety に基準の対象かを問い合わせる

??? success "答えと解説"
    **正解: A**

    使うサービスごとに対象かを確認します。

    - A: 正しい。
    - B: 誤り。対象の確認を省くと要件を満たせない恐れがある。
    - C: 誤り。設定で対象に入るわけではない。
    - D: 誤り。Trust & Safety は悪用の報告の窓口。

    **スキル:** [サービスで異なる準拠の範囲](../domain2.md#t2-2-service-variance) / **参照:** [AWS Artifact](../../../services/cloud-foundations.md#artifact)
