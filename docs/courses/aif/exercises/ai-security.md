# AI システムのセキュリティの問題集

対象の解説: [AI システムを守るサービス](../../../services/ai-fundamentals.md#security-services)、[データプライバシー](../../../services/ai.md#data-privacy)、[多層防御](../../../services/genai-apps.md#defense-in-depth)

### 問1 {#q1}

FM の学習データを入れる S3 バケットに、顧客の個人情報が含まれていないかを確認します。適切なサービスはどれですか。

- A. AWS Trusted Advisor
- B. Amazon Inspector
- C. AWS Artifact
- D. Amazon Macie

??? success "答えと解説"
    **正解: D**

    Macie は S3 のデータから PII などの機密データを見つけます。

    - A: 誤り。環境を点検して推奨を出すサービスです。
    - B: 誤り。ソフトウェアの脆弱性を調べるサービスで、データの中身は見ません。
    - C: 誤り。AWS の監査レポートを入手するサービスです。
    - D: 正しい。

    **スキル:** [5.1.1](../domain5.md#obj-5-1-1) / **参照:** [Macie](../../../services/threat-detection.md#macie)

### 問2 {#q2}

VPC 内のアプリから、インターネットを経由せずに Bedrock を呼びたいと考えています。適切なものはどれですか。

- A. SageMaker Model Cards
- B. Bedrock Guardrails
- C. AWS PrivateLink
- D. AWS KMS

??? success "答えと解説"
    **正解: C**

    インターフェイス VPC エンドポイントを使うと、インターネットを経由せずに呼べます。

    - A: 誤り。モデルの文書化の機能です。
    - B: 誤り。入出力を検査する機能です。
    - C: 正しい。
    - D: 誤り。暗号鍵を管理するサービスで、経路は変わりません。

    **スキル:** [5.1.1](../domain5.md#obj-5-1-1) / **参照:** [VPC エンドポイントでの接続](../../../services/ai.md#privatelink)

### 問3 {#q3}

特定のチームだけが特定のモデルを呼べるようにしたいと考えています。適切な手段はどれですか。

- A. temperature の設定
- B. IAM のロールとポリシー
- C. Amazon Macie の検出
- D. Bedrock のバッチ推論

??? success "答えと解説"
    **正解: B**

    最小権限で、誰が何をできるかを制御します。

    - A: 誤り。推論のパラメータです。
    - B: 正しい。
    - C: 誤り。機密データを見つけるサービスで、利用の権限は制御しません。
    - D: 誤り。推論の方式で、権限の制御ではありません。

    **スキル:** [5.1.1](../domain5.md#obj-5-1-1) / **参照:** [最小権限](../../../services/iam.md#least-privilege)、[IAM のスコープ](../../../services/ai.md#iam-scope)

### 問4 {#q4}

エージェントが外部の API を呼ぶときの ID と資格情報を、安全に管理したいと考えています。適切な機能はどれですか。

- A. AgentCore Identity
- B. AgentCore Memory
- C. AgentCore Browser
- D. Bedrock Knowledge Bases

??? success "答えと解説"
    **正解: A**

    AgentCore Identity はエージェント向けの ID と資格情報の管理のサービスです。

    - A: 正しい。
    - B: 誤り。短期と長期の記憶を提供する機能です。
    - C: 誤り。隔離されたブラウザの機能です。
    - D: 誤り。文書を検索する機能です。

    **スキル:** [5.1.1](../domain5.md#obj-5-1-1) / **参照:** [AgentCore の構成要素と設定](../../../services/ai.md#agentcore-components)

### 問5 {#q5}

エージェントの返金ツールを「金額が 10,000 円以下のときだけ許可」にしたいと考えています。プロンプトで指示するより確実な方法はどれですか。

- A. AgentCore Memory に禁止事項を保存する
- B. システムプロンプトを長くする
- C. Policy in AgentCore
- D. temperature を 0 にする

??? success "答えと解説"
    **正解: C**

    エージェントのコードの外で、決定的にツール呼び出しを判定します。

    - A: 誤り。記憶は判定の仕組みではありません。
    - B: 誤り。モデルの判断に頼るので、確実ではありません。
    - C: 正しい。
    - D: 誤り。ばらつきを減らすだけで、認可にはなりません。

    **スキル:** [5.1.1](../domain5.md#obj-5-1-1) / **参照:** [Policy](../../../services/genai-apps.md#agentcore-policy)

### 問6 {#q6}

自社で鍵を管理して、保存時のデータを暗号化したいと考えています。適切なサービスはどれですか。

- A. AWS KMS
- B. AWS Config
- C. Amazon Inspector
- D. AWS CloudTrail

??? success "答えと解説"
    **正解: A**

    保存時は KMS で、転送時は TLS で保護します。

    - A: 正しい。
    - B: 誤り。リソースの設定を評価するサービスです。
    - C: 誤り。脆弱性を調べるサービスです。
    - D: 誤り。API の操作を記録するサービスです。

    **スキル:** [5.1.1](../domain5.md#obj-5-1-1) / **参照:** [保存時と転送時の暗号化](../../../services/kms.md#at-rest-in-transit)

### 問7 {#q7}

学習データの欠損、重複、誤りをルールで測りたいと考えています。適切なサービスを選んでください。（2つ選択）

- A. Amazon Macie
- B. AWS Config
- C. Amazon Inspector
- D. AWS Glue DataBrew
- E. AWS Glue Data Quality

??? success "答えと解説"
    **正解: D, E**

    データ品質の評価は、安全なデータエンジニアリングの第一歩です。

    - A: 誤り。機密データを発見するサービスで、品質のルールは評価しません。
    - B: 誤り。リソースの設定を評価するサービスで、データの中身は測りません。
    - C: 誤り。ソフトウェアの脆弱性を調べるサービスです。
    - D: 正しい。
    - E: 正しい。

    **スキル:** [5.1.3](../domain5.md#obj-5-1-3) / **参照:** [Data Quality](../../../services/data-engineering.md#glue-data-quality)、[DataBrew](../../../services/data-engineering.md#databrew)

### 問8 {#q8}

クレジットカード番号を `****-1234` と表示します。このプライバシー強化技術はどれですか。

- A. トークン化
- B. マスキング
- C. 差分プライバシー
- D. 匿名化

??? success "答えと解説"
    **正解: B**

    一部を隠すのがマスキングです。

    - A: 誤り。別の値に置き換えて、対応表で管理する技術です。
    - B: 正しい。
    - C: 誤り。計算して調整したノイズを加える技術です。
    - D: 誤り。個人を特定できる情報を取り除く技術です。

    **スキル:** [5.1.3](../domain5.md#obj-5-1-3) / **参照:** [サニタイズとマスキング](../../../services/secrets.md#sanitization-masking)、[データの保護](../../../services/genai-apps.md#data-protection)

### 問9 {#q9}

集計結果に調整したノイズを加えて、個人の情報を推定しにくくします。この技術はどれですか。

- A. トークン化
- B. 暗号化
- C. マスキング
- D. 差分プライバシー

??? success "答えと解説"
    **正解: D**

    計算して調整したノイズを加える技術です。

    - A: 誤り。別の値に置き換える技術です。
    - B: 誤り。鍵がなければ読めなくする技術で、ノイズは加えません。
    - C: 誤り。一部を隠す技術です。
    - D: 正しい。

    **スキル:** [5.1.3](../domain5.md#obj-5-1-3) / **参照:** [サニタイズとマスキング](../../../services/secrets.md#sanitization-masking)、[AI システムを守るサービス](../../../services/ai-fundamentals.md#security-services)

### 問10 {#q10}

データレイクの学習データに、列単位の細かいアクセス権を設定します。適切なサービスはどれですか。

- A. Amazon Macie
- B. AWS Lake Formation
- C. Amazon Inspector
- D. AWS Config

??? success "答えと解説"
    **正解: B**

    データのアクセス制御は IAM と Lake Formation で行います。

    - A: 誤り。機密データを発見するサービスで、権限は設定しません。
    - B: 正しい。
    - C: 誤り。ソフトウェアの脆弱性を調べるサービスです。
    - D: 誤り。リソースの設定を評価するサービスで、データの権限は設定しません。

    **スキル:** [5.1.3](../domain5.md#obj-5-1-3) / **参照:** [AWS Lake Formation](../../../services/data-engineering.md#lake-formation)

### 問11 {#q11}

学習データが改ざんされないよう、一定期間は上書きも削除もできないようにしたいと考えています。適切な機能はどれですか。

- A. S3 ライフサイクル
- B. AWS Glue DataBrew
- C. AWS Config のルール
- D. S3 Object Lock

??? success "答えと解説"
    **正解: D**

    データの完全性の例です。Object Lock は保持期間中の削除や上書きを防ぎます。

    - A: 誤り。移行や削除を自動化する機能で、削除を防ぐものではありません。
    - B: 誤り。データの準備の機能です。
    - C: 誤り。設定を評価するだけで、上書きや削除は防げません。
    - D: 正しい。

    **スキル:** [5.1.3](../domain5.md#obj-5-1-3) / **参照:** [Object Lock](../../../services/s3.md#object-lock)

### 問12 {#q12}

セキュリティ部門が、誰が Bedrock のガードレールを変更したかと、モデルに送られたプロンプトの内容の両方を調べます。確認先の組み合わせはどれですか。

- A. どちらも AWS Config
- B. 変更はモデル呼び出しログ、内容は CloudTrail の管理イベント
- C. 変更は CloudTrail、内容はモデル呼び出しログ
- D. どちらも Amazon Inspector

??? success "答えと解説"
    **正解: C**

    操作は CloudTrail、プロンプトと応答の本文はモデル呼び出しログです。

    - A: 誤り。Config はリソースの設定の記録と評価を行います。
    - B: 誤り。逆です。CloudTrail は API の操作を、呼び出しログは本文を記録します。
    - C: 正しい。
    - D: 誤り。Inspector は脆弱性を調べるサービスです。

    **スキル:** [5.1.4](../domain5.md#obj-5-1-4) / **参照:** [モデル呼び出しログ](../../../services/ai.md#invocation-logging)、[イベントの種類](../../../services/observability.md#cloudtrail-events)

### 問13 {#q13}

Bedrock のモデル呼び出しログの説明として正しいものを選んでください。（2つ選択）

- A. 有効にしなくても自動で S3 に保存される
- B. Guardrails でブロックした内容もログには平文で残る
- C. 本文は記録されず、API の呼び出し元だけが残る
- D. Guardrails のマスクが適用された値だけが記録される
- E. 既定では無効である

??? success "答えと解説"
    **正解: B, E**

    有効にして CloudWatch Logs や S3 に送ります。ログに残る内容を踏まえて保護します。

    - A: 誤り。有効にする必要があります。
    - B: 正しい。
    - C: 誤り。プロンプトと応答の本文を記録します。
    - D: 誤り。ログには元の入力が残るので、ログ自体を保護します。
    - E: 正しい。

    **スキル:** [5.1.4](../domain5.md#obj-5-1-4) / **参照:** [モデル呼び出しログ](../../../services/ai.md#invocation-logging)

### 問14 {#q14}

エージェントが動くコンテナイメージの既知の脆弱性を見つけます。適切なサービスはどれですか。

- A. Amazon Inspector
- B. Amazon Macie
- C. AWS Config
- D. AWS Artifact

??? success "答えと解説"
    **正解: A**

    脆弱性の管理は Inspector で、EC2、コンテナイメージ、Lambda をスキャンします。

    - A: 正しい。
    - B: 誤り。S3 の機密データを発見するサービスです。
    - C: 誤り。リソースの設定を評価するサービスで、イメージの脆弱性は調べません。
    - D: 誤り。AWS の監査レポートを入手するサービスです。

    **スキル:** [5.1.4](../domain5.md#obj-5-1-4) / **参照:** [Inspector](../../../services/threat-detection.md#inspector)

### 問15 {#q15}

利用者が普通の質問をしただけなのに、RAG で取得した文書の中に仕込まれた指示にモデルが従いました。この攻撃はどれですか。

- A. データドリフト
- B. コールドスタート
- C. 間接プロンプトインジェクション
- D. 過学習

??? success "答えと解説"
    **正解: C**

    利用者の入力だけでなく、文書やツールの結果に指示が仕込まれることもあります。

    - A: 誤り。本番の入力の分布の変化です。
    - B: 誤り。資源の準備に時間がかかることです。
    - C: 正しい。
    - D: 誤り。学習データを暗記する状態です。

    **スキル:** [5.1.4](../domain5.md#obj-5-1-4) / **参照:** [多層防御](../../../services/genai-apps.md#defense-in-depth)

### 問16 {#q16}

AI アプリのネットワークを分離して、基盤を保護します。適切な組み合わせはどれですか。

- A. Macie と Artifact
- B. VPC と PrivateLink
- C. Budgets と Cost Explorer
- D. KMS と CloudTrail

??? success "答えと解説"
    **正解: B**

    基盤の保護は、VPC でネットワークを分離し、閉域で接続します。

    - A: 誤り。機密データの発見と監査レポートのサービスです。
    - B: 正しい。
    - C: 誤り。コストのサービスです。
    - D: 誤り。暗号鍵の管理と API の記録のサービスで、ネットワークは分離しません。

    **スキル:** [5.1.4](../domain5.md#obj-5-1-4) / **参照:** [VPC の基本](../../../services/networking.md#vpc)、[VPC エンドポイントでの接続](../../../services/ai.md#privatelink)

### 問17 {#q17}

応答に含まれる機密情報の漏えいを防ぎ、攻撃的な内容も止めたいと考えています。適切な対策はどれですか。

- A. AWS Trusted Advisor のセキュリティの推奨を定期的に確認して設定を直す
- B. AWS Config のルール
- C. S3 のライフサイクル
- D. Guardrails の機密情報フィルターとコンテンツフィルター

??? success "答えと解説"
    **正解: D**

    データ漏えいの防止と有害性の防止には、出力の検査が効きます。

    - A: 誤り。環境の点検で、応答の内容は検査しません。
    - B: 誤り。リソースの設定の評価で、応答の内容は検査しません。
    - C: 誤り。オブジェクトの移行と削除の機能です。
    - D: 正しい。

    **スキル:** [5.1.4](../domain5.md#obj-5-1-4) / **参照:** [フィルターの種類](../../../services/ai.md#guardrail-filters)
