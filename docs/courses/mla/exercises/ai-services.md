# AI サービスの問題集

対象の解説: [マネージド AI サービス](../../../services/ai-managed-services.md#choosing)、[Bedrock Data Automation](../../../services/genai-apps.md#bda)

### 問1 {#q1}

コールセンターの通話の録音を、検索できるテキストにして S3 に保存します。どのサービスを使いますか。

- A. Comprehend
- B. Kinesis Video Streams の HLS 配信
- C. Transcribe
- D. Polly

??? success "答えと解説"
    **正解: C**

    音声は Transcribe で文字にします。原本は S3 に残します。

    - A: 誤り。テキストの分析で、音声は扱いません。
    - B: 誤り。映像の配信で、文字起こしの機能ではありません。
    - C: 正しい。
    - D: 誤り。文字を音声にするサービスで、逆です。

    **スキル:** [1.1.8](../domain1.md#skill-1-1-8) / **参照:** [マネージド AI サービスの選び方](../../../services/ai-managed-services.md#choosing)

### 問2 {#q2}

オンプレミスのファイルサーバーから、スキャン文書を大量に S3 へ移します。移行の転送に使うサービスはどれですか。

- A. S3 Transfer Acceleration
- B. Firehose
- C. Storage Gateway の S3 File Gateway
- D. DataSync のエージェントとタスク

??? success "答えと解説"
    **正解: D**

    ファイルサーバーから S3 へ大量に移すなら DataSync です。

    - A: 誤り。インターネット経由のアップロードを速くする機能で、ファイルサーバーからの移行を管理しません。
    - B: 誤り。ストリームのレコードの配信で、ファイルサーバーの移行には向きません。
    - C: 誤り。オンプレミスから S3 をファイル共有として使い続ける選択で、一括の移行の第一候補ではありません。
    - D: 正しい。

    **スキル:** [1.1.8](../domain1.md#skill-1-1-8) / **参照:** [DataSync](../../../services/migration.md#datasync)

### 問3 {#q3}

図と表を含む文書と画像を、1 つのベクトルストアで意味検索します。埋め込みモデルの選択として適切なものはどれですか。

- A. テキスト専用の Titan Text Embeddings V2 だけで画像も埋め込む
- B. Nova Multimodal Embeddings
- C. Comprehend のエンティティ検出で画像をベクトルにする
- D. Rekognition の顔照合 API の結果を、テキスト検索に使う

??? success "答えと解説"
    **正解: B**

    画像も扱うなら Titan Multimodal Embeddings G1 や Nova Multimodal Embeddings のようなマルチモーダルのモデルを選びます。

    - A: 誤り。テキスト専用で、画像は扱えません。
    - B: 正しい。
    - C: 誤り。テキストの分析で、画像の埋め込みを作りません。
    - D: 誤り。顔の照合の結果で、文書の意味検索には使えません。

    **スキル:** [1.1.8](../domain1.md#skill-1-1-8) / **参照:** [Nova と Titan](../../../services/genai-apps.md#nova-titan)

### 問4 {#q4}

請求書を毎日 10 万枚処理し、決まった項目を確実に抽出します。出力の形式は固定で、再現性を重視します。どの選択が適切ですか。

- A. Textract の `AnalyzeExpense`
- B. 上位の FM に毎回プロンプトで抽出させる
- C. JumpStart の FM を自前の GPU でホストする
- D. SageMaker AI で OCR モデルを独自に学習する

??? success "答えと解説"
    **正解: A**

    決まった作業を大量に確実に行うなら、専用の AI サービスを選びます。

    - A: 正しい。
    - B: 誤り。トークンのコストがかさみ、出力も揺れやすくなります。
    - C: 誤り。運用の手間とコストが増えます。
    - D: 誤り。手間が最大で、決まった作業には過剰です。

    **スキル:** [2.1.4](../domain2.md#skill-2-1-4) / **参照:** [マネージド AI サービスと Bedrock](../../../services/ai-managed-services.md#vs-bedrock)

### 問5 {#q5}

自社の FM を選んで GPU の種類も細かく決め、VPC の中で運用します。多少の手間は問題ありません。どれを選びますか。

- A. Bedrock のオンデマンド
- B. Comprehend のカスタム分類とカスタムのエンティティ認識
- C. Lex のボット
- D. JumpStart の事前学習済みモデル

??? success "答えと解説"
    **正解: D**

    FM を自分のインスタンスで制御するなら JumpStart です。

    - A: 誤り。インスタンスを制御できません。
    - B: 誤り。用途が限られ、FM を制御する選択ではありません。
    - C: 誤り。対話の機能で、FM のインスタンスは制御できません。
    - D: 正しい。

    **スキル:** [2.1.4](../domain2.md#skill-2-1-4) / **参照:** [AI の 3 階層](../../../services/ai-managed-services.md#three-layers)、[選び方の比較](../../../services/sagemaker.md#choosing)

### 問6 {#q6}

自社の表データと独自のアルゴリズムで需要を予測します。制御を最大にし、運用の手間は受け入れます。どの選択ですか。

- A. SageMaker AI で独自に学習する
- B. Translate
- C. Personalize
- D. Bedrock の FM

??? success "答えと解説"
    **正解: A**

    独自の表データと独自のアルゴリズムには、SageMaker AI での独自の学習が合います。

    - A: 正しい。
    - B: 誤り。翻訳のサービスです。
    - C: 誤り。レコメンド向けのマネージドのサービスです。
    - D: 誤り。生成や要約に向き、独自のアルゴリズムは動かせません。

    **スキル:** [2.1.4](../domain2.md#skill-2-1-4) / **参照:** [選び方の比較](../../../services/sagemaker.md#choosing)

### 問7 {#q7}

製品レビューの文章から、感情と製品名などの固有表現を取り出します。モデルの学習や運用はしたくありません。どのサービスですか。

- A. Textract
- B. Comprehend
- C. Bedrock の FM に毎回プロンプトで抽出させる
- D. SageMaker AI の BlazingText で分類モデルを学習する

??? success "答えと解説"
    **正解: B**

    文の意味を扱うのは Comprehend です。Textract は文書の文字を扱います。

    - A: 誤り。文書の文字や表を抽出するサービスです。
    - B: 正しい。
    - C: 誤り。実現できますが、決まった作業には専用のサービスより費用がかさみ、出力も揺れやすくなります。
    - D: 誤り。学習と運用の手間がかかり、要件に合いません。

    **スキル:** [2.1.8](../domain2.md#skill-2-1-8) / **参照:** [紛らわしい組み合わせ](../../../services/ai-managed-services.md#confusing-pairs)

### 問8 {#q8}

SNS に投稿された画像から不適切な内容を検出します。どのサービスですか。

- A. Transcribe
- B. Comprehend
- C. Rekognition
- D. Textract

??? success "答えと解説"
    **正解: C**

    写真や動画は Rekognition です。文書は Textract を使います。

    - A: 誤り。音声の文字起こしです。
    - B: 誤り。テキストの分析です。
    - C: 正しい。
    - D: 誤り。文書の文字の抽出です。

    **スキル:** [2.1.8](../domain2.md#skill-2-1-8) / **参照:** [紛らわしい組み合わせ](../../../services/ai-managed-services.md#confusing-pairs)

### 問9 {#q9}

次の業務とサービスの組み合わせとして正しいものを選んでください。（2つ選択）

- A. 問い合わせのチャットボットを作る: Rekognition
- B. EC サイトの閲覧履歴から商品を推薦する: Personalize
- C. 英語のマニュアルを日本語にする: Polly
- D. 紙の請求書から項目を抽出する: Transcribe
- E. 電子カルテのテキストから病名や薬を抽出する: Comprehend Medical

??? success "答えと解説"
    **正解: B, E**

    医療のテキストは Comprehend Medical、レコメンドは Personalize です。

    - A: 誤り。チャットボットは Lex です。
    - B: 正しい。
    - C: 誤り。翻訳は Translate です。Polly は音声合成です。
    - D: 誤り。文書の抽出は Textract です。
    - E: 正しい。

    **スキル:** [2.1.8](../domain2.md#skill-2-1-8) / **参照:** [選び方](../../../services/ai-managed-services.md#choosing)

### 問10 {#q10}

FHIR 形式の医療データを、FHIR の API で保存、検索して分析します。データストアの運用はなるべく任せます。どのサービスですか。

- A. HealthLake
- B. Comprehend の一般のテキスト分析の API
- C. Comprehend Medical
- D. S3 と Glue カタログに FHIR の JSON をそのまま置く

??? success "答えと解説"
    **正解: A**

    FHIR での医療データには HealthLake を使います。

    - A: 正しい。
    - B: 誤り。一般のテキスト分析で、FHIR のデータの保存はしません。
    - C: 誤り。医療のテキストから情報を抽出するサービスで、FHIR のデータストアではありません。
    - D: 誤り。保存はできますが、FHIR の検索や API を自分で作ることになります。

    **スキル:** [2.1.8](../domain2.md#skill-2-1-8) / **参照:** [HealthLake](../../../services/ai-managed-services.md#healthlake)
