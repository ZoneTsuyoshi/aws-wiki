# 監視と調査の問題集

対象の解説: [SageMaker の CloudWatch メトリクス](../../../services/sagemaker.md#cloudwatch-metrics)、[Bedrock のメトリクス](../../../services/ai.md#bedrock-metrics)、[ダッシュボード](../../../services/observability.md#dashboards)

### 問1 {#q1}

サーバーレス推論の遅延が増えました。`ModelLatency` は変わらず、`OverheadLatency` が増えています。切り分けの結論はどれですか。

- A. モデルの処理が遅くなった。インスタンスを大きくする
- B. 基盤側のコールドスタートが原因である
- C. クライアントの権限が足りない。IAM を直す
- D. データドリフトである。再学習する

??? success "答えと解説"
    **正解: B**

    `ModelLatency` が大きければモデルやインスタンス、`OverheadLatency` が大きければコールドスタートなどの基盤側です。

    - A: 誤り。`ModelLatency` が変わらないので、モデルは原因ではありません。
    - B: 正しい。
    - C: 誤り。権限の問題は遅延の増加になりません。
    - D: 誤り。入力の分布の変化は遅延の内訳を説明しません。

    **スキル:** [4.1.2](../domain4.md#skill-4-1-2) / **参照:** [SageMaker の CloudWatch メトリクス](../../../services/sagemaker.md#cloudwatch-metrics)

### 問2 {#q2}

曜日で変動する呼び出し数に、固定のしきい値のアラームを設定すると誤報が多く出ます。適切な機能はどれですか。

- A. CloudTrail Lake のクエリ
- B. Budgets の予測アラート
- C. Logs Insights の毎日の手動のクエリ
- D. CloudWatch の異常検知

??? success "答えと解説"
    **正解: D**

    季節性のある指標には CloudWatch の異常検知を使います。

    - A: 誤り。API の記録のクエリで、指標の変動を学習しません。
    - B: 誤り。コストのしきい値の機能で、呼び出し数の異常の検出ではありません。
    - C: 誤り。自動のアラームになりません。
    - D: 正しい。

    **スキル:** [4.1.2](../domain4.md#skill-4-1-2) / **参照:** [異常検知](../../../services/observability.md#anomaly-detection)

### 問3 {#q3}

ML のワークフローの異常を検知します。次の組み合わせのうち正しいものを選んでください。（2つ選択）

- A. ログのパターンを Budgets で見る
- B. 推論のエラーを `Invocation5XXErrors` で見る
- C. Pipelines と Glue の状態変更を EventBridge で受ける
- D. 前処理の失敗を X-Ray の課金で見る
- E. データの品質を `ModelLatency` で見る

??? success "答えと解説"
    **正解: B, C**

    前処理は EventBridge、データの品質は Glue Data Quality、推論のエラーは `Invocation4XXErrors` と `Invocation5XXErrors` で見ます。

    - A: 誤り。コストの機能です。
    - B: 正しい。サーバー側のエラーを検知できます。
    - C: 正しい。前処理のジョブの失敗を検知できます。
    - D: 誤り。課金の情報では失敗を検知できません。
    - E: 誤り。遅延の指標で、データの品質は分かりません。

    **スキル:** [4.1.2](../domain4.md#skill-4-1-2) / **参照:** [SageMaker の CloudWatch メトリクス](../../../services/sagemaker.md#cloudwatch-metrics)、[Glue Data Quality](../../../services/data-engineering.md#glue-data-quality)

### 問4 {#q4}

対話アプリの「最初の応答が遅い」という声を調べます。どの Bedrock の指標を見ますか。

- A. `InputTokenCount`
- B. `InvocationLatency`
- C. `TimeToFirstToken`
- D. `CacheReadInputTokenCount`

??? success "答えと解説"
    **正解: C**

    `TimeToFirstToken` は最初のトークンまでの時間で、体感の待ち時間を表します。

    - A: 誤り。トークン数で、時間を示しません。
    - B: 誤り。最後のトークンまでの時間で、最初の応答の遅さを直接示しません。
    - C: 正しい。
    - D: 誤り。キャッシュから読んだトークン数です。

    **スキル:** [4.1.6](../domain4.md#skill-4-1-6) / **参照:** [Bedrock のメトリクス](../../../services/ai.md#bedrock-metrics)

### 問5 {#q5}

Bedrock でスロットリングが起きています。`Invocations` は増えていません。正しい説明と、見る指標はどれですか。

- A. `Invocations` に含まれない。`InvocationThrottles` を見る
- B. スロットリングは `InvocationServerErrors` に含まれる。これを見る
- C. スロットリングは起きていない。別の原因を探す
- D. スロットリングは `Invocations` に含まれる。`Invocations` だけ見る

??? success "答えと解説"
    **正解: A**

    スロットリングされた分は `Invocations` に含まれません。`InvocationThrottles` と `EstimatedTPMQuotaUsage` を見ます。

    - A: 正しい。
    - B: 誤り。含まれません。
    - C: 誤り。`Invocations` に含まれないので、この指標では判断できません。
    - D: 誤り。含まれません。

    **スキル:** [4.1.6](../domain4.md#skill-4-1-6) / **参照:** [Bedrock のメトリクス](../../../services/ai.md#bedrock-metrics)

### 問6 {#q6}

大きなプロンプトを送っているアプリを特定するため、CloudWatch Logs Insights でプロンプトを検索します。先に必要な設定はどれですか。

- A. CloudTrail のデータイベントを有効にする
- B. モデル呼び出しログを有効にする
- C. 生成 AI オブザーバビリティの画面を開く
- D. CloudTrail の管理イベントを有効にする

??? success "答えと解説"
    **正解: B**

    呼び出しログは既定で無効です。有効にすると Logs Insights で大きなプロンプトを探せます。

    - A: 誤り。API の記録で、プロンプトの本文を検索する設定ではありません。
    - B: 正しい。
    - C: 誤り。画面を開くだけではプロンプトの本文は記録されません。
    - D: 誤り。プロンプトの内容は記録されません。

    **スキル:** [4.1.6](../domain4.md#skill-4-1-6) / **参照:** [モデル呼び出しログ](../../../services/ai.md#invocation-logging)

### 問7 {#q7}

API Gateway、Lambda、エンドポイントをつなぐ推論のシステムで、どこで遅いかを探します。どのツールが適切ですか。

- A. CloudTrail
- B. CloudWatch Logs Insights
- C. エンドポイントの `ModelLatency`
- D. X-Ray

??? success "答えと解説"
    **正解: D**

    サービス間の呼び出しをつなげて遅い箇所を探すなら X-Ray です。

    - A: 誤り。誰が API を呼んだかの記録です。
    - B: 誤り。ログの検索で、サービスをまたぐ呼び出しの経路をつなげません。
    - C: 誤り。エンドポイントの中の遅延だけで、API Gateway や Lambda の区間は分かりません。
    - D: 正しい。

    **スキル:** [4.2.2](../domain4.md#skill-4-2-2) / **参照:** [X-Ray](../../../services/observability.md#xray)

### 問8 {#q8}

昨夜エンドポイントの設定を変更した人を調べます。どのサービスですか。

- A. Logs Insights
- B. AWS Config
- C. CloudTrail
- D. X-Ray

??? success "答えと解説"
    **正解: C**

    「誰が変更したか」は CloudTrail です。

    - A: 誤り。アプリのログの集計で、API を呼んだ人の記録の第一候補ではありません。
    - B: 誤り。設定の変化の記録で、誰が API を呼んだかは CloudTrail で確認します。
    - C: 正しい。
    - D: 誤り。遅い箇所を探すサービスです。

    **スキル:** [4.2.2](../domain4.md#skill-4-2-2) / **参照:** [CloudTrail と CloudWatch](../../../services/observability.md#cloudtrail-vs-cloudwatch)

### 問9 {#q9}

AgentCore のエージェントの動作を調べます。正しい説明を選んでください。（2つ選択）

- A. エージェントの動作は Cost Explorer だけで確認する
- B. トレースは S3 Glacier からしか読めない
- C. OpenTelemetry に対応している
- D. データは AWS の外にしか保存できない
- E. スパンとログは CloudWatch に保存される

??? success "答えと解説"
    **正解: C, E**

    AgentCore Observability はエージェントのスパンとログを CloudWatch に保存し、OpenTelemetry に対応します。

    - A: 誤り。コストの分析で、動作は分かりません。
    - B: 誤り。CloudWatch で確認できます。
    - C: 正しい。
    - D: 誤り。CloudWatch に保存されます。
    - E: 正しい。

    **スキル:** [4.2.2](../domain4.md#skill-4-2-2) / **参照:** [監視とオブザーバビリティ](../../../services/genai-apps.md#observability)

### 問10 {#q10}

複数のリージョンのエンドポイントの指標を、1 つの画面で見ます。追加のサービスを増やさない選択はどれですか。

- A. CloudWatch のダッシュボードに載せる
- B. EC2 に監視ソフトを入れて自前で構築する
- C. リージョンごとにコンソールを切り替える
- D. Athena で指標をテーブルにして手で集計する

??? success "答えと解説"
    **正解: A**

    CloudWatch のダッシュボードは、複数のリージョンのリソースを 1 つに載せられます。

    - A: 正しい。
    - B: 誤り。管理が増えます。
    - C: 誤り。1 つの画面になりません。
    - D: 誤り。手間が大きく、ダッシュボードになりません。

    **スキル:** [4.2.3](../domain4.md#skill-4-2-3) / **参照:** [ダッシュボード](../../../services/observability.md#dashboards)

### 問11 {#q11}

複数のアカウントのエンドポイントの指標を CloudWatch でまとめ、事業の指標は経営層向けに別に見せます。組み合わせとして適切なものはどれですか。

- A. アカウントごとの IAM ユーザーと、手作りの PDF
- B. Glue のクローラーと Macie
- C. クロスアカウントオブザーバビリティと Amazon Quick
- D. CodeBuild のレポートと Inspector

??? success "答えと解説"
    **正解: C**

    複数のアカウントはクロスアカウントオブザーバビリティで扱います。事業の指標を経営層に見せるなら Amazon Quick です。

    - A: 誤り。自動の集約になりません。
    - B: 誤り。データカタログと機密データの機能です。
    - C: 正しい。
    - D: 誤り。ビルドと脆弱性の情報です。

    **スキル:** [4.2.3](../domain4.md#skill-4-2-3) / **参照:** [ダッシュボード](../../../services/observability.md#dashboards)、[Amazon Quick](../../../services/ai.md#quick)

### 問12 {#q12}

CloudWatch のダッシュボードに Logs Insights のウィジェットを多数置き、10 秒ごとに自動更新すると、料金が増えました。理由と対応はどれですか。

- A. ダッシュボードの閲覧者に課金される。閲覧者を減らす
- B. 更新ごとにクエリが走る。間隔を延ばす
- C. X-Ray のトレースが増える。サンプリングを下げる
- D. ウィジェットは無料だがデータの保存で課金される。保持期間を 0 にする

??? success "答えと解説"
    **正解: B**

    Logs Insights のウィジェットは更新のたびにクエリが走り、料金がかかります。自動更新の間隔を短くしすぎないようにします。

    - A: 誤り。料金の要因はクエリの実行です。
    - B: 正しい。
    - C: 誤り。ウィジェットの更新とは関係ありません。
    - D: 誤り。更新のたびにクエリの料金がかかります。

    **スキル:** [4.2.3](../domain4.md#skill-4-2-3) / **参照:** [ダッシュボードの設定](../../../services/observability.md#dashboard-settings)
