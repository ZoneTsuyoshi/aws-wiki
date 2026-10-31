# 分野5: AI ソリューションのセキュリティ、コンプライアンス、ガバナンス

配点は **14%** です。目的に合うサービスを選べること、データと AI のリスクの考え方を説明できることが中心です。実際の設定や枠組みの策定は求められません。

## タスク 5.1: AI システムを保護する方法を説明する {#task-5-1}

### 5.1.1 AI システムを保護するサービスと機能 {#obj-5-1-1}

| 要件 | 選択 | 問題文の手がかり |
|---|---|---|
| 誰が何をできるかを制御する | IAM のロール、ポリシー、権限 | 最小権限、モデルの利用を制限 |
| データを暗号化する | KMS（保存時）、TLS（転送時） | 自社で鍵を管理 |
| S3 の PII を見つける | Macie | 学習データに個人情報がないか |
| インターネットを経由しない | PrivateLink（VPC エンドポイント） | 閉域から Bedrock を呼ぶ |
| 役割を分担する | 責任共有モデル | AWS と利用者の担当 |
| エージェントの ID と資格情報 | AgentCore Identity | エージェントが外部の API を呼ぶ |
| ツール呼び出しの認可 | Policy in AgentCore | 返金は 10,000 円以下だけ許可 |
| 入出力の保護 | Bedrock Guardrails | 有害な内容、PII、プロンプト攻撃 |

**責任共有モデル:** AWS は基盤、サービス、Bedrock の FM の運用を担当します。利用者は、データ、アクセス権、プロンプト、ガードレールの設定、アプリのセキュリティ、出力の扱いを担当します。

**AgentCore Policy** は、エージェントのコードの外でツール呼び出しを判定します。モデルの判断に頼らないので、プロンプトで「してはいけない」と書くより確実です。

詳細: [AI システムを守るサービス](../../services/ai-fundamentals.md#security-services)、[責任共有モデル](../../services/ai-fundamentals.md#shared-responsibility)、[最小権限](../../services/iam.md#least-privilege)、[保存時と転送時の暗号化](../../services/kms.md#at-rest-in-transit)、[Macie](../../services/threat-detection.md#macie)、[VPC エンドポイントでの接続](../../services/ai.md#privatelink)、[AgentCore の構成要素](../../services/ai.md#agentcore-components)、[AgentCore Policy](../../services/genai-apps.md#agentcore-policy)

### 5.1.2 出典の明示とデータの出所の記録 {#obj-5-1-2}

| 考え方 | 内容 | AWS の例 |
|---|---|---|
| 出典の明示 | 回答の根拠となる文書を示す | Knowledge Bases の引用 |
| データ系譜 | データの出所と加工の履歴を記録する | メタデータタグ、処理の記録 |
| データカタログ | どのデータがどこにあるかを登録する | Glue Data Catalog |
| モデルの文書化 | 学習データ、用途、評価を記録する | SageMaker Model Cards |

**具体例:** 監査で「このモデルはどのデータで学習したか」と聞かれたら、カタログと Model Cards で答えられるようにします。

詳細: [統治の仕組み](../../services/genai-apps.md#governance-controls)、[Data Catalog](../../services/data-engineering.md#glue-data-catalog)、[Model Cards](../../services/sagemaker.md#model-cards)

### 5.1.3 安全なデータエンジニアリングのベストプラクティス {#obj-5-1-3}

| 実践 | 内容 | AWS の例 |
|---|---|---|
| データ品質の評価 | 欠損、重複、誤りをルールで測る | Glue Data Quality、DataBrew |
| プライバシー強化技術 | 個人を特定しにくくする | 下の表 |
| データのアクセス制御 | 必要な人だけに必要な範囲を許可する | IAM、Lake Formation |
| データの完全性 | 改ざんや破損を防ぎ、検知する | S3 Object Lock、CloudTrail |

**プライバシー強化技術:**

| 技術 | 内容 | 例 |
|---|---|---|
| マスキング | 一部を隠す | `****-1234` |
| トークン化 | 別の値に置き換え、対応表で管理する | `tok_a1b2` |
| 匿名化 | 個人を特定できる情報を取り除く | 氏名や住所の列を削除 |
| 差分プライバシー | 計算して調整したノイズを加え、個人の情報を推定しにくくする | 集計結果への適用 |

データの最小化も基本です。学習や推論に必要のない機密情報は、そもそもモデルに渡しません。

詳細: [データ品質](../../services/data-engineering.md#glue-data-quality)、[DataBrew](../../services/data-engineering.md#databrew)、[Lake Formation](../../services/data-engineering.md#lake-formation)、[サニタイズとマスキング](../../services/secrets.md#sanitization-masking)、[データの保護](../../services/genai-apps.md#data-protection)、[Object Lock](../../services/s3.md#object-lock)

### 5.1.4 AI システムのセキュリティとプライバシーの考慮点 {#obj-5-1-4}

| 観点 | 内容 | AWS の例 |
|---|---|---|
| アプリのセキュリティ | 入力の検証、認証、最小権限 | IAM、Secrets Manager |
| 脅威の検知 | 不審な動きを見つける | CloudTrail、CloudWatch |
| 脆弱性の管理 | ソフトウェアの既知の脆弱性を見つける | Inspector |
| 基盤の保護 | ネットワークを分離する | VPC、PrivateLink |
| プロンプトインジェクション | 入力に指示を混ぜて動作を変える | Guardrails のプロンプト攻撃 |
| 保存時と転送時の暗号化 | データを読めなくする | KMS、TLS |
| データ漏えいの防止 | 機密情報を出力やログに出さない | 機密情報フィルター、Macie |
| 出力のフィルターと検証 | 応答を利用する前に確かめる | Guardrails、JSON Schema の検証 |
| 監査証跡とログ | 誰が何をしたか、何を入出力したかを残す | CloudTrail、モデル呼び出しログ |
| 有害性（toxicity） | 攻撃的、差別的な内容を防ぐ | コンテンツフィルター |

**ログの区別:**

| ログ | 記録するもの | 既定 |
|---|---|---|
| CloudTrail | API の操作（誰が呼んだか） | 管理イベントはイベント履歴に 90 日 |
| モデル呼び出しログ | プロンプトと応答の本文 | 無効。有効にして CloudWatch Logs や S3 に送る |

モデル呼び出しログには元の入力がそのまま残ります。Guardrails のマスクはログには効かないので、ログ自体を保護します。

**間接プロンプトインジェクション:** 利用者の入力だけでなく、RAG の文書やツールの結果に指示が仕込まれることもあります。

**範囲の注意:** GuardDuty、WAF、Shield、Security Hub は範囲外の一覧に載っています。考え方は押さえますが、試験の選択肢としては上の表のサービスを優先して考えます。

詳細: [AI システムを守るサービス](../../services/ai-fundamentals.md#security-services)、[多層防御](../../services/genai-apps.md#defense-in-depth)、[モデル呼び出しログ](../../services/ai.md#invocation-logging)、[CloudTrail のイベント](../../services/observability.md#cloudtrail-events)、[Inspector](../../services/threat-detection.md#inspector)、[VPC](../../services/networking.md#vpc)

### 5.1.5 ハルシネーションの検出とグラウンディング {#obj-5-1-5}

| 手法 | 内容 | AWS の例 |
|---|---|---|
| RAG によるグラウンディング | 文書に基づいて答えさせる | Knowledge Bases |
| グラウンディングの検査 | 応答が参照元に基づくか採点する | コンテキストグラウンディング |
| 論理の検証 | 規定との矛盾を検出する | Automated Reasoning |
| 出力の検証 | 形式や業務ルールに沿うか確かめる | 構造化出力 |
| 信頼度スコア | 低いときは人に回す | しきい値を決めて人がレビュー |

コンテキストグラウンディングのスコアには 2 種類あります。

| スコア | 意味 | 低い例 |
|---|---|---|
| グラウンディング | 応答が参照元に基づくか | 質問に答えているが、文書と違う |
| 関連性 | 応答が質問に答えているか | 文書の内容だが、質問に答えていない |

詳細: [ハルシネーションへの対策](../../services/ai-fundamentals.md#hallucinations)、[コンテキストグラウンディング](../../services/genai-apps.md#contextual-grounding)、[Automated Reasoning](../../services/genai-apps.md#automated-reasoning)、[構造化出力](../../services/genai-apps.md#structured-output)

## タスク 5.2: AI システムのガバナンスとコンプライアンスを認識する {#task-5-2}

### 5.2.1 ガバナンスと規制への準拠を支えるサービス {#obj-5-2-1}

| サービス | 役割 | 問題文の手がかり |
|---|---|---|
| AWS Config | リソースの設定を記録し、ルールで評価する | 設定が基準に合っているか |
| Amazon Inspector | 脆弱性をスキャンする | EC2、コンテナイメージ、Lambda の脆弱性 |
| AWS Artifact | AWS の監査レポートや契約を入手する | SOC レポート、ISO の認証を監査人に渡す |
| AWS CloudTrail | API の操作を記録する | 誰がいつ呼んだか |
| AWS Trusted Advisor | ベストプラクティスに沿った推奨を出す | コスト、セキュリティ、耐障害性の点検 |

**Config と CloudTrail:** Config は「設定がどうなっているか」、CloudTrail は「誰が何をしたか」です。

Artifact の文書は AWS 側のものです。自社のシステムの準拠は、利用者が別に示します。

詳細: [Config](../../services/governance.md#config)、[Config と CloudTrail の違い](../../services/governance.md#config-vs-cloudtrail)、[Inspector](../../services/threat-detection.md#inspector)、[AWS Artifact](../../services/cloud-foundations.md#artifact)、[CloudTrail](../../services/observability.md#cloudtrail)、[Trusted Advisor](../../services/cloud-foundations.md#trusted-advisor)

### 5.2.2 データガバナンスの戦略 {#obj-5-2-2}

| 戦略 | 内容 | AWS の例 |
|---|---|---|
| データのライフサイクル | 作成から削除までを管理する | S3 ライフサイクル |
| ログ | 操作と入出力を記録する | CloudTrail、モデル呼び出しログ |
| データの所在（レジデンシー） | データを置き、処理する場所を守る | リージョンの選択、地理的な推論プロファイル |
| 監視 | ポリシー違反や異常を検知する | Config、CloudWatch |
| 観察 | 利用状況や品質の傾向を見続ける | CloudWatch の生成 AI オブザーバビリティ |
| 保持 | 必要な期間だけ残し、期限後に消す | CloudWatch Logs の保持期間、S3 Object Lock |

**具体例:** データを EU の外で処理してはいけないなら、`eu` の推論プロファイルを使います。`global` では要件を満たしません。

詳細: [データの保護](../../services/genai-apps.md#data-protection)、[S3 ライフサイクル](../../services/s3.md#lifecycle)、[データの保持](../../services/storage.md#retention)、[クロスリージョン推論の違い](../../services/ai.md#model-identifiers)、[CloudWatch の生成 AI オブザーバビリティ](../../services/genai-apps.md#genai-observability)

### 5.2.3 ガバナンスの手順 {#obj-5-2-3}

| 手順 | 内容 | 例 |
|---|---|---|
| 方針 | 使ってよいデータやツールを定める | 承認済み、評価中、禁止に分類して公開する |
| レビューの頻度 | 影響に応じて見直しの間隔を決める | 高リスクの用途ほど頻繁に見直す |
| レビューの方法 | 誰がどの観点で確認するかを決める | 法務、セキュリティ、事業の担当者が合同で確認する |
| ガバナンスの枠組み | 共通の基準を使う | 下の Scoping Matrix |
| 透明性の基準 | 文書化や開示の水準を揃える | Model Cards、AI の使用の表示 |
| チームの研修 | 責任ある AI やデータの扱いを学ぶ | 開発者と利用者への定期的な研修 |

**Generative AI Security Scoping Matrix:** AWS が公開している、生成 AI の利用形態を 5 つに分ける枠組みです。番号が大きいほど、自社の制御と責任が大きくなります。

| スコープ | 形態 | 例 |
|---|---|---|
| 1 | 消費者向けアプリ | 公開のチャットサービスを使う |
| 2 | 企業向けアプリ | 第三者の業務 SaaS に組み込まれた AI を使う |
| 3 | 事前学習済みモデル | Bedrock の FM で自社のアプリを作る |
| 4 | ファインチューニングしたモデル | FM を自社のデータで調整する |
| 5 | 自社で学習したモデル | ゼロから学習する |

**標準と規制の例:** ISO/IEC 42001（AI マネジメントシステム）、NIST AI RMF（リスク管理）、EU AI 法（リスクを 4 段階に分類）があります。

詳細: [Scoping Matrix](../../services/ai-fundamentals.md#scoping-matrix)、[標準と規制](../../services/ai-fundamentals.md#standards)、[役割と責任](../../services/ai-fundamentals.md#governance-roles)、[シャドー AI](../../services/ai-fundamentals.md#shadow-ai)

## 確認問題 {#self-check}

??? question "問1: FM の学習データを入れる S3 バケットに、顧客の個人情報が含まれていないか確認したいです。どのサービスを使いますか。"
    Amazon Macie です。S3 のデータから PII などの機密データを見つけます。Inspector はソフトウェアの脆弱性を調べるサービスで、データの中身は見ません。

??? question "問2: VPC 内のアプリから、インターネットを経由せずに Bedrock を呼びたいです。何を使いますか。また、この対策でデータの学習利用も防げますか。"
    AWS PrivateLink（インターフェイス VPC エンドポイント）です。PrivateLink が守るのは通信経路で、データの利用方法は別の話です。なお、Bedrock は入出力をモデルの学習に使いません。

??? question "問3: 監査人から、AWS のデータセンターの SOC レポートを求められました。どこから入手しますか。"
    AWS Artifact です。AWS の監査レポートや認証をダウンロードできます。AWS Config は自社のリソースの設定を評価するサービスで、AWS の監査レポートは入手できません。

??? question "問4: 企業が Bedrock の FM を自社の過去の問い合わせでファインチューニングして使います。Generative AI Security Scoping Matrix のどのスコープですか。"
    スコープ 4 です。既存の FM を自社のデータで調整しているからです。そのまま API で使うならスコープ 3 です。学習データとカスタムモデルも自社で管理する必要があります。

??? question "問5: セキュリティ部門が、誰が Bedrock のガードレールを変更したかと、モデルに送られたプロンプトの内容の両方を調べたいです。何を確認しますか。"
    変更の操作は CloudTrail、プロンプトの内容はモデル呼び出しログです。モデル呼び出しログは既定で無効なので、事前に有効にしておきます。本文には機密情報が残るので、ログの保護も必要です。

??? question "問6: 社内規定に答える RAG アプリが、文書にない内容を答えることがあります。本番で、根拠のない応答を検出して止めるにはどうしますか。"
    Bedrock Guardrails のコンテキストグラウンディングを使います。応答が参照元に基づくかを採点し、しきい値を下回ればブロックします。temperature を下げるだけでは、根拠のない応答を検出できません。
