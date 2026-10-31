# 分野5: テスト、検証、トラブルシューティング

配点は **11%** です。評価の仕組みとトラブルシューティングの2タスクがあります。

FM の出力は毎回変わり、正解も 1 つとは限りません。完全一致のテストでは足りないので、どう測り、どこで止めるかを問われます。

## タスク 5.1: 生成 AI の評価システムを実装する {#task-5-1}

### 5.1.1 FM の出力の評価の枠組み {#skill-5-1-1}

従来の ML の精度や再現率だけでは足りません。

| 観点 | 問うこと | Bedrock の指標の例 |
|---|---|---|
| 関連性 | 質問に答えているか | Relevance |
| 事実の正確さ | 正しいか、根拠に沿うか | Correctness、Faithfulness |
| 一貫性 | 矛盾がないか | Coherence |
| 流暢さ | 自然で読みやすいか | ProfessionalStyleAndTone |
| 完全さ | 必要なことをすべて述べたか | Completeness |

BLEU や ROUGE は参照文との比較で、言い換えを低く評価することがあります。意味を見るなら判定モデルや埋め込みの類似度を使います。

詳細: [Bedrock Evaluations](../../services/genai-apps.md#bedrock-evaluations)、[NLP の指標](../../services/ai-fundamentals.md#nlp-metrics)

### 5.1.2 最適な構成を見つけるモデル評価 {#skill-5-1-2}

| 手段 | 使いどころ | 利用者への影響 |
|---|---|---|
| Bedrock Evaluations | 本番の前に複数のモデルを比べる | なし |
| A/B テスト | 本番で 2 案の事業成果を比べる | あり |
| カナリア | 一部のトラフィックで新モデルを試す | 一部 |
| シャドウテスト | 応答を返さず新モデルに流す。SageMaker AI | なし |

| 測るもの | 例 |
|---|---|
| トークンの効率 | 1 件の成功あたりのトークン |
| 遅延と品質の比 | 品質スコアに対する `InvocationLatency` |
| 事業成果 | 解決率、人への引き継ぎ率 |

Bedrock Evaluations の対象は、基盤モデル、Marketplace モデル、カスタムモデル、インポートしたモデル、プロンプトルーターです。

詳細: [Bedrock Evaluations](../../services/genai-apps.md#bedrock-evaluations)、[テスト](../../services/genai-apps.md#testing)、[デプロイとテストの戦略](../../services/sagemaker.md#deployment-strategies)

### 5.1.3 利用者を中心にした評価 {#skill-5-1-3}

| 手段 | 実装 |
|---|---|
| フィードバックの画面 | 評価ボタンを API Gateway と Lambda で受ける |
| 評価の保存 | DynamoDB。応答の ID と結びつける |
| アノテーション | 専門家が応答を採点する。Bedrock の人による評価 |
| 改善への反映 | 低評価の例をゴールデンデータセットやプロンプトの改善に使う |

評価する人は偏ります。不満のある人が多く評価するので、自動の評価と組み合わせます。

!!! note "Ground Truth の状況"
    SageMaker Ground Truth は新規顧客を受け付けていません。試験の対象一覧には載っているので、人がラベル付けや評価を行う仕組みとして役割を押さえます。

詳細: [利用者からの評価](../../services/genai-apps.md#user-feedback)、[Bedrock Evaluations](../../services/genai-apps.md#bedrock-evaluations)、[Ground Truth](../../services/sagemaker.md#ground-truth)

### 5.1.4 品質保証のプロセス {#skill-5-1-4}

| 段階 | 手段 |
|---|---|
| 継続的な評価 | EventBridge のスケジュールで評価を実行 |
| 回帰テスト | プロンプトやモデルの変更時にゴールデンデータセットで比較 |
| 品質ゲート | CodeBuild でスコアを判定し、CodePipeline を止める |

**品質ゲートの例:** 新しいプロンプトで `Faithfulness` が 0.8 未満なら昇格しません。

モデルを変えなくても品質は変わります。文書の更新や利用者の質問の変化があるので、定期の評価も必要です。

詳細: [テスト](../../services/genai-apps.md#testing)、[GenAI ゲートウェイと CI/CD](../../services/genai-apps.md#genai-gateway)、[CodeBuild](../../services/cicd.md#codebuild)、[ステージ条件](../../services/cicd.md#stage-conditions)

### 5.1.5 多面的な評価 {#skill-5-1-5}

| 視点 | 手段 | 強み | 弱み |
|---|---|---|---|
| 自動の指標 | プログラムのジョブ | 安く大量に | 意味を捉えにくい |
| 判定モデル | LLM-as-a-Judge | 意味を採点し、説明も返す | 判定にも費用と誤りがある |
| 人 | 人による評価 | 主観や専門性 | 遅く高い |
| RAG | 取得と生成を分けて採点 | 原因を切り分けられる | 評価データの準備が要る |

実務では、判定モデルで広く見て、結果の分かれるものや重要なものを人が確認します。

詳細: [Bedrock Evaluations](../../services/genai-apps.md#bedrock-evaluations)、[利用者からの評価](../../services/genai-apps.md#user-feedback)

### 5.1.6 取得の品質のテスト {#skill-5-1-6}

| テスト | 手段 |
|---|---|
| 関連性のスコア | `ContextRelevance` |
| 文脈の一致 | `ContextCoverage`。正解に必要な情報を取れたか |
| 取得の遅延 | p95 を測る |

| 結果 | 原因の候補 |
|---|---|
| ContextRelevance が低い | チャンク、埋め込み、検索 |
| ContextCoverage が低い | 取得件数が少ない、文書がない |
| 取得はよいが Faithfulness が低い | プロンプトやモデル |

`Retrieve` を単体で呼べば、生成と切り離して検索だけを確かめられます。

詳細: [RAG の指標](../../services/genai-apps.md#bedrock-evaluations)、[Knowledge Bases を呼ぶ](../../services/ai.md#knowledge-bases)、[運用](../../services/genai-apps.md#vector-operations)

### 5.1.7 エージェントの性能の枠組み {#skill-5-1-7}

| 指標 | 内容 |
|---|---|
| タスク完了率 | 目的を達成した割合 |
| ツールの効果 | 正しいツールと引数か |
| 推論の品質 | 手順は妥当か |
| 効率 | ステップ数、トークン、時間 |

ガイドの「Bedrock Agent の評価」に相当する現在の機能は AgentCore Evaluations です。トレースを LLM-as-a-Judge で採点し、組み込みの評価項目（例: `Builtin.Helpfulness`）を使います。Strands と LangGraph に対応します。

最終的な回答だけを見ると、正しい答えに無駄な手順でたどり着いた場合を見逃します。トレースも評価します。

詳細: [エージェントの評価](../../services/genai-apps.md#agent-evaluation)、[Evaluations と Optimization](../../services/genai-apps.md#agentcore-evaluations)

### 5.1.8 関係者への報告 {#skill-5-1-8}

| 手段 | 向いている相手 |
|---|---|
| CloudWatch ダッシュボード | 運用担当 |
| Quick Sight | 事業の担当、経営層 |
| Managed Grafana | 複数のデータソースを見る技術者 |
| 自動の報告 | EventBridge と Lambda で定期的に集計して SNS で配信 |
| モデルの比較 | 品質、遅延、費用を並べて可視化。評価ジョブの結果を S3 から |

相手ごとに指標を変えます。経営層には技術の指標より、解決率や削減した工数を見せます。

詳細: [監視とオブザーバビリティ](../../services/genai-apps.md#observability)、[Quick Sight](../../services/data-engineering.md#quick-sight)、[Managed Grafana](../../services/operations.md#managed-grafana)、[ダッシュボード](../../services/observability.md#dashboards)、[KPI と ROI](../../services/ai-fundamentals.md#kpi-roi)

### 5.1.9 デプロイの検証 {#skill-5-1-9}

| 検証 | 手段 |
|---|---|
| 合成の利用者の操作 | CloudWatch Synthetics のカナリア |
| ハルシネーション率 | 固定の質問を流して評価する |
| 意味のドリフト | 応答の埋め込みを前の版と比べる |
| 応答の一貫性 | 同じ入力の出力の差分を比べる |
| 自動で戻す | CloudWatch アラームと段階的なデプロイ |

**HTTP の死活監視だけでは足りません。** 200 が返っても、品質が落ちていることがあります。Synthetics のスクリプトで応答の内容も検証します。

詳細: [テスト](../../services/genai-apps.md#testing)、[CloudWatch Synthetics](../../services/operations.md#synthetics)、[AppConfig のロールバック](../../services/secrets.md#appconfig-rollback)

## タスク 5.2: 生成 AI アプリのトラブルシューティング {#task-5-2}

### 5.2.1 内容の処理の問題 {#skill-5-2-1}

| 症状 | 調べるもの | 対応 |
|---|---|---|
| 応答が途中で切れる | `stopReason` が `max_tokens` | `maxTokens` を増やす |
| 文脈の超過 | `model_context_window_exceeded` | 履歴を要約、チャンクを減らす |
| 長い文書の後半が無視される | トークン数、切り捨ての有無 | 分割して処理、文書に合わせたチャンク |
| 埋め込みでエラー | モデルの入力上限 | `maxTokens` を下げる |

`CountTokens` で呼び出しの前に判定します。文書によってチャンクの大きさを変える動的な戦略も有効です。

詳細: [トラブルシューティング](../../services/genai-apps.md#troubleshooting)、[チャンク化の戦略](../../services/genai-apps.md#chunking)、[トークンとコンテキストウィンドウ](../../services/ai-fundamentals.md#tokens)、[クォータ](../../services/ai.md#quotas-detail)

### 5.2.2 FM の統合の問題 {#skill-5-2-2}

| エラー | 主な原因 | 見るところ |
|---|---|---|
| `ValidationException` | 入力形式、データ保持モードの要件 | リクエストの形式 |
| `AccessDeniedException` | IAM、モデル利用の前提、Agents Classic の新規 | 権限、宛先リージョンのモデル |
| `ResourceNotFoundException` | モデル ID の誤り | ID や ARN |
| `ThrottlingException` | クォータ超過 | `InvocationThrottles` |
| `ModelErrorException` | モデルの処理中のエラー | `originalStatusCode` |

**切り分け:** スロットリングは `Invocations` に含まれません。`InvocationThrottles` を見ます。ストリームの途中のエラーは、ループの中の例外処理で受けます。

詳細: [エラー処理とスロットリング](../../services/ai.md#errors-throttling)、[ストリーミング](../../services/ai.md#streaming)、[CloudWatch のメトリクス](../../services/ai.md#bedrock-metrics)、[アクセスの要求と管理](../../services/ai.md#access)

### 5.2.3 プロンプトの問題 {#skill-5-2-3}

| 手法 | 内容 |
|---|---|
| テストの枠組み | 固定の評価データで合格率を測る |
| 版の比較 | Prompt Management のバージョンを同じデータで比べる |
| 体系的な改善 | 1 回に 1 つだけ変えて測る |

複数を同時に変えると、何が効いたか分かりません。悪化したら、まずバージョンを戻してから調べます。

詳細: [プロンプトの管理](../../services/genai-apps.md#prompt-management)、[トラブルシューティング](../../services/genai-apps.md#troubleshooting)、[テスト](../../services/genai-apps.md#testing)

### 5.2.4 検索システムの問題 {#skill-5-2-4}

| 症状 | 原因の候補 | 対応 |
|---|---|---|
| 無関係な文書が返る | チャンクが大きい、検索方式 | ハイブリッド検索、リランク |
| 急に精度が落ちた | 埋め込みモデルの変更、データの変化 | 全データの再埋め込み、ドリフトの監視 |
| 取り込みエラー | `dimension` の不一致 | モデルと索引の次元を揃える |
| 更新が出ない | 同期していない | `StartIngestionJob` |
| フィルターが効かない | `.metadata.json` の名前、`nmslib` | 名前を揃える、`faiss` |
| 表が崩れる | 既定のパーサー | BDA か FM のパーサー |
| 検索が遅い | インデックス、メモリ | HNSW の調整、シャードの見直し |

**切り分け:** `Retrieve` の単体テストで、検索の問題か生成の問題かを分けます。埋め込みの品質は、似た質問と文書のベクトルの距離を調べて確認します。

詳細: [トラブルシューティング](../../services/genai-apps.md#troubleshooting)、[チャンク化の戦略](../../services/genai-apps.md#chunking)、[埋め込みの選び方](../../services/genai-apps.md#embedding-selection)、[メタデータ](../../services/genai-apps.md#kb-metadata)、[運用](../../services/genai-apps.md#vector-operations)

### 5.2.5 プロンプトの保守の問題 {#skill-5-2-5}

| 症状 | 手段 |
|---|---|
| モデルが指示を取り違える | テンプレートのテスト、CloudWatch Logs で実際のプロンプトを確認 |
| どの段階で問題が起きたか不明 | X-Ray で流れを追う |
| 形式の不一致 | スキーマで検証し、失敗を指標にする |
| 繰り返す不具合 | 失敗の例を評価データに加えて、改善を繰り返す |

**シナリオ:** 変数の埋め込みで指示と入力の区切りが崩れると、モデルが入力を指示として読むことがあります。実際に送られたプロンプトを呼び出しログで確認します。

詳細: [トラブルシューティング](../../services/genai-apps.md#troubleshooting)、[構造化出力](../../services/genai-apps.md#structured-output)、[Logs Insights](../../services/observability.md#logs-insights)、[X-Ray](../../services/observability.md#xray)

## 確認問題 {#self-check}

??? question "問1: RAG の評価で ContextRelevance は高いのに、Faithfulness が低いです。どこを直しますか？"
    検索は適切なので、生成の問題です。プロンプトで「文書の内容だけで答える」と指示する、モデルを変える、コンテキストグラウンディングで低いものを止める、などを試します。チャンクや埋め込みを変えても改善しにくい状況です。

??? question "問2: 新しいプロンプトを本番に出す前に、品質の悪化を自動で止めたいです。本番の利用者には影響させません。どう作りますか？"
    CodePipeline の中で CodeBuild からゴールデンデータセットの評価を実行し、`Faithfulness` などのしきい値を下回ったらパイプラインを止めます。判定モデルは Bedrock Evaluations を使えます。A/B テストやカナリアは利用者に影響するので、この段階の答えではありません。

??? question "問3: 文書を更新したのに古い内容で回答します。同期ジョブは成功と表示されています。何を確認しますか？"
    ジョブの統計で、対象の文書が処理されたか、失敗していないかを見ます。ファイルが対象のデータソースの場所にあるか、形式が対応しているかも確認します。`Retrieve` を単体で呼び、新しい内容が返るかで検索と生成を分けます。アプリがキャッシュした回答を返している場合もあるので、セマンティックキャッシュの有無も調べます。

??? question "問4: 埋め込みを Titan Text Embeddings V2 の 1,024 次元から 256 次元に変えたところ、取り込みでエラーになりました。何が問題で、どう進めますか？"
    索引の `dimension` が 1,024 のままで、モデルの次元と一致していません。256 次元の索引を新しく作り、全データを再び埋め込みます。差分の同期では足りません。切り替えの前に、取得の評価で精度の低下を確かめます。古い索引を残して切り替えれば、問題があれば戻せます。

??? question "問5: エージェントが正しい最終回答を返していますが、費用が想定の 5 倍です。最終回答の評価は高いです。何を測りますか？"
    トレースを評価します。ステップ数、ツールの呼び出し回数、不要なツールの利用、トークンを測ります。AgentCore Evaluations でツールの選択や推論の品質を採点します。同じ操作を繰り返しているなら、ツールの説明の見直し、繰り返しの上限を入れます。最終回答だけの評価では、この問題は見えません。

??? question "問6: モデルの更新後も `5xx` は増えていませんが、回答の傾向が変わったとの報告があります。今後これを早く検知するには？"
    CloudWatch Synthetics のカナリアで固定の質問を定期的に流し、応答の内容を検証します。応答の埋め込みを前の版と比べて意味のドリフトを測り、カスタムメトリクスとアラームにします。段階的なデプロイと組み合わせ、アラームで自動で戻します。HTTP の成否だけでは品質の変化は分かりません。
