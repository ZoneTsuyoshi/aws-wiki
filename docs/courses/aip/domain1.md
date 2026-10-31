# 分野1: FM の統合、データ管理、コンプライアンス

配点は **31%** で、5分野の中で最大です。要件の分析、FM の選定、データの整備、ベクトルストア、検索、プロンプトの6タスクがあります。

この分野の中心は RAG です。「どのサービスが使えるか」ではなく、「この制約なら何を選び、何を諦めるか」を問われます。

この分野に限らず、コース全体で使うサービスは[サービス一覧](services.md)から確認できます。

## タスク 1.1: 要件を分析して生成 AI ソリューションを設計する {#task-1-1}

### 1.1.1 業務要件と技術的制約に合う設計 {#skill-1-1-1}

要件を次の順に制約へ翻訳します。先に決まる制約ほど、選択肢を大きく絞ります。

| 制約 | 確認すること | 設計への影響 |
|---|---|---|
| データの所在 | 国外に出せるか | `global` の推論プロファイルは使えない。地理的プロファイルか単一リージョン |
| 情報の更新頻度 | 毎日変わるか | RAG を選ぶ。ファインチューニングは更新のたびに再学習が要る |
| 応答時間 | 画面で待てるか | ストリーミングか、SQS での非同期か |
| 処理量の波 | 一定か急増するか | オンデマンド、Provisioned Throughput、バッチ |
| モデルの自由度 | 独自の重みが必要か | Bedrock か SageMaker AI か |

**シナリオ:** 社内規定の質問に答えるアプリで、規定は月に数回変わり、データは国内に置く必要があるとします。RAG を選び、地理的プロファイルかリージョン内の呼び出しに限定します。

詳細: [FM の選択](../../services/genai-apps.md#fm-selection)、[選び方の比較](../../services/genai-apps.md#choosing)、[クロスリージョン推論](../../services/ai.md#model-identifiers)

### 1.1.2 PoC で実現性と価値を検証する {#skill-1-1-2}

全面展開の前に、小さく作って3つを測ります。品質、性能、事業価値です。

- **品質:** 同じ評価データで複数のモデルを比べます。Bedrock Evaluations を使えます。
- **性能:** `TimeToFirstToken` と `InvocationLatency`、スロットリングの有無を見ます。
- **価値:** 本番の想定件数と入出力トークンから月額を試算し、削減できる工数と比べます。

Bedrock はインフラなしで始められるので、PoC に向いています。合格の基準は PoC を始める前に決めます。後から決めると、都合のよい結果を選びがちです。

詳細: [選定の観点](../../services/genai-apps.md#fm-criteria)、[Bedrock Evaluations](../../services/genai-apps.md#bedrock-evaluations)、[KPI と ROI](../../services/ai-fundamentals.md#kpi-roi)

### 1.1.3 標準化された部品を作る {#skill-1-1-3}

複数のチームが同じ形で実装できるように、部品と確認項目を揃えます。

| 手段 | 使いどころ |
|---|---|
| Well-Architected Tool と Generative AI Lens | 設計の確認項目を揃える。リスクを記録して改善を追う |
| CDK のコンストラクト、CloudFormation | 構成を部品にして配る |
| Service Catalog | 承認済みの構成を各チームに提供する |
| GenAI ゲートウェイ | 認証、記録、モデル選択を1か所に置く |

Lens はレビューの枠組みで、実行時に何かを強制するものではありません。強制が必要なら、IAM や Organizations のポリシーと組み合わせます。

詳細: [Well-Architected Tool](../../services/cloud-foundations.md#wa-tool)、[Service Catalog](../../services/governance.md#service-catalog)、[CDK](../../services/iac.md#cdk)、[GenAI ゲートウェイ](../../services/genai-apps.md#genai-gateway)

## タスク 1.2: FM を選定して設定する {#task-1-2}

### 1.2.1 FM の評価と選定 {#skill-1-2-1}

ベンチマークの順位だけでは決めません。自社のデータで評価し、制約で落とします。

1. **必須条件で落とす:** モダリティ、対応言語、リージョン、ツール利用やキャッシュの対応。
2. **限界を確認する:** コンテキスト長、最大出力、ライフサイクルの状態。
3. **自社データで比べる:** 品質、遅延、コストを同じ評価データで表にします。

Legacy のモデルは新規採用しません。EOL に達するとリクエストが失敗し、自動移行もないためです。

詳細: [選定の観点](../../services/genai-apps.md#fm-criteria)、[Nova と Titan](../../services/genai-apps.md#nova-titan)、[モデルのライフサイクル](../../services/genai-apps.md#model-lifecycle)

### 1.2.2 コードを変えずにモデルを切り替える {#skill-1-2-2}

モデル ID を外に出します。典型は API Gateway、Lambda、AppConfig の組み合わせです。`Converse` を使うと、モデルごとの本文の違いも吸収できます。

| 方式 | 変更の反映 | 向いている場面 |
|---|---|---|
| 環境変数 | Lambda の設定更新が必要 | 変更がまれ |
| AppConfig | デプロイなし。段階配布と自動ロールバック | モデルの更新、割合の変更 |
| Intelligent Prompt Routing | Bedrock が同じ系統の中で選ぶ | 別の提供者には切り替えられない |

**判断の分かれ目:** 提供者をまたいで切り替えるなら、Intelligent Prompt Routing ではなく AppConfig と自前の振り分けです。

詳細: [動的なモデル切り替え](../../services/genai-apps.md#dynamic-model-selection)、[AppConfig](../../services/secrets.md#appconfig)、[Converse](../../services/ai.md#converse)

### 1.2.3 障害時も動き続ける設計 {#skill-1-2-3}

障害の範囲ごとに、対策を重ねます。

| 障害の範囲 | 対策 | トレードオフ |
|---|---|---|
| 一時的なスロットリング | バックオフとジッター | 遅延が増える |
| リージョンの容量不足 | クロスリージョン推論 | データがリージョンをまたぐ |
| モデルの障害 | 別モデルへのフォールバック | 品質や出力形式が変わる |
| 継続的な失敗 | サーキットブレーカー | 状態の保存先が要る。例は DynamoDB |
| リージョン全体の障害 | 別リージョンにも構成を置く | コストと同期の手間が増える |
| すべて失敗 | キャッシュ済みの回答、機能の縮退 | 回答の鮮度が落ちる |

サーキットブレーカーは Step Functions でも組めます。失敗の回数を DynamoDB に記録し、しきい値を超えたら第一候補を呼ばずに代替へ進めます。

**別リージョンへの展開:** モデルだけでは RAG は動きません。文書を S3 のクロスリージョンレプリケーションで複製し、別リージョンのナレッジベースで同期します。入口は Route 53 のフェイルオーバーで切り替えます。

!!! tip "データの所在との衝突"
    `global` のプロファイルは容量の面で有利ですが、データの所在の要件があると選べません。地理的プロファイルを選びます。SCP でリージョンを制限している場合は、プロファイルの宛先リージョンをすべて許可します。

詳細: [耐障害の設計](../../services/genai-apps.md#fm-resilience)、[サーキットブレーカー](../../services/sdk-resilience.md#circuit-breaker)、[機能の縮退](../../services/sdk-resilience.md#graceful-degradation)、[クロスリージョン推論](../../services/ai.md#model-identifiers)、[S3 レプリケーション](../../services/s3.md#replication)、[Route 53 のフェイルオーバー](../../services/resilience.md#route53-failover)

### 1.2.4 カスタマイズしたモデルのデプロイとライフサイクル {#skill-1-2-4}

モデルの学習そのものは範囲外です。問われるのは、調整済みのモデルをどう載せ、更新し、戻し、引退させるかです。

| 場面 | 選択 |
|---|---|
| 用途別の調整モデルを少ない GPU で多数提供する | LoRA アダプターとアダプター推論コンポーネント |
| 版の管理と承認 | SageMaker Model Registry の `ModelApprovalStatus` |
| 更新の自動化 | 承認の変更を EventBridge で検知し、CodePipeline や Lambda を起動 |
| 失敗時の復旧 | デプロイガードレールのアラームで自動で戻す |
| 外部で調整した重みを Bedrock で使う | Custom Model Import |

LoRA は基盤モデルの計算資源を共有し、差分の小さな重みだけを追加します。

**引退:** 基盤モデルが Legacy になると、新しいファインチューニングと Provisioned Throughput を作れません。EOL の日付を追い、後継で再評価してから切り替えます。

詳細: [SageMaker AI での FM](../../services/genai-apps.md#sagemaker-fm)、[推論コンポーネントと LoRA](../../services/sagemaker.md#multi-model)、[Model Registry](../../services/sagemaker.md#model-registry)、[デプロイ戦略](../../services/sagemaker.md#deployment-strategies)、[カスタムモデルの実行](../../services/genai-apps.md#custom-model-deploy)

## タスク 1.3: FM に渡すデータの検証と処理のパイプラインを作る {#task-1-3}

### 1.3.1 データ検証のワークフロー {#skill-1-3-1}

品質の悪いデータは、そのまま悪い回答になります。モデルに渡す前に止めます。

| 手段 | 向いている場面 |
|---|---|
| Glue Data Quality | ルールを DQDL で宣言する。データカタログや ETL で検査 |
| SageMaker Data Wrangler | ML の前処理を画面で試す |
| Lambda | 文字数、形式、禁止語など独自の検査。1 件ずつ |
| CloudWatch | 不合格の件数をメトリクスにしてアラーム |

本格的なデータエンジニアリングは範囲外です。AIP-C01 では「FM に渡す前の品質ゲートをどう置くか」が焦点です。

詳細: [Glue Data Quality](../../services/data-engineering.md#glue-data-quality)、[Data Wrangler](../../services/sagemaker.md#data-wrangler)、[非同期と統合](../../services/genai-apps.md#async-integration)

### 1.3.2 複雑なデータ型の処理 {#skill-1-3-2}

| データ | 処理 | 選ぶ理由 |
|---|---|---|
| 音声 | Transcribe で文字にする | 話者の区別や語彙の調整 |
| PDF の表とフォーム | Textract | 決まった構造の抽出 |
| 図やグラフを含む文書 | マルチモーダルの FM、Bedrock Data Automation | 図の意味の解釈 |
| 文書、画像、動画、音声の一括処理 | Bedrock Data Automation | プロンプトなしで構造化 |
| 大規模な独自の変換 | SageMaker Processing | 任意のコンテナでジョブを実行 |

**判断の分かれ目:** Textract は抽出が決定的で、大量の定型帳票に向きます。FM は解釈が柔軟ですが、結果は検証が必要でトークンの費用がかかります。

詳細: [Bedrock Data Automation](../../services/genai-apps.md#bda)、[解析の選択肢](../../services/genai-apps.md#kb-ingestion)、[Transcribe](../../services/ai-managed-services.md#transcribe)、[Textract](../../services/ai-managed-services.md#textract)、[Processing](../../services/sagemaker.md#processing)

### 1.3.3 モデルが要求する形式に整える {#skill-1-3-3}

| 呼び出し先 | 形式 |
|---|---|
| Bedrock `Converse` | `messages` と `system`。モデルをまたいで共通 |
| Bedrock `InvokeModel` | モデルごとに異なる本文の JSON |
| バッチ推論 | S3 の JSONL。1 行に `recordId` と `modelInput` |
| SageMaker AI エンドポイント | コンテナが定める形式 |

対話では、`user` と `assistant` のやり取りを順に渡します。モデルは前回の内容を覚えていないので、必要な履歴はアプリが毎回渡します。

詳細: [API の選び方](../../services/ai.md#invoke-apis)、[Converse の全パラメータ](../../services/ai.md#converse-params)、[InvokeModel](../../services/ai.md#invoke-model)、[バッチの設定](../../services/ai.md#throughput-options)

### 1.3.4 入力の質を高める {#skill-1-3-4}

| 手法 | 例 | 効果 |
|---|---|---|
| Bedrock で書き換え | 口語の質問や崩れた文を整える | 検索と回答が安定する |
| Comprehend で固有表現の抽出 | 製品名や組織名をメタデータにする | 絞り込みの精度が上がる |
| Lambda で正規化 | 日付や単位、全角と半角を揃える | 表記の揺れを減らす |

大量の定型の抽出なら Comprehend、自由な書き換えなら Bedrock です。Comprehend の PII 検出は英語とスペイン語が対象なので、日本語の文書には別の手段を考えます。

詳細: [Comprehend](../../services/ai-managed-services.md#comprehend)、[非同期と統合](../../services/genai-apps.md#async-integration)

## タスク 1.4: ベクトルストアを設計して実装する {#task-1-4}

### 1.4.1 FM を補強するベクトル DB の構成 {#skill-1-4-1}

| 要件 | 選択 | 諦めるもの |
|---|---|---|
| 管理を減らす | Managed Knowledge Base | 細かい制御、`RetrieveAndGenerate` |
| 高い検索品質、細かい調整 | OpenSearch。Neural プラグインで Bedrock と連携 | 運用の手間 |
| 既存の PostgreSQL と結合 | Aurora / RDS + pgvector | サイズの設計が必要 |
| 大量で低頻度、低コスト | S3 Vectors | ハイブリッド検索 |
| 関係をたどる質問 | Neptune Analytics | 1 グラフ 1 インデックス |

**構成のパターン:**

- **階層的な構成:** Knowledge Bases の階層チャンクで、子で検索して親を返します。
- **話題ごとの分割:** OpenSearch で話題の単位に分けて索引します。
- **文書と検索を分ける:** 原本は S3、検索と業務データは RDS に置きます。
- **メタデータと埋め込みを分ける:** 属性は DynamoDB でキー検索し、埋め込みはベクトル DB に置きます。

2 つのストアに分けると、更新のずれが問題になります。DynamoDB Streams などで同期します。

詳細: [Managed と Customer-managed](../../services/genai-apps.md#managed-kb)、[ベクトルストア](../../services/genai-apps.md#vector-stores)、[OpenSearch](../../services/genai-apps.md#opensearch-vectors)、[pgvector](../../services/genai-apps.md#pgvector)、[DynamoDB Streams](../../services/dynamodb.md#streams)

### 1.4.2 メタデータの枠組み {#skill-1-4-2}

ベクトルの近さだけでは、古い文書や権限のない文書も返ります。メタデータで絞ります。

| 要素 | 実装 | 効果 |
|---|---|---|
| タイムスタンプ | S3 のオブジェクトメタデータ、`.metadata.json` | 古い版を除く |
| 著者や部署 | カスタム属性 | 権限や部署で絞る |
| 分類 | タグ | 分野を限定する |

Knowledge Bases では、文書と同じ場所に `<ファイル名>.metadata.json` を置き、検索時に `filter` で絞ります。更新日などを S3 のオブジェクトメタデータで管理しているなら、その値をこのファイルに書き出して検索に使います。

**落とし穴:** OpenSearch Serverless のエンジンが `nmslib` だと、メタデータファイルが無視されます。`faiss` を使います。

詳細: [メタデータ](../../services/genai-apps.md#kb-metadata)、[検索のパラメータ](../../services/ai.md#kb-params)

### 1.4.3 大規模で高速なベクトル DB {#skill-1-4-3}

| 手法 | 内容 | 注意 |
|---|---|---|
| シャード | 検索の遅延を重視するなら 1 シャード 10〜30 GiB が目安 | プライマリの数は後から簡単に変えられない。多すぎても無駄 |
| マルチインデックス | 分野ごとに索引を分け、問い合わせを振り分ける | 分野をまたぐ検索は複数の索引を調べる |
| 階層インデックス | 大分類から小分類へ順に検索する | 大分類を誤ると見つからない |
| HNSW の調整 | `ef_search` を上げると精度が上がり、遅くなる | `m` と `ef_construction` を上げると構築も遅くなる |
| 次元の削減 | 1,024 から 256 にすると、生データは約 4.1 GB から約 1.0 GB に | 精度が下がることがある。100 万チャンクの計算 |

シャード数の目安は「(元データ + 増加分) × (1 + 索引のオーバーヘッド) ÷ 1 シャードの大きさ」です。公式の例では、オーバーヘッドを 10% として計算しています。66 GiB を 30 GiB ずつなら、66 × 1.1 ÷ 30 で約 3 シャードです。

詳細: [OpenSearch](../../services/genai-apps.md#opensearch-vectors)、[ベクトルインデックス](../../services/databases-specialized.md#vector-indexes)、[埋め込みの選び方](../../services/genai-apps.md#embedding-selection)

### 1.4.4 データソースとの統合 {#skill-1-4-4}

| 接続先 | 手段 |
|---|---|
| S3、SharePoint、Confluence、Web、Google Drive、OneDrive | Managed Knowledge Base のコネクタ |
| SaaS | AppFlow で S3 へ転送してから取り込む |
| オンプレミスのファイル | DataSync で S3 へ。SFTP なら Transfer Family |
| 独自の社内 wiki | Custom のデータソースに Lambda から文書を送る |
| 既存の Kendra | Kendra GenAI インデックスを Knowledge Bases から使う |

新しく作れる Customer-managed のコネクタは S3 と Custom だけです（2026年9月30日より前に作ったものは動き続けます）。多くのコネクタが要るなら、Managed の強みになります。

!!! note "Kendra と Q Business の状況"
    Kendra は 2026-06-30 にメンテナンスモードに入り、2026-07-30 から新規顧客を受け付けていません。公式の移行先は Managed Knowledge Base です。Q Business と Q Apps も新規顧客を受け付けておらず、移行先は Amazon Quick です。どちらも試験の対象一覧には載っています。

詳細: [Managed と Customer-managed](../../services/genai-apps.md#managed-kb)、[AppFlow](../../services/data-engineering.md#appflow)、[DataSync](../../services/migration.md#datasync)、[Transfer Family](../../services/migration.md#transfer-family)、[Kendra](../../services/ai-managed-services.md#kendra)、[Q Business](../../services/ai-managed-services.md#q-business)

### 1.4.5 ベクトルストアの鮮度を保つ {#skill-1-4-5}

Customer-managed のナレッジベースは自動で同期しません。ファイルを変えたら `StartIngestionJob` を実行します。処理されるのは差分だけです。Managed はスケジュール同期も設定できますが、頻度は日次、週次、月次です。

| 方式 | 実装 | 鮮度 | 向いている場面 |
|---|---|---|---|
| 定期 | EventBridge のスケジュールで同期 | 1 日など | 更新が一定で少ない |
| 変更の検知 | S3 イベント、EventBridge、Lambda | 数分 | 更新をすぐ反映したい |
| 検証つき | Step Functions で同期、評価、切り替え | 評価の分だけ遅い | 品質の悪化を防ぎたい |

更新が頻繁なら、イベントごとに同期せず、一定の間隔にまとめる設計も考えます。

**埋め込みモデルの変更は差分では済みません。** 全データの再埋め込みが必要です。

詳細: [同期と鮮度](../../services/genai-apps.md#kb-sync)、[EventBridge](../../services/messaging.md#eventbridge)、[S3 イベント通知](../../services/messaging.md#s3-events)

## タスク 1.5: FM を補強する検索の仕組みを設計する {#task-1-5}

### 1.5.1 文書の分割 {#skill-1-5-1}

| 文書と症状 | 選択 | トレードオフ |
|---|---|---|
| まず試す | 既定（約 300 トークン） | |
| 均質な文書 | 固定サイズと重なり | 文の途中で切れることがある |
| マニュアル、規定集で文脈が足りない | 階層チャンク | 返る件数が指定より少なくなる |
| 話題が変わる長文 | セマンティック | FM を使うので追加料金 |
| FAQ など独自の構造 | チャンクなしと Lambda のカスタム変換 | 実装と保守が要る |

設定値の例は、固定サイズの `maxTokens` 512 と `overlapPercentage` 20、階層の親 1,500 と子 300 です。埋め込みモデルの入力上限を超えるとエラーになります。

詳細: [チャンク化の戦略](../../services/genai-apps.md#chunking)

### 1.5.2 埋め込みの選択と設定 {#skill-1-5-2}

| 観点 | Titan Text Embeddings V2 の場合 |
|---|---|
| 次元 | 1,024（既定）、512、256 |
| 入力の上限 | 8,192 トークン、50,000 文字 |
| クォータ | TPM ではなく RPM |

- **次元:** 大きいと精度が上がる傾向で、保存と検索のコストが増えます。
- **分野との適合:** 自社の文書で検索の評価をして比べます。
- **モダリティ:** 画像や音声も検索するならマルチモーダルの埋め込みです。
- **大量の生成:** RPM に当たるので、SQS と Lambda で流量を制御するか、バッチ推論を使います。

詳細: [埋め込みの選び方](../../services/genai-apps.md#embedding-selection)、[Nova と Titan](../../services/genai-apps.md#nova-titan)、[クォータ](../../services/ai.md#quotas-detail)

### 1.5.3 ベクトル検索のデプロイと設定 {#skill-1-5-3}

| 選択 | 必須の設定 | 誤ったときの症状 |
|---|---|---|
| OpenSearch | `knn: true`、`knn_vector`、`dimension` | 次元の不一致で取り込みエラー |
| Aurora + pgvector | HNSW は pgvector 0.5.0 以上。`vector(n)` をモデルの次元に | 取り込みエラー |
| Knowledge Bases のマネージド | 埋め込みと検索を任せる | 細かく調整できない |

Knowledge Bases から Aurora へは、Data API と Secrets Manager で接続します。ハイブリッド検索には GIN インデックスを作ります。

詳細: [OpenSearch](../../services/genai-apps.md#opensearch-vectors)、[pgvector](../../services/genai-apps.md#pgvector)、[取り込みの流れ](../../services/genai-apps.md#kb-ingestion)

### 1.5.4 関連性を高める検索の構成 {#skill-1-5-4}

| 症状 | 手法 | 注意 |
|---|---|---|
| 製品番号や固有名詞で外れる | ハイブリッド検索 | S3 Vectors では使えない |
| 関連はするが順位が悪い | リランク（Amazon Rerank 1.0、Cohere Rerank 3.5） | テキストのみ。遅延と費用が増える |
| 候補が広すぎる | メタデータフィルター | 属性の整備が前提 |

**組み合わせの例:** ハイブリッド検索で上位 20 件を取り、リランクで 5 件に絞ります。精度が上がり、モデルに渡すトークンも減ります。

詳細: [検索の改善](../../services/genai-apps.md#retrieval-optimization)、[検索のパラメータ](../../services/ai.md#kb-params)

### 1.5.5 問い合わせの処理 {#skill-1-5-5}

| 手法 | 実装 | 効く質問 |
|---|---|---|
| クエリ拡張 | Bedrock で同義語や言い換えを足す | 語彙が文書とずれている |
| クエリ分解 | `RetrieveAndGenerate` の設定、Lambda | 「A 社と B 社で売上が高いのは?」 |
| クエリの変換 | Step Functions で書き換え、検索、確認を順に | 複数の手順が要る |
| 暗黙のフィルター | `implicitFilterConfiguration` | 質問から絞り込み条件を作る |

各手法は FM の呼び出しを増やすので、遅延と費用が増えます。単純な質問まで通さないよう、分類してから適用します。

詳細: [検索の改善](../../services/genai-apps.md#retrieval-optimization)、[Step Functions の状態](../../services/step-functions.md#state-types)

### 1.5.6 一貫したアクセスの仕組み {#skill-1-5-6}

| 方式 | 内容 | 向いている場面 |
|---|---|---|
| 関数呼び出し | `Converse` の `toolConfig` に検索を定義する | 1 つのアプリ |
| MCP | 検索を MCP サーバーで公開する | 複数のアプリやエージェントで再利用する |
| 標準の API | `Retrieve` を社内共通の API の裏に置く | モデルを介さない呼び出しも含める |

検索をツールにすると、モデルが必要なときだけ検索します。常に検索するより無駄が減りますが、呼び忘れがありえます。必ず根拠が必要な業務なら、アプリ側で先に検索します。

詳細: [ツール利用の流れ](../../services/ai.md#tool-use-flow)、[MCP](../../services/genai-apps.md#mcp)、[Knowledge Bases を呼ぶ](../../services/ai.md#knowledge-bases)

## タスク 1.6: プロンプトエンジニアリングとガバナンスを実装する {#task-1-6}

### 1.6.1 モデルへの指示の枠組み {#skill-1-6-1}

| 目的 | 手段 | 強制力 |
|---|---|---|
| 役割の統一 | Prompt Management のテンプレート | テンプレートを使う限り |
| 責任ある AI の方針 | Guardrails | モデルの外で検査する |
| 応答の形式 | テンプレートの指定、構造化出力 | 構造化出力はスキーマに合わせる |

「してはいけない」とプロンプトに書くだけでは、確実ではありません。守らせたいルールは Guardrails やアプリの検証に置きます。

詳細: [プロンプトの管理](../../services/genai-apps.md#prompt-management)、[Guardrails の実践](../../services/genai-apps.md#guardrails-depth)、[構造化出力](../../services/genai-apps.md#structured-output)

### 1.6.2 文脈を保つ対話システム {#skill-1-6-2}

| 要素 | 手段 |
|---|---|
| 会話履歴 | DynamoDB。パーティションキーをセッション ID に、TTL で自動削除 |
| 意図の判定 | Comprehend のカスタム分類、または小さな FM |
| 聞き返し | Step Functions で「情報が足りなければ質問して待つ」流れを作る |
| エージェントの記憶 | AgentCore Memory |

履歴をすべて渡すと、トークンが増え続けます。古い部分は要約します。Step Functions で人の入力を待つなら、Standard の `waitForTaskToken` です。Express では使えません。

詳細: [プロンプトの管理](../../services/genai-apps.md#prompt-management)、[Memory の設計](../../services/genai-apps.md#agentcore-memory)、[TTL](../../services/dynamodb.md#ttl)、[Standard と Express](../../services/step-functions.md#standard-express)

### 1.6.3 プロンプトの管理とガバナンス {#skill-1-6-3}

| 目的 | 手段 |
|---|---|
| 定型化 | `{{変数}}` を含むテンプレート |
| 版の固定 | 変更できないバージョン。ARN を `modelId` に指定 |
| 承認 | CI/CD でのレビューと評価の通過を条件に昇格 |
| 保管 | S3 やリポジトリのテンプレート |
| 操作の追跡 | CloudTrail |
| 利用内容の記録 | CloudWatch Logs、呼び出しログ |

CloudTrail は「誰がいつ API を呼んだか」、呼び出しログは「何を入力して何が返ったか」です。この違いがよく問われます。

詳細: [プロンプトの管理](../../services/genai-apps.md#prompt-management)、[モデル呼び出しログ](../../services/ai.md#invocation-logging)、[CloudWatch と CloudTrail の違い](../../services/observability.md#cloudtrail-vs-cloudwatch)

### 1.6.4 プロンプトの品質保証 {#skill-1-6-4}

| 検査 | 手段 |
|---|---|
| 期待する出力か | Lambda で形式と内容を検証 |
| 境界条件 | Step Functions の Map で空の入力や長い入力を流す |
| 回帰 | 合格率を CloudWatch の指標にしてアラーム |

出力は毎回変わるので、完全一致では判定できません。形式の検証、意味的な類似度、判定モデルの採点を組み合わせます。

詳細: [プロンプトの管理](../../services/genai-apps.md#prompt-management)、[テスト](../../services/genai-apps.md#testing)、[Map の設定](../../services/step-functions.md#map-settings)

### 1.6.5 プロンプトの反復的な改善 {#skill-1-6-5}

| 手法 | 例 |
|---|---|
| 入力の構造化 | 指示、文脈、データを区切る |
| 出力形式の指定 | JSON Schema、項目の順序 |
| Chain-of-thought | 段階的に考えさせる。計算や推論に |
| フィードバックのループ | 低評価の例を集めて改善し、評価してから昇格する |

Chain-of-thought は出力トークンが増えます。単純な分類では費用だけが増えることがあります。

詳細: [プロンプトエンジニアリング](../../services/ai-fundamentals.md#prompt-engineering)、[利用者からの評価](../../services/genai-apps.md#user-feedback)

### 1.6.6 複雑なプロンプトシステム {#skill-1-6-6}

Bedrock Flows（ガイドの Prompt Flows）は、プロンプト中心の流れを画面で組みます。

| 要件 | ノードや機能 |
|---|---|
| 順に実行する連鎖 | Prompt ノードをつなぐ |
| 応答による分岐 | Condition |
| 再利用 | Prompt Management のプロンプトを使う |
| 前処理と後処理 | Lambda function、Inline code |
| 繰り返し | DoWhile loop、Iterator / Collector |
| リリース | バージョンとエイリアス |

| ツール | 向いている場面 |
|---|---|
| Flows | プロンプト中心で、画面で作りたい |
| Step Functions | AWS サービス全般、複雑なエラー処理、人の承認 |
| AgentCore / Strands | モデルが手順を自分で決める |

詳細: [Bedrock Flows](../../services/genai-apps.md#flows)、[構造のパターン](../../services/genai-apps.md#workflow-patterns)

## 確認問題 {#self-check}

??? question "問1: EU の顧客データを扱う RAG アプリで、ピーク時にスロットリングが出ます。データは EU の外に出せません。モデルの呼び出しをどう変えますか？"
    `eu` の地理的な推論プロファイルを使います。EU 内のリージョンに振り分けられ、データの所在の要件を保ったまま容量を増やせます。`global` は要件を満たしません。SCP でリージョンを制限しているなら、プロファイルの宛先リージョンをすべて許可します。Provisioned Throughput は推論プロファイルに対応しないので、組み合わせられません。

??? question "問2: 複数の提供者のモデルを評価中で、本番のモデルを数分で切り替え、問題があれば自動で戻したいです。デプロイはしたくありません。どう設計しますか？"
    モデル ID を AppConfig に置き、Lambda から読みます。呼び出しは `Converse` にして本文の違いを吸収します。AppConfig の段階配布と CloudWatch アラームで、自動で戻せます。Intelligent Prompt Routing は同じ系統のモデルの中でしか振り分けないので、提供者をまたぐ切り替えには使えません。

??? question "問3: 製品マニュアルの RAG で、回答に前後の文脈が足りません。検索の一致は細かい単位で行いたいです。どのチャンク戦略を選び、何に注意しますか？"
    階層チャンクです。子チャンクで検索し、親チャンクに置き換えて返します。返る件数が `numberOfResults` より少なくなることがあります。また、S3 Vectors では非推奨で、メタデータの上限に達することがあります。ベクトルストアとの組み合わせも確認します。

??? question "問4: 部品番号「AB-123」で検索すると、無関係な文書が上位に返ります。ベクトルストアは S3 Vectors です。何を変えますか？"
    キーワードの一致が必要なのでハイブリッド検索にします。Knowledge Bases で S3 Vectors を使うとハイブリッド検索はできないので、OpenSearch Serverless などへストアを移します。そのうえでリランクを加えると、順位も改善します。リランクだけでは、候補に入らない文書を救えません。

??? question "問5: 用途別に調整した 20 個のモデルを SageMaker AI で提供します。どれも同じ基盤モデルから LoRA で調整しました。GPU のコストを抑えるにはどう載せますか？"
    基盤モデルを推論コンポーネントで載せ、S3 のアダプターを指すアダプター推論コンポーネントを 20 個作ります。基盤モデルの計算資源を共有できます。版の管理は Model Registry で行い、承認の変更を EventBridge で検知してデプロイします。モデルごとのエンドポイントは、基盤モデルの重みを 20 回載せることになり高くつきます。

??? question "問6: 監査チームが「誰がプロンプトのテンプレートを変更したか」と「ある回答のときにモデルへ何が送られたか」の両方を求めています。それぞれ何で答えますか？"
    変更の操作は CloudTrail です。送信の内容は Bedrock のモデル呼び出しログです。既定で無効なので、事前に有効にしておく必要があります。呼び出しログには本文が入るので、CloudWatch Logs のデータ保護や SSE-KMS でログ自体も保護します。
