# モデルと AI の評価の問題集

対象の解説: [評価指標](../../../services/ai-fundamentals.md#metrics)、[NLP の指標](../../../services/ai-fundamentals.md#nlp-metrics)、[Bedrock Evaluations](../../../services/genai-apps.md#bedrock-evaluations)

### 問1 {#q1}

従来の ML と FM の実験で、パラメータ、指標、成果物を記録して比較します。どのツールが適切ですか。

- A. CloudTrail
- B. AWS Config
- C. MLflow on SageMaker AI
- D. Glue Data Catalog のテーブルのバージョン

??? success "答えと解説"
    **正解: C**

    MLflow はパラメータ、指標、成果物を記録し、従来の ML と FM の実験に使えます。

    - A: 誤り。API の呼び出しの記録で、実験の指標は記録しません。
    - B: 誤り。リソースの設定の記録です。
    - C: 正しい。
    - D: 誤り。データのメタデータの管理で、実験の記録ではありません。

    **スキル:** [2.3.1](../domain2.md#skill-2-3-1) / **参照:** [MLflow](../../../services/sagemaker.md#mlflow)

### 問2 {#q2}

半年前の実験の結果を再現します。記録が必要なものの組み合わせを選んでください。（2つ選択）

- A. 実験に参加した人数
- B. コードのコミットとハイパーパラメータ
- C. インスタンスの課金の明細
- D. 当時の CloudWatch アラームの状態
- E. データのバージョン

??? success "答えと解説"
    **正解: B, E**

    再現するには、データのバージョン、コードのコミット、ハイパーパラメータを記録します。

    - A: 誤り。再現に関係しません。
    - B: 正しい。同じ処理と同じ設定で学習する必要があります。
    - C: 誤り。コストの情報で、結果の再現には使えません。
    - D: 誤り。運用の状態で、学習結果の再現には使えません。
    - E: 正しい。同じデータで学習する必要があります。

    **スキル:** [2.3.1](../domain2.md#skill-2-3-1) / **参照:** [MLflow](../../../services/sagemaker.md#mlflow)

### 問3 {#q3}

FM とプロンプトの組み合わせを、同じ評価データで比べて結果を残します。それぞれの役割の組み合わせとして正しいものはどれですか。

- A. Knowledge Bases が評価を実行し、Lambda がプロンプトを保存する
- B. Prompt Management が評価を実行し、Bedrock Evaluations がプロンプトを保存する
- C. CloudWatch が評価を実行し、X-Ray がプロンプトを保存する
- D. Bedrock Evaluations が評価し、Prompt Management がプロンプトの版を管理する

??? success "答えと解説"
    **正解: D**

    モデルとプロンプトの評価は Bedrock Evaluations、プロンプトのバージョンとバリアントは Prompt Management です。

    - A: 誤り。評価と版の管理の機能ではありません。
    - B: 誤り。役割が逆です。
    - C: 誤り。監視のサービスで、この役割はありません。
    - D: 正しい。

    **スキル:** [2.3.1](../domain2.md#skill-2-3-1) / **参照:** [Bedrock Evaluations](../../../services/genai-apps.md#bedrock-evaluations)、[プロンプトの管理](../../../services/genai-apps.md#prompt-management)

### 問4 {#q4}

融資の否決の理由を、申込者ごとに示します。アカウントでは SageMaker Clarify を使えません。適切な方法はどれですか。

- A. Model Monitor の特徴量の寄与のドリフトを見る
- B. SHAP ライブラリで特徴量ごとの寄与を計算する
- C. Bedrock Evaluations の Stereotyping の指標を使う
- D. Model Cards に全体の説明を書く

??? success "答えと解説"
    **正解: B**

    特徴量ごとの予測への寄与は SHAP です。Clarify を新規に使えないなら、SHAP を直接使います。

    - A: 誤り。全体の順位の変化の監視で、申込者ごとの理由にはなりません。
    - B: 正しい。
    - C: 誤り。FM の評価で、表データの予測の説明に使えません。
    - D: 誤り。用途やリスクの記録で、申込者ごとの理由は出ません。

    **スキル:** [2.3.4](../domain2.md#skill-2-3-4) / **参照:** [Clarify](../../../services/sagemaker.md#clarify)、[説明可能性と透明性](../../../services/ai-fundamentals.md#explainability)

### 問5 {#q5}

監査のために、モデルの用途、学習データ、評価結果、リスクをまとめて記録します。どの機能ですか。

- A. Model Cards
- B. 部分依存プロット
- C. データキャプチャ
- D. Feature Store

??? success "答えと解説"
    **正解: A**

    Model Cards は用途、学習、評価、リスクの記録です。

    - A: 正しい。
    - B: 誤り。特徴量と予測の関係の可視化で、記録の機能ではありません。
    - C: 誤り。本番の入出力を保存する機能です。
    - D: 誤り。特徴量の管理です。

    **スキル:** [2.3.4](../domain2.md#skill-2-3-4) / **参照:** [Model Cards](../../../services/sagemaker.md#model-cards)

### 問6 {#q6}

生成 AI の回答の根拠を利用者に示します。適切な手段はどれですか。

- A. RAG の引用を返す
- B. temperature を上げる
- C. プロンプトキャッシュを使う
- D. 呼び出しログを無効にする

??? success "答えと解説"
    **正解: A**

    RAG の引用は根拠を示します。エージェントならトレースで推論の過程を示します。

    - A: 正しい。
    - B: 誤り。文の多様性の設定で、根拠を示しません。
    - C: 誤り。コストと遅延の手法です。
    - D: 誤り。根拠を示す手段にならず、監査の記録も失います。

    **スキル:** [2.3.4](../domain2.md#skill-2-3-4) / **参照:** [説明可能性と透明性](../../../services/ai-fundamentals.md#explainability)

### 問7 {#q7}

スパム検知の結果は TP 80、FN 20、FP 30、TN 870 です。適合率に最も近い値はどれですか。

- A. 0.7619
- B. 0.95
- C. 0.727
- D. 0.80

??? success "答えと解説"
    **正解: C**

    適合率は TP / (TP + FP) = 80 / 110 = 0.727 です。

    - A: 誤り。F1 です。
    - B: 誤り。精度（accuracy）です。
    - C: 正しい。
    - D: 誤り。再現率です。

    **スキル:** [2.3.6](../domain2.md#skill-2-3-6) / **参照:** [評価指標](../../../services/ai-fundamentals.md#metrics)

### 問8 {#q8}

病気の検査で、見逃しの損失が誤検知よりはるかに大きいです。重視する指標はどれですか。

- A. 適合率
- B. 再現率
- C. 精度（accuracy）
- D. 特異度（TN / (TN + FP)）

??? success "答えと解説"
    **正解: B**

    見逃しの損失が大きいなら再現率を重視します。

    - A: 誤り。誤検知の損失が大きいときに重視します。
    - B: 正しい。
    - C: 誤り。陰性が多いと、見逃しが多くても高くなります。
    - D: 誤り。陰性を正しく当てる割合で、見逃しを表しません。

    **スキル:** [2.3.6](../domain2.md#skill-2-3-6) / **参照:** [評価指標](../../../services/ai-fundamentals.md#metrics)

### 問9 {#q9}

配送時間の回帰モデルで、まれな大きな誤差を強く罰して評価します。どの指標を見ますか。

- A. MAPE
- B. R²
- C. MAE
- D. RMSE

??? success "答えと解説"
    **正解: D**

    RMSE は大きな誤差を強く罰します。MAE は外れ値に強い指標です。

    - A: 誤り。誤差の割合の指標で、大きな誤差を強く罰する指標ではありません。
    - B: 誤り。説明できる分散の割合で、大きな誤差を強く罰する指標ではありません。
    - C: 誤り。外れ値に強く、大きな誤差を強くは罰しません。
    - D: 正しい。

    **スキル:** [2.3.6](../domain2.md#skill-2-3-6) / **参照:** [回帰の指標](../../../services/ai-fundamentals.md#regression-metrics)

### 問10 {#q10}

FM の要約の品質を、人の評価者に採点してもらいます。Bedrock の機能はどれですか。

- A. Provisioned Throughput
- B. `ApplyGuardrail` の検査の結果を人の評価者なしで集計する
- C. Guardrails の拒否トピック
- D. Bedrock Evaluations の人のジョブ

??? success "答えと解説"
    **正解: D**

    文章の品質を人が評価するなら、Bedrock Evaluations の人のジョブです。

    - A: 誤り。容量の機能です。
    - B: 誤り。安全策の検査で、文章の品質の評価ではありません。
    - C: 誤り。話題を禁止する機能です。
    - D: 正しい。

    **スキル:** [2.3.7](../domain2.md#skill-2-3-7) / **参照:** [Bedrock Evaluations](../../../services/genai-apps.md#bedrock-evaluations)

### 問11 {#q11}

新規のシステムで、信頼度が 80% 未満の予測だけ担当者の確認に回します。A2I は新規に使えません。代替の実装はどれですか。

- A. Step Functions の `waitForTaskToken`
- B. CloudWatch の異常検知だけで判定して、人を介さず自動で確定する
- C. Macie の検出結果で担当者を選ぶ
- D. FM に「人のように確認して」と指示する

??? success "答えと解説"
    **正解: A**

    新規の代替の例は、Step Functions の人の承認と Bedrock の人による評価です。`waitForTaskToken` で承認を待てます。

    - A: 正しい。
    - B: 誤り。人の確認になりません。
    - C: 誤り。機密データの検出で、人の確認の仕組みではありません。
    - D: 誤り。人の確認になりません。

    **スキル:** [2.3.7](../domain2.md#skill-2-3-7) / **参照:** [人による確認](../../../services/genai-apps.md#human-in-the-loop)、[Augmented AI](../../../services/ai-managed-services.md#a2i)

### 問12 {#q12}

生成 AI の回答に対する利用者の「よい、悪い」の評価を集めて、改善に使います。適切な構成はどれですか。

- A. 利用者の全ての評価を Prompt Management のバリアントとして登録して比べる
- B. API Gateway、Lambda、DynamoDB で保存し、低評価をレビューする
- C. CloudTrail のログに評価を書き込み、Athena で読む
- D. 評価を受け取らず、FM の temperature を毎日変える

??? success "答えと解説"
    **正解: B**

    利用者の評価は API Gateway、Lambda、DynamoDB で集めます。低評価の例はゴールデンデータセットやプロンプトの改善に使います。

    - A: 誤り。プロンプトの版の管理の機能です。
    - B: 正しい。
    - C: 誤り。API の記録で、利用者の評価の保存先ではありません。
    - D: 誤り。改善の根拠がありません。

    **スキル:** [2.3.7](../domain2.md#skill-2-3-7) / **参照:** [利用者からの評価](../../../services/genai-apps.md#user-feedback)

### 問13 {#q13}

機械翻訳のモデルを、正解の翻訳文との n-gram の一致で評価します。どの指標ですか。

- A. ROUGE
- B. BERTScore
- C. BLEU
- D. WER

??? success "答えと解説"
    **正解: C**

    BLEU は正解文との n-gram の一致を見ます。適合率寄りの指標です。

    - A: 誤り。主に要約の評価に使います。
    - B: 誤り。埋め込みで意味の近さを比べる指標で、n-gram の一致を見ません。
    - C: 正しい。
    - D: 誤り。単語の挿入、削除、置換の数を見る指標で、n-gram の一致を見ません。

    **スキル:** [2.3.8](../domain2.md#skill-2-3-8) / **参照:** [NLP の指標](../../../services/ai-fundamentals.md#nlp-metrics)

### 問14 {#q14}

要約モデルの ROUGE は低いのですが、人が読むと正確な言い換えです。評価に足す指標はどれですか。

- A. 文字の編集距離
- B. クロスエントロピー損失
- C. BERTScore
- D. BLEU

??? success "答えと解説"
    **正解: C**

    BERTScore は BERT の埋め込みで意味の近さを比べるので、言い換えも評価できます。

    - A: 誤り。文字の一致を見るので、言い換えを低く評価します。
    - B: 誤り。学習の損失で、要約の意味の近さを見ません。
    - C: 正しい。
    - D: 誤り。これも語の一致を見るので、言い換えを低く評価します。

    **スキル:** [2.3.8](../domain2.md#skill-2-3-8) / **参照:** [NLP の指標](../../../services/ai-fundamentals.md#nlp-metrics)

### 問15 {#q15}

a = (1, 0)、b = (1, 1) のコサイン類似度はどれですか。

- A. 0.707
- B. 0
- C. 1.4142
- D. 0.5

??? success "答えと解説"
    **正解: A**

    内積 1 を大きさ 1 × 1.414 で割り、0.707 です。1 に近いほど似ています。

    - A: 正しい。
    - B: 誤り。直交するときの値です。
    - C: 誤り。b の大きさです。コサイン類似度は 1 を超えません。
    - D: 誤り。大きさで割る計算が合いません。

    **スキル:** [2.3.8](../domain2.md#skill-2-3-8) / **参照:** [NLP の指標](../../../services/ai-fundamentals.md#nlp-metrics)

### 問16 {#q16}

問い合わせの回答の品質を、大量に自動で採点し、理由も残します。人の評価者は使いません。どの方法ですか。

- A. CloudWatch の `Invocations` で採点する
- B. 判定モデルで LLM-as-a-judge を使う
- C. ROUGE だけで採点する
- D. 全件を A/B テストに流す

??? success "答えと解説"
    **正解: B**

    LLM-as-a-judge は別の LLM が出力を採点し、説明を付けます。Bedrock Evaluations の判定モデルで実行します。

    - A: 誤り。呼び出しの回数で、品質は分かりません。
    - B: 正しい。
    - C: 誤り。語の一致の指標で、理由は残りません。
    - D: 誤り。業務指標の比較で、応答ごとの採点になりません。

    **スキル:** [2.3.9](../domain2.md#skill-2-3-9) / **参照:** [Bedrock Evaluations](../../../services/genai-apps.md#bedrock-evaluations)

### 問17 {#q17}

FM の応答の偏りを評価します。性別だけを変えたプロンプトの比較に加えて、Bedrock Evaluations で見る指標はどれですか。

- A. `TimeToFirstToken`
- B. CitationPrecision
- C. ContextCoverage
- D. Stereotyping

??? success "答えと解説"
    **正解: D**

    バイアスの検出には、Stereotyping の指標や、属性だけを変えたプロンプトの比較を使います。

    - A: 誤り。遅延の指標です。
    - B: 誤り。引用の正しさの指標です。
    - C: 誤り。検索の指標です。
    - D: 正しい。

    **スキル:** [2.3.9](../domain2.md#skill-2-3-9) / **参照:** [透明性と公平性](../../../services/genai-apps.md#transparency-fairness)

### 問18 {#q18}

AgentCore Runtime のエージェントの品質を、実行のトレースから採点します。どの機能ですか。

- A. Bedrock Evaluations の RAG のジョブ
- B. AgentCore Evaluations
- C. CloudWatch の異常検知
- D. Prompt Management のバリアント

??? success "答えと解説"
    **正解: B**

    エージェントは AgentCore Evaluations でトレースを採点します。

    - A: 誤り。モデルや RAG の評価で、Runtime のトレースを採点する機能ではありません。
    - B: 正しい。
    - C: 誤り。指標の変動の検知で、エージェントの品質は採点しません。
    - D: 誤り。プロンプトの案を比べる機能で、トレースは採点しません。

    **スキル:** [2.3.9](../domain2.md#skill-2-3-9) / **参照:** [エージェントの評価](../../../services/genai-apps.md#agent-evaluation)
