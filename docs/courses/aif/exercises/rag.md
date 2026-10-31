# RAG とベクトルストアの問題集

対象の解説: [RAG](../../../services/ai-fundamentals.md#rag)、[Knowledge Bases](../../../services/genai-apps.md#knowledge-bases)、[ベクトルストア](../../../services/genai-apps.md#vector-stores)

### 問1 {#q1}

RAG の説明として正しいものはどれですか。

- A. 応答を別の言語に翻訳してから返す
- B. 質問に関連する文書を検索し、プロンプトに加えてモデルに渡す
- C. 自社の文書でモデルの重みを更新する
- D. 大きなモデルの応答を使って、小さなモデルの重みを調整して推論を安くする

??? success "答えと解説"
    **正解: B**

    RAG はモデルを再学習せず、最新の社内情報で答えられます。

    - A: 誤り。RAG とは関係がありません。
    - B: 正しい。
    - C: 誤り。それはファインチューニングの説明です。
    - D: 誤り。それは蒸留の説明です。

    **スキル:** [3.1.3](../domain3.md#obj-3-1-3) / **参照:** [RAG](../../../services/ai-fundamentals.md#rag)

### 問2 {#q2}

RAG の事前準備の順番として正しいものはどれですか。

- A. 埋め込みをベクトルストアに保存し、文書をチャンクに分け、モデルを再学習する
- B. モデルをファインチューニングし、ベクトルを削除し、文書を要約する
- C. 文書をチャンクに分け、埋め込みを作り、ベクトルストアに保存する
- D. ベクトルストアから文書を消し、質問を翻訳し、チャンクに分ける

??? success "答えと解説"
    **正解: C**

    取り込みでは、チャンク化、埋め込み、保存の順に行います。

    - A: 誤り。チャンクごとに埋め込みを作るので順番が逆で、再学習は不要です。
    - B: 誤り。RAG の準備に再学習は要りません。
    - C: 正しい。
    - D: 誤り。事前準備の流れではありません。

    **スキル:** [3.1.3](../domain3.md#obj-3-1-3) / **参照:** [RAG](../../../services/ai-fundamentals.md#rag)、[取り込みの流れ](../../../services/genai-apps.md#kb-ingestion)

### 問3 {#q3}

人事の規定が毎月更新されます。社員の質問に最新の規定で答え、根拠も示したいと考えています。適切な方法はどれですか。

- A. RAG を使う
- B. temperature を下げる
- C. ファインチューニングを毎月行う
- D. 自社で事前学習からモデルを作る

??? success "答えと解説"
    **正解: A**

    文書を更新すれば再学習なしで回答に反映でき、引用も示せます。

    - A: 正しい。
    - B: 誤り。応答のばらつきの調整で、最新の規定は反映されません。
    - C: 誤り。規定が変わるたびに費用をかけて調整し直すことになります。
    - D: 誤り。費用が最大で、更新の頻度にも合いません。

    **スキル:** [3.1.3](../domain3.md#obj-3-1-3) / **参照:** [モデルを業務に合わせる方法](../../../services/ai-fundamentals.md#customization-options)

### 問4 {#q4}

RAG の仕組みをマネージドで提供し、回答に引用も含められる AWS の機能はどれですか。

- A. Amazon Comprehend
- B. SageMaker Pipelines
- C. Bedrock Prompt Management
- D. Amazon Bedrock Knowledge Bases

??? success "答えと解説"
    **正解: D**

    Knowledge Bases は取り込みから検索まで提供します。公式は管理の少ない Managed Knowledge Base を推奨しています。

    - A: 誤り。テキストを分析するサービスで、文書の検索と回答の生成はしません。
    - B: 誤り。ML のワークフローを自動化する機能です。
    - C: 誤り。プロンプトの版を管理する機能で、文書の検索はしません。
    - D: 正しい。

    **スキル:** [3.1.3](../domain3.md#obj-3-1-3) / **参照:** [Knowledge Bases](../../../services/genai-apps.md#knowledge-bases)、[Managed と Customer-managed](../../../services/genai-apps.md#managed-kb)

### 問5 {#q5}

RAG が業務に合う場面として適切なものを選んでください。（2つ選択）

- A. 製品マニュアルに基づいて、カスタマーサポートの質問に答える
- B. 独特の文体でモデルに宣伝文を書かせる
- C. 住宅価格を表データから予測する
- D. 法務の質問に、根拠の条文の引用つきで答える
- E. 視聴履歴から個人別のおすすめを作る

??? success "答えと解説"
    **正解: A, D**

    社内の質問応答、カスタマーサポート、根拠の提示が代表的な使い方です。

    - A: 正しい。
    - B: 誤り。文体を学ばせるならファインチューニングです。
    - C: 誤り。従来の ML の回帰の用途です。
    - D: 正しい。
    - E: 誤り。レコメンドの用途です。

    **スキル:** [3.1.3](../domain3.md#obj-3-1-3) / **参照:** [RAG](../../../services/ai-fundamentals.md#rag)

### 問6 {#q6}

既に Aurora PostgreSQL で商品データを管理しています。新たなデータベースを増やさずに、説明文の埋め込みを保存して検索したいと考えています。適切な選択はどれですか。

- A. Amazon Neptune Analytics に全データを移して検索する
- B. Aurora PostgreSQL の pgvector
- C. OpenSearch Service のクラスターを新しく作って同期する
- D. DynamoDB に新しいテーブルを作って埋め込みを保存する

??? success "答えと解説"
    **正解: B**

    既存のデータベースに合わせると運用が増えず、商品データとも SQL で結合できます。

    - A: 誤り。新たなデータベースが増え、関係をたどる要件もありません。
    - B: 正しい。
    - C: 誤り。新たな基盤が増え、同期の運用も必要になります。
    - D: 誤り。新たなデータストアが増え、ベクトル検索にも向きません。

    **スキル:** [3.1.4](../domain3.md#obj-3-1-4) / **参照:** [pgvector](../../../services/genai-apps.md#pgvector)

### 問7 {#q7}

キーワードの全文検索と k-NN のベクトル検索を組み合わせて、高い検索品質を得たいと考えています。適切なサービスはどれですか。

- A. Amazon Comprehend
- B. Amazon RDS for PostgreSQL
- C. Amazon Neptune Analytics
- D. Amazon OpenSearch Service

??? success "答えと解説"
    **正解: D**

    OpenSearch Service は k-NN 検索とハイブリッド検索が特徴です。

    - A: 誤り。テキストを分析するサービスで、ベクトルは保存しません。
    - B: 誤り。pgvector は使えますが、全文検索との併用が特徴のサービスではありません。
    - C: 誤り。グラフとベクトルの組み合わせに向くサービスです。
    - D: 正しい。

    **スキル:** [3.1.4](../domain3.md#obj-3-1-4) / **参照:** [ベクトルストア](../../../services/genai-apps.md#vector-stores)、[OpenSearch](../../../services/genai-apps.md#opensearch-vectors)

### 問8 {#q8}

「この部品を使う製品の取引先はどこか」のように、関係をたどる質問が中心です。適切なベクトルストアはどれですか。

- A. Amazon S3 Glacier
- B. Amazon OpenSearch Service
- C. Amazon Neptune Analytics
- D. Amazon Aurora PostgreSQL

??? success "答えと解説"
    **正解: C**

    グラフとベクトルを組み合わせる GraphRAG には Neptune Analytics が向きます。

    - A: 誤り。アーカイブのストレージで、ベクトル検索はできません。
    - B: 誤り。全文検索との併用に向くサービスです。
    - C: 正しい。
    - D: 誤り。既に Aurora を使っている場面に向きますが、関係をたどる GraphRAG の中心ではありません。

    **スキル:** [3.1.4](../domain3.md#obj-3-1-4) / **参照:** [ベクトルストア](../../../services/genai-apps.md#vector-stores)、[Managed と Customer-managed](../../../services/genai-apps.md#managed-kb)

### 問9 {#q9}

既に PostgreSQL の RDS を運用しているチームが、埋め込みの検索を追加します。最も運用を増やさない選択はどれですか。

- A. RDS for PostgreSQL の pgvector を使う
- B. Neptune Analytics に移す
- C. OpenSearch Service のクラスターを新しく作って同期する
- D. Amazon Kendra の新しいインデックスを作る

??? success "答えと解説"
    **正解: A**

    既存のデータベースがあれば、それに合わせると運用が増えません。

    - A: 正しい。
    - B: 誤り。新しいデータベースの運用が増えます。
    - C: 誤り。新しい基盤の運用が増えます。
    - D: 誤り。新規顧客を受け付けておらず、新しい基盤の運用も増えます。

    **スキル:** [3.1.4](../domain3.md#obj-3-1-4) / **参照:** [ベクトルストア](../../../services/genai-apps.md#vector-stores)

### 問10 {#q10}

10 億件の古い文書を、検索の頻度は低いまま低コストで保存したいと考えています。適切な選択はどれですか。

- A. Amazon Neptune Analytics
- B. S3 Vectors のインデックス
- C. 常時起動の OpenSearch Service クラスター
- D. ElastiCache のキャッシュ

??? success "答えと解説"
    **正解: B**

    S3 Vectors は、大量でアクセスが少ないデータを低コストで扱います。

    - A: 誤り。関係をたどる質問に向くサービスで、低頻度の大量保存の選択肢ではありません。
    - B: 正しい。
    - C: 誤り。低遅延の検索に向く代わりに、使わない時間も費用がかかります。
    - D: 誤り。インメモリで高速な代わりに、大量の長期保存には向きません。

    **スキル:** [3.1.4](../domain3.md#obj-3-1-4) / **参照:** [S3 Vectors](../../../services/genai-apps.md#s3-vectors)
