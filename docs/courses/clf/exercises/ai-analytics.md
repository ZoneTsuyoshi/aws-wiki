# AI/ML と分析 の問題集

対象の解説: [マネージド AI サービス](../../../services/ai-managed-services.md)、[SageMaker AI](../../../services/sagemaker.md)、[ストリーミングと分析](../../../services/streaming.md)、[データエンジニアリング](../../../services/data-engineering.md)

### 問1 {#q1}

データサイエンティストが、独自のモデルを作り、学習してデプロイしたいと考えています。最も適切なサービスはどれですか。

- A. Amazon Rekognition
- B. Amazon SageMaker AI
- C. Amazon Translate
- D. Amazon Polly

??? success "答えと解説"
    **正解: B**

    SageMaker AI はモデルの作成、学習、デプロイを行います。

    - A: 誤り。画像や動画を分析するサービス。
    - B: 正しい。
    - C: 誤り。言語を翻訳するサービス。
    - D: 誤り。文字を音声に変換するサービス。

    **スキル:** [AI/ML のサービス](../domain3.md#t3-7-ai-ml) / **参照:** [開発環境](../../../services/sagemaker.md#studio)

### 問2 {#q2}

Web サイトの問い合わせに答えるチャットボットを作りたいと考えています。最も適切なサービスはどれですか。

- A. Amazon Comprehend
- B. Amazon Transcribe
- C. Amazon Textract
- D. Amazon Lex

??? success "答えと解説"
    **正解: D**

    Lex はチャットボットや音声の対話を作ります。

    - A: 誤り。テキストの感情やエンティティを抽出するサービス。
    - B: 誤り。音声を文字に変換するサービス。
    - C: 誤り。文書から文字や表を抽出するサービス。
    - D: 正しい。

    **スキル:** [AI/ML のサービス](../domain3.md#t3-7-ai-ml) / **参照:** [Amazon Lex](../../../services/ai-managed-services.md#lex)

### 問3 {#q3}

ニュース記事の文章を読み上げる音声を作りたいと考えています。最も適切なサービスはどれですか。

- A. Amazon Transcribe
- B. Amazon Lex
- C. Amazon Polly
- D. Amazon Translate

??? success "答えと解説"
    **正解: C**

    Polly は文字を音声に変換します。

    - A: 誤り。音声を文字に変換するサービスで、向きが逆。
    - B: 誤り。対話のボットを作るサービス。
    - C: 正しい。
    - D: 誤り。言語を翻訳するサービス。

    **スキル:** [AI/ML のサービス](../domain3.md#t3-7-ai-ml) / **参照:** [Amazon Polly](../../../services/ai-managed-services.md#polly)、[Amazon Transcribe](../../../services/ai-managed-services.md#transcribe)

### 問4 {#q4}

コールセンターの通話の録音を文字にしたいと考えています。最も適切なサービスはどれですか。

- A. Amazon Transcribe
- B. Amazon Polly
- C. Amazon Rekognition
- D. Amazon Textract

??? success "答えと解説"
    **正解: A**

    Transcribe は音声を文字に変換します。

    - A: 正しい。
    - B: 誤り。文字を音声に変換するサービスで、向きが逆。
    - C: 誤り。画像や動画を分析するサービス。
    - D: 誤り。文書から文字や表を抽出するサービス。

    **スキル:** [AI/ML のサービス](../domain3.md#t3-7-ai-ml) / **参照:** [Amazon Transcribe](../../../services/ai-managed-services.md#transcribe)

### 問5 {#q5}

目的とサービスの組み合わせとして正しいものはどれですか。（2つ選択）

- A. 商品の写真に写る物を判別する: Amazon Translate
- B. スキャンした請求書から表を抽出する: Amazon Comprehend
- C. レビューの文章から感情を分析する: Amazon Rekognition
- D. レビューの文章から感情を分析する: Amazon Comprehend
- E. スキャンした請求書から表を抽出する: Amazon Textract

??? success "答えと解説"
    **正解: D, E**

    Comprehend はテキストの意味、Textract は文書からの抽出です。

    - A: 誤り。写真の分析は Amazon Rekognition。
    - B: 誤り。Comprehend はテキストの意味を分析するサービス。
    - C: 誤り。Rekognition は画像や動画を分析するサービス。
    - D: 正しい。
    - E: 正しい。

    **スキル:** [AI/ML のサービス](../domain3.md#t3-7-ai-ml) / **参照:** [Amazon Comprehend](../../../services/ai-managed-services.md#comprehend)、[Amazon Textract](../../../services/ai-managed-services.md#textract)

### 問6 {#q6}

投稿された画像に不適切な内容がないかを判定したいと考えています。最も適切なサービスはどれですか。

- A. Amazon Rekognition
- B. Amazon Translate
- C. Amazon Polly
- D. Amazon Lex

??? success "答えと解説"
    **正解: A**

    Rekognition は画像や動画を分析します。

    - A: 正しい。
    - B: 誤り。言語を翻訳するサービス。
    - C: 誤り。文字を音声に変換するサービス。
    - D: 誤り。対話のボットを作るサービス。

    **スキル:** [AI/ML のサービス](../domain3.md#t3-7-ai-ml) / **参照:** [Amazon Rekognition](../../../services/ai-managed-services.md#rekognition)、[Amazon Translate](../../../services/ai-managed-services.md#translate)

### 問7 {#q7}

Web サイトの商品説明を日本語から複数の言語に自動で変換したいと考えています。最も適切なサービスはどれですか。

- A. Amazon Transcribe
- B. Amazon SageMaker AI
- C. Amazon Comprehend
- D. Amazon Translate

??? success "答えと解説"
    **正解: D**

    Translate は言語を翻訳します。

    - A: 誤り。音声を文字に変換するサービス。
    - B: 誤り。独自のモデルを作るサービスで、翻訳の機能をそのまま提供するものではない。
    - C: 誤り。テキストの感情やエンティティを抽出するサービス。
    - D: 正しい。

    **スキル:** [AI/ML のサービス](../domain3.md#t3-7-ai-ml) / **参照:** [Amazon Translate](../../../services/ai-managed-services.md#translate)

### 問8 {#q8}

S3 に置いたログに、サーバーを用意せずに SQL で問い合わせたいと考えています。最も適切なサービスはどれですか。

- A. AWS Glue
- B. Amazon Athena
- C. Amazon Quick
- D. Amazon Kinesis

??? success "答えと解説"
    **正解: B**

    Athena は S3 のデータに SQL で問い合わせます。

    - A: 誤り。ETL とカタログのサービス。
    - B: 正しい。
    - C: 誤り。ダッシュボードと BI のサービス。
    - D: 誤り。ストリーミングデータを受けるサービス。

    **スキル:** [分析のサービス](../domain3.md#t3-7-analytics) / **参照:** [Amazon Athena](../../../services/streaming.md#athena)

### 問9 {#q9}

クリックのデータをリアルタイムに受け取って処理したいと考えています。最も適切なサービスはどれですか。

- A. Amazon Redshift
- B. Amazon Athena
- C. Amazon Kinesis
- D. AWS Glue

??? success "答えと解説"
    **正解: C**

    Kinesis はストリーミングデータを受けます。

    - A: 誤り。データウェアハウス。
    - B: 誤り。S3 のデータへの SQL の問い合わせのサービス。
    - C: 正しい。
    - D: 誤り。ETL とカタログのサービス。

    **スキル:** [分析のサービス](../domain3.md#t3-7-analytics) / **参照:** [Kinesis Data Streams](../../../services/streaming.md#kinesis-data-streams)

### 問10 {#q10}

複数のデータソースからデータを変換して読み込み（ETL）、データのカタログも管理したいと考えています。最も適切なサービスはどれですか。

- A. Amazon Quick
- B. Amazon OpenSearch Service
- C. AWS Glue
- D. Amazon Kinesis

??? success "答えと解説"
    **正解: C**

    Glue はデータの ETL とカタログのサービスです。

    - A: 誤り。ダッシュボードと BI のサービス。
    - B: 誤り。全文検索とログ分析のサービス。
    - C: 正しい。
    - D: 誤り。ストリーミングデータを受けるサービス。

    **スキル:** [分析のサービス](../domain3.md#t3-7-analytics) / **参照:** [AWS Glue](../../../services/data-engineering.md#glue)

### 問11 {#q11}

経営層向けに、売上のダッシュボードを作って共有したいと考えています。最も適切なサービスはどれですか。

- A. Amazon EMR
- B. Amazon Quick
- C. AWS Glue
- D. Amazon Kinesis

??? success "答えと解説"
    **正解: B**

    Quick の BI の機能（Quick Sight）でダッシュボードを作れます。古い教材の QuickSight にあたります。

    - A: 誤り。Spark などのビッグデータ基盤。
    - B: 正しい。
    - C: 誤り。ETL とカタログのサービス。
    - D: 誤り。ストリーミングデータを受けるサービス。

    **スキル:** [分析のサービス](../domain3.md#t3-7-analytics) / **参照:** [Amazon Quick Sight](../../../services/data-engineering.md#quick-sight)

### 問12 {#q12}

要件とサービスの組み合わせとして正しいものはどれですか。（2つ選択）

- A. ログを全文検索する: Amazon OpenSearch Service
- B. データウェアハウスで分析する: Amazon Kinesis
- C. ログを全文検索する: AWS Glue
- D. データウェアハウスで大量のデータを分析する: Amazon Redshift
- E. Spark の基盤を動かす: Amazon Redshift

??? success "答えと解説"
    **正解: A, D**

    要件から分析のサービスを選びます。

    - A: 正しい。
    - B: 誤り。Kinesis はストリーミングデータのサービス。
    - C: 誤り。Glue は ETL とカタログのサービス。
    - D: 正しい。
    - E: 誤り。Spark などの基盤は Amazon EMR。

    **スキル:** [分析のサービス](../domain3.md#t3-7-analytics) / **参照:** [Amazon Redshift](../../../services/data-engineering.md#redshift)、[Amazon EMR](../../../services/data-engineering.md#emr)、[Amazon OpenSearch Service](../../../services/streaming.md#opensearch)
