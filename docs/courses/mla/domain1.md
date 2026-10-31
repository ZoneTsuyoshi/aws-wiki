# 分野1: ML と AI のためのデータ準備

MLA-C02 の配点は **28%** で、4分野の中で最大です。従来の ML のデータ処理に加えて、ベクトルデータベース、埋め込み、RAG 向けの文書の準備、FM の学習データも範囲です。

アソシエイトの試験なので、要件に合うサービスを選び、設定まで答えられるようにします。

[![データの取り込み、カタログ、変換、分析の流れ](../../assets/diagrams/data-engineering-pipeline.png)](../../assets/diagrams/data-engineering-pipeline.png)

この分野に限らず、コース全体で使うサービスは[サービス一覧](services.md)から確認できます。

## タスク 1.1: データを収集して保存する {#task-1-1}

### 1.1.1 データソースからの抽出 {#skill-1-1-1}

データがどこにあるかで、取り出し方が変わります。学習に使うデータは、多くの場合 S3 に集めます。

| ソース | 取り出し方 | 試験で見る点 |
|---|---|---|
| S3 | 学習ジョブのチャネル、Athena、Glue | 大きなデータは FastFile モード |
| EBS | アタッチしたインスタンスから読む | 通常 1 台からのみ。共有には向かない |
| EFS | マウントして読む。学習チャネルにも指定できる | チャネルでは File モードを使う |
| RDS | Glue の接続で読み、S3 に書き出す | 本番 DB の負荷に注意する |
| DynamoDB | S3 へのエクスポート | PITR が必要。読み取りキャパシティを消費しない |
| OpenSearch Service | 検索 API で必要な文書を取り出す | 全件の処理より検索に向く |

DynamoDB のエクスポートは非同期で、テーブルの性能に影響しません。形式は DynamoDB JSON か Amazon Ion です。全件の Scan で本番に負荷をかける選択肢は誤りです。

詳細: [入力モード](../../services/sagemaker.md#input-modes)、[Data Wrangler](../../services/sagemaker.md#data-wrangler)、[比較](../../services/storage.md#comparison)、[Glue](../../services/data-engineering.md#glue)、[DynamoDB](../../services/dynamodb.md#backup)

### 1.1.2 ストレージの選択と設定 {#skill-1-1-2}

コスト、性能、データの構造、コンプライアンスの4つで決めます。

| 要件 | 選択 |
|---|---|
| 学習データの置き場所、耐久性、低コスト | S3 |
| 1 桁ミリ秒で読む必要がある | S3 Express One Zone |
| アクセスが不明または変わる | S3 Intelligent-Tiering |
| 何年も保管し、読むのは年 1 回未満 | S3 Glacier Deep Archive |
| 複数の Linux から共有 | EFS |
| 大量の学習データを GPU へ高速に渡す | FSx for Lustre |
| 1 台のインスタンスの低遅延ディスク | EBS |

コンプライアンスの要件には、KMS の暗号化、S3 のライフサイクルによる削除、Lake Formation の細かい権限を組み合わせます。

詳細: [ストレージクラス](../../services/s3.md#storage-classes)、[ライフサイクル](../../services/s3.md#lifecycle)、[ストレージの比較](../../services/storage-advanced.md#storage-comparison)、[Lake Formation](../../services/data-engineering.md#lake-formation)

### 1.1.3 取り込みと保存の問題の解決 {#skill-1-1-3}

容量と拡張性に関する症状を、原因と結びつけます。

| 症状 | 原因 | 対応 |
|---|---|---|
| Kinesis で `ProvisionedThroughputExceededException` | シャードの上限、キーの偏り | シャード追加、キーの分散、バックオフ |
| `IteratorAgeMilliseconds` が増え続ける | 消費が書き込みに追いつかない | 消費者の強化、拡張ファンアウト |
| S3 で HTTP 503（Slow Down） | 同じプレフィックスへの急増 | プレフィックスの分散、バックオフ |
| DynamoDB のスロットリング | キーの偏り、容量不足 | 高カーディナリティのキー、オンデマンド |
| 学習ジョブで `No space left` | EBS の容量不足 | ボリュームの拡大、FastFile |
| EFS が遅くなる | Bursting のクレジット切れ | Elastic か Provisioned へ変更 |
| 新しいパーティションがクエリに出ない | カタログに未登録 | `MSCK REPAIR TABLE`、クローラー |

シャード数は、書き込みサイズ、書き込み件数、読み取りのうち最も大きい値で決めます。2 KB のレコードを毎秒 2,500 件なら、書き込みサイズの条件で 5 シャードです。

詳細: [シャード数の計算](../../services/streaming.md#shard-calculation)、[Kinesis のエラー](../../services/streaming.md#kinesis-errors)、[S3 のリクエストレート](../../services/s3.md#request-rate)、[DynamoDB のスロットリング](../../services/dynamodb.md#throttling)、[EFS のスループット](../../services/storage.md#efs-throughput-mode)、[パーティションの同期](../../services/data-engineering.md#partition-sync)

### 1.1.4 ストリーミングでの取り込み {#skill-1-1-4}

| 要件 | 選択 |
|---|---|
| 独自のコードで順序どおりに読む、複数の消費者 | Kinesis Data Streams |
| S3 や OpenSearch へ届けるだけ | Amazon Data Firehose |
| ウィンドウ集計や結合など状態を持つ処理 | Managed Service for Apache Flink |
| 既存の Kafka のコードを使う | Amazon MSK |
| カメラなどの動画や音声 | Kinesis Video Streams |

Firehose はバッファの分だけ遅れます。リアルタイムの特徴量計算には Kinesis Data Streams と Lambda か Flink を選びます。

詳細: [選び方](../../services/streaming.md#choosing)、[Kinesis Data Streams](../../services/streaming.md#kinesis-data-streams)、[Firehose](../../services/streaming.md#firehose)、[Flink](../../services/data-engineering.md#flink)、[MSK との違い](../../services/data-engineering.md#msk-vs-kinesis)、[Kinesis Video Streams](../../services/other-services.md#kinesis-video)

### 1.1.5 データ形式の選択 {#skill-1-1-5}

| 形式 | 向き | 向いている場面 |
|---|---|---|
| Parquet | 列 | 分析と学習の一般的な選択。必要な列だけ読める |
| ORC | 列 | Hive 中心の環境 |
| CSV | 行 | 受け渡し。スキーマがない |
| JSON | 行 | ログ、API、入れ子のデータ |

「一部の列だけを読むクエリが遅くて高い」なら、Parquet に変換して日付でパーティションを切ります。変換は Athena の CTAS か Glue のジョブで行います。

gzip の大きな 1 ファイルは分割して読めません。Parquet の中で Snappy などの圧縮を使います。

詳細: [データ形式](../../services/data-engineering.md#data-formats)、[パーティション](../../services/data-engineering.md#partitioning)

### 1.1.6 複数のソースの結合 {#skill-1-1-6}

| 手段 | 向いている場面 |
|---|---|
| pandas などのコード | メモリに載る量。Processing ジョブで実行する |
| Glue の Spark ジョブ | カタログと連携したサーバーレスの結合 |
| EMR の Spark | 既存の Spark コード、細かな調整 |
| Data Wrangler | 画面で結合を試す |

結合が重いジョブでエグゼキューターの OOM が出たら、Glue では `R` タイプか大きなワーカーに変えます。

時系列のデータでは、予測の時点より後の値を結合しないようにします。未来の情報が学習に混ざると、検証の結果だけがよくなります。

詳細: [Glue のジョブ](../../services/data-engineering.md#glue-jobs)、[EMR](../../services/data-engineering.md#emr)、[変換エンジンの選び方](../../services/data-engineering.md#choosing-transform)

### 1.1.7 ベクトルデータベースの設定 {#skill-1-1-7}

| ストア | 向いている場面 | 注意 |
|---|---|---|
| OpenSearch Serverless | 既定の選択、ハイブリッド検索 | OCU の課金 |
| OpenSearch Service（ドメイン） | シャードを細かく制御する | 運用が必要 |
| RDS または Aurora の pgvector | 既に PostgreSQL を使っている、SQL と結合したい | pgvector 0.5.0 以上で HNSW |
| S3 Vectors | 大量で低頻度の検索、低コスト | ハイブリッド検索は不可、次元は 1〜4,096 |

設定でよく問われるのは次の点です。

- 次元はモデルと一致させます。Titan Text Embeddings V2 の既定は 1,024 です。一致しないと取り込みエラーになります。
- Knowledge Bases で OpenSearch のメタデータを使うなら、エンジンは `faiss` です。
- HNSW は速くて高精度ですがメモリを使います。pgvector では `ef_search` を上げると精度が上がり、遅くなります。

詳細: [ベクトルストア](../../services/genai-apps.md#vector-stores)、[OpenSearch](../../services/genai-apps.md#opensearch-vectors)、[pgvector](../../services/genai-apps.md#pgvector)、[S3 Vectors](../../services/genai-apps.md#s3-vectors)、[ベクトルインデックス](../../services/databases-specialized.md#vector-indexes)

### 1.1.8 多様なデータ型の取り込みと保存 {#skill-1-1-8}

原本は S3 に置き、用途に合わせてテキストや埋め込みに変換します。

| データ | 変換や取り込み |
|---|---|
| スキャン文書、PDF | Textract、Bedrock Data Automation |
| 音声 | Transcribe で文字にする |
| 動画や音声のストリーム | Kinesis Video Streams |
| 画像 | マルチモーダルの埋め込みモデル、Rekognition |
| 図や表を含む文書 | Knowledge Bases の BDA パーサーか FM パーサー |

ファイルサーバーから S3 へ大量に移すなら DataSync です。

詳細: [マネージド AI サービスの選び方](../../services/ai-managed-services.md#choosing)、[Bedrock Data Automation](../../services/genai-apps.md#bda)、[Nova と Titan](../../services/genai-apps.md#nova-titan)、[DataSync](../../services/migration.md#datasync)

### 1.1.9 Feature Store への取り込み {#skill-1-1-9}

フィーチャーグループには、レコード ID（`RecordIdentifierFeatureName`）とイベント時刻（`EventTimeFeatureName`）が必須です。

| 方法 | 使いどころ |
|---|---|
| `PutRecord` API | ストリームやバッチから 1 件ずつ |
| Spark コネクタ | 大量のバッチ |
| Data Wrangler / Canvas | 前処理の結果を出力する |

Kinesis のイベントを Lambda で集計し、`PutRecord` で書く構成が典型です。

詳細: [Feature Store](../../services/sagemaker.md#feature-store)

## タスク 1.2: データ変換、特徴量エンジニアリング、前処理を行う {#task-1-2}

### 1.2.1 AWS ツールによるデータ変換 {#skill-1-2-1}

| ツール | 向いている場面 |
|---|---|
| Glue（Spark） | 大規模な ETL をサーバーレスのコードで |
| Glue DataBrew | アナリストが画面で整形する。レシピは再利用できる |
| EMR の Spark | 既存の Spark コード、クラスターの細かい制御 |
| Data Wrangler | ML の前処理を画面で試し、Pipelines や Feature Store へ渡す |
| SageMaker Processing | ML のパイプラインにコードで組み込む |

「コードを書かずに」なら DataBrew か Data Wrangler です。ML の前処理の文脈なら Data Wrangler、分析担当の整形なら DataBrew を選びます。

詳細: [Data Wrangler と使い分け](../../services/sagemaker.md#data-wrangler)、[DataBrew](../../services/data-engineering.md#databrew)、[Processing](../../services/sagemaker.md#processing)、[EMR](../../services/data-engineering.md#emr)

### 1.2.2 特徴量の作成と管理 {#skill-1-2-2}

Feature Store は、学習と推論で同じ特徴量を使うための機能です。**学習と推論のずれ（training-serving skew）** を減らせます。

| ストア | 内容 | 用途 |
|---|---|---|
| オンライン | 最新のレコードだけ。低遅延。`GetRecord` で読む | リアルタイム推論 |
| オフライン | 全履歴を S3 に保存。Athena で検索できる | 学習、バッチ推論 |

オンラインストアだけの設定では履歴が残りません。後から学習に使うなら、オフラインストアも有効にします。`TtlDuration` を設定すると、期限を過ぎたレコードを削除できます。

詳細: [Feature Store](../../services/sagemaker.md#feature-store)

### 1.2.3 ストリーミングデータの変換 {#skill-1-2-3}

| 手段 | 動作 | 向いている場面 |
|---|---|---|
| Firehose の Lambda 変換 | 宛先に届く前にレコードを変換する | 軽い整形、配信が目的 |
| Lambda のイベントソースマッピング | Kinesis を読み、バッチで処理する | 1 件ごとの処理、短い集計 |
| Lambda のタンブリングウィンドウ | 0〜900 秒の枠で状態を持って集計する | シャードごとの短い集計 |
| Glue の Spark Streaming | マイクロバッチで処理する | Spark のコードをサーバーレスで |
| EMR の Spark Structured Streaming | Kinesis コネクタで読む。EMR 7.1.0 以降に同梱 | Spark のコードをクラスターで |
| Flink | 状態を持つ継続的な処理 | 複雑なウィンドウ、結合 |

Firehose の変換で返す `recordId` は入力と同じにします。`result` は `Ok`、`Dropped`、`ProcessingFailed` のいずれかです。

詳細: [Firehose の変換](../../services/streaming.md#firehose-transform)、[Lambda とストリーム](../../services/streaming.md#lambda-streams)、[タンブリングウィンドウ](../../services/lambda.md#esm-tumbling-window)、[Glue のジョブ](../../services/data-engineering.md#glue-jobs)、[Flink](../../services/data-engineering.md#flink)

### 1.2.4 特徴量エンジニアリング {#skill-1-2-4}

| 手法 | 例 | 使いどころ |
|---|---|---|
| 正規化（最小最大） | 範囲 0〜100 で 25 → 0.25 | 範囲を 0〜1 に揃える |
| 標準化 | 平均 50、標準偏差 10 で 70 → 2.0 | 線形モデルや k-means の前 |
| 対数変換 | 10、1,000、100,000 → 1、3、5 | 右に長い分布（年収など） |
| ビニング | 年齢を 0-19、20-39 に分ける | 非線形の関係を単純にする |
| 特徴量の分割 | 日時 → 曜日、時間帯 | 周期を捉える |
| ワンホット | 赤、青、緑 → 3 列 | 順序のないカテゴリ |

落とし穴はデータ漏えいです。全データの平均で標準化してから分割すると、テストの情報が学習に混ざります。学習データだけで計算し、同じ値を検証とテストに使います。

k-means や k-NN は尺度を揃えないと、桁の大きい列が結果を支配します。XGBoost などの木モデルは揃えなくても動きます。

詳細: [特徴量エンジニアリング](../../services/ai-fundamentals.md#feature-engineering)

### 1.2.5 埋め込みモデルの設定と利用 {#skill-1-2-5}

| 観点 | 判断 |
|---|---|
| モダリティ | テキストは Titan Text Embeddings V2、画像も扱うなら Titan Multimodal Embeddings G1 や Nova Multimodal Embeddings |
| 次元数 | 大きいと精度が上がる傾向で、保存と検索のコストが増える。V2 は 1,024、512、256 |
| 入力の上限 | V2 は 8,192 トークン、50,000 文字 |
| 言語 | 多言語なら対応モデルを確認する |
| 変更 | モデルを変えると全データの再埋め込みが必要 |

100 万チャンクで float32 の場合、生データの大きさは 1,024 次元で約 4.1 GB、256 次元で約 1.0 GB です。

埋め込みの API は RPM で制限されます。大量に生成するなら、SQS と Lambda で流量を制御するか、バッチ推論を使います。

詳細: [埋め込みの選び方](../../services/genai-apps.md#embedding-selection)、[Nova と Titan](../../services/genai-apps.md#nova-titan)、[埋め込みとベクトル](../../services/ai-fundamentals.md#embeddings)

### 1.2.6 高度なテキストの前処理 {#skill-1-2-6}

| 処理 | 内容 |
|---|---|
| トークン化 | 文を単語やトークンに分ける |
| 正規化 | 大文字小文字や全角半角を揃える |
| TF-IDF | 文書で多く、全体で少ない語の重みを高くする |
| ドメイン固有の拡張 | 専門用語の同義語で学習データを増やす |

BlazingText の Word2vec で単語埋め込みを作れます。医療の略語のように一般のモデルが知らない語は、同義語を足して学習データを増やします。

詳細: [テキストの前処理](../../services/ai-fundamentals.md#text-preprocessing)、[組み込みアルゴリズム](../../services/sagemaker.md#built-in-algorithms)

### 1.2.7 RAG 向けの文書の準備 {#skill-1-2-7}

[![S3 の文書を解析、チャンク化、埋め込みしてベクトルストアに保存する RAG の構成](../../assets/diagrams/genai-apps-rag.png)](../../assets/diagrams/genai-apps-rag.png)

| チャンク戦略 | 向いている文書 | 注意 |
|---|---|---|
| 既定 | まず試す。約 300 トークン | |
| 固定サイズ | 均質な文書。`maxTokens` と `overlapPercentage` を指定 | 文の途中で切れることがある |
| 階層 | マニュアル、規定集。子で検索し親を返す | 返る件数が指定より少なくなる |
| セマンティック | 話題が変わる文書 | FM を使うので追加料金 |
| なし + Lambda | FAQ など独自の構造 | カスタム変換と組み合わせる |

メタデータは、文書と同じ場所に `<ファイル名>.metadata.json` として置きます。部署や更新日で検索時に絞り込めます。

表や図を含む PDF は、既定のパーサーでは内容を取り出せません。BDA か FM のパーサーを選びます。

詳細: [取り込みの流れ](../../services/genai-apps.md#kb-ingestion)、[チャンク化](../../services/genai-apps.md#chunking)、[メタデータ](../../services/genai-apps.md#kb-metadata)

### 1.2.8 マスキング、秘匿化、匿名化 {#skill-1-2-8}

データがどの段階にあるかで、手段を選びます。

| 段階 | 手段 | できること |
|---|---|---|
| S3 にある機密データの発見 | Macie | 検出と報告。マスクはしない |
| ETL の中 | Glue の Detect PII 変換 | 検出、文字列への置換、部分的な置換、SHA-256 ハッシュ |
| 画面での整形 | DataBrew の PII 手順 | 置換、シャッフル、決定的または確率的な暗号化、NULL 化や削除、マスク、ハッシュ |
| テキスト | Comprehend の PII | 検出と位置の特定。マスクは非同期ジョブで行う |
| FM の入出力 | Guardrails の機密情報フィルター | `BLOCK` か `ANONYMIZE`。組み込みの PII と正規表現 |
| ログ | CloudWatch Logs のデータ保護 | ログの中のマスク |

**Comprehend の PII は英語とスペイン語のテキストが対象です。** 日本語のデータには、Guardrails の機密情報フィルターや Glue の正規表現などを検討します。

元の値に戻す必要があるなら決定的または確率的な暗号化、結合のキーとして使いたいが値を隠すならハッシュや決定的な暗号化を選びます。

詳細: [Macie](../../services/threat-detection.md#macie)、[Comprehend](../../services/ai-managed-services.md#comprehend)、[Guardrails のフィルター](../../services/ai.md#guardrail-filters)、[サニタイズとマスキング](../../services/secrets.md#sanitization-masking)、[データの保護](../../services/genai-apps.md#data-protection)

### 1.2.9 FM のカスタマイズ向けのデータ準備 {#skill-1-2-9}

| 手法 | 必要なデータ |
|---|---|
| 教師ありファインチューニング | 入力と出力の組 |
| 強化ファインチューニング | プロンプトと報酬関数（Lambda）。呼び出しログも使える |
| 蒸留 | プロンプト。教師モデルの応答で生徒モデルを調整する |
| 継続的な事前学習 | ラベルのない大量のデータ |

形式は `.jsonl` で、1 行が 1 件です。S3 に置きます。会話形式では `schemaVersion: bedrock-conversation-2024` を使います。

現在の Bedrock の一覧にあるのは教師あり、強化、蒸留の 3 つです。継続的な事前学習はガイドに残る用語なので、ラベルなしのデータで学習を続ける手法として押さえます。

詳細: [モデルカスタマイズ](../../services/genai-apps.md#customization)、[データの準備](../../services/genai-apps.md#fine-tuning-data)、[方法の比較](../../services/ai-fundamentals.md#customization-options)

## タスク 1.3: データ品質を検証し、バイアスを管理する {#task-1-3}

### 1.3.1 データ品質の検証 {#skill-1-3-1}

| ツール | 書き方 | 向いている場面 |
|---|---|---|
| Glue Data Quality | DQDL | パイプラインの中で検査し、不良レコードを隔離する |
| DataBrew | ルールセットとプロファイルジョブ | 画面で分布や欠損を確認する |

DQDL の例は `IsComplete "order_id"` や `Completeness "email" > 0.95` です。ETL ジョブに入れると、ロードの前に悪いデータを止められます。

詳細: [Glue Data Quality](../../services/data-engineering.md#glue-data-quality)、[DataBrew](../../services/data-engineering.md#databrew)

### 1.3.2 ラベル付けとアノテーション {#skill-1-3-2}

!!! note "Ground Truth の提供状況"
    SageMaker Ground Truth は新規顧客の受付を終了しています。公式の移行先の案内はありません。試験には役割の理解が必要です。

Ground Truth は、画像、テキスト、動画、3D 点群のラベル付けを行う機能です。作業者はベンダーかプライベートのワークフォースから選びます。

自動ラベル付けはアクティブラーニングです。信頼度の高いデータはモデルが、低いデータは人がラベルを付けます。データが多いほど効果があります。

ラベルの誤りには、複数人での確認と判定者間の一致度の確認で対応します。

詳細: [Ground Truth](../../services/sagemaker.md#ground-truth)、[データ品質](../../services/ai-fundamentals.md#data-quality)

### 1.3.3 データのバイアスの特定と緩和 {#skill-1-3-3}

!!! note "Clarify の提供状況"
    SageMaker Clarify は新規顧客の受付を終了しています。代替は、指標の自前計算、SHAP の直接利用、FM の評価には Bedrock Evaluations です。Bedrock Evaluations は表データのバイアス検出の代わりにはなりません。

| 原因 | 緩和の手段 |
|---|---|
| 特定の集団が少ない | データの追加、データ拡張、再サンプリング |
| 収集が偏っている、順序に依存する | シャッフル、層化分割 |
| 判定者の偏見 | 複数人のレビュー |
| 多数派に最適化される | 重み付け、集団ごとの評価 |

学習前の指標を押さえます。CI は集団の人数の差で、800 人と 200 人なら (800−200)/1000 = 0.6 です。DPL は陽性ラベルの割合の差で、0.6 と 0.3 なら 0.3 です。

時系列は未来のデータが混ざらないよう、シャッフルせず時間順に分けます。

詳細: [バイアス指標](../../services/sagemaker.md#clarify-metrics)、[Clarify](../../services/sagemaker.md#clarify)、[バイアスと公平性](../../services/ai-fundamentals.md#fairness)、[データの分割](../../services/ai-fundamentals.md#ml-lifecycle)

### 1.3.4 マルチモーダルデータの分布の最適化 {#skill-1-3-4}

テキストや画像でも、属性ごとに件数と結果を集計すれば、表データと同じ考え方でバイアス指標を計算できます。

例えば、画像データの撮影地域ごとに枚数とラベルの割合を集計します。CI が大きければ少ない地域のデータを追加し、拡張します。DPL が大きければラベルの付け方を確認します。

| データ | 集計の例 |
|---|---|
| 数値 | 年齢層ごとの件数と陽性率 |
| テキスト | 言語や話題ごとの件数と陽性率 |
| 画像 | 撮影条件や地域ごとの枚数と陽性率 |

詳細: [マルチモーダルでの考え方](../../services/sagemaker.md#clarify-metrics)

### 1.3.5 クラス不均衡の解消 {#skill-1-3-5}

| 手法 | 内容 | 注意 |
|---|---|---|
| ランダムオーバーサンプリング | 少数クラスを複製する | 過学習しやすい |
| ランダムアンダーサンプリング | 多数クラスを減らす | 情報が減る |
| SMOTE | 近傍の補間で少数クラスを合成する | 表データ向け |
| クラスの重み付け | 少数クラスの誤りを重くする | データは変えない |
| データ拡張 | 画像の回転、テキストの言い換え | 画像とテキストで有効 |

Data Wrangler の Balance data で、オーバーサンプリング、アンダーサンプリング、SMOTE を実行できます。

再サンプリングは学習データだけに適用します。評価には accuracy を使わず、適合率、再現率、PR 曲線を見ます。

詳細: [データ品質と不均衡](../../services/ai-fundamentals.md#data-quality)、[分類の指標](../../services/ai-fundamentals.md#classification-metrics)

### 1.3.6 AI の学習データの完全性の検証 {#skill-1-3-6}

FM の学習データは、誤りも有害な内容もそのまま学習されます。

| 確認項目 | 方法の例 |
|---|---|
| 質問と回答の組の正しさ | スキーマの検証、サンプルの人手確認 |
| 有害な内容 | Guardrails の `ApplyGuardrail` で検査する |
| 機密情報 | Macie、Comprehend で検出してマスクする |
| データの出所 | 出所の管理でポイズニングを防ぐ |
| 代表性 | 本番の質問に似ているか確認する |

`ApplyGuardrail` はモデルを呼ばずに内容を検査できるので、学習データの検査にも使えます。

詳細: [データの準備](../../services/genai-apps.md#fine-tuning-data)、[ApplyGuardrail](../../services/ai.md#apply-guardrail)、[プロンプトのリスク](../../services/ai-fundamentals.md#prompt-engineering)

### 1.3.7 データのクリーニング {#skill-1-3-7}

| 問題 | 対応 | 例 |
|---|---|---|
| 欠損 | 平均、中央値、最頻値で補完。行や列の削除。別モデルで推定 | 外れ値がある年収は中央値で補完する |
| 外れ値 | 検出して確認。上限で丸める、除外する | 四分位範囲の 1.5 倍の外を確認する |
| 完全な重複 | 削除する | 同じ ID の行 |
| あいまいな重複 | Lake Formation の FindMatches | 表記が違う同じ顧客 |

FindMatches は ML の変換で、共通の ID がなく値も完全には一致しないレコードを照合します。Glue のジョブで作成して実行します。

SageMaker の Random Cut Forest は、ラベルなしで異常なレコードを見つけられます。

詳細: [データ品質](../../services/ai-fundamentals.md#data-quality)、[組み込みアルゴリズム](../../services/sagemaker.md#built-in-algorithms)

## 確認問題 {#self-check}

??? question "問1: 列が 200 あるクリックログを CSV で S3 に保存しています。学習前の集計で毎回数列しか使わないのに、Athena のスキャン料金が高額です。最も効果の大きい対策は何ですか？"
    Parquet に変換し、日付でパーティションを切ります。列指向なので必要な列だけ読めて、パーティションで不要な範囲も読みません。インスタンスを増やす案は、スキャン量を減らさないので効果がありません。

??? question "問2: 不正検知のリアルタイム推論で「直近 1 時間の取引回数」を使い、同じ特徴量で再学習もしたいです。学習と推論のずれも防ぎたいです。どう構成しますか？"
    Kinesis のイベントを Managed Service for Apache Flink のスライディングウィンドウで集計し、Feature Store に `PutRecord` で書きます。オンラインストアとオフラインストアの両方を有効にします。推論は `GetRecord` で最新の値を読み、学習はオフラインストアの履歴を Athena で読みます。

??? question "問3: Knowledge Bases で OpenSearch Serverless を使っています。ファイルごとの `.metadata.json` を用意したのに、フィルターが効きません。最初に何を確認しますか？"
    インデックスのエンジンです。`nmslib` だとメタデータファイルが無視されるので、`faiss` のベクトルインデックスを作り、それを指定する新しいナレッジベースを作ります。ファイル名が元の文書と拡張子まで揃っているかも確認します。

??? question "問4: 表が多い製品マニュアルの RAG で、表の内容を聞くと答えられません。章単位の広い文脈も回答に使いたいです。何を変えますか？"
    パーサーを BDA か FM に変えて表を取り出し、チャンク戦略を階層にします。子チャンクで検索し、親チャンクで広い文脈を返せます。パーサーを変えるとコストが増える点は確認します。

??? question "問5: 陽性が 1% のデータで学習したモデルの accuracy は 99% ですが、陽性を 1 件も検出できません。データと評価をどう変えますか？"
    学習データだけに SMOTE や再サンプリング、またはクラスの重み付けを適用します。評価は再現率、適合率、PR 曲線で行います。テストデータは本番に近い分布のまま残します。

??? question "問6: 日本語の問い合わせ履歴を FM のファインチューニングに使います。氏名と電話番号を除き、誤った回答も避けたいです。Comprehend の PII で一括マスクする案の問題点と代案は？"
    Comprehend の PII の対象は英語とスペイン語なので、日本語のデータには使えません。代案は、Guardrails の機密情報フィルターと `ApplyGuardrail` の利用や、電話番号の正規表現です。質問と回答の組はサンプルの人手確認で検証し、形式は JSONL で検査します。
