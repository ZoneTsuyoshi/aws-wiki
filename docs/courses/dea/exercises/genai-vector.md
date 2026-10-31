# LLM とベクトルの問題集

対象の解説: [AI サービスと AI 開発ツール](../../../services/ai.md)、[生成 AI アプリの設計と運用](../../../services/genai-apps.md)、[ベクトルインデックス](../../../services/databases-specialized.md#vector-indexes)

### 問1 {#q1}

S3 に置いた 100 万件の問い合わせ文を、LLM で分類します。即時の応答は要らず、一度に処理します。結果は S3 に出します。どの方法が適切ですか。

- A. Bedrock のバッチ推論のジョブを S3 の入出力で実行する
- B. SageMaker AI でモデルを学習し、リアルタイムのエンドポイントを作る
- C. Athena の CTAS に文を渡し、LLM の処理を SQL だけで置き換える
- D. Lambda から Converse API を 100 万回順に呼び、結果を 1 件ずつ書く

??? success "答えと解説"
    **正解: A**

    入力を S3 に置き、結果も S3 に出ます。

    - A: 正しい。
    - B: 誤り。モデルの学習は範囲外で、要件にも合いません。
    - C: 誤り。CTAS は LLM を呼ぶ機能ではありません。
    - D: 誤り。動きますが、大量の非同期処理にはバッチ推論が向きます。

    **スキル:** [1.2.10](../domain1.md#skill-1-2-10) / **参照:** [アプリから Bedrock を呼ぶ](../../../services/ai.md#bedrock-runtime)、[スループットの選択肢](../../../services/ai.md#throughput-options)

### 問2 {#q2}

PDF の請求書と音声の記録を、パイプラインで構造化データにします。自分でモデルの呼び出しを組み立てません。どのサービスですか。

- A. Glue のクローラー
- B. DataBrew のレシピジョブ
- C. Bedrock Data Automation
- D. Bedrock Guardrails

??? success "答えと解説"
    **正解: C**

    PDF、画像、音声を構造化データにできます。

    - A: 誤り。スキーマの推定で、PDF や音声の中身は構造化しません。
    - B: 誤り。表形式のデータの整形に向きます。
    - C: 正しい。
    - D: 誤り。入出力の制御で、構造化の機能ではありません。

    **スキル:** [1.2.10](../domain1.md#skill-1-2-10) / **参照:** [Bedrock Data Automation](../../../services/genai-apps.md#bda)、[アプリから Bedrock を呼ぶ](../../../services/ai.md#bedrock-runtime)

### 問3 {#q3}

Lambda から Converse API を呼ぶパイプラインで、急増時に `ThrottlingException` が出ます。また手順を連結します。適切な対応はどれですか。（2つ選択）

- A. 手順の連結と再試行を Step Functions に任せる
- B. SQS を挟んで流量を抑え、バックオフして再試行する
- C. `ThrottlingException` は権限の不足なので、IAM ポリシーを広げる
- D. 再試行をなくし、失敗した文はパイプラインから捨てる
- E. プロンプトを長くして、1 回あたりの処理の量を増やす

??? success "答えと解説"
    **正解: A, B**

    レート制限は流量の調整で対応します。

    - A: 正しい。`Retry` で再試行できます。
    - B: 正しい。レート制限への基本の対応です。
    - C: 誤り。レート制限のエラーです。
    - D: 誤り。データを失います。
    - E: 誤り。トークンが増え、制限に近づきます。

    **スキル:** [1.2.10](../domain1.md#skill-1-2-10) / **参照:** [エラー処理とスロットリング](../../../services/ai.md#errors-throttling)、[SQS](../../../services/messaging.md#sqs)

### 問4 {#q4}

Bedrock のバッチ推論について正しいものはどれですか。

- A. プロビジョンドのモデルでだけ使える
- B. 完了の検知に EventBridge を使える
- C. 入力は API の本文で直接送り、S3 は使わない
- D. 結果は同期で Lambda へ返り、S3 には出力されない

??? success "答えと解説"
    **正解: B**

    バッチ推論は非同期です。

    - A: 誤り。プロビジョンドのモデルでは使えません。
    - B: 正しい。
    - C: 誤り。入力は S3 に置きます。
    - D: 誤り。非同期で、結果は S3 に出ます。

    **スキル:** [1.2.10](../domain1.md#skill-1-2-10) / **参照:** [スループットの選択肢](../../../services/ai.md#throughput-options)、[アプリから Bedrock を呼ぶ](../../../services/ai.md#bedrock-runtime)

### 問5 {#q5}

Aurora PostgreSQL で数百万件のベクトルを検索します。メモリに余裕があり、速度と精度を優先します。構築の遅さは許容します。どのインデックスですか。

- A. B ツリー
- B. Flat（全件比較）
- C. IVFFlat
- D. HNSW

??? success "答えと解説"
    **正解: D**

    HNSW はメモリを使いますが、速く高精度です。

    - A: 誤り。ベクトルの近傍検索のインデックスではありません。
    - B: 誤り。完全ですが、件数が多いと遅くなります。
    - C: 誤り。メモリは少なめですが、問題の条件では HNSW を選びます。
    - D: 正しい。

    **スキル:** [2.1.8](../domain2.md#skill-2-1-8) / **参照:** [ベクトルインデックス](../../../services/databases-specialized.md#vector-indexes)、[pgvector](../../../services/genai-apps.md#pgvector)

### 問6 {#q6}

HNSW の検索の精度が足りません。検索は多少遅くなってもかまいません。インデックスの再構築はしません。どのパラメータを上げますか。

- A. `probes`
- B. `ef_construction`
- C. `ef_search`
- D. `m`

??? success "答えと解説"
    **正解: C**

    `ef_search` は検索時に調整でき、上げると精度が上がります。

    - A: 誤り。IVFFlat のパラメータです。
    - B: 誤り。構築時のパラメータです。
    - C: 正しい。
    - D: 誤り。構築時のパラメータです。

    **スキル:** [2.1.8](../domain2.md#skill-2-1-8) / **参照:** [ベクトルインデックス](../../../services/databases-specialized.md#vector-indexes)

### 問7 {#q7}

IVFFlat について正しいものはどれですか。

- A. 階層化したグラフをたどる方式で、HNSW より多くのメモリを使う
- B. データ投入後に作り、`probes` を上げると精度が上がって検索が遅くなる
- C. 全件と比較する方式で、構築は不要で、常に完全な結果を返す
- D. データがない状態で最初に作り、`probes` を上げると精度が下がって検索が速くなる

??? success "答えと解説"
    **正解: B**

    クラスターに分け、近いものだけ探します。

    - A: 誤り。それは HNSW の説明です。
    - B: 正しい。
    - C: 誤り。それは Flat の説明です。
    - D: 誤り。どちらも逆です。

    **スキル:** [2.1.8](../domain2.md#skill-2-1-8) / **参照:** [ベクトルインデックス](../../../services/databases-specialized.md#vector-indexes)、[ベクトルストア](../../../services/genai-apps.md#vector-stores)

### 問8 {#q8}

RDS for PostgreSQL の pgvector で HNSW のインデックスを作ると、`access method "hnsw" does not exist` で失敗します。確認すべきことはどれですか。

- A. pgvector のバージョンが 0.5.0 以上か
- B. パラメータグループの `shared_buffers` が十分か
- C. インスタンスが Multi-AZ か
- D. パラメータグループの `rds.force_ssl` が有効か

??? success "答えと解説"
    **正解: A**

    HNSW には pgvector 0.5.0 以上が必要です。

    - A: 正しい。
    - B: 誤り。メモリの設定で、このエラーの原因ではありません。
    - C: 誤り。インデックスの作成の条件ではありません。
    - D: 誤り。接続の暗号化の設定で、関係しません。

    **スキル:** [2.1.8](../domain2.md#skill-2-1-8) / **参照:** [pgvector](../../../services/genai-apps.md#pgvector)

### 問9 {#q9}

Knowledge Bases で、回答に文脈が足りないことが多いです。チャンクの大きさの調整の説明として正しいものはどれですか。

- A. 小さいほど文脈が増え、大きいほど無関係な文が減る
- B. 大きさは検索の結果に影響せず、費用だけが変わる
- C. チャンクは埋め込みの後に作るので、大きさは取り込みに影響しない
- D. 小さすぎると文脈が足りず、大きすぎると無関係な文が増える

??? success "答えと解説"
    **正解: D**

    文書の性質に合わせて調整します。

    - A: 誤り。逆です。
    - B: 誤り。検索の結果に影響します。
    - C: 誤り。順序が逆で、チャンク化の後に埋め込みます。
    - D: 正しい。

    **スキル:** [2.4.6](../domain2.md#skill-2-4-6) / **参照:** [チャンク化の戦略](../../../services/genai-apps.md#chunking)、[Knowledge Bases](../../../services/genai-apps.md#knowledge-bases)

### 問10 {#q10}

埋め込みモデルを 1,024 次元のものへ変更します。pgvector の列は `vector(1536)` です。必要な作業はどれですか。（2つ選択）

- A. 埋め込みモデルは変更したまま、質問だけを新しいモデルで埋め込む
- B. 全データを新しいモデルで再度埋め込む
- C. 既存のベクトルの末尾を切り詰め、1,024 次元に揃える
- D. インデックスの `ef_search` を上げて次元の差を吸収する
- E. 列の次元をモデルに合わせる

??? success "答えと解説"
    **正解: B, E**

    モデルの変更には再埋め込みが必要です。

    - A: 誤り。保存済みのベクトルと比較できません。
    - B: 正しい。異なるモデルのベクトルは比較できません。
    - C: 誤り。モデルが違うので、意味のある比較になりません。
    - D: 誤り。次元の差は吸収できません。
    - E: 正しい。違うと取り込みエラーになります。

    **スキル:** [2.4.6](../domain2.md#skill-2-4-6) / **参照:** [埋め込みの選び方](../../../services/genai-apps.md#embedding-selection)、[ベクトルストア](../../../services/genai-apps.md#vector-stores)

### 問11 {#q11}

100 万チャンクを 1,024 次元、float32 で保存します。ベクトルだけの容量はおよそいくらですか。

- A. 約 410 MB
- B. 約 1 GB
- C. 約 41 GB
- D. 約 4.1 GB

??? success "答えと解説"
    **正解: D**

    100 万 × 1,024 × 4 バイトです。

    - A: 誤り。桁が 1 つ違います。
    - B: 誤り。float32 は 4 バイトです。
    - C: 誤り。桁が 1 つ違います。
    - D: 正しい。

    **スキル:** [2.4.6](../domain2.md#skill-2-4-6) / **参照:** [埋め込みの選び方](../../../services/genai-apps.md#embedding-selection)

### 問12 {#q12}

ベクトルの取り込みの流れの順序として正しいものはどれですか。

- A. データソース、埋め込み、ベクトルストア、解析、チャンク化
- B. 解析、ベクトルストア、データソース、埋め込み、チャンク化
- C. データソース、解析、チャンク化、埋め込み、ベクトルストア
- D. ベクトルストア、チャンク化、解析、データソース、埋め込み

??? success "答えと解説"
    **正解: C**

    分割してから埋め込み、保存します。

    - A: 誤り。埋め込みの前にチャンク化します。
    - B: 誤り。保存は最後です。
    - C: 正しい。
    - D: 誤り。順序が逆です。

    **スキル:** [2.4.6](../domain2.md#skill-2-4-6) / **参照:** [Knowledge Bases](../../../services/genai-apps.md#knowledge-bases)、[チャンク化の戦略](../../../services/genai-apps.md#chunking)
