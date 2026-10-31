# マネージド AI サービスの問題集

対象の解説: [マネージド AI サービス](../../../services/ai-managed-services.md)、[SageMaker AI](../../../services/sagemaker.md)

### 問1 {#q1}

顧客のレビューを肯定、否定に分類し、製品名も抽出します。モデルの学習はしません。どれを選びますか。

- A. Textract
- B. Rekognition
- C. Comprehend
- D. Polly

??? success "答えと解説"
    **正解: C**

    Comprehend は感情分析と固有表現の抽出を提供します。

    - A: 誤り。文書から文字と表を取り出すサービス。
    - B: 誤り。画像と動画の分析のサービス。
    - C: 正しい。
    - D: 誤り。テキストを音声にするサービス。

    **スキル:** [マネージド AI](../domain2.md#t2-2-managed-ai) / **参照:** [Amazon Comprehend](../../../services/ai-managed-services.md#comprehend)

### 問2 {#q2}

Web の記事をテキストから音声に変えて配信します。どれを選びますか。

- A. Translate
- B. Transcribe
- C. Lex
- D. Polly

??? success "答えと解説"
    **正解: D**

    Polly はテキストを音声にします。

    - A: 誤り。言語を翻訳するサービス。
    - B: 誤り。音声をテキストにするサービスで、逆。
    - C: 誤り。会話のボットを作るサービス。
    - D: 正しい。

    **スキル:** [マネージド AI](../domain2.md#t2-2-managed-ai) / **参照:** [Amazon Polly](../../../services/ai-managed-services.md#polly)

### 問3 {#q3}

コールセンターの録音を文字に起こして、検索できるようにします。どれを選びますか。

- A. Transcribe
- B. Rekognition
- C. Comprehend
- D. Polly

??? success "答えと解説"
    **正解: A**

    Transcribe は音声をテキストに変換します。

    - A: 正しい。
    - B: 誤り。画像と動画の分析のサービス。
    - C: 誤り。テキストが対象で、音声を直接は扱わない。
    - D: 誤り。テキストから音声を作るサービス。

    **スキル:** [マネージド AI](../domain2.md#t2-2-managed-ai) / **参照:** [Amazon Transcribe](../../../services/ai-managed-services.md#transcribe)

### 問4 {#q4}

スキャンした請求書の PDF から、表とキーと値の組を抽出します。OCR のモデルは作りたくありません。どれを選びますか。

- A. SageMaker AI
- B. Textract
- C. Comprehend
- D. Lex

??? success "答えと解説"
    **正解: B**

    Textract は文書から文字、表、フォームを抽出します。

    - A: 誤り。作りたくないという要件に反する。
    - B: 正しい。
    - C: 誤り。テキストの分析で、スキャン画像の抽出ではない。
    - D: 誤り。会話のボットのサービス。

    **スキル:** [マネージド AI](../domain2.md#t2-2-managed-ai) / **参照:** [Amazon Textract](../../../services/ai-managed-services.md#textract)

### 問5 {#q5}

投稿された画像に不適切な内容がないかを、モデルを学習せずに自動で判定します。どれを選びますか。

- A. Macie
- B. Comprehend
- C. SageMaker AI
- D. Rekognition

??? success "答えと解説"
    **正解: D**

    Rekognition は画像と動画の分析を提供し、モデレーションにも使えます。

    - A: 誤り。S3 の機密データの検出で、画像の内容の判定ではない。
    - B: 誤り。テキストが対象。
    - C: 誤り。独自のモデルを作るサービスで、学習しないという要件に合わない。
    - D: 正しい。

    **スキル:** [マネージド AI](../domain2.md#t2-2-managed-ai) / **参照:** [Amazon Rekognition](../../../services/ai-managed-services.md#rekognition)

### 問6 {#q6}

製品マニュアルの英語のテキストを日本語にします。どれを選びますか。

- A. Comprehend
- B. Translate
- C. Polly
- D. Lex

??? success "答えと解説"
    **正解: B**

    Translate はニューラル機械翻訳のサービスです。

    - A: 誤り。テキストの分析で、翻訳はしない。
    - B: 正しい。
    - C: 誤り。音声の合成で、翻訳ではない。
    - D: 誤り。会話のボットのサービス。

    **スキル:** [マネージド AI](../domain2.md#t2-2-managed-ai) / **参照:** [Amazon Translate](../../../services/ai-managed-services.md#translate)

### 問7 {#q7}

問い合わせの窓口で、音声とテキストで予約を受け付ける会話型のボットを作ります。どれを選びますか。

- A. Lex
- B. Transcribe
- C. Polly
- D. Comprehend

??? success "答えと解説"
    **正解: A**

    Lex はインテントとスロットで会話型のボットを作ります。

    - A: 正しい。
    - B: 誤り。文字起こしで、意図を理解して応答しない。
    - C: 誤り。テキストを音声にするサービスで、会話を理解しない。
    - D: 誤り。分析で、会話を管理しない。

    **スキル:** [マネージド AI](../domain2.md#t2-2-managed-ai) / **参照:** [Amazon Lex](../../../services/ai-managed-services.md#lex)

### 問8 {#q8}

自社の独自のデータと特徴量で需要予測のモデルを作り、学習からデプロイまで管理します。どれを選びますか。

- A. Polly
- B. Comprehend のカスタム分類
- C. SageMaker AI
- D. Translate

??? success "答えと解説"
    **正解: C**

    独自のモデルを作る要件があるときは SageMaker AI を選びます。

    - A: 誤り。音声の合成のサービス。
    - B: 誤り。テキストの分類で、需要予測の用途ではない。
    - C: 正しい。
    - D: 誤り。翻訳のサービス。

    **スキル:** [マネージド AI](../domain2.md#t2-2-managed-ai) / **参照:** [SageMaker AI](../../../services/sagemaker.md)

### 問9 {#q9}

外国語のコールの録音を、日本語の要約の分析につなげます。処理の順に正しいサービスの組み合わせはどれですか。

- A. Polly、Translate、Comprehend の順
- B. Comprehend、Transcribe、Translate の順
- C. Transcribe、Translate、Comprehend の順
- D. Textract、Rekognition、Lex の順

??? success "答えと解説"
    **正解: C**

    音声をテキストに、翻訳して、分析します。

    - A: 誤り。最初に音声を作ることになり、順番が合わない。
    - B: 誤り。テキストがない段階で分析はできない。
    - C: 正しい。
    - D: 誤り。音声を扱わない。

    **スキル:** [マネージド AI](../domain2.md#t2-2-managed-ai) / **参照:** [Amazon Transcribe](../../../services/ai-managed-services.md#transcribe)、[Amazon Translate](../../../services/ai-managed-services.md#translate)、[Amazon Comprehend](../../../services/ai-managed-services.md#comprehend)

### 問10 {#q10}

専用のサービスを選ぶ判断として適切なものを選んでください。（2つ選択）

- A. 音声の文字起こしのために、EC2 に OSS を入れて運用を続ける
- B. 翻訳のために、SageMaker AI で翻訳モデルを一から学習させる
- C. 動画の中の人物の検出に、Rekognition を使う
- D. 請求書の抽出に、学習済みの Textract を使う
- E. 感情分析のために、Lambda に自作の辞書を載せて保守する

??? success "答えと解説"
    **正解: C, D**

    機能ごとの専用サービスがあるなら、モデルを自分で作りません。

    - A: 誤り。専用の Transcribe があり、運用負荷も大きい。
    - B: 誤り。専用の Translate がある。
    - C: 正しい。
    - D: 正しい。
    - E: 誤り。専用の Comprehend がある。

    **スキル:** [マネージド AI](../domain2.md#t2-2-managed-ai) / **参照:** [Amazon Textract](../../../services/ai-managed-services.md#textract)、[Amazon Rekognition](../../../services/ai-managed-services.md#rekognition)
