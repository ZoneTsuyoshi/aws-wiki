# コストと容量の問題集

対象の解説: [予算の種類](../../../services/cost-management.md#budget-types)、[Bedrock の料金](../../../services/cost-management.md#bedrock-pricing)、[推論の最適化](../../../services/sagemaker.md#inference-optimization)

### 問1 {#q1}

本番のエンドポイントの信頼性を上げます。AZ の障害に備える最も基本の設定はどれですか。

- A. エンドポイント名を変える
- B. 1 台の大きなインスタンスに変える
- C. インスタンスを 2 台以上にする
- D. データキャプチャを 100% にする

??? success "答えと解説"
    **正解: C**

    インスタンスを 2 台以上にすると、複数の AZ に分散します。

    - A: 誤り。信頼性に関係しません。
    - B: 誤り。1 台では AZ の障害に耐えられません。
    - C: 正しい。
    - D: 誤り。監視の設定で、可用性は上がりません。

    **スキル:** [4.2.4](../domain4.md#skill-4-2-4) / **参照:** [リアルタイム](../../../services/sagemaker.md#realtime)

### 問2 {#q2}

Bedrock のオンデマンドで、ピーク時に容量不足のエラーが出ます。容量を確保する選択肢を選んでください。（2つ選択）

- A. Flex 層に切り替える
- B. `maxTokens` を最大にする
- C. Provisioned Throughput を購入する
- D. クロスリージョン推論を使う
- E. 埋め込みの次元を下げる

??? success "答えと解説"
    **正解: C, D**

    Bedrock の容量不足には、クロスリージョン推論か Provisioned Throughput を検討します。

    - A: 誤り。安くなりますが遅くなり、容量の確保の手段ではありません。
    - B: 誤り。クォータの予約が増えて悪化します。
    - C: 正しい。専用の処理量を確保できます。
    - D: 正しい。複数のリージョンの容量へ振り分けられます。
    - E: 誤り。関係がありません。

    **スキル:** [4.2.4](../domain4.md#skill-4-2-4) / **参照:** [耐障害の設計](../../../services/genai-apps.md#fm-resilience)

### 問3 {#q3}

使用率の低いエンドポイントが 20 個あり、それぞれ別のインスタンスで動いています。容量を最適化する手順の順序として適切なものはどれですか。

- A. Savings Plans を先に買い、そのあとで使用量を減らし、最後に種類とサイズを見直す
- B. 全てを 1 つの大きな GPU に載せ、測定はしない
- C. 自動スケーリングを無効にしてから、最大の台数に固定する
- D. 推論の種類を選ぶ、サイズを決める、統合する、スケーリング、Savings Plans

??? success "答えと解説"
    **正解: D**

    手順は、推論の種類を選ぶ、Inference Recommender でサイズを決める、統合する、自動スケーリング、Savings Plans の順です。

    - A: 誤り。不要な容量に対してコミットしてしまいます。
    - B: 誤り。サイズの根拠がありません。
    - C: 誤り。過剰な容量が固定されます。
    - D: 正しい。

    **スキル:** [4.2.4](../domain4.md#skill-4-2-4) / **参照:** [推論の最適化](../../../services/sagemaker.md#inference-optimization)

### 問4 {#q4}

月の予算の超過に早く気付き、超えそうなら新しいリソースの作成を止めます。AWS Budgets の設定として適切なものを選んでください。（2つ選択）

- A. コストをリアルタイムに止める機能として Cost Explorer を使う
- B. 通知の種類を `FORECASTED` にして、しきい値を低めにする
- C. Trusted Advisor のチェックを有効にするだけにする
- D. 予算アクションで IAM ポリシーを適用する
- E. 超過後の通知だけにする

??? success "答えと解説"
    **正解: B, D**

    Budgets の通知は遅れることがあるので `FORECASTED` を使い、しきい値を低めにします。予算アクションで IAM ポリシーを適用できます。

    - A: 誤り。実績の分析のツールです。
    - B: 正しい。通知の遅れに備えられます。
    - C: 誤り。超過を止める機能ではありません。
    - D: 正しい。新しいリソースの作成を止められます。
    - E: 誤り。気付くのが遅れます。

    **スキル:** [4.2.5](../domain4.md#skill-4-2-5) / **参照:** [予算の種類](../../../services/cost-management.md#budget-types)、[予算アクション](../../../services/cost-management.md#budget-actions)

### 問5 {#q5}

チームごとの ML のコストを Cost Explorer で見たいです。リソースに `team` タグを付けましたが、請求データに出ません。何が足りませんか。

- A. コスト配分タグの有効化
- B. Budgets のしきい値の設定
- C. タグの値を大文字に変更すること
- D. リソースの再作成

??? success "答えと解説"
    **正解: A**

    タグは付けるだけでは請求データに出ません。コスト配分タグとして有効化します。

    - A: 正しい。
    - B: 誤り。タグの請求データへの表示とは別です。
    - C: 誤り。値の形式の問題ではありません。
    - D: 誤り。タグの有効化で足ります。

    **スキル:** [4.2.5](../domain4.md#skill-4-2-5) / **参照:** [コスト配分タグ](../../../services/cost-management.md#cost-allocation-tags)

### 問6 {#q6}

次の目的とツールの組み合わせとして正しいものはどれですか。

- A. しきい値で通知: Compute Optimizer
- B. リソースの適正サイズ: Compute Optimizer
- C. サービスクォータの引き上げの申請: Cost Explorer
- D. 実績の分析: Service Quotas

??? success "答えと解説"
    **正解: B**

    Compute Optimizer は適正サイズ、Cost Explorer は実績の分析、Budgets はしきい値の通知、Service Quotas はクォータの管理です。

    - A: 誤り。Budgets の役割です。
    - B: 正しい。
    - C: 誤り。Service Quotas の役割です。
    - D: 誤り。Cost Explorer の役割です。

    **スキル:** [4.2.5](../domain4.md#skill-4-2-5) / **参照:** [推奨を出すサービス](../../../services/cost-management.md#recommendation-tools)

### 問7 {#q7}

24 時間一定の負荷の GPU のエンドポイントを 3 年運用します。購入方法はどれですか。

- A. オンデマンドのまま
- B. SageMaker AI Savings Plans
- C. Managed Spot
- D. 1 年分のトレーニングプランの GPU 容量の予約

??? success "答えと解説"
    **正解: B**

    継続する利用には Savings Plans が向きます。1 年か 3 年で、最大 64% の割引です。

    - A: 誤り。継続する利用なら割引が受けられます。
    - B: 正しい。
    - C: 誤り。学習向けで、エンドポイントには使いません。
    - D: 誤り。大規模な学習の GPU 容量の予約です。

    **スキル:** [4.2.6](../domain4.md#skill-4-2-6) / **参照:** [インスタンスの選び方](../../../services/sagemaker.md#instance-selection)

### 問8 {#q8}

夜間の学習ジョブは中断されても問題なく、コストを最大に下げます。割引の最大の値も含めて正しいものはどれですか。

- A. トレーニングプラン、最大 90%
- B. Savings Plans、最大 64%
- C. オンデマンド、最大 90%
- D. Managed Spot、最大 90%

??? success "答えと解説"
    **正解: D**

    中断できる学習は Managed Spot です。最大 90% の割引です。

    - A: 誤り。容量の予約の仕組みです。
    - B: 誤り。継続する利用の割引で、スポットの割引より小さい値です。
    - C: 誤り。オンデマンドが基準です。割引はありません。
    - D: 正しい。

    **スキル:** [4.2.6](../domain4.md#skill-4-2-6) / **参照:** [購入の選び方](../../../services/cost-management.md#purchase-choice)、[マネージドスポット学習](../../../services/sagemaker.md#spot-training)

### 問9 {#q9}

大規模な FM の学習を来月行います。GPU の容量を計画的に確保します。どれですか。

- A. SageMaker AI Savings Plans
- B. オンデマンドの開始を毎時試す
- C. トレーニングプラン
- D. Managed Spot

??? success "答えと解説"
    **正解: C**

    大規模な学習の GPU 容量はトレーニングプランで予約します。

    - A: 誤り。割引の仕組みで、容量の予約ではありません。
    - B: 誤り。容量を確保できる保証がありません。
    - C: 正しい。
    - D: 誤り。中断があり、容量も保証されません。

    **スキル:** [4.2.6](../domain4.md#skill-4-2-6) / **参照:** [インスタンスの選び方](../../../services/sagemaker.md#instance-selection)

### 問10 {#q10}

入力 100 万トークンあたり $3、出力 100 万トークンあたり $15 の仮のモデルです。1 日 1,000 回、1 回あたり入力 2,000、出力 500 トークンです。1 日の費用はどれですか。

- A. $13.5
- B. $135
- C. $7.5
- D. $6

??? success "答えと解説"
    **正解: A**

    入力は 200 万トークンで $6、出力は 50 万トークンで $7.5 で、合計 $13.5 です。

    - A: 正しい。
    - B: 誤り。桁が違います。
    - C: 誤り。出力の分だけです。
    - D: 誤り。入力の分だけです。

    **スキル:** [4.2.7](../domain4.md#skill-4-2-7) / **参照:** [Bedrock の料金](../../../services/cost-management.md#bedrock-pricing)、[トークン](../../../services/ai-fundamentals.md#tokens)

### 問11 {#q11}

FM のコストを見積もります。トークンのほかに含める項目を選んでください。（2つ選択）

- A. CloudTrail の管理イベントの最初の証跡
- B. 利用者の数だけ増える IAM ユーザーの料金
- C. Guardrails の利用料金
- D. ナレッジベースのベクトルストアの費用
- E. Inspector の検出の数に応じた FM の割引

??? success "答えと解説"
    **正解: C, D**

    Guardrails、Knowledge Bases のベクトルストア、カスタムモデルの保存の費用も含めて見積もります。

    - A: 誤り。FM の推論のコストの見積もりの主な項目ではありません。
    - B: 誤り。IAM に料金はかかりません。
    - C: 正しい。
    - D: 正しい。
    - E: 誤り。そのような割引はありません。

    **スキル:** [4.2.7](../domain4.md#skill-4-2-7) / **参照:** [Bedrock の料金](../../../services/cost-management.md#bedrock-pricing)

### 問12 {#q12}

Bedrock のサービス層の特徴の組み合わせとして正しいものはどれですか。

- A. Priority は Standard より安く遅い。Flex は Standard より高く速い
- B. Priority は割増で速い。Flex は割引で処理に時間がかかる
- C. Priority も Flex も Standard と同じ価格で、応答の速さだけが異なる
- D. Priority は容量を時間単位で予約する。Flex はモデルユニットで買う

??? success "答えと解説"
    **正解: B**

    Priority は標準のオンデマンドより割増で最速の応答、Flex は割引で長い処理時間を許容できる処理向けです。

    - A: 誤り。逆です。
    - B: 正しい。
    - C: 誤り。価格も異なります。
    - D: 誤り。モデルユニットは Provisioned Throughput の単位です。

    **スキル:** [4.2.7](../domain4.md#skill-4-2-7) / **参照:** [Bedrock の料金](../../../services/cost-management.md#bedrock-pricing)

### 問13 {#q13}

長いシステムプロンプトと固定の社内規定を毎回送っています。後半の質問だけが毎回変わります。コストを下げる変更はどれですか。

- A. `maxTokens` を最大にする
- B. 毎回 temperature を変える
- C. 固定の内容を毎回後ろに置き、毎回変わる質問を先に置く
- D. 固定の内容を先に置いてプロンプトキャッシュを使う

??? success "答えと解説"
    **正解: D**

    プロンプトキャッシュは固定の前半を再利用します。TTL は多くのモデルで 5 分です。

    - A: 誤り。入力のコストは減りません。
    - B: 誤り。コストに関係しません。
    - C: 誤り。キャッシュは前半の一致で効くので、固定の内容を先に置きます。
    - D: 正しい。

    **スキル:** [4.2.9](../domain4.md#skill-4-2-9) / **参照:** [トークンの削減](../../../services/genai-apps.md#token-efficiency)

### 問14 {#q14}

`maxTokens` を実態より大きく設定すると、コスト以外に何が起きますか。

- A. 必ず応答が短くなる
- B. 未使用の分のトークンも出力料金で課金される
- C. クォータの予約が増えて、スロットリングの原因になる
- D. プロンプトキャッシュが無効になる

??? success "答えと解説"
    **正解: C**

    `maxTokens` が大きすぎると、クォータの予約も増えてスロットリングの原因になります。

    - A: 誤り。上限を上げても短くなりません。
    - B: 誤り。課金されるのは実際の出力トークンです。
    - C: 正しい。
    - D: 誤り。キャッシュの条件とは関係ありません。

    **スキル:** [4.2.9](../domain4.md#skill-4-2-9) / **参照:** [エラーとスロットリング](../../../services/ai.md#errors-throttling)

### 問15 {#q15}

会話の履歴が長くなり、トークンが増えています。アプリごとのコストも追跡します。適切な手段を選んでください。（2つ選択）

- A. タグ付きのアプリケーション推論プロファイルを使う
- B. 全履歴を毎回そのまま送る
- C. Provisioned Throughput を全アプリで共有し、集計はしない
- D. 古い履歴を要約する
- E. 履歴を 2 回繰り返して精度を上げる

??? success "答えと解説"
    **正解: A, D**

    文脈の削減には履歴の要約を使います。アプリごとのコストはアプリケーション推論プロファイルのタグで追跡します。

    - A: 正しい。アプリごとにコストを追跡できます。
    - B: 誤り。トークンが増え続けます。
    - C: 誤り。コストの追跡になりません。
    - D: 正しい。文脈を減らせます。
    - E: 誤り。トークンが増えるだけです。

    **スキル:** [4.2.9](../domain4.md#skill-4-2-9) / **参照:** [トークンの削減](../../../services/genai-apps.md#token-efficiency)、[推論の容量とプロファイル](../../../services/genai-apps.md#inference-profiles)

### 問16 {#q16}

プロンプトキャッシュの効果を確認します。CloudWatch で見る Bedrock の指標はどれですか。

- A. `CacheReadInputTokenCount`
- B. `Invocation4XXErrors`
- C. `ApproximateBacklogSizePerInstance`
- D. `OverheadLatency`

??? success "答えと解説"
    **正解: A**

    キャッシュから読んだ入力トークンは `CacheReadInputTokenCount` です。

    - A: 正しい。
    - B: 誤り。SageMaker AI のエンドポイントのエラーの指標です。
    - C: 誤り。非同期推論のキューの指標です。
    - D: 誤り。SageMaker AI のエンドポイントの遅延の指標です。

    **スキル:** [4.2.10](../domain4.md#skill-4-2-10) / **参照:** [見るべき指標](../../../services/genai-apps.md#genai-metrics)

### 問17 {#q17}

ベクトルの保存のコストが急増しました。文書は 1 億チャンクで、古い文書の検索はまれです。対策として適切なものを選んでください。（2つ選択）

- A. 低頻度のデータを S3 Vectors へ移す
- B. 次元を下げ、精度を評価で確かめる
- C. 古い文書を複製してレプリカを増やす
- D. 全文書を毎日再埋め込みする
- E. OCU の上限を外す

??? success "答えと解説"
    **正解: A, B**

    ベクトルの保存は次元と件数で決まります。次元の削減と、低頻度のデータの S3 Vectors への移動を検討します。

    - A: 正しい。低コストで保存できます。
    - B: 正しい。保存量が減ります。
    - C: 誤り。保存量が増えます。
    - D: 誤り。埋め込みの計算コストが増えます。
    - E: 誤り。コストが増える方向です。

    **スキル:** [4.2.10](../domain4.md#skill-4-2-10) / **参照:** [ベクトルストア](../../../services/genai-apps.md#vector-stores)、[埋め込みの選び方](../../../services/genai-apps.md#embedding-selection)

### 問18 {#q18}

Bedrock の日次のコストが突然 3 倍になったことに、自動で気付きたいです。どの機能が適切ですか。

- A. Budgets の固定のしきい値の通知
- B. Cost Anomaly Detection
- C. Compute Optimizer の推奨
- D. X-Ray のサービスマップで呼び出しの増加を見る

??? success "答えと解説"
    **正解: B**

    コストの急増の検知には Cost Anomaly Detection を使います。

    - A: 誤り。決めた金額を超えたときの通知で、いつもと違う急増の検知ではありません。
    - B: 正しい。
    - C: 誤り。適正サイズの推奨で、コストの急増を検知しません。
    - D: 誤り。呼び出しの経路の可視化で、コストの急増を検出しません。

    **スキル:** [4.2.10](../domain4.md#skill-4-2-10) / **参照:** [Cost Anomaly Detection](../../../services/cost-management.md#cost-anomaly-detection)
