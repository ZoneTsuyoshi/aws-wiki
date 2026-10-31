# AI サービスと AI 開発ツールの問題集

対象の解説: [AI サービスと AI 開発ツール](../../../services/ai.md)

### 問1 {#q1}

アプリは `Converse` で複数のモデルを呼びます。特定のモデルだけが持つパラメータ `top_k` を指定したいと考えています。最も適切な実装はどれですか。

- A. `inferenceConfig` に `top_k` を追加する
- B. `additionalModelRequestFields` に `top_k` を指定する
- C. `toolConfig` に `top_k` を追加する
- D. `requestMetadata` に `top_k` を追加してモデルへ転送させるようにする

??? success "答えと解説"
    **正解: B**

    `inferenceConfig` の共通の項目は `maxTokens`、`temperature`、`topP`、`stopSequences` です。それ以外のモデル固有の項目は `additionalModelRequestFields` で渡します。

    - A: `inferenceConfig` に定義されていない項目です。
    - B: 正しい実装です。
    - C: ツールの定義の場所です。
    - D: 呼び出しログの絞り込み用のキーと値で、モデルには渡りません。

    **スキル:** C03 1.1.10 / **参照:** [Converse の全パラメータ](../../../services/ai.md#converse-params)

### 問2 {#q2}

`Converse` で `inferenceConfig` を省略し、入力は短いにもかかわらず、呼び出しがすぐ `ThrottlingException` になります。リクエストの数は少なめです。最も可能性の高い原因と対応はどれですか。

- A. `temperature` の既定値がモデルの最大値になり、クォータの予約が増えるので、0 に下げる
- B. `stopSequences` がないので、2,500 個まで追加する
- C. `maxTokens` がモデルの最大値になり、クォータを先に多く予約するので、実態に近づける
- D. クロスリージョン推論が既定で有効なので、無効にする

??? success "答えと解説"
    **正解: C**

    `maxTokens` の既定はモデルの最大値です。リクエストの開始時に「入力トークン + `max_tokens`」が TPM と TPD から差し引かれるので、大きいと同時に処理できる数が減ります。

    - A: `temperature` はクォータの計算に関係しません。
    - B: 停止条件はクォータの予約量を変えません。
    - C: 正しい説明です。
    - D: クロスリージョン推論は、推論プロファイルを指定したときに使うものです。

    **スキル:** C03 1.1.10 / **参照:** [クォータとトークンの数え方](../../../services/ai.md#quotas-detail)

### 問3 {#q3}

出力トークンの消費率が 5 倍のモデルで、入力 1,000 トークン、`max_tokens` 8,000、実際の出力 100 トークンのリクエストを処理しました。正しい説明はどれですか。

- A. 開始時に 41,000 トークンを差し引き、課金も 41,000 トークンである
- B. 開始時に 9,000 トークンを差し引き、最終的な消費は 1,500、課金は 1,100 である
- C. 開始時に 1,100 トークンを差し引き、完了時の消費と課金はどちらも 1,500 トークンである
- D. 開始時には何も差し引かず、完了時に 1,100 トークンを消費する

??? success "答えと解説"
    **正解: B**

    開始時は `入力 + max_tokens = 9,000` です。完了時の消費は `入力 + 出力 × 消費率 = 1,000 + 100 × 5 = 1,500` で、差は戻ります。課金は実トークン数の `1,100` です。

    - A: 開始時の予約に消費率は掛けません。課金も実トークン数です。
    - B: 正しい説明です。
    - C: 開始時の予約と課金を取り違えています。
    - D: 開始時に予約があります。

    **スキル:** C03 1.1.10 / **参照:** [クォータとトークンの数え方](../../../services/ai.md#quotas-detail)

### 問4 {#q4}

`Converse` のツール利用について、正しい説明はどれですか。（2つ選択）

- A. Bedrock がツールを自動で実行し、結果をアプリに返す
- B. `stopReason` が `tool_use` なら、アプリがツールを実行して結果を返す
- C. 結果は `toolResult` で、受け取った `toolUseId` を指定する
- D. `toolChoice` の既定は `any` である
- E. `guardrailConfig` は `toolResult` の内容も評価する

??? success "答えと解説"
    **正解: B, C**

    クライアント側のツール利用では、モデルは実行を要求するだけです。アプリが実行し、同じ `toolUseId` の `toolResult` を次のメッセージで返します。

    - A: `Converse` の通常のツール利用では、アプリが実行します。
    - B: 正しい説明です。
    - C: 正しい説明です。
    - D: 既定は `auto` です。
    - E: `toolResult` は評価されません。必要なら `ApplyGuardrail` を使います。

    **スキル:** C03 1.1.10 / **参照:** [ツール利用の流れ](../../../services/ai.md#tool-use-flow)

### 問5 {#q5}

`ConverseStream` を使うチャットで、請求の集計のために使用トークン数を記録したいと考えています。ストリームのどのイベントから取得すべきですか。

- A. `messageStart`
- B. `contentBlockDelta`
- C. `contentBlockStop`
- D. `metadata`

??? success "答えと解説"
    **正解: D**

    `usage` と `metrics` は最後の `metadata` イベントに含まれます。途中でループを抜けると取得できません。

    - A: 役割だけが入っています。
    - B: テキストの差分が入っています。
    - C: ブロックの終了を示します。
    - D: 正しいイベントです。

    **スキル:** C03 1.1.10 / **参照:** [ストリームのイベント](../../../services/ai.md#stream-events)

### 問6 {#q6}

アプリは EU のお客様のデータを扱い、処理を EU 域内に留める要件があります。一方で、単一リージョンの容量不足も避けたいと考えています。EU リージョンから呼ぶ場合の `modelId` として最も適切なものはどれですか。

- A. `global.` で始まる推論プロファイル
- B. `eu.` で始まる推論プロファイル
- C. `us.` で始まる推論プロファイル
- D. Provisioned Throughput の ARN を推論プロファイルに関連付けたもの

??? success "答えと解説"
    **正解: B**

    地理的な推論プロファイルは、その地理の中のリージョンにルーティングします。EU に留める要件を満たしながら、複数リージョンの容量を使えます。

    - A: 対応する商用リージョン全体に送られるので、データの所在の要件を満たしません。
    - B: 正しい選択です。
    - C: 米国のリージョンへ送られます。
    - D: 推論プロファイルは Provisioned Throughput に対応していません。

    **スキル:** C03 2.3.2 / **参照:** [モデル ID と推論プロファイル](../../../services/ai.md#model-identifiers)

### 問7 {#q7}

推論プロファイル経由で呼ぶロールに、プロファイルの ARN だけを許可したところ、`AccessDeniedException` になりました。最も適切な修正はどれですか。

- A. `bedrock:Converse` アクションを追加する
- B. `aws-marketplace:Subscribe` を拒否する
- C. 宛先の各リージョンの基盤モデルの ARN も許可する
- D. `bedrock:GuardrailIdentifier` の条件を追加する

??? success "答えと解説"
    **正解: C**

    推論プロファイルの呼び出しには、プロファイルと、経路上の各リージョンの基盤モデルの両方の許可が必要です。`bedrock:InferenceProfileArn` の条件で、プロファイル経由に限定できます。

    - A: `Converse` には `bedrock:InvokeModel` を使います。`bedrock:Converse` というアクションはありません。
    - B: 拒否しても、呼び出しの許可は増えません。
    - C: 正しい修正です。
    - D: ガードレールの強制のためのキーで、この問題の解決にはなりません。

    **スキル:** C03 2.3.1 / **参照:** [IAM のスコープ](../../../services/ai.md#iam-scope)

### 問8 {#q8}

数十万件の文書を夜間に要約します。応答はすぐに必要ありません。Bedrock の機能のうち、最も適切なものはどれですか。

- A. `CreateModelInvocationJob` で S3 の JSONL を処理し、EventBridge で完了を受け取る
- B. 1 か月のコミットメントで Provisioned Throughput を購入し、`Converse` で 1 件ずつ順に呼んで保存する
- C. `ConverseStream` を文書の数だけ並列に呼び、結果をアプリから S3 と EventBridge へ順に送る
- D. Provisioned Throughput の ARN を指定したバッチジョブを作る

??? success "答えと解説"
    **正解: A**

    大量で即時性の不要な処理はバッチ推論が適します。入力は S3 の JSONL で、状態の変化は EventBridge で受け取れます。

    - A: 正しい選択です。
    - B: 期間中は削除できず、夜間だけの処理には過剰です。
    - C: スロットリングの原因になります。
    - D: バッチ推論はプロビジョンドモデルに対応していません。

    **スキル:** C03 1.1.10 / **参照:** [スループットの選択肢](../../../services/ai.md#throughput-options)

### 問9 {#q9}

Bedrock のサービスティアの説明として、正しいものはどれですか。（2つ選択）

- A. 指定しないと Standard の層で処理される
- B. `reserved` はオンデマンドのクォータを共有する
- C. Priority の利用には事前の予約が必要である
- D. `flex` は処理時間が長くてもよい処理向けで、割引がある
- E. Provisioned Throughput を購入しないと層を指定できない

??? success "答えと解説"
    **正解: A, D**

    `service_tier` を省略すると Standard です。Flex は割引があり、時間に余裕のある処理向けです。

    - A: 正しい説明です。
    - B: `reserved` の容量はオンデマンドのクォータとは別です。
    - C: Priority は事前の予約が不要です。
    - D: 正しい説明です。
    - E: 層は通常のオンデマンド呼び出しで指定できます。

    **スキル:** C03 1.1.10 / **参照:** [スループットの選択肢](../../../services/ai.md#throughput-options)

### 問10 {#q10}

CloudWatch の `AWS/Bedrock` で、利用者が感じる待ち時間（最初の文字が表示されるまで）を監視したいと考えています。`ConverseStream` を使っています。最も適切なメトリクスはどれですか。

- A. `InvocationLatency`
- B. `InvocationThrottles`
- C. `OutputTokenCount`
- D. `TimeToFirstToken`

??? success "答えと解説"
    **正解: D**

    `TimeToFirstToken` は、リクエストの送信から最初のトークンまでの時間です。

    - A: 最後のトークンまでの全体の時間です。
    - B: スロットリングの件数です。
    - C: 出力量で、時間ではありません。
    - D: 正しいメトリクスです。

    **スキル:** C03 4.3.5 / **参照:** [CloudWatch のメトリクス](../../../services/ai.md#bedrock-metrics)

### 問11 {#q11}

`bedrock-runtime` の呼び出しログを有効にします。監査の要件で、本文は S3 に残さず、ログの絞り込みにテナントを使いたいと考えています。実装の組み合わせとして最も適切なものはどれですか。

- A. Guardrails の `ANONYMIZE` を有効にして、ログをそのまま保存する
- B. `textDataDeliveryEnabled` を `false` にし、`requestMetadata` にテナントを入れる
- C. `textDataDeliveryEnabled` を `true` にし、`additionalModelRequestFields` にテナントを入れる
- D. ログを無効のままにして、`usage` をアプリの標準出力へ書く

??? success "答えと解説"
    **正解: B**

    `LoggingConfig` の `textDataDeliveryEnabled` で、テキストの記録を制御します。`requestMetadata` は呼び出しログの絞り込みに使えるキーと値です。

    - A: 呼び出しログの入力は、ガードレールが介入しても元のままです。
    - B: 正しい実装です。
    - C: 本文が残り、`additionalModelRequestFields` はモデルに渡す値です。
    - D: 呼び出しログを有効にするという前提を満たしません。

    **スキル:** C03 2.3.5 / **参照:** [モデル呼び出しログ](../../../services/ai.md#invocation-logging)

### 問12 {#q12}

ガードレールの設定について、正しい説明はどれですか。（2つ選択）

- A. 正規表現の機密情報フィルターは、先読みと後読みに対応しない
- B. 拒否トピックは 1 ガードレールに最大 30 件である
- C. コンテンツフィルターの `ANONYMIZE` で不適切な語をマスクできる
- D. ワードフィルターの 1 項目は 10 語まで指定できる
- E. コンテキストグラウンディングの `threshold` には 1.0 を設定できる

??? success "答えと解説"
    **正解: A, B**

    カスタムの正規表現は lookaround に対応しません。拒否トピックの上限は 30 件です。

    - A: 正しい説明です。
    - B: 正しい説明です。
    - C: `ANONYMIZE` は機密情報フィルターだけの機能です。
    - D: 1 項目は 3 語までです。
    - E: 範囲は 0〜0.99 です。

    **スキル:** C03 2.3.3 / **参照:** [ポリシーごとの設定](../../../services/ai.md#guardrail-policy-settings)

### 問13 {#q13}

検索結果を根拠に回答するアプリで、根拠にない情報を含む応答をブロックしたいと考えています。ガードレールのどの設定が最も適切ですか。

- A. `PROMPT_ATTACK` の `inputStrength` を `HIGH` にする
- B. `MISCONDUCT` の `outputStrength` を `HIGH` にする
- C. `GROUNDING` の `threshold` を設定し、ソースとクエリを渡す
- D. 拒否トピックに「根拠のない情報」を定義する

??? success "答えと解説"
    **正解: C**

    コンテキストグラウンディングの `GROUNDING` は、応答がソースに基づいているかをスコアにします。しきい値を下回るとブロックします。ソース、クエリ、対象の応答の 3 つが必要です。

    - A: 入力の攻撃の検出で、応答の根拠は見ません。
    - B: 犯罪行為などの有害な内容の検出です。
    - C: 正しい設定です。
    - D: 話題の検出であり、根拠の有無の検証ではありません。

    **スキル:** C03 2.3.3 / **参照:** [ポリシーごとの設定](../../../services/ai.md#guardrail-policy-settings)

### 問14 {#q14}

本番のアプリの `guardrailConfig` に `guardrailVersion: "DRAFT"` を指定しています。開発者がコンソールで編集すると、そのまま本番の動作が変わってしまいます。最も適切な対応はどれですか。

- A. `CreateGuardrailVersion` で版を作り、番号を指定する
- B. ガードレールの ARN にバージョンの ARN を指定した IAM ポリシーで編集を止める
- C. `trace` を `disabled` にする
- D. `streamProcessingMode` を `async` にする

??? success "答えと解説"
    **正解: A**

    `DRAFT` は作業中の版です。番号付きの版はスナップショットなので、編集の影響を受けません。

    - A: 正しい対応です。
    - B: 編集の権限を絞っても、本番が `DRAFT` を参照する状態は変わらず、版の固定になりません。
    - C: トレースの有無で、適用される版は変わりません。
    - D: ストリームの評価のタイミングの設定です。

    **スキル:** C03 2.3.3 / **参照:** [バージョン](../../../services/ai.md#guardrail-versions)

### 問15 {#q15}

Knowledge Bases の `Retrieve` で、最大 10 件を、メタデータの `dept` が `support` のチャンクだけから検索したいと考えています。指定する設定の組み合わせはどれですか。（2つ選択）

- A. `vectorSearchConfiguration.numberOfResults` を 10 にする
- B. `vectorSearchConfiguration.filter` に `equals` で `dept` を指定する
- C. `inferenceConfig.maxTokens` を 10 にする
- D. `overrideSearchType` を `support` にする
- E. `sessionId` を `support` にする

??? success "答えと解説"
    **正解: A, B**

    件数は `numberOfResults`（既定 5、1〜100）で、メタデータの条件は `filter` で指定します。

    - A: 正しい設定です。
    - B: 正しい設定です。
    - C: 生成のトークンの上限で、検索の件数ではありません。
    - D: 値は `HYBRID` か `SEMANTIC` です。
    - E: セッションの識別子で、検索対象を絞りません。

    **スキル:** C03 1.1.10 / **参照:** [Knowledge Bases のパラメータ](../../../services/ai.md#kb-params)

### 問16 {#q16}

プライベートサブネットのアプリから、インターネットを経由せず `Converse` を呼びます。セキュリティの担当者は、特定のロールが特定のモデルだけ呼べるように、経路でも絞りたいと考えています。最も適切な構成はどれですか。

- A. `com.amazonaws.<region>.bedrock` のエンドポイントとセキュリティグループ
- B. `com.amazonaws.<region>.bedrock-runtime` のエンドポイントとエンドポイントポリシー
- C. S3 のゲートウェイエンドポイントとバケットポリシー
- D. NAT ゲートウェイとスコープダウンしたセキュリティグループ

??? success "答えと解説"
    **正解: B**

    `Converse` は `bedrock-runtime` の API です。エンドポイントポリシーは既定でフルアクセスなので、プリンシパルとアクションとモデルを絞ります。

    - A: `bedrock` はコントロールプレーンです。
    - B: 正しい構成です。
    - C: S3 の通信にしか効きません。
    - D: インターネット経由の経路が残ります。

    **スキル:** C03 2.3.2 / **参照:** [VPC エンドポイントでの接続](../../../services/ai.md#privatelink)

### 問17 {#q17}

AgentCore Runtime で動くエージェントで、利用者が 30 分おきに質問するたびに、メモリ上の会話の文脈が失われます。既定の設定のままです。適切な対応はどれですか。（2つ選択）

- A. `idleRuntimeSessionTimeout` を延ばす
- B. 会話の内容を AgentCore Memory に保存する
- C. 呼び出しごとに新しい `runtimeSessionId` を発行する
- D. `maxLifetime` を 900 秒に短くする
- E. Bedrock の `requestMetadata` に履歴を入れる

??? success "答えと解説"
    **正解: A, B**

    既定のアイドルの制限は 900 秒（15 分）で、停止すると microVM は破棄され、メモリも消えます。アイドルの時間を伸ばすか、文脈を Memory に残します。

    - A: 正しい対応です。
    - B: 正しい対応です。
    - C: 新しいセッションになり、問題が悪化します。
    - D: セッションをさらに短くします。
    - E: ログの絞り込み用で、エージェントの記憶にはなりません。

    **スキル:** C03 2.3.4 / **参照:** [AgentCore の構成要素と設定](../../../services/ai.md#agentcore-components)

### 問18 {#q18}

AgentCore Gateway に AWS の IAM 認証で接続するクライアントのポリシーに、必ず含めるアクションはどれですか。

- A. `bedrock:InvokeAgent`
- B. `bedrock:InvokeModel`
- C. `bedrock-agentcore:InvokeGateway`
- D. `lambda:InvokeFunction`

??? success "答えと解説"
    **正解: C**

    IAM の受信認可では、呼び出し側に `bedrock-agentcore:InvokeGateway` が必要です。リソースは作成したゲートウェイに絞ります。

    - A: Bedrock Agents Classic の呼び出しです。
    - B: モデルの推論の権限です。
    - C: 正しいアクションです。
    - D: Lambda のターゲットへの送信はゲートウェイ側の認可の話で、クライアントの権限ではありません。

    **スキル:** C03 2.3.4 / **参照:** [AgentCore の構成要素と設定](../../../services/ai.md#agentcore-components)

### 問19 {#q19}

Kiro のワークスペースで、テストのファイルを扱うときだけ読み込まれる規約を Steering で書きたいと考えています。ファイル先頭の YAML として最も適切なものはどれですか。

- A. `inclusion: always`
- B. `inclusion: manual`
- C. `inclusion: fileMatch` と `fileMatchPattern: "**/*.test.ts"`
- D. `inclusion: auto` と `fileMatchPattern: "**/*.test.ts"`

??? success "答えと解説"
    **正解: C**

    `fileMatch` は、指定のパターンのファイルを扱うときに読み込みます。

    - A: すべてのやり取りで読み込みます。
    - B: `#ファイル名` で指定したときだけ読み込みます。
    - C: 正しい指定です。
    - D: `auto` は `name` と `description` で判定するモードです。

    **スキル:** C03 1.1.9 / **参照:** [Steering の読み込みモード](../../../services/ai.md#steering-modes)

### 問20 {#q20}

開発チームは Kiro の Hook で、エージェントがファイルを保存したときに `npx eslint --fix` を実行するように設定しました。動作の説明として正しいものはどれですか。

- A. 開発者がエディターで手で保存したときも実行される
- B. `action.type` を `command` にすると、エージェントのクレジットを消費する
- C. コマンドのタイムアウトの既定は 60 秒である
- D. 設定は `.kiro/settings/mcp.json` に書く

??? success "答えと解説"
    **正解: C**

    コマンドのタイムアウトの既定は 60 秒で、`timeout` の 0 で無効にできます。

    - A: ファイルのトリガーは、エージェントの変更にだけ反応します。
    - B: クレジットを消費するのは `agent` のアクションです。
    - C: 正しい説明です。
    - D: Hook は `.kiro/hooks/` の JSON です。`mcp.json` は MCP の設定です。

    **スキル:** C03 1.1.9 / **参照:** [Hooks の設定](../../../services/ai.md#hooks-settings)
