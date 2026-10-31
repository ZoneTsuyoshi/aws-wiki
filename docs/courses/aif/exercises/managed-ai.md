# マネージド AI サービスの問題集

対象の解説: [マネージド AI サービス](../../../services/ai-managed-services.md)

### 問1 {#q1}

コールセンターの通話の録音を文字にしたいと考えています。適切なサービスはどれですか。

- A. Amazon Translate
- B. Amazon Transcribe
- C. Amazon Textract
- D. Amazon Polly

??? success "答えと解説"
    **正解: B**

    音声を文字にするのは Transcribe です。

    - A: 誤り。テキストを別の言語に翻訳するサービスです。
    - B: 正しい。
    - C: 誤り。文書から文字や表を取り出すサービスで、音声は扱いません。
    - D: 誤り。文字を音声にするサービスで、向きが逆です。

    **スキル:** [1.2.5](../domain1.md#obj-1-2-5) / **参照:** [Amazon Transcribe](../../../services/ai-managed-services.md#transcribe)

### 問2 {#q2}

ニュース記事を自然な音声で読み上げるアプリを作ります。適切なサービスはどれですか。

- A. Amazon Lex
- B. Amazon Comprehend
- C. Amazon Transcribe
- D. Amazon Polly

??? success "答えと解説"
    **正解: D**

    テキストを音声にするのは Polly です。

    - A: 誤り。会話のインターフェイスを作るサービスです。
    - B: 誤り。テキストの意味を分析するサービスです。
    - C: 誤り。音声を文字にするサービスで、向きが逆です。
    - D: 正しい。

    **スキル:** [1.2.5](../domain1.md#obj-1-2-5) / **参照:** [Amazon Polly](../../../services/ai-managed-services.md#polly)

### 問3 {#q3}

商品レビューが肯定的か否定的かを判定し、レビューに含まれる人名なども取り出したいと考えています。適切なサービスはどれですか。

- A. Amazon Comprehend
- B. Amazon Rekognition
- C. Amazon Personalize
- D. Amazon Textract

??? success "答えと解説"
    **正解: A**

    感情や固有表現の抽出は Comprehend の機能です。

    - A: 正しい。
    - B: 誤り。画像と動画を分析するサービスです。
    - C: 誤り。行動データからおすすめを作るサービスです。
    - D: 誤り。文書から文字を取り出すサービスで、文の意味は分析しません。

    **スキル:** [1.2.5](../domain1.md#obj-1-2-5) / **参照:** [Amazon Comprehend](../../../services/ai-managed-services.md#comprehend)

### 問4 {#q4}

ホテル予約の手続きを進めるチャットボットを作ります。利用者の目的を判定し、日付や人数を聞き返します。適切なサービスはどれですか。

- A. Amazon Polly
- B. Amazon Transcribe
- C. Amazon Lex
- D. Amazon Translate

??? success "答えと解説"
    **正解: C**

    Lex はインテントとスロットで対話を進める会話インターフェイスを作ります。

    - A: 誤り。音声への変換だけを担当し、対話の理解はしません。
    - B: 誤り。文字起こしのサービスで、手続きの対話は作れません。
    - C: 正しい。
    - D: 誤り。翻訳のサービスで、インテントの判定はしません。

    **スキル:** [1.2.5](../domain1.md#obj-1-2-5) / **参照:** [Amazon Lex](../../../services/ai-managed-services.md#lex)

### 問5 {#q5}

スキャンした請求書から、表の内容と合計金額を取り出したいと考えています。適切なサービスはどれですか。

- A. Amazon Comprehend
- B. Amazon Textract
- C. Amazon Rekognition
- D. Amazon Transcribe

??? success "答えと解説"
    **正解: B**

    文書から文字、表、フォームを取り出すのは Textract で、請求書には `AnalyzeExpense` があります。

    - A: 誤り。既にテキストになった文の意味を分析するサービスで、スキャンは読めません。
    - B: 正しい。
    - C: 誤り。写真や動画の分析に向くサービスで、文書の表の構造は扱いません。
    - D: 誤り。音声を文字にするサービスです。

    **スキル:** [1.2.5](../domain1.md#obj-1-2-5) / **参照:** [Amazon Textract](../../../services/ai-managed-services.md#textract)

### 問6 {#q6}

自社の表データで独自のモデルを学習し、デプロイから監視まで管理したいと考えています。適切なサービスはどれですか。

- A. Amazon SageMaker AI
- B. Amazon Comprehend
- C. Amazon Personalize
- D. Amazon Bedrock Knowledge Bases

??? success "答えと解説"
    **正解: A**

    独自のモデルを作るなら SageMaker AI です。

    - A: 正しい。
    - B: 誤り。学習済みの NLP 機能を中心に呼ぶサービスで、表データのモデルは作りません。
    - C: 誤り。レコメンドに特化したサービスで、任意の表データのモデルの管理はしません。
    - D: 誤り。文書を検索して答える RAG の機能で、表データのモデルは学習しません。

    **スキル:** [1.2.5](../domain1.md#obj-1-2-5) / **参照:** [選び方の比較](../../../services/sagemaker.md#choosing)

### 問7 {#q7}

英語の通話の録音を日本語の文章にして、顧客の感情を分析します。処理の順番として正しいものはどれですか。

- A. Polly、Translate、Comprehend
- B. Translate、Transcribe、Comprehend
- C. Comprehend、Transcribe、Translate
- D. Transcribe、Translate、Comprehend

??? success "答えと解説"
    **正解: D**

    音声を文字にし、翻訳し、感情を分析します。

    - A: 誤り。Polly は文字を音声にするサービスで、最初の段階に使えません。
    - B: 誤り。音声のままでは翻訳できないので、先に文字にします。
    - C: 誤り。感情の分析にはテキストが必要なので、最初には置けません。
    - D: 正しい。

    **スキル:** [1.2.5](../domain1.md#obj-1-2-5) / **参照:** [紛らわしい組み合わせ](../../../services/ai-managed-services.md#confusing-pairs)

### 問8 {#q8}

投稿された画像から、不適切な内容を自動で検出したいと考えています。この用途の分野と AWS の選択肢の組み合わせとして正しいものはどれですか。

- A. レコメンドで、Amazon Personalize
- B. 音声認識で、Amazon Transcribe
- C. コンピュータビジョンで、Amazon Rekognition
- D. 自然言語処理で、Amazon Bedrock Guardrails

??? success "答えと解説"
    **正解: C**

    画像と動画のモデレーションは Rekognition の機能です。

    - A: 誤り。おすすめを作るサービスです。
    - B: 誤り。音声を文字にするサービスです。
    - C: 正しい。
    - D: 誤り。画像の中身の分野は自然言語処理ではなく、Guardrails は FM の入出力を検査する機能です。

    **スキル:** [1.2.4](../domain1.md#obj-1-2-4) / **参照:** [Amazon Rekognition](../../../services/ai-managed-services.md#rekognition)

### 問9 {#q9}

動画配信サービスが、視聴履歴に基づいて利用者ごとのおすすめを表示したいと考えています。適切なサービスはどれですか。

- A. Amazon Comprehend
- B. Amazon Rekognition
- C. Amazon Personalize
- D. Amazon Bedrock Knowledge Bases

??? success "答えと解説"
    **正解: C**

    自社の行動データからレコメンドを作るのが Personalize です。

    - A: 誤り。テキストを分析するサービスです。
    - B: 誤り。画像と動画の中身を分析するサービスで、視聴履歴からのおすすめは作りません。
    - C: 正しい。
    - D: 誤り。文書を検索して答える RAG の機能で、視聴履歴からのおすすめは作りません。

    **スキル:** [1.2.4](../domain1.md#obj-1-2-4) / **参照:** [Amazon Personalize](../../../services/ai-managed-services.md#personalize)

### 問10 {#q10}

社内規定への質問に、文書に基づいて答えるアシスタントを新しく作ります。現在の AWS の選択肢として適切なものはどれですか。

- A. Amazon Polly
- B. Amazon Bedrock Knowledge Bases
- C. Amazon Translate
- D. Amazon Kendra の新しいインデックスを新規顧客として契約する

??? success "答えと解説"
    **正解: B**

    ナレッジベースの用途で、新規に作るなら Bedrock Knowledge Bases です。

    - A: 誤り。音声合成のサービスで、文書の検索はできません。
    - B: 正しい。
    - C: 誤り。翻訳のサービスで、質問応答はできません。
    - D: 誤り。Kendra は新規顧客を受け付けていません。公式は Bedrock の Managed Knowledge Base を案内しています。

    **スキル:** [1.2.4](../domain1.md#obj-1-2-4) / **参照:** [Knowledge Bases](../../../services/genai-apps.md#knowledge-bases)、[Amazon Kendra](../../../services/ai-managed-services.md#kendra)

### 問11 {#q11}

実世界の AI の活用例と分野の組み合わせとして正しいものを選んでください。（2つ選択）

- A. 視聴履歴からの作品の提案: 自然言語処理
- B. 会議の録音の文字起こし: コンピュータビジョン
- C. 不審なクレジットカード取引の検出: 不正検知
- D. 来月の店舗別の需要の見積もり: 予測
- E. 製品写真からの傷の発見: 音声認識

??? success "答えと解説"
    **正解: C, D**

    入力と出力の形から、どの分野かを見分けます。

    - A: 誤り。レコメンドの例です。
    - B: 誤り。音声認識の例です。
    - C: 正しい。
    - D: 正しい。
    - E: 誤り。コンピュータビジョンの例です。

    **スキル:** [1.2.4](../domain1.md#obj-1-2-4) / **参照:** [選び方の比較](../../../services/ai-managed-services.md#choosing)、[問題の種類](../../../services/ai-fundamentals.md#problem-types)

### 問12 {#q12}

新規に不正検知のモデルを作りたいと考えています。現在の AWS の選択肢として適切なものはどれですか。

- A. Amazon Fraud Detector を新規に契約する
- B. Amazon Comprehend
- C. Amazon Rekognition
- D. Amazon SageMaker AI

??? success "答えと解説"
    **正解: D**

    Fraud Detector は新規顧客の受付を終えており、公式は代替として SageMaker AI、AutoGluon、AWS WAF を挙げています。

    - A: 誤り。新規顧客を受け付けていません。
    - B: 誤り。テキストを分析するサービスで、不正検知のモデルは作りません。
    - C: 誤り。画像と動画を分析するサービスで、取引の不正検知のモデルは作りません。
    - D: 正しい。

    **スキル:** [1.2.4](../domain1.md#obj-1-2-4) / **参照:** [Amazon Fraud Detector](../../../services/ai-managed-services.md#fraud-detector)

### 問13 {#q13}

請求書の項目を毎月大量に、決まった形式で確実に抽出します。Bedrock の FM ではなく、マネージド AI サービスを選ぶ理由はどれですか。

- A. 決まった作業の出力の形式と再現性が安定している
- B. トークン単位で課金されるので、常に費用が安くなる
- C. プロンプトの設計と評価が中心の開発になる
- D. 自由な指示で自由な形式の出力を作れる

??? success "答えと解説"
    **正解: A**

    決まった形式の処理を大量に確実に行うなら、マネージド AI サービスが向きます。

    - A: 正しい。
    - B: 誤り。マネージド AI サービスの料金はリクエストやページの単位です。
    - C: 誤り。それは FM の特徴で、マネージド AI サービスは API を呼ぶのが中心です。
    - D: 誤り。それは FM の強みです。

    **スキル:** [2.1.2](../domain2.md#obj-2-1-2) / **参照:** [マネージド AI サービスと Bedrock](../../../services/ai-managed-services.md#vs-bedrock)
