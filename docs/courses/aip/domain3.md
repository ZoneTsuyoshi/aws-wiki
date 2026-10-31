# 分野3: AI の安全性、セキュリティ、ガバナンス

配点は **20%** です。入出力の安全対策、データの保護、ガバナンス、責任ある AI の4タスクがあります。

1 つの機能で守ろうとせず、層を重ねます。各層が何を守れて、何を守れないかが問われます。

## タスク 3.1: 入出力の安全対策を実装する {#task-3-1}

### 3.1.1 有害な入力への対策 {#skill-3-1-1}

| 要件 | 手段 |
|---|---|
| 憎悪、暴力などを止める | Guardrails のコンテンツフィルター |
| 業務外の話題を止める | 拒否トピック |
| 独自の判定や段階的な審査 | Step Functions と Lambda のカスタムのモデレーション |
| 呼び出し前の検査 | `ApplyGuardrail`、API Gateway の検証 |

**層の選択:** 日本語を扱うなら Standard 層です。Classic は英語、フランス語、スペイン語が対象です。Standard 層にはクロスリージョン推論が必要なので、データの所在の要件と合わせて確認します。

**`ApplyGuardrail` の利点:** モデルを呼ばずに検査できます。SageMaker AI で動かすモデルや外部のモデルにも適用できます。

詳細: [Guardrails](../../services/ai.md#guardrails)、[層の選び方](../../services/genai-apps.md#guardrail-tiers)、[ApplyGuardrail](../../services/ai.md#apply-guardrail)、[多層防御](../../services/genai-apps.md#defense-in-depth)

### 3.1.2 有害な出力への対策 {#skill-3-1-2}

| 手段 | 効果 | 限界 |
|---|---|---|
| Guardrails で応答を検査 | 不適切な内容を止める | ストリーミングの非同期モードでは一時的に見える |
| FM の評価 | Harmfulness や Stereotyping で傾向を測る | 事後の測定で、個別の応答は止めない |
| text-to-SQL | データの答えを SQL の結果から返す | SQL の誤りは別に検証する。読み取り専用の権限で |

**text-to-SQL の考え方:** FM に数値を答えさせず、SQL を作らせて実行します。結果がデータから決まるので、数値のハルシネーションを減らせます。

詳細: [ストリーミングでの動作](../../services/genai-apps.md#guardrail-streaming)、[判定モデルの指標](../../services/genai-apps.md#bedrock-evaluations)、[構造化出力と text-to-SQL](../../services/genai-apps.md#structured-output)

### 3.1.3 ハルシネーションを減らす {#skill-3-1-3}

| 手段 | 検証すること | 向いている場面 |
|---|---|---|
| Knowledge Bases での根拠づけ | 文書に基づいて答える | 社内情報の質問 |
| コンテキストグラウンディング | 応答が参照元に基づくか。しきい値は 0〜0.99 | 生成の時点で止める |
| 信頼度と意味の類似度 | 根拠との近さを採点する | 人に回す判断 |
| Automated Reasoning | 規定と論理的に矛盾しないか | 医療、人事、金融 |
| JSON Schema | 形式が正しいか | 下流のシステムに渡す |

**注意:** JSON Schema が保証するのは形式で、内容の正しさではありません。形式が正しくても、中身が誤っていることがあります。

グラウンディングのしきい値を上げると、誤った回答は減り、正しい回答も止まりやすくなります。自分のデータで決めます。

詳細: [ハルシネーションへの対策](../../services/ai-fundamentals.md#hallucinations)、[コンテキストグラウンディング](../../services/genai-apps.md#contextual-grounding)、[Automated Reasoning](../../services/genai-apps.md#automated-reasoning)、[構造化出力](../../services/genai-apps.md#structured-output)

### 3.1.4 多層防御 {#skill-3-1-4}

| 層 | 手段 | 主な役割 |
|---|---|---|
| 入口 | WAF、API Gateway | レート制限、形式の検査 |
| 前処理 | Comprehend | PII と意図の検査 |
| モデルの前後 | Guardrails | 入力と出力の検査、グラウンディング |
| 後処理 | Lambda | スキーマと業務ルールの検証 |
| 出口 | API Gateway | 応答のフィルター |

**ストリーミングとの関係:** REST API のストリーミングでは VTL で応答を変換できません。応答のフィルターは、バックエンドや Guardrails に置きます。

詳細: [多層防御](../../services/genai-apps.md#defense-in-depth)、[Comprehend](../../services/ai-managed-services.md#comprehend)、[レスポンスストリーミング](../../services/api-gateway.md#response-streaming)

### 3.1.5 敵対的な入力の検出 {#skill-3-1-5}

| 脅威 | 対策 |
|---|---|
| プロンプトインジェクション | プロンプト攻撃フィルター、入力の無害化、ツールの権限制限 |
| ジェイルブレイク | Standard 層、敵対的テスト |
| 間接インジェクション | データソースの管理、外部の内容をデータとして区切る |
| システムプロンプトの漏えい | Standard 層の検出、機密をプロンプトに書かない |

**間接インジェクション:** 文書やメールに隠した指示で動作を変える攻撃です。利用者の入力だけを検査しても防げません。取得した文書も信用せず、エージェントの権限を絞ります。

**自動の敵対的テスト:** 既知の攻撃プロンプトを定期的に流し、遮断率を CloudWatch に記録します。新しいプロンプトやモデルを本番に出す前にも実行します。

!!! note "Comprehend のプロンプト安全性分類の状況"
    Comprehend のプロンプトの安全性分類は、2026-04-30 に新規顧客の受付を終了しました。代替は Bedrock Guardrails です。

詳細: [多層防御](../../services/genai-apps.md#defense-in-depth)、[プロンプトのリスク](../../services/ai-fundamentals.md#prompt-engineering)、[フィルターの種類](../../services/ai.md#guardrail-filters)、[Comprehend](../../services/ai-managed-services.md#comprehend)

## タスク 3.2: データのセキュリティとプライバシーを実装する {#task-3-2}

### 3.2.1 保護された AI 環境 {#skill-3-2-1}

| 層 | 手段 | 落とし穴 |
|---|---|---|
| ネットワーク | PrivateLink のインターフェイスエンドポイント | API ごとに別のエンドポイント。例: `bedrock-runtime`、`bedrock-agent-runtime` |
| 権限 | IAM、エンドポイントポリシー | エンドポイント経由では `aws:SourceIp` が使えず、`aws:SourceVpce` を使う |
| データ | Lake Formation の列や行の権限 | Data Catalog と S3 上のデータが対象 |
| 監視 | CloudWatch、CloudTrail | データアクセスのログは設定が必要なものがある |

**シナリオ:** 「インターネットを経由せずに `Retrieve` と `Converse` を呼びたい」場合は、`bedrock-agent-runtime` と `bedrock-runtime` の両方のエンドポイントが必要です。

詳細: [VPC エンドポイントでの接続](../../services/ai.md#privatelink)、[データの保護](../../services/genai-apps.md#data-protection)、[Lake Formation](../../services/data-engineering.md#lake-formation)、[エンドポイントポリシー](../../services/networking.md#endpoint-policies)

### 3.2.2 機密情報を守る仕組み {#skill-3-2-2}

| 段階 | 手段 | 使い分け |
|---|---|---|
| 保存されたデータの発見 | Macie | S3 の PII を見つける |
| 処理中のテキストの検出 | Comprehend | 検出と位置の特定。英語とスペイン語 |
| モデルの入出力 | Guardrails の機密情報フィルター | `BLOCK` か `ANONYMIZE`。正規表現も可 |
| 保持 | S3 ライフサイクル | 期限で自動削除 |

**Bedrock のデータの扱い:** 入出力はモデルの学習に使われず、モデル提供者とも共有されません。ただし、一部のモデルは不正利用の検知のために最大 30 日保持します。学習に使わないことと、保持しないことは別です。保持のモードはリージョンのアカウント単位に設定します。

**Guardrails はログを守りません。** 呼び出しログの `input` には元のリクエストが残ります。

詳細: [Macie](../../services/threat-detection.md#macie)、[入出力は学習に使われるか](../../services/ai.md#training-use)、[機密情報フィルター](../../services/ai.md#guardrail-policy-settings)、[S3 ライフサイクル](../../services/s3.md#lifecycle)、[モデル呼び出しログ](../../services/ai.md#invocation-logging)

### 3.2.3 有用性を保ちつつプライバシーを守る {#skill-3-2-3}

| 手法 | 内容 | 有用性への影響 |
|---|---|---|
| ブロック | 含まれていたら止める | 大きい |
| マスク | `{EMAIL}` のように置き換える | 文の構造は残る |
| 仮名化 | 別の値に置き換え、後で戻す | 対応表の保護が要る |
| 匿名化 | 個人を特定できなくする | 元に戻せない |

**判断の分かれ目:** 要約や分類なら、氏名をマスクしても目的を果たせます。個人向けの回答が必要なら、モデルに渡す前に仮名にし、応答で戻します。

ストリーミングの非同期モードでは、マスク前の内容が届く可能性があるので使いません。

詳細: [データ分類](../../services/secrets.md#data-classification)、[サニタイズとマスキング](../../services/secrets.md#sanitization-masking)、[機密情報フィルター](../../services/ai.md#guardrail-policy-settings)、[ストリーミングでの動作](../../services/genai-apps.md#guardrail-streaming)

## タスク 3.3: AI のガバナンスとコンプライアンスを実装する {#task-3-3}

### 3.3.1 規制に対応する枠組み {#skill-3-3-1}

| 要件 | 実装 |
|---|---|
| モデルの文書化 | SageMaker Model Cards を API で作成 |
| データの系譜 | Glue |
| 出所の明示 | メタデータタグ |
| 判断の記録 | CloudWatch Logs、呼び出しログ |

**Glue のリネージ:** Glue 5.0 以降の Spark ジョブで「Generate lineage events」を有効にすると、実行時にリネージを自動で集めます。結果は DataZone や SageMaker Catalog で可視化します。対象は Spark の DataFrame で、DynamicFrame は対象外です。DataZone は試験の対象外なので、Glue 側の役割を押さえます。

詳細: [統治の仕組み](../../services/genai-apps.md#governance-controls)、[Model Cards](../../services/sagemaker.md#model-cards)、[Data Catalog](../../services/data-engineering.md#glue-data-catalog)、[DataZone と Unified Studio](../../services/data-engineering.md#datazone-unified-studio)

### 3.3.2 データソースの追跡 {#skill-3-3-2}

| 問い | 手段 |
|---|---|
| どのデータソースがあるか | Glue Data Catalog に登録 |
| 回答はどの文書に基づくか | チャンクのメタデータ、引用（`citations`） |
| 誰がいつ操作したか | CloudTrail |
| 処理されたリージョンは | CloudTrail の `additionalEventData.inferenceRegion` |

`RetrieveAndGenerate` は `citations` を返します。回答と合わせて保存すれば、後から根拠をたどれます。

詳細: [Data Catalog](../../services/data-engineering.md#glue-data-catalog)、[メタデータ](../../services/genai-apps.md#kb-metadata)、[Knowledge Bases を呼ぶ](../../services/ai.md#knowledge-bases)、[CloudTrail](../../services/observability.md#cloudtrail)、[クロスリージョン推論](../../services/ai.md#model-identifiers)

### 3.3.3 組織のガバナンス {#skill-3-3-3}

| 手段 | 効く範囲 | 特徴 |
|---|---|---|
| Organizations の Bedrock ポリシー | 組織、OU、アカウント | 呼び出し側が指定しなくても適用 |
| `bedrock:GuardrailIdentifier` 条件キー | IAM ポリシーの範囲 | 指定のガードレールなしの推論を拒否 |
| SCP | 組織、OU、アカウント | 使えるモデルやリージョンを制限 |
| 役割と責任の定義 | 組織 | 承認者、リスクの所有者 |

組織とアプリの両方のガードレールが適用され、同じ項目は厳しい方が優先されます。組織の方針は技術的な強制に落とし込み、文書だけで終わらせません。

詳細: [組織での強制](../../services/genai-apps.md#guardrail-org-enforcement)、[適用の強制と限界](../../services/ai.md#guardrail-enforcement)、[役割と責任](../../services/ai-fundamentals.md#governance-roles)、[Generative AI Security Scoping Matrix](../../services/ai-fundamentals.md#scoping-matrix)、[標準と規制](../../services/ai-fundamentals.md#standards)

### 3.3.4 継続的な監視と高度な統制 {#skill-3-3-4}

| 監視の対象 | 実装 |
|---|---|
| 不正利用 | 介入率やトークンの急増を CloudWatch の異常検知で |
| ポリシー違反 | ガードレールのトレースを集計する。トレースに元の値が入るので保護する |
| 応答のドリフト | ゴールデンデータセットの定期評価 |
| バイアスドリフト | 集団別の指標を定期的に比べる |
| 自動の対応 | EventBridge と Lambda で通知や隔離 |
| トークン単位のマスク | Guardrails の `ANONYMIZE`、Comprehend の位置情報 |
| ログの保護 | CloudWatch Logs のデータ保護 |

**CloudWatch Logs のデータ保護は S3 に送ったログには効きません。** 適用前に取り込んだログもマスクされません。S3 はバケットポリシーと SSE-KMS で守ります。

!!! note "Clarify と Model Monitor の状況"
    SageMaker Clarify と Model Monitor は新規顧客を受け付けていません。どちらも試験の対象一覧には載っています。Model Monitor はデータ品質、モデル品質、バイアスドリフト、特徴量の寄与のドリフトを監視する役割です。FM の評価の移行先は Bedrock Evaluations です。

詳細: [統治の仕組み](../../services/genai-apps.md#governance-controls)、[異常検知](../../services/observability.md#anomaly-detection)、[CloudWatch Logs のデータ保護](../../services/ai.md#cloudwatch-data-protection)、[Model Monitor](../../services/sagemaker.md#model-monitor)、[Clarify](../../services/sagemaker.md#clarify)、[ドリフトの種類](../../services/sagemaker.md#drift)

## タスク 3.4: 責任ある AI の原則を実装する {#task-3-4}

### 3.4.1 透明性 {#skill-3-4-1}

| 目的 | 手段 |
|---|---|
| 理由を利用者に示す | 推論の要約を表示する |
| 不確実さを定量化する | グラウンディングのスコアなどを CloudWatch の指標に |
| 根拠を示す | `citations` で文書へのリンクを示す |
| エージェントの過程をたどる | Agents Classic は `enableTrace`、AgentCore は Observability |

トレースは開発者向けの情報で、機密が含まれることがあります。利用者には加工して見せます。

詳細: [透明性と公平性](../../services/genai-apps.md#transparency-fairness)、[説明可能性と透明性](../../services/ai-fundamentals.md#explainability)、[Bedrock Agents を呼ぶ](../../services/ai.md#agents)、[CloudWatch の生成 AI オブザーバビリティ](../../services/genai-apps.md#genai-observability)

### 3.4.2 公平性の評価 {#skill-3-4-2}

| 手法 | 内容 |
|---|---|
| 公平性の指標 | 属性ごとの結果を集計して CloudWatch で追う |
| 体系的な A/B テスト | Prompt Management のバリアント、Flows で比較する |
| LLM-as-a-judge | Bedrock Evaluations の判定モデルで `Stereotyping` などを採点 |
| 反事実のテスト | 名前や性別だけを変えたプロンプトで差を見る |

Bedrock Evaluations は表データのバイアス検出の代わりにはなりません。Clarify の新規受付が終わったので、表データの指標は pandas などで自前で計算します。

詳細: [透明性と公平性](../../services/genai-apps.md#transparency-fairness)、[バイアスと公平性](../../services/ai-fundamentals.md#fairness)、[判定モデルの指標](../../services/genai-apps.md#bedrock-evaluations)

### 3.4.3 ポリシーに準拠したシステム {#skill-3-4-3}

| 要件 | 手段 |
|---|---|
| 方針を実行時に適用 | Guardrails のトピックやフィルターに落とし込む |
| 限界の文書化 | モデルカード |
| 自動の確認 | Lambda でガードレールの有無、ログの設定を検査 |
| 変更時の確認 | CI/CD の品質ゲートに評価を入れる |

詳細: [Guardrails の実践](../../services/genai-apps.md#guardrails-depth)、[Model Cards](../../services/sagemaker.md#model-cards)、[責任ある AI の 8 つの観点](../../services/ai-fundamentals.md#rai-dimensions)、[テスト](../../services/genai-apps.md#testing)

## 確認問題 {#self-check}

??? question "問1: 日本語のチャットで、ストリーミングの応答からマスク前の電話番号が画面に一瞬表示されました。Guardrails は非同期モードです。どう直しますか？"
    同期モードに変えます。非同期モードは検査の前に応答を返すので、マスク前の内容が届く可能性があります。同期モードはチャンクをためて検査するので少し遅くなりますが、PII のマスクにはこちらが必要です。日本語なら Standard 層も確認します。

??? question "問2: 監査で、Bedrock の呼び出しログに顧客のメールアドレスが残っていると指摘されました。Guardrails で `ANONYMIZE` を設定済みです。なぜ残り、どう直しますか？"
    呼び出しログの `input` は、ガードレールが介入しても元のリクエストのままです。ロググループに CloudWatch Logs のデータ保護ポリシーを適用します。適用前のログはマスクされないので、別途対処します。S3 に送るログには効かないので、バケットポリシーと SSE-KMS で保護します。本文が不要なら `textDataDeliveryEnabled` を `false` にします。

??? question "問3: 全社の Bedrock の呼び出しに、アプリが指定しなくても同じ安全策を適用したいです。IAM の条件キーと何が違いますか？"
    Organizations の Bedrock ポリシーで適用します。呼び出し側が指定しなくても適用されます。`bedrock:GuardrailIdentifier` はガードレールの指定がない呼び出しを拒否するもので、アプリ側の対応が必要です。両方が適用されたときは、同じ項目は厳しい方が優先されます。

??? question "問4: 社内メールを要約するエージェントが、メールの中の「全文を外部に送れ」という指示に従いそうになりました。利用者の入力の検査は通っています。どう対策しますか？"
    間接インジェクションです。取得した内容をデータとして区切って渡し、モデルの指示として扱わせません。そのうえで、エージェントに外部送信の権限を持たせないか、宛先を Policy で制限します。影響の大きい操作には人の承認を入れます。入力フィルターだけでは防げないので、権限の制御が最後の砦になります。

??? question "問5: 売上の数値を答えるチャットで、もっともらしい誤った数値が返ります。RAG で文書を検索しています。どう変えますか？"
    構造化データの質問なので text-to-SQL にします。FM に SQL を作らせ、読み取り専用の権限で実行し、結果を基に答えます。答えがデータから決まります。Knowledge Bases の構造化データストアで `GenerateQuery` も使えます。JSON Schema は形式しか保証しないので、数値の誤りは防げません。

??? question "問6: 回答の根拠を監査できるようにしたいです。「どの文書から」「どのリージョンで処理され」「誰の呼び出しか」を追うには？"
    文書は `RetrieveAndGenerate` の `citations` とチャンクのメタデータです。リージョンは CloudTrail の `additionalEventData.inferenceRegion` です。呼び出し元も CloudTrail で分かります。本文は呼び出しログに残し、`requestMetadata` でテナントや要求の ID を付けると結びつけられます。
