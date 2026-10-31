# Knowledge Bases と RAG の問題集

対象の解説: [Knowledge Bases を呼ぶ](../../../services/ai.md#knowledge-bases)、[取り込みの流れ](../../../services/genai-apps.md#kb-ingestion)、[Bedrock Evaluations](../../../services/genai-apps.md#bedrock-evaluations)

### 問1 {#q1}

表や図の多い PDF のマニュアルで RAG を作ります。表の内容を聞くと答えられません。解析の設定はどう変えますか。

- A. チャンク戦略をなしにして、1 文書を 1 チャンクにする
- B. 既定のパーサーのまま、埋め込みの次元を増やす
- C. BDA か FM のパーサーに変える
- D. 既定のパーサーのまま、`numberOfResults` を増やす

??? success "答えと解説"
    **正解: C**

    図や表を含む文書には BDA か FM のパーサーを選びます。どちらも処理の分の料金がかかります。

    - A: 誤り。解析の問題は解決しません。
    - B: 誤り。取り込まれていない内容は、次元を増やしても検索できません。
    - C: 正しい。
    - D: 誤り。既定のパーサーはテキストしか出力しないので、表の内容がそもそも取り込まれていません。

    **スキル:** [1.2.7](../domain1.md#skill-1-2-7) / **参照:** [取り込みの流れ](../../../services/genai-apps.md#kb-ingestion)

### 問2 {#q2}

章と節の構造を持つ規定集です。検索は細かい単位で当てたいですが、回答には節全体の文脈を渡します。どのチャンク戦略を選びますか。

- A. 固定サイズで `maxTokens` を最大にする
- B. セマンティックで `bufferSize` を 0 にする
- C. なし（1 文書を 1 チャンク）にする
- D. 階層

??? success "答えと解説"
    **正解: D**

    階層チャンクは子で検索し、親に置き換えて返します。返る件数が指定より少なくなることがあります。

    - A: 誤り。細かい単位での検索ができなくなります。
    - B: 誤り。意味の切れ目で分ける戦略で、親子の関係を使って文脈を広げるものではありません。
    - C: 誤り。検索の単位が大きすぎ、ページ番号の引用やフィルターも使えません。
    - D: 正しい。

    **スキル:** [1.2.7](../domain1.md#skill-1-2-7) / **参照:** [チャンク化](../../../services/genai-apps.md#chunking)

### 問3 {#q3}

部署ごとに検索を絞るため、S3 の `policy.pdf` にメタデータを付けます。ファイルの名前と置き場所として正しいものはどれですか。

- A. 同じ場所に `policy.pdf.metadata.json` を置く
- B. 同じ場所に `policy.metadata.json` を置く
- C. 同じ場所に `metadata.json` を 1 つだけ置いて全文書で共有する
- D. 別のバケットに `policy.json` を置く

??? success "答えと解説"
    **正解: A**

    メタデータは文書と同じ場所に、`<ファイル名>.metadata.json` として置きます。

    - A: 正しい。
    - B: 誤り。拡張子まで元のファイル名と揃えます。
    - C: 誤り。文書ごとに、ファイル名を揃えて作ります。
    - D: 誤り。同じ場所に置く必要があり、名前も違います。

    **スキル:** [1.2.7](../domain1.md#skill-1-2-7) / **参照:** [メタデータ](../../../services/genai-apps.md#kb-metadata)

### 問4 {#q4}

社内ポータルの RAG を早く作り、運用の管理を減らします。組み込みの検索とリランクを使います。生成は別の FM を自分で呼びます。正しい設計はどれですか。

- A. FM のファインチューニングに全文書を学習させる
- B. Managed Knowledge Base の `Retrieve` のあとに `Converse` を呼ぶ
- C. Managed Knowledge Base の `RetrieveAndGenerate` で検索と生成まで一度に行う
- D. Customer-managed で OpenSearch の設定を細かく調整する

??? success "答えと解説"
    **正解: B**

    管理を減らすなら Managed です。`Retrieve` で検索し、生成は別に呼びます。

    - A: 誤り。RAG ではありません。更新のたびに再学習が必要になります。
    - B: 正しい。
    - C: 誤り。Managed では `RetrieveAndGenerate` を使えません。
    - D: 誤り。ベクトル DB を自分で制御する選択で、管理が増えます。

    **スキル:** [2.1.5](../domain2.md#skill-2-1-5) / **参照:** [Managed と Customer-managed](../../../services/genai-apps.md#managed-kb)

### 問5 {#q5}

Redshift のデータウェアハウスに、自然文で「先月の地域別の売上は?」と質問させます。文書の検索ではありません。どのパターンですか。

- A. 自然文を SQL に変換する構造化データストア
- B. 表を CSV に書き出して、ベクトルストアに埋め込む
- C. Neptune Analytics の GraphRAG
- D. 全行を Provisioned Throughput の FM に入力する

??? success "答えと解説"
    **正解: A**

    Knowledge Bases の構造化データストアは、自然文を SQL に変換してデータウェアハウスに問い合わせます。

    - A: 正しい。
    - B: 誤り。集計の質問に向かず、データの鮮度も落ちます。
    - C: 誤り。関係をたどる質問の選択です。
    - D: 誤り。コンテキスト長とコストの面で現実的ではありません。

    **スキル:** [2.1.5](../domain2.md#skill-2-1-5) / **参照:** [Managed と Customer-managed](../../../services/genai-apps.md#managed-kb)

### 問6 {#q6}

製品、部品、供給元の関係をたどる質問に答える RAG です。「この部品を使う製品の供給元はどこですか」のような質問が中心です。適切なパターンはどれですか。

- A. OpenSearch のキーワード検索だけを使う
- B. S3 Vectors のセマンティック検索だけを使う構成
- C. Neptune Analytics の GraphRAG
- D. OpenSearch のハイブリッド検索

??? success "答えと解説"
    **正解: C**

    関係をたどる質問には Neptune Analytics の GraphRAG を選びます。

    - A: 誤り。語の一致を探すだけで、複数の関係をたどれません。
    - B: 誤り。意味の近さの検索で、関係をたどる質問には向きません。
    - C: 正しい。
    - D: 誤り。語と意味の近さの検索で、複数の関係をたどれません。

    **スキル:** [2.1.5](../domain2.md#skill-2-1-5) / **参照:** [選び方の比較](../../../services/genai-apps.md#choosing)

### 問7 {#q7}

RAG の取得のみの評価で ContextRelevance は高いのですが、ContextCoverage が低いです。原因の候補として最も適切なものはどれですか。

- A. コンテキストグラウンディングのしきい値が高い
- B. 引用の形式が誤っている
- C. 生成モデルの temperature が高い
- D. 取得件数が少ないか、答えを含む文書がない

??? success "答えと解説"
    **正解: D**

    ContextCoverage は、取得した文章が正解の情報をどれだけ含むかを見ます。低ければ取得件数や文書の不足を疑います。

    - A: 誤り。応答の検査の設定で、この結果の原因ではありません。
    - B: 誤り。Citation の指標の話で、取得のみの評価の対象ではありません。
    - C: 誤り。取得のみの評価に生成は含まれません。
    - D: 正しい。

    **スキル:** [2.3.10](../domain2.md#skill-2-3-10) / **参照:** [Bedrock Evaluations](../../../services/genai-apps.md#bedrock-evaluations)

### 問8 {#q8}

検索の精度を、応答の生成と切り離して定期的に評価します。Bedrock Evaluations の設定として適切なものはどれですか。

- A. 取得と生成のジョブで Faithfulness を見る
- B. 取得のみのジョブで ContextRelevance と ContextCoverage を見る
- C. FM の評価ジョブで Stereotyping を見る
- D. CloudWatch で `InvocationThrottles` と `InvocationLatency` を見る

??? success "答えと解説"
    **正解: B**

    取得のみのジョブでは ContextRelevance と ContextCoverage を評価できます。

    - A: 誤り。生成も含む指標で、検索だけを切り離せません。
    - B: 正しい。
    - C: 誤り。モデルの安全性の指標です。
    - D: 誤り。スロットリングの指標で、検索の精度を示しません。

    **スキル:** [2.3.10](../domain2.md#skill-2-3-10) / **参照:** [Bedrock Evaluations](../../../services/genai-apps.md#bedrock-evaluations)

### 問9 {#q9}

RAG の誤答を調査します。切り分けの順序として適切なものはどれですか。

- A. `InvocationLatency` を見る、`TimeToFirstToken` を見る、再起動する
- B. FM を変える、文書を増やす、インデックスを作り直す
- C. 課金を見る、IAM を見る、VPC を見る
- D. 取得は正しいか、文書に答えはあるか、生成は文書に従っているか

??? success "答えと解説"
    **正解: D**

    取得、文書、生成の順に分けて調べます。

    - A: 誤り。遅延の調査で、回答の内容の調査ではありません。
    - B: 誤り。原因を調べずに変更しています。
    - C: 誤り。誤答の調査の手順ではありません。
    - D: 正しい。

    **スキル:** [2.3.10](../domain2.md#skill-2-3-10) / **参照:** [トラブルシューティング](../../../services/genai-apps.md#troubleshooting)

### 問10 {#q10}

`RetrieveAndGenerate` で最大 10 件を取得したいです。設定する項目はどれですか。

- A. `overrideSearchType`
- B. `overlapPercentage`
- C. `numberOfResults`
- D. `maxTokens`

??? success "答えと解説"
    **正解: C**

    `numberOfResults` は取得するチャンクの最大数で、範囲は 1〜100、既定は 5 です。

    - A: 誤り。検索方式の設定です。
    - B: 誤り。固定サイズのチャンクの重なりの設定です。
    - C: 正しい。
    - D: 誤り。生成の長さの設定です。

    **スキル:** [3.1.8](../domain3.md#skill-3-1-8) / **参照:** [Knowledge Bases のパラメータ](../../../services/ai.md#kb-params)

### 問11 {#q11}

S3 Vectors をベクトルストアにしたナレッジベースで、`overrideSearchType` を `HYBRID` にしました。結果として正しいものはどれですか。

- A. 使えない。`SEMANTIC` で検索する
- B. 使えない。OCU を増やすと使える
- C. 動作する。キーワードとベクトルの両方で検索する
- D. 動作する。ただし検索は全文検索だけになる

??? success "答えと解説"
    **正解: A**

    ハイブリッド検索は RDS、OpenSearch Serverless、MongoDB でフィルター可能なテキスト列があるときに使えます。S3 Vectors では使えません。

    - A: 正しい。
    - B: 誤り。OCU は OpenSearch Serverless の単位です。
    - C: 誤り。S3 Vectors はハイブリッド検索に対応しません。
    - D: 誤り。S3 Vectors はセマンティック検索だけです。

    **スキル:** [3.1.8](../domain3.md#skill-3-1-8) / **参照:** [検索の改善](../../../services/genai-apps.md#retrieval-optimization)、[S3 Vectors](../../../services/genai-apps.md#s3-vectors)

### 問12 {#q12}

階層チャンクのナレッジベースで `numberOfResults` を 10 にしたのに、返るのは 6 件です。正しい説明はどれですか。

- A. 埋め込みの次元が小さい。1,024 に上げる
- B. 仕様である。複数の子が同じ親に置き換わる
- C. Guardrails のブロック。しきい値を変える
- D. 同期が失敗している。`StartIngestionJob` をやり直す

??? success "答えと解説"
    **正解: B**

    階層チャンクでは返る件数が `numberOfResults` より少なくなることがあります。

    - A: 誤り。次元は返る件数に関係しません。
    - B: 正しい。
    - C: 誤り。Guardrails は検索の件数を調整する機能ではありません。
    - D: 誤り。同期の失敗とは別の話です。階層では子が親に置き換わります。

    **スキル:** [3.1.8](../domain3.md#skill-3-1-8) / **参照:** [Knowledge Bases のパラメータ](../../../services/ai.md#kb-params)、[チャンク化](../../../services/genai-apps.md#chunking)

### 問13 {#q13}

2026 年 10 月に新しく作る Customer-managed のナレッジベースで、データソースとして指定できるものはどれですか。（2つ選択）

- A. S3
- B. Confluence
- C. Custom
- D. SharePoint
- E. Web Crawler

??? success "答えと解説"
    **正解: A, C**

    新しく作る Customer-managed のデータソースは S3 と Custom です。Managed はほかに SharePoint や Confluence なども使えます。

    - A: 正しい。
    - B: 誤り。Customer-managed での新規の作成は 2026 年 9 月 30 日で終了しました。
    - C: 正しい。
    - D: 誤り。Customer-managed での新規の作成は 2026 年 9 月 30 日で終了しました。
    - E: 誤り。Customer-managed での新規の作成は 2026 年 9 月 30 日で終了しました。

    **スキル:** [3.2.7](../domain3.md#skill-3-2-7) / **参照:** [Managed と Customer-managed](../../../services/genai-apps.md#managed-kb)

### 問14 {#q14}

データソースを削除するとき、ベクトルストアのデータも一緒に消します。どの設定ですか。

- A. `dataDeletionPolicy` を `DELETE` にする
- B. `numberOfResults` を 0 にする
- C. `overrideSearchType` を `SEMANTIC` にする
- D. `TtlDuration` を 0 にする

??? success "答えと解説"
    **正解: A**

    データソースを消したときのベクトルの扱いは、`dataDeletionPolicy` の `RETAIN` か `DELETE` で決めます。

    - A: 正しい。
    - B: 誤り。範囲は 1〜100 で、検索の設定です。
    - C: 誤り。検索方式の設定です。
    - D: 誤り。Feature Store のレコードの設定です。

    **スキル:** [3.2.7](../domain3.md#skill-3-2-7) / **参照:** [同期と鮮度](../../../services/genai-apps.md#kb-sync)

### 問15 {#q15}

既存のナレッジベースの埋め込みモデルを新しいものへ変更します。適切な手順はどれですか。

- A. `dataDeletionPolicy` を `RETAIN` にして、データソースだけを作り直す
- B. 新しいインデックスとナレッジベースへ全データを同期して切り替える
- C. ナレッジベースの設定でモデルだけを変更して、次回の差分の同期に任せる
- D. 新しいモデルで新しい文書だけを追加し、古いベクトルは残す

??? success "答えと解説"
    **正解: B**

    埋め込みモデルを変えると、全データの再埋め込みが必要です。新しいインデックスを作ってから切り替えます。

    - A: 誤り。埋め込みモデルは変わりません。
    - B: 正しい。
    - C: 誤り。既存のナレッジベースの埋め込みモデルは変更できません。
    - D: 誤り。古いベクトルと比較できず、検索結果が壊れます。

    **スキル:** [3.2.7](../domain3.md#skill-3-2-7) / **参照:** [埋め込みの選び方](../../../services/genai-apps.md#embedding-selection)

### 問16 {#q16}

検索の前に入力を検査し、検索と生成を別に制御します。部署ごとに文書を絞ります。正しい組み合わせはどれですか。

- A. `RetrieveAndGenerate` だけで、部署は利用者に質問文で書いてもらう
- B. `ApplyGuardrail`、`StartIngestionJob`、`Converse`
- C. `Retrieve`、`ApplyGuardrail`、`Converse`
- D. `ApplyGuardrail`、`filter` 付きの `Retrieve`、`Converse`

??? success "答えと解説"
    **正解: D**

    `ApplyGuardrail` で入力を検査し、`filter` で絞った `Retrieve` のあとに、アプリから `Converse` を呼びます。

    - A: 誤り。検索と生成を別に制御できず、絞り込みも利用者に任せることになります。
    - B: 誤り。`StartIngestionJob` は同期の API で、検索はしません。
    - C: 誤り。検索のあとに検査していて、検索の前の検査になりません。`filter` もありません。
    - D: 正しい。

    **スキル:** [3.2.8](../domain3.md#skill-3-2-8) / **参照:** [ApplyGuardrail](../../../services/ai.md#apply-guardrail)、[Knowledge Bases を呼ぶ](../../../services/ai.md#knowledge-bases)

### 問17 {#q17}

言い換えの質問が多く、同じ回答を何度も生成しています。検索パイプラインに加えて、FM の呼び出しを減らします。何を実装しますか。

- A. ハイブリッド検索
- B. プロンプトキャッシュの TTL を延ばす
- C. セマンティックキャッシュ
- D. リランクの対象の件数を増やす

??? success "答えと解説"
    **正解: C**

    セマンティックキャッシュは、意味の似た質問に保存した回答を返し、モデルを呼びません。

    - A: 誤り。検索の精度の手法で、FM の呼び出しは減りません。
    - B: 誤り。固定の前半を再利用する手法で、言い換えの質問を同じものとして扱いません。
    - C: 正しい。
    - D: 誤り。生成の呼び出しは減りません。

    **スキル:** [3.2.8](../domain3.md#skill-3-2-8) / **参照:** [キャッシュの種類](../../../services/genai-apps.md#caching)

### 問18 {#q18}

質問の文に「2025 年の人事規定」と書かれていたら、自動で年と部署のフィルターを付けて検索します。どの設定ですか。

- A. `rerankingConfiguration` で並べ替える
- B. `dataDeletionPolicy`
- C. `implicitFilterConfiguration`
- D. `overlapPercentage`

??? success "答えと解説"
    **正解: C**

    `implicitFilterConfiguration` は質問からフィルターを自動生成します。

    - A: 誤り。結果の並べ替えの設定です。
    - B: 誤り。データソースを消すときの設定です。
    - C: 正しい。
    - D: 誤り。チャンクの重なりの設定です。

    **スキル:** [3.2.8](../domain3.md#skill-3-2-8) / **参照:** [検索の改善](../../../services/genai-apps.md#retrieval-optimization)、[Knowledge Bases のパラメータ](../../../services/ai.md#kb-params)

### 問19 {#q19}

S3 の文書を更新してから、数分以内に回答へ反映させます。同期の仕組みとして適切なものはどれですか。

- A. S3 イベントを EventBridge で受け、Lambda から `StartIngestionJob` を呼ぶ
- B. 1 か月ごとに全ナレッジベースを作り直す
- C. FM を毎回ファインチューニングして、新しい文書を数分おきに学習させる
- D. 何もしない。Knowledge Bases は S3 を常時監視する

??? success "答えと解説"
    **正解: A**

    変更の検知には S3 イベント、EventBridge、Lambda を組み合わせ、`StartIngestionJob` で差分を同期します。

    - A: 正しい。
    - B: 誤り。数分以内の要件に合いません。同期は差分だけで済みます。
    - C: 誤り。更新のたびに再学習が必要で、数分では反映できません。
    - D: 誤り。ファイルを変えても、同期は自動では動きません。

    **スキル:** [3.3.11](../domain3.md#skill-3-3-11) / **参照:** [同期と鮮度](../../../services/genai-apps.md#kb-sync)

### 問20 {#q20}

夜間に 1 回同期する運用で、S3 の 100 万件のうち更新は 500 件です。同期ジョブの処理の範囲はどれですか。

- A. 新しく追加された文書だけ。変更と削除は反映しない
- B. 追加、変更、削除された文書だけ
- C. 全 100 万件を毎回処理する
- D. メタデータのファイルだけ

??? success "答えと解説"
    **正解: B**

    同期は差分だけを処理します。頻繁に実行しやすいのはこのためです。

    - A: 誤り。変更と削除も対象です。
    - B: 正しい。
    - C: 誤り。同期は増分で処理します。
    - D: 誤り。文書の本体も同期の対象です。

    **スキル:** [3.3.11](../domain3.md#skill-3-3-11) / **参照:** [同期と鮮度](../../../services/genai-apps.md#kb-sync)

### 問21 {#q21}

規定の文書の更新を、品質を確認してから本番の RAG に反映します。評価に合格しなければ切り替えません。適切な実装はどれですか。

- A. EventBridge のスケジュールで同期だけを実行し、評価は手で後から行う
- B. S3 のライフサイクルで、古い文書を移す
- C. 同期を止めて、担当者が回答を手で直す
- D. Step Functions で同期、評価、切り替えを順に実行する

??? success "答えと解説"
    **正解: D**

    Step Functions で同期、評価、切り替えの順に実行すれば、確認してから反映できます。

    - A: 誤り。定期の同期はできますが、評価と切り替えを組み込めません。
    - B: 誤り。品質の確認や切り替えの機能はありません。
    - C: 誤り。運用が続かず、更新が反映されません。
    - D: 正しい。

    **スキル:** [3.3.11](../domain3.md#skill-3-3-11) / **参照:** [同期と鮮度](../../../services/genai-apps.md#kb-sync)
